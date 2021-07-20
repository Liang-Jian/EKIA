# encoding: utf-8

from bind import filed_transfer_out_unicode, get_javaserver
from bind import check_eslid_exist, get_xmlserver, send_exit
from database import DB
from esl_init import set_config, log
import esl_init, htp, api20, pprint, netlink, heartbeat, updata, errno, uuid 
from netlink import save_netlink_buf, get_bind_nw1_nw3, get_bind_nw1_nw3_3g, bind_list_init, load_and_set_netlink_data_to_db
from netlink import get_old_para

from SimpleXMLRPCServer import SimpleXMLRPCServer
import time, multiprocessing, os, Queue, threading, sys, socket, platform, xmlrpclib, random
import cPickle as pickle
from string import atof
from copy import deepcopy
from esl_init import conf, print_except

def is_esl_rf_ok(item):
	eslid = str(item["eslid"]).upper().strip()
	wakeupid = str(item["nw1"]).upper().strip()
	channel = item["nw3"]
	setchn = int(item.get("setchn", channel))
	grpchn = int(item.get("grpchn", channel))

	try:
		e1 = eslid.split('-')
		n1 = wakeupid.split('-')
		if len(e1) == 4  and len(n1) == 4 and int(''.join(e1), 16) and int(''.join(n1), 16) and \
			(0 < int(channel) < 256) and (0 < int(setchn) < 256) and (0 < int(grpchn) < 256):
			pass
		else:
			raise KeyError, 'netlink para error'
	except Exception, e:
		esl_init.log.warning("esl info error: %s, %s, %s, %s, %s" % (eslid, wakeupid, channel, setchn, grpchn))
		return False

	return True

def is_esl_info_ok(db, eslid):
	i = db.get_all_info(db.esl, eslid)
	
	if not i:
		return False
	if None in [i['nw1'], i['nw3'], i['nw4'], i['op2'], i['op3']]:
		return False
	
	if not is_esl_rf_ok(i):
		return False

	return True

def get_unbind_temp(info):
	if info['nw4'] == 'NORMAL':
		return 'UNBIND'

	op5 = eval(info['op5'], {}, {})
	temp = "unbind-" + str(op5.get('resolution_x', '')) + str(op5.get('resolution_y', ''))\
				+ '-' + op5.get('color', 'black')
	return temp.replace('--', '-')

def is_list(args):
	if not args:
		return False

	for t in [list, tuple, dict]:
		if isinstance(args, t): 
			return True
	return False

def list_all_type(db, args):
	if not is_list(args):
		return
   
	if isinstance(args, list):
		for x in args:
			list_all_type(db, x)
   
	if isinstance(args, dict):
		for k in args:
			if is_list(args[k]):
				list_all_type(db, args[k])
			else:
				if args[k] == None:
					args[k] = "None"

def get_all_esl_list(db, item):
	id_list = []
	if "esllist" not in item:
		id_list = db.get_sales_bind_esl_list(item['salesno'])
	else:
		for ids in item.get("esllist", []):
			id_list.append(ids.get("eslid", None))
	
	return id_list

def get_all_info(db, id1, cmd):
	esl_info = db.get_all_info(db.esl, id1)
	bind_info = db.get_all_info(db.bind, id1)

	bind_info.pop('status', None)
	salesno = bind_info.get('salesno', None)
	apid = bind_info.get('apid', None)
	ap_info = db.get_all_info(db.ap, apid)
	ap_info.pop('status', None)
	ap_info.pop('version', None)

	sales_info = db.get_all_info(db.sales, salesno)
	sales_info.pop('salesno', None)
	sales_info.pop('status', None)
	
	info = {}
	info.update(esl_info)
	info.update(bind_info)
	info.update(ap_info)
	info.update(sales_info)

	info['data_cmd'] = cmd

	return info

def select_netid(db, nw1, nw3, ids):
    # f -> {'nw1+nw3' : [netid1,netid2...]} allready sorted
	f = db.get_nw1_nw3_group()
	d = {}
	i = 0
	_ids = ids[:]
	while (i<1000):
		if i not in f[nw1+nw3]:
			if len(_ids) != 0:
				x = _ids.pop()
				d[x] = i
			else:
				break
		i += 1
	return d

def esl_status_has_changed(eslid, ret, db):
	if htp.ack_ok(ret):
		status = 'online'
	elif htp.ack_low_power(ret):
		#status = 'lowpower'
		status = 'error' #上面需要这个值
	elif ret != 0:
		status = 'offline'
	else:
		status = 'offline'

	_, old_status = db.get_last_status(db.esl, eslid)
	if old_status == 'lowpower':
		old_status = 'error'	#比较用

	return True if status != old_status else False, status

def get_esl_status(esl1, db):
	esl_status = db.get_one(db.esl, esl1)['status']

	if esl_status == 'offline':
		status = "offline"
	elif esl_status == 'lowpower':
		status = "lowpower"
	elif esl_status == "waiting":
		status = "waiting"
	elif esl_status == "online":
		status = "online"
	else:
		status = "offline"

	return status

def is_xmlserver_alive():
	try:
		xml_server = get_xmlserver()
		xml_server.send_cmd("ECHO", [])
		return True
	except Exception, e:
		esl_init.log.error_msg("xmlserver is not alive:%s" % e, errid='EXM001')
		return False

def is_java_alive(xmlserver):
	try:
		ret = xmlserver.stationHandler.send_cmd("HELLO", [{}])
		if ret == 'OK':
			return True
	except Exception, e:
		return False

def resend_failed_msg():
	failed_msg = []
	try:
		with open("log/failed_msg.pkl", "r") as f:
			failed_msg = pickle.load(f)
			
	except Exception, e:
		pass

	for (cmd, val) in failed_msg:
		reply_ack(cmd, val, None)

	with open("log/failed_msg.pkl", "w") as f:
		pickle.dump([], f)

def save_reply_failed_msg(cmd, val):
	failed_msg = []
	try:
		with open("log/failed_msg.pkl", "r") as f:
			failed_msg = pickle.load(f)

	except Exception, e:
		pass
	
	if (cmd, val) not in failed_msg:
		failed_msg.append((cmd, val))
		with open("log/failed_msg.pkl", "w") as f:
			pickle.dump(failed_msg, f)
			

def cmd_updata_ack_filter(db, val):
	for item in val:
		try:
			if len(item['ack']) == 1:
				eslid = item['ack'][0]['eslid']
				if "@%s" % eslid in item['sid']:
					item['eslid'] = eslid
			n1 = item['sid'].rindex("@")
			item['sid'] = item['sid'][0:n1]
		except Exception, e:
			pass

def reply_ack_thread(task_data):
	'''
	反馈消息给服务器，包括提交基站状态，提交价签状态，提交绑定状态，提交解绑状态,
	反馈更新结果，提交价签信息，提交门店心跳信息
	'''

	esl_init.log.info("0.4 reply_ack thread starting")
	server = get_javaserver()
	db = DB()

	while True:
		
		cmd, val = None, None
		try:
			cmd, val = reply_ack_q.get(timeout=1)
		except Queue.Empty, e:
			pass
		finally:
			if task_data['isquit']['xmlserver']:
				break

		if cmd == None:
			continue

		list_all_type(db, val)

		if cmd == 'UPDATA_ACK':
			cmd_updata_ack_filter(db, val)

		skip = False
		if cmd in conf.system.uplink_cmd_block_list or conf.system.parent_enable.lower() == 'no':
			skip = True

		if cmd not in ['AP_STATUS', 'ESL_STATUS', 'ESL_HB_STATUS', "ESL_HB_REALTIME"]:
			esl_init.log.info("reply_ack%s: %s,%s;%s" , '[S]' if skip else '', cmd, len(val), val)
		else: #基站心跳的esl_init.log.为debug级别，要不能太多了
			esl_init.log.debug("reply_ack%s: %s,%s;%s" , '[S]' if skip else '', cmd, len(val), val)

		if skip:
			continue

		n = 0
		try_max = 5

		while n <= try_max:
			try:
				n += 1
				if server.stationHandler.send_cmd(cmd, val).upper() == 'OK':
					break
			except xmlrpclib.Fault as e:
				esl_init.log.error("EXM002:Code %s, string %s" % (e.faultCode, e.faultString))
				break
			except Exception, e:
				esl_init.log.error('EXM003:reply_ack error: %s, retry %s' % (e, n))
				for j in xrange(n):
					time.sleep(1)
					if task_data['isquit']['xmlserver']:
						n = try_max +1
						break
				server = get_javaserver()
		
		if n > try_max:
			save_reply_failed_msg(cmd, val)

		del val

	esl_init.log.info("0.4 reply_ack thread exit")

reply_ack_q = None
def reply_ack(cmd, val, notuse, pri= 5):
	if (cmd not in ['RESEND_UPDATE']) and (val == [{}] or val == []):
		return
	reply_ack_q.put((cmd, val), pri)

def thread_return_(args, server):
	'''整包返回数据,挡板用'''
	ret = [{"salesno": item['salesno'], "status":random.choice(["OK","failed", "invalid"]), "sid":item['sid'], "ack":[{"eslid":"12-34-56-78", "status":"online"}]} for item in args]
	reply_ack("UPDATA_ACK", ret, server)

def thread_return(val, server):
	'''门店挡板程序'''
	threading.Thread(target=thread_return_, args=(val, server)).start()

def check_zero(updata_ack, server): 
	'''如果一个都不能更新则发送空报文给上层'''
	for item in updata_ack:
		if item['bak'] == "00":
			return
	reply_ack("UPDATA_ACK", [{"salesno" : "", "status" : "failed", "sid" : updata_ack[0]['sid']}], server)

def check_index(args):
	if "start_index" not in args:
		args['start_index'] = "0"
	if "end_index" not in args:
		args['end_index'] = str(int(args['start_index']) + 20)
	if int(args['end_index']) < int(args['start_index']):
		args['end_index'] = str(int(args['start_index']) + 20)

	return int(args['start_index']), int(args['end_index'])+1

def set_esl_priority(db, salesno, eslid, esl_priority):
	if eslid:
		esl_priority[eslid] = 1

	try:
		try:
			salesno_old = db.get_one(db.bind, eslid)['salesno']
		except Exception, e:
			salesno_old = None
		salesno_new = salesno_old
		if salesno != None:
			salesno_new = salesno

		for sn in [salesno_old, salesno_new]:
			if sn:
				esl_list = db.get_sales_bind_esl_list(sn)
				for id1 in esl_list:
					esl_priority[id1] = 1
	except Exception, e:
		esl_init.log.warning("set esl priority failed: %s" % e)

last_wait_for_proc = {}

def save_wait_for_proc(wait_for_proc):
	global last_wait_for_proc

	if last_wait_for_proc == wait_for_proc:
		return

	try:
		with open("log/wait_for_proc.pkl", "w") as f:
			pickle.dump(wait_for_proc, f)
	except Exception, e:
		pass
	
	last_wait_for_proc = deepcopy(wait_for_proc)

def load_wait_for_proc():
	#缓存待处理的解绑和绑定请求
	try:
		with open("log/wait_for_proc.pkl", "r") as f:
			wait_for_proc = pickle.load(f)
	except Exception, e:
		wait_for_proc = {"UNBIND":{}, "BIND":{},'WAIT_UNBIND':{}}	

	return wait_for_proc


class ExampleService:
	'''
	xml-prc服务，对外提供send_cmd函数，cmd值有SALES_UPDATA,BIND,UNBIND,SALES_QUERY服务
	'''
	updating_esl_list = [] # 用来记录当前正在更新的价签
	sales_ack_list = {} #用来记录当前正在更新的商品对应的所有价签ACK值
	salesno_not_valid = [] #用来保存服务器返回的商品信息不存在的列表

	def __init__(self, task_data):
		self.updata_in_queue = task_data['updata']['in_queue']
		self.updata_buf_in_queue = task_data['updata']['buf_in_queue']
		self.updata_out_queue = task_data['updata']['out_queue']
		self.bind_in_queue = task_data['bind']['in_queue']
		self.query_in_queue = task_data['query']['in_queue']
		self.beacom_in_queue = task_data['beacom']['in_queue']
		self.beacom_out_queue = task_data['beacom']['out_queue']
		self.netlink_in_queue = task_data['netlink']['in_queue']
		self.netlink_data = task_data['netlink']['rf_para']
		self.javaserver = None
		self.wait_for_proc = load_wait_for_proc()	#缓存待处理的解绑和绑定请求
		self.ap_level = task_data['ap_level']
		self.esl_power_info = task_data['esl_power_info']
		self.esl_power_his = task_data['esl_power_his']
		self.esl_level_change_count = task_data['esl_level_change_count']

		self.parent_enable = False if conf.system.parent_enable.lower() == 'no' else True
		self.esl_info = task_data['esl_info']
		self.esl_priority = task_data['esl_priority']
		self.db = DB()
		self.g = bind_list_init(self.db)
		self.ap_work_time = task_data['ap_work_time']

		self.last_ack_time = 0
		self.all_info = task_data['all_info']
		self.update_dict = task_data['updata']['updata_dict']
		self.e_flag = task_data['threading_event']
		self.apset = task_data['apset'] # set_list.ini
		self.api_version = '1.2.1'
		self.task_data = task_data

	def get_updating_esl_list(self, db, args):
		return "OK", self.updating_esl_list

	def clear_updating_esl_list(self, db, args):
		if self.updating_esl_list:
			self.updating_esl_list = []
		return "OK", self.updating_esl_list

	def sales_updata_for_gan(self, db, args):
		#把枪只能上传一条记录

		esl_list = db.get_sales_bind_esl_list(args[0]['salesno'])

		for id1 in esl_list:
			if db.is_esl_busy(id1):
				esl_init.log.warning("%s in busy, cancel this job of %s" % (id1, args[0]['salesno']))
				args[0]['bak'] = '04'
				return 'OK', args

		if not db.has_key(db.sales, args[0]['salesno']):
			args[0]['bak'] = "03"
		else:
			args[0]['sid'] = "only-for-hander:%07d" % random.randint(1,1000000) + '@' +str(uuid.uuid1())
			#使用新接口
			self.updata_buf_in_queue.put(args)
			set_esl_priority(db, args[0]['salesno'], None, self.esl_priority) #设置高优先级
			for item in args:
				item['bak'] = "00"
				item['ack'] = item['bak']
		
		return 'OK', args
	
	def sales_updata_db(self, db, args):
		esl_init.log.info("sales_updata_db: %s; %s" % (len(args), args))
		for ids in args:
			ids['bak'] = '00'
		thread_return(args, self.javaserver)
		return 'OK', args
	
	def update_bind_list(self, db, id1, item):
		if not db.has_key(db.sales, item['salesno']):
			db.list_updata(db.sales, [item])
		if not db.has_key(db.bind, id1):
			bind_request = [{"eslid":id1, "apid":"-1", "salesno":item['salesno']}]
			self.bind(db, bind_request)
		else:
			bind_info = db.get_all_info(db.bind, id1)
			#绑定关系不对
			if str(bind_info['salesno']) != str(item['salesno']):
				bind_request = [{"eslid":id1, "apid":bind_info['apid'], "salesno":item['salesno']}]
				self.bind(db, bind_request)

	def esl_update(self, db, args):
		esl_init.log.info("esl_update: %s; %s" % (len(args), args))
		#一直缓存数据
		for item in args:
			if 'eslid' not in item:
				item['bak'] == '02' #key不存在
				continue

			item['bak'] = "00"
			if 'sid' not in item:
				item['sid'] = 'nosid'
			item['oldsid'] = item['sid']
			if 'salesno' not in item:
				item['salesno'] = 'nosalesno' + item['eslid']
				item['salesno'] = item['salesno'].upper()
			item['sid'] = item['sid'] + '@' + str(item["eslid"]) + '-' + str(uuid.uuid1())

			all_info = {}

			id1 = item["eslid"]
			self.update_bind_list(db, id1, item)
			all_info[id1] = get_all_info(db, id1, "CMD_UPDATE")

			i = deepcopy(item)
			if 'template' in i:
				i['esllist'] = [{"eslid":id1, "template":i['template']}]
			else:
				i['esllist'] = [{"eslid":id1}]

			self.updata_buf_in_queue.put(([i], all_info))

		#再恢复
		for item in args:
			item['sid'] = item['oldsid']
			if 'oldsid' in item:
				item.pop("oldsid")
		return "OK", args

	def sales_updata_buf(self, db, args):
		esl_init.log.info("sales_updata_buf: %s; %s" % (len(args), args))
		#一直缓存数据
		for item in args:

			item['bak'] = "00"
			if 'sid' not in item:
				item['sid'] = 'nosid'
			item['oldsid'] = item['sid']
			if "salesno" not in item:
				item['salesno'] = 'nosalesno' + item['eslid']
				item['salesno'] = item['salesno'].upper()
			item['sid'] = item['sid'] + '@' + str(item["salesno"]) + '-' + str(uuid.uuid1())

			all_info = {}

			id_list = get_all_esl_list(db, item)
			for id1 in id_list: 
				self.update_bind_list(db, id1, item)
				all_info[id1] = get_all_info(db, id1, "CMD_UPDATE")
			i = deepcopy(item)
			self.updata_buf_in_queue.put(([i], all_info))

		#再恢复
		for item in args:
			if 'oldsid' in item:
				item['sid'] = item.pop('oldsid')
		return "OK", args
	
	def bind_to_default(self, db, eslid, info):
		if not db.has_key(db.sales, '0'):
			db.list_updata(db.sales, [{"salesno":"0"}])

		if eslid in self.esl_power_info:
			best_ap = heartbeat.get_best_ap(db, eslid, self.esl_power_info[eslid], self.ap_work_time)
			best_ap = "9"
			if best_ap:
				esl_init.log.warning("find available ap %s for esl %s", best_ap, eslid)
				info.update(db.get_all_info(db.ap, best_ap))
				info['salesno'] = '0'
				return True
		
		esl_init.log.warning("can't find available ap for esl %s", eslid)
		return False

	def bind(self, db, args):
		esl_init.log.info("bind request(%s);%s" % (len(args), args))
		valid_list, sales_query_list, esl_active_list = [], [], []
		bind_key, esl_list = {}, []

		for item in args:
			eslid = item.get('eslid', None)
			apid = item.get('apid', None)
			salesno = item.get('salesno', None)
			item['bak'] = '00'
			if not eslid:
				item['bak'] = '01'
			if not salesno:
				item['bak'] = '01'
			item['eslid'] = eslid.upper()

			if (not db.has_key(db.esl, eslid)) or (not is_esl_info_ok(db, eslid)):
				item['bak'] = '02'
			if not db.has_key(db.sales, salesno):
				db.list_updata(db.sales, [{"salesno":salesno}])
				#item['bak'] = '06' #商品待查询
				sales_query_list.append({"salesno":salesno})
			if (not apid) or (int(apid) == -1):
				if eslid not in self.esl_power_info:
					esl_init.log.warning("eslid %s not any bind ap information" % (eslid))
					item['apid'] = '-1'
					item['bak'] = '05'
					continue
				best_ap = heartbeat.get_best_ap(db, eslid, self.esl_power_info[eslid], self.ap_work_time)
				if not best_ap:
					esl_init.log.warning("retry to find best ap for eslid %s failed" % (eslid))
					item['apid'] = '-1'
					item['bak'] = '05'
					continue
				item['apid'] = str(best_ap)
				esl_init.log.info("eslid %s try to bind ap %s" % (eslid, best_ap))		
			if not db.has_key(db.ap, item['apid']):
				item['bak'] = '05'
			
			if item['bak'] == '00':
				valid_list.append(item)
				e = {"eslid":item['eslid']}
				if 'extESLID' in item:
					e['exteslid'] = item['extESLID']
				if 'template' in item:
					e['template'] = item['template']
				if len(e) >= 2:
					esl_list.append(e)

		has_bind_list  = get_old_para(db, args)
		check_eslid_exist(args, db) #获取价签信息
		db.list_updata(db.bind, valid_list)
		db.list_updata(db.esl, esl_list)
		net = []

		for item in valid_list:
			eslid = item['eslid']
			set_esl_priority(db, item['salesno'], eslid, self.esl_priority) #设置高优先级
			#拼接绑定报文
			esl_info = db.get_all_info(db.esl, eslid)
			esl_info.update(db.get_all_info(db.bind, eslid))
			esl_info['status'] = 'online'
			for k in esl_info.keys():
				if esl_info[k] == None:
					esl_info.pop(k, None)

			if "not_active" not in item:
				esl_active_list.append(esl_info)
			if "not_netlink" in item:
				continue #不需要进行组网
			#拼接组网报文
			if 'HS_EL_5300' == esl_info['op3']:
				is_netlink_3g, nw1, nw3, setchn, grpchn = \
					get_bind_nw1_nw3_3g(db, item['eslid'], item['apid'], self.g, has_bind_list, self.apset)
				if is_netlink_3g:
					net.append({"eslid":item['eslid'], "nw1":nw1, "nw3":nw3, "setchn":setchn, "grpchn":grpchn})
			else:
				is_netlink, nw1, nw3, setchn, grpchn = \
					get_bind_nw1_nw3(db, item['eslid'], item['apid'], self.g, has_bind_list)
				if is_netlink:
					net.append({"eslid":item['eslid'], "nw1":nw1, "nw3":nw3, "setchn":setchn, "grpchn":grpchn})
			
		if net: #进行组网
			self.esl_netlink(db, net)

		reply_ack("SALES_QUERY", sales_query_list, self.javaserver)
		reply_ack("ESL_ACTIVE", esl_active_list, self.javaserver, pri = 2) #每次绑定都发送一次价签信息给上层

		return "OK", args

	def bind_status_ack(self, db, args):
		esl_init.log.info("recv bind_status_ack: %s" % args)
		return "OK"

	def unbind_status_ack(self, db, args):
		esl_init.log.info("recv unbind_status_ack: %s" % args)
		return "OK"
	
	def esl_refresh(self, db, args):
		esl_init.log.info("esl_refresh %s" % args)
		for item in args:
			item['bak'] = "00"
		return "OK", args

	def esl_active_ack(self, db, args):
		esl_init.log.info("esl_active_ack: %s" % args)
		return "OK"

	def esl_recover(self, db, args):
		esl_init.log.info("recv esl_recover: %s" % args)
		esl_list, bind_list, query_list = [], [], []
		for item in args:
			one_esl_list = {}
			one_bind_list = {}
			for key in db.table_column[db.esl]:
				if key in item:
					one_esl_list[key] = item[key]
			for key in db.table_column[db.bind]: 
				if key in item:
					one_bind_list[key] = item[key]
			esl_list.append(one_esl_list)
			if 'salesno' in one_bind_list and 'apid' in one_bind_list \
				and one_bind_list['salesno'] != "" and one_bind_list['salesno'] != None \
				and one_bind_list['apid'] != "" and one_bind_list['apid'] != None:

				bind_list.append(one_bind_list)
				query_list.append({"salesno": one_bind_list['salesno']})

		db.list_updata(db.esl, esl_list)
		db.list_updata(db.bind, bind_list)
		heartbeat.is_man_updata(args, self.esl_info)
		reply_ack("SALES_QUERY", query_list, self.javaserver)
		return "OK"

	def bind_recover(self, db, args):
		return 'OK', db.list_updata(db.bind, args)

	def unbind(self, db, args):
		esl_init.log.info("unbind request(%s);%s" % (len(args), args))
		valid_list = []
		for item in args:
			#检查ID
			eslid = item.get("eslid", None)
			if not eslid:
				item['bak'] = '02'
				continue
			eslid = eslid.upper()
			
			if (not db.has_key(db.bind, eslid)) or (not is_esl_info_ok(db, eslid)):
				item['bak'] = '02'
				continue
			
			info = get_all_info(db, eslid, "CMD_UPDATE")
			valid_list.append(item)

			try:
				self.g[info['apid']][info['op3']][info['nw1']][info['nw3']] -= 1
			except KeyError, e:
				pass

			item['bak'] = '00'
			unbind_temp = info.get('template', None)
			if not unbind_temp:
				unbind_temp = get_unbind_temp(info)
			up_buf = [{"sid":"only-for-handler:%07d" % random.randint(1,1000000),\
					"salesno":info['salesno'], "priority":"9",\
					"esllist":[{"eslid":eslid, "template":unbind_temp}]}] #启用解绑模板
			self.sales_updata_buf(db, up_buf) 

			db.remove_key(db.bind, eslid) #删除绑定关系
			
			set_esl_priority(db, None, item['eslid'], self.esl_priority) #设置高优先级
		
		reply_ack("UNBIND_STATUS", valid_list, self.javaserver) #发送解绑报文
		return "OK", args
	
	def sales_query_ack(self, db, args):
		esl_init.log.info("sales_query_ack : %s" % args)
		for item in args[:]:
			if item['bak'] != "00":
				args.remove(item)
				self.salesno_not_valid.append(item['salesno'])
		ok_list = db.list_updata(db.sales, args)
		return "OK"

	def sales_query(self, db, args):
		esl_init.log.info( "sales_query request : %s" % args)
		query_list = []
		for item in args:
			if not item.get('salesno', None):
				item['bak'] = '03'
				continue
			salesno = item['salesno'].strip()
			item['bak'] = '03'
			if db.has_key(db.sales, salesno):
				salesinfo = db.get_all_info(db.sales, salesno)
				for field in item:
					if field != 'bak' and field in salesinfo:
						item[field] = salesinfo[field]
				item['bak'] = '00'
			else:
				item['bak'] = '06'
				query_list.append({'salesno':item['salesno']})
		reply_ack("SALES_QUERY", query_list, self.javaserver)
		return "OK", args
	
	def sales_del(self, db, args):
		for item in args:
			item['bak'] = '00'
			if not item.get('salesno', None):
				item['bak'] = '03'
		db.list_del(db.sales, args)
		for sales in args:
			if sales['bak'] == '01':
				sales.update({'bak': '06'})
		return 'OK', args
	
	def esl_beacom(self, db, args):
		for ids in args:
			ids['bak'] = '02'
			eslid = ids["eslid"].upper().strip()
			if db.has_key(db.bind, eslid):
				ids['bak'] = '00'
				self.beacom_in_queue.put(eslid)

		return 'OK', args

	def esl_query_realtime(self, db, args):
		for ids in args:
			eslid = ids["eslid"].upper().strip()
			ids['bak'] = '02'
			if (not db.has_key(db.esl, eslid)) or (not is_esl_info_ok(db, eslid)):
				esl_init.log.warning("query %s status failed, not in database" % eslid)
				continue
				
			if db.has_key(db.bind, eslid):
				esl_init.log.info("query %s status" % eslid)
				info = get_all_info(db, eslid, "CMD_QUERY")
				self.query_in_queue.put((eslid, info))
				ids['bak'] = '00'
			else:
				info = get_all_info(db, eslid, "CMD_QUERY")
				ret = self.bind_to_default(db, eslid, info)
				if ret:
					esl_init.log.info("query %s status" % eslid)
					self.query_in_queue.put((eslid, info))
					ids['bak'] = '00'
				else:
					esl_init.log.warning("can't find ap for esl %s", eslid)

		return 'OK', args

	def ap_add(self, db, args):
		return 'OK', db.list_updata(db.ap, args)

	def ap_del(self, db, args):
		for item in args:
			item['bak'] = '00'
			if not item.get('apid', None):
				item['bak'] = '06'
		db.list_del(db.ap, args)
		del_list = []
		for ap in args:
			if ap['bak'] == '00':
				del_list.append({"apid":ap['apid'], "status":"deleted"})
			if ap['bak'] == '01':
				ap.update({'bak': '05'})
		reply_ack("AP_STATUS", del_list, self.javaserver)
		return 'OK', args

	def ap_query(self, db, args):
		#返回数据库的内容
		for ids in args:
			apid = ids["apid"].upper().strip()
			esl_init.log.debug("query ap:%s" % apid)
			ids['bak'] = '05'
			if db.has_key(db.ap, apid):
				item = db.get_all_info(db.ap, apid)
				for title in item:
					ids[title] = item[title]
				ids['bak'] = '00'
				'加入成把枪的接口值'
				ids['bs_status'] = item['status']
				ids['apip'] = item['apip']
		return 'OK', args

	def esl_add(self, db, args):
		esl_init.log.info("esl_add %s,%s" % (len(args), args))
		heartbeat.is_man_updata(args, self.esl_info)

		for i in args:
			if not i.get("eslid", ''):
				i['bak'] = '02'
				continue
			info = db.get_all_info(db.esl, i['eslid'])
			info.update(i)
			for k in ['eslid', 'nw1', 'nw3', 'nw4', 'op2', 'op3']:
				if not info.get(k, None):
					i['bak'] = '02'
					break

		return 'OK', db.list_updata(db.esl, args)

	def esl_del(self, db, args):
		for item in args:
			item['bak'] = '00'
			if not item.get('eslid', None):
				item['bak'] = '02'
		db.list_del(db.esl, args)
		del_list = []
		for esl1 in args:
			if esl1['bak'] == '00':
				del_list.append({"eslid":esl1['eslid'], "status":"deleted"})
			if esl1['bak'] == '01':
				esl1.update({'bak': '02'})
		reply_ack("ESL_STATUS", del_list, self.javaserver)
		args_dp = deepcopy(args)
		for row in args_dp:
			row['op1'] = '30'
		heartbeat.is_man_updata(args_dp, self.esl_info)
		return 'OK', args

	def esl_query(self, db, args):
		#返回数据库的内容
		for ids in args:
			eslid = ids["eslid"].upper().strip()
			esl_init.log.info("query ids:%s" % eslid)
			ids['bak'] = '02'
			if db.has_key(db.bind, eslid) and is_esl_info_ok(db, eslid):

				#更新商品信息
				item_bind = db.get_one(db.bind, eslid)
				item = db.get_one(db.sales, item_bind['salesno'])
				for title in ['salesno', 'salesname', 'Price', 'Price1', 'Price2', 'Price3']:
					ids[title] = item[title]

				ids['esl_status'] = get_esl_status(eslid, db)
				ids['apid'] = item_bind['apid']

				item = db.get_one(db.esl, eslid)
				for title in ids:
					if title != 'bak' and title in item:
						ids[title] = item[title]
				ids['bak'] = '00'
				if item['status'] == "online":
					ids["Updata_status"] = "success"
				elif item['status'] == "offline":
					ids["Updata_status"] = "failed"
				else:
					ids["Updata_status"] = item['status']

				ids["Updata_time"] = ""
				try:
					tis = time.strptime(item['lastworktime'], "%a %b %d %H:%M:%S %Y")
					ids["Updata_time"] = "%d%02d%02d%02d%02d%02d" % (tis.tm_year, tis.tm_mon, tis.tm_mday,\
						tis.tm_hour, tis.tm_min, tis.tm_sec)
				except:
					pass

		return 'OK', args

	def esl_failed_list(self, db, args):
		failed_list = []
		for eslid in db.key_list(db.bind):
			#status = db.get_one(db.esl, eslid)['status']
			#价签状态从商品更新结果获取
			#sales_status = db.get_one(db.sales, db.get_one(db.bind, eslid)['salesno'])['status']
			#status = "online" if sales_status == "update success" else "offline"
			status = get_esl_status(eslid, db)
			if status == "offline":
				failed_list.append({"eslid":eslid, "error":"offline"})
			'''
			if not status:
				continue
			if status == "offline":
				failed_list.append({"eslid":eslid, "error":"offline"})
			elif "update failed" in status:
				#failed_list.append({"eslid":eslid, "error":"unupdated"})
				failed_list.append({"eslid":eslid, "error":"offline"})
			'''
		return "OK", failed_list

	def ap_failed_list(self, db, args):
		failed_list = []
		for apid in db.key_list(db.ap):
			ap = db.get_one(db.ap, apid)
			if not ap['status']:
				continue
			if ap['status'] == "offline":
				failed_list.append({"apid":apid, "apip":ap['apip'],"error":"offline"})
			elif "error" in ap['status']:
				failed_list.append({"apid":apid, "apip":ap['apip'], "error":"error"})
		return "OK", failed_list
	
	def ap_list(self, db, args):
		args = args[0]
		apn = db.get_all_ap()
		start_index, end_index = check_index(args)
		args['total_num'] = str(len(apn))
		args['ap_list'] = []
		for ap1 in apn:
			ap_info = db.get_one(db.ap, ap1)
			args['ap_list'].append({"apid":ap_info['apid'], "status":ap_info['status']})
		args['ap_list'] = filed_transfer_out_unicode(args['ap_list'][start_index:end_index])
		return "OK", [args]

	def sales_list(self, db, args):
		args = args[0]
		start_index, end_index = check_index(args)
		all_esl = db.key_list(db.bind)
		args['sales_list'] = []
		total_num = len(all_esl)
		for esl1 in all_esl:
			try:
				item = {}
				item['eslid'] = esl1
				
				item['esl_status'] = get_esl_status(esl1, db)
				'''
				esl_status = db.get_one(db.esl, esl1)['status']

				if esl_status == 'offline':
					item['esl_status'] = "offline"
				elif esl_status == 'lowpower':
					item['esl_status'] = "lowpower"
				else:
					item['esl_status'] = "online"
				'''
				salesno = db.get_one(db.bind, esl1)['salesno']
				sales_info = db.get_one(db.sales, salesno)
				for title in ['salesno', 'Price', 'Price1', 'Price2', 'Price3']:
					item[title] = sales_info[title]
				item["updata_status"] = "ok" if sales_info['status'] == "update success" else "fail"

				#价签状态统一从商品更新结果获取
				#if not item['esl_status'] == "lowpower":
				#	item['esl_status'] = "online" if item["updata_status"] == "ok" else "offline"

				item['salesname'] = sales_info['salesname']
				try:
					tis = time.strptime(sales_info['lastworktime'], "%a %b %d %H:%M:%S %Y")
					item["updata_time"] = "%d%02d%02d%02d%02d%02d" % (tis.tm_year, tis.tm_mon, tis.tm_mday,\
						tis.tm_hour, tis.tm_min, tis.tm_sec)
				except:
					item['updata_time'] = ""

				args['sales_list'].append(item)
			except Exception, e:
				total_num -= 1
				esl_init.log.error_msg("get sales info for esl %s failed: %s" % (esl1, e),
						errid='EXM002', eslid=esl1)

		if 'salesno' in args:
			for i in xrange(len(args['sales_list']) -1, -1, -1):
				if not args['salesno'] == args['sales_list'][i]['salesno']:
					del args['sales_list'][i]
					total_num -= 1
		elif 'eslid' in args:
			for i in xrange(len(args['sales_list']) -1, -1, -1):
				if args['eslid'].upper() != args['sales_list'][i]['eslid']:
					del args['sales_list'][i]
					total_num -= 1
		elif 'esl_status' in args:
			for i in xrange(len(args['sales_list']) -1, -1, -1):
				if not args['esl_status'] == args['sales_list'][i]['esl_status']:
					del args['sales_list'][i]
					total_num -= 1

		args['sales_list'] = args['sales_list'][start_index:end_index]
		args['sales_list'] = filed_transfer_out_unicode(args['sales_list'])
		args['total_num'] = str(total_num)

		return "OK", [args]

	def exited(self, db, args):
		return 'OK', args

	def is_valid_ip(self, ip):
		ip_list = ip.split(".")
		if len(ip_list) != 4:
			return False
		for ip1 in ip_list:
			if not ip1.isdigit():
				return False
		return True
	
	def ap_beacom(self, db, args): # 基站心跳接口
		ap = args[0]
		status, old_status = [], []
		if not self.is_valid_ip(ap['apip']):
			esl_init.log.error_msg("ap[%s] ip %s is not valid" % (ap['apid'], ap['apip']), errid='EXM003')
		else:
			if int(ap['status']) != 0:
				esl_init.log.error_msg("ap[%s] status %s, change to error" % 
					(ap['apid'], ap['status']), errid='EXM004')
				status = 'error'
			else:
				status = "online"
			_, old_status = db.get_last_status(db.ap, ap['apid'])
			#if status != old_status: #状态发生改变，发送消息给上层
			reply_ack("AP_STATUS", [{"apid":ap['apid'], 'status':status}], self.javaserver)
			ap['lastworktime'] = time.asctime()
			ap['listenport'] = "5649"
			if int(ap['status']) == 0:
				ap['status'] = status
			self.ap_add(db, [ap])
			netlink.save_apset_info(ap['apid'], self.apset, db) # 生成set_list.ini
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect((ap["apip"], 1))
			lip = s.getsockname()[0]
			s.close()
		except Exception, e:
			lip = "0.0.0.0"
		finally:
			return "OK", '[{"serverip":"' + lip + '","status":"0"}]'
	
	def gang_beacom(self, db, args):
		gang = args[0]
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect((gang["ip"], 1))
			lip = s.getsockname()[0]
			s.close()
		except Exception, e:
			lip = "0.0.0.0"
		finally:
			return "OK", '[{"serverip":"' + lip + '","status":"0"}]'
	
	def hello(self, db, args):
		return "OK"
	
	def echo(self, db, args):
		esl_init.log.debug("echo %s " % args)
		return "OK"
	
	def api_ver(self, db, args):
		return "OK", [{"api_version": self.api_version}]
	
	def empty_buffered_bind(self, db):
		#取空待解绑的清单
		unbind_list = [{"eslid":eslid, 'wait':'1'} for eslid in self.wait_for_proc['UNBIND'].keys()]
		_, acks = self.unbind(db, unbind_list)
		for ack in acks:
			if ack['wait'] == '0':
				eslid = ack['eslid']
				self.wait_for_proc['UNBIND'].pop(eslid, None)
				esl_init.log.debug("pop eslid %s from unbind buf" % eslid)
			
		#取空待绑定的清单
		_, acks = self.bind(db, self.wait_for_proc['BIND'].values())
		for ack in acks:
			if ack['wait'] == '0':
				eslid = ack['eslid']
				esl_init.log.debug("pop eslid %s from bind buf" % self.wait_for_proc['BIND'][eslid])
				self.wait_for_proc['BIND'].pop(eslid, None)
		#保存缓存表进文件
		save_wait_for_proc(self.wait_for_proc)

	def esl_netlink(self, db, args):
		# 接收需要组网的价签，当价签正在组网时返回失败，不处理该价签任务
		esl_init.log.info("esl_netlink (%s)%s " % (len(args), args))
		net = []
		esl_info = {}

		for item in args:

			item['bak'] = '00'
			for k in ["eslid", "nw1", "nw3"]:
				if not item.get(k, None):
					item['bak'] = '02'
					break

			if not is_esl_rf_ok(item):
				item['bak'] = '02' #BUSY
				continue
			
			if item['bak'] != '00':
				continue

			eslid = str(item["eslid"]).upper().strip()
			wakeupid = str(item["nw1"]).upper().strip()
			channel = item["nw3"]
			setchn = int(item.get("setchn", channel))
			grpchn = int(item.get("grpchn", channel))

			if eslid in self.netlink_data:
				item['bak'] = '03' #BUSY
				continue

			esl_info[eslid] = get_all_info(db, eslid, "CMD_NETLINK")
			if (not db.has_key(db.esl, eslid)) or (not is_esl_info_ok(db, eslid)):
				item['bak'] = '02' #not exist
				continue
			elif not db.has_key(db.bind, eslid): #绑定关系不存在
				ret = self.bind_to_default(db, eslid, esl_info[eslid])
				if not ret:
					item['bak'] = '05' #ap not exist
					continue
			else:
				pass

			if "op2" not in item:
				try:
					netid = int(esl_info[eslid]['op2'])
				except Exception, e:
					netid = int(eslid[6]+eslid[7], 16)
			else:
				netid = int(item['op2'])

			wakeupid, channel, setchn, grpchn = \
					load_and_set_netlink_data_to_db(db, eslid, wakeupid, channel, setchn, grpchn)
			item['nw1'] = wakeupid
			item['nw3'] = channel
			item['op2'] = netid
			item['setchn'] = setchn
			item['grpchn'] = grpchn

			if None not in [wakeupid, channel]:
				para = (wakeupid, channel, 'netlink', netid, setchn, grpchn)
				self.netlink_data[eslid] = para
				net.append(eslid)
				item['bak'] = "00" # 成功
			else:
				item['bak'] = "04" # 失败

		for id1 in net:
			self.netlink_in_queue.put((id1, esl_info[id1]))
		return 'OK', args

	def print_netlink(self, db, args):
		# 返回当前正在组网价签的信息并输出日志
		esl_init.log.info("print netlink_data %s " % self.netlink_data)
		data = []
		for id1 in self.netlink_data.keys():
			item = {}
			wid, chn, _ = self.netlink_data[id1]
			item['eslid'] = id1
			item['nw1'] = wid
			item['nw3'] = str(chn)
			data.append(item)

		args = data
		return 'OK', args

	def config_update(self, db, args):
		esl_init.log.info("config_update: %s; %s" % (len(args), args))
		section = 'section'
		for item in args:
			if (section not in item) or (not item[section]):
				esl_init.log.warning("update config failed, section %s", item[section])
				item['bak'] = '07'
				continue
			for key in item.keys():
				if (key == section) or (not key):
					continue
				if (not hasattr(conf, item[section])) or (not hasattr(getattr(conf, item[section]), key)):
					esl_init.log.warning("update config failed, section %s key %s", item[section], item[key])
					item['bak'] = '07'
					break
				esl_init.log.warning("update config file, %s.%s->%s", item[section], key, item[key])
				if not (item[key] and set_config(item[section], key, item[key])):
					item[key] = getattr(getattr(conf, item[section]), key)
				item['bak'] = '00'

		return 'OK', args
	
	def esl_heart_beat(self, db, args):
		try:
			bind_list, online_status = heartbeat.esl_register(db, args, self.esl_info, \
					self.esl_power_info, self.esl_power_his,\
					self.esl_level_change_count, self.ap_work_time, self.e_flag)
			if bind_list:
				self.bind(db, bind_list)
			if online_status:
				reply_ack("ESL_HB_STATUS", online_status, self.javaserver)
		except Exception, e:
			esl_init.log.error_msg('xml-heart_beat error: %s'%e, errid='EXM005')
		return 'OK', '[]'
	
	def get_esl_hb(self, db, args):
		esl_timeout = float(conf.system.esl_heartbeat_timeout)
			
		for item in args:
			eslid = item.get('eslid', None)
			if eslid not in self.esl_power_info:
				item['bak'] = '02'
				continue
			item['bak'] = '00'
			for level in self.esl_power_info.get(eslid, {}):
				for apid in self.esl_power_info[eslid][level]:
					level, rfpower, timelast = self.esl_power_info[eslid][level][apid]
					lasttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timelast))
					power_his = self.esl_power_his.get(eslid, {}).get(apid, [])
					item.update({apid:{"rfpower":rfpower, "lasttime":lasttime, "powerhis":power_his}})
			
		return 'OK', args

	def get_ap_level(self,db,esl_list):
		esl_timeout = float(conf.system.esl_heartbeat_timeout)

		for esl_dict in esl_list:
			esl_dict['ap_level'] = []
			eslid = esl_dict['eslid']
			if eslid in self.esl_power_info and eslid in self.esl_power_his:
				for level in self.esl_power_info[eslid]:
					for apid in self.esl_power_info[eslid][level]:
						if len(self.esl_power_his[eslid][apid]) < 7:
							continue
						if apid not in self.esl_power_his[eslid]:
							continue
				 		level, rfpower, timelast = self.esl_power_info[eslid][level][apid]
						timeout = heartbeat.get_heartbeat_timeout(apid, timelast, self.ap_work_time, esl_timeout)
						esl_dict['ap_level'].append((eslid, apid, level, rfpower, \
						time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timelast)),\
							"%s second before" % int(time.time() - timelast), \
							"timeout is %s sec" % int(timeout), "power list is %s" % self.esl_power_his[eslid][apid]))

		return 'OK', esl_list
	
	def ap_timeout(self, db, args):
		return 'OK', []

	def refresh_bind(self, db, args):
		esl_list = db.key_list(db.bind)
		bind_list = [{"eslid":eslid} for eslid in esl_list]
		return 'OK', heartbeat.refresh_bind_list(db, bind_list, \
						self.esl_power_info, self.ap_work_time)
	
	def ap_list_v2(self, db, args):
		return 'OK', api20.ap_list(db, args)
	def esl_list(self, db, args):
		return 'OK', api20.esl_list(db, args)
	def bind_list(self, db, args):
		return 'OK', api20.bind_list(db, args)
	def esl_report(self, db, args):
		return "OK", api20.esl_report(db, args)
	def ap_report(self, db, args):
		return "OK", api20.ap_report(db, args)
	def template_update(self, db, args):
		api20.template_update(db, args)
		return "OK", args
	def update_report(self, db, args):
		return "OK", updata.update_report(self.update_dict)

	def esl_info_api(self, db, args):
		api20.esl_info(db, args)
		return "OK", args

	def ap_info(self, db, args):
		api20.ap_info(db, args)
		return "OK", args
	
	def run_info(self, db, args):
		return "OK", api20.run_info(db, self.task_data)
	
	def set_cmd(self, db, args):
		for i in args:
			if 'setid' not in i or (not i['setid']):
				i['bak'] = '02'
				continue
			if 'setcmd' not in i or (not i['setcmd']):
				i['bak'] = '02'
				continue
			i['setcmd'] = i['setcmd'].upper()
			if i['setcmd'] not in ["CMD_LED_CONFIG", "CMD_LCD_CONFIG", "CMD_HB_CONFIG", "CMD_PAGE_CHANGE", 
							"CMD_HB_REQUEST", "CMD_SET_CONFIG", "CMD_CHN_CONFIG"]:
				i['bak'] = '02'
				esl_init.log.warning("set %s cmd %s error", i['setid'], i['setcmd'])
				continue
				
			try:
				if type(i['setargs']) == list:
					for v in i['setargs']:
						args1 = int(v)
					if i['setcmd'] == 'CMD_HB_REQUEST' and len(i['setargs'] != 2):
						raise KeyError, "CMD_HB_REQUEST args error"
					if i['setcmd'] == 'CMD_CHN_CONFIG' and len(i['setargs'] != 3):
						raise KeyError, "CMD_CHN_CONFIG args error"
				else:
					args1 = int(i['setargs'])
			except Exception, e:
				i['bak'] = '02'
				esl_init.log.warning("set %s cmd args %s error", i['setid'], i['setargs'])
				continue
				
			esl_list = db.get_set_eslid_one(i['setid'])
			for id1 in esl_list:
				cmd = {"eslid":id1, "setcmd":i['setcmd'], "setargs":i.get("setargs", [])}

				info = get_all_info(db, id1, "CMD_SET_CMD")
				info.update(cmd)
				ret = self.bind_to_default(db, id1, info)
				if ret:
					esl_init.log.info("set cmd for %s" % i['setid'])
					self.query_in_queue.put((id1, info))
					i['bak'] = '00'
				else:
					esl_init.log.warning("can't find ap for set %s", i['setid'])
			
		return "OK", args
	
	def send_cmd(self, cmd, args):
		cmd = cmd.upper()
		cmd_arr ={  #对外提供的方法名和处理函数
						"SALES_UPDATA_FOR_GAN" : self.sales_updata_for_gan, 
						"SALES_UPDATA_BUF" : self.sales_updata_buf,
						"ESL_UPDATE" : self.esl_update,
						#"SALES_UPDATA_BUF" : self.sales_updata_db,
						"BIND" : self.bind,
						"BIND_RECOVER" : self.bind_recover,
						"UNBIND" : self.unbind,
						"SALES_QUERY" : self.sales_query,
						"SALES_QUERY_ACK" : self.sales_query_ack,
						"SALES_DEL" : self.sales_del,
						"ESL_QUERY" : self.esl_query,
						"ESL_QUERY_REALTIME" : self.esl_query_realtime,
						"ESL_BEACOM" : self.esl_beacom,
						"ESL_ADD" : self.esl_add,
						"ESL_DEL" : self.esl_del,
						"ESL_REFRESH" : self.esl_refresh,
						"AP_QUERY" : self.ap_query,
						"AP_ADD" : self.ap_add,
						"AP_DEL" : self.ap_del,
						"AP_BEACOM" : self.ap_beacom,
						"GANG_BEACOM" : self.gang_beacom,
						"BIND_STATUS_ACK": self.bind_status_ack,
						"UNBIND_STATUS_ACK": self.unbind_status_ack,
						"ESL_ACTIVE_ACK": self.esl_active_ack,
						"ESL_RECOVER" : self.esl_recover,
						"HELLO" : self.hello,
						"ECHO" : self.echo,
						"EXIT":	self.exited,
						"ESL_FAILED_LIST": self.esl_failed_list,
						"AP_FAILED_LIST" : self.ap_failed_list,
						#苏宁把枪新接口
						#查询所有绑定的商品、或者根据商品号、价签号查询，返回价签ID，商品信息
						"SALES_LIST": self.sales_list, 
						#查询所有基站的状态，返回基站ID，基站状态
						#"AP_LIST" : self.ap_list,
						"ESL_NETLINK" : self.esl_netlink,
						"PRINT_NETLINK" : self.print_netlink,
						"GET_UPDATING_ESL_LIST" : self.get_updating_esl_list,
						"CLEAR_UPDATING_ESL_LIST" : self.clear_updating_esl_list,
						"CONFIG_UPDATE" : self.config_update,
 						"HEART_BEAT" : self.esl_heart_beat,
						"GET_AP_LEVEL":self.get_ap_level,
						"GET_ESL_HB": self.get_esl_hb,
						"REFRESH_BIND": self.refresh_bind,
						"AP_TIMEOUT": self.ap_timeout,
						#2.0接口
						"AP_LIST": self.ap_list_v2,
						"ESL_LIST": self.esl_list,
						"BIND_LIST": self.bind_list,
						"AP_REPORT": self.ap_report,
						"ESL_REPORT": self.esl_report,
						"TEMPLATE_UPDATE": self.template_update,
						"UPDATE_REPORT": self.update_report,
						"API_VERSION": self.api_ver,
						"ESL_INFO": self.esl_info_api,
						"AP_INFO": self.ap_info,
						"RUN_INFO": self.run_info,
						"SET_CMD": self.set_cmd,
					}
		
		if cmd in cmd_arr:
			try:
				ret_res, ret_val = cmd_arr[cmd](self.db, args)
				if type(ret_res) == str and type(ret_val) == str and ret_res + ret_val == 'OK':
					return 'OK'
				list_all_type(self.db, ret_val)
				ret = ret_res, ret_val
			except Exception, e:
				print_except()
				esl_init.log.error_msg("error!! cmd = %s, args = %s, %s" % (cmd, args, e), errid='EXM006')
				ret = "failed", args
			finally:
				self.db.commit()
			return ret
		else:
			return 'failed', "recv unknown cmd, cmd = %s, args = %s" % (cmd,  args)

def process(task_data):
	''' xml-rpc服务主进程，将在9000端口提供服务。'''

	ack_th = threading.Thread(target = reply_ack_thread, args=(task_data,))
	ack_th.start()

	try:

		ip = str(conf.extend_service.ip_addr)
		port = int(conf.extend_service.xml_rpc_port)

		server = SimpleXMLRPCServer((ip, port), logRequests=False, allow_none = True)
		server.timeout = 5
		server.register_introspection_functions()
		server.register_multicall_functions()
		server.register_instance(ExampleService(task_data))
		esl_init.log.info("xml_server starting")
		while True:
			if task_data['isquit']['xmlserver']:
				break
			if not ack_th.is_alive():
				esl_init.log.error("EXM006:reply ack thread is exit")
				break
			server.handle_request()
	except IOError, e:
		if e.errno == errno.EADDRINUSE:
			esl_init.log.error_msg("prov xmlserver is running, send exit cmd for it", errid='EXM007')
			server = get_xmlserver()
			server.send_cmd("EXIT", [])
	except Exception, e:
		esl_init.log.error_msg('xml_server:%s' % e, errid='EXM008')

	ack_th.join()
	esl_init.log.info("xml_server exit")

def start(task_data):
	'''启动xmlp-prc服务并返回进程对象'''
	#proc = multiprocessing.Process(target = process, args=(task_data,))
	global reply_ack_q
	reply_ack_q = task_data['reply_ack_q']
	proc = threading.Thread(target = process, args=(task_data,))
	proc.start()
	return proc

