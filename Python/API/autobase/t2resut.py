import os,json
import datetime
from jinja2 import Template
from  autobase import getdata4file
from autobase import GetTestData_fix1
from autobase.utils import log
class t2result(object):
    def __init__(self,inputdatastream):
        self.data = inputdatastream

    def transformIndex(self): #// total result data table show

        templetepath = os.path.abspath("..") + "/autodata/template/index.html.vm"
        s = Template(templetepath)
        s.render()

    def transformBrowse(self,flowname):#// get every case data templete ,use this

        #casecode

        templetepath = os.path.abspath('..') + '/autodata/template/browse_demo.vm'
        s = Template(getdata4file.connect_to(templetepath).parsed_data)
        log.info("return data %s" % self.data)

        # datain = {"casecode":self.data[1],"caseTitle":self.data[2],"reqString":self.data[0]} # data inputdatstream

        datain = {
            "casecode":self.data[1],  #案例名称
            "caseTitle":self.data[2], #案例标题
            "reqString":json.dumps(self.data[0],ensure_ascii=False,separators=(',',':')),#发送报文
            "finishTime":datetime.datetime.now() #完成时间
        } # data inputdatstream

        log.info("datain %s",datain)
        fileoutstream = s.render(datain)


        with open(os.path.abspath("..")+"/autodata/records/" + flowname + "/"+ self.data[1] +".html" , 'w',encoding="utf-8") as f:
            f.write(fileoutstream)
        f.close()


def test():
    flowname = "冰鉴"
    xlxsfp = "冰鉴接口案例.xlsx"
    exeshtname = "冰鉴对外投资"
    testfile = GetTestData_fix1.CaseDataMap4Xls(flowname, xlxsfp, exeshtname,9).casealldata()
    print(testfile)
    t2result(testfile).transformBrowse()