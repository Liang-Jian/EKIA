# encoding: utf-8

#
# 本模块用来初始化系统，包括配置信息和数据库信息
#

import os, sys, ConfigParser, codecs,platform,time
import logging, traceback, shutil
import logging.handlers
from ftplib import FTP
from StringIO import StringIO

try:
	os.mkdir("log") 
except OSError:
	pass

work_dir = os.path.split(os.path.realpath(__file__))[0] 
if work_dir == '':
	work_dir = '.'
os.chdir(work_dir)

config_file = "config/config.ini"
def get_basic_config():
	config = ConfigParser.SafeConfigParser()
	config.optionxform = str
	config.read(config_file)
	return config

#修改缓存中的配置信息
def set_config(section, options, value):
	try:
		config = get_basic_config()
		if not config.has_section(section):
			config.add_section(section)
		config.set(section, options, value)

		with open(config_file, "w+") as f:
			config.write(f)
			f.close()
		ret = True
	except Exception, e:
		ret = False
	return ret

#检查目录是否存在，不存在则创建之
def check_dirs(dir_list):
	for one_dir in dir_list:
		if not os.path.exists(one_dir):
			try:
				os.makedirs(one_dir)
			except Exception, e:
				pass

def check_htp_kickoff_file():
	#创建ap_kickoff空文件
	
	for x in range(3):
		try:
			time.sleep(x+1) #保证main把ftp跑起来
			port = int(conf.htp.ftp_port)
			f = FTP()
			f.connect(conf.htp.ftp_server, port)
			f.login(conf.htp.ftp_user, conf.htp.ftp_pass)
			tmp = StringIO()
			tmp.write("")
			f.storbinary('STOR ap_kickoff.txt', tmp)
			f.quit()
			f.close()
			#log.info(" create ap_kickoff successfully!")
			break
		except Exception, e:
			#log.info("create ap_kickoff failed: %s" % e)
			pass

class configs(object):
	def __setattr__(self, name, value):
		object.__setattr__(self, name, value)

def init_configs(conf):
	config_key = {
		"system":[ ("ids", "S1234567", str), ("store_heardbeat_time", "1200", int), ("ap_heardbeat_time", "300", int),
						("esl_heartbeat_timeout", "3600", int), ("esl_update_timeout", "3600", int),
						("update_sid_timeout", "7200", int), ("parent_url", "", str),
						("lock_file", "/tmp/esl-working.lock", str), ("log_file", "log/log.txt", str), 
						("log_file_max", "200", int), ("ftp_log_file", "log/ftp_log.txt", str),
						("esl_config_file", " config/esl_conf.ini", str),("dot_temp_file", "./temp_json/esl_temp.txt", str),
						("dot_temp_dir", "./temp_json/", str),("temp_json", "yes", str), ("debug_lever", "info", str),
						("parent_enable", "yes", str),("parent_ip", "127.0.0.1", str),("parent_xml_rpc_port", "8088", int),
						("esl_hb_report_max", "1000", int), ("esl_hb_report_timeout", "60", int), ("testmode", "advance", str),
						("uplink_cmd_block_list", "['ESL_STATUS', 'AP_STATUS', 'ESL_HB_STATUS']", eval),
					],
		"db_file": [("db_file", "db.sqlite", str), ("sales_list_title", "['salesno','salesname','Price','oldprice','startdate','enddate','Price1','Price2','Price3','sid','lastworktime', 'status','barcode','origin','spec','location','unit','grade','position','exhibition','protype','qrcode','specifications','newtask','shelfposition']", eval)
					],
		"htp": [("sleep_times", "1", int), ("lowpower_warning", "-1",int), ("htp_version", "16",int),
						("htp_version_str", "HTPv16", str), ("rcved_timeout_sec", "30",int), ("ack_timeout_sec", "60",int),
						("ap_dead_time", "7*24*3600", eval),
						("socket_timeout_sec", "6",int), ("internal_ftp", "yes", str), ("ftp_server", "127.0.0.1", str),
						("ftp_user", "hanshow", str), ("ftp_pass", "hanshow", str), ("ftp_port", "9005",int),
						("osd_args", "LOG_OFF 512 A8", str), ("osd_args_v2", "LOG_OFF 4500 A8", str), 
						("lcd_args_v2", "LOF_OFF DEBUG_OFF", str), ("vitrual_htp", "no", str),
						("vitrual_pass_rate", "0",int), ("esl_power_level", "[40, 50, 60, 70, 80, 90, 100]", eval), 
						("esl_power_threshold", "30",int),
						("auto_bind_after_register", "no", str), ("auto_netlink_after_bind", "yes", str), 
						("auto_refresh_bind_at_hour", "-1",int),
						("auto_retry_after_failed", "no", str), ("retry_time_interval", "[3600, 5*3600, 12*3600, 6*24*3600]", eval), 
						("fix_retry_time_for_5103", "12",int),
						("fix_retry_time_for_5033", "6",int), ("global_retry_time_max", "0",int), ("failed_retry_time_max", "8",int),
						("enable_roaming", "yes", str), ("max_set_wakeup", "10",int), ("max_wakeup_group", "3",int),
						("max_wakeup_esl", "150",int), 
				],
		"extend_service": [ ("ip_addr", "0.0.0.0", str), ("xml_rpc_port", "9000",int), ("bind_listen_port", "8800",int),
						("summary_html_port", "9006", int), ("apv3_enable", "no", str), ("apv3_listen_port", "1234",int),
				],
		"netlink": [ ("group_num_max", "160",int), ("wakeupid_list", "['51-01-01-66', '51-FE-FE-66']", eval), 
						("channel_list", "[158, 168, 178]", eval),
				],
		"idsystem": [ ("enable", "no", str), ("url", "https://123.57.225.81:8082", str), ("timeout", "3",int),
						("username", "hanshowidsystem", str), ("password", "hanshowidsystem", str), 
				],
	}

	if conf == None:
		conf = configs()

	config = get_basic_config()

	for k in config_key:
		section = configs()
		for item in config_key[k]:
			fun = item[2]
			try:
				v = 'None'
				v = config.get(k, item[0]).strip()
				if fun == eval:
					v = fun(v, {}, {})
				else:
					v = fun(v)
			except Exception, e:
				try:
					print("apply config %s.%s value %s failed, use default value %s" % 
						(k, item[0], v, item[1]))
					log.warning("apply config %s.%s value %s failed, use default value %s" % 
							(k, item[0], v, item[1]))
				except:
					pass
				v = item[1]
				if fun == eval:
					v = fun(v, {}, {})
				else:
					v = fun(v)
			
			section.__setattr__(item[0], v)
		conf.__setattr__(k, section)
	
	conf.mtime = os.stat(config_file).st_mtime
	
	return conf

conf = init_configs(None)

def reload_config(conf):
	mtime = os.stat(config_file).st_mtime
	if mtime != conf.mtime:
		init_configs(conf)
		log.warning("reload configration from config/config.ini")
		set_logger(log)

def check_log_size():
	log_size = os.path.getsize(conf.system.log_file)
	if log_size < conf.system.log_file_max * 1024*1024:
		return
	fn_list = ["%s.%s" % (conf.system.log_file,i) for i in xrange(10, 0, -1)]

	for i in xrange(9, 0, -1):
		dst = "%s.%s" % (conf.system.log_file, i +1)
		src = "%s.%s" % (conf.system.log_file, i)
		try:
			shutil.move(src, dst)
		except Exception, e:
			pass
	try:
		shutil.copy(conf.system.log_file, "%s.%s" % (conf.system.log_file, 1))
		with open(conf.system.log_file, "w"): #截断log文件
			pass
	except Exception, e:
		pass
			
#配置log文件
def set_logger(log):
	
	if log.normal_hdl != None:
		log.removeHandler(log.normal_hdl)
	if log.error_hdl != None:
		log.removeHandler(log.error_hdl)

	log_level = {'debug':logging.DEBUG, 'info':logging.INFO, 'error' : logging.ERROR,
						'warning': logging.WARNING}
	log_level = log_level.get(conf.system.debug_lever, logging.INFO)
	log_file = conf.system.log_file
	log_file_size = int(conf.system.log_file_max)

	fmt = '%(levelname)-10s;%(asctime)s;%(message)s'
	formatter = logging.Formatter(fmt = fmt, datefmt='%Y-%m-%d %H:%M:%S')

	ch = logging.FileHandler(log_file)
	ch.setFormatter(formatter)

	err = logging.FileHandler("./log/error.log")
	err.setFormatter(formatter)

	ch.setLevel(log_level)
	log.setLevel(log_level)
	err.setLevel(logging.ERROR)

	log.addHandler(ch)
	log.addHandler(err)
	
	log.normal_hdl = ch
	log.error_hdl = err
	
_n = 0
def trace(T, t, val, *args, **argv):
	global _n
	f, l = excep_fun_line()
	_n += 1
	if platform.system() == 'Windows':
		T = T.decode("utf-8").encode("GBK")
		t = t.decode("utf-8").encode("GBK")
	print "%s;%s;%s;%s;%s;%s;%s" % (_n, f, l, T, t, val, str(args)+str(argv))
	sys.exit(1)

def excep_fun_line():
	try:
		raise KeyError
	except Exception, e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		try:
			e = traceback.extract_stack()[-3]
		except IndexError:
			return "unknown", 0
		return os.path.basename(e[0]), e[1]

from database import DB
class LOG(logging.Logger):
	
	q = None
	normal_hdl = None
	error_hdl = None
	pid = os.getpid()

	def set_uplink_q(self, q):
		self.q = q
	
	def debug(self, msg, *args, **kwargs):
		f, l = excep_fun_line()
		msg = "%-15s[%04s][%-5s];" % (f, l, self.pid) + str(msg)
		logging.Logger.debug(self, msg, *args, **kwargs)
	
	def info(self, msg, *args, **kwargs):
		f, l = excep_fun_line()
		msg = "%-15s[%04s][%-5s];" % (f, l, self.pid) + str(msg)
		logging.Logger.info(self, msg, *args, **kwargs)
	
	def warning(self, msg, *args, **kwargs):
		f, l = excep_fun_line()
		msg = "%-15s[%04s][%-5s];" % (f, l, self.pid) + str(msg)
		logging.Logger.warning(self, msg, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		f, l = excep_fun_line()
		msg = "%-15s[%04s][%-5s];" % (f, l, self.pid) + str(msg)
		logging.Logger.error(self, msg, *args, **kwargs)
	
	def error_msg(self, msg, errid="E00000", \
						eslid="unknown", salesno="unknown", *args, **kwargs):
		try:
			if self.q:
				msg1 = [{"errid":errid, "eslid":eslid, "salesno":salesno, "errmsg":msg}]
				self.q.put_nowait(("ERROR_ACK", msg1))

			f, l = excep_fun_line()
			msg = "%-15s[%04s][%-5s];" % (f, l, self.pid) + str(errid) + ':' + str(msg)
			logging.Logger.error(self, msg, *args, **kwargs)
		except Exception, e:
			pass

# log_desc 生成命令
# egrep -e 'log.info\(|log.error\(|log.warning\(|log.error_msg\(' *.py | sed -e 's/:[[:space:]]*/^/' -e 's/[^a-zA-Z)]*$//g' -e 's/\\//g' -e 's/"/\\"/g' | awk -F^ '{printf("\"%s\" : \{\"module\" : \"%s\", \"desc\" : \"\", \"howto\" : \"\"}, \n", $2, $1)}' | grep -v '^"#'
#

log = LOG('esl')
set_logger(log)

def print_except():
	with open("log/exception.log", "a") as f:
		f.write("%s\n" % time.asctime())
		traceback.print_exc(file=f)
		f.write("\n")

