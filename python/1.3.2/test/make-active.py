import os, sqlite3 
import xmlrpclib, time, random 

conn = sqlite3.connect("db.sqlite")
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
curs = conn.cursor()


server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")

#cmd = "select count(nw1), nw1 from esl_list where eslid in (select eslid from bind_list where apid in (select apid from ap_list)) group by nw1"
#cmd = "select count(nw1), nw1, a.apid from esl_list e,  bind_list b, ap_list a  where b.apid=a.apid and e.eslid=b.eslid group by nw1, a.apid"
cmd = "select eslid, apid, salesno from bind_list"
curs.execute(cmd)

bind_list = []
for row in curs.fetchall():
	bind_list.append({"eslid":row[0], "salesno":row[1], "apid":row[2]})

print server.send_cmd("BIND", bind_list)

