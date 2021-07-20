# encoding: utf-8

import multiprocessing, time, socket, select, threading, xmlrpclib, os, platform
from htp import htp_task, get_nw4_val
from database import DB
from esl_init import get_config
import esl_init
import urllib2, json, Queue

def start(task_data):
	'''
	启动绑定进程并返回进程对象
	'''
	proc = multiprocessing.Process(target = process, args =
				(task_data,))
	proc.start()
	return proc

#通过把抢上传的json字段和数据库中的字段名字不一致，因此需要转译
tran_word = {"ESLID":"eslid", "Name":"salesname","Unicode":"salesno", "Oprice":"oldprice","bsid":"apid", "bsip" : "apip"}

def filed_transfer_in(data):
	"数据格式转换，入参是json格式的字节流，返回值是python格式的字典列表。"
	for item in tran_word:
		data = data.replace(item, tran_word[item])

	data = eval(data, {}, {})

	for item in data:
		#if item.has_key('eslid'):
		if 'eslid' in item:
			eslid = item['eslid'].strip().upper()
			item['eslid'] = eslid[0:2] + '-' + eslid[2:4] + '-' + eslid[4:6] + '-99'
		if 'salesno' in item:
			item['salesno'] = item['salesno'].strip().upper()
		if 'apid' in item:
			item['apid'] = item['apid'].strip().upper()

		if item.has_key('bak'):
			item.pop('bak')
		
	return data

def filed_transfer_out(data):
	"数据格式转换，入参是python格式的字典列表, 返回值为json格式的字节流。"

	for item in data:
		for k in item.keys():
			if item[k] == None:
				item.pop(k)
		if item.has_key('eslid'):
			eslid = item['eslid'].strip().lower()
			item['eslid'] = eslid.replace('-', '')[0:6]
		if 'salesno' in item:
			item['salesno'] = item['salesno'].strip().lower()
		if 'apid' in item:
			item['apid'] = item['apid'].strip().lower()
		if item.has_key('salesname'):
			item['salesname'] = item['salesname'].encode('gb2312','ignore')
	
	s = '['
	c = ''
	for item in data:
		c += '{'
		for id1 in item:
			c += '"' + id1 + '":' + '"' + item[id1] + '",'
		c = c[0:-1] + '},'
	s = s + c[0:-1] + ']'

	for item in tran_word:
		s = s.replace(tran_word[item], item)

	#sales_list和ap_list会被双引号括起来，导致语法错误
	if '"[' in s:
		s = s.replace('"[', '[')
		s = s.replace(']"',']')

	return s
	
def filed_transfer_out_unicode(data):
	"数据格式转换，入参是python格式的字典列表, 返回值为json格式的字节流。"

	for item in data:
		for k in item.keys():
			if item[k] == None:
				item.pop(k)
		if item.has_key('eslid'):
			eslid = item['eslid'].strip().lower()
			item['eslid'] = eslid.replace('-', '')[0:6]
		if 'salesno' in item:
			item['salesno'] = item['salesno'].strip().lower()
		if 'apid' in item:
			item['apid'] = item['apid'].strip().lower()

	s = '['
	c = ''
	for item in data:
		c += '{'
		for id1 in item:
			c += '"' + id1 + '":' + '"' + item[id1] + '",'
		c = c[0:-1] + '},'
	s = s + c[0:-1] + ']'

	for item in tran_word:
		s = s.replace(tran_word[item], item)

	return s

def find_head_of_package(data):
	return data.find('[') - 5

def unpack_data(data, xmlserver):
	'''
	解包程序，将socket数据去掉包头，提取json字段转成python对象，发给xml-rpc服务进行处理
	并返回xml-prc调用的返回值
	'''
	if 'DATASTART' not in data or 'DATAEND' not in data:
		esl_init.log.error("in data valid:%s" % data)

	if 'DATASTART' in data and 'DATAEND' in data:
		n = find_head_of_package(data)
		data = data[n:-12]
		cmd = int(data[0:2])

		cmd_dict = {1 : "bind", 9 :"SALES_QUERY", 10 : "SALES_UPDATA_FOR_GAN", \
			8 : "UNBIND", 50 : "AP_BEACOM", 60: "GANG_BEACOM", 99 : "EXIT",
			11 : "ESL_REFRESH", 12 : "ESL_QUERY", 13 : "AP_QUERY", 
			14 : "AP_LIST", 15 : "SALES_LIST",
			20 : "ESL_FAILED_LIST", 25 : "AP_FAILED_LIST",51:"HEART_BEAT",
            52 : 'ECHO'}

		#return xmlserver.send_cmd(cmd_dict[cmd], filed_transfer_in(data[5:-1]))
		retry_times = 0
		max_retry_times = 5
		while retry_times < max_retry_times:
			try:
				if cmd == 51:
					trans_data = json.loads(data[5:-1])
				else:
					trans_data = filed_transfer_in(data[5:-1])
				ret, ok_list = xmlserver.send_cmd(cmd_dict[cmd], trans_data)
				break
			except xmlrpclib.Fault as err:
				esl_init.log.error('Fault: Code %s, String %s' %(err.faultCode, err.faultString))
			except xmlrpclib.ProtocolError as err:
				esl_init.log.error('ProtocolError: headers : %s, Code %s, Msg %s'\
						%(err.headers, err.errcode, err.errmsg))
			except socket.error,e:
				esl_init.log.error('socket error occourred! %s' % e)
			except KeyError,e:
				esl_init.log.error('KeyError, %s'%e)
			except Exception, e:
				esl_init.log.error('Other Error : %s' % e)
			finally:
				retry_times += 1
		
		if retry_times >= max_retry_times:
			ret = "FAILED"
			ok_list = [{"bak":""}]
			esl_init.log.error("unpack_data send_cmd exception: (%d, %s)" % (cmd, cmd_dict[cmd]))
		
		return ret, ok_list

def send_exit():
	ip = '127.0.0.1'
	port = int(get_config('extend_service', 'bind_listen_port', '8800'))
	sock = socket.create_connection((ip, port))
	sock.sendall('DATASTART00000000000099001[{"exit":""}]0X0000DATAEND')
	sock.close()

def pack_data(data, ok_list):
	'''
	打包程序，将xml-prc的返回值转译成字字节流，并加上包头。
	'''
	s = filed_transfer_out(ok_list).replace("'", '"')
	s = s.replace(" ", "")
	n = find_head_of_package(data)
	n1 = n + 2
	return data[0:n] + '02' + data[n1:(n1+3)]+ s + '0x0000DATAEND'

def query_salesno(salesno, salesno_not_valid):
	'''
	向服务器查询商品信息，如果服务器返回商品不存在则将其写入salesno_not_valid
	如果存在，则将商品写入到商品数据表中
	'''
	xmlserver = xmlrpclib.ServerProxy("http://127.0.0.1:9000", allow_none=True)
	ack = xmlserver.send_cmd("SALES_QUERY_FOR_TEST", salesno)
	if ack['bak'] == "00":
		ack.pop('bak')
		db = DB()
		db.list_updata(db.sales, [ack])
	else:
		salesno_not_valid.append(salesno)

def recv_all_data(sd):
	inputs = [sd]
	outputs = []
	total_data=[]
	while True:
		timeout = 0.5
		readable, _,  _ = select.select(inputs, outputs, inputs, timeout)
		if not readable:
			break
		data = sd.recv(10240)
		if data:
			total_data.append(data)
		else:
			break

	return ''.join(total_data)

def get_esl_info_opener():
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	top_level_url = get_config('idsystem', 'url', "https://127.0.0.1:9082")
	username = get_config('idsystem', 'username', 'hanshowidsystem')
	password = get_config('idsystem', 'password', 'hanshowidsystem')

	if 'https' in top_level_url:
		password_mgr.add_password(None, top_level_url, username, password)
	else:
		password_mgr.add_password(None, top_level_url, None, None)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

	return opener

def check_eslid_exist(bind_request, db):
	en = get_config('idsystem', 'enable', 'no').upper()
	if en != "YES":
		return

	opener = None
	top_level_url = get_config('idsystem', 'url', "https://127.0.0.1:9082")
	timeout = int(get_config('idsystem', 'timeout', '3'))
	idlist = [bind_request['eslid'] for bind_request in bind_request]
	for id1 in idlist:
		try:
			id1 = id1.upper()
			is_exist = db.get_one(db.esl, id1)
			if not is_exist:
				if opener == None:
					opener = get_esl_info_opener()
				info = opener.open(top_level_url + "/" + str(id1), timeout = timeout).read()
				info = json.loads(info)
				if info:
					info['bak'] = '00'
					db.list_updata(db.esl, [info])
					esl_init.log.debug("get esl infor: %s" % info)
		except Exception, e:
			esl_init.log.error("get esl %s infor failed: %s" % (id1, e))

def bind_thread(conn, addr, xmlserver):
	'''
	处理单个把抢的连接请求，这是一个线程，入参为socket层accept函数返回值
	线程将从conn中读取数据，解析并执行任务后返回数据。
	线程只读取一次最多2K的数据，读取超时为5秒。之后将断开链接，结束线程。
	'''
	conn.setblocking(0)
	inputs = [conn]
	outputs = []
	timeout = 5
	retn = None
	try:
		readable, _,  _ = select.select(inputs, outputs, inputs, timeout)
		if not readable:
			esl_init.log.error("recv timeout from %s" % repr(addr))
		else:
			data = recv_all_data(conn)
			esl_init.log.debug("<<<:%s" % data)
			retn, ok_list = unpack_data(data, xmlserver)
			ret = pack_data(data, ok_list)
			try:
				conn.sendall(ret)
				esl_init.log.debug(">>>:%s" % ret.decode("gb2312",'ignore'))
			except Exception, e:
				conn.sendall(ret.encode("gb2312",'ignore'))
				esl_init.log.debug(">>>:%s" % ret.encode("gb2312",'ignore'))
	finally:
		if retn == 'FAILED':
			raise KeyError,"unpack_data error"
		conn.close()

def get_xmlserver():
	#绑定数据通过webservice进行更新
	ip_port = "http://127.0.0.1:%s" % (
		get_config('extend_service', 'xml_rpc_port', '9000'))
	return xmlrpclib.ServerProxy(ip_port, allow_none=True)

def get_javaserver():
	ip_port = "http://%s:%s/shop-web/stationHandler" % (
		get_config('system', 'parent_ip', '192.168.1.11'),
		get_config('syste,', 'parent_xml_rpc_port', '8888'))
	return xmlrpclib.ServerProxy(ip_port, allow_none=True)

def is_esl_register(data):
	if 'DATASTART51000' in data:
		return True
	return False

esl_register_buf = []
esl_register_buf_len = 0
def append_esl_register(data, fetch):
	global esl_register_buf
	global esl_register_buf_len

	d = data[15:-14]
	if esl_register_buf_len == 100 or fetch == True:
		esl_register_buf_len = 0
		v = 'DATASTART51000[' + ','.join(esl_register_buf) + ']0X0000DATAEND'
		esl_register_buf = []
		return True, v
	else:
		esl_register_buf_len += 1
		esl_register_buf.append(d)
		return False, ''

def udp_networking(q,server):
	while True:
		try:
			data = ''
			try:
				data = q.get(timeout=1) #阻塞取数据
			except Queue.Empty, e:
				if esl_register_buf_len > 0:
					flag, v = append_esl_register(data, True)
					esl_init.log.error("aaaaa5:%s" % v)
					_, ok_list = unpack_data(v, server)
			else:
				if is_esl_register(data):
					flag, v = append_esl_register(data, False)
					if flag == True:
						esl_init.log.error("aaaaa5:%s" % v)
						_, ok_list = unpack_data(v, server)
				else:
					_, ok_list = unpack_data(data, server)

		except Exception,e:
			esl_init.log.error(" udp_networking Error %s!"%e)
			server = get_xmlserver()
			time.sleep(1)

def tcp_networking(q,server):
	while True:
		try:
			conn, client_address = q.get(1)#阻塞取数据
			bind_thread(conn, client_address, server)
		except Exception,e:
			esl_init.log.error(" tcp_networking Error %s!"%e)
			server = get_xmlserver()
			time.sleep(1)

def filter_CMD(data):
	l = ['51','52']
	if data[9:11] in l:
		return True
	return False
			
def check_bind_listen_alive():
	try:
		#TCP 8800 isalive
		port = int(get_config('extend_service', 'bind_listen_port', '8800'))
		val = 'DATASTART13001[{"apid":"0", "apip":"", "status":""}]0X0000DATAEND'
		sock = socket.create_connection(('127.0.0.1', port))
		sock.sendall(val)
		ret = sock.recv(2048)
		sock.close()

		#UDP 8800 isalive
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		val = 'DATASTART51001[{}]0X0000DATAEND'
		sock.sendto(val, ('127.0.0.1', port))
		sock.close()

		return True
	except Exception, e:
		esl_init.log.error("check_bind_listen_alive failed:%s" % e)
		return False

def check_ap_timeout(db, ap_timeout, server, javaserver):
	from xmlserver import reply_ack

	offline_ap_list = db.refresh_ap_online_status(ap_timeout)
	if offline_ap_list:
		esl_init.log.error("ap beacom timeout:%s" % offline_ap_list)
		#发送一个虚假的价签注册信息，强制更新绑定表
		esl_info = []
		for ap in offline_ap_list:
			for id1 in db.get_ap_bind_esl_list(ap['apid']):
				#beacom_in_queue.put(id1) #不再触发漫游
				esl_info.append({"eslid":id1, "apid":ap['apid']})
		server.send_cmd("AP_TIMEOUT", esl_info)
		reply_ack("AP_STATUS", offline_ap_list, javaserver)

def ap_beacom_thread_fun(task_data,q):
	import Queue

	esl_init.log.info("bind_process starting for beacom")
	RECV_BUF_SIZE = 10*1024*1024
	conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	conn.setsockopt(socket.SOL_SOCKET , socket.SO_BROADCAST , 1)
	try:
		conn.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)
		r_bufsize = conn.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
		esl_init.log.debug("set socket max_buf  %d"%(r_bufsize))
	except Exception,e:
		esl_init.log.error('socket %s' %e)

	ip = ""
	port = int(get_config('extend_service', 'bind_listen_port', '8800'))
	conn.bind((ip, port))

	ap_timeout = int(get_config('system', 'ap_heardbeat_time', '300'))

	conn.setblocking(0)
	inputs = [conn]
	outputs = []
	timeout = 5
	db = DB()
	out_queue = task_data['bind']['out_queue']
	beacom_in_queue = task_data['beacom']['in_queue']
	
	server = get_xmlserver()
	javaserver = get_javaserver()
	while True:
		try:
			readable, _,  _ = select.select(inputs, outputs, inputs, timeout)
			if not readable:

				while not out_queue.empty():
					(ids, ret) = out_queue.get() 
					#db.remove_key(db.bind, ids)  #解绑请求, 成功也挪到core层实时处理
					#esl_init.log.info("unbind for %s" % ids)
				check_ap_timeout(db, ap_timeout, server, javaserver)
			else:
				data, addr = conn.recvfrom(10240)
				esl_init.log.debug("<<<:%s" % data)
				if not filter_CMD(data):
					_, ok_list = unpack_data(data, server)
					ret = data[0:9] + '02' + data[11:14]+ ok_list + '0x0000DATAEND'
					conn.sendto(ret, addr)
					esl_init.log.debug(">>>:%s" % ret.decode("gb2312"))
					check_ap_timeout(db, ap_timeout, server, javaserver)
				else:
					q.put(data,1)
							
		except socket.error, e:
			pass
		except Exception, e:
			esl_init.log.error( "bind process beacom:%s" % e)
			server = get_xmlserver()
			javaserver = get_javaserver()

	

def process(task_data):
	'''
	绑定进程主任务，监听8800端口，等待连接请求，对每个连接将创建一个线程进行服务。
	'''
	from main import main_is_exist
	if platform.system() == 'Windows':
		import mmap
		mm = mmap.mmap(-1,1024,access=mmap.ACCESS_WRITE, tagname='share_mmap')
	else:
		mm = None
	esl_init.log.info("bind_process starting")
	import Queue
	q = Queue.Queue()
	q_tcp = Queue.Queue()
	ap_beacom_thread = threading.Thread(target = ap_beacom_thread_fun, args=(task_data,q))
	ap_beacom_thread.start()
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0) # 非阻塞
	ip = ""
	port = int(get_config('extend_service', 'bind_listen_port', '8800'))
	server.bind((ip, port))
	server.listen(5)
	
	inputs = [server]
	outputs = []
	server_timeout = 3

	conn = None
	xmlserver = get_xmlserver()
	'''
	udp_networking 主要负责基站的UDP心跳，价签心跳通过q转发给tcp_networking处理
	ap_beacom_thread 主要处理TCP的基站心跳信息
	'''

	try:
		udp_network = threading.Thread(target = udp_networking, args=(q,xmlserver))
		tcp_network = threading.Thread(target = tcp_networking, args=(q_tcp,xmlserver))
		udp_network.start()
		tcp_network.start()
	except Exception ,e:
		esl_init.log.error("tc(ud)p_networking: %s "%e)

	try:
		while True:
			readable, _, _ = select.select(inputs, outputs, inputs, server_timeout)
			if readable:
				conn, client_address = server.accept()
				q_tcp.put((conn, client_address))

			if not main_is_exist(task_data['ppid'],mm):
				break
			for th1 in [ap_beacom_thread, udp_network, tcp_network]:
				if not th1.is_alive():
					esl_init.log.error("bind thread is not alive")
					break
	except Exception, e:
		esl_init.log.error( "bind process:%s" % e)
	finally:
		for th1 in [ap_beacom_thread, udp_network, tcp_network]:
			th1.join(timeout=5)

	if conn:
		conn.close()
	server.close()

def action(groups):
	'''
	负责处理一组价签绑定后的操作（更新），传入参数格式为(apid, chn, nw1, [ids,...])
	入参为一组ID
	返回格式为 [(id, ack), (id, ack),...]
	'''
	#绑定关系已经写入数据库，只需要发起更新，而且不需要记录结果,直接返回即可
	#??是不是需要更新价签的最后通讯时间??
	db = DB()
	_, _, _, ids, _, _, _ = groups
	#nw4_val 值为 段码价签，点阵价签2.0、2.4、2.9、4.3
	nw4_val = get_nw4_val(db, ids[0])
	#作为解绑用
	return htp_task(groups, nw4_val, "UNBIND")
	
