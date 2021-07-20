#encoding=utf-8
import platform ,multiprocessing
from authorizers import DummyAuthorizer
from handlers import FTPHandler
from servers import FTPServer
import os, sys, ConfigParser
import logging as log


#获取配置信息，获取失败时使用默认值
def get_config(section, options, default_value):
	try:
		ret = config.get(section, options).strip()
	except Exception, e:
		ret = default_value
	return ret

def start_log():
	#打开ftp log 开关
	work_dir = os.path.dirname(os.path.abspath(sys.argv[0])) #作为系统服务时需要打开这个开关
	if work_dir == '':
		work_dir = '.'
	os.chdir(work_dir)

	config = ConfigParser.SafeConfigParser()
	config.read("config.ini")
	log_level = {'debug':log.DEBUG, 'info':log.INFO, 'error' : log.ERROR}

	log_level = log_level.get(get_config('system', 'debug_lever', 'INFO'), log.DEBUG)
#	log_file = get_config('system', 'log_file', 'ftp_log.txt')
	log_file = 'ftp_log.txt'
	print os.path.join(work_dir,log_file)

	log.basicConfig(filename = os.path.join(work_dir, log_file), level = log_level, \
			format ='%(levelname)-10s;%(asctime)s;%(filename)-15s[%(lineno)3d][%(process)-5d];%(message)s',\
			datefmt='%Y-%m-%d %H:%M:%S')

def process(task_data):
	'''
		在此文件添加的用户才能访问ftp服务
	'''
#	log.info("ftp server starting")
	authorizer = DummyAuthorizer()
	if platform.system() == 'Linux':
		authorizer.add_user("hanshow", "hanshow", "/home/gee/ftpshare/", perm="elradfmwM")
#允许多个账户加入ftp只需重复调用add_user
		authorizer.add_user("gee", "gee", "/home/gee/ftpshare/", perm="elradfmw")
#这样就允许两个账户(hanshow gee)就能用ftp服务了
	else: # windows
		authorizer.add_user("hanshow", "hanshow", "C:\\ftp", perm="elradfmwM")
		authorizer.add_user("gee", "gee", "C:\\ftp", perm="elradfmw")

#    |     Read permissions:
#    |       - "e" = change directory (CWD command)
#    |       - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
#    |       - "r" = retrieve file from the server (RETR command)
#    |      
#    |      Write permissions:
#    |       - "a" = append data to an existing file (APPE command)
#    |       - "d" = delete file or directory (DELE, RMD commands)
#    |       - "f" = rename file or directory (RNFR, RNTO commands)
#    |       - "m" = create directory (MKD command)
#    |       - "w" = store a file to the server (STOR, STOU commands)
#    |       - "M" = change file mode (SITE CHMOD command)


	handler = FTPHandler
	handler.authorizer = authorizer
	
#开启ftp log 日志功能 写入到ftp_log.txt中
#	start_log()
	log.basicConfig(filename='./ftp_log.txt',level = log.INFO)
	server = FTPServer(('0.0.0.0', 9005), handler)
	server.serve_forever()

def start(task_data):
	'''启动ftp服务,并返回进程对象'''
	proc = multiprocessing.Process(target = process, args = (task_data,))
	proc.start()
	return proc

if __name__ == '__main__':
	start(None)
