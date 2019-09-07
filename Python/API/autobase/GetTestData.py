from autobase.parseexcel import *
from autobase.utils import *
# from CommonRules.IdNmuber import *
# from CommonRules.Birthday import *
# from CommonRules.Name import *
from string import Template
# from config.read_excel_conf_ini import *
import json
from openpyxl import load_workbook

d = {'serialNo': 'P9dvI', 'product_id': '6', 'amount': '30000', 'premium': '30', 'company': '希望金融下邳分公司', 'name': 'AaLP', 'certi_no': 1231234324, 'employment': '00205001', 'phone': '${localproduct_id', 'profitpersonList_name': '新希望慧农(天津)科技有限公司', 'profitpersonList_certi_type': '3', 'profitpersonList_certi_no': '911201163286974380'}



def localdata(dictey): #// 给local里面的赋值
    for key, val in dictey.items():
        if isinstance(val, str) and val.startswith("${local"): dictey[key] = dictey[val[7:]]
    return dictey


def local(key): # //返回一个ico给localdata
    return "${local"+key


class CaseDataMap4Xls(object):



    def __init__(self, xlxspath, xlsxsheet):
        # //  etst
        self.test_data_path = xlxspath
        self.test_data_sheet = xlsxsheet
        self.pe = ParseExcel()
        self.pe.load_work_book(self.test_data_path)

    def data4rows(self, flowaction, start_line, end_line):  # two line data []-> {}
        '''
        1、调两次方法
        2、第一次取第2行、第3行，dict(zip(,))
        3、第二次取第6行、第n行(n是执行行)，dict(zip(,))
        4、两次调用都是带有表达式的
        '''
        # 生成sheet对象，取任意两行的数据对象
        sheet = self.pe.get_sheet_by_name(self.test_data_sheet)
        _key  = self.pe.get_row(sheet, start_line)
        _value = self.pe.get_row(sheet, end_line)


        key = list()
        for x in _key:# key
            x = x.value
            key.append(x)
        value = list()# val
        for y in _value:
            y = y.value
            value.append(y)


        # // 数据是由<data-in-$$>进行了分段，分段截取对应场景交易的数据，组成dict

        startdataico = "<data-in-name=\""  + flowaction + "\">"
        enddataico   = "<data-out-name=\"" + flowaction + "\">"

        key_len = len(key)
        start_index = 0
        end_index   = 0
        for i in range(key_len):
            if key[i] == startdataico:
                start_index = key.index(key[i]) + 1
                for i in range(start_index, key_len):
                    print(key[i])
                    if key[i] == enddataico:
                        end_index = key.index(key[i])
                        break
        key   = key[start_index:end_index]
        value = value[start_index:end_index]

        self.dataMap = dict(zip(key, value))

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
            print(value)
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
            print(value)
            value = str(value)
            if value.startswith("${"):
                value_new = value[2:-1]
                # print(value_new)
                value_new = eval(value_new)
                key_m.append(key)
                value_m.append(value_new)

        dict_m = dict(zip(key_m, value_m))
        self.casedata = dict(self.dict_n, **dict_m)
        # print(localdata(self.case_test_data))
        # self.case_test_data.update(localdata(self.case_test_data))
        print(self.casedata)
        return self.casedata

    def get_test_data_replace(self):
        '''
        1、替换源数据self.test_data中value为${}的表达式
        2、查找value为${}的表达式，脱去${},再用eval()执行
        :return:
        '''
        key_n   = list()
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
        print(self.get_test_data_be_replaced)
        return self.get_test_data_be_replaced



    def be_executed_test_data(self, transaction, line):

        self.data4rows(transaction, 4, 5)
        self.publicdata = self.get_test_data_replace()
        print(self.publicdata)

        self.data4rows(transaction, 8, 10)
        self.casedata = self.handle_case_test_data()
        print(self.casedata)

        self.real_case_test_data = dict(self.publicdata, **self.casedata)
        print(localdata(self.real_case_test_data))
        # print(self.real_case_test_data)
        return self.real_case_test_data

if __name__ == '__main__':
    test_data_path = r"D:\ApiTestFrame\autodata\testcase\冰鉴接口案例.xlsx"
    test_data_sheet = "冰鉴对外投资"
    CaseDataMap4Xls(test_data_path, test_data_sheet).be_executed_test_data("冰鉴", 7)




