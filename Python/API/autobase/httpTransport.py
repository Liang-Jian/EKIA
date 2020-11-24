from autobase import HttpTransStatus
from autobase.recorder import *
import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from autobase.signatureUtil import Signature
from autobase.proceCasedata import *

signature = Signature()


class HttpTransport(object):

    def __init__(self):

        self.reqdatalist  = ""                                     # data from xls
        self.encode       = ""                                     # gbk or utf8
        self.contentType  = ""                                     # "application/xml";
        self._method      = "post"
        self._http_post_status  = "http_post_status"               #
        self._resultData = "resultData"
        self.result = None
        self.resultrsp = list()                                    # get all score
        self.sess = requests.session()                             # request
        self.loginreq = HttpGetHeader.getLoginReq()                # login req ,get login data
        self._headers = {
            "appKey": "201820011141153",
            "token": "123",
            "signature": signature.getSignature(self.loginreq[0]),
            "tenantId": "pycmspre",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.loginReponseStr = self.sess.post(url=self.loginreq[4], stream='True', data=json.loads(self.loginreq[0]), verify=False, timeout=4, headers=self._headers).text
        AllFlowData().allflowdata=(eval(self.loginReponseStr))

    # def httpMethod(self, url, contentstring):
    #
    #     totaldata = dict()
    #     try:
    #         result  = requests.post(url=url,headers=self.header,json=contentstring)
    #         log.info("resultCode %s" , result.status_code)
    #         if result.status_code == 200:
    #             totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_SUC})
    #         elif result.status_code == 500:
    #             totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_500})
    #         else:
    #             totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_FAIL})
    #     except IOError as e:
    #         totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_FAIL})
    #         log.error(e)
    #
    #
    #     #get return data
    #     try:
    #         returndata  = result.text
    #         log.info("返回数据:=%s" % returndata)
    #
    #         totaldata.update({self._resultData:returndata})
    #         log.info("totalData %s",totaldata)
    #     except Exception as e :
    #         raise  e
    #
    #     return totaldata



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
        # Logi("案例报文:=%s" % self.reqdatalist)
        self.writesMsg(self.reqdatalist[0])


        if l[0] == "post" and l[1] == "js":
            response_Str = self.sess.post(url=__url, data=json.dumps(eval(self.reqdatalist[0]), ensure_ascii=True), headers=self._headers, verify=False, timeout=4, stream='True')

        elif l[0] == "post" and l[1] == "ue":
            response_Str = self.sess.post(url=__url,data=json.loads(self.reqdatalist[0]), headers=self._headers,verify=False, timeout=4)

        elif l[0] == "put" and l[1] == "ue":
            response_Str = self.sess.put(url=__url, data=json.loads(self.reqdatalist[0]),headers=self._headers)

        try:
            responsecasedata = response_Str.text
            self.writeMsg(responsecasedata)
            Logi("返回数据:=%s" % responsecasedata)
            self.dataAssert(self.reqdatalist[5],responsecasedata)

        except Exception as e:
            raise e
        return responsecasedata

    @property
    def headerMap(self):
        return  self._headers

    @headerMap.setter
    def headerMap(self,key,value):
        self._headers[key] = value

    def setHeaderToken(self, data):
        if data.lower() == "ue":
            self._headers['Content-Type'] = "application/x-www-form-urlencoded"
            self._headers['token']     = AllFlowData().allflowdata.get('value').get('token')
            self._headers['userId'] = str(AllFlowData().allflowdata.get('value').get('sysUserId'))  # must be str
            self._headers['signature'] = Signature().getSignature(self.reqdatalist[0])
        elif data.lower() == "js":
            self._headers['Content-Type'] = "application/json"
            self._headers['token'] = AllFlowData().allflowdata.get('value').get('token')
            self._headers['userId'] = str(AllFlowData().allflowdata.get('value').get('sysUserId'))
            self._headers['signature'] = signature.getSignature()

    def dataAssert(self,A,B):
        '''
        1,数据比较 ，断言 ， 保存断言结果，使用计数器保存对比结果，计算出通过率,发给结果函数，保存为html
        :return:
        '''
        if A in B :
            Logi("assert PASS")
            self.resultrsp.append("T")
            self.reqdatalist.insert(7, "T")
            self.reqdatalist.insert(8, B)
            HtmlRecorder(self.reqdatalist).data2html()

        else:
            Logi("assert FAIL")
            self.reqdatalist.insert(7, "T")
            self.reqdatalist.insert(8, B)
            HtmlRecorder(self.reqdatalist).data2html()

    def writeMsg(self,message):
        try:
            recv_msg = open(
                os.path.abspath("../") + "\\Msg\\" + self.reqdatalist[-1][:-3] + datetime.datetime.now().strftime("%d-%H-%M-%S") + "_recv.txt", "w",
                encoding="utf-8")
            recv_msg.write(str(message))
        finally:
            recv_msg.close()

    def writesMsg(self,message):
        send_msg = open(
            os.path.abspath("../") + "\\Msg\\" + self.reqdatalist[-1][:-3] + datetime.datetime.now().strftime("%d-%H-%M-%S") + "_send.txt", "w",
            encoding="utf-8")
        send_msg.write(str(message))
        send_msg.close()

    def __del__(self):
        pass

class HttpGetHeader(object):
    pe          = ParseExcel()
    reqlist     = list()
    loginPath   = "/system/sysUser/login"
    postmethod  = "post.ue"
    loginvmname = "cmslogin.vm"

    @classmethod
    def getLoginReq(cls):
        xlxsObject = HttpGetHeader.pe.load_work_book(os.path.abspath('..') + "\\autodata\\testcase\\" +"培优接口用例.xlsx").get_sheet_by_name("CMS接口")
        username = HttpGetHeader.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=3)  # username
        password = HttpGetHeader.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=4)  # password
        loginurl = HttpGetHeader.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=2)  # u   r  l

        templetepath = os.path.abspath('..') + '\\autodata\\template\\' + HttpGetHeader.loginvmname
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
if __name__ == '__main__':
    xlxsfp = "培优接口用例.xlsx"
    exeshtname = "CMS接口"
    execline = 12
    p = HttpTransport()
    for i in range(9,13):
        testfile = CaseDataMap4Xls(xlxsfp, exeshtname,i).caseDataAll()
        p.httpMethod(testfile)