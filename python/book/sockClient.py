# -*- coding:utf-8 -*-

import time, select, socket, traceback, threading, hashlib, json,SM3,os
import re, sys, struct, string,binascii,uuid,queue,configparser
from time import strftime,gmtime

reload(sys)
sys.setdefaultencoding('utf-8')


def unpack(fmt, bytes, start=0):

	#解包方法

	size = struct.calcsize(fmt)
	data = struct.unpack(fmt, bytes[start: start + size])
	return size, data

def cutstr(data):

	#把字符串每两个以空格分开,把sm算好的值b分隔发送出去
	# data = '08004500'
	# print data
	result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
	# print result
	return  result
def timestmp():

	#获取当前时间戳
	dt = time.strftime('%Y-%m-%d %H:%M:%S')
	return dt
def datoB(list):

	#list转bytes流

	datatobin=struct.pack("%dB"%(len(list)),*list)
	return  datatobin
def strconvert(data):

	#把string转化为bytes发送，格式 "XX XX XX"

	data=str(data).strip().split(' ')
	my=r'\x'
	fin=''
	for i in range(len(data)):
		fin=fin+struct.pack('B',int(data[i],16))
	return fin
def usertohex(data):

	#把客户标识转化hex model的string,与hash(timestamp)拼接并发送

	strtohex = cutstr(binascii.b2a_hex(data))
	# print strtohex,type(strtohex)
	return strtohex
def datahash(data): #
	_buffer = ""
	# SM3.out_hex(data)
	for i in data:
		j = ((i << 24) & 0xff000000) + ((i << 8) & 0x00ff0000) + ((i >> 8) & 0x0000ff00) + ((i >> 24) & 0xff)
		_buffer += struct.pack("I", j)
	# 相当于 _buffer += struct.pack(">I", J)，只是大小端换了一下
	# mylog.logger.debug("SM3 %d = %r" % (len(_buffer), _buffer))
	# print ("SM3 %d = %r" % (len(_buffer), _buffer))
	return _buffer
def datauid():
	uid = uuid.uuid5(uuid.uuid1(), "sutest")
	uid_buf = binascii.b2a_hex(uid.get_bytes())
	uid_l = long(uid_buf[:8], 16)
	return uid_l
def receive(channel,fmt):
	#为了确保收到全部的32B
	size = 32
	pro = channel.recv(size)
	while len(pro) < size:
		pro += channel.recv(size - len(pro))
	# print "pro",repr(pro)
	try:
		body24 = struct.unpack(fmt, pro[8:32])
	except struct.error as e:
		return ''
	#确保收到全部的DATA
	buf = ""
	while len(buf) < body24[1]:
		buf += channel.recv(body24[1] - len(buf))
	# print "buf",repr(buf)
	return body24,buf


class AMClient:
	def __init__(self):
		self.HOST ='127.0.0.1'
		# self.HOST ='192.168.1.80'
		self.PORT =12345
		self.USER = "lexus"
		self.PASSWD = "a"
		self.SM_SIZE = 32
		self.BUFFER_SIZE =4096
		self.PROICON = [0x20,0x03,0x19,0x9E,0xE8,0xA3,0x4C,0x9C] #协议标记
		self.sep = [0x00] #分隔符用来分隔标识和hash(timestamp)
		self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  #关闭nagle算法
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  #开启心跳维护
		self.__fmt = "<HIQI6s"
		self.FAIL = "客户端不合法"
		self.FAIL2= "令牌无效"
		self.WELLEN = 7
		self.SU =61441 	#F001
		self.F =61440	#F000
		self.running = False
		self.keep=""
		# self.s.setblocking(0)  #不设置阻塞

	def login(self):

		__cmd=1
		__datalen=len(self.USER)+len(self.sep)+self.SM_SIZE
		__dataid=0												
		__datapacksid=0

		#第一条信息
		FPROHEAD = struct.pack(self.__fmt,__cmd,__datalen,__dataid,__datapacksid,self.keep)
		#第二条信息
		SPROHEAD = struct.pack(self.__fmt,2,self.SM_SIZE,__dataid,__datapacksid,self.keep)


		try:
			self.s.connect((self.HOST,self.PORT))#1 多线程连接client出现10061
		except socket.gaierror as e:
			print ("Address-related error connecting to server: %s") % e
			sys.exit(1)
		except socket.error as  e:
			print("Connection error: %s") % e
			sys.exit(1)
		
		# self.s.connect((self.HOST,self.PORT))
		#2
		self.s.send(datoB(self.PROICON))
		self.s.send(FPROHEAD)
		# print "timestmp is : ",timestmp()
		sjc = timestmp()
		self.s.send(strconvert(cutstr(usertohex(self.USER)+"00")))
		# self.s.send(datahash(SM3.hash_msg(timestmp())))
		self.s.send(datahash(SM3.hash_msg(sjc)))
		#sm3+P
		# clientsm = datahash(SM3.hash_msg(timestmp()))
		clientsm = datahash(SM3.hash_msg(sjc))
		clientsm += self.PASSWD
		sm_passwdA = datahash(SM3.hash_msg(clientsm))

		while True:
			fst = receive(self.s,self.__fmt)
			print(fst)
			if len(fst)<=0:
				break
			else:
				if fst[0][0] == self.SU: #F001
					if len(fst[1]) == self.SM_SIZE * 2:
						if fst[1][:self.SM_SIZE] == sm_passwdA:
							print("service sm right")
							smvalue = fst[1][self.SM_SIZE:]
							smvalue += self.PASSWD
							print("client send 02 command start")
							#5，发送0002
							self.s.send(datoB(self.PROICON))
							self.s.send(SPROHEAD)
							#test
							# self.s.send(datahash(SM3.hash_msg(timestmp())))

							self.s.send(datahash(SM3.hash_msg(smvalue)))
							print("client send 02 command succes")
						else:
							print("service sm error")
							print("error sm",repr(fst[1][:self.SM_SIZE]))
							print("++++++++++++++++")
							self.s.shutdown(socket.SHUT_WR)
							# self.s.shutdown(socket.SHUT_WR)
					elif fst[0][1] ==  len(self.USER)+self.WELLEN:
					# else:
						print("service handshake succ")
						self.running = True
						break
				elif fst[0][0] == self.F: #F000
					#4，client接收到0xF000
					if fst[0][1] == self.SM_SIZE+len(self.FAIL.encode("gb2312"))+1:
						if fst[1][:self.SM_SIZE] == sm_passwdA:
							print("record error message")
							self.s.shutdown(socket.SHUT_WR)
							break
						else:
							print("service out of  law")
							self.s.shutdown(socket.SHUT_WR)
							break
					elif fst[0][1] == len(self.FAIL2)+1:
					# else:
						if fst[0][1].decode("gb2312") == self.FAIL2:
							print("token error")
							self.s.shutdown(socket.SHUT_WR)
							break
				else:
					print("unknown command word")
					self.running = False
					self.s.shutdown(socket.SHUT_WR)
					break
	'''
	def test(self):
		两种方法，这个为笨办法
		fst_data = ""
		while True:
			rec = self.s.recv(self.BUFFER_SIZE)#str
			fst_data += rec

			if len(fst_data) ==96: #转hex192 str(bytes) 96
				if fst_data[32:64] != sm_passwdA:  #代码中应该拒绝使用固定值
					# print "服务器身份验证失败"
					print "service token fail"
					self.s.close()
				else:
					# print "服务器身份验证通过"
					print "service token succ"
				print "servier return data: ",repr(fst_data),len(fst_data)
				# print "服务器回发的数据为: ",repr(fst_data),len(fst_data)
				smvalue = fst_data[64:]
				smvalue += self.PASSWD
				# time.sleep(1)
				# print "客户端发送02命令开始"
				print "client send 02 command start"
				self.s.send(datoB(self.PROICON))
				self.s.send(SPROHEAD)
				self.s.send(datahash(SM3.hash_msg(smvalue)))
				# print "客户端发送02命令成功"
				print "client send 02 command succes"
				# time.sleep(1)
				break
			else:
				continue
		# sec_data = ""
		while True:   #两个whileTrue最好写成一个
			sec_data = receive(self.s,self.__fmt)
			# print repr(sec_data)
			# data = sec_data[1][:4].decode('gb2312')#.encode('unicode')# =="欢迎"
			# print data,type(data)
			if sec_data[1][:4].decode('gb2312') ==self.WELCOME.decode("utf-8"):
				# print "服务器握手验证成功"
				print "service handshake succ"
				break
			else:
				# print "服务器握手验证失败"
				print "service handshake fail"
				self.s.close()
				break
	'''
	def fileRequest(self,uid):
		__ffile = struct.pack(self.__fmt,49,1,uid,0,self.keep)
		self.s.send(datoB(self.PROICON))
		self.s.send(__ffile)
		self.s.send(datoB(self.sep))

		rdata = receive(self.s,self.__fmt)

		if rdata[0][0] == self.SU: #F001
			if rdata[1][:2].decode('gb2312') == "OK":
				print("ask send file succ(31)")
			else:
				print("comfirm message fail(31)")
		else:
			print("ask send file fail(31)")
	def fileOver(self,uid,sid):
		self.s.send(datoB(self.PROICON))
		self.s.send(struct.pack(self.__fmt,51,1,uid,sid,self.keep))
		self.s.send(datoB([0x00]))

		odata = receive(self.s,self.__fmt)

		if odata[0][0] == self.SU: #F001
			if odata[1][:2].decode('gb2312') == "OK":
				print("comfirm file send succ(33)")
			else:
				print("comfirm message fail(33)")
		else:
			print("comfirm file send fail(33)")
	def shutsock(self):
		self.s.shutdown(socket.SHUT_WR)
	def sendfile(self,filepath,readsize):
		##############

		sid = 1
		uid = datauid()
		filedaxiao =0
		self.login()
		###########################

		# print "开始进行传输文件"
		filesize = os.path.getsize(filepath)
		# print "文件大小 %d k" %(filesize /1024)
		print("file size %d k" %(filesize /1024))
		f = open(filepath, 'rb')

		try:
			while self.running:
				self.fileRequest(uid)
				fdata = f.read(readsize)
				# print "start sending file(32)"
				self.s.send(datoB(self.PROICON))
				self.s.send(struct.pack(self.__fmt,50,len(fdata),uid,sid,self.keep))
				self.s.send(fdata)

				#每个包延时时间，单位s
				time.sleep(0)

				filedaxiao += len(fdata)
				if len(fdata) <= 0:
					print("file have been reading over")
					break
				tdata = receive(self.s,self.__fmt)
				# print "tdata",tdata
				if tdata[0][0] ==self.SU:
					print("sending file succ(32)")
				else:
					print("sending file fail(32)")
				sid +=1
				self.fileOver(uid,sid)
				print("send file size %d K" % (filedaxiao / 1024))
		finally:

			f.close()
			self.shutsock()
	'''
	在类中不要自己调自己这样会多出一个线程来。逻辑问题，自己调自己
	__init__已经生成了连接
	def mulThread(self,count,fpath,fsize):
		#多线程发送文件

		threads = []
		t1 = threading.Thread(target=AMClient().sendfile(fpath,fsize),args=(self,))
		threads.append(t1)
		t2 = threading.Thread(target=AMClient().sendfile(fpath,fsize),args=(self,))
		threads.append(t2)
		for tt in threads:
			tt.start()
		

		for i in range(count):
			threading.Thread(target=AMClient().sendfile(fpath,fsize),args=(self,))
	'''

if __name__ == '__main__':

	fname = sys.argv[1] 				#文件名称
	fsize = int(sys.argv[2])*1024		#发包大小
	loops = int(sys.argv[3])			#线程数
	threads = []
	for i in range(loops):
		threads.append(threading.Thread(target=AMClient().sendfile,args=(fname,fsize)))
	for tt in threads:
		tt.start()
	for tt in threads:
		tt.join()
