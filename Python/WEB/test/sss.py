#coding=utf-8
import os,sys
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "."))
from util.functionTool import *
import name
'''
无GPS：
江西 河南

GPS：
天津
'''



class CheXian_LiPei(SelenFun):

    def __init__(self,baodan):
        self.baodan = baodan
        self.result_txt = {}
        self.location = gps

    def baoan(self):#OK 报案
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % TBUN)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        time.sleep(3)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[3].click();")
        time.sleep(3)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name","leftFrame")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='理赔子系统'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='报案管理'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='理赔子系统 >> 报案管理 >> 报案新增'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        __win = self.driver.current_window_handle
        self.click_by_css("input[value='保单信息']")
        while len(self.driver.window_handles) != 1:
            break
        __all = self.driver.window_handles
        for h in __all:
            if h != __win:
                self.driver.switch_to.window(h)
                self.send_by_css("input[name='queryPolicyPolicyNo']",self.baodan)
                self.send_by_names("queryPolicyDamageDate_DAY",nowdate())
                self.click_by_css("input[value='查询']")
                self.swich2frame("name", "QueryResultFrame")
                self.click_by_csss("input[name='checkboxSelect']",0)
                self.click_by_csss("input[name='checkboxSelect']",1)
                self.click_by_css("input[value='新增']")
                self.alert_acc()
                self.driver.switch_to.window(__win)

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.driver.find_elements_by_css_selector("input[name='registCarSubSinglecar']")[1].click()#否
        self.click_by_css("input[name='registCarSubLosspersonflag'][value=\"0\"]")#否，是否有人伤

        self.click_by_css("input[name='registLossItemTypes'][tabIndex='13']") #本车车损
        self.click_by_css("input[name='registLossItemTypes'][tabIndex='22']") #第三者其它财产损失
        self.click_by_css("input[name='registLossItemTypes'][tabIndex='24']") # 第三者人员人伤医疗


        self.send_by_css("input[name='registDriverName']",SKNAME)
        self.send_by_css("input[name=\"registCollisionObject\"]","止战之殇")
        self.send_by_css("input[name='registReportorPhoneNumber']", TEL)
        self.send_by_names("registPhoneNumber",TEL)
        win = self.driver.current_window_handle
        self.send_by_names("registReportorName", SKNAME)
        self.scrollto("[name='registReportorName']")


        if self.location=="gps":
            self.click_by_csss("[value='地图']",0)
            # self.driver.execute_script("MapForGps()")
            time.sleep(2)
            print(len(self.driver.window_handles))
            for h in self.driver.window_handles:
                if h != win:
                    self.driver.switch_to.window(h)
                    self.send_by_names("SuggestId","上海市浦东新区上海银行(总行)")
                    time.sleep(4)
                    self.click_by_css("[value='搜索'][class='button']")
                    time.sleep(3)
                    self.click_by_css("[value='确定'][class='button']")
                    self.driver.switch_to.window(win)
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        if self.location != "gps":
            self.send_by_names("registDamageAddress", "上海市浦东新区上海银行(总行)")
            self.send_by_names("registGpsAddr", "上海市浦东新区上海银行(总行)")
            self.send_by_names("registCheckAddr", "上海市浦东新区上海银行(总行)")
        time.sleep(2)

        su = self.driver.find_element_by_css_selector("TABLE[id='TopButton']")
        self.driver.execute_script("arguments[0].scrollIntoView();", su)
        self.driver.find_elements_by_css_selector("input[name='buttonchargeCarsInsert']")[0].click()#三者车信息上面
        time.sleep(2)
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarCarDtoRemark']")[1].send_keys("测试")
        time.sleep(2)

        self.driver.find_elements_by_css_selector("input[name='buttonchargePersonInsert']")[1].click() #物损信息
        time.sleep(2)
        Select(self.driver.find_elements_by_name("gcThirdCarSubPersonDtoLossType")[1]).select_by_index(1)  #车外人
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarSubPersonDtoPersonName']")[1].send_keys("测试2")

        self.driver.find_elements_by_css_selector("input[name='buttonchargePropInsert']")[1].click()#出现摘要
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarSubPropDtoLossName']")[1].send_keys("测试")

        time.sleep(2)
        dr = self.driver.find_element_by_css_selector("input[value='提交']")
        self.driver.execute_script("arguments[0].scrollIntoView();", dr)
        self.click_by_css("input[value='生成出险摘要']")
        self.click_by_css("input[value='提交']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.isExist(".tishi")
        baohao_text = re.findall("\d+",self.driver.find_element_by_css_selector(".tishi > tbody > tr:nth-child(3) > td").text)
        if baohao_text !=[]: self.result_txt["报案号"] = baohao_text[0]
        print("报案新增", self.baoan.__name__  + "\t" +  self.result_txt.get("报案号"))
        # self.click_by_css("input[name='buttonSurveyDelegate']")

    def diaodu(self):#OK
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        # self.alert_acc()
        # self.click_by_csss("input[name='selectPolicy']",0)#调度指派
        self.click_by_css("[name='selectPolicy][tabIndex='6']")
        # self.click_by_css("[name='selectPolicy][tabIndex='13']")
        # self.click_by_csss("input[name='selectPolicy']", 1)  # 调度指派
        self.send_by_names("DelegateDtoObjectType","004")
        self.send_by_names("DelegateDtoObjectName","公司内部人员")
        self.send_by_names("DelegateDtoCheckUnitCode","01")
        self.send_by_names("DelegateDtoCheckUnitName","泰康在线财产保险股份有限公司")
        self.send_by_names("DelegateDtoCheckerCode1","00000088@upic.com")
        self.send_by_names("DelegateDtoChecker1","北京核损核赔初级岗")
        self.send_by_names("DelegateDtoCheckerCode2","00000099@upic.com")
        self.send_by_names("DelegateDtoChecker2","北京核损核赔中级岗")

        self.click_by_css("[value='任务指派']")
        self.click_by_css("[value='提交']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            diaodu_text = self.driver.find_element_by_css_selector(".tishi").text
            print("调度 ",getfunname() + "\t" + diaodu_text)
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + getfunname() + ".jpg")
        except:
            print("调度 ",self.diaodu.__name__ + "\t")

    def chakan(self):#OK查看
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"查勘管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 查勘管理 >> 查勘新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GcSurveyMainDtoRegistNo']",self.result_txt.get("报案号"))
        self.click_by_csss("input[value='查询']", 1)
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.driver.find_element_by_css_selector("input[name='GcSurveyMainDtoNoDutyInd'][value='0']").click()#无责代赔
        self.driver.find_element_by_css_selector("input[name='GcSurveyMainDtoCheckSimpleCaseInd'][value='0']").click()#是否开启简易赔案检查
        self.driver.find_element_by_css_selector("input[name='GcSurveyMainDtoFirstSiteInd'][value='2']").click()#是否现场查勘

        # 获取页面输入元素 并模拟鼠标双击操作
        GcSurveyMainDtoDamageSurveyProvinceCode = self.driver.find_element_by_name("GcSurveyMainDtoDamageSurveyProvinceCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GcSurveyMainDtoDamageSurveyProvinceCode).perform()
        self.driver.find_element_by_name('GcSurveyMainDtoDamageSurveyProvinceCode').send_keys(Keys.ENTER)
        self.driver.find_element_by_name('GcSurveyMainDtoDamageSurveyProvinceCode').send_keys(Keys.ENTER)

        GcSurveyMainDtoDamageCityCode = self.driver.find_element_by_name("GcSurveyMainDtoDamageCityCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GcSurveyMainDtoDamageCityCode).perform()
        self.driver.find_element_by_name('GcSurveyMainDtoDamageCityCode').send_keys(Keys.ENTER)
        self.driver.find_element_by_name('GcSurveyMainDtoDamageCityCode').send_keys(Keys.ENTER)

        GcSurveyMainDtoDamageCountyCode = self.driver.find_element_by_name("GcSurveyMainDtoDamageCountyCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GcSurveyMainDtoDamageCountyCode).perform()
        self.driver.find_element_by_name('GcSurveyMainDtoDamageCountyCode').send_keys(Keys.ENTER)
        self.driver.find_element_by_name('GcSurveyMainDtoDamageCountyCode').send_keys(Keys.ENTER)

        Select(self.driver.find_element_by_name("GcSurveyMainDtoAccidentType")).select_by_index(2)#事故处理类型
        time.sleep(2)
        self.driver.find_elements_by_css_selector("a[href='javascript:;']")[5].click()
        # 标的车
        time.sleep(2)

        # 标的车
        time.sleep(2)
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarLossItemDtoLiabCode");q[1].value = "%s";' % "01")
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarLossItemDtoLiabName");q[1].value = "%s";' % "车损")
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarDtoLicensePlateType");q[1].value = "%s";' % "02")
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarDtoLicensePlateTypeName");q[1].value = "%s";' % "小型汽车")
        self.driver.find_elements_by_css_selector("input[name='gcSurveyCarLossItemDtoSumLoss']")[1].send_keys("100")
        self.driver.find_elements_by_css_selector("input[name='gcSurveyDriverDtoDrivingLicenseNo']")[1].send_keys(ID) #驾驶证编号
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyDriverDtoIdentifyNumber");q[1].value = "%s";' % ID)
        self.send_by_csss("input[name=\"gcSurveyDriverDtoLienseFileNo\"]", 0, ID) #出险驾驶员档案编号

        self.driver.find_elements_by_css_selector("input[name='gcSurveyPropDtoSumLoss']")[1].send_keys("100")
        Select(self.driver.find_elements_by_css_selector("select[name=\"gcSurveyPropDtoDutyFlag\"]")[1]).select_by_value("0")  # 是否属于有责车


        '''

        self.click_by_css("input[name=\"innerBtnDelete\"][tabIndex=\"147\"]")
        self.driver.find_elements_by_css_selector("input[name='gcSurveyDriverDtoDrivingLicenseNo']")[1].send_keys(ID) #驾驶证编号
        self.driver.execute_script('var q = document.getElementsByName("gcSurveyDriverDtoIdentifyNumber");q[1].value = "%s";' % ID)
        self.send_by_csss("input[name=\"gcSurveyDriverDtoLienseFileNo\"]", 0, ID) #出险驾驶员档案编号
        # self.send_by_names("gcSurveyDriverDtoLienseFileNo",ID) #出险驾驶员档案编号

        self.driver.find_elements_by_css_selector("input[name='gcSurveyPropDtoSumLoss']")[1].send_keys("100")
        Select(self.driver.find_elements_by_css_selector("select[name=\"gcSurveyPropDtoDutyFlag\"]")[1]).select_by_value("0") #是否属于有责车
        time.sleep(2)
        '''
        time.sleep(2)
        # self.click_by_css("input[name=\"innerBtnDelete\"][tabIndex=\"159\"]")
        # self.send_by_names("gcSurveyCarLossItemDtoLiabCode","01",1)
        # self.send_by_names("gcSurveyCarLossItemDtoLiabName","车损",1)
        # self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarDtoLicensePlateType");q[1].value = "%s";' % "02")
        # self.driver.execute_script('var q = document.getElementsByName("gcSurveyCarDtoLicensePlateTypeName");q[1].value = "%s";' % "小型汽车")
        # self.driver.find_elements_by_css_selector("input[name='gcSurveyCarLossItemDtoSumLoss']")[1].send_keys("100")
        # self.driver.find_elements_by_css_selector("input[name='gcSurveyDriverDtoDrivingLicenseNo']")[1].send_keys(ID) #驾驶证编号
        # self.driver.execute_script('var q = document.getElementsByName("gcSurveyDriverDtoIdentifyNumber");q[1].value = "%s";' % ID)
        # self.send_by_names("gcSurveyDriverDtoLienseFileNo",ID,1)#出险驾驶员档案编号
        #
        # self.driver.find_elements_by_css_selector("input[name='gcSurveyPropDtoSumLoss']")[1].send_keys("100")
        # Select(self.driver.find_elements_by_css_selector("select[name=\"gcSurveyPropDtoDutyFlag\"]")[1]).select_by_value("0") #是否属于有责车
        # time.sleep(2)

        # 三者车上人员
        self.driver.find_elements_by_css_selector("a[href='javascript:;']")[10].click()
        time.sleep(2)

        self.send_by_csss("input[name='gcCarSurveyPersonDtoMobile']", 0, TEL)
        Select(self.driver.find_elements_by_name("gcCarSurveyPersonDtoPersonDealMethod")[1]).select_by_index(2)#人伤处理方式
        self.send_by_csss("input[name='gcCarSurveyPersonDtoInjuryScopeDesc']",0,"孩子们眼中的形状是什么模样")#伤情描述
        self.send_by_csss("input[name='gcCarSurveyPersonDtoCertiCode']", 0, ID)#伤亡人员证件号码
        Select(self.driver.find_elements_by_css_selector("select[name=\"gcCarSurveyPersonDtoDutyFlag\"]")[1]).select_by_index(1) #是否属于有责车

        self.send_by_names("GcSurveyPersonFeeDtoLiabCode","M007",1)
        self.send_by_names("GcSurveyPersonFeeDtoLiabName","营养费",1)
        # self.driver.execute_script('var q = document.getElementsByName("GcSurveyPersonFeeDtoLiabCode");q[1].value = "%s";' % "M007")
        # self.driver.execute_script('var q = document.getElementsByName("GcSurveyPersonFeeDtoLiabName");q[1].value = "%s";' % "营养费")
        self.send_by_csss("input[name='GcSurveyPersonFeeDtoSumLoss']",0,"100")#预估金额
        #车外人 测试2
        self.driver.find_elements_by_css_selector("a[href='javascript:;']")[11].click()#伤情部位
        self.click_by_css("input[name='gcCarSurveyPersonLossTypes0'][value='13']")#下肢骨折
        time.sleep(2)
        self.driver.find_elements_by_css_selector("a[href='javascript:;']")[15].click()#查看报告

        self.send_by_csss("TEXTAREA[name='GcSurveyMainDtoContext']",0,"三年二班==这第一名到底有多强")
        #提交
        _win = self.driver.current_window_handle
        self.click_by_css("input[value='提交']")

        self.isWintwo()

        #网页对话框
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != _win:
                self.driver.switch_to.window(h)
                self.click_by_css("input[name='gcSurveyCarDtoSelectFlag']")
                self.driver.find_element_by_css_selector("input[name='gcSurveyPropDtoSelectFlag']").click()#
                self.driver.find_element_by_css_selector("input[name='gcCarSurveyPersonDtoSelectFlag']").click()#
                self.driver.find_element_by_css_selector("input[value='确定']").click()
        self.driver.switch_to.window(_win)
        self.alert_acc()
        self.driver.switch_to.window(_win)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            chankan_text = self.driver.find_element_by_css_selector(".tishi").text
            print("查勘新增",getfunname() + "\t" + chankan_text[0:4])
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + getfunname() + ".jpg")
        except:
            print("查勘新增",self.chakan.__name__  + "\t")

    def dingsunxinzeng(self):# OK 车辆定损新增
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"车险定损管理\"]")
        self.click_by_css("a[title=\"车辆定损管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 车险定损管理 >> 车辆定损管理 >> 车辆定损新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='gcRegistPolicyDtoRegistNo']",self.result_txt.get("报案号"))
        self.driver.find_elements_by_css_selector("input[value='查询']")[1].click()
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")

        self.driver.find_element_by_css_selector("input[name='gcCarEvaluateMainFirstSiteInd'][value='1']").click()#是否现场查勘

        # 获取页面输入元素 并模拟鼠标双击操作
        gcCarEvaluateMainDamageEvaluateAreaCode = self.driver.find_element_by_name("gcCarEvaluateMainDamageEvaluateAreaCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(gcCarEvaluateMainDamageEvaluateAreaCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateAreaCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateAreaCode').send_keys(Keys.ENTER)

        gcCarEvaluateMainDamageEvaluateCityCode = self.driver.find_element_by_name("gcCarEvaluateMainDamageEvaluateCityCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(gcCarEvaluateMainDamageEvaluateCityCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateCityCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateCityCode').send_keys(Keys.ENTER)

        gcCarEvaluateMainDamageEvaluateCountyCode = self.driver.find_element_by_name("gcCarEvaluateMainDamageEvaluateCountyCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(gcCarEvaluateMainDamageEvaluateCountyCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateCountyCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('gcCarEvaluateMainDamageEvaluateCountyCode').send_keys(Keys.ENTER)


        # self.send_by_names("gcCarEvaluateMainFrameNo",chejiahao) #需要改车架号
        Select(self.driver.find_element_by_name("gcCarEvaluateMainFactoryKind")).select_by_index(4) #修理厂类型 ?其他
        self.driver.find_element_by_css_selector("input[name='gcCarEvaluateMainFactoryName']").send_keys(name.random_gbk2312(6))#修理厂名称
        self.driver.find_element_by_css_selector("input[name='gcCarEvaluateMainFactoryCooprate'][value='0']").click()#否
        Select(self.driver.find_element_by_name("gcCarEvaluateMainIsFloodedCar")).select_by_index(2) #是否水淹车 否
        Select(self.driver.find_element_by_name("gcCarEvaluateMainFireFlag")).select_by_index(2) #是否火自爆
        self.driver.find_element_by_css_selector("input[name='buttonpartInsert'][value='新增']").click() #xinzeng
        time.sleep(2)
        self.send_by_names("GCCarEvaluateFeeKindCode","01",1)
        self.send_by_names("GCCarEvaluateFeeKindName","车辆损失险",1)

        self.driver.find_elements_by_css_selector("input[name='GCCarEvaluateFeeFeeTypeCode']")[1].send_keys("02") #施救费
        self.driver.find_elements_by_css_selector("input[name='GCCarEvaluateFeeFeeTypeCode']")[1].send_keys(Keys.TAB) #施救费不起
        self.driver.find_elements_by_css_selector("input[name='GCCarEvaluateFeeSumDefLoss']")[1].send_keys("100")#定损金额
        time.sleep(1.5)
        self._maxWin()
        self.click_by_css("[value='提交']")
        self.alert_acc()
        time.sleep(3)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            chankan_text = self.driver.find_element_by_css_selector(".tishi").text
            print("车辆定损新增",getfunname() + "\t" + chankan_text[0:4])
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + getcurmethod() + ".jpg")
        except:
            print("车辆定损新增",getfunname() + "\t")

    def caichandingsunxinzeng(self):#OK 财产定损新增
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("[title=\"理赔子系统\"]")
        self.click_by_css("[title=\"车险定损管理\"]")
        self.click_by_css("[title=\"财产定损管理\"]")
        self.click_by_css("[title=\"理赔子系统 >> 车险定损管理 >> 财产定损管理 >> 财产定损新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='gcRegistPolicyDtoRegistNo']",self.result_txt.get("报案号"))
        time.sleep(1)
        self.driver.find_elements_by_css_selector("input[value='查询']")[1].click()

        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.alert_acc()


        self.driver.find_element_by_css_selector("input[name='GCCarEvaluateMainFirstSiteInd'][value='1']").click()#是否现场查勘

        # 获取页面输入元素 并模拟鼠标双击操作
        GCCarEvaluateMainDamageEvaluateAreaCode = self.driver.find_element_by_name("GCCarEvaluateMainDamageEvaluateAreaCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GCCarEvaluateMainDamageEvaluateAreaCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateAreaCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateAreaCode').send_keys(Keys.ENTER)

        GCCarEvaluateMainDamageEvaluateCityCode = self.driver.find_element_by_name("GCCarEvaluateMainDamageEvaluateCityCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GCCarEvaluateMainDamageEvaluateCityCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateCityCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateCityCode').send_keys(Keys.ENTER)

        GCCarEvaluateMainDamageEvaluateCountyCode = self.driver.find_element_by_name("GCCarEvaluateMainDamageEvaluateCountyCode")
        action_chains = ActionChains(self.driver)
        action_chains.double_click(GCCarEvaluateMainDamageEvaluateCountyCode).perform()
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateCountyCode').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_name('GCCarEvaluateMainDamageEvaluateCountyCode').send_keys(Keys.ENTER)

        Select(self.driver.find_element_by_name("gcCarEvaluateMainDtoLicenseNoA6")).select_by_index(1)#所属车辆  ?

        self.send_by_names("GCCarEvaluateFeeKindCode","02",1)
        self.send_by_names("GCCarEvaluateFeeKindName","商业第三者责任险",1)
        # self.driver.execute_script('var q = document.getElementsByName("GCCarEvaluateFeeKindCode");q[1].value = "%s";' % "02")
        # self.driver.execute_script('var q = document.getElementsByName("GCCarEvaluateFeeKindName");q[1].value = "%s";' % "商业第三者责任险")
        self.driver.find_elements_by_css_selector("input[name='GCCarEvaluateFeeSumDefLoss']")[1].send_keys("100")#定损金额
        self.driver.find_elements_by_css_selector("input[name='GCCarEvaluateFeeItemName']")[1].send_keys("止战之殇") #损失项目
        self.click_by_css("[value='提交']")
        self.alert_acc()

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            chankan_text = self.driver.find_element_by_css_selector(".tishi").text
            print("财产定损新增",getfunname() + "\t" + chankan_text[0:5])
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + get_current_methodn() + ".jpg")
        except:
            print("财产定损新增",getfunname() + "\t")

    def pingjiyijiao(self):#平级移交 OK
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 平级移交\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name=\"gcClaimStatusDetailDtoRegistNo\"]",self.result_txt.get("报案号"))
        _win = self.driver.current_window_handle
        self.click_by_css("input[value=\"查询\"]")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_csss("a[href=\"#\"]", 1)
        self.isWintwo()
        for h in self.driver.window_handles:
            if h !=_win:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.send_by_names("GcClaimStatusDetailDtoObjectType","004")
                self.send_by_names("GcClaimStatusDetailDtoObjectName","公司内部人员")
                self.send_by_names("gcClaimStatusDetailDtoInstitution","01")
                self.send_by_names("gcClaimStatusDetailDtoInstitutionName","泰康在线财产保险股份有限公司")
                self.send_by_names("gcClaimStatusDetailDtoOperatorCode","00000088@upic.com")
                self.send_by_names("gcClaimStatusDetailDtoOperateName","北京核损核赔初级岗")

                # self.driver.execute_script('var q = document.getElementsByName("GcClaimStatusDetailDtoObjectType");q[0].value = "%s";' % "004")
                # self.driver.execute_script('var q = document.getElementsByName("GcClaimStatusDetailDtoObjectName");q[0].value = "%s";' % "公司内部人员")
                # self.driver.execute_script('var q = document.getElementsByName("gcClaimStatusDetailDtoInstitution");q[0].value = "%s";' % "01")
                # self.driver.execute_script('var q = document.getElementsByName("gcClaimStatusDetailDtoInstitutionName");q[0].value = "%s";' % "泰康在线财产保险股份有限公司")
                # self.driver.execute_script('var q = document.getElementsByName("gcClaimStatusDetailDtoOperatorCode");q[0].value = "%s";' % "00000088@upic.com")
                # self.driver.execute_script('var q = document.getElementsByName("gcClaimStatusDetailDtoOperateName");q[0].value = "%s";' % "北京核损核赔初级岗")
                self.click_by_css("[value=\"任务移交\"]")
        time.sleep(1)

        for h in self.driver.window_handles:
            if h != _win:
                self.driver.switch_to.window(h)
                self.driver.close()
                time.sleep(1)
        self.driver.switch_to.window(_win)
        self.driver.switch_to.default_content()
        time.sleep(1.5)
        # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + get_current_methodn() + ".jpg")
        print("平级移交",getfunname() + "\t" + "操作成功!")

    def renshanggenzong(self):# OK人伤跟踪新增
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"人伤跟踪管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 人伤跟踪管理 >> 人伤跟踪新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        # self.send_by_css("input[name='gcRegistPolicyDtoRegistNo']",self.result_txt.get("报案号"))
        self.send_by_names("gcRegistPolicyDtoRegistNo",self.result_txt.get("报案号"))
        self.click_by_csss("input[value='查询']", 1)
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='gcCarEvaluatePersonDtoLinker']",SKNAME)#联系人姓名

        self.driver.find_element_by_css_selector("input[name='gcCarEvaluateMainDtoSickInd'][value='1']").click() # 是否跟踪完毕  是
        self.click_by_css("[value='提交']")#提交

        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            renshang_text = self.driver.find_element_by_css_selector(".tishi").text
            print("人伤跟踪新增",getfunname() + "\t" + renshang_text[0:4])
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + get_current_methodn() + ".jpg")
        except:
            print("人伤跟踪新增",getfunname() + "\t")

    def shenjipingtai1(self):#审核批改
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"定核损审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 定核损审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[value='查询(Q)']")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        # __sh = self.driver.find_element_by_css_selector("input[value='审核意见']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", __sh)
        self.scrollto("[value='审核意见']")
        time.sleep(1)

        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1)#同意
        __win1 = self.driver.current_window_handle
        self.click_by_css("input[value='审核意见']")#点审核意见
        self.isWintwo()

        for h in self.driver.window_handles:
            if h != __win1:
                self.driver.switch_to.window(h)
                time.sleep(1.5)
                self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(__win1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过'][name='passBtn']")
        self.alert_acc()
        self.alert_acc()
        time.sleep(2)
        for h in  self.driver.window_handles:
            if h!= __win1:
                self.driver.switch_to.window(h)
                time.sleep(2)
                self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(__win1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            shenjipingtai1_text = self.driver.find_element_by_css_selector(".tishi").text
            time.sleep(1)
            print("定核损审核待处理任务查询",getfunname() + "\t" + shenjipingtai1_text[0:4])
            # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + get_current_methodn() + ".jpg")
        except:
            print("定核损审核待处理任务查询",getfunname() + "\t")

    def shenjipingtai2(self): #OK
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"定核损审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 定核损审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[value='查询(Q)']")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.scrollto("[value='审核意见'][name='butViewTranceInfo']")

        time.sleep(1)
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1)#同意
        __win3 = self.driver.current_window_handle
        self.click_by_css("input[value='审核意见'][name='butViewTranceInfo']")#点审核意见
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win3:
                self.driver.switch_to.window(h)
                time.sleep(3)
                self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(__win3)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过']")
        self.alert_acc()
        time.sleep(2)

        for h in self.driver.window_handles:
            if h != __win3:
                self.driver.switch_to.window(h)
                self.driver.close()
                self.driver.switch_to.window(__win3)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.isExist(".tishi")
        shenjipingtai2_text = self.driver.find_element_by_css_selector(".tishi").text
        print("定核损审核待处理任务查询",getfunname() + "\t" + shenjipingtai2_text[0:4])
        # cutscreem(os.path.curdir + "\\" + self.result_txt.get("报案号") + "\\" + get_current_methodn() + ".jpg")

    def yiliaoshenhe1(self):#OK
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"医疗审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 医疗审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[value='查询(Q)']")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(1)
        self.scrollto("[name='uwResultListBln']")
        time.sleep(1)
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1) #同意
        __win2 = self.driver.current_window_handle
        self.click_by_css("input[value='审核意见'][name='butViewTranceInfo']")#点审核意见
        time.sleep(1.5)
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win2:
                self.driver.switch_to.window(h)
                time.sleep(2)
                self.driver.close()
                self.driver.switch_to.window(__win2)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过'][name='passBtn']")
        self.alert_acc()

        for h in self.driver.window_handles:
            if h != __win2:
                self.driver.switch_to.window(h)
                time.sleep(2)
                self.driver.close()
                self.driver.switch_to.window(__win2)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过'][name='passBtn']")
        self.alert_acc()
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            yiliaoshenhe1_text = self.driver.find_element_by_css_selector(".tishi").text
            print("医疗审核待处理任务查询",getfunname() + "\t" + yiliaoshenhe1_text[0:4])
        except:
            print("医疗审核待处理任务查询",getfunname() + "\t")

    def danzhengshouji(self):#O K单证收集
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"单证收集管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 单证收集管理 >> 单证待收集\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("[name='queryRegistRegistNo']",self.result_txt.get("报案号"))
        self.click_by_css("[value='查询'][name='buttonQuery']")
        self.swich2frame("name", "QueryResultFrame")
        try:
            self.driver.find_elements_by_css_selector("a[href='#']")[1].click()
        except:
            self.driver.find_element_by_css_selector("a[href='#']").click()

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("[value='索赔清单']")
        time.sleep(2)
        #标的车
        chexun ='''
            var p = document.getElementsByName("GcDocCollectGuideDtoPitchFlag");
            for (var i =0 ; i < p.length ; i++){
                if ((p[i].getAttribute("value").indexOf("车损相片")) !=-1){
                    p[i].click();
                }
            }
        '''

        wusun = '''
        var p = document.getElementsByName("GcDocCollectGuideDtoPitchFlag");
            for (var i =0 ; i < p.length ; i++){
                if ((p[i].getAttribute("value").indexOf("物损相片")) !=-1){
                    p[i].click();
                }
            }
                '''


        renshang = '''
            var p = document.getElementsByName("GcDocCollectGuideDtoPitchFlag");
                for (var i =0 ; i < p.length ; i++){
                if ((p[i].getAttribute("value").indexOf("伤者身份证明")) !=-1){
                    p[i].click();
                }
            }
                '''
        self.usejs(chexun)
        self.usejs(wusun)
        self.usejs(renshang)

        time.sleep(1)
        #人伤资料

        self.click_by_css("[name='save'][tabIndex='1']")#保存
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        Select(self.driver.find_element_by_name("gcItemExtDtoFieldBA")).select_by_index(2)#否

        self.click_by_css("[value='提交']")#提交
        self.alert_acc()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            danzhengshouji_text = self.driver.find_element_by_css_selector(".tishi").text
            print("单证待收集",getfunname() + "\t" + danzhengshouji_text[0:4])
        except:
            print("单证待收集",getfunname() + "\t")

    def lisuanxinzeng(self): #理算新增

        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"理算管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 理算管理 >> 理算新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='queryClaimRegistNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[value='查询'][name='buttonQuery']")
        self.swich2frame("name", "QueryResultFrame")

        # try:
        #     self.driver.find_elements_by_css_selector("a[href='#']")[1].click()
        # except:
        #     self.driver.find_element_by_css_selector("a[href='#']").click()

        # time.sleep(2)
        # self.keyud(VK_CODE['tab'])
        # time.sleep(2)
        # self.keyud(VK_CODE['tab'])
        # time.sleep(2)
        # self.keyud(VK_CODE['enter'])
        time.sleep(5)

        self.driver.find_element_by_xpath("//table[@id='ResultTable']/tbody/tr/td/a").click()

        self.alert_acc()

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(2)
        self.click_by_css("input[value='计算赔款金额'][name=\"calCompbutton\"]")#计算赔款金额
        time.sleep(1)
        self.click_by_names("collectFeeButton") #生成计算书
        # self.click_by_css("input[name=\"collectFeeButton\"][value=\"生成计算书\"]")#生成计算书

        self.driver.find_elements_by_css_selector("input[name=\"adjustmentFeePayeeView\"]")[1].click()
        time.sleep(1)
        Select(self.driver.find_elements_by_name("adjustmentFeeBankPayType")[1]).select_by_index(2)  # 对私
        self.send_by_names("adjustmentFeeBankCode","102",1)#银行编码
        self.send_by_names("adjustmentFeeBankBranchNameView","中国工商银行",1)#银行名
        self.send_by_names("adjustmentFeePayeeMobile","13333333333",1)#联系人电话
        self.send_by_names("adjustmentFeeAccountNo","6222222222222222",1)#银行帐号
        self.send_by_names("adjustmentFeeIdNo",ID,1)#证件号码
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeBankCode");q[1].value = "%s";' % "102") #银行编码
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeBankBranchNameView");q[1].value = "%s";' % "中国工商银行") #银行名
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeePayeeMobile");q[1].value = "%s";' % "13333333333") #联系人电话
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeAccountNo");q[1].value = "%s";' % "6222222222222222")#银行帐号
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeIdNo");q[1].value = "%s";' % ID)#证件号码
        time.sleep(1)
        self.scrollto("input[value='确定']")
        time.sleep(0.5)
        try:
            self.click_by_names("btnCloseFeeDetail",1)

            # self.driver.execute_script("var q = document.getElementsByName('btnCloseFeeDetail');q[1].click()")  #确定
        except:
            # self.driver.execute_script("var q = document.getElementsByName('btnCloseFeeDetail');q[2].click()")  #确定
            self.click_by_names("btnCloseFeeDetail", 2)
        #收款人证件号码
        self.alert_acc()
        try:
            self.send_by_names("adjustmentFeeIdNoView",ID,1)
            # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeIdNoView");q[1].value = "%s";' % ID)#收款人id
        except:
            self.send_by_names("adjustmentFeeChargeIdNoView",ID,1)
            # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeChargeIdNoView");q[1].value = "%s";' % ID)#id
        #第二个
        time.sleep(1)
        self.driver.find_elements_by_css_selector("input[name=\"adjustmentFeePayeeView\"]")[2].click()
        # self.driver.find_elements_by_name("adjustmentFeePayeeView")[2].click()  # 点名字
        time.sleep(1)
        Select(self.driver.find_elements_by_name("adjustmentFeeBankPayType")[2]).select_by_index(2)  # 对私
        self.usejs('var q = document.getElementsByName("adjustmentFeeBankCode");q[2].value = "%s";' % "102") #银行
        self.usejs('var q = document.getElementsByName("adjustmentFeeBankBranchNameView");q[2].value = "%s";' % "中国工商银行")
        self.usejs('var q = document.getElementsByName("adjustmentFeePayeeMobile");q[2].value = "%s";' % "13333333333") #电话
        self.usejs('var q = document.getElementsByName("adjustmentFeeAccountNo");q[2].value = "%s";' % "6222222222222222")#银行帐号
        self.usejs('var q = document.getElementsByName("adjustmentFeeIdNo");q[2].value = "%s";' % ID)#证件号码
        time.sleep(2)
        self.scrollto("input[value='确定']")

        time.sleep(0.5)
        try:
            self.driver.execute_script("var q = document.getElementsByName('btnCloseFeeDetail');q[2].click()")  #确定
        except:
            self.driver.execute_script("var q = document.getElementsByName('btnCloseFeeDetail');q[3].click()")  #确定

        self.alert_acc() # 收款人证件号码
        try:
            self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeIdNoView");q[2].value = "%s";' % ID) #收款人id
        except:
            self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeChargeIdNoView");q[2].value = "%s";' % ID)#id
        time.sleep(1)
        self._maxWin()
        self.driver.find_element_by_css_selector("input[id='submitButton'][tabIndex='5']").click() #提交submitButton
        time.sleep(2)

        self.alert_acc()
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            lisuanxinzeng_text = self.driver.find_element_by_css_selector(".tishi").text
            print("理算新增",getfunname() + "\t" + lisuanxinzeng_text[0:4])
        except:
            print("理算新增",getfunname() + "\t")

    def hepeishenhe(self):

        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"核赔审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 核赔审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[value='查询(Q)']")
        self.swich2frame("name", "QueryResultFrame")
        self.driver.find_elements_by_css_selector("a[href='#']")[0].click()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.scrollto("input[name='passBtn']")

        time.sleep(1)
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1) #同意
        __win2 = self.driver.current_window_handle
        self.driver.find_element_by_css_selector("input[name='butViewTranceInfo']").click()#点审核意见
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win2:
                self.driver.switch_to.window(h)
                time.sleep(2)
                self.driver.close()
                self.driver.switch_to.window(__win2)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.driver.find_element_by_css_selector("input[name='passBtn']").click()
        self.alert_acc()
        self.alert_acc()
        for h in self.driver.window_handles:
            if h != __win2:
                self.driver.switch_to.window(h)
                time.sleep(1.5)
                self.driver.close()
                self.driver.switch_to.window(__win2)

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(1)
        try:
            hepeishenhe1_text = self.driver.find_element_by_css_selector(".tishi").text
            print("核赔审核待处理任务查询",getfunname() + "\t" + hepeishenhe1_text[0:4])
        except:
            print("核赔审核待处理任务查询",getfunname() + "\t")
        getnumber(_baodanhao[i] + "|" + self.result_txt.get("报案号")+"\n")
        print("报案号：", self.result_txt.get("报案号"))
        self.driver.quit()

    def run(self):
        print("<--start-" + time.ctime() + "->")
        killie2()
        self.baoan()
        self.diaodu()
        self.chakan()
        self.dingsunxinzeng()
        self.caichandingsunxinzeng()
        self.pingjiyijiao()
        self.renshanggenzong()
        self.shenjipingtai1()
        self.shenjipingtai2()
        self.yiliaoshenhe1()
        self.danzhengshouji()
        self.lisuanxinzeng()
        self.hepeishenhe()

class CheXian_ChongKai(SelenFun):

    def __init__(self,baoanhao):
        self.baoanhao= baoanhao

    def peikuanzhifushangchuan(self, SYJQ):#赔款支付上传
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.send_by_attr("input","id","username","value",TBUN)
        self.send_by_attr("input","id","password","value",PW)
        self.click_by_css("#logonsubmit")
        time.sleep(1)
        self.usejs("var a = document.getElementsByTagName('a');a[3].click();")
        time.sleep(1)
        self.driver.close()
        self.isWinone()
        self.driver.maximize_window()
        self.driver.switch_to.frame("leftFrame")

        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"重开赔案管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 重开赔案管理 >> 重开赔案新增\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("[name='closecaseRegistNo']",self.baoanhao)
        self.click_by_css("[name='buttonQuery']")
        self.swich2frame("name", "QueryResultFrame")

        if SYJQ == "SY":
            self.click_by_csss("a[href='#']",0)
        if SYJQ == "JQ":
            self.click_by_csss("a[href='#']",1)
        # self.driver.find_elements_by_css_selector("")[0].click()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_names("reopenContext","他们咬着苹果，手里拿着长镜头")
        self.click_by_css("[value='提交']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("[value='显示列表']")
        self.swich2frame("name", "QueryResultFrame")
        # self.driver.find_element_by_css_selector("a[href='#']").click()
        # self.driver.switch_to.default_content()
        # self.swich2frame("name","mainFrame")
        # self.send_by_css("textarea[name='reopenContext']","三年二班")
        # self.click_by_css("input[value='提交']")
        # self.driver.switch_to.default_content()
        # self.swich2frame("name","mainFrame")
        #重开审核
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"重开赔案审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 重开赔案审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_names("GwWfLogDtoContractNo",self.baoanhao)
        self.click_by_css("[value='查询(Q)']")
        self.swich2frame("name", "QueryResultFrame")
        self.driver.find_elements_by_css_selector("a[href='#']")[0].click()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.scrollto("[value='审核意见']")
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1) #同意
        __win = self.driver.current_window_handle
        self.click_by_css("[value='审核意见'][name='butViewTranceInfo']")
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win:
                self.driver.switch_to.window(h)
                time.sleep(1.1)
                self.driver.close()
                self.driver.switch_to.window(__win)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.driver.find_element_by_css_selector("[name='passBtn']").click()

        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        # self.click_by_css("[value='显示列表']")
        # self.swich2frame("name", "QueryResultFrame")
        time.sleep(1)
        #
        # print(self.isExist("a[href='#']"))
        # time.sleep(1)
        # if self.isExist("a[href='#']") is True:
        #     self.driver.find_element_by_css_selector("a[href='#']").click()
        #     self.alert_acc()
        #     self.driver.switch_to.default_content()
        #     self.swich2frame("name","mainFrame")
        #     time.sleep(1)
        #     __sh = self.driver.find_element_by_css_selector("input[value='审核意见']")
        #     self.driver.execute_script("arguments[0].scrollIntoView();", __sh)
        #     time.sleep(1)
        #     Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1) #同意
        #     self.driver.find_element_by_css_selector("input[value='审核意见'][name='butViewTranceInfo']").click()
        #     time.sleep(2)
        #     __all1 = self.driver.window_handles
        #     for h in __all1:
        #         if h != __win:
        #             self.driver.switch_to.window(h)
        #             time.sleep(2)
        #             self.driver.close()
        #             self.driver.switch_to.window(__win)
        #     self.driver.switch_to.default_content()
        #     self.swich2frame("name","mainFrame")
        #     self.click_by_css("[name='passBtn']")
        #     self.alert_acc()

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        try:
            peikuanzhifushangchuan_text = self.driver.find_element_by_css_selector(".tishi").text
            print(getfunname() + "\t" + peikuanzhifushangchuan_text[0:4])
        except:
            print(getfunname() + "\t")

    def lisuanbupei(self):#理算补赔
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"理算管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 理算管理 >> 理算补赔\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='queryClaimRegistNo']",self.baoanhao)#输入报案号
        self.click_by_css("input[name='buttonQuery']")#点击查找
        self.swich2frame("name", "QueryResultFrame")
        self.driver.find_elements_by_css_selector("a[href='#']")[0].click()#点击查找到的第一条

        self.alert_acc()
        # time.sleep(20)

        # try:
        #     while True:
        #         self.alert_acc()
        # except:
        #     pass

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_names("calCompbutton")#计算赔款金额
        time.sleep(1)
        self.click_by_names("collectFeeButton")#点击生成计算书

        time.sleep(2)

        self.driver.find_elements_by_css_selector("input[name=\"adjustmentFeePayeeView\"]")[1].click()
        time.sleep(1)

        Select(self.driver.find_elements_by_name("adjustmentFeeBankPayType")[1]).select_by_index(2)  # 对私
        time.sleep(1)
        self.send_by_names("adjustmentFeeBankCode","102",1)
        self.send_by_names("adjustmentFeeBankBranchNameView","中国工商银行",1)#银行名
        self.send_by_names("adjustmentFeePayeeMobile","13613552858",1)#联系人电话
        self.send_by_names("adjustmentFeeAccountNo","6222222222222222",1)#银行帐号
        # self.driver.find_element_by_name("adjustmentFeeAccountNo").send_keys("6222222222222222")
        # self.usejs('var q = document.getElementsByName("adjustmentFeeIdNo");q[1].value = "%s";' % ID)#证件号码
        self.usejs('var q = document.getElementsByName("adjustmentFeeIdNo");q[1].value = "110101198001010010"')#证件号码

        # self.driver.find_element_by_name("btnCloseFeeDetail").click()
        # self.scrollto("[value='确定'][name='btnCloseFeeDetail']")
        # Select(self.driver.find_elements_by_name("adjustmentFeeAccountType")[1]).select_by_index(1)  # 帐号类型

        # self.driver.find_element_by_names("btnCloseFeeDetail",1)

        # self.click_by_csss("input[value='确定'][name='btnCloseFeeDetail']", 1)
        # self.send_by_names("adjustmentFeeIdNoView",ID,1)# 收款人id


        time.sleep(3)
        self.usejs('var q = document.getElementsByName("adjustmentFeePayeeMobileView");q[1].value = "%s";' % "13333333333")  # 电话
        time.sleep(1)
        self.usejs('var q = document.getElementsByName("adjustmentFeeIdNoView");q[1].value = "%s";' % "110101198001010010")  # 证件号码
        time.sleep(1)
        self.usejs('var q = document.getElementsByName("adjustmentFeeBankCodeView");q[1].value = "%s";' % "102")  # 银行
        time.sleep(1)
        self.usejs('var q = document.getElementsByName("adjustmentFeeBankBranchName");q[1].value = "%s";' % "中国工商银行")
        time.sleep(1)
        self.usejs('var q = document.getElementsByName("adjustmentFeeAccountNoView");q[1].value = "%s";' % "6222222222222222")  # 银行帐号
        time.sleep(2)
        self.usejs('var q = document.getElementsByName("adjustmentFeeSumPaidView");q[1].value = "%s";' % "200.00")  # 支付金额
        time.sleep(2)
        self.click_by_names("collectFeeButton")#点击生成计算书
        time.sleep(2)


        #第二个 没有第二个 pass
        # time.sleep(1)
        # self.driver.find_elements_by_name("adjustmentFeePayeeView")[2].click()  # 点名字
        # Select(self.driver.find_elements_by_name("adjustmentFeeBankPayType")[2]).select_by_index(2)  # 对私
        # time.sleep(1)
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeBankCode");q[2].value = "%s";' % "102") #银行
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeBankBranchNameView");q[2].value = "%s";' % "中国工商银行")
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeePayeeMobile");q[2].value = "%s";' % "13333333333") #电话
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeAccountNo");q[2].value = "%s";' % "6222222222222222")#银行帐号
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeIdNo");q[2].value = "%s";' % ID)#证件号码
        # time.sleep(1)
        # __qd = self.driver.find_element_by_css_selector("input[value='确定'][name='btnCloseFeeDetail']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", __qd)
        # Select(self.driver.find_elements_by_name("adjustmentFeeAccountType")[2]).select_by_index(1)  # 帐号类型
        # time.sleep(0.5)
        # self.click_by_csss("input[value='确定'][name='btnCloseFeeDetail']", 0)
        # self.driver.execute_script('var q = document.getElementsByName("adjustmentFeeIdNoView");q[2].value = "%s";' % ID)  # 收款人id
        # self.driver.find_element_by_css_selector("input[id='submitButton'][tabIndex='5']").click() #提交submitButton
        time.sleep(1)

        self.click_by_css("[id='submitButton']")#提交submitButton
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(1)
        try:
            lisuanbupei_text = self.driver.find_elements_by_css_selector(".tishi").text
            print(getfunname() + "\t" + lisuanbupei_text[0:4])
        except:
            print(getfunname() + "\t")

        self.tag = True

    def lisuanbupeishenhe(self):
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"核赔审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 核赔审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.baoanhao)#输入报案号
        self.click_by_names("buttonQuery")#点击查找
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_csss("a[href='#']",0)#点击查找到的第一条

       #  查询有没有查询到
       #  if no
       #      n=0
       #      while(n<5){
       #          lisuanbupei.py
       #           查询有没有查询到
       #          if yes
       #              n=10
       #      }
       # else

        # self.driver.find_elements_by_css_selector("a[href='#']")[0].click()#点击查找到的第一条
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(1)
        self.scrollto("[value='审核意见'][name='butViewTranceInfo']")
        time.sleep(1)
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1) #同意
        _win1 = self.driver.current_window_handle
        self.click_by_css("[value='审核意见'][name='butViewTranceInfo']")#点审核意见
        time.sleep(1)

        for h in self.driver.window_handles:
            if h != _win1:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.driver.close()
                self.driver.switch_to.window(_win1)
        self.isWinone()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("[value='审核通过'][name='passBtn']")
        self.alert_acc()
        # self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(1)
        try:
            lisuanbupeishenhe_text = self.driver.find_elements_by_css_selector(".tishi").text
            print(getfunname() + "\t" + lisuanbupeishenhe_text[0:4])
        except:
            print(getfunname() + "\t")
        self.driver.quit()

    def run(self, SYJQ):
        print("<--start-" + time.ctime() + "->")
        killie2()
        self.peikuanzhifushangchuan(SYJQ)

        while True:
            try:
                self.lisuanbupei()
                if self.tag == True:
                    break
            except:
                pass

        self.lisuanbupeishenhe()

class CheXian_ZhuXiao(SelenFun):

    def __init__(self,baodan):
        self.baodan = baodan
        self.result_txt = {}
        self.location = gps

    def baoan(self):#OK 报案
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % TBUN)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        time.sleep(2)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[3].click();")
        time.sleep(1)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name","leftFrame")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='理赔子系统'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='报案管理'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.execute_script("function te(){ \
            var t_ele = document.getElementsByTagName('a'); \
            for (var i=0;i<t_ele.length;i++){ \
                if (t_ele[i].getAttribute('title')=='理赔子系统 >> 报案管理 >> 报案新增'){ \
                    t_ele[i].click(); \
                } \
            } \
        };te();")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        __win = self.driver.current_window_handle
        self.click_by_css("input[value='保单信息']")
        while len(self.driver.window_handles) != 1:
            break
        __all = self.driver.window_handles
        for h in __all:
            if h != __win:
                self.driver.switch_to.window(h)
                self.send_by_css("input[name='queryPolicyPolicyNo']",self.baodan)
                self.send_by_names("queryPolicyDamageDate_DAY",nowdate())
                self.click_by_css("input[value='查询']")
                self.swich2frame("name", "QueryResultFrame")
                self.click_by_csss("input[name='checkboxSelect']",0)
                self.click_by_csss("input[name='checkboxSelect']",1)
                self.click_by_css("input[value='新增']")
                self.alert_acc()
                self.driver.switch_to.window(__win)

        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.driver.find_elements_by_css_selector("input[name='registCarSubSinglecar']")[1].click()#否
        self.click_by_css("input[name='registCarSubLosspersonflag'][value=\"0\"]")#否，是否有人伤

        self.click_by_css("input[name='registLossItemTypes'][tabIndex='13']") #本车车损
        self.click_by_css("input[name='registLossItemTypes'][tabIndex='22']") #第三者其它财产损失
        self.click_by_css("input[name='registLossItemTypes'][tabIndex='24']") # 第三者人员人伤医疗


        self.send_by_css("input[name='registDriverName']",SKNAME)
        self.send_by_css("input[name=\"registCollisionObject\"]","止战之殇")
        self.send_by_css("input[name='registReportorPhoneNumber']", TEL)
        self.send_by_names("registPhoneNumber",TEL)
        win = self.driver.current_window_handle
        self.send_by_names("registReportorName", SKNAME)
        self.scrollto("[name='registReportorName']")

        if self.location=="gps":
            self.click_by_csss("[value='地图']",0)
            # self.driver.execute_script("MapForGps()")
            time.sleep(2)
            print(len(self.driver.window_handles))
            for h in self.driver.window_handles:
                if h != win:
                    self.driver.switch_to.window(h)
                    self.send_by_names("SuggestId","上海市浦东新区上海银行(总行)")
                    time.sleep(4)
                    self.click_by_css("[value='搜索'][class='button']")
                    time.sleep(3)
                    self.click_by_css("[value='确定'][class='button']")
                    self.driver.switch_to.window(win)

        time.sleep(1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        if self.location != "gps":
            self.send_by_names("registDamageAddress", "上海市浦东新区上海银行(总行)")
            self.send_by_names("registGpsAddr", "上海市浦东新区上海银行(总行)")
            self.send_by_names("registCheckAddr", "上海市浦东新区上海银行(总行)")
        time.sleep(2)

        su = self.driver.find_element_by_css_selector("TABLE[id='TopButton']")
        self.driver.execute_script("arguments[0].scrollIntoView();", su)
        self.driver.find_elements_by_css_selector("input[name='buttonchargeCarsInsert']")[0].click()#三者车信息上面
        time.sleep(2)
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarCarDtoRemark']")[1].send_keys("测试")
        time.sleep(2)

        self.driver.find_elements_by_css_selector("input[name='buttonchargePersonInsert']")[1].click() #物损信息
        time.sleep(2)
        Select(self.driver.find_elements_by_name("gcThirdCarSubPersonDtoLossType")[1]).select_by_index(1)  #车外人
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarSubPersonDtoPersonName']")[1].send_keys("测试2")

        self.driver.find_elements_by_css_selector("input[name='buttonchargePropInsert']")[1].click()#出现摘要
        self.driver.find_elements_by_css_selector("input[name='gcThirdCarSubPropDtoLossName']")[1].send_keys("测试")

        time.sleep(2)
        dr = self.driver.find_element_by_css_selector("input[value='提交']")
        self.driver.execute_script("arguments[0].scrollIntoView();", dr)
        self.click_by_css("input[value='生成出险摘要']")
        self.click_by_css("input[value='提交']")
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.isExist(".tishi")
        baohao_text = re.findall("\d+",self.driver.find_element_by_css_selector(".tishi > tbody > tr:nth-child(3) > td").text)
        if baohao_text !=[]: self.result_txt["报案号"] = baohao_text[0]
        print(self.baoan.__name__  + "\t" +  self.result_txt.get("报案号"))
        # self.click_by_css("input[name=\"buttonSurveyDelegate\"]")

    def lianzhuxiao(self): #立案注销
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"理赔子系统\"]")
        self.click_by_css("a[title=\"立案注销管理\"]")
        self.click_by_css("a[title=\"理赔子系统 >> 立案注销管理 >> 注销待处理\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='queryRegistRegistNo']",self.result_txt.get("报案号"))
        self.click_by_css("input[name='buttonQuery']")

        self.swich2frame("name", "QueryResultFrame")
        self.click_by_csss("[href='#']",0)
        # self.driver.find_elements_by_css_selector("")[0].click()
        self.alert_acc()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        time.sleep(2)
        # self.send_by_names("GcCancellationDtoApplyReasonName","04")
        self.send_by_css("[name='GcCancellationDtoApplyReasonName']","04")
        self.keyud(VK_CODE['tab'])

        self.send_by_names("GcCancellationDtoDetailInfo","我始终还是我，谁都改变不了我")
        self.click_by_css("input[value='提交']")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("[value='显示列表']")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_csss("[href='#']",0)
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GcCancellationDtoApplyReasonName']","04")
        self.keyud(VK_CODE['tab'])
        self.send_by_css("[name='GcCancellationDtoDetailInfo']","红龙")
        self.click_by_css("[value='提交']")
        time.sleep(1.5)
        print(getfunname()+"\t")

    def zhuxiaoshenhe(self):
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"立案注销审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 立案注销审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.send_by_names("GwWfLogDtoContractNo",self.result_txt.get("报案号"))
        self.click_by_names("buttonQuery")
        self.swich2frame("name", "QueryResultFrame")
        # self.click_by_csss("[href='#']",0)

        time.sleep(1)
        self.driver.find_elements_by_css_selector("a[href='#']")[0].click()
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1)#同意
        __win1 = self.driver.current_window_handle
        self.click_by_names("butViewTranceInfo")#点审核意见
        self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win1:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(__win1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过'][name='passBtn']")
        self.alert_acc()
        # self.isWintwo()
        for h in self.driver.window_handles:
            if h!= __win1:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(__win1)
        time.sleep(1.5)
        self.driver.switch_to.default_content()
        # self.swich2frame("name","mainFrame")
       
        print("zhuxiaoshenhe" + "\t")

    def zhuxiaoshenhe1(self):
        self.driver.get(URL_)
        self.driver.switch_to.default_content()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"立案注销审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 立案注销审核 >> 待处理任务查询\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.send_by_css("input[name='GwWfLogDtoContractNo']",self.result_txt.get("报案号"))
        self.click_by_names("buttonQuery")
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_csss("a[href='#']",0)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        Select(self.driver.find_element_by_name("NotionContent")).select_by_index(1)#同意
        __win1 = self.driver.current_window_handle
        self.click_by_css("input[value='审核意见'][name='butViewTranceInfo']")#点审核意见
        # self.isWintwo()
        for h in self.driver.window_handles:
            if h != __win1:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(__win1)
        self.driver.switch_to.default_content()
        self.swich2frame("name","mainFrame")
        self.click_by_css("input[value='审核通过'][name='passBtn']")
        self.alert_acc()
        # self.isWintwo()
        for h in self.driver.window_handles:
            if h!= __win1:
                self.driver.switch_to.window(h)
                time.sleep(1)
                self.driver.close()
                time.sleep(1)
        self.driver.switch_to.window(__win1)
        time.sleep(1)
        self.driver.switch_to.default_content()

        # self.swich2frame("name","mainFrame")
        print("zhuxiaoshenhe1" + "\t")
        # try:
        #     zhuxiaoshenhe1_text = self.driver.find_element_by_css_selector(".tishi").text
        #     print(getfunname() + "\t" + zhuxiaoshenhe1_text[-5:-1])
        # except:
        #     print(getfunname() + "\t")

        self.driver.quit()

    def run(self):
        print("<--start-" + time.ctime() + "->")
        killie2()
        self.baoan()
        self.lianzhuxiao()
        self.zhuxiaoshenhe()
        self.zhuxiaoshenhe1()

class CheXian_PiGai_关系人投保人(SelenFun):
    def __init__(self, baodan):
        self.baodan = baodan

    def pigaishenqin(self):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % HXTB)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % uat_PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        self.alert_acc()

        time.sleep(3)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[8].click();")
        time.sleep(3)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"承保子系统\"]")
        self.click_by_css("a[title=\"批改管理\"]")
        self.click_by_css("a[title=\"承保子系统 >> 批改管理 >> 批改申请处理\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.send_by_names("PolicyNo", self.baodan)
        self.driver.find_element_by_xpath("//input[@value='下一步']").click()
        time.sleep(2)
        Select(self.driver.find_element_by_name("endorType")).select_by_value("35")
        self.click_by_names("target_select")
        self.driver.find_element_by_xpath("//input[@value='下一步']").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.swich2frame("id", "myFrame")
        time.sleep(5)
        # 修改地址
        # 滑动
        element_target = self.driver.find_element_by_name("AppliGuRelatedPartyInsuredAddress")
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element_target)

        Address = self.driver.find_element_by_name("AppliGuRelatedPartyInsuredAddress")
        Address.clear()
        Address.send_keys("我是新地址"+random_num(10))
        # 配送信息
        self.driver.find_element_by_name("buttonCourierInfoCollect").click()
        self.driver.find_element_by_xpath("//input[@value='关闭']").click()
        # 保存
        self.driver.find_element_by_name("saveButton").click()
        time.sleep(3)
        self.alert_acc()
        time.sleep(3)

        #  险种信息
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.driver.find_elements_by_id("myTD")[2].click()
        time.sleep(5)
        self.swich2frame("id", "myFrame")
        self.swich2frame("name", "RiskFrame")
        self.swich2frame("id", "myFrame")

        # 交强险
        self.driver.find_element_by_name("CalculateMotorOth").click()
        time.sleep(8)
        self.alert_acc()
        time.sleep(5)
        # 商业险
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.swich2frame("id", "myFrame")
        self.click_by_css("input[name='button_Risk_Open'][tabIndex='7']") #商业险详细信息
        time.sleep(5)
        self.swich2frame("name", "RiskFrame")
        self.swich2frame("id", "myFrame")
        self.driver.find_element_by_name("CalculateMotorOth").click()
        time.sleep(8)
        self.alert_acc()
        time.sleep(10)
        # 批文信息
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.driver.find_elements_by_id("myTD")[4].click()
        time.sleep(5)
        self.swich2frame("id", "myFrame")
        # self.driver.find_elements_by_id("GuEndorTextEndorseTextByInput'")[0].send_keys("这个鬼批文"+random_num(10))
        # self.driver.find_elements_by_id("GuEndorTextEndorseTextByInput'")[1].send_keys("这个鬼批文"+random_num(10))

        element_target = self.driver.find_element_by_name("saveButton")
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element_target)
        self.driver.find_element_by_name("saveButton").click()
        time.sleep(5)
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")

        self.driver.find_element_by_name("Save").click()
        time.sleep(2)
        try:
            self.driver.find_element_by_name("buttonAuthentiCode").click()
            time.sleep(25)
        except:
            pass

        try:
            self.driver.find_element_by_xpath("//div[@id='ConfirmMsg']/table/tbody/tr/td/input[@value='确定']").click()
        except:
            pass
        # 获取批单申请号
        pdsqh = self.driver.find_element_by_xpath("//body/form/table/tbody/tr/td").text
        self.pdsqh = re.sub("\D", "", pdsqh)
        self.driver.quit()

    def 双核审核(self):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % HEUN5)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        time.sleep(3)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[3].click();")
        time.sleep(3)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name", "leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"核保审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 核保审核 >> 任务处理\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.driver.find_element_by_name("GwWfLogDtoBusinessNo").send_keys(self.pdsqh)
        # self.driver.find_element_by_name("GwWfLogDtoBusinessNo").send_keys("2640120136020190000028")
        self.driver.find_element_by_name("buttonQuery").click()
        time.sleep(1)
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        time.sleep(3)
        two_key("alt", "f4")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.swich2frame("id", "myFrame")
        Select(self.driver.find_element_by_name("NotionContent")).select_by_value("1")
        self.driver.find_element_by_name("passBtn").click()
        time.sleep(2)
        self.alert_acc()
        two_key("alt", "f4")
        time.sleep(1)
        self.driver.find_element_by_name("passBtn").click()
        time.sleep(2)
        self.alert_acc()
        time.sleep(15)

    def run(self):
        print("<--start-" + time.ctime() + "->")
        killie2()
        self.pigaishenqin()
        self.双核审核()

class CheXian_PiGai_全单退保(SelenFun):
    def __init__(self, baodan):
        self.baodan = baodan

    def pigaishenqin(self):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % HXTB)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % uat_PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        self.alert_acc()
        time.sleep(3)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[8].click();")
        time.sleep(3)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name","leftFrame")
        self.click_by_css("a[title=\"承保子系统\"]")
        self.click_by_css("a[title=\"批改管理\"]")
        self.click_by_css("a[title=\"承保子系统 >> 批改管理 >> 批改申请处理\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.send_by_names("PolicyNo", self.baodan)
        self.driver.find_element_by_xpath("//input[@value='下一步']").click()
        time.sleep(2)
        Select(self.driver.find_element_by_name("endorType")).select_by_value("16")
        self.click_by_names("target_select")
        time.sleep(2)
        Select(self.driver.find_element_by_name("endorType")).select_by_value("16")
        self.click_by_names("target_select")
        self.driver.find_element_by_xpath("//input[@value='下一步']").click()
        time.sleep(10)
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")

        TBRname  = self.driver.find_element_by_xpath("//body/form/table[2]/tbody/tr[2]/td[4]/input").text
        print(TBRname)
        self.driver.find_element_by_name("butn").click()
        self.driver.switch_to.default_content()
        time.sleep(15)
        self.swich2frame("name", "mainFrame")
        # 滑动到提交核保
        element_target = self.driver.find_element_by_xpath("//input[@value='提交核保']")
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element_target)
        time.sleep(5)

        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")

        self.driver.find_element_by_name("adjustmentFeePayeeBankAccountName").send_keys("刘煜辉")


        time.sleep(2)
        self.driver.find_element_by_name("adjustmentFeeAccountNo").send_keys("112233445566")

        adjustmentFeePayeeBankProvinceCode = self.driver.find_element_by_name("adjustmentFeePayeeBankProvinceCode")
        ActionChains(self.driver).double_click(adjustmentFeePayeeBankProvinceCode).perform()
        time.sleep(2)
        self.driver.find_element_by_name("adjustmentFeePayeeBankProvinceCode").send_keys(Keys.ENTER)
        self.driver.find_element_by_name("adjustmentFeePayeeBankProvinceCode").send_keys(Keys.ENTER)

        adjustmentFeePayeeBankCityCode = self.driver.find_element_by_name("adjustmentFeePayeeBankCityCode")
        ActionChains(self.driver).double_click(adjustmentFeePayeeBankCityCode).perform()
        time.sleep(2)
        self.driver.find_element_by_name("adjustmentFeePayeeBankCityCode").send_keys(Keys.ENTER)
        self.driver.find_element_by_name("adjustmentFeePayeeBankCityCode").send_keys(Keys.ENTER)

        adjustmentFeePayeeBankCode = self.driver.find_element_by_name("adjustmentFeePayeeBankCode")
        ActionChains(self.driver).double_click(adjustmentFeePayeeBankCode).perform()
        time.sleep(2)
        self.driver.find_element_by_name("adjustmentFeePayeeBankCode").send_keys(Keys.ENTER)
        self.driver.find_element_by_name("adjustmentFeePayeeBankCode").send_keys(Keys.ENTER)

        self.driver.find_element_by_xpath("//input[@value='提交核保']").click()
        time.sleep(2)
        self.alert_acc()
        time.sleep(1)
        try:
            self.driver.find_element_by_name("buttonAuthentiCode").click()
            time.sleep(20)
        except:
            pass
        # time.sleep(10)
        self.alert_acc()

        pdsqh = self.driver.find_element_by_xpath("//body/form/table/tbody/tr/td").text
        self.pdsqh = re.sub("\D", "", pdsqh)
        print(self.pdsqh)
        self.driver.quit()

        # self.swich2frame("id", "myFrame")
        # time.sleep(5)
        # # 修改地址
        # # 滑动
        # element_target = self.driver.find_element_by_name("AppliGuRelatedPartyInsuredAddress")
        # self.driver.execute_script("arguments[0].scrollIntoView(false);", element_target)
        #
        # Address = self.driver.find_element_by_name("AppliGuRelatedPartyInsuredAddress")
        # Address.clear()
        # Address.send_keys("我是新地址"+random_num(10))
        # # 配送信息
        # self.driver.find_element_by_name("buttonCourierInfoCollect").click()
        # self.driver.find_element_by_xpath("//input[@value='关闭']").click()
        # # 保存
        # self.driver.find_element_by_name("saveButton").click()
        # time.sleep(3)
        # self.alert_acc()
        # time.sleep(3)
        #
        # #  险种信息
        # self.driver.switch_to.default_content()
        # self.swich2frame("name", "mainFrame")
        # self.driver.find_elements_by_id("myTD")[2].click()
        # time.sleep(5)
        # self.swich2frame("id", "myFrame")
        # self.swich2frame("name", "RiskFrame")
        # self.swich2frame("id", "myFrame")
        #
        # # 交强险
        # self.driver.find_element_by_name("CalculateMotorOth").click()
        # time.sleep(8)
        # self.alert_acc()
        # time.sleep(5)
        # # 商业险
        # self.driver.switch_to.default_content()
        # self.swich2frame("name", "mainFrame")
        # self.swich2frame("id", "myFrame")
        # self.click_by_css("input[name='button_Risk_Open'][tabIndex='7']") #商业险详细信息
        # time.sleep(5)
        # self.swich2frame("name", "RiskFrame")
        # self.swich2frame("id", "myFrame")
        # self.driver.find_element_by_name("CalculateMotorOth").click()
        # time.sleep(8)
        # self.alert_acc()
        # time.sleep(10)
        # # 批文信息
        # self.driver.switch_to.default_content()
        # self.swich2frame("name", "mainFrame")
        # self.driver.find_elements_by_id("myTD")[4].click()
        # time.sleep(5)
        # self.swich2frame("id", "myFrame")
        # # self.driver.find_elements_by_id("GuEndorTextEndorseTextByInput'")[0].send_keys("这个鬼批文"+random_num(10))
        # # self.driver.find_elements_by_id("GuEndorTextEndorseTextByInput'")[1].send_keys("这个鬼批文"+random_num(10))
        #
        # element_target = self.driver.find_element_by_name("saveButton")
        # self.driver.execute_script("arguments[0].scrollIntoView(false);", element_target)
        # self.driver.find_element_by_name("saveButton").click()
        # time.sleep(5)
        # self.driver.switch_to.default_content()
        # self.swich2frame("name", "mainFrame")
        #
        # self.driver.find_element_by_name("Save").click()
        # time.sleep(2)
        # try:
        #     self.driver.find_element_by_xpath("//div[@id='ConfirmMsg']/table/tbody/tr/td/input[@value='确定']").click()
        # except:
        #     pass
        # # 获取批单申请号
        # pdsqh = self.driver.find_element_by_xpath("//body/form/table/tbody/tr/td").text
        # self.pdsqh = re.sub("\D", "", pdsqh)
        # self.driver.quit()

    def 双核审核(self):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.driver.get(URL_)
        self.driver.execute_script("document.getElementById('username').setAttribute('value','%s');" % HEUN5)
        self.driver.execute_script("document.getElementById('password').setAttribute('value','%s');" % PW)
        self.driver.execute_script("document.getElementById('logonsubmit').click();")
        time.sleep(3)
        self.driver.execute_script("var a = document.getElementsByTagName('a');a[3].click();")
        time.sleep(3)
        self.driver.close()
        while len(self.driver.window_handles) < 2:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            break
        self.driver.maximize_window()
        self.swich2frame("name", "leftFrame")
        self.click_by_css("a[title=\"审核平台子系统\"]")
        self.click_by_css("a[title=\"核保审核\"]")
        self.click_by_css("a[title=\"审核平台子系统 >> 核保审核 >> 任务处理\"]")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.driver.find_element_by_name("GwWfLogDtoBusinessNo").send_keys(self.pdsqh)
        # self.driver.find_element_by_name("GwWfLogDtoBusinessNo").send_keys("2640120136020190000028")
        self.driver.find_element_by_name("buttonQuery").click()
        time.sleep(1)
        self.swich2frame("name", "QueryResultFrame")
        self.click_by_css("a[href='#']")
        time.sleep(3)
        two_key("alt", "f4")
        self.driver.switch_to.default_content()
        self.swich2frame("name", "mainFrame")
        self.swich2frame("id", "myFrame")
        Select(self.driver.find_element_by_name("NotionContent")).select_by_value("1")
        self.driver.find_element_by_name("passBtn").click()
        time.sleep(2)
        self.alert_acc()
        two_key("alt", "f4")
        time.sleep(1)
        self.driver.find_element_by_name("passBtn").click()
        time.sleep(2)
        self.alert_acc()
        time.sleep(13)

    def run(self):
        print("<--start-" + time.ctime() + "->")
        killie2()
        self.pigaishenqin()
        self.双核审核()


if __name__ == '__main__':

    gps = "gpsasdfd"

    # for i in range(len(_baodanhao)):
    m = 0
    i  = 0
    while True:
        # if m == len(_baodanhao):
        if m == 4:
            break
        try:
            m += 1

            # print("保单号", _baodanhao[0])
            # CheXian_LiPei(_baodanhao[i]).run()
            # CheXian_ZhuXiao(_baodanhao[i]).run()
            # CheXian_ChongKai(_baoanhao[i]).run("JQ")
            # print(_baodanhao[i])
            CheXian_PiGai_关系人投保人(_baodanhao[0]).run()
            # CheXian_PiGai_全单退保(_baodanhao[i]).run()
            print("第%s次" % (m), _baodanhao[i])
            i += 1

        except:
            # pass
            os.system('taskkill /f /im iexplore.exe')
            os.system('taskkill /f /im IEDriverServer.exe')
