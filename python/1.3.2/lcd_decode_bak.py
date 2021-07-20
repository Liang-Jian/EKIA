# encoding:utf-8
# LCD价格数据测试函数

import struct
import sys
from binascii import b2a_hex
from esl_init import log

def _get_led_config(led_config):
	'''
	led_num, t0, t1, t2, cnt
	'''
	led_color_map = {"GREEN":0, "BLUE":1, "RED":2}

	led_num, t0, t1, t2, count =  int(led_color_map[led_config['color']]), \
										int(led_config['on_time']), int(led_config['off_time']),\
										int(led_config['sleep_time']), int(led_config['count'])

	fmt = '<BBBHH'
	d = struct.pack(fmt, led_num, t0, t1, t2, count)
	return d

def get_led_config(i, t):
	'''
	led_num, t0, t1, t2, cnt
	'''
	led_config = t['led_config_map'][t[i['op3']][i['op4']]['led_config']]
	return  _get_led_config(led_config)

def get_rc(i, t):
	'''
	page_flag, page_id, time, led_flag, led_config
	'''
	page_id = int(t[i['op3']][i['op4']]['rc_config']['rc_page_id'])

	rf_config_mode = t[i['op3']][i['op4']]['rc_config']['rc_config_mode']
	rc_config_mode = t['rc_config_mode_map'][rf_config_mode]

	page_flag = int(rc_config_mode['page_flag'])
	times = int(rc_config_mode['time'])
	led_flag = int(rc_config_mode['led_flag'])
	fmt = '<BBHB'
	d = struct.pack(fmt, page_flag, page_id, times, led_flag)

	led_config = rc_config_mode['led_config']
	led_config = t['led_config_map'][led_config]
	d += _get_led_config(led_config)

	return d

def get_value(zone, i):
	if zone['title'] in ['None', 'NONE', 'none', None]:
		return str(zone['value'])
	return str(i[zone['title']])

def get_seg_data(i, t):
	'''
	eslid, version, security_code, magnet, led_t, seg_rc, zone patch, module path, seg_page_t
	'''
	fmt = '>IBBBBB'

	pages = t[i['op3']][i['op4']]['pages']

	d = struct.pack("B", len(pages))

	for p in pages:
		page_id, mask, scroll, zone_num =  p['page_id'], p['mask'], p['scroll'], len(p['data'])
		d += struct.pack("BBBB", page_id, mask, scroll, zone_num)
		for zone in p['data']:
			v = str(get_value(zone, i))
			z = str(zone["area"])
			d += struct.pack("32s64s", z, v)

	return d

def get_test_data():

	esl_info = {'eslid':'59-12-09-99', 'version':'0', 'security_code':'0', 'magnet':'0',
	'op3':'HS_EL_5300', 'op4':'normal', 'Price':1, 'Price1':2, 'Price2':3, 'Price3':4
	}

	temp = {
		"HS_EL_5300": {
			"demo": {
			"led_config" : "RED_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3",
			"rc_config" : {"rc_page_id":"1", "rc_config_mode":"RC_CONFIG_MODE_1"},
			"pages": [
				{"page_id":0, "mask":0, "scroll":15, "data":[							
					{"title":"NONE", "value":"18888", "area":"zn_big_num"},
					{"title":"NONE", "value":"188888", "area":"unit_num"},
					{"title":"NONE", "value":"******", "area":"zn_letter"},
					{"title":"NONE", "value":"1234", "area":"zn_currency"},
					{"title":"NONE", "value":"4", "area":"zn_redbar"},
					{"title":"NONE", "value":"a", "area":"zn_promo_left"},
					{"title":"NONE", "value":"uglk", "area":"zn_unit"},
					{"title":"NONE", "value":"a", "area":"zn_arrow"},
					{"title":"NONE", "value":"dxsc1", "area":"zn_flag"},
					{"title":"NONE", "value":"12", "area":"zn_vba"},
					{"title":"NONE", "value":"1236", "area":"zn_dot"}
				]},
				{"page_id":1, "mask":0, "scroll":10, "data":[							
					{"title":"NONE", "value":"01736", "area":"zn_big_num"},
					{"title":"NONE", "value":"  2240", "area":"unit_num"},
					{"title":"NONE", "value":"Gr1500", "area":"zn_letter"},
					{"title":"NONE", "value":"13", "area":"zn_currency"},
					{"title":"NONE", "value":"", "area":"zn_redbar"},
					{"title":"NONE", "value":"r", "area":"zn_promo_left"},
					{"title":"NONE", "value":"k", "area":"zn_unit"},
					{"title":"NONE", "value":"u", "area":"zn_arrow"},
					{"title":"NONE", "value":"d", "area":"zn_flag"},
					{"title":"NONE", "value":"", "area":"zn_vba"},
					{"title":"NONE", "value":"1", "area":"zn_dot"}
				]},
				{"page_id":2, "mask":0, "scroll":5, "data":[							
					{"title":"NONE", "value":"01736", "area":"zn_big_num"},
					{"title":"NONE", "value":"  3360", "area":"unit_num"},
					{"title":"NONE", "value":"PrPRec", "area":"zn_letter"},
					{"title":"NONE", "value":"13", "area":"zn_currency"},
					{"title":"NONE", "value":"", "area":"zn_redbar"},
					{"title":"NONE", "value":"r", "area":"zn_promo_left"},
					{"title":"NONE", "value":"k", "area":"zn_unit"},
					{"title":"NONE", "value":"d", "area":"zn_arrow"},
					{"title":"NONE", "value":"x", "area":"zn_flag"},
					{"title":"NONE", "value":"", "area":"zn_vba"},
					{"title":"NONE", "value":"1", "area":"zn_dot"}
				]},
				{"page_id":3, "mask":0, "scroll":1, "data":[							
					{"title":"NONE", "value":"01736", "area":"zn_big_num"},
					{"title":"NONE", "value":" -20<>", "area":"unit_num"},
					{"title":"NONE", "value":"SC0NT0", "area":"zn_letter"},
					{"title":"NONE", "value":"3", "area":"zn_currency"},
					{"title":"NONE", "value":"", "area":"zn_redbar"},
					{"title":"NONE", "value":"r", "area":"zn_promo_left"},
					{"title":"NONE", "value":"", "area":"zn_unit"},
					{"title":"NONE", "value":"d", "area":"zn_arrow"},
					{"title":"NONE", "value":"s", "area":"zn_flag"},
					{"title":"NONE", "value":"1", "area":"zn_vba"},
					{"title":"NONE", "value":"", "area":"zn_dot"}
				]},
				{"page_id":4, "mask":0, "scroll":2, "data":[							
					{"title":"NONE", "value":"01736", "area":"zn_big_num"},
					{"title":"NONE", "value":" 30-12", "area":"unit_num"},
					{"title":"NONE", "value":"fin>al", "area":"zn_letter"},
					{"title":"NONE", "value":"3", "area":"zn_currency"},
					{"title":"NONE", "value":"", "area":"zn_redbar"},
					{"title":"NONE", "value":"r", "area":"zn_promo_left"},
					{"title":"NONE", "value":"", "area":"zn_unit"},
					{"title":"NONE", "value":"", "area":"zn_arrow"},
					{"title":"NONE", "value":"c", "area":"zn_flag"},
					{"title":"NONE", "value":"", "area":"zn_vba"},
					{"title":"NONE", "value":"3", "area":"zn_dot"}
				]},
				{"page_id":8, "mask":1, "scroll":0, "data":[
					{"title":"NONE", "value":"", "area":"zn_big_num"},
					{"title":"NONE", "value":"", "area":"unit_num"},
					{"title":"NONE", "value":"", "area":"zn_letter"},
					{"title":"NONE", "value":"", "area":"zn_currency"},
					{"title":"NONE", "value":"", "area":"zn_redbar"},
					{"title":"NONE", "value":"", "area":"zn_promo_left"},
					{"title":"NONE", "value":"", "area":"zn_unit"},
					{"title":"NONE", "value":"", "area":"zn_arrow"},
					{"title":"NONE", "value":"", "area":"zn_flag"}
				]}
			]
			}
		},
		"zone_path":"./config/zone/zn_sn-1130.json",
		"module_path":"./config/zone/bm_sn-1130.json", 
		"led_config_map" : {
			"RED_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3" : 
				{"color":"RED", "on_time":30, "off_time":30, "sleep_time":3, "count":3},
			"BLUE_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3" : 
				{"color":"BLUE", "on_time":30, "off_time":30, "sleep_time":3, "count":3},
			"GREEN_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3" : 
				{"color":"GREEN", "on_time":30, "off_time":30, "sleep_time":3, "count":3},
			"BLUE_ON_20ms_OFF_20ms_SLEEP_0s_COUNT_20":
				{"color":"BLUE", "on_time":20, "off_time":20, "sleep_time":0, "count":20},
			"RED_ON_10ms_OFF_20ms_SLEEP_20s_COUNT_5":
				{"color":"RED", "on_time":10, "off_time":20, "sleep_time":254, "count":5},
			"GREEN_ON_3ms_OFF_3ms_SLEEP_20s_COUNT_10":
				{"color":"GREEN", "on_time":1, "off_time":1, "sleep_time":20, "count":10},
			"BLUE_ON_4ms_OFF_2ms_SLEEP_0s_COUNT_255":
				{"color":"BLUE", "on_time":4, "off_time":2, "sleep_time":0, "count":255},
			"GRED_ON_2ms_OFF_1ms_SLEEP_0s_COUNT_20":
				{"color":"RED", "on_time":2, "off_time":1, "sleep_time":0, "count":20},
			"GREEN_ON_1ms_OFF_1ms_SLEEP_5s_COUNT_10":
				{"color":"GREEN", "on_time":1, "off_time":1, "sleep_time":5, "count":10},
			"GREEN_ON_8ms_OFF_4ms_SLEEP_0s_COUNT_10":
				{"color":"GREEN", "on_time":8, "off_time":4, "sleep_time":0, "count":10}
		},
		"rc_config_mode_map" : {
			"RC_CONFIG_MODE_1" : {"page_flag":0, "time":256, "led_flag":1,
						"led_config" : "GREEN_ON_30ms_OFF_30ms_SLEEP_3s_COUNT_3"}
		}
	}

	return esl_info, temp

def send_seg_data(i, t):
	eslid = int(i['eslid'].replace('-', ''), 16)
	version = int(i.get('version', 1))
	security_code = int(i.get('security_code', 0xfa58))
	magnet = int(i.get('magnet', 0x0f0f))

	fmt = '>IB'
	d = struct.pack(fmt, eslid, version)
	fmt = '<HH'
	d += struct.pack(fmt, security_code, magnet)

	d += get_led_config(i, t)
	d += get_rc(i, t)

	#zone_path = str(t.get("zone_path"))
	#module_path = str(t.get("module_path"))

	o5=eval(i.get("op5"), {}, {})
	zone_path = str(o5.get("zone_path"))
	module_path = str(o5.get("module_path"))

	fmt = '64s64s'

	d += struct.pack(fmt, zone_path, module_path)

	d += get_seg_data(i, t)

	return d

def make_test_data():
	w = sys.stdout.write

	esl_info, temp = get_test_data()

	d = struct.pack("<H", 1)
	d += send_seg_data(esl_info, temp)
	w(i)


if __name__ == '__main__':
	make_test_data()


