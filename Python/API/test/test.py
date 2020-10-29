
'''
signature:
登录的时候，content-type : urlencode  。 提交数据使用的content-type ： json
signature: 对登录的用户名和密码进行加 。 提交数据使用的是固定的signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"

loginName=13716697293&password=123456

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

	# dict1--传入字典
	def get_signature(self,dict1=None):
		'''
		:param dict1: 登录传用户名密码 。提交数据置为空。
		:return: signarure
		'''
		if dict1 is None:
			signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
			return signature
		if isinstance(dict1,dict):
			string_dict = self.get_string(dict1)
			signature = self.hmac_string(string_dict).upper()
			return signature
		if isinstance(dict1,str):
			data = json.loads(dict1)
			string_dict = self.get_string(data)
			signature = self.hmac_string(string_dict).upper()
			return signature


import requests,json,hmac
from hashlib import sha1



content  = '{"loginName":"13716697293","password":"123456"}'
# test1 = {"pageNum":"1","pageSize":"10"}
test1 = '{"pageNum":"1","pageSize":"10"}'
# dic_data = json.loads(content)
# print(dic_data)
# login_sginature = Signature().get_signature()  # 提交数据
login_sginature = Signature().get_signature(test1) # 登录
print(login_sginature)


# headerss = {"appKey": "201820011141153",  "token": "","signature": Signature.get_signature(dic_data), "tenantId": "pycmspre"}
#
# response=requests.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True',data=json.loads(content), verify=False,timeout=4,headers=headerss)
# print(response.text)



dict1={"a":"2","e":"3","f":"8","d":"4"}
dict2 = sorted(dict1)
print(dict2)