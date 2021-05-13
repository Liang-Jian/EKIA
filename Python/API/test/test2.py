import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from autobase.SignatureUtil import Signature
import requests,json,hmac



# 取模板文件。 str

content = {"loginName":17611519238,"password":123456}

# str - json
# zhuangtai_dict = json.loads(content)
# print(zhuangtai_dict)
# 获取 signature
login_sginature = Signature().getSignature(content)
# print(login_sginature)
headerss = {
	"appKey":"201820011141153",
	"token": "123",
	"signature": login_sginature,
	"tenantId": "pycmstest",
	"Content-Type":"application/x-www-form-urlencoded"
}


sess = requests.session()
sess.auth=("token", "1234")
sess.headers.update(headerss)
login_response = sess.post(url='https://pycmstest.lexue.com/system/sysUser/login', stream='True', params=content, verify=False, timeout=4, headers=headerss)
# 取token
print(login_response.text)
token1 = eval(login_response.text).get('value').get('token')
userId = eval(login_response.text).get('value').get('sysUserId')


data2 = {
    'assistantTile': '222222',
    'campusStr': '499,476,465,453',
    'couponType': '1',
    'courseTypeFully': '1',
    'courseTypeStr': '1,2,3,4',
    'effectiveDays': '0',
    'gradeFully': '1',
    'gradeStr': '2125,2126,2127,2296',
    'mainTitle': '代金券100',
    'mutexFlag': '1',
    'overlay': '0',
    'preferentialAmt': '100',
    'reductionAmt': '0',
    'schoolId': '375',
    'seasonFully': '1',
    'seasonStr': '482,479,480,481',
    'subjectFully': '1',
    'subjectStr': '2142,2143,2144,2183,2184,2185,2194,2195',
    'Time': '',
    'totalStock': '10',
    'validityDays': '1',
    'validityType': '2'
}

siganture2 = Signature().getSignature(data2)

sess.headers.update(
	{
	 	'isAdmin':'2',
		'signature':siganture2,
		'token': token1,
		'userId':str(userId),
		# 'Content-Type':'application/x-www-form-urlencoded'
	 }
)

print(sess.headers)

res1 = sess.post(url='https://pycmstest.lexue.com/coupon/coupon/saveCoupon', data=data2, verify=False)
print(res1.text)