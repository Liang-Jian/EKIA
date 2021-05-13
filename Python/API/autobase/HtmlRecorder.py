import os,datetime,json,ast
from  autobase import GetVmFile,Logger
from jinja2 import Template
from autobase.Logger import AllFlowData


def t2Pass(_str):
    if _str == "F":
        return "fail"
    elif _str == "T":
        return "pass"

def t2Dict(_str):
    try:
        _dic = ast.literal_eval(_str)
        return _dic
    except:
        raise ("con't convert dict")


class HtmlRecorder(object):
    # data in  =[req,案例编号, 案例名称,接口类型,接口路径,预期结果,模板名称,断言结果,rsp]
    # >>> htmlrecorder

    def __init__(self,result_data):
        self.data = result_data
        self.reqString      = self.data[0]             # 请求报文
        self.casecode       = self.data[1]             # 案例编号
        self.caseTitle      = self.data[2]             # 案例名称
        self.interType      = self.data[3]             # 接口类型
        self.interPath      = self.data[4]             # 接口路径
        self.expectResult   = self.data[5]             # 预期结果
        self.templeteName   = self.data[6]             # 模板名称
        self.assertresult   = t2Pass(self.data[7])     # 断言结果
        self.responseString = self.data[8]             # 返回报文
        # Allflowdata      deving                      # 流程报文


    def dataassert(self):
        pass

    def data2html(self):

        templetepath = os.path.abspath('..') + '/autodata/template/browse_demo.vm'
        s = Template(GetVmFile.connect_to(templetepath).parsed_data)
        Logger.Logi("HtmlRecorder received data:=%s" % self.data)

        datain = \
            {
            "reqString": self.reqString,
            "casecode": self.casecode,
            "caseTitle": self.caseTitle,
            "interType": self.interType,
            "interPath": self.interPath,
            "expectResult": self.expectResult,
            "templeteName": self.templeteName,
            "assertresult": self.assertresult,
            "responseString": self.responseString,
            "finishTime": datetime.datetime.now(),
            "responseStringdict": json.loads(self.responseString),
            "flowdata": AllFlowData().allflowdata
        }

        _fileOutStream = s.render(datain)
        self.writeHtml(_fileOutStream)
        Logger.Logi("%s writed to html success" % self.templeteName[:-3])
        Logger.Logi("#--------------分隔符---------------#")
        return

    def writeHtml(self, message):
        send_msg = open(
            os.path.abspath("../") + "/autodata/records/" + self.templeteName[:-3] + "_"+ self.data[7] +".html", "w",
            encoding="utf-8")
        send_msg.write(message)
        send_msg.close()


    def __del__(self):
        pass

