
# li = list()
# for x in range(5):
#     li.append(lambda x: x**2)
#
# print(li[0](2)) # 4
# print(li[1](3)) # 9
# print(li[0](1))
#
#
#
# # y = list(filter([ lambda  :x for x in range(4)]))
#
# newlist = list(filter(lambda n:n%2==1,[1,2,3,4,5,6,7,8,9,10]))
#
# # print(y[0](2))
# print(newlist)
# # print(y)
#
# z = list(x for x in [1,2,3,4,5,6,7,8,9,10] if x%2==1)
# print(z)
#
# #map（函数,shuju）
# k = list(map(lambda x:x*2,[1,2,3,4,5]))
# print(k)
#
#
# def dick(a):
#     return a*2
# dd = list(map(dick,[1,2,3,4]))
# print(dd)
#
#
# def normalize(name):
#     print(name)
#     return name[0].upper()+ name[1:].lower()
# Name = ['lily','JACK','mAriN']
#
# s = (list(map(normalize,Name)))
# print(s)
#
#
# from functools import reduce
# def sum(x,y):
#     return x+y
# l = [1,2,3,4,5,6]
# l = reduce(sum,l)
# print(l)
#
# l = [1,2,3,4,5,6]
# l = reduce(lambda x,y:x+y,l)                # 结合lambda
# print(l)
# help(reduce)


# from openpyxl import load_workbook
#
# wb = load_workbook("/home/robot/ApiTestFrame/autodata/testcase/小渠道一步希望.xlsx")
#
#
# print(wb.sheetnames) #get danyuange
# asheet = wb.get_sheet_by_name("核保出单")
# a1 = asheet['A1']
# print(a1)


# for row in asheet.rows:
#     for cell in row:
#         print(cell.value)

# for col in asheet.columns:
#     for cell in col:
#         print(cell.value)
import queue
import time
import threading

# q = queue.Queue()
# def a():
#
#     for i in range(3):
#
#         print('a'+time.ctime())
#         time.sleep(1)
# def b():
#     for k in range(4):
#         print('b'+time.ctime())
#         time.sleep(2)
#
#
# t = list()
# t1 = threading.Thread(target=a,args=())
# t.append(t1)
# t2 = threading.Thread(target=b,args=())
# t.append(t2)
#
# for i in t:
#     i.setDaemon(True)#  true 父进程死，县城死
#     i.start()



###########################
# def a(num):
#     print("running thread: %s" % num)
#
# def b():
#     pass
#
# t = list()
# t1 = threading.Thread(target=a,args=("s",))
# t.append(t1)
# t2 = threading.Thread(target=b,args=())
# t.append(t2)
# for k in t:
#     k.start()
#     print(k.getName())
#
#
# class te(threading.Thread):
#     def __init__(self,num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#
#     def run(self):
#         print("running thread %s " % self.num)
#         time.sleep(3)
#
# if __name__ == '__main__':
#     t1 = te(1)
#     t2 = te(2)
#     t1.start()
#     t2.start()

############################

# def addNum():
#     global num
#     print("-get num:",num)
#     time.sleep(1)
#     num -=1
#
# num = 100
# thread_list = list()
# for i in range(100):
#     t = threading.Thread(target=addNum)
#     t.start()
#     thread_list.append(t)
# for t in thread_list:
#     t.join()
#
# print("final num ",num)


###########################

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




content  = '{"loginName":"13716697293","password":"123456"}'
#
URL = "https://pycmspre.lexue.com"
#
# header = '{"appKey": "201820011141153",  "token": "123","signature": "signature_value"}'
#
dic_data = json.loads(content)
print(dic_data)
login_sginature = Signature().get_signature(dic_data)
# str_headers1 = header.replace("signature_value", login_sginature)
# print(str_headers1)
# result = HttpMethods().get_result(URL, "POST", json.loads(str_headers1), str(dic_data))
#
# print(result)



# r = requests.get(url=URL,cert=pem)
# print(r.text)



# paths = r"C:\Users\Administrator\Desktop\123.pem"
paths = "D:\\1.cer"
pathss = "D:\\1.crt"
#
# r = requests.get('https://www.12306.cn',cert=paths)
# print(r.text)

# signature:79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74
import ssl


headerss = {"appKey": "201820011141153",  "token": "123","signature": "917B810FC675789F63C1AFA75BBF5A52AC81CC35", "tenantId": "pycmspre"}



add = {
"classAuthority": 2,
"cityId": 654000,
"schoolId": "",
"mobile": "13711110011",
"currentSchool": "伊利第一小学",
"currentSchoolId": 18,
"gradeId": 25,
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
dic_data = json.loads(addschool)
# print(dic_data)
# scho_ = Signature().get_signature(dic_data)
# print(scho_)
#
# hea = {
# "signature": "917B810FC675789F63C1AFA75BBF5A52AC81CC35",
# "tenantid": "pycmspre",
# "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
# }
response=requests.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True',data=json.loads(content), verify=False,timeout=4,headers=headerss)
print(response.text)
Text = response.text
if "SUCCESS" in Text: print("pass")
# handle=open('dest_file.txt','wb')
# # for chunk in response.iter_content(chunk_size=512):
# #     if chunk:  # filter out keep-alive new chunks
# #         handle.write(chunk)
# # handle.close()