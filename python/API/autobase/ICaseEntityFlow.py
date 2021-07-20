import sys,os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autobase.HttpTransport import HttpTransport
from autobase.ProceCasedata import *
from autobase.Scheduler import ICaseEntityFlow

'''
程序入口
creat by joker shi
'''

class flow(ICaseEntityFlow):
    def __init__(self):
        self.startline = 9
        self.execfp = readYaml("path")
        self.execst = readYaml("sheet")
        self.execli = readYaml("finishRowNo")
    def run(self):
        start = time.time()
        p = HttpTransport()
        for i in range(self.startline,self.execli + 1):
            testfile = CaseDataMap4Xls(self.execfp, self.execst,i).caseDataAll()
            p.httpMethod(testfile)

        end = time.time()

        Logi("执行时间:={} 秒".format(float(end-start)))


if __name__ == '__main__':
    flow().run()