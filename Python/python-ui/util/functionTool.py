import re
import time
import os
import win32api
import time,configparser
from selenium import webdriver
from abc import ABCMeta
import random

import win32con,sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui  import Select
import PIL
import xlrd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xlutils.copy import copy
import inspect
from interface.interfaceDriver import DriVer
from .logger import *
from util.driver import StartDriver


'''
create by joker
datetime: 2018/4/12

'''
#####public Data#####

URL_HX    = "http://10.130.201.229:7011/index.jsp"
URL_PRE   = "https://pycmspre.lexue.com/login"
uat_URL   = "http://10.130.206.54/index.jsp"
URL_YSC   = "http://10.130.206.54/index.jsp"
TBUN      = "00000088@upic.com"               #投保用户名
HEUN      = "hebao1@upic"                     #核保用户名
HEUN5     = "hebao5@upic"                     #核保用户名
LPUN      = "payment@upic.com"                #收付用户
PW        = "upic@312"                        #密码
uat_PW    = "upic@123"                        #密码

HXTB      = "manager@upic"
ADDRESS   = "北京"
POSTCODE  = "047501"
TEL       = "13901234567"
SKNAME    = "汉尼拔"                           #收款人
bankname  = "中国银行"                         #收款银行
CARICON   = "凯迪拉克"
TIME_OUT  = 24

#######################
##oracle##

ORCLE_URL= "upiccore/sinosoft@10.130.201.118:1521/tkpi"


#######
VK_CODE = {
    'c': 0x43,
    'ctrl': 0x11,
    'win': 91,
    'm': 0x4D,
    'tab':0x09,
    'alt':0x12,
    'f4':0x73,
    'enter':0x0D
}


def getnumber(data,path="E:\\TK\\pythoncode\\report.txt"):
    with open(path,"a+") as f:
        f.write(data)
    f.close()

def nowdate():
    return time.strftime('%Y-%m-%d')

def nowtime():
    return time.strftime('%H-%M-%S')

def getfunname():
    return inspect.stack()[1][3]

def takeScreenshot(): # jietu function
    from PIL import ImageGrab
    win32api.keybd_event(44,win32api.MapVirtualKey(44,0),0,0)
    time.sleep(1)
    win32api.keybd_event(44, win32api.MapVirtualKey(44, 0), win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    im = ImageGrab.grabclipboard()
    im.save("D:\\a.png")
# takeScreenshot()

def PicFilePath(name):

    # fp = os.getcwd() + "\\" + name
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        print("截图文件夹已经存在")

def w2file(filename,data):
    if not os.path.exists(filename):
        print("文件已经存在，确保没有重要数据")
    f = open(filename,"w")
    f.writelines(data)
    f.close()

def getdata4f(filename):
    file_data =""
    f = open(filename,"r",encoding="utf-8")
    file_data = f.read()
    print(file_data)
    return file_data

def killie2():
    try:
        os.system('taskkill /F /im iexplore.exe')
        os.system('taskkill /F /im IEDriverServer.exe')
    finally:
        pass

def getDataFromSheet(excelPath=os.path.realpath("..") + "\\datapool\\" + '\\身份证.xls', sheetName="Sheet1"):
    dataList = []
    data = xlrd.open_workbook(excelPath) # 读取excel数据
    table = data.sheet_by_name(sheetName) # 获取一个工作表
    nrows = table.nrows # 获取工作表的总行数
    for line in range(nrows):
        rowData = table.row_values(line)
        if rowData[3] == "":
            dataList.append(rowData)
            wb = copy(data)
            ws = wb.get_sheet(0)
            ws.write(line, 3, "1")
            ws.write(line, 4, time.ctime())
            wb.save(excelPath)
            break
    if len(dataList) == 0:
        print("数据读取完毕")
    else:
        indentityId = dataList[0][0]
        name = dataList[0][1]
        sex = dataList[0][2]
        return indentityId, name, sex


def two_key(keyName1, keyName2):
    win32api.keybd_event(VK_CODE[keyName1], 0, 0, 0)
    win32api.keybd_event(VK_CODE[keyName2], 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(VK_CODE[keyName1], 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(VK_CODE[keyName2], 0, win32con.KEYEVENTF_KEYUP, 0)

def one_key(keyName1):
    win32api.keybd_event(VK_CODE[keyName1], 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(VK_CODE[keyName1], 0, win32con.KEYEVENTF_KEYUP, 0)




lianxiren = getDataFromSheet()
TBNAME    = lianxiren[1]
ID        = lianxiren[0]
sex       = lianxiren[2]
birday    = lianxiren[0][6:14]
chejiahao = "LSGPC52U7AF1" + ID[-5::]
carnb     = "京A" + ID[-5::]
engnb     = ID[-7::]


class SelenFun(StartDriver):
    def __init__(self):
        super(SelenFun, self).__init__()

    def swich2frame(self,type,attribute):
        if   type == "id":
            WebDriverWait(self.driver, TIME_OUT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, attribute)))
        elif type == "name":
            WebDriverWait(self.driver, TIME_OUT).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, attribute)))
        elif type == "css":
            WebDriverWait(self.driver, TIME_OUT).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, attribute)))
        else:
            raise("没有该属性")

    def alert_acc(self):

        for i in range(5):
            try:
                WebDriverWait(self.driver, 9).until(EC.alert_is_present()).accept()
                time.sleep(0.5)
            except:
                break

    def clickByCss(self, css):

        WebDriverWait(self.driver, TIME_OUT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css))).click()

    def sendByCss(self, css, value):
        ele =  WebDriverWait(self.driver, TIME_OUT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
        ele.send_keys(value)
        Logi("{} element={} value={} success".format(sys._getframe().f_code.co_name,css,value))

    def clickByCsss(self, css, index):
        ele = WebDriverWait(self.driver, TIME_OUT).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, css)))
        ele[index].click()
        Logi("{} element={} index={} success".format(sys._getframe().f_code.co_name,css,index))

    def send_by_csss(self, css, index, value):
        ele =  WebDriverWait(self.driver, TIME_OUT).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, css)))
        ele[index].send_keys(value)

    def send_by_names(self, names, content, index=0):#通过js填写内容
        time.sleep(0.2)
        js = 'var q=document.getElementsByName("%s");q[%d].value ="%s"' % (names, index, content)
        self.driver.execute_script(js)

    def click_by_names(self, names, index=0):#通过js填写内容
        time.sleep(0.5)
        js = 'var q=document.getElementsByName("%s");q[%d].click()' % (names, index)
        self.driver.execute_script(js)

    def usejs(self,js,*args):
        self.driver.execute_script(js)

    def _isExist(self, css_element):
        try:
            self.driver.find_element_by_css_selector(css_element)
            return True
        except:
            return False

    def keyud(self,keyName):
        win32api.keybd_event(keyName, 0, 0, 0)
        time.sleep(0.5)
        win32api.keybd_event(keyName, 0, win32con.KEYEVENTF_KEYUP, 0)

    def isWintwo(self):
        n = 0
        while n < 120:
            time.sleep(0.5)
            n += 1
            if len(self.driver.window_handles) != 1: break

    def isWinone(self):
        startN = 0
        while startN < 120:
            time.sleep(0.5)
            if len(self.driver.window_handles) < 2:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                break

    def isExist(self,css):
        startN = 0
        while startN < 15:
            time.sleep(1)
            startN += 1
            if self._isExist(css) is True:
                return True
        else:
            return False


    def clickAttr(self, tag, attribute, attributevalue):
        self.driver.execute_script("function sct(){ \
            var t_ele = document.getElementsByTagName(\"" + tag +"\"); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute(\"" + attribute +"\")==\"" + attributevalue + "\"){ \
                    t_ele[i].click(); \
                } \
            } \
        };sct();")


    def clickClassIndex(self, ele, index):

        _js = '''function joker(){ \
                    var ele = document.getElementsByClassName('%s'); \
                    ele[%d].click(); \
                };joker();''' % (ele, index)

        self.driver.execute_script(_js)
        Logi("{} element={} index={} success".format(sys._getframe().f_code.co_name,ele,index))
    def send_by_attr(self,tag, attribute, attributevalue,newattr,newvalue):
        self.driver.execute_script("function sct(){ \
            var t_ele = document.getElementsByTagName(\"" + tag +"\"); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute(\"" + attribute +"\")==\"" + attributevalue + "\"){ \
                    t_ele[i].setAttribute(\""+newattr+"\",\""+newvalue+"\"); \
                } \
            } \
        };sct();")



    def _click_by_attr(self, tag, attribute, attributevalue):
        self.driver.execute_script("function sct(){ \
            var t_ele = document.getElementsByTagName(\"" + tag +"\"); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute(\"" + attribute +"\").indexOf(\"" + attributevalue +"\")) !=-1){ \
                    t_ele[i].click(); \
                } \
            } \
        };sct();")


    def ClickByMuiWord(self, ele, p_ele):
        """
        :param ele: mui object or css element
        :param p_ele: page element string
        :return:  None create by ShiChengTao  action ""  ''
        """
        if self.isExist(ele) is not True : raise (f"{ele}  not Found, please check")
        _js = '''function joker(){ \
                    var ele_list = mui('%s'); \
                    for (var i=0;i<ele_list.length;i++){ \
                          if (q[i].innerText == '%s'){ \
        		            q[i].addEventListener('tap',function(){}); \
        		            mui.trigger(q[i],'tap');\
        	            } \
                    } \
                };joker();''' % (ele, p_ele)
        self.driver.execute_script(_js)


    def ClickByInWord(self, ele, p_ele):
        """
        :param ele: mui object or css element
        :param p_ele: page element string, regex match word
        :return:  None create by ShiChengTao
        """
        if self.isExist(ele) is not True : raise (f"{ele}  not Found, please check")
        _js = '''function joker(){ \
                    var ele_list = mui('%s'); \
                    for (var i=0;i<ele_list.length;i++){ \
                          if (q[i].innerText.indexOf('%s') != -1){ \
        		            q[i].addEventListener('tap',function(){}); \
        		            mui.trigger(q[i],'tap');\
        	            } \
                    } \
                };joker();''' % (ele, p_ele)
        self.driver.execute_script(_js)

    def scrollto(self,css):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element_by_css_selector(css))

    def _maxWin(self):
        self.usejs("document.getElementsByTagName(\"body\")[0].style.zoom=0.5")
        time.sleep(0.5)
        self.usejs("document.getElementsByTagName(\"body\")[0].style.zoom=1")

    def _sendbyvalue(self,tag,attribute,):
        pass


    def clickByWord(self, word,ele='span'):
        """
        :param word:  页面显示的字
        :param ele:   标签
        :return: None
        """
        if self.isExist(ele) is not True :
            Logi("f{ele} Not Found".format(ele))
            raise (f"{ele}  Not Found, Pls check")  #  返回的都是T ，需要fix

        _js = '''function joker(){ \
                    var ele = document.getElementsByTagName('%s'); \
                    for (var i=0;i<ele.length; i++){ \
                        if (ele[i].innerText == '%s'){ \
        		            ele[i].click(); \
        	            } \
                    } \
                };joker();''' % (ele,word)
        self.driver.execute_script(_js)
        Logi("{} {} success".format(sys._getframe().f_code.co_name,word))

    def sleep(self, second=2):
        time.sleep(second)
        Logi("{} {} success".format(sys._getframe().f_code.co_name,second)) # sys._getframe().f_code.co_name 当前函数名



