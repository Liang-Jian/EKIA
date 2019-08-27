# encoding: utf-8

from __future__ import division
import database, esl_init, os, json, string, copy
from esl_init import conf

def is_normal_power(power):
	try:
		if power =='NONE' or power == '':
			return False
		else:
			return True if float(power) > 28 else False
	except Exception, e:
		return False
		
def esl_report(db, args):
	all_c = len(db.key_list(db.esl))
	bind_esl = db.key_list(db.bind)
	bind_esl_copy = copy.deepcopy(bind_esl)
	for esl in bind_esl_copy:
		if not db.has_key(db.esl, esl):
			bind_esl.remove(esl)
	bind_c = len(bind_esl)
	unbind_c = all_c - bind_c
	
	esl_status = {}
	battery = {}
	transmission = {}
	status_v = db.count_by_key_str(db.esl, 'status')
	trans_v = db.count_by_key_str(db.esl, 'work_mode')
	battery_v = db.count_by_key_str(db.esl, 'op1')

	normal, low = 0, 0
	for k in battery_v:
		if is_normal_power(k):
			normal += int(battery_v[k])
		else:
			low += int(battery_v[k])
	val = {"bak":"00", "bind":[{"bind":str(bind_c), "unbind":str(unbind_c)}],
				"esl_status":[status_v], "transmission":[trans_v],
				"battery":[{'normal':str(normal), "low":str(low)}]}
	
	if len(args) == 0:
		return [val]
	for k in ["bind", "esl_status", "transmission", "battery"]:
		if k not in args[0]:
			val.pop(k, None)
	return [val]

def ap_report(db, args):
	g = db.get_nw1_nw3_ap_group()
	bind_count = {}
	group_count = {}
	chn_count = {}
	
	for wkid in g.keys():
		for chn in g[wkid].keys():
			for apid in g[wkid][chn].keys():
				if not db.has_key(db.ap, apid): 
					continue
				count = g[wkid][chn][apid]
				bind_count.setdefault(apid, 0)
				bind_count[apid] += count
				group_count.setdefault(apid, {})[wkid] = 1
				chn_count.setdefault(apid, {})[chn] = 1
	
	bind_v = [{"apid":k, "bind":str(bind_count[k])} for k in bind_count]
	group_v = [{"apid":k, "group":str(len(group_count[k])), "chn":str(len(chn_count[k]))} for k in bind_count]
	
	aplist = db.key_list(db.ap)
	online, offline, trans, standby = 0, 0, 0, 0
	for ap1 in aplist:
		i = db.get_one(db.ap, ap1)
		if i['status'] == 'online':
			online += 1
		else:
			offline += 1
		if i['work_mode'] == 'transmitting':
			trans += 1
		else:
			standby += 1
	
	val = {"bak":"00", "bind":bind_v, "ap_status":[{"online":str(online), "offline":str(offline)}],
				"group":group_v, "transmission":[{"transmitting":str(trans), "standby":str(standby)}], 
			}
	if len(args) == 0:
		return [val]
	
	for k in ["bind", "ap_status", "group", "transmission"]:
		if k not in args[0]:
			val.pop(k, None)
	
	return [val]

def esl_list(db, argv):
	esllist = [item['eslid'] for item in argv]
	if esllist == []:
		esllist = db.key_list(db.esl)
	
	esl_info_list = []
	for id1 in esllist:
		info = {}
		if not db.has_key(db.esl, id1):
			info['bak'] = '01'
			info['eslid'] = id1
			esl_info_list.append(info)
			continue
		info.update(db.get_one(db.esl, id1))
		try:
			info['battery'] = 'normal' if is_normal_power(info['op1']) else 'lowpower'
		except Exception, e:
			info['battery'] = 'normal'
		try:
			info['success_rate'] = "%.2f%%" % ((1 - float(info['failed_times'])*8 / float(info['transmission_times']))*100) #假设每次失败的价签均重试8次
		except Exception, e:
			info['success_rate'] = "100.00%"
		esl_info_list.append(info)
	
	return esl_info_list

def get_esl_status_of_ap(db, ap1):
	esl_list = db.get_ap_bind_esl_list(ap1)
	eslinfo = []
	for id1 in esl_list:
		info = db.get_one(db.esl, id1)
		if not info:
			continue
		eslinfo.append({"eslid":info['eslid'], "status":info['status'], "signal":"-50"})
	return eslinfo

def get_group_of_ap(g, ap1):
	ap_g = []
	for (apid, nw1, nw3, op3, count) in g:
		if apid != ap1:
			continue
		ap_g.append({"id":nw1, "ch":nw3, "count":str(count)})
	return ap_g
	
def ap_list(db, argv):
	aplist = [item['apid'] for item in argv]
	if aplist == []:
		aplist = db.key_list(db.ap)
	
	g = db.get_ap_bind_group()
	ap_info_list = []
	for ap1 in aplist:
		info = {}
		info['apid'] = str(ap1)
		if not db.has_key(db.ap, ap1):
			info['bak'] = "03"
			ap_info_list.append(info)
			continue
		i = db.get_one(db.ap, ap1) 
		info['ap_status'] = i['status']
		info['bak'] = "00"
		info['esl_list'] = get_esl_status_of_ap(db, ap1)
		info['group'] = get_group_of_ap(g, ap1)

		ap_info_list.append(info)
	
	return ap_info_list

def bind_list(db, args):
        
	bindlist = []
	if len(args) > 0:
		for i in args:
			if "eslid" in i:
				bindlist.append(i['eslid'])
				continue
			if "salesno" in i:
				bindlist.extend(db.get_sales_bind_esl_list(i['salesno']))
				continue
			if "apid" in i:
				bindlist.extend(db.get_ap_bind_esl_list(i['apid']))
				continue
	else:
		bindlist = db.key_list(db.bind)
	bind_list_info = {}
	for id1 in bindlist:
		if db.has_key(db.bind, id1) and db.has_key(db.esl, id1):
			i = db.get_all_info(db.bind, id1)
			if not db.has_key(db.sales, i['salesno']):
				continue
			bind_list_info[id1] = i
	
	return bind_list_info.values()

def send_status(ids, aps, status):
	from xmlserver import reply_ack

	esl_status, ap_status = [], []

	esl_s = "transmitting" if status == 'busy' else "sleep"
	for id1 in set(ids):
		esl_status.append({"eslid":id1, "work_mode": esl_s})

	ap_s = "transmitting" if status == 'busy' else "standby"
	for ap1 in set(aps):
		ap_status.append({"apid":ap1, "work_mode": ap_s, "status":"online"})

	try:
		reply_ack("ESL_STATUS", esl_status, None)
		reply_ack("AP_STATUS", ap_status, None)
	except Exception, e:
		esl_init.log.warning("send status failed: %s" % (e))

def update_htp_start_status(db, apid, ids, sleepids, slaveap):
	aplist = [apid]
	aplist.extend(slaveap)
	try:
		for ap1 in aplist:
			db.change_key_val_without_commit(db.ap, ap1, "work_mode", "transmission")
		
		for id1 in set(ids):
			db.change_key_val_without_commit(db.esl, id1, "work_mode", "transmission")
			db.increace_status(id1, ["wake_times", "transmission_times",])

		for id1 in set(sleepids):
			db.increace_status(id1, ["wake_times", "sleep_times"])
	finally:
		db.commit()
	send_status(ids, [apid] + slaveap, "busy")
	
def udpate_htp_end_status(db, apid, ids, sleepids, slaveap):
	aplist = [apid]
	aplist.extend(slaveap)
	try:
		for ap1 in aplist:
			db.change_key_val_without_commit(db.ap, ap1, "work_mode", "standby")
		
		for id1 in set(ids):
			db.change_key_val_without_commit(db.esl, id1, "work_mode", "sleep")
	finally:
		db.commit()

	send_status(ids, [apid] + slaveap, "free")

def get_file(temp_name):
	json_dir_name = conf.system.dot_temp_dir

	try:
		os.mkdir("%s%s" % (json_dir_name, temp_name))
	except Exception, e:
		pass
	try:
		f = open("%s%s/%s.json" % (json_dir_name, temp_name, temp_name), "w")	
	except Exception, e:
		esl_init.log.error_msg("update template failed: %s, %s" % (temp_name, e), errid='EAP001')
		f = None
	return f
 
def check_temp_name():
	case_list = []
	num_list = range(10)
	num_list = [str(item) for item in num_list]
	for word in string.lowercase:
		case_list.append(word)
		case_list.append(word.upper())
	case_list.append('_')
	case_list.extend(num_list)
	return case_list
 
def template_update(db, args):
	for item in args:
		temp_name = item.get('name', None)
		temp_name_format = check_temp_name() #定义模板名只能是数字、大小写字母、下划线
		if not temp_name:
			item['bak'] = "07"
			continue
		for c in temp_name:
			if c not in temp_name_format:
				item['bak'] = "07"
		
		if 'bak' in item and item['bak'] == "07":
			continue
		f = get_file(temp_name)
		if f:
			json.dump(item, f, encoding="utf-8")
			f.close()
			item['bak'] = "00"
		else:
			item['bak'] = "07"
			
def esl_info(db, args):
	for item in args:
		item['bak'] = '02'
		eslid = item.get('eslid', None)
		if (not eslid) or (not db.has_key(db.esl, eslid)):
			return
		item.update(db.get_all_info(db.esl, eslid))
		item.pop('op6', None)
		item['bak'] = '00'

def ap_info(db, args):
	for item in args:
		item['bak'] = '03'
		apid = item.get('apid', None)
		if apid == None or (not db.has_key(db.ap, apid)):
			return
		item.update(db.get_all_info(db.ap, apid))
		item['bak'] = '00'

def run_info(db, task_data):
	s = {}
	s['uplink_q'] = task_data['reply_ack_q'].qsize()

	#任务清单
	s['work_list'] = {}
	for m in ['updata', 'netlink', 'query']:
		s['work_list'].setdefault(m, {})
		for eslid in task_data[m]['work_list']:
			retry = "retry_%s" % task_data[m]['work_list'][eslid]
			s['work_list'][m].setdefault(retry, 0)
			s['work_list'][m][retry] += 1
		s['work_list'][m]['total'] = len(task_data[m]['work_list'])
	
	#优先级状态
	s['update_priority'] = {}
	for id1 in task_data['esl_priority']:
		if id1 not in task_data['updata']['work_list']:
			continue
		p = task_data['esl_priority'][id1]
		s['update_priority'].setdefault(p, 0)
		s['update_priority'][p] += 1
	
	s['ack_count'] = task_data['ack_count']

	return [s]
