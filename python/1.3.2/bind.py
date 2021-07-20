# encoding: utf-8

import multiprocessing, time, socket, select, threading, xmlrpclib, os, platform
from htp import htp_task, get_nw4_val
from database import DB
from esl_init import conf, log
import esl_init
import urllib2, json

def start(task_data):
	'''
	启动绑定进程并返回进程对象
	'''
	#proc = multiprocessing.Process(target = process, args = (task_data,))
	proc = threading.Thread(target = process, args = (task_data,))
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
			item['eslid'] = item['eslid'].strip().upper()
			#item['eslid'] = eslid[0:2] + '-' + eslid[2:4] + '-' + eslid[4:6] + '-99'
		if 'salesno' in item:
			item['salesno'] = item['salesno'].strip().upper()
		if 'apid' in item:
			item['apid'] = item['apid'].strip().upper()

		if item.has_key('bak'):
			item.pop('bak')
		
	return data

def filed_transfer_out_v2(data):
	for item in data:
		for k in tran_word:
			if tran_word[k] in item:
				item[k] = item.pop(tran_word[k])
	return json.dumps(data)

def filed_transfer_out(data):
	"数据格式转换，入参是python格式的字典列表, 返回值为json格式的字节流。"

	for item in data:
		for k in item.keys():
			if item[k] == None:
				item.pop(k)
		if item.has_key('eslid'):
			eslid = item['eslid'].strip().lower()
			item['eslid'] = eslid
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

	s = s.replace(" ", "")
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
		esl_init.log.error_msg("in data valid:%s" % data, errid='EBI001')

	if 'DATASTART' in data and 'DATAEND' in data:
		n = find_head_of_package(data)
		data = data[n:-12]
		cmd = int(data[0:2])

		cmd_dict = {1 : "bind", 9 :"SA,,LES_QUERY", 10 : "SALES_UPDATA_FOR_GAN", \
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
					trans_data = json.loads(data[data.index('['):(data.rindex(']') +1)])
				else:
					trans_data = filed_transfer_in(data[data.index('['):(data.rindex(']') +1)])
				ret, ok_list = xmlserver.send_cmd(cmd_dict[cmd], trans_data)
				break
			except xmlrpclib.Fault as err:
				esl_init.log.error_msg('Fault: Code %s, String %s' %(err.faultCode, err.faultString), errid='EBI002')
				time.sleep(retry_times)
			except xmlrpclib.ProtocolError as err:
				esl_init.log.error_msg('ProtocolError: headers : %s, Code %s, Msg %s'\
						%(err.headers, err.errcode, err.errmsg), errid='EBI003')
				time.sleep(retry_times)
			except socket.error,e:
				esl_init.log.error_msg('socket error occourred! %s' % e, errid='EBI004')
				time.sleep(retry_times)
			except KeyError,e:
				esl_init.log.error_msg('KeyError, %s'%e, errid='EBI005')
			except Exception, e:
				esl_init.log.debug('Error: %s, %s' % (e, trans_data))
			finally:
				retry_times += 1
		
		if retry_times >= max_retry_times:
			ret = "FAILED"
			ok_list = [{"bak":""}]
			esl_init.log.error_msg("unpack_data send_cmd exception: (%d, %s)" % 
					(cmd, cmd_dict[cmd]), errid='EBI006')
		
		return ret, ok_list

def send_exit():
	ip = '127.0.0.1'
	port = int(conf.extend_service.bind_listen_port)
	sock = socket.create_connection((ip, port))
	sock.sendall('DATASTART99001[]0X0000DATAEND')
	sock.close()

def pack_data(data, ok_list):
	'''
	打包程序，将xml-prc的返回值转译成字字节流，并加上包头。
	'''
	#s = filed_transfer_out(ok_list).replace("'", '"')
	s = filed_transfer_out_v2(ok_list)
	n = find_head_of_package(data)
	n1 = n + 2
	return data[0:n] + '02' + data[n1:(n1+3)]+ s + '0x0000DATAEND'

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
	top_level_url = conf.idsystem.url
	username = conf.idsystem.username
	password = conf.idsystem.password

	if 'https' in top_level_url:
		password_mgr.add_password(None, top_level_url, username, password)
	else:
		password_mgr.add_password(None, top_level_url, None, None)

	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

	return opener

def check_eslid_exist(bind_request, db):
	en = conf.idsystem.enable.upper()
	if en != "YES":
		return

	opener = None
	top_level_url = conf.idsystem.url
	timeout = int(conf.idsystem.timeout)
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
			esl_init.log.warning("get esl %s infor failed: %s" % (id1, e))

def bind_thread(conn, addr, xmlserver):
	'''
	处理单个把抢的连接请求，这是一个线程，入参为socket层accept函数返回值
	线程将从conn中读取数据，解析并执行任务后返回数据。
	线程只读取一次最多2K的数据，读取超时为5秒。之后将断开链接，结束线程。
	'''
	conn.setblocking(0)
	inputs = [conn]
	outputs = []
	timeout = 3
	retn = None
	try:
		readable, _,  _ = select.select(inputs, outputs, inputs, timeout)
		if not readable:
			esl_init.log.warning("recv timeout from %s" % repr(addr))
		else:
			data = recv_all_data(conn)
			esl_init.log.debug("<<<:%s" % data)
			retn, ok_list = unpack_data(data, xmlserver)
			retn = retn.upper()
			if retn != 'FAILED':
				ret = pack_data(data, ok_list)
			else:
				ret = 'DATASTART02001[]0X0000DATAEND'
			try:
				conn.sendall(ret)
				esl_init.log.debug(">>>:%s" % ret.decode("utf8",'ignore'))
			except Exception, e:
				conn.sendall(ret.encode("gb2312",'ignore'))
				esl_init.log.debug(">>>:%s" % ret.encode("gb2312",'ignore'))
	finally:
		if retn == 'FAILED':
			raise KeyError,"unpack_data error"
		conn.close()

class TimeoutTransport(xmlrpclib.Transport):

    def __init__(self, timeout, use_datetime=0):
        self.timeout = timeout
        # xmlrpclib uses old-style classes so we cannot use super()
        xmlrpclib.Transport.__init__(self, use_datetime)

    def make_connection(self, host):
        connection = xmlrpclib.Transport.make_connection(self, host)
        connection.timeout = self.timeout
        return connection

class TimeoutServerProxy(xmlrpclib.ServerProxy):

    def __init__(self, uri, timeout=10, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
        t = TimeoutTransport(timeout)
        xmlrpclib.ServerProxy.__init__(self, uri, t, encoding, verbose, allow_none, use_datetime)

def get_xmlserver():
	#绑定数据通过webservice进行更新
	ip_port = "http://127.0.0.1:%s" % (
		conf.extend_service.xml_rpc_port)
	return TimeoutServerProxy(ip_port, timeout = 5, allow_none=True)

def get_javaserver():
	if conf.system.parent_url:
		ip_port = conf.system.parent_url
	else:
		ip_port = "http://%s:%s/shop-web/stationHandler" % (
			conf.system.parent_ip, conf.system.parent_xml_rpc_port)
	return TimeoutServerProxy(ip_port, allow_none=True)

def udp_networking(task_data, q,server):
	from xmlserver import reply_ack
	import heartbeat
	import Queue

	esl_init.log.info("0.1 udp_networking starting")
	T = task_data
	db = DB()

	while True:
		try:
			data = q.get(timeout = 1)#阻塞取数据
			if "DATASTART51000" in data:
				trans_data = json.loads(data[data.index('['):(data.rindex(']') +1)])
				bind_list, online_status = heartbeat.esl_register(db, trans_data, T['esl_info'], \
					T['esl_power_info'], T['esl_power_his'],\
					T['esl_level_change_count'], T['ap_work_time'], T['threading_event'],\
					T['esl_power_last_time'])
				if bind_list:
					server.send_cmd("BIND", bind_list)
				if online_status:
					reply_ack("ESL_HB_STATUS", online_status, None)
			else:
				_, ok_list = unpack_data(data, server)
		except Queue.Empty, e:
			pass
		except KeyboardInterrupt, e:
			break
		except Exception,e:
			server = get_xmlserver()
			time.sleep(1)
		finally:
			if task_data['isquit']['bind']:
				break

	esl_init.log.info("0.1 udp_networking exit")

def tcp_networking(task_data, q, server):
	import Queue

	esl_init.log.info("0.2 tcp_networking starting")
	while True:
		try:
			conn, client_address = q.get(timeout=1)#阻塞取数据
			bind_thread(conn, client_address, server)
		except Queue.Empty, e:
			pass
		except KeyboardInterrupt, e:
			break
		except Exception,e:
			server = get_xmlserver()
			time.sleep(1)
		finally:
			if task_data['isquit']['bind']:
				break
	esl_init.log.info("0.2 tcp_networking exit")

def filter_CMD(data):
	l = ['51','52']
	if data[9:11] in l:
		return True
	return False
			
def check_bind_listen_alive():
	try:
		#TCP 8800 isalive
		port = int(conf.extend_service.bind_listen_port)
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
		esl_init.log.error_msg("check_bind_listen_alive failed:%s" % e, errid='EBI007')
		return False

def check_ap_timeout(db, ap_timeout, server, javaserver):
	from xmlserver import reply_ack

	offline_ap_list = db.refresh_ap_online_status(ap_timeout)
	if offline_ap_list:
		esl_init.log.warning("ap beacom timeout:%s" % offline_ap_list)
		#发送一个虚假的价签注册信息，强制更新绑定表
		esl_info = []
		for ap in offline_ap_list:
			for id1 in db.get_ap_bind_esl_list(ap['apid']):
				#beacom_in_queue.put(id1) #不再触发漫游
				esl_info.append({"eslid":id1, "apid":ap['apid']})
		server.send_cmd("AP_TIMEOUT", esl_info)
		reply_ack("AP_STATUS", offline_ap_list, javaserver)

def ap_beacom_thread_fun(task_data, q):
	import Queue

	esl_init.log.info("0.3 ap_beacom_thread starting")
	RECV_BUF_SIZE = 10*1024*1024
	conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	conn.setsockopt(socket.SOL_SOCKET , socket.SO_BROADCAST , 1)
	try:
		conn.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)
		r_bufsize = conn.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
		esl_init.log.debug("set socket max_buf  %d"%(r_bufsize))
	except Exception,e:
		esl_init.log.warning('socket %s' %e)

	ip = ""
	port = int(conf.extend_service.bind_listen_port)
	conn.bind((ip, port))


	conn.setblocking(0)
	inputs = [conn]
	outputs = []
	timeout = 2
	db = DB()
	out_queue = task_data['bind']['out_queue']
	beacom_in_queue = task_data['beacom']['in_queue']
	
	server = get_xmlserver()
	javaserver = None
	skipn = 0

	while True:
		try:
			readable, _,  _ = select.select(inputs, outputs, inputs, timeout)
			if task_data['isquit']['bind']:
				break
			ap_timeout = int(conf.system.ap_heardbeat_time)
			if not readable:
				while not out_queue.empty():
					(ids, ret, sid) = out_queue.get() 
				if time.time() - task_data['startup_time'] >= ap_timeout:
					check_ap_timeout(db, ap_timeout, server, javaserver)
				continue

			data, addr = conn.recvfrom(10240)
			esl_init.log.debug("<<<:%s" % data)
			if not filter_CMD(data):
				_, ok_list = unpack_data(data, server)
				ret = data[0:9] + '02' + data[11:14]+ ok_list + '0x0000DATAEND'
				conn.sendto(ret, addr)
				esl_init.log.debug(">>>:%s" % ret.decode("gb2312"))
				if time.time() - task_data['startup_time'] >= ap_timeout:
					check_ap_timeout(db, ap_timeout, server, javaserver)
				continue

			if skipn > 0:
				skipn -= 1
				continue

			try:
				q.put_nowait(data)
			except Queue.Full, e:
				esl_init.log.error_msg("heardbeat message q out of 100W, skip next 1W messaage", errid='EBI008')
				skipn = 10000
							
		except socket.error, e:
			pass
		except KeyboardInterrupt, e:
			break
		except Exception, e:
			esl_init.log.error_msg( "bind process beacom:%s" % e, errid='EBI009')
			server = get_xmlserver()
	
	try:
		conn.shutdown(socket.SHUT_RDWR)
	except socket.error:
		pass
	conn.close()
	esl_init.log.info("0.3 ap_beacom_thread exit")

def process(task_data):
	'''
	绑定进程主任务，监听8800端口，等待连接请求，对每个连接将创建一个线程进行服务。
	'''
	esl_init.log.info("bind_process starting")
	import Queue
	q_tcp = Queue.Queue()
	ap_beacom_thread = threading.Thread(target = ap_beacom_thread_fun, args=(task_data, task_data['bind_udp_q']))
	ap_beacom_thread.start()
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(0) # 非阻塞
	ip = ""
	port = int(conf.extend_service.bind_listen_port)
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
		udp_network = threading.Thread(target = udp_networking, args=(task_data, task_data['bind_udp_q'], xmlserver))
		tcp_network = threading.Thread(target = tcp_networking, args=(task_data, q_tcp, xmlserver))
		udp_network.start()
		tcp_network.start()
	except Exception ,e:
		esl_init.log.error_msg("tc(ud)p_networking: %s "%e, errid='EBI010')

	try:
		while True:
			readable, _, _ = select.select(inputs, outputs, inputs, server_timeout)
			if readable:
				conn, client_address = server.accept()
				q_tcp.put((conn, client_address))

			if task_data['isquit']['bind']:
				break
			for th1 in [ap_beacom_thread, udp_network, tcp_network]:
				if not th1.is_alive():
					raise KeyError, "bind thread is exist"
	except Exception, e:
		esl_init.log.error_msg( "bind process:%s" % e, errid='EBI011')
		
	for th1 in [ap_beacom_thread, udp_network, tcp_network]:
		th1.join()

	if conn:
		conn.close()
	server.close()

	esl_init.log.info("bind_process exit")

def action(groups):
	'''
	负责处理一组价签绑定后的操作（更新），传入参数格式为(apid, chn, nw1, [ids,...])
	入参为一组ID
	返回格式为 [(id, ack), (id, ack),...]
	'''
	#绑定关系已经写入数据库，只需要发起更新，而且不需要记录结果,直接返回即可
	#??是不是需要更新价签的最后通讯时间??
	#db = DB()
	_, _, _, ids, _, _, _, _, db = groups
	#nw4_val 值为 段码价签，点阵价签2.0、2.4、2.9、4.3
	nw4_val = get_nw4_val(db, ids[0])
	#作为解绑用
	return htp_task(groups, nw4_val, "UNBIND")
	
