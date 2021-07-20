#-*- coding:utf-8 -*-

# print "i wan fufck %s  i like her  %s age" %("lily",32)
import requests, json, sqlite3, random,time,threading
from time import ctime

class Shua(object):
    def __init__(self):

        self.url = "http://blog.bccn.net/s912360101/6524"
        self.url1 = "http://blog.bccn.net/s912360101/6523"
        self.url2 = "http://blog.bccn.net/s912360101/6522"
        self.url4 = "http://blog.bccn.net/s912360101/6521"
        selfurl3 = "http://blog.bccn.net/s912360101/6519"
    def jb1(self):
        print 'jb1 start' +ctime()
        n = 0
        while True:
            n = n + 1
            s = requests.get(self.url)
            time.sleep(0.1)
            print n
        print 'jb1 over' +ctime()
    def jb2(self):
        print 'jb2 start' +ctime()
        n = 0
        while True:
            n = n + 2
            s = requests.get(self.url2)
            time.sleep(1)
        print 'jb2 over' +ctime()
    def jb3(self):
        print 'jb3 start' +ctime()
        n = 0
        while True:
            n = n + 3
            s = requests.get(self.url3)
            time.sleep(0.1)
        print 'jb3 over' +ctime()
    def jb4(self):
        print 'jb4 start' +ctime()
        n = 0
        while True:
            n = n + 4
            s = requests.get(self.url1)
            time.sleep(1)
        print 'jb4 over' +ctime()
    def jb5(self):
        print 'jb5 start' +ctime()
        n = 0
        while True:
            n = n + 5
            s = requests.get(self.url4)
            time.sleep(1)
        print 'jb5 over' +ctime()
    def process(self):
        threads = []
        t1 = threading.Thread(target=Shua.jb1,args=(self,))
        threads.append(t1)
        t2 = threading.Thread(target=Shua.jb2,args=(self,))
        threads.append(t2)
        t3 = threading.Thread(target=Shua.jb3,args=(self,))
        threads.append(t3)
        t4 = threading.Thread(target=Shua.jb4,args=(self,))
        threads.append(t4)
        t5 = threading.Thread(target=Shua.jb5,args=(self,))
        threads.append(t5)

        for tt in threads:
            tt.start()

class footb:
    def __init__(self):
        self.url = "https://www.jleague.jp/match/j1/2017/082601/live/#live"
    def getdata(self):
        s = requests.get(self.url)
        s.raise_for_status()
        s.encoding = s.apparent_encoding
        return s.text
def a():
	pass


import socket,sys,argparse
host ='localhost'
def echo_client():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)
    print "connecting to %s  port %s" % server_address
    s.connect(server_address)
    try:
        message = 'test message '
        print 'sending %s' % message
        s.sendall(message)
        amount_recv = 0
        amount_expe = len(message)
        while amount_recv < amount_expe:
            s.recv(16)
            amount_recv += len(data)
            print "received : %s" % data
    except socket.errno,e:
        print 'socket error: %s' % str(e)
    except Exception,e:
        print "Other exception: %s" %str(e)
    finally:
        print 'close connect to servier'
        s.close()

class hs:
    def 18t011(self):
        import sys
        if  len(sys.argv) < 2:
            filename=raw_input("input filename where your 18byte file")
        else:
            filename=sys.argv[1]
        lst=[]
        fw=open('11byte.txt', 'w')
        with open(filename, 'r') as f:
            for eachline in f:
                s = format(int(eachline[8:]),'x')
                s=''.join((s[0:2],'-',s[2:4],'-',s[4:6],'-', s[6:8],'\n')).upper()
                if s not in lst:
                    fw.write(s)
                lst.append(s)
        fw.close()
class dick:
	country = "chinafu"
	# def getCountry(self):
	# 	print self.__country

	@classmethod
	def getCou(cls):
		print cls.country

class Univer:
	def __init__(self,name,age):
		self.name = name
		self.age = age
	def getName(self):
		print self.name
	def getAge(self):
		print self.age
class Student(Univer):
	def __init__(self,name,age,sno,mark):
		Univer.__init__(self,name,age)
		self.sno = sno
		self.mark = mark
	def getSno(self,sno):

		print self.sno
	def getMark(self):
		print self.mark

########################
# print  17 /3  # int /int  -> int
# print 17 /3.0 # int /float -> float
# print 17 // 3.00#floor	division
# print 5 ** 2#计算幂乘方
# print 3*3.75 /1.5 #整数和浮点数的混合计算中,整数会被转换为浮点数
# print 'c:\some\name'
# print r'c:\some\name'
# print 'py' 'thon' #相邻的两个或多个字符串字面量
# word = 'python'
# print word[0:2] #包含起始的字符,不包含末尾的字符。这使得s[:i]+s[i:]永远等于s
# print str(u"abc")
# li = [2,4,5,6]
# li.append( 2 ** 3)
# print li
#斐波那契初始子序列
# a ,b = 0,1
# while b <10:
# 	print b
# 	a,b = b ,a +b



# def fib2(n):
# 	result = []
# 	a,b = 0,1
# 	while a < n:
# 		result.append(a)
# 		a,b =b ,a + b
# 	return result
# def fib2(100)


# i = 4
# def f(arg = i ): #默认值只计算一次
# 	print arg
# i = 6
# f()

# def f(a,L=[]):
# 	L.append(a)
# 	return L
# print f(1)
# print f(2)
# print f(3)

# def cheeseshop(kind,*arguments,**keywords):
# 	print "-- doyou have any ",kind, "?"
# 	print "-- i,m sorry ,we are  all out of ",kind
# 	for arg in arguments:
# 		print arg
# 	print "-" * 40
# 	keys = sorted(keywords.keys())
# 	for kw in keys:
# 		print kw, ":",keywords[kw]
# cheeseshop("lim","it;s very runny")

# strings = ["ad","fb","ca","dq"]
# for i ,j in enumerate(strings): //suoyin && weizhi
# 	if  "a" in j:
# 		strings[i] = 'f'
# print strings
'''
str = ("fsdf","wef","sfd","as")
for i ,j in enumerate(str):
	print i ,j

这个脚本仅供测试使用,因为会循环获取时间，所以请关闭不用的进程，以免造成卡顿
如有其他问题请及时联系

class SickMan:
	#这个执行脚本的次数 96为次数
	def __chu__(self):
		for i in range(96):
			print "chu"
			time.sleep(300) #两个命令之间的间隔
	#这个是监控时间的模块
	def __run__(self):
		while True:
			current_time = time.localtime(time.time())
			if ((current_time.tm_hour == 9) and (current_time.tm_min == 0) and (current_time.tm_sec == 0)):# 9 为指定时间，0 为分 ，0为秒
				self.__chu__()
			else:
				pass
if __name__ == '__main__':
	P = SickMan().__run__()
'''

'''
import os.path
rootdir='/home/sct/workspace/1.3.2/train'
print "***********"
for parent,dirnames,filenames in os.walk(rootdir):
    print "&&&&&&&&&&&&&&"
    for dirname in dirnames:
        print "parent is:"+parent
        print "dirname is"+dirname
    for filename in filenames:
        print "parent is:"+parent
        print "filename is:"+filename
        print "the full name of the file is:"+os.path.join(parent,filename)

import  os
url = 'test.bar.bz2'
print(os.path.basename(os.path.realpath(__file__)))
print(os.listdir('./'))
filename = os.path.basename(url)
filepath = os.path.dirname(url)
print filename
print filepath

import os
filename = 'test.bar.bz2'
(filepath, tempfilename) = os.path.split(filename);
print filepath, tempfilename
(shotname, extension) = os.path.splitext(tempfilename);
print shotname, extension


import  os
print os.getcwd()

filename = raw_input("输入文件名，包含拓展名,且文件名必须和脚本放在同一目录下")
if not os.path.exists('./' + filename):
	print "file not in this content"
else:
	print "file"


#-*- coding: UTF-8 -*-
import os,struct,sys,uuid,binascii
from binascii import b2a_hex
import datetime,time
starttime = datetime.datetime.now()
#long running
time.sleep(5)
endtime = datetime.datetime.now()
# print str()+"s"
print "total time %ds" % (endtime-starttime).seconds
'''

# print os.getcwd()
# print  os.listdir('./')
# for filelist in filename:
# 	print filename,os.path.getsize(filelist)
# # s.listdir()

'''
import threading,sys
from Queue import Queue

#假设有10000个任务
myqueue = Queue(10000)
for i in range(10000):
    myqueue.put('task%d' % (i + 1))

'''
#任务执行方法，任务执行完成就被移除
#以下只是简单输出任务执行字符串，并记录日志
'''
def foo():
    try:
        task = myqueue.get_nowait()
    except Exception, e:
        pass
    print '%s execute!' % task

    logfile = open('./log.txt', 'a')
    print >> logfile, '%s finish!' % task
    logfile.close()

#自定义线程类，继承threading.Thread
class MyThread(threading.Thread):
    def __init__(self, func, args=(), name=''):
        super(MyThread, self).__init__(target=func, args=args, name=name)
        self.name = name
        self.func = func
        self.args = args

    '''
    '''
    重写threading.Thread的run方法
    在这个方法中，会循环检测myqueue是否还有任务
    '''
    '''
    def run(self):
        while myqueue.qsize() > 0:
            self.func()

#主方法
def main():
    #开启30条线程来执行
    threads = []
    nloops = range(30)

    for i in nloops:
        t = MyThread(foo)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

if __name__ == '__main__':
    main()

 '''
