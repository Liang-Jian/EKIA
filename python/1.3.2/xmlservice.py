# encoding: utf-8
import Queue
import cPickle as pickle
import random
import socket
import threading
import time
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from copy import deepcopy
import hashlib
import os
from  base64 import b64encode as be
from  base64 import b64decode as bd

import api20
import errno
import esl_init
import heartbeat
import htp
import netlink
import updata
import uuid
from bind import check_eslid_exist, get_xmlserver
from bind import filed_transfer_out_unicode, get_javaserver
from database import DB
from esl_init import conf, print_except
from esl_init import set_config, trace
from netlink import get_bind_nw1_nw3, get_bind_nw1_nw3_3g, bind_list_init, load_and_set_netlink_data_to_db
from netlink import get_old_para
from util import const
from util import func

def calc_md5(x):
	m=hashlib.md5()
	m.update(x)
	return m.hexdigest()

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
				if k in ['eslid', 'apid']:
					args[k] = args[k].upper()

def get_all_esl_list(db, item):
	id_list = []
	if "esllist" not in item:
		id_list = db.get_sales_bind_esl_list(item['salesno'])
		if not id_list:
			id_list = []

		esl_list = []
		for eslid in id_list:
			esl_obj = {'eslid':eslid}
			esl_list.append(esl_obj)

		item['esllist'] = esl_list

	for ids in item.get("esllist", []):
		try:
			if 'eslid' in ids:
				id_list.append(ids["eslid"])
		except Exception, e:
			esl_init.log.error_msg("can't find esllist in update request;%s" % item, errid='EXM009')
	
	return id_list

def get_all_esl_list_test(db):
	
	t = '解析sales_updata_buf中esl_list字段'

	t1 = 'esllist 字段不是字典'
	item = {'esllist':['5a-11-22-44']}
	id_list = get_all_esl_list(db, item)
	if id_list != []:
		trace(t, t1, 'failed')

	t1 = 'esllist 中没有eslid'
	item = {'esllist':[{'template':"2222"}]}
	id_list = get_all_esl_list(db, item)
	if id_list != []:
		trace(t, t1, 'failed', id_list)

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

			for ack in item['ack']:
				ack.pop('starttime', None)
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
	reply_ack_q.put((cmd, val))

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

	def __init__(self, task_data, db_file = None):
		self.updata_in_queue = task_data['updata']['in_queue']
		self.updata_buf_in_queue = task_data['updata']['buf_in_queue']
		self.updata_out_queue = task_data['updata']['out_queue']
		self.bind_in_queue = task_data['bind']['in_queue']
		self.query_in_queue = task_data['query']['in_queue']
		self.set_in_queue = task_data['set_only_q']['in_queue']
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
		self.db = DB(db_file = db_file)
		self.g = bind_list_init(self.db)
		self.ap_work_time = task_data['ap_work_time']

		self.last_ack_time = 0
		self.all_info = task_data['all_info']
		self.update_dict = task_data['updata']['updata_dict']
		self.e_flag = task_data['threading_event']
		self.esl_power_last_time = task_data['esl_power_last_time']
		self.apset = task_data['apset'] # set_list.ini
		self.api_version = task_data['system_version']
		self.task_data = task_data

	def update_bind_list(self, db, id1, item):
		if not db.has_key(db.sales, item['salesno']):
			db.list_updata(db.sales, [item])

		val = []
		if not db.has_key(db.bind, id1):
			bind_request = [{"eslid":id1, "apid":"-1", "salesno":item['salesno'], "not_active":1}]
			_, val = self.bind(db, bind_request)
		else:
			bind_info = db.get_all_info(db.bind, id1)
			#绑定关系不对
			#if str(bind_info['salesno']) != str(item['salesno']):
			if bind_info['salesno'] != item['salesno']:
				bind_request = [{"eslid":id1, "apid":bind_info['apid'], "salesno":item['salesno'], "not_active":1}]
				_, val = self.bind(db, bind_request)
		if 'esllist' in item:
			if val:
				bak = val[0]["bak"]
				ret = val[0]["ret"]
				# 只要有一个价签有错误信息，最外层返回的bak就必须是错误码
				if bak != const.SUCCESS:
					item['bak'] = const.ESL_LIST_ERR
					item['ret'] = const.ESL_LIST_ITEM_ERR
			else:
				bak = const.SUCCESS
				ret = const.SUCCESS_INFO

			# 如果价签绑定错误，在item的esllist字段找到对应的价签，并写入错误码
			for esl_item in item.get('esllist', {}):
				if esl_item['eslid'] == id1:
					esl_item['bak'] = bak
					esl_item['ret'] = ret

	def upload_file(self,db,args):
		"""
		"""

		import time    
		for item in args:
			if not item.get('md5',None):
				item["bak"]="07"
				continue
			else:
				md5=item.get("md5")

			if not item.get("stream",None):
				item["bak"]="07"
				continue
			else:        
				stream=bd(item.get("stream"))

			if not item.get("name",""):
				item["bak"]="07"
				continue
			else:
				name=item.get("name")

			workingdir=os.path.abspath('.')
			abspath=os.path.abspath(os.path.join(workingdir,'upload'))			
			p,f=os.path.split(os.path.abspath(os.path.join(workingdir,'upload',name)))
			
			if  not p.startswith(abspath):
				item["bak"]="07"
				continue

			if not (p and f):
				item["bak"]="07"
				continue

			try:
				m=hashlib.md5()
				if not os.path.exists(p):
					os.makedirs(p)

				m.update(stream)
				if m.hexdigest() != md5:
					item["bak"]='07'
					raise Exception,"wrong md5 %s<>%s"%(md5,m.hexdigest())
				with open(os.path.join(p,f),'wb') as fh:
					fh.write(stream)
			except Exception, e:
				item["bak"]='07'
				
				
		return "OK",args

	def remoter_cmd(self, db, args):

		for item in args:
			try:
				udf={str(x):item.pop(x,None) for x in ["color","on_time","off_time","sleep_time","count"] }
				udf["led_flag"]=1 if None not in udf.values() else 0
				page={str(x):item.pop(x,None) for x in ["page","time"]}
				udf["page_flag"]= 1 if None not in page.values() else 0
				udf.update(page)
				item["udf"]=udf
			except Exception, e:
				#  not enough args
				item["bak"]="07"
			finally:
				item["sid"]=item["sid"]+"@"+str(uuid.uuid1())+"RTCMD"

		return self.esl_update(db, args)

	def esl_update(self, db, args):
		esl_init.log.info("esl_update: %s; %s" % (len(args), args))
		#一直缓存数据
		for item in args:
			if 'eslid' not in item:
				item['bak'] == '02' #key不存在
				continue
			item.pop('apid', None)
			item['bak'] = "00"
			if 'sid' not in item:
				item['sid'] = 'nosid'
			item['oldsid'] = item['sid']

			#获取商品号
			if 'salesno' not in item:
				bind_info = db.get_all_info(db.bind, item['eslid'])
				if (not bind_info) or (not bind_info['salesno']):
					item['salesno'] = 'nosalesno' + item['eslid']
					item['salesno'] = item['salesno'].upper()
				else:
					item['salesno'] = bind_info['salesno']

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

			item['bak'] = const.SUCCESS
			item['ret'] = const.SUCCESS_INFO
			if 'sid' not in item:
				item['sid'] = 'nosid'
			item['oldsid'] = item['sid']
			if "salesno" not in item:
				item['salesno'] = 'nosalesno'
				item['salesno'] = item['salesno'].upper()
			item['sid'] = item['sid'] + '@' + '-' + str(uuid.uuid1())

			all_info = {}

			id_list = get_all_esl_list(db, item)
			for id1 in id_list:
				self.update_bind_list(db, id1, item)
				all_info[id1] = get_all_info(db, id1, "CMD_UPDATE")

			if len(id_list) > 0:
				i = deepcopy(item)
				self.updata_buf_in_queue.put(([i], all_info))
			else:
				item['bak'] = const.ESL_LIST_ERR
				item['ret'] = const.ESL_LIST_EMPTY


		#再恢复
		for item in args:
			if 'oldsid' in item:
				item['sid'] = item.pop('oldsid')
		return "OK", args

	def bind_to_default(self, db, eslid, info, defaultap = None):
		if not db.has_key(db.sales, '0'):
			db.list_updata(db.sales, [{"salesno":"0"}])
		
		if defaultap:
			best_ap = defaultap
		else:
			best_ap = heartbeat.get_best_ap(db, eslid, \
						self.esl_power_info.get(eslid, {}), \
						self.esl_power_his.get(eslid, {}), \
						self.ap_work_time,
						self.esl_power_last_time.get(eslid, {})
						)
		if best_ap:
			esl_init.log.warning("find available ap %s for esl %s", best_ap, eslid)
			info.update(db.get_all_info(db.ap, best_ap))
			info['salesno'] = '0'
			return True
		
		esl_init.log.warning("can't bind available ap for esl %s", eslid)
		return False

	def bind(self, db, args):
		esl_init.log.info("bind request(%s);%s" % (len(args), args))
		valid_list, sales_query_list, esl_active_list = [], [], []
		bind_key, esl_list = {}, []

		for item in args:
			eslid = item.get('eslid', None)
			apid = item.get('apid', None)
			salesno = item.get('salesno', None)
			item['bak'] = const.SUCCESS
			item['ret'] = const.SUCCESS_INFO
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				item['bak'] = ret_dict["bak"]
				item['ret'] = ret_dict["ret"]
				continue
			# if not salesno:
			# 	item['bak'] = const.PRODUCT_ERR
			# 	item['ret'] = const.PRODUCT_NONE
			# 	continue

			eslid = eslid.upper()
			item['eslid'] = eslid

			if not db.has_key(db.sales, salesno):
				db.list_updata(db.sales, [{"salesno":salesno}])
				#item['bak'] = '06' #商品待查询
				sales_query_list.append({"salesno":salesno})
			if (not apid) or (str(apid) == '-1'):
				best_ap = heartbeat.get_best_ap(db, eslid, \
							self.esl_power_info.get(eslid, {}), \
							self.esl_power_his.get(eslid, {}), \
							self.ap_work_time,
							self.esl_power_last_time.get(eslid, {}),
							)
				if not best_ap:
					esl_init.log.warning("try to find best ap for eslid %s failed" % (eslid))
					item['apid'] = '-1'
					item['bak'] = const.APID_ERR
					item['ret'] = const.AP_NOT_MATCH
					continue
				item['apid'] = str(best_ap)
				esl_init.log.info("eslid %s bind to ap %s" % (eslid, best_ap))

			if not db.has_key(db.ap, item['apid']):
				item['bak'] = const.APID_ERR
				item['ret'] = const.AP_NOT_EXIST
				continue
			
			if item['bak'] == const.SUCCESS:
				valid_list.append(item)
				e = {"eslid":item['eslid']}
				if 'extESLID' in item:
					e['exteslid'] = item['extESLID']
				if 'template' in item:
					e['op4'] = item['template']
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
			if 'HS_EL_53' in esl_info['op3']:
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
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				item['bak'] = ret_dict["bak"]
				item['ret'] = ret_dict["ret"]
				continue

			eslid = eslid.upper()
			
			info = get_all_info(db, eslid, "CMD_UPDATE")
			valid_list.append(item)

			try:
				self.g[info['apid']][info['op3']][info['nw1']][info['nw3']] -= 1
			except KeyError, e:
				pass

			item['bak'] = const.SUCCESS
			item['ret'] = const.SUCCESS_INFO
			unbind_temp = item.get('template', None)
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
		esl_init.log.info("sales_query_ack ; %s" % args)
		for item in args[:]:
			if item['bak'] != "00":
				args.remove(item)
				self.salesno_not_valid.append(item['salesno'])
		ok_list = db.list_updata(db.sales, args)
		return "OK"

	def sales_query(self, db, args):
		esl_init.log.info( "sales_query request ; %s" % args)
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
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				ids['bak'] = ret_dict["bak"]
				ids['ret'] = ret_dict["ret"]
				esl_init.log.warning("query %s status failed,bak=%s,ret=%s" % (eslid, ret_dict["bak"], ret_dict["ret"]))
				continue
			# if (not db.has_key(db.esl, eslid)) or (not func.is_esl_info_ok(db, eslid)):
			# 	esl_init.log.warning("query %s status failed, not in database" % eslid)
			# 	continue
				
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

	def ap_query(self, db, args):
		#返回数据库的内容
		for ids in args:
			if "apid" not in  ids:
				ids['bak'] = '07'
				continue
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
		esl_init.log.info("esl_add %s;%s" % (len(args), args))
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
			if "eslid" not in ids:
				ids['bak'] = '07'
				continue
			eslid = ids["eslid"].upper().strip()
			esl_init.log.info("query ids;%s" % eslid)
			ids['bak'] = '05'
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				ids['bak'] = ret_dict["bak"]
				ids['ret'] = ret_dict["ret"]
				continue

			# todo 增加价签ID在绑定表中不存在的错误码
			if not db.has_key(db.bind, eslid):
				ids['bak'] = const.ESLID_ERR
				ids['ret'] = const.ESL_NOT_EXIST
				continue

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
				salesno = db.get_one(db.bind, esl1)['salesno']
				sales_info = db.get_one(db.sales, salesno)
				for title in ['salesno', 'Price', 'Price1', 'Price2', 'Price3']:
					item[title] = sales_info[title]
				item["updata_status"] = "ok" if sales_info['status'] == "update success" else "fail"

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
			if status == 'online' and old_status == 'offline':
				ap['onlinebegintime'] = time.asctime()
			reply_ack("AP_STATUS", [{"apid":ap['apid'], 'status':status}], self.javaserver)
			ap['lastworktime'] = time.asctime()
			ap['listenport'] = "5649"
			if int(ap['status']) == 0:
				ap['status'] = status
			db.list_updata(db.ap, [ap])
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
	
	def esl_netlink(self, db, args):
		# 接收需要组网的价签，当价签正在组网时返回失败，不处理该价签任务
		esl_init.log.info("esl_netlink (%s);%s " % (len(args), args))
		net = []
		esl_info = {}

		for item in args:

			item['bak'] = const.SUCCESS
			item['ret'] = const.SUCCESS_INFO
			if not item.get('eslid', None):
				item['bak'] = const.ESLID_ERR
				item['ret'] = const.ESL_NONE
				continue

			for k in ["nw1", "nw3"]:
				if not item.get(k, None):
					item['bak'] = const.ESLID_ERR
					item['ret'] = const.ESL_ARG_PROP_ERR
					break

			if item['bak'] != const.SUCCESS:
				continue

			if not func.is_valid_id(item['eslid']):
				item['bak'] = const.ESLID_ERR
				item['ret'] = const.ESL_FMT_ERR
				continue

			if not func.is_esl_rf_ok(item):
				item['bak'] = const.ESLID_ERR
				item['ret'] = const.ESL_ARG_PROP_ERR
				continue
			
			eslid = str(item["eslid"]).upper().strip()
			wakeupid = str(item["nw1"]).upper().strip()
			channel = item['nw3']
			setchn = int(item.get("setchn", channel))
			grpchn = int(item.get("grpchn", channel))
			
			if eslid in self.netlink_data:
				item['bak'] = const.BUSY
				item['ret'] = const.BUSY_INFO
				continue

			esl_info[eslid] = get_all_info(db, eslid, "CMD_NETLINK")
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				item['bak'] = ret_dict["bak"]
				item['ret'] = ret_dict["ret"]
				continue
			# if (not db.has_key(db.esl, eslid)) or (not func.is_esl_info_ok(db, eslid)):
			# 	item['bak'] = '02' #not exist
			# 	continue
			elif not db.has_key(db.bind, eslid): #绑定关系不存在
				ret = self.bind_to_default(db, eslid, esl_info[eslid])
				if not ret:
					item['bak'] = const.APID_ERR
					item['ret'] = const.AP_NOT_MATCH
					continue
			else:
				pass

			try:
				if "op2" not in item:			
					netid = int(esl_info[eslid]['op2'])		
				else:
					netid = int(item['op2'])
			except Exception, e:
					netid = int(eslid[6]+eslid[7], 16)

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
				item['bak'] = const.SUCCESS # 成功
				item['ret'] = const.SUCCESS_INFO
			else:
				item['bak'] = const.BUSY # 失败
				item['ret'] = const.BUSY_INFO

		for id1 in net:
			self.netlink_in_queue.put((id1, esl_info[id1]))
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
					self.esl_level_change_count, self.ap_work_time, self.e_flag,\
					self.esl_power_last_time)
			if bind_list:
				self.bind(db, bind_list)
			if online_status:
				reply_ack("ESL_HB_STATUS", online_status, self.javaserver)
		except Exception, e:
			print_except()
			esl_init.log.error_msg('xml-heart_beat error: %s'%e, errid='EXM005')
		return 'OK', '[]'
	
	def get_esl_hb(self, db, args):
		esl_timeout = float(conf.system.esl_heartbeat_timeout)
			
		for item in args:
			eslid = item.get('eslid', None)
			if not eslid:
				item['bak'] = '02'
				continue
			eslid = eslid.upper()
			if not db.has_key(db.esl, eslid):
				item['bak'] = '02'
				continue
			item['bak'] = '00'
			
			ap_list, ap_level_map = [], {}
			for level in self.esl_power_info.get(eslid, {}):
				for apid in self.esl_power_info[eslid][level]:
					level, rfpower, timelast = self.esl_power_info[eslid][level][apid]
					ap_level_map[apid] = level
					ap_list.append(apid)

			for apid in self.esl_power_his.get(eslid, {}):
				ap_list.append(apid)

			for apid in set(ap_list):
				try:
					level, rfpower, timelast = self.esl_power_info[eslid][ap_level_map[apid]][apid]
					lasttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timelast))
				except KeyError, e:
					level, rfpower, lasttime = "None", "None", "None"
				
				power_his = self.esl_power_his.get(eslid, {}).get(apid, [])
				last_hb = self.esl_power_last_time.get(eslid, {}).get(apid, None)
				if last_hb:
					last_hb = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_hb))
				else:
					last_hb = "None"

				item.update({apid:{"rfpower":level, "lasttime":lasttime, \
							"powerhis":power_his, "lasthbtime":last_hb}})

		return 'OK', args

	def get_ap_level(self,db,esl_list):
		esl_timeout = float(conf.system.esl_heartbeat_timeout)

		for esl_dict in esl_list:
			esl_dict['ap_level'] = []
			eslid = esl_dict.get('eslid', None)
			ret_dict = func.check_esl(db, eslid)
			if ret_dict["bak"] != const.SUCCESS:
				esl_dict['bak'] = ret_dict["bak"]
				esl_dict['ret'] = ret_dict["ret"]
				continue
			if eslid in self.esl_power_info and eslid in self.esl_power_his:
				for level in self.esl_power_info[eslid]:
					for apid in self.esl_power_info[eslid][level]:
						if apid not in self.esl_power_his[eslid]:
							continue
						if len(self.esl_power_his[eslid][apid]) < 7:
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
		bind_list =  heartbeat.refresh_bind_list(db, bind_list, self.esl_power_info, \
							self.esl_power_his, self.ap_work_time, self.esl_power_last_time)
		if bind_list:
			self.bind(db, bind_list)
		
		return 'OK', bind_list
	
	def ap_list_v2(self, db, args):
		return 'OK', api20.ap_list(db, args,self.esl_power_info)
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
					if i['setcmd'] == 'CMD_HB_REQUEST' and len(i['setargs']) != 2:
						raise KeyError, "CMD_HB_REQUEST args error"
					if i['setcmd'] == 'CMD_CHN_CONFIG' and len(i['setargs']) != 3:
						raise KeyError, "CMD_CHN_CONFIG args error"
				else:
					args1 = int(i['setargs'])
			except Exception, e:
				i['bak'] = '02'
				esl_init.log.warning("set %s cmd args %s error", i['setid'], i['setargs'])
				continue
				
			esl_ap_list = db.get_set_eslid_one(i['setid'], self.esl_power_his)

			for (id1, apid1) in esl_ap_list:
				cmd = {"eslid":id1, "setcmd":i['setcmd'], "setargs":i.get("setargs", [])}

				info = get_all_info(db, id1, "CMD_SET_CMD")
				info.update(cmd)
				ret = self.bind_to_default(db, id1, info, defaultap = apid1)
				if ret:
					esl_init.log.info("set cmd for %s on ap %s" % (i['setid'], apid1))
					self.set_in_queue.put((id1, info))
					i['bak'] = '00'
				else:
					esl_init.log.warning("can't find ap for set %s", i['setid'])
			
		return "OK", args
	
	def send_cmd(self, cmd, args):
		cmd = cmd.upper()
		cmd_arr ={  #对外提供的方法名和处理函数
						"SALES_UPDATA_FOR_GAN" : self.echo, 
						"SALES_UPDATA_BUF" : self.sales_updata_buf,
						"ESL_UPDATE" : self.esl_update,
						"BIND" : self.bind,
						"BIND_RECOVER" : self.bind_recover,
						"UNBIND" : self.unbind,
						"SALES_QUERY_ACK" : self.sales_query_ack,
						"ESL_QUERY" : self.esl_query,
						"ESL_QUERY_REALTIME" : self.esl_query_realtime,
						"ESL_BEACOM" : self.esl_beacom,
						"ESL_ADD_INTERNEL" : self.esl_add,
						"ESL_DEL_INTERNEL" : self.esl_del,
						"ESL_REFRESH" : self.echo,
						"AP_QUERY" : self.ap_query,
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
						"ESL_NETLINK" : self.esl_netlink,
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
						"REMOTER_CMD": self.remoter_cmd,
						"UPLOAD_FILE": self.upload_file,
					}
		
		if cmd in cmd_arr:
			try:
				list_all_type(self.db, args)
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
	global reply_ack_q
	reply_ack_q = task_data['reply_ack_q']
	proc = threading.Thread(target = process, args=(task_data,))
	proc.start()
	return proc



def bind_test(self, db):

	t = "绑定测试"

	eslid = "55-55-55-99"
	eslid, old_nw1, old_chn = "55-55-55-99", "51-11-21-66", "158"
	esl_list = [{"eslid":"55-55-55-99", "setchn":old_chn, "grpchn":old_chn, "nw3":old_chn,
		"nw1":old_nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]
	sales_list = [{"salesno":"2"}, {"salesno":"3"}, {"salesno":"4"}]
	ap_list = [{"apid":"2"}]

	db.list_updata(db.esl, esl_list)

	t1 = "价签KEY为空"
	bind_list = [{"apid":"2", "salesno":"ccc"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	t1 = "价签KEY在数据库中不存在"
	bind_list = [{"apid":"2", "eslid":"55-11-11-99", "salesno":"ccc"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	t1 = "价签KEY的格式错误"
	bind_list = [{"apid":"2", "eslid":"55-11-11", "salesno":"ccc"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	# t1 = "商品KEY为空"
	# bind_list = [{"apid":"2", "eslid":eslid}]
	# ret, val = self.bind(db, bind_list)
	# bak = val[0]["bak"]
	# if bak != const.PRODUCT_ERR:
	# 	trace(t, t1, "failed", ret, val)

	t1 = "基站KEY为空"
	bind_list = [{"salesno":"2", "eslid":eslid}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.APID_ERR:
		trace(t, t1, "failed", ret, val)

	t1 = "基站KEY在数据库中不存在"
	bind_list = [{"salesno":"2", "apid":"12", "eslid":eslid}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.APID_ERR:
		trace(t, t1, "failed", ret, val)
	
	t1 = "缺少3个key"
	bind_list = [{"salesno1":"2", "eslid1":eslid, "apid1":"2"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)
	
	db.list_updata(db.sales, sales_list)
	db.list_updata(db.ap, ap_list)

	t1 = "提交多个，头尾OK，中间异常"
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"2"}, {"salesno":"3", "eslid":"", "apid":"2"}, \
						{"salesno":"3", "eslid":eslid, "apid":"2"}]
	ret, val = self.bind(db, bind_list)
	bak0, bak1, bak2 = val[0]["bak"], val[1]["bak"], val[2]["bak"]
	if (bak0, bak1, bak2) != (const.SUCCESS, const.ESLID_ERR, const.SUCCESS):
		trace(t, t1, "failed", ret, val)
	
	t1 = "价签属性不合法"
	_esl_list = [{"eslid":eslid, "nw3":"cc"}]
	db.list_updata(db.esl, _esl_list)
	bind_list = [{"salesno1":"2", "eslid1":eslid, "apid1":"2"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	#附加属性测试
	db.list_updata(db.esl, esl_list)
	db.list_updata(db.sales, sales_list)
	db.list_updata(db.ap, ap_list)

	t1 = "价签附属属性，添加模版"
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"2", "template":"aaa"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	op4 = db.get_one(db.esl, eslid)['op4']
	if bak != const.SUCCESS or op4 != "aaa":
		trace(t, t1, "failed", ret, val, op4)

	t1 = "价签附属属性，添加extESLID"
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"2", "extESLID":"aaa"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	exteslid = db.get_one(db.esl, eslid)['exteslid']
	if bak != const.SUCCESS or exteslid != "aaa":
		trace(t, t1, "failed", ret, val, exteslid)

	t1 = "价签附属属性，添加其余字段"
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"2", "op3":"aaa"}]
	ret, val = self.bind(db, bind_list)
	bak = val[0]["bak"]
	op3 = db.get_one(db.esl, eslid)['op3']
	if bak != const.SUCCESS or op3 == "aaa":
		trace(t, t1, "failed", ret, val, op3)

	#自动绑定测试

	t1 = "任何信息都没有，自动选基站，基站号为－1"
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"-1", "op3":"aaa"}]
	db.list_del(db.bind, bind_list)
	ret, val = self.bind(db, bind_list)
	bak, apid = val[0]["bak"], val[0]["apid"]
	if bak != const.APID_ERR or apid != "-1":
		trace(t, t1, "failed", ret, val)

	# "1号基站有过充足的心跳；2号基站有最近3次的心跳; 3号基站没有心跳，但是上次绑定过，4号是默认基站"
	times = time.time()
	self.esl_power_info = {eslid:{40:{"1":(40, 48, times - 50)}}}
	self.esl_power_his = {eslid:{"1":[20,20,20,20,20,20,20,], "2":[80,90,]}}
	self.esl_power_last_time = {eslid:{"1" : times - 3*60, "2":times - 2*60}}

	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"3", "extESLID":"aaa"}]
	db.list_updata(db.bind, bind_list)
	db.list_updata(db.ap, [{"apid":"1"}, {"apid":"2"}, {"apid":"3"}, {"apid":"4"}])
	
	t1 = "绑定指定基站，但是没有心跳，也要绑成功"
	ret, val = self.bind(db, [{"salesno":"2", "eslid":eslid, "apid":"3", "extESLID":"aaa"}])
	bak, apid = val[0]["bak"], val[0]["apid"]
	if bak != const.SUCCESS or apid != "3":
		trace(t, t1, "failed", ret, val)

	t1 = "所有条件都满足，绑定到1号基站"
	ret, val = self.bind(db, [{"salesno":"2", "eslid":eslid, "apid":"-1", "extESLID":"aaa"}])
	bak, apid = val[0]["bak"], val[0]["apid"]
	if bak != const.SUCCESS or apid != "1":
		trace(t, t1, "failed", ret, val)

	t1 = "满足条件2，绑到2号基站"
	self.esl_power_info = {eslid:{40:{"1":(40, 48, times - 7200)}}}
	ret, val = self.bind(db, [{"salesno":"2", "eslid":eslid, "apid":"-1", "extESLID":"aaa"}])
	bak, apid = val[0]["bak"], val[0]["apid"]
	if bak != const.SUCCESS or apid != "2":
		trace(t, t1, "failed", ret, val)

	t1 = "满足条件3，绑到3号基站"
	self.esl_power_info = {eslid:{40:{"1":(40, 48, times - 7200)}}}
	self.esl_power_last_time = {eslid:{"1" : times - 7200, "2":times - 31*60}}
	bind_list = [{"salesno":"2", "eslid":eslid, "apid":"3", "extESLID":"aaa"}]
	db.list_updata(db.bind, bind_list)
	ret, val = self.bind(db, [{"salesno":"2", "eslid":eslid, "apid":"-1", "extESLID":"aaa"}])
	bak, apid = val[0]["bak"], val[0]["apid"]
	if bak != const.SUCCESS or apid != "3":
		trace(t, t1, "failed", ret, val)

	t1 = "满足条件4，绑到4号基站" #暂时测试不了

	#自组网测试

def unbind_test(self, db):
	t = "解绑测试"

	eslid = "55-55-55-99"
	bind_list = [{"eslid":eslid, "salesno":"2", "apid":"2"}]
	db.list_updata(db.bind, bind_list)

	t1 = "价签KEY为空"
	unbind_list = [{"eslid1":eslid}]
	ret, val = self.unbind(db, unbind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	t1 = "价签KEY格式错误"
	unbind_list = [{"eslid":"55-55-55"}]
	ret, val = self.unbind(db, unbind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

	t1 = "价签KEY在数据库中不存在"
	unbind_list = [{"eslid":"55-11-11-99"}]
	ret, val = self.unbind(db, unbind_list)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, "failed", ret, val)

def sales_updata_buf_test(self, db):
	t = 'sales_updata_buf测试'

	eslid, old_nw1, old_chn = "55-11-22-99", "51-11-21-66", "158"
	esl_list = [{"eslid":eslid, "setchn":old_chn, "grpchn":old_chn, "nw3":old_chn,
		"nw1":old_nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]
	sales_list = [{"salesno":"2"}, {"salesno":"3"}, {"salesno":"4"}]
	ap_list = [{"apid":"2"}]

	db.list_updata(db.esl, esl_list)
	db.list_updata(db.sales, sales_list)
	db.list_updata(db.ap, ap_list)
	db.list_updata(db.bind, [{'salesno':'11', 'apid':'11', 'eslid':eslid}])

	t1 = 'esllist 字段为空列表'
	item = [{'bak': '00', 'esllist': [], 'salesno': '1', 'Price': '8.79', 'oldsid': '8.79', 'location': '2016-06-15',
			'sid': '234234234', 'Price3': '8.79', 'Price2': '65535', 'Price1': '8.79',
			'spec': '52-88-01-99 50', 'spec1': '528801'}]
	ret, val = self.sales_updata_buf(db, item)
	bak = val[0]["bak"]
	if bak != const.ESL_LIST_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'esllist 字段为空列表'
	item = [{'bak': '00', 'esllist1': [{'eslid1':eslid}], 'salesno': '1', 'Price': '8.79', 'oldsid': '8.79', 'location': '2016-06-15',
			'sid': '234234234', 'Price3': '8.79', 'Price2': '65535', 'Price1': '8.79',
			'spec': '52-88-01-99 50', 'spec1': '528801'}]
	ret, val = self.sales_updata_buf(db, item)
	bak = val[0]["bak"]
	if bak != const.ESL_LIST_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'esllist中价签KEY为空'
	item = [{'bak': '00', 'esllist': [{'eslid':eslid}], 'salesno': '1', 'Price': '8.79', 'oldsid': '8.79', 'location': '2016-06-15',
			'sid': '234234234', 'Price3': '8.79', 'Price2': '65535', 'Price1': '8.79',
			'spec': '52-88-01-99 50', 'spec1': '528801'}]
	ret, val = self.sales_updata_buf(db, item)
	bak = val[0]["bak"]
	if bak != const.ESL_LIST_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'esllist中价签格式错误'
	item = [{'bak': '00', 'esllist': [{'eslid':'55-211-11-99'}], 'salesno': '1', 'Price': '8.79', 'oldsid': '8.79', 'location': '2016-06-15',
			'sid': '234234234', 'Price3': '8.79', 'Price2': '65535', 'Price1': '8.79',
			'spec': '52-88-01-99 50', 'spec1': '528801'}]
	ret, val = self.sales_updata_buf(db, item)
	bak = val[0]["bak"]
	if bak != const.ESL_LIST_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'esllist中价签在数据库中不存在'
	item = [{'bak': '00', 'esllist': [{'eslid':'55-21-22-99', "apid":"2"}], 'salesno': '1', 'Price': '8.79', 'oldsid': '8.79', 'location': '2016-06-15',
			'si11d': '234234234', 'Price3': '8.79', 'Price2': '65535', 'Price1': '8.79',
			'spec': '52-88-01-99 50', 'spec1': '528801'}]
	ret, val = self.sales_updata_buf(db, item)
	bak = val[0]["bak"]
	if bak != const.ESL_LIST_ERR:
		trace(t, t1, 'failed', ret, val)

def upload_file_test(self, db):
		p='upload_file_test'

		p1="only name "
		p0="123"
		self.upload_file(None,[{'name': p0, 'stream': 'MTI=', 'md5': 'c20ad4d76fe97759aa27a0c99bff6710'}])
		if not os.path.isfile('./upload/123'):
			trace(p, p1, 'failed')

		p1="file with subdir "
		p0="1/123"
		self.upload_file(None,[{'name': p0, 'stream': 'MTI=', 'md5': 'c20ad4d76fe97759aa27a0c99bff6710'}])
		if not os.path.isfile('./upload/1/123'):
			trace(p, p1, 'failed')
	
		p1="file with subdir no name"
		p0="1/"
		s,v=self.upload_file(None,[{'name': p0, 'stream': 'MTI=', 'md5': 'c20ad4d76fe97759aa27a0c99bff6710'}])
		
		for item in v:
			if not item.get('bak'):
				trace(p, p1, 'failed')

		p1="file with subdir include . .. "
		p0="1/123/../2"
		self.upload_file(None,[{'name': p0, 'stream': 'MTI=', 'md5': 'c20ad4d76fe97759aa27a0c99bff6710'}])
		for item in v:
			if not item.get('bak'):
				trace(p, p1, 'failed')
		
		p1="file with subdir "
		p0="1/dd/ddd/ss"
		self.upload_file(None,[{'name': p0, 'stream': 'MTI=', 'md5': 'c20ad4d76fe97759aa27a0c99bff6710'}])
		for item in v:
			if not item.get('bak'):
				trace(p, p1, 'failed')

def all_api_normaly_test(self, db):
	t = 'API正常操纵测试'
	
	eslid, nw1, chn = "55-11-22-99", "51-11-21-66", "158"
	esl_list = [{"eslid":eslid, "setchn":chn, "grpchn":chn, "nw3":chn,
		"nw1":nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]

	db.list_updata(db.sales, [{'salesno':'11'}])
	db.list_updata(db.ap, [{'apid':'11', 'apip':'10.2.4.59'}])
	db.list_updata(db.esl, esl_list)
	db.list_updata(db.bind, [{'salesno':'11', 'apid':'11', 'eslid':eslid}])

	t1 = 'sales_updata_buf 接口测试'
	ret, val = self.send_cmd('SALES_UPDATA_BUF', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'esl_update 接口测试'
	ret, val = self.send_cmd('ESL_UPDATE', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'bind 接口测试'
	ret, val = self.send_cmd('BIND', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'unbind 接口测试'
	ret, val = self.send_cmd('UNBIND', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'bind 接口测试'
	ret, val = self.send_cmd('BIND', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'esl_query_realtime 接口测试'
	ret, val = self.send_cmd('ESL_QUERY_REALTIME', [{'salesno':'11', 'apid':'11', 'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'set_cmd 接口测试'
	ret, val = self.send_cmd('SET_CMD', [{'setcmd':'CMD_LED_CONFIG', 'apid':'11', 'setid':eslid, 'setargs':[2]}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'runinfo 接口测试'
	ret, val = self.send_cmd('RUN_INFO', [{'setcmd':'CMD_LED_CONFIG', 'apid':'11', 'setid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'apinfo'
	ret, val = self.send_cmd('AP_INFO', [{'apid':'11'}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'esl_info'
	ret, val = self.send_cmd('ESL_INFO', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'api_version'
	ret, val = self.send_cmd('API_VERSION', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'ap_list'
	ret, val = self.send_cmd('AP_LIST', [{'apid':'11'}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'esl_list'
	ret, val = self.send_cmd('ESL_LIST', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'bind_list'
	ret, val = self.send_cmd('BIND_LIST', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'ap_report'
	ret, val = self.send_cmd('AP_REPORT', [{'apid':'11'}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 ='esl_report'
	ret, val = self.send_cmd('ESL_REPORT', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'template_update'
	ret, val = self.send_cmd('TEMPLATE_UPDATE', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 ='get_esl_hb'
	ret, val = self.send_cmd('GET_ESL_HB', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 = 'refresh_bind'
	ret, val = self.send_cmd('REFRESH_BIND', [{'eslid':eslid}])
	if ret == 'failed':
		trace(t, t1, ret, val)

	t1 = 'ap_query'
	ret, val = self.send_cmd('AP_QUERY', [{'apid':'11'}])
	if ret == 'failed':
		trace(t, t1, ret, val)
	
	t1 ='ap_beacom'
	ret, val = self.send_cmd('AP_BEACOM', [{'apid':'11', 'apip':'10.2.2.59', 'status':'0'}])
	if ret == 'failed':
		trace(t, t1, ret, val)

def esl_netlink_test(self, db):
	t = '组网测试'

	eslid, old_nw1, old_chn = "55-11-22-99", "51-11-21-66", "158"
	esl_list = [{"eslid":eslid, "setchn":old_chn, "grpchn":old_chn, "nw3":old_chn,
		"nw1":old_nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]
	sales_list = [{"salesno":"2"}, {"salesno":"3"}, {"salesno":"4"}]
	ap_list = [{"apid":"2"}]

	db.list_updata(db.esl, esl_list)
	db.list_updata(db.sales, sales_list)
	db.list_updata(db.ap, ap_list)
	db.list_updata(db.bind, [{'salesno':'2', 'apid':'2', 'eslid':eslid}])

	t1 = 'eslid 字段为空'
	item = [{"nw1":"51-03-05-66", "nw3":"35", "op2":"123", "setchn":"55", "grpchn":"88"}]
	ret, val = self.esl_netlink(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段为空'
	item = [{"eslid1":eslid, "nw1":"51-03-05-66", "nw3":"35", "op2":"123", "setchn":"55", "grpchn":"88"}]
	ret, val = self.esl_netlink(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段格式错误'
	item = [{"eslid":"55-111-22-99", "nw1":"51-03-05-66", "nw3":"35", "op2":"123", "setchn":"55", "grpchn":"88"}]
	ret, val = self.esl_netlink(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段在数据库中不存在'
	item = [{"eslid":"55-33-22-99", "nw1":"51-03-05-66", "nw3":"35", "op2":"123", "setchn":"55", "grpchn":"88"}]
	ret, val = self.esl_netlink(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = '传入参数中的其他属性错误'
	item = [{"eslid":eslid, "nw1":"51-023-05-66", "nw3":"35", "op2":"123", "setchn":"55", "grpchn":"88"}]
	ret, val = self.esl_netlink(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

def get_ap_level_test(self, db):
	t = '获取基站能量级别测试'

	eslid, nw1, chn = "55-11-22-99", "51-11-21-66", "158"
	esl_list = [{"eslid":eslid, "setchn":chn, "grpchn":chn, "nw3":chn,
		"nw1":'', "nw4":"NORMAL", "op3":"HS_EL_5300"},]

	db.list_updata(db.sales, [{'salesno':'11'}])
	db.list_updata(db.ap, [{'apid':'11', 'apip':'10.2.4.59'}])
	db.list_updata(db.esl, esl_list)
	db.list_updata(db.bind, [{'salesno':'11', 'apid':'11', 'eslid':eslid}])

	t1 = 'eslid 字段没有输入'
	item = [{}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段输入错误'
	item = [{'eslid1':eslid}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段为空'
	item = [{'eslid':''}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段格式错误'
	item = [{'eslid':'55-111-22-99'}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = 'eslid 字段在数据库中不存在'
	item = [{'eslid':'55-12-22-99'}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

	t1 = '价签的其他属性错误'
	item = [{'eslid':'55-11-22-99'}]
	ret, val = self.get_ap_level(db, item)
	bak = val[0]["bak"]
	if bak != const.ESLID_ERR:
		trace(t, t1, 'failed', ret, val)

def self_test():
	from tempfile import mktemp
	import os
	from main import create_task_data
	
	for test_fun in [bind_test,unbind_test, sales_updata_buf_test,
							esl_netlink_test, get_ap_level_test, 
							all_api_normaly_test,upload_file_test
	
						]:
		db_file = mktemp()
		db = DB(db_file = db_file)
		db.check_db()
		db.conn.close()

		task_data = create_task_data()
		global reply_ack_q
		reply_ack_q = task_data['reply_ack_q']

		xml_ser = ExampleService(task_data, db_file = db_file)

		test_fun(xml_ser, xml_ser.db)

		xml_ser.db.conn.close()
		os.remove(db_file)

	for test_fun in [get_all_esl_list_test, ]:
		db_file = mktemp()
		db = DB(db_file = db_file)
		db.check_db()

		test_fun(db)

		db.conn.close()
		os.remove(db_file)

