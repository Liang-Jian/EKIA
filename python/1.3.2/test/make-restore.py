# encoding: utf-8
import os, xmlrpclib, database, time

db = database.DB()

query_list, active_list = [], []
esl_list = db.key_list(db.bind)

for id1 in esl_list:
	info = db.get_all_info(db.esl, id1)
	info.update(db.get_all_info(db.bind, id1))
	info['status'] = 'online'
	for k in info.keys():
		if info[k] == None:
			info.pop(k)
	try:
		info['op5'] = database.uniode2str(eval(info['op5'], {}, {}))
		info['op6'] = database.uniode2str(eval(info['op6'], {}, {}))
	except Exception, e:
		print "esl %s id error" % id1
		continue

	query_list.append({"salesno":info['salesno']})
	active_list.append(info)

db.conn.commit()
db.conn.close()

server = xmlrpclib.ServerProxy('http://192.168.1.152:8088/shop-web/stationHandler')
#print query_list, active_list

#同步商品信息
#print server.stationHandler.send_cmd("SALES_QUERY", query_list)

#同步绑定关系
print server.stationHandler.send_cmd("ESL_ACTIVE", active_list)
#for x in range(100):
#	print server.stationHandler.send_cmd("ESL_ACTIVE", active_list)
#	time.sleep(3600)

