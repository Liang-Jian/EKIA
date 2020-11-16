
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import urllib.parse


def tostr(any):
	if isinstance(any,int):
		any = str(any)
	elif isinstance(any,list):
		any = urllib.parse.urlencode(any)
	return any

def strtoenlencode(_string):

	url_code_name = urllib.parse.quote(_string)
	print(url_code_name)
	return url_code_name

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
		dict2urlencode_String = ""
		if dict1 != {}:
			sorted_list = sorted(dict1.items(),key = lambda d:d[0])
			for i in iter(sorted_list):
				str1 = i[0] + "=" + tostr(i[1]) + "&"
				dict2urlencode_String += str1
		return dict2urlencode_String[0:-1]




	# dict1--传入字典

	def get_signature(self,dict1=None):
		if dict1==None:
			signature = "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74"
			return signature
		# string_dict = self.get_string(dict1)
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
zhuangtai_dict = json.loads(content)
print(zhuangtai_dict)
# 获取 signature
login_sginature = Signature().get_signature(zhuangtai_dict)
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
userId = eval(login_response.text).get('value').get('sysUserId')

getcookies ={
	'token':token,
	'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74',
	'userId': userId

}


sess.headers.update({'token':token,'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74'})

# print(sess.headers)


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
shanghuhaobind = sess.post("https://pycmspre.lexue.com/basic/campus/saveClassroom",data=json.dumps(tjjs_dict_data,ensure_ascii=True), verify=False, timeout=4)  
print(shanghuhaobind.text)'''



'''添加角色
tianjiajuesebaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\tianjiajuese.vm', 'r', encoding='utf-8', errors='ignore').read()
tianjiajuse_dict_data = json.loads(tianjiajuesebaowen)
print(tianjiajuse_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(tianjiajuse_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/system/role/saveSchoolRole", data=json.loads(tianjiajuesebaowen), verify=False, timeout=4)  
print(tianjiajuese.text)'''


'''角色启用
{"roleId":"89"} Id 

jsqybaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\jueseqiyong.vm', 'r', encoding='utf-8', errors='ignore').read()
jsqybaowen_dict_data = json.loads(jsqybaowen)
print(jsqybaowen_dict_data)
tjjs_sginature = Signature().get_signature(jsqybaowen_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/system/role/enableOrDisable", data=json.loads(jsqybaowen))
print(tianjiajuese.text)'''



'''新建员工


# {
#   "code" : 0,
#   "message" : "保存成功",
#   "value" : null
# }

xxjygbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\templatexinjianyuangong.vm', 'r', encoding='utf-8', errors='ignore').read()
xxjygbaowen_dict_data = eval(xxjygbaowen)

time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
xjyg = sess.post("https://pycmspre.lexue.com/personnel/teacher/saveTeacher",data=json.dumps(xxjygbaowen_dict_data,ensure_ascii=True), verify=False, timeout=4)  # ｏｋ
print(xjyg.text)'''


'''菜单权限分配
cdqxbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\caidanquanxian.vm', 'r', encoding='utf-8', errors='ignore').read()
cdqx_dict_data = json.loads(cdqxbaowen)
print(cdqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(cdqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/system/sysUser/updateUserAndMenu", data=json.loads(cdqxbaowen))
print(tianjiajuese.text)'''


'''数据权限
sjqxbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\shujuquanxian.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(sjqxbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/system/sysUser/updateUserAndCampus", data=json.loads(sjqxbaowen))
print(tianjiajuese.text)'''


'''新建面授课-长期班


"courseLevelCoursewareList":"[{\"levelId\":\"0\",\"coursewareList\":[]}]",
"courseLevelDetailList":"[{\"levelId\":\"0\",\"content": \"\",\"detailPic\":[]}]"

xjcqbbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianchangqiban.vm', 'r', encoding='utf-8', errors='ignore').read()
xjcqb_dict_data = json.loads(xjcqbbaowen)
print(xjcqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjcqb_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/educational/course/saveCourse", data=json.loads(xjcqbbaowen), verify=False, timeout=4)
print(tianjiajuese.text)'''



'''新建面授可-短期班
# "courseLevelCoursewareList":" [{"levelId"":""0","coursewareList"":"[]}]
# "courseLevelDetailList":" [{"levelId"":""0","content"":""","detailPic"":"[]}]
xjdqbbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianduanqiban.vm', 'r', encoding='utf-8', errors='ignore').read()
xjdqb_dict_data = json.loads(xjdqbbaowen)
print(xjdqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjdqb_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/educational/course/saveCourse", data=json.loads(xjdqbbaowen), verify=False, timeout=4)
print(tianjiajuese.text)'''

'''新建考试课
xjkskbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjiankaoshike.vm', 'r', encoding='utf-8', errors='ignore').read()
xjdqb_dict_data = json.loads(xjkskbaowen)
print(xjdqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjdqb_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/educational/course/saveCourse", data=json.loads(xjkskbaowen), verify=False, timeout=4)
print(tianjiajuese.text)'''


'''新建公开课
xjgkkbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjiangongkaike.vm', 'r', encoding='utf-8', errors='ignore').read()
xjdqb_dict_data = json.loads(xjgkkbaowen)
print(xjdqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjdqb_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.post("https://pycmspre.lexue.com/educational/course/saveCourse", data=json.loads(xjgkkbaowen), verify=False, timeout=4)
print(tianjiajuese.text)'''


'''新建上课规律确认
skglbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\shengchengshangkeguilv.vm', 'r', encoding='utf-8', errors='ignore').read()
xjdqb_dict_data = json.loads(skglbaowen)
print(xjdqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjdqb_dict_data)
print(tjjs_sginature)
sess.headers.update({'Content-Type':'application/json'})
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
# xxskgl = sess.get("https://pycmspre.lexue.com/educational/classRule/generateClassDate",data=json.loads(skglbaowen))
xxskgl = sess.get("https://pycmspre.lexue.com/educational/classRule/generateClassDate?%s" % xjdqb_dict_data)
print(xxskgl.text)'''

'''新建上课规律
xjskglbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianshangkeguilv.vm', 'r', encoding='utf-8', errors='ignore').read()
xjdqb_dict_data = json.loads(xjskglbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
# xjyg = sess.post("https://pycmspre.lexue.com/personnel/teacher/saveTeacher",data=json.dumps(xxjygbaowen_dict_data,ensure_ascii=True), verify=False, timeout=4)
xjskglreponse =sess.post("https://pycmspre.lexue.com/educational/classRule/saveClassRule",data=json.dumps(xjdqb_dict_data,ensure_ascii=True),verify=False, timeout=4)
print(xjskglreponse.text)'''


'''新建在线课长期班生成课次1
zxkqrbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\templatexinjianzaixiankechangqiban1.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(zxkqrbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/educational/onlineClass/queryClassCourse",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)'''


'''新建在线课长期班生成课次2
zxkqrbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\xinjianzaixiankechangqiban2.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(zxkqrbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/educational/onlineClass/create",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)'''

'''
新建在线课短期班生成课次1
{
  "code" : 0,
  "message" : "SUCCESS",
  "value" : [ {
    "quoteStatus" : 0,
    "conflictTotal" : 0,
    "classCourseId" : null,
    "classId" : null,
    "campusId" : null,
    "classroomId" : null,
    "teacherId" : 5881,
    "teacherName" : "自动化老师1",
    "classDate" : "2020-11-14",
    "classStartTime" : "07:30:00",
    "classEndTime" : "09:00:00",
    "weekName" : "周六",
    "weekCode" : 6,
    "occupationStatus" : null,
    "courseSort" : 1,
    "createTime" : null,
    "className" : null,
    "classCourseName" : null,
    "campusName" : null,
    "timeAndName" : null,
    "classTimeName" : "07:30~09:00",
    "classroomName" : null,
    "teacherOccupation" : 0,
    "classroomOccupation" : null,
    "timeCode" : 1,
    "timeName" : "上午",
    "courseStage" : "1/1",
    "coursePrice" : null,
    "dateStartTime" : "2020-11-14 07:30:00",
    "dateEndTime" : "2020-11-14 09:00:00",
    "classTimeId" : 4606,
    "classRuleId" : 7746,
    "receiveCourseNum" : null,
    "createUserId" : null,
    "createName" : null,
    "updateTime" : null,
    "updateUserId" : null,
    "updateName" : null,
    "courseFirstDate" : null,
    "courseFrequency" : null
  } ]
}
'''

'''
新建在线课短期班生成课次2
response
{
	"classCapacity": 25,
	"classTeacherId": 5881,
	"orderScale": 60,
	"singleTuitionFee": 350,
	"courseTypeCode": 2,
	"specialPrice": 0,
	"className": "2021秋季中班数学",
	"teacherType": 1,
	"playType": 1,
	"screenType": 1,
	"school_share_flag": 1,
	"mailFlag": 0,
	"campusId": 445,
	"yearId": 488,
	"seasonId": 481,
	"sectionId": 2121,
	"gradeId": 2126,
	"subjectId": 2143,
	"levelId": 2934,
	"teacherId": 5881,
	"courseFrequency": "1",
	"tuitionFee": "1",
	"schoolFee": "2",
	"entryFee": "3",
	"classPrice": "6.00",
	"changeClassLimit": 1,
	"changeAdjustLimit": 1,
	"content": "",
	"coverUrl": "https://picspy.lexue.com/avatar-employee-1605165297097",
	"numLimit": 13,
	"adjustLimit": 0,
	"testClassFlag": 0,
	"schoolId": 375,
	"gradeName": "中班",
	"auditingStatus": 1,
	"lowPriceClassFlag": 1,
	"superNumberClassFlag": 0,
	"specialClass": 0,
	"classTeacherName": "自动化老师1",
	"schoolName": "清水二中测试",
	"campusName": "奎屯测试校区",
	"classTimeName": "07:30~09:00",
	"teacherName": "自动化老师1",
	"startTime": "2020-11-12 00:00:00",
	"endTime": "2020-12-12 00:00:00",
	"yearName": "2021",
	"seasonName": "秋季",
	"sectionName": "学龄前",
	"subjectName": "数学",
	"courseTypeName": "短期班",
	"classTimeId": 4606,
	"classDateStartTime": "2020-11-14 07:30:00",
	"classDateEndTime": "2020-11-14 09:00:00",
	"classCourseDtoList": [{
		"quoteStatus": 0,
		"conflictTotal": 0,
		"classCourseId": null,
		"classId": null,
		"campusId": null,
		"classroomId": null,
		"teacherId": 5881,
		"teacherName": "自动化老师1",
		"classDate": "2020-11-14",
		"classStartTime": "07:30:00",
		"classEndTime": "09:00:00",
		"weekName": "周六",
		"weekCode": 6,
		"occupationStatus": null,
		"courseSort": 1,
		"createTime": null,
		"className": null,
		"classCourseName": "2021秋季中班数学第1讲",
		"campusName": null,
		"timeAndName": null,
		"classTimeName": "07:30~09:00",
		"classroomName": null,
		"teacherOccupation": 0,
		"classroomOccupation": null,
		"timeCode": 1,
		"timeName": "上午",
		"courseStage": "1/1",
		"coursePrice": null,
		"dateStartTime": "2020-11-14 07:30:00",
		"dateEndTime": "2020-11-14 09:00:00",
		"classTimeId": 4606,
		"classRuleId": 7746,
		"receiveCourseNum": null,
		"createUserId": null,
		"createName": null,
		"updateTime": null,
		"updateUserId": null,
		"updateName": null,
		"courseFirstDate": null,
		"courseFrequency": null,
		"isEdit": false
	}],
	"classStartTime": "07:30:00",
	"classEndTime": "09:00:00",
	"managerList": [],
	"ruleId": 7746,
	"schoolShareFlag": 1,
	"ruleName": "(每周周六周日)自动化测试上课规律0001",
	"courseVideoList": [],
	"detailPicList": [],
	"quoteStatus": 0,
	"levelName": "",
	"liveFlow": null,
	"gradeFully": 1,
	"subjectFully": 0
}
'''


'''新建讲座
zxkqrbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\xinjianjiangzuo.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(zxkqrbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/marketing/onlineLecture/create",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)'''


'''编辑长期班
# "courseLevelCoursewareList":"[{"levelId":"0","coursewareList":[]}]",
# "courseLevelDetailList":"[{"levelId":"0","content":"","detailPic":[]}]"

xjcqbbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\bianjichangqiban.vm', 'r', encoding='utf-8', errors='ignore').read()
xjcqb_dict_data = json.loads(xjcqbbaowen)
print(xjcqb_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(xjcqb_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
tianjiajuese = sess.put("https://pycmspre.lexue.com/educational/course/updateCourse", data=json.loads(xjcqbbaowen))
print(tianjiajuese.text)'''


'''编辑讲座
bjjzbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\bianjijiangzuo.vm', 'r', encoding='utf-8', errors='ignore').read()
xjcqb_dict_data = json.loads(bjjzbaowen)
print(xjcqb_dict_data)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
tianjiajuese = sess.post("https://pycmspre.lexue.com/marketing/onlineLecture/edit", data=json.dumps(xjcqb_dict_data,ensure_ascii=True),verify=False, timeout=4)
print(tianjiajuese.text)'''


'''课程上架
kcsjbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\kechengshangjia.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(kcsjbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/educational/onlineClass/updateStatus", data=json.loads(kcsjbaowen))
print(tianjiajuese.text)'''



'''课程下架
kcxjbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\kechengxiajia.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(kcxjbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/educational/onlineClass/updateStatus", data=json.loads(kcxjbaowen))
print(tianjiajuese.text)'''


'''新建学生
xjxxbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianxuesheng.vm', 'r', encoding='utf-8', errors='ignore').read()
xjcqb_dict_data = json.loads(xjxxbaowen)
print(xjcqb_dict_data)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
tianjiajuese = sess.post("https://pycmspre.lexue.com/personnel/student/saveStudents", data=json.dumps(xjcqb_dict_data,ensure_ascii=True),verify=False, timeout=4)
print(tianjiajuese.text)'''


'''编辑学生-修改性别
bjxsbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\bianjixuesheng.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(bjxsbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmstsl.lexue.com/personnel/student/updateStudentsById", data=json.loads(bjxsbaowen))
print(tianjiajuese.text)'''


'''学生签到
xsqdbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xueshengqiandao.vm', 'r', encoding='utf-8', errors='ignore').read()
xjcqb_dict_data = json.loads(xsqdbaowen)
print(xjcqb_dict_data)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
tianjiajuese = sess.post("https://pycmspre.lexue.com/educational/sign/updateStudentsSign", data=json.dumps(xjcqb_dict_data,ensure_ascii=True),verify=False, timeout=4)
print(tianjiajuese.text)'''

'''新建代金卷
bjxsbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjiandaijinquan.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(bjxsbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.post("https://pycmspre.lexue.com/coupon/coupon/saveCoupon", data=json.loads(bjxsbaowen))
print(tianjiajuese.text)'''


'''新建限时购
xjxsgbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\\xinjianxianshigou.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(xjxsgbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.post("https://pycmspre.lexue.com/marketing/limittimePurchase/create", data=json.loads(xjxsgbaowen))
print(tianjiajuese.text)'''


'''关班
gbbaowen = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\guanban.vm', 'r', encoding='utf-8', errors='ignore').read()
sjqx_dict_data = json.loads(gbbaowen)
print(sjqx_dict_data)
# 获取 signature
tjjs_sginature = Signature().get_signature(sjqx_dict_data)
print(tjjs_sginature)
time.sleep(1)
sess.headers.update({'token':token,'signature':tjjs_sginature})
print(sess.headers)
tianjiajuese = sess.put("https://pycmspre.lexue.com/educational/classBase/updateBatchEndClassBase", data=json.loads(gbbaowen))
print(tianjiajuese.text)'''


'''在线课编辑
zxkbjbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\bianjizaixianke.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(zxkbjbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/educational/onlineClass/edit",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)
'''

'''新建教室
zxkbjbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\xinjianjiaoshi.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(zxkbjbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/basic/campus/saveClassroom",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)
'''

'''编辑教室
bjjsbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\bianjijiaoshi.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(bjjsbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
zxkresponse = sess.post("https://pycmspre.lexue.com/basic/campus/updateClassroom",data=json.dumps(zxkqr_dick_data,ensure_ascii=True),verify=False, timeout=4)
print(zxkresponse.text)'''

'''新建营销活动联报
xjyxhdbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\xinjianyingxiaohuodonglianbao.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(xjyxhdbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
respontext = sess.post("https://pycmspre.lexue.com/marketing/jointEnroll/create", data=json.dumps(zxkqr_dick_data, ensure_ascii=True), verify=False, timeout=4)
print(respontext.text)
'''


'''新建营销活动单科'''
xjyxhddkbaowen = open('D:\\zdhlog\\EKIA\\Python\\API\\autodata\\template\\xinjianyingxiaohuodongdanke.vm', 'r', encoding='utf-8', errors='ignore').read()
zxkqr_dick_data = json.loads(xjyxhddkbaowen)
time.sleep(1)
sess.headers.update({'Content-Type':'application/json'})
respontext = sess.post("https://pycmspre.lexue.com/marketing/jointEnroll/create", data=json.dumps(zxkqr_dick_data, ensure_ascii=True), verify=False, timeout=4)
print(respontext.text)






