# encoding:utf-8

import xmlrpclib
from database import DB
from time import sleep

'''
绑定表价签与商品表内的商品一一绑定
'''
server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")
db = DB()
cmd = 'select eslid from esl_list'
db.cursor.execute(cmd)
all_esl = db.cursor.fetchall()

cmd1 = 'select salesno from sales_list'
db.cursor.execute(cmd1)
all_sales = db.cursor.fetchall()

esl_list = []
for eslid in all_esl:
	eslid = eslid[0]
	esl_list.append(eslid)

salesno_list = []	
for salesno in all_sales:
	salesno = salesno[0]
	salesno_list.append(salesno)

bind_all_list = []
for i in range(0, len(salesno_list)-1):
	bind_all_list.append({'apid': '1', 'salesno': '%s' % salesno_list[i], 'eslid': '%s' % esl_list[i]})
	
	
server.send_cmd("BIND", bind_all_list)
