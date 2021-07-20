#! /usr/bin/python
# encoding: utf-8

from struct import unpack_from as U
from struct import calcsize as L
from struct import pack as P
from binascii import b2a_hex

#from esl_init import log
import esl_init

import os
import struct
import time, pickle

##########################################
#
# Notice: 
# U can call osd_output(data , number) 
#
##########################################


def get_time():
	t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() ) )	
	return t

def _ParsePacketNum(pack_num):
	ret = pack_num & 0b11111111111111
	return ret

def _ParseRF(data,length,esl_data): # GET CMD_PACKET
	pack_num_flag = 0

	cmd = []  # cmd = [pack_num , frame]
	fmt = "B"   # 1B
	offset = 0
	ctr_sid  = struct.unpack_from(fmt, data, offset)[0]  # CTRL + SID
		
	offset += struct.calcsize(fmt)  # ADDR
	fmt = "B"   # 1B		
	addr = struct.unpack_from(fmt, data, offset)[0]

	offset += struct.calcsize(fmt)  # PKG_NUM
	fmt = "H"   # 2B
	pack_num = struct.unpack_from(fmt, data, offset)[0]
	cmd.append(pack_num)
	if pack_num >= 0xC000:
		pack_num_flag = 1

	offset += struct.calcsize(fmt)  # FRAME 
	fmt = "%ss" % (length - offset - 2 )   # length - offset - CRC
	frame = struct.unpack_from(fmt, data, offset)[0]
	
	lseek_len = (_ParsePacketNum(pack_num) - 1)
	#os.lseek(filefd,lseek_len * 20 , os.SEEK_SET)
	#os.write(filefd,frame)
	esl_data[lseek_len] = frame
	
	t = pack_num_flag
	return t 

def _ParseAP(data , number): # Get RF_PACKET
	esl_id = []
	d={}  # d = {pn1 : data1, pn2 : data2,...}
	l = []
	ret = []
	dic = []
	offset = 0
	filefd = None
	open_once = 0
	flag = 0 
	filename = []
	dir_name = 'tmp_file'
	e_id = 0
	esl_data = {}
	try:
		os.mkdir(dir_name)
	except OSError:
		pass


	while (number > 0):
		fmt = ">I"   # 4B
		e_id = struct.unpack_from(fmt,data,offset)[0]  # ESL_ID
		filename = os.path.join(dir_name,str(hex(e_id)).upper()[2:])
		#esl_init.log.debug("ESL_ID is %x" % e_id)
		if open_once < 1:
			try:
				filefd = open(filename, 'r')
				esl_data = pickle.load(filefd)
				if not esl_data:
					esl_data = {}
				filefd.close()
			except:
				esl_data = {}
			open_once = 1
		esl_id.append(e_id)

		offset += struct.calcsize(fmt)  # LEN
		fmt = "I"   # 4B
		length = struct.unpack_from(fmt, data, offset)[0]

		offset += struct.calcsize(fmt)  # FRAME n
		fmt = "%ss" % length  
		frame = struct.unpack_from(fmt, data, offset)[0]

		# now we catch RF frame
		# and next we parse it
		flag = _ParseRF(frame,length,esl_data) 

		offset += struct.calcsize(fmt)  # next data_ack_t 
		number -= 1

	filefd = open(filename, 'w')
	pickle.dump(esl_data, filefd)
	filefd.close()

	buf=[]
	if flag > 0:
		#os.fsync(filefd)
		#os.lseek(filefd,0,os.SEEK_SET) # 需要重新定位文件指针
		#while(buf != ""):
		#	buf = os.read(filefd,20)
		#	ret.append(buf)
		#os.close(filefd)
#		os.remove(filename)
		
		#l = ''.join(ret)
		#esl_init.log.debug(b2a_hex(l))
		filefd = open(filename, 'r')
		esl_data = pickle.load(filefd)
		filefd.close()
		ks = esl_data.keys()
		ks.sort()
		l = ''.join(esl_data[k] for k in ks)

		cmd_des(l,filename)

	return ret
	
def ParseHtp(data,number): 
	l = []
	esl_id = []
	i = 0
	offset = {}
	for i in range(number + 1):
		offset[i] = 0

	lens = len(data)

	while(number > 0):

		fmt = ">I"   # 4B			  
		e_id = struct.unpack_from(fmt, data, offset[number])[0]  # ESL_ID
		try:
			esl_id.append(e_id)
		
			offset[number] += struct.calcsize(fmt)  # ACK
#		esl_init.log.debug(" #1 ... offset %d" , offset[number])
			fmt = "B"   # 1B		
			ack = struct.unpack_from(fmt, data, offset[number])[0]
			if ack == 1 :	   # ACK ?= 0
				number -= 1
				continue

			offset[number] += struct.calcsize(fmt)  # NUMBER
			fmt = "H"   # 2B
			pack_num = struct.unpack_from(fmt, data, offset[number])[0]

			offset[number] += struct.calcsize(fmt)  # LEN
			fmt = "I"   # 4B
			length = struct.unpack_from(fmt, data, offset[number])[0]

			offset[number] += struct.calcsize(fmt)  # FRAME n
			fmt = "%ss" % length
			frame = struct.unpack_from(fmt, data, offset[number])[0]

			_ParseAP(frame,pack_num)

			offset[number] += struct.calcsize(fmt)  # next data_ack_t 
			number -= 1
		
			offset[number] = offset[number+1]

		except Exception, e:
			esl_init.log.debug("%s" % e)
	return

#命令解析函数
def num_fun(cmd, data, offset):
	out = []
	d = 0
	for (title, fmt) in num_par[cmd]:
		#解析某个字段
		if fmt == 'LEN':
			#d = U("%ss" % out[5], data, offset)[0]
			d = cmd3_fun(data, offset)
			offset += L("%ss" % (out[7]))

		elif fmt == 'BITMAP':
			lens = (out[7] - out[3] +1) * ((out[9]-out[5] +1 + 7) / 8)
			d = U("%ss" % lens, data, offset)[0]
			offset += L("%ss" % lens)
		elif fmt == 'nums_B': #6号命令
			for i in range(d):
				d = U('B', data, offset)[0]
				offset += L('B')
				out.append(title)
				out.append(d)
			continue #已经遍历完数据，不需要下面的逻辑处理
		else:
			d = U(fmt, data, offset)[0]
			offset += L(fmt)
		out.append(title)
		out.append(d)

	return offset, out

def cmd3_fun(data, offset):
	d = []
	p = U('B', data, offset+0)[0]

	color = p & 0b1111
	para = (p & 0b00110000) >> 4

	p_dic = {1: "font", 2:"OSD", 0:"bitmap"}
	d.append(p_dic[para])
	d.append("color %s"%color)
	
	if para == 1:
		#d.extend( U('BB%ss' % (offset-3), data, offset+1) )
		d.extend( U('BB', data, offset+1) )
	elif para == 2:
		#d.extend( U('HHHHBB%ss' % (offset-11), data, offset+1) )	
		d.extend( U('HHHHBB', data, offset+1) )	
	elif para == 0:
		#d.extend( U('HHHH%ss' % (offset-9), data, offset+1) )	
		d.extend( U('HHHH', data, offset+1) )	
	
	return d

#命令解析器表 命令号：命令处理函数，此函数返回命令所在的数据段长度
num_par = {1:[('Display LID', 'B'),('LID', 'B')], 
			2:[('Display OSD','B'),('LID','B'),('num','I')], 
			3:[('Write LID','B'),('LID', 'B'),('size','H'),('len','H'),('DATA','LEN'),('CRC', 'H')], 
			4:[('Display BITMAP', 'B'),('start_x', 'H'),('start_y', 'H'),('end_x', 'H'),('end_y', 'H'),('BITMAP','BITMAP')], 
			5:[('DELAY', 'B'),('sec', 'B')], 
			6:[('DISPLAY Multi', 'B'),('delay','B'),('nums', 'B'),('LID', 'nums_B')],
			7:[('OSD', 'B'),('LastD', 'B'), ('LID1', 'B'),('num1', 'I'),('LID2', 'B'),('num2','I'),('LID3','B'),('num3','I')], 
			128:[('ERASE', 'B')],
			0x76:[('END', 'B')]}

def get_cmd(data, offset):
	return U('B', data, offset)[0]

def cmd_des(data,e_id):
	f = open("log/osd_out_put.tmp", "a+")
	t = get_time()
	f.write("---------BEGIN [%s][%s]-------------------\n" % (t,e_id))
	offset = 0
	lens = len(data)
	while offset < lens:
		cmd = get_cmd(data, offset)
		if cmd not in num_par:
			esl_init.log.debug("ERROR: cmd %s is not valid." % cmd)
			esl_init.log.debug("ERROR: CMD DATA  offset is %d \nFllowing is CMD DATA:" % offset )
			esl_init.log.debug(b2a_hex(data))
			ef = open("%s.err" % e_id, "w")
			ef.write(data)
			ef.close()
			esl_init.log.error("###################%s, offset:%s" % (e_id, offset))
			f.write("ERROR: cmd %s is not valid.\n" % cmd)
			break
		offset, out = num_fun(cmd, data, offset)
		#esl_init.log.debug(out)
		f.write("%s\n" % out)
		if cmd == 0x76:
			break
	
	f.write("---------END [%s][%s]-------------------\n\n" % (t, e_id))
	f.close()

def osd_output(output_value,number):
	try:
		#esl_init.log.debug(b2a_hex(output_value))
		ParseHtp(output_value,number)
	except Exception, e:
		pass
