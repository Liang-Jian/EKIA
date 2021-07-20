# -*- coding: utf-8 -*-

# 汉朔价签系统生产web后台作为windows服务
# Author  cwtao@hanshows.com

# 安装服务
# python web_service.py install

# 让服务自动启动
# python web_service.py --startup auto install 

# 启动服务
# python web_service.py start

# 重启服务
# python web_service.py restart

# 停止服务
# python web_service.py stop

# 删除/卸载服务
# python web_service.py remove




import win32serviceutil
import win32service
import win32event
import time,sys,multiprocessing,os
import win32process
from esl_init import log

	
class web_service(win32serviceutil.ServiceFramework):
    _svc_name_ = "Hanshow web sevice"
    _svc_display_name_ = "Hanshow ESL Web Server"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    def SvcStop(self):
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
    def SvcDoRun(self):
        #what to do# 
        path = os.path.split(os.path.realpath(__file__))[0]
        #os.chdir(sys.path[0])#切换工作路径
        os.chdir(path)#切换工作路径

        if os.path.exists("web_manufacture.py"):
            os.system("python web_manufacture.py")
        else:
            os.system("python web_manufacture.pyc")

        win32event.WaitForSingleObject(self.hWaitStop, 0)  #win32event.INFINITE)

if __name__=='__main__':
    if sys.platform.startswith('win'):
        pass
    else:
        os.exit(-1)
        
    if len(sys.argv) <= 1:
        log.info("web_service lack para")
    else:
        log.info("web_service %s" % sys.argv[1])

	win32serviceutil.HandleCommandLine(web_service)