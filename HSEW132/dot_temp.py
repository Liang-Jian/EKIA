# encoding: utf-8

import struct, os, random, codecs, json
from esl_init import conf
import esl_init
def check_price(price):
	'''将数据库价格装换成价签可以解析的字符串价格，2位小数点'''
	try:
		num_list = str(price).split('.')
		if len(num_list) == 1:
			decimal_str = '.00'
			sales = str(int(num_list[0])) + decimal_str
		elif len(num_list) == 2:
			#取小数部分
			if len(num_list[1]) == 1:
				num_list[1] = num_list[1] + '0'
			decimal_str = '0.' + str(num_list[1])
			sales = str(int(num_list[0])) + decimal_str[1:4]
	except Exception, e:
		esl_init.log.error_msg("check number failed: %s" % price, errid='EDO001')
		raise KeyError, e
	return sales

def check_price_int(price):
	return int(check_price(price)[:-3])

def check_price_int_str(price):
	return str(int(check_price(price)[:-3]))

def get_seg_json(filename):
	t = None
	for cd in ['ascii','gb18030','gb2312','utf-8','utf-8-sig',]:
		try:
			with codecs.open(filename, 'r', encoding=cd) as f: 
				t = json.load(f)
			break
		except Exception, e:
			pass
	if not t:
		esl_init.log.error_msg("load json file %s failed" % filename, errid='EDO002')

	return t

