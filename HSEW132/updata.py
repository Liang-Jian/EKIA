# encoding: utf-8

import struct
import subprocess
import threading
import time
import xmlrpclib

import dot_temp
import json
import lcd_decode
import osd
from bind import get_xmlserver
from esl_init import conf, print_except
from heartbeat import check_bind_to
from osd import _init_esl, is_info_ok, _init_esl_json, Util
from osd_out_put import osd_output
from xmlserver import reply_ack

try:
   import cPickle as pickle
except Exception:
   import pickle

import esl_init
from htp import htp_task, get_nw4_val, ack_ok, is_ap_offline, get_apid_from_ack
from database import DB

T = None

def start(task_data):
   proc = threading.Thread(target = process, args = (task_data,))
   proc.start()
   return proc

def check_last_status_fast(task_data, lowpower_warning):
	db = DB()
	try:
		db.change_last_status_without_commit(db.sales, "status", "updating", "update failed")
		for eslid in db.get_lowpower_esl():
			task_data['lowpower_counter'][eslid] = lowpower_warning
		for eslid in db.get_unbinding_esl():
			task_data['bind']['in_queue'].put(eslid)
			esl_init.log.info("continue unbinding for %s" % (eslid))
	finally:
		db.commit()

def update_report(update_dict):
	report = {}
	report['wait_esl'] = len(update_dict)
	report['val'] = update_dict
	return [report]

def check_is_finished(db, updata_out_queue, update_dict, wait_dict, esl_power_info):
	from core import set_id_notbusy

	acks, vlist, blist = [], [], []
	while not updata_out_queue.empty():
		acks.append(updata_out_queue.get())
	for (id1, ack, sid) in acks:
		set_id_notbusy(id1)
		if id1 not in update_dict:
			continue
		status = 'online'
		if not ack_ok(ack):
			status = 'offline'
			if is_ap_offline(db, ack):
				status = 'apoffline'
		#设置更新状态
		if update_dict[id1]['sid'] != sid:
			continue #任务已经被提前cacnel掉，忽略此更新结果
		for item in update_dict[id1]['ack']:
			if item['eslid'] == id1:
				item['status'] = status
				newap = get_apid_from_ack(ack)
				s = update_dict[id1]['salesno']
				if status == 'online' and check_bind_to(db, id1, item['apid'], newap, s, esl_power_info):
					blist.append({"eslid":id1, "apid":newap, "salesno":s, 'not_active':1})
				break

	#检查是否更新结束
	for id1 in update_dict.keys():
		if id1 not in update_dict:
			continue
		is_finished, v, remove_list = check_is_finished_one(update_dict[id1], update_dict, wait_dict)
		if is_finished:
			vlist.append(v)
	
	return vlist, blist

failed_ack_dict = {"offline":1, "apoffline":1, "templateerror":1, "dataerror":1, "eslerror":1,
						"binderror":1, "timeout":1}
def check_is_finished_one(update_one, update_dict, wait_dict):

	ack_num = len(update_one['ack'])
	is_finished = True
	is_failed = False
	esl_list = []
	v = None
	remove_list = []

	sid = update_one['sid']
	for i in xrange(ack_num):
		ack = update_one['ack'][i]
		esl_list.append(ack['eslid'])
		if ack['status'] == 'waitting':
			if time.time() - ack['starttime'] < conf.system.update_sid_timeout: #2小时内
		 		is_finished = False
				break
			else: # 超过2小时还未更新结束，则设置为timeout
				esl_init.log.warning("esl %s update timeout, from %s" % (ack['eslid'], 
								time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ack['starttime']))))
				ack['status'] = 'timeout'
		if ack['status'] in failed_ack_dict:
			is_failed = True

	if is_finished:
		update_one['status'] = 'OK'
		if is_failed:
			update_one['status'] = 'failed'
		v = update_one
		for id1 in esl_list:
			remove_list.append(id1)
			#这个价签的任务还未被取消
			if id1 in update_dict and update_dict[id1]['sid'] == sid:
				del update_dict[id1]
			if id1 in wait_dict and wait_dict[id1][2]['sid'] == sid:
				del wait_dict[id1]

	return is_finished, v, remove_list

def get_id_list(db, item, esl_update_list, all_info):
	id_list = []
	if "esllist" not in item:
		id_list = db.get_sales_bind_esl_list(item['salesno'])
	else:
		for ids in item.get("esllist", []):
			eslid = ids.get("eslid", None)
			if not eslid:
				continue
			ids.pop("apid", None) #绑定关系里不同步基站
			if 'template' in ids: #更新模板
				try:
					if ('HS_EL_51' not in all_info[eslid]['op3'] and 'HS_EL_53' not in all_info[eslid]['op3']) \
							and ids['template'] == 'UNBIND': #老断码价签解绑定
						ids['data_cmd'] = 'CMD_UNBIND'
					else:
						ids['op4'] = ids['template']
						if 'unbind' not in ids['op4'].lower():#但是解绑模板不需要保存进数据库
							esl_update_list[eslid] = {'eslid': eslid, 'op4':ids['op4']}
				except Exception, e:
					esl_init.log.warning("get eslid %s info error", eslid)

			all_info[eslid].update(ids) #更新价签信息
			id_list.append(eslid)
	
	return id_list

def get_acks(db, item, id_list, all_info, cancel_esl_list):
	from core import is_id_ok
	from util.const import SUCCESS
	from util.func import check_esl

	ack = []
	for id1 in id_list:
		apid = all_info[id1].get('apid', "-1")
		status = 'waitting'
		#提前检测更新不了的情况
		if (apid == "-1"): #绑定关系不存在
			esl_init.log.warning("eslid %s have not bind ap" % id1)
			cancel_esl_list.append(id1)
			status = 'binderror'
			#绑定关系不对
		elif all_info[id1].get('salesno', None) != item['salesno']:
			esl_init.log.warning("eslid %s not bind to salesno %s" % (id1, item['salesno']))
			cancel_esl_list.append(id1)
			status = 'binderror'
		else: #价签不存在、属性错误、或者模版错误
			all_info[id1].update(item) #更新价格信息
			if (check_esl(db, id1)["bak"] != SUCCESS) or (not is_id_ok(all_info, id1)):
				status = 'eslerror'
				cancel_esl_list.append(id1)
				esl_init.log.warning("eslid %s info error" % id1)
				db.set_last_status_without_commit(db.esl, id1, time.asctime(), "offline")
			if (not is_info_ok(id1, all_info[id1])):
				status = 'dataerror'
				cancel_esl_list.append(id1)
				esl_init.log.warning("eslid %s info error" % id1)
				db.set_last_status_without_commit(db.esl, id1, time.asctime(), "offline")

		ack.append({'status': status, 'apid':apid, 'eslid':id1, 'starttime':time.time()})

	acks = {'sid':item['sid'], 'salesno':item['salesno'], \
		'status':'waitting','ack':ack}
	
	return acks

def add_to_update(id_list, item, all_info, update_dict, wait_update_dict, acks, cancel_esl_list, esl_priority):
	from core import is_esl_in_process 

	for id1 in id_list:
		#如果价签已经在wait队列中
		if id1 in wait_update_dict: 
			id1, info, old = wait_update_dict.pop(id1)
			for ack in old['ack']:
				if ack['eslid'] == id1:
					ack['status'] = 'cancel'
					esl_init.log.info('cancel %s prov update; %s' % (id1, old))
					is_finished, v, remove_list = check_is_finished_one(old, update_dict, wait_update_dict)
					if is_finished:
						reply_ack("UPDATA_ACK", [v], None)
					break
		#如果价签已经在刷新过程中
		if is_esl_in_process(id1): 
			esl_init.log.info("esl %s is in process, wait for it" % id1)
			wait_update_dict[id1] = (id1, all_info[id1], acks)
			priority = get_update_priority(item)
			if priority < esl_priority.get(id1, 15): #如果价签已经在busy中，但是优先级较现在低，则提高它的优先级
				esl_priority[id1] = priority
			cancel_esl_list.append(id1)
			continue
		#如果还有未开始的任务，直接设置为结束
		if id1 in update_dict:
			for old in update_dict[id1]['ack']:
				if old['eslid'] == id1:
					old['status'] = 'cancel'
					esl_init.log.info('cancel %s prov update; %s' % (id1, update_dict[id1]))
					is_finished, v, remove_list = check_is_finished_one(update_dict[id1], update_dict, wait_update_dict)
					update_dict[id1] = acks
					if is_finished:
						reply_ack("UPDATA_ACK", [v], None)
					break
		else:	#登记新的更新任务, 有可能多个价签共享一个ack
			update_dict[id1] = acks

		esl_priority[id1] = get_update_priority(item)  #默认更新级别为5

def get_update_priority(item):
	try:
		p = item.get('priority', 15)
		p = int(p)
	except ValueError, e:
		esl_init.log.warning("priority error, set to 15; %s" % item)
		p = 15
	except TypeError, e:
		p = 15
		esl_init.log.warning("priority error, set to 15; %s" % item)
	
	if p < 0 or p > 99:
		p = 15
		esl_init.log.warning("priority error, set to 15; %s" % item)

	return p
	
def get_new_update(db, buf_in_queue, update_in_queue, update_dict, esl_priority, wait_update_dict):
	from core import is_esl_in_process 

	sales_update_list = {}
	esl_update_list = {}
	esl_id_list = []
	all_info = {}
	cancel_esl_list = []

	#发送缓存的更新
	for id1 in wait_update_dict.keys():
		if is_esl_in_process(id1):
			continue
		id1, info, acks = wait_update_dict[id1]
		esl_init.log.info("pop wait for id: %s, %s" % (id1, acks))
		update_dict[id1] = acks
		update_in_queue.put((id1, info))
		wait_update_dict.pop(id1, None)
		db.set_last_status_without_commit(db.esl, id1, time.asctime(), "waiting")

	#从Q里面取更新
	while not buf_in_queue.empty():
		args, all_info_one = buf_in_queue.get()	
		all_info.update(all_info_one)

		for item in args:
			#获取待更新的价签ID
			id_list = get_id_list(db, item, esl_update_list, all_info)
			#如果id_list为空
			if not id_list or len(id_list) == 0:
				reply_ack("UPDATA_ACK", [{"sid":item['sid'], 'salesno':item['salesno'],\
						'status':'invalid', 'ack':[]}], None)
				continue

			sales_update_list[item['salesno']] = item
			esl_id_list.extend(id_list)

			#更新更新状态表
			try:
				acks = get_acks(db, item, id_list, all_info, cancel_esl_list)
			finally:
				db.commit()
				
			add_to_update(id_list, item, all_info, update_dict, \
						wait_update_dict, acks, cancel_esl_list, esl_priority)


	#更新本地商品数据库
	db.list_updata(db.sales, sales_update_list.values())
	db.list_updata(db.esl, esl_update_list.values())

	#发送到core处理
	try:
		for id1 in set(esl_id_list):
			if id1 in cancel_esl_list:
				continue
			info = all_info[id1]
			update_in_queue.put((id1, info))
			db.set_last_status_without_commit(db.esl, id1, time.asctime(), "waiting")
	finally:
		db.commit()
	
def process(task_data):
   '''
   负责从数据源解析处待更新的价签ID，缓冲一组发送到in_queue
   并从out_queue读取处理结果
   '''

   esl_init.log.info("updata_process starting")
   lowpower_warning = int(conf.htp.lowpower_warning)
   check_last_status_fast(task_data, lowpower_warning)
   buf_in_queue = task_data['updata']['buf_in_queue']
   is_parent_enable = conf.system.parent_enable.lower() == 'yes'

   timeout = 0

   xml_server = get_xmlserver()

   db = DB()
   update_dict = task_data['updata']['updata_dict']
   update_in_queue = task_data['updata']['in_queue']
   updata_out_queue = task_data['updata']['out_queue']
   esl_priority = task_data['esl_priority']
   wait_update_dict = {}

   try:
      import socket
      while True:
         #监听待更新的数据
         get_new_update(db, buf_in_queue, update_in_queue, update_dict, esl_priority, wait_update_dict)
         ack, blist = check_is_finished(db, updata_out_queue, update_dict, wait_update_dict, task_data['esl_power_info'])
         for k in ack:
            reply_ack("UPDATA_ACK", [k], None)
         if blist:
            xml_server.send_cmd("BIND", blist)
         time.sleep(1)

         if task_data['isquit']['updata']:
            break
   except xmlrpclib.Fault as err:
      if not task_data['isquit']['updata']:
         esl_init.log.error_msg('Fault: Code %s, String %s'% (err.faultCode, err.faultString), errid='EUP0002')
   except xmlrpclib.ProtocolError as err:
      if not task_data['isquit']['updata']:
         esl_init.log.error_msg('ProtocolError: headers %s, Code %s, Msg %s'\
              % (err.headers, err.errcode, err.errmsg), errid='EUP0003')
   except socket.error,e:
      if not task_data['isquit']['updata']:
         esl_init.log.error_msg('socket error:%s' % e, errid='EUP0004')
   except Exception, e:
      esl_init.log.error_msg("updata process:%s" % e, errid='EUP0005')
      print_except()
   finally:
		db.commit()

   esl_init.log.info("updata_process exit")
#-----------------------------------------------
#-----------------------------------------------
#-----------------------------------------------
#-----------------------------------------------

def fetch_one_item(ids, db):
   '''
   根据输入的价签id清单，返回每个价签id对应的id号、屏幕类型、其对应的商品信息，返回值是一个迭代器
   '''
   #可选的空值表
   for id1 in ids:
      try:
         salesno = db.get(id1)['salesno']
         op5 = db.get(id1)['op5']	
         if not op5:
             esl_init.log.warning('%s : op5 is None please check database!'%id1)
         try:
             op5 = eval(op5,{},{})
             op3 = op5['screen_type']
         except Exception,e:
             esl_init.log.warning("%s : op5 is illegal,%s  "%(id1,e))
             esl_init.log.warning("op5's value is : %s "%op5)
             raise KeyError #为了让下边的except捕捉到
         op4 = db.get(id1)['op4']
         item = db.get(id1)
      except Exception, e:
         yield None, None, None
      else: #将可选的空值置0
         yield id1, op3, item


def check_valid_num(ids, db):
   n = 0
   for id1, op3, item in fetch_one_item(ids, db):
      if None in [id1, op3, item] or item['Price'] == None:
         esl_init.log.warning("get esl info from db failed: %s" % id1)
         continue
      n += 1
   return n

seg_cmd_arr = {"CMD_UPDATE":0, "CMD_UNBIND":1, "CMD_QUERY":2, "CMD_NETLINK":3}

def split_lcd_data(data, ids):
	num, offset = 0, 0
	data_area, ok_esl = [], []

	esl_num = len(ids)

	s = struct.unpack_from
	l = struct.calcsize
	del ids[:]

	data_len = len(data)

	while (offset < data_len):
		(eslid, ) = s('>I', data, offset)
		
		offset += l('>I')

		(lens, ) = s('I', data, offset)
		offset += l('I')

		e = list(str(hex(eslid)).upper()[2:])
		e.insert(2,'-')
		e.insert(5,'-')
		e.insert(8,'-')
		e = ''.join(e)
		if "L" in e:
			e = e[0:-1]

		ids.append(e) #扩展ID
		offset += lens

def seg_updata_data_area(db, ids, exe_file):
   '''
   段码价签协议数据生成函数
   调用exe_file生成HTP数据包中的data_area部分
   如果exe_file标准错误输出有输出，则将其输出记录到esl_init.log.
   '''
   flags = 0
   data_area = None
   failed_list = []

   op3 = db[ids[0]]['op3']

   exe_name_args = get_args(exe_file, 4, is_osd = False)

   try:
      fifo = subprocess.Popen(exe_name_args, stdin = subprocess.PIPE, 
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              bufsize = -1,)

      #T = get_seg_json("./config/esl_conf.ini")

      s_data = ''
      #输入数据格式为[2B len][1B esl_type][4B id][各个屏幕的自定义类型]
      for id1, esl_type, item in fetch_one_item(ids, db):
         if None in [id1, esl_type, item]:
            failed_list.append(id1)
            continue
         cmd = db[id1]['data_cmd']

         item['util'] = Util()

         T0 = _init_esl_json("./config/esl_conf.ini", is_epd = False)
         L0 = _init_esl_json("./config/template_led_rc.json", is_epd = False)

         try:
            T = json.loads(T0.merge(item))
            L = json.loads(L0.merge(item))
            T.update(L)
         except Exception, e:
            print_except()
            failed_list.append(id1)
            esl_init.log.warning("load or apply template for %s failed" % id1)
            continue

         if op3 == 'HS_EL_5300' and (cmd == "CMD_UPDATE" or cmd == 'CMD_UNBIND'):
            try:
               v = lcd_decode.send_seg_data(item, T)
               if v == None:
                  raise KeyError, "error of eslid %s" % id1
               s_data += v
            except KeyError, e:
               failed_list.append(id1)
               print_except()
            except TypeError, e:
               failed_list.append(id1)
               print_except()
            except ValueError, e:
               failed_list.append(id1)
               print_except()
            continue
         			
         if cmd == 'CMD_QUERY' or cmd == 'CMD_UNBIND' or cmd == 'CMD_SET_CMD':
            flags = 1
         if cmd == 'CMD_SET_CMD': #set cmd伪装成查询下去
            cmd = 'CMD_QUERY'

         cmd = seg_cmd_arr.get(cmd, 0)
         try:
            s_1 = struct.pack('>IBBBB16s',int(id1.replace('-', ''), 16), \
				   cmd, 0,0,0, str(esl_type))
            item['esl_type'] = esl_type
            s_1 += seg_updata_data_from_template_new(item, fifo, db, id1, flags, T)

            s_data += s_1
         except Exception, e:
            failed_list.append(id1)
            print_except()

      #先输入2字节的更新个数
      fifo.stdin.write(struct.pack('<H', len(ids) - len(failed_list)))
      fifo.stdin.write(s_data)

      data_area, err = fifo.communicate()
      #esl_init.log.info( "epd ret: %s", b2a_hex(data_area))
      split_lcd_data(data_area, ids)

      if err != '':
         esl_init.log.debug("%s:%s" % (exe_file, err))
   except Exception, e:
      esl_init.log.error_msg( "seg_updata_data_area, %s, %s" % (exe_file, e), errid='EUP006')
      print_except()
   finally:
		try:
			fifo.terminate()
		except Exception, e:
			pass

   return data_area, failed_list

def empty_with_zero_func(nothing):
	ret = dot_temp.check_price(nothing)
	if ret == '0.00':
		return ' '
	return ret

def empty_func(nothing):
	return ' '

price_fun_table = \
{"check_price":dot_temp.check_price,"check_price_int_str":dot_temp.check_price_int_str,"int":int,"str":str,\
"empty":empty_func,"empty_with_zero": empty_with_zero_func}

def func_nothing_s(nothing):
   return "0"

def func_nothing_int(nothing):
   return 0


#传入参数格式为 模板的flags标志
#输出标志合成的16位（unsigned short）类型数据
def parse_flag(temp_flags,mapping):
   data = 0
   for sf in temp_flags:
       data += 1 << mapping[sf]
   return data

def seg_updata_data_from_template_new(id1,fifo,db,esl_id,flags,T):
   count = 0
   esl_type = str(id1['esl_type'])

   s_data = ''
   
   temp_name = db.get(esl_id)['op4']	
   if (not temp_name) or temp_name not in T[esl_type] or 'title' not in T[esl_type][temp_name]:
      esl_type = "default_temp"
      temp_name = "normal"
      if flags != 1:
      	esl_init.log.warning("set default template for esl %s", esl_id)		
   count = len(T[esl_type][temp_name]['title'])
   if count > 8:
      raise KeyError,"updata.py : seg data fields > 8"
   
   for title in T[esl_type][temp_name]['title']:
      f = T[esl_type][temp_name][title]['format']
      f = str(f)# win7用struct.pack()时，如果f是unicode会出现错误,json默认解析出来的都是unicode
      c = price_fun_table[T[esl_type][temp_name][title]['check_fun']]
      l = T[esl_type][temp_name][title]['maxlen']
      
      if title == 'NONE':
         s_data += struct.pack(f, '0')
         continue
      if flags == 1:
         c = func_nothing_s
         s_data += struct.pack(f, "0")
      else:
      	s_data += struct.pack(f, c(id1[title])[-l:])
   for x in range(8-count):
      s_data += struct.pack(f, '0')

   temp_flags =  T[esl_type][temp_name]['flags']['flag']
   mapping = T["seg_display_propertis"][esl_type]
   data = parse_flag(temp_flags,mapping)
   s_data += struct.pack('H', data)

   return s_data

def split_dataarea(data, ids, is_first):
	'''解析从OSD返回的数据，分为data_ara和ack 2部分'''
	'''esl_num, [esl_id, len, data], esl_num, [eslid, ack]'''
	num, offset = 0, 0
	data_area, ok_esl = [], []
	global osd_next_data_cache

	esl_num = len(ids)

	s = struct.unpack_from
	l = struct.calcsize
	del ids[:]

	data_len = len(data)

	#for i in range(esl_num):
	while (offset < data_len):
		eslid, ack = s('>IB', data, offset)
		offset += l('>IB')

		e = list(str(hex(eslid)).upper()[2:])
		e.insert(2,'-')
		e.insert(5,'-')
		e.insert(8,'-')
		e = ''.join(e)
		if "L" in e:
			e = e[0:-1]

		if ack == 1: #通讯成功
			ok_esl.append(e)
			continue
		#通讯失败
		num1 = s("H", data, offset)[0]
		offset += l('H')
		lens = s("I", data, offset)[0]
		offset += l('I')
		ids.extend([e]*num1) #扩展ID
		num += num1
		d = s("%ss" % (lens), data, offset)[0]

		data_area.append(d)
		offset += lens

		if not is_first: #只有第二次的结果才需要存储
			osd_next_data_cache[e] = (num1, d)
	
	return data_area, ok_esl

def get_op5_dire(eslinfo):
	op5 = eslinfo['op5']	
	dire = eslinfo['op9']
	id1 = eslinfo['eslid']
	try:
		op5 = eval(op5,{},{})
	except Exception,e:
		esl_init.log.warning("op5 is illegal of %s ,please check it %s", id1, e)
		op5 = {}

	try:
		dire = int(dire)
		if dire > 3:
			esl_init.log.warning("dire %s is illegal of %s, please check it, use default value 0", id1, dire)
			dire = 0
	except Exception, e:
		dire = int(op5.get('resolution_direction', 0))
		esl_init.log.warning("dire is illegal of %s, please check it, use default value %s from op5", id1, dire)
	
	return op5, dire

osd_next_data_cache = {}
def check_osd_finished(db, ids, exe_file, ack_comp, mode):
	last_ack = {}
	ids_temp, ids_temp_bak = [], []
	for id1 in ack_comp:
		ids_temp.append(id1)
		ids_temp_bak.append(id1)
		for i in xrange(len(ack_comp[id1])):
			last_ack.setdefault(id1, []).append(ack_comp[id1][i])
	_, ok_eslid, _= dot_updata_data_area_osd(db, ids_temp, exe_file, last_ack, MODE = mode, is_first = False)
	
	for id1 in ids_temp_bak:
		if id1 not in ids_temp:
			try:
				ack_comp[id1] = {0:0}
			except KeyError, e:
				pass

	return ok_eslid

def fetch_data_area_from_cache(ids, is_first, max_package):
	#先从cache里面取出已有的data_area
	global osd_next_data_cache
	data_area_cache, ids_cache = [], []

	for id1 in osd_next_data_cache.keys():
		if id1 in ids:
			num, data_area = osd_next_data_cache[id1]
			if len(ids_cache) + num > max_package:
				break
			osd_next_data_cache.pop(id1)
			if is_first:
				data_area_cache.append(data_area)
				ids_cache.extend([id1] * num)
				ids.remove(id1)
	return data_area_cache, ids_cache

def get_osd_args(args, used_num):
	freen = int(args[2]) - used_num
	args[2] = str(freen)
	return freen

def get_args(exe_file, mode, is_osd = False):
	exe_name_args = []

	if (int(mode) != 4):
		if is_osd:
			args = conf.htp.osd_args
		else:
			args = ''
	else:
		if is_osd:
			args = conf.htp.osd_args_v2
		else:
			args = conf.htp.lcd_args_v2
	_args = args.split()

	exe_name_args.append(exe_file)
	for x in _args:
		exe_name_args.append(x.upper())
	
	return exe_name_args

def dot_updata_data_area_osd(db, ids, exe_file, last_ack, MODE = 0, is_first = True):
   '''OSD传输模式，last_ack格式为[(id1,ack_num,[ack_val]),...]'''
   data_area, err, ok_list, failed_list = None, None, [], []
   name_del = []
   data_area_cache, ids_cache = [], []

   exe_name_args = get_args(exe_file, MODE, is_osd = True)

   try:
      if is_first: #只有第一次调用才可能需要从cache里拿
         data_area_cache, ids_cache = fetch_data_area_from_cache(ids, is_first, exe_name_args[2])
      if is_first and (get_osd_args(exe_name_args, len(ids_cache)) <= 0 or len(ids) == 0):
         del ids[:]
         raise ZeroDivisionError, "all use cache"

      fifo = subprocess.Popen(exe_name_args, stdin = subprocess.PIPE, 
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              bufsize = -1,)

      ret = conf.system.temp_json.upper()

      if ret == "NO": #如果是json模板将不再检测
      	TEMP = _init_esl()  
		
      s_data = []
      for id1, _, item in fetch_one_item(ids, db):
         eslinfo = db.get(id1)
         temp_name = eslinfo['op4']	
         op5, dire = get_op5_dire(eslinfo)
         try:
            if ret == 'YES':
               s =  osd.send_dot_info_json(fifo, id1, temp_name, item , op5, dire)
            else:
               s =  osd.send_dot_info(fifo, id1, temp_name, item , op5, dire, TEMP)
         except Exception, e:
            print_except()
            failed_list.append(id1)
         else:
			   s_data.extend(s)
				 
		#发送模板数据
      fifo.stdin.write(struct.pack('H', len(ids) - len(failed_list)))
      fifo.stdin.write(''.join(s_data))
		#发送上一次通讯的ACK值
      fifo.stdin.write(struct.pack('H', len(ids)))
      #上一次的ACK
      for id1 in ids:
            #esl_init.log.info("last ack:%s, %s, %s" % (id1, len(last_ack[id1]), last_ack[id1]))
            osd.dot_ack(fifo, id1, last_ack[id1])

      data_area, err = fifo.communicate()
      #esl_init.log.info( "0 epd ret: %s", b2a_hex(data_area))
      if data_area:
        if "LOG_ON" in exe_name_args:  
            osd_output(data_area, len(ids)) #for debug
        data_area, ok_list = split_dataarea(data_area, ids, is_first)
        #esl_init.log.info( "1 epd ret: %s", b2a_hex(''.join(data_area)))
      else:
         esl_init.log.debug("osd decode error, %s, ret:%s" % (exe_file, data_area))
   except ZeroDivisionError, e:
       pass
   except KeyError, e:
       print_except()
       esl_init.log.warning("%s ,  check template file"%e)
   except ValueError, e:
       print_except()	
       esl_init.log.warning("%s  check database" %e)
   except Exception, e:
      print_except()
      esl_init.log.warning("dot_updata_data_area: %s, %s" % (exe_file, e))
   finally:
		try:
			fifo.terminate()
		except Exception, e:
			pass
   if err:
      esl_init.log.debug("%s" % err)
   
   if data_area:
      data_area_cache.extend(data_area)
   if data_area_cache:
      data_area = ''.join(data_area_cache)
   if ids_cache:
      ids.extend(ids_cache)
   #esl_init.log.info( "2 epd ret: %s", b2a_hex(data_area))
   return data_area, ok_list, failed_list

def action(groups):
   '''
   负责处理一组价签更新操作，传入参数格式为(apid, chn, nw1, [ids,...])
   返回格式为 [(id, ack), (id, ack),...]
   '''
   #根据型号选择是采用段码更新程序还是点阵更新程序
   _, _, _, _, ids, _, _, flags, _, db = groups
   nw4_val = get_nw4_val(db, ids[0])

   cmd_val = "UPDATA"
   if "OSD" in flags and nw4_val != 'NORMAL':
      cmd_val = "OSD"
   htp_task(groups, nw4_val, cmd_val)

