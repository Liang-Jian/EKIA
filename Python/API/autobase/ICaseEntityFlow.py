
from abc import ABCMeta,abstractclassmethod
from autobase.httpTransport import *
from autobase.proceCasedata import *


# flowname   = "冰鉴"
# xlxsfp     = "冰鉴接口案例.xlsx"
# exeshtname = "冰鉴对外投资"
# execline   = 10

#
# import yaml,os
# def readyaml(key):
#     file = open(os.path.abspath('..') + r"\configure\database.yml", "r", encoding="utf8")
#     config = yaml.load(file.read(), Loader=yaml.Loader)
#     conf = config['pycms_controller']
#     print(conf[key])
#     return conf[key]



class ICaseEntityFlow(metaclass=ABCMeta):
    @abstractclassmethod
    def run(self):
        pass


class flow(ICaseEntityFlow):
    def __init__(self):
        self.startline = 9
        # self.line = line
        # self.execResultMap = dict()
        # self.execResultInfo= dict()

    # @property
    # def caseEntity(self):
    #     return  self.execResultMap

    def run(self):
        caseEntityData = []

        # caseEntityData = GetTestData_fix1.CaseDataMap4Xls(flowname, xlxsfp, exeshtname,self.line).caseDataAll()
        # responData = self.p.httpMethod("http://10.10.94.23:7001/flow/dataflow/getData", caseEntityData[0])
        # Logi("repondata type %s" % type(responData))
        # Logi("caseEntityData %s" % caseEntityData)
        # t2resut.t2result(caseEntityData).transformBrowse(flowname)


        execfp = readyaml("path")
        execst = readyaml("sheet")
        execli = readyaml("finishRowNo")

        p = HttpTransport()

        for i in range(self.startline,execli+1):
            testfile = CaseDataMap4Xls(execfp, execst,i).caseDataAll()
            p.httpMethod(testfile)



def startrun():
    flow().run()


startrun()