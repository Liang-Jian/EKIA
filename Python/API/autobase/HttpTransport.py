import requests
from autobase import HttpTransStatus
from autobase.logger import *


class HttpTransport(object):
    __headerMap = dict()
    def __init__(self):

        self.encode       = "" #= "GBK"; //"UTF-8";
        self.contentType  = ""  #"application/xml";
        self._method      = "post"
        self._http_post_status  = "http_post_status"
        self._resultData = "resultData"
        self.result = None
        self.header = {"Content-Type":"application/json"}

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




