
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


pem = r"D:\zdhlog\EKIA\Python\API\cert\cmspre.pem"
class Signature:

	def hash_mac(self,appSecret,string_dict,sha1):
		hmac_code = hmac.new(appSecret.encode(),string_dict.encode(),sha1)
		return hmac_code.hexdigest()

	def hmac_string(self,string_dict):
		# set appSecret
		appSecret = "661ee319dff061d4fb6532787f7b6wgl"
		str3 = self.hash_mac(appSecret, string_dict, sha1)
		return str3

	def get_string(self,dict1):
		string_dict = ""
		if dict1 != {}:
			sorted_list = sorted(dict1.items(),key = lambda d:d[0])


			for i in iter(sorted_list):
				str1 = i[0] + "=" + i[1] + "&"
				string_dict += str1
			#print(string_dict)
			print(string_dict[0:-1])

		return string_dict[0:-1]

	# dict1--传入字典

	def get_signature(self,dict1):
		if dict1==None:
			signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
			return signature
		string_dict = self.get_string(dict1)
		signature = self.hmac_string(string_dict).upper()

		return signature

import demjson
class HttpMethods:
    def __init__(self):
        self.retry = 0
        self.json_temp = ""
        self.result = ""

    def get_result(self, url, method, header, req_data):
        while self.retry < 3:
            try:
                if method == 'POST':
                    self.result = requests.post(url, data=json.loads(req_data), headers=header,pem=pem)

                elif method == 'GET':
                    self.result = requests.get(url, params=json.loads(req_data), headers=header)
                    self.result.encoding("utf-8")
                elif method == 'PUT':
                    self.result = requests.put(url, data=req_data.encoding("utf-8"), headers=header)
                break
            except Exception as f:
                # time.sleep(2)
                self.retry += 1
                print(f)
                # print("Send Request Error: " + str(error))

        self.json_temp = self.result
        return self.json_temp



import requests,json,hmac
from hashlib import sha1




# 取模板文件。 str
content = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\cmslogin.vm','r',encoding='utf-8',errors='ignore').read()

# str - json
zhuangtai_data = json.loads(content)
print(zhuangtai_data)
# 获取 signature
login_sginature = Signature().get_signature(zhuangtai_data)
print(login_sginature)



headerss = {
	"appKey":"201820011141153",
	"token": "123",
	"signature": "917B810FC675789F63C1AFA75BBF5A52AC81CC35",
	"tenantId": "pycmspre",
	"Content-Type":"application/x-www-form-urlencoded"
}


sess = requests.session()
sess.auth=("token", "1234")
sess.headers.update(headerss)
# response = sess.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True', data=json.dumps(eval(content),ensure_ascii=True), verify=False, timeout=4,headers=headerss)
login_response = sess.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True', data=json.loads(content), verify=False, timeout=4, headers=headerss)
print(login_response.text)
# 取token
token = eval(login_response.text).get('value').get('token')
getcookies ={
	'token':token,
	'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74',
	'userId': '4656'

}


sess.headers.update({'token':token,'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74'})

print(sess.headers)


sess.headers.update(
	{'userId': '4656',
	 'isAdmin':'2',
	 }
)


''' feng ceng deng ji 
sess.headers.update({'Content-Type':'application/json'})
f = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\fengcengdengji.vm','r',encoding='utf-8',errors='ignore')
data = f.read()
dict_data = eval(data)
time.sleep(1)
response1 = sess.post("https://pycmspre.lexue.com/basic/level/saveLevels",data=json.dumps(dict_data,ensure_ascii=True), verify=False, timeout=4)  # ｏｋ
print(response1.text)'''



'''班级状态更新
req:
{"id":"488","campusStatus":"1"}
rep:
{
  "code" : 0,
  "message" : "更新状态成功",
  "value" : 1
}


question:
id 如何取
1 : 启用 0: 禁用

zhuangtaibaowen = open(r'D:\zdhlog\EKIA\Python\API\\autodata\\template\\xiaoquzhuangtai.vm','r',encoding='utf-8',errors='ignore').read()

zhuangtai_data = json.loads(zhuangtaibaowen)
print(zhuangtai_data)
# 获取 signature
zhuangtai_sginature = Signature().get_signature(zhuangtai_data)
print(zhuangtai_sginature)
sess.headers.update({'token':token,'signature':zhuangtai_sginature})
banjizhuangtai = sess.put("https://pycmspre.lexue.com/basic/campus/updateCampusStatus",data=json.loads(zhuangtaibaowen))
print(banjizhuangtai.text)'''


'''商户号绑定
shhbdbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\shanghuhaobangding.vm','r',encoding='utf-8',errors='ignore').read()
shhbdbaowen_dict_data = eval(shhbdbaowen)

time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
shanghuhaobind = sess.post("https://pycmspre.lexue.com/basic/merchant/saveMerchantBind",data=json.dumps(shhbdbaowen_dict_data,ensure_ascii=True), verify=False, timeout=4)  # ｏｋ
print(shanghuhaobind.text)
'''

'''添加教室

tjjsbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\tianjiajiaoshi.vm','r',encoding='utf-8',errors='ignore').read()
tjjs_dict_data = eval(tjjsbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
shanghuhaobind = sess.post("https://pycmspre.lexue.com/basic/campus/saveClassroom",data=json.dumps(tjjs_dict_data,ensure_ascii=True), verify=False, timeout=4)  # ｏｋ
print(shanghuhaobind.text)'''



'''添加角色
tianjiajuesebaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\tianjiajuese.vm', 'r', encoding='utf-8', errors='ignore').read()
tianjiajuse_dict_data = json.loads(tianjiajuesebaowen)
print(tianjiajuse_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(tianjiajuse_dict_data)
print(tjjs_sginature)
time.sleep(1)

# sess.headers.update({'Content-Type':'application/json'})
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/system/role/saveSchoolRole", data=json.loads(tianjiajuse_dict_data), verify=False, timeout=4)  # ｏｋ
print(tianjiajuese.text)
print(sess.headers)'''


'''新建员工
xxjygbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianyuangong.vm', 'r', encoding='utf-8', errors='ignore').read()
xxjygbaowen_dict_data = eval(xxjygbaowen)

time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
xjyg = sess.post("https://pycmspre.lexue.com/personnel/teacher/saveTeacher",data=json.dumps(xxjygbaowen_dict_data,ensure_ascii=True), verify=False, timeout=4)  # ｏｋ
print(xjyg.text)
'''


