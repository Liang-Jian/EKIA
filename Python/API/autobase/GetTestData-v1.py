from autobase.parseexcel import *
# from testScripts_low_interface.conf import *
# from CommonRules.IdNmuber import *
# from CommonRules.Name import *
from string import Template
import json




class GetTestData():

    def __init__(self):
        '''
        test_data_path数据表路径需要配置
        并且要导入对应的模块路径
        '''
        self.pe = ParseExcel()
        self.pe.load_work_book("/home/robot/ApiTestFrame/autodata/testcase/小渠道一步希望.xlsx")

    def get_test_data(self, action, start_line, end_line):
        # 生成sheet对象，取任意两行的数据对象
        sheet = self.pe.get_sheet_by_name("核保出单")
        _key  = self.pe.get_row(sheet, start_line)
        _value = self.pe.get_row(sheet, end_line)

        # 其中一行数据，定为dict的key
        key = []
        for x in _key:
            x = x.value
            key.append(x)

        # 其中一行数据，定为dict的value
        value = []
        for y in _value:
            y = y.value
            value.append(y)

        '''
        数据是由$进行了分段，分段截取对应场景交易的数据，组装成dict
        '''
        # str = "$" + action
        # key_len = len(key)
        # start_index = 0
        # end_index = 0
        # for i in range(key_len):
        #     if key[i] == str:
        #         start_index = key.index(key[i]) + 1
        #         for i in range(start_index, key_len):
        #             if key[i][:1] == "$":
        #                 end_index = key.index(key[i])
        #                 break
        # key = key[start_index:end_index]
        # value = value[start_index:end_index]
        # print(value)

        # try:
        #     for i in range(len(value)):
        #         if value[i].startswith("${"):
        #             value_new = value[i][2:-1]
        #             value[i] = eval(value_new)
        # except:
        #     pass

        self.test_data = dict(zip(key, value))
        print(self.test_data)

        '''
        单个案例的测试数据只填写了，与测试意图相关的数据字段，  其他的未填写，这部分做了value的去空处理
        '''
        _key = []
        _value = []
        for value in self.test_data.values():
            if value != None:
                key = list(self.test_data.keys())[list(self.test_data.values()).index(value)]
                _key.append(key)
                _value.append(value)

        '''
        1、excel中表达式赋值${id_card_mum('2015-01-01')}
        2、_value为列表，循环找到"${"开头的位置，然后做字符串前后截取[2:-1]
        3、截取后为id_card_mum('2015-01-01')，调用eval()
        4、将eval()值，进行原地赋值，生成新的列表
        5、eval()内可以调用任意个函数
        '''
        for i in range(len(_value)):
            if _value[i].startswith("${"):
                _value_new = _value[i][2:-1]
                _value[i] = eval(_value_new)

        self.source_data = dict(zip(_key,_value))
        print(self.source_data)
        return self.source_data


    def be_executed_test_data(self,line):
        self.get_test_data("randomStr",4,5)
        initial_data = self.test_data

        test_data = self.get_test_data("hebao", 6,line)

        self.executed_test_data = dict(initial_data, **test_data)

        self.executed_test_data = json.dumps(self.executed_test_data)
        self.executed_test_data = self.executed_test_data.replace("<null>", "")
        self.executed_test_data = json.loads(self.executed_test_data)

        print(self.executed_test_data)
        return  self.executed_test_data



def randomStr(randomlength):
    import random,string
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = "".join(str_list)
    return random_str


if __name__ == '__main__':
    d = GetTestData()

    d.be_executed_test_data(7)



