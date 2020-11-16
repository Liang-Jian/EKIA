from autobase import HttpTransStatus
from autobase.logger import *
import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from autobase.signatureUtil import *
from string import Template
from autobase.parseexcel import *

class HttpTransport(object):
    __headerMap = dict()
    def __init__(self):

        self.encode       = "" #= "GBK"; //"UTF-8";
        self.contentType  = ""  #"application/xml";
        self._method      = "post"
        self._http_post_status  = "http_post_status"
        self._resultData = "resultData"
        self.result = None
        self.sess = requests.session()



    def httpMethod(self, url, contentstring):
        #send-recv method  url contentsting --> data
        #return new map data,include all key
        totaldata = dict()
        try:
            result  = requests.post(url=url,headers=self.header,json=contentstring)
            log.info("resultCode %s" , result.status_code)
            if result.status_code == 200:
                totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_SUC})
            elif result.status_code == 500:
                totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_500})
            else:
                totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_FAIL})
        except IOError as e:
            totaldata.update({self._http_post_status: HttpTransStatus.HttpTransStatus().HTTPTRANS_STATUS_FAIL})
            log.error(e)


        #get return data
        try:
            returndata  = result.text
            log.info("返回数据:=%s" % returndata)

            totaldata.update({self._resultData:returndata})
            log.info("totalData %s",totaldata)
        except Exception as e :
            raise  e

        return totaldata

    @property
    def headerMap(self):
        return  self.__headerMap
    @headerMap.setter
    def headerMap(self,key,value):
        self.__headerMap[key] = value





class HttpHeaderMap(object):
    def __init__(self, request_str):
        self.request_str = request_str   # 传进来的报文，用来算signature
        self.pe = ParseExcel()
        self.headerss    = {
            "appKey"      : "201820011141153",
            "token"       : "123",
            "signature"   : "79E48482F30ED5CA96DCBB4DFA43D1576DBC2B74",
            "tenantId"    : "pycmspre",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    def __str__(self):
        pass

    @property
    def headerMaps(self):
        return self.headerss
    @headerMaps.setter
    def headerMaps(self,key,value):
        self.headerss[key] = value
    def post(self):
        content = open(r'D:\zdhlog\EKIA\Python\API\autodata\template\cmslogin.vm', 'r', encoding='utf-8',errors='ignore').read()
        # content = self.request_str
        xlxsObject = self.pe.load_work_book(r"D:\zdhlog\EKIA\Python\API\autodata\testcase\培优接口用例.xlsx").get_sheet_by_name("CMS接口")
        username = self.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=3)  # url
        password = self.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=4)  # url

        templetepath = os.path.abspath('..') + '\\autodata\\template\\' + 'cmslogin.vm'
        print(templetepath)
        templetestring = open(templetepath,'r', encoding='utf-8', errors='ignore').read()
        caseTepletedata = Template(templetestring)
        casedata = caseTepletedata.substitute(loginName=username,password=password)
        # str - json
        zhuangtai_data = json.loads(casedata)
        print(zhuangtai_data)
        # 获取 signature
        login_sginature = Signature().getSignature(zhuangtai_data)
        print(login_sginature)
        self.headerMaps['signature'] = login_sginature
if __name__ == '__main__':
    s  =HttpHeaderMap().post()
