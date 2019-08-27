from autobase.parseexcel import *
from autobase.utils import *
import json
from jinja2 import Template
from autobase import getdata4file


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
    for key, val in dictey.items():
        if isinstance(val, str) and val.startswith("${local"): dictey[key] = dictey[val[7:]]
    return dictey


def local(key):  # //返回一个ico给localdata
    return "${local" + key


class CaseDataMap4Xls(object):
    __filepaht = os.path.abspath("..") + "/autodata/testcase/"

    def __init__(self, execflowname, xlxspath, xlsxsheet, execline):
        '''

        :param execflowname: 冰鉴
        :param xlxspath:     冰鉴接口案例.xlsx
        :param xlsxsheet:    冰鉴对外投资
        :param execline:
        :param caseendrow:
        '''

        self.test_data_path = CaseDataMap4Xls.__filepaht + xlxspath  # 文件路径 str->
        self.test_data_sheet = xlsxsheet  # sheet名 str->冰鉴接口
        self.execline = execline  # 执行行   int-> 8
        self.pe = ParseExcel()
        self.pe.load_work_book(self.test_data_path)
        self.__casedata = list()  # 返回总的list
        self.commondata = dict()  # 返回公共数据，只需要读取一次
        # self.casedata = dict()
        self.execflowname = execflowname  # 执行流程名字
        self._caseinfo = []
        self.rows = None
        # self.casestartrow = casestartrow
        # self.caseendrow = caseendrow
        self.publicdata = dict()
    def data4rows(self, flowaction, start_line, end_line) -> dict:  # two line data []-> {}
        '''
        1、调两次方法
        2、第一次取第2行、第3行，dict(zip(,))
        3、第二次取第6行、第n行(n是执行行)，dict(zip(,))
        4、两次调用都是带有表达式的
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

        # // 数据是由<data-in-$$>进行了分段，分段截取对应场景交易的数据，组成dict

        startdataico = "<data-in-name=\"" + flowaction + "\">"
        enddataico   = "<data-out-name=\"" + flowaction + "\">"

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
        # print(self.dataMap)

    def handle_case_test_data(self):
        '''
        1、处理案例测试数据，去除value值为None空，以便与源数据进行数据合并
        2、step1:将获取到的案例数据做替换，把“${null}”，替换成“”，意思是赋值对应的字段空值，然后重组dict
        3、step2:重组后的dict做，表达式赋值“${}”，查找value为${}的表达式，脱去${},再用eval()执行
        :return:
        '''
        key_n = list()
        value_n = list()
        for key, value in self.dataMap.items():
            # print(value)
            if value != None:
                key_n.append(key)
                value_n.append(value)
        dict_n = dict(zip(key_n, value_n))
        dict_n = json.dumps(dict_n)
        dict_n = dict_n.replace("${null}", "")
        self.dict_n = json.loads(dict_n)

        key_m = []
        value_m = []
        for key, value in self.dict_n.items():
            # print(value)
            value = str(value)
            if value.startswith("${"):
                value_new = value[2:-1]
                value_new = eval(value_new)
                key_m.append(key)
                value_m.append(value_new)

        dict_m = dict(zip(key_m, value_m))
        self.casedata = dict(self.dict_n, **dict_m)

        # print(self.casedata)
        return self.casedata

    def get_test_data_replace(self):  # ${}-> realValue

        key_n = list()
        value_n = list()
        for key, value in self.dataMap.items():
            # print(value)
            if value.startswith("${"):
                value_new = value[2:-1]
                value_new = eval(value_new)
                key_n.append(key)
                value_n.append(value_new)

        dict_n = dict(zip(key_n, value_n))
        self.get_test_data_be_replaced = dict(self.dataMap, **dict_n)
        # print(self.get_test_data_be_replaced)
        return self.get_test_data_be_replaced




    def caseinfo(self) -> list:  # //return caseinfo []

        caseInfoData = list()
        xlxsObject = self.pe.load_work_book(self.test_data_path).get_sheet_by_name(self.test_data_sheet)
        caseid = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=1))  # 案例编号
        caseName = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=2))  # 名称
        casenu = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=3))  # 案例名称
        casetype = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=7))  # 预期结果
        caserr = (self.pe.get_cell_of_value(xlxsObject, rowNo=self.execline, colsNo=9))  # 正反例
        caseInfoData.insert(0, caseid)
        caseInfoData.insert(1, caseName)
        caseInfoData.insert(3, casenu)
        caseInfoData.insert(4, casetype)
        caseInfoData.insert(5, caserr)

        return caseInfoData



    def getvmfile(self, data):
        # get vm+ casedata

        xlxsObject = self.pe.load_work_book(self.test_data_path).get_sheet_by_name(self.test_data_sheet)
        vmname = (self.pe.get_cell_of_value(xlxsObject, rowNo=2, colsNo=3))  # vm-tem-name
        templetepath = os.path.abspath('..') + '/autodata/template/' + vmname
        # print(templetepath)
        caseTepletedata = Template(getdata4file.connect_to(templetepath).parsed_data)
        caseDAta = json.loads(caseTepletedata.render(data))

        # print(caseDAta)
        return caseDAta

    def casealldata(self):


        if len(self.publicdata) == 0:
            self.data4rows(self.execflowname, 4, 5)
            self.publicdata = self.get_test_data_replace()
        # print(self.publicdata)

        self.data4rows(self.execflowname, 8, self.execline)
        self.casedata = self.handle_case_test_data()
        # print(self.casedata)

        self.casekeymap = dict(self.publicdata, **self.casedata)
        # print(localdata(self.casekeymap))
        # print(self.casekeymap)

        self.__casedata.append(self.getvmfile(self.casekeymap))
        self.__casedata += self.caseinfo()

        return self.__casedata


# if __name__ == '__main__':
#     flowname = "冰鉴"
#     xlxsfp = "冰鉴接口案例.xlsx"
#     exeshtname = "冰鉴对外投资"
#     execline = 10
#     testfile = CaseDataMap4Xls(flowname, xlxsfp, exeshtname,execline).casealldata()
#     print(testfile)
