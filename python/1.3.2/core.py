# encoding: utf-8

import esl_init, time
import cPickle as pickle
from htp import ack_ok, ack_ok_osd, ack_failed, ack_low_power, get_apid_from_ack,is_osd_ack
from htp import get_setid
import multiprocessing, time, os, platform, random, codecs, pprint, threading, Queue, json
import updata, query, bind, database, beacom, netlink, errno
from xmlserver import reply_ack
from heartbeat import update_ap_work_time, dump_ap_work_time, get_heartbeat_timeout
from heartbeat import get_good_list, get_bad_list, balanced_by_group
import main
from copy import deepcopy

from esl_init import conf, print_except

retry_max_of_eslid = {} #经过调准后的最大重试次数，失败的价签最大重试次数会被减为3
start_update_time_of_eslid = {}
esl_of_curr_sid = {}
esl_in_process = {}

def set_id_notbusy(ids):
	global esl_in_process
	esl_in_process.pop(ids, None)

def set_id_inprocess(ids):
	global esl_in_process
	for id1 in ids:
		esl_in_process[id1] = 1

def is_esl_in_process(id1):
	global esl_in_process
	if id1 in esl_in_process:
		return True
	return False

def count_online(db, ids):
	n = 0
	for id1 in ids:
		try:
			status = db[id1]['status']
			if 'online' in status or 'success' in status:
				n = n +1
		except Exception, e:
			pass
	return n

def count_priority(wakeup_group, esl_priority):
	n = 0
	prio = {}
	for id1 in wakeup_group:
		if id1 in esl_priority:
			prio[int(esl_priority[id1])] = 1
	
	s = prio.keys()
	s.sort()
	if not s:
		return 5

	return s[0]

def count_retry_min(wakeup_group, work_list):
	n = 0
	for id1 in wakeup_group:
		if id1 in work_list and work_list[id1] > n:
			n = work_list[id1]
	return n

def group_from_one_groups(groups, mode, flags, db, ap_groups, esl_priority = {}):
	'''
	找到一组，某个基站，某个信道，某个nw1，个数最大的
	groups形式 {(ap,ch,nw1):[first_updata_time, [id1, id2, id3, ....]]}
	返回[(ap, ch, wakeupid, ids, [slave aps], retry_times, {flag})]
	'''
	id_group = []

	del_groups = {}
	esl_update_timeout = int(conf.system.esl_update_timeout)
	max_set_wakeup = int(conf.htp.max_set_wakeup)

	group_level = {}
	for (ap, chn, nw1) in groups:
		wakeup_group = groups[(ap, chn, nw1)][1]
		group_level[(ap, chn, nw1)] = {}
		group_level[(ap, chn, nw1)]["high_priority_n"] = count_priority(wakeup_group, esl_priority)
		group_level[(ap, chn, nw1)]["online_n"] = count_online(db, wakeup_group)
		group_level[(ap, chn, nw1)]["esl_count"] = len(wakeup_group)
		group_level[(ap, chn, nw1)]["min_retry"] = count_retry_min(wakeup_group, mode['work_list'])
		group_level[(ap, chn, nw1)]['max_timeout'] = groups[(ap, chn, nw1)][0]

	while True:
		if len(groups) == 0:
			break
			
		#找到优先级最高的一组
		max_pri = 99
		max_pri_list = []
		for (ap, chn, nw1) in groups:
			if group_level[(ap, chn, nw1)]["high_priority_n"] < max_pri:
				max_pri = group_level[(ap, chn, nw1)]["high_priority_n"]
		for (ap, chn, nw1) in groups:
			if group_level[(ap, chn, nw1)]["high_priority_n"] == max_pri:
				max_pri_list.append((ap, chn, nw1))

		#优先处理距离step0超过10分钟的
		max_timeout = -1
		max_timeout_list = []
		for (ap, chn, nw1) in max_pri_list:
			if group_level[(ap, chn, nw1)]["max_timeout"] > esl_update_timeout:
				max_timeout = group_level[(ap, chn, nw1)]["max_timeout"]
		for (ap, chn, nw1) in max_pri_list:
			if group_level[(ap, chn, nw1)]["max_timeout"] == max_timeout:
				max_timeout_list.append((ap, chn, nw1))
		#esl_init.log.info("max_timeout_list:%s" % max_timeout_list)
		if len(max_timeout_list) == 0: #如果都是10分钟以内的，则无所谓先后
			max_timeout_list = max_pri_list
		
		#在从中找到重试次数最小的一组
		min_retry = 99
		min_retry_list = []
		for (ap, chn, nw1) in max_timeout_list:
			if group_level[(ap, chn, nw1)]["min_retry"] < min_retry:
				min_retry = group_level[(ap, chn, nw1)]["min_retry"]
		for (ap, chn, nw1) in max_timeout_list:
			if group_level[(ap, chn, nw1)]["min_retry"] == min_retry:
				min_retry_list.append((ap, chn, nw1))
		#esl_init.log.info("min_retry_list:%s" % min_retry_list)
		
		#再从中找到在线数最多的一组
		max_online = -1
		max_online_list = []
		for (ap, chn, nw1) in min_retry_list:
			if group_level[(ap, chn, nw1)]["online_n"] > max_online:
				max_online = group_level[(ap, chn, nw1)]["online_n"]
		for (ap, chn, nw1) in min_retry_list:
			if group_level[(ap, chn, nw1)]["online_n"] == max_online:
				max_online_list.append((ap, chn, nw1))

		#esl_init.log.info("max_online_list:%s" % max_online_list)
		#再从中找到价签个数最多的一组
		max_count = -1
		max_count_list = []
		for (ap, chn, nw1) in max_online_list:
			if group_level[(ap, chn, nw1)]["esl_count"] > max_count:
				max_count = group_level[(ap, chn, nw1)]["esl_count"]
		for (ap, chn, nw1) in max_online_list:
			if group_level[(ap, chn, nw1)]["esl_count"] == max_count:
				max_count_list.append((ap, chn, nw1))
		
		#esl_init.log.info("max_count_list:%s" % max_count_list)
		#再从中挑选第一个
		ap, chn, nw1 = max_count_list[0]
		wakeup_group = groups[(ap, chn, nw1)][1]
		find_ap, find_chn, find_nw1, find_ids = ap, chn, nw1, wakeup_group

		#找到重试轮次
		retry_max = 0
		for id1 in find_ids:
			if mode['work_list'][id1] > retry_max:
				retry_max = mode['work_list'][id1]

		ap_task_num = flags.setdefault('ap_task_num', {})
		task_id = ap_task_num.setdefault(find_ap, 0)

		id_group.append((task_id, find_ap, find_chn, find_nw1, find_ids, [], retry_max, flags))
		ap_task_num[find_ap] += 1
		flags.setdefault('ap_task_nw1', {}).setdefault(find_ap, []).append(find_nw1)

		groups.pop((find_ap, find_chn, find_nw1))
		if retry_max <= 6: 
			#再添加同基站下同类型的若干个组，尽量并组更新
			flags.setdefault('add_wk', {}).setdefault(find_ap, {})[task_id] = []
			add_wk = flags['add_wk'][find_ap][task_id]
			find_op3 = db[find_ids[0]]['op3']
			curr_len = get_ids_len(find_ids, add_wk)
			add_additional_group(mode, curr_len, add_wk, find_ap, find_chn, \
					find_op3, groups, db, find_ap)

			#如果还不饱和，则添加附近的基站进行通讯
			add_additional_group_from_slave_ap(mode, find_ids, add_wk, find_ap, \
					find_chn, ap_groups, find_op3, groups, db)
			#如果还不饱和，从已经删除的组里挑选通讯组
			add_additional_group_from_slave_ap(mode, find_ids, add_wk, find_ap, \
					find_chn, ap_groups, find_op3, del_groups, db)

		#删除除此基站外所有使用了此信道的分组
		#删除此基站内，所有不属于这个set的分组
		for (ap, chn, nw1) in groups.keys():
			if (ap != find_ap and (set(chn) & set(find_chn))) \
				or (ap == find_ap and not is_same_set(find_nw1, find_chn, nw1, chn)):
				del_groups[(ap, chn, nw1)] = groups.pop((ap, chn, nw1))

		if ap_task_num[find_ap] >= max_set_wakeup:
			#删除此基站和所有此信道
			for (ap, chn, nw1) in groups.keys():
				if (ap == find_ap) or (set(chn) & set(find_chn)):
					del_groups[(ap, chn, nw1)] = groups.pop((ap, chn, nw1))

	return id_group

def is_same_set(find_nw1, find_chn, nw1, chn):
	return get_setid(find_nw1) == get_setid(nw1) and find_chn[0] == chn[0]

def get_ids_len(find_ids, add_wk):
	ret = 0
	ret += len(find_ids)
	for (nw1, chn, ids) in add_wk:
		ret += len(ids)
	
	return ret

def add_additional_group_from_slave_ap(mode, find_ids, add_wk, find_ap, find_chn, ap_groups, find_op3, groups, db):
	for slave_ap1 in ap_groups[find_ap]:
		slave_ap1 = str(slave_ap1)
		#查看此AP是否可以加入到附加的任务列表
		curr_len = get_ids_len(find_ids, add_wk)
		add_additional_group(mode, curr_len, add_wk, slave_ap1, find_chn, find_op3, groups, db, find_ap)

def add_additional_group(mode, curr_len, add_wk, find_ap, find_chn, find_op3, groups, db, htp_ap):
	max_wakeup_group = int(conf.htp.max_wakeup_group)
	max_wakeup_esl = int(conf.htp.max_wakeup_esl)

	if max_wakeup_group <= 0 or max_wakeup_group > 5 or conf.extend_service.apv3_enable.lower == 'yes':
		return
	
	for (ap, chn, nw1) in groups.keys():
		if curr_len > max_wakeup_esl: #超出单组限制
			break
		if len(add_wk) >= max_wakeup_group -1: #超出容量限制
			break
		if ap != find_ap or chn != find_chn: #基站不相等, 或信道不相同
			continue
		ids = groups[(ap, chn, nw1)][1] #类型不相等
		if db[ids[0]]['op3'] != find_op3:
			continue
		if 'HS_EL_51' not in db[ids[0]]['op3']: #非点阵价签
			continue
		if len(ids) + curr_len > max_wakeup_esl: #超出容量限制
			continue
		#找到一组合适的
		#但要刨除此基站没有收到心跳信息的
		for i in range(len(ids)-1, -1, -1):
			if htp_ap not in mode['ap_check_list'].get(ids[i], []):
				del ids[i]
		if len(ids) > 0:
			curr_len += len(ids)
			add_wk.append((nw1, chn, ids))
		groups.pop((ap, chn , nw1))

def sava_ap_list(db):
	ap_list = get_ap_group(db)
	with open("config/ap_list.ini","w") as f:
		f.write(json.dumps(ap_list, indent = 4))

def get_ap_group(not_use):
	from osd import _init_esl_json

	try:
		ap_list = _init_esl_json("config/ap_list.ini", is_epd = False, is_airspeed = False)
	except KeyError, e:
		ap_list = {}

	db = database.DB()
	ap_db = [str(ap1) for ap1 in db.get_all_ap()]

	for group_name in ap_list:
		for ap1 in ap_list[group_name].keys():
			if str(ap1) not in ap_db and ap1 != '-1':
				ap_list[group_name].pop(ap1)
			else:
				for ap_slave in ap_list[group_name][ap1][:]:
					#如果辅助基站不在数据中，则将其从辅助基站里删除
					if str(ap_slave) not in ap_db:
						ap_list[group_name][ap1].remove(ap_slave)

	#如果基站在数据库中有，但不在配置文件中
	is_change = False
	for ap1 in ap_db:
		ap1 = str(ap1)
		for group_name in ap_list:
			if ap1 in ap_list[group_name].keys():
				break
		else:
			ap_list.setdefault("DEFAULT_GROUP", {})[str(ap1)] = []
			is_change = True

	if is_change:
		with open("config/ap_list.ini","w") as f:
			f.write(json.dumps(ap_list, indent = 4))

	return ap_list

def get_default_ap(db, ap, ap_list):
	ap = str(ap)
	default_ap_list = []

	for k in ap_list:
		#要查找和某基站同个group内的默认基站
		if ap in ap_list[k] or ap == "NONE":
			default_ap_list = ap_list[k].get('-1', [])
			break

	default_ap_list = [str(ap) for ap in default_ap_list]

	default_ap_list = db.bind_sort_count(include_ap_list = default_ap_list, \
				exclude_ap_list = [], count_max = conf.netlink.group_num_max)

	default_ap_list = balanced_by_group(default_ap_list)

	return default_ap_list

def is_switch_to_roaming_mode(esl_info, retry_times):

	enable_roming = str(conf.htp.enable_roaming).upper()
	if enable_roming != "YES":
		return False

	if esl_info['nw4'] == 'NORMAL':
		if retry_times == 3:
			return True
	if esl_info['nw4'] == 'DOT20':
		if retry_times == 5:
			return True
	return False

def _fill_roaming_ap(ap_list, n):
	ap, i = [], 0
	if not ap_list:
		return []
	while n:
		ap.append(ap_list[i % len(ap_list)])
		i += 1
		n -= 1
	return ap

def fill_roaming_ap(all_ap, good_list, n):
	good = []

	for ap in good_list:
		if ap not in all_ap:
			good.append(ap)
	
	return _fill_roaming_ap(good, n)

def change_to_roaming_list(db, id1, esl_power_info, esl_power_his, \
			ap, ap_work_list, retry_times, ap_work_time, esl_power_last_time):

	#按照心跳的时间新旧，作为漫游列表
	new_list = get_bad_list(db, id1, esl_power_info.get(id1, {}), \
										esl_power_his.get(id1, {}), ap_work_time,
										esl_power_last_time.get(id1, {}),
										)
	default_list = get_default_ap(db, ap, get_ap_group(None))
	
	for ap1 in new_list[:]:
		if not db.has_key(db.ap, ap1):
			esl_init.log.warning("ap %s not in db for eslid %s" % (ap1, id1))
			new_list.remove(ap1)

	for ap1 in default_list[:]:
		if not db.has_key(db.ap, ap1):
			esl_init.log.warning("ap %s not in db for eslid %s" % (ap1, id1))
			default_list.remove(ap1)

	max_len = len(ap_work_list)
	all_ap = ap_work_list[:]
	all_ap.extend(default_list)
	#均衡填充
	roaming_list = fill_roaming_ap(all_ap, new_list, max_len - retry_times)
	if roaming_list:
		ap_work_list = ap_work_list[:0-len(roaming_list)]
		ap_work_list.extend(roaming_list)
	
	#最后填充默认基站
	if default_list:
		els_n = max_len - retry_times - len(roaming_list)
		if els_n <= 0:
			ap_work_list[-1] = default_list[0]
		else:
			ext_def = _fill_roaming_ap(default_list, els_n)
			ap_work_list = ap_work_list[:0-len(ext_def)]
			ap_work_list.extend(ext_def)

	esl_init.log.info("switch eslid %s to roaming mode, roaming list is %s, base on new ap %s, default ap %s" % \
			(id1, ap_work_list, new_list, default_list))
	return ap_work_list

def get_all_ap_list(id1, esl_power_info, ap_work_time, defaultap, retry_max):
	ap_fix = [defaultap] * retry_max
	return ap_fix

def group_from_groups(groups, mode, db, flags, esl_priority = {}):
	'''把整个基站分为n组，每组内m个基站；组间并行；组内可并、串行'''
	ap_groups = get_ap_group(db)
	ap_group_pro = {}

	#把所有的任务都分布基站组内
	for (ap, chn, nw1) in groups:
		for group_name in ap_groups:
			for ap1 in ap_groups[group_name].keys():
				if int(ap1) == int(ap)\
					and ((group_name not in ap_group_pro) or (ap1 not in ap_group_pro[group_name])):

					ap_group_pro.setdefault(group_name,{}).update({(ap,chn,nw1):groups[(ap,chn,nw1)]})
	
	ap_group_list = []
	used_ap_list = []
	
	for group_name in ap_group_pro:
		#组内再挑出可以并行的基站
		id_group = group_from_one_groups(ap_group_pro[group_name], mode, flags, db, \
							ap_groups[group_name], esl_priority = esl_priority)
		
		ap_group_list.extend(id_group)
		
	return ap_group_list
	
def groups_extend_one(groups, ap, chn, nw1, ids, updata_time):
	if (ap, chn, nw1) not in groups:
		groups[(ap, chn, nw1)] = [0, []]
	groups[(ap, chn, nw1)][1].append(ids)
	#给每一组加上一个时间戳，作为排序参考值之一
	elapse_time = time.time() - updata_time
	if elapse_time > groups[(ap, chn, nw1)][0]: #first_updata_time 存储每组中更新请求最早的
		groups[(ap, chn, nw1)][0] = elapse_time

def is_id_ok(db, id1):
	'''删除属性有问题的价签'''
	try:
		bindinfo = db.get(id1, None)
		if not bindinfo:
			esl_init.log.error_msg("get bind info failed for esl %s" % (id1), errid='ECO001', eslid=id1)
			return False

		ap = db.get(id1, None)
		if not ap:
			esl_init.log.error_msg("get ap info failed for esl %s" % (id1), errid='ECO002', eslid=id1)
			return False
		
		ei = db.get(id1, None)
		if not ei:
			esl_init.log.error_msg("get esl info failed for esl %s" % (id1), errid='ECO003', eslid=id1)
			return False
		
		try:
			op5 = eval(ei['op5'], {}, {})
		except Exception, e:
			esl_init.log.error_msg("get esl op5 failed for esl %s" % (id1), errid='ECO004', eslid=id1)
			return False

		try:
			op6 = eval(ei['op6'], {}, {})
		except Exception, e:
			esl_init.log.error_msg("get esl op6 failed for esl %s" % (id1), errid='ECO005', eslid=id1)
			return False

		if None in [ap.get('apid', None), ap.get('apip', None), ap.get('listenport', None)]:
			esl_init.log.error_msg("ap info error for esl %s" % id1, errid='ECO006', eslid=id1)
			return False
		if None in [ei['nw1'], ei['nw2'],ei['nw3'],ei['nw4'],ei['op2'],ei['op3']]:
			esl_init.log.error_msg("esl info error for esl %s" % id1, errid='ECO007', eslid=id1)
			return False
		if ei['nw4'] not in ['NORMAL', 'DOT20']:
			esl_init.log.error_msg("esl type error for esl %s" % id1, errid='ECO008', eslid=id1)
			return False
		if ei['nw4'] == "DOT20" and (ei['op4'] == "none" or ei['op3'] == None):
			esl_init.log.error_msg("esl template error for dot esl %s" % id1, errid='ECO009', eslid=id1)
			return False
		if "HS" not in ei['op3']:
			esl_init.log.error_msg("esl type '%s' error for esl %s" % (ei['op3'], id1), errid='ECO010', eslid=id1)
			return False
	except KeyError, e:
		esl_init.log.error_msg("get info of esl %s error, %s" % (id1, e), errid='ECO011', eslid=id1)
		return False
	return True


def get_retry_max_time(id1, item = {}):
	fix_retry_time_for_5103 = int(conf.htp.fix_retry_time_for_5103)
	fix_retry_time_for_5033 = int(conf.htp.fix_retry_time_for_5033)

	try:
		retry_max = int(item['op8'])
	except Exception, e:
		retry_max = 6
		#老价签没有op8值
		if "5103" in item['op3']:
			retry_max = fix_retry_time_for_5103
		if "5033" in item['op3']:
			retry_max = fix_retry_time_for_5033

	prov_retry_max = retry_max

	try:
		status = item['status']
	except Exception, e:
		status = None

	global_retry_time_max = int(conf.htp.global_retry_time_max)
	failed_retry_time_max = int(conf.htp.failed_retry_time_max)

	if global_retry_time_max > 0:
		retry_max = global_retry_time_max
	if status and ('offline' in status or 'failed' in status):
		retry_max = failed_retry_time_max #失败的价签只重试3次
	
	if retry_max <= 0:
		retry_max = 1
	if prov_retry_max <= 0:
		prov_retry_max = 1
	
	if retry_max > prov_retry_max:
		retry_max = prov_retry_max

	return retry_max, prov_retry_max

def yield_one_item_2(db, ids):
	ap, chn, nw1,  wrong_id, updata_time, retry_max, prov_retry_max = \
		None, None, None, None, None, None, None
	wrong_id = ids
	if is_id_ok(db, ids):
		wrong_id = None
		ap = db[ids]['apid']
		item = db[ids]
		status = item['status']
		chn, nw1, updata_time = item['nw3'], item['nw1'], item['lastworktime']
		try:
			setchn = int(item['setchn'])
			setchn = item['setchn']
		except Exception, e:
			setchn = nw1

		try:
			grpchn = int(item['grpchn'])
			grpchn = item['grpchn']
		except Exception, e:
			grpchn = nw1
		
		chn = (setchn, grpchn, chn)

		retry_max, prov_retry_max = get_retry_max_time(ids, item)
		if ids not in retry_max_of_eslid:
			retry_max_of_eslid[ids] = retry_max
		if not updata_time:
			updata_time = time.asctime()
		
	return (ap, chn, nw1, ids, updata_time, prov_retry_max, wrong_id)

def yield_one_item(db, id_list):
	ap, chn, nw1, ids, wrong_id, updata_time, retry_max, prov_retry_max = \
		None, None, None, None, None, None, None, None
	for ids in id_list:
		wrong_id = ids
		if is_id_ok(db, ids):
			wrong_id = None
			ap = db[ids]['apid']
			item = db[ids]
			status = item['status']
			chn, nw1, updata_time = item['nw3'], item['nw1'], item['lastworktime']

			try:
				setchn = int(item['setchn'])
				setchn = item['setchn']
			except Exception, e:
				setchn = nw1

			try:
				grpchn = int(item['grpchn'])
				grpchn = item['grpchn']
			except Exception, e:
				grpchn = nw1
			
			chn = (setchn, grpchn, chn)

			retry_max, prov_retry_max = get_retry_max_time(ids, item)
			if ids not in retry_max_of_eslid:
				retry_max_of_eslid[ids] = retry_max
			if not updata_time:
				updata_time = time.asctime()
		
		yield (ap, chn, nw1, ids, updata_time, prov_retry_max), wrong_id

def group_ids_by_chn(id_list, mode, db, flags, esl_power_info, ap_work_time, esl_priority = {}):
	#将ap，chn，ids归并到字典中 {(ap,ch,nw1):[first_updata_time, [id1, id2, id3, ....]]}
	#这个函数只用于漫游
	
	groups, wrong_ids = {}, []

	for (ap, chn, nw1, ids, updata_time, retry_max), wrong_id in yield_one_item(db, id_list):
		if wrong_id:
			wrong_ids.append(wrong_id)
			continue
		if ids not in mode["ap_check_list"]:
			mode["ap_check_list"][ids] = get_all_ap_list(ids, esl_power_info, ap_work_time, ap, retry_max)
			start_update_time_of_eslid[ids] = time.time()
		
		ap = mode["ap_check_list"][ids][mode['work_list'][ids]]
		groups_extend_one(groups, ap, chn, nw1, ids, start_update_time_of_eslid[ids])

	id_group = group_from_groups(groups, mode, db, flags, esl_priority = esl_priority)

	return id_group, wrong_ids

def is_osd_esl(db, id1):
	ei = db.get(id1, None)
	if not ei:
		return False

	if ei['nw4'] == "DOT20":
		return True
	else:
		return False
	
def filter_groups(db, groups):
	# 过滤不同组通信中的相同价签id
	id_group = groups
	
	all_ids = set([])
	# 添加所有组通信价签id到集合中
	for item in id_group:
		all_ids |= set(item[3])

	# 每组价签id与集合比较，分别取到不同的id
	for item in id_group:
		ids = set(item[3])
		if ids.issubset(all_ids):
			all_ids -= ids
			ids.clear()
		else:
			temp = all_ids & ids
			ids -= temp
			all_ids -= temp
		while ids:
			#item[3].remove(ids.pop())
			id1 = ids.pop()
			if is_osd_esl(db, id1):
				item[3].remove(id1)

		if not item[3]:
			id_group.remove(item)

	return id_group

yield_one_item_cache = {}
def get_item_form_cache(db, id1, work_list):
	global yield_one_item_cache

	if id1 not in yield_one_item_cache or work_list[id1] == 0:
		yield_one_item_cache[id1] = yield_one_item_2(db, id1)
	
	return yield_one_item_cache[id1]

def group_ids_by_ap(id_list, mode, db, flags, esl_power_info, ap_work_time, esl_priority = {}):
	#将ap，chn，ids归并到字典中 {(ap,ch,nw1):[first_updata_time, [id1, id2, id3, ....]]}
	groups, wrong_ids = {}, []

	#for (ap, chn, nw1, ids, updata_time, retry_max), wrong_id in yield_one_item(db, id_list):
	for id1 in id_list:
		ap, chn, nw1, ids, updata_time, retry_max, wrong_id = get_item_form_cache(db, id1, mode['work_list'])
		if wrong_id:
			wrong_ids.append(wrong_id)
			continue
		#首次更新时获取价签的所有基站列表，当更新失败时移除一个
		if (ids not in mode["ap_check_list"]) or mode['work_list'][ids] == 0:
			mode["ap_check_list"][ids] = get_all_ap_list(ids, esl_power_info, ap_work_time,ap, retry_max)
			start_update_time_of_eslid[ids] = time.time()
			#如果属于OSD的首次传输，则清空它之前的ack值
			if "OSD" in flags and 'osd_last_ack' in flags:
				flags['osd_last_ack'][ids] = []

		#单个价签不再并行更新,减少系统复杂度
		ap = mode["ap_check_list"][ids][mode['work_list'][ids]] #每次取最头1个基站进行更新
		groups_extend_one(groups, ap, chn, nw1, ids, start_update_time_of_eslid[ids])

	id_group = group_from_groups(groups, mode, db, flags, esl_priority = esl_priority)
	#id_group [(ap, ch, wakeupid, ids, [slave aps], retry_times, {flags})]

	return id_group, wrong_ids

def group_ids_by_para(id_list, mode, db, flags, esl_power_info,ap_work_time, esl_priority = {}):
	#将ap，chn，ids归并到字典中 {(ap,ch,nw1):[first_updata_time, [id1, id2, id3, ....]]}
	#这个函数只用于组网
	groups, wrong_ids, id_groups = {}, [], []

	para = flags.get('NETLINK', {})

	group_step = None

	for (ap, chn, nw1, ids, updata_time, retry_max), wrong_id in yield_one_item(db, id_list):
		if wrong_id:
			wrong_ids.append(wrong_id)
			continue
		if ids not in mode["ap_check_list"] or mode['work_list'][ids] == 0:
			mode["ap_check_list"][ids] = get_all_ap_list(ids, esl_power_info, ap_work_time, ap, retry_max)
			start_update_time_of_eslid[ids] = time.time()
		
		# 使用新无线通信参数发送查询命令
		if para:
			#esl_init.log.info("rf_para: %s" % para)
			wid, ch, step, netid, setchn, grpchn = para[ids]
			if step == 'query':
				nw1 = wid
				chn = (setchn, grpchn, ch)

			#避免对同一个组既进行组网又进行查询
			if group_step == None:
				group_step = step
			if step != group_step:
				continue

			db[ids]['data_cmd'] = 'CMD_QUERY' if step == 'query' else 'CMD_NETLINK'

		else:# 无组网需要的新的通信参数
			wrong_ids.append(ids)
			continue

		#单个价签不再并行更新,减少系统复杂度
		ap = mode["ap_check_list"][ids][mode['work_list'][ids]]
		groups_extend_one(groups, ap, chn, nw1, ids, start_update_time_of_eslid[ids])

	id_group = group_from_groups(groups, mode, db, flags, esl_priority = esl_priority)

	for group in id_group:
		task_id,	find_ap, find_chn, find_nw1, find_ids, slave_ap, retry_max, flag = group
		flag.update({"OSD":"","NETLINK":{}})
		flag["NETLINK"] = para
		#for id1 in find_ids:
		#	flag["NETLINK"].setdefault(id1, para[id1])
		# [(ap, ch, wakeupid, ids, [slave aps], retry_times, {flag})]
		id_groups.append((task_id, find_ap, find_chn, find_nw1, find_ids, slave_ap, retry_max, flag))

	#esl_init.log.info("id_groups: %s" % id_groups)

	return id_groups, wrong_ids

def max_retry_times(groups):
	max_retry = 0
	for group in groups:
		if group[5] > max_retry:
			max_retry = group[5]
	return max_retry

def task_schedu(groups):
	#task_num = 1 #不开启基站并行模式
	task_num = len(groups) #一直开启基站并行模式
	return task_num

	#按照时间段分配并行机制
	#晚上21点到早上10点，只并行2次
	max_retry = max_retry_times(groups)
	tim = int(time.strftime('%H',time.localtime(time.time())))
	if tim > 21 or tim < 10:
		task_num = 1 if max_retry >= 4 else len(groups)
	else:
		task_num = 1 if max_retry >= 6 else len(groups)

	return task_num

def is_esl_in_ack_list(id1, ack_list):
	'''ack_list格式为 [(id1, (apid, packnum, ack, osd_flag))]'''
	for ack in ack_list:
		if id1 == ack[0]:
			return True
	return False

def get_temp_id_dict(ack_list):
	t = {}
	for ack in ack_list:
		t[ack[0]] = 1
	
	return t

def osd_ack_pack(ack_list, osd_ack1):
	#每一次都需要把上一次的OSD_ACK清除掉
	#esl_init.log.debug("ack_list in core:%s" % ack_list)
	#esl_init.log.debug("osd_ack in core:%s" % osd_ack1)
	osd_ack = {}
	temp_id_dict = get_temp_id_dict(ack_list)

	for id1 in osd_ack1.keys(): #如果价签这回没有被更新到，它的lastack值需要被保留住
		#if not is_esl_in_ack_list(id1, ack_list):
		if id1 not in temp_id_dict:
			osd_ack[id1] = osd_ack1[id1][:]
		else:
			osd_ack[id1] = []

	for (id1,(ap, n, ack, cmd)) in ack_list:
		#if cmd != "OSD":
		if not is_osd_ack((ap, n, ack, cmd)):
			continue
		if id1 not in osd_ack:
			esl_init.log.warning("recv wrong ack: (%s, (%s, %s, %s, %s))" % (id1, ap, n, ack, cmd))
			continue
		if len(osd_ack[id1]) == n: 
			osd_ack[id1].append(0)  #ACK不存在, 默认为0 
		#if ack_ok_osd((ap, n, ack, cmd)):
		osd_ack[id1][n] = ack   #所有值都透传
	
	#合并OSD ACK为标准的ACK值, 将多个ACK合并为1个,有1为0，无1为0
	#但OSD价签只能出现1个基站的ACK
	#但只处理标志为OSD的ack包
	save_list = {}
	for (id1,(ap, n, ack, cmd)) in ack_list:
		if cmd != "OSD":
			continue
		if (id1, ap) not in save_list:
			save_list[(id1, ap)] = (id1,(ap, n, ack, cmd))
		if ack_ok_osd((ap, n, ack, cmd)): #osd包传成功
			save_list[(id1, ap)] = (id1,(ap, n, 1, cmd))

	#将OSDack从ack_list中删除，后面将扩展osdack为标准的ack值
	for (id1,(ap, n, ack, cmd)) in ack_list[:]:
		#if cmd == "OSD":
		if is_osd_ack((ap, n, ack, cmd)):
			ack_list.remove((id1,(ap, n, ack, cmd)))
	
	ack_list.extend(save_list.values())

	#esl_init.log.debug("last_ack from core:%s" % osd_ack)
	return osd_ack
	
def pool_action(task_name, groups, action, ap_work_time):
	'''
	并发执行action函数，回收ack值
	入参为group_ids的输出，为一组可以并发的id清单。
	函数将调用pool.map方法，开启n个（由入参的len决定）进程，并等待它们结束，
	最后汇集各个进程的输出做为ACK返回.
	返回值为 [(id1, ack), (id2, ack), (id3, ack), ...]
	'''
	task_num = task_schedu(groups)
	starttime = time.time()

	for (apid, _, _, _, _, _, _) in groups:
		dump_ap_work_time(apid, ap_work_time)

	pool = multiprocessing.Pool(processes = task_num)
	try:
		pool_output = []
		pool_output = pool.map(action, groups)
	except Exception, e:
		pool.terminate()
		esl_init.log.error_msg("pool:%s" % e, errid='ECO012')
	finally:
		pool.close()
		pool.join()
	
	endtime = time.time()
	for (apid, _, _, _, _, _, _) in groups:
		update_ap_work_time(apid, starttime, endtime, ap_work_time)

	return [v for acks in pool_output for v in acks]

def pool_action_thread(task_name, groups, action, ap_work_time, all_info):
	'''
	并发执行action函数，回收ack值
	入参为group_ids的输出，为一组可以并发的id清单。
	函数将调用pool.map方法，开启n个（由入参的len决定）进程，并等待它们结束，
	最后汇集各个进程的输出做为ACK返回.
	返回值为 [(id1, ack), (id2, ack), (id3, ack), ...]
	'''
	task_num = task_schedu(groups)
	starttime = time.time()

	for (_, apid, _, _, _, _, _, _) in groups:
		dump_ap_work_time(apid, ap_work_time)

	q = Queue.Queue()
	thr_list, ids_list, wrong_ids, i = [], [], [], 0
	for group in groups:
		task_id, apid, chn, wakeupid, ids, slaveap, retry_times, flags = group
		args1 = (task_id, apid, chn[2], wakeupid, ids, slaveap, retry_times, flags, q, all_info)
		thr_list.append(threading.Thread(target = action, args=(args1,)))
		ids_list.append(ids)
	for thr in thr_list:
		thr.start()
	for thr in thr_list:
		thr.join(360) #最多等待360秒
		try:
			if thr.isAlive():
				esl_init.log.error("htp task timeout, cancel the job %s" % ids_list[i])
				wrong_ids.extend(ids_list[i])
		except Exception, e:
			pass
		i += 1

	pool_output = []
	while not q.empty():
		pool_output.append(q.get())

	endtime = time.time()
	for (_, apid, _, _, _, _, _, _) in groups:
		update_ap_work_time(apid, starttime, endtime, ap_work_time)

	return pool_output, wrong_ids
	#return [v for acks in pool_output for v in acks]

#取空队列q中的所有元素，返回一个字典，key为元素，值为0
#返回值: {item:0, ...}
def fetch_all(q, task_data, db):
	global esl_of_curr_sid
	d = {}
	while True:
		if q.empty():
			time.sleep(0.2)
			break

		while not q.empty():
			eslid, info = q.get()
			d[eslid] = 0
			task_data['all_info'][eslid] = info

			if eslid in task_data['rf_para_is_changed']:
				task_data['rf_para_is_changed'].pop(eslid)
				check_esl_info(db, task_data['all_info'], eslid, task_data, 0)

			if 'sid' in info:
				esl_of_curr_sid[eslid] = info['sid']
		time.sleep(0.7)

	return d

def check_esl_info(db, all_info, ids, task_data, retry_times):
	ed  = db.get_all_info(db.esl, ids)
	em = all_info[ids]

	if retry_times % 2 == 1 and ids in task_data['netlink']['rf_para'] and \
		task_data['netlink']['work_list'].get(ids, 0) > 0:
		#奇数次重试时，且价签已经开始组网，则从组网参数里查
		nw1, nw3, step, op2, setchn, grpchn = task_data['netlink']['rf_para'][ids]
	else:
		#否则始终使用数据库值
		nw1, setchn, grpchn, nw3, op2 = ed['nw1'], ed['setchn'], ed['grpchn'], ed['nw3'], ed['op2']
	
	all_info[ids].update({'nw1':nw1, 'setchn':setchn, 'grpchn':grpchn, 'nw3':nw3, 'op2':op2})
	yield_one_item_cache.pop(ids, None)	

def is_set_cmd_finished(ids, info):
	if info.get('data_cmd', None) != 'CMD_SET_CMD':
		return False
	setid = info['nw1'].split('-')
	setid[2] = "00"
	setid = '-'.join(setid)
	setcmd = info.get("setcmd", '')
	setargs = info.get("setargs", [])
	apid = info.get("apid", '')
	esl_init.log.info("set cmd %s args %s for %s success on apid %s" % (setcmd, setargs, setid, apid))
	reply_ack("SET_CMD_ACK", [{"setid":setid, "setcmd":setcmd, "setargs":setargs}], None)
	
	return True

def check_need_roaming(db, ids, all_info, mode, task_data, ack):
	if is_switch_to_roaming_mode(all_info[ids], mode['work_list'][ids]):
		mode['ap_check_list'][ids] = change_to_roaming_list(db, ids, 
						task_data['esl_power_info'], 
						task_data['esl_power_his'], 
						get_apid_from_ack(ack), 
						mode['ap_check_list'][ids], 
						mode['work_list'][ids], 
						task_data['ap_work_time'],
						task_data['esl_power_last_time'],
						)

def process_ack(module_name, group_list, ack_list, mode, db, all_info, task_data, esl_priority = {}):
	
	if module_name == "beacom":
		beacom.check_ack(group_list, ack_list, mode, retry_max_of_eslid)
		return
	
	if module_name == "netlink":
		netlink.check_ack(group_list, ack_list, mode, db, retry_max_of_eslid, task_data)
		return

	#esl_init.log.info("ack_list:%s" % ack_list)
	beacom_list = []
	for ids, ack in ack_list:
		ids = ids.upper()
		if ids not in mode['work_list']: #说明已经通讯成功，已经被删除，后面的ACK值没有用
			continue

		if (ack_ok(ack) or ack_low_power(ack)):
			is_set = is_set_cmd_finished(ids, all_info[ids])
			if not is_set:
				esl_init.log.info("%s esl %s retry %s times success" % (module_name, ids, mode['work_list'][ids]))                        
			mode['work_list'].pop(ids, None) #从队列中删除
			if not is_set:
				mode['out_queue'].put((ids, ack, esl_of_curr_sid.get(ids, "NONE"))) #处理成功，返回成功的ID
			mode["ap_check_list"].pop(ids)
			esl_priority.pop(ids, None)
			retry_max_of_eslid.pop(ids, None)
			db.set_last_status_without_commit(db.esl, ids, time.asctime(), "online")

			if module_name == "updata":
				db.increace_status(ids, ["refresh_times"])

			if module_name == "bind":	#bind的q只作为解绑用
				db.remove_key(db.bind, ids) #刷新完OFF后即刻删除绑定关系
			if module_name == 'query':
				set_id_notbusy(ids)
		else: #通讯失败
			mode['work_list'][ids] += 1 
			
			#如果通讯失败，则从数据库或组网参数加载通讯参数
			check_esl_info(db, all_info, ids, task_data, mode['work_list'][ids]) 
			check_need_roaming(db, ids, all_info, mode, task_data, ack)

			#如果是osd价签，且链路层更新成功，则取消其失败状态，将重试次数恢复成正常值。
			if ack_ok_osd(ack):
				item = all_info.get(ids)
				retry_max, prov_retry_max = get_retry_max_time(ids, item)
				if retry_max_of_eslid[ids] < prov_retry_max:
					esl_init.log.info("change retry max from %s to %s for esl %s" % 
						(retry_max_of_eslid[ids], prov_retry_max, ids))
					retry_max_of_eslid[ids] = prov_retry_max
			#漫游失败
			if retry_max_of_eslid.get(ids, 5) <= mode['work_list'][ids]:
				esl_init.log.info("%s esl %s retry %s times failed" % (module_name, ids, mode['work_list'][ids]))
				salesno = all_info[ids].get("salesno", "NONE")				
				mode['work_list'].pop(ids, None) #从队列中删除
				mode['out_queue'].put((ids, ack_failed(apid = get_apid_from_ack(ack)), 
												esl_of_curr_sid.get(ids, "NONE"))) #错误数超过5次，返回失败
				mode["ap_check_list"].pop(ids, None)
				esl_priority.pop(ids, None)
				retry_max_of_eslid.pop(ids, None)
				db.set_last_status_without_commit(db.esl, ids, time.asctime(), "offline")
				beacom_list.append(ids)

				if module_name == "updata":
					db.increace_status(ids, ["failed_times"])

				if module_name == "bind":	#bind的q只作为解绑用
					db.remove_key(db.bind, ids) #刷新完OFF后即刻删除绑定关系

				if module_name == 'query':
					set_id_notbusy(ids)

	beacom.beacom_find_esl(beacom_list)

def load_esl_power_info(info, ap_list):
	try:
		f = open("log/esl_power_info.pkl", "r")
		info1 = pickle.load(f)
		f.close()
		info.update(info1)

		for eslid in info.keys():
			for level in info[eslid].keys():
				for apid in info[eslid][level].keys():
					if apid not in ap_list:
						esl_init.log.info("load hb history for eslid %s, but apid %s not in ap_list, skip this hb" \
							% (eslid, apid))
						info[eslid][level].pop(apid, None)
				if not info[eslid][level]:
					info[eslid].pop(level, None)
			if not info[eslid]:
				info.pop(eslid, None)

	except KeyboardInterrupt, e:
		raise KeyboardInterrupt, "KeyboardInterrupt"
	except Exception, e:
		pass
	
def save_esl_power_info(info):
	try:
		ninfo = {}
		klist = info.keys()
		for k in klist:
			if k in info:
				ninfo[k] = info[k]
		with open("log/esl_power_info.pkl", "w") as f:
			pickle.dump(ninfo, f)
	except KeyboardInterrupt, e:
		raise KeyboardInterrupt, "KeyboardInterrupt"
	except  Exception, e:
		esl_init.log.warning("save_esl_power_info:%s" % e)

data_cmd_arr = {"updata":"CMD_UPDATE", "bind":"CMD_UNBIND", "query":"CMD_QUERY", 
		"netlink":"CMD_NETLINK", "beacom":"CMD_QUERY", "set_only_q":"CMD_SET_CMD"}

def update_data_cmd(mode, work_list, all_info):
	data_cmd = data_cmd_arr.get(mode)
	for id1 in work_list:
		try:
			all_info[id1]['data_cmd'] = data_cmd
		except KeyError, e:
			esl_init.log.error_msg("update data cmd to %s for eslid %s failed" % (data_cmd, id1), errid='ECO014')

def process(task_data):
	'''
	core进程的主循环，将不断（1秒间隔）的从任务队列中取出id，更新到任务清单(work_list)中。
	如果work_list不为空，则调用group_ids获得一组任务，发送给poll_action进行处理，并根据
	处理结果更新work_list：成功，则将id从work_list中删除，失败则在下次重试，直至超过最大
	失败值。
	函数没有入参和处参，通过队列和其他进程进行通信
	'''
	esl_init.log.info("core_process starting")
	#modes 是一组要处理的任务对象，它包含了入队队列，出队队列，工作列表，和单次任务的回调函数
	modes = ["bind", "updata", "netlink", "set_only_q", "query", "beacom"] #处理任务的优先顺序
	db = database.DB()

	while True:
		try:
			if task_data['isquit']['core']:
				break
			group_list = []
			for task_name in modes:
				mode = task_data[task_name]
				new_list = fetch_all(mode['in_queue'], task_data, db)
				mode['work_list'].update(new_list)
				if not mode['work_list']:
					continue;	#如果work_list为空，则执行下一个任务
					
				update_data_cmd(task_name, mode['work_list'], task_data['all_info']) 
				#从work_list中取出一组可以并发的id
				flags = {"OSD":""}
				flags['ack_count'] = task_data['ack_count']
				flags['osd_last_ack'] = task_data['osd_last_ack']
				flags['apv3'] = task_data.get("apv3", None)
				if task_name == 'beacom':
					group_fun = group_ids_by_chn
				elif task_name == 'netlink':
					group_fun = group_ids_by_para
					flags.setdefault("NETLINK", mode['rf_para'])
				else:
					group_fun = group_ids_by_ap
				group_list, wrong_ids = group_fun(mode['work_list'].keys(), mode, task_data['all_info'], flags, \
							task_data['esl_power_info'], task_data['ap_work_time'],\
							esl_priority = task_data['esl_priority'])
				if task_name == 'updata':
					group_list = filter_groups(task_data['all_info'], group_list)
				if len(wrong_ids) > 0:
					wrong_id_act(db, wrong_ids, mode, task_name, task_data)
					continue
				if len(group_list) == 0:
					continue
				#传入一组ID，进行更新处理，返回ID和ACK值的元组列表
				ack_list, wrong_ids = pool_action_thread(task_name, group_list, mode['action'], task_data['ap_work_time'],\
									task_data['all_info'])
				wrong_id_act(db, wrong_ids, mode, task_name, task_data)
				osd_ack = osd_ack_pack(ack_list, task_data['osd_last_ack']) #收集OSD_ACK
				task_data['osd_last_ack'] = osd_ack
				flags['osd_last_ack'] = task_data['osd_last_ack'] 
				#处理完一组数据后,接着从头开始扫描任务
				try:
					process_ack(task_name, group_list, ack_list, mode, db, \
						task_data['all_info'], task_data, esl_priority = task_data['esl_priority'])
				finally:
					db.commit()
				break
			if task_data['isquit']['core']:
				break
		except IOError, e:
			if e.errno == errno.EPIPE:
				esl_init.log.error_msg("core: %s" % e, errid='ECO013')
				break
		except KeyboardInterrupt, e:
			break
		except Exception, e:
			print_except()
			try:
				wrong_ids = get_all_ids(group_list)
				if len(wrong_ids) == 0:
					wrong_ids = mode['work_list'].keys()
			except Exception, e:
				wrong_ids = mode['work_list'].keys()
			wrong_id_act(db, wrong_ids, mode, task_name, task_data)
			esl_init.log.warning("core: %s, cancel %s" % (e, wrong_ids))

	db.conn.close()
	db = None
	esl_init.log.info("core_process exit")

def get_all_ids(groups):
	ids = []
	for (_, _, _, idlist, _, _, _) in groups:
		ids.extend(idlist)
	return ids

def wrong_id_act(db, wrong_ids, mode, task_name, task_data):
	for ids in wrong_ids:
		mode['work_list'].pop(ids, None) #删除错误的ID
		set_id_notbusy(ids)
		if ids in mode['ap_check_list']:
			mode['ap_check_list'].pop(ids, None)
		if task_name == 'beacom':
			mode['out_queue'].put((ids, ack_failed()))
		elif task_name == "netlink":
			task_data['netlink']['rf_para'].pop(ids, None)
		elif task_name == "bind":
			db.remove_key(db.bind, ids) #刷新完OFF后删除绑定关系
		else:
			mode['out_queue'].put((ids, ack_failed(), esl_of_curr_sid.get(ids, "NONE"))) #ID不存在，返回失败
			db.set_last_status_without_commit(db.esl, ids, time.asctime(), "offline")

	db.commit()

def start(task_data):
	'''
	启动core进程，并返回对应进程对象
	'''
	#proc = multiprocessing.Process(target = process, args=(task_data,))
	proc = threading.Thread(target = process, args=(task_data,))
	proc.start()

	return proc
