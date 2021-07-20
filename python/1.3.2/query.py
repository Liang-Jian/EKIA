# encoding: utf-8

import multiprocessing, time, os, platform, threading
from htp import htp_task, ack_ok, ack_low_power, check_real_low_power
from esl_init import  conf
import esl_init
from database import DB
import bind, xmlserver

def start(task_data):
	'''启动查询进程并返回进程对象'''
	proc = threading.Thread(target = process, args = (task_data,))
	proc.start()
	return proc

def process(task_data):
	'''
	负责从数据源解析处待查询的价签ID，缓冲一组发送到in_queue
	并从out_queue读取处理结果
	'''
	esl_init.log.info("query_process starting")
	db = DB()
	out_queue = task_data['query']['out_queue']
	beacom_in_queue = task_data['beacom']['in_queue']
	lowpower_warning = int(conf.htp.lowpower_warning)

	try:
		while True:
			status_list = []
			while not out_queue.empty():
				ids, ret_old, sid = out_queue.get()
				#关闭漫游功能，直接返回失败
				task_data['beacom']['out_queue'].put((ids, ret_old))
			time.sleep(1)
			if task_data['isquit']['query']:
				break
	except Exception, e:  
		esl_init.log.error_msg("query process:%s" % e, errid='EQU001')
	
	esl_init.log.info("query is quit")

def action(groups):
	'''
	负责处理一组查询数据，需要按照基站、信道、nw1进行分组，然后并发执行，并返回ack列表
	返回格式为 {id: ack, id : ack,...}
	'''
	htp_task(groups, "NORMAL", "QUERY")
