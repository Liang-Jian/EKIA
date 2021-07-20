# coding: utf8
import time,re

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




# # 取模板文件。 str
# content = open(r'D:\zdhlog\EKIA\python\API\autodata\template\cmslogin.vm','r',encoding='utf-8',errors='ignore').read()
#
# # str - json
# zhuangtai_data = json.loads(content)
# print(zhuangtai_data)
# # 获取 signature
# login_sginature = Signature().get_signature(zhuangtai_data)
# print(login_sginature)
#
#
#
# headerss = {
# 	"appKey":"201820011141153",
# 	"token": "123",
# 	"signature": "917B810FC675789F63C1AFA75BBF5A52AC81CC35",
# 	"tenantId": "pycmspre",
# 	"Content-Type":"application/x-www-form-urlencoded"
# }
#
#
# sess = requests.session()
# sess.auth=("token", "1234")
# sess.headers.update(headerss)
# # response = sess.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True', data=json.dumps(eval(content),ensure_ascii=True), verify=False, timeout=4,headers=headerss)
# login_response = sess.post('https://pycmspre.lexue.com/system/sysUser/login', stream='True', data=json.loads(content), verify=False, timeout=4, headers=headerss)
# print(login_response.text)
# # 取token
# token = eval(login_response.text).get('value').get('token')
# getcookies ={
# 	'token':token,
# 	'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74',
# 	'userId': '4656'
#
# }
#
#
# sess.headers.update({'token':token,'signature':'79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74'})
#
# print(sess.headers)
#
#
# sess.headers.update(
# 	{'userId': '4656',
# 	 'isAdmin':'2',
# 	 }
# )


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

zhuangtaibaowen = open(r'D:\zdhlog\EKIA\Python\API\\autodata\\template\\banjizhuangtai.vm','r',encoding='utf-8',errors='ignore').read()

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


'''新建引用课
生成课次表
post js 
https://pycmspre.lexue.com/educational/onlineClass/queryClassCourse
{"courseFirstDate":"2020-11-27","courseFrequency":3,"teacherId":4373,"teacherName":"杜岩松","classTimeId":5937,"classTimeName":"09:30~09:44","classStartTime":"09:30:00","classEndTime":"09:44:00","classRuleId":7053,"quoteStatus":0}/educational/onlineClass/queryClassCourse
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
    "teacherId" : 4373,
    "teacherName" : "杜岩松",
    "classDate" : "2020-11-27",
    "classStartTime" : "09:30:00",
    "classEndTime" : "09:44:00",
    "weekName" : "周五",
    "weekCode" : null,
    "occupationStatus" : null,
    "courseSort" : 1,
    "createTime" : null,
    "className" : null,
    "classCourseName" : null,
    "campusName" : null,
    "timeAndName" : null,
    "classTimeName" : "09:30~09:44",
    "classroomName" : null,
    "teacherOccupation" : 0,
    "classroomOccupation" : null,
    "timeCode" : 1,
    "timeName" : "上午",
    "courseStage" : "1/3",
    "coursePrice" : null,
    "dateStartTime" : "2020-11-27 09:30:00",
    "dateEndTime" : "2020-11-27 09:44:00",
    "classTimeId" : 5937,
    "classRuleId" : null,
    "receiveCourseNum" : null,
    "createUserId" : null,
    "createName" : null,
    "updateTime" : null,
    "updateUserId" : null,
    "updateName" : null,
    "courseFirstDate" : null,
    "courseFrequency" : null
  }, {
    "quoteStatus" : 0,
    "conflictTotal" : 0,
    "classCourseId" : null,
    "classId" : null,
    "campusId" : null,
    "classroomId" : null,
    "teacherId" : 4373,
    "teacherName" : "杜岩松",
    "classDate" : "2020-11-28",
    "classStartTime" : "09:30:00",
    "classEndTime" : "09:44:00",
    "weekName" : "周六",
    "weekCode" : null,
    "occupationStatus" : null,
    "courseSort" : 2,
    "createTime" : null,
    "className" : null,
    "classCourseName" : null,
    "campusName" : null,
    "timeAndName" : null,
    "classTimeName" : "09:30~09:44",
    "classroomName" : null,
    "teacherOccupation" : 0,
    "classroomOccupation" : null,
    "timeCode" : 1,
    "timeName" : "上午",
    "courseStage" : "2/3",
    "coursePrice" : null,
    "dateStartTime" : "2020-11-28 09:30:00",
    "dateEndTime" : "2020-11-28 09:44:00",
    "classTimeId" : 5937,
    "classRuleId" : null,
    "receiveCourseNum" : null,
    "createUserId" : null,
    "createName" : null,
    "updateTime" : null,
    "updateUserId" : null,
    "updateName" : null,
    "courseFirstDate" : null,
    "courseFrequency" : null
  }, {
    "quoteStatus" : 0,
    "conflictTotal" : 0,
    "classCourseId" : null,
    "classId" : null,
    "campusId" : null,
    "classroomId" : null,
    "teacherId" : 4373,
    "teacherName" : "杜岩松",
    "classDate" : "2020-11-29",
    "classStartTime" : "09:30:00",
    "classEndTime" : "09:44:00",
    "weekName" : "周日",
    "weekCode" : null,
    "occupationStatus" : null,
    "courseSort" : 3,
    "createTime" : null,
    "className" : null,
    "classCourseName" : null,
    "campusName" : null,
    "timeAndName" : null,
    "classTimeName" : "09:30~09:44",
    "classroomName" : null,
    "teacherOccupation" : 0,
    "classroomOccupation" : null,
    "timeCode" : 1,
    "timeName" : "上午",
    "courseStage" : "3/3",
    "coursePrice" : null,
    "dateStartTime" : "2020-11-29 09:30:00",
    "dateEndTime" : "2020-11-29 09:44:00",
    "classTimeId" : 5937,
    "classRuleId" : null,
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
新建
https://pycmspre.lexue.com/educational/onlineClass/create
{"classCapacity":25,"classTeacherId":4373,"orderScale":0,"singleTuitionFee":0,"courseTypeCode":1,"specialPrice":0,"className":"2020秋季小班综合不限","teacherType":1,"playType":1,"screenType":1,"school_share_flag":1,"mailFlag":0,"campusId":456,"yearId":484,"seasonId":481,"sectionId":2381,"gradeId":2299,"subjectId":2371,"levelId":0,"teacherId":4373,"courseFrequency":3,"tuitionFee":0,"schoolFee":0,"entryFee":0,"classPrice":"0.00","changeClassLimit":1,"changeAdjustLimit":1,"content":"","coverUrl":"https://picspy.lexue.com/avatar-employee-1606384702481","numLimit":25,"adjustLimit":0,"testClassFlag":0,"schoolId":379,"gradeName":"小班","limitEditFlag":1,"appTeacherName":"杜岩松","appTeacherId":"4373,4373,4373,4373,4373,4373","auditingStatus":0,"lowPriceClassFlag":0,"superNumberClassFlag":0,"specialClass":0,"classTeacherName":"杜岩松","schoolName":"北京总部","campusName":"乐学教育集团","classTimeName":"09:30~09:44","teacherName":"杜岩松","startTime":"2020-11-27 00:00:00","endTime":"2020-12-04 00:00:00","yearName":"2020","seasonName":"秋季","sectionName":"学龄前","subjectName":"综合","courseTypeName":"长期班","classTimeId":5937,"classDateStartTime":"2020-11-27 09:30:00","classDateEndTime":"2020-11-29 09:44:00","classCourseDtoList":[{"quoteStatus":0,"conflictTotal":0,"classCourseId":null,"classId":null,"campusId":null,"classroomId":null,"teacherId":4373,"teacherName":"杜岩松","classDate":"2020-11-27","classStartTime":"09:30:00","classEndTime":"09:44:00","weekName":"周五","weekCode":null,"occupationStatus":null,"courseSort":1,"createTime":null,"className":null,"classCourseName":"2020秋季小班综合不限第1讲","campusName":null,"timeAndName":null,"classTimeName":"09:30~09:44","classroomName":null,"teacherOccupation":0,"classroomOccupation":null,"timeCode":1,"timeName":"上午","courseStage":"1/3","coursePrice":null,"dateStartTime":"2020-11-27 09:30:00","dateEndTime":"2020-11-27 09:44:00","classTimeId":5937,"classRuleId":null,"receiveCourseNum":null,"createUserId":null,"createName":null,"updateTime":null,"updateUserId":null,"updateName":null,"courseFirstDate":null,"courseFrequency":null,"isEdit":false},{"quoteStatus":0,"conflictTotal":0,"classCourseId":null,"classId":null,"campusId":null,"classroomId":null,"teacherId":4373,"teacherName":"杜岩松","classDate":"2020-11-28","classStartTime":"09:30:00","classEndTime":"09:44:00","weekName":"周六","weekCode":null,"occupationStatus":null,"courseSort":2,"createTime":null,"className":null,"classCourseName":"2020秋季小班综合不限第2讲","campusName":null,"timeAndName":null,"classTimeName":"09:30~09:44","classroomName":null,"teacherOccupation":0,"classroomOccupation":null,"timeCode":1,"timeName":"上午","courseStage":"2/3","coursePrice":null,"dateStartTime":"2020-11-28 09:30:00","dateEndTime":"2020-11-28 09:44:00","classTimeId":5937,"classRuleId":null,"receiveCourseNum":null,"createUserId":null,"createName":null,"updateTime":null,"updateUserId":null,"updateName":null,"courseFirstDate":null,"courseFrequency":null,"isEdit":false},{"quoteStatus":0,"conflictTotal":0,"classCourseId":null,"classId":null,"campusId":null,"classroomId":null,"teacherId":4373,"teacherName":"杜岩松","classDate":"2020-11-29","classStartTime":"09:30:00","classEndTime":"09:44:00","weekName":"周日","weekCode":null,"occupationStatus":null,"courseSort":3,"createTime":null,"className":null,"classCourseName":"2020秋季小班综合不限第3讲","campusName":null,"timeAndName":null,"classTimeName":"09:30~09:44","classroomName":null,"teacherOccupation":0,"classroomOccupation":null,"timeCode":1,"timeName":"上午","courseStage":"3/3","coursePrice":null,"dateStartTime":"2020-11-29 09:30:00","dateEndTime":"2020-11-29 09:44:00","classTimeId":5937,"classRuleId":null,"receiveCourseNum":null,"createUserId":null,"createName":null,"updateTime":null,"updateUserId":null,"updateName":null,"courseFirstDate":null,"courseFrequency":null,"isEdit":false}],"classStartTime":"09:30:00","classEndTime":"09:44:00","managerList":[],"ruleId":7053,"schoolShareFlag":1,"ruleName":"测试直播间","courseVideoList":[],"detailPicList":[],"quoteStatus":0,"levelName":"不限","liveFlow":null,"gradeFully":1,"subjectFully":0}
'''




import datetime,calendar
def getNextSaturday():
    # 获取下一周 周六
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    m1 = calendar.SATURDAY
    while today.weekday() != m1:
        today += oneday
    nextMonday = today.strftime('%Y-%m-%d')
    print(nextMonday)
    return nextMonday


def calClassDay(icon=1):
    if icon == 1:
        start = "00:00:00"
        end = "00:15:00"
    elif icon == 2:
        start = "01:00:00"
        end = "01:15:00"
    elif icon == 3:
        pass
    td= datetime.date.today()               # today
    st= datetime.date.today()               # saturday
    sn= datetime.date.today()               # sunday
    today = datetime.date.today()
    print(td.isoweekday())
    if td.isoweekday() == 7:                # 如果是星期日取下个周六
        b_t = td.strftime('%Y-%m-%d {}'.format(start))
        a_t = getNextSaturday() + " {}".format(end)
        return b_t,a_t

    oneday = datetime.timedelta(days=1)
    while st.weekday() != 5:
        st += oneday
    while sn.weekday() != 6:
        sn += oneday
    b_t = st.strftime('%Y-%m-%d {}'.format(start))
    a_t = sn.strftime('%Y-%m-%d {}'.format(end))
    print(b_t,a_t)
    return b_t,a_t



s ='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<meta name="mobile-agent" content="format=html5; https://live.m.500.com/home/zq/jczq/2019-02-23">
<meta name="applicable-device" content="pc">
<title>190223足球比分直播-500彩票网</title>
<meta name="Keywords" content="190223足球比分直播" />
<meta name="Description" content="看2019年02月23日足球比分直播，上500彩票网！免费提供最快、最全、最准的比分2019年02月23日直播，中超、英超、欧冠、世界杯等热门赛事比分数据应有尽有！更有比分预测、战绩统计等服务助你赢大奖！" />
<link rel="canonical" href="https://live.500.com/"/>
<link href="https://www.500cache.com/live/css/new_main.css?v=2015128" rel="stylesheet" type="text/css" />
<link href="https://www.500cache.com/live/css/zq.css?v=20140527" rel="stylesheet" type="text/css" />
<link href="https://www.500cache.com/live/css/new_bifen.css?v=2015128" rel="stylesheet" type="text/css" />
</head>
<body>
<script type="text/javascript">
var pagestarttime=+new Date();
var _configs = _configs || {};
_configs.public_js = "https://www.500cache.com/public/js";
_configs.base_cache = _configs.public_js.replace(/\/public\/js/, "");
</script>
    <script type="text/javascript" src="https://www.500cache.com/public/js/public/core_jq.js"></script>
    <link href="//www.500cache.com/public/css/top_v2.css?v=2020-6-19" rel="stylesheet" type="text/css" />	
<div id="top_nav" class="topbar">
	<div class="div_m">
		<ul class="person_part">
			<li class="tips_li first phone_li">
				<a href="//www.500.com/wap/" target="_blank" title="500彩票网手机购彩平台" class="tips_hd hometc" aria-haspopup="true" onclick="stat4home('20130514','top_sj')"  rel="nofollow"><span class="topbar_icon icon_phone"></span>手机版<s class="arrow"></s></a>
				<div class="tips_bd">
					<div class="phone_tips_right">
						<p class="p_tit">扫描二维码下载</p>
						<p class="p_explain">使用手机二维码软件扫描下方二维码即可下载。</p>
						<p class="tc"><span class="topbar_icon icon_code"></span></p>
					</div>
				</div>
			</li>
		</ul>
		<ul class="person_part" id="lbefore">
			<li class="login_li"><a href="//passport.500.com/user/login/" onclick="stat4home('08071001','top_dl')" id="loginbtn_new" class="topbar_login" rel="nofollow">请登录</a><s class="vertical_line"></s></li>
			<li><a href="//passport.500.com/user/" onclick="stat4home('08071002','top_zc')" id="rigist_top" target="_blank" class="topbar_reg" rel="nofollow">免费注册</a><s class="vertical_line"></s></li>
		</ul>
		<ul class="person_part" id="lafter" style="display:none;">
			<li>欢迎您</li>
			<li class="tips_li account_li" id="account_li_tag">
				<span class="tips_hd" id="loginname_content"><a target="_blank" id="loginnamelink" aria-haspopup="true" onclick="stat4home('20130516','top_yhm')"></a></span>
				<div class="tips_bd">
					<ul style="height:110px">
						<li>余额：<span class="money" id="yemoney"></span></li>
						<li class="hb"><a href="javascript:;" class="hide_balance">隐藏</a>红包：<span class="money" id="hbmoney"></span></li>
						<li class="lineh_30">我的成长&#160;<a href="//vip.500.com" target="_blank" class="vipdengji_con" id="vip_grade" title="前往会员中心" rel="nofollow"><span style="" class="vipdengji_v"></span><span class="vipdengji_text"></span></a></li>
                        <li class="lineh_30">我的安全&#160;<a href="//trade.500.com/useraccount/default.php?url=//passport.500.com/useraccount/user/safe.php" title="前往安全首页" target="_blank" class="vipdengji_con" id="safe_odds" rel="nofollow"><span class="vipdengji_v"></span><span class="vipdengji_text"></span></a></li>
					</ul>
					<a href="javascript:;" class="show_balance">显示余额</a>
					<div class="my_account"><a href="javascript:;" class="btn_blue_l btn_blue_l_h18 login_out" onclick="stat4home('20130521','top_tc')" rel="nofollow" id="logouta">退出</a><a target="_blank" id="loginuserurl" rel="nofollow" onclick="stat4home('20130520','top_wdzh')">个人中心>></a></div>
				</div>
			</li>
			<li>
			     <a target="_blank" href="//trade.500.com/useraccount/default.php?tp=addmoney" onclick="stat4home('08071008','top_cz')" class="btn_recharge btn_orange btn_orange_h24" rel="nofollow">充值</a>
			     <a id="chongzhisong_tips" style="position:absolute;display:none;top:0px;*top:-2px; right:-7px;height:18px;" target="_blank" onclick="javascript:void(0)"><img width="16" height="18" alt="充值送" src="//www.500cache.com/public/images/song.gif" style="vertical-align:top" /></a>
		    </li>
            <li class="tips_li info_li" id="topmsg" style="display:none;">
                <a href="//trade.500.com/pages/trade/?strurl=//passport.500.com/pages/useraccount/usermsg/index.php" target="_blank" rel="nofollow" class="tips_hd" onclick="stat4home('20130523','top_zlx')">消息<span class="icon_num" data-key="all"></span><s class="arrow"></s></a>
                <div class="tips_bd">
                    <ul>
                        <li><a href="//trade.500.com/useraccount/default.php?url=https://passport.500.com/useraccount/usermsg/index.php?type=1" target="_blank" rel="nofollow">提醒<span data-key="warning"></span></a></li>
                        <li><a href="//trade.500.com/useraccount/default.php?url=https://passport.500.com/useraccount/usermsg/index.php?type=2" target="_blank" rel="nofollow">活动优惠<span data-key="huodong"></span></a></li>
                        <li><a href="//trade.500.com/useraccount/default.php?url=https://passport.500.com/useraccount/usermsg/index.php?type=3" target="_blank" rel="nofollow">系统通知<span data-key="system"></span></a></li>
                    </ul>
                    <a href="javascript:;" class="info_know" id="msg_btn_i_know"  rel="nofollow">我知道了</a>
                </div>
            </li>
		</ul>
		<ul class="site_link">
			<li><a href="//www.500.com/" target="_blank" onclick="stat4home('20130524','top_sy')"  title="500彩票网首页" id="hometc">首页</a><s class="vertical_line"></s></li>
			<li class="tips_li site_li">
				<s class="vertical_line"></s>
				<a href="javascript:void(0);"  class="tips_hd tradetc" aria-haspopup="true" title="" onclick="stat4home('20130525','top_gmcp')">彩票<s class="arrow"></s></a>
				<div class="tips_bd">
					<ul class="lottery_box"> 
      					<li class="first">
                        	<a class="lottery_tit jz" href="//trade.500.com/jczq/" target="_blank" title="竞彩足球">
                            <span class="jz"></span>
                            <h3>竞足</h3>
                            </a>
                            <p class="sub_lottery sub_lottery_1row">
                                <a href="//trade.500.com/jczq/" target="_blank" title="竞彩足球胜平负/让球" style="font-weight:bold; color:#E60010;">胜平负/让球</a>
                                <a href="//trade.500.com/jczq/index.php?playid=312&g=2" target="_blank" title="竞彩足球混合过关">混合过关</a>
                                <a href="//trade.500.com/jczq/index.php?playid=271&g=2" target="_blank" style="margin-right:0px;"  title="竞彩足球比分">比分</a>
                                <a href="//trade.500.com/jczq/index.php?playid=270&g=2" target="_blank" title="竞彩足球总进球数">进球数</a>
                                <a href="//trade.500.com/jczq/index.php?playid=272&g=2" target="_blank"  title="竞彩足球半全场">半全场</a>
                                <a href="//trade.500.com/jczq/?playid=312&g=1" target="_blank" title="竞彩足球单关投注">单关</a>
                            </p>
						</li>
                        <li data-type="jjtb" data-lot="jclq" data-left="35" data-top="-7">
                        <a class="lottery_tit" href="//trade.500.com/jclq/?playid=275&g=2" target="_blank" title="竞彩篮球">
                            <span class="jl"></span>
                            <h3>竞篮</h3>
                        </a>
                        <p class="sub_lottery">
                            <a target="_blank" href="//trade.500.com/jclq/" style="font-weight:bold; color:#E60010;" title="单关固赔、单场固定奖玩法投注">单关投注</a>
                            <a href="//trade.500.com/jclq/index.php?playid=275&g=2" target="_blank" title="竞彩篮球让分胜负">让分胜负</a>
                            <a href="//trade.500.com/jclq/?playid=274&g=2" target="_blank" title="竞彩篮球让分胜负">胜负</a>    
                            <a href="//trade.500.com/jclq/index.php?playid=276&g=2" target="_blank" title="竞彩篮球胜分差">胜分差</a>
                            <a href="//trade.500.com/jclq/index.php?playid=277&g=2" target="_blank" title="竞彩篮球大小分">大小分</a>
                            <a href="//trade.500.com/jclq/index.php?playid=313&g=2" target="_blank"  title="竞彩篮球混合过关">混合过关</a>
                        </p>                        
                    	</li>
						<li>
                        <a class="lottery_tit" href="//trade.500.com/bjdc/" target="_blank" title="足彩北京单场">
                            <span class="dc"></span>
                            <h3>单场</h3>
                        </a>
                        <p class="sub_lottery">
                            <a href="//trade.500.com/bjdc/" target="_blank"  title="足彩胜平负">胜平负</a>
                            <a href="//trade.500.com/bjdc/project_fq_bf.php" target="_blank"  style="margin-right:0px;" title="足球单场比分">比分</a>
                            <a href="//trade.500.com/bjdc/project_fq_bq.php" target="_blank" title="足球单场半全场，竞猜足球比赛半场结果和最终的全场结果">半全场</a>
                            <a href="//trade.500.com/bjdc/project_fq_jq.php" target="_blank" title="足球单场总进球">总进球数</a>
                            <a href="//trade.500.com/bjdc/project_fq_ds.php"  style="margin: 0px;" target="_blank" title="足球单场上下单双，大小球，进球数奇偶">上下单双</a>
                            <a target="_blank" href="//trade.500.com/bjdcsf/" style="margin: 0px;" title="单场胜负过关新玩法">胜负过关</a> 
                        </p>                        
                   		</li>
						<li>
                        <a class="lottery_tit" href="//trade.500.com/dlt/" target="_blank"  title="体彩超级大乐透">
                            <span class="szc"></span>
                            <h3>体彩</h3>
                        </a>
                        <p class="sub_lottery">
                            <a href="//trade.500.com/dlt/" target="_blank"  title="体彩超级大乐透">超级大乐透</a>
                            <a href="//trade.500.com/qxc/" target="_blank"  title="7星彩">7星彩</a>
                            <a href="//trade.500.com/pls/" target="_blank" title="体彩排列3">排列3</a>
                            <a href="//trade.500.com/plw/" target="_blank" title="体彩排列5">排列5</a>
                        </p>                        
                    	</li>
                        <li>
                        <a class="lottery_tit" href="//trade.500.com/sfc/" target="_blank" title="足彩胜负">
                            <span class="zc"></span>
                            <h3>足彩</h3>
                        </a>
                        <p class="sub_lottery">
                            <a href="//trade.500.com/sfc/" target="_blank" title="足彩胜负">足彩胜负</a>
                            <a href="//trade.500.com/rj/" target="_blank" title="足彩任选9场">任选<span class="eng">9场</span></a>
                            <a href="//trade.500.com/jqc/" target="_blank" title="足彩4场进球"><span class="eng">4</span>场进球</a>
                            <a href="//trade.500.com/bqc/" target="_blank"  title="足彩半全场"><span class="eng">6</span>场半全场</a>
                        </p>                        
                    	</li>                      
					</ul>
				</div>
			</li>
			<li><a href="//vip.500.com/" target="_blank" onclick="stat4home('40010011','top_vipcztx')" title="VIP会员成长中心"  rel="nofollow">会员</a><s class="vertical_line"></s></li>
			<li><a href="//zx.500.com/" target="_blank" onclick="stat4home('20130526','top_zx')"  title="彩票资讯">资讯</a><s class="vertical_line"></s></li>
			<li><a href="http://help.500.com/" target="_blank" onclick="stat4home('20130528','top_bz')"  rel="nofollow" title="购彩帮助" id="helptc">帮助</a><s class="vertical_line"></s></li>
			<li class="tips_li site_li site_li2">
				<s class="vertical_line"></s>
				<a href="//www.500.com/about/sitemap.shtml" class="tips_hd" target="_blank" aria-haspopup="true" onclick="stat4home('20130529','top_wzdh')">网站导航<s class="arrow"></s></a>
				<div class="tips_bd">
					<ul style="height:140px">
						<li class="first">
							<h3>
								<a href="//trade.500.com/" class="tradetc" target="_blank" title="500彩票网购彩大厅">彩票</a>
								<a href="//zx.500.com/" target="_blank" title="彩票资讯">彩票资讯</a>
								<a href="//www.500.com/wap/" target="_blank"  rel="nofollow" title="客户端下载">客户端下载</a>
								<a href="//zx.500.com/gongju/" target="_blank" class="last eng"  rel="nofollow" title="智能大数据">智能大数据</a>
							</h3>
						</li>
						<li>
							<p><a href="//zx.500.com/gongju/" target="_blank" title="智能大数据">智能大数据</a></p>
							<a target="_blank" href="//www.500.com/wap/index.php"  rel="nofollow" title="手机购彩客户端下载">手机客户端</a>
							<a target="_blank" href="//zx.500.com/calculator/dlt.php?type=jjjs" title="超级大乐透中奖计算">中奖计算器</a>
							<a target="_blank" href="//zx.500.com/calculator/" title="胜负彩复式计算器">复式计算器</a>
							<a target="_blank" href="//zx.500.com/zc/jjjs.php" title="足彩奖金计算器">奖金预算器</a>
							<!--<a target="_blank" href="https://soft.500.com/" title="彩票软件下载">彩票软件</a>-->
						</li>
						<li>
							<a class="blue" target="_blank" href="//www.500.com/tag/"  rel="nofollow" >热门标签</a>
							<a class="blue" target="_blank" href="//www.500.com/about/sitemap.shtml">更多内容</a>>>
						</li>
					</ul>
				</div>
			</li>
		</ul>
	</div>
</div> 
<script type="text/javascript" charset="gbk"  src="//www.500cache.com/public/js/public/top_v2_fortemp.js?v=20201127002"></script>


<!--登录弹出层-->
<div class="new_tips_box" id="loginform" style="display:none;">
    <div class="tips_title">
        <h2 class="tips_title_text">用户登录</h2>
        <a href="javascript:void(0)" class="tips_close" id="flclose">关闭</a>
    </div>
    <div class="tips_content">
        <form class="tips_form" method="post" action="" target="loginIframe" id="toploginform">
            <div class="dl_tips" id="loginerrdiv" style="display:none;"><b class="dl_err"></b><span id="loginerrmsg"></span></div>
            <table cellspacing="0" cellpadding="0" border="0" width="100%" id="loginformtable">
                <tr>
                    <td width="58">用户名：</td>
                    <td width="205"><input type="text" class="tips_txt" id="lu" name="u" placeholder="用户名/手机号码" /></td>
                    <td><a href="https://passport.500.com/user/" rel="nofollow" target="_blank" tabindex="-1" onClick="stat4home('08071101','dlc_mfzc')" class="font_size12 gray">免费注册</a><a class="icon-gift" href="//huodong.500.com/2018/newregisterforredpack/index.shtml" target="_blank"></a></td>
                </tr>
                <tr>
                    <td>密&nbsp;&nbsp;码：</td>
                    <td><input class="tips_txt" type="password" id="lp" name="p"/></td>
                    <td><a class="font_size12 gray" href="https://passport.500.com/user/getpwd.php" rel="nofollow" target="_blank" tabindex="-1">忘记密码</a></td>
                </tr>
                <tr>
                    <td>验证码：</td>
                    <td colspan="2"><input class="tips_yzm" type="text" id="yzmtext" name="c" style="ime-mode:disabled;" /><span class="tips_yzm_notice" id="yzm_tips"><span></span></span><img alt="验证码" id="yzmimg" height="25px" class="yzm_img" /><a href="javascript:void(0)" id="login_yzm_refresh" class="font_size12 yzm_btn">换一张</a></td>
                </tr>
                <tr>
                    <td>
                    	<input name="r" type="hidden" value="1" />
	                    <input type="hidden" name="t" value="4" />
	                    <input name="pwdlevel" id="pwdlevel" type="hidden" value="" />
	                    <input name="rw" type="hidden" value="/public/login.php?callback=parent.loginafter" />
                    </td>
                    <td colspan="2"><a class="btn_orange" href="javascript:void(0)" id="floginbtn">登录</a> &nbsp; <a class="font_size12 gray" href="http://help.500.com/h_wzhaq/20130403_327335.shtml" style="color:gray;position:absolute;display:inline-block;line-height:30px;" target="_blank">如何开启手机号登录？</a></td>
                </tr>
            </table>
        </form>
    </div>
	<iframe src="" name="loginIframe" id="loginIframe" style="display:none;"></iframe>
</div>
<link href="https://www.500cache.com/public/css/dxt/topmenuheader.css?v=20151210" rel="stylesheet">
<div id="header" class="header header2">
    <div class="header-in">
        <div class="header-l">
            <h1 class="header-logo">
            	<a href="https://www.500.com" target="_blank">500彩票</a>
            </h1>
        </div>
        <div class="header-r">
            <div class="header-tel">
                <p class="header-tel-500">500彩票网客服热线：4000-500-500</p>
            </div>
        </div>
    </div>
</div>
<div id="nav" class="nav">
	<div class="nav-in">
    <div class="nav-lott" id="nav-lott">
        <div class="nav-lott-hd"><a href="javascript:;" class="nav-lott-tit">选择彩种<span class="nav-ico-drop1"></span></a></div>
        <div class="nav-lott-bd clearfix">
            <div class="nav-lott-bd-in">
                <div class="nav-lott-itm nav-lott-dlt">
                    <div class="nav-lott-l">
                        <a class="nav-logo-dlt" href="https://trade.500.com/dlt/" title="体彩大乐透" target="_blank">超级大乐透</a>
                    </div>
                    <div class="nav-lott-r">
                        <div class="nav-lott-shd"><a href="https://trade.500.com/dlt/" class="nav-lott-stit">超级大乐透</a></div>
                        <div class="nav-lott-sbd">
                            <ul>
                                <li><a href="https://trade.500.com/dlt/" title="基本投注" target="_blank">基本投注</a></li>
                                <li><a href="https://trade.500.com/dlt/" title="复式投注" target="_blank">复式投注</a></li>
                                <li><a href="https://trade.500.com/dlt/?ptype=dt" title="胆拖投注" target="_blank">胆拖投注</a></li>
                                <li><a href="https://trade.500.com/dlt/?ptype=dd" title="定胆杀号" target="_blank">定胆杀号</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="nav-lott-itm nav-lott-jz">
                    <div class="nav-lott-l">
                        <a href="https://trade.500.com/jczq/?playid=269&g=2" class="nav-logo-jz" target="_blank">竞彩足球</a>
                    </div>
                    <div class="nav-lott-r">
					    <div class="nav-lott-shd"><a href="https://trade.500.com/jczq/?playid=269&g=2" class="nav-lott-stit" target="_blank">竞彩足球</a></div>
                        <div class="nav-lott-sbd">
                            <ul>
                                <li><a href="https://trade.500.com/jczq/" target="_blank">单关投注</a></li>
                                <li><a href="https://trade.500.com/jczq/?playid=269&amp;g=2" target="_blank">胜平负/让球</a></li>
                                <li><a href="https://trade.500.com/jczq/?playid=312&amp;g=2" target="_blank">混合过关</a></li>
                                <li><a href="https://trade.500.com/jczq/?playid=271&amp;g=2" target="_blank">比分</a></li>
                                <li><a href="https://trade.500.com/jczq/?playid=270&amp;g=2" target="_blank">进球数</a></li>
                                <li><a href="https://trade.500.com/jczq/?playid=272&amp;g=2" target="_blank">半全场</a></li>
                                <li><a href="https://trade.500.com/gyj/" target="_blank">冠亚军</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="nav-lott-itm nav-lott-jl">
                	<div class="nav-lott-l"><a href="https://trade.500.com/jclq/?playid=275&amp;g=1" class="nav-logo-jl" title="竞彩篮球" target="_blank">竞彩篮球</a></div>
                    <div class="nav-lott-r"><div class="nav-lott-shd"><a href="https://trade.500.com/jclq/?playid=275&amp;g=1" class="nav-lott-stit">竞彩篮球</a></div>
                        <div class="nav-lott-sbd">
                            <ul>
                                <li><a href="https://trade.500.com/jclq/?playid=275&amp;g=1" target="_blank">单关投注</a></li>
                                <li><a href="https://trade.500.com/jclq/" target="_blank" title="竞彩篮球胜负">胜负</a></li>
                                <li><a href="https://trade.500.com/jclq/?playid=275" target="_blank" title="竞彩篮球让分胜负">让分胜负</a></li>
                                <li><a href="https://trade.500.com/jclq/?playid=276" target="_blank" title="竞彩篮球胜分差">胜分差</a></li>
                                <li><a href="https://trade.500.com/jclq/?playid=277" target="_blank" title="竞彩篮球大小分">大小分</a></li>
                                <li><a href="https://trade.500.com/jclq/?playid=313&g=2" target="_blank" title="竞彩篮球混合过关">混合过关</a></li>
                            </ul>
                        </div>
                    </div>
                </div>


				<div class="nav-lott-itm nav-lott-zc">
					<div class="nav-lott-l"> <a href="https://trade.500.com/sfc/" class="nav-logo-zc" target="_blank" id="link44">足彩</a> </div>
					<div class="nav-lott-r">
						<div class="nav-lott-shd"><a href="https://trade.500.com/sfc/" class="nav-lott-stit" target="_blank" id="link45">足彩</a></div>
						<div class="nav-lott-sbd">
							<ul>
								<li><a href="https://trade.500.com/sfc/" target="_blank" id="link46">胜负彩</a></li>
								<li><a href="https://trade.500.com/rj/" target="_blank" id="link47">任选九</a></li>
								<li><a href="https://trade.500.com/bqc/" target="_blank" id="link48">半全场</a></li>
								<li><a href="https://trade.500.com/jqc/" target="_blank" id="link49">进球彩</a></li>
							</ul>
						</div>
					</div>
				</div>
				<div class="nav-lott-itm nav-lott-lt">
					<div class="nav-lott-l"> <a href="https://trade.500.com/qxc/" class="nav-logo-lt" target="_blank" id="link50">乐透</a> </div>
					<div class="nav-lott-r">
						<div class="nav-lott-shd"><a href="https://trade.500.com/pls/" class="nav-lott-stit" target="_blank" id="link51">排列3</a><a href="https://trade.500.com/plw/" class="nav-lott-stit" target="_blank" id="link52">排列5</a><a href="https://trade.500.com/qxc/" class="nav-lott-stit" target="_blank" id="link53">7星彩</a></div>
					</div>
				</div>

            </div>
        </div>
    </div>
    <ul class="nav-list">
        <li class="nav-home"><a href="https://www.500.com" target="_blank">首页</a></li>
        <li><a href="//kaijiang.500.com/" target="_blank">全国开奖</a></li>
        <li><a href="//datachart.500.com/" target="_blank">数据图表</a></li>
        <li class="jNavDrop">
            <a href="//live.500.com" target="_blank">足球比分<span class="nav-ico-drop2"></span></a>
            <div class="nav-list-drop jNavDropBD">
                <a href="//live.500.com/lq.php" target="_blank">篮球比分</a>
                <a href="//live.500.com/tennis/" target="_blank">网球比分</a>
            </div>
        </li>
        <li class="jNavDrop">
            <a href="//liansai.500.com" target="_blank">足球联赛<span class="nav-ico-drop2"></span></a>
            <div class="nav-list-drop jNavDropBD">
                <a href="//liansai.500.com/lq/" target="_blank">篮球联赛</a>
            </div>
        </li>
        <li class="jNavDrop">
            <a href="//zx.500.com" target="_blank">彩票资讯</a>            
        </li>
        <!--li><a href="https://huodong.500.com/main/" target="_blank">活动专区</a></li-->
        <li><a href="http://help.500.com/" target="_blank">帮助中心</a></li>
		<li class="itm-sj"><a href="//www.500.com/wap/" target="_blank">客户端下载</a></li>
		<li class="itm-dlt"><a href="//zx.500.com/gongju/" target="_blank">智能大数据</a></li>
		<li><a href="https://football.choopaoo.com/client/main/index.html" target="_blank">500联赛</a></li>
    </ul>
</div>
</div>
<script>
$(function(){
if(!document.getElementsByClassName){document.getElementsByClassName=function(e,d){var c=(d||document).getElementsByTagName("*");var f=new Array();for(var b=0;b<c.length;b++){var h=c[b];var g=h.className.split(" ");for(var a=0;a<g.length;a++){if(g[a]==e){f.push(h);break}}}return f}};
if(document.cookie.indexOf('fromtc')==-1){var bar = document.getElementById('top_nav');/*transition style,after it will be unified*/document.getElementsByClassName('div_m')[0].style.width = '1180px';bar.style.height = '34px';bar.style.fontSize = '12px';}
var yu = location.host.split(".").shift(),l = document.getElementsByClassName('nav-list')[0].getElementsByTagName('a'),lotlist = document.getElementById('nav-lott'),header = document.getElementById('nav'),headernav = document.getElementsByClassName('jNavDrop');
for(i=0;i<l.length;i++){if(l[i].href.indexOf(yu)>0){l[i].parentNode.className  = l[i].parentNode.className + ' cur';}}
lotlist.onmouseover = function(){header.className.indexOf('nav-lott-on')==-1?(header.className =  header.className +' nav-lott-on') :''; }
lotlist.onmouseout = function(){header.className =  header.className.replace(' nav-lott-on',''); }
for(i=0;i<headernav.length;i++){headernav[i].onmouseover = function(){this.className.indexOf('on')==-1?(this.className =  this.className +' on') :''; };headernav[i].onmouseout = function(){this.className =  this.className.replace(' on',''); }}
})
</script>


<div class="topad" style="height: 60px;" id="live_top_ad"><a href="javascript:void(0)" style="z-index:100" title="关闭" class="ggclose" onclick="$(this).parent().hide();return false">关闭</a> 
<div style="float:left;">
<a  href="https://zx.500.com/gongju/?from=bifen" target="_blank" title="" onclick="if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000424','DCSext.button_n','10059756');}" {$appShowHtml} ><img  src="https://img.500.com/upimages/sfc/202007/20200709165835_3196.jpg" border="0" width="720" height="60" alt="" align="top" /></a><script>setTimeout(function(){ if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000424','DCSext.button_n','00059756');}},3000)</script>
</div>
<div id='uma'>
<a  href="https://www.sanyol.cn/mesporthome/?channelCode=10001&from=pcbifen" target="_blank" title="" onclick="if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000425','DCSext.button_n','10053924');}" {$appShowHtml} ><img  src="https://img.500.com/upimages/sfc/201912/20191219140323_7727.jpg" border="0" width="460" height="60" alt="" align="top" /></a><script>setTimeout(function(){ if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000425','DCSext.button_n','00053924');}},3000)</script>
</div>
</div><div id="bd">
<div class="wrap"  >
    <div class="bf_nav">
    <ul class="tab" id="menu_ul">
      <li><a title="足球比分完整版" href="/2h1.php">完整版</a></li>
      <li><a title="单场即时比分" href="/zqdc.php">单场比分</a></li>
      <li><a title="竞彩足球比分" href="/">竞彩比分</a></li>
      <li><a title="足彩比分" href="/zucai.php">足彩比分</a></li>
      <li><a title="完场即时比分" href="/wanchang.php">完场比分</a></li>
      <li><a title="未来赛事" href="/weekfixture.php">未来赛事</a></li>
    </ul>
<script type="text/javascript">
(function(a,b,c,d,e,i){
	for (i=0; i<c.length; i++) {
		if ((new RegExp('/'+c[i]+'\\.(php|shtml)$')).test(a)) {
			d = i;
			e = a.match(/\/(\w+)\.(?:php|shtml)$/)[1];
			break;
		}
	}
	b[d].className = 'cur';
	window.live_type = e;
})( location.pathname,
	document.getElementById('menu_ul').getElementsByTagName('LI'),
	['2h1','zqdc','index','(zucai|6chang|4chang)','wanchang','weekfixture'],
	2, 'index'
);
</script>
    <div class="r">
      <label for="check_voice"><input type="checkbox" id="check_voice" checked="checked" />进球声</label>&nbsp;
      <label for="check_win"><input type="checkbox" id="check_win" checked="checked" />进球弹窗</label>&nbsp;
      <label for="ck_y_1"><input type="radio" name="check_lang" id="ck_y_1" value="0" checked="checked" />国语</label>&nbsp;
      <label for="ck_y_2"><input type="radio" name="check_lang" id="ck_y_2" value="1" />粤语</label>
    </div>
  </div>
  <div class="bf_btn"> <div class="l"><span class="dot">
    <input type="button" value="保留选中" class="btn_gray_s" id="btn_match_show" />
    </span>&nbsp;
    <input type="button" value="隐藏选中" class="btn_gray_s" id="btn_match_hide" />&nbsp;
    <span class="btn_select_w"><a href="javascript:void(0)" class="btn_select" id="btn_league">赛事选择</a> <span class="layer lsxz" id="layer_league">
    <div class="sx"><label for="ck_s_0"><input type="radio" name="check_status" id="ck_s_0" value=".+" checked="checked" />所有比赛</label>&nbsp;
    <label for="ck_s_1"><input type="radio" name="check_status" id="ck_s_1" value="0" />未开场</label>&nbsp;
    <label for="ck_s_2"><input type="radio" name="check_status" id="ck_s_2" value="4" />已完场</label>&nbsp;
    <label for="ck_s_3"><input type="radio" name="check_status" id="ck_s_3" value="[1-3]" />进行中</label></div>
    <table width="300" border="0" align="center" cellpadding="2" cellspacing="0">
	    
      <tr>
	
        <td><label for="ck_l_39"><input id="ck_l_39" type="checkbox" name="check_league[]" value="39" checked="checked" /><span class="team" style="background:#017001">日职</span>[5]</label></td>	
        <td><label for="ck_l_312"><input id="ck_l_312" type="checkbox" name="check_league[]" value="312" checked="checked" /><span class="team" style="background:#336699">澳超</span>[1]</label></td>	
        <td><label for="ck_l_32"><input id="ck_l_32" type="checkbox" name="check_league[]" value="32" checked="checked" /><span class="team" style="background:#DB31EE">德乙</span>[4]</label></td>
      </tr>	    
      <tr>
	
        <td><label for="ck_l_58"><input id="ck_l_58" type="checkbox" name="check_league[]" value="58" checked="checked" /><span class="team" style="background:#990099">德甲</span>[3]</label></td>	
        <td><label for="ck_l_106"><input id="ck_l_106" type="checkbox" name="check_league[]" value="106" checked="checked" /><span class="team" style="background:#FF1717">英超</span>[2]</label></td>	
        <td><label for="ck_l_62"><input id="ck_l_62" type="checkbox" name="check_league[]" value="62" checked="checked" /><span class="team" style="background:#CC3300">英冠</span>[11]</label></td>
      </tr>	    
      <tr>
	
        <td><label for="ck_l_93"><input id="ck_l_93" type="checkbox" name="check_league[]" value="93" checked="checked" /><span class="team" style="background:#006633">西甲</span>[2]</label></td>	
        <td><label for="ck_l_71"><input id="ck_l_71" type="checkbox" name="check_league[]" value="71" checked="checked" /><span class="team" style="background:#008888">葡超</span>[3]</label></td>	
        <td><label for="ck_l_107"><input id="ck_l_107" type="checkbox" name="check_league[]" value="107" checked="checked" /><span class="team" style="background:#663333">法甲</span>[2]</label></td>
      </tr>	    
      <tr>
	
        <td><label for="ck_l_91"><input id="ck_l_91" type="checkbox" name="check_league[]" value="91" checked="checked" /><span class="team" style="background:#ff6699">荷甲</span>[3]</label></td>	
        <td><label for="ck_l_92"><input id="ck_l_92" type="checkbox" name="check_league[]" value="92" checked="checked" /><span class="team" style="background:#0066FF">意甲</span>[1]</label></td>	
        <td><label for="ck_l_" style="display:none;"><input id="ck_l_" style="display:none;" type="checkbox" name="check_league[]" value="" style="display:none;" checked="checked" /><span class="team" style="background:"></span></label></td>
      </tr>      
    </table>
    <div class="btn"><input type="button" value="全选" class="btn_Lblue_m" id="btn_league_all" />&nbsp;&nbsp;<input type="button" value="反选" class="btn_Lblue_m" id="btn_league_opp" />&nbsp;&nbsp;<input type="button" value="关闭" class="btn_Lblue_m" id="btn_league_close" /></div>
    </span></span>&nbsp;<span class="btn_select_w"><a href="javascript:void(0)" class="btn_select" id="btn_function">功能选择</a> <span class="layer lsxz" id="layer_function">
    <div class="sx"><label for="check_pk"><input type="checkbox" id="check_pk" checked="checked" />盘口提示</label><br />
<label for="check_card"><input type="checkbox" id="check_card" checked="checked" />红牌提示</label><br />
<label for="check_rank"><input type="checkbox" id="check_rank" checked="checked" />球队排名</label></div>

<table border="0" align="center" cellpadding="2" cellspacing="0">
  <tr>
    <td>进球声</td>
    <td><select id="sel_voice">
      <option value="0">无声</option>
      <option value="7" selected="selected">默认</option>
      <option value="2">经典</option>
	  <option value="5">喇叭</option>
	  <option value="6">哨子</option>
	  <option value="4">号角</option>
	  <option value="1">鸟鸣</option>
    </select></td>
  </tr>
  <tr>
    <td>提示窗</td>
    <td><select id="sel_win">
      <option value="0">正上方</option>
	  <option value="1">正下方</option>
	  <option value="2">正左方</option>
	  <option value="3">正右方</option>
	  <option value="4">左上方</option>
	  <option value="5">右上方</option>
	  <option value="6">左下方</option>
	  <option value="7">右下方</option>
    </select></td>
  </tr>
  <tr>
    <td>背景皮肤</td>
    <td><select id="sel_skin">
      <option value="0">默认</option>
      <option value="1">酷炫紫</option>
      <option value="2">海洋蓝</option>
      <option value="3">天空蓝</option>
      <option value="4">草地绿</option>
    </select></td> 
  </tr>
	<tr>
		<td>公司</td><td><select id="sel_company">
			<option value="3">Bet365</option>
			<option value="5">澳门</option>
		</select></td>
	</tr>
</table>

    <div class="btn"><input type="button" value="关闭" class="btn_Lblue_m" id="btn_function_close" /></div>
    </span></span>&nbsp;&nbsp;共37场 隐藏<span class="red" id="hide_count">0</span>场&nbsp;&nbsp;<a href="javascript:void(0)" id="show_all">显示全部</a></div>
    <div class="r"><a href="javascript:void(0);" id="importProject" class="btn_Lblue_m">方案直播</a> | <a href="http://zx.500.com/jczq/kaijiang.php" target="_blank">赛果开奖</a> | <a href="http://zx.500.com/jczq/paihang/" target="_blank">中奖排行榜</a> | <a href="http://help.500.com/jczq/help_01.shtml" target="_blank">玩法介绍</a> |
	<select id="sel_expect">
      <option value="2019-02-23">2019-02-23</option>
    </select></div>
    </div>
  <table width="100%" cellspacing="0" cellpadding="0" class="bf_tablelist01" id="table_match">
  <thead>
  <tr>
    <td width="80" align="center" class="td_title01">场次</td>
    <td width="70" align="center" class="td_title01">赛事</td>
    <td width="70" align="center" class="td_title01">轮次</td>
    <td width="90" align="center" class="td_title01">比赛时间</td>
    <td width="40" align="center" class="td_title01">状态</td>
    <td width="150" align="center" class="td_title01">主队</td>
    <td width="120" align="center" class="td_title01">比分</td>
    <td width="150" align="center" class="td_title01">客队</td>
    <td width="60" align="center" class="td_title01">半场</td>
    <td width="130" align="center" class="td_title01">
        <select id="sel_odds">
            <option value="sp" selected>胜负奖金</option>
            <option value="rqsp">让球奖金</option>
            <option value="0">平均欧赔</option>
            <option value="293">威廉希尔</option>
            <option value="5">澳门彩票</option>
            <option value="3">bet365</option>
            <option value="280">皇冠</option>
        </select>
    </td>
    <td width="60" align="center" class="td_title01"><select id="sel_result">
        <option value="5" selected>胜负</option>
        <option value="0">让球</option>
		<option value="1">进球</option>
		<option value="2">比分</option>
		<option value="3">半全</option>
      </select></td>
    <td align="center" class="td_title01">分析</td>
    <td width="40" align="center" class="td_title01">置顶</td>
  </tr>
  </thead>
  <tbody>
	  	
  <tr id="a779380" order="6001" status="4" gy="日职,川崎前锋,东京FC" yy="日职,川崎前鋒,FC東京" lid="39" fid="779380" sid="5126" class="" infoid="129375" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="779380" />周六001</td>
    <td bgcolor="#017001" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5126/">日职</a></td>
    <td align="center">第1轮</td>
    <td align="center">02-23 13:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[06]</span><span class="yellowcard">3</span><a target="_blank" href="//liansai.500.com/team/2272/">川崎前锋</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=779380&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=779380&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球">半球</a><a href="./detail.php?fid=779380&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/267/">东京FC</a><span class="yellowcard">2</span><span class="gray">[17]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-779380.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-779380.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-779380.shtml">欧</a> <a target="_blank" id="qing_779380" class="red hide"   href="//odds.500.com/fenxi/youliao-779380.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a779384" order="6002" status="4" gy="日职,鸟栖沙岩,名古屋鲸" yy="日职,鳥栖沙岩,名古屋八鯨" lid="39" fid="779384" sid="5126" class="bg02" infoid="129376" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="779384" />周六002</td>
    <td bgcolor="#017001" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5126/">日职</a></td>
    <td align="center">第1轮</td>
    <td align="center">02-23 13:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[04]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/3839/">鸟栖沙岩</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=779384&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=779384&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手">平手</a><a href="./detail.php?fid=779384&r=1" target="_blank" class="clt3" >4</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1100/">名古屋鲸</a><span class="yellowcard">2</span><span class="gray">[11]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-779384.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-779384.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-779384.shtml">欧</a> <a target="_blank" id="qing_779384" class="red hide"   href="//odds.500.com/fenxi/youliao-779384.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a779378" order="6003" status="4" gy="日职,仙台七夕,浦和红钻" yy="日职,仙台维加泰,浦和紅鑽" lid="39" fid="779378" sid="5126" class="" infoid="129377" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="779378" />周六003</td>
    <td bgcolor="#017001" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5126/">日职</a></td>
    <td align="center">第1轮</td>
    <td align="center">02-23 13:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[07]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1296/">仙台七夕</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=779378&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=779378&r=1" target="_blank" class="fhuise" data-ao="受平手/半球" data-pb="受半球">受半球</a><a href="./detail.php?fid=779378&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1164/">浦和红钻</a><span class="yellowcard">2</span><span class="gray">[09]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-779378.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-779378.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-779378.shtml">欧</a> <a target="_blank" id="qing_779378" class="red hide"   href="//odds.500.com/fenxi/youliao-779378.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a779390" order="6004" status="4" gy="日职,大阪钢巴,横滨水手" yy="日职,大阪飛腳,橫濱水手" lid="39" fid="779390" sid="5126" class="bg02" infoid="129378" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="779390" />周六004</td>
    <td bgcolor="#017001" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5126/">日职</a></td>
    <td align="center">第1轮</td>
    <td align="center">02-23 14:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[16]</span><a target="_blank" href="//liansai.500.com/team/752/">大阪钢巴</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=779390&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=779390&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手">平手</a><a href="./detail.php?fid=779390&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/870/">横滨水手</a><span class="gray">[13]</span></td>
    <td align="center" class="red">1 - 3</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-779390.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-779390.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-779390.shtml">欧</a> <a target="_blank" id="qing_779390" class="red hide"   href="//odds.500.com/fenxi/youliao-779390.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a779386" order="6005" status="4" gy="日职,鹿岛鹿角,大分三神" yy="日职,鹿島鹿角,大分三神" lid="39" fid="779386" sid="5126" class="" infoid="129379" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="779386" />周六005</td>
    <td bgcolor="#017001" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5126/">日职</a></td>
    <td align="center">第1轮</td>
    <td align="center">02-23 14:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[12]</span><a target="_blank" href="//liansai.500.com/team/1029/">鹿岛鹿角</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=779386&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=779386&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球/一球">半球/一球</a><a href="./detail.php?fid=779386&r=1" target="_blank" class="clt3" >2</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/754/">大分三神</a><span class="yellowcard">1</span><span class="gray">[15]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-779386.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-779386.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-779386.shtml">欧</a> <a target="_blank" id="qing_779386" class="red hide"   href="//odds.500.com/fenxi/youliao-779386.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a765034" order="6006" status="4" gy="澳超,墨胜利,墨尔本城" yy="澳超,墨爾本勝利,墨尔本中心" lid="312" fid="765034" sid="5016" class="bg02" infoid="129380" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="765034" />周六006</td>
    <td bgcolor="#336699" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-5016/">澳超</a></td>
    <td align="center">第20轮</td>
    <td align="center">02-23 16:50</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[03]</span><span class="yellowcard">6</span><span class="redcard">1</span><a target="_blank" href="//liansai.500.com/team/3615/">墨胜利</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=765034&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=765034&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=765034&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/6245/">墨尔本城</a><span class="yellowcard">4</span><span class="gray">[05]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-765034.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-765034.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-765034.shtml">欧</a> <a target="_blank" id="qing_765034" class="red hide"   href="//odds.500.com/fenxi/youliao-765034.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a738216" order="6007" status="4" gy="德乙,科隆,桑德豪森" yy="德乙,科隆,桑德豪森" lid="32" fid="738216" sid="4854" class="" infoid="129381" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="738216" />周六007</td>
    <td bgcolor="#DB31EE" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4854/">德乙</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 20:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[03]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/932/">科隆</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=738216&r=1" target="_blank" class="clt1" >3</a><a href="./detail.php?fid=738216&r=1" target="_blank" class="fhuise" data-ao="一球/球半" data-pb="一球/球半">一球/球半</a><a href="./detail.php?fid=738216&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/3716/">桑德豪森</a><span class="yellowcard">4</span><span class="gray">[17]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-738216.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-738216.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-738216.shtml">欧</a> <a target="_blank" id="qing_738216" class="red hide"   href="//odds.500.com/fenxi/youliao-738216.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a738220" order="6008" status="4" gy="德乙,圣保利,因戈施塔" yy="德乙,聖保利,恩高斯達特" lid="32" fid="738220" sid="4854" class="bg02" infoid="129382" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="738220" />周六008</td>
    <td bgcolor="#DB31EE" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4854/">德乙</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 20:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[06]</span><span class="yellowcard">5</span><a target="_blank" href="//liansai.500.com/team/495/">圣保利</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=738220&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=738220&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手">平手</a><a href="./detail.php?fid=738220&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/2918/">因戈施塔</a><span class="redcard">1</span><span class="yellowcard">3</span><span class="gray">[16]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-738220.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-738220.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-738220.shtml">欧</a> <a target="_blank" id="qing_738220" class="red hide"   href="//odds.500.com/fenxi/youliao-738220.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a738215" order="6009" status="4" gy="德乙,达姆施塔,德累斯顿" yy="德乙,達蒙士達,特雷斯登" lid="32" fid="738215" sid="4854" class="" infoid="129383" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="738215" />周六009</td>
    <td bgcolor="#DB31EE" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4854/">德乙</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 20:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[14]</span><span class="yellowcard">3</span><a target="_blank" href="//liansai.500.com/team/1926/">达姆施塔</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=738215&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=738215&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=738215&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/4654/">德累斯顿</a><span class="yellowcard">5</span><span class="gray">[12]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-738215.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-738215.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-738215.shtml">欧</a> <a target="_blank" id="qing_738215" class="red hide"   href="//odds.500.com/fenxi/youliao-738215.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a738214" order="6010" status="4" gy="德乙,波鸿,基尔" yy="德乙,波琴,基爾" lid="32" fid="738214" sid="4854" class="bg02" infoid="129384" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="738214" />周六010</td>
    <td bgcolor="#DB31EE" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4854/">德乙</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 20:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[08]</span><a target="_blank" href="//liansai.500.com/team/695/">波鸿</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=738214&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=738214&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手">平手</a><a href="./detail.php?fid=738214&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1915/">基尔</a><span class="yellowcard">3</span><span class="gray">[07]</span></td>
    <td align="center" class="red">0 - 3</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-738214.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-738214.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-738214.shtml">欧</a> <a target="_blank" id="qing_738214" class="red hide"   href="//odds.500.com/fenxi/youliao-738214.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a737749" order="6011" status="4" gy="德甲,门兴,沃夫斯堡" yy="德甲,慕遜加柏,沃爾夫斯堡" lid="58" fid="737749" sid="4852" class="" infoid="129385" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="737749" />周六011</td>
    <td bgcolor="#990099" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4852/">德甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 22:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[03]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1089/">门兴</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=737749&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=737749&r=1" target="_blank" class="fhuise" data-ao="半球" data-pb="半球">半球</a><a href="./detail.php?fid=737749&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1269/">沃夫斯堡</a><span class="yellowcard">1</span><span class="gray">[06]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 <a href="http://live.500.com/tv/737749/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-737749.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-737749.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-737749.shtml">欧</a> <a target="_blank" id="qing_737749" class="red hide"   href="//odds.500.com/fenxi/youliao-737749.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a737753" order="6012" status="4" gy="德甲,弗赖堡,奥格斯堡" yy="德甲,費雷堡,奥格斯堡" lid="58" fid="737753" sid="4852" class="bg02" infoid="129386" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="737753" />周六012</td>
    <td bgcolor="#990099" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4852/">德甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 22:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[13]</span><a target="_blank" href="//liansai.500.com/team/804/">弗赖堡</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=737753&r=1" target="_blank" class="clt1" >5</a><a href="./detail.php?fid=737753&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=737753&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1923/">奥格斯堡</a><span class="redcard">1</span><span class="yellowcard">3</span><span class="gray">[15]</span></td>
    <td align="center" class="red">3 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 <a href="http://live.500.com/tv/737753/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-737753.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-737753.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-737753.shtml">欧</a> <a target="_blank" id="qing_737753" class="red hide"   href="//odds.500.com/fenxi/youliao-737753.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a731167" order="6013" status="4" gy="英超,伯恩茅斯,狼队" yy="英超,般尼茅夫,狼隊" lid="106" fid="731167" sid="4826" class="" infoid="129387" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="731167" />周六013</td>
    <td bgcolor="#FF1717" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4826/">英超</a></td>
    <td align="center">第27轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[11]</span><span class="yellowcard">4</span><a target="_blank" href="//liansai.500.com/team/667/">伯恩茅斯</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=731167&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=731167&r=1" target="_blank" class="fhuise" data-ao="受平手/半球" data-pb="受平手/半球">受平手/半球</a><a href="./detail.php?fid=731167&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/978/">狼队</a><span class="yellowcard">6</span><span class="gray">[08]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 <a href="http://live.500.com/tv/731167/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-731167.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-731167.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-731167.shtml">欧</a> <a target="_blank" id="qing_731167" class="red hide"   href="//odds.500.com/fenxi/youliao-731167.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735124" order="6014" status="4" gy="英冠,伯明翰,布莱克本" yy="英冠,伯明翰,布力般流浪" lid="62" fid="735124" sid="4843" class="bg02" infoid="129388" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735124" />周六014</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[09]</span><a target="_blank" href="//liansai.500.com/team/701/">伯明翰</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735124&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=735124&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=735124&r=1" target="_blank" class="clt3" >2</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/723/">布莱克本</a><span class="yellowcard">2</span><span class="gray">[14]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735124.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735124.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735124.shtml">欧</a> <a target="_blank" id="qing_735124" class="red hide"   href="//odds.500.com/fenxi/youliao-735124.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735125" order="6015" status="4" gy="英冠,布伦特,赫尔城" yy="英冠,賓福特,赫尔城" lid="62" fid="735125" sid="4843" class="" infoid="129389" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735125" />周六015</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[16]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/1361/">布伦特</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735125&r=1" target="_blank" class="clt1" >5</a><a href="./detail.php?fid=735125&r=1" target="_blank" class="fhuise" data-ao="半球" data-pb="半球/一球">半球/一球</a><a href="./detail.php?fid=735125&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/872/">赫尔城</a><span class="yellowcard">3</span><span class="gray">[12]</span></td>
    <td align="center" class="red">3 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735125.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735125.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735125.shtml">欧</a> <a target="_blank" id="qing_735125" class="red hide"   href="//odds.500.com/fenxi/youliao-735125.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735126" order="6016" status="4" gy="英冠,利兹联,博尔顿" yy="英冠,列斯聯,保頓" lid="62" fid="735126" sid="4843" class="bg02" infoid="129390" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735126" />周六016</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[03]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/1015/">利兹联</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735126&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=735126&r=1" target="_blank" class="fhuise" data-ao="球半/两球" data-pb="球半">球半</a><a href="./detail.php?fid=735126&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/704/">博尔顿</a><span class="yellowcard">4</span><span class="gray">[23]</span></td>
    <td align="center" class="red">1 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735126.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735126.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735126.shtml">欧</a> <a target="_blank" id="qing_735126" class="red hide"   href="//odds.500.com/fenxi/youliao-735126.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735127" order="6017" status="4" gy="英冠,米堡,女王巡游" yy="英冠,米杜士堡,昆士柏流浪" lid="62" fid="735127" sid="4843" class="" infoid="129391" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735127" />周六017</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[05]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1095/">米堡</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735127&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=735127&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球">半球</a><a href="./detail.php?fid=735127&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/954/">女王巡游</a><span class="yellowcard">1</span><span class="gray">[18]</span></td>
    <td align="center" class="red">2 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735127.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735127.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735127.shtml">欧</a> <a target="_blank" id="qing_735127" class="red hide"   href="//odds.500.com/fenxi/youliao-735127.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735128" order="6018" status="4" gy="英冠,米尔沃尔,普雷斯顿" yy="英冠,米禾爾,普雷斯頓" lid="62" fid="735128" sid="4843" class="bg02" infoid="129392" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735128" />周六018</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[19]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1097/">米尔沃尔</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735128&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=735128&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=735128&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1165/">普雷斯顿</a><span class="yellowcard">1</span><span class="gray">[11]</span></td>
    <td align="center" class="red">0 - 3</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735128.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735128.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735128.shtml">欧</a> <a target="_blank" id="qing_735128" class="red hide"   href="//odds.500.com/fenxi/youliao-735128.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735129" order="6019" status="4" gy="英冠,诺维奇,布城" yy="英冠,諾域治,布里斯托城" lid="62" fid="735129" sid="4843" class="" infoid="129393" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735129" />周六019</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[01]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/1144/">诺维奇</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735129&r=1" target="_blank" class="clt1" >3</a><a href="./detail.php?fid=735129&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球">半球</a><a href="./detail.php?fid=735129&r=1" target="_blank" class="clt3" >2</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/728/">布城</a><span class="yellowcard">3</span><span class="gray">[06]</span></td>
    <td align="center" class="red">1 - 2</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735129.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735129.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735129.shtml">欧</a> <a target="_blank" id="qing_735129" class="red hide"   href="//odds.500.com/fenxi/youliao-735129.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735131" order="6020" status="4" gy="英冠,雷丁,罗瑟汉姆" yy="英冠,雷丁,洛達咸" lid="62" fid="735131" sid="4843" class="bg02" infoid="129394" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735131" />周六020</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[21]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/989/">雷丁</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735131&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=735131&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=735131&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1037/">罗瑟汉姆</a><span class="yellowcard">3</span><span class="gray">[22]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735131.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735131.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735131.shtml">欧</a> <a target="_blank" id="qing_735131" class="red hide"   href="//odds.500.com/fenxi/youliao-735131.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735132" order="6021" status="4" gy="英冠,谢周三,斯旺西" yy="英冠,錫菲尔德星期三,史雲斯" lid="62" fid="735132" sid="4843" class="" infoid="129395" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735132" />周六021</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[15]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/1300/">谢周三</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735132&r=1" target="_blank" class="clt1" >3</a><a href="./detail.php?fid=735132&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手">平手</a><a href="./detail.php?fid=735132&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/511/">斯旺西</a><span class="gray">[13]</span></td>
    <td align="center" class="red">3 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735132.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735132.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735132.shtml">欧</a> <a target="_blank" id="qing_735132" class="red hide"   href="//odds.500.com/fenxi/youliao-735132.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735133" order="6022" status="4" gy="英冠,斯托克城,维拉" yy="英冠,史篤城,阿士東維拉" lid="62" fid="735133" sid="4843" class="bg02" infoid="129396" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735133" />周六022</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[17]</span><span class="yellowcard">3</span><a target="_blank" href="//liansai.500.com/team/1197/">斯托克城</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735133&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=735133&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=735133&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/555/">维拉</a><span class="yellowcard">1</span><span class="gray">[10]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735133.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735133.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735133.shtml">欧</a> <a target="_blank" id="qing_735133" class="red hide"   href="//odds.500.com/fenxi/youliao-735133.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735135" order="6023" status="4" gy="英冠,维冈,伊普斯" yy="英冠,韋根,葉士域治" lid="62" fid="735135" sid="4843" class="" infoid="129397" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735135" />周六023</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-23 23:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[20]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1258/">维冈</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735135&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=735135&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球/一球">半球/一球</a><a href="./detail.php?fid=735135&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1314/">伊普斯</a><span class="redcard">1</span><span class="yellowcard">2</span><span class="gray">[24]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735135.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735135.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735135.shtml">欧</a> <a target="_blank" id="qing_735135" class="red hide"   href="//odds.500.com/fenxi/youliao-735135.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a748863" order="6024" status="4" gy="西甲,塞维利亚,巴萨" yy="西甲,西維爾,巴塞隆拿" lid="93" fid="748863" sid="4913" class="bg02" infoid="129398" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="748863" />周六024</td>
    <td bgcolor="#006633" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4913/">西甲</a></td>
    <td align="center">第25轮</td>
    <td align="center">02-23 23:15</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[05]</span><span class="yellowcard">6</span><a target="_blank" href="//liansai.500.com/team/464/">塞维利亚</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=748863&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=748863&r=1" target="_blank" class="fhuise" data-ao="受半球" data-pb="受半球">受半球</a><a href="./detail.php?fid=748863&r=1" target="_blank" class="clt3" >4</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/653/">巴萨</a><span class="yellowcard">1</span><span class="gray">[01]</span></td>
    <td align="center" class="red">2 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 <a href="http://live.500.com/tv/748863/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-748863.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-748863.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-748863.shtml">欧</a> <a target="_blank" id="qing_748863" class="red hide"   href="//odds.500.com/fenxi/youliao-748863.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a746328" order="6025" status="4" gy="葡超,费伦斯,摩雷伦斯" yy="葡超,費倫斯,摩里倫斯" lid="71" fid="746328" sid="4890" class="" infoid="129399" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="746328" />周六025</td>
    <td bgcolor="#008888" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4890/">葡超</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-23 23:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[18]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/2923/">费伦斯</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=746328&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=746328&r=1" target="_blank" class="fhuise" data-ao="受平手/半球" data-pb="受平手/半球">受平手/半球</a><a href="./detail.php?fid=746328&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1110/">摩雷伦斯</a><span class="gray">[05]</span></td>
    <td align="center" class="red">0 - 2</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-746328.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-746328.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-746328.shtml">欧</a> <a target="_blank" id="qing_746328" class="red hide"   href="//odds.500.com/fenxi/youliao-746328.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a729458" order="6026" status="4" gy="法甲,巴黎圣曼,尼姆" yy="法甲,巴黎聖日門,尼姆" lid="107" fid="729458" sid="4820" class="bg02" infoid="129400" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="729458" />周六026</td>
    <td bgcolor="#663333" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4820/">法甲</a></td>
    <td align="center">第26轮</td>
    <td align="center">02-24 00:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[01]</span><span class="yellowcard">3</span><a target="_blank" href="//liansai.500.com/team/647/">巴黎圣曼</a><span class="sp_rq">(-2)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=729458&r=1" target="_blank" class="clt1" >3</a><a href="./detail.php?fid=729458&r=1" target="_blank" class="fhuise" data-ao="两球" data-pb="两球">两球</a><a href="./detail.php?fid=729458&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1132/">尼姆</a><span class="gray">[10]</span></td>
    <td align="center" class="red">1 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 <a href="http://live.500.com/tv/729458/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-729458.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-729458.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-729458.shtml">欧</a> <a target="_blank" id="qing_729458" class="red hide"   href="//odds.500.com/fenxi/youliao-729458.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a731172" order="6027" status="4" gy="英超,莱切斯特,水晶宫" yy="英超,李斯特城,水晶宮" lid="106" fid="731172" sid="4826" class="" infoid="129401" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="731172" />周六027</td>
    <td bgcolor="#FF1717" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4826/">英超</a></td>
    <td align="center">第27轮</td>
    <td align="center">02-24 01:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[12]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/973/">莱切斯特</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=731172&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=731172&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=731172&r=1" target="_blank" class="clt3" >4</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/516/">水晶宫</a><span class="yellowcard">1</span><span class="gray">[14]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-731172.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-731172.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-731172.shtml">欧</a> <a target="_blank" id="qing_731172" class="red hide"   href="//odds.500.com/fenxi/youliao-731172.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a735134" order="6028" status="4" gy="英冠,西布罗姆,谢菲联" yy="英冠,西布朗,錫菲聯" lid="62" fid="735134" sid="4843" class="bg02" infoid="129402" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="735134" />周六028</td>
    <td bgcolor="#CC3300" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4843/">英冠</a></td>
    <td align="center">第34轮</td>
    <td align="center">02-24 01:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[04]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/1284/">西布罗姆</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=735134&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=735134&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=735134&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1299/">谢菲联</a><span class="yellowcard">3</span><span class="gray">[02]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-735134.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-735134.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-735134.shtml">欧</a> <a target="_blank" id="qing_735134" class="red hide"   href="//odds.500.com/fenxi/youliao-735134.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a737752" order="6029" status="4" gy="德甲,杜塞多夫,纽伦堡" yy="德甲,杜塞爾多夫,紐倫堡" lid="58" fid="737752" sid="4852" class="" infoid="129403" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="737752" />周六029</td>
    <td bgcolor="#990099" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4852/">德甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 01:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[13]</span><span class="yellowcard">3</span><a target="_blank" href="//liansai.500.com/team/781/">杜塞多夫</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=737752&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=737752&r=1" target="_blank" class="fhuise" data-ao="半球/一球" data-pb="半球">半球</a><a href="./detail.php?fid=737752&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1138/">纽伦堡</a><span class="redcard">1</span><span class="yellowcard">4</span><span class="gray">[18]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 <a href="http://live.500.com/tv/737752/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-737752.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-737752.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-737752.shtml">欧</a> <a target="_blank" id="qing_737752" class="red hide"   href="//odds.500.com/fenxi/youliao-737752.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a748855" order="6030" status="4" gy="西甲,阿拉维斯,塞尔塔" yy="西甲,艾拉維斯,切爾達" lid="93" fid="748855" sid="4913" class="bg02" infoid="129404" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="748855" />周六030</td>
    <td bgcolor="#006633" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4913/">西甲</a></td>
    <td align="center">第25轮</td>
    <td align="center">02-24 01:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[06]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/542/">阿拉维斯</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=748855&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=748855&r=1" target="_blank" class="fhuise" data-ao="平手/半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=748855&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/457/">塞尔塔</a><span class="yellowcard">2</span><span class="gray">[17]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 <a href="http://live.500.com/tv/748855/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-748855.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-748855.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-748855.shtml">欧</a> <a target="_blank" id="qing_748855" class="red hide"   href="//odds.500.com/fenxi/youliao-748855.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a746330" order="6031" status="4" gy="葡超,波尔蒂芒,阿维斯" yy="葡超,保迪蒙尼斯,艾維斯" lid="71" fid="746330" sid="4890" class="" infoid="129405" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="746330" />周六031</td>
    <td bgcolor="#008888" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4890/">葡超</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 02:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[10]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/2397/">波尔蒂芒</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=746330&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=746330&r=1" target="_blank" class="fhuise" data-ao="半球" data-pb="平手/半球">平手/半球</a><a href="./detail.php?fid=746330&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/223/">阿维斯</a><span class="yellowcard">3</span><span class="gray">[16]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-746330.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-746330.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-746330.shtml">欧</a> <a target="_blank" id="qing_746330" class="red hide"   href="//odds.500.com/fenxi/youliao-746330.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a731487" order="6032" status="4" gy="荷甲,福图纳,海伦芬" yy="荷甲,幸运薛达,海倫維恩" lid="91" fid="731487" sid="4827" class="bg02" infoid="129406" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="731487" />周六032</td>
    <td bgcolor="#ff6699" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4827/">荷甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 02:45</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[11]</span><span class="yellowcard">4</span><span class="redcard">1</span><a target="_blank" href="//liansai.500.com/team/1303/">福图纳</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=731487&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=731487&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="受平手/半球">受平手/半球</a><a href="./detail.php?fid=731487&r=1" target="_blank" class="clt3" >4</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/857/">海伦芬</a><span class="yellowcard">1</span><span class="gray">[15]</span></td>
    <td align="center" class="red">2 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-731487.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-731487.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-731487.shtml">欧</a> <a target="_blank" id="qing_731487" class="red hide"   href="//odds.500.com/fenxi/youliao-731487.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a731486" order="6033" status="4" gy="荷甲,兹沃勒,格拉夫" yy="荷甲,施禾尼,迪加史卓普" lid="91" fid="731486" sid="4827" class="" infoid="129407" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="731486" />周六033</td>
    <td bgcolor="#ff6699" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4827/">荷甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 02:45</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[13]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/1353/">兹沃勒</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=731486&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=731486&r=1" target="_blank" class="fhuise" data-ao="一球" data-pb="一球">一球</a><a href="./detail.php?fid=731486&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/782/">格拉夫</a><span class="redcard">1</span><span class="yellowcard">1</span><span class="gray">[17]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-731486.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-731486.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-731486.shtml">欧</a> <a target="_blank" id="qing_731486" class="red hide"   href="//odds.500.com/fenxi/youliao-731486.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a729455" order="6034" status="4" gy="法甲,甘冈,昂热" yy="法甲,吉英坎,昂热" lid="107" fid="729455" sid="4820" class="bg02" infoid="129408" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="729455" />周六034</td>
    <td bgcolor="#663333" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4820/">法甲</a></td>
    <td align="center">第26轮</td>
    <td align="center">02-24 03:00</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[20]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/813/">甘冈</a><span class="sp_rq">(-1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=729455&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=729455&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="平手">平手</a><a href="./detail.php?fid=729455&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/597/">昂热</a><span class="yellowcard">2</span><span class="gray">[12]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">胜 <a href="http://live.500.com/tv/729455/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-729455.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-729455.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-729455.shtml">欧</a> <a target="_blank" id="qing_729455" class="red hide"   href="//odds.500.com/fenxi/youliao-729455.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a750035" order="6035" status="4" gy="意甲,弗洛西诺,罗马" yy="意甲,費辛隆尼,羅馬" lid="92" fid="750035" sid="4919" class="" infoid="129409" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="750035" />周六035</td>
    <td bgcolor="#0066FF" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4919/">意甲</a></td>
    <td align="center">第25轮</td>
    <td align="center">02-24 03:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[19]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/2000/">弗洛西诺</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=750035&r=1" target="_blank" class="clt1" >2</a><a href="./detail.php?fid=750035&r=1" target="_blank" class="fhuise" data-ao="受一球/球半" data-pb="受一球/球半">受一球/球半</a><a href="./detail.php?fid=750035&r=1" target="_blank" class="clt3" >3</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/1032/">罗马</a><span class="yellowcard">2</span><span class="gray">[05]</span></td>
    <td align="center" class="red">1 - 2</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">负 <a href="http://live.500.com/tv/750035/3/" class="live_video" title="视频" target="_blank"></a></td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-750035.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-750035.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-750035.shtml">欧</a> <a target="_blank" id="qing_750035" class="red hide"   href="//odds.500.com/fenxi/youliao-750035.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a731488" order="6036" status="4" gy="荷甲,布雷达,格罗宁根" yy="荷甲,比達,高寧根" lid="91" fid="731488" sid="4827" class="bg02" infoid="129410" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="731488" />周六036</td>
    <td bgcolor="#ff6699" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4827/">荷甲</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 03:45</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[18]</span><span class="yellowcard">1</span><a target="_blank" href="//liansai.500.com/team/350/">布雷达</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=731488&r=1" target="_blank" class="clt1" >0</a><a href="./detail.php?fid=731488&r=1" target="_blank" class="fhuise" data-ao="受平手/半球" data-pb="受平手/半球">受平手/半球</a><a href="./detail.php?fid=731488&r=1" target="_blank" class="clt3" >0</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/834/">格罗宁根</a><span class="yellowcard">1</span><span class="gray">[09]</span></td>
    <td align="center" class="red">0 - 0</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-731488.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-731488.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-731488.shtml">欧</a> <a target="_blank" id="qing_731488" class="red hide"   href="//odds.500.com/fenxi/youliao-731488.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
  	  	
  <tr id="a746331" order="6037" status="4" gy="葡超,塞图巴尔,吉马良斯" yy="葡超,塞圖巴爾,甘馬雷斯" lid="71" fid="746331" sid="4890" class="" infoid="129411" r="1">
    <td align="center" class=""><input type="checkbox" name="check_id[]" value="746331" />周六037</td>
    <td bgcolor="#008888" class="ssbox_01"><a style="color:#fff" target="_blank" href="//liansai.500.com/zuqiu-4890/">葡超</a></td>
    <td align="center">第23轮</td>
    <td align="center">02-24 04:30</td>
    <td align="center"><span class="red">完</span></td>
    <td align="right" class="p_lr01"><span class="gray">[15]</span><span class="yellowcard">2</span><a target="_blank" href="//liansai.500.com/team/463/">塞图巴尔</a><span class="sp_sr">(+1)</span></td>
    <td align="center"><div class="pk"><a href="./detail.php?fid=746331&r=1" target="_blank" class="clt1" >1</a><a href="./detail.php?fid=746331&r=1" target="_blank" class="fhuise" data-ao="平手" data-pb="受平手/半球">受平手/半球</a><a href="./detail.php?fid=746331&r=1" target="_blank" class="clt3" >1</a></div></td>
    <td align="left" class="p_lr01"><a target="_blank" href="//liansai.500.com/team/893/">吉马良斯</a><span class="redcard">1</span><span class="yellowcard">4</span><span class="gray">[06]</span></td>
    <td align="center" class="red">0 - 1</td>
    <td align="center" class="bf_op">&nbsp;</td>
    <td align="center" class="red">平 </td>
    <td align="center" class="td_warn"><a target="_blank" href="//odds.500.com/fenxi/shuju-746331.shtml">析</a> <a target="_blank" href="//odds.500.com/fenxi/yazhi-746331.shtml">亚</a> <a target="_blank" href="//odds.500.com/fenxi/ouzhi-746331.shtml">欧</a> <a target="_blank" id="qing_746331" class="red hide"   href="//odds.500.com/fenxi/youliao-746331.shtml?channel=pc_score">情</a></td>
    <td align="center" class=""><a href="javascript:void(0)" class="icon_notop">置顶</a></td>
  </tr>
    
  </tbody>
</table>
  <div class="bf_sm01">500.com即时比分提示：点击球队名：查看球队战绩，点击比分：查看比赛事件数据，(中)表示中立场，<img align="absmiddle" src="https://live.500.com/images/shuju_row_01.gif">表示天气，<img align="absmiddle" src="https://www.500cache.com/live/images/live_video.gif">表示视频直播  <img align="absmiddle" src="https://www.500cache.com/live/images/live_animate.png">表示虚拟动画。<br />
  网站提醒：以上比分数据仅供浏览、投注参考之用，并不作为最终派奖赛果依据。
  <p class="gray">为保证您最佳的浏览效果，请使用IE9或以上版本, Chrome等浏览器进行访问</p>
  </div>
 
<!--百度联盟广告start-->
<div class="section clearfix" style="text-align: center;margin-top: 5px;">
	<div class="" id="pc_ad_hf"></div>
</div>
<div style="position:fixed;bottom:0;right:0;z-index:1000; background-color:#ffffff; border:6px solid #fff;box-shadow: 0 0px 5px rgba(0,0,0,.1);-webkit-box-shadow: 0 0px 5px rgba(0,0,0,.1); cursor:pointer;">
	<div class="" id="pc_ad_cc"></div>
</div>
<!--百度联盟广告end-->  
 </div>
</div>
<script type="text/javascript">
// 服务器时间与客户端时间差
var time_offset = 1609904427 - ~~((new Date).getTime() / 1000);
var d = new Date();
d.setTime(d.getTime()+time_offset*1000);
if (d.getHours()<12) {
	d.setDate(d.getDate()-1);
}
function date_format(D){
	var y = D.getFullYear(),
		m = D.getMonth() + 1,
		d = D.getDate();
	return y + '-' + (m<10?'0':'') + m + '-' + (d<10?'0':'') + d;
}
window.live_json_path = 'jczq/20190223';
</script>
<script type="text/javascript">
var liveOddsList={"746328":{"0":[3.7,3.17,2.06],"5":[3.42,3.18,2.01],"rqsp":[1.60,3.45,4.10],"sp":[3.45,2.90,1.91],"280":[3.35,3.3,2.11],"293":[3.75,3.2,2.1],"1055":[3.79,3.44,2.12]},"735124":{"0":[2.14,3.14,3.57],"3":[2.25,3.2,3.75],"5":[2.05,3.05,3.45],"rqsp":[3.90,3.45,1.63],"sp":[1.89,3.02,3.35],"280":[2.23,3.15,3.5],"293":[2.2,3.2,3.5],"1055":[2.29,3.14,3.7]},"735125":{"0":[1.75,3.82,4.29],"3":[1.8,4.0,4.6],"5":[1.7,3.7,4.05],"rqsp":[2.80,3.45,1.95],"sp":[1.60,3.60,3.90],"280":[1.74,4.05,4.4],"293":[1.75,3.9,4.5],"1055":[1.76,4.07,4.64]},"735126":{"0":[1.27,5.21,11.58],"3":[1.28,5.5,15.0],"5":[1.22,5.8,9.0],"rqsp":[1.68,3.50,3.60],"sp":[1.15,5.15,10.50],"280":[1.3,5.4,10.0],"293":[1.29,5.25,12.0],"1055":[1.3,5.45,12.44]},"735127":{"0":[1.79,3.34,4.86],"3":[1.83,3.4,5.5],"5":[1.75,3.23,4.35],"rqsp":[2.97,3.25,1.94],"sp":[1.60,3.25,4.41],"280":[1.86,3.3,4.7],"293":[1.8,3.4,5.0],"1055":[1.85,3.36,5.24]},"735128":{"0":[2.6,2.98,2.9],"3":[2.62,3.0,3.2],"5":[2.4,3.0,2.8],"rqsp":[5.40,4.00,1.38],"sp":[2.38,2.84,2.58],"280":[2.47,2.96,3.25],"293":[2.5,3.0,3.2],"1055":[2.55,3.05,3.28]},"735129":{"0":[1.82,3.61,4.18],"3":[1.85,3.75,4.5],"5":[1.8,3.4,3.9],"rqsp":[3.36,3.40,1.76],"sp":[1.72,3.25,3.70],"280":[1.84,3.7,4.25],"293":[1.85,3.7,4.2],"1055":[1.87,3.7,4.51]},"735131":{"0":[2.15,3.25,3.4],"3":[2.2,3.4,3.6],"5":[2.05,3.13,3.33],"rqsp":[3.90,3.45,1.63],"sp":[1.87,3.08,3.33],"280":[2.21,3.3,3.35],"293":[2.2,3.25,3.5],"1055":[2.28,3.28,3.56]},"735132":{"0":[2.65,3.19,2.67],"3":[2.8,3.3,2.75],"5":[2.5,2.8,2.6],"rqsp":[5.55,4.10,1.36],"sp":[2.44,2.94,2.44],"280":[2.71,3.2,2.68],"293":[2.7,3.2,2.75],"1055":[2.7,3.33,2.82]},"735133":{"0":[2.16,3.25,3.4],"3":[2.2,3.4,3.6],"5":[2.08,3.28,3.1],"rqsp":[4.10,3.65,1.56],"sp":[1.99,3.05,3.05],"280":[2.19,3.2,3.55],"293":[2.15,3.3,3.5],"1055":[2.25,3.32,3.58]},"735134":{"0":[2.4,3.3,2.88],"3":[2.45,3.5,3.0],"5":[2.35,3.2,2.7],"rqsp":[5.00,4.10,1.40],"sp":[2.30,3.05,2.52],"280":[2.33,3.4,3.05],"293":[2.4,3.3,3.0],"1055":[2.4,3.43,3.17]},"735135":{"0":[1.72,3.41,5.26],"3":[1.72,3.6,6.0],"5":[1.68,3.3,4.85],"rqsp":[2.77,3.15,2.08],"sp":[1.50,3.30,5.26],"280":[1.73,3.45,5.6],"293":[1.75,3.5,5.25],"1055":[1.75,3.64,5.5]},"731172":{"0":[2.23,3.27,3.41],"3":[2.3,3.4,3.4],"5":[2.1,3.25,3.1],"rqsp":[4.40,3.60,1.53],"sp":[2.02,3.05,2.98],"280":[2.25,3.25,3.45],"293":[2.2,3.3,3.4],"1055":[2.27,3.41,3.5]},"738214":{"0":[2.4,3.41,2.74],"3":[2.37,3.4,2.8],"5":[2.35,3.25,2.68],"rqsp":[4.70,4.15,1.42],"sp":[2.25,3.25,2.46],"280":[2.49,3.5,2.74],"293":[2.38,3.4,2.8],"1055":[2.44,3.6,2.91]},"738215":{"0":[2.23,3.23,3.16],"3":[2.25,3.3,3.1],"5":[2.15,3.15,3.1],"rqsp":[4.45,3.75,1.50],"sp":[2.07,3.05,2.87],"280":[2.21,3.25,3.35],"293":[2.25,3.25,3.1],"1055":[2.22,3.42,3.45]},"738216":{"0":[1.4,4.4,7.46],"3":[1.44,4.5,7.5],"5":[1.37,4.35,6.9],"rqsp":[1.98,3.35,2.81],"sp":[1.26,4.50,6.95],"280":[1.43,4.45,7.8],"293":[1.4,4.33,8.0],"1055":[1.42,4.53,8.49]},"738220":{"0":[2.43,3.14,2.88],"3":[2.37,3.2,3.0],"5":[2.35,3.05,2.8],"rqsp":[5.00,3.85,1.43],"sp":[2.24,3.05,2.60],"280":[2.51,3.25,2.91],"293":[2.45,3.1,3.0],"1055":[2.56,3.22,3.03]},"779378":{"0":[3.49,3.43,1.98],"3":[3.6,3.5,2.0],"5":[3.2,3.45,1.98],"rqsp":[1.70,3.50,3.50],"sp":[3.22,3.45,1.79],"280":[3.7,3.65,2.02],"293":[3.7,3.5,2.0],"1055":[3.81,3.6,2.03]},"748855":{"0":[2.48,3.04,3.12],"3":[2.5,3.0,3.2],"5":[2.23,3.15,2.93],"rqsp":[5.38,3.85,1.40],"sp":[2.25,2.92,2.69],"280":[2.49,3.0,3.25],"293":[2.45,3.0,3.2],"1055":[2.49,3.1,3.32]},"731167":{"0":[2.96,3.24,2.49],"3":[3.1,3.4,2.45],"5":[2.88,3.2,2.25],"rqsp":[1.43,3.90,4.90],"sp":[2.58,3.10,2.23],"280":[3.15,3.2,2.4],"293":[3.1,3.25,2.38],"1055":[3.22,3.28,2.46]},"748863":{"0":[3.83,4.04,1.85],"3":[3.8,4.0,1.83],"5":[3.6,3.9,1.75],"rqsp":[1.94,3.65,2.70],"sp":[3.80,3.80,1.58],"280":[3.95,4.1,1.84],"293":[4.0,4.0,1.8],"1055":[4.03,4.27,1.83]},"750035":{"0":[7.35,4.58,1.43],"3":[7.5,4.75,1.4],"5":[6.0,4.65,1.38],"rqsp":[2.67,3.40,2.04],"sp":[6.25,4.35,1.30],"280":[8.0,4.7,1.42],"293":[8.5,4.6,1.4],"1055":[8.51,4.77,1.42]},"737749":{"0":[1.97,3.51,3.86],"3":[2.0,3.5,3.8],"5":[1.98,3.2,3.46],"rqsp":[3.22,3.50,1.78],"sp":[1.73,3.30,3.60],"280":[2.06,3.5,3.75],"293":[2.05,3.5,3.7],"1055":[2.05,3.57,3.86]},"737752":{"0":[1.82,3.59,4.4],"3":[1.8,3.6,4.5],"5":[1.73,3.48,4.15],"rqsp":[3.10,3.45,1.84],"sp":[1.68,3.30,3.85],"280":[1.9,3.6,4.2],"293":[1.85,3.6,4.33],"1055":[1.93,3.55,4.42]},"737753":{"0":[2.34,3.28,3.12],"3":[2.25,3.4,3.2],"5":[2.22,3.1,3.0],"rqsp":[4.50,3.90,1.47],"sp":[2.15,3.10,2.70],"280":[2.47,3.3,2.99],"293":[2.38,3.3,3.1],"1055":[2.48,3.31,3.13]},"746330":{"0":[2.09,3.29,3.46],"3":[2.0,3.3,3.8],"5":[2.0,3.25,3.35],"rqsp":[3.75,3.50,1.65],"sp":[1.88,3.10,3.30],"280":[2.17,3.3,3.15],"293":[2.15,3.25,3.5],"1055":[2.19,3.34,3.7]},"746331":{"0":[3.19,2.89,2.43],"3":[3.1,3.0,2.45],"5":[3.2,2.85,2.25],"rqsp":[1.50,3.50,4.85],"sp":[3.05,2.82,2.10],"280":[3.2,2.85,2.4],"293":[3.3,2.9,2.4],"1055":[3.49,3.01,2.46]},"731486":{"0":[1.59,4.07,5.17],"3":[1.6,4.2,5.0],"5":[1.5,4.28,5.0],"rqsp":[2.30,3.50,2.28],"sp":[1.41,4.00,5.00],"280":[1.63,4.1,5.1],"293":[1.57,4.2,5.25],"1055":[1.65,3.97,5.56]},"731487":{"0":[2.76,3.68,2.3],"3":[2.87,3.4,2.4],"5":[2.6,3.62,2.25],"rqsp":[1.44,4.20,4.45],"sp":[2.40,3.45,2.22],"280":[2.75,3.8,2.36],"293":[2.75,3.7,2.3],"1055":[2.84,3.76,2.38]},"731488":{"0":[3.35,3.38,2.1],"3":[3.3,3.5,2.05],"5":[3.3,3.3,2.0],"rqsp":[1.63,3.60,3.75],"sp":[3.20,3.20,1.87],"280":[3.3,3.4,2.21],"293":[3.3,3.3,2.15],"1055":[3.43,3.43,2.23]},"765034":{"0":[2.13,3.37,3.29],"3":[2.2,3.4,3.25],"5":[2.14,3.2,3.08],"rqsp":[4.15,3.80,1.53],"sp":[2.03,3.20,2.82],"280":[2.31,3.4,3.2],"293":[2.2,3.3,3.1],"1055":[2.33,3.48,3.25]},"729455":{"0":[2.58,2.99,3.0],"3":[2.5,3.2,3.0],"5":[2.35,3.03,2.85],"rqsp":[5.90,3.85,1.37],"sp":[2.39,2.70,2.70],"280":[2.68,2.88,3.0],"293":[2.55,3.1,2.9],"1055":[2.69,3.06,3.07]},"729458":{"0":[1.19,7.15,13.13],"3":[1.2,7.0,13.0],"5":[1.14,6.9,12.0],"rqsp":[2.18,3.90,2.25],"sp":[1.09,6.20,12.50],"280":[1.2,7.4,12.5],"293":[1.18,7.0,15.0],"1055":[1.2,7.55,13.83]},"779380":{"0":[1.78,3.44,4.38],"3":[1.85,3.5,4.2],"5":[1.88,3.15,3.9],"rqsp":[3.15,3.40,1.83],"sp":[1.66,3.35,3.90],"280":[1.95,3.5,4.1],"293":[1.88,3.4,4.2],"1055":[1.94,3.41,4.42]},"779384":{"0":[2.4,3.27,2.79],"3":[2.5,3.3,2.8],"5":[2.35,3.15,2.75],"rqsp":[5.30,3.90,1.40],"sp":[2.32,3.10,2.47],"280":[2.54,3.4,2.8],"293":[2.45,3.4,2.8],"1055":[2.55,3.51,2.83]},"779386":{"0":[1.68,3.6,4.83],"3":[1.75,3.75,4.5],"5":[1.65,3.7,4.35],"rqsp":[2.85,3.40,1.95],"sp":[1.57,3.60,4.10],"280":[1.77,3.65,4.7],"293":[1.73,3.5,5.0],"1055":[1.75,3.56,5.47]},"779390":{"0":[2.59,3.43,2.47],"3":[2.5,3.4,2.7],"5":[2.65,3.15,2.45],"rqsp":[5.00,4.20,1.39],"sp":[2.35,3.40,2.28],"280":[2.8,3.6,2.45],"293":[2.7,3.5,2.45],"1055":[2.69,3.67,2.59]}};
</script>
		<script type="text/javascript" src="https://www.500cache.com/live/js/socket.io-1.3.4.js?v=20150812"></script>
		<script type="text/javascript" src="https://www.500cache.com/live/js/common_ws.js?v=20200525001"></script><script type="text/javascript">
$(function(){
	var e = $('#sel_expect').val();
	var a = [], d = new Date();
	for (; a.length <= 7;) {
		a.push(date_format(d));
		d.setDate(d.getDate()-1);
	}
	if (e && in_array(e, a)==-1) {
		a.push(e);
	}
	a.sort().reverse();
	var ops = [];
	for (var i=0; i<a.length; i++) {
		ops.push('<option value="'+a[i]+'"'+(a[i]==e?' selected="selected"':'')+(i?'':' style="color:red"')+'>'+a[i]+'</option>');
	}
	$('#sel_expect').html(ops.join('')).change(expect_change);
});
</script>
<div id="ft"><link rel="stylesheet" href="//www.500cache.com/public/css/footer.css?v=20181019"> 
<!--百度联盟广告start-->
<div class="section clearfix" style="text-align:center;margin-top: 5px;margin-bottom: 5px;">
	<div class="" id="pc_ad_hf"></div>
</div>
<div style="position:fixed;bottom:0;right:0;z-index:1000; background-color:#ffffff; border:6px solid #fff;box-shadow: 0 0px 5px rgba(0,0,0,.1);-webkit-box-shadow: 0 0px 5px rgba(0,0,0,.1); cursor:pointer;">
	<div class="" id="pc_ad_cc"></div>
</div>
<!--百度联盟广告end-->
<div class="footer">
	<div class="f-link"> <a title="关于我们" target="_blank" href="//www.500.com/about/" rel="nofollow">关于我们</a> | <a title="投资者关系" target="_blank" href="http://ir.500.com/" rel="nofollow">Investor Relations</a> | <a title="用户注册" target="_blank" href="//passport.500.com/user/" rel="nofollow">用户注册</a> | <a title="加盟合作" target="_blank" href="//www.500.com/about/joinus.shtml" rel="nofollow">加盟合作</a> | <a title="网站地图" target="_blank" href="//www.500.com/about/sitemap.shtml">网站地图</a> | <a title="友情链接" target="_blank" href="//www.500.com/link.shtml">友情链接</a> | <a title="500.com招聘" target="_blank" href="https://job.500.com/" rel="nofollow">500.com招聘</a> </div>
	<div class="copy_new">
		<p><a href="//www.500.com/about/xuke.shtml" target="_blank" rel="nofollow">增值电信业务经营许可证：粤B2-20070298</a>&#160;&#160;&#160;<a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow">粤ICP备11007122号</a>&#160;&#160;&#160;<a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=44030702000009"><img src="//www.500cache.com/news/images/dxt/ghs.png" width="20" height="20">粤公网安备 44030702000009号</a></p>
		<p>
        	&#169;2001-2020
        	500彩票 版权所有&#160;&#160;股票代码：<span class="red">WBAI</span>&#160;&#160;客服热线：4000-500-500
        </p>
		
		<p class="security">
			<a href="https://seal.qualys.com/sealserv/info/?i=8daaed52-427d-474e-bc07-9c83a8a53188" title="qualys secure" target="_blank" class="security07" rel="nofollow"></a><a target="_blank" href="https://www.500.com/about/wangan/index.htm" title="公共信息网络安全监察" class="security04" rel="nofollow">公共信息网<br />络安全监察</a><a title="网上交易保障中心" href="http://www.315online.com.cn/member/315120077.html" target="_blank" class="security03" rel="nofollow">网上交易<br />保障中心</a><a title="工商网监电子标识" href="https://szcert.ebs.org.cn/ec1c33b3-f78d-483e-988c-f41abb93058a" target="_blank" class="security09" rel="nofollow">工商网监<br>电子标识</a><a title="中国信用企业" href="http://shuidi.cn/shuidi/company-license-aaa?digest=a9978bd9bd441ba35753a48614abfa51" target="_blank" class="security05" rel="nofollow"></a><a  key ="5577ecb1efbfb03ac5bfa753"  logo_size="124x47"  logo_type="business"  href="https://v.yunaq.com/certificate?domain=www.500.com&from=label&code=90030" title="安全联盟标识" target="_blank" class="security10" rel="nofollow"></a><a title="可信网站身份验证" href="https://www.500.com/about/knet.html" target="_blank" class="security08" rel="nofollow"></a><a id='___szfw_logo___' href='https://search.szfw.org/cert/l/CX20150210006686006756' target='_blank' class="szfw_logo"></a><script type='text/javascript'>(function(){document.getElementById('___szfw_logo___').oncontextmenu = function(){return false;}})();</script><a title="广东省文化厅备案资质" href="http://sq.ccm.gov.cn/ccnt/sczr/service/business/emark/toDetail/9EF18B0460C04F1385E18D9E23013B4D" target="_blank" class="security12" rel="nofollow">广东省文化厅<br>备案资质</a><a target="_blank" href="http://gdga.gd.gov.cn/" title="广东网络警察举报平台" class="security01" rel="nofollow">广东<br />网警</a><a title="深圳网络警察举报平台" href="http://ga.sz.gov.cn/" target="_blank" class="security06 last" rel="nofollow">深圳<br />网警</a>
			</p>
	</div>
</div>
<div class="footer-keywords">
        <div class="footer-keywords-wrap">
          <ul class="footer-keywords-list" id="footer-keywords-list">
            <li><span>热点导读：</span><a href="//zx.500.com/zc/" title="足彩" target="_blank">足彩</a><a href="//zx.500.com/szpl/" title="数字排列" target="_blank">数字排列</a><a href="//trade.500.com/dlt/" title="体彩大乐透" target="_blank">体彩大乐透</a><a href="//trade.500.com/pls/" title="排列3" target="_blank">排列3</a><a href="//trade.500.com/plw/" title="排列5" target="_blank">排列5</a><a href="//trade.500.com/sfc/" title="胜负彩" target="_blank">胜负彩</a><a href="//trade.500.com/jczq/?playid=269&g=2" title="竞彩" target="_blank">竞彩</a><a href="//trade.500.com/jclq/?playid=275&g=2" title="篮彩" target="_blank">篮彩</a><a href="//zx.500.com/sd/" title="福彩3d" target="_blank">福彩3d</a><a href="//zx.500.com/dlt/" title="大乐透" target="_blank">大乐透</a><a href="//zx.500.com/zqdc/" title="北京单场" target="_blank">北京单场</a><a href="//zx.500.com/jczq/" title="竞彩足球" target="_blank">竞彩足球</a><a href="//zx.500.com/" title="彩票预测" target="_blank">彩票预测</a><a href="//zx.500.com/jclq/" title="竞彩篮球" target="_blank">竞彩篮球</a><a href="//zx.500.com/ssq/" title="双色球" target="_blank">双色球</a></li>
            <li><span>彩种信息：</span><a href="//datachart.500.com/pls/" title="排列3走势图" target="_blank">排列3走势图</a><a href="//datachart.500.com/plw/" title="排列5走势图" target="_blank">排列5走势图</a><a href="//kaijiang.500.com/sd.shtml" title="3d开奖结果" target="_blank">3d开奖结果</a><a href="//kaijiang.500.com/dlt.shtml" title="大乐透开奖结果" target="_blank" >大乐透开奖结果</a><a href="//datachart.500.com/dlt/" title="大乐透走势图" target="_blank">大乐透走势图</a><a href="//datachart.500.com/qxc/" title="七星彩走势图" target="_blank">七星彩走势图</a><a href="//kaijiang.500.com/qxc.shtml" title="七星彩开奖结果" target="_blank">七星彩开奖结果</a><a href="//datachart.500.com/sd/" title="3d走势图" target="_blank" >3d走势图</a><a href="//kaijiang.500.com/pls.shtml" title="排列3开奖结果" target="_blank">排列3开奖结果</a><a href="//datachart.500.com/ssq/" title="双色球走势图" target="_blank">双色球走势图</a><a href="//kaijiang.500.com/plw.shtml" title="排列5开奖结果" target="_blank">排列5开奖结果</a><a href="//kaijiang.500.com/ssq.shtml" title="双色球开奖结果" target="_blank">双色球开奖结果</a></li>
            <li><span>赛事比分：</span><a href="//trade.500.com/jqc/" title="四场进球" target="_blank">四场进球</a><a href="//live.500.com/jczq.php" title="竞彩足球比分直播" target="_blank">竞彩足球比分直播</a><a href="//live.500.com/lq.php" title="竞彩篮球比分直播" target="_blank">竞彩篮球比分直播</a><a href="//liansai.500.com/" title="联赛资料" target="_blank">联赛资料</a><a href="//trade.500.com/jczq/?playid=272&g=2" title="竞彩足球半全场" target="_blank">竞彩足球半全场</a><a href="//trade.500.com/rj/" title="任选九场" target="_blank">任选九场</a><a href="//trade.500.com/jclq/index.php?playid=313&g=2" title="竞彩篮球混合过关" target="_blank">竞彩篮球混合过关</a><a href="//trade.500.com/jclq/index.php?playid=275" title="竞彩篮球让分胜负" target="_blank">竞彩篮球让分胜负</a><a href="//trade.500.com/bqc/" title="六场半全场" target="_blank">六场半全场</a><a href="//odds.500.com/" title="盘口" target="_blank" >盘口</a><a href="//trade.500.com/jczq/?playid=312&g=2" title="竞彩足球混合过关" target="_blank">竞彩足球混合过关</a><a href="//liansai.500.com/lq/" title="篮球比赛" target="_blank">篮球比赛</a></li>
          </ul>
          <a href="javascript:;" data-fold="1" class="btn-keywords"  id="footer-btn-keywords">+ 更多</a>
      </div>
</div>
<script>
(function(){
	var elemKeywords = document.getElementById('footer-btn-keywords');
	var elemKeywordsList = document.getElementById('footer-keywords-list');
	elemKeywords.onclick = function(){
		if (this.getAttribute("data-fold") == 1){
			this.innerHTML = "- 收起"
			this.setAttribute("data-fold", 0);
			elemKeywordsList.style.height = "60px";
			return;
		}
		this.innerHTML = "+ 更多"
		this.setAttribute("data-fold", 1);
		elemKeywordsList.style.height = "20px";
	};
}());

(function(){
	//显示百度联盟广告
function showBaiduAd(){
	//
	var adidjson = getBaiduAdId();
		if(adidjson === false){
			return false;
		}
		if(location.hostname == 'zx.500.com' && location.pathname.indexOf('/gongju/') > -1){
			return false;
		}
		var pathlen = location.pathname.length;
		var hf_id,hf_container,cc_id,cc_container;
		if(pathlen == 1){//首页
			hf_id = adidjson["index"]["hfAd"] !== undefined ? adidjson["index"]["hfAd"]["id"] : '' ;
			hf_container = adidjson["index"]["hfAd"] !== undefined ? adidjson["index"]["hfAd"]["container"] : '' ;
			cc_id = adidjson["index"]["ccAd"] !== undefined ? adidjson["index"]["ccAd"]["id"] : '' ;
			cc_container = adidjson["index"]["ccAd"] !== undefined ? adidjson["index"]["ccAd"]["container"] : '' ;
		}else{//非首页
			hf_id = adidjson["detail"]["hfAd"] !== undefined ? adidjson["detail"]["hfAd"]["id"] : '' ;
			hf_container = adidjson["detail"]["hfAd"] !== undefined ? adidjson["detail"]["hfAd"]["container"] : '';
			cc_id = adidjson["detail"]["ccAd"] !== undefined ? adidjson["detail"]["ccAd"]["id"] : '' ;
			cc_container = adidjson["detail"]["ccAd"] !== undefined ? adidjson["detail"]["ccAd"]["container"] : '' ;
		}
		if(hf_id == '' && cc_id == ''){
			return false;
		}
		
		if(hf_id != ''){
			//横幅广告
			(window.slotbydup = window.slotbydup || []).push({
				id: hf_id,
				container: hf_container,
				async: true
			});
			document.getElementById('pc_ad_hf').className = hf_container;
		}

		if(cc_id != ''){
			//橱窗广告
			(window.slotbydup = window.slotbydup || []).push({
				id: cc_id,
				container: cc_container,
				async: true
			});
			document.getElementById('pc_ad_cc').className = cc_container;
		}
		runScript('//cpro.baidustatic.com/cpro/ui/cm.js');
	}
	//根据域名获取百度广告ID
	function getBaiduAdId(){
		var bd_json = {"www.500.com":{"index":{"hfAd":{"id":"u6245944","container":"_ogmhb6adau"}}},"kaijiang.500.com":{"index":{"hfAd":{"id":"u6245940","container":"_s56gzhhhnti"},"ccAd":{"id":"u6245941","container":"_6anq7hpfgg4"}},"detail":{"hfAd":{"id":"u6245942","container":"_lbzoi44vlt9"},"ccAd":{"id":"u6245943","container":"_8rvmoa54s58"}}},"datachart.500.com":{"index":{"hfAd":{"id":"u6245923","container":"_i8n6qxg6qmr"},"ccAd":{"id":"u6245924","container":"_lndfxwov32m"}},"detail":{"hfAd":{"id":"u6245923","container":"_i8n6qxg6qmr"},"ccAd":{"id":"u6245924","container":"_lndfxwov32m"}}},"live.500.com":{"index":{"hfAd":{"id":"u6245932","container":"_t6sq4tyshqq"},"ccAd":{"id":"u6245933","container":"_2womekckak"}},"detail":{"hfAd":{"id":"u6245932","container":"_t6sq4tyshqq"},"ccAd":{"id":"u6245933","container":"_2womekckak"}}},"zx.500.com":{"index":{"hfAd":{"id":"u6245934","container":"_fup2x8ef1cw"},"ccAd":{"id":"u6245935","container":"_1p1e814uq17"}},"detail":{"hfAd":{"id":"u6245936","container":"_rqf7wikavd"},"ccAd":{"id":"u6245937","container":"_iibuxfuxlbc"}}},"odds.500.com":{"index":{"hfAd":{"id":"u6245938","container":"_964mjrcnnln"},"ccAd":{"id":"u6245939","container":"_lnycg6ur42e"}},"detail":{"hfAd":{"id":"u6245938","container":"_964mjrcnnln"},"ccAd":{"id":"u6245939","container":"_lnycg6ur42e"}}}};
		var hostname = location.hostname.replace("500boss","500");
		return bd_json[hostname] !== undefined ? bd_json[hostname] : false;
	}
	
	// 是否有登录信息的cookie
	// 分别触发登录/登出消息
	if (!/ck_user=[^=;]+/.test(document.cookie)) {
		//显示百度联盟广告
		setTimeout(function(){ 
			showBaiduAd();
		}, 1000);
	} 
})();

</script>
<!-- Baidu Button BEGIN -->
<script type="text/javascript" id="bdshare_js" data="type=tools&uid=6678073"></script>
<script type="text/javascript" id="bdshell_js"></script>
<script type="text/javascript">
var https ='https:' == document.location.protocol;
if(!https){
	document.getElementById("bdshell_js").src = "http://bdimg.share.baidu.com/static/js/shell_v2.js?cdnversion=" + Math.ceil(new Date()/3600000)
}
</script>
<!-- Baidu Button END -->
<!-- 用户战绩调整 begin -->
<span class="fu_icon_layer record_tips">
    <span style="left: 6px;" class="fu_icon_top"></span>
    <span style="width: auto;" class="fu_icon_con new_record"></span>
</span>
<!-- 用户战绩调整 end-->
<script type="text/javascript" src="https://www.500cache.com/public/js/stats.js?v=123"></script> </div>
<div class="tips_m" id="goal_tip" style="width:490px;display:none;z-index:100;">
	<div class="tips_b">
		<div class="tips_box">
			<div class="tips_title">
				<h2>500.com即时比分 进球提示</h2>
				<span class="close"><a href="javascript:void(0)" onclick="$('#goal_tip').hide();return false;">关闭</a></span>
			</div>
			<div class="tips_text">
				<table cellpadding="0" cellspacing="0" style="width:100%">
					<tr>
						<td width="60">联赛</td>
						<td width="56"></td>
						<td align="center" width="50">时间</td>
						<td align="center" width="120" style="font-weight:bold;">主队</td>
						<td align="center" width="50" style="font-size:20px;font-family:Verdana,Arial,Helvetica,sans-serif;padding-bottom:5px;"><strong><span class="blue">0</span>-<span class="blue">0</span></strong></td>
						<td align="center" width="120" style="font-weight:bold;">客队</td>
					</tr>
					<tr>
						<td colspan="6" align="right"><a href="https://live.500.com/" target="_blank">https://live.500.com/</a></td>
					</tr>
				</table>
			</div>
		</div>
	</div>
</div>
<div class="tips_m" id="yapan_tip" style="width:430px;display:none;z-index:99;">
	<div class="tips_b">
		<div class="tips_box">
			<div class="tips_table">
				<div style="text-align:center;font-size:14px;font-weight:bold;line-height:20px;"><span id="yapan_home"></span>&nbsp;<span id="yapan_score"> - </span>&nbsp;<span id="yapan_away"></span></div>
				<table id="yapan_table" class="pub_table" cellpadding="0" cellspacing="0" style="width:100%">
					<tr>
						<th width="20">&nbsp;</th>
						<th width="200">即时指数</th>
						<th width="200">初盘指数</th>
					</tr>
					<tr>
						<td>亚</td>
						<td>&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td>欧</td>
						<td>正在加载数据</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td>大</td>
						<td>&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
				</table>
			</div>
		</div>
	</div>
</div>
<div class="new_tips_box" style="width: 480px; display:none;" id="myproject">
  <div class="tips_title">
    <h2 class="tips_title_text">我的直播 - 导入方案</h2>
    <a href="javascript:void(0)" class="tips_close">关闭</a> </div>
  <form action="" method="get" class="drfa">
  <input type="hidden" name="t" value="my" />
  <div class="tips_content">
   <p>可在您购买的<span class="red">竞彩足球</span>方案中选择导入(最多查看近三天复式投注方案)</p>
    <div class="import_hml">
      <table width="100%" cellspacing="0" cellpadding="0" border="0" class="import_table">
        <colgroup>
        <col width="50px">
        <col width="110px">
        <col width="120px">
        <col>
        </colgroup>
        <tbody>
          <tr>
            <th>选中</th>
            <th>购买时间</th>
            <th>玩法</th>
            <th>购买金额</th>
          </tr>
        </tbody>
      </table>
      <div id="prolist" class="import_table">
        <table width="100%" cellspacing="0" cellpadding="0" border="0">
          <colgroup>
	        <col width="50px">
	        <col width="110px">
	        <col width="120px">
	        <col>
          </colgroup>
          <tbody></tbody>
        </table>
      </div>
      <div id="s_skep_foot" class="page"> <span class="float_l">全部:<label for="s_allSkepCase"><input class="cbox_radio ck_all" type="checkbox" value="" checked="checked"></label></span></div>
    </div>
  </div>
  <div class="tips_btn"><a class="btn_orange btn_width_auto import" href="javascript:void(0)">导入</a><span class="red notice"></span></div>
  </form>
</div>

<script>
$(function(){
    $(".td_warn").find("a").click(function(ev){
        var r = $(this).parents("tr").attr("r"),
            href = $(this).attr("href");
        if(r=='-1'){
            $(".warning_icon").removeClass("hide");            
            $(".warn_close").click(function(){    
                $(".warning_icon").addClass("hide");  
                window.open(href); 
            });
        }else{
            window.open(href);
        }
        ev.preventDefault();
    });    
});
</script>
		<style type="text/css">
			.app_cartoon_wrap {
	        position: fixed;
	        top: 300px;
	        left: 100px;
	        width: 140px;
	        height: 160px;
	        overflow: hidden;
	      }
	      .app_cartoon_wrap .app_cartoon_content {
	        position: absolute;
	        top: 0;
	        left: 74px;
	        width: 140px;
	        height: 160px;
	        transition: left 0.6s ease;
	        -moz-transition: left 0.6s ease;
	        -webkit-transition: left 0.6s ease;
	        -o-transition: left 0.6s ease;
	      }
	      .app_cartoon_wrap .app_cartoon_content .btn_close {
	        position: absolute;
	        top: 0;
	        right: 0;
	        width: 20px;
	        height: 20px;
	        background: url(https://www.500cache.com/public/images/ad/btn_close.png) no-repeat;
	        background-size: contain;
	        z-index: 2;
	      }
	      .app_cartoon_wrap .app_cartoon_content a {
	        position: relative;
	        display: block;
	        width: 100%;
	        height: 100%;
	        border: none;
	        z-index: 1;
	      }
	      .app_cartoon_wrap .app_cartoon_content img {
	        position: relative;
	        width: 100%;
	        height: 100%;
	        border: none;
	      }
	      .app_cartoon_wrap .app_cartoon_content:hover {
	        left: 0;
	      }
	      .app_cartoon_wrap.nohover .app_cartoon_content{
	        left: 0;
	      }
		</style>		<div id="cartonnLeft" style="display:none" class="app_cartoon_wrap " onclick="_hmt.push(['_trackEvent','pc_kaijiang','click','floatAD'])">
	      <div class="app_cartoon_content">
	        <span class="btn_close" onclick="btnClose()"></span>
	        <a  href="https://www.500.com/wap/index.php" target="_blank" title="" onclick="if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000609','DCSext.button_n','10082315');}" {$appShowHtml} ><img  src="https://img.500.com/upimages/sfc/202002/20200213115909_9480.gif" border="0" width="140" height="160" alt="" align="top" /></a>
	      </div>
	    </div>  <script  type="text/javascript">
                    function getElementsClassObj(strClass){
                        var obj = null;
                        if(document.getElementsByClassName){
                            obj = document.getElementsByClassName(strClass);
                        }else{
                            var ret = [];   
                            var els = document.getElementsByTagName('div');
                            for(var i=0; i<els.length; i++){       
                                if(els[i].className === strClass  || els[i].className.indexOf(strClass)>=0 ){           
                                    ret.push(els[i]);
                                    break;
                                }
                            }
                        }
                        return obj?obj[0]:null;
                    }
                    function changeDivWidth(){
                        var _bodyObj = document.getElementById("bd"),
                            divLeft = "100px",bodyLeft = _bodyObj && _bodyObj.offsetLeft;
                        document.getElementById("cartonnLeft").style.left = (bodyLeft  -140 )+"px";
                        
                        document.getElementById("cartonnLeft").style.display = "block";
                       
                    }
                    function btnClose(){                       
                        document.getElementById("cartonnLeft").style.display = "none";
                    }
                    window.onload = function() {
                        changeDivWidth();
                    };
                    window.onresize=function(){  
                         changeDivWidth();  
                    } 
                    ; </script><script>setTimeout(function(){ if(typeof(dcsMultiTrack)=='function'){dcsMultiTrack('DCSext.button_t','05000000','DCSext.button_w','05000000','DCSext.button_b','05000000','DCSext.button_c','05000609','DCSext.button_n','00082315');}},3000)</script>
</body>
</html>

'''




urlt = "https://pycmstest.lexue.com"
urlp = "https://pycmspre.lexue.com"
urlts = "https://pycmstsl.lexue.com"
urlo = "https://pycms.lexue.com"

url = ["https://pycmstest.lexue.com","https://pycmspre.lexue.com","https://pycmstsl.lexue.com","https://pycms.lexue.com"]

import os,yaml
file = open(os.path.abspath('..') + r"\configure\database.yml", "r", encoding="utf8")
config = yaml.load(file.read(), Loader=yaml.Loader)
print(config['pycms_controller']['path'])