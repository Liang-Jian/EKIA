# -*- coding:utf-8 -*-



import SocketServer,struct,os,random,binascii,SM3,uuid,re,sys
import time,datetime

reload(sys)
sys.setdefaultencoding('utf8')



def unpack(fmt, bytes, start=0):

	#解包方法

	size = struct.calcsize(fmt)
	data = struct.unpack(fmt, bytes[start: start + size])
	return size, data
def sm(data):

	#把hash后值转化string
	print data
	y = SM3.hash_msg(data)
	list = []
	for i in y:
		list.append("%08x" % i),
	# print "\n",
	#只返回hash后的值，便于比较，不在里面进行补位
	# list ="00"+"".join(list)  # len2 = len(client)+(00+hash()) 33byte+len1
	list ="".join(list)  # len2 = len(client)+(00+hash()) 33byte+len1
	print list
	return list
def cutstr(data):

	#把字符串每两个以空格分开,把sm算好的值分隔发送出去
	print data
	if (len(data) %2) !=0:
		print "can't con"
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
	print strtohex,type(strtohex)
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
    except struct.error, e:
        return ''
    #确保收到全部的DATA
    buf = ""
    while len(buf) < body24[2]:
        buf += channel.recv(body24[2] - len(buf))
        # print "buf",repr(buf)
    return body24,buf

def checkFile():#随机文件名
	fileFORMAT='%Y%m%d%H%M%S'
	sj = random.randint(1000,9999)
	pwdict = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+=-"
	sa = ""
	for i in range(8):
		sa +=random.choice(pwdict)
	filename =str(time.strftime(fileFORMAT))+sa+str(sj)+".data"

	if os.path.exists('./'+filename):
		print "文件名重复已经删除"
		os.remove('./'+filename)
	return filename

HOST = '127.0.0.1'
PORT = 12345
class AMService(SocketServer.BaseRequestHandler):
	fmt = "<HIQI6s"
	USER = "lexus"
	PASSWD = "a"
	SM_SIZE =32
	PROICON = [0x20,0x03,0x19,0x9E,0xE8,0xA3,0x4C,0x9C] #协议标记
	HEADERSIZE = 32
	# bufsize = sock.getsockopt

	# self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# self.s.bind((self.HOST, self.PORT))
	# self.s.listen(5)
	# self.s.setblocking(10)  #设置阻塞
	WEL = "欢迎，"+USER
	FAIL = "客户端不合法"
	FAIL2 ="令牌无效"
	COMFIRM ="OK"
	UID = datauid()
	totalfiledata = 0
	keep=""
	SU =61441 	#F001
	F =61440	#F000


	def handle(self):
		sjc =timestmp()
		with open('./'+checkFile(),'ab') as f:
			try:
				while True:
					# data = self.request.recv(1024)
					data = receive(self.request,self.fmt)
					print len(data),self.client_address #repr(data)数据较多，忽略
					# self.checkdata(data)
					if len(data) <=0:
						print "not data"
						break
					# elif len(data) ==0:
						#     continue
					else:
						if data[0][0] == 1:
							#3，检查客户端
							if ((data[1][:len(self.USER)].decode('ascii')) == self.USER):
								hash1 = data[1][len(self.USER)+1:]
								hash1 += self.PASSWD
								print "client id pass"
								self.request.send(datoB(self.PROICON))
								self.request.send(struct.pack(self.fmt,self.SU,self.SM_SIZE*2,0,0,self.keep))
								self.request.send(datahash(SM3.hash_msg(hash1))+datahash(SM3.hash_msg(sjc)))

							else:
								#"握手失败：客户端标识["+lexu+"]不合法！"
								print "client id fail"
								hash1 = data[1][len(self.USER)+1:]
								hash1 += self.PASSWD
								self.request.send(datoB(self.PROICON))
								self.request.send(struct.pack(self.fmt,self.F,self.SM_SIZE+len(self.FAIL.encode("gb2312"))+1,0,0,self.keep))
								self.request.send(datahash(SM3.hash_msg(hash1)))
								self.request.send(self.FAIL.encode("gb2312"))
								self.request.send(datoB([0x00]))
						elif data[0][0] == 2:
							servicesm = datahash(SM3.hash_msg(sjc))
							servicesm += self.PASSWD
							sm_passwdB = datahash(SM3.hash_msg(servicesm))
							#5,检查sm
							if data[1] == sm_passwdB:
								print "client check pass"
								self.request.send(datoB(self.PROICON))
								self.request.send(struct.pack(self.fmt,self.SU,len(self.WEL.encode("gb2312"))+1,0,0,self.keep))
								self.request.send(self.WEL.encode("gb2312"))
								self.request.send(datoB([0x00]))
								starttime = datetime.datetime.now()
							else:
								print "client check error"
								print repr(data[1])
								print "++++++++++++++++++"
								self.request.send(datoB(self.PROICON))
								self.request.send(struct.pack(self.fmt,self.F,len(self.FAIL2.encode("gb2312"))+1,0,0,self.keep))
								self.request.send(self.FAIL2.encode("gb2312"))
								self.request.send(datoB([0x00]))
						elif data[0][0] == 49:
							print "file ask send(31)"
							self.request.send(datoB(self.PROICON))#8
							self.request.send(struct.pack(self.fmt,1,240,2+1,0,0,0,0))#24
							self.request.send(self.COMFIRM.encode("gb2312")+datoB([0x00])) #3
						elif data[0][0] == 50:
							'''
								print "file sending(32)"
								# print "收到文件长度：%s " % len(data[1])
								print "recv file length：%s " % len(data[1])
								#判断收到的全部data 长度
								if len(data[1]) <=0:
									print "file data over"
									# time.sleep(1)
									endtime = datetime.datetime.now()
									print "+---------------+"
									print "|file total time %ds   |" % (endtime-starttime).seconds
									print "+---------------+"
									f.close()
								f.write(data[1])
								self.totalfiledata += len(data[1])
								# print "收到文件数据"
								self.request.send(datoB(self.PROICON))#8
								self.request.send(struct.pack(self.fmt,1,240,1,0,0,0,0))#24
								self.request.send(datoB([0x00]))#1 00
							# print "文件开始传输(32)"
							# print "收到文件长度：%s " % len(data[1])
							# 判断收到的全部data 长度
							'''
							# print "file sending(32)"
							# print "收到文件长度：%s " % len(data[1])
							# print "recv file length：%s " % len(data[1])
							f.write(data[1])
							if len(data[1]) <= 0:
								print "file have been received "
								# time.sleep(1)
								endtime = datetime.datetime.now()
								# print "+--------------+"
								# print "|file total used  %ds |" % (endtime-starttime).seconds
								# print "+--------------+"
								# f.close()
								break
							self.totalfiledata += len(data[1])
							# print "===收到文件数据==="
							self.request.send(datoB(self.PROICON))  # 8
							self.request.send(struct.pack(self.fmt, 1, 240, 1, 0, 0, 0, 0))  # 24
							self.request.send(datoB([0x00]))  # 1 00

						elif data[0][0] == 51:
							# print "file send over(33)"
							self.request.send(datoB(self.PROICON))#8
							self.request.send(struct.pack(self.fmt,1,240,2+1,0,0,0,0))#24
							self.request.send(self.COMFIRM.encode("gb2312")+datoB([0x00])) #3
			except:
				print "socket error ingore "
			finally:
				f.close()
				self.request.shutdown(0)

if __name__ == '__main__':
	s = SocketServer.ThreadingTCPServer((HOST,PORT),AMService)
	s.serve_forever()
