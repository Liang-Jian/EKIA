from autobase.HtmlRecorder import HtmlRecorder,t2Dict
import requests,sys,datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from autobase.SignatureUtil import Signature
from autobase.ProceCasedata import *
from autobase.FunctionLibray import readYaml,readYam
from autobase.Logger import ExecCount
from autobase.MailOperation import LexueMail

signature = Signature()


class HttpTransport(object):

    def __init__(self):

        self.reqdatalist  = ""                                     # data from xls
        self.encode       = ""                                     # gbk or utf8
        self.contentType  = ""                                     # application/xml
        self._method      = "post"
        self._http_post_status  = "http_post_status"               #
        self._resultData = "resultData"
        self.result = None
        self.resultrsp = list()                                    # get all score
        self.sess = requests.session()                             # request
        self.loginreq = HttpGetHeader.getLoginReq()                # login req ,get login data
        self.T_count = ExecCount()                                 # succ case count all
        self.F_count = ExecCount()                                 # fail case count
        self.timeout = readYaml("timeout")
        loginurl = readYaml("url")
        tenantId= loginurl.split(".")[0].replace("https://","")

        self._headers = {
            "appKey": readYaml("appKey"),
            "token": "123",
            "signature": signature.getSignature(self.loginreq[0]),
            "tenantId": tenantId,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.loginReponseStr = self.sess.post(url=self.loginreq[4], stream='True', data=json.loads(self.loginreq[0]), verify=False, timeout=self.timeout, headers=self._headers).text
        AllFlowData().allflowdata=(eval(self.loginReponseStr))
        getBasicClassInfo()

    def httpMethod(self, reqdata):
        self.reqdatalist = reqdata
        __url  = self.reqdatalist[4]
        __req  = self.reqdatalist[0]
        __icon = self.reqdatalist[3]
        l = __icon.split(".")
        self.setHeaderToken(l[1])

        Logi("接   口:=%s" % self.reqdatalist[-1][:-3])
        Logi("headers:\t")
        for k,v in self._headers.items():
            Logi("\t\t%s:=%s" % (k,v))
        self.writesMsg(self.reqdatalist[0])


        if l[0] == "post" and l[1] == "js":
            response_Str = self.sess.post(url=__url, data=json.dumps(json.loads(self.reqdatalist[0]), ensure_ascii=True), headers=self._headers, verify=False, timeout=4, stream='True')

        elif l[0] == "post" and l[1] == "ue":
            response_Str = self.sess.post(url=__url,data=json.loads(self.reqdatalist[0]), headers=self._headers,verify=False, timeout=4)

        elif l[0] == "put" and l[1] == "ue":
            response_Str = self.sess.put(url=__url, data=json.loads(self.reqdatalist[0]),headers=self._headers)

        elif l[0] == "get":
            response_Str = self.sess.get(url=__url,params=json.loads(self.reqdatalist[0]),headers=self._headers)
            # 把get 请求后的数据放到allflowdata zhong
            return
        try:
            responsecasedata = response_Str.text
            self.writerMsg(responsecasedata)
            Logi("返回数据:=%s" % responsecasedata)
            self.dataAssert(self.reqdatalist[5],responsecasedata)

        except Exception as e:
            raise e
        return responsecasedata


    def setHeaderToken(self, data):
        if data.lower() == "ue":
            self._headers['Content-Type'] = "application/x-www-form-urlencoded"
            self._headers['token']     = AllFlowData().allflowdata.get('value').get('token')
            self._headers['isadmin']     =str(AllFlowData().allflowdata.get('value').get('isAdmin'))
            self._headers['userId'] = str(AllFlowData().allflowdata.get('value').get('sysUserId'))  # must be str
            self._headers['signature'] = Signature().getSignature(self.reqdatalist[0])
        elif data.lower() == "js":
            self._headers['Content-Type'] = "application/json;charset=utf-8"
            self._headers['token'] = AllFlowData().allflowdata.get('value').get('token')
            self._headers['isadmin']     =str(AllFlowData().allflowdata.get('value').get('isAdmin'))
            self._headers['userId'] = str(AllFlowData().allflowdata.get('value').get('sysUserId'))
            self._headers['signature'] = signature.getSignature()
        else: # get method .
            self._headers['Content-Type'] = "application/json;charset=utf-8"
            self._headers['token']     = AllFlowData().allflowdata.get('value').get('token')
            self._headers['isadmin']     =str(AllFlowData().allflowdata.get('value').get('isAdmin'))
            self._headers['userId'] = str(AllFlowData().allflowdata.get('value').get('sysUserId'))
            self._headers['signature'] = Signature().getSignature(self.reqdatalist[0])

    def dataAssert(self,A,B):
        '''
        1,数据比较 ，断言 ， 保存断言结果，使用计数器保存对比结果，计算出通过率,保存为html
        :return:
        '''

        if A in B :
            Logi("断    言 PASS")
            self.resultrsp.append("T")
            self.reqdatalist.insert(7, "T")
            self.reqdatalist.insert(8, B)
            self.T_count.count()
            # HtmlRecorder(self.reqdatalist).data2html()  # only failcase have record file

        else:
            Logi("断    言 FAIL")
            Logi("A:=%s" % A)
            Logi("B:=%s" % B)
            self.reqdatalist.insert(7, "F")
            self.reqdatalist.insert(8, B)
            self.F_count.count()
            HtmlRecorder(self.reqdatalist).data2html()
            # sys.exit(1)
    def writerMsg(self, message):
        try:
            recv_msg = open(
                os.path.abspath("../") + "/msg/" + self.reqdatalist[-1][:-3] + datetime.datetime.now().strftime("%d-%H-%M") + "_recv.txt", "w",
                encoding="utf-8")
            recv_msg.write(str(message))
        finally:
            recv_msg.close()

    def writesMsg(self,message):
        send_msg = open(
            os.path.abspath("../") + "/msg/" + self.reqdatalist[-1][:-3] + datetime.datetime.now().strftime("%d-%H-%M") + "_send.txt", "w",
            encoding="utf-8")
        send_msg.write(str(message))
        send_msg.close()

    def __del__(self):
        LexueMail(self.T_count.count(),self.F_count.count())
        # pass

class HttpGetHeader(object):
    reqlist     = list()
    loginPath   = "/system/sysUser/login"
    postmethod  = "post.ue"
    loginvmname = "cmslogin.vm"

    @classmethod
    def getLoginReq(cls):

        username = readYaml("loginName")
        password = readYaml("password")
        loginurl = readYaml("url")

        templetepath = os.path.abspath('..') + '/autodata/template/' + HttpGetHeader.loginvmname
        templetestring = open(templetepath,'r', encoding='utf-8', errors='ignore').read()
        caseTepletedata = Template(templetestring)
        loginreq = caseTepletedata.substitute(loginName=username,password=password)

        HttpGetHeader.reqlist.append(loginreq)
        HttpGetHeader.reqlist.insert(1, None)
        HttpGetHeader.reqlist.insert(2, None)
        HttpGetHeader.reqlist.insert(3, HttpGetHeader.postmethod)
        HttpGetHeader.reqlist.insert(4, loginurl + HttpGetHeader.loginPath)
        HttpGetHeader.reqlist.insert(5, "SUCCESS")
        HttpGetHeader.reqlist.insert(6, HttpGetHeader.loginvmname)
        Logi("登录报文:=%s" % HttpGetHeader.reqlist)
        return HttpGetHeader.reqlist

def getBasicClassInfo():
    basicinfo = readYam("ClassInfo")
    for key,val in basicinfo.items():
        if isinstance(val, str) and val.startswith("select"):
            basicinfo[key] = sqlValue(MsqService().search_db(val))
    AllFlowData().allflowdata.update(basicinfo)