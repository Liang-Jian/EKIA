import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import requests,json,hmac

# 取模板文件。 str

content ={
        "pageSize": "10",
        "sort": 0,
        "longitude": "116.514390",
        "cityCode": "110100",
        "latitude": "39.992457",
        "isShowServiceMeCount": 0,
        "sex": 1,
        "pageNum": 3
}


seach ={
	"latitude": "39.992508",
	"longitude": "116.514413",
	"userId": "c1ed17fbb44c41acb4121dcc5537e8f7",
	"cityCode": "110100"
}

headerss = {
        "user-agent": "wang yue/30.79 (iPad; iOS 13.6.1; Scale/2.00)",
        "Content-Type":"application/json;charset=UTF-8"
}


sess = requests.session()
sess.headers.update(headerss)
login_response = sess.post(url='http://47.110.117.16:9010/api/v3/document/technician/technicianList',json=seach, verify=False, timeout=4)
# 取token
print(login_response.text)


r = requests.post(url="http://101.201.81.174:5000/b",json=login_response.json())
print(r.text)
