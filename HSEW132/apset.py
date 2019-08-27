# encoding:utf-8
import database, esl_init, pprint, codecs
from esl_init import conf

setid_list = ['01','FF']
startid = int(setid_list[0], 16)
endid = int(setid_list[1], 16)

def get_setid(ap, ap_list):
	used = {}
	for group_name in ap_list:
		for ap in ap_list[group_name]:
			for setid in ap_list[group_name][ap][1:]:
				used[int(setid, 16)] = '1'
	
	for setid in xrange(startid, endid):
		N = hex(setid)
		if setid not in used and setid <= 15: #小于15:'0X'
			return ('0' + N[2]).upper()	
		elif setid not in used:
			return (N[2] + N[3]).upper()
		else:
			continue
	
def get_nw3(ap, ap_list):
	channel_list = conf.netlink.channel_list
	used = {}
	for nw3 in channel_list:
		used[str(nw3)] = 0
	
	for group_name in ap_list:
		for ap in ap_list[group_name].keys():
			for nw3 in ap_list[group_name][ap]:
				if nw3 in used:
					used[nw3] += 1
	used = sorted(used.iteritems(), key=lambda used : used[1], reverse=False) # 从小到大排列
	ap_list = [item[0] for item in used][:-1] #把信道使用最多的排除掉
	return ap_list[0]

def read_setid_info():
	for code in ['utf-8-sig', 'utf-8', 'gb2312', 'ascii']:
		try:
			f = codecs.open("config/set_list.ini", 'r', encoding=code)
			txt = f.read()
			f.close()
			apset_list = eval(txt, {}, {})
			return apset_list
		except Exception, e:
			pass

def save_apset_info(apid, apset_info, db): # 传入db，防止数据库报错:SQLite objects created in a thread can only be used in that same thread...

	group_esl_max = int(conf.netlink.group_num_max)

	apset_list = apset_info	
	apset_list.setdefault('DEFAULT_GROUP', {})
	if apid in apset_list['DEFAULT_GROUP']:
		set = apset_list['DEFAULT_GROUP'][apid][-1]
		if db.set_esl_count(set) > (group_esl_max * 24):
			new_setid = get_setid(apid, apset_list)
			apset_list['DEFAULT_GROUP'][apid].append(new_setid)
	else:
		apset_list.setdefault('DEFAULT_GROUP', {}).setdefault(apid, [])
		new_nw3 = get_nw3(apid, apset_list) # 系统开启时生成默认json格式, 新基站加入时分配chn与setid
		apset_list['DEFAULT_GROUP'][apid].append(new_nw3)
		new_setid = get_setid(apid, apset_list)
		apset_list['DEFAULT_GROUP'][apid].append(new_setid)	
	
	load_apset_info(apset_list) # 将改变写入到set_list.ini中
		
def load_apset_info(apset_list):
	with open("config/set_list.ini","w") as f:
		pprint.pprint(apset_list, stream=f)
			
			
