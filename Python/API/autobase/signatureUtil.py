import hmac , sys ,json
# 加密过程
from hashlib import sha1
from autobase.logger import *

'''
signature:
登录的时候，content-type : urlencode  。 post 使用的content-type ： json
signature: 对登录的用户名和密码进行加 。 提交数据使用的是固定的signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
loginName=13716697293&password=123456
get 请求，需要对请求的报文进行加密

'''


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
		'''
		:param dict1:
		:return:  {key:value} -> key=&value
		'''
		string_dict = ""
		if dict1 != dict():
			sorted_list = sorted(dict1.items(),key = lambda d:d[0])   # -> tuple
			for i in iter(sorted_list):
				str1 = i[0] + "=" + i[1] + "&"
				string_dict += str1
		return string_dict[0:-1]

	def get_signature(self,dict1=None):
		'''
		:param dict1: 登录传用户名密码 。提交数据置为空。
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

if __name__ == '__main__':
	# content = '{"loginName":"13716697293","password":"123456"}'
	content = {
"classAuthority": "2",
"cityId": "654000",
"schoolId": "",
"mobile": "13711110011",
"currentSchool": "伊利第一小学",
"currentSchoolId": "18",
"gradeId": "25",
"sex": "1",
"studentName": "autotest1",
"birthday": "",
"studentCode": "",
"headPic": "",
"registerTime": "",
"spareMobile": "",
"inviterNumber": "",
"recommender": "",
"idnumber": "",
"cityName": "伊犁哈萨克自治州",
"studentLevelList": [],
"studentStatus": 1
}
	# test1 = {"pageNum":"1","pageSize":"10"}
	# test1 = '{"pageNum":"1","pageSize":"10"}'
	# dic_data = json.loads(content)
	# print(dic_data)
	# login_sginature = Signature().get_signature()  # 提交数据
	login_sginature = Signature().get_signature()  # 登录
	print(login_sginature)