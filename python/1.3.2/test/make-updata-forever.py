import os, sqlite3, sys 
import xmlrpclib, time, random

server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")

conn = sqlite3.connect("db.sqlite")
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
curs = conn.cursor()

esl_table_title = ['nw1','eslid','nw2','nw3','nw4','op1', 
	'op2','op3','op4','lastworktime', 'status']
bind_table_title = ['eslid','salesno','apid']


cmd = 'select eslid from bind_list'
curs.execute(cmd)
eslid = [row[0] for row in curs.fetchall()]


def count_bind(price):
	cmd = 'select count(*) from sales_list where Price ="%s"' % (price)
	curs.execute(cmd)
	return [row[0] for row in curs.fetchall()][0]

def clear_status(status):
	cmd = 'update esl_list set status ="%s" where eslid in (select eslid from bind_list)' % (status)
	curs.execute(cmd)
	conn.commit()

def count_status(status):
	cmd = 'select count(*) from esl_list e, bind_list b where e.status ="%s" and b.eslid=e.eslid' % (status)
	curs.execute(cmd)
	return [row[0] for row in curs.fetchall()][0]

total_use, total_n = 0, 0

def run():
	global total_use
	global total_n

	for n in xrange(500):
		eslinfo = []

		updata_list = []
		price = str(random.randint(1,9999))
		start_time = time.asctime()
		sys.stdout.write("Task %s, %s, %s" % (n, price, start_time))
		sys.stdout.flush()

		cmd = "select distinct salesno from bind_list"
		curs.execute(cmd)
		for row in curs.fetchall():
				 updata_list.append({"salesno":row[0], "Price":price, "Price1":price, "Price2":"64", "Price3":price, "sid":str(price), "spec":"aaa"})

		clear_status("aaaa")
		count = count_status("aaaa")
		server.send_cmd("SALES_UPDATA_BUF", updata_list)

		while True:
			time.sleep(1)
			ok = count_status("online")
			failed = count_status("offline")
			
			if (ok + failed == count):
				break

		end_time = time.asctime()
		els_time = time.mktime(time.strptime(end_time, "%a %b %d %H:%M:%S %Y")) - time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
		sys.stdout.write(", %s, use %s sec, ok %s, pass %0.4f\n" %(end_time, els_time, ok, float(ok) / count))
		sys.stdout.flush()
		total_use += els_time
		total_n += 1

		time.sleep(10)

if __name__ == '__main__':
	try:
		run()
	except KeyboardInterrupt, e:
		pass
	except Exception, e:
		pass

	if total_n > 0:
		sys.stdout.write("\ntotal run %s, ava %s\n" % (total_n, total_use/total_n))


