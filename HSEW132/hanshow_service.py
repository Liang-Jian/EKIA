# -*- coding: utf-8 -*-


import win32serviceutil
import win32service
import win32event
import time,sys,multiprocessing,os
import mmap
import win32process
from esl_init import log

	
class hanshow_service(win32serviceutil.ServiceFramework):
    _svc_name_ = "Hanshow sevice"
    _svc_display_name_ = "Hanshow ESL Server"

    def __init__(self, args):

		win32serviceutil.ServiceFramework.__init__(self, args)

		# Create an event which we will use to wait on.
		# The "service stop" request will set this event.
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		self.mm = None
		self.main_handle = None
		self.ret = 0
    def SvcStop(self):
		# Before we do anything, tell the SCM we are starting the stop process.
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		# And set my event.
		if self.ret == 0:
			self.mm.seek(0)
			self.mm.write("quite") 
			self.mm.close()
		time.sleep(2)
		log.info("HanshowService stop")


	
    def SvcDoRun(self):
		#what to do# 
		path = os.path.split(os.path.realpath(__file__))[0]
		#os.chdir(sys.path[0])#切换工作路径
		os.chdir(path)#切换工作路径
		
		self.mm = mmap.mmap(-1,1024,access=mmap.ACCESS_WRITE, tagname='esl-working-share-mmap')
		self.mm.seek(0)
		self.mm.write("start") 
		
		if os.path.exists("main.py"):
			self.ret = os.system("python main.py")
		else:
			self.ret = os.system("python main.pyc")
#		log.info(" main return values is %s " % self.ret)		
		if self.ret != 0:
			self.mm.seek(0)
			self.mm.write("exits")
			self.mm.close()

		
		# self.main_handle = win32process.CreateProcess('c:\\python27\\python main.py',None,None,0,win32process,CREAT_NO_WINDOW,
			# None,None,win32process.STARTUPINFO())
		win32event.WaitForSingleObject(self.hWaitStop, 0)  #win32event.INFINITE)

if __name__=='__main__':
	if sys.platform.startswith('win'):
		pass
	else:
		os.exit(-1)
		
	if len(sys.argv) <= 1:
		print (
		'''
# start as service
 python hanshowService.py --startup auto install 
 python hanshowService.py start

# restart
 python hanshowService.py restart

# stop
 python hanshowService.py stop

# remove
 python hanshowService.py remove
		'''
		)
	else:
		log.info("hanshowService %s" % sys.argv[1])

	win32serviceutil.HandleCommandLine(hanshow_service)
