#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Connect new generation AP and esl-working with HTPv3 over TCP
# created by Benny Gao

import time, select, socket, traceback, threading, hashlib, json
import re, Queue, sys, struct, ConfigParser
from esl_init import log
import bind

LISTENING_PORT = 1234
BUFFER_SIZE = 1024

# inbound报文处理线程数
INBOUND_PACKET_PROCESSORS_NUM = 4
# HTPv3多个任务参与者提交任务数据的超时时间
TIMEOUT_HTPv3_TASK_PARTICIPANT_SUBMIT_DATA = 5

# AP通讯报文中payload_id的定义
PID_REQ_AP_AUTHENTICATE	= 1  # AP认证请求, AP->esl-working
PID_RSP_AP_AUTHENTICATE	= 2  # AP认证结果响应
PID_REQ_AP_HEARTBEAT	= 3  # AP心跳
PID_REQ_ESL_HEARTBEAT	= 5  # ESL价签心跳
PID_REQ_ESL_UPDATE		= 8  # ESL更新请求
PID_ACK_ESL_UPDATE		= 7  # ESL更新结果ACK
PID_REQ_NETWORKING		= 16 # 组网请求
PID_ACK_NETWORKING		= 15 # 组网结果ACK
PID_REQ_ESL_QUERY		= 18 # ESL查询
PID_ACK_ESL_QUERY		= 17 # ESL查询ACK

# 协议值定义

HTP_VERSION_1 = 0x0370
HTP_VERSION_2 = 0x0360
HTP_VERSION_3 = 0x0350

HTP_SLEEP_CMD = 0x03B0

standalone = False
connection_ip_addr = lambda x: str(x.getpeername()[0])
indent = lambda x: str(bytearray(['\t' for i in xrange(x)]))
get_value = lambda dict, key, default: dict[key] if key in dict else default


def get_version(op3):
	version_dict = {"HS_EL_5300":HTP_VERSION_3, 
						"HS_EL_5301":HTP_VERSION_3, 
						"HS_EL_5104":HTP_VERSION_2, 
						"HS_EL_5033":HTP_VERSION_1}
	return version_dict.get(op3, HTP_VERSION_1)

def indent_member(txt, n = 1):
	_str = ''
	l = 0
	blank = indent(n)
	for s in txt.splitlines(True):
		if len(s.split()) == 0:
			continue

		_str += s if l == 0 else blank + s
		l += 1
	return _str

crc16_ccitt_table = [  # CRC 字节余式表
	0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
	0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
	0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
	0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
	0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
	0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
	0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
	0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
	0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
	0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
	0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
	0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
	0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
	0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
	0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
	0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
	0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
	0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
	0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
	0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
	0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
	0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
	0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
	0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
	0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
	0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
	0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
	0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
	0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
	0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
	0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
	0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0
]


def crc16_ccitt(data, start, len):
	crc = 0
	for byte in data[start: start + len]:
		high = (crc >> 8) & 0xff
		crc = ((crc << 8) ^ crc16_ccitt_table[high ^ byte]) & 0xffff
	return crc


def md5_digest(data):
	digest = hashlib.md5()
	digest.update(data)
	return digest.hexdigest().upper()


def b2a_hex(data):
	ascii = ""
	for byte in data:
		ascii += "%02X " % byte
	return ascii.strip()


def format_binary(bytes):
	str = '----+---------------------------------------------------+------------------+\n'
	str += "    | "
	for i in xrange(0, 16):
		str += ("%02d " % i) + ('- ' if i == 7 else '')
	str += '| %16d |\n' % len(bytes)
	str += '----+---------------------------------------------------+------------------+'
	left = ''
	right = ''
	for i in xrange(0, len(bytes)):
		if i % 16 == 0:
			str += ('\n' if i == 0 else "%s| %s |\n" % (left, right))
			left = "%04d| " % i
			right = ''

		left += ('- ' if i % 8 == 0 and i % 16 != 0 else '') + ("%02X " % bytes[i])
		right += (bytes[i: i + 1].decode() if bytes[i] in xrange(32, 127) else '.')

	str += "%-56s| %-16s |\n" % (left, right)
	str += '----+---------------------------------------------------+------------------+\n'
	return str


def unpack(fmt, bytes, start=0):
	size = struct.calcsize(fmt)
	data = struct.unpack(fmt, bytes[start: start + size])
	return size, data

def is_empty(list):
	if not list:
		return True
	elif len(list) == 0:
		return True
	else:
		return False

def get_id_by_num(num, size):
	id = bytearray([0 for i in xrange(size)])
	for i in xrange(size):
		idx = size - i - 1
		id[idx] = (num >> (idx << 3)) & 0x00FF
	return id

def id2str(id):
	size = len(id)
	txt = ''
	for i in xrange(size):
		if i > 0:
			txt += '-'
		txt += "%02X" % id[i]
	return txt

def str2id(txt):
	id = bytearray()
	if not re.match(r"^[0-9a-fA-F]{2}(-[0-9a-fA-F]{2})*$", txt):
		return id

	start = 0
	while True:
		m = re.search(r'[0-9a-fA-F]{2}', txt[start:])
		if not m:
			break
		id.extend([int(m.group(), 16)])
		start += m.end()

	return id

class Config:
	def __init__(self):
		self.config = None
		self.filename = None
		self.lock = threading.Lock()

	def load(self, filename):
		self.filename = filename
		self.config = ConfigParser.SafeConfigParser()
		self.config.optionxform = str
		try:
			self.config.read(filename)
		except Exception, ex:
			print ex

	def save(self):
		f = open(self.filename, "w+")
		self.config.write(f)
		f.close()

	def get(self, section, option, default):
		try:
			return self.config.get(section, option, default)
		except:
			return default

	def get_options(self, section):
		sec = {}
		try:
			for opt in self.config.options(section):
				sec[opt] = self.config.get(section, opt)
		except Exception:
			pass

		return sec

	def set(self, section, option, value):
		if not section in self.config.sections():
			self.config.add_section(section)
		self.config.set(section, option, value)

class HTPv2UnitData:
	__head_fmt = "<4sI"

	def __init__(self):
		self.data_id = bytearray([0 for x in xrange(4)])
		self.len = 0
		self.data = None

	def strid(self):
		return id2str(self.data_id)

	def decode(self, bytes, start):
		consumed, (self.data_id, self.len) = unpack(HTPv2UnitData.__head_fmt, bytes, start)
		self.data_id = bytearray(self.data_id)
		self.data = bytes[start + consumed: start + consumed + self.len]
		return consumed + self.len

	def encode(self, bytes):
		self.len = len(self.data)
		bytes.extend(struct.pack(HTPv2UnitData.__head_fmt, self.data_id, self.len))
		bytes.extend(self.data)


class HTPv3UnitData:
	__head_fmt = "<4sBB"

	def __init__(self):
		self.data_id = bytearray([0 for x in xrange(4)])
		self.channel = 0
		self.len = 0
		self.data = None

		self.index = 0 # 这个packet在整个HTP task报文中的次序
		self.sequence = 0 # sequence in packets of task participant
		self.ack = 0 # 这个packet对应收到的ack值

	def __str__(self):
		_str_fmt = '''HTPv3UnitData {
	id = [%s]
	channel = %d
	len = %d
	data = [%s]
}
'''
		return _str_fmt % (id2str(self.data_id), self.channel, self.len, \
						   "null" if not self.data else b2a_hex(self.data))

	def decode(self, bytes, start=0):
		consumed, (self.data_id, self.channel, self.len) = unpack(HTPv3UnitData.__head_fmt, bytes, start)
		self.data = bytes[start + consumed: start + consumed + self.len]
		return consumed + self.len

	def encode(self, bytes):
		self.len = len(self.data)
		bytes.extend(struct.pack(HTPv3UnitData.__head_fmt, str(self.data_id), self.channel, self.len))
		bytes.extend(self.data)

	def calc_size(self):
		self.len = struct.calcsize(HTPv3UnitData.__head_fmt) + (0 if not self.data else len(self.data))
		return self.len


class WakeupCommand:
	__head_fmt = "<HIHBBB8s"

	def __init__(self):
		self.cmd = 0x0310
		self.len = 0
		self.bandrate = 0
		self.power = 0
		self.duration = 0
		self.slot_duration = 0
		self.reserved = bytearray([0 for x in range(8)])
		self.data = None

	def __str__(self):
		_str_fmt = '''WakeupCommand {
	cmd = 0x%04X
	len = %d
	bandrate = %d
	power = %d
	duration = %d
	slot_duration = %d
	reserved = "%s"
	data = %s
}
'''
		return _str_fmt % (self.cmd, self.len, self.bandrate, self.power, self.duration, self.slot_duration, \
						   self.reserved, "null" if not self.data else indent_member(str(self.data)))

	def encode(self, bytes):
		self.len = struct.calcsize(WakeupCommand.__head_fmt) + self.data.calc_size() - 2 - 4  # 减去command和size的长度
		bytes.extend(struct.pack(WakeupCommand.__head_fmt, self.cmd, self.len, self.bandrate, self.power,
								 self.duration, self.slot_duration, str(self.reserved)))
		self.data.encode(bytes)

	def calc_size(self):
		size = struct.calcsize(WakeupCommand.__head_fmt)
		if self.data:
			size += self.data.calc_size()
		return size

class SleepCommand:
	__head_fmt = "<HIHBBBBBB7sH"

	def __init__(self):
		self.cmd = HTP_SLEEP_CMD
		self.len = 0
		self.bandrate = 0
		self.power = 0
		self.mode = 0
		self.interval = 0
		self.idxctrl = 0
		self.times = 0
		self.framelen = 1
		self.reserved = bytearray([0 for x in range(7)])
		self.sleepn = 0
		self.data_list = []

	def __str__(self):
		_str_fmt = '''SleepCommand {
	cmd = 0x%04X
	len = %d
	bandrate = %d
	power = %d
	mode = %d
	interval = %d
	idxctrl = %d
	times = %d
	framelen = %d
	reserved = "%s"
	sleen = %d
	data = [%s]
}
'''
		idstr = ''
		for item in self.data_list:
			idstr += indent_member(str(item), 2)
		return _str_fmt % (self.cmd, self.len, self.bandrate, self.power, self.mode, self.interval, \
						   self.idxctrl, self.times, self.framelen, self.reserved, self.sleepn, \
							"null" if not self.data_list else indent_member(idstr))

	def encode(self, bytes):
		self.len = self.calc_size() - 4 -2
		bytes.extend(struct.pack(SleepCommand.__head_fmt, self.cmd, self.len, self.bandrate, self.power,
						self.mode, self.interval,self.idxctrl, self.times, self.framelen, str(self.reserved), self.sleepn))
		for data1 in self.data_list:
			data1.encode(bytes)

	def calc_size(self):
		size = struct.calcsize(SleepCommand.__head_fmt)
		for data1 in self.data_list:
			size += data1.calc_size()
		return size

class EslConfig:
	__data_fmt = "<4sB"
	def __init__(self):
		self.esl_id = bytearray([0 for x in xrange(4)])
		self.net_id = 0

	def __str__(self):
		_str_fmt = '''EslConfig {
	esl_id = %s
	net_id = %d
}
'''
		return _str_fmt % (id2str(self.esl_id), self.net_id)

	def encode(self, bytes):
		bytes.extend(struct.pack(EslConfig.__data_fmt, str(self.esl_id), self.net_id))

	def calc_size(self):
		return struct.calcsize(EslConfig.__data_fmt)

	def decode(self, bytes, start=0):
		consumed, (self.esl_id, self.net_id) = unpack(EslConfig.__data_fmt, bytes, start)
		return consumed


class GroupConfig:
	__head_fmt = "<4sBIH"

	def __init__(self):
		self.group_id = bytearray([0 for x in xrange(4)])  # group id	uint8	4
		self.group_channel = 0  # channel uint8	1
		self.reserved = 0  # reserved	uint8	4
		self.num = 0  # n	uint16	2
		self.esl_config_list = []  # esl cfg data	uint8	x

	def __str__(self):
		_str_fmt = '''GroupConfig {
	group_id = %s
	channel = %d
	reserved = %d
	num = %d
	esl_config_list = [
		%s
	]
}
'''
		ecstr = ''
		for ec in self.esl_config_list:
			ecstr += indent_member(str(ec), 2)
		return _str_fmt % (id2str(self.group_id), self.group_channel, self.reserved, self.num, ecstr)

	def encode(self, bytes):
		self.num = len(self.esl_config_list)
		bytes.extend(struct.pack(GroupConfig.__head_fmt, str(self.group_id), self.group_channel, \
								 self.reserved, self.num))
		for esl_config in self.esl_config_list:
			esl_config.encode(bytes)

	def calc_size(self):
		self.num = len(self.esl_config_list)
		size = struct.calcsize(GroupConfig.__head_fmt)
		for ec in self.esl_config_list:
			size += ec.calc_size()
		return size

	def decode(self, bytes, start=0):
		del self.esl_config_list[:]
		consumed, (self.group_id, self.group_channel, self.reserved, self.num) = unpack(GroupConfig.__head_fmt, bytes,
																					  start)
		for i in xrange(self.num):
			esl_config = EslConfig()
			consumed += esl_config.decode(bytes, start + consumed)
			self.esl_config_list.append(esl_config)
		return consumed

class RetryConfig:
	__head_fmt = "<HIBB12sB"
	def __init__(self):
		self.cmd = 0xFF00
		self.len = 0
		self.retry_times = 0
		self.retry_mode = 0 # 价签只要有一个数据包失败,就重传该价签的所有数据包.
		self.reserved = bytearray([0 for x in xrange(12)])
		self.num = 0
		self.group_config = []

	def __str__(self):
		_str_fmt = '''RetryConfig {
	cmd = 0x%04X
	len = %d
	retry_times = %d
	retry_mode = %d
	reserved = [%s]
	num = %d
	group_config = [
		%s
	]
}
'''
		gcstr = ''
		for gc in self.group_config:
			gcstr += indent_member(str(gc), 2)
		return _str_fmt % (self.cmd, self.len, self.retry_times, self.retry_mode, b2a_hex(self.reserved), self.num, gcstr)

	def calc_size(self):
		self.num = len(self.group_config)
		size = struct.calcsize(RetryConfig.__head_fmt)
		for gc in self.group_config:
			size += gc.calc_size()
		return size

	def encode(self, bytes):
		self.len = self.calc_size() - 2 - 4
		bytes.extend(struct.pack(RetryConfig.__head_fmt, self.cmd, self.len, self.retry_times, self.retry_mode, \
								 str(self.reserved), self.num))
		for i in xrange(self.num):
			self.group_config[i].encode(bytes)


class GroupFrame1Command:
	__head_fmt = "<HIHBBB8sH"

	def __init__(self):
		self.cmd = 0x0340  # uint16, 2bytes
		self.len = 0  # uint32, 4bytes
		self.bandrate = 0  # uint16, 2bytes
		self.power = 0  # uint8, 1byte
		self.duration = 0  # uint8, 1byte
		self.mode = 0  # uint8, 1byte
		self.reserved = bytearray([0 for x in xrange(8)])  # uint8[8], 8bytes
		self.n = 0  # uint16, 2bytes, 后面UnitData的个数
		self.data = []  # n * UnitData

	def __str__(self):
		_str_fmt = '''GroupFrame1 {
	cmd = 0x%04X
	len = %d
	bandrate = %d
	power = %d
	duration = %d
	mode = %d
	reserved = [%s]
	num = %d
	frame1_data = [
		%s
	]
}
'''
		f1str = ''
		for f1_data in self.data:
			f1str += indent_member(str(f1_data), 2)
		return _str_fmt % (self.cmd, self.len, self.bandrate, self.power, self.duration, self.mode,\
						   b2a_hex(self.reserved), self.n, f1str)

	def decode(self, bytes, start=0):
		consumed, (self.cmd, self.len, self.bandrate, self.power, self.duration, self.mode, self.reserved, self.n) = \
			unpack(GroupFrame1Command.__head_fmt, bytes, start)
		for i in xrange(self.n):
			unit_data = HTPv3UnitData()
			consumed += unit_data.decode(bytes, start + consumed)
			self.data.append(unit_data)
		return consumed

	def encode(self, bytes):
		self.n, data_len = 0, 0
		for data in self.data:
			self.n += 1
			data_len += data.calc_size()
		self.len = struct.calcsize(GroupFrame1Command.__head_fmt) - 2 - 4 + data_len

		bytes.extend(
			struct.pack(GroupFrame1Command.__head_fmt, self.cmd, self.len, self.bandrate, self.power, self.duration, \
						self.mode, str(self.reserved), self.n))
		for data in self.data:
			data.encode(bytes)

	def calc_size(self):
		size = struct.calcsize(GroupFrame1Command.__head_fmt)
		self.n = len(self.data)
		for data in self.data:
			size += data.calc_size()
		return size

class GroupDataCommand:
	__head_fmt = "<HI4sBHHBBBBB7sH"

	def __init__(self, protocol_version = HTP_VERSION_3):
		self.cmd = protocol_version  # uint16, 2bytes
		self.len = 0  # uint32, 4bytes
		self.master_id = bytearray([0 for x in xrange(4)])  # uint8[4], 4bytes
		self.power = 0  # uint8, 1byte
		self.tx_bandrate = 0  # uint16, 2bytes
		self.rx_bandrate = 0  # uint16, 2bytes
		self.esl_work_time = 0  # uint8, 1byte
		self.id_x_ctrl = 0  # uint8, 1byte
		self.mode = 0  # uint8, 1byte
		self.deal_duration = 0  # uint8, 1byte

		# 此值表示价签从接收完一包数据，到开启接收的时间，单位是毫秒
		# 0表示使用基站默认的值
		self.tx_interval = 0

		self.reserved = bytearray([0 for x in xrange(7)])  # uint8[8], 8bytes
		self.num = 0  # uint16, 2bytes
		self.esl_data = []  # n * UnitData

	def __str__(self):
		_str_fmt = '''GroupData {
	cmd = 0x%04X
	len = %d
	master_id = %s
	power = %d
	tx_bandrate = %d
	rx_bandrate = %d
	work_time = %d
	id_x_ctrl = %d
	mode = %d
	deal_duration = %d
	tx_interval = %d
	reserved = [%s]
	num = %d
	esl_data = [
		%s
	]
}
'''
		eslstr = ''
		for ed in self.esl_data:
			eslstr += indent_member(str(ed), 2)
		return _str_fmt % (self.cmd, self.len, id2str(self.master_id), self.power, self.tx_bandrate, self.rx_bandrate, \
						   self.esl_work_time, self.id_x_ctrl, self.mode, self.deal_duration, self.tx_interval, \
						   b2a_hex(self.reserved), self.num, eslstr)

	def decode(self, bytes, start=0):
		consumed, (self.cmd, self.len, self.master_id, self.power, self.tx_bandrate, self.rx_bandrate, \
				   self.esl_work_time, self.id_x_ctrl, self.mode, self.deal_duration, self.tx_interval, \
				   self.reserved, self.num) = \
			unpack(GroupDataCommand.__head_fmt, bytes, start)
		for i in xrange(self.num):
			unit_data = HTPv3UnitData()
			consumed += unit_data.decode(bytes, start + consumed)
			self.esl_data.append(unit_data)
		return consumed

	def encode(self, bytes):
		self.num, data_len = 0, 0
		for data in self.esl_data:
			self.num += 1
			data_len += data.calc_size()
		self.len = struct.calcsize(GroupDataCommand.__head_fmt) - 2 - 4 + data_len

		bytes.extend(struct.pack(GroupDataCommand.__head_fmt, self.cmd, self.len, str(self.master_id), self.power, \
								 self.tx_bandrate, self.rx_bandrate, self.esl_work_time, self.id_x_ctrl, self.mode, \
								 self.deal_duration, self.tx_interval, str(self.reserved), self.num))
		for data in self.esl_data:
			data.encode(bytes)

	def calc_size(self):
		size = struct.calcsize(GroupDataCommand.__head_fmt)
		for data in self.esl_data:
			size += data.calc_size()
		return size


class HTPv3Group1:
	__head_fmt = "<HI"

	def __init__(self):
		self.cmd = 0  # uint16, 2bytes
		self.len = 0  # uint32, 4bytes
		self.frame1 = GroupFrame1Command()
		self.data = GroupDataCommand()

	def decode(self, bytes, start=0):
		consumed, (self.cmd, self.len) = unpack(HTPv3Group1.__head_fmt, bytes, start)
		consumed += self.frame1.decode(bytes, start + consumed)
		consumed += self.data.decode(bytes, start + consumed)
		return consumed

	def encode(self, bytes):
		self.len = self.frame1.calc_size() + self.data.calc_size()
		bytes.extend(struct.pack(HTPv3Group1.__head_fmt, self.cmd, self.len))
		self.frame1.encode(bytes)
		self.data.encode(bytes)

class SetWakeupData:
	__data_fmt = "<4sBB6s"
	def __init__(self):
		self.wakeup_id = bytearray([0 for x in xrange(4)])
		self.channel = 0
		# Set Wakeup Data固定长度6bytes
		self.len = 6
		self.wakeup_frame_data = bytearray([0 for x in xrange(6)])

	def __str__(self):
		_str_fmt = '''SetWakeupData {
	wakeup_id = %s
	channel = %d
	len = %d
	wakeup_frame_data = [%s]
}
'''
		return _str_fmt % (id2str(self.wakeup_id), self.channel, self.len, b2a_hex(self.wakeup_frame_data))

	def calc_size(self):
		return struct.calcsize(SetWakeupData.__data_fmt)

	def encode(self, bytes):
		bytes.extend(struct.pack(SetWakeupData.__data_fmt, \
								 str(self.wakeup_id), self.channel, self.len, str(self.wakeup_frame_data)))

class SleepData:
	__data_fmt = '<4sBB'
	def __init__(self, eslid, chn):
		self.eslid = str2id(eslid) #bytearray([0 for x in xrange(4)])
		self.channel = chn
		self.len = 0
	
	def __str__(self):
		_str_fmt = '''SleepData {
	eslid = %s
	channel = %d
	len = %d
}
'''
		return _str_fmt % (id2str(self.eslid), self.channel, self.len)

	def calc_size(self):
		return struct.calcsize(SleepData.__data_fmt)

	def encode(self, bytes):
		bytes.extend(struct.pack(SleepData.__data_fmt, \
								 str(self.eslid), self.channel, self.len))

class GroupWakeupData:
	__data_fmt = "<4sBB2s"
	def __init__(self):
		self.group_id = bytearray([0 for x in xrange(4)]) # 4bytes, GROUP ID
		self.channel = 0 # 1byte
		self.len = 2 # 1byte

		# 2bytes
		# - 头3bits 101: Grp_wkup_pkg
		# - 后续13bits: 价签进入ESL Data transfer模式所需要的同步时间。时间单位为5ms。5~8192*5ms
		self.ctrl_and_slot = bytearray([0xA0, 0xA0]) # 3bits ctrl 固定101

	def __str__(self):
		_str_fmt = '''GroupWakeupData {
	group_id = %s
	channel = %d
	len = %d
	ctrl&slot = %s
}
'''
		return _str_fmt % (id2str(self.group_id), self.channel, self.len, b2a_hex(self.ctrl_and_slot))

	def calc_size(self):
		return struct.calcsize(GroupWakeupData.__data_fmt)

	def encode(self, bytes):
		self.len = 2
		bytes.extend(struct.pack(GroupWakeupData.__data_fmt, \
								 str(self.group_id), self.channel, self.len, str(self.ctrl_and_slot)))

class HTPv3GroupN:
	__head_fmt = "<HI"

	def __init__(self, protocol_version = HTP_VERSION_3):
		self.cmd = 0x0300  # uint16, 2bytes
		self.len = 0  # uint32, 4bytes
		self.group_wakeup = WakeupCommand()  # WakeupCommand
		self.frame1 = GroupFrame1Command()  # GroupFrame1Command
		self.sleep = SleepCommand()
		self.data = GroupDataCommand(protocol_version = HTP_VERSION_3)  # GroupDataCommand

	def __str__(self):
		_str_fmt = '''GroupN {
	cmd = 0x%04X
	len = %d
	sleep = %s
	group_wakeup = %s
	frame1 = %s
	group_data = [
		%s
	]
}
'''
		return _str_fmt % (self.cmd, self.len, \
						   indent_member(str(self.group_wakeup)), \
						   indent_member(str(self.frame1)), \
						   indent_member(str(self.sleep)), \
						   indent_member(str(self.data)))

	def encode(self, bytes):
		self.len = self.sleep.calc_size() + self.group_wakeup.calc_size() \
					+ self.frame1.calc_size() + self.data.calc_size()
		bytes.extend(struct.pack(HTPv3GroupN.__head_fmt, self.cmd, self.len))
		self.group_wakeup.encode(bytes)
		self.frame1.encode(bytes)
		self.sleep.encode(bytes)
		self.data.encode(bytes)


class HTPv3Head:
	default_version = "htp v3.0"
	__head_fmt = "<16s16s16s"

	def __init__(self):
		self.htp_version = HTPv3Head.default_version + str(
			bytearray([0 for x in range(16 - len(HTPv3Head.default_version))]))
		self.timestamp = time.strftime('%Y%m%d%H%M%S') + "\x00\x00"
		self.reserved = str(bytearray([0 for x in range(16)]))

	def decode(self, bytes, start=0):
		consumed, (self.htp_version, self.timestamp, self.reserved) = unpack(HTPv3Head.__head_fmt, bytes, start)
		return consumed

	def encode(self, bytes):
		bytes.extend(struct.pack(HTPv3Head.__head_fmt, self.htp_version, self.timestamp, self.reserved))

	def calc_size(self):
		return struct.calcsize(HTPv3Head.__head_fmt)

	def __str__(self):
		_str_fmt = '''HTPv3Head {
	version = "%s"
	stimestamp = "%s"
	reserved = "%s"
}
'''
		return _str_fmt % (self.htp_version, self.timestamp, self.reserved)

class HTPv3:
	def __init__(self):
		self.payload_id = 0
		self.size = 0

		self.head = HTPv3Head()
		
		self.protocol_version = HTP_VERSION_3
		self.set_wakeup = WakeupCommand()
		self.retry_config = RetryConfig()
		self.group1 = None
		self.normal_groups = []  # HTPv3GroupN[]

	def calc_size(self):
		size = self.head.calc_size()
		size += self.set_wakeup.calc_size()
		size += self.retry_config.calc_size()
		if self.group1:
			size += self.group1.calc_size()
		for gn in self.normal_groups:
			size += gn.calc_size()

	def __str__(self):
		_str_fmt = '''HTPv3 {
	payload_id = %d
	packet_length = %d

	head = %s
	retry_config = %s
	set_wakeup = %s
	normal_groups = [
		%s
	]
}

'''
		ngstr = ''
		for gn in self.normal_groups:
			ngstr += indent_member(str(gn), 2)
		return _str_fmt % (self.payload_id, self.size,
							indent_member(str(self.head)),
							indent_member(str(self.retry_config)),
							indent_member(str(self.set_wakeup)),
							ngstr)


	def encode(self):
		bytes = bytearray()
		bytes.extend(struct.pack("<II", self.payload_id, self.size))

		if self.head:
			self.head.encode(bytes)

		if self.set_wakeup:
			self.set_wakeup.encode(bytes)

		if self.retry_config:
			self.retry_config.encode(bytes)

		if self.group1:
			self.group1.encode(bytes)

		for group_n in self.normal_groups:
			group_n.encode(bytes)

		self.size = len(bytes) - 8
		bytes[4] = self.size & 0x000000FF
		bytes[5] = (self.size & 0x0000FF00) >> 8
		bytes[6] = (self.size & 0x00FF0000) >> 16
		bytes[7] = (self.size & 0xFF000000) >> 24
		return bytes


class AckData:
	__fmt = "<4sB"

	def __init__(self):
		self.esl_id = bytearray([0 for x in xrange(4)])
		self.code = 0

	def calc_size(self):
		return struct.calcsize(AckData.__fmt)

	def decode(self, bytes, start=0):
		consumed, (esl_id, self.code) = unpack(AckData.__fmt, bytes, start)
		self.esl_id = bytearray(esl_id)
		return consumed

	def encode(self, bytes):
		bytes.extend(struct.pack(AckData.__fmt, self.esl_id, self.code))

	def __str__(self):
		return id2str(self.esl_id) + ':' + str(self.code)

class HTPv3Ack:
	__fmt = "<HIB8sH"

	def __init__(self):
		self.head = HTPv3Head()
		self.cmd = 0x0900  # ack cmd	UINT16	2
		self.len = 0  # ack cmd len	UINT32	4
		self.para = 0  # PARA	UINT8	1
		self.reserved = bytearray([0 for x in xrange(8)])  # reversed	UINT8	8
		self.num = 0  # NUM	UINT16	2
		self.ack_list = []  # ACK area	x	X

	def decode(self, bytes, start=0):
		head_len = self.head.decode(bytes, start)
		consumed, (self.cmd, self.len, self.para, self.reserved, self.num) = unpack(HTPv3Ack.__fmt, bytes,
																					start + head_len)
		consumed += head_len
		for i in xrange(self.num):
			ack_data = AckData()
			consumed += ack_data.decode(bytes, start + consumed)
			self.ack_list.append(ack_data)
		return consumed

class Packet:
	__head_fmt = "<II"
	__head_length = struct.calcsize(__head_fmt)

	def __init__(self, session):
		self.session = session

		self.payload_id = 0
		self.packet_length = 0
		self.data = None

	def __str__(self):
		tostring = 'packet {\n'
		tostring += '  \"payload_id\": 0x%04X\n' % self.payload_id
		tostring += '  \"packet_length\": %d\n' % self.packet_length
		tostring += '  \"data\": %s\n' % b2a_hex(self.data)
		tostring += '}\n'
		return tostring

	def encode(self):
		data_len = len(self.data)
		self.packet_length = data_len
		whole_fmt = "%s%ds" % (self.__head_fmt, data_len)
		bytes = bytearray(struct.pack(whole_fmt, self.payload_id, self.packet_length, self.data))
		return bytes

	def decode(self, payload_id, packet_length, bytes):
		self.payload_id = payload_id
		self.packet_length = packet_length
		self.data = bytes[0: packet_length]
		return packet_length


class PacketFormatError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class Session:
	SEQUENCE = 0
	TL_fmt = "<II"
	TL_len = struct.calcsize(TL_fmt)

	def __init__(self, endpoint, connection):
		self.cid = Session.SEQUENCE
		Session.SEQUENCE += 1

		self.state_lock = threading.Lock()
		self.rw_lock = threading.Lock()

		self.state = "normal"
		self.authenticated = False
		self.endpoint = endpoint
		self.connection = connection
		self.peer_ip_addr = connection_ip_addr(connection)
		self.phase = "head"
		self.need_bytes = Session.TL_len
		self.buffer = bytearray()
		self.payload_id = 0
		self.packet_length = 0
		self.attributes = {}

	def __change_state(self, old, new):
		self.state_lock.acquire()
		try:
			if self.state == old:
				self.state = new
				return True
			else:
				return False
		finally:
			self.state_lock.release()

	def close(self):
		if self.__change_state("normal", "closed"):
			self.endpoint.request_close_session(self)

	def set_attr(self, dict):
		self.attributes.update(dict)

	def get_attr(self, key, default=None):
		try:
			return self.attributes[key]
		except KeyError:
			return default

	def __change_read_phase(self, name, n):
		self.phase = name
		self.need_bytes = n

	def __reset_read_phase(self):
		self.phase = "head"
		self.need_bytes = Session.TL_len
		self.payload_id = 0
		self.packet_length = 0

	def on_data_read(self, data):
		self.buffer.extend(data)
		packets = []

		while True:
			buffer_len = len(self.buffer)
			if buffer_len >= self.need_bytes:
				if self.phase == "head":
					self.payload_id, self.packet_length = struct.unpack(Session.TL_fmt, self.buffer[0: Session.TL_len])
					del self.buffer[0: Session.TL_len]
					self.__change_read_phase("body", self.packet_length)
				else:
					packet = Packet(self)
					consumed = packet.decode(self.payload_id, self.packet_length, self.buffer)
					del self.buffer[0: consumed]
					packets.append(packet)
					self.__reset_read_phase()
			else:
				break

		return packets

	def send_data(self, data):
		self.rw_lock.acquire()
		try:
			cnt, start, total = 0, 0, len(data)
			while start < total:
				_, writable, exceptional = select.select([], [self.connection], [self.connection], 5)
				if self.connection in exceptional:
					return False
				if not self.connection in writable:
					return False
				cnt = self.connection.send(data[start:])
				if cnt > 0:
					start += cnt
			return True
		except:
			return False
		finally:
			self.rw_lock.release()

class UDPEndpoint(threading.Thread):
	def __init__(self, connector, port):
		threading.Thread.__init__(self)
		self.connector = connector
		self.running = False
		self.sock = None
		self.port = port

	def start_listening(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', self.port))

	def __get_my_ip_address(self, peer_address):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect((peer_address[0], 1))
			addr = s.getsockname()[0]
			s.close()
			packedIP = socket.inet_aton(addr)
			return struct.unpack("<I", packedIP)[0]
		except:
			return None

	def run(self):
		self.running = True
		while self.running:
			try:
				readable, writable, exceptional = select.select([self.sock], [], [], 3)
				if len(readable) > 0:
					message, peer = self.sock.recvfrom(512)
					req = json.loads(str(message).replace('\0', ''))
					if "uid" in req:
						apid = self.connector.validate_ap_uid(req["uid"])
						my_ip = self.__get_my_ip_address(peer)
						if apid > 0 and my_ip:
							resp = bytearray()
							resp.extend(struct.pack("<IIII", 0, my_ip, self.port, apid))
							self.sock.sendto(resp, peer)
				elif len(exceptional) > 0:
					break
			except:
				pass
		self.sock.close()

	def stop_listening(self):
		self.running = False

class TCPEndpoint(threading.Thread):
	def __init__(self, connector, port):
		threading.Thread.__init__(self)
		self.state = "init"
		self.port = port
		self.connector = connector
		self.command_queue = Queue.Queue()
		self.server_socket = None

		# 已经建立的连接
		self.sessions = {}

		# 控制命令key及动作
		self.commands = {
			"closeSession": self.__close_session
		}

	def start_listening(self):
		assert self.state == "init", "TCPEndpoint hasn't been stopped."
		# 创建Server listening socket
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setblocking(False)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_address = ('', self.port)
		self.server_socket.bind(server_address)
		self.server_socket.listen(socket.SOMAXCONN)
		self.state = "listening"

	def __exec_command(self):
		while not self.command_queue.empty():
			try:
				command = self.command_queue.get_nowait()
				commandId = command["commandId"]
				if commandId == 'quit':
					return True

				action = self.commands[command["commandId"]]
				if action:
					action(command["arg"])
				else:
					log.warning("TCPEndpoint control command %s isn't been define." % commandId)
			except Queue.Empty, empty:
				break

		return False

	def run(self):
		assert self.state == "listening", "TCPEndpoint is not at listening state."
		self.state = "running"
		self.sessions[self.server_socket] = None
		while True:
			listening_list = self.sessions.keys()
			readable, writable, exceptional = select.select(listening_list, [], listening_list)
			if self.__exec_command():
				break

			for s in readable:
				if s is self.server_socket:
					connection, client_address = s.accept()
					connection.setblocking(0)
					self.sessions[connection] = Session(self, connection)
				else:
					try:
						data = s.recv(BUFFER_SIZE)
						if data:
							self.__recv_packet(s, data)
						else:
							# 连接断开
							self.__close_connection(s)
					except:
						self.__close_connection(s)

			for s in exceptional:
				self.__close_connection(s)

		# stop处理
		self.state = "stopping"
		for connection in self.sessions:
			if not connection is self.server_socket:
				connection.close()

		self.server_socket.close()
		self.sessions.clear()
		self.state = "init"

	def stop_listening(self):
		try:
			self.command_queue.put_nowait({"commandId": "quit", "arg": ''})
			self.__notify_self()
		except:
			pass

	def __notify_self(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ("127.0.0.1", self.port)
		sock.connect(server_address)
		sock.close()

	def request_close_session(self, session):
		try:
			self.command_queue.put_nowait({"commandId": "closeSession", "arg": session})
			self.__notify_self()
		except:
			pass

	def __recv_packet(self, s, data):
		if s in self.sessions:
			session = self.sessions[s]
		else:
			self.sessions[s] = session = Session(self, s)

		packets = session.on_data_read(data)
		if packets:
			self.connector.packet_received(packets)

	def __close_connection(self, connection):
		try:
			session = self.sessions.pop(connection)
			connection.close()
			self.connector.session_closed(session)
		except KeyError:
			pass

		return True

	def __close_session(self, session):
		return self.__close_connection(session.connection)


class InboundPacketProcessor(threading.Thread):
	zero_char = bytearray([0]).decode()
	__AP_SEQUENCE = 0

	def __init__(self, connector):
		threading.Thread.__init__(self)
		self.connector = connector
		self.sequence = 0
		self.thread = None
		self.xml_server = bind.get_xmlserver()

		self.__process = {
			PID_REQ_AP_AUTHENTICATE: self.__authenticate_ap,
			PID_REQ_AP_HEARTBEAT: self.__ap_heartbeat,
			PID_REQ_ESL_HEARTBEAT: self.__esl_heartbeat,
			PID_ACK_ESL_UPDATE: self.__htpv3_task_ack,
			PID_ACK_NETWORKING: self.__htpv3_task_ack,
			PID_ACK_ESL_QUERY: self.__htpv3_task_ack
		}

	def run(self):
		self.thread = threading.currentThread()
		while True:
			packet = self.connector.take_packet()
			if packet == "quit":
				break

			try:
				self.sequence += 1
				if packet.payload_id in self.__process:
					if packet.payload_id != PID_REQ_AP_AUTHENTICATE:  # AP Login之外的报文都要验证是否已经授权
						if not packet.session.authenticated:
							log.warning("received packet from unauthenticated session, peer=%s" % packet.session.peer_ip_addr)
							continue

					self.__process[packet.payload_id](packet)
				else:
					log.warning("undefined payload_id %02X." % packet.payload_id)
			except Exception, ex:
				log.warn("InboundPacketProcess error.\n%s\n%s" % (traceback.format_exc(), format_binary(packet.data)))

	def __strip_zero(self, *str_list):
		return_list = []
		for s in str_list:
			return_list.append(s.replace(InboundPacketProcessor.zero_char, ''))
		return tuple(return_list)

	def __rpc_ap_heartbeat(self, args):
		try:
			cmd = "AP_BEACOM"
			code, msg = self.xml_server.send_cmd(cmd, args)
			return code.upper() == "OK"
		except Exception, ex:
			log.debug("XML-RPC AP_BEACOM error, %s" % ex)
			return False

	def __authenticate_ap(self, request):
		session = request.session
		result_code = 0

		# 认证结果响应数据
		response = Packet(session)
		response.payload_id = PID_RSP_AP_AUTHENTICATE

		apid = 0
		if not session.authenticated:
			consumed, (uid, sn, version) = unpack("<128s32s32s", request.data)
			# 兼容协议更改, elinker不传desc时把desc设为空串.
			try:
				consumed, (desc_tuple) = unpack("1024s", request.data, consumed)
				desc = desc_tuple[0]
			except:
				desc = ''
			uid, sn, version, desc = self.__strip_zero(uid, sn, version, desc)
			apid = self.connector.validate_ap_uid(uid)
			ap_info = {
				"apid": apid,
				"apip": session.peer_ip_addr,
				"status": 0,
				"sn": sn,
				"version": version,
				"mac": uid,
				"desc": desc
			}
			rpc_args = ap_info.copy()
			rpc_args["apid"] = str(ap_info["apid"])
			rpc_args["status"] = "0"
			if apid <= 0:
				log.warning("received AP authentication request from unknown UID(%s)." % uid)
				result_code = 0x01  # 认证失败, uid不在ACL中
			else:
				if not standalone:
					if not self.__rpc_ap_heartbeat([rpc_args]):
						result_code = 0x05 # 服务暂停
					else:
						result_code = 0x00
				else:
					result_code = 0x00

				if result_code == 0:
					session.authenticated = True
					session.set_attr(ap_info)
					self.connector.session_authenticated(session)
				else:
					session.close()
		else:
			apid = session.get_attr("apid")

		output_fmt = "<II20s"
		response.data = struct.pack(output_fmt, apid, result_code, time.strftime('%Y-%m-%d %H:%M:%S'))
		# 发送响应
		bytes = response.encode()
		session.send_data(bytes)

	def __ap_heartbeat(self, request):
		# apid: AP ID, 33bytes ascii string
		# hb_id: heartbeat ID, 1byte
		# body: 33bytes, no use
		try:
			input_fmt = "<II"
			apid, status = struct.unpack(input_fmt, request.data)
			ap = self.connector.get_ap(apid)
			ap_info = ap.session.attributes
			ap_info["status"] = status
			rpc_args = ap_info.copy()
			rpc_args["apid"] = str(ap_info["apid"])
			rpc_args["status"] = "0"
			self.__rpc_ap_heartbeat([rpc_args])
		except Exception, ex:
			log.warn("process AP heartbeat error. ")

	def __esl_heartbeat(self, request):
		# uint16 num个数
		# num个17字节的心跳信息
		head_len, (head) = unpack("<H", request.data)
		num = head[0]
		# CTRL&VERSION: 共用2bytes，其中CTRL=bit[0:4], VERSION=bit[4:16]
		# set_wakeup_id: set唤醒ID，3bytes，使用时转换为字符串"59-AA-BB"格式
		# esl_id: ESL ID， 4bytes，使用时转换为字符串"5x-xx-xx-xx"格式
		# set_wakeup_channel: set唤醒信道，1byte
		# group_wakeup_channel: group唤醒信道，1byte
		# data_channel: 数据通信信道，1 byte
		# esl_netid: ESL子网号， 1byte
		# esl_information: 心跳帧价签上传信息， 1byte
		# CRC: 以上所有数据的CRC值
		# rfpower: 能量值,由AP子板获得,附加在价签心跳数据后面上传.
		session = request.session
		start = head_len
		esl_hb_list = []
		for i in xrange(num):
			consumed, (ctrl0, ctrl1) = unpack("<BB", request.data, start)  # 先读两个字节的ctrl
			start += consumed
			if ctrl0 & 0xF0 == 0xC0:  # 二代价签心跳信息
				consumed, (ignore) = unpack("<15s", request.data, start)
			else:  # 三代价签心跳信息
				consumed, (set_wakeup_id, esl_id, set_wakeup_channel, group_wakeup_channel,
						   data_channel, esl_netid, esl_information, CRC, rfpower) = unpack("3s4sBBBBB2sB",
																							request.data, start)
				set_wakeup_id = bytearray(set_wakeup_id)
				esl_id = bytearray(esl_id)
				esl_hb = {}
				esl_hb["eslid"] = "%02X-%02X-%02X-%02X" % tuple(esl_id[0: 4])
				esl_hb["setchn"] = str(set_wakeup_channel)
				esl_hb["grpchn"] = str(group_wakeup_channel)
				esl_hb["apid"] = str(session.get_attr("apid"))
				esl_hb["nw1"] = "%02X-%02X-%02X" % tuple(set_wakeup_id[0: 3])
				esl_hb["nw3"] = str(data_channel)
				esl_hb["rfpower"] = str(rfpower)  # 能量值
				esl_hb["netid"] = str(esl_netid)
				esl_hb["version"] = str(((ctrl0 & 0x0F) << 8) | ctrl1)
				esl_hb["battery"] = str(esl_information)  # 最小电量1.9v
				esl_hb["reserve"] = str(0)
				esl_hb_list.append(esl_hb)
			start += consumed

		if not is_empty(esl_hb_list):
			hb_once = "DATASTART51000%s0X0000DATAEND" % json.dumps(esl_hb_list)
			self.connector.esl_heartbeat_queue.put_nowait(hb_once)

	def __htpv3_task_ack(self, packet):
		htp_ack = HTPv3Ack()
		htp_ack.decode(packet.data, 0)
		apid = packet.session.get_attr("apid")
		ap = self.connector.get_ap(apid)
		ap.commit_task(htp_ack)

class APv3:
	def __init__(self, session, apid, uid):
		self.apid = apid
		self.uid = uid
		self.peer_ip_addr = session.peer_ip_addr
		self.session = session

		self.data_ready = threading.Condition()
		self.task_data = {}
		self.task_lock = threading.Lock()
		self.total_members = 0
		self.current_task_id = ""
		self.total_packet_num = 0

	def __str__(self):
		return "AP(%s, %s, %s, %s)" % (self.apid, self.uid, self.peer_ip_addr, "connected" if self.session else "disconnection")

	def is_connected(self):
		return True if self.session else False

	def cancelTask(self):
		if not self.task_lock.acquire(0):
			for i in xrange(self.total_members):
				queue = self.task_data[i]["ack_queue"]
				queue.put_nowait([])

	def __save_data(self, num, record):
		queue = Queue.Queue()
		self.task_data[num] = record
		self.task_data[num]["ack_queue"] = queue
		return queue

	def __task_owner(self, total, num, record):
		self.__clear()
		self.total_members = total
		self.data_ready.acquire()
		try:
			queue = self.__save_data(num, record)
			begin_waiting_time = time.time()
			while True:
				if len(self.task_data) >= self.total_members:
					return True, True, queue, None
				self.data_ready.wait(timeout=TIMEOUT_HTPv3_TASK_PARTICIPANT_SUBMIT_DATA)
				if len(self.task_data) >= self.total_members:
					return True, True, queue, None
				elif time.time() - begin_waiting_time > 60:
					self.__clear()
					self.task_lock.release()
					err_msg = "waiting HTPv3 task participant timeout!"
					return False, False, None, err_msg
		finally:
			self.data_ready.release()

	def __task_participant(self, total, num, record):
		if total != self.total_members:
			err_msg = "total data number(%d) of task participant is not equals to owners(%d)." \
					  % (total, self.total_members)
			return False, False, None, err_msg
		elif num in self.task_data:
			err_msg = "data of HTPv3 task participant %d has already submitted before." % num
			return False, False, None, err_msg

		self.data_ready.acquire()
		try:
			queue = self.__save_data(num, record)
			self.data_ready.notify()
			return True, False, queue, None
		finally:
			self.data_ready.release()

	def begin_task(self, total, num, record):
		if self.current_task_id != "":
			return False, False, None, "AP received new task when busying"

		is_taks_owner = self.task_lock.acquire(0)
		if is_taks_owner:
			return self.__task_owner(total, num, record)
		else:
			return self.__task_participant(total, num, record)

	def __grouping_ack_list(self, ack_list):
		grouped_ack = {}
		if is_empty(ack_list):
			for pid in self.task_data:
				grouped_ack[pid] = []
			return grouped_ack

		index = 0
		total_ack_num = len(ack_list)
		if self.total_packet_num != total_ack_num:
			log.warn("task sent esl packets number %d is not equals to ACK number %d." % \
					 (self.total_packet_num, total_ack_num))

		last_esl_id = ''
		packet_num = 0
		for pid in xrange(self.total_members):
			grouped_ack[pid] = []
			for packet in self.task_data[pid].get("packets", []):
				esl_id = packet.data_id
				str_esl_id = id2str(esl_id)
				if str_esl_id != last_esl_id:
					packet_num = 0
					last_esl_id = str_esl_id

				if index < total_ack_num:
					ack_code = ack_list[index].code
				else:
					ack_code = 0
				grouped_ack[pid].append((str(self.apid), str_esl_id, packet_num, ack_code))
				index += 1
				packet_num += 1

		return grouped_ack

	def commit_task(self, htp_ack):
		if htp_ack.head.timestamp != self.current_task_id:
			log.warn("HTPv3 ack task_id[%s] not equals to sent task_id [%s]" % (htp_ack.head.timestamp, self.current_task_id))
			return
		else:
			self.__end_task(htp_ack.ack_list)

	def __end_task(self, ack_list):
		try:
			grouped_ack = self.__grouping_ack_list(ack_list)
			for pid in grouped_ack:
				queue = self.task_data[pid]["ack_queue"]
				queue.put_nowait(grouped_ack[pid])
		finally:
			self.__clear()

		try:
			self.task_lock.release()
		except:
			pass

	def cancel_task(self):
		self.__end_task([])

	def offline(self):
		self.cancel_task()
		self.session = None

	def __clear(self):
		for pid in self.task_data:
			queue = self.task_data[pid]["ack_queue"]
			queue.put_nowait([])

		self.task_data.clear()
		self.total_members = 0
		self.total_packet_num = 0
		self.current_task_id = ""

	def __convert_task_data(self, pid, channel, index):
		v2_data = HTPv2UnitData()
		v2_packets = self.task_data[pid]["data_area"]
		self.task_data[pid]["packets"] = []
		start = 0
		sequence = 0
		count = len(v2_packets) / (4 + 4 + 26)
		for x in xrange(count):
			start += v2_data.decode(v2_packets, start)
			v3_data = HTPv3UnitData()
			v3_data.data_id = v2_data.data_id
			v3_data.channel = channel
			v3_data.len = v2_data.len
			v3_data.data = bytearray(v2_data.data)
			v3_data.sequence = sequence
			v3_data.index = index + sequence
			sequence += 1
			self.task_data[pid]["packets"].append(v3_data)
		return sequence

	def __count_total_packet_num(self):
		count = 0
		for pid in xrange(self.total_members):
			v2_packets = self.task_data[pid]["data_area"]
			count += len(v2_packets) / (4 + 4 + 26)
		self.total_packet_num = count

	def __create_htpv3(self):
		htp = HTPv3()
		htp.payload_id = PID_REQ_ESL_UPDATE # 固定为update
		helper = None
		htp.retry_config.retry_times = 3
		htp.retry_config.retry_mode = 0
		self.__count_total_packet_num()
		index = 0

		# htp_para['grpchn'] 为 group唤醒信道，htp_para['channel'] 为数据通讯信道，htp_para['setchn'] 为set唤醒信道，
		# htp_para['setid'] 为带横杆的11位set唤醒id，htp_para['wakeupid-str']为11位的group唤醒ID
		for pid in xrange(self.total_members):
			eslid_list = self.task_data[pid]["eslid_list"]
			if not eslid_list:  # eslid_list为None
				continue
			elif len(eslid_list) == 0:  # 该组没有价签
				continue

			helper = self.task_data[pid]["helper"]
			eslid_info = self.task_data[pid]["eslid_info"]
			group_id = self.task_data[pid]["group_id"]
			tx_power = get_value(helper, 'rf_tx_power', 2)

			#######################################################################
			# Failed Packets Retry Config
			group_config = GroupConfig()
			htp.retry_config.group_config.append(group_config)
			group_config.group_id = group_id
			group_config.group_channel = int(helper['channel'])
			group_config.num = len(eslid_list)
			str_group_id = id2str(group_id)
			for esl_id in eslid_info:
				if  str_group_id == eslid_info[esl_id]["nw1"]:
					esl_config = EslConfig()
					esl_config.esl_id = str2id(esl_id)
					esl_config.net_id = int(eslid_info[esl_id]["op2"])
					group_config.esl_config_list.append(esl_config)

			#######################################################################
			# Every Group
			htp.protocol_version = get_version(eslid_info[eslid_list[0]]['op3'])
			group_n = HTPv3GroupN(protocol_version = htp.protocol_version)
			htp.normal_groups.append(group_n)

			group_n.group_wakeup.data = GroupWakeupData()
			group_n.group_wakeup.bandrate = 500
			group_n.group_wakeup.power = tx_power
			group_n.group_wakeup.duration = helper["wakeuptime"]
			group_n.group_wakeup.slot_duration = int(helper['wk0_slot'])
			group_n.group_wakeup.data.group_id = group_id
			group_n.group_wakeup.data.channel = int(helper['grpchn'])

			group_n.frame1.bandrate = helper.get("mastersendbps", 500)
			group_n.frame1.power = tx_power
			group_n.frame1.duration = 20
			group_n.frame1.mode = 0
			group_n.frame1.n = 1

			# helper["grp_wk_frame1"] -> 4B wakeupid + 4B length + 26Bdata
			grp_wk_frame1 = bytearray(helper["grp_wk_frame1"])
			f1_data = HTPv3UnitData()
			f1_data.data_id = grp_wk_frame1[0: 4]
			f1_data.channel = int(helper['grpchn'])
			f1_data.len = 26
			f1_data.data = grp_wk_frame1[8: 8 + 26]
			# esl_comm_channel = f1_data.data[1] # frame1 data的offset[1]字节是价签通信信道
			group_n.frame1.data.append(f1_data)
			
			#sleep data
			group_n.sleep.bandrate = 500
			group_n.sleep.power = tx_power
			group_n.sleep.mode = 0
			group_n.sleep.interval = 0 #sleep帧间隔
			group_n.sleep.idxctrl = int(helper['sleepid_ctrl'])
			group_n.sleep.times = 1
			group_n.sleep.framelen = int(helper['framelen'])
			group_n.sleep.sleepn = len(helper["sleepids"])
			for id1 in helper["sleepids"]:
				chn = int(helper['channel'])
				group_n.sleep.data_list.append(SleepData(id1, chn))

			group_n.data.master_id = get_id_by_num(helper["masterid"], 4)
			group_n.data.power = tx_power
			group_n.data.tx_bandrate = 500
			group_n.data.rx_bandrate = helper["masterrecvbps"]
			group_n.data.esl_work_time = helper["worktime"]
			group_n.data.id_x_ctrl = helper["sleepid_ctrl"]
			group_n.data.mode = 1
			# group_n.data.deal_duration = helper["framerecvtimeout"]
			group_n.data.deal_duration = int(helper['query_timeout'])
			group_n.data.tx_interval = int(0.75*int(helper['dummy_frame']))

			index += self.__convert_task_data(pid, int(helper['channel']), index)
			packets = self.task_data[pid]["packets"]
			group_n.data.num = len(packets)
			for packet in packets:
				group_n.data.esl_data.append(packet)

		#修正重试次数，一二代协议，不需要基站内部进行重试, 且不需要SET命令
		if htp.protocol_version != HTP_VERSION_3:
			htp.retry_config.retry_times = 0

		#######################################################################
		# Set Wakeup
		if self.total_packet_num <= 0:
			return htp #异常情况，一个数据包都没有生成

		try:
			if helper["is_set_cmd"] == True:
				htp.set_wakeup.cmd = 0x0120 # global Setting
				htp.retry_config.retry_times = 0 # global Setting时不需要重传
			else:
				htp.set_wakeup.cmd = 0x0110 # global TRN
		except:
			htp.set_wakeup.cmd = 0x0110 # global TRN

		htp.set_wakeup.bandrate = 500
		if htp.protocol_version != HTP_VERSION_3:
			htp.set_wakeup.duration = 1
		else:
			htp.set_wakeup.duration = helper["set_wkup_time"]
		htp.set_wakeup.power = tx_power
		htp.set_wakeup.slot_duration = 10
		htp.set_wakeup.data = set_wakeup_data = SetWakeupData()
		# config["set_wk_frame"]: 4B set wakeup id + 1B channel + 1B set wakeup time + 1B frame length + 6Bframe contents
		set_wk_frame = bytearray(helper["set_wk_frame"])
		set_wakeup_data.wakeup_id = set_wk_frame[0: 4]
		set_wakeup_data.channel = int(helper['setchn'])
		set_wakeup_data.wakeup_frame_data = set_wk_frame[7: 13]
		return htp

	def send_task(self):
		htp = self.__create_htpv3()
		if not htp:
			return False

		htp_data = htp.encode()
		log.debug(str(htp).replace('\t', '    '))
		self.current_task_id = htp.head.timestamp
		group_tx_time = 0
		if self.session.send_data(htp_data):
			for grp in htp.normal_groups:
				group_tx_time += grp.group_wakeup.duration + grp.data.esl_work_time
			waiting_time = htp.set_wakeup.duration + group_tx_time * (1 + htp.retry_config.retry_times)
			return waiting_time * 2
		else:
			return -1

class APv3Connector:
	def __init__(self, esl_heartbeat_queue):
		self.config = Config()
		self.port = LISTENING_PORT
		self.esl_heartbeat_queue = esl_heartbeat_queue
		self.inbound_queue = Queue.Queue()
		self.thread_tcp_endpoint = None
		self.thread_udp_endpoint = None
		self.inbound_packet_processors = []
		self.active_ap_list = {}
		self.lock = threading.Lock()

	def start(self):
		self.config.load("config/htpv3.ini")
		self.__start_tcp_endpoint()
		self.__start_udp_endpoint()
		self.__start_inbound_packet_processor()
		log.info("APv3Connector started, listening on port %d.", self.port)

	def __start_tcp_endpoint(self):
		self.thread_tcp_endpoint = TCPEndpoint(self, self.port)
		self.thread_tcp_endpoint.start_listening()
		self.thread_tcp_endpoint.start()

	def __start_udp_endpoint(self):
		self.thread_udp_endpoint = UDPEndpoint(self, self.port)
		self.thread_udp_endpoint.start_listening()
		self.thread_udp_endpoint.start()

	def __stop_tcp_endpoint(self):
		self.thread_tcp_endpoint.stop_listening()
		self.thread_tcp_endpoint.join()
		self.thread_tcp_endpoint = None

	def __stop_udp_endpoint(self):
		self.thread_udp_endpoint.stop_listening()
		self.thread_udp_endpoint.join()
		self.thread_udp_endpoint = None

	def __start_inbound_packet_processor(self):
		for i in xrange(0, INBOUND_PACKET_PROCESSORS_NUM):
			processor = InboundPacketProcessor(self)
			self.inbound_packet_processors.append(processor)
			processor.start()

	def __stop_inbound_packet_processor(self):
		for i in xrange(0, INBOUND_PACKET_PROCESSORS_NUM):
			self.inbound_queue.put_nowait("quit")

		for processor in self.inbound_packet_processors:
			processor.join()

		del self.inbound_packet_processors[:]

	def stop(self):
		self.__stop_tcp_endpoint()
		self.__stop_udp_endpoint()
		self.__stop_inbound_packet_processor()
		self.__clear_inbound_queue()
		for apid in self.active_ap_list:
			ap = self.active_ap_list[apid]
			ap.cancelTask()

		log.info("APv3Connector stopped.")

	def session_created(self, session):
		pass

	def session_authenticated(self, session):
		self.lock.acquire()
		try:
			apid = session.get_attr("apid")
			uid = session.get_attr("uid")
			if apid in self.active_ap_list:
				ap = self.active_ap_list[apid]
				ap.session = session
			else:
				self.active_ap_list[apid] = APv3(session, apid, uid)
		except Exception:
			log.warn("create active AP record error.\n" + traceback.format_exc())
			session.close()
		finally:
			self.lock.release()

	def validate_ap_uid(self, uid):
		mac = uid.strip()
		if len(mac) == 0:
			return 0

		mac = mac.upper().replace(':', '_')
		apid = -1
		str_apid = self.config.get("authenticated_ap_list", mac, "null")
		if str_apid != "null":
			try:
				apid = int(str_apid)
			except:
				return -1

		if apid > 0:
			return apid

		self.config.lock.acquire()
		try:
			all_ap = self.config.get_options("authenticated_ap_list")
			apid = len(all_ap) + 1
			self.config.set("authenticated_ap_list", mac, str(apid))
			self.config.save()
			return apid
		finally:
			self.config.lock.release()

	def get_ap(self, apid):
		self.lock.acquire()
		try:
			return self.active_ap_list[apid] if apid in self.active_ap_list else None
		finally:
			self.lock.release()

	def session_closed(self, session):
		self.lock.acquire()
		try:
			apid = session.get_attr("apid")
			ap = self.active_ap_list[apid]
			bind_session = ap.session
			# 缺陷#1410
			# 以太网路由器断电后重启路由器, elinker重新建立连接并登陆授权会先于老TCP连接中断的事件发生,
			# 此时如果不判断session.cid 与 中断的connection对应的session.cid是否为同一个,就调用ap.offline()的话,
			# 会把已经建立的连接又重新关闭一次,导致AP状态为离线.
			if session.cid == bind_session.cid:
				ap.offline()
		finally:
			self.lock.release()

	def packet_received(self, packets):
		try:
			for p in packets:
				self.inbound_queue.put_nowait(p)
		except Queue.Full:
			log.warn("APv3Connector inbound queue is full.")

	def take_packet(self):
		return self.inbound_queue.get()

	def __clear_inbound_queue(self):
		while not self.inbound_queue.empty():
			try:
				self.inbound_queue.get_nowait()
			except Queue.Empty, empty:
				break

	def __do_htp_task(self, task_id, task_num, db, ap, h, data_area, eslid_list, eslid_info):
		ok, owner, queue, err_msg = ap.begin_task(task_num, task_id, {
			"group_id": get_id_by_num(h["wakeupid"], 4),
			"data_area": data_area,
			"helper": h,
			"db": db,
			"eslid_list": eslid_list,
			"eslid_info": eslid_info})

		if not ok:
			return [], err_msg

		if owner:
			waiting_time = ap.send_task()
			if waiting_time <= 0:
				raise IOError, "send task to AP failed."
			else:
				try:
					ack = queue.get(True, waiting_time)
					return ack, None
				except:
					return [], "waiting ACK timeout"
		else:
			return queue.get(), None

	def htp_start(self, task_id, task_num, db, apid_str, h, data_area, eslid_list, eslid_info):
		'''
		以HTPv3协议与AP通信,每一个group调用一次.
		:param task_id: 当前基站任务编号
		:param task_num: 当前基站总任务数。如果task_id等于1，task_num等于4，则表示此次通讯此基站共有4个任务，当前的任务为第1个（任务编号从0开始)
		:param db: 数据库对象，可以通过其操作db.sqlite3数据库，数据库对象的方法集见database.py，不允许通过db执行原始的sql语句
		:param apid_str: 基站号码, string
		:param h: 适合于当前价签分组的通讯层参数，包括setid, set唤醒时间，链路层查询超时时间等各个控制值，大部分参数来至config/htp_config.ini文件
		:param data_area: 当前分组价签的数据帧集合，格式为 4B id ＋ 4B len ＋ 26B 数据
		:param eslid_list: 此次group通讯涉及到的价签清单，格式为 ["55-11-22-99",...]。
		:param eslid_info: 价签的属性字典，格式为 {"55-11-22-99":{"eslid":"55-11-22-99", "op2":"4", "n21":"55-00-11-66",...}, ...}
		:return: [(apid, eslid, package num, ack)]
		'''
		# h["wakeupid"]是group id
		# h["channel"] 是group的channel
		apid = int(apid_str)
		if not apid in self.active_ap_list:
			return "[]", "htp_start(): not existed apid %d." % apid
		elif task_id < 0 or task_num <= 0:  # or not data_area or not eslid_list or not eslid_info:
			return "[]", "htp_start(): task_id or task_num error."
		# elif len(data_area) == 0 or len(eslid_list) == 0 or len(eslid_info) == 0:
		# 	return "[]", "htp_start(): collection arguments is empty."
		else:
			ap = self.active_ap_list[apid]
			if not ap.is_connected():
				return "[]", "htp_start(): specified AP(%d) is not connected." % apid

		try:
			ack, error_msg = self.__do_htp_task(task_id, task_num, db, ap, h, data_area, eslid_list, eslid_info)
			if error_msg:
				ap.cancel_task()
				return "[]", error_msg
			else:
				return str(ack), None
		except:
			ap.cancel_task()
			error_msg = traceback.format_exc()
			log.warn("APv3Connector send HTPv3 task data failed.\n%s", error_msg)
			return "[]", error_msg

	def send_update_data(self):
		payload = bytearray()
		# payload.extend(struct.pack("<II", 8, len(test_data)))
		for k in self.active_ap_list:
			if self.active_ap_list[k].session:
				session = self.active_ap_list[k].session
				session.send_data(payload)
				# session.send_data(test_data)
				print "test_data sent."

########################################################################################################################
# from test_data import test_data
htp_update = bytearray()

def __main__():
	global standalone
	standalone = True
	server = APv3Connector(Queue.Queue())
	server.start()
	cmd_line(server)
	server.stop()


def cmd_line(connector):
	actions = {
		"exit": lambda x: (x.stop(), sys.exit(0)),
		"stop": lambda x: x.stop(),
		"start": lambda x: x.start(),
		"ap": lambda x: [str(x.active_ap_list[k]) for k in x.active_ap_list],
		"update": lambda x: x.send_update_data()
	}

	while True:
		cmd = raw_input(">> ")
		cmd.strip()
		if len(cmd) == 0:
			continue

		try:
			action = actions[cmd]
			ret = action(connector)
			if ret:
				print ret
		except KeyError:
			print >> sys.stderr, "unknown command \"%s\"" % cmd


if __name__ == "__main__":
	# print len(test_data)
	__main__()
