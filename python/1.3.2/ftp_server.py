#encoding=utf-8
import platform ,multiprocessing,threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os, sys, time, socket
import logging
import logging.handlers
from esl_init import log, conf


def process(task_data):
	'''
		在此文件添加的用户才能访问ftp服务
	'''
	
	log.info("ftp server starting")
	ftp_file_name = 'ftp'

	try:
		os.mkdir(ftp_file_name,0777)
	except Exception,e:
		pass
	authorizer = DummyAuthorizer()
	
	user = conf.htp.ftp_user
	passwd = conf.htp.ftp_pass


	authorizer.add_user(user, passwd, ftp_file_name, perm="elradfmwM")
#允许多个账户加入ftp只需重复调用add_user
#这样就允许两个账户(hanshow gee)就能用ftp服务了

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
	
	try:
		port = int(conf.htp.ftp_port)
		server = FTPServer(('0.0.0.0', port), handler)
		while True:
			try:
				if task_data['isquit']['ftp_server']:
					server.close_all()
					break
				server.serve_forever(5, False, False)
			except Exception,e:
				log.error_msg("<ftp error> : %s" % e, errid='EFT001')
				time.sleep(10)
	except Exception,e:
		log.error_msg("<FTPServer error> : %s" % e, errid='EFT002')

	log.info("ftp server exit")

def ftp_exit():
	port = int(conf.htp.ftp_port)
	server = conf.htp.ftp_server

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((server, port))
		s.shutdown(2)
	except Exception, e:
		pass

def start(task_data):
	'''启动ftp服务,并返回进程对象'''
	proc = threading.Thread(target = process, args = (task_data,))
	
	proc.start()
	return proc
