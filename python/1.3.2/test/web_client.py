# coding: utf-8

import web, sqlite3, xmlrpclib, random, os, multiprocessing, random, time, datetime
from osd import _init_esl as get_template_list
import esl_init
from esl_init import conf

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

LINE_CUT = 6
PASS_RATE = 0.9 #单个价签更新成功率合格底线

about_me = '''

<h1>使用说明</h1>
<h2>价格更新</h2>
对价签进行更新，可以指定更新对次数，更新的价格，使用的模版。
<h2>绑定</h2>
用于批量绑定价签。需要手动将绑定的价签ID清单拷贝到文本框中，每行一条，ID格式可以是"546a7d"的格式，也可以是“53-6A-7D-99”的格式。
<br>提交绑定后，系统会自动将未绑定过价签的商品分配给价签，同时将自动分配基站，保证每个基站挂载的价签组大致相等。
<br>提交绑定时，默认将清除以前的绑定记录。提交时需要看清楚。
<h2>解绑</h2>
解除指定价签的绑定关系，ID格式和绑定一样.
<br>此解绑操作不会促发刷OFF的操作。
<h2>查询</h2>
查询指定价签，ID格式和绑定一样。
<br>提交查询后将跳转到实时统计页面，ACK值返回1表示查询成功，0表示通讯失败，2表示低电量，其它值表示RF异常。
<h2>实时统计</h2>
提交价格更新后，系统将跳转到这个页面。每隔10秒刷新以此页面，实时显示更新结果。
<br>如果价签通讯成功率低于90%，价签ID将会在页面上标红。反之则为绿色。
<br>当对某些价签更新了10轮，若有一个价签更新失败轮2次，则将标为红色。
<br>当更新结束后，此页面将显示每次更新的开始时间、结束时间、耗时和总体成功率，并统计出失败价签清单，ACK值分布情况。
<h2>运行日志</h2>
输出后台系统的运行日志。此页面不会自动刷新。
<h2>数据库操作</h2>
<h3>数据库导入</h3>
可以通过此页面导入价签ID文件、测试商品信息，以及绑定关系。
<br>此3个文件都是csv格式，支持逗号或分号为风格符。
<br>价签ID文件一般会发送给生产部门，研发服务器上也有备份。
<h3>SQL命令</h3>
可以通过页面输入数据库命令进行数据库操作
<h2>手动组网</h2>
此功能用于手动对价签进行重新组网，修改价签的网络参数。
<br>使用此功能前，需要保证待组网价签能够正常通讯上。
<br>可以对单个价签或者多个价签组到一起，价签ID格式与绑定移植。wakeupid格式必须是完整的，比如"5A-04-33-66"，channel时合法的数字，值为10～160之间。
'''

log_file = conf.system.log_file
test_mode = conf.system.testmode

SLAES_UPDATA_FILE = "tmp_sales_updata_task.txt"

def list_update_status(times, curs, ret):
	i = 0
	h = '<br>价签更新结果\
		<br>总共更新%s次，成功率低于%s将标红\
		<br><价签ID,商品ID,成功次数,失败次数>\
		<table border=1>' % (times,PASS_RATE)
	for k in ret:
		if i % LINE_CUT == 0:
			h = h + '<tr>'

		success = ret[k]["online"]
		failed = ret[k]["offline"]
		p = float(success) / (success + failed)
		c = color("online") if p > PASS_RATE else color("offline")

		h = h + '<td BGCOLOR=%s>%s</td>' % (c , k)
		h = h + '<td>%s</td>' % ret[k]["salesno"]
		h = h + '<td>%s</td>' % success
		h = h + '<td>%s</td>' % failed
		if i % LINE_CUT == LINE_CUT -1:
			h =  h + '</tr>'
		i = i + 1

	if (i -1) % LINE_CUT != LINE_CUT - 1:
		h =  h + '</tr>'
	h = h + '</table>'

	return h

def col_one_time(curs, esllist, ret):
	for e in esllist:
		cmd = 'select status from esl_list where eslid="%s"'  % e
		curs.execute(cmd)
		status = [row[0] for row in curs.fetchall()][0]
		try:
			i = ret.setdefault(e, {"salesno":"  ", "online":0, "offline":0, "waiting":0})[status]
			ret[e][status] = i + 1
		except KeyError, e:
			pass

def ack_count():
	ret = "\nACK值分布:\n"
	cmd = "grep ack_list %s | cut -d';' -f5  | tr '()' '\n\n' | grep -E \"^'\"" % log_file
	cmd_ack = cmd + "| cut -d \",\" -f4 | sort | uniq -c"
	ret = ret + os.popen(cmd_ack).read()

	ret = ret + "\n失败价签统计\n"
	cmd_id = "grep \"update failed\" %s | cut -d\";\" -f4 | cut -d\" \" -f2 |sort | uniq -c" % log_file
	ret = ret + os.popen(cmd_id).read()

	ret = ret + "\n失败ACK分布\n"
	cmd_failed = cmd + "| cut -d \",\" -f2,4 | grep -v \", 1$\" | sort | uniq -c | sort -rn"
	ret = ret + os.popen(cmd_failed).read()

	return ret

def list_failed_group(curs, f):
	cmd = "select e.nw1, e.nw3, count(*), s.status from esl_list e, sales_list s, bind_list b where b.eslid=e.eslid and b.salesno=s.salesno and e.status<>'online' group by e.nw1, e.nw3, s.status"
	curs.execute(cmd)
	f.write("[")
	for row in curs.fetchall():
		f.write("(%s,%s)," % (row[0][6:8], row[2]))
	f.write("]")

def db_set_op5_dire(esl_list, curs, dire):
    op5_list = []
    for id1 in esl_list:
        cmd = "select eslid, op5 from esl_list where eslid='%s'" % id1
        curs.execute(cmd)
        for row in curs.fetchall():
            op5 = {"eslid":row[0], "op5":eval(row[1],{},{})};
            op5['op5']['resolution_direction'] = dire
            op5_list.append(op5)
    print "esl_add", op5_list
    send_cmd("ESL_ADD", op5_list)

def clear_status_all(curs, conn):
	cmd = 'update esl_list set status = "%s"' % ("")
	curs.execute(cmd)
	conn.commit()

def clear_status(status, curs, conn, esllist):
	for e in esllist:
		cmd = 'update esl_list set status = "%s" where eslid = "%s"' % (status, e)
		curs.execute(cmd)
	conn.commit()

def count_status(status, curs, conn, esllist):
	c = 0
	for e in esllist:
		cmd = 'select count(*) from esl_list e where e.status = "%s" and eslid= "%s"' % (status, e)
		curs.execute(cmd)
		c += [row[0] for row in curs.fetchall()][0]
	return c

def sales_updata_task(times, sleeps, price, updata_list):
	
	conn = sqlite3.connect("db.sqlite", timeout=120)
	conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
	curs = conn.cursor()
	ret = {}

	with open(SLAES_UPDATA_FILE, 'w') as f:
		for n in xrange(int(times)):

			price = str(price);
			#db_set_op5_dire([i['spec'] for i in updata_list], curs, n % 4)

			start_time = time.asctime()
			f.write("%d/%d: %s, %s" % (n+1, int(times), price, time.strftime("%Y%m%d %H:%M:%S")))
			f.flush()
			if n % 10 == 0:
				os.system("rm -rf ./cache")
			esllist = []
			for item in updata_list:
				item['sid'] = price
				item['Price'] = price
				for x in item['esllist']:
					esllist.append(x['eslid'])
	
			clear_status_all(curs, conn)
			clear_status("waiting", curs, conn, esllist)
			count = count_status("waiting", curs, conn, esllist)
			send_cmd("SALES_UPDATA_BUF", updata_list)
                        f_50, f_60, f_70, f_80, f_90 = False, False, False, False, False
			while True:
				time.sleep(1)
				ok = count_status("online", curs, conn, esllist)
				failed = count_status("offline", curs, conn, esllist)
                                if (ok + failed >= count/10*5 and not f_50):
                                        els_time = time.mktime(time.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y")) - \
                                                   time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
                                        f.write(', 50%% %s' % els_time)
                                        f.flush()
                                        f_50 = True
                                if (ok + failed >= count/10*6 and not f_60):
                                        els_time = time.mktime(time.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y")) - \
                                                   time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
                                        f.write(', 60%% %s' % els_time)
                                        f.flush()
                                        f_60 = True
                                if (ok + failed >= count/10*7 and not f_70):
                                        els_time = time.mktime(time.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y")) - \
                                                   time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
                                        f.write(', 70%% %s' % els_time)
                                        f.flush()
                                        f_70 = True
                                if (ok + failed >= count/10*8 and not f_80):
                                        els_time = time.mktime(time.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y")) - \
                                                   time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
                                        f.write(', 80%% %s' % els_time)
                                        f.flush()
                                        f_80 = True
                                if (ok + failed >= count/10*9 and not f_90):
                                        els_time = time.mktime(time.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y")) - \
                                                   time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
                                        f.write(', 90%% %s' % els_time)
                                        f.flush()
                                        f_90 = True
				if (ok + failed == count):
					break

			end_time = time.asctime()
			els_time = time.mktime(time.strptime(end_time, "%a %b %d %H:%M:%S %Y")) - time.mktime(time.strptime(start_time, "%a %b %d %H:%M:%S %Y"))
			if failed == 0:
				f.write(", %s, use %s sec, ok %s, <font color='green'>PASS</font> %0.4f" % \
					(time.strftime("%Y%m%d %H:%M:%S"), els_time, ok, float(ok) / count))
			else:
				f.write(", %s, use %s sec, ok %s, <font color='red'>failed</font> %0.4f, " % \
					(time.strftime("%Y%m%d %H:%M:%S"), els_time, ok, float(ok) / count))
				list_failed_group(curs, f)

			f.write(".\n")
			f.flush()
			time.sleep(int(sleeps))

			price = str(random.randint(1,10)/0.91)
			col_one_time(curs, esllist, ret)

		f.write(list_update_status(times, curs, ret))

def send_cmd(cmd, args):
	server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")
	return str(server.send_cmd(cmd, args))

def js(h):
	h = h + '<head><script language="javascript">\
	function checkAll(idn){\
 		for (var i=0;i<document.forms[idn].elements.length;i++)\
 		{\
  			var e=document.forms[idn].elements[i];\
  			if ((e.name != "allbox") && (e.type=="checkbox"))\
 			{\
   			e.checked=document.forms[idn].allbox.checked;\
 			}\
 		}\
	}\
	</script></head>'

	return h

def js_reload(h):
	h = h + '<script language="JavaScript">\
	function myrefresh() \
	{ \
		window.location.reload();\
	} \
	setTimeout("myrefresh()",10000);\
	</script>'
	
	return h


def col(src):
	d = {"online":0, "offline":0,"waiting":0}
	for (_,_,_,s) in src:
		if s not in d:
			d[s] = 0
		d[s] = d[s] + 1

	return d["online"], d["offline"], d["waiting"]

def price_status(h, src):
	price = random.randint(1,10) / 0.91
	h = h + '<tr>'
	#价格
	h = h + '<td colspan=2>刷新价格</td><td><input type="text" name="price" value="%.2f" size="8"></td>' % price
	#刷几次
	h = h + '<td colspan=3>刷新次数</td><td><input type="text" name="times" value="1" size="3"></td>'
	#间隔时间
	h = h + '<td colspan=3>间隔时间</td><td><input type="text" name="sleep" value="1" size="3"></td>'
	#模板
	
	temp_src = conf.system.temp_json
	if temp_src == 'no':
		temp_list = get_template_list().keys()
	else:
		temp_list = os.listdir("temp_json") 
		if "esl_temp.txt" in temp_list:
			temp_list.remove("esl_temp.txt")

	h = h + '<td colspan=2>模板</td><td colspan=3><select name="template">'

	success, failed, updating = col(src)
	total = success+ failed + updating
	if total == 0:
		total = 1
	pass_rate = float(success) / total

	for n in temp_list:
		h = h + '<option value="%s">%s' % (n, n)
	h = h + '</td>'

	h = h + '<td colspan=3 BGCOLOR=%s>更新成功 %s</td>' % (color("online"),success)
	h = h + '<td colspan=3 BGCOLOR=%s>更新失败 %s</td>' % (color("offline"),failed)
	h = h + '<td colspan=3 BGCOLOR=%s>更新中 %s</td>' % (color("waiting"),updating)
	h = h + '<td colspan=3>成功率 %0.2f%%</td>' % (pass_rate*100)
	h = h + '</tr>'

	return h

def color(status):
	if status == 'online':
		return "#228B22"
	if status == "offline":
		return "#FF00AF"
	if status == "waiting":
		return "#FFD700"
	return "#FFFFFF"

def table_select(values):
	h = ""
	i = 0
	for v in values:
		i = i + 1
		v1 = ''.join(v.split('-'))
		h =  h + "<option %s value='%s'>%s" % ('selected' if i == 1 else "", v, v1)
	return h

def table_bind(curs, src):

	cmd = "select eslid from esl_list"
	curs.execute(cmd)
	esl_list = [row[0] for row in curs.fetchall()]

	#cmd = "select salesno from sales_list"
	cmd = "select salesno from sales_list where salesno not in (select salesno from bind_list)"
	curs.execute(cmd)
	sales_list = [row[0] for row in curs.fetchall()]

	cmd = "select apid from ap_list"
	curs.execute(cmd)
	ap_list = [row[0] for row in curs.fetchall()]

	h = '<html><br>绑定功能<table border=1>'
	'''
	h = h + '<form method="post" action="/bind">'
	h = h + '<tr><td>价签ID <select name="eslid" size="8" multiple="multiple" >'+table_select(esl_list)+'</select></td><tr/>'
	h = h + '<tr><td>商品ID <select name="salesno" size="4" multiple="multiple">'+table_select(sales_list)+'</select></td></tr>'
	h = h + '<tr><td>基站ID <select name="apid">'+table_select(ap_list)+'</select></td></tr>'
	h = h + '<tr><td><input type="submit" value="绑定">\
				<input type="reset" value="重置"></td>'
	h = h + '</tr></form></table>'
	'''

	#批量方式
	h = h + "<br>批量绑定(只需要价签号)"
	h = h + "<br>格式:536677,或者53-66-77-99"
	h = h + '<table border=1><form method="post" action="/bind2">'
	h = h + '<tr><td><textarea name="multi_list" rows="20"></textarea></td></tr>'
	h = h + '<tr><td>基站ID <select name="apid2">'+table_select(ap_list)+'</select></td></tr>'
	h = h + '<tr><td>先清除绑定关系 <input type="checkbox" checked name="clear" value="yes"></td></tr>'
	h = h + '<tr><td><input type="submit" value="批量提交">\
				<input type="reset" value="重置"></td></tr>'
	h + h + '</form></table>'
	
	h = h + '</html>'

	return h

def table_netlink(src):
	h = "<br>手动组网功能"
	h = h + "<br>批量组网(只需要价签号)"
	h = h + "<br>格式:536677,或者53-66-77-99"
	h = h + '<table border=1><form method="post" action="/netlink">'
	#通过文本框提交
	h = h + '<tr><td><textarea name="multi_list" rows="20"></textarea></td></tr>'
	h = h + '<tr><td>Wakeupid<input type="text" name="nw1" size="16"></td></tr>'
	h = h + '<tr><td>Channel<input type="text" name="nw3" size="8"></td></tr>'
	h = h + '<td><input type="submit" value="组网"><input type="reset" value="重置"></td>'
	h = h + '</tr></form></table>'

	return h

def table_query(src):
	h = "<br>查询功能"
	h = h + "<br>批量查询(只需要价签号)"
	h = h + "<br>格式:536677,或者53-66-77-99"
	h = h + '<table border=1><form method="post" action="/query">'
	#通过文本框提交
	h = h + '<tr><td><textarea name="multi_list" rows="20"></textarea></td></tr>'
	h = h + '<td><input type="submit" value="查询"><input type="reset" value="重置"></td>'
	h = h + '</tr></form></table>'

	return h

def table_unbind(src):
	h = "<br>解绑功能"
	h = h + "<br>批量解绑(只需要价签号)"
	h = h + "<br>格式:536677,或者53-66-77-99"
	h = h + '<table border=1><form method="post" action="/unbind">'
	'''
	i = 0
	for line in src:
		if i % LINE_CUT == 0:
			h = h + '<tr>'
		h =  h + '<td><input type="checkbox" NAME="%s", value="%s"></td>' % (line[0],line[0])
		h = h + '<td>' + line[0] + '</td>'
		if i % LINE_CUT == LINE_CUT -1:
			h =  h + '</tr>'
		i = i + 1

	if (i -1) % LINE_CUT != LINE_CUT - 1:
		h =  h + '</tr>'


	h = h + '<tr><td><input type="checkbox" value="on" name="allbox" onclick="checkAll(0);"/></td>'
	'''

	#通过文本框提交
	h = h + '<tr><td><textarea name="multi_list" rows="20"></textarea></td></tr>'
	h = h + '<td><input type="submit" value="解绑"><input type="reset" value="重置"></td>'
	h = h + '</tr></form></table>'

	return h

def table_format(curs, src):
	i = 0

	html = js("<html>")

	html = html + '<body>'
	html = html + '<br>刷新功能<table border=1>'
	html = html + '<form method="post" action="/" >'
	html = price_status(html, src)

	for line in src:
		if i % LINE_CUT == 0:
			html = html + '<tr>'
		html =  html + '<td><INPUT TYPE="checkbox" NAME="%s", value="%s"></td>' % (line[0],line)
		j = 0
		for ele in line[0:-1]:
			if j == 0:
				html = html + '<td BGCOLOR=%s>' % color(line[-1]) + ele + '</td>'
			else:
				html = html + '<td>' + ele + '</td>'
			j = j +1
		if i % LINE_CUT == LINE_CUT -1:
			html =  html + '</tr>'
		i = i + 1

	if (i -1) % LINE_CUT != LINE_CUT - 1:
		html =  html + '</tr>'

	html = html + '<tr> <td><input type="checkbox" value="on" \
						name="allbox" onclick="checkAll(0);"/></td> \
						<td><input type="submit" value="提交"/>\
						<input type="reset", value="重置"/></td>\
						</tr>'
	html = html + '</form>'
	html =  html + '</table>'

	html = html +"</body></html>"

	return html

def url_home():
	h = "<a href = '/'>返回</a><br>"
	return h

def url_menu():
	h = "<html><head></head><body>"
	h = h + '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><table border=0><tr>'
	h = h + '<td><a href=/updata>价格更新</a></td>'
	h = h + '<td><a href=/bind>绑定</a></td>'
	if test_mode ==  "advance":
		h = h + '<td><a href=/unbind>解绑</a></td>'
		h = h + '<td><a href=/query>查询</a></td>'
	h = h + '<td><a href=/report>实时统计</a></td>'
	if test_mode ==  "advance":
		h = h + '<td><a href=/log>运行日志</a></td>'
	h = h + '<td><a href=/upload>数据库操作</a></td>'
	if test_mode ==  "advance":
		h = h + '<td><a href=/netlink>手动组网</a></td>'
	h = h + '<td><a href=/help>使用说明</a></td>'
	h = h + '</tr></table>'
	return h

#database app
def get_all_bind_list(curs):
	cmd = 'select b.eslid, b.salesno, b.apid, e.status from esl_list e, bind_list b, sales_list s \
			where s.salesno = b.salesno and b.eslid = e.eslid'
	curs.execute(cmd)
	bind_list = [row for row in curs.fetchall()]
	return bind_list

def db_set_temp(esl_list, tempname):
	for key  in ['price', 'times', 'template', 'allbox', 'sleep']:
		if key in esl_list:
			esl_list.remove(key)
	
	add_cmd = [{"eslid":eslid, "op4":tempname} for eslid in esl_list]
	send_cmd("ESL_ADD", add_cmd)

def sales_updata(data):
	h = "total update %s esl, price is %s, %s times, user template %s.<br>"\
		% (len(data) -3, data['price'], data['times'], data['template'])

	#修改模板
	#db_set_temp(data.keys(), data['template'])

	sales_list = {}
	for key in data:
		if key not in ['price', 'times', 'template', 'allbox', 'sleep']:
			sales_list[(eval(data[key])[0], eval(data[key])[1])] = 0
	sales_list = sales_list.keys()

	price = str(data['price'])
	if price == '0':
		price = str(random.randint(1,10) / 0.91)

	sid = random.randint(1,10000)
	t = time.localtime()
	t = "%4d-%02d-%02d" % (t[0],t[1],t[2])

	updata_buf = [{'sid':str(sid), 'salesno':salesno, "Price":price, "spec":eslid, "Price1":price, \
		"Price2":"65535", "Price3":price, "location":t, "esllist":[{"eslid":eslid}]}\
		for (eslid, salesno) in sales_list]

	multiprocessing.Process(target = sales_updata_task, \
			args = (data['times'], data['sleep'], data['price'], updata_buf)).start()

	return h + str(updata_buf)

#web app
urls = (
	'/', 'updata',
	'/bind', 'bind',
	'/bind2', 'bind2',
	'/unbind', 'unbind',
	'/updata', 'updata',
	'/upload', 'upload',
	'/dbview', 'dbview',
	'/query', 'query',
	'/report', 'report',
	'/log', 'log',
	'/netlink', 'netlink',
	'/help', 'web_help',
	)

class db:
	def __init__(self):
		conn = sqlite3.connect("db.sqlite", timeout=120)
		conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		curs = conn.cursor()
		self.curs = curs
		self.conn = conn

def check_eslid(esl1):
	if len(esl1) == 11:
		return esl1.upper()

	eslid = list(esl1.upper())
	eslid.insert(2,'-')
	eslid.insert(5,'-')
	eslid.insert(8,'-')
	eslid.append('99')
	return ''.join(eslid)

class bind2(db):
	def POST(self):
		data = web.input()
		esl_list = data["multi_list"].splitlines()
		esl_list = [check_eslid(esl1) for esl1 in esl_list]
		n = len(esl_list)
		ap_list = [data['apid2']] * n
		data['salesno2'] = u"随机商品"

		if 'clear' in data and data['clear'] == 'yes':
			#先清空绑定表
			self.curs.execute("delete from bind_list")
			self.conn.commit()

		if data['salesno2'] == u"随机商品":
			cmd = "select salesno from sales_list where salesno not in (select salesno from bind_list)"
			self.curs.execute(cmd)
			sales_list = [row[0] for row in self.curs.fetchall()][:n]
		else:
			sales_list = data['salesno2'] * n
		
		bind_cmd = [{"eslid":e, "salesno":s, "apid":a} for (e,s,a) in zip(esl_list, sales_list, ap_list)]
		send_cmd("BIND", bind_cmd)
		time.sleep(5)
		raise web.seeother('/updata')

class bind(db):
	def GET(self):
		src = get_all_bind_list(self.curs)
		return url_menu() + table_bind(self.curs, src)

	def POST(self):
		data = web.input()
		bind_list = [{"eslid":data["eslid"], "salesno":data["salesno"],\
				"apid":data["apid"]}]
		send_cmd("BIND", bind_list)

		raise web.seeother('/updata')

class netlink(db):
	def GET(self):
		return url_menu() + table_netlink(self.curs)

	def POST(self):
		data = web.input()
		esl_list = data["multi_list"].splitlines()
		net_list = [{"eslid":check_eslid(esl1), "nw1":check_eslid(data["nw1"]), "nw3":str(data["nw3"])} \
			for esl1 in esl_list]
		save_log_file("netlink")
		send_cmd("ESL_NETLINK", net_list)
		raise web.seeother('/log')

class query(db):
	def GET(self):
		return url_menu() + table_query(self.curs)

	def POST(self):
		data = web.input()
		esl_list = data["multi_list"].splitlines()
		esl_list = [{"eslid":check_eslid(esl1)} for esl1 in esl_list]
		save_log_file("query")

		send_cmd("ESL_QUERY_REALTIME", esl_list)
		raise web.seeother('/report')

class unbind(db):
	def GET(self):
		src = get_all_bind_list(self.curs)
		return url_menu() + js("") + table_unbind(src)

	def POST(self):
		data = web.input()
		esl_list = data["multi_list"].splitlines()
		esl_list = [check_eslid(esl1) for esl1 in esl_list]
		
		for id1 in esl_list:
			cmd = "delete from bind_list where eslid='%s'" % id1
			self.curs.execute(cmd)
		self.conn.commit()
		raise web.seeother('/updata')

		#data = web.input()
		#unbind_list = [{'eslid' : eslid} for eslid in data.keys()]
		#raise web.seeother('/updata')
		#return url_home() + send_cmd("UNBIND", unbind_list)

def copy_file(f1, f2):
	f11 = open(f1, 'rb')
	f22 = open(f2, 'wb')
	f22.write(f11.read())
	f22.close()
	f11.close()

def save_log_file(price):
	file_basename = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
	new_file_name = "updata_log/" + file_basename + '-' + str(price) + '-update.txt'
	new_db_name = "updata_log/" + file_basename + '-' + str(price) + '-db.sqlite'

	try:
		os.mkdir("updata_log")
	except OSError:
		pass

	copy_file(log_file, new_file_name)
	copy_file('db.sqlite', new_db_name)

	log = open(log_file, 'w')
	log.close()

class updata(db):
	def GET(self):
		bind_list = get_all_bind_list(self.curs)
		return url_menu() + table_format(self.curs, bind_list)
	
	def POST(self):
		data = web.input()
		cmd = "update sales_list set status=''"
		self.curs.execute(cmd)
		self.conn.commit()
		save_log_file(str(data['price']))
		ret = url_home() + sales_updata(data)

		raise web.seeother('/report')
		#return ret

def txt2dict(data):
	cont = data.splitlines()
	sp1=','
	if ';' in cont[0]:
		sp1=';'
	k = cont[0].split(sp1)
	return [dict(zip(k, v.split(sp1))) for v in cont[1:]]

def txt2html(data):
	h = '<td height="84" align="left" valign="top" class="t2">'
	h = h + '<pre style="word-wrap: break-word; white-space: pre-wrap; white-space: -moz-pre-wrap">'
	h = h + data + "</pre></td>"
	return h

class web_help:
	def GET(self):
		h =  url_menu() + about_me
		h = h + "</body></html>"
		return h

class dbview(db):
	def POST(self):
		f= web.input()
		h =  url_menu()
		try:
			self.curs.execute(f['dbcmd'])
			self.conn.commit()
			for row in self.curs.fetchall():
				h = h + '<br>'
				for item in row:
					h = h + str(item) + ','
				h = h[:-1]
		except Exception, e:
			h = h + "<br>ERROR: " + str(e)
		h = h + "</body></html>"
		return h

class upload:
	def GET(self):
		h = url_menu() + """只支持csv格式的文件
					<form method="POST" enctype="multipart/form-data" action="">
					<br>价签文件<input type="file" name="esl_file"/>
					<br>商品文件<input type="file" name="sales_file"/>
					<br>绑定文件<input type="file" name="bind_file"/>
					<br>
					<input type="submit" />
					</form>"""
		
		h = h +	"""
					<form method="post" action="dbview">
					SQL语句<input type="text" name="dbcmd" size="80">
					<br>
					<input type="submit" />
					</form>
					"""
		h = h + "</body></html>"
		return h

	def POST(self):
		f = web.input()
		if f['esl_file']:
			send_cmd("ESL_ADD", txt2dict(f['esl_file']))
		if f['sales_file']:
			v = txt2dict(f['sales_file'])
			for k in v:
				k['bak'] = '00'
			send_cmd("SALES_QUERY_ACK",v)
		if f['bind_file']:
			send_cmd("BIND", txt2dict(f['bind_file']))
			
		raise web.seeother('/upload')

class log:
	def GET(self):
		with open(log_file, 'r') as f:
			return url_menu() + txt2html(f.read())

class report:
	def GET(self):
		h = url_menu()
		h = js_reload(h)
		f = open(SLAES_UPDATA_FILE, "r")
		d = f.read().splitlines()
		d.reverse()
		d = '\n'.join(d)
		h = h + txt2html(d)
		h = h + txt2html(ack_count());
		f.close()

		return h.encode("utf-8")

class index:
	def GET(self):
		h = url_menu()
		return h

def main():
	esl_init.log.info("test mode starting ......")
	f = open(SLAES_UPDATA_FILE, "w")
	f.close()

	try:
		sys.argv[1] = "8880"
	except:
		pass

	app = web.application(urls, globals())
	app.run()

if __name__ == '__main__':
	main()

