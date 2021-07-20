#!/usr/bin/env python

import os, sys, time, xmlrpclib
from esl_init import get_config

#cp this file to /etc/rc.local

main_dir = "/opt/esl-working/main.py"

def parnet_xmlserver_restart():
	pass

def hanshow_xmlserver_restart():
	os.system("python " + main_dir + " restart")

while True:
		
	try:
		parnet_xmlserver = xmlrpclib.ServerProxy("http://127.0.0.1:8880", allow_none=True)
		if parnet_xmlserver.stationHandler.send_cmd("HELLO",[{}]) != 'OK':
			parnet_xmlserver_restart()
	except Exception, e:
		print e
		parnet_xmlserver_restart()
	
	try:
		hanshow_xmlserver = xmlrpclib.ServerProxy("http://127.0.0.1:9000", allow_none=True)
		if hanshow_xmlserver.send_cmd("HELLO", [{}]) != 'OK':
			hanshow_xmlserver_restart()
	except Exception, e:
		print e
		hanshow_xmlserver_restart()
	
	time.sleep(3)

