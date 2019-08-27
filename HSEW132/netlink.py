# encoding: utf-8

import multiprocessing, subprocess, time, struct, os, platform, threading, pprint, codecs, copy
from htp import htp_task, ack_ok, ack_low_power, check_real_low_power, get_apid_from_ack
from esl_init import conf, print_except, trace
import esl_init, core, heartbeat
from database import DB
import cPickle as pickle
from operator import itemgetter
import bind, xmlserver
from copy import deepcopy
from threading import Timer
from binascii import b2a_hex
from random import choice

retry_time_max = 6 #组网固定6次

failed_netlink = {}

def start(task_data):
	'''启动组网进程并返回进程对象'''
	proc = threading.Thread(target = process, args = (task_data,))
	proc.start()
	return proc

def process_netlink_ack(ok_ret, id_para, db, task_data):
	ids_list = []

	for (ids, ret_old) in ok_ret:
		if ids not in id_para:
				return 
		wid, chn, step, netid, setchn, grpchn = id_para[ids]
		# 如果查询成功，更新价签无线通信参数
		if step == 'query': # 查询成功
			if query_ack_ok(ret_old) or netlink_ack_ok(ret_old) or query_ack_low_power(ret_old):
				db.change_esl_rfpara_without_commit(ids, wid, chn, netid, setchn, grpchn)
				ids_list.append(ids)
				save_netlink_data_to_db(db, ids, id_para)

	if ids_list:
		# 每次组网任务结束都保存一次数据库并发送一次价签信息给上层
		esl_change_list = []
		db.commit()
		for ids in ids_list:
			id_para.pop(ids, 'not found!')
			if db.has_key(db.esl, ids):
				esl_info = db.get_all_info(db.esl, ids)
				bind_info = db.get_all_info(db.bind, ids)
				esl_info.update(bind_info)
				if ids in task_data['all_info']: #如果组网成功，则需要更新正在更新中的价签信息
					task_data['all_info'][ids].update(esl_info)
					core.yield_one_item_cache.pop(ids, None)
					task_data['rf_para_is_changed'][ids] = 1

				esl_change_list.append({"eslid":ids, \
					"nw1":esl_info["nw1"], "nw3":esl_info["nw3"]})

		#将价签注册信息置为实效
		heartbeat.is_man_updata(esl_change_list, task_data['esl_info'])

def process(task_data):
	'''
	负责从数据源解析处待组网的价签ID，缓冲一组发送到in_queue
	并从out_queue读取处理结果
	'''
	esl_init.log.info("netlink_process starting")
	db = DB()
	# 启动生成组网价签任务
	in_queue = task_data['netlink']['in_queue']
	out_queue = task_data['netlink']['out_queue']
	id_para = task_data['netlink']['rf_para']

	xml_server = bind.get_xmlserver()

	try:
		while True:
			while not out_queue.empty():
				(ids, ret_old) = out_queue.get()
			time.sleep(1)
			if task_data['isquit']['netlink']:
				break
	except Exception, e:
		esl_init.log.error_msg("netlink process:%s" % e, errid='ENE001')
	
	esl_init.log.info("netlink is quit")

def action(groups):
	'''
	负责处理一组组网数据，需要按照基站、信道、nw1进行分组，然后并发执行，并返回ack列表
	返回格式为 {id: ack, id : ack,...}
	'''
	htp_task(groups, "NORMAL", "NETLINK")

def check_valid_num(ids, db):
   n = 0
   for id1, op3 in fetch_one_esl_type(ids, db):
      if None in [id1, op3]:
         esl_init.log.error_msg("get esl info from db failed: %s" % id1, errid='ENE002', eslid=id1)
         continue
      n += 1
   return n

def fetch_one_esl_type(ids, db):
   '''
   根据输入的价签id清单，返回每个价签id对应的id号和屏幕类型，返回值是一个迭代器
   '''
   #可选的空值表
   for id1 in ids:
      try:
         op5 = db.get(id1)['op5']
         op5 = eval(op5,{},{})
         op3 = op5['screen_type']
      except Exception, e:
         yield None, None
      else: #将可选的空值置0
         yield id1, op3

def send_netlink_data_v3(cmd, id1, para, fifo, esl_type):
	wakeupid, chn, _, netid, setchn, grpchn = para[id1]
	s_data = ''

	s_data += struct.pack('>IBBBB16s',int(id1.replace('-', ''), 16), \
		cmd, 0,0,0,str(esl_type))

	s_data += struct.pack('>I', int(wakeupid.replace('-', ''), 16))
	s_data += struct.pack('>I', int(id1.replace('-', ''), 16))
	s_data += struct.pack('BBBB', int(setchn), int(grpchn), int(chn), int(netid))
	s_data += struct.pack('%ds' % (16*8+2-12), '')
	
	return s_data

def esl_netlink_data_area(db, ids, para, exe_file):
   '''
   价签组网协议数据生成函数
   调用exe_file生成HTP数据包中的data_area部分
   如果exe_file标准错误输出有输出，则将其输出记录到esl_init.log.
   '''

   from updata import seg_cmd_arr, split_lcd_data

   flags = 0
   data_area = None
   s_data = ''
   failed_list = []

   try:
      fifo = subprocess.Popen(exe_file, stdin = subprocess.PIPE, 
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              bufsize = -1,)
		
      #输入数据格式为[2B len][1B esl_type][4B id][各个屏幕的自定义类型]
      for id1, esl_type in fetch_one_esl_type(ids, db):
         if None in [id1, esl_type]:
            failed_list.append(id1)
            continue
         try:
            s_1 = ''

            if 'HS_EL_53' not in esl_type:
               wakeupid, chn, _, netid, setchn, grpchn = para[id1]
               s_1 += struct.pack('>I16s', int(id1.replace('-', ''), 16), str(esl_type))
               s_1 += struct.pack('>IB', int(wakeupid.replace('-', ''), 16), int(chn))
               s_1 += struct.pack('B', int(netid))
               s_1 += struct.pack('6s', '')
            else:
               cmd = seg_cmd_arr.get(db[id1]['data_cmd'], 0)
               s_1 += send_netlink_data_v3(cmd, id1, para, fifo, esl_type)
            s_data += s_1
         except Exception, e:
            esl_init.log.error_msg("%s info error %s" % (id1, e), errid='ENE003', eslid=id1)
            failed_list.append(id1)

      #先输入2字节的组网个数
      fifo.stdin.write(struct.pack('<H', len(ids) - len(failed_list)))
      fifo.stdin.write(s_data)
      data_area, err = fifo.communicate()
      split_lcd_data(data_area, ids)
      #esl_init.log.info( "epd ret: %s", b2a_hex(data_area))

      if err != '':
         esl_init.log.error_msg("%s:%s" % (exe_file, err), errid='ENE004')
   except Exception, e:
      print_except()
      esl_init.log.error_msg("esl_netlink_data_area, %s, %s" % (exe_file, e), errid='ENE005')
   return data_area, failed_list

def check_ack(group_list, ack_list, netlink_data, db, retry_max_of_eslid, task_data):
	# 根据分组情况和ack情况，确定价签是否被组网成功

	from xmlserver import reply_ack
	from core import set_id_notbusy

	max_retry_times = 3 * 2
	timer_list = []

	ok_ret = []
	
	for id1, ack in ack_list:
		id1 = id1.upper()
		ap = get_apid_from_ack(ack)
		
		if id1 not in netlink_data['ap_check_list']:
			continue # 说明分区域并行的时候，某个基站已经找到了这个价签，并将之删除了

		netlink_data['work_list'][id1] += 1
		flag = False
		wid, chn, step, netid, setchn, grpchn = netlink_data['rf_para'][id1]
		
		if step == 'query':
			if query_ack_ok(ack) or query_ack_low_power(ack):
				flag = True # 查询成功
			else:
				netlink_data['rf_para'][id1] = (wid, chn, 'netlink', netid, setchn, grpchn)
		else:
			netlink_data['rf_para'][id1] = (wid, chn, 'query', netid, setchn, grpchn)
			if netlink_ack_ok(ack) or netlink_ack_low_power(ack):
				flag = True # 组网成功
		
		if flag:
			netlink_data['ap_check_list'].pop(id1, None)
			netlink_data['work_list'].pop(id1, None)
			netlink_data['out_queue'].put((id1,ack))

			ok_ret.append((id1, ack))

			retry_max_of_eslid.pop(id1, None)
			set_id_notbusy(id1)

			failed_netlink.pop(id1, None)
			db.increace_status(id1, ["netlink_times"])

			reply_ack("ESL_NETLINK_ACK", [{"eslid":id1, "nw1":wid, "nw3":chn, "op2":netid, 
					"setchn":setchn, "grpchn":grpchn, "status":"OK"}], None)
			esl_init.log.info("netlink for %s success" % id1)
		else: #
			core.check_need_roaming(db, id1, task_data['all_info'], netlink_data, task_data, ack)

			if netlink_data['work_list'][id1] >= max_retry_times:
				netlink_data['ap_check_list'].pop(id1, None)
				netlink_data['work_list'].pop(id1, None)
				set_id_notbusy(id1)
				netlink_data['out_queue'].put((id1, ack))
				retry_max_of_eslid.pop(id1, None)
				esl_init.log.warning("netlink for %s failed" % id1)
				reply_ack("ESL_NETLINK_ACK", [{"eslid":id1, "nw1":wid, "nw3":chn, "op2":netid, 
						"setchn":setchn, "grpchn":grpchn, "status":"failed"}], None)
				salesno = task_data['all_info'][id1].get("salesno", "NONE")
				netlink_data['rf_para'].pop(id1, 'not found!')
				db.increace_status(id1, ["netlink_times"])

				timer_list.append((id1, wid, chn))
		
	process_netlink_ack(ok_ret, netlink_data['rf_para'], db, task_data)
	start_timer_for_netlink(timer_list)

	#esl_init.log.info("rf_para: %s" % netlink_data['rf_para'])

def start_timer_for_netlink(timer_list):
	#组网失败后重试
	if conf.htp.auto_retry_after_failed.lower() != 'yes':
		return
	
	job= {}
	retry_time_interval = conf.htp.retry_time_interval

	for (id1, wid, chn) in timer_list:
		if id1 not in failed_netlink:
			failed_netlink[id1] = 0
		else:
			failed_netlink[id1] += 1

		sec_table = retry_time_interval
		if failed_netlink[id1] >= len(sec_table):
			failed_netlink.pop(id1)
		else:
			try:
				sec = int(sec_table[failed_netlink[id1]])
				job.setdefault(sec, []).append((id1, wid, chn))
			except Exception, e:
				esl_init.log.warning("try to netlink failed for %s, %s" % (id1, e))
	
	for sec in job:
		args = [{"eslid":i[0], "nw1":i[1], "nw3":i[2], "retry":"1"} for i in job[sec]]
		try:
			Timer(sec, retry_netlink_timer, args).start()
			esl_init.log.info("will try to netlink %s after %s sec" % (args, sec))
		except Exception, e:
			esl_init.log.error_msg("try to netlink failed for %s, %s" % (args, e), errid="ENE006")

def retry_netlink_timer(args):
	try:
		xml_server = bind.get_xmlserver()
		xml_server.send_cmd("ESL_NETLINK", [args])
	except Exception, e:
		esl_init.log.error_msg("retry_netlink_timer failed %s, %s" % (e, args), errid='ENE007')

def load_netlink_buf():
	netlink_buf = {}
	try:
		f = open("log/netlink_buf.pkl", "r")
		netlink_buf = pickle.load(f)
		f.close()
	except Exception, e:
		pass

	#去重
	rf_para = {}
	for i in netlink_buf.keys():
		rf_para.setdefault(i, netlink_buf[i])

	return rf_para

def save_netlink_buf(netlink_list):
	rf_para = {}
	for i in netlink_list.keys():
		rf_para.setdefault(i, netlink_list[i])
	f = open("log/netlink_buf.pkl", "w")
	pickle.dump(rf_para, f)
	f.close()

def alloc_netlink_data(id_para, in_queue):
	rf_para = load_netlink_buf()
	for i in rf_para.keys():
		id_para.setdefault(i, rf_para[i])
	
	for i in id_para.keys():
		wid, chn, step, netid = id_para[i]
		if step != 'netlink':
			id_para[i] = (wid, chn, 'netlink', netid)
		in_queue.put(i)

def netlink_ack_ok(ack1):
	(_, _, ack, cmd) = ack1
	if ack == 1:
		return True
	return False

def netlink_ack_low_power(ack1):
	(_, _, ack, cmd) = ack1
	if ack == 0x2:
		return True
	return False

def query_ack_ok(ack1):
	(_, _, ack, cmd) = ack1
	if (((ack & 0xF0) >> 4) == 0x1 or (ack & 0x0F) == 0x1):
		return True
	return False

def query_ack_low_power(ack1):
	(_, _, ack, cmd) = ack1
	if (((ack & 0xf0) >> 4) == 0x2 or (ack & 0x0F) == 0x2):
		return True
	return False

def load_and_set_netlink_data_to_db(db, eslid, nw1, nw3, setchn, grpchn):
	try:
		try:
			info = db.get_one(db.esl, eslid)
			op3 = info['op3']
			op6 = info['op6']
			op6 = eval(op6,{},{})
		except Exception, e:
			op6 = {}
			op3 = ''

		if is_g2g3_op3(op3): #二三代价签不需要保留组网参数
			return nw1, nw3, setchn, grpchn

		if 'new_nw1' in op6 and 'new_nw3' in op6 and 'new_setchn' in op6 and 'new_grpchn' in op6 \
				and (op6['new_nw1'] != nw1 or op6.get('new_nw3') != nw3 or \
				op6['new_setchn'] != setchn or op6['new_grpchn'] != grpchn):
			esl_init.log.info("%s prov netlink failed, use the prov para: %s,%s,%s,%s" % 
				(eslid, op6['new_nw1'], op6['new_nw3'], op6['new_setchn'], op6['new_grpchn']))
		nw1 = op6.get('new_nw1', nw1)
		nw3 = op6.get('new_nw3', nw3)
		setchn = op6.get('new_setchn', setchn)
		grpchn = op6.get('new_grpchn', grpchn)
		op6['new_nw1'] = nw1
		op6['new_nw3'] = nw3
		op6['new_setchn'] = setchn
		op6['new_grpchn'] = grpchn
		db.change_esl_op6_without_commit(eslid, op6)
	except Exception, e:
		esl_init.log.error_msg("load_and_set_netlink_data_to_db: %s" % e, errid='ENE008', eslid=eslid)
		return None, None, None, None
		
	return nw1, nw3, setchn, grpchn

def save_netlink_data_to_db(db, eslid, para):
	try:
		if eslid in para:
			op6 = db.get_one(db.esl, eslid)['op6']
			op6 = eval(op6,{},{})
			wid, chn, _, netid, setchn, grpchn = para[eslid]
			op6['wid'] = str(wid)
			op6['chn'] = str(chn)
			op6['setchn'] = str(setchn)
			op6['grpchn']  = str(grpchn)
			op6.pop("new_nw1", None)
			op6.pop("new_nw3", None)
			op6.pop("new_setchn", None)
			op6.pop("new_grpchn", None)
			db.change_esl_op6_without_commit(eslid, op6)
	except Exception, e:
		esl_init.log.error_msg("save_netlink_data_to_db: %s" % e, errid='ENE009', eslid=eslid)

def get_old_para(db, args):
	old = {}
	for item in args:
		eslid = item.get('eslid')
		if db.has_key(db.esl, eslid) and db.has_key(db.bind, eslid):
			e = db.get_one(db.bind, eslid)
			e1 = db.get_one(db.esl, eslid)
			old[eslid] = (e['apid'], e1['nw1'], e1['nw3'])
	
	return old

#初始化数据
def bind_list_init(db): 
	g = {}
	for (apid, wkid, chn, op3, count) in db.get_ap_bind_group(): 
		g.setdefault(apid, {}).setdefault(op3, {}).setdefault(wkid, {})[chn] = count
	return g #, last_bind_ap

def is_g2g3_op3(op3):
	if op3 in ['HS_EL_5104', 'HS_EL_5300', 'HS_EL_5301']:
		return True
	return False

def get_bind_nw1_nw3_3g(db, eslid, apid, g, has_bind_list, apset_cache): # 3代价签add
	
	if conf.htp.auto_netlink_after_bind.lower() != 'yes':
		return False, None, None, None, None
	
	e = db.get_one(db.esl, eslid)
	old_nw1, old_nw3, old_setchn, old_grpchn, old_op3, op6 = e['nw1'], e['nw3'], e['setchn'], e['grpchn'], e['op3'], e['op6']
	
	g1, nw1_nw3 = {}, {}
	if eslid in has_bind_list:  #从老组里减1，下面从新组里加1
		ap11, nw11, nw33 = has_bind_list[eslid]
		try:
			g[ap11][old_op3][nw11][nw33] -= 1
		except KeyError, e:
			pass
	
	#如果上一次组网失败，则继续使用上一次的参数进行组网
	op6 = eval(op6, {}, {})
	if "new_nw1" in op6 and (not is_g2g3_op3(old_op3)):
		esl_init.log.warning("%s prov netlink failed, use the prov para: %s,%s" % \
			(eslid, op6['new_nw1'], op6['new_nw3']))
		g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(op6['new_nw1'], {}).\
			setdefault(op6['new_nw3'], 0)
		g[apid][old_op3][op6['new_nw1']][op6['new_nw3']] += 1
		return True, op6['new_nw1'], op6['new_nw3'], op6['new_nw3'], op6['new_nw3']
		
	#找到同基站，同类型且有富余的所有组
	channel_list = conf.netlink.channel_list
	if apid in g:
		if old_op3 in g[apid]:
			for nw1 in g[apid][old_op3]:
				for nw3 in g[apid][old_op3][nw1]:
					if int(nw3) not in channel_list:
						continue
					count = g[apid][old_op3][nw1][nw3]
					nw1_nw3[(nw1, nw3)] = 1
					if int(count) < int(conf.netlink.group_num_max) and int(count) >= 0:
						g1[(nw1, nw3)] = count
	
	#再进行个数从高到低排序
	g1 = sorted(g1.iteritems(), key=lambda g1 : g1[1], reverse=True)

	#如果最多的1组和当前的一样多，则刨除当前的，使用前面的组信息
	#if len(g1) >= 2:
	#	((e1_nw1, e1_nw3), c1), ((e2_nw1, e2_nw3), c2) = g1[0], g1[1]
	#	if c1 == c2 and e1_nw1 == old_nw1 and e1_nw3 == old_nw3:
	#		g1.remove(((e1_nw1, e1_nw3), c1))
	
	for ((nw1, nw3), count) in g1:
		if nw1 == old_nw1 and nw3 == old_nw3 and count >= conf.netlink.group_num_max * 0.6:
			g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
			g[apid][old_op3][nw1][nw3] += 1
			return False, nw1, nw3, nw3, nw3 #存在同组的价签

	for ((nw1, nw3), count) in g1:
		#有一组可以容纳新的价签,使用组成员数最多的
		g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
		g[apid][old_op3][nw1][nw3] += 1
		is_changed = True if (old_nw1, old_nw3) != (nw1, nw3) else False
		return is_changed, nw1, nw3, nw3, nw3
	
	# 分配新的setid or group_id
	try:
		setid0 = g[apid][old_op3].keys()[0][0:2]
	except Exception, e:
		setid0 = old_nw1[0:2]

	cfg_txt = apset_cache
	for group_name in cfg_txt:
		if apid in cfg_txt[group_name].keys():
			nw3 = cfg_txt[group_name][apid][0]
			for setid_flag in cfg_txt[group_name][apid][1:]:
				for grpid_flag in ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18']:
					setid_flag = str(setid_flag)
					if len(str(setid_flag)) == 1:
						setid_flag = '0' + str(setid_flag)
					nw1 = setid0 + '-' + str(setid_flag) + '-' + grpid_flag + '-' + '66'
					try:
						#g由于是在xmlserver的构造函数中定义的，所以系统刚开始会为空(bind_list中没有值)
						if not g or apid not in g: 
							g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
							g[apid][old_op3][nw1][nw3] += 1
							is_changed = True if (old_nw1, old_nw3) != (nw1, nw3) else False
							return is_changed, nw1, nw3, nw3, nw3
						g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
						if nw1 in g[apid][old_op3].keys():
							count = g[apid][old_op3][nw1][nw3] 
							if int(count) < int(conf.netlink.group_num_max) and int(count) >= 0:
								g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
								g[apid][old_op3][nw1][nw3] += 1
								is_changed = True if (old_nw1, old_nw3) != (nw1, nw3) else False
								return is_changed, nw1, nw3, nw3, nw3
							else:
								continue
						else:
							g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
							g[apid][old_op3][nw1][nw3] += 1
							is_changed = True if (old_nw1, old_nw3) != (nw1, nw3) else False
							return is_changed, nw1, nw3, nw3, nw3
					except Exception, e:
						pass
		else:
			esl_init.log.info('Please check the apid %s config in set_list.ini file' % apid) 	

	return False, None, None, None, None
	
def get_bind_nw1_nw3_3g_test(db):
	
	t = "组网测试"

	eslid, old_nw1, old_chn = "55-55-55-99", "51-11-21-66", "158"
	esl_list = [{"eslid":"55-55-55-99", "setchn":old_chn, "grpchn":old_chn, "nw3":old_chn, 
							"nw1":old_nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]
	db.list_updata(db.esl, esl_list)
	set_list = {}
	apid = "1"
	g = {"1":
				{
					"HS_EL_5300": {
						old_nw1: {old_chn : 3, "40" : 5},
						"51-11-22-66": {"168" : 2, "40" : 5},
						},
					"HS_EL_5104": {
						"52-11-21-66": {old_chn : 2, "40" : 5},
						"52-11-22-66": {"168" : 2, "40" : 5},
						},
				}
			}

	has_bind_list = {eslid:("2", "51-11-21-66", old_chn)}

	t1 = "基站内，存在和自己同组的，且成员最多大于阀值，不组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"][old_nw1][old_chn] = 130
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)
	if is_change:
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，存在和自己同组的，且成员小于阀值，另外一个分组也较小，要组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"][old_nw1][old_chn] = 3
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 5
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)
	if not is_change or (new_nw1, new_nw3) != ("51-11-22-66", "168"):
		trace(t, t1, "failed", is_change, new_nw1, new_nw3)

	t1 = "基站内，存在和自己同组的，且成员较少大于阀值，不组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"][old_nw1][old_chn] = 130
	_g["1"]["HS_EL_5300"]["51-11-22-66"][old_chn] = 180
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if is_change:
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，不存在和自己同组的，有另外一个组, 要组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"].pop(old_nw1)
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if not is_change or (new_nw1, new_nw3) == (old_nw1, old_chn):
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，不存在和自己同组的，也没有其余的组, 不组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"].pop(old_nw1)
	_g["1"]["HS_EL_5300"].pop("51-11-22-66")
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if is_change:
		trace(t, t1, "failed", new_nw1)
	
	g = {"1":
				{
					"HS_EL_5300": {
						old_nw1: {old_chn : 160, "168" : 6},
						"51-11-22-66": {"168" : 8, "168" : 5},
						},
					"HS_EL_5104": {
						"52-11-21-66": {old_chn : 2, "40" : 5},
						"52-11-22-66": {"168" : 2, "40" : 5},
						},
				}
			}

	t1 = "基站内，本组价签已满，要组网"
	_g = deepcopy(g)
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if not is_change or (new_nw1, new_nw3) == (old_nw1, old_chn):
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，本组价签已满，另外一组也满，但有空余组，要组到空余组"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 160
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if not is_change or new_nw1 != old_nw1 or new_nw3 != "168":
		trace(t, t1, "failed", new_nw1, new_nw3)
	
	t1 = "基站内，本组价签已满，另外一组快满，但也有空余小组，要组到较多组内"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 159
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3_3g(db, eslid, apid, _g, has_bind_list, set_list)	
	if not is_change or new_nw1 != "51-11-22-66" or new_nw3 != "168":
		trace(t, t1, "failed", new_nw1, new_nw3)

#负责在指定的基站里找到合适的组网参数
def get_bind_nw1_nw3(db, eslid, apid, g, has_bind_list):

	if conf.htp.auto_netlink_after_bind.lower() != 'yes':
		return False, None, None, None, None
	
	e = db.get_one(db.esl, eslid)
	old_nw1, old_nw3, old_op3, op6 = e['nw1'], e['nw3'], e['op3'], e['op6']
	g1, nw1_nw3 = {}, {}

	if eslid in has_bind_list:  #从老组里减1，下面从新组里加1
		ap11, nw11, nw33 = has_bind_list[eslid]
		try:
			g[ap11][old_op3][nw11][nw33] -= 1
		except KeyError, e:
			pass

	#如果上一次组网失败，则继续使用上一次的参数进行组网
	op6 = eval(op6, {}, {})
	if "new_nw1" in op6 and (not is_g2g3_op3(old_op3)):
		esl_init.log.warning("%s prov netlink failed, use the prov para: %s,%s" % \
			(eslid, op6['new_nw1'], op6['new_nw3']))
		g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(op6['new_nw1'], {}).\
			setdefault(op6['new_nw3'], 0)
		g[apid][old_op3][op6['new_nw1']][op6['new_nw3']] += 1
		return True, op6['new_nw1'], op6['new_nw3'], op6['new_nw3'], op6['new_nw3']
	
	#找到同基站，同类型且有富余的所有组
	channel_list = conf.netlink.channel_list
	if apid in g:
		if old_op3 in g[apid]:
			for nw1 in g[apid][old_op3]:
				for nw3 in g[apid][old_op3][nw1]:
					if int(nw3) not in channel_list:
						continue
					count = g[apid][old_op3][nw1][nw3]
					nw1_nw3[(nw1, nw3)] = 1
					if int(count) < int(conf.netlink.group_num_max) and int(count) >= 0:
						g1[(nw1, nw3)] = count
	
	#再进行个数从高到低排序	
	g1 = sorted(g1.iteritems(), key=lambda g1 : g1[1], reverse=True)

	#如果最多的1组和当前的一样多，则刨除当前的，使用前面的组信息
	#if len(g1) >= 2:
	#	((e1_nw1, e1_nw3), c1), ((e2_nw1, e2_nw3), c2) = g1[0], g1[1]
	#	if c1 == c2 and e1_nw1 == old_nw1 and e1_nw3 == old_nw3:
	#		g1.remove(((e1_nw1, e1_nw3), c1))
	
	for ((nw1, nw3), count) in g1:
		#存在同组且个数大于等于组阀值的60%
		if nw1 == old_nw1 and nw3 == old_nw3 and g[apid][old_op3][nw1][nw3] >= conf.netlink.group_num_max * 0.6:
			g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
			g[apid][old_op3][nw1][nw3] += 1
			return False, nw1, nw3, nw3, nw3 
	
	for ((nw1, nw3), count) in g1:
		#有一组可以容纳新的价签，且成员数最多的
		g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)
		g[apid][old_op3][nw1][nw3] += 1
		is_changed = True if (old_nw1, old_nw3) != (nw1, nw3) else False
		return is_changed, nw1, nw3, nw3, nw3

	#开始分配新参数, 先默认使用自身的nw1,但信道需要均衡
	new_nw3 = get_free_nw3(g, apid, old_op3, old_nw3)
	if (old_nw1, new_nw3) not in nw1_nw3:
		g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(old_nw1, {}).setdefault(new_nw3, 0)
		g[apid][old_op3][old_nw1][new_nw3] += 1
		ischanged = True if new_nw3 != old_nw3 else False
		return ischanged, old_nw1, new_nw3, new_nw3, new_nw3 
	
	#从系统里挑选1个未被使用的wakeupid, 和基站内均衡的chn
	nw1 = get_free_nw1(g)
	nw3 = new_nw3
	g.setdefault(apid, {}).setdefault(old_op3, {}).setdefault(nw1, {}).setdefault(nw3, 0)

	ischanged = False if (nw1 == old_nw1 and nw3 == old_nw3) else True
	if ischanged:
		esl_init.log.info("change eslid %s to (%s, %s) from (%s, %s)" % (eslid, nw1, nw3, old_nw1, old_nw3))

	g[apid][old_op3][nw1][nw3] += 1
	return ischanged, nw1, nw3, nw3, nw3


def get_bind_nw1_nw3_test(db):
	
	t = "组网测试"

	eslid, old_nw1, old_chn = "55-55-55-99", "51-11-21-66", "158"
	esl_list = [{"eslid":"55-55-55-99", "setchn":old_chn, "grpchn":old_chn, "nw3":old_chn, 
							"nw1":old_nw1, "nw4":"NORMAL", "op3":"HS_EL_5300"},]
	db.list_updata(db.esl, esl_list)
	apid = "1"
	g = {"1":
				{
					"HS_EL_5300": {
						old_nw1: {old_chn : 3, "40" : 5},
						"51-11-22-66": {"168" : 2, "40" : 5},
						},
					"HS_EL_5104": {
						"52-11-21-66": {old_chn : 2, "40" : 5},
						"52-11-22-66": {"168" : 2, "40" : 5},
						},
				}
			}

	has_bind_list = {eslid:("2", "51-11-21-66", old_chn)}

	t1 = "基站内，存在和自己同组的，且成员最多大于阀值，不组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"][old_nw1][old_chn] = 130
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if is_change:
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，存在和自己同组的，且成员小于于阀值，组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"][old_nw1][old_chn] = 3
	_g["1"]["HS_EL_5300"]["51-11-22-66"][old_chn] = 180
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 5
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if not is_change or (new_nw1, new_nw3) != ("51-11-22-66", "168"):
		trace(t, t1, "failed", new_nw1, new_nw3)
	
	t1 = "基站内，不存在和自己同组的，有另外一个组, 要组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"].pop(old_nw1)
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if not is_change or (new_nw1, new_nw3) == (old_nw1, old_chn):
		trace(t, t1, "failed", is_change, new_nw1, new_nw3)
	
	t1 = "基站内，不存在和自己同组的，也没有其余的组, 不组网"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"].pop(old_nw1)
	_g["1"]["HS_EL_5300"].pop("51-11-22-66")
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if is_change:
		trace(t, t1, "failed", new_nw1)
	
	g = {"1":
				{
					"HS_EL_5300": {
						old_nw1: {old_chn : 160, "168" : 6},
						"51-11-22-66": {"168" : 8, "168" : 5},
						},
					"HS_EL_5104": {
						"52-11-21-66": {old_chn : 2, "40" : 5},
						"52-11-22-66": {"168" : 2, "40" : 5},
						},
				}
			}

	t1 = "基站内，本组价签已满，要组网"
	_g = deepcopy(g)
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if not is_change or (new_nw1, new_nw3) == (old_nw1, old_chn):
		trace(t, t1, "failed", new_nw1)
	
	t1 = "基站内，本组价签已满，另外一组也满，但有空余组，要组到空余组"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 160
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if not is_change or new_nw1 != old_nw1 or new_nw3 != "168":
		trace(t, t1, "failed", new_nw1, new_nw3)
	
	t1 = "基站内，本组价签已满，另外一组快满，但也有空余小组，要组到较多组内"
	_g = deepcopy(g)
	_g["1"]["HS_EL_5300"]["51-11-22-66"]["168"] = 159
	is_change, new_nw1, new_nw3, new_nw3, new_nw3 = get_bind_nw1_nw3(db, eslid, apid, _g, has_bind_list)	
	if not is_change or new_nw1 != "51-11-22-66" or new_nw3 != "168":
		trace(t, t1, "failed", new_nw1, new_nw3)

def get_free_nw1(g):
	used = {}

	wakeupid_list = conf.netlink.wakeupid_list
	startid = int(wakeupid_list[0].replace('-',''),16)
	endid = int(wakeupid_list[1].replace('-',''),16)

	for ap in g:
		for op3 in g[ap]:
			for nw1 in g[ap][op3]:
				used[int(nw1.replace('-',''),16)] = 1
	
	for nw1 in xrange(startid, endid, 10*256):
		if nw1 not in used:
			N = hex(nw1)
			return (N[2]+N[3]+'-'+N[4]+N[5]+'-'+N[6]+N[7]+'-'+N[8]+N[9]).upper()
	
	esl_init.log.error_msg('no any groups except max group: 51-FF-FF-66', errid='ENE010')
	return '51-FF-FF-66'

def get_free_nw3(g, ap, old_op3, default_nw3):

	channel_list = conf.netlink.channel_list

	try:
		notused = g[ap][old_op3]
	except KeyError, e:
		return str(choice(channel_list))
		
	used = {}
	for nw3 in channel_list:
		used[str(nw3)] = 0

	if ap in g:
		for op3 in g[ap]:
			for nw1 in g[ap][op3]:
				for nw3 in g[ap][op3][nw1]:
					if nw3 in used:
						used[nw3] += 1
	
	used = sorted(used.iteritems(), key=lambda used : used[1], reverse=False) # 从小到大排列
	ap_list = [item[0] for item in used][:-1] #把信道使用最多的排除掉
	if default_nw3 in ap_list or not ap_list:
		return default_nw3
	return ap_list[0]

setid_list = ['01','FF']
startid = int(setid_list[0], 16)
endid = int(setid_list[1], 16)

def get_setid(ap, ap_list): #set add
	used = {}
	for group_name in ap_list:
		for ap in ap_list[group_name]:
			for setid in ap_list[group_name][ap][1:]:
				used[int(setid, 16)] = '1'
	for setid in xrange(startid, endid):
		N = hex(setid)
		if setid not in used and setid <= 15: #小于15:'0X'
			return ('0' + N[2]).upper()	
		elif setid not in used:
			return (N[2] + N[3]).upper()
		else:
			continue
	
def get_nw3(ap, ap_list): #set add
	channel_list = conf.netlink.channel_list
	used = {}
	for nw3 in channel_list:
		used[str(nw3)] = 0
	for group_name in ap_list:
		for ap in ap_list[group_name].keys():
			for nw3 in ap_list[group_name][ap]:
				if nw3 in used:
					used[nw3] += 1
	used = sorted(used.iteritems(), key=lambda used : used[1], reverse=False) # 从小到大排列
	ap_list = [item[0] for item in used][:-1] #把信道使用最多的排除掉
	return ap_list[0]

def read_setid_info():
	for code in ['utf-8-sig', 'utf-8', 'gb2312', 'ascii']:
		try:
			f = codecs.open("config/set_list.ini", 'r', encoding=code)
			txt = f.read()
			f.close()
			apset_list = eval(txt, {}, {})
			return apset_list
		except Exception, e:
			pass

def load_apset_info(apset_list):
	with open("config/set_list.ini","w") as f:
		pprint.pprint(apset_list, stream=f)
			
def save_apset_info(apid, apset_info, db): #传入db，防止数据库报错
	group_esl_max = int(conf.netlink.group_num_max)

	old_setFile_config = copy.deepcopy(apset_info)

	apset_list = apset_info	
	apset_list.setdefault('DEFAULT_GROUP', {})
	if apid in apset_list['DEFAULT_GROUP']:
		set_list = apset_list['DEFAULT_GROUP'][apid][-1]
		if db.set_esl_count(set_list) >= (group_esl_max * 24):
			new_setid = get_setid(apid, apset_list)
			apset_list['DEFAULT_GROUP'][apid].append(new_setid)
	else:
		apset_list.setdefault('DEFAULT_GROUP', {}).setdefault(apid, [])
		new_nw3 = get_nw3(apid, apset_list) #系统开启时生成默认json格式, 新基站加入时分配chn与setid
		apset_list['DEFAULT_GROUP'][apid].append(new_nw3)
		new_setid = get_setid(apid, apset_list)
		apset_list['DEFAULT_GROUP'][apid].append(new_setid)

	if apset_list != old_setFile_config:
		load_apset_info(apset_list) #配置改变直接写入set_list.ini
		core.sava_ap_list(db) #更新基站表文件

def self_test():
	from database import DB
	from tempfile import mktemp
	import os

	if conf.system.esl_heartbeat_timeout != 3600:
		print "conf.system.esl_heartbeat_timeout values != 3600, some test will be failed, change to 3600" 
		conf.system.esl_heartbeat_timeout = 3600
	if conf.netlink.group_num_max != 160:
		print "conf.netlink.group_num_max != 160, some test will be failed, change to 160" 
		conf.netlink.group_num_max = 160
	if conf.netlink.channel_list != [158, 168, 178]:
		print "conf.netlink.channel_list != [158, 168, 178], some test will be failed, change to [158, 168, 178]" 
		conf.netlink.channel_list = [158, 168, 178]

	for test_fun in [ get_bind_nw1_nw3_test, 
							get_bind_nw1_nw3_3g_test,
							]:
		db_file = mktemp()
		db = DB(db_file = db_file)
		db.check_db()

		test_fun(db)

		db.conn.close()
		os.remove(db_file)
