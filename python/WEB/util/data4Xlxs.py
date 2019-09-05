from util.ParseExcel import *
from CommonRules.IdNmuber import *
from CommonRules.Birthday import *
from CommonRules.Name import *
from string import Template
from config.read_excel_conf_ini import *
import json


class GetTestData():

    startDate = read_excel_conf_ini("保险师百万重大疾病疾保险续保需求(T20180808305)" ,"startDate")
    # print(startDate)


    def __init__(self,test_data_path, test_data_sheet):
        '''
        test_data_path数据表路径需要配置
        并且要导入对应的模块路径
        '''
        self.test_data_path = test_data_path
        self.test_data_sheet = test_data_sheet
        self.pe = ParseExcel()
        self.pe.load_work_book(self.test_data_path)

    def get_test_data(self, action, start_line, end_line):
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

        # 其中一行数据，设为dict的key
        key = []
        for x in _key:
            x = x.value
            key.append(x)

        # 其中一行数据，设为dict的value
        value = []
        for y in _value:
            y = y.value
            value.append(y)

        '''
        数据是由$进行了分段，分段截取对应场景交易的数据，组成dict
        '''
        str = "$" + action
        key_len = len(key)
        start_index = 0
        end_index = 0
        for i in range(key_len):
            if key[i] == str:
                start_index = key.index(key[i]) + 1
                for i in range(start_index, key_len):
                    if key[i][:1] == "$":
                        end_index = key.index(key[i])
                        break
        key = key[start_index:end_index]
        value = value[start_index:end_index]

        self.test_data = dict(zip(key, value))

    def handle_case_test_data(self):
        '''
        1、处理案例测试数据，去除value值为None空，以便与源数据进行数据合并
        2、step1:将获取到的案例数据做替换，把“${null}”，替换成“”，意思是赋值对应的字段空值，然后重组dict
        3、step2:重组后的dict做，表达式赋值“${}”，查找value为${}的表达式，脱去${},再用eval()执行
        :return:
        '''
        key_n = []
        value_n = []
        for key, value in self.test_data.items():
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
            # if value.startswith("${"):
                value_new = value[2:-1]
                # print(value_new)
                value_new = eval(value_new)
                key_m.append(key)
                value_m.append(value_new)
        dict_m = dict(zip(key_m, value_m))
        self.case_test_data = dict(self.dict_n, **dict_m)
        return self.case_test_data

    def get_test_data_replace(self):
        '''
        1、替换源数据self.test_data中value为${}的表达式
        2、查找value为${}的表达式，脱去${},再用eval()执行
        :return:
        '''
        key_n = []
        value_n = []
        for key, value in self.test_data.items():
            # print(value)
            if value.startswith("${"):
                value_new = value[2:-1]
                value_new = eval(value_new)
                key_n.append(key)
                value_n.append(value_new)
        dict_n = dict(zip(key_n, value_n))
        self.get_test_data_be_replaced = dict(self.test_data, **dict_n)
        return self.get_test_data_be_replaced



    def be_executed_test_data(self, transaction, line):

        self.get_test_data(transaction, 2, 3)
        self.raw_test_data = self.get_test_data_replace()
        # print(self.raw_test_data)

        self.get_test_data(transaction, 6, line)
        self.case_test_data = self.handle_case_test_data()
        # print(self.case_test_data)

        self.real_case_test_data = dict(self.raw_test_data, **self.case_test_data)
        print(self.real_case_test_data)
        return self.real_case_test_data

if __name__ == '__main__':
    # test_data_path = read_excel_conf_ini("华创明德住院保综合险(T20180717194)" ,"test_data_path")
    # print(test_data_path)
    # test_data_sheet = read_excel_conf_ini("华创明德住院保综合险(T20180717194)" ,"test_data_sheet")
    test_data_path = "E:/TK/AutomatedTestingFramework/ProjectUI/Examples/test_data/保险师百万重大疾病疾保险续保需求(T20180808305).xlsx"
    test_data_sheet = "test_data"
    d = GetTestData(test_data_path, test_data_sheet)

    d.be_executed_test_data("hebao", 7)






