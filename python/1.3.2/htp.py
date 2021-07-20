# encoding: utf-8

from esl_init import conf,log,print_except
import esl_init, api20
from socket import htonl
import struct, subprocess, platform
from struct import  pack as P
from struct import  unpack_from as U
from database import DB
import datetime, time, random, os
from dot_temp import get_seg_json
from copy import deepcopy

crc16tab = [
		0x0000,0x1021,0x2042,0x3063,0x4084,0x50a5,0x60c6,0x70e7,
		0x8108,0x9129,0xa14a,0xb16b,0xc18c,0xd1ad,0xe1ce,0xf1ef,
		0x1231,0x0210,0x3273,0x2252,0x52b5,0x4294,0x72f7,0x62d6,
		0x9339,0x8318,0xb37b,0xa35a,0xd3bd,0xc39c,0xf3ff,0xe3de,
		0x2462,0x3443,0x0420,0x1401,0x64e6,0x74c7,0x44a4,0x5485,
		0xa56a,0xb54b,0x8528,0x9509,0xe5ee,0xf5cf,0xc5ac,0xd58d,
		0x3653,0x2672,0x1611,0x0630,0x76d7,0x66f6,0x5695,0x46b4,
		0xb75b,0xa77a,0x9719,0x8738,0xf7df,0xe7fe,0xd79d,0xc7bc,
		0x48c4,0x58e5,0x6886,0x78a7,0x0840,0x1861,0x2802,0x3823,
		0xc9cc,0xd9ed,0xe98e,0xf9af,0x8948,0x9969,0xa90a,0xb92b,
		0x5af5,0x4ad4,0x7ab7,0x6a96,0x1a71,0x0a50,0x3a33,0x2a12,
		0xdbfd,0xcbdc,0xfbbf,0xeb9e,0x9b79,0x8b58,0xbb3b,0xab1a,
		0x6ca6,0x7c87,0x4ce4,0x5cc5,0x2c22,0x3c03,0x0c60,0x1c41,
		0xedae,0xfd8f,0xcdec,0xddcd,0xad2a,0xbd0b,0x8d68,0x9d49,
		0x7e97,0x6eb6,0x5ed5,0x4ef4,0x3e13,0x2e32,0x1e51,0x0e70,
		0xff9f,0xefbe,0xdfdd,0xcffc,0xbf1b,0xaf3a,0x9f59,0x8f78,
		0x9188,0x81a9,0xb1ca,0xa1eb,0xd10c,0xc12d,0xf14e,0xe16f,
		0x1080,0x00a1,0x30c2,0x20e3,0x5004,0x4025,0x7046,0x6067,
		0x83b9,0x9398,0xa3fb,0xb3da,0xc33d,0xd31c,0xe37f,0xf35e,
		0x02b1,0x1290,0x22f3,0x32d2,0x4235,0x5214,0x6277,0x7256,
		0xb5ea,0xa5cb,0x95a8,0x8589,0xf56e,0xe54f,0xd52c,0xc50d,
		0x34e2,0x24c3,0x14a0,0x0481,0x7466,0x6447,0x5424,0x4405,
		0xa7db,0xb7fa,0x8799,0x97b8,0xe75f,0xf77e,0xc71d,0xd73c,
		0x26d3,0x36f2,0x0691,0x16b0,0x6657,0x7676,0x4615,0x5634,
		0xd94c,0xc96d,0xf90e,0xe92f,0x99c8,0x89e9,0xb98a,0xa9ab,
		0x5844,0x4865,0x7806,0x6827,0x18c0,0x08e1,0x3882,0x28a3,
		0xcb7d,0xdb5c,0xeb3f,0xfb1e,0x8bf9,0x9bd8,0xabbb,0xbb9a,
		0x4a75,0x5a54,0x6a37,0x7a16,0x0af1,0x1ad0,0x2ab3,0x3a92,
		0xfd2e,0xed0f,0xdd6c,0xcd4d,0xbdaa,0xad8b,0x9de8,0x8dc9,
		0x7c26,0x6c07,0x5c64,0x4c45,0x3ca2,0x2c83,0x1ce0,0x0cc1,
		0xef1f,0xff3e,0xcf5d,0xdf7c,0xaf9b,0xbfba,0x8fd9,0x9ff8,
		0x6e17,0x7e36,0x4e55,0x5e74,0x2e93,0x3eb2,0x0ed1,0x1ef0
]

def is_osd_ack(ret):
	(_, _, _, cmd) = ret
	return True if "OSD" in cmd else False

OSD_FINISHED_NUMBER = 0xFFFF

def is_osd_ack_finished(ret):
	(_, n, _, cmd) = ret
	return True if (n == OSD_FINISHED_NUMBER and "OSD" in cmd) else False

def ack_failed():
	return (None, 0, 0, "NORMAL")

def set_apid_to_ack(ack, ap1):
	apid, n, val, cmd = ack
	return (ap1, n, val, cmd)

def get_apid_from_ack(ack):
	apid, n, val, cmd = ack
	return apid

def ack_ok_osd(ack1):
	'''只在解析OSD的ack使用'''
	(_, _, ack, cmd) = ack1
	if (\
			((ack & 0xF0) >> 4) == 0x1 or (ack & 0x0F) == 0x1 \
			or (ack & 0x0F) == 0x2 or ((ack & 0xF0) >> 4) == 0x2\
		) and cmd == 'OSD':
		return True
	return False

def ack_ok(ack1):
	(_, _, ack, cmd) = ack1
	if (((ack & 0xF0) >> 4) == 0x1 or (ack & 0x0F) == 0x1) and not is_osd_ack(ack1):
		return True
	return False

def ack_low_power(ack1):
	(_, _, ack, cmd) = ack1
	if (((ack & 0xf0) >> 4) == 0x2 or (ack & 0x0F) == 0x2)  and not is_osd_ack(ack1):
		return True
	return False

def check_real_low_power(ids, ret1, low_power_counter, lowpower_warning):
	apid, n, ret, cmd = ret1
	if ret == 0: #没有结果，或者结果不可期望：
		return ret1

	if ack_ok(ret1): #通讯正常
		low_power_counter[ids] = 0 #清零
		return ret1
	
	if not ack_low_power(ret1):
		return ret1

	if ids not in low_power_counter:
		low_power_counter[ids] = 0
	else:
		low_power_counter[ids] += 1

	esl_init.log.debug("%s low power count:%s" % (ids, low_power_counter[ids]))
	if low_power_counter[ids] < lowpower_warning: 
		return (apid, n, 0x1, cmd)	#5次以内，返回正常
	
	if lowpower_warning == -1:
		return (apid, n, 0x1, cmd) #不再返回低电量
	return (apid, n, 0x2, cmd) #返回低电量

def get_nw4_val(db, id1):
	'''从数据库中获取nw4字段的字符串值, 返回结果为“NORMAL”，“DOT20” '''
	return db.get(id1)['nw4']

def get_exe_file(exe):
	exe_name = exe +'_' + platform.system()
	if platform.architecture()[0] == '32bit' or platform.system() == 'Windows':
		exe_name += '_32'
	else:
		exe_name += '_64'

	if platform.system() == 'Windows':
		exe_name += '.exe'
	try:
		import stat
		if not os.access(exe_name,os.X_OK):
			f_mode = os.stat(exe_name).st_mode			
			os.chmod(exe_name, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IMODE(f_mode))
	except Exception,e:
		log.error_msg("%s : %s"%(exe_name ,e), errid='EHT001')
	return exe_name

def check_htp_config(args):
	if args > 255:
		args = 255
	elif args < 0:
		args = 0
	return args

def my_cal_crc16(crc ,ptr, lengh):
	for counter in range(lengh):
		value = U('B',ptr,counter)[0]
#		print 'value',value
		crc = ((crc<<8)%65536 ^ crc16tab[((crc>>8)%65536 ^ value )])%65536
#	s = str(hex(crc))[2:]
#	s = '0'*(4-len(s)) + s #自动补0

#	return s[2:]+s[0:2]
	return crc


def fill_netmask(h, db,ids,length):
# ids --> [u'5A-11-CD-99',u'5A-11-CC-99', ...]
	_ids = set(ids)
	list_ids = [str(i) for i in _ids]
	str_ids = str(list_ids)[1:-1]
	netmask_bytes = length
	netmask_str = '\x00' * netmask_bytes
	netmask = bytearray(netmask_str)
#cmd = "select op2 from esl_list where eslid in (%s) " % str_ids
	if h.get("netid_from_para", "no") == "yes":
		#组网时候的查询，使用全局表里的netid
		ret = []
		for id1 in ids:
			if id1 in h["idpara"]:
				_, _, _, netid, _, _ = h["idpara"][id1]
				ret.append(netid)
	else:
		ret = db.get_netid(str_ids)


# ret -> [(u'100',),(u'123',), ....]
	for x in ret:
		try:
			num = int(x) % 160 
		except ValueError,e:
			continue
		bit = num % 8 # bit位
		index = num / 8 # 下标
		index = index % netmask_bytes

		netmask[index] |= (1 << bit)

	netmask[20] = 0xff
	netmask[21] = 0x00

	return [i for i in netmask]

def send_add_wakeup_frame1(h, db, add_wk, fifo):
	for (nw1, chn, ids) in add_wk:
		nw1 = htonl(int(nw1.replace('-',''), 16))
		chn = int(chn)
		make_wakeup_frame1(h, chn, nw1, db, ids)
		fifo.stdin.write(h['grp_wk_frame1'])
	for (nw1, chn, ids) in add_wk:
		nw1 = htonl(int(nw1.replace('-',''), 16))
		fifo.stdin.write(struct.pack('<I', nw1))
	for (nw1, chn, ids) in add_wk:
		chn = int(chn)
		fifo.stdin.write(struct.pack('B', chn))

def make_wakeup_frame1(h, channel, wakeupid, db, sleepids):
	ver = h.get("wk1_ver", 0)
	if ver == 0:
		s = send_wakeup_frame1_v0(h, channel, wakeupid, db, sleepids)
	elif ver == 1:
		s = send_wakeup_frame1_v1(h, channel, wakeupid, db, sleepids)
	else:
		s = send_wakeup_frame1_v0(h, channel, wakeupid, db, sleepids)

	h['grp_wk_frame1'] = s

def send_wakeup_frame1_v0(h, channel, wakeupid, db, sleepids):
	s = struct.pack('<II', wakeupid, 26)
	ctrl = 6 << 5 # frame 1 :  110
	netmask = fill_netmask(h, db, sleepids,22) 
	fmt = '<IBB'
	string = P(fmt, wakeupid, ctrl, int(h['channel']))
	crc_value = my_cal_crc16(0, string, len(string))

	for i in netmask:
		string = P('B',i)
		crc_value = my_cal_crc16(crc_value,string,len(string))
	
	s += struct.pack('<BB', ctrl, int(h['channel']))
	for i in netmask:
		s += struct.pack('B',i)
	s += struct.pack('H',crc_value)

	return s

def send_wakeup_frame1_v1(h, channel, wakeupid, db, sleepids):
	s = struct.pack('<II', wakeupid, 26)
	ctrl = 6 << 5 # frame 1 :  110
	netmask = fill_netmask(h, db, sleepids,22) 
	fmt = 'BB'
	string = P(fmt, ctrl, int(h['channel']))
	crc_value = my_cal_crc16(0, string, len(string))

	for i in netmask:
		string = P('B',i)
		crc_value = my_cal_crc16(crc_value,string,len(string))

	fmt = '<I'
	string = P(fmt, wakeupid)
	crc_value = my_cal_crc16(crc_value, string, len(string))
	
	s += struct.pack('<BB', ctrl, int(h['channel']))
	for i in netmask:
		s += struct.pack('B',i)
	s += struct.pack('H',crc_value)

	return s

def get_group_mask(nw1_list):
	B = [0, 0, 0]
	
	for nw1 in nw1_list:
		mask = int(nw1.split('-')[2], 16)
		mask = mask % 24
		i, b = mask /8, mask % 8
		B[i] |= (1 << b)
	
	return B[0], B[1], B[2]

def make_set_wakeup_frame(h, db, nw1_list):

	s = struct.pack('>I', int(h['setid'].replace('-', ''), 16)) #set wkup id
	s += struct.pack('BBB', int(h['setchn']), h.get('set_wkup_time', 0), \
															h.get('set_data_len', 0)) #set wkup chn, time, datalen
	wk_time_dict = {1:0, 2:1, 4:3, 6:9, 8:10}
	wk_time = wk_time_dict.get(h.get("wakeuptime", 4), 3)
	wk_time = wk_time << 4
	wk_time |= wk_time_dict.get(h.get("worktime", 4), 3)

	s += struct.pack('BB', (h.get("set_ctrl", 3) << 5) & 0xE0, 0)
	#s += struct.pack('BBB', 0xff, 0xff, 0xff)
	b1, b2, b3 = get_group_mask(nw1_list)
	s += struct.pack('BBB', b1, b2, b3)
	s += struct.pack('B', wk_time)

	h['set_wk_frame'] = s

def htp_start(task_id, task_num, db, apid, h, data_area, slaveap, sleepids, retry_times, add_wk, same_netid):
	'''
	封装htp包头，加入updata或query模块生成的data_area数据，加上sleep_ids，发送给htp进程
	输入参数依次为：数据库实例对象，apid，信道，nw1，数据区的ID个数，nw4字段值，
	para值，op2，及已经组好的数据区值。
	返回值为htp层函数的标准输出和标准错误输出
	'''
	
	wkup_group_num = len(add_wk)

	ap = db.get_one(db.ap, apid)
	if ap and ap['apip'] and ap['listenport']:
		ap_addr, ap_port = str(ap['apip']), ap['listenport']
		#数据长度等于48字节头，40字节子头，数据区长度，休眠区长度
		if (h['transfermode'] == 4):
			ap_datalen = 48 + 40 + len(data_area) + 34
			if wkup_group_num > 0:
				ap_datalen -= 34
				ap_datalen += wkup_group_num * (34 + 4 +1)
				ap_datalen += 13
				ap_datalen += 4 * len(same_netid)
		else:
			ap_datalen = 48 + 40 + len(data_area) + len(sleepids) * 4
	else:
		return [], "get ap ip addr failed: %s, %s." % (ap_addr, ap_port)
   
	if task_id != 0:
		h['is_send_set'] = 0

   #FTP INFO
	rcved_timeout = int(conf.htp.rcved_timeout_sec)
	ack_timeout = int(conf.htp.ack_timeout_sec)
	socket_timeout = int(conf.htp.socket_timeout_sec)
	sleep_times = int(conf.htp.sleep_times)

	#check_htp_config:
	rcved_timeout = check_htp_config(rcved_timeout)
	ack_timeout = check_htp_config(ack_timeout)
	socket_timeout = check_htp_config(socket_timeout)
	sleep_times = check_htp_config(sleep_times)
	if sleep_times > 3 or sleep_times < 0:
		sleep_times = 1
	retry_times = check_htp_config(retry_times)

	ftp_server = str(conf.htp.ftp_server)
	ftp_port = conf.htp.ftp_port
	ftp_user = str(conf.htp.ftp_user)
	ftp_pass = str(conf.htp.ftp_pass)

	fifo = subprocess.Popen(get_exe_file("lib/bin/htp"), stdin = subprocess.PIPE,
										stdout = subprocess.PIPE,
										stderr = subprocess.PIPE,)

	ack_timeout += h.get("set_wkup_time", 0)
	rcved_timeout += h.get("set_wkup_time", 0)
	is_set_cmd = 0
	if h.get('is_set_cmd', False):
		is_set_cmd = 1

	try:
		fifo.stdin.write(struct.pack('<BBBBBBB16sH16s16s16s16sHI', task_id, task_num, h.get("set_wkup_time", 0), \
				retry_times, rcved_timeout,\
				ack_timeout, socket_timeout, ftp_server, int(ftp_port), ftp_user, ftp_pass,\
				str(apid), str(ap_addr), int(ap_port), ap_datalen))
		#发送包头

		fifo.stdin.write(struct.pack('<16s16s16s', str(h['version']), h['timestamp'],h['htpreserve']))
		fifo.stdin.write(struct.pack('<BBIIBBBB', h['ctrl'], h['para'], h['masterid'], h['wakeupid'],\
								h['channel'], h['wakeuptime'], h['worktime'], h['framerecvtimeout']))
		fifo.stdin.write(struct.pack('<BHBBBHBBBBBBBBH2s', h['transfermode'], h['masterrecvbps'], h['framelen'], \
								sleep_times, h['sleepid_ctrl'], h['query_timeout'], h['rf_tx_power'], \
								wkup_group_num, h.get("is_send_set", 0) , h.get("pkn_offset", 2), task_num -1, \
								h['dummy_frame'], h['wk0_slot'] , is_set_cmd, len(same_netid), h['rfreserve']))
		fifo.stdin.write(struct.pack('<HHH', h['updatanum'], h['sleepnum'], h['crc']))
		#发送data_area
		fifo.stdin.write(data_area)
		#发送sleepid
		if (h['transfermode'] == 4):
			if wkup_group_num == 0:
				fifo.stdin.write(h['grp_wk_frame1'])
			else:
				send_add_wakeup_frame1(h, db, add_wk, fifo)
			#发送set帧
			fifo.stdin.write(h['set_wk_frame'])
			#发送相同子网号的价签
			for id1 in same_netid:
				fifo.stdin.write(struct.pack('>I', int(id1.replace('-', ''), 16)))
		else:
			for item in sleepids:
				fifo.stdin.write(struct.pack('>I', int(item.replace('-', ''), 16)))
		#发送辅基站IP
		if h['transfermode'] == 4:
			slaveap = []
		fifo.stdin.write(struct.pack('<I', len(slaveap)))
		for ap in slaveap:
			ap1 = db.get_one(db.ap, ap)
			fifo.stdin.write(struct.pack('16s16s', str(ap), str(ap1['apip'])))
		return fifo.communicate()
	finally:
		try:
			fifo.terminate()
		except Exception, e:
			pass

def fill_htp_para(db, ids, cmd, real_len, retry_times):
	htp_para = {}
	try:
		#HTP_HEADER
		htp_para['version'] = conf.htp.htp_version

		htp_para['timestamp'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		htp_para['htpreserve'] = ''

		#RF_HEADER
		T = get_seg_json("./config/htp_conf.ini")
		id1 = db.get(ids[0])
		rf_para = T[id1['op3']]['rf_para']

		if cmd in rf_para['ctrl']:
			htp_para['ctrl'] = rf_para['ctrl'][cmd]
		else:
			htp_para['ctrl'] = rf_para['ctrl']['UPDATA']

		htp_para['para'] = 0 # BIT0 ap ass, it will be change in htp lib 
		htp_para['masterid'] = htonl(int(id1['nw2'].replace('-',''), 16))
		htp_para['wakeupid'] = htonl(int(id1['nw1'].replace('-',''), 16)) 

		htp_para['channel'] = int(id1['nw3'])
		if id1['grpchn'] and (not conf.extend_service.apv3_enable.lower() == 'yes'):
			htp_para['channel'] = int(id1['grpchn'])

		htp_para['wakeuptime'] = rf_para['wakeuptime'] #获取真实的唤醒时间
		htp_para['worktime'] = rf_para['worktime']
		htp_para['framerecvtimeout'] = rf_para['timeout']
		htp_para['framelen'] = rf_para['framelen']
		htp_para['transfermode'] = rf_para['transfermode']
		htp_para['masterrecvbps'] = rf_para['bps']
		htp_para['sleepid_ctrl'] = rf_para['sleepid_ctrl']
		htp_para['rfreserve'] = ""
		htp_para['query_timeout'] = rf_para.get('query_timeout',0)
		htp_para['rf_tx_power'] = 0x00
		htp_para['wk1_ver'] = int(rf_para.get('wk1_ver', 0))

		htp_para['set_wkup_time'] = int(rf_para.get('set_wkup_time', 8))
		htp_para['set_data_len'] = int(rf_para.get('set_data_len', 6))
		htp_para['is_send_set'] = int(rf_para.get('is_send_set', 0))
		htp_para['pkn_offset'] = int(rf_para.get('pkn_offset',2))

		htp_para['wk0_slot'] = int(rf_para.get('wk0_slot', 5))
		
		try:
			#当价签数少于5，且重试次数大于5时，使用超级模式
			if real_len <= rf_para.get('adv_less', 5) and retry_times >= rf_para.get('adv_retry_time', 5):
				htp_para['rf_tx_power'] = rf_para.get('adv_rf_tx_power', 55)
				htp_para['wakeuptime'] = rf_para.get('adv_wakup_time', 5)
		except KeyError, e:
			pass

		htp_para['updatanum'] = len(ids)
		#htp_para['sleepnum'] = ""
		htp_para['crc'] = 0
		
		#for other use
		htp_para['masterid-str'] = id1['nw2']
		htp_para['wakeupid-str'] = id1['nw1']
		
		htp_para['dummy_frame'] = rf_para.get('dummy_frame', 6)

		htp_para['setid'] = id1['nw1']
		if not htp_para['setid']:
			htp_para['setid'] = id1['nw1']

		htp_para['setid']= get_setid(htp_para['setid'])
		
		try:
			htp_para['setchn'] = int(id1['setchn'])
		except TypeError, e:
			htp_para['setchn'] = htp_para['channel']
		except ValueError, e:
			htp_para['setchn'] = htp_para['channel']

	except Exception, e:
		esl_init.log.error_msg("fill_htp_para: %s" % e, errid='EHT002')
	
	return htp_para

def get_setid(src):
	setid = "%s%s-%s%s-00-%s%s" % (src[0], src[1], src[3], src[4], src[9], src[10])
	return setid

def filter_htp_para(htp_para, wakeupid, channel, idpara, setchn, grpchn):
	
	htp_para['wakeupid'] = htonl(int(wakeupid.replace('-',''), 16)) 
	htp_para['channel'] = int(channel)
	
	htp_para['wakeupid-str'] = wakeupid

	htp_para["netid_from_para"] = "yes"
	htp_para["idpara"] = idpara
	htp_para['setchn'] = setchn
	htp_para['channel'] = grpchn
	htp_para['setid']=  get_setid(wakeupid)

def get_ap_of_group(apid, ap_group):
	for name1 in ap_group:
		for ap_str in ap_group[name1]:
			if int(apid) == int(ap_str):
				return name1
	return None

def is_same_2bit(id1, id2):

	esl1 = htonl(int(id1.replace('-',''), 16))
	esl2 = htonl(int(id2.replace('-',''), 16))

	if esl1 == esl2:
		return False

	val = esl1 ^ esl2
	n1 = 0
	BIT_DIFF = 2
	for i in xrange(32):
		if val & (1 << i):
			n1 += 1
			if n1 > BIT_DIFF: #超过2个bit不同
				break
	
	return False if n1 > BIT_DIFF else True

def is_same_1bit(id1, id2):

	esl1 = htonl(int(id1.replace('-',''), 16))
	esl2 = htonl(int(id2.replace('-',''), 16))

	if esl1 == esl2:
		return False

	val = esl1 ^ esl2
	n1 = 0
	BIT_DIFF = 1
	for i in xrange(32):
		if val & (1 << i):
			n1 += 1
			if n1 > BIT_DIFF: #超过2个bit不同
				break
	
	return False if n1 > BIT_DIFF else True

def adjust_ids(ids):
	'''将需要进行数据传输的id进行过滤，排除掉相差2bit以内的价签'''
	tmp_ids = ids[:]
	same_ids = []
	for id1 in tmp_ids:
		i = tmp_ids.index(id1)
		for id2 in tmp_ids[i:]: 
			if id2 in ids and id1 in ids and is_same_2bit(id1, id2):
				ids.remove(id2)
				same_ids.append(id2)
				esl_init.log.debug("%s same as %s, remove it" % (id2, id1))
	return ids

def adjust_sleep_ids(ids, sleep_ids):
	same_ids, same_ids1, same_ids2 = [], {}, {}
	for id1 in ids:
		for id2 in sleep_ids:
			if is_same_1bit(id1, id2): #相差1个BIT,扩大3倍
				same_ids1[id2] = 0
				#esl_init.log.debug("id2 %s ^ id1 %s == 1bit" % (id2, id1))
			elif is_same_2bit(id1, id2): #相差2个BIT，一倍即可
				#esl_init.log.debug("id2 %s ^ id1 %s == 2bit" % (id2, id1))
				same_ids2[id2] = 0

	for key in same_ids2.keys():
		if key in same_ids1:
			same_ids2.pop(key)

	#esl_init.log.info("ids: [%s]%s" % (len(ids), ids))
	#esl_init.log.info("same_ids2: [%s]%s" % (len(same_ids2), same_ids2.keys()))
	#esl_init.log.info("same_ids1: [%s]%s" % (len(same_ids1), same_ids1.keys()))

	s1 = []
	s1.extend(same_ids1.keys())
	s1.extend(same_ids2.keys())
	
	s2 = []
	s2.extend(same_ids1.keys()*2)
	s2.extend(same_ids2.keys())
	#最多512个时间窗口
	n = (512 - len(s1)) / (len(s2)+1) +1
	s2 *= n
	s1.extend(s2)
	return s1[:512] #填满512个sleep窗口

def append_add_wk(wakeupid, chn, ids, add_wk, nw1_list):
	id1 = deepcopy(ids)
	for (nw1, nw3, esl_list) in add_wk:
		ids.extend(esl_list)
		nw1_list.apend(nw1)
	add_wk.insert(0, (wakeupid, chn, id1))

def remove_zero_add_wkup(ids, add_wk):
	for (wkid, chn, esl_list) in add_wk:
		for id1 in esl_list[:]:
			if id1 not in ids:
				esl_list.remove(id1)
	for i in xrange(len(add_wk)-1, -1, -1):
		if len(add_wk[i][2]) == 0:
			del add_wk[i]

def is_set_cmd(ids, all_info):
	for id1 in ids:
		cmd = all_info[id1]['data_cmd']
		if cmd == 'CMD_SET_CMD':
			return True, id1
	return False, None

def get_set_cmd_frame(id1, info, h):
	s = struct.pack('>I', int(h['setid'].replace('-', ''), 16)) #set wkup id
	s += struct.pack('BBB', int(h['setchn']), h.get('set_wkup_time', 0), \
															h.get('set_data_len', 0)) #set wkup chn, time, datalen

	cmd, args = info['setcmd'], info['setargs']

	if cmd == "CMD_LED_CONFIG":
		cmd = 0xB4
		if int(args):
			args = 0x72
		else:
			args = 0x70
	elif cmd == "CMD_LCD_CONFIG":
		cmd = 0xF0
		args = (5 << 5) | (int(args) & 0x1F)
	elif cmd == "CMD_HB_CONFIG":
		cmd = 0x5A
		args = (1 << 5) | (int(args) & 0x1F)
	elif cmd == "CMD_PAGE_CHANGE":
		cmd = 0xA5
		args = (2 << 5) | (int(args) & 0x1F)
	elif cmd == "CMD_HB_REQUEST":
		cmd = 0x3C
		args = (4 << 5) | ((int(args[0] & 0x7) << 2)) | (int(args[1]) & 3)
	elif cmd == "CMD_SET_CONFIG":
		cmd = 0x96
		args = (2 << 5) | (int(args) & 0x1F)
	elif cmd == "CMD_CHN_CONFIG":
		cmd = 0x8A
		ids = h['setid'].split('-')

		crc = 0
		for v in [cmd, int(args[0]), int(args[1]), int(args[2]), 
					int(ids[0], 16), int(ids[1], 16), int(ids[2], 16),int(ids[3], 16)]:
			crc = ((crc<<8)%65536 ^ crc16tab[((crc>>8)%65536 ^ v )])%65536

		s += struct.pack('BBBBBB', cmd, int(args[0]), int(args[1]), int(args[2], crc % 256, crc / 256))
		
		return s

	s += struct.pack('BBBBBB', 0x20, cmd, 0xFF, 0xFF, 0xFF, args)
	return s

def get_dataarea(cmd, flags, epd_type, ack_def, ids, htp_para, all_info, real_len, retry_times, MODE,\
						add_wk, apid):

	from core import get_ap_group, set_id_inprocess
	from updata import seg_updata_data_area, dot_updata_data_area_osd
	from netlink import esl_netlink_data_area

	data_area, ok_eslid, is_osd, step = None, [], False, None
	failed_list = []

	if cmd == "QUERY": #处理所有的查询
		T1 = get_seg_json("./config/htp_conf.ini")
		id1 = all_info.get(ids[0])
		if T1[id1['op3']] != 'HS_EL_5104':
			args = []
		else:
			rf_para = T1[id1['op3']]['rf_para']
			args = [rf_para['register_on'], rf_para['register_chn']]
		is_set, id1 = is_set_cmd(ids, all_info)
		if is_set:
			htp_para['is_set_cmd'] = True
			htp_para['set_cmd_frame'] = get_set_cmd_frame(id1, all_info[id1], htp_para)
			ids = [id1]

		data_area, failed_list = seg_updata_data_area(all_info, ids, get_exe_file("lib/bin/updata"))

		if 'OSD' in flags:	#断码更新不需要处理OSD
			flags.pop('OSD')
	elif cmd == "UNBIND":#组包成OFF字段
		data_area, failed_list = seg_updata_data_area(all_info, ids, get_exe_file("lib/bin/updata"))
		if 'OSD' in flags:	#断码更新不需要处理OSD
			flags.pop('OSD')
	elif cmd == "NETLINK":#处理所有的组网
		para = flags.get('NETLINK', {})
		if para:
			wid, ch, step, netid, setchn, grpchn = para[ids[0]]
			if step == 'query':
				htp_para_1 = fill_htp_para(all_info, ids, "QUERY", real_len, retry_times)
				filter_htp_para(htp_para_1, wid, ch, para, setchn, grpchn)
				htp_para.update(htp_para_1)
				data_area, failed_list = seg_updata_data_area(all_info, ids, get_exe_file("lib/bin/updata"))
			else:
				op3 = all_info.get(ids[0]).get('op3', 'HS_EL_5104')
				if op3 == 'HS_EL_5300':	
					data_area, failed_list = esl_netlink_data_area(all_info, ids, para, get_exe_file("lib/bin/updata"))
				else:
					data_area, failed_list = esl_netlink_data_area(all_info, ids, para, get_exe_file("lib/bin/netlink"))
		else:
			# 获取组网数据结构错误
			pass
		
		if 'OSD' in flags:	# 断码更新不需要处理OSD
			flags.pop('OSD')
	else:
		if epd_type == "NORMAL": #处理段码的更新	
			op3 = all_info.get(ids[0]).get('op3', 'HS_EL_5104')
			if op3 != 'HS_EL_5300':
				data_area, failed_list = seg_updata_data_area(all_info, ids, get_exe_file("lib/bin/updata"))
			else:
				data_area, failed_list = seg_updata_data_area(all_info, ids, get_exe_file("lib/bin/lcd3"))
				
			if 'OSD' in flags:	#断码更新不需要处理OSD
				flags.pop('OSD')
		else: #点阵价签更新
			is_osd = True
			last_ack = {}
			for id1 in ids:
				#防护 bugfree #68
				if id1 not in flags['osd_last_ack']:
					flags['osd_last_ack'][id1] = []
				last_ack[id1] = flags['osd_last_ack'][id1]
			data_area, ok_eslid, failed_list = dot_updata_data_area_osd(all_info, ids, \
											get_exe_file("lib/bin/osd"), last_ack, MODE = MODE, is_first = True)

			if (not data_area) and (not ok_eslid): #防止OSD程序异常没有生成任何数据
				esl_init.log.warning("osd return 0 bytes, will resend all data in next time")
				for id1 in ids:
					flags['osd_last_ack'][id1] = []
					
			set_id_inprocess(set(ids))
			#将不需要发送的价签从add_wk中移除，避免发生唤醒
			remove_zero_add_wkup(ids, add_wk)
			#osd不发送的价签则不反馈ack，避免记重试次数
			for id1 in ack_def.keys():
				if id1 not in ids:
					ack_def[id1] = (apid, 0,0, "OSD_WAIT")
					
			htp_para['updatanum'] = len(ids)
	
	htp_para['updatanum'] = len(ids)
	
	set_id_inprocess(set(ids))
	for id1 in ack_def.keys():
		if id1 in failed_list: #错误的价签直接设置为失败
			ack_def[id1] = (apid, 0,0, "NORMAL")

	return data_area, ok_eslid, is_osd, step

def gen_ack(is_osd, ack_list, all_info, ids, MODE, ok_eslid, ack_def, osd_ack, apid, cmd):
	from updata import check_osd_finished

	ack_comp = {}
	if is_osd:
		#合并主辅基站的ACK
		for (ap1, id1, n, ret) in ack_list:
			if ret >= 2:
				ret = 2
			ack_comp.setdefault(id1,{}).setdefault(n,0)
			if ack_ok_osd((ap1, id1, ret, "OSD")):
				ack_comp[id1][n] = ret

		#将ack的值再次调用OSD，有通讯结束的append到ok_eslid,还有未完成的，则保留到全局变量里
		ok_eslid_again = check_osd_finished(all_info, list(set(ids)), get_exe_file("lib/bin/osd"), ack_comp, MODE)
		ok_eslid.extend(ok_eslid_again)
		for id1 in ok_eslid_again:
			ack_comp.pop(id1, None)
			if id1 in ack_def:
				ack_def.pop(id1)

		for id1 in ack_comp:
			for n in xrange(len(ack_comp[id1])):
				osd_ack.append((id1, (str(apid), n, ack_comp[id1][n], "OSD")))
			if id1 in ack_def:
				ack_def.pop(id1)
		
		for id1 in ack_def: #如果HTP通讯失败，则使用默认值
			if ack_def[id1] == (apid, 0, 0, "NORMAL"):
				osd_ack.append((id1, (apid, 0, 0, "OSD")))
			else:
				osd_ack.append((id1, ack_def[id1]))

		for id1 in ok_eslid:	#再加上已经更新成功的价签
			osd_ack.append((id1, (apid, OSD_FINISHED_NUMBER, 1, "NORMAL")))
	else:
		if ack_list:
			ack_cmp = {}
			for (ap1, id1, n, ret) in ack_list:
				if id1 not in ids:
					continue	#收到一个预期外的价签ID返回值
				ack_cmp.setdefault(id1, []).append(int(ret))

			for id1 in ack_cmp:
				if 0 in ack_cmp[id1]:
					ack_def[id1] = (apid, 0, 0, cmd) 
				else:
					ack_def[id1] = (apid, 0, ack_cmp[id1][0], cmd) 

def htp_task(groups, epd_type, cmd):
	'''
	负责处理一组段码价签的更新或者查询，传入参数格式为(apid, chn, nw1, [ids,...])
	返回格式为 [(id, ack), (id, ack),...]
	'''
	from core import get_ap_group, set_id_inprocess

	is_vitrual_htp = conf.htp.vitrual_htp.lower() == 'yes'
	vitrual_pass_rate = conf.htp.vitrual_pass_rate

	task_id, apid, chn, wakeupid, ids, slaveap, retry_times, flags, ack_q, all_info = groups
	add_wk, nw1_list = [], []

	task_num = flags['ap_task_num'][apid]
	nw1_list = flags['ap_task_nw1'][apid]

	if 'HS_EL_51' in all_info[ids[0]]['op3'] or 'HS_EL_53' in all_info[ids[0]]['op3']:
		try:
			add_wk = flags['add_wk'][apid][task_id]
			append_add_wk(wakeupid, chn, ids, add_wk, nw1_list) #添加附加组ID
		except KeyError, e:
			pass

	real_len = len(ids)
	ids_backup = deepcopy(ids)

	#先使用字典记录默认值
	ack_def, ack_list = {}, '[]'
	_ids = ids[:]
	
	for id1 in ids:
		ack_def[id1] = (apid, 0, 0, "NORMAL")

	osd_ack = []
	is_osd = False

	try:
		db = DB()
		ap_group = get_ap_group(None)
		htp_para = fill_htp_para(all_info, ids, cmd, real_len, retry_times);
		MODE = htp_para['transfermode']

		data_area, ok_eslid, is_osd, step = get_dataarea(cmd, flags, epd_type, ack_def, ids, htp_para, \
								all_info, real_len, retry_times, MODE, add_wk, apid)

		apg = get_ap_of_group(apid, ap_group)
		cmd_str = cmd
		if step != None:
			if step == 'query':
				cmd_str = 'QUERY'
		if htp_para.get('is_set_cmd', False):
			cmd_str ='SETCMD'

		esl_init.log.info("retry: %s, start htp[%s, %s, %s/%s, %s, %s, %s, %s, %s, %s]" % \
			(retry_times, apg, apid, task_id+1, task_num ,chn, wakeupid, real_len, len(ids), slaveap, cmd_str))

		try:
			same_netid = []
			sleepids = db.get_wakeup_channel_esl_list(htp_para['wakeupid-str'], htp_para['channel'])
			for id1 in ids:	#sleep IDs去掉数据区已有的id
				if id1 in sleepids:
					sleepids.remove(id1)
			api20.update_htp_start_status(db, apid, ids, sleepids, slaveap)
			if htp_para['transfermode'] != 4:
				sleepids = sleepids[:512] # 要睡眠的价签
				if cmd == 'query' or cmd =='netlink':
					ids = ids
			else: # 当为模式4时 不需要睡眠帧
				sleepids = ids # 要工作的价签
				same_netid = db.get_wakeup_channel_netid_same(htp_para['wakeupid-str'], htp_para['channel'], ids)

			htp_para['sleepnum'] = len(sleepids)
			if htp_para.get('is_set_cmd', False):
				htp_para['set_wk_frame'] = htp_para['set_cmd_frame']
			else:
				make_set_wakeup_frame(htp_para, db, nw1_list)
			make_wakeup_frame1(htp_para, htp_para['channel'], htp_para['wakeupid'], db, sleepids)

			if data_area:
				if not is_vitrual_htp:
					if conf.extend_service.apv3_enable.lower() == 'yes':
						ack_list, err = flags['apv3'].htp_start(task_id, task_num, db, apid, htp_para, 
								data_area, ids, all_info)
					else:
						ack_list, err = htp_start(task_id, task_num, db, apid, htp_para, data_area, 
								slaveap, sleepids, retry_times, add_wk, same_netid)
					if err:
						esl_init.log.info("htp_task:%s", err)
				else:
					#for test start
					ack_list, err = [], ''
					n, prov_id = 0, None
					for id1 in ids:
						if prov_id != id1:
							prov_id = id1
							n = 0
						ok_v = 1
						ack = ok_v if random.randint(1, 100) <= vitrual_pass_rate else 0
						ack_list.append((str(apid), id1.upper(), n, ack))
						n += 1

			if is_vitrual_htp and not data_area:
				ack_list = []
			if is_vitrual_htp:
				ack_list = str(ack_list)

		except Exception,e:
			print_except()
			esl_init.log.error_msg("%s" % e, errid='EHT003')
		esl_init.log.info("end htp[%s]" % (apid))

		#返回ack和值的字典
		if not ack_list:
			ack_list = '[]'
		try:
			ack_list = eval(ack_list, {}, {})
		except Exception, e:
			esl_init.log.warning("ack_list: %s" % e)
			ack_list = '[]'

		api20.udpate_htp_end_status(db, apid, ids, sleepids, slaveap)
		if htp_para.get('is_set_cmd', False): #set命令直接设置结果为成功
			ack_list = [(apid, ids[0], 0, 1)]
			
		if htp_para['ctrl'] == 0x11: #过滤老系统的组网结果成标准的ACK
			new_ack_list = []
			for (ap1, id1, n, ret) in ack_list:
				if ret == 0x40:
					new_ack_list.append((ap1, id1, n, 1))
				else:
					new_ack_list.append((ap1, id1, n, 0))
			ack_list = new_ack_list

		esl_init.log.info("ack_list: [%s];%s" % (len(ack_list), ack_list))
		
		for (ap1, id1, n, ret) in ack_list:
			flags['ack_count'].setdefault(ret, 0)
			flags['ack_count'][ret] += 1
					
		gen_ack(is_osd, ack_list, all_info, ids, MODE, ok_eslid, ack_def, osd_ack, apid, cmd)

	except Exception, e:
		print_except()
		esl_init.log.error_msg("htp_task: %s" % e, errid='EHT004')
	finally:
		db.conn.close()
		db = None
		if is_osd:
			for k in osd_ack:
				ack_q.put(k)
			return 
		for k in ack_def:
			ack_q.put((k, ack_def[k]))


