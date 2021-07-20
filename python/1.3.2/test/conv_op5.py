import os, sqlite3, sys 
import xmlrpclib, time, random
import database

db = database.DB()

conn = sqlite3.connect("db.sqlite")
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
curs = conn.cursor()

cmd = 'select eslid, op3, op5, op6, op8, op9 from esl_list'
curs.execute(cmd)

op5_list = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in curs.fetchall()]

for (eslid, op3, op5, op6, op8, op9) in op5_list:
	if not eslid or len(eslid) != 11:
		print "eslid", eslid, "invalid"
		continue

	if op5:
		try:
			op5 = eval(op5, {}, {})
			db.change_esl_op5_without_commit(eslid, op5)
		except Exception, e:
			print eslid, op5, e

	if op6:
		try:
			op6 = eval(op6, {}, {})
			db.change_esl_op6_without_commit(eslid, op6)
		except Exception, e:
			db.change_esl_op6_without_commit(eslid, {})
			print eslid, op6, e, "set to default {}"
	
	if not op6 and "5104" not in op3:
		db.change_esl_op6_without_commit(eslid, {})
	
	if not op8:  #retry max
		if "5104" not in op3: 
			if "5103" in op3:
				db.change_key_val_without_commit(db.esl, eslid, "op8", "12")
			else:
				db.change_key_val_without_commit(db.esl, eslid, "op8", "6")
	
	if not op9:  #direction
		dire = op5.get('resolution_direction', '0')
		db.change_key_val_without_commit(db.esl, eslid, "op9", str(dire))

db.conn.commit()

