

from  autobase import getdata4file
send_list = []

class HtmlRecorder: #生成模板表达式  html报告

    #传入list的数据，[案例编号,测试需求,编号案例名称,{send_baowen},{recv_baowen}] >> htmlRecordfile

    caserecordpath = '/home/joker/ApiTestFrame/autodata/template/browse_demo.vm'
    def __init__(self):
        self.vmpath = None
        self.data = {}



    def filePath(self):

        xml_factory = getdata4file.connect_to('/home/joker/ApiTestFrame/autodata/template/browse_demo.vm')
        xml_data = xml_factory.parsed_data
        print(xml_data)


HtmlRecorder().filePath()