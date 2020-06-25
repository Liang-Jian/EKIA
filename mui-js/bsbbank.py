# -* - coding :utf-8 -*-
##** caseId = {caseId}
##** expectedResult = {expectedResult2}
##** intent = {intent2}
##** imagePath = {MainDir}/result/image/{track}/{caseId}
path = "{MainDir}"

# procedure=

import os, platform, sys, logging, threading, subprocess, pickle
# import win32api,win32con,win32gui
from appium.webdriver.mobilecommand import MobileCommand

sep = os.path.sep  # \

import pickle, requests
from appium import webdriver
import time, os
from abc import abstractstaticmethod

# open(path + "/processLog.txt","w")
# loggerfile = logging.getLogger("bsb")
# loggerfile.setLevel(logging.INFO)
#
# fh = logging.FileHandler(path + "/processLog.txt")
# fmt =logging.Formatter("%(message)s")
# fh.setFormatter(fmt)
# loggerfile.addHandler(fh)
# desired_caps['deviceName'] = 'JRDEGIRCMNFUHIHY'
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


class AndroidTest(object):
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '9'  # 手机系统版本
        desired_caps['deviceName'] = 'QV7129M024'  # 刚才的devicename
        desired_caps['appPackage'] = 'com.google.android.calculator'  # 计算器的package
        desired_caps['appActivity'] = 'com.android.calculator2.Calculator'  # 计算器的activity
        desired_caps['noReset'] = 'true'  # 计算器的activity
        desired_caps['fullrReset'] = 'false'  # 计算器的activity
        desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}  # 计算器的activity
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)  # start desired_caps

    def touchtap(self, x, y, duration=500):  # 点击坐标  ,x1,x2,y1,y2,duration
        '''
        method explain:点击坐标
        parameter explain：【x,y】坐标值,【duration】:给的值决定了点击的速度
        Usage:
            device.touch_coordinate(277,431)      #277.431为点击某个元素的x与y值
        '''
        screen_width = self.driver.get_window_size()['width']  # 获取当前屏幕的宽
        screen_height = self.driver.get_window_size()['height']  # 获取当前屏幕的高
        a = (float(x) / screen_width) * screen_width
        x1 = int(a)
        b = (float(y) / screen_height) * screen_height
        y1 = int(b)
        self.driver.tap([(x1, y1), (x1, y1)], duration)

    def ClickTextA(self, String):
        self.driver.find_element_by_android_uiautomator('text("' + String + '")').click()
        time.sleep(2)

    def ClickIfExist(self, by, value):
        try:
            if (by == "id"):
                WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.ID, value))).click()
            elif (by == "name"):
                WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.NAME, value))).click()
            elif (by == "xpath"):
                WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.XPATH, value))).click()
            # elif(by=="className"):
            # elif(by=="aut"):

        except Exception:
            pass

    # zuobiao
    def ClickToJS(self, x, y):
        # 通过JS使用作用坐标进行点击
        self.driver.execute_script("mobile:tap", {"tapCount": 1, "touchCount": 1, "duration": 0.5, "x": x, "y": y})

    def touchTapA(self, x, y):
        #
        _CMD = "adb shell input tap {} {}".format(x, y)
        os.popen(_CMD)
        time.sleep(0.5)

    def touch(self):
        time.sleep(3)
        print("connect successfullly")
        self.driver.find_element_by_android_uiautomator('text("订阅号")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("wxid_i2ugr5cpmk4721的接...")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("我")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("绑卡")').click()
        time.sleep(2)
        self.touchTapA(437, 1528)  # click app in link's point
        contexts = self.driver.contexts  # print h2 file
        print(contexts)
        # 切换进webview视图
        view_context = 'WEBVIEW_com.tencent.mm:tools'  # view_context的值由contexts的打印中获取
        self.driver.switch_to.context(view_context)
        time.sleep(2)
        self.driver.find_element_by_css_selector("#signaccount").send_keys("1234")  # account
        time.sleep(2)
        self.driver.find_element_by_css_selector("#signPhone").send_keys("13613552859")  # phone
        time.sleep(2)
        self.driver.find_element_by_css_selector("#actionCode").send_keys("112233")  # actity code
        time.sleep(3)
        self.driver.find_element_by_css_selector("#nextBtn").click()  # hide keyword
        time.sleep(2)
        self.touchTapA(544, 1555)  # click next need change

    def quit(self):
        self.driver.quit()

    def getMsg(self, requestIP, userName, passwd, tel):
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP + "/msg/msgSendInfoQuery.action"
        print(login_url)
        search_data = {
            "messageSend.taskID": "",
            "messageSend.tellerID": "",
            "messageSend.address": tel,
            "messageSend.appId": "",
            "messageSend.checkState": "",
            "messageSend.transBranch": "",
            "messageSend.msgClassID": "",
            "messageSend.payBranch": ""
        }
        session = requests.Session()
        login_resp = session.post(url=login_url, data=login_data)
        resp = session.post(url=search_url, data=search_data)
        html = resp.text
        print(html)
        print("获取页面")
        # m = html.index("短信验证密码：")
        m = html.index("您本次签约绑定账号短信验证码:")
        print(m)
        print("交易成功")
        # code = html[m+7:m+13]
        code = html[m + 15:m + 21]
        return code

    def ClickByValue(self, value):
        '''
        根据text点击
        '''
        # print("//*[text()='"+text+"']")
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@value,'" + value + "')]"))).click()

    def getMsg_addCard(self, requestIP, userName, passwd, tel):
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP + "/msg/msgSendInfoQuery.action"
        print(login_url)
        search_data = {
            "messageSend.taskID": "",
            "messageSend.tellerID": "",
            "messageSend.address": tel,
            "messageSend.appId": "",
            "messageSend.checkState": "",
            "messageSend.transBranch": "",
            "messageSend.msgClassID": "",
            "messageSend.payBranch": ""
        }
        session = requests.Session()
        login_resp = session.post(url=login_url, data=login_data)
        resp = session.post(url=search_url, data=search_data)
        html = resp.text
        m = html.index("您本次用于礼品兑换的bs银行短信验证码:")
        code = html[m + 20:m + 26]
        return code

    def getMsg1(self, requestIP, userName, passwd, tel):
        # 绑卡的短信验证码
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP + "/msg/msgSendInfoQuery.action"
        print(login_url)
        search_data = {
            "messageSend.taskID": "",
            "messageSend.tellerID": "",
            "messageSend.address": tel,
            "messageSend.appId": "",
            "messageSend.checkState": "",
            "messageSend.transBranch": "",
            "messageSend.msgClassID": "",
            "messageSend.payBranch": ""
        }
        session = requests.Session()
        login_resp = session.post(url=login_url, data=login_data)
        resp = session.post(url=search_url, data=search_data)
        html = resp.text
        print(html)
        m = html.index("您本次签约绑定账号短信验证码:")
        print(m)
        code = html[m + 15:m + 21]
        print(code)
        return code

    def login(self):
        time.sleep(5)
        print("connect successfullly")
        # 进入订阅号
        self.driver.find_element_by_android_uiautomator('text("订阅号消息")').click()
        time.sleep(2)
        # self.driver.find_element_by_android_uiautomator('text("订阅号")').click()
        self.driver.find_element_by_xpath("//android.widget.ImageButton[@content-desc=\"订阅号\"]").click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("wxid_i2ugr5cpmk4721的接…")').click()
        time.sleep(2)
        print("进入接口管理")

    def Clickkw(self, String):
        for i in String:
            print(i)
            self.driver.execute_script('$("a[data-val={}]").click()'.format(int(i)))
            time.sleep(0.5)

    def ClickByXpath_tap(self, xpath):
        ele = self.driver.find_element_by_xpath(xpath)
        # print(ele.text)
        xOne = ele.location['x']
        yOne = ele.location['y']
        widOne = ele.size['width']
        heiOne = ele.size['height']
        x = xOne + widOne * 0.5
        y = yOne + heiOne * 0.5
        print("x: {} , y:{}".format(3 * x, 3 * y))
        self.touchTapA(3 * x, (3 * y + 198))
        time.sleep(3)

    def ClickById_tap(self, ID):
        ele = self.driver.find_element_by_id(ID)
        # print(ele.text)
        xOne = ele.location['x']
        yOne = ele.location['y']
        widOne = ele.size['width']
        heiOne = ele.size['height']
        print("output ...")
        print(xOne)
        print(yOne)
        print(widOne)
        print(heiOne)
        print("finish")
        # 1080 1920  360 574
        x = xOne + widOne * 0.5
        y = yOne + heiOne * 0.5
        print("x: {} , y:{}".format(3 * x, 3 * y))
        self.touchTapA(3 * x, (3 * y + 198))
        time.sleep(3)


    def muiJs(self,js):
        _cmd = """
        var q =document.getElementsByTagName('li');
            q[3].addEventListener("tap",function () {});
            mui.trigger(q[3],'tap');
        """
        self.driver.execute_script(_cmd)
class Produce(AndroidTest):
    def bsbank(self):
        pass


    def baoshang_yuntingtang(self):
        self.login()
        self.driver.find_element_by_android_uiautomator('text("bs")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("云厅堂")').click()
        time.sleep(10)
        contexts = self.driver.contexts  # print h2 file
        print(contexts)
        self.driver.switch_to.context(contexts[-1])
        # self.driver.find_element_by_css_selector("#wxdgBtn").click()
        self.driver.execute_script('$("#wxdgBtn").click()')

        time.sleep(3)
        # self.driver.find_element_by_css_selector("#phoneNum").send_keys("13333333333")
        self.driver.execute_script('$("#phoneNum").val("13333333333")')
        # self.driver.find_element_by_css_selector("#phoneNum").send_keys("13333333333")
        time.sleep(3)
        self.driver.find_element_by_css_selector("#inputCode").send_keys("test")
        time.sleep(2)
        self.driver.find_element_by_css_selector("#vcode").send_keys("23452")
        time.sleep(2)
        self.driver.find_element_by_css_selector("#loginBtn").click()
        time.sleep(2)

    def baoshang_erleihukaihu(self):
        self.login()
        self.driver.find_element_by_android_uiautomator('text("bs")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("二类户开户")').click()
        time.sleep(2)
        self.touchTapA(390, 1560)
        time.sleep(10)
        contexts = self.driver.contexts  # print h2 file
        print(contexts)
        self.driver.switch_to.context(contexts[-1])
        time.sleep(2)
        self.driver.find_element_by_css_selector("#PID1").click()  # upload front IDcard
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("拍摄照片")').click()  # click take photo
        time.sleep(2)
        self.driver.find_element_by_css_selector("#PID2").click()  # upload front IDcard
        time.sleep(2)

        # self.driver.find_element_by_css_selector("#wxdgBtn").click()
        # time.sleep(3)
        # self.driver.find_element_by_css_selector("#phoneNum").send_keys("13333333333")
        # time.sleep(3)
        # self.driver.find_element_by_css_selector("#inputCode").send_keys("test")
        # time.sleep(2)
        # self.driver.find_element_by_css_selector("#vcode").send_keys("23452")
        # time.sleep(2)
        # self.driver.find_element_by_css_selector("#loginBtn").click()
        # time.sleep(2)

    def wo_bangka(self):  # 绑卡
        self.login()
        self.driver.find_element_by_android_uiautomator('text("我")').click()
        time.sleep(2)
        self.driver.find_element_by_android_uiautomator('text("绑卡")').click()
        time.sleep(2)
        self.touchTapA(544, 1555)
        time.sleep(8)
        contexts = self.driver.contexts  # print h2 file
        print(contexts)
        view_context = 'WEBVIEW_com.tencent.mm:tools'  # view_context的值由contexts的打印中获取
        self.driver.switch_to.context(view_context)
        time.sleep(2)
        ps = self.driver.page_source
        print(ps)
        # self.driver.find_element_by_css_selector("#signaccount").send_keys("62176056080280597")      # account
        self.driver.find_element_by_css_selector("#signaccount").send_keys("62176056080280597")  # account
        time.sleep(2)
        self.driver.find_element_by_css_selector("#signPhone").send_keys("15800010003")  # phone
        time.sleep(2)
        self.driver.find_element_by_css_selector("#actionCode").send_keys("112233")  # actity code
        time.sleep(3)
        self.driver.find_element_by_css_selector("#nextBtn").click()
        a = self.get_sm_vcode("14.16.10.36:7001", "qdcs01", "bsb@12345", "15800010003")
        time.sleep(3)
        # self.driver.find_element_by_css_selector("#inputCode").send_keys("test")
        # self.driver.execute_script('$("#inputCode").val("test")')
        time.sleep(2)
        self.driver.find_element_by_css_selector("#vcode").send_keys("a")
        time.sleep(2)
        self.driver.find_element_by_css_selector("#loginBtn").click()
        # self.touchTapA(437, 1528)                                                     # click app in link's point
        # 切换进webview视图
        view_context = 'WEBVIEW_com.tencent.mm:tools'  # view_context的值由contexts的打印中获取
        self.driver.switch_to.context(view_context)

    def wo_baoshangjifen(self):
        pass

    def wo_jiaguaka(self):
        # 加挂卡
        # 登录
        self.login()
        time.sleep(3)
        # 选择我
        self.driver.find_element_by_android_uiautomator('text("我")').click()
        # self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id=\"com.tencent.mm:id/aiu\" and @text=\"我\"]').click()
        print("点击成功1")
        # 选择更多服务
        self.driver.find_element_by_android_uiautomator('text("更多服务")').click()
        time.sleep(2)
        print("点击成功2")
        # 点击键盘按钮
        self.driver.find_element_by_xpath("//android.widget.ImageView[@content-desc=\"消息\"]").click()
        time.sleep(2)
        # 点击转化文字框
        # self.driver.find_element_by_id('com.tencent.mm:id/aic').click()
        time.sleep(2)
        # 选择加挂卡
        self.driver.find_element_by_xpath(
            "//android.widget.FrameLayout[@content-desc=\"当前所在页面,与wxid_i2ugr5cpmk4721的接口测试号的聊天\"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ScrollView/android.widget.EditText").send_keys(
            "1")
        time.sleep(3)
        # 发送
        self.driver.find_element_by_android_uiautomator('text("发送")').click()
        print("点击发送成功3")
        time.sleep(4)
        # self.driver.find_element_by_id('com.tencent.mm:id/aiw').click()
        self.touchTapA(1035, 711)
        print('touchou 1035 ,353')
        time.sleep(3)
        # 立即绑定其他用户
        print("立即绑定其他用户")
        time.sleep(4)
        self.touchTapA(437, 1674)
        print('touchou 437 ,1674')
        time.sleep(0.5)
        # self.driver.find_element_by_id('com.tencent.mm:id/b6g').click()
        # self.driver.find_element_by_class_name("【立即绑定其他账户】").click()
        print("点击成功4")
        time.sleep(3)
        webcontext = self.driver.contexts[-1]
        self.driver.switch_to.context(webcontext)
        time.sleep(3)

        print("input finished~")
        # 输入账号
        self.driver.find_element_by_xpath("//*[@id=\"signaccount\"]").send_keys("62176056080280613")
        # 输入手机号
        self.driver.find_element_by_id("signPhone").send_keys("15800010004")
        time.sleep(3)
        self.driver.back()
        # self.driver.find_element_by_css_selector("#iconChecked").click()
        time.sleep(3)
        self.driver.find_element_by_css_selector("#nextBtn").click()
        _CMD = "adb shell input tap {} {}".format(550, 1567)
        os.popen(_CMD)
        time.sleep(6)
        print("请输入密码")
        # 输入555666
        self.Clickkw("555666")

        # 短信验证码
        time.sleep(3)
        msg = self.getMsg1("14.16.10.36:7001", "qdcs01", "bsb@12345", "15800010004")
        print(msg)
        self.driver.find_element_by_id("verify").send_keys(msg)
        # 确认
        self.driver.execute_script("$(\'button[data-submit=\"modal\"]').click()")
        print("确认成功")
        time.sleep(5)
        # 取成功(jquery)
        self.driver.execute_script("$('.p10').text()")
        print("111")
        #
        _SUCCESS = self.driver.find_element_by_css_selector(".p10").text
        print(_SUCCESS)
        # 返回
        # self.driver.execute_script('$(".yellow_big_btn1").click()')
        self.driver.find_element_by_id("finish").click()
        # 解除签约

    def wo_jiechuqianyue(self):
        # 登录
        self.login()
        time.sleep(3)
        # 选择我
        self.driver.find_element_by_android_uiautomator('text("我")').click()
        # 选择更多服务
        self.driver.find_element_by_android_uiautomator('text("更多服务")').click()
        time.sleep(2)
        # 点击键盘按钮
        self.driver.find_element_by_xpath("//android.widget.ImageView[@content-desc=\"消息\"]").click()
        time.sleep(2)
        # 选择解除签约选项
        self.driver.find_element_by_xpath(
            "//android.widget.FrameLayout[@content-desc=\"当前所在页面,与wxid_i2ugr5cpmk4721的接口测试号的聊天\"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ScrollView/android.widget.EditText").send_keys(
            "2")
        # 发送
        self.driver.find_element_by_android_uiautomator('text("发送")').click()
        # 请选择解约的账号 问题  输入的4不确定， app内 取得 解约成功的字。即可。技术：ocr
        self.driver.find_element_by_xpath(
            "//android.widget.FrameLayout[@content-desc=\"当前所在页面,与wxid_i2ugr5cpmk4721的接口测试号的聊天\"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ScrollView/android.widget.EditText").send_keys(
            "4")
        # 发送
        self.driver.find_element_by_android_uiautomator('text("发送")').click()
    def wo_baoshangjifen(self):
        # bs积分
        # 登录
        self.login()
        time.sleep(3)
        # 选择我
        self.driver.find_element_by_android_uiautomator('text("我")').click()
        # 选择bs积分
        self.driver.find_element_by_android_uiautomator('text("bs积分")').click()
        time.sleep(5)
        print("等待进入bs积分商城")
        # 进入bs积分商城
        self.touchTapA(226, 1219)
        print('touchou 226,1219')
        time.sleep(5)
        print("进入成功")
        m = self.driver.contexts
        print("contexts:")
        print(m)
        # a=self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT,{"name":"NATIVE_APP"})
        # self.driver.find_element_by_xpath("//*[@id=\"clickBtn2\"]").click()
        # print(111)
        time.sleep(5)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.tencent.mm:toolsmp"})
        time.sleep(3)
        # 点击积分兑换好礼
        print("成功前")
        time.sleep(3)
        self.ClickByXpath_tap("//*[@id=\"clickBtn2\"]")
        print("成功后")
        time.sleep(6)
        a = self.driver.contexts
        print("contexts:")
        print(a)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/h6")
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/img")
        print(s1)
        time.sleep(3)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.tencent.mm:appbrand0"})
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/h6")
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/img")
        print(s2)
        time.sleep(3)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.tencent.mm:toolsmp"})
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/h6")
        self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/img")
        print(s4)
        time.sleep(3)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.tencent.mm:tools"})
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/h6")
        self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/img")
        print(s4)
        time.sleep(3)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_com.tencent.mm"})
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/h6")
        self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/img")
        print(s5)
        time.sleep(3)

        # 选择大有梦想-贵宾等机权益
        print("选择大有梦想-贵宾等机权益")
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div")
        # self.ClickByXpath_tap("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div/span")
        print("选择大有梦想-贵宾等机权益2")
        # self.driver.find_element_by_xpath("//*[@id=\"jifenMKL\"]/div[1]/ul/li[4]/div").click()
        # self.touchTapA(782,1200)
        # print('touchou 782,1200')
        # 选择我要兑换
        time.sleep(6)
        self.ClickById_tap("btn")
        print(666)
        print("选择我要兑换")
        # 确认我要兑换
        time.sleep(7)
        self.ClickById_tap("btn")
        print("确认我要兑换")
        # 确认订单
        time.sleep(4)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/button").click()
        # 短信验证码
        time.sleep(3)
        print("xianshuchushishi")
        msg = self.getMsg_addCard("14.16.10.36:7001", "qdcs01", "bsb@12345", "15800010004")
        # print(msg)
        self.driver.find_element_by_id("verify").send_keys(msg)
        # 确认
        time.sleep(4)
        self.touchTapA(310, 590)
        print('touchou 310,590')
        time.sleep(4)
        # 点击确认
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/button").click()

    def erleihukaihu(self):
        # 二类户开户
        # 登录
        self.login()
        time.sleep(3)
        # 选择bs
        self.driver.find_element_by_android_uiautomator('text("bs")').click()
        # 选择二类户开户
        time.sleep()
        self.driver.find_element_by_android_uiautomator('text("二类户开户")').click()
        print("选择二类户开户")
        time.sleep(4)
        # self.driver.find_element_by_id("com.tencent.mm:id/azn").click()
        self.touchTapA(502, 1530)
        print('touchou 502,1530')
        #

    def aichuxu_zhengcunzhengqu(self):
        # 登录
        self.login()
        time.sleep(3)
        # 选择爱
        self.driver.find_element_by_android_uiautomator('text("爱")').click()
        # 爱储蓄
        self.driver.find_element_by_android_uiautomator('text("爱储蓄")').click()
        # 点击爱储蓄
        # time.sleep(3)
        self.touchTapA(442, 823)
        print('touchou 442,823')
        # self.driver.find_element_by_id("com.tencent.mm:id/azn").click()

        time.sleep(4)
        # 进入定期页面
        time.sleep(2)
        m = self.driver.contexts
        print("contexts:")
        print(m)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
        time.sleep(3)

        # 选择类型
        self.touchTapA(500, 279)
        print('touchou 500,279')
        time.sleep(5)
        self.driver.find_element_by_xpath("//*[@id=\"savingPro\"]/li[1]").click()
        # self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT,{"name":"WEBVIEW_com.tencent.mm:tools"})

    def text(self):
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Custom View")').click()  # text
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains("View")').click()  # textContains
        self.driver.find_element_by_android_uiautomator('new UiSelector().textStartsWith("Custom")').click()  # textStartsWith
        self.driver.find_element_by_android_uiautomator('new UiSelector().textMatches("^Custom.*")').click()

    def open(self):
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("账户查询")') # click
        time.sleep(6)
        self.driver.tap(540,840)  # click zhongjian de jianpan
        self.driver.tap(112,1460) # click a
        self.driver.tap(144,1760) # click 123
        self.driver.tap(540,1690) # click 0
        time.sleep(3)
if __name__ == "__main__":
    # AndroidTest().touch()
    Produce().wo_baoshangjifen()
