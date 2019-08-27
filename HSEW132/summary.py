# encoding: utf-8

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from database import DB
import urlparse, threading, esl_init, httplib, json, pprint

class GetHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			parsed_path = urlparse.urlparse(self.path)
			url_path = parsed_path.path
			url_seg = url_path.split('/')
			if '' in url_seg:
				url_seg.remove('')
			try:
				url = url_seg[0]
				seg = url_seg[1] # str
			except IndexError, e:
				pass
			url_path_list = {
						'esl': self.get_all_esl_info,
						'ap': self.get_all_ap_info,
						'sales': self.get_all_sales_info,
						'bind': self.get_all_bind_info,
						'update': self.get_all_update_info,
					}
			html_views = url_path_list[url](seg)
			pprint.pprint(html_views, stream = self.wfile)
			return
		except KeyError, e:
			pass

	def get_all_ap_info(self, seg):
		'''
		ap_info
		'''
		db = DB()
		table_name = db.ap
		if not seg:
			url_params = db.key_list(table_name)
		else:
			url_params = seg
		ap_info = []
		for i in url_params:
			ap_single_info = db.get_all_info(table_name, i)
			ap_info.append(ap_single_info)
		encode_json = json.dumps(ap_info)
		return encode_json
		
	def get_all_esl_info(self, seg):
		'''
		esl_info
		'''
		db = DB()
		url_list = {}
		table_name = db.esl
		if not seg:
			url_params = db.key_list(table_name)
		else:
			url_list.setdefault(seg, [])
			url_params = url_list
		esl_info = []
		for i in url_params:
			esl_single_info = db.get_all_info(table_name, i)
			esl_info.append(esl_single_info)
		#encode_json = json.dumps(esl_info)
		return esl_info
		
	def get_all_sales_info(self, seg):
		'''
		sales_info
		'''
		db = DB()
		url_list = {}
		table_name = db.sales
		if not seg:
			url_params = db.key_list(table_name)
		else:
			url_list.setdefault(seg, [])
			url_params = url_list
		sales_info = []
		for i in url_params:
			sales_single_info = db.get_all_info(table_name, i)
			sales_info.append(sales_single_info)
		encode_json = json.dumps(sales_info)
		return encode_json
		
	def get_all_bind_info(self, seg):
		'''
		bind_info
		'''
		db = DB()
		url_list = {}
		table_name = db.bind
		if not seg:
			url_params = db.key_list(table_name)
		else:
			url_list.setdefault(seg, [])
			url_params = url_list
		bind_info = []
		for i in url_params:
			bind_single_info = db.get_all_info(table_name, i)
			bind_info.append(bind_single_info)
		encode_json = json.dumps(bind_info)
		return encode_json
		
	def get_all_update_info(self, seg):
		'''
		updata_info
		'''
		db = DB()
		update_data = web_data
		update_times = update_data['updata']['work_list']
		url_list = {}
		table_name = db.bind
		if not seg:
			url_params = []
		else:
			url_list.setdefault(seg, [])
			url_params = url_list
		esl_info = []
		for i in url_params:
			esl_single_info = db.get_all_info(table_name, i)
			esl_info.append(esl_single_info)
		encode_json = json.dumps(esl_info)
		return encode_json
		
def http_server_exit():
	try:
		conn = httplib.HTTPConnection('localhost', 9500, timeout = 10)
		conn.request('GET', '/')
		conn.close()
	except Exception,e:
		esl_init.log.info('http server exit error: %s' % e)
		
def process(task_data):
	'''
	进程实时读取系统状态
	'''
	try:
		global web_data
		web_data = task_data
		esl_init.log.info("summary_process starting")
		server_address = ('localhost', 9500)
		server = HTTPServer(server_address, GetHandler)
		server.timeout = 5
		while not task_data['isquit']['summary']:
			server.handle_request()
	except Exception, e:  
		esl_init.log.error_msg("summary process:%s" % e, errid='ESU001')
	except KeyboardInterrupt:
		raise KeyboardInterrupt, 'KeyboardInterrupt'
	esl_init.log.info("summary is exit")

def start(task_data):
	'''启动汇总进程并返回进程对象'''
	proc = threading.Thread(target = process, args = (task_data,))
	proc.start()
	return proc
