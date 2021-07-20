# encoding: utf-8

import time, sys, os, multiprocessing, platform, gc, threading
import esl_init, core, updata, query, bind, xmlserver, database, api20
import osd, beacom, ftp_server, netlink, summary, htp
from daemon import Daemon
import heartbeat, Queue, socket
from esl_init import conf
from apv3_connector import APv3Connector
from xmlserver import reply_ack

db = database.DB()

version = "1.3.6_rc1"

try:
	import win32serviceutil
	import win32service
	import win32event
	windows_service = True
except Exception, e:
	windows_service = False

if windows_service:
	class SmallestPythonService(win32serviceutil.ServiceFramework):
		_svc_name_ = "esl-working"
		_svc_display_name_ = "esl-working"
		def __init__(self, args):
			win32serviceutil.ServiceFramework.__init__(self, args)
			# Create an event which we will use to wait on.
			# The "service stop" request will set this event.
			self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
			self.stop = False

		def SvcStop(self):
			# Before we do anything, tell the SCM we are starting the stop process.
			self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
			# And set my event.
			win32event.SetEvent(self.hWaitStop)
			self.stop = True

		def SvcDoRun(self):
			# 把你的程序代码放到这里就OK了
			path = os.path.split(os.path.realpath(__file__))[0]
			os.chdir(path)#切换工作路径
			create_process(opt = self)		
			
			win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

def is_port_free(prot, port):
	s = socket.socket(socket.AF_INET, prot) #socket.SOCK_STREAM)
	try:
		s.connect(('127.0.0.1', int(port)))
		s.shutdown(2)
		print "network port %s is in use, please check it again" % port
		return False
	except Exception, e:
		return True

def is_system_clean():
	#先检查网络端口
	if not (is_port_free(socket.SOCK_STREAM, conf.extend_service.xml_rpc_port)
		and is_port_free(socket.SOCK_STREAM, conf.extend_service.bind_listen_port)
		and is_port_free(socket.SOCK_STREAM, conf.extend_service.apv3_listen_port)
		and is_port_free(socket.SOCK_STREAM, conf.extend_service.summary_html_port)):
		return False
	
	if conf.htp.internal_ftp.lower() == 'yes' \
		and (not is_port_free(socket.SOCK_STREAM, conf.htp.ftp_port)):
		return False
	
	return True

def store_hb(task_data):
	storeid = conf.system.ids
	esl_init.log.info("store [%s] heardbeat" % (storeid))
	task_data['threading_event'].clear() # 设置event标志为False, 此时心跳接口调用e_flag.wait()阻塞线程
	try:
		xmlserver.resend_failed_msg()
		core.save_esl_power_info(task_data['esl_power_info'])
		heartbeat.auto_refresh_bind_at_hour_fun()
	except KeyboardInterrupt:
		raise KeyboardInterrupt, "KeyboardInterrupt"
	except Exception, e:
		esl_init.log.error_msg("store_hb:%s" % e, errid='EMA001')
	finally:
		task_data['threading_event'].set()

def create_task_data():
	task_data = {}
	for task_name in ['updata', 'bind', 'query', 'beacom', 'netlink']:
		task_data.setdefault(task_name, {})
		task_data[task_name]['in_queue'] = Queue.Queue() #multiprocessing.Queue() 
		task_data[task_name]['out_queue'] = Queue.Queue()#multiprocessing.Queue() 
		task_data[task_name]['work_list'] = {} # 更新次数，更新第几次

	task_data['updata']['action'] = updata.action
	task_data['bind']['action'] = bind.action
	task_data['query']['action'] = query.action
	task_data['beacom']['action'] = beacom.action
	task_data['netlink']['action'] = netlink.action

	task_data['updata']['ap_check_list'] = {} #beacom.ap_check_list # 漫游列表
	task_data['bind']['ap_check_list'] = {} # beacom.ap_check_list
	task_data['query']['ap_check_list'] = {} #beacom.ap_check_list
	task_data['beacom']['ap_check_list'] = {} #beacom.ap_check_list #不再共用
	task_data['netlink']['ap_check_list'] = {} #beacom.ap_check_list

	#一些只有q但没有处理单元的, 其处理单元都借用query模块的
	for small_name in ['set_only_q']:
		task_data.setdefault(small_name, {})
		task_data[small_name]['in_queue'] = Queue.Queue()
		task_data[small_name]['work_list'] = {}
		task_data[small_name]['out_queue'] = task_data['query']['out_queue']
		task_data[small_name]['action'] = task_data['query']['action']
		task_data[small_name]['ap_check_list'] = task_data['query']['ap_check_list']

	task_data['ppid'] = os.getpid()
	
	task_data['updata']['buf_in_queue'] = Queue.Queue() #multiprocessing.Queue()
	task_data['updata']['updata_dict'] = {} # 更新数据结构
	task_data['lowpower_counter'] = {} #multiprocessing.Manager().dict()
	task_data['osd_last_ack'] = {} #multiprocessing.Manager().dict()
	task_data['netlink']['rf_para'] = {} #multiprocessing.Manager().dict()
	task_data['ap_level'] = {} #multiprocessing.Manager().dict()
	task_data['esl_power_info'] = {} #multiprocessing.Manager().dict()
	task_data['esl_priority'] = {} #multiprocessing.Manager().dict()
	task_data['ap_work_time'] = {} #multiprocessing.Manager().dict()
	task_data["all_info"] = {}
	task_data['esl_info'] = {}
	task_data['esl_power_his'] = {}
	task_data['esl_power_last_time'] = {} #存储价签最近一次的心跳时间
	task_data['esl_level_change_count'] = {}

	task_data['reply_ack_q'] = Queue.Queue()
	task_data['isquit'] = {}

	task_data['threading_event'] = threading.Event() # 标志位
	task_data['threading_event'].set() # 设置标志位为True
	task_data['apset'] = {} # 生成set_list.ini

	task_data['bind_udp_q'] = Queue.Queue(maxsize = 1000000)
	task_data['ack_count'] = {}
	task_data['rf_para_is_changed'] = {}

	task_data['startup_time'] = time.time()
	task_data['system_version'] = version

	esl_init.log.set_uplink_q(task_data['reply_ack_q'])
	
	return task_data

def create_process(opt = None):
	'''
	程序设置为deamon后，将分别启动核心进程，更新进程，绑定进程，查询进程，xml-prc进程。
	并且将一直循环（1秒一次）检测这些进程的状态，如果进程因为异常而导致退出，则重新启动之
	'''
	try:
		try:
			db.check_db()
		except Exception, e:
			esl_init.print_except()
			esl_init.log.error("check db error: %s" % e)

		task_data = create_task_data()
		task_module = [core, xmlserver, updata, bind, query, beacom, ftp_server, netlink, summary]
		for t1 in ['core', 'xmlserver', 'updata', 'bind', 'query', 'beacom', 'ftp_server', 'netlink', 'summary']:
			task_data['isquit'][t1] = False

		if conf.extend_service.apv3_enable.lower() == 'yes':
			apv3 = APv3Connector(task_data['bind_udp_q'])
			apv3.start()
			task_data['apv3'] = apv3
			esl_init.log.info("apv3 starting")

		inner_ftp = conf.htp.internal_ftp.upper()
		if inner_ftp == 'NO':
			try:
				task_module.remove(ftp_server)
			except Exception ,e:
				pass

		core.load_esl_power_info(task_data['esl_power_info'], db.get_all_ap())
		if not os.path.isfile('config/set_list.ini'):
			netlink.load_apset_info(task_data['apset']) # 生成set_list.ini
		else:
			task_data['apset'] = netlink.read_setid_info()
		task_list = [task.start(task_data) for task in task_module]
		esl_init.check_htp_kickoff_file()
		n = 0
		platform_os = platform.system()
		pid = task_data['ppid']
		updata_restart_n = 0
		
	except KeyboardInterrupt, e:
		system_exit(task_data)
		esl_init.log.warning("ESL system exit")
		return
	
	esl_init.log.info("ESL system starting, version %s" % version)
	reply_ack("RESEND_UPDATE", [], None)

	try:
		while True:
			for task in task_list:
				#如果task死掉
				if not task.is_alive():
					task.join(timeout=1)
					id1 = task_list.index(task)

					task_list[id1] = task_module[id1].start(task_data)
					if task_module[id1] == core:
						task_data['isquit']['updata'] = True
						task_list[task_module.index(updata)].join()
						task_data['isquit']['netlink'] = True
						task_list[task_module.index(netlink)].join()
					if task_module[id1] == xmlserver:
						task_data['isquit']['core'] = True
						task_list[task_module.index(core)].join()
			time.sleep(1)
			n += 1
			if n % 5 == 0:
				try:
					esl_init.reload_config(conf)
					osd.watch_temp_change()
					esl_init.check_log_size()
				except KeyboardInterrupt, e:
					raise KeyboardInterrupt, e
				except Exception, e:
					esl_init.log.error_msg("esl watch event error %s" % e, errid='EMA002')

			if n == int(conf.system.store_heardbeat_time):
				n = 0
				store_hb(task_data)
				#如果接口服务死掉
				if bind.check_bind_listen_alive() == False:
					task_data['isquit']['bind'] = True
					task_list[task_module.index(bind)].join()
				if xmlserver.is_xmlserver_alive() == False:
					task_data['isquit']['xmlserver'] = True
					task_list[task_module.index(xmlserver)].join()				
				gc.collect()
			if windows_service and opt and opt.stop:
				raise KeyboardInterrupt, "stop"
	except KeyboardInterrupt, e:	
		esl_init.log.warning("system exit, wait for save file")
		core.sava_ap_list(db)
		core.save_esl_power_info(task_data['esl_power_info'])
		netlink.load_apset_info(task_data['apset'])#apset_list.ini

		system_exit(task_data)

		if platform.system() == 'Windows':
			multiprocessing.Process(target = kill_main_task, args = (pid,)).start()
		for task in task_list:	
			task.join()
	except Exception, e:
		pass
	finally:
		esl_init.log.warning("ESL system exit")

def system_exit(task_data):
	for t1 in ['core', 'xmlserver', 'updata', 'bind', 'query', 'beacom', 'ftp_server', 'netlink', 'summary']:
		task_data['isquit'][t1] = True
	summary.http_server_exit()
	if conf.extend_service.apv3_enable.lower() == 'yes':
		task_data['apv3'].stop()
		esl_init.log.info("apv3 exit")
	ftp_server.ftp_exit()

def kill_main_task(pid):
	try:
		time.sleep(10)
		os.kill(pid, 9)
	except Exception, e:
		pass

class TestDaemon(Daemon):
	'''
	继承Daemon类，覆写run函数
	'''
	def run(self):
		create_process()

def self_test_main():
	try:
		import self_test.main_test
		self_test.main_test.main_test()
	except Exception, e:
		print 'not self test module: %s' % e

def main_run():
	'''
	程序入口函数，主要作用是实例化一个daemon对象，将自身设置为daemon进程。
	程序执行时需要提供1个而外的参数，[start|stop|restart], 用于指示启动、停止后者重启程序。
	'''
	try:
		if len(sys.argv) <= 1:
			if platform.system() == 'Windows' and windows_service:
				print "Usage: python %s [--startup auto install|remove|start|stop|restart]" % sys.argv[0]	
			else:
				print "Usage: python %s [start|stop|restart]" % sys.argv[0]	
			return 

		if sys.argv[1] == 'start' and (not is_system_clean()):
			print "system start failed"
			return

		if platform.system() == 'Windows' and windows_service:
			if sys.argv[1] not in ['start', 'stop', 'restart', 'install', 'remove', '--startup']:
				print "Usage: python %s [--startup auto install|remove|start|stop|restart]" % sys.argv[0]	
				return 
		else:
			if sys.argv[1] not in ['start', 'stop', 'restart']:
				print "Usage: python %s [start|stop|restart]" % sys.argv[0]
				return 
			
		if platform.system() == 'Linux':
			test_daemon = TestDaemon('/tmp/esl-working.lock', home_dir = os.getcwd(), username='hanshow')
			if sys.argv[1] == 'start':
				test_daemon.start()
			elif sys.argv[1] == 'stop':
				test_daemon.stop()
			elif sys.argv[1] == 'restart':
				test_daemon.restart()
		else:
			if windows_service:
				win32serviceutil.HandleCommandLine(SmallestPythonService)
			else:
				esl_init.log.warning("can't detect python_win32_module, esl-working not running as service")
				create_process()
	except IOError, e:
		pass
	except socket.error, e:
		pass
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	if sys.platform.startswith('win'):
		multiprocessing.freeze_support()
	
	if 'test' in sys.argv:
		esl_init.log.warning("start self test mode")
		for m in [heartbeat, netlink, xmlserver, database, api20, htp]:
			m.self_test()
		print "test finished"
	else:
		main_run()


