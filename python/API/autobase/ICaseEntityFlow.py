

from abc import ABCMeta,abstractclassmethod
from autobase import GetTestData_fix1,HttpTransport,t2resut
from autobase.utils import log

flowname   = "冰鉴"
xlxsfp     = "冰鉴接口案例.xlsx"
exeshtname = "冰鉴对外投资"
execline   = 10



class ICaseEntityFlow(metaclass=ABCMeta):
    @abstractclassmethod
    def run(self):
        pass


class flow(ICaseEntityFlow):
    def __init__(self ,line):

        self.line = line
        self.execResultMap = dict()
        self.execResultInfo= dict()
        self.p = HttpTransport.HttpTransport()

    @property
    def caseEntity(self):
        return  self.execResultMap

    def run(self):
        caseEntityData = []

        caseEntityData = GetTestData_fix1.CaseDataMap4Xls(flowname, xlxsfp, exeshtname,self.line).casealldata()
        responData = self.p.httpPost("http://10.10.94.23:7001/flow/dataflow/getData", caseEntityData[0])
        log.info("repondata type %s" ,type(responData))
        log.info("caseEntityData %s" , caseEntityData)
        t2resut.t2result(caseEntityData).transformBrowse(flowname)

if __name__ == '__main__':

    for i in range(9,11):
        flow(i).run()