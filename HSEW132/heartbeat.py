# encoding=utf-8
from esl_init import log, conf
from dot_temp import get_seg_json
import json, bind, time


def unicode2str():
    ''' load json will be unicode,
        transfer it to str '''
    table_esl = get_seg_json('config/table_esl.ini')
    table_esl_a = {}
    for version in table_esl:
        table_esl_a.setdefault(str(version),{})
        for attr in table_esl[version]:
            table_esl_a[str(version)].setdefault(str(attr),{})
            if attr == 'op5' or attr == 'op6':
                for ele in table_esl[version][attr]:
                    table_esl_a[str(version)][str(attr)].setdefault(str(ele),{})
                    v = table_esl[version][attr][ele]
                    if type(v) == unicode:
                        table_esl_a[str(version)][str(attr)][str(ele)] = str(v)
                    else:
                        table_esl_a[str(version)][str(attr)][str(ele)] = v
            else:
                v = table_esl[version][attr]
                if type(v) == unicode:
                    table_esl_a[str(version)][str(attr)] = str(v)
                else:
                    table_esl_a[str(version)][str(attr)] = v
    return table_esl_a

table_esl = unicode2str()
EPL = conf.htp.esl_power_level


class Power_level():
	try:
		BEST    = EPL[0]
		BETTER  = EPL[1]
		BETTER1 = EPL[2]
		BETTER2 = EPL[3]
		BETTER3 = EPL[4]
		BETTER4 = EPL[5]
		BAD     = EPL[6]
	except Exception, e:
		pass

P = Power_level()

def level_of_power(rfpower):
	rfpower = int(rfpower)
	if (rfpower < P.BETTER):
		return P.BEST
	if (rfpower < P.BETTER1):
		return P.BETTER
	if (rfpower < P.BETTER2):
		return P.BETTER1
	if (rfpower < P.BETTER3):
		return P.BETTER2
	if (rfpower < P.BETTER4):
		return P.BETTER3
	if (rfpower < P.BAD):
		return P.BETTER4
	return P.BAD

def is_man_updata(args, reg_info):
	for item in args:
		for k in ['nw1', 'nw2', 'nw3', 'nw4', 'op1', 'op2', 'op3', 'op5', 'op6', 'op7', 'op8', 'op9', 'setchn', 'grpchn']:
			if k in item:
				reg_info.pop(item['eslid'].upper(), None)
				break

def conv_info_to_mem(reg):
	e = {}
	version = str(reg['version'])
	e['nw1'] = reg['nw1'] #wakeupid
	e['eslid'] = reg['eslid']
	e['nw2'] = '52-56-78-53' #masterid
	e['nw3'] = reg['nw3'] #channel
	e['nw4'] = table_esl[version]['nw4'] #esltype
	e['op1'] = reg['battery']
	e['op2'] = reg['netid']
	e['op3'] = table_esl[version]['op3'] #esltype
	e['op5'] = table_esl[version]['op5'] #fix para
	e['op7'] = reg['reserve'] #reserve
	e['op8'] = table_esl[version]['op8'] #retry times
	e['setchn'] = reg['nw3']
	e['grpchn'] = reg['nw3']
	if 'setchn' in reg:  # 以特殊心跳字段判断3代价签
		e['setchn'] = reg['setchn']
		e['grpchn'] = reg['grpchn']
		e['nw1'] = e['nw1']+'-'+'66'
		trans_op1 = reg['battery']
		if trans_op1 == '0':
			e['op1'] = '30'
		else:
			e['op1'] = '27'

	
	return e, version

def is_info_change2(mem, provinfo):
	#必选字段发生改变
	for k in ['nw1', 'nw2', 'nw3', 'nw4', 'op1', 'op2', 'op3', 'op5', 'op7', 'op8', 'setchn', 'grpchn']:
		if k not in mem or k not in provinfo or mem[k] != provinfo[k]:
			return True
	#其余字段不关心
	return False
		
def conv_info_to_db(db, id1, mem, version):
	if db.has_key(db.esl, id1):
		info = db.get_all_info(db.esl, id1)
	else:
		info = {}

	#如下值只进行初始化，不负责改写
	for k in ['op4', 'op6', 'op9']:
		if k in table_esl[version] and (k not in info or (not info[k])):
			mem[k] = table_esl[version][k]
		
	return mem

esl_hb_dict = {}
esl_hb_dict_last_time = time.time()

def esl_hb_report(i):
	global esl_hb_dict
	global esl_hb_dict_last_time
	esl_hb_list = []

	esl_hb_dict[i['eslid']] = {'eslid':i['eslid'], 'apid':i['apid'], 'battery':i['battery']}

	ESL_HB_REPORT_MAX = int(conf.system.esl_hb_report_max)
	ESL_HB_REPORT_TIMEOUT = int(conf.system.esl_hb_report_timeout)

	if ESL_HB_REPORT_MAX <= 0 or ESL_HB_REPORT_TIMEOUT <= 0:
		return []

	if len(esl_hb_dict) >= ESL_HB_REPORT_MAX or \
		time.time() - esl_hb_dict_last_time >= ESL_HB_REPORT_TIMEOUT:
		esl_hb_list = esl_hb_dict.values()
		esl_hb_dict = {}
		esl_hb_dict_last_time = time.time()
	
	return esl_hb_list

def esl_register(db, info, reg_info, esl_power_info, esl_power_his, \
						esl_level_change_count, ap_work_time, e_flag):

	save_list, bind_list, online_status = [], [], []
	esl_hb_report_list = []

	for i in info:
		#conv(i) #数据字段做转义
		if not e_flag.isSet():
			e_flag.wait() # wait(): event没有被set()会一直阻塞	
		id1 = i.get("eslid", None)
		if not id1: #不存在key
			continue
		reserve_flag = i.get("reserve", None)
		if not reserve_flag:
			i["reserve"] = "0"  # 保留'reserve'字段，2、3代价签兼容
		mem, version = conv_info_to_mem(i)		
		if id1 not in reg_info or is_info_change2(mem, reg_info[id1]):
			reg_info[id1] = mem
			dbinfo = conv_info_to_db(db, id1, mem, version)
			save_list.append(dbinfo)
		#保存基站能量值信息, 如果能力值发送变化，则返回到bind_list中
		bind_list.extend(update_esl_power_info(\
			i, esl_power_info, esl_power_his, esl_level_change_count, ap_work_time))
		esl_hb_report_list.extend(esl_hb_report(i))

	#如果参数发生变更，则保存进数据库
	db.list_updata(db.esl, save_list)
	auto_bind_after_register = conf.htp.auto_bind_after_register.lower()
	if auto_bind_after_register == 'yes':
		return refresh_bind_list(db, bind_list, esl_power_info, ap_work_time), online_status
	return [], esl_hb_report_list

def linearSmooth3(indata, n):
	out = indata[:]
	if n < 3:
		return indata[n-1]

	out[0] = ( 5.0 * indata[0] + 2.0 * indata[1] - indata[2] ) / 6.0
	for i in range(1, n-1):
		out[i] = ( indata[i - 1] + indata[i] + indata[i + 1] ) / 3.0
	out[n - 1] = ( 5.0 * indata[n - 1] + 2.0 * indata[n - 2] - indata[n - 3] ) / 6.0

	for i in range(n):
		indata[i] = int(out[i])

	return indata[n-1]


def linearSmooth7(indata, n):
	out = indata[:]
	if n < 7:
		return indata[n-1]

	out[0] = ( 13 * indata[0] + 10 * indata[1] + 7 * indata[2] + 4 * indata[3] +
		indata[4] - 2 * indata[5] - 5 * indata[6] ) / 28
	out[1] = ( 5 * indata[0] + 4 * indata[1] + 3 * indata[2] + 2 * indata[3] +
		indata[4] - indata[6] ) / 14
	out[2] = ( 7 * indata[0] + 6 * indata [1] + 5 * indata[2] + 4 * indata[3] +
		3 * indata[4] + 2 * indata[5] + indata[6] ) / 28
	
	for i in range(3, n - 4):
		out[i] = ( indata[i - 3] + indata[i - 2] + indata[i - 1] + indata[i] + indata[i + 1] + indata[i + 2] + indata[i + 3] ) / 7
	
	out[n - 3] = ( 7 * indata[n - 1] + 6 * indata [n - 2] + 5 * indata[n - 3] +
		4 * indata[n - 4] + 3 * indata[n - 5] + 2 * indata[n - 6] + indata[n - 7] ) / 28
	out[n - 2] = ( 5 * indata[n - 1] + 4 * indata[n - 2] + 3 * indata[n - 3] +
		2 * indata[n - 4] + indata[n - 5] - indata[n - 7] ) / 14
	out[n - 1] = ( 13 * indata[n - 1] + 10 * indata[n - 2] + 7 * indata[n - 3] +
		4 * indata[n - 4] + indata[n - 5] - 2 * indata[n - 6] - 5 * indata[n - 7] ) / 28

	for i in range(n):
		indata[i] = int(out[i])

	return indata[n-1]

def linear_normal(indata, n):
	#取平均数
	power_list = sorted(indata)
	if len(power_list) > 4:
		power_list = power_list[2:-2]
	return sum(power_list)/len(power_list)

def append_to_his(eslid, apid, rfpower, esl_power_his):
	rfpower = int(rfpower)
	esl_power_threshold = int(conf.htp.esl_power_threshold)

	esl_power_his.setdefault(eslid, {}).setdefault(apid, [])
	esl_power_his[eslid][apid].append(rfpower)
	'''
	#取平均数算法
	esl_power_his[eslid][apid] = esl_power_his[eslid][apid][-10:]
	ret = linear_normal(esl_power_his[eslid][apid], 10)
	if abs(ret-rfpower) > esl_power_threshold and len(power_list) >= 10:
		skip = False
	'''

	#3点滑动算法
	esl_power_his[eslid][apid] = esl_power_his[eslid][apid][-7:]
	n = len(esl_power_his[eslid][apid])
	p = esl_power_his[eslid][apid]
	ret = linearSmooth7(p, n)
	
	return ret

def is_level_change(level_old, level_curr, esl_power_his):
	esl_power_threshold = int(conf.htp.esl_power_threshold)

	if len(esl_power_his) < 7:
		return False
	if abs(level_old - level_curr) < esl_power_threshold:
		return False
	if abs(esl_power_his[0] - esl_power_his[-1]) > 10: 
		return False
	return True

def update_esl_power_info(info, esl_power_info,\
								esl_power_his, esl_level_change_count, ap_work_time):
	timeNow = time.time()
	eslid = info['eslid']
	apid = info['apid']
	rfpower = info['rfpower']
	bind_list = []
	rfpower = append_to_his(eslid, apid, rfpower, esl_power_his)
	level_curr = level_of_power(rfpower)
	esl_level_change_count.setdefault(eslid, [])

	if len(esl_power_his[eslid][apid]) < 7: #至少收到7个值，才开始计入信号表
		return []

	#首次加入
	is_ap_first = True
	if eslid in esl_power_info:
		for level in esl_power_info[eslid]:
			if apid in esl_power_info[eslid][level]:
				is_ap_first = False
				level_old, power_old, _ = esl_power_info[eslid][level][apid]
				break
	
	if is_ap_first:
		level_old, power_old = level_curr, rfpower
		esl_level_change_count[eslid].append(apid)
	#单个基站的能量值有变化
	is_change = is_level_change(level_old, level_curr, esl_power_his[eslid][apid])
	if is_change:
		log.debug("%slevel change: %s, %s, pre %s, cur %s, avg %s/%s, cur level %s, prov level %s" %\
			("skip " if not is_change else "", eslid, apid, power_old, info['rfpower'], rfpower, \
			(esl_power_his[eslid][apid]), level_curr, level_old))
		esl_power_info[eslid][level_old].pop(apid, None) #把过去的值从另外一个级别中删除掉
		level_old = level_curr
		#bind_list.append(eslid)
		esl_level_change_count[eslid].append(apid)
	#入库注册信息
	esl_power_info.setdefault(eslid, {}).setdefault(level_old, {})[apid] = (level_old, rfpower, timeNow)

	#再判断是否有基站超时
	esl_timeout = float(conf.system.esl_heartbeat_timeout)
	if eslid in esl_power_info:
		for level1 in esl_power_info[eslid]:
			for ap1 in esl_power_info[eslid][level1].keys():
				_, power_old, timelast = esl_power_info[eslid][level1][ap1]
				timeout = get_heartbeat_timeout(ap1, timelast, ap_work_time, esl_timeout)
				if (timeNow - timelast) > timeout: #注册信息过期
					esl_level_change_count[eslid].append(ap1)
					#删除所有过期的值,避免参与后面的运算
					esl_power_info[eslid][level1].pop(ap1, None) 
					esl_power_his[eslid].pop(ap1, None)
					break
	
	#发生了2个以上的变动，才切换绑定关系
	if len(set(esl_level_change_count[eslid])) >= 2:
		esl_level_change_count[eslid] = []
		bind_list.append(eslid)

	#去重
	bind_list = list(set(bind_list))
	bind_list = [{"eslid":eslid} for eslid in bind_list]

	return bind_list

def is_heardbeat_all_timeout(eslid, esl_power_info, ap_work_time):
	timeNow = time.time()
	timeout_flag = True
	esl_timeout = float(conf.system.esl_heartbeat_timeout)

	if eslid in esl_power_info:
		if timeout_flag:
			for level1 in esl_power_info[eslid]:
				if timeout_flag:
					for ap1 in esl_power_info[eslid][level1]:
						_, power_old, timelast = esl_power_info[eslid][level1][ap1]
						timeout = get_heartbeat_timeout(ap1, timelast, ap_work_time, esl_timeout)
						if (timeNow - timelast) <= timeout: #注册信息未过期
							timeout_flag = False
							break
	return timeout_flag

def refresh_heardbeat_offline(esl_power_info, ap_work_time):
	from xmlserver import reply_ack

	timeNow = time.time()
	timeout_dict = {}
	esl_timeout = float(conf.system.esl_heartbeat_timeout)

	for eslid in esl_power_info:
		for level in esl_power_info[eslid]:
			for apid in esl_power_info[eslid][level]:
				try:
					timeout_dict.setdefault(eslid, True)
					_, power_old, timelast = esl_power_info[eslid][level][apid]
					timeout = get_heartbeat_timeout(apid, timelast, ap_work_time, esl_timeout)
					if (timeNow - timelast) <= timeout: #注册信息未过期
						timeout_dict[eslid] = False
				except KeyError, e:
					pass

	esl_status_offline = []
	for eslid in timeout_dict:
		if timeout_dict[eslid] == True:
			esl_status_offline.append({"eslid":eslid, "status":"offline"})
	if esl_status_offline:
		reply_ack("ESL_STATUS", esl_status_offline, None)

def get_ap_level_of_esl(eslid, level_dict, ap_work_time):
	timeNow = time.time()

	all_list = []
	better_list = []
	best_list = []
	esl_timeout = float(conf.system.esl_heartbeat_timeout)
	
	l = level_dict.keys()
	l.sort()
	for level in l:
		for ap in level_dict[level].keys():
			level, rfpower, timelast = level_dict[level][ap]
			timeout = get_heartbeat_timeout(ap, timelast, ap_work_time, esl_timeout)
			if (timeNow - timelast) > timeout:
				continue
			all_list.append(ap)
			if level == P.BEST:
				best_list.append(ap)
				better_list.append(ap)
			if level == P.BETTER:
				better_list.append(ap)
			
	if not best_list:
		best_list = better_list
	if not best_list:
		best_list = all_list

	return best_list, better_list, all_list

def get_best_ap(db, eslid, esl_power_info, ap_work_time):
	best_list, better_list, all_list = get_ap_level_of_esl(eslid, esl_power_info, ap_work_time)
	#1.最好和次好的基站中挑选和本价签网络参数相符的
	esl_info = db.get_one(db.esl, eslid)
	group_esl_max = int(conf.netlink.group_num_max)

	ap_bind_count = db.bind_sort_nw1_nw3_op3(esl_info['nw1'], esl_info['nw3'], esl_info['op3'], group_esl_max) # 组ap绑定的价签数
	#加上为空的
	empty_list = list((set(best_list) | set(better_list)) - set([item[0] for item in ap_bind_count])) # 收到价签心跳，但是没有绑定关系的基站
	ap_bind_count.extend([(ap1, 0) for ap1 in empty_list])

	a1 = [item[0] for item in ap_bind_count]
	ap_list = list(set(a1) & (set(best_list) | set(better_list)))
	if ap_list: #如果不为空，则挑选绑定最多的返回
		for ap in a1:
			if ap in ap_list:
				return ap

	#最好的和次好的基站一起按照绑定数排序，去重后，取排名第二的基站进行绑定
	ap_bind_count = db.bind_sort_count()
	empty_list = list((set(best_list) | set(better_list)) - set([item[0] for item in ap_bind_count]))
	ap_bind_count.extend([(ap1, 0) for ap1 in empty_list])

	s, ap_list = {}, []
	for (ap, count) in ap_bind_count:
		if ap not in best_list and ap not in better_list:
			continue
		if count not in s:
			s[count] = ap
			ap_list.append(ap)
	if len(ap_list) >= 2:
		return ap_list[1]
	
	#3.还没有找到合适的基站，则选择第一个
	if not best_list:
		return None
	return best_list[0]
   
def refresh_bind_list(db, bind_request_list, esl_power_info, ap_work_time):

	bind_list = []
	
	for info in bind_request_list:
		eslid = info['eslid']
		try:
			esl_info = db.get_one(db.bind, eslid)
			apid, salesno = esl_info['apid'], esl_info['salesno']
		except Exception, e:
			continue #未绑定

		if eslid not in esl_power_info:
			continue
		
		best_ap = get_best_ap(db, eslid, esl_power_info[eslid], ap_work_time)
		if best_ap and apid != best_ap:
			ap = best_ap
			log.info("refresh_bind_list, bind eslid %s from %s to %s" % (eslid, apid, ap))
			bind_list.append({"eslid":eslid, "apid": ap, "salesno":salesno, "not_active":1})
		else:
			log.info("refresh_bind_list for %s, best_ap is %s" % (eslid, best_ap))
	
	return bind_list


auto_refresh_bind_at_hour_busy = False
def auto_refresh_bind_at_hour_fun():
	global auto_refresh_bind_at_hour_busy
	auto_bind_after_register = conf.htp.auto_bind_after_register.lower()
	auto_refresh_bind_at_hour = int(conf.htp.auto_refresh_bind_at_hour)

	try:
		if auto_refresh_bind_at_hour < 0 or auto_bind_after_register == 'yes' \
				or auto_refresh_bind_at_hour_busy:
			return

		tim = int(time.strftime('%H',time.localtime(time.time())))
		if tim == auto_refresh_bind_at_hour:
			bind.get_xmlserver().send_cmd("REFRESH_BIND", [])
			auto_refresh_bind_at_hour_busy = True
		else:
			auto_refresh_bind_at_hour_busy = False
	except Exception, e:
		log.error_msg("auto refresh bind failed:%s" % e, errid='EHB001')

def dump_ap_work_time(ap, ap_work_time_list):
	return 
	time_list = ap_work_time_list.get(ap, [])

def update_ap_work_time(ap, starttime, endtime, ap_work_time_list):
	time_list = ap_work_time_list.get(ap, [])
	time_list.append((starttime, endtime, endtime - starttime))
	for (s, e, u) in time_list[:]: #删除超期的
		if starttime - s > 24*3600: #保留一天以内的工作时间片
			time_list.remove((s, e, u))
	ap_work_time_list[ap] = time_list

def get_heartbeat_timeout(ap, timelast, ap_work_time_list, esl_timeout):
	time_list = ap_work_time_list.get(ap, [])
	count = esl_timeout
	
	for (s, e, u) in time_list:
		if s < timelast: #最后一次心跳之前的时间片不计算
			continue
		count += u #累计最有一次心跳之后，基站忙了多少时间
	return count
