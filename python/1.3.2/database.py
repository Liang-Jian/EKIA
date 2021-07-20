# encoding: utf-8

#
# 数据库模块
#

import os, sqlite3, csv, time, codecs, json
from esl_init import conf, trace
import esl_init

class DB:
	'''
	数据库对象
	'''
	def __init__(self, timeouts = 120, db_file = None):
		#[db_file]
		if db_file:
			conf.db_file.db_file = db_file

		self.db_file = conf.db_file.db_file

		self.timeouts = timeouts
		#[table]
		self.esl 	= 'esl_list';
		self.sales 	= 'sales_list';
		self.bind 	= 'bind_list';
		self.ap		= 'ap_list'
		self.excep  = 'exception_list'

		self.table_keys = {self.esl : "eslid", self.sales : "salesno", self.ap : "apid", \
							self.bind : "eslid", self.excep : "id"}
		self.table_column = {
					#wakeupid,slaveid,masterid,channel,epd_type,battery,
					#netid, op3, op4, op5, op6,reserve, retry_max, direct
					self.esl: [('nw1','50-00-00-00'),('eslid', ''), ('nw2', '52-56-78-53'),('setchn', '0'),
									('grpchn', '0'),('nw3', '0'),('nw4', 'NORMAL'),('op1', '30'),
								('op2', '0'),('op3', 'HS_EL_5300'), ('op4', ''), ('op5', '{}'),
								('op6', '{}'),('op7', '0'), ('op8', '6'), ('op9', '0'),
								('lastworktime', ''), ('status', ''), ('refresh_times', '0'), ('netlink_times', '0'),
								('wake_times', '0'), ('transmission_times', '0'), ('sleep_times', '0'),
								('failed_times', '0'), ('work_mode', ''), ('exteslid', ''),
								('op10', ''), ('op11', ''), ('op12', ''), ('op13', ''), ('op14',''), ('op15',''),
								('op16',''), ('op17',''), ('op18',''), ('op19',''), ('op20',''), ('op21',''),
								],
					self.sales : [(col, '')  for col in conf.db_file.sales_list_title],
					self.ap: [('apid', ''),('apip', ''),('netmask', ''), ('gateway', ''),('listenport', ''),('lastworktime', ''),
								('onlinebegintime', ''), ('status', ''), ('work_mode', ''), ('version', ''), ('sn', ''), ('desc', ''),
								('mac', '')],
					self.bind: [('eslid', ''),('salesno', ''),('apid', ''), ('status', '')],
					self.excep:[('datetime', ''), ('id', ''), ('errid', ''), ('salesno', ''), ('eslid', ''), ('errormsg', '')]
					}

		#sales_list 必选字段
		sales_list = self.get_column_list(self.sales)
		for k in ['salesno', 'sid', 'lastworktime', 'status']:
			if k not in sales_list:
				self.table_column[self.sales].append((k, ''))

		self.conn_db(self.db_file,timeouts)

	def check_db(self):

		if not os.path.isfile(self.db_file):
			#创建数据库文件
			conn = sqlite3.connect(self.db_file)
			conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
			curs = conn.cursor()

			for table in self.table_column:
				self.create_table(table, curs)
			conn.commit()
			conn.close()
					
		self.conn_db(self.db_file, self.timeouts)

		#检查表是否存在
		table_new_flag = False
		for table in self.table_column:
			cmd = "SELECT count(*) FROM sqlite_master WHERE type='table' and name='%s'" % table
			self.cursor.execute(cmd)
			for item in  self.cursor.fetchall():
				n = item[0]
			if n == 0:
				self.create_table(table, self.cursor)
				table_new_flag = True
			self.conn.commit()

		if table_new_flag:
			self.conn.close()
			self.conn_db(self.db_file, self.timeouts)

		#检查列是否存在
		column_new_flag = False
		for tb in self.table_column:
			cmd = 'select * from %s limit 1' % tb
			self.cursor.execute(cmd)
			tb_exist = [i[0] for i in self.cursor.description]
			for (col, default) in self.table_column[tb]:
				if col not in tb_exist: #列不存在
					cmd = 'alter table %s add column %s ' % (tb, self.get_column_cmd(tb, col, default))
					self.cursor.execute(cmd)
					self.conn.commit()
					column_new_flag = True
		
		if column_new_flag:
			self.conn.close()
			self.conn_db(self.db_file, self.timeouts)

		#检查价签表字段值
		for tb in self.table_column:
			for (col, default) in self.table_column[tb]:
				if tb == self.esl and col in ['setchn', 'grpchn']:
					val = (tb, col, col)
					cmd = "update %s set %s = nw3 where %s is null" % val
				else:
					val = (tb, col, default, col)
					cmd = "update %s set %s = '%s' where %s is null" % val
				try:
					self.cursor.execute(cmd)
				except Exception, e:
					esl_init.log.info("cmd: %s, %s" % (cmd, e))

		self.conn.commit()
		self.conn.close()
		self.conn_db(self.db_file, self.timeouts)

	def get_column_cmd(self, table, column, default):
		if column == 'datatime':
			cmd = column + " timestamp not null default (datetime('now','localtime'))"
		elif column == 'id':
			cmd = column + " INTEGER PRIMARY KEY AUTOINCREMENT"
		else:
			cmd = column + " TEXT DEFAULT '%s' " % default

		if column == self.table_keys[table] and column != 'id':
			cmd += " PRIMARY KEY"
		return cmd
		
	def create_table(self, table, curs):
		cmd = "CREATE TABLE " + table + "( "
		for (column, default) in self.table_column[table]:
			cmd += self.get_column_cmd(table, column, default)
			cmd += ','
		cmd = cmd[0:-1] + ')'
		curs.execute(cmd)

	def conn_db(self,db_file,timeouts):
		self.conn = sqlite3.connect(db_file,timeout = timeouts, 
				cached_statements = 10000, isolation_level=None)
		self.conn.text_factory = lambda x: unicode(x,'utf-8','ignore')
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()
		self.conn.execute('PRAGMA journal_mode = OFF')
		self.conn.execute('PRAGMA synchronous = OFF')
		self.conn.execute('PRAGMA cache_size = 20000')
	
	def commit(self):
		pass
		#self.conn.commit()
	
	def get_column_list(self, table_name):
		return [item[0]  for item in self.table_column[table_name]]
	
	def change_key_val_without_commit(self, table_name, key, col, val):
		cmd = "update %s set %s = '%s' where %s = '%s'" %\
			(table_name, col, str(val), self.table_keys[table_name], key)
		self.cursor.execute(cmd)
	
	def change_key_val_with_commit(self, table_name, key, col, val):
		try:
			self.change_key_val_without_commit(table_name, key, col, val)
		finally:
			self.commit()
	
	def count_by_key_str(self, table_name, col):
		cmd = "select %s, count(*) from %s group by %s" % (col, table_name, col)
		self.cursor.execute(cmd)
		v = {}
		for row in self.cursor.fetchall():
			if row[0] == None:
				k = "NONE"
			else:
				k = row[0]
			v[k] = str(row[1])
		return v

	def increace_status(self, eslid, key_list):
		'''由外面提交'''
		for k in key_list:
			cmd = "select %s from esl_list where eslid= '%s'" % (k, eslid)
			self.cursor.execute(cmd)
			for row in self.cursor.fetchall():
				v = row[0]
				break
			try:
				v = int(v)
			except Exception, e:
				v = 0
			v += 1
			v = str(v)
			cmd = "update esl_list set %s = '%s' where eslid='%s'" % (k, v, eslid)
			self.cursor.execute(cmd)

	def get_all_info(self, table_name, key):
		ret = {}
		if not self.has_key(table_name, key):
			return ret
		row = self.get_one(table_name, key)
		for field in self.get_column_list(table_name):
			try:
				ret[field] = row[field]
			except Exception, e:
				esl_init.log.error_msg("field %s not exist of %s" % (field, key), errid='EDA001')
		return ret

	def get_one(self, table_name, key):
		'''
		从指定的数据库中获取指定健的列值
		返回第一条记录
		'''
		cmd = "select * from %s where %s = ?" % (table_name, self.table_keys[table_name])
		if table_name != self.sales:
			key = str(key).upper()
		self.cursor.execute(cmd, (key,))
		for row in self.cursor.fetchall():
			return row

	def get_salesno_from_eslid(self, ids):
		return self.get_one(self.bind, str(ids).upper())['salesno']
	
	def get_sales_bind_esl_number(self, salesno):
		return len(self.get_sales_bind_esl_list(salesno))
	
	def get_sales_bind_esl_list(self, salesno):
		cmd = "select eslid from %s where salesno = ?" % self.bind
		self.cursor.execute(cmd, (salesno,))
		return [item['eslid'] for item in self.cursor.fetchall()]
	
	def get_ap_bind_esl_list(self, apid):
		cmd = "select eslid from %s where apid = ?" % self.bind
		self.cursor.execute(cmd, (apid,))
		return [item['eslid'] for item in self.cursor.fetchall()]
	
	def get_ap_group_v3(self, apid):
		cmd  = "select apid, nw1, setchn, grpchn, nw3, op3, count(*) as c "
		cmd += "from bind_list b, esl_list e where e.eslid=b.eslid "
		if apid :
			cmd += " and apid = %s " % apid
		cmd += "group by apid, nw1, setchn, grpchn, nw3, op3 order by c desc"
		self.cursor.execute(cmd)

		return [{"apid":i[0], "nw1":i[1], "setchn":i[2], "grpchn":i[3],
					"nw3":i[4], "op3":i[5], "count":i[6]} for i in self.cursor.fetchall()]

	def get_ap_bind_group(self):
		cmd = "select apid, nw1, nw3, op3, count(*) as count from bind_list b, esl_list e "
		cmd += "where e.eslid=b.eslid group by apid, nw1, nw3, op3 order by count desc"
		self.cursor.execute(cmd)
		return [(item[0], item[1], item[2], item[3], item[4]) for item in self.cursor.fetchall()]
	
	def bind_sort_nw1_nw3_op3(self, i, include_ap_list = [], count_max = 99999):
		cmd =  "select apid, count(*) as counts from bind_list b, esl_list e "
		cmd += "where e.eslid=b.eslid and e.setchn=? and e.grpchn=? and e.nw3=? "
		cmd += "and e.nw1=? and e.nw4=? and e.op3=? "
		cmd += "group by apid order by counts desc"
		self.cursor.execute(cmd, (i['setchn'], i['grpchn'], i['nw3'] ,i['nw1'], i['nw4'], i['op3']))
		return [(item[0], item[1]/count_max*count_max) \
					for item in self.cursor.fetchall() if item[1] <= count_max \
					and item[0] in include_ap_list]
	
	def bind_sort_set(self, i, include_ap_list = [], count_max = 99999):
		cmd =  "select apid, count(*) as counts from bind_list b, esl_list e "
		cmd += "where e.eslid=b.eslid and e.setchn=? and e.nw1 != ? "
		cmd += "and e.nw1 like ? and e.nw4=? and e.op3=? "
		cmd += "group by apid order by counts desc"

		setid = [item for item in str(i['nw1'])]

		setid[6] = '%'
		setid[7] = '%'
		setid = ''.join(setid)

		self.cursor.execute(cmd, (i['setchn'], i['nw1'], setid, i['nw4'], i['op3']))
		return [(item[0], item[1]) for item in self.cursor.fetchall() if item[1] <= count_max \
				and item[0] in include_ap_list]

	def bind_sort_count(self, include_ap_list = [], exclude_ap_list = [], count_max = 99999):
		cmd = "select apid, count(*) as count from bind_list group by apid order by count desc"
		self.cursor.execute(cmd)
		ap_count = [(item[0], item[1]/count_max*count_max) for item in self.cursor.fetchall() \
			if item[0] not in exclude_ap_list and item[0] in include_ap_list]
		
		#加上计数为0的分组
		first_choose_list = [item[0] for item in ap_count]
		for ap in include_ap_list:
			if ap not in first_choose_list and ap not in exclude_ap_list:
				ap_count.append((ap, 0))

		return ap_count

	def get_wakeup_channel_esl_list(self, wakeupid, channel):
		cmd = "select eslid from %s where nw1 = '%s' and nw3 = '%s' " % (self.esl, wakeupid, channel)
		self.cursor.execute(cmd)
		return [item['eslid'] for item in self.cursor.fetchall()]

	def get_wakeup_channel_netid_same(self, wakeupid, channel, ids):
		cmd = "select eslid, op2 from %s where nw1 = '%s' and nw3 = '%s' " % (self.esl, wakeupid, channel)
		self.cursor.execute(cmd)
		op2_dict, use_op2, esl_list = {}, {}, []
		for item in self.cursor.fetchall():
			try:
				op2 = int(item['op2']) % 160
				eslid = item['eslid']
				op2_dict.setdefault(op2, []).append(item['eslid'])
				if eslid in ids:
					use_op2[op2] = 1
			except Exception, e:
				pass
		
		for op2 in use_op2:
			esl_list.extend(op2_dict[op2])

		return list(set(esl_list) - set(ids))
	
	def get_all_ap(self):
		cmd = "select apid from %s" % self.ap
		ap_list = []
		self.cursor.execute(cmd)
		for ap in self.cursor.fetchall():
			ap_list.append(ap['apid'])
		return ap_list
	
	def set_esl_count(self, setid):
		nw1 = '%%'+'-'+setid+'-'+'%%'+'-'+'66'
		cmd = "select count(*) from esl_list e, bind_list b where b.eslid = e.eslid and e.nw1 like '%s'" % nw1
		self.cursor.execute(cmd)
		return [item[0] for item in self.cursor.fetchall()][0]
	
	def refresh_ap_online_status(self, timeout):
		cmd = "select * from %s where status = 'online'" % self.ap
		offline_ap_list = []
		self.cursor.execute(cmd)
		try:
			for ap in self.cursor.fetchall():
				lastworktime = ap['lastworktime']
				try: #格式不正确
					time.strptime(lastworktime, "%a %b %d %H:%M:%S %Y")
				except Exception:
					lastworktime = time.asctime()

				elapse_time = time.time() - time.mktime(time.strptime(lastworktime, "%a %b %d %H:%M:%S %Y"))
				if elapse_time > timeout:
					self.set_last_status_without_commit(self.ap, ap['apid'], time.asctime(), "offline")
					offline_ap_list.append({'apid':ap['apid'], 'status':'offline'})
		finally:
			self.commit()
		return offline_ap_list

	def is_esl_busy(self, esl1,wait={}):
		if not self.has_key(self.bind, esl1):
			return False
		if self.get_one(self.bind, esl1)['status'] == "unbinding":
			return True
		if esl1 in wait:
			return True
		salesno = self.get_salesno_from_eslid(esl1)
		sales_info = self.get_one(self.sales, salesno)
		if sales_info and sales_info['status'] == "updating":
			return True
		return False

	def get_online_ap(self):
		cmd = "select apid, lastworktime from %s where status = 'online'" % self.ap
		ap_list = []
		self.cursor.execute(cmd)
		for ap in self.cursor.fetchall():
			ap_list.append(ap['apid'])
		return ap_list

	def get_last_status(self, table_name, key):
		if table_name != self.sales:
			key = str(key).upper()
		item = self.get_one(table_name, key)

		try:
			lastworktime, status = item['lastworktime'], item['status']
		except Exception, e:
			lastworktime, status = None, None

		return lastworktime, status
	
	def get_netid(self,ids):
		cmd = "select op2 from esl_list where eslid in (%s)" % ids
		self.cursor.execute(cmd)
		return [item[0] for item in self.cursor.fetchall()]

	def get_nw1_nw3_ap_group(self):
		cmd = "select nw1, nw3, apid, count(e.eslid) from esl_list e, bind_list b"\
				" where b.eslid=e.eslid group by nw1, nw3, apid"
		self.cursor.execute(cmd)
		g = {}
		for i in self.cursor.fetchall():
			wkid, chn, apid, count = i
			if not wkid or not chn:
				continue
			g.setdefault(wkid, {}).setdefault(chn, {})[apid] = count
		return g

	def get_nw1_nw3_group(self):
		cmd = 'select distinct nw1, nw3 from esl_list'
		self.cursor.execute(cmd)
		f = {}
		for x,y in self.cursor.fetchall():
			d = {}
			cmd = 'select op2 from esl_list where nw1="%s" and nw3="%s"'%(x,y)
			self.cursor.execute(cmd)
			try:
				for z in self.cursor.fetchall() :
					d[int(z[0])] = 0
			except Exception,e:
				esl_init.log.error_msg('ValueError: %s, %s'% (e,z[0]), errid='EDA002')
			f[x+y] = d
		return f

	def get_updating_esl(self):
		cmd = "select b.eslid from esl_list e, bind_list b where b.eslid=e.eslid and e.status='updating'"
		self.cursor.execute(cmd)
		return [item['eslid'] for item in self.cursor.fetchall()]

	def get_updating_sales(self):
		cmd = "select b.salesno from sales_list s, bind_list b where b.salesno=s.salesno and s.status='updating'"
		self.cursor.execute(cmd)
		return [item['salesno'] for item in self.cursor.fetchall()]

	def get_unbinding_esl(self):
		cmd = "select eslid from bind_list where status='unbinding'"
		self.cursor.execute(cmd)
		return [item['eslid'] for item in self.cursor.fetchall()]

	def get_lowpower_esl(self):
		cmd = "select b.eslid from esl_list e, bind_list b where b.eslid=e.eslid and e.status='lowpower'"
		self.cursor.execute(cmd)
		return [item['eslid'] for item in self.cursor.fetchall()]

	def change_esl_to_ap_without_commit(self, id1, ap):
		cmd = "update %s set 'apid' = '%s' where %s = '%s'" % \
			(self.bind, ap, self.table_keys[self.bind], str(id1).upper())
		self.cursor.execute(cmd)

	def change_last_status_without_commit(self, table_name, col_name, col_value, status):
		'''更新表中某个字段的状态或内容：col_value->status'''
		cmd = 'update %s set "%s" = "%s" where "%s" = "%s"' % (table_name, col_name, status, col_name, col_value) 
		self.cursor.execute(cmd)

	def change_esl_rfpara_without_commit(self, id1, wakeupid, channel, netid, setchn, grpchn):
		'''更新价签无线通信字段内容：wakeupid,channel'''
		cmd = 'update esl_list set nw1="%s", nw3="%s", op2="%s", setchn="%s", grpchn="%s" where eslid="%s"' % (wakeupid, channel, netid, setchn, grpchn, id1)
		self.cursor.execute(cmd)

	def change_bind_ap_without_commit(self, id1, apid):
		'''更新价签bind_list ap字段内容'''
		cmd = 'update bind_list set apid="%s" where eslid="%s"' % (apid, id1)
		self.cursor.execute(cmd)	   

	def change_esl_op2_without_commit(self, id1, op2):
		'''更新价签op2字段内容'''
		cmd = 'update esl_list set op2="%s" where eslid="%s"' % (op2, id1)
		self.cursor.execute(cmd)

	def change_esl_op5_without_commit(self, id1, op5):
		'''更新价签op5字段内容'''
		op5 = json.dumps(op5)
		cmd = 'update esl_list set op5=? where eslid=?'
		self.cursor.execute(cmd, (op5, id1))

	def change_esl_op6_with_commit(self, id1, op6):
		'''更新价签op6字段内容'''
		try:
			op6 = json.dumps(op6)
			cmd = 'update esl_list set op6=? where eslid=?'
			self.cursor.execute(cmd, (op6, id1))
		finally:
			self.commit()

	def change_esl_op6_without_commit(self, id1, op6):
		'''更新价签op6字段内容'''
		op6 = json.dumps(op6)
		cmd = 'update esl_list set op6=? where eslid=?'
		self.cursor.execute(cmd, (op6, id1))

	def change_esl_op5_with_commit(self, id1, op5):
		'''更新价签op5字段内容'''
		try:
			op5 = json.dumps(op5)
			cmd = 'update esl_list set op5=? where eslid=?'
			self.cursor.execute(cmd, (op5, id1))
		finally:
			self.commit()

	def change_esl_op4_without_commit(self, id1, op4):
		'''更新价签op4字段内容'''
		cmd = 'update esl_list set op4="%s" where eslid="%s"' % (op4, id1)
		self.cursor.execute(cmd)

	def set_last_status_without_commit(self, table_name, key, work_time, status):
		'''更新表中某个主键key的更新时间和工作状态, work_time为空时不更新时间'''
		if table_name != self.sales:
			key = str(key).upper()
		if work_time:
			cmd = 'update %s set "lastworktime" = "%s", "status" = "%s" where "%s" = ?' \
				% (table_name, work_time, status, self.table_keys[table_name]) 
		else:
			cmd = 'update %s set "status" = "%s" where "%s" = ?' \
				% (table_name, status, self.table_keys[table_name])
		self.cursor.execute(cmd, (key,))

	def set_except_without_commit(self, errid, salesno, eslid, errmsg):
		cmd = "insert into %s (errid, salesno, eslid, errormsg) values ('%s', ?, '%s', ?)" % (\
				self.excep, errid, eslid)
		self.cursor.execute(cmd, (salesno, errmsg,))

	def has_key(self, table_name, key):
		'''检查在table_name中是否存在主键为key的条目，返回True或False'''
		cmd = "select * from %s where %s = ?" % (table_name, self.table_keys[table_name])
		if table_name != self.sales:
			key = str(key).upper()
		self.cursor.execute(cmd, (key,))
		return True if len(self.cursor.fetchall()) > 0 else False

	def remove_key(self, table_name, key):
		'''删除在table_name中主键为key的条目'''
		try:
			self.commit()
			cmd = "delete from %s where %s = ?" % (table_name, self.table_keys[table_name])
			if table_name != self.sales:
				key = str(key).upper()
			self.cursor.execute(cmd, (key,))
		finally:
			self.commit()
	
	def get_cmd_new(self, table_name, row):
		'''
		通过传入的字典列表生成对应的sql语句
		row的格式为 {"apid":0, "salveid":"12-34-56-78", "salesno":1000}
		若apid为0的条目在bind表中存在，将将返回sql命令 
			update table_name set apid = ?, salveid = ?, salesno = ? where apid = ?
		若不存在，则将返回一条插入语句
			insert into table_name (apid, salveid, salesno) values (?, ?, ?)
		并返回一个参数元组args，供excute命令调用
		'''
		key1 = self.table_keys[table_name]
		if table_name != self.sales:
			key = str(row[key1]).upper()
		else:
			key = row[key1]
		cmd = "select %s from %s where %s = ?" % (key1, table_name, key1)
		self.cursor.execute(cmd, (key,))
		is_updata = len(self.cursor.fetchall())
		args = []

		if is_updata:
			cmd = "update " + table_name  +" set "
			for key in row.keys():
				if key in self.get_column_list(table_name):
					cmd += '%s = ?,' % (key)
					try:
						args.append(str(row[key]))
					except Exception, e:
						args.append(row[key])
			cmd = cmd[0:-1]
			cmd += ' where %s = ?' % (key1)
			if table_name != self.sales:
				args.append(str(row[key1]).upper())
			else:
				args.append(row[key1])
		else:
			cmd = "insert into " + table_name + ' ('
			for key in row.keys():
				if key in self.get_column_list(table_name):
					cmd +=  '%s,' %  key
			cmd = cmd[0:-1]
			cmd += ') values ('
			for key in row.keys():
				if key in self.get_column_list(table_name):
					cmd +=  '?,'
					try:
						args.append(str(row[key]))
					except Exception, e:
						args.append(row[key])
			cmd = cmd[0:-1]
			cmd += ')'

		return cmd, self.table_keys[table_name], args

	def upper_key(self, row):
		'''
		将row中的索引键值大写，避免传入的数据中有小写的键值存在。
		'''
		for title in ["nw1", "eslid", "nw2", "apid"]:
			if row.has_key(title):
				try:
					row[title] = str(row[title]).upper()
				except Exception, e:
					return False
		return True

	def list_updata(self, table_name, source):
		'''批量更新数据库，数据源是字典列表'''
		try:
			for row in source:
				if 'bak' in row and row['bak'] != '00':
					continue
				if self.upper_key(row): #导入数据时KEY转成大写
					new_cmd, table_key, args = self.get_cmd_new(table_name, row)
					self.cursor.execute(new_cmd, args)
					ack = "00"
				else:
					table_key = self.table_keys[table_name]
					ack = "01"
				row['bak'], row['ack'] = ack, ack
		finally:
			self.commit()
		return source
	
	def get_reader(self, fn):
		for code in ['utf-8-sig', 'utf-8', 'gb2312', 'ascii']:
			try:
				f = codecs.open(fn, 'r', encoding=code) 
				cont = f.read().splitlines()
				f.close()
				break
			except Exception, e:
				pass
		sep = ','
		if ';' in cont[0]:
			sep = ';'
		k = cont[0].split(sep)
		return [dict(zip(k, v.split(sep))) for v in cont[1:]] 

	def updata_from_file(self, table_name, updata_file):
		'''批量更新数据库，数据源是文件对象'''
		return self.list_updata(table_name, self.get_reader(updata_file))

	def key_list(self,table_name):
		'''返回数据库中table_name的所有索引建值'''
		cmd = """ select %s from %s """ % (self.table_keys[table_name], table_name)
		self.cursor.execute(cmd)
		return [items[0] for items in self.cursor.fetchall()]

	def list_del(self, table, reader):
		'''批量删除'''
		key_title = self.table_keys[table]
		try:
			for row in reader:
				if 'bak' in row and row['bak'] != '00':
					continue
				if not self.has_key(table, row[key_title]):
					row['bak'] = "01" #key不存在
					esl_init.log.warning("del key(%s) for table(%s) failed" % (row[key_title], table))
					continue

				if table == self.esl: #价签状态是否busy由其所绑的商品决定
					if self.is_esl_busy(row[key_title]):
						row['bak'] = "04" #key busy
						continue

				_, status = self.get_last_status(table, row[key_title])
				if status == 'updating':
					row['bak'] = "04" #key busy
					continue
				cmd = "delete from %s where %s = ?" % (table, self.table_keys[table])
				if table != self.sales:
					self.cursor.execute(cmd, (str(row[key_title]).upper(),))
				else:
					self.cursor.execute(cmd, (row[key_title],))
				row['bak'] = '00'
		finally:
			self.commit()
	
	def get_set_eslid_one(self, setid, esl_power_his):
		#循环每个基站：
		#能量表里有收到过，则临时绑定，挑一个加入清单
		from htp import get_setid

		setid = setid.upper()
		cmd  = 'select e.eslid, setchn, apid from esl_list e, bind_list b  where b.eslid=e.eslid and '
		cmd += 'nw1 like "%s-%s-%%%%-%s" group by setchn, apid' % \
				(setid[0:2], setid[3:5], setid[9:])

		esl_ap_list, esllist, aplist = [], [], []
		self.cursor.execute(cmd)
		for row in self.cursor.fetchall():
			esl_ap_list.append((row[0], row[2]))
			esllist.append(row[0])
			aplist.append(row[2])
		
		for apid in self.key_list(self.ap):
			if apid in aplist:
				continue
			#这个AP没有绑定过此set的价签，但可能也覆盖了此set的价签
			#因此需要找到
			for id1 in esl_power_his:
				if id1 in esllist:
					continue
				if apid not in esl_power_his[id1]:
					continue
				e = self.get_one(self.esl, id1)
				if e and get_setid(e['nw1']) != get_setid(setid):
					continue
				esl_ap_list.append((id1, apid))
				esllist.append(id1)
				aplist.append(apid)
				break

		return esl_ap_list

def get_set_eslid_one_test(db):
	t = '发送set命令时挑选特定的价签覆盖全店'

	'''
	3个基站: 1个绑定过此set,1个收到过此set的心跳,1个没有绑定过，也没有收到过心跳
	2个价签: 1个绑定过,
	'''

def self_test():
	from database import DB
	from tempfile import mktemp
	import os

	for test_fun in []:
		db_file = mktemp()
		db = DB(db_file = db_file)
		db.check_db()

		test_fun(db)

		os.remove(db_file)

