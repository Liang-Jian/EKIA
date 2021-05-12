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
	"pageSize": "10",
	"sort": 0,
	"longitude": "116.55116",
	"cityCode": "110100",
	"latitude": "39.967599",
	"name": "兰婷",
	"pageNum": 1
}


headerss = {
	"token": "123",
	"user-agent": "wang yue/30.79 (iPad; iOS 13.6.1; Scale/2.00)",
	"Content-Type":"application/json;charset=UTF-8"
}


sess = requests.session()
sess.headers.update(headerss)
login_response = sess.post(url='http://47.110.117.16:9010/api/v3/document/technician/technicianList',json=seach, verify=False, timeout=4)
# 取token
print(login_response.text)


