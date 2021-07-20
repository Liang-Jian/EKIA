# encoding: utf-8

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  
import urllib2

top_level_url = "https://123.57.225.81:8082"
username = 'hanshowidsystem'
password = 'hanshowidsystem'

def get_esl_info_opener():
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

	password_mgr.add_password(None, top_level_url, username, password)
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)

	return opener

class TestHTTPHandle(BaseHTTPRequestHandler):  
	def do_GET(self):  
		self.protocal_version = "HTTP/1.1"   
		self.send_response(200)  
		self.send_header("Welcome", "Contect")         
		self.end_headers()  
		eslid = self.path.upper()
		opener = get_esl_info_opener()
		info = opener.open(top_level_url + str(eslid), timeout = 3).read()

		self.wfile.write(info) 

def start_server(port):  
	http_server = HTTPServer(('0.0.0.0', int(port)), TestHTTPHandle)  
	http_server.serve_forever() #设置一直监听并接收请求

if __name__ == '__main__':
	start_server(8082)
