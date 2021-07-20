#encoding: utf-8
import sqlite3



all_op5_update_data = "{'max_package': 512, 'flash_size': 16, 'resolution_y': 128, 'version': 1, 'resolution_x': 296, 'temperature': '0-10', 'wid': '5A-04-8C-66', 'screen_type': 'HS_EL_5103', 'resolution_direction': 0, 'chn': 150}"

multi_id = [('flash_size',16),('screen_type','HS_EL_5103')]	


one_id = [("max_package",512),('screen_type','HS_EL_5103')]
eslid = '57-11-02-99' #更新一个价签的id


class update_esl_list(object):

	def __init__(self):
	
		self.conn = sqlite3.connect("./db.sqlite")
		self.cursor = self.conn.cursor()
		self.str_value = ['screen_type','temperature','wid']
		self.help()
		self.input_num = raw_input("Select one chioce: ")
		self.lists =[]
		
		self.foundAllBindList_inEsl_list()
		


	def help(self):
		
		print '''
			<help> 
			[A]ll #更新所有绑定表里的价签中op5的值
			[M]ulti #更新所有绑定表里的价签op5中某一项或多项的值
			[O]ne  #更新一个价签op5中一项或多项的值
			'''
		
	def close_it(self):
			
		self.conn.commit()
		self.conn.close()
		
		print 'Bye!'

	def foundAllBindList_inEsl_list(self):
	#查询所有bind_list的价签，必须在esl_list表里，并返回这些价签ID
		cmd = 'select e.eslid  from esl_list e,bind_list b where e.eslid=b.eslid'
		self.cursor.execute(cmd)
		row =self.cursor.fetchall()	
		
		self.lists = [x[0] for x in row]
		
		print "all bind_list's eslid in esl_list:"
		print self.lists
		print '*' * 80
	

	def update_all(self):
	
		for slaveID in self.lists:
			#	ids = start_id + n
			#slaveID = "%s-%02X-%02X-99" % (first_id, ids/256, ids%256)
			cmd = 'update esl_list set op5="%s" where eslid="%s"' %(all_op5_update_data,slaveID)
			self.cursor.execute(cmd)

	
	def update_it(self,key,value,eslid):
			cmd = "select op5 from esl_list where eslid='%s'" %eslid
			self.cursor.execute(cmd)
			row = self.cursor.fetchall()[0][0]
			row = eval(row,{},{})
			
			print "\n [*] original op5 is %s" % row
			if row:
				if key not in self.str_value:
					row[key] = int(value)
				else:
					row[key] = value
				
			cmd = 'update esl_list SET op5="%s" where eslid="%s" ' % (row ,eslid)
			print "\n [*] after update op5 is : %s\n" % row 
			
			self.cursor.execute(cmd)


	
	def update_all_op5_one_field(self):
		for x ,y in multi_id:
			for eslid in self.lists:
				self.update_it(x,y,eslid)
		
	def update_op5_only_one_field(self,eslid,key,value):

		cmd = "select 1 from esl_list where eslid='%s'" % eslid
		self.cursor.execute(cmd)

		all_eslid = self.cursor.fetchall()

		
		if  all_eslid:
			
			print "\n [*] select eslid : %s" % eslid
			cmd = "select op5 from esl_list where eslid='%s'" %eslid
			self.cursor.execute(cmd)
			row = self.cursor.fetchall()[0][0]
			row = eval(row,{},{})
			
			print "\n [*] original op5 is %s" % row
			if row:
				if key not in self.str_value:
					row[key] = int(value)
				else:
					row[key] = value
				


			cmd = 'update esl_list SET op5="%s" where eslid="%s" ' % (row ,eslid)
			print "\n [*] after update op5 is : %s\n" % row 
			
			self.cursor.execute(cmd)
		else:
			print "\neslid not in database_list"

	def update_one(self,eslid,one_id):
		for key,value in one_id:
			self.update_op5_only_one_field(eslid,key,value)
	
if __name__ == "__main__":		
	
	uel = update_esl_list()
	if uel.input_num.upper() == 'A':
		uel.update_all()
	elif uel.input_num.upper() == 'M':
		uel.update_all_op5_one_field()
	elif uel.input_num.upper() == 'O':
		uel.lists = []
		uel.lists.append(eslid)
		print `uel.lists`
		uel.update_all()
		uel.update_one(eslid,one_id)
	else:
		pass
	
	uel.close_it()
	
