
from util.functionTool import *


'''


乐学教育CMS UI自动化框架

create by : joker shi
date : 2020/10/14

'''


class LeXue(SelenFun):
    # def __init__(self): pass

    def jichudangan(self): #  基础档案

        self.driver.get(URL_PRE)
        self.sendByCss("[placeholder=\"用户名\"]","15921769547")
        self.sendByCss("[placeholder=\"密码\"]","123456")
        self.clickByWord("登录")
        self.clickByWord("基础档案")
        self.clickByWord("学校档案")
        self.sleep()                                                    # 刷新的时候需要强制等待
        self.clickByCsss(".el-cascader__label",0)
        self.clickByWord("西北")
        self.clickByWord("新疆维吾尔自治区")
        self.clickByWord("伊犁哈萨克自治州")
        self.clickByCss("[placeholder=\"请选择学校\"]")
        self.clickByWord("清水二中测试")
        self.clickByWord("查询")
        self.clickByWord("重置")
        self.clickByWord("添加")
        self.sleep()
        self.clickClassIndex("el-cascader__label",1)
        self.clickByWord("华北")
        self.clickByWord("山西省")
        self.clickByWord("太原市")
        self.sendByCss("[maxlength=\"20\"]","乐学自动化UI")
        self.clickByCss("[placeholder=\"分校等级\"]")
        self.clickByWord("T1")
        self.clickByWord("取 消")
        # self.clickByWord("保存 & 设置参数")




        self.scrollto("[name='registReportorName']")

        self.swich2frame("name","mainFrame")
        self.isExist(".tishi")
        baohao_text = re.findall("\d+",self.driver.find_element_by_css_selector(".tishi > tbody > tr:nth-child(3) > td").text)
        if baohao_text !=[]: self.result_txt["报案号"] = baohao_text[0]
        print("报案新增", self.baoan.__name__  + "\t" +  self.result_txt.get("报案号"))
        # self.click_by_css("input[name='buttonSurveyDelegate']")


    def run(self):
        self.jichudangan()


