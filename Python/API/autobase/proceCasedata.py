from autobase.parseexcel import *
import json
from string import Template
from autobase.logger import *
from autobase.functinlibs import *


def delNkey(dictey):
    startN = 0
    while startN < len(dictey):
        try:
            dictey.pop(list(dictey.keys())[list(dictey.values()).index("$local")])
        except ValueError as e:
            print(e)
            break
        startN += 1
    return dictey


def localdata(dictey):  # // set value2local
    print(dictey)
    for key, val in dictey.items():
        if isinstance(val, str) and val.startswith("${local"): dictey[key] = dictey[val[7:]]
    return dictey


def local(key):  # //返回一个ico给localdata
    return "${local" + key


def flowdatafix(data):   # // set flowkey
    for key, val in data.items():
        if isinstance(val, str) and val.startswith("${flow"):
            flowdata = AllFlowData().allflowdata
            data[key] = flowdata.get(val[8:-3])
    return data

class CaseDataMap4Xls(object):
    __filepath = os.path.abspath("..") + "/autodata/testcase/"

    def __init__(self, xlxspath, xlsxsheet, execline):

        self.test_data_path = CaseDataMap4Xls.__filepath + xlxspath  # 文件路径 str->
        self.test_data_sheet = xlsxsheet                             # sheet名 str->冰鉴接口
        self.execline = execline                                     # 执行行   int-> 8
        self.pe = ParseExcel()
        self.pe.load_work_book(self.test_data_path)
        self.__casedata = list()  # 返回总的list
        self.commondata = dict()  # 返回公共数据，只需要读取一次
        self.execflowname = ""    # 执行流程名字
        self._caseinfo = []
        self.rows = None
        # self.casestartrow = casestartrow
        # self.caseendrow = caseendrow
        self.publicdata = dict()
    def data4rows_flow(self, start_line, end_line):
        '''
        :param flowaction:
        :param start_line: {2:3} {6:N}
        :param end_line:
        :return: dict
        '''
        # # 生成sheet对象，取任意两行的数据对象
        # test = AllFlowData().dictdata.get('value')
        # print(test)

        sheet = self.pe.get_sheet_by_name(self.test_data_sheet)
        _key = self.pe.get_row(sheet, start_line)
        _value = self.pe.get_row(sheet, end_line)

        key = list()
        for x in _key:  # key
            x = x.value
            key.append(x)
        value = list()  # val
        for y in _value:
            y = y.value
            value.append(y)

        # // 数据是由<di-$$>进行了分段，分段截取对应场景交易的数据，组成dict

        startdataico = "<Di=\"" + self.execflowname + "\">"
        enddataico   = "<Do=\"" + self.execflowname + "\">"

        key_len = len(key)
        start_index = 0
        end_index = 0
        for i in range(key_len):
            if key[i] == startdataico:
                start_index = key.index(key[i]) + 1
                for i in range(start_index, key_len):
                    # print(key[i])
                    if key[i] == enddataico:
                        end_index = key.index(key[i])
                        break
        key = key[start_index:end_index]
        value = value[start_index:end_index]
        self.dataMap = dict(zip(key, value))

    def data4rows_case(self, start_line, end_line):
        '''
        :param start_line: 起始行
        :param end_line:   结束行
        :return: casedata(!: 必须先执行，取得模板名,给公共数据用)，数据处理flowdata
        '''
        # 生成sheet对象，取任意两行的数据对象
        sheet = self.pe.get_sheet_by_name(self.test_data_sheet)
        _key = self.pe.get_row(sheet, start_line)
        _value = self.pe.get_row(sheet, end_line)

        key = list()
        for x in _key:  # key
            x = x.value
            key.append(x)
        value = list()  # val
        for y in _value:
            y = y.value
            value.append(y)
        self.execflowname = value[5][:-3]

        # // 数据是由<di-$$>进行了分段，分段截取对应场景交易的数据，组成dict
        startdataico = "<Di=\"" + self.execflowname + "\">"
        enddataico   = "<Do=\"" + self.execflowname + "\">"

        key_len = len(key)
        start_index = 0
        end_index = 0
        for i in range(key_len):
            if key[i] == startdataico:
                start_index = key.index(key[i]) + 1
                for i in range(start_index, key_len):
                    # print(key[i])
                    if key[i] == enddataico:
                        end_index = key.index(key[i])
                        break
        key = key[start_index:end_index]
        value = value[start_index:end_index]
        self.dataMap = dict(zip(key, value))


    def testdataprocess(self):
        '''
        1、处理案例测试数据，去除value值为None空，以便与源数据进行数据合并
        2、step1:将获取到的案例数据做替换，把“${null}”，替换成“”，意思是赋值对应的字段空值，然后重组dict
        3、step2:重组后的dict做，表达式赋值“${}”，查找value为${}的表达式，脱去${},再用eval()执行
        :return:
        '''
        key_n = list()
        value_n = list()

        for key, value in self.dataMap.items():
            if value != None:
                key_n.append(key)
                value_n.append(value)
        dict_n = dict(zip(key_n, value_n))
        dict_n = json.dumps(dict_n)
        dict_n = dict_n.replace("${null}", "")
        self.dict_n = json.loads(dict_n)

        key_m   = []
        value_m = []

        for key, value in self.dict_n.items():
            value = str(value)
            if value.startswith("${") and "flow" not in value and "local" not in value:
                value_new = value[2:-1]
                value_new = eval(value_new)
                key_m.append(key)
                value_m.append(value_new)
        dict_m = dict(zip(key_m, value_m))
        self.casedata = dict(self.dict_n, **dict_m)
        # print(localdata(self.casedata))            # process ${local data

        flowdatafix(self.casedata)            # process ${flow  data
        return self.casedata

    def get_test_data_replace(self):  # ${}-> realValue

        key_n   = list()
        value_n = list()
        for key, value in self.dataMap.items():
            if value.startswith("${"):
                value_new = value[2:-1]
                value_new = eval(value_new)
                key_n.append(key)
                value_n.append(value_new)

        dict_n = dict(zip(key_n, value_n))
        self.get_test_data_be_replaced = dict(self.dataMap, **dict_n)
        # localdata(self.get_test_data_be_replaced)
        return self.get_test_data_be_replaced

    def caseinfo(self):
        caseInfoData = list()
        xlxsObject = self.pe.load_work_book(self.test_data_path).get_sheet_by_name(self.test_data_sheet)
        caseid = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=1))                        # 案例编号
        caseName = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=2))                      # 案例名称
        interfacetype = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=3))                 # 接口类型
        interfacepath = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=4))                 # 接口路径
        exresult = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=5))                      # 预期结果
        templename = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=6))                    # 模板名称
        caseInfoData.insert(0, caseid)
        caseInfoData.insert(1, caseName)
        caseInfoData.insert(3, interfacetype)
        caseInfoData.insert(4, interfacepath)
        caseInfoData.insert(5, exresult)
        caseInfoData.insert(6, templename)

        return caseInfoData



    # def getFinallyReq(self, data):
    #     '''
    #     :param data:  拼好的报文
    #     :return    :  报文完成体
    #     '''
    #
    #     xlxsObject = self.pe.load_work_book(self.test_data_path).get_sheet_by_name(self.test_data_sheet)
    #     vmname = (self.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=3))  # vm-tem-name
    #     print(vmname)
    #     Logi("模板文件:=%s" % vmname)
    #     templetepath = os.path.abspath('..') + '\\autodata\\template\\' + vmname
    #
    #     # caseTepletedata = Template(getdata4file.connect_to(templetepath).parsed_data)
    #     caseTemplate = Template(templetepath)
    #     caseTemplate1= caseTemplate.substitute()

    def getFinallyReq(self, data):
        '''
        :param data:  拼好的报文 list ， 拼interface url
        :return    :  报文完成体
        '''

        if not isinstance(data,list): raise ("Data Type Not Dick")
        _l = data
        vm_name,singlecasedata  = _l[-1],_l[0]
        Logi("模板文件:=%s" % vm_name)
        xlxsObject = self.pe.load_work_book(self.test_data_path).get_sheet_by_name(self.test_data_sheet)
        mainurl = self.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=2)  # url
        templetepath = os.path.abspath('..') + '\\autodata\\template\\' + vm_name
        templetestring = open(templetepath,'r', encoding='utf-8', errors='ignore').read()
        caseTepletedata = Template(templetestring)
        casedata = caseTepletedata.substitute(singlecasedata) # 报文 Str type
        Logi("发送报文:=%s" % casedata)
        _l[0] = casedata.replace("\n","").replace("\t","")
        _l[4] = mainurl + _l[4]
        Logi("执行报文:=%s" % _l)
        return _l

    def caseDataAll(self):

        self.data4rows_case(8, self.execline)
        self.casedata = self.testdataprocess()
        Logi("单行数据:=%s" % self.casedata)

        if len(self.publicdata) == 0:
            self.data4rows_flow(4, 5)
            self.publicdata = self.get_test_data_replace()
        Logi("公共数据:=%s" % self.publicdata)

        self.finallycasedata = dict(self.publicdata, **self.casedata)
        print(self.finallycasedata)
        Logi("合并数据:=%s" % localdata(self.finallycasedata))
        # Logi("合并数据:=%s" % self.finallycasedata)

        self.__casedata.append(self.finallycasedata)
        self.__casedata += self.caseinfo()
        # Logi("用例数据:=%s" % self.__casedata)
        self.getFinallyReq(self.__casedata)

        return self.__casedata
