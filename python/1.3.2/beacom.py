# encoding: utf-8

import multiprocessing, time, xmlrpclib, threading, os, platform
from htp import htp_task, ack_ok, ack_low_power, check_real_low_power, get_apid_from_ack
from esl_init import log, conf
from database import DB
import xmlserver
from bind import get_xmlserver
from threading import Timer

work_list = {}

def start(task_data):
	'''启动查询进程并返回进程对象'''
	#proc = multiprocessing.Process(target = process, args = (task_data,))
	proc = threading.Thread(target = process, args = (task_data,))
	proc.start()
	return proc

def get_available_ap(db):
	idn = len(db.key_list(db.bind))
	ap_list = db.get_online_ap()
	return ap_list

beacom_list = {}
def cancel_beacom_find(id1):
	beacom_list.pop(id1, None)

def beacom_find_esl(idlist):

	auto_retry_after_failed = conf.htp.auto_retry_after_failed.lower()
	if auto_retry_after_failed != 'yes':
		return

	job = {}
	retry_time_interval = conf.htp.retry_time_interval

	for id1 in idlist:
		if id1 not in beacom_list:
			beacom_list[id1] = 0
		else:
			beacom_list[id1] += 1
		sec_table = retry_time_interval
		if beacom_list[id1] >= len(sec_table):
			beacom_list.pop(id1)
			continue
		
		try:
			sec = int(sec_table[beacom_list[id1]])
			job.setdefault(sec, []).append(id1)
			#Timer(sec, retry_send_beacom, (id1,)).start()
		except Exception, e:
			log.warning("try to beacom failed:%s, %s" % (id1, e))
	
	for sec in job:
		args = [{"eslid":id1} for id1 in job[sec]]
		try:
			Timer(sec, retry_send_beacom, args).start()
			log.info("will refind esl %s after %s sec" % (args, sec))
		except Exception, e:
			log.warning("try to beacom failed:%s, %s" % (args, e))

def retry_send_beacom(args):
	try:
		xml_server = get_xmlserver()
		xml_server.send_cmd("ESL_BEACOM", [args])
	except Exception, e:
		log.warning("retry_send_beacom failed: %s, %s" % (args, e))

def check_ack(group_list, ack_list, beacom_data, retry_max_of_eslid):
	'''根据分组情况和ack情况，确定价签是不是漫游到来这个基站下面'''
	db = DB()
	bind_list = []
	out_list = []
	beacom_list = []

	max_retry_times = 6

	for id1, ack in ack_list:
		id1 = id1.upper()
		ap = get_apid_from_ack(ack)
		
		if id1 not in beacom_data['ap_check_list']:
			continue #说明分区域并行的时候，某个基站已经找到了这个价签，并将之删除了

		if ack_ok(ack):
			beacom_data['ap_check_list'].pop(id1, None)
			beacom_data['work_list'].pop(id1, None)
			beacom_data['out_queue'].put((id1,ack))
			retry_max_of_eslid.pop(id1, None)
			cancel_beacom_find(id1)
		else: #全部基站都轮循来一次都没有成功
			beacom_data['work_list'][id1] += 1
			if beacom_data['work_list'][id1] >= max_retry_times:
				beacom_data['ap_check_list'].pop(id1, None)
				beacom_data['work_list'].pop(id1, None)
				beacom_data['out_queue'].put((id1, ack))
				retry_max_of_eslid.pop(id1, None)
				beacom_list.append(id1)
	
	beacom_find_esl(beacom_list)

	#输出统计结果
	#dump_bind_count(db)

def sleep_until_12AM():
	now_hour = time.localtime()[3]
	if now_hour > 4:
		log.info("cancel esl heardbeat, wait %s hours" % (24 - now_hour))
		time.sleep((24-now_hour)*60*60)

def process(task_data):
	'''
	负责从数据源解析待查询的价签ID，缓冲一组发送到in_queue
	并从out_queue读取处理结果
	'''
	db = DB()
	from xmlserver import reply_ack

	log.info("beacom_process starting")
	out_queue = task_data['beacom']['out_queue']

	try:
		while True:
			while not out_queue.empty():
				(ids, ret) = out_queue.get()
				ap = get_apid_from_ack(ret)
				lowpower_warning = int(conf.htp.lowpower_warning)
				ret = check_real_low_power(ids, ret, task_data['lowpower_counter'],lowpower_warning)
				
				yes, status = xmlserver.esl_status_has_changed(ids, ret, db)
				
				if ack_ok(ret) or ack_low_power(ret): #成功一次即为成功
					db.set_last_status_without_commit(db.esl, ids, time.asctime(), \
						"online" if status == "online" else "lowpower")
				else: #最后一次还是失败，则为失败
					db.set_last_status_without_commit(db.esl, ids, time.asctime(),"offline")

				info = db.get_all_info(db.esl, ids)
				reply_ack("ESL_QUERY_REALTIME_ACK", [info], None)

				if out_queue.empty():
					db.commit()

			time.sleep(0.3)
			if task_data['isquit']['beacom']:
				break
	except Exception, e:
		log.error_msg("beacom process:%s" % e, errid='EBE001')
	finally:
		db.conn.close()

	log.info("beacom exit")

def action(groups):
	'''
	负责处理一组查询数据，需要按照基站、信道、nw1进行分组，然后并发执行，并返回ack列表
	返回格式为 {id: ack, id : ack,...}
	'''
	htp_task(groups, "NORMAL", "QUERY")

def dump_bind_count(db):
	cmd = "select apid from %s" % (db.ap)
	db.cursor.execute(cmd)
	ap_binds = []
	for item in db.cursor.fetchall():
		ap = item['apid']
		cmd = "select eslid from %s where apid = %s" % (db.bind, ap)
		db.cursor.execute(cmd)
		ap_binds.append((ap, len(db.cursor.fetchall())))
	
