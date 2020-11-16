import hmac , sys ,json
# 加密过程
from hashlib import sha1
from autobase.logger import *
import urllib.parse
'''
signature:
登录的时候，content-type : urlencode  。 post 使用的content-type ： json
signature: 对登录的用户名和密码进行加 。 提交数据使用的是固定的signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
loginName=13716697293&password=123456
get 请求，需要对请求的报文进行加密

'''



def tostr(datatype):
	if isinstance(datatype, int):
		datatype = str(datatype)
	elif isinstance(datatype, list):
		datatype = urllib.parse.urlencode(datatype)
	return datatype

class Signature:

	__appSecret = "661ee319dff061d4fb6532787f7b6wgl"

	def hash_mac(self,appSecret,string_dict,sha1):
		hmac_code = hmac.new(appSecret.encode(),string_dict.encode(),sha1)
		return hmac_code.hexdigest()

	def hmac_string(self,string_dict):
		# set appSecret
		str3 = self.hash_mac(Signature.__appSecret, string_dict, sha1)
		return str3

	def get_string(self,dict1):
		dict2urlencode_String = ""
		if dict1 != {}:
			sorted_list = sorted(dict1.items(),key = lambda d:d[0])
			for i in iter(sorted_list):
				str1 = i[0] + "=" + tostr(i[1]) + "&"
				dict2urlencode_String += str1
		return dict2urlencode_String[0:-1]

	def getSignature(self, dict1=None):
		'''
		:param : 登录传用户名密码 。提交数据置为空。
		:return: signarure
		'''
		if dict1 is None:
			signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
			Logi("data:=%s,signature:= %s" % (dict1,signature))
			return signature
		if isinstance(dict1,dict):
			string_dict = self.get_string(dict1)
			signature = self.hmac_string(string_dict).upper()
			Logi("data:=%s,signature:= %s" % (dict1,signature))
			return signature
		elif isinstance(dict1,str):
			data = eval(dict1)
			string_dict = self.get_string(data)
			signature = self.hmac_string(string_dict).upper()
			Logi("data:=%s,signature:= %s" % (dict1,signature))
			return signature

