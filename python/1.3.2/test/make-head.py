import os, sqlite3 
import xmlrpclib, time, random 

conn = sqlite3.connect("db.sqlite")
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
curs = conn.cursor()

server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")

cmd = "select eslid from bind_list"
curs.execute(cmd)

esl_list = []
for row in curs.fetchall():
	esl_list = []
	esl_list.append({"eslid":row[0]})
	val = server.send_cmd("GET_AP_LEVEL", esl_list)
	if 'error' in val:
		continue
	ret, ack = val
	v = ack[0]
	if v['ap_level'] == []:
		continue
	print "%s;%s;%s" % (v['eslid'], len(v['ap_level']), v['ap_level'])


