#-*- coding:UTF-8 -*-

import os, sqlite3 ,unittest
import xmlrpclib, time, random

#from PublicFunction import ReadXml

server = xmlrpclib.ServerProxy("http://127.0.0.1:9000")

'''
这个文件放在eslwokrinig的主目录下
'''

class AP_INFO(unittest.TestCase): #504-1049
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(0.5)
	def test_case001(self):#正常获取单个基站的基站信息
		id = 'AP 504'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd504")
		ret,val = P.s(P.r("testdata2", 0, "type504"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok504"),ret)
		self.assertEqual(P.r("testdata2", 0, "act504"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret504"),val[0]['ret'])
	def test_case002(self):#正常获取多个基站的基站信息
		id = '505'
		print '\n'+id
		P.sql("INSERT INTO ap_list('apid', 'apip', 'listenport', 'status') VALUES ('2', '192.168.1.102', 5649, 'online')")

		a =  P.r("testdata2", 0, "send_cmd505")
		ret,val = P.s(P.r("testdata2", 0, "type505"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok505"),ret)
		self.assertEqual(P.r("testdata2", 0, "act505"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret505"),val[0]['ret'])
		time.sleep(5)
		P.sql("delete from ap_list where apid = '2'")
	def test_case003(self):#指定查询的基站不存在于数据库的基站表中
		id = '506'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd506")
		ret,val = P.s(P.r("testdata2", 0, "type506"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok506"),ret)
		self.assertEqual(P.r("testdata2", 0, "act506"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret506"),val[0]['ret'])
	def test_case004(self):#指定查询的基站中有且只有一个基站存在于数据库的基站表中
		id = '507'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd507")
		ret,val = P.s(P.r("testdata2", 0, "type507"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok507"),ret)
		self.assertEqual(P.r("testdata2", 0, "act507"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret507"),val[0]['ret'])
	def test_case005(self):#输入apid为空
		id = '508'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd508")
		ret,val = P.s(P.r("testdata2", 0, "type508"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok508"),ret)
		self.assertEqual(P.r("testdata2", 0, "act508"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret508"),val[0]['ret'])
	def test_case006(self):#输入apid含字符（汉字or字母）
		id = '509'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd509")
		ret,val = P.s(P.r("testdata2", 0, "type509"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok509"),ret)
		self.assertEqual(P.r("testdata2", 0, "act509"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret509"),val[0]['ret'])
	def test_case007(self):#输入apid中含空格
		id = '510'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd510")
		ret,val = P.s(P.r("testdata2", 0, "type510"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok510"),ret)
		self.assertEqual(P.r("testdata2", 0, "act510"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret510"),val[0]['ret'])
	def test_case008(self):#输入apid中含Tab
		id = '511'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd511")
		ret,val = P.s(P.r("testdata2", 0, "type511"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok511"),ret)
		self.assertEqual(P.r("testdata2", 0, "act511"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret511"),val[0]['ret'])
	def test_case009(self):#输入apid中含特殊字符（~！@#￥%……&*（）<>?）
		id = '512'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd512")
		ret,val = P.s(P.r("testdata2", 0, "type512"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok512"),ret)
		self.assertEqual(P.r("testdata2", 0, "act512"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret512"),val[0]['ret'])
	def test_case010(self):#输入apid为小数
		id = '513'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd513")
		ret,val = P.s(P.r("testdata2", 0, "type513"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok513"),ret)
		self.assertEqual(P.r("testdata2", 0, "act513"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret513"),val[0]['ret'])
	def test_case011(self):#输入apid为负数
		id = '514'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd514")
		ret,val = P.s(P.r("testdata2", 0, "type514"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok514"),ret)
		self.assertEqual(P.r("testdata2", 0, "act514"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret514"),val[0]['ret'])
	def test_case012(self):#输入一个apid的长度为254位
		id = '515'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd515")
		ret,val = P.s(P.r("testdata2", 0, "type515"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok515"),ret)
		self.assertEqual(P.r("testdata2", 0, "act515"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret515"),val[0]['ret'])
	def test_case013(self):#输入一个apid的长度为255位
		id = '516'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd516")
		ret,val = P.s(P.r("testdata2", 0, "type516"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok516"),ret)
		self.assertEqual(P.r("testdata2", 0, "act516"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret516"),val[0]['ret'])
	def test_case014(self):#输入一个apid的长度为256位
		id = '517'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd517")
		ret,val = P.s(P.r("testdata2", 0, "type517"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok517"),ret)
		self.assertEqual(P.r("testdata2", 0, "act517"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret517"),val[0]['ret'])
	def test_case015(self):#命令中"apid"字段不写
		id = '518'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd518")
		ret,val = P.s(P.r("testdata2", 0, "type518"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok518"),ret)
		self.assertEqual(P.r("testdata2", 0, "act518"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret518"),val[0]['ret'])
	def test_case016(self):#命令中"apid"字段书写错误
		id = '519'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd519")
		ret,val = P.s(P.r("testdata2", 0, "type519"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok519"),ret)
		self.assertEqual(P.r("testdata2", 0, "act519"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret519"),val[0]['ret'])

class AP_LIST(unittest.TestCase):
	def setUp(self):
		time.sleep(1)

	def tearDown(self):
		P.sql("delete from bind_list")
		# P.sql("delete from bind_list')")


	def test_case001(self):#单个基站AP_LIST查询
		id = '520'
		print '\n'+id
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 1, 1, NULL)")
		time.sleep(2)
		a =  P.r("testdata2", 0, "send_cmd520")
		ret,val = P.s(P.r("testdata2", 0, "type520"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok520"),ret)
		self.assertEqual(P.r("testdata2", 0, "act520"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret520"),val[0]['ret'])

	def test_case002(self):#多个基站AP_LIST查询
		id = '521'
		print '\n'+id
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 1, 1, NULL)")
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-76-D9-99', 1, 2, NULL)")
		P.sql("INSERT INTO ap_list('apid', 'apip', 'listenport', 'status') VALUES (2, '192.168.1.103', 5649,'online')")
		time.sleep(5)
		a =  P.r("testdata2", 0, "send_cmd521")
		ret,val = P.s(P.r("testdata2", 0, "type521"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok521"),ret)
		self.assertEqual(P.r("testdata2", 0, "act521"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret521"),val[0]['ret'])
		time.sleep(5)
		P.sql("delete from ap_list where apid=2")
	def test_case003(self):#单个基站AP_LIST异常查询
		id = '522'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd522")
		ret,val = P.s(P.r("testdata2", 0, "type522"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok522"),ret)
		self.assertEqual(P.r("testdata2", 0, "act522"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret522"),val[0]['ret'])

	def test_case004(self):#存在所要查询基站,基站下没有绑定任何价签
		id = '523'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd523")
		ret,val = P.s(P.r("testdata2", 0, "type523"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok523"),ret)
		self.assertEqual(P.r("testdata2", 0, "act523"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret523"),val[0]['ret'])

	def test_case005(self):#指定查询的多个基站中，只有一个基站（基站11）存在于数据库的基站表中
		id = '524'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd524")
		ret,val = P.s(P.r("testdata2", 0, "type524"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok524"),ret)
		self.assertEqual(P.r("testdata2", 0, "act524"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret524"),val[0]['ret'])

	def test_case006(self):#指定查询的多个基站中，只有2个基站（基站11，基站12）存在于数据库的基站表中，其余基站均不在基站表中，
		id = '525'
		print '\n'+id
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 1, 1, NULL)")
		P.sql("INSERT INTO ap_list('apid', 'apip', 'listenport', 'status') VALUES (2, '192.168.1.103', 5649,'online')")
		time.sleep(4)
		a =  P.r("testdata2", 0, "send_cmd525")
		ret,val = P.s(P.r("testdata2", 0, "type525"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok525"),ret)
		self.assertEqual(P.r("testdata2", 0, "act525"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret525"),val[0]['ret'])
		time.sleep(5)
		P.sql("delete from ap_list where apid=2")
	def test_case007(self):#输入基站号为空
		id = '526'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd526")
		ret,val = P.s(P.r("testdata2", 0, "type526"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok526"),ret)
		self.assertEqual(P.r("testdata2", 0, "act526"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret526"),val[0]['ret'])

	def test_case008(self):#输入基站号含字符（汉字or字母）
		id = '527'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd527")
		ret,val = P.s(P.r("testdata2", 0, "type527"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok527"),ret)
		self.assertEqual(P.r("testdata2", 0, "act527"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret527"),val[0]['ret'])

	def test_case009(self):#输入基站号中含空格
		id = '528'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd528")
		ret,val = P.s(P.r("testdata2", 0, "type528"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok528"),ret)
		self.assertEqual(P.r("testdata2", 0, "act528"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret528"),val[0]['ret'])

	def test_case010(self):#输入基站号中含Tab
		id = '529'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd529")
		ret,val = P.s(P.r("testdata2", 0, "type529"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok529"),ret)
		self.assertEqual(P.r("testdata2", 0, "act529"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret529"),val[0]['ret'])

	def test_case011(self):#输入基站号中含特殊字符（~！@#￥%……&*（）<>?）
		id = '530'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd530")
		ret,val = P.s(P.r("testdata2", 0, "type530"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok530"),ret)
		self.assertEqual(P.r("testdata2", 0, "act530"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret530"),val[0]['ret'])

	def test_case012(self):#输入基站号为小写
		id = '531'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd531")
		ret,val = P.s(P.r("testdata2", 0, "type531"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok531"),ret)
		self.assertEqual(P.r("testdata2", 0, "act531"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret531"),val[0]['ret'])

	def test_case013(self):#输入基站号为小数
		id = '532'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd532")
		ret,val = P.s(P.r("testdata2", 0, "type532"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok532"),ret)
		self.assertEqual(P.r("testdata2", 0, "act532"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret532"),val[0]['ret'])

	def test_case014(self):#输入基站号为负数
		id = '533'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd533")
		ret,val = P.s(P.r("testdata2", 0, "type533"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok533"),ret)
		self.assertEqual(P.r("testdata2", 0, "act533"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret533"),val[0]['ret'])

	def test_case015(self):#输入一个基站号的长度为254位
		id = '534'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd534")
		ret,val = P.s(P.r("testdata2", 0, "type534"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok534"),ret)
		self.assertEqual(P.r("testdata2", 0, "act534"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret534"),val[0]['ret'])

	def test_case016(self):#输入一个基站号的长度为255位
		id = '535'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd535")
		ret,val = P.s(P.r("testdata2", 0, "type535"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok535"),ret)
		self.assertEqual(P.r("testdata2", 0, "act535"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret535"),val[0]['ret'])

	def test_case017(self):#输入一个基站号的长度为256位
		id = '536'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd536")
		ret,val = P.s(P.r("testdata2", 0, "type536"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok536"),ret)
		self.assertEqual(P.r("testdata2", 0, "act536"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret536"),val[0]['ret'])
	def test_case018(self):#命令行中"apid"/"esl_list"/"group"字段书写错误
		id = '537'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd537")
		ret,val = P.s(P.r("testdata2", 0, "type537"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok537"),ret)
		self.assertEqual(P.r("testdata2", 0, "act537"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret537"),val[0]['ret'])
	def test_case019(self):#命令中"apid"字段不写，可选字段正常填写
		id = '538'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd538")
		ret,val = P.s(P.r("testdata2", 0, "type538"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok538"),ret)
		self.assertEqual(P.r("testdata2", 0, "act538"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret538"),val[0]['ret'])
	def test_case020(self):#命令中只填写"apid"字段，其余字段均不用填写
		id = '539'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd539")
		ret,val = P.s(P.r("testdata2", 0, "type539"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok539"),ret)
		self.assertEqual(P.r("testdata2", 0, "act539"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret539"),val[0]['ret'])
	def test_case021(self):#命令中所有字段均不填写
		id = '540'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd540")
		ret,val = P.s(P.r("testdata2", 0, "type540"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok540"),ret)
		self.assertEqual(P.r("testdata2", 0, "act540"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret540"),val[0]['ret'])
	def test_case022(self):#命令中"apid"/"esl_list"/"group"等字段书写异常
		id = '541'
		#print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd541")
		ret,val = P.s(P.r("testdata2", 0, "type541"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok541"),ret)
		self.assertEqual(P.r("testdata2", 0, "act541"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret541"),val[0]['ret'])

class AP_REPORT(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass

	def test_case001(self):#单项查询

		id = '542'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd542")
		ret,val = P.s(P.r("testdata2", 0, "type542"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok542"),ret)
		self.assertEqual(P.r("testdata2", 0, "act542"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret542"),val[0]['ret'])

	def test_case002(self):#多项组合查询

		id = '543'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd543")
		ret,val = P.s(P.r("testdata2", 0, "type543"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok543"),ret)
		self.assertEqual(P.r("testdata2", 0, "act543"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret543"),val[0]['ret'])

	def test_case003(self):#单项异常查询

		id = '544'
		print '\n'+id
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 1, 2, '')")
		time.sleep(3)
		a =  P.r("testdata2", 0, "send_cmd544")
		ret,val = P.s(P.r("testdata2", 0, "type544"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok544"),ret)
		self.assertEqual(P.r("testdata2", 0, "act544"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret544"),val[0]['ret'])
		time.sleep(4)
		P.sql("delete from bind_list")
	def test_case004(self):#单项异常查询

		id = '545'
		print '\n'+id
		# P.sql("delete from ap_list")
		time.sleep(3)
		a =  P.r("testdata2", 0, "send_cmd545")
		ret,val = P.s(P.r("testdata2", 0, "type545"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok545"),ret)
		self.assertEqual(P.r("testdata2", 0, "act545"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret545"),val[0]['ret'])
		time.sleep(10)

	def test_case005(self):#多项异常查询

		id = '546'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd546")
		ret,val = P.s(P.r("testdata2", 0, "type546"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok546"),ret)
		self.assertEqual(P.r("testdata2", 0, "act546"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret546"),val[0]['ret'])

	def test_case006(self):#所有可选字段均缺失

		id = '547'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd547")
		ret,val = P.s(P.r("testdata2", 0, "type547"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok547"),ret)
		self.assertEqual(P.r("testdata2", 0, "act547"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret547"),val[0]['ret'])

	def test_case007(self):#命令格式书写异常

		id = '548'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd548")
		ret,val = P.s(P.r("testdata2", 0, "type548"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok548"),ret)
		self.assertEqual(P.r("testdata2", 0, "act548"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret548"),val[0]['ret'])

class ESL_LIST(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(0.5)
	def test_case001(self):#数据库中存在所要查询价签的相关信息
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd615")
		ret,val = P.s(P.r("testdata2", 0, "type615"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok615"),ret)
		self.assertEqual(P.r("testdata2", 0, "act615"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret615"),val[0]['ret'])
	def test_case002(self):#数据库中存在所要查询价签的相关信息
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd616")
		ret,val = P.s(P.r("testdata2", 0, "type616"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok616"),ret)
		self.assertEqual(P.r("testdata2", 0, "act616"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret616"),val[0]['ret'])
	def test_case003(self):#数据库中不存在所要查询价签的相关信息
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd617")
		ret,val = P.s(P.r("testdata2", 0, "type617"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok617"),ret)
		self.assertEqual(P.r("testdata2", 0, "act617"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret617"),val[0]['ret'])
	def test_case004(self):#只有一个价签存在于数据库的价签表中
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd618")
		ret,val = P.s(P.r("testdata2", 0, "type618"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok618"),ret)
		self.assertEqual(P.r("testdata2", 0, "act618"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret618"),val[0]['ret'])
	def test_case005(self):#输入价签号为空

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd619")
		ret,val = P.s(P.r("testdata2", 0, "type619"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok619"),ret)
		self.assertEqual(P.r("testdata2", 0, "act619"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret619"),val[0]['ret'])
	def test_case006(self):#输入价签号含字符（汉字or字母）

		id = '620'
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd620")
		ret,val = P.s(P.r("testdata2", 0, "type620"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok620"),ret)
		self.assertEqual(P.r("testdata2", 0, "act620"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret620"),val[0]['ret'])
	def test_case007(self):#输入价签号中含空格

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd621")
		ret,val = P.s(P.r("testdata2", 0, "type621"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok621"),ret)
		self.assertEqual(P.r("testdata2", 0, "act621"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret621"),val[0]['ret'])
	def test_case008(self):#输入价签号中含Tab

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd622")
		ret,val = P.s(P.r("testdata2", 0, "type622"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok622"),ret)
		self.assertEqual(P.r("testdata2", 0, "act622"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret622"),val[0]['ret'])
	def test_case009(self):#输入价签号中含特殊字符（~！@#￥%……&*（）<>?）

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd623")
		ret,val = P.s(P.r("testdata2", 0, "type623"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok623"),ret)
		self.assertEqual(P.r("testdata2", 0, "act623"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret623"),val[0]['ret'])
	def test_case010(self):#输入的价签号中不含“ 99 ”

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd624")
		ret,val = P.s(P.r("testdata2", 0, "type624"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok624"),ret)
		self.assertEqual(P.r("testdata2", 0, "act624"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret624"),val[0]['ret'])
	def test_case011(self):#输入的价签号中不含“ - ”

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd625")
		ret,val = P.s(P.r("testdata2", 0, "type625"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok625"),ret)
		self.assertEqual(P.r("testdata2", 0, "act625"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret625"),val[0]['ret'])
	def test_case012(self):#输入的价签号不含“ - ”，不含"99"

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd626")
		ret,val = P.s(P.r("testdata2", 0, "type626"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok626"),ret)
		self.assertEqual(P.r("testdata2", 0, "act626"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret626"),val[0]['ret'])
	def test_case013(self):#输入价签号为小写

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd627")
		ret,val = P.s(P.r("testdata2", 0, "type627"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok627"),ret)
		self.assertEqual(P.r("testdata2", 0, "act627"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret627"),val[0]['ret'])
	def test_case014(self):#输入价签号为小数

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd628")
		ret,val = P.s(P.r("testdata2", 0, "type628"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok628"),ret)
		self.assertEqual(P.r("testdata2", 0, "act628"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret628"),val[0]['ret'])
	def test_case015(self):#输入价签号为负数

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd629")
		ret,val = P.s(P.r("testdata2", 0, "type629"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok629"),ret)
		self.assertEqual(P.r("testdata2", 0, "act629"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret629"),val[0]['ret'])
	def test_case016(self):#输入一个价签号的长度为254位

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd630")
		ret,val = P.s(P.r("testdata2", 0, "type630"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok630"),ret)
		self.assertEqual(P.r("testdata2", 0, "act630"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret630"),val[0]['ret'])
	def test_case017(self):#输入一个价签号的长度为255位

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd631")
		ret,val = P.s(P.r("testdata2", 0, "type631"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok631"),ret)
		self.assertEqual(P.r("testdata2", 0, "act631"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret631"),val[0]['ret'])
	def test_case018(self):#输入一个价签号的长度为256位

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd632")
		ret,val = P.s(P.r("testdata2", 0, "type632"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok632"),ret)
		self.assertEqual(P.r("testdata2", 0, "act632"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret632"),val[0]['ret'])
	def test_case019(self):#命令中不写"eslid"字段

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd633")
		ret,val = P.s(P.r("testdata2", 0, "type633"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok633"),ret)
		self.assertEqual(P.r("testdata2", 0, "act633"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret633"),val[0]['ret'])
	def test_case020(self):#命令行中"eslid"字段书写错误

		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd634")
		ret,val = P.s(P.r("testdata2", 0, "type634"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok634"),ret)
		self.assertEqual(P.r("testdata2", 0, "act634"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret634"),val[0]['ret'])

class AP_QUERY(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(1)
	def test_case001(self):#数据库的基站表中存在所查询基站的相关信息
		a =  P.r("testdata2", 0, "send_cmd549")
		ret,val = P.s(P.r("testdata2", 0, "type549"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok549"),ret)
		self.assertEqual(P.r("testdata2", 0, "act549"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret549"),val[0]['ret'])
	def test_case002(self):#数据库的基站表中存在所查询基站的相关信息
		P.sql("INSERT INTO ap_list('apid', 'apip', 'listenport', 'status') VALUES (2, '192.168.1.103', 5649,'online')")
		time.sleep(3)
		a =  P.r("testdata2", 0, "send_cmd550")
		ret,val = P.s(P.r("testdata2", 0, "type550"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok550"),ret)
		self.assertEqual(P.r("testdata2", 0, "act550"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret550"),val[0]['ret'])
		time.sleep(3)
		P.sql("delete from ap_list where apid=2")
	def test_case003(self):#数据库的基站表中不存在所要查询的基站的相关信息
		a =  P.r("testdata2", 0, "send_cmd551")
		ret,val = P.s(P.r("testdata2", 0, "type551"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok551"),ret)
		self.assertEqual(P.r("testdata2", 0, "act551"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret551"),val[0]['ret'])
	def test_case004(self):#数据库的基站表中只存在所要查询的多个基站中的一个基站的相关信息
		a =  P.r("testdata2", 0, "send_cmd552")
		ret,val = P.s(P.r("testdata2", 0, "type552"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok552"),ret)
		self.assertEqual(P.r("testdata2", 0, "act552"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret552"),val[0]['ret'])
	def test_case005(self):#输入apid为空

		a =  P.r("testdata2", 0, "send_cmd553")
		ret,val = P.s(P.r("testdata2", 0, "type553"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok553"),ret)
		self.assertEqual(P.r("testdata2", 0, "act553"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret553"),val[0]['ret'])
	def test_case006(self):#输入apid含字符（汉字or字母）

		a =  P.r("testdata2", 0, "send_cmd554")
		ret,val = P.s(P.r("testdata2", 0, "type554"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok554"),ret)
		self.assertEqual(P.r("testdata2", 0, "act554"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret554"),val[0]['ret'])
	def test_case007(self):#输入apid中含空格

		a =  P.r("testdata2", 0, "send_cmd555")
		ret,val = P.s(P.r("testdata2", 0, "type555"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok555"),ret)
		self.assertEqual(P.r("testdata2", 0, "act555"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret555"),val[0]['ret'])
	def test_case008(self):#输入apid中含Tab

		a =  P.r("testdata2", 0, "send_cmd556")
		ret,val = P.s(P.r("testdata2", 0, "type556"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok556"),ret)
		self.assertEqual(P.r("testdata2", 0, "act556"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret556"),val[0]['ret'])
	def test_case009(self):#输入apid中含特殊字符（~！@#￥%……&*（）<>?）
		a =  P.r("testdata2", 0, "send_cmd557")
		ret,val = P.s(P.r("testdata2", 0, "type557"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok557"),ret)
		self.assertEqual(P.r("testdata2", 0, "act557"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret557"),val[0]['ret'])
	def test_case010(self):#输入apid为小数

		a =  P.r("testdata2", 0, "send_cmd558")
		ret,val = P.s(P.r("testdata2", 0, "type558"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok558"),ret)
		self.assertEqual(P.r("testdata2", 0, "act558"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret558"),val[0]['ret'])
	def test_case011(self):#输入apid为负数

		a =  P.r("testdata2", 0, "send_cmd559")
		ret,val = P.s(P.r("testdata2", 0, "type559"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok559"),ret)
		self.assertEqual(P.r("testdata2", 0, "act559"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret559"),val[0]['ret'])
	def test_case012(self):#输入一个apid的长度为254位

		a =  P.r("testdata2", 0, "send_cmd560")
		ret,val = P.s(P.r("testdata2", 0, "type560"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok560"),ret)
		self.assertEqual(P.r("testdata2", 0, "act560"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret560"),val[0]['ret'])
	def test_case013(self):#输入一个apid的长度为255位

		a =  P.r("testdata2", 0, "send_cmd561")
		ret,val = P.s(P.r("testdata2", 0, "type561"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok561"),ret)
		self.assertEqual(P.r("testdata2", 0, "act561"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret561"),val[0]['ret'])
	def test_case014(self):#输入一个apid的长度为256位

		a =  P.r("testdata2", 0, "send_cmd562")
		ret,val = P.s(P.r("testdata2", 0, "type562"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok562"),ret)
		self.assertEqual(P.r("testdata2", 0, "act562"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret562"),val[0]['ret'])
	def test_case015(self):#命令中"apid"字段不写

		a =  P.r("testdata2", 0, "send_cmd563")
		ret,val = P.s(P.r("testdata2", 0, "type563"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok563"),ret)
		self.assertEqual(P.r("testdata2", 0, "act563"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret563"),val[0]['ret'])
	def test_case016(self):#命令中"apid"字段书写错误

		a =  P.r("testdata2", 0, "send_cmd564")
		ret,val = P.s(P.r("testdata2", 0, "type564"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok564"),ret)
		self.assertEqual(P.r("testdata2", 0, "act564"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret564"),val[0]['ret'])

class API_VERSION(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(0.5)
	def test_case001(self):#获取API版本号

		id =565
		print id
		a =  P.r("testdata2", 0, "send_cmd565")
		ret,val = P.s(P.r("testdata2", 0, "type565"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok565"),ret)
	def test_case002(self):#命令格式异常

		id = 566
		print id
		a =  P.r("testdata2", 0, "send_cmd566")
		ret,val = P.s(P.r("testdata2", 0, "type566"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok566"),ret)

class ESL_INFO(unittest.TestCase):
	def setUp(self):
		time.sleep(0.5)
	def tearDown(self):
		pass
	def test_case001(self):#获取单个价签信息
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd593")
		ret,val = P.s(P.r("testdata2", 0, "type593"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok593"),ret)
		self.assertEqual(P.r("testdata2", 0, "act593"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret593"),val[0]['ret'])
	def test_case002(self):#获取多个价签信息
		id = ''
		print '\n' +id

		a =  P.r("testdata2", 0, "send_cmd594")
		ret,val = P.s(P.r("testdata2", 0, "type594"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok594"),ret)
		self.assertEqual(P.r("testdata2", 0, "act594"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret594"),val[0]['ret'])
	def test_case003(self):#指定查询的价签不存在于数据库的价签表中
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd595")
		ret,val = P.s(P.r("testdata2", 0, "type595"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok595"),ret)
		self.assertEqual(P.r("testdata2", 0, "act595"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret595"),val[0]['ret'])
	def test_case004(self):#只有一个价签存在于数据库的价签表中
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd596")
		ret,val = P.s(P.r("testdata2", 0, "type596"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok596"),ret)
		self.assertEqual(P.r("testdata2", 0, "act596"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret596"),val[0]['ret'])
	def test_case005(self):#输入价签号为空
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd597")
		ret,val = P.s(P.r("testdata2", 0, "type597"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok597"),ret)
		self.assertEqual(P.r("testdata2", 0, "act597"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret597"),val[0]['ret'])
	def test_case006(self):#输入价签号含字符（汉字or字母）
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd598")
		ret,val = P.s(P.r("testdata2", 0, "type598"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok598"),ret)
		self.assertEqual(P.r("testdata2", 0, "act598"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret598"),val[0]['ret'])
	def test_case007(self):#输入价签号中含空格
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd599")
		ret,val = P.s(P.r("testdata2", 0, "type599"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok599"),ret)
		self.assertEqual(P.r("testdata2", 0, "act599"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret599"),val[0]['ret'])
	def test_case008(self):#输入价签号中含Tab
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd600")
		ret,val = P.s(P.r("testdata2", 0, "type600"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok600"),ret)
		self.assertEqual(P.r("testdata2", 0, "act600"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret600"),val[0]['ret'])
	def test_case009(self):#输入价签号中含特殊字符（~！@#￥%……&*（）<>?）
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd601")
		ret,val = P.s(P.r("testdata2", 0, "type601"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok601"),ret)
		self.assertEqual(P.r("testdata2", 0, "act601"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret601"),val[0]['ret'])
	def test_case010(self):#输入的价签号中不含“ 99 ”
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd602")
		ret,val = P.s(P.r("testdata2", 0, "type602"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok602"),ret)
		self.assertEqual(P.r("testdata2", 0, "act602"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret602"),val[0]['ret'])
	def test_case011(self):#输入的价签号中不含“ - ”
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd603")
		ret,val = P.s(P.r("testdata2", 0, "type603"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok603"),ret)
		self.assertEqual(P.r("testdata2", 0, "act603"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret603"),val[0]['ret'])
	def test_case012(self):#输入的价签号不含“ - ”，不含"99"
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd604")
		ret,val = P.s(P.r("testdata2", 0, "type604"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok604"),ret)
		self.assertEqual(P.r("testdata2", 0, "act604"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret604"),val[0]['ret'])
	def test_case013(self):#输入价签号为小写
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd605")
		ret,val = P.s(P.r("testdata2", 0, "type605"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok605"),ret)
		self.assertEqual(P.r("testdata2", 0, "act605"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret605"),val[0]['ret'])
	def test_case014(self):#输入价签号为小数
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd606")
		ret,val = P.s(P.r("testdata2", 0, "type606"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok606"),ret)
		self.assertEqual(P.r("testdata2", 0, "act606"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret606"),val[0]['ret'])
	def test_case015(self):#输入价签号为负数
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd607")
		ret,val = P.s(P.r("testdata2", 0, "type607"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok607"),ret)
		self.assertEqual(P.r("testdata2", 0, "act607"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret607"),val[0]['ret'])
	def test_case016(self):#输入一个价签号的长度为254位
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd608")
		ret,val = P.s(P.r("testdata2", 0, "type608"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok608"),ret)
		self.assertEqual(P.r("testdata2", 0, "act608"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret608"),val[0]['ret'])
	def test_case017(self):#输入一个价签号的长度为255位
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd609")
		ret,val = P.s(P.r("testdata2", 0, "type609"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok609"),ret)
		self.assertEqual(P.r("testdata2", 0, "act609"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret609"),val[0]['ret'])
	def test_case018(self):#输入一个价签号的长度为256位
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd610")
		ret,val = P.s(P.r("testdata2", 0, "type610"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok610"),ret)
		self.assertEqual(P.r("testdata2", 0, "act610"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret610"),val[0]['ret'])
	def test_case019(self):#要删除的价签不存在于绑定表中
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd611")
		ret,val = P.s(P.r("testdata2", 0, "type611"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok611"),ret)
		self.assertEqual(P.r("testdata2", 0, "act611"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret611"),val[0]['ret'])
	def test_case020(self):#要删除的价签存在于绑定表中
		id = '612'
		print '\n' +id
		P.sql("INSERT INTO bind_list('eslid', 'salesno', 'apid', 'status') VALUES ('54-72-C0-99', 100001, 1, NULL)")
		time.sleep(4)
		a =  P.r("testdata2", 0, "send_cmd612")
		ret,val = P.s(P.r("testdata2", 0, "type612"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok612"),ret)
		self.assertEqual(P.r("testdata2", 0, "act612"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret612"),val[0]['ret'])
		time.sleep(4)
		P.sql('delete from bind_list')
	def test_case021(self):#命令中"eslid"字段不填写
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd613")
		ret,val = P.s(P.r("testdata2", 0, "type613"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok613"),ret)
		self.assertEqual(P.r("testdata2", 0, "act613"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret613"),val[0]['ret'])
	def test_case022(self):#"eslid"字段书写异常
		id = ''
		print '\n' +id
		a =  P.r("testdata2", 0, "send_cmd614")
		ret,val = P.s(P.r("testdata2", 0, "type614"),eval(a))
		print ret,val
		self.assertEqual(P.r("testdata2", 0, "ok614"),ret)
		self.assertEqual(P.r("testdata2", 0, "act614"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret614"),val[0]['ret'])

class ESL_QUERY_REALTIME(unittest.TestCase):#659-687
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(15)
	def test_case001(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd659")
		ret,val = P.s(P.r("testdata2", 0, "type659"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok659"),ret)
		self.assertEqual(P.r("testdata2", 0, "act659"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret659"),val[0]['ret'])
	def test_case002(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd660")
		ret,val = P.s(P.r("testdata2", 0, "type660"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok660"),ret)
		self.assertEqual(P.r("testdata2", 0, "act660"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret660"),val[0]['ret'])
	def test_case003(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd661")
		ret,val = P.s(P.r("testdata2", 0, "type661"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok661"),ret)
		self.assertEqual(P.r("testdata2", 0, "act661"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret661"),val[0]['ret'])
	def test_case004(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd662")
		ret,val = P.s(P.r("testdata2", 0, "type662"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok662"),ret)
		self.assertEqual(P.r("testdata2", 0, "act662"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret662"),val[0]['ret'])
	def test_case005(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd663")
		ret,val = P.s(P.r("testdata2", 0, "type663"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok663"),ret)
		self.assertEqual(P.r("testdata2", 0, "act663"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret663"),val[0]['ret'])
	def test_case006(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd664")
		ret,val = P.s(P.r("testdata2", 0, "type664"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok664"),ret)
		self.assertEqual(P.r("testdata2", 0, "act664"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret664"),val[0]['ret'])
	def test_case007(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd665")
		ret,val = P.s(P.r("testdata2", 0, "type665"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok665"),ret)
		self.assertEqual(P.r("testdata2", 0, "act665"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret665"),val[0]['ret'])
	def test_case008(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd666")
		ret,val = P.s(P.r("testdata2", 0, "type666"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok666"),ret)
		self.assertEqual(P.r("testdata2", 0, "act666"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret666"),val[0]['ret'])
	def test_case009(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd667")
		ret,val = P.s(P.r("testdata2", 0, "type667"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok667"),ret)
		self.assertEqual(P.r("testdata2", 0, "act667"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret667"),val[0]['ret'])
	def test_case010(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd668")
		ret,val = P.s(P.r("testdata2", 0, "type668"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok668"),ret)
		self.assertEqual(P.r("testdata2", 0, "act668"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret668"),val[0]['ret'])
	def test_case011(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd669")
		ret,val = P.s(P.r("testdata2", 0, "type669"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok669"),ret)
		self.assertEqual(P.r("testdata2", 0, "act669"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret669"),val[0]['ret'])
	def test_case012(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd670")
		ret,val = P.s(P.r("testdata2", 0, "type670"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok670"),ret)
		self.assertEqual(P.r("testdata2", 0, "act670"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret670"),val[0]['ret'])
	def test_case013(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd671")
		ret,val = P.s(P.r("testdata2", 0, "type671"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok671"),ret)
		self.assertEqual(P.r("testdata2", 0, "act671"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret671"),val[0]['ret'])
	def test_case014(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd672")
		ret,val = P.s(P.r("testdata2", 0, "type672"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok672"),ret)
		self.assertEqual(P.r("testdata2", 0, "act672"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret672"),val[0]['ret'])
	def test_case015(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd673")
		ret,val = P.s(P.r("testdata2", 0, "type673"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok673"),ret)
		self.assertEqual(P.r("testdata2", 0, "act673"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret673"),val[0]['ret'])
	def test_case016(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd674")
		ret,val = P.s(P.r("testdata2", 0, "type674"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok674"),ret)
		self.assertEqual(P.r("testdata2", 0, "act674"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret674"),val[0]['ret'])
	def test_case017(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd675")
		ret,val = P.s(P.r("testdata2", 0, "type675"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok675"),ret)
		self.assertEqual(P.r("testdata2", 0, "act675"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret675"),val[0]['ret'])
	def test_case018(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd676")
		ret,val = P.s(P.r("testdata2", 0, "type676"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok676"),ret)
		self.assertEqual(P.r("testdata2", 0, "act676"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret676"),val[0]['ret'])
	def test_case019(self):
		id = ''
		print id
		a =  P.r("testdata2", 0, "send_cmd677")
		ret,val = P.s(P.r("testdata2", 0, "type677"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok677"),ret)
		self.assertEqual(P.r("testdata2", 0, "act677"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret677"),val[0]['ret'])
	def test_case020(self):
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd678")
		ret,val = P.s(P.r("testdata2", 0, "type678"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok678"),ret)
		self.assertEqual(P.r("testdata2", 0, "act678"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret678"),val[0]['ret'])
	def test_case021(self):
		id = ''
		print '\n'+id
		a =  P.r("testdata2", 0, "send_cmd679")
		ret,val = P.s(P.r("testdata2", 0, "type679"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok679"),ret)
		self.assertEqual(P.r("testdata2", 0, "act679"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret679"),val[0]['ret'])
	def test_case022(self):
		#使用前请备份原来的字段值
		# P.sql("update bind_list set nw1 = '',nw3= '',nw4= '',op2= '',op3 = '' where eslid = '55'")

		a =  P.r("testdata2", 0, "send_cmd680")
		ret,val = P.s(P.r("testdata2", 0, "type680"),eval(a))
		self.assertEqual(P.r("testdata2", 0, "ok680"),ret)
		self.assertEqual(P.r("testdata2", 0, "act680"),val[0]['bak'])
		self.assertEqual(P.r("testdata2", 0, "ret680"),val[0]['ret'])

class RUN_INFO(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(0.5)

class GET_ESL_HB(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		time.sleep(0.5)


if __name__ == '__main__':
	unittest.main()

'''
	try:
#		跑一个class
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(HELLO)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(SALES_QUERY_ACK)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(UNBIND)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(ESL_QUERY)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(AP_REPORT)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(ESL_LIST)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(ESL_NETLINK)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(API_VERSION)
		suite1 = unittest.TestLoader().loadTestsFromTestCase(AP_INFO)
#		suite1 = unittest.TestLoader().loadTestsFromTestCase(ESL_INFO)
		# suite1 = unittest.TestLoader().loadTestsFromTestCase(ESL_UPDATE)
		unittest.TextTestRunner().run(suite1)
	except Exception,e:
		print "%d error"
	finally:
		pass

	这个是跑指定多个case

	caselist = ("test_case262","test_case263","test_case264","test_case265","test_case266","test_case267","test_case268")
	regSuite = unittest.TestSuite()
	while True:
		for tmpcase in caselist:
			regSuite.addTest(ESL_NETLINK(tmpcase))
		unittest.TextTestRunner().run(regSuite)


	这个是调试单个case

	regSuite = unittest.TestSuite()
	regSuite.addTest(ESL_NETLINK("test_case267"))
	regSuite.addTest(TEMPLATE_UPDATE("test_case887"))
	unittest.TextTestRunner().run(regSuite)
'''
