#! /usr/bin/python
# encoding: utf-8

import codecs, os
import copy, json
import pprint
#import subprocess
import struct, airspeed
import platform,subprocess
from copy import deepcopy

from esl_init import log, conf, print_except
from dot_temp import check_price, check_price_int_str

#去除 content_title 和 value 字段
s_block_dict = [
		('start_x', 'H'),
		('start_y', 'H'),
		('end_x' , 'H'),
		('end_y' , 'H'),
		('origin_font_type' , 'I'),
		('font_type', '50s'),
		('font_size' , 'B'),
		('content_type', 'B'),
		('content_alignment' , 'B'),
		('content_reverse' , 'B'),
		('number_script', 'B'),
		('number_gap', 'B'),
		('font_type_script' , '50s'),
		('font_size_script' , 'B'),
		('content_color', 'B'),
		]

esl_field_values= {
		'CONTENT_TYPE_NUMBER' : 0,
		'CONTENT_TYPE_TEXT' : 1,
		'CONTENT_TYPE_QRCODE' : 2,
		'CONTENT_TYPE_BMP_FILE' : 3,
		'CONTENT_TYPE_BMP_TEMP' : 4,
		'CONTENT_TYPE_LINE' : 5,
		'CONTENT_TYPE_ABORDER' : 6,
		'CONTENT_TYPE_BARCODE': 7,
		'CONTENT_TYPE_ROMFILE': 8,

		'BLACK': 0,
		'RED': 1,
		'BLUE' : 2,
		'YELLOW' : 3,


		'LEFT' : 0,
		'CENTER' : 1,
		'RIGHT' : 2,
		'JUSTIFIED' : 3,

		'TRUE' : 1,
		'FALSE' : 0,

		'SUPER' : 0,
		'SUB' : 1,
		'NONE' : 2,

		'CONSECUTIVE' : 0,
		'INTERVAL' : 1
		}

def file_exist(file_name):
	return os.path.exists(file_name)

# 为字体添加路径
def add_path_prefix_font(pack_name,font_name):
	json_dir_name = conf.system.dot_temp_dir

	path1 = pack_name + os.sep +  font_name
	font_path1 = os.path.join(json_dir_name,path1)
	path2 = "Fonts" + os.sep + font_name
	font_path2 = os.path.join(json_dir_name,path2)

	if file_exist(font_name):
		return font_name
	if file_exist(font_path1):
		return font_path1
	if file_exist(font_path2):
		return font_path2
	raise IOError,"%s  is not exists! check path" % font_name

# 为图片添加路径
def add_path_prefix_image(pack_name,image_name):
	json_dir_name = conf.system.dot_temp_dir

	path1 = pack_name + os.sep +  image_name
	image_path1 = os.path.join(json_dir_name,path1)
	path2 = "Images" + os.sep + image_name
	image_path2 = os.path.join(json_dir_name,path2)

	if file_exist(image_name):
		return image_name
	if file_exist(image_path1):
		return image_path1
	if file_exist(image_path2):
		return image_path2
	raise IOError,"%s  is not exists! check path" % image_name

def _init_esl():
	TEMP = {}
	file_name = conf.system.dot_temp_file
	for cd in ['ascii','gb18030','gb2312','utf-8','utf-8-sig']:
		try:
			with codecs.open(file_name, 'r', encoding=cd) as f:
				strs = f.read()
				TEMP = eval(strs, {}, {})
				if TEMP.get('encoding', 'utf-8').lower() not in cd:
					raise KeyError, 'encode error: %s' % cd
				break
		except Exception, e:
				pass
	if not TEMP:
		raise KeyError, (" open %s error" % file_name) 
	return TEMP			

json_temp_cache = {}
json_temp_timeslot = {}
def watch_temp_change():
	for temp in json_temp_cache.keys():
		prov_mtime = json_temp_timeslot.get(temp, 0)
		if os.stat(temp).st_mtime != prov_mtime:
			json_temp_cache.pop(temp, None)
			log.info("template %s is changed, it will be reload after next time", temp)
			
def _init_esl_json(name):
	global json_temp_cache
	json_dir_name = conf.system.dot_temp_dir

	TEMP = {}
	if json_dir_name == "NONE" or name == None:
		raise KeyError,"temp name or dir %s is not exists" % name
	#跨平台处理目录分隔符
	_temp_name = name + os.sep + name +".json"
	temp_name = os.path.join(json_dir_name,_temp_name)
	
	if temp_name in json_temp_cache:
		t = deepcopy(json_temp_cache[temp_name])
		return t

	for cd in ['utf-8','utf-8-sig']:
		try:
			with codecs.open(temp_name, 'r', encoding=cd) as f:
				TEMP = airspeed.Template(f.read())
			break
		except Exception, e:
			pass

	if not TEMP:
		raise KeyError , "open template file error: %s" % temp_name
	
	log.info("load template %s", temp_name)
	json_temp_cache[temp_name] = TEMP
	json_temp_timeslot[temp_name] = os.stat(temp_name).st_mtime
	t = deepcopy(json_temp_cache[temp_name])

	return t
	
def check_block(sb, data):
	ret = True
        
	if sb['content_type'] == 'CONTENT_TYPE_BMP_FILE':
		import imghdr
		if not sb['content_title']:
			try:
				fmt = imghdr.what(sb['content_value']) # raise IOError if not exists
				if fmt != 'bmp':
					raise ValueError,' "%s" is  %s file, not bmp file '% (sb['content_value'],fmt)
			except Exception,e:
				log.error_msg("check bmp file %s wrong, %s" % (sb.get('content_value', 'none'), e), \
						errid='EOS001')
				ret = False

	return ret

def get_font_size(s):
	try:
		s1 = s.strip()
	except AttributeError,e:
		raise AttributeError, "font_type or font_type_script is not a string  " 
	l = s1.split(" ")
	for x in l:
		if x.isdigit():
			return x,l
	return '8', None

# src_num of strs replaced by des_num
def set_font_size(strs, src_num, des_num):
	return strs.replace(src_num,des_num)

def check_digit(B, dict1, MAX_X, MAX_Y, DIRECT): #二维码 一维码。 如果值为空，则置为''
	if B['content_type'] == 'CONTENT_TYPE_QRCODE':
		B['content_reverse'] = "FALSE"
		if B['content_title'] is None and not B['content_value'] :
			B['content_value'] = ' '
		elif B['content_title'] and not dict1[B['content_title']]:
			dict1[B['content_title']] = " "
	elif  B['content_type'] == 'CONTENT_TYPE_BARCODE':
		if B['content_title'] is None and not B['content_value'] :
			B['content_value'] = ' '
		elif B['content_title'] and not dict1[B['content_title']]:
			dict1[B['content_title']] = " "
# 处理字体为0的情况
	font_size_script, l = get_font_size(B['font_type_script'])
	if font_size_script:
		if (int(font_size_script) <= 0):
			log.warning('font_size_script <= 0')
			l[len(l) - 1] = '8'
			font_size_script = '8'
			B['font_type_script'] = ' '.join(l)

	font_size, l = get_font_size(B['font_type'])
	if font_size:
		if (int(font_size) <= 0):
			log.warning('font_size <= 0')
			l[len(l) - 1] = '8'
			font_size = '8'
			B['font_type'] = ' '.join(l)

# 方向及其坐标越界
	if (DIRECT == 0) or (DIRECT == 2):
		if B['end_x'] >= MAX_X :
			log.warning("end_x %s overflow %s ! ,direction is %s " % (B['end_x'], MAX_X, DIRECT))
			B['end_x'] = MAX_X - 1
		if B['end_y'] >= MAX_Y:
			log.warning("end_y %s overflow %s ! ,direction is %s" %(B['end_y'], MAX_X, DIRECT))
			B['end_y'] = MAX_Y - 1
	else:
	 	if B['end_x'] >= MAX_Y:
			log.warning("end_x %s overflow %s ! ,direction is %s " % (B['end_x'], MAX_Y, DIRECT))
	 		B['end_x'] = MAX_Y - 1 
	 	if B['end_y'] >= MAX_X:
			log.warning("end_y %s overflow %s ! ,direction is %s" %(B['end_y'], MAX_Y, DIRECT))
	 		B['end_y'] = MAX_X - 1
	
	if B['content_type'] == 'CONTENT_TYPE_LINE' and B['end_y'] == B['start_y']:
		pass
	elif B['end_x'] <= B['start_x'] or B['end_y'] <= B['start_y']:
		raise KeyError,"end(x|y) is less than start(x|y)"

	if B['content_type'] !=  'CONTENT_TYPE_NUMBER': #以下处理数字
		return


	if font_size_script and font_size:
		if int(font_size_script) > int(font_size):
			log.debug("The decimal part font is greater than the integer's ")
			B['font_type_script'] =	set_font_size(B['font_type_script'],font_size_script,font_size)
			if B['number_script'] is 'SUB':
				B['number_script'] = 'SUPER'
	else: #someone maybe None
		log.warning("Cannot find font_size in font_type or font_size_script")
		if B['number_script'] is 'SUB':
			B['number_script'] = 'SUPER'
		if font_size:
			B['font_type_script'] = B['font_type']
		elif font_size_script:
			B['font_type'] = B['font_type_script']

	
def check_field(B):
	content_type = [
		'CONTENT_TYPE_NUMBER',
		'CONTENT_TYPE_TEXT' ,
		'CONTENT_TYPE_QRCODE',
		'CONTENT_TYPE_BMP_FILE' ,
		'CONTENT_TYPE_BMP_TEMP' ,
		'CONTENT_TYPE_LINE' ,
		'CONTENT_TYPE_ABORDER' ,
		'CONTENT_TYPE_BARCODE',
		'CONTENT_TYPE_ROMFILE']
	content_color=['BLACK','RED','BLUE', 'YELLOW' ]

	content_alignment = ['LEFT' ,'RIGHT' ,'CENTER' ,'JUSTIFIED', ]
	content_reverse = ['TRUE' ,'FALSE' ]
	number_script = ['SUPER' ,'SUB' ,'NONE' ]
	number_gap = ['CONSECUTIVE', 'INTERVAL' ]
	
	if B['content_type'] not in content_type:
		raise KeyError,"\"%s\" should not be in content_type" % B['content_type']
	if B['content_color'] not in content_color:
		raise KeyError,"\"%s\" should not be in content_color" % B['content_color']
	if B['content_alignment'] not in content_alignment:
		raise KeyError,"\"%s\" should not be in content_alignment" % B['content_alignment']
	if B['content_reverse'] not in content_reverse:
		raise KeyError,"\"%s\" should not be in content_reverse" % B['content_reverse']
	if B['number_script'] not in number_script:
		raise KeyError,"\"%s\" should not be in number_script" % B['number_script']
	if B['number_gap'] not in number_gap:
		raise KeyError,"\"%s\" should not be in number_gap" % B['number_gap']


#check number< 0.1
def check_number(B, dict1):
	if B['content_type'] !=  'CONTENT_TYPE_NUMBER':
		return
	if B['content_title'] is None or B['content_title'] == "NONE":
		data_tran = B['content_value']
	else:
		data_tran = dict1.get(B['content_title'], '')
		if data_tran == '':
			log.warning("%s, %s not in %s", dict1.get('eslid',''), B['content_title'], dict1)

	#4294967295
	try:
		if float(data_tran) <= 0.1 :
			pass
	except Exception,e:
		B['content_type'] = 'CONTENT_TYPE_TEXT'
		log.warning("cannot conver non-numberic '%s', reset to text" % (data_tran))

	if B['number_script'] != "NONE": #小数
		if float(data_tran) > float(4294967295)/100 or float(data_tran) < 0.001:
			B['content_type'] = 'CONTENT_TYPE_TEXT'
	else:
		if int(float(data_tran)) > 4294967295 or int(float(data_tran)) < 0: # 整数
			B['content_type'] = 'CONTENT_TYPE_TEXT'
	return

def check_path(B,name):
	if B['content_type'] == "CONTENT_TYPE_BMP_FILE":
		B['content_value'] = add_path_prefix_image(name,B['content_value'])
			
	if B['content_title'] == "NONE":
		B['content_title'] = None

class Util:
	def toInt(self, txt):
		return int(txt)
	def toFloat(self, txt):
		return float(txt)
	def toString(self, txt):
		return str(txt)
	def round(self, txt, n):
		fmt = "%%.%df" % n
		return fmt % round(float(txt), n)
	def roundFloor(self, txt, n):
		txt = str(float(txt)) + '0'*n
		txt = txt.split('.')
		txt = txt[0] + '.' + txt[1][:n]
		return txt
	def strlen(self, txt):
		return len(txt)

def is_lcd_info_ok(eslid, info):
	temp_name = info.get('op4', '')
	if not temp_name:
		return False
	return True

def is_info_ok(eslid, info):
	from updata import get_op5_dire
	is_json_temp = conf.system.temp_json.upper() == 'YES'

	info["util"] = Util()

	if info.get('nw4', None) != "DOT20":
		return is_lcd_info_ok(eslid, info)

	if not is_json_temp:
		return True
	
	temp_name = info.get('op4', '')
	if not temp_name:
		temp_name = ''
	try: #打开模版失败
		T = _init_esl_json(temp_name)
	except KeyError, e:
		if "unbind" in temp_name.lower():
			try:
				info['op4'] = 'UNBIND' #使用默认的解绑模版
				T = _init_esl_json('UNBIND')
				log.warning("unbind template %s not exist, use default template 'UNBIND'" % temp_name)
			except KeyError, e:
				print_except()
				log.error_msg("check info error for eslid %s, %s, %s" % (eslid, e, info),
						errid='EOS002', eslid = info.get("eslid", "none"), salesno=info.get('salesno', "none"))
				return False
		else:
			print_except()
			log.error_msg("check info error for eslid %s, %s, %s" % (eslid, e, info),
						errid='EOS003', eslid = info.get("eslid", "none"), salesno=info.get('salesno', "none"))
			return False
			
	try:
		op5, dire = get_op5_dire(info)
		max_x, max_y = op5['resolution_x'], op5['resolution_y']
		T = T.merge(info)
		T = json.loads(T)
		for B in T["screen_block"]:
			check_path(B, temp_name)
			check_field(B)
			check_number(B, info)
			check_block(B, info)
			check_digit(B, info, max_x, max_y, dire) 
	except Exception, e:
		print_except()
		log.error_msg("check info error for eslid %s, %s, %s" % (eslid, e, info),
				errid='EOS004', eslid = info.get("eslid", "none"), salesno=info.get('salesno', "none"))
		return False
	
	return True

def send_dot_info_json(fifo,esl_id,temp_name,dict1,op5, dire):

		dict1["util"] = Util()
		TEMP = _init_esl_json(temp_name) # TEMP is dict {TEMP_20:[{},{}...]}
		TEMP = json.loads(TEMP.merge(dict1))
		temp_list = TEMP["screen_block"] # list : [ {},{},..]
		
		epd_types = 1
		max_package = op5['max_package']
		flash_size = op5['flash_size']
		version = op5['version']

		MAX_X = op5['resolution_x']
		MAX_Y = op5['resolution_y']

		DIRECT = dire

		block_num = len(temp_list)
		s = []
		s.append(struct.pack('>I',int(esl_id.replace('-', ''), 16))) # 1 id
		s.append(struct.pack("H", max_package))   # 2  send max_package
		s.append(struct.pack("H", flash_size))   # 2  send flash_size
		s.append(struct.pack("H", version))   # 2  send version
		
		s.append(struct.pack("H", op5['resolution_x']))   # 2  send max x
		s.append(struct.pack("H", op5['resolution_y']))   # 2  send max y
		s.append(struct.pack("B", DIRECT))   # 3  send scree direction
		
		s.append(struct.pack("B", block_num))   # 3  send block_num
		# 4  发送c语言对应的结构体
		
		for B in temp_list: # B:字典类型, 每个block : {}							
			check_path(B,temp_name)
			check_field(B)
			check_number(B,dict1) # 0.1 ,4字节
			check_digit(B,dict1, MAX_X,MAX_Y,DIRECT) # 二维码翻转,小数字体大于整数字体, end < start

			for sb in s_block_dict: #sb : ('start_x','H'),('start_y' ,'H')...
				if sb[0] not in B:
					raise KeyError,"%s not found " % sb[0]
				data = B[sb[0]] # data : 80(start_x的值) ,"CONTENT_TYPE_TEXT"("content_type" )
				
				if 'B' in sb[1]: # C语言宏定义部分
					data_tran = esl_field_values.get(data)
					if data_tran is None:
						data_tran = data
					s.append(struct.pack(sb[1],data_tran))
				elif 's' in sb[1]:
					data_tran = data.encode("utf-8") # 需将其转换成utf-8 因为json转换的格式默认是utf-8
					s.append(struct.pack(sb[1],data_tran))
				else:
					s.append(struct.pack(sb[1],data))
			
			if B['content_title'] is None:			   # 特殊字段的处理	   
				data_tran = B['content_value']
				if data_tran == None:
					log.warning("content_value is None of %s, reset to empty" % esl_id)
					data_tran = " "
			else:
				data_tran = dict1.get(B['content_title'], None) 
				if not data_tran: #防止数据库为空
					data_tran = " "
					log.warning("title '%s' is None of %s, reset to empty" % (B['content_title'], esl_id))
	
				#如果字段为价格，则乘以100, 只有点阵价签才会这样
			if B['content_type'] == 'CONTENT_TYPE_NUMBER':
				if B['number_script'] != 'NONE': #有小数点
					data_tran = str(int(''.join(check_price(data_tran).split('.'))))
				else: # 如果发送的数字没有小数点,但是又可能带了小数点
					if('.' in data_tran):
						log.warning("number_script is \"NONE\" ,but %s : decimal point found!" % data_tran)
					data_tran = check_price_int_str(data_tran)

			if not data_tran:
				data_tran = " "

			data_tran = data_tran.encode("utf-8") # len(data_tran) 其实就是内存字节数
			fmt = "%ss" % (len(data_tran) + 1)	  # data字段的格式
			if not check_block(B, data_tran):
			   raise IOError, '%s'% B['content_value']
			
			s.append(struct.pack("H" , (len(data_tran)+1)))	# 5 发送data字段的长度	 
			s.append(struct.pack(fmt , data_tran))			  # 6 发送data字段

		return s

def send_dot_info(fifo,esl_id,temp_name,dict1,op5, dire, TEMP):
		temp_list = TEMP[temp_name] # list : [ {},{},..]

		epd_types = 1
	
		max_package = op5['max_package']
		flash_size = op5['flash_size']
		version = op5['version']

		MAX_X = op5['resolution_x']
		MAX_Y = op5['resolution_y']

		DIRECT = dire

		block_num = len(temp_list)
		s = struct.pack('>I',int(esl_id.replace('-', ''), 16)) # 1 id
		s += struct.pack("H", max_package)   # 2  send max_package
		s += struct.pack("H", flash_size)   # 2  send flash_size
		s += struct.pack("H", version)   # 2  send version
		  
		s += struct.pack("H", op5['resolution_x'])   # 2  send max x
		s += struct.pack("H", op5['resolution_y'])   # 2  send max y
		s += struct.pack("B", dire)   # 3  send scree direction

		s += struct.pack("B", block_num)   # 3  send block_num
		# 4  发送c语言对应的结构体
		
		for B in temp_list: # B:字典类型, 每个block : {}							
		###	临时增加检测数值小于0.1的值	
		### 如果有这种现象把原始数据中的content_type值改成CONTENT_TYPE_TEXT
#			check_path(B,temp_name)
			check_field(B)
			check_number(B,dict1) # 0.1 ,4字节
			check_digit(B,dict1, MAX_X,MAX_Y,DIRECT) # 二维码翻转,小数字体大于整数字体, end < start


			for sb in s_block_dict: #sb : ('start_x','H'),('start_y' ,'H')...
				if sb[0] not in B:
					raise KeyError,"%s not found " % sb[0]

				data = B[sb[0]] # data : 80(start_x的值) ,"CONTENT_TYPE_TEXT"("content_type" )
				
				if 'B' in sb[1]:
					data_tran = esl_field_values.get(data)
					if data_tran is None:
						data_tran = data
					s += struct.pack(sb[1],data_tran)
				elif 's' in sb[1]:
					data_tran = data
					s += struct.pack(sb[1],data_tran)
				else:
					s += struct.pack(sb[1],data)
			if B['content_title'] is None:			   # 特殊字段的处理	   
				data_tran = B['content_value']
				if data_tran == None:
					raise KeyError, "content_value is None"
				
			else:
				data_tran = dict1[B['content_title']]   
				if not data_tran: #防止数据库为空
					raise ValueError, "database '%s' is None" % B['content_title']
	
				#如果字段为价格，则乘以100, 只有点阵价签才会这样
			if B['content_type'] == 'CONTENT_TYPE_NUMBER':
				if B['number_script'] != 'NONE': #有小数点
					data_tran = str(int(''.join(check_price(data_tran).split('.'))))
				else: # 如果发送的数字没有小数点,但是又可能带了小数点
					if('.' in data_tran):
						log.error_msg("number_script is \"NONE\" ,but %s : decimal point found!" % data_tran,
							errid='EOS005', eslid = dict1.get("eslid", "none"), salesno=dict1.get('salesno', "none"))
					data_tran = check_price_int_str(data_tran)

			if not data_tran:
				data_tran = ""

			data_tran = data_tran.encode("utf-8") # len(data_tran) 其实就是内存字节数
			fmt = "%ss" % (len(data_tran) + 1)	  # data字段的格式
			if not check_block(B, data_tran):
			   raise IOError, '%s'% B['content_value']
			
			s += struct.pack("H" , (len(data_tran)+1))	# 5 发送data字段的长度	 
			s += struct.pack(fmt , data_tran)			  # 6 发送data字段

		return s

def dot_ack(fifo,esl_id, ack):
		fifo.stdin.write(struct.pack('>I',int(esl_id.replace('-', ''), 16)))
		fifo.stdin.write(struct.pack("H", len(ack) ))   # 2 ack number
		for i in ack:								   # 3 send ack
			fifo.stdin.write(struct.pack("B", i))
