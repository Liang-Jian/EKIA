
from abc import ABCMeta,abstractclassmethod


# flowname   = "冰鉴"
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

    @property
    def caseEntity(self):
        return  self.execResultMap

    def run(self):
        caseEntityData = []

        # caseEntityData = GetTestData_fix1.CaseDataMap4Xls(flowname, xlxsfp, exeshtname,self.line).caseDataAll()
        # responData = self.p.httpMethod("http://10.10.94.23:7001/flow/dataflow/getData", caseEntityData[0])
        # Logi("repondata type %s" % type(responData))
        # Logi("caseEntityData %s" % caseEntityData)
        # t2resut.t2result(caseEntityData).transformBrowse(flowname)

if __name__ == '__main__':

    for i in range(9,11):
        flow(i).run()