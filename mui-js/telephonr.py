## -*- coding:utf-8 -*- bsb123456
##**caseId=手机银行_账户信息查询_账户信息查询流程001 
##**expectedResult={expectedResult2}   
##**intent={intent2}    
#procedure=
##**imagePath=D:\\xueersiAgent1.6.0通用版(接口&UI&手机)\\execute/result/image/手机银行_微信银行_账户查询对比(安卓)/手机银行_账户信息查询_账户信息查询流程001
from fractions import Fraction
import os, platform, sys, logging, time, subprocess, re, decimal, pickle, threading,multiprocessing,decimal,json,time
from decimal import Decimal
from PIL import Image
# driver持久化包

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for mobile
from appium.webdriver.mobilecommand import MobileCommand
from selenium.webdriver.support.ui import Select
# 窗口操作
# import win32api,win32con,win32gui,tempfile, shutil,pymysql
#from PIL import Image
sep = os.path.sep  #当前系统分隔符
PATH = lambda p: os.path.abspath(
            os.path.join(os.path.dirname(__file__), p)
    )
timeout = 20
global logger,path
# path="D:\\jettpack"
path="/home/robot/"
path=path.replace("\\",sep)
monkeyPath=path+"/.."
UserName = infoTable = model = ifInstallMonkey = ifRunMonkey = None
import platform
s_hc=platform.platform()
if "indows" in s_hc:
    #print("windows")
    # 创建一个logger  
    open(path+'/processLog.txt', 'w')  
    logger = logging.getLogger("pyLogging")   
    logger.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件    
    fh = logging.FileHandler(path+'/processLog.txt')  
    # 定义handler的输出格式formatter    
    formatter = logging.Formatter('%(message)s')  
    fh.setFormatter(formatter)  
    # 给logger添加handler    
    logger.addHandler(fh)
else:
    #print("mac")
    # 创建一个logger  
    # open(path+'/processLog.txt', mode='wt', buffering=1, encoding='gbk', errors=None, newline="\n", closefd=True, opener=None)
    open(path+'/processLog.txt', mode='wt', buffering=1, encoding='gbk', errors=None, newline="\n", closefd=True, opener=None)
    logger = logging.getLogger("pyLogging")
    logger.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件    
    fh = logging.FileHandler(path+'/processLog.txt',encoding='gbk')  
    # 定义handler的输出格式formatter    
    formatter = logging.Formatter('%(message)s')  
    fh.setFormatter(formatter)  
    # 给logger添加handler    
    logger.addHandler(fh)

class FileTools(): 
    global s1
    s1=[]
    def __init__(self,file):
        self.filepath=file
        
    #monkey日志
    def fileOperationMonkey(self):
        fo = open('C:/Users/Public/Documents/monkeyResult.txt', mode='rt',encoding='gbk', errors=None, newline="\n", closefd=True, opener=None)
        while True:
            s = fo.readline()
            s1.append(s)
            if not s:
                break
        fo.close()
    def fileWrite(self):
        fi2=open(self.filepath+'/importantLog.txt', mode='wt', buffering=1, encoding='gbk', errors=None, newline="\n", closefd=True, opener=None)
        if (s1!=None):
            for line in s1:
               logger.info(line)
        if platform.system() == 'Windows' and os.path.exists(self.filepath+'/importantLog.txt') and model!=None:
            fi2.write("设备型号是： "+str(model)+"\n")
        if ifRunMonkey=="1":
            fi2.write("monkey详细日志路径："+path[:-8]+"/Monkey.log ")
        fi2.close()

    def fileSplice(self):  
        if ifRunMonkey=="1":
            self.fileOperationMonkey()
        self.fileWrite()
            
class scriptError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
 
class FunctionLibrary():
    def excepTion(function):
        """
        异常装饰器，用来替代try except
        """
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                # log the exception
                funcName = function.__name__
                self = args[0]
                #组装异常信息
                paramsStr = "--".join([str(v) for k,v in enumerate(args) if k>0])
                x = "[Error]:"+funcName+"--"+paramsStr+"  [异常信息：%s]"%repr(e)
                if funcName != "get_screen" and funcName != "takeTakesScreenshot":
                    #当异常信息不是来自于截图的时候才进行截图，防止因截图异常而引起死循环
                    if "indows" in s_hc:
                        time.sleep(1)
                        self.takeTakesScreenshot("异常截图",funcName)
                    else:
                        time.sleep(1)
                        self.takeTakesScreenshot("异常截图",funcName)
                        #self.get_screen("异常截图"+funcName)
                self.quitDriver("1")
                #删除driver.ini文件
                # re-raise the exception
                raise scriptError(x)
        return wrapper

    def log(self,msg):
        logger.info(msg)
    def back(self):
        #返回上一步，一般情况下连续按两次为退出程序，请注意
        self.driver.back()
    def quitDriver(self,isDel="1"):
        #当isDel传值为1或者没有传值时说明程序发生异常
        #此时删除driver持久化的文件
        if isDel != "0":
            try:
                os.remove(self.tempPath)
            except:
                pass
            self.driver.quit()
            
            
    def loadingWait(self):
        a = 0
        platformFlag = 1
        if platform.system() == 'Windows':
            platformFlag = 0
        while 1:
            a+=1
            try:
                if (platformFlag == 0):
                    if (self.driver.find_element_by_name("请您稍候...").is_displayed() == True):
                        time.sleep(1)
                    else:
                        break
                else:
                    if (self.driver.find_element_by_name("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]").is_displayed() == True):
                        time.sleep(1)
                    else:
                        break
            except Exception:
                    break
            if a > 80:
                break 
    @excepTion
    def mem(self,memKey,memValue):
        contentMap = {}
        fileName = path+'/tempData.txt'
        try:

            if not os.path.exists(fileName):
                self.getFile(fileName,'wt+')
            file=self.getFile(fileName,'rt+')
            '''
            lines=file.readlines();
            for line in lines:
                key_value=line.split("$-----$")
                contentMap[key_value[0]]=key_value[1]
            '''
            line = file.readline().strip('\r\n')             
            while line: 
                key_value=line.split("$-----$")
                contentMap[key_value[0]]=key_value[1]
                line = file.readline().strip('\r\n') 
            if memKey in contentMap:
                del contentMap[memKey]
            file.close()
            if os.path.exists(fileName):
                os.remove(fileName)
            contentMap[memKey]  =  memValue
            file=self.getFile(fileName,'wt+') 
            for key in contentMap.keys():
                file.write(key+'$-----$'+contentMap[key]+'\r\n')     
            file.close()
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("异常截图")
            self.quitDriver("1")
            raise scriptError(funcName+'----'+memKey+'--'+memValue+'----异常')
    @excepTion
    def takeTakesScreenshot(self,fileName,funcName = ''):
        '''
        截图函数
        '''
        from PIL import Image

        #self.loadingWait()
        path = self.url+"%sresult%simage%s手机银行_微信银行_账户查询对比(安卓)%s手机银行_账户信息查询_账户信息查询流程001"%(sep,sep,sep,sep)
        print(path)
        self.num+=1
        if 1<=self.num<10:
            line="00"+str(self.num)
        elif 10<=self.num<100:
            line="0"+str(self.num)
        elif 100<=self.num<1000:
            line=str(self.num)
        if not os.path.exists(path):
            os.makedirs(path)
        self.driver.get_screenshot_as_file(path+sep+line+fileName+str(time.time())+".png")
        #img=Image.open(path+"/"+self.desired["threadName"][:3]+line+fileName+".png")
        # img=img.transpose(Image.ROTATE_90)
        # img=img.save(path+"/"+self.desired["threadName"][:3]+line+fileName+".png")
    @excepTion
    def ClickByXpath(self,xpath):
        '''
        根据xpath点击
        '''
        #element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element= self.driver.find_element_by_xpath(xpath)
        element.click()
    @excepTion
    def ClickByName(self,name):
        '''
        根据name点击
        '''
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, name))).click()
    @excepTion
    def ClickByID(self,id):
        '''
        根据id点击
        '''
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, id))).click()
    @excepTion
    def ClickByDesc(self,desc):
        '''
        根据content-desc点击
        '''
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ACCESSIBILITY_ID, desc)))
        el.click()
    @excepTion
    def ClickByUiauto(self,Uiauto):
        '''
        根据uiselector点击
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ANDROID_UIAUTOMATOR, Uiauto)))
        el.click()
        '''
        self.driver.find_element_by_android_uiautomator(Uiauto).click()
    @excepTion
    def ClickByClassName(self,className):
        '''
        根据classname点击
        '''
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, className)))
        el.click()
    @excepTion
    def ClickByLinkText(self,linkText):
        '''
        根据链接文字进行点击
        '''
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.LINK_TEXT, linkText)))
        el.click()
    @excepTion
    def SendKeysByID(self,Id,content):
        '''
        根据id发送内容
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, Id)))
        element.clear() 
        element.send_keys(content)
        '''
        element=self.driver.find_element_by_id(Id)
        element.clear() 
        element.send_keys(content)
    @excepTion
    def SendKeysByXpath(self,xpath,content):
        '''
        根据xpath发送内容
        '''
        #element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element= self.driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(content)
    @excepTion
    def SendKeysByName(self,name,content):
        '''
        根据name发送内容
        '''
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, name)))
        element.clear() 
        element.send_keys(content)
    @excepTion
    def SendKeysUseAdbInputText(self,content):
        '''
        安卓手机中使用adb进行输入
        '''
        for i in content:
            strCmd = 'adb -s %s shell input text "%s"'%(self.udid,content)
            subprocess.Popen(strCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.readlines()
    @excepTion
    def sendKeysByClassName(self,className,str):
        '''
        根据ClassName发送内容
        '''
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, className)))
        el.send_keys(str)
    @excepTion
    def SendKeysByUiauto(self,Uiauto,content):
        '''
        根据Uiauto发送内容
        '''
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ANDROID_UIAUTOMATOR, Uiauto)))
        el.send_keys(content)
    @excepTion
    def inputUseJsByID(self,Id,content):
        '''
        根据id，使用js填写内容
        '''
        js = 'var q=document.getElementById("%s");q.value = "%s"'%(Id,content)
        self.driver.execute_script(js)
    @excepTion
    def safeKeyBord_Video(self,pwd):
        self.getVideo()
        imagePath = self.safe_get_screenshot()
        #print(imagePath)
        for i in pwd:
            if i.isalpha():
                top_left = self.safeKeyBordClick_shot(imagePath,self.configPath,i)
                self.driver.tap([top_left,])
            if i.isnumeric():
                str = "123"
                top_left_123 = self.safeKeyBordClick_shot( imagePath,self.configPath,str)
                self.driver.tap([top_left_123,])
                #进入到字母键盘后截图
                #self.get_screenshot(resolution,firstDir)
                self.getVideo()
                self.safe_get_screenshot()
                #点击对应字母
                top_left = self.safeKeyBordClick_shot( imagePath,self.configPath,i)
                self.driver.tap([top_left,])
                #点击123，回到数字键盘
                top_left_ABC = self.safeKeyBordClick_shot( imagePath,self.configPath,"ABC")
                self.driver.tap([top_left_ABC])
                #返回数字键盘后截图
                #self.get_screenshot(resolution,firstDir)
                self.getVideo()
                self.safe_get_screenshot()
        end = "end"
        top_left_end = self.safeKeyBordClick_shot( imagePath,self.configPath,end)
        self.driver.tap([top_left_end,])
    @excepTion
    def waitID(self,id):
        '''
        等待某个ID出现，切换到新页面时填写，然后截图
        '''
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, id)))
    @excepTion
    def waitDESC(self,desc):
        '''
        等待某个ID出现，切换到新页面时填写，然后截图
        '''
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ACCESSIBILITY_ID, desc)))
    @excepTion
    def waitUiauto(self,Uiauto):
        '''
        等待某个ID出现，切换到新页面时填写，然后截图
        '''
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ANDROID_UIAUTOMATOR, Uiauto)))
    @excepTion
    def waitXPATH(self,xpath):
        '''
        等待某个XPATH出现，切换到新页面时填写，然后截图
        '''
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    @excepTion
    def waitNAME(self,name):
        '''
        等待某个ID出现，切换到新页面时填写，然后截图
        '''
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, name)))
    @excepTion
    def getAttrValByNAME(self,name,attr): 
        '''
        根据name找到控件

        attr字符串类型：
        name(返回 content-desc 或 text)
        text(返回 text)
        className(返回 class，只有 API=>18 才能支持)
        resourceId(返回 resource-id，只有 API=>18 才能支持)
        '''
        str =WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, name))).get_attribute(attr) 
        return str
    @excepTion
    def getAttrValByID(self,id,attr): 
        '''
        根据id找到控件

        attr字符串类型：
        name(返回 content-desc 或 text)
        text(返回 text)
        className(返回 class，只有 API=>18 才能支持)
        resourceId(返回 resource-id，只有 API=>18 才能支持)
        '''
        str =WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, id))).get_attribute(attr) 
        return str
    @excepTion
    def getAttrValByXPATH(self,xpath,attr): 
        '''
        根据xpath找到控件

        attr类型：
        name(返回 content-desc 或 text)
        text(返回 text)
        className(返回 class，只有 API=>18 才能支持)
        resourceId(返回 resource-id，只有 API=>18 才能支持)
        '''
        str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute(attr) 
        return str
    def ClickByTap(self,PX,PY):

        try:
            #self.loadingWait()
            #time.sleep(3)
            #self.driver.implicitly_wait(5)
            print("begin")
            self.driver.tap([(PX,PY)],200)
            
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.quitDriver("1")
            raise scriptError(funcName+"----异常")
    @excepTion
    #根据视频获取到密码键盘的截图
    def safe_get_screenshot(self):
        import cv2
        #从录屏中截取一帧图片
        
        vidcap = cv2.VideoCapture(self.SafeImagePath+'/'+'xueersi.avi')
        success,image = vidcap.read()
        count = 0
        #success = True
        #while success: 
        success,image = vidcap.read()
        print ('Read a new frame: ', success)
        cv2.imwrite(self.SafeImagePath+'/'+"frame%d.jpg" % count, image)
        self.get_screenshot2(self.configPath)
        #print(sss)path = "%s/conf/safeKeyBordTemplate/tempimage/"%firstDir
        return self.SafeImagePath+'/'+"frame%d.jpg" % count
    @excepTion
    #录制视频并将手机视频pull到电脑，默认目录是脚本执行的当前目录（可自定义目录）
    def getVideo(self):
        phonePath = '/sdcard/xueersi.avi'
        #recordCommand = 'adb shell screenrecord  --time-limit 1.5 ' + phonePath
        recordCommand = "adb -s "+self.udid+" shell screenrecord --time-limit 1 "+phonePath
        #执行录屏命令
        os.system(recordCommand)
        #将AVI视频pull到电脑（这里是我自己电脑的路径）
        outPullCommand = "adb  -s "+self.udid+" pull "+phonePath+" "+self.SafeImagePath 
        #print(outPullCommand)
        os.system(outPullCommand)
    @excepTion
    def safeKeyBordClick(self,imagePath,i):
        import cv2
        img = cv2.imread(imagePath,0)
        img2 = img.copy()
        template = cv2.imread(self.SafeImagePath+"/%s.jpg"%i,0)
        # 6 中匹配效果对比算法
        methods = ['cv2.TM_CCOEFF_NORMED']
        for meth in methods:
            img = img2.copy()
            method = eval(meth)
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = (min_loc[0],min_loc[1])
            else:
                top_left = (max_loc[0],max_loc[1])
        return top_left
    @excepTion
    def reduceAB(self,strA,strB):
        '''
        A-B
        '''
        num = str(Decimal(strA) - Decimal(strB))
        print(num)
        return num
    @excepTion
    def compareAandB(self,strA,strB):
        '''
        返回1则相等，返回0则不相等
        '''
        if strA == strB:
            print("比较值相等")
            return 1
        else:
            #print("比较值不相等")
            raise scriptError("比较值不相等")
    def addAB(self,strA,strB):

        num = Decimal(strA) + Decimal(strB)
        return num
    @excepTion
    def safeKeyBord_NUM(self, pwd):
        time.sleep(2)
        #self.getVideo()
        #imagePath = self.safe_get_screenshot()
        firstDir = self.configPath
        #imagePath = self.get_screenshot("360*640",firstDir)
        imagePath = self.safe_screenshot_shot(firstDir)
        for i in pwd:
            #top_left = self.safeKeyBordClick_shot(imagePath,self.configPath,"N_"+i)
            top_left = self.safeKeyBordClick_shot(imagePath, firstDir, "N_"+i)
            self.driver.tap([top_left,])
        time.sleep(1)
        top_left = self.safeKeyBordClick_shot(imagePath, firstDir, "Nend")
        self.driver.tap([top_left,])
    @excepTion
    def safeKeyBordClick_shot(self, imagePath, firstDir, i):
        import cv2
        
        img = cv2.imread(imagePath,0)
        #print(img)
        #img = cv2.imread('D:/eclipsespace/xueersi_app/python_script/src/conf/safeKeyBordTemplate/tempimage/1000main.png',0)
        img2 = img.copy()
        template = cv2.imread("%s/conf/safeKeyBordTemplate/%s.bmp"%(firstDir,i),0)
        # 6 中匹配效果对比算法
        methods = ['cv2.TM_CCOEFF_NORMED']
        # ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED',
                # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        
        for meth in methods:
            img = img2.copy()
            method = eval(meth)
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = (min_loc[0]*self.beishuX,min_loc[1]*self.beishuY)
            else:
                top_left = (max_loc[0]*self.beishuX,max_loc[1]*self.beishuY)
        return top_left
    @excepTion
    def get_screenshot2(self, firstDir):
        from PIL import Image
        path = "%s/conf/safeKeyBordTemplate/tempimage/"%firstDir

        #imagePath = path+"%smain.png"%self.desired["threadName"]
        #print(firstDir)
        mypath = "%s%sconf%ssafeKeyBordTemplate%stempimage%s"%(firstDir,sep,sep,sep,sep)
        imagePath = mypath+"frame0.jpg"
        #print(imagePath)
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            #self.driver.get_screenshot_as_file(imagePath)
            mainIm = Image.open(imagePath)
            mainW,mainH = mainIm.size
            im_ss = mainIm.resize((360,640))
        # im_ss = mainIm.convert('P')
            im_ss.save(imagePath)
            self.beishuX = mainW/360
            self.beishuY = mainH/640
            
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("安全键盘","异常截图",funcName)
            raise scriptError(funcName+"----异常")
        return imagePath
    @excepTion
    def GetCheckCode(self,phone):#phone
        try:
            from selenium import webdriver
            import platform
            #关闭保护模式
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True
            self.url = path
            PF = platform.system()
            if (PF =="Windows"):
                chser="C:\chromedriver.exe"
            else:#苹果
                chser="/Users/xueersi/chromedriver"
            option = webdriver.ChromeOptions()
            self.driverIE = webdriver.Chrome(chser,0,chrome_options=option)
            self.driverIE.maximize_window()
            self.driverIE.switch_to_window(self.driverIE.current_window_handle)
            self.driverIE.get("http://10.100.16.87:7001/smsif/terminal/frame.jsp")
            el1=WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.NAME, "branchId")))
            el1.clear()
            el1.send_keys("dztb")   #zhangqian0131  500
            el2=WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.NAME, "password")))
            el2.clear()
            el2.send_keys("123.com")
            
            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='center_submit']/div/img"))).click()

            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.ID, "code1")))
            print(444)
            self.driverIE.switch_to.default_content()
            self.driverIE.switch_to.frame("code1")
            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.ID, 'ygtvlabelel7'))).click()
            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.ID, 'ygtvlabelel8'))).click()
            self.driverIE.switch_to.default_content()
            self.driverIE.switch_to.frame("main")           
            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.NAME, "phone"))).send_keys(phone)
            
            WebDriverWait(self.driverIE, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='查询']"))).click()
            time.sleep(3)
            i=0
            while 1:
                try:
                    str = WebDriverWait(self.driverIE, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='queryListDiv']/table/tbody/tr[2]/td[5]/textarea"))).text
                except Exception:
                    pass
                #print(str[len(str)-29:len(str)-23])
                code = str[len(str)-29:len(str)-23]
                if(code!=None):
                    break
                else:
                    i+=1
                    if(i==20):
                        print("验证码没有找到！")
                        break
                    time.sleep(1)
                
            self.driverIE.quit()
            print(code)
            return code            
        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            self.quitDriver("1")
            raise scriptError(funcName+"查询验证码----异常")
    @excepTion
    def getFile(self,path,handle):
        file=open(path, mode=handle, 
           buffering=1, encoding='gbk', errors=None, 
           newline='\r\n', closefd=True, opener=None)
        return file
    @excepTion
    def safe_screenshot_shot(self, firstDir):
        from PIL import Image
        path = "%s/conf/safeKeyBordTemplate/tempimage/"%firstDir

        #imagePath = path+"%smain.png"%self.desired["threadName"]
        mypath = "%s%sconf%ssafeKeyBordTemplate%stempimage%s"%(firstDir,sep,sep,sep,sep)
        imagePath = mypath+"%s.png"%self.udid
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            self.driver.get_screenshot_as_file(imagePath)
            mainIm = Image.open(imagePath)
            mainW,mainH = mainIm.size
            im_ss = mainIm.resize((360,640))
        # im_ss = mainIm.convert('P')
            im_ss.save(imagePath)
            self.beishuX = mainW/360
            self.beishuY = mainH/640
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("安全键盘","异常截图",funcName)
            raise scriptError(funcName+"----异常")
        return imagePath  
    @excepTion
    def moneyReduceAB(self,strA,strB):
        from decimal import Decimal
        '''
        A-B
        '''
        strA2=strA.replace(",","")
        strB2=strB.replace(",","")
        num = str(Decimal(strA2) - Decimal(strB2))
        print(num)
        return num
    @excepTion
    def moneyCompareAandB(self,strA,strB):
        '''
        返回1则相等，返回0则不相等
        '''
        strA2=strA.replace(",","")
        strB2=strB.replace(",","")
        if strA2== strB2:
            print("比较值相等")
            return 1
        else:
            #print("比较值不相等")
            raise scriptError("比较值不相等")
    @excepTion
    def SendKeysByDesc(self,desc,content):
        '''
        根据desc发送内容
        '''
        element= WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ACCESSIBILITY_ID, desc)))
        element.clear() 
        element.send_keys(content)
    def swipeUP(self):
        try:
            x=self.driver.get_window_size()
            width=x["width"]
            height=x["height"]
            self.driver.implicitly_wait(4)
            self.driver.swipe(width/2, height*3/4, width/2, height/4, 1000)
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("异常截图",funcName)
            self.quitDriver("1")
            raise scriptError(funcName+"----异常")

    @excepTion
    def screenTapDriver(self,floatStartX,floatEndY):
        '''
        1440  0.11
        2560  0.3
        '''
        screen = self.driver.get_window_size()
        screenWidth = screen["width"]  #当前手机的宽度
        screenHeight = screen["height"]  #当前手机的高度
        #print(screenWidth)
        #print(screenHeight)
        #time.sleep(3)
        print("1")
        self.ClickByTap(screenWidth*floatStartX,screenHeight*floatEndY)
    @excepTion
    def  login(self,loginname,loginpwd):
        self.SendKeysByID("cn.com.xib.xibpb.v3:id/id_user_ipt",loginname) 
        self.log("[SendKeysByID==cn.com.xib.xibpb.v3:id/id_user_ipt=="+loginname+"==执行成功]")
        self.ClickByID("cn.com.xib.xibpb.v3:id/id_pwd_ipt") 
        self.log("[ClickByID==cn.com.xib.xibpb.v3:id/id_pwd_ipt==执行成功]")
        self.safeKeyBord(loginpwd)
        self.log("[safeKeyBord=="+loginpwd+"==执行成功]")
        self.ClickByName("登 录")
        self.log("[ClickByName==登 录==执行成功]")
        self.mem("login","13511112267") 
        self.log("[mem==login==13511112267==执行成功]")
        self.mem("pwd","207207") 
        self.log("[mem==pwd==207207==执行成功]")
        time.sleep(5)
    def webSetBrowser(self,browser,url):
        try:
            from selenium import webdriver
            #关闭保护模式
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True
            self.url = path
            self.num = 0
            ieser="C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"
            if browser == "ie":
                self.driver = webdriver.Ie(ieser)
            elif browser == "chrome":
                self.driver = webdriver.Chrome()
            else:
                #默认启动火狐浏览器
                self.driver = webdriver.Firefox()
            self.driver.maximize_window()
            self.driver.get(url)
        except Exception:
            funcName = sys._getframe().f_code.co_name
            raise scriptError(funcName+"--web driver init error--"+"----异常")
    @excepTion
    def switch_to_window(self,handleName):
        '''
        关闭当前window 窗口，转换到新窗口
        '''
        #self.driver.close();
        self.driver.switch_to_window(handleName)
    @excepTion
    def switchToAlertAccept(self):
        '''
        alert确定
        '''
        self.driver.switch_to_alert().accept()
    @excepTion
    def switchToAlertDismiss(self):
        '''
        alert取消
        '''
        self.driver.switch_to_alert().dismiss()
    @excepTion
    def switchToFrame(self,name):
        #切换到frame中

        #self.driver.switch_to.default_content()
        self.driver.switch_to.frame(name)
    @excepTion
    def switchToFrameDef(self):
        #切换到default_content中

        self.driver.switch_to.default_content()
    @excepTion
    def getAlertText(self):
        '''
        获取alert的text文字
        '''
        alertText = self.driver.switch_to_alert().text
        return alertText
    @excepTion
    def SendKeysByAlert(self,content):
        '''
        在alert输入框输入
        '''
        self.driver.switch_to_alert().send_keys(content)
    @excepTion
    def SendKeysByADB(self,content):
            #if(self.changToADB != 1):
            CommandADB = "adb shell ime set com.android.adbkeyboard/.AdbIME"
            os.system(CommandADB)
                #self.changToADB = 1
            Command = "adb shell am broadcast -a ADB_INPUT_TEXT --es msg  " +content
            os.system(Command)
    @excepTion
    def ClickTapByElementXOrY(self,by,value,change,percent,n=1):
        
            '''
            以by,value查找到的元素为基准，change 决定 x轴或y轴变化，percent另一个坐标轴按屏幕百分比点击
             
            '''
            if(by=="id"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, value)))
            elif(by=="name"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, value)))
            elif(by=="xpath"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, value)))
            #left = el.location['x']
            #top = el.location['y']
            x = el.location['x'] + el.size['width']*0.5
            y = el.location['y'] + el.size['height'] *0.5
            P=self.driver.get_window_size()
            width=P["width"]
            height=P["height"]

            if change=="y" or change=="Y" :
                for i in range(0,n):
                   self.driver.implicitly_wait(5)
                   self.ClickByTap(x,height*percent)

            if change=="x" or change=="X" :
                for i in range(0,n):
                   self.driver.implicitly_wait(5)
                   self.ClickByTap(width*percent,y)
    @excepTion
    def CheckByID(self,id):
        '''
        根据id
        '''
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, id)))
    @excepTion
    def CheckByName(self,name):
        '''
        根据name
        '''
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, name)))
    @excepTion
    def CheckByXpath(self,xpath):
        '''
        根据xpath
        '''
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
    @excepTion
    def ClickByText(self,text):
        '''
        根据text点击
        '''
       #print("//*[text()='"+text+"']")
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='"+text+"']"))).click()
    @excepTion    
    def getText(self,by,value): 

        if(by=="id"):
            str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, value))).text 
        elif(by=="name"):
            str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, value))).text 
        elif(by=="xpath"):
            str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, value))).text 
        elif(by=="css"):
            str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value))).text 
        return str
        '''
        if(by=="id"):
            str = self.driver.find_element_by_id(value).text 
        elif(by=="name"):
            str = self.driver.find_element_by_name(value).text 
        elif(by=="xpath"):
            str = self.driver.find_element_by_xpath(value).text   
        elif(by=="css"):
            str = self.driver.find_element_by_css_selector(value).text 
        return str
        '''
    @excepTion
    def swipeUPByADB(self,n):
        size_str = os.popen('adb shell wm size').read()
        if not size_str:
            print("请按装 ADB 及驱动并配置环境变量")
            sys.exit()
        #print(size_str)
        x=re.search(r'(\d+)x(\d+)',size_str)
        width=x.group(1)
        height=x.group(2)
        for i in range(0,n):
            Command = "adb shell input swipe " +str(int(width)/2)+" "  +str(int(height)*4/5)+" " +str(int(width)/2)+" "+ str(int(height)/5)
            os.system(Command)
        '''
        x=self.driver.get_window_size()
        width=x["width"]
        height=x["height"]
        self.driver.implicitly_wait(2)
        #self.driver.swipe(width/2, height*3/4, width/2, height/4, 1000)
        for i in range(0,n):
            Command = "adb shell input swipe " +str(width/2)+" "  +str(height*4/5)+" " +str(width/2)+" "+ str(height/5)
            os.system(Command)
        '''
    @excepTion
    def ScreenTapByJs(self,perX,perY,n):
            x = self.driver.get_window_size()
            width = x["width"]
            height = x["height"]
            for i in range(0,n):
                self.driver.execute_script('mobile:tap',{'x':perX*width,'y':perY*height});

    def ClickIfExist(self,by,value):
        try:
            if(by=="id"):
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.ID, value))).click()
            elif(by=="name"):
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.NAME, value))).click()
            elif(by=="xpath"):
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, value))).click()
        except Exception:
            pass

    def SendKeysIfExist(self,by,value,content):
        try:
            if(by=="id"):
                el = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.ID, value)))
            elif(by=="name"):
                el = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.NAME, value)))
            elif(by=="xpath"):
                el = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, value)))
            el.clear()
            el.send_keys(content)
        except Exception:
            pass
    @excepTion
    def swipeOnScreenN(self,Xstart,Ystart,Xend,Yend,n):
        '''
        size_str = os.popen('adb shell wm size').read()
        if not size_str:
            print("请安装 ADB 及驱动并配置环境变量")
            sys.exit()
        #print(size_str)
        x=re.search(r'(\d+)x(\d+)',size_str)
        width=x.group(1)
        height=x.group(2)
        '''
        for i in range(0,n):
            Command = "adb shell input swipe "+str(int(Xstart))+" "+str(int(Ystart))+" "+str(int(Xend))+" "+str(int(Yend))
            os.system(Command)
        '''
        try:
            x=self.driver.get_window_size()
            width=x["width"]
            height=x["height"]
            for i in range(0,n):
                #self.driver.implicitly_wait(5)
                time.sleep(1)
                self.driver.swipe(width*Xstart, height*Ystart, width*Xend, height*Yend, 1000)
        except Exception:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("异常截图",funcName)
            self.quitDriver("1")
            raise scriptError(funcName+"----异常")
        '''
    @excepTion
    def swipeDirectionByJs(self,Dir):#up/down/left/right
        self.driver.execute_script('mobile:scroll',{'direction':Dir});
    @excepTion
    def dragByJs(self,name,fromX,fromY,toX,toY,n):#up/down/left/right
        if(name==""):
            x = self.driver.get_window_size()
            width = x["width"]
            height = x["height"]
            for i in range(0,n):
                time.sleep(1)
                self.driver.execute_script('mobile:dragFromToForDuration',{'fromX':fromX*width,'fromY':fromY*height,'toX':toX*width,'toY':toY*height,'duration':0.5}); 

        else:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, name)))
            x=element.size['width']
            y=element.size['height']
            for i in range(0,n):
                time.sleep(1)
                self.driver.execute_script('mobile:dragFromToForDuration',{'element':element.id,'fromX':x*fromX,'fromY':y*fromY,'toX':x*toX,'toY':y*toY,'duration':0.5}); 

    @excepTion
    def switch_to_Webcontext(self):
        #print (self.driver.contexts)
        webcontext=self.driver.contexts[-1]
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "WEBVIEW_cn.com.cmbc.dbank"})
    @excepTion
    def switch_to_Appcontext(self):
        #print (self.driver.contexts)
        appcontext=self.driver.contexts[0]
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": appcontext})
    @excepTion
    def SendKeysByText(self,text,content):
        '''
        根据text点击
        '''
       #print("//*[text()='"+text+"']")
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='"+text+"']")))
        el.clear()
        el.send_keys(content)
    @excepTion
    def ClickByValue(self,value):
        '''
        根据text点击
        '''
       #print("//*[text()='"+text+"']")
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@value,'"+value+"')]"))).click()
    @excepTion
    def Scroll_TO_OEl_DEl(self,by1,value1,by2,value2):
        
            '''
            控件位置滚动 el 初始元素位置  el2 终点元素位置
             
            '''
            if(by1=="id"):
                el1 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, value1)))
            elif(by1=="name"):
                el1 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, value1)))
            elif(by1=="xpath"):
                el1 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, value1)))
                
            if(by2=="id"):
                el2 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, value2)))
            elif(by2=="name"):
                el2 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, value2)))
            elif(by2=="xpath"):
                el2 = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, value2)))
            self.driver.scroll(el1,el2)
    @excepTion
    def CheckByText(self,text):
        '''
        根据text点击
        '''
       #print("//*[text()='"+text+"']")
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='"+text+"']")))
    @excepTion
    def SwipeByElementXOrY(self,by,value,Unchange,start,end,n=1):
        
            '''
            以by,value查找到的元素为基准，Unchange 决定 x轴或y轴不变，另一个坐标轴按屏幕百分比滑动
             
            '''
            if(by=="id"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, value)))
            elif(by=="name"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.NAME, value)))
            elif(by=="xpath"):
                el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, value)))
            #left = el.location['x']
            #top = el.location['y']
            x = el.location['x'] + el.size['width']*0.5
            y = el.location['y'] + el.size['height'] *0.5
            P=self.driver.get_window_size()
            width=P["width"]
            height=P["height"]

            if Unchange=="y" or Unchange=="Y" :
                for i in range(0,n):
                   time.sleep(1)
                   self.driver.swipe(x, height*start, x, height*end, 1000)

            if Unchange=="x" or Unchange=="X" :
                for i in range(0,n):
                   time.sleep(1)
                   self.driver.swipe(width*start, y, width*end, y, 1000)
    @excepTion
    def AndroidLogin(self,loginName,password):
      #if(self.isLogin == 1):
        self.waitDESC("公司介绍")
        self.log("[waitDESC==公司介绍==执行成功]")
        self.screenTapDriver(0.75,0.1)               
        self.log("[screenTapDriver====执行成功]")
        self.ClickIfExist("name","更多") 
        self.log("[ClickIfExist==name==更多==执行成功]")
        self.screenTapDriver(0.5,0.99)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ACCESSIBILITY_ID, "请输入绑定的手机号码")))
            self.back()
            self.ClickIfExist("name","更多") 
            self.screenTapDriver(0.5,0.99)
        except Exception:
            pass 
        self.log("[screenTapDriver====执行成功]")
        self.SendKeysByDesc("请输入用户账号 ",loginName) 
        self.log("[SendKeysByDesc==请输入用户账号 ==851B161069==执行成功]")
        self.SendKeysByXpath("//android.view.View/android.widget.EditText[2]",password) 
        self.log("[SendKeysByID==//android.view.View/android.widget.EditText[2]==Wa33Wa33==执行成功]")
        self.ClickByDesc("登录 ") 
    @excepTion
    def IosLogin(self,loginName,password): 
      #if(self.isLogin == 1):
        self.waitNAME("公司介绍")
        self.log("[waitNAME==公司介绍==执行成功]")
        self.ScreenTapByJs(0.75,0.1,1) 
        self.log("[ScreenTapByJs====执行成功]")
        self.ClickIfExist("name","更多") 
        self.log("[ClickIfExist==name==更多==执行成功]")
        self.ScreenTapByJs(0.5,0.78,1) 
        self.log("[ScreenTapByJs====执行成功]")
        time.sleep(1)
        self.SendKeysByXpath("//*[1]//*[1]//*[1]//*[2]//*[1]//*[1]//*[3]//*[1]//*[2]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[3]",loginName) 
        self.log("[SendKeysByID==//*[1]//*[1]//*[1]//*[2]//*[1]//*[1]//*[3]//*[1]//*[2]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[3]==851B161069==执行成功]")
        self.ClickByName("完成")  
        self.log("[ClickByName==完成==执行成功]")
        self.SendKeysByXpath("//*[1]//*[1]//*[1]//*[2]//*[1]//*[1]//*[3]//*[1]//*[2]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[6]",password) 
        self.log("[SendKeysByID==//*[1]//*[1]//*[1]//*[2]//*[1]//*[1]//*[3]//*[1]//*[2]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[1]//*[6]==Wa33Wa33==执行成功]")
        self.ClickByName("完成")  
        self.log("[ClickByName==完成==执行成功]")
        self.ClickByName("登录") 
    @excepTion
    def AndroidLogin2(self,loginName,password):
      #if(self.isLogin == 1):
        self.waitDESC("公司介绍")
        self.log("[waitDESC==公司介绍==执行成功]")
        self.screenTapDriver(0.75,0.1)               
        self.log("[screenTapDriver====执行成功]")

        self.log("[SendKeysByDesc==请输入用户账号 ==851B161069==执行成功]")
        self.SendKeysByXpath("//android.webkit.WebView/android.webkit.WebView[1]/android.view.View[3]/android.widget.EditText[1]",password) 
        self.log("[SendKeysByID==//android.view.View/android.widget.EditText[2]==Wa33Wa33==执行成功]")
        self.ClickByDesc("登录 ") 
    @excepTion
    def safeKeyBord(self,pwd):
        self.getVideo()
        imagePath = self.safe_get_screenshot()
        #print(imagePath)
        for i in pwd:
            if i.isalpha():
                top_left = self.safeKeyBordClick_shot(imagePath,self.configPath,i)
                self.driver.tap([top_left,])
            if i.isnumeric():
                str = "123"
                top_left_123 = self.safeKeyBordClick_shot( imagePath,self.configPath,str)
                self.driver.tap([top_left_123,])
                #进入到字母键盘后截图
                #self.get_screenshot(resolution,firstDir)
                self.getVideo()
                self.safe_get_screenshot()
                #点击对应字母
                top_left = self.safeKeyBordClick_shot( imagePath,self.configPath,i)
                self.driver.tap([top_left,])
                #点击123，回到数字键盘
                top_left_ABC = self.safeKeyBordClick_shot( imagePath,self.configPath,"ABC")
                self.driver.tap([top_left_ABC])
                #返回数字键盘后截图
                #self.get_screenshot(resolution,firstDir)
                self.getVideo()
                self.safe_get_screenshot()
        end = "end"
        top_left_end = self.safeKeyBordClick_shot( imagePath,self.configPath,end)
        self.driver.tap([top_left_end,])
    @excepTion
    def safeKeyBord_NUM2(self, pwd):
        time.sleep(1)
        #self.getVideo()
        #imagePath = self.safe_get_screenshot()
        firstDir = self.configPath
        #imagePath = self.get_screenshot("360*640",firstDir)
        imagePath = self.safe_screenshot_shot(firstDir)
        for i in pwd:
            #top_left = self.safeKeyBordClick_shot(imagePath,self.configPath,"N2_"+i)
            top_left = self.safeKeyBordClick_shot(imagePath, firstDir, "N2_"+i)
            self.driver.tap([top_left,])
            time.sleep(0.5)
        top_left = self.safeKeyBordClick_shot(imagePath, firstDir, "N2_end")
        self.driver.tap([top_left,])
    @excepTion
    def swipeToRight(self,value):
        el=WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ACCESSIBILITY_ID, value)))
        scrolldict = {"direction": "right", 'element': el.id}
        self.driver.execute_script('mobile: swipe', scrolldict)
    @excepTion
    def ClickToJS(self,x,y):
        # 通过JS使用作用坐标进行点击
        self.driver.execute_script("mobile:tap", {"tapCount": 1, "touchCount": 1, "duration": 0.5, "x": x, "y": y})
    @excepTion
    def jsDoSwipe(self,x1,y1,x2,y2,duration = 0.5):
        """
        根据坐标滑动
        :param x1: 起始x
        :param y1: 起始y
        :param x2: 结束x
        :param y2: 结束y
        :param duration:滑动时长
        :return:
        """
        self.driver.execute_script("mobile: dragFromToForDuration",{"fromX":x1,"fromY":y1,"toX":x2,"toY":y2,"duration":duration})
    @excepTion
    def sendkeysmoneybsb(self, money):
        money1 = str(money)
        for i in money1:
            if i == '1':
                self.clickToJS(160, 390)
            elif i == '2':
                self.clickToJS(250, 390)
            elif i == '3':
                self.clickToJS(350, 390)
            elif i == '4':
                self.clickToJS(160, 450)
            elif i == '5':
                self.clickToJS(250, 450)
            elif i == '6':
                self.clickToJS(350, 450)
            elif i == '7':
                self.clickToJS(160, 510)
            elif i == '8':
                self.clickToJS(250, 510)
            elif i == '9':
                self.clickToJS(350, 510)
            elif i == '0':
                self.clickToJS(250, 570)
        self.clickToJS(650, 290)

    def safeKeyBord2(self, resolution, suffix, pwd):
        import cv2
        import aircv as ac
        '''
        :param resolution: 分辨率 宽*高
        :param suffix: 模板后缀名（所有模板要统一）
        :param initStatus:
        :param pwd:  字符串
        :return:
        '''
        # safeKeyBord操作安全键盘，根据需求修改这个
        filePathList = path.split("/")
        firstDir = "/".join(filePathList[:len(filePathList) - 1])
        imagePath = self.get_screenshot(resolution, firstDir)
        for i in pwd:
            top_left = self.safeKeyBordXY(imagePath, suffix, firstDir, i)
            # print(top_left)
            self.ClickToJS(top_left[0],top_left[1])
    def get_screenshot(self, resolution, firstDir):
        import cv2
        import aircv as ac
        # 安全键盘屏幕截图
        # 被safeKeyBord调用
        try:
            from fractions import Fraction
            from PIL import Image
            width = resolution.split("*")[0]  # 模板图片的宽
            height = resolution.split("*")[1]  # 模板图片的宽
            mypath = "%s/conf/safeKeyBordTemplate/tempimage/" % firstDir
            imagePath = mypath + "%s.png" % self.udid
            if not os.path.exists(path):
                os.makedirs(path)
            self.driver.get_screenshot_as_file(imagePath)
            # 当前图片
            mainIm = Image.open(imagePath)
            mainW, mainH = mainIm.size
            self.beishuX = Fraction(mainW / int(width))
            im_ss = mainIm.resize((int(width), int(height)))  # 将当前图片转换成和模板同等大小的图片
            # im_ss = mainIm.convert('P')
            im_ss.save(imagePath)
            return imagePath
        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("异常截图", funcName)
            self.quitDriver()
            raise scriptError("[Error]:" + funcName + "--" + firstDir + "  [异常信息：%s]" % repr(e))
    def safeKeyBordXY(self, imagePath, suffix, firstDir, i):
        import cv2
        import aircv as ac
        # safeKeyBordXY安全键盘获取坐标，被safeKeyBord调用
        try:
            # imagePath 正在运行的手机的图片
            templatePath = "%s/conf/safeKeyBordTemplate/%s.%s" % (firstDir, i, suffix)
            # 6 中匹配效果对比算法

            imsrc = ac.imread(imagePath)  # 原始图像
            imsch = ac.imread(templatePath)  # 带查找的部分
            cur_point = ac.find_template(imsrc, imsch)['result']  # 得到的是转换后的位置，需要转换成真实图片的坐标
            real_point = ac.find_template(imsrc, imsch)['result']  # 得到的是转换后的位置，需要转换成真实图片的坐标
            # cur_point = ac.find_template(imsrc, imsch)        # 得到的是转换后的位置，需要转换成真实图片的坐标
            # print(cur_point)
            # real_point = [i * self.beishuX for i in cur_point]
            # print(real_point)
        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            self.takeTakesScreenshot("异常截图", funcName)
            self.quitDriver()
            raise scriptError("[Error]:" + funcName + "  [异常信息：%s]" % repr(e))
        return real_point
    def js_DoSwipeUP(self,duration = 0.5):
        """
        根据坐标滑动
        :param x1: 起始x
        :param y1: 起始y
        :param x2: 结束x
        :param y2: 结束y
        :param duration:滑动时长
        :return:
        """
        x = self.driver.get_window_size()
        width = x["width"]
        height = x["height"]
        x = width / 2
        y1 = height * 0.8
        y2 = height * 0.2
        self.driver.execute_script("mobile: dragFromToForDuration",{"fromX":x,"fromY":y1,"toX":x,"toY":y2,"duration":duration})
    @excepTion
    def sendkeysBsbPhoneOrMoney(self,phoneOrMoney):
        value = str(phoneOrMoney)
        for i in value:
            if i == '1':
                self.ClickByDesc('1')
            elif i == '2':
                self.ClickByDesc('2')
            elif i == '3':
                self.ClickByDesc('3')
            elif i == '4':
                self.ClickByDesc('4')
            elif i == '5':
                self.ClickByDesc('5')
            elif i == '6':
                self.ClickByDesc('6')
            elif i == '7':
                self.ClickByDesc('7')
            elif i == '8':
                self.ClickByDesc('8')
            elif i == '9':
                self.ClickByDesc('9')
            elif i == '0':
                self.ClickByDesc('0')
            elif i == ".":
                self.ClickByDesc(".")
            else:
                self.ClickByDesc("N D N")
    def sendyzm(self,user='170523',pwd='abc@1234',tel='15810045207'):

        num = self.get_yzm(user=user,pwd=pwd,tel=tel)
        for i in str(num):
            if i == '1':
                self.ClickByDesc('1')
            elif i == '2':
                self.ClickByDesc('2')
            elif i == '3':
                self.ClickByDesc('3')
            elif i == '4':
                self.ClickByDesc('4')
            elif i == '5':
                self.ClickByDesc('5')
            elif i == '6':
                self.ClickByDesc('6')
            elif i == '7':
                self.ClickByDesc('7')
            elif i == '8':
                self.ClickByDesc('8')
            elif i == '9':
                self.ClickByDesc('9')
            elif i == '0':
                self.ClickByDesc('0')
            elif i == ".":
                self.ClickByDesc(".")
            else:
                self.ClickByDesc("N D N")
    @excepTion
    def get_yzm(self,user,pwd,tel):
        """
        获取验证码
        :param user: 用户名
        :param pwd: 密码
        :param tel: 手机号
        :return: 验证码
        """
        from selenium import webdriver
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.common.by import By
        driver = webdriver.Chrome("/Users/bsb/Downloads/chromedriver")
        driver.get("http://14.16.3.224:7001/msg/")
        # 输入用户名
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.ID,"tellerId")).send_keys(user)
        # 输入密码
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.ID,"password")).send_keys(pwd)
        # 点击登陆
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.CLASS_NAME,"login_button")).click()
        #
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.ID,"sideBar_Close_id_1")).click()
        #
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.LINK_TEXT,"下行信息发送查询")).click()
        #
        driver.switch_to.frame("MainIframe")
        #
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.ID,"address")).send_keys(tel)
        #
        # WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.ID,"tellerId")).send_keys("170523")
        #
        WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.CLASS_NAME,"search")).click()
        #
        ls = WebDriverWait(driver,timeout= 20,poll_frequency=0.5).until(lambda x:x.find_element(By.XPATH,'//*[@id="tableId"]/tbody/tr[2]/td[6]')).text
        print(ls)

        ls1 = str(ls).split(":")[1]

        print(ls1)

        num = str(ls1).split("。")[0]
        driver.quit()

        return num
    def selectTransactor(self,a):
        """
        选择办理人
        :param a: 
        :return: 
        """
        return a
    @excepTion
    def getPageSource(self):
        """
        获取当前屏幕内的元素并返回
        :return: 
        """
        pagefile = "./{}.txt".format("pagesource" + str(time.time()))
        with open(pagefile,"w") as f:
            # 保存当前屏幕内可见的元素结构
            f.write(self.driver.page_source)
        with open(pagefile,"r") as f:
            # 读取当前屏幕内的元素
            pagesource = f.read()
            return pagesource
    @excepTion
    def get_screen(self, image):
        # 截图名字
        _path = self.url + "%sresult%simage%s手机银行_微信银行_账户查询对比(安卓)%s手机银行_账户信息查询_账户信息查询流程001" % (sep, sep, sep, sep)
        if not os.path.exists(_path): os.makedirs(_path)
        imagePath = _path + "\\" + image + ".png"
        print(imagePath)
        self.driver.get_screenshot_as_file(imagePath)
    @excepTion
    def findElement(self, loc, timeout=60, poll=0.5):
        return WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(*loc))
    def moneyAB(self,moneyA,moneyB):
        """
        判断两个金额的大小
        :param moneyA: 
        :param moneyB: 
        :return: 
        """
        num = Decimal(moneyA) - Decimal(moneyB)
        return num
    @excepTion
    def clickElement(self,loc):
        """
        点击元素
        :param loc:
        :return:
        """
        self.findElement(loc).click()
    @excepTion
    def sendKeys(self,loc,text):
        """
        输入内容
        :param loc:
        :param text: 输入的文本
        :return:
        """
        input_text = self.findElement(loc)
        input_text.clear()
        input_text.send_keys(text)
    @excepTion
    def getElementText(self,loc):
        """
        获取文本
        :param loc:
        :return:
        """
        return self.findElement(loc).text
    @excepTion
    def getattribute(self,loc,value):
        """
        返回元素指定的属性值
        :param loc:
        :param value: 指定的属性
        :return:
        """
        return self.findElement(loc).get_attribute(value)
    @excepTion
    def assertAB(self,assertA,assertB):
        """
        断言
        :param assertA:
        :param assertB:
        :return:
        """
        assert assertA in assertB or assertA == assertB, "失败"
    @excepTion
    def assertAB2(self,assertA,assertB):
        """
        断言
        :param assertA:
        :param assertB:
        :return:
        """
        assert assertA >= assertB, "bug，卡内余额不能不大于等于交易金额"
    @excepTion
    def waitElement(self, by, value, timeout=60, poll=0.5):
        """
        等待元素出现
        :param by:
        :param value:
        :return:
        """
        WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of_element_located((by, value)))
    @excepTion
    def sendKeys(self,loc,text):
        """
        输入内容
        :param loc:
        :param text: 输入的文本
        :return:
        """
        if len(text) == 0:
            pass
        else:
            input_text = self.findElement(loc)
            input_text.clear()
            input_text.send_keys(text)
    @excepTion
    def clearEmail(self, loc):
        text = self.getElementText(loc)
        if len(text) > 0 and text != "输入邮箱":
            for i in text:
                self.findElement(loc).clear()
                self.ClickToJS(1020,760)
                text = self.getElementText(loc)
                if text == "输入邮箱":
                    break
        else:
            pass
    @excepTion
    def changeDataType(self,var):
        import decimal
        from decimal import Decimal
        decimal.getcontext().prec = len(var) - 2
        if "." in var:
            return Decimal(str(var).split("万")[0]) * 10000
        else:
            return Decimal(str(var).split("万")[0] + "0000")

    @excepTion
    def assertAB3(self,assertA,assertB):
        """
        断言
        :param assertA:
        :param assertB:
        :return:
        """
        assert assertA > assertB, "bug，交易金额不能不大于卡内余额"
    @excepTion
    def dragAndDrop(self, loc1, loc2, duration=0.5):
        """
        从一个元素滑动到另一个元素的位置，第二个元素取代第一个元素在屏幕上的位置。仅iOS可用
        :param loc1: （定位到的元素1）
        :param loc2: （定位到的元素2）
        :param duration: （滑动的时间）
        :return:
        """
        startX = self.getLocation(loc1).get('x')
        startY = self.getLocation(loc1).get('y')
        endX = self.getLocation(loc2).get('x')
        endY = self.getLocation(loc2).get('y')
        self.driver.execute_script("mobile: dragFromToForDuration", {"fromX": startX, "fromY": startY, "toX": endX, "toY": endY, "duration": duration})
    @excepTion
    def sendkeysBsbCardNumber(self,CardNumber):
        value = str(CardNumber)
        
        for i in value:
            self.getPageSource()
            
            if i == '1':
                self.ClickByDesc('1')
            elif i == '2':
                self.ClickByDesc('2')
            elif i == '3':
                self.ClickByDesc('3')
            elif i == '4':
                self.ClickByDesc('4')
            elif i == '5':
                self.ClickByDesc('5')
            elif i == '6':
                self.ClickByDesc('6')
            elif i == '7':
                self.ClickByDesc('7')
            elif i == '8':
                self.ClickByDesc('8')
            elif i == '9':
                self.ClickByDesc('9')
            elif i == '0':
                self.ClickByDesc('0')
            elif i == ".":
                self.ClickByDesc(".")
            else:
                self.ClickByDesc("N D N")
    @excepTion
    def sendKeysCardNumber(self,cardNumber):
        """
        输入卡号
        :param cardNumber: 
        :return: 
        """
        count = 1
        for i in str(cardNumber):
            self.ClickByDesc(i)
            if count == 15 or count >= 17:
                time.sleep(1)
                page = self.getPageSource2("卡号输入后的页面元素")
                if "确定" in page:
                    self.clickElement((By.ID, "确定"))
            count = count + 1
    @excepTion
    def getLocation(self, loc):
        """
        获取元素的坐标
        :param loc: 定位到的元素
        :return: 元素的坐标
        """
        return self.findElement(loc).location
    @excepTion
    def getPageSource2(self,pagefilename):
        """
        获取当前屏幕内的元素并返回
        :return: 
        """
        pagefile = "./{}.txt".format(pagefilename)
        with open(pagefile,"w") as f:
            # 保存当前屏幕内可见的元素结构
            f.write(self.driver.page_source)
        with open(pagefile,"r") as f:
            # 读取当前屏幕内的元素
            pagesource = f.read()
            return pagesource
    @excepTion
    def sendkeysDate(self, newyear, newmonth, newdate, locyear, locmonth, locdate):
        """
        包商银行日期控件输入日期
        :param newyear: 输入的年份（int类型）
        :param newmonth: 输入的月份（int类型）
        :param newdate: 输入的日（int类型）
        :param locyear: 控件上的年份属性
        :param locmonth: 控件上的月份属性
        :param locdate: 控件上的日属性
        :return: 
        """
        while True:
            yeartext = self.getElementText(locyear)
            year = str(yeartext).split("年")[0]
            if int(year) == int(newyear):
                break
            elif int(year) > int(newyear):
                self.ClickToJS(215, 395)
            else:
                self.ClickToJS(215, 455)
        while True:
            monthtext = self.getElementText(locmonth)
            month = str(monthtext).split("月")[0]
            if int(month) == int(newmonth):
                break
            elif int(month) > int(newmonth):
                self.ClickToJS(295, 395)
            else:
                self.ClickToJS(295, 455)

        while True:
            datetext = self.getElementText(locdate)
            date = str(datetext).split("日")[0]
            if int(date) == int(newdate):
                break
            elif int(date) > int(newdate):
                self.ClickToJS(365, 395)
            else:
                self.ClickToJS(365, 455)

    @excepTion
    def scrollBankBsb(self, bank, duration=0.1):
        """
        选择开户行控件的处理
        :param bank: 要选择的银行全名
        :param duration: 时间
        :return:
        """
        # 等待加载出现其他银行后获取页面元素
        self.waitElement(By.ID, "其他银行")
        openingbank = self.getPageSource2('开户行')
        # 如果要选择的银行在页面中点击要选择的银行
        if bank in openingbank:
            self.clickElement((By.XPATH, '//XCUIElementTypeStaticText[contains(@name,"{}")]'.format(bank)))
        # 不再页面中执行如下操作
        else:
            # 点击其他银行
            self.clickElement((By.ID, "其他银行"))
            # 等待页面加载
            self.waitElement(By.ID, "交通银行")
            # 循环执行以下操作
            while True:
                # 如果要选择的银行出现在页面中执行点击该银行
                if self.findElement((By.ID, "{}".format(bank))).is_displayed():
                    self.waitElement(By.ID, "{}".format(bank))
                    self.clickElement((By.ID, "{}".format(bank)))
                    # 判断是否成功点击选择的该银行（页面出现确认按钮则点击成功）
                    # 如果页面出现确认按钮：不执行任何操作
                    if self.findElement((By.ID, "确认")).is_displayed():
                        pass
                    # 如果未出现确认按钮：再次点击
                    else:
                        self.clickElement((By.ID, "{}".format(bank)))
                    # 点击要选择的银行后停止执行循环操作
                    break
                # 如果要选择的银行未出现在页面中：执行滑动操作
                else:
                    self.driver.execute_script("mobile: dragFromToForDuration",
                                               {"fromX": 315, "fromY": 569, "toX": 315, "toY": 219,
                                                "duration": duration})
    @excepTion
    def ClickTextA(self,String):
        self.driver.find_element_by_android_uiautomator('text("'+String+'")').click()
        time.sleep(2)
    @excepTion
    def Switch2Context(self):
        #print (self.driver.contexts)
        webcontext=self.driver.contexts[-1]
        self.driver.switch_to.context(webcontext)
        time.sleep(2)

    @excepTion
    def SendByCss(self,css,content):
        '''
        根据xpath发送内容
        '''
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.clear()
        element.send_keys(content)
    @excepTion
    def getMsg(self,requestIP,userName,passwd,tel):
        import requests
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP +"/msg/msgSendInfoQuery.action"
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
        #m = html.index("您本次签约绑定账号短信验证码:")
        m = html.index("您本次用于礼品兑换的短信验证码:")
        code = html[m+16:m+22]
        return code
    @excepTion
    def TouchTapA(self, x, y):
        #
        _CMD = "adb shell input tap {} {}".format(x,y)
        os.popen(_CMD)
        time.sleep(0.5)
    @excepTion
    def Clickkw(self, String):
        time.sleep(1)
        for i in String:
            print(i)
            self.driver.execute_script('$("a[data-val={}]").click()'.format(int(i)))
            time.sleep(0.5)
    @excepTion
    def YunGetCode(self):
        import datetime
        _result=""
        _time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')
        _sql = "select * from cpm.efwk_captcha where CREATEDAT >= {};".format(_time)
        print(_time)
        conn = ibm_db.connect("DATABASE=CPM;HOSTNAME=14.16.10.202;PORT=60000;PROTOCOL=TCPIP;UID=bsbview;PWD=U2bpQT5z;","","")
        if conn:
            stmt = ibm_db.exec_immediate(conn,sql)
            result = ibm_db.fetch_both(stmt)
            while (result):
                #print(result)
                _string = result
                result = ibm_db.fetch_both(stmt)
        print(_string.get("STRVALUE"))
        return _string.get("STRVALUE")
    @excepTion   
    def mobile_setConfig1(self,platformName,port,udid):
        try:
            from appium import webdriver 
            #self.desired=desired_caps 
            desired_caps={}
            self.url=path
            self.udid = udid
            self.platformName = platformName
            compare = "True"
            desired_caps["fullrReset"] = "false"
            desired_caps["noReset"] = "true"
            # 启用UNICODE输入，可以输入中文
            desired_caps["unicodeKeyboard"] = True
            desired_caps["resetKeyboard"] = True
            desired_caps["deviceName"] = self.udid
            desired_caps["platformName"] = platformName
            desired_caps["udid"] = udid
            desired_caps["url"] = "http://127.0.0.1:"+port     
            #desired_caps["app"] = os.path.dirname(self.url)+"/apps/{param1}"  
            desired_caps["appPackage"] = "com.tencent.mm"  
            desired_caps["appActivity"] = "com.tencent.mm.ui.LauncherUI"  
            desired_caps["bundleId"] = "com.yitong.SRCBBank"  
            desired_caps["platformVersion"] = "7.0"  
            desired_caps["platformName"] = "Android"
            desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}
            #conf文件目录
            filePathList = path.split(sep)
            self.configPath = sep.join(filePathList[:len(filePathList)-1])
            self.SafeImagePath = "%s/conf/safeKeyBordTemplate/tempimage"%self.configPath
            #conf文件目录
            self.tempPath = "%s%sconf%sdriver.ini"%(self.configPath,sep,sep)
            if not os.path.exists(self.tempPath):
                #如果持久化driver的文件不存在，就启动driver，然后保存driver
                self.driver = webdriver.Remote(desired_caps["url"]+"/wd/hub", desired_caps)
                f1 = open(self.tempPath,"wb")
                pickle.dump(self.driver,f1,0)
                f1.close()
                #是否登陆
                self.isLogin = 1
            else:
                #否则就从文件中将driver读取出来，如果发生异常，第一件事是删除文件
                f1 = open(self.tempPath,"rb")
                self.driver = pickle.load(f1)
                f1.close()
                time.sleep(1)
                self.isLogin = 0
            self.num=0
            #---截图对比用到的数据
            #self.screenShotNum = 0 #案例截图顺序
            #self.mainMobil = compare
            #self.transName = "APP-转账汇款-预约查询及撤销"
            #self.caseId = "App-IOS-转账汇款-预约查询撤销-0001"
            #self.track = "IOS-智能转账-10003-3"
            #ADB输入法设置标准 0 没用; 1  切换到ADB
            #self.changToADB = 0
            #---截图对比用到的数据end
            
        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            raise scriptError(funcName+"--"+"--driver init error--"+"--[异常信息]:%s"%repr(e))
    @excepTion
    def bsbLoginAndToOA(self):
        time.sleep(6)
        self.driver.find_element_by_android_uiautomator('text("订阅号消息")').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//android.widget.ImageButton[@content-desc=\"订阅号\"]").click()
        time.sleep(1)
        self.driver.find_element_by_android_uiautomator('text("wxid_i2ugr5cpmk4721的接…")').click()
        '''
        elOne = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ANDROID_UIAUTOMATOR, "text(\"订阅号消息\")")))
        elOne.click()
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, "订阅号"))).click()
        elTwo = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ANDROID_UIAUTOMATOR, 'text("wxid_i2ugr5cpmk4721的接…")')))
        elTwo.click()
        '''
    @excepTion
    def switch_to_Webcontext_S(self,contextStr):
        #print (self.driver.contexts)
        #webcontext=self.driver.contexts[-1]
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name":contextStr})
    @excepTion
    def ClickById_tapXY(self,ID):
        ele = self.driver.find_element_by_id(ID)
        #print(ele.text)
        xOne = ele.location['x']
        yOne = ele.location['y']
        widOne = ele.size['width']
        heiOne = ele.size['height']
        #1080 1920  360 574
        x = xOne + widOne * 0.5
        y = yOne + heiOne * 0.5
        #print("x: {} , y:{}".format(3*x,3*y))
        _CMD = "adb shell input tap {} {}".format(3*x,(3*y+198))
        os.popen(_CMD)
        time.sleep(3)
    @excepTion
    def ClickByXpath_tapXY(self,xpath):
        ele = self.driver.find_element_by_xpath(xpath)
        #print(ele.text)
        xOne = ele.location['x']
        yOne = ele.location['y']
        widOne = ele.size['width']
        heiOne = ele.size['height']
        #1080 1920  360 574
        x = xOne + widOne * 0.5
        y = yOne + heiOne * 0.5
        #print("x: {} , y:{}".format(3*x,3*y))
        _CMD = "adb shell input tap {} {}".format(3*x,(3*y+198))
        os.popen(_CMD)
        time.sleep(3)
    @excepTion
    def ClickByCss(self,css):
        '''
        根据css点击
        '''
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css))).click()
    @excepTion
    def getMsg_AddCard(self,requestIP,userName,passwd,tel):
        import requests
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP +"/msg/msgSendInfoQuery.action"
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
        m = html.index("您本次签约绑定账号短信验证码:")
        code = html[m+15:m+21]
        return code
    @excepTion
    def OperateByExecuteScript(self,value):
        # 通过Script进行点击等操作
        self.driver.execute_script(value)
    @excepTion
    def inputPSD_custom(self,pwd):
        for ch in pwd:
            xpathStr = "//XCUIElementTypeStaticText[@name=\""+ch+"\"]"
            #print("xpathStr:"+xpathStr)
            self.ClickByXpath(xpathStr)
        time.sleep(5)
    @excepTion
    def getMsgByKeyStr(self,requestIP,userName,passwd,tel,keyStr):
        import requests
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP +"/msg/msgSendInfoQuery.action"
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
        m = html.index(keyStr)
        m += len(keyStr)
        code = html[m:m+6]
        return code
    @excepTion
    def CheckTextAB(self,strA,strB):
        if strA is strB:
            logger.info("预期结果："+strA+" 与实际结果："+strB+" 一致")
        else:
            #print("比较值不相等")
            logger.info("预期结果："+strA+" 与实际结果："+strB+"不一致")
            raise scriptError("预期结果："+strA+" 与实际结果："+strB+" 不一致")
    @excepTion
    def SwipeFromEleOneToEleTwo(self,by1,value1,by2,value2):
        #获取第一个控件
        if(by1=="id"):
            elOne = self.driver.find_element_by_id(value1)
        elif(by1=="name"):
            elOne = self.driver.find_element_by_name(value1)
        elif(by1=="xpath"):
            elOne = self.driver.find_element_by_xpath(value1)
        elif(by1=="css"):
            elOne = self.driver.find_element_by_css_selector(value1)
        xOne = elOne.location['x']
        yOne = elOne.location['y']
        widOne = elOne.size['width']
        heiOne = elOne.size['height']
        x = xOne + widOne * 0.5
        y = yOne + heiOne * 0.5
        x1 = 3*x
        y1 = 3*y+198
        #获取第二个控件
        if(by2=="id"):
            elTwo = self.driver.find_element_by_id(value2)
        elif(by2=="name"):
            elTwo = self.driver.find_element_by_name(value2)
        elif(by2=="xpath"):
            elTwo = self.driver.find_element_by_xpath(value2)
        elif(by2=="css"):
            elTwo = self.driver.find_element_by_css_selector(value2)        
        xTwo = eleTwo.location['x']
        yTwo = eleTwo.location['y']
        widTwo = eleTwo.size['width']
        heiTwo = eleTwo.size['height']
        xx = xTwo + widTwo * 0.5
        yy = yTwo + heiTwo * 0.5
        x2 = 3*xx
        y2 = 3*yy+198
        Command = "adb shell input swipe "+str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)
        os.system(Command)
        #os.popen(_CMD)
        #self.driver.scroll(elOne,elTwo)
        time.sleep(3)
    @excepTion
    def SendKeysByCss(self,cssStr,content):
        '''
        根据css发送内容
        '''
        #element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element= WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, cssStr)))
        element.clear()
        element.send_keys(content)
    @excepTion
    def switch_to_context_index(self,index):
        print (self.driver.contexts)
        appcontext = self.driver.contexts[index]
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": appcontext})
    @excepTion
    def Next(self):
        '''

        :return:
        '''
        Next_Str = """
        var q = mui('button');
        q[0].addEventListener('tap',function(){});
        mui.trigger(q[0],'tap');
        """
        self.driver.execute_script(Next_Str)
    @excepTion
    def CheckTextA_B(self,strA,strB):
        if strA in strB:
            logger.info("预期结果："+strA+" 与实际结果："+strB+" 一致")
        else:
            #print("比较值不相等")
            logger.info("预期结果："+strA+" 与实际结果："+strB+"不一致")
            raise scriptError("预期结果："+strA+" 与实际结果："+strB+" 不一致")
    @excepTion
    def getMsg_danwei(self, requestIP, userName, passwd, tel):
        # 单位预约开户
        import requests
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
        m = html.index("您好，")
        code = html[m + 3:m + 9]
        return code
    @excepTion
    def SendUseJs(self, element,value):
        ''' Send value use jquery  '''

        self.driver.execute_script('$("{}").val("{}")'.format(element, value))
        time.sleep(0.5)
    @excepTion
    def setYuyue(self):
        # 预约日期 多一天
        import datetime
        TomorowDay = datetime.datetime.now() + datetime.timedelta(days=1)
        _val = TomorowDay.strftime("%Y.%#m.%d")
        print(_val)
        _jihuo = """
        var q = mui("#timepickerte");
        q[0].addEventListener("tap", function(){});
        mui.trigger(q[0], "tap");"""
        self.driver.execute_script(_jihuo)   # 输入值
        time.sleep(1)
        _queding ="""
        var o = mui(".mui-poppicker-btn-ok");
        o[0].addEventListener("tap",function(){});
        mui.trigger(o[0],"tap");"""
        self.driver.execute_script(_queding) # 点击确定
        time.sleep(1)
        _setval = "$('#timepickerte').val('{}')".format(_val)
        self.driver.execute_script(_setval)  # 修改值
    @excepTion
    def ClickUseJquery(self, element):
        ''' Click us jquery '''

        self.driver.execute_script('$("{}").click()'.format(element))
        time.sleep(0.5)
    @excepTion
    def SendUseJquery(self, element,value):
        ''' Send value use jquery  '''

        self.driver.execute_script('$("{}").val("{}")'.format(element, value))
        time.sleep(0.5)
    @excepTion
    def ClickByMui(self,ele):
        # 通过mui点击元素
        _Element = 'var q = mui("%s");q[0].addEventListener("tap", function(){});mui.trigger(q[0], "tap");' % (ele)
        #print(_Element)
        self.driver.execute_script(_Element)
    @excepTion
    def getMsg_erleihu(self,requestIP, userName, passwd, tel):
        # 二类户开户获取验证码
        import requests
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP + "/msg/msgSendInfoQuery.action"
        # print(login_url)
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
        m = html.index("【包商银行】")
        code = html[m + 35:m + 41]
        return code
    @excepTion
    def getTextByUI(self, Uiauto):
        '''
        UiAutomator
        '''
        s = self.driver.find_element_by_android_uiautomator(Uiauto).text
        return s
    @excepTion
    def ClickByMuiIndex(self,ele,index):
        # 通过mui点击元素
        _index  = index
        _Element = 'var q = mui("%s");q[%d].addEventListener("tap", function(){});mui.trigger(q[%d], "tap");' % (ele,index,_index)
        #print(_Element)
        self.driver.execute_script(_Element)
    @excepTion
    def mobile_setConfig_bsb(self, platformName, port, udid, driverType=0):
        try:
            from appium import webdriver
            # self.desired=desired_caps
            desired_caps = {}
            self.url = path
            self.udid = udid
            self.platformName = platformName
            compare = "True"
            desired_caps["noSign"] = "true"
            desired_caps["noReset"] = "true"
            desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
            # 启用UNICODE输入，可以输入中文
            desired_caps["unicodeKeyboard"] = True
            desired_caps["resetKeyboard"] = True
            desired_caps["deviceName"] = self.udid
            desired_caps["platformName"] = platformName
            desired_caps["udid"] = udid
            desired_caps["url"] = "http://127.0.0.1:" + port
            desired_caps["platformVersion"] = "7"
            desired_caps["appActivity"] = "io.dcloud.BSBankActivity"
            desired_caps["appPackage"] = "cn.com.bsb.mbank"
            desired_caps["newCommandTimeout"] = 180
            # conf文件目录
            filePathList = path.split(sep)
            self.configPath = sep.join(filePathList[:len(filePathList) - 1])
            self.SafeImagePath = "%s/conf/safeKeyBordTemplate/tempimage" % self.configPath
            # conf文件目录
            if (driverType == 1):
                self.tempPath = "%s%sconf%sdriver1.ini" % (self.configPath, sep, sep)
            else:
                self.tempPath = "%s%sconf%sdriver.ini" % (self.configPath, sep, sep)

            if not os.path.exists(self.tempPath):
                # 如果持久化driver的文件不存在，就启动driver，然后保存driver
                self.driver = webdriver.Remote(desired_caps["url"] + "/wd/hub", desired_caps)
                f1 = open(self.tempPath, "wb")
                pickle.dump(self.driver, f1, 0)
                f1.close()
                # 是否登陆
                self.isLogin = 1
            else:
                # 否则就从文件中将driver读取出来，如果发生异常，第一件事是删除文件
                f1 = open(self.tempPath, "rb")
                self.driver = pickle.load(f1)
                f1.close()
                time.sleep(1)
                self.isLogin = 0
            self.num = 0
            # ---截图对比用到的数据
            self.screenShotNum = 0  # 案例截图顺序
            self.mainMobil = compare
            self.transName = "单位预约开户_微信银行"
            self.caseId = "微信银行_单位预约开户001"
            self.track = "微信银行_单位预约开户001"
            # ---截图对比用到的数据end

        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            raise scriptError(funcName + "--" + "--driver init error--" + "--[异常信息]:%s" % repr(e))
    @excepTion
    def YunGetCode1(self):
        import datetime, ibm_db, time
        time.sleep(4)
        _result = ""
        _time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')
        _sql = "select * from cpm.efwk_captcha"
        conn = ibm_db.connect("DATABASE=CPM;HOSTNAME=14.16.10.202;PORT=60000;PROTOCOL=TCPIP;UID=bsbview;PWD=U2bpQT5z;","", "")
        if conn:
            stmt = ibm_db.exec_immediate(conn, _sql)
            result = ibm_db.fetch_both(stmt)
            while (result):
                # print(result)
                _string = result
                result = ibm_db.fetch_both(stmt)
        print(_string.get("STRVALUE"))
        return _string.get("STRVALUE")
    @excepTion
    def TouchTapA_bsb(self,height,loop):
        # 包商银行方法，MID 为手机屏幕宽度的一半 。
        Mid  = int(self.driver.get_window_size()['width']) / 2
        print(Mid)
        for i in range(loop):
            _CMD = "adb shell input tap {} {}".format(Mid,height)
            os.popen(_CMD)
            time.sleep(0.5)
    @excepTion
    def TouchTapL(self, x, y,loop):
        #
        for i in range(loop):
            _CMD = "adb shell input tap {} {}".format(x,y)
            os.popen(_CMD)
            time.sleep(0.5)
    @excepTion
    def getText_bsb_getattr(self,element):
        ele = self.driver.find_element_by_xpath(element)
        name = ele.get_attribute('name')

        return name
    @excepTion
    def getText_bsb(self, by, value):
        _str = ""
        if (by == "id"):
            _str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, value))).text
        elif (by == "name"):
            _str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, value))).text
        elif (by == "xpath"):
            _str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, value))).text
        elif (by == "css"):
            _str = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value))).text
        MONEY = _str.replace(",","")
        return MONEY
    @excepTion
    def Clickkw_erleihu(self, String):
        time.sleep(1)
        for i in String:
            print(i)
            self.driver.execute_script('$("input[value={}]").click()'.format(int(i)))
            time.sleep(0.5)
    @excepTion
    def mobile_setConfigL(self,platformName,port,udid,driverType=0):
        try:
            from appium import webdriver 
            #self.desired=desired_caps 
            desired_caps={}
            self.url=path
            self.udid = udid
            self.platformName = platformName
            compare = "True"
            desired_caps["noSign"] = "true"
            desired_caps["noReset"] = "true"
            desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
            # 启用UNICODE输入，可以输入中文
            desired_caps["unicodeKeyboard"] = True
            desired_caps["resetKeyboard"] = True
            desired_caps["deviceName"] = self.udid
            desired_caps["platformName"] = platformName
            desired_caps["udid"] = udid
            desired_caps["url"] = "http://127.0.0.1:"+port
            desired_caps["platformVersion"] = "9"  
            desired_caps["appActivity"] = "com.tencent.mm.ui.LauncherUI"  
            desired_caps["appPackage"] = "com.tencent.mm"
            desired_caps["newCommandTimeout"] = 180
            #conf文件目录
            filePathList = path.split(sep)
            self.configPath = sep.join(filePathList[:len(filePathList)-1])
            self.SafeImagePath = "%s/conf/safeKeyBordTemplate/tempimage"%self.configPath
            #conf文件目录
            if(driverType==1):
                self.tempPath = "%s%sconf%sdriver1.ini"%(self.configPath,sep,sep)
            else:
                self.tempPath = "%s%sconf%sdriver.ini"%(self.configPath,sep,sep)
            
            if not os.path.exists(self.tempPath):
                #如果持久化driver的文件不存在，就启动driver，然后保存driver
                self.driver = webdriver.Remote(desired_caps["url"]+"/wd/hub", desired_caps)
                f1 = open(self.tempPath,"wb")
                pickle.dump(self.driver,f1,0)
                f1.close()
                #是否登陆telephonr
                self.isLogin = 1
            else:
                #否则就从文件中将driver读取出来，如果发生异常，第一件事是删除文件
                f1 = open(self.tempPath,"rb")
                self.driver = pickle.load(f1)
                f1.close()
                time.sleep(1)
                self.isLogin = 0
            self.num=0
            #---截图对比用到的数据
            self.screenShotNum = 0 #案例截图顺序
            self.mainMobil = compare
            self.transName = "单位预约开户_微信银行"
            self.caseId = "微信银行_单位预约开户001"
            self.track = "微信银行_单位预约开户001"
            #---截图对比用到的数据end
            
        except Exception as e:
            funcName = sys._getframe().f_code.co_name
            raise scriptError(funcName+"--"+"--driver init error--"+"--[异常信息]:%s"%repr(e))
    @excepTion
    def get_screen_bsb(self):
        # 截图名字
        _path = r"D:\a\\"
        if not os.path.exists(_path): os.makedirs(_path)
        self.driver.get_screenshot_as_file(_path+"1234.png")
    @excepTion
    def getvalue_ocr(self):
        '''
        :param path: 文件的路径
        :return:  返回识别出来的值
        '''
        import time,requests
        img = Image.open("D:\\a\\1234.png")
        img = img.crop((22, 515, 862, 635))
        img = img.resize((280, 40), Image.ANTIALIAS)
        img.save(r"D:\\a\\12345.png")
        time.sleep(2)
        url = "http://14.33.7.230:5000/ocr1"

        files = {'image_file': ("filename", open("D:\\a\\12345.png", 'rb'), 'application')}
        r = requests.post(url=url, files=files)
        print(r.text)
        value = json.loads(r.text)
        print(value.get("value"))
        return value.get("value")
    @excepTion
    def getMsg_ShuHui(self, requestIP, userName, passwd, tel):
        # 基金赎回
        import requests
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
        m = html.index("您本次用于理财产品实时赎回的蒙商银行短信验证码:")
        code = html[m + 24:m + 30]
        return code
    @excepTion
    def ElementIfExist(self,by,value):
        try:
            self.driver.find_element(by=by, value=value)
        except Exception as e:
            # 打印异常信息
            print(e)
            # 发生了 NoSuchElementException异常，说明页面中未找到该元素，返回False
            print("没有该元素")
            return "False"
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            print("找到元素了")
            return "True"
    @excepTion
    def FindAndClick(self,functionLibrary,text,count):
        countNum = 1
        xpathString = "//XCUIElementTypeStaticText[@name="+"\""+text+"\""+"]"
        xpathString_One = "(//XCUIElementTypeStaticText[@name="+"\""+text+"\""+"])[1]"
        print(xpathString)
        print(xpathString_One)
        while True:
            #存在则点击第一次出现的那条数据
            existElement = functionLibrary.ElementIfExist("xpath",xpathString)
            existElement_One = functionLibrary.ElementIfExist("xpath",xpathString_One)
            if existElement == "True":
                if countNum > 1: 
                    self.driver.swipe(88, 280, 88, 60, 1000)
                    time.sleep(1)
                    self.driver.swipe(88, 280, 88, 60, 1000)
                    time.sleep(1)
                    self.driver.swipe(88, 240, 88, 60, 1000)
                    time.sleep(1)
                x = 254 + 104*0.5
                y = self.driver.find_element_by_xpath(xpathString).location['y'] + 193 - 125 + 37*0.5
                self.driver.tap([(x,y)],200)
                time.sleep(2)
                break
            elif existElement_One == "True":
                if countNum > 1: 
                    self.driver.swipe(88, 280, 88, 60, 1000)
                    time.sleep(1)
                    self.driver.swipe(88, 280, 88, 60, 1000)
                    time.sleep(1)
                    self.driver.swipe(88, 280, 88, 60, 1000)
                time.sleep(1)
                x = 254 + 104*0.5
                y_One = self.driver.find_element_by_xpath(xpathString_One).location['y'] + 193 - 125 + 37*0.5
                self.driver.tap([(x,y_One)],200)
                time.sleep(2)
                break
            #刷新完所有数据后没要找到需要的元素
            noMoreElement = functionLibrary.ElementIfExist("xpath","//XCUIElementTypeStaticText[@name=\"没有更多数据了\"]")
            if noMoreElement == "True":
                raise scriptError("FindAndClick"+'----未找到'+text+'元素----异常')
                break
            #循环到一定次数后直接报出未找到该元素
            if countNum > count:
                raise scriptError("FindAndClick"+'----未找到'+text+'元素----异常')
                print("没找到该交易")
                break
            countNum += 1
            print(countNum)
            self.driver.swipe(88, 260, 88, 50, 1000)
            time.sleep(2)
    @excepTion    
    def getNumWithStr(self,string1,string2):
        m = string1.rfind(string2)
        code = string1[m-4:m]
        code = re.sub("\D", "", code)
        return code

    @excepTion
    def getMsgInFrontOfKeyStr(self,requestIP,userName,passwd,tel,keyStr):
        import requests
        login_url = "http://" + requestIP + "/msg/Login.action"
        login_data = {"tellerId": userName, "password": passwd}
        search_url = "http://" + requestIP +"/msg/msgSendInfoQuery.action"
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
        m = html.rfind(keyStr)
        code = html[m-6:m]
        return code
    @excepTion
    def inputPSD_unboundM(self,pwd):
        for ch in pwd:
            print(ch)
            if ch == "0":
                ch = "16"
            else:
                ch = str(int(ch)+5)
            xpathStr = "//XCUIElementTypeOther[@name=\"许下心愿\"]/XCUIElementTypeOther["+ch+"]"
            #print("xpathStr:"+xpathStr)
            self.ClickByXpath(xpathStr)
        time.sleep(5)
    @excepTion
    def ClickByTagText(self,tag,text):
        '''
        :param tag:  html tg
        :param text: html innertext value
        :return:
        '''
        _js = '''function joker(){ \
                    var ele_list = mui('%s'); \
                    for (var i=0;i<ele_list.length;i++){ \
                          if (q[i].innerText == '%s'){ \
        		            q[i].addEventListener('tap',function(){}); \
        		            mui.trigger(q[i],'tap');\
        	            } \
                    } \
                };joker();''' % (tag,text)
        self.driver.execute_script(_js)
    @excepTion
    def mobile_setConfig(self,platformName,port,udid,driverType=0):
        try:
            from appium import webdriver 
            #self.desired=desired_caps 
            desired_caps={}
            self.url=path
            self.udid = udid
            self.platformName = platformName
            compare = "True"
            desired_caps["noSign"] = "true"
            desired_caps["noReset"] = "true"
            desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
            # 启用UNICODE输入，可以输入中文
            desired_caps["unicodeKeyboard"] = True
            desired_caps["resetKeyboard"] = True
            desired_caps["deviceName"] = self.udid
            desired_caps["platformName"] = platformName
            desired_caps["udid"] = udid
            desired_caps["url"] = "http://127.0.0.1:"+port
            desired_caps["platformVersion"] = "9"  
            desired_caps["appActivity"] = "iio.dcloud.BSBankActivity"
            desired_caps["appPackage"] = "cn.com.bsb.mbank"
            #conf文件目录
            filePathList = path.split(sep)
            self.configPath = sep.join(filePathList[:len(filePathList)-1])
            self.SafeImagePath = "%s/conf/safeKeyBordTemplate/tempimage"%self.configPath
            #conf文件目录
            if(driverType==1):
                self.tempPath = "%s%sconf%sdriver1.ini"%(self.configPath,sep,sep)
            else:
                # self.tempPath = "%s%sconf%sdriver.ini"%(self.configPath,sep,sep)
                pass
            
            if not os.path.exists(self.tempPath):
                #如果持久化driver的文件不存在，就启动driver，然后保存driver
                self.driver = webdriver.Remote(desired_caps["url"]+"/wd/hub", desired_caps)
                f1 = open(self.tempPath,"wb")
                pickle.dump(self.driver,f1,0)
                f1.close()
                #是否登陆
                self.isLogin = 1
            else:
                #否则就从文件中将driver读取出来，如果发生异常，第一件事是删除文件
                f1 = open(self.tempPath,"rb")
                self.driver = pickle.load(f1)
                f1.close()
                time.sleep(1)
                self.isLogin = 0
            self.num=0
            #---截图对比用到的数据
            self.screenShotNum = 0 #案例截图顺序
            self.mainMobil = compare
            self.transName = "账户信息查询_手机银行"
            self.caseId = "手机银行_账户信息查询_账户信息查询流程001"
            self.track = "手机银行_微信银行_账户查询对比(安卓)"
            #---截图对比用到的数据end
            
        except Exception as e: print(e)
            # funcName = sys._getframe().f_code.co_name
            # raise scriptError(funcName+"--"+"--driver init error--"+"--[异常信息]:%s"%repr(e))
class Procedure():
    def mainTest(self):
        functionLibrary=FunctionLibrary()
        functionLibrary.log("[==========ScriptStart==========执行成功]")
        #ConfVar=functionLibrary.getModel("{param1}")
        functionLibrary.mobile_setConfig("Android","4723","QV7129M024")
        functionLibrary.log("[mobile_setConfig====执行成功]")
        time.sleep(20)
        functionLibrary.ClickTextA("https://test8.bsb.com.cn/perbank_zsc/") 
        functionLibrary.log("[ClickTextA==https://test8.bsb.com.cn/perbank_zsc/==执行成功]")
        time.sleep(10  )
        functionLibrary.ClickByUiauto("text(\"我的\")") 
        functionLibrary.log("[ClickByUiauto==text(\"我的\")==执行成功]")
        time.sleep(5)
        functionLibrary.ClickByUiauto("text(\"登录/注册\")") 
        functionLibrary.log("[ClickByUiauto==text(\"登录/注册\")==执行成功]")
        time.sleep(5)
        functionLibrary.TouchTapA_bsb(1791,1) 
        functionLibrary.log("[TouchTapA==1791==1==执行成功]")
        time.sleep(5)
        functionLibrary.TouchTapA_bsb(607,1) 
        functionLibrary.log("[TouchTapA==607==1==执行成功]")
        functionLibrary.SendKeysUseAdbInputText("18700050009")
        functionLibrary.log("[SendKeysUseAdbInputText==18700050009==执行成功]")
        time.sleep(2)
        functionLibrary.TouchTapA_bsb(806,1) 
        functionLibrary.log("[TouchTapA==806==1==执行成功]")
        time.sleep(2)
        functionLibrary.TouchTapL(110,1534,3) 
        functionLibrary.log("[TouchTapL==110==1534==3==执行成功]")
        functionLibrary.TouchTapL(151,1861,1) 
        functionLibrary.log("[TouchTapL==151==1861==1==执行成功]")
        time.sleep(2)
        functionLibrary.TouchTapL(544,1833,5) 
        functionLibrary.log("[TouchTapL==544==1833==5==执行成功]")
        time.sleep(1)
        functionLibrary.TouchTapA_bsb(1053,1) 
        functionLibrary.log("[TouchTapA==1053==1==执行成功]")
        time.sleep(6)
        CHUXU = functionLibrary.getText_bsb_getattr("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[1]/android.view.View[3]") 
        functionLibrary.log("[getText_bsb_getattr==/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[1]/android.view.View[3]==执行成功]")
        functionLibrary.mem("chuxui",CHUXU) 
        functionLibrary.log("[mem==chuxui=={val}==执行成功]")
        LICAI = functionLibrary.getText_bsb_getattr("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[2]/android.view.View[3]") 
        functionLibrary.log("[getText_bsb_getattr==/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[2]/android.view.View[3]==执行成功]")
        functionLibrary.mem("licaii",LICAI) 
        functionLibrary.log("[mem==licaii=={val}==执行成功]")
        JIJIN = functionLibrary.getText_bsb_getattr("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[3]/android.view.View[3]") 
        functionLibrary.log("[getText_bsb_getattr==/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/android.widget.ListView[5]/android.view.View[3]/android.view.View[3]==执行成功]")
        functionLibrary.mem("jijini",JIJIN) 
        functionLibrary.log("[mem==jijini=={val}==执行成功]")
        time.sleep(3)
        functionLibrary.get_screen("手机银行账户信息截图")
        functionLibrary.log("[ScreenShot==手机银行账户信息截图==执行成功]")
        functionLibrary.ClickByUiauto("text(\"资产总览 明细\")") 
        functionLibrary.log("[ClickByUiauto==text(\"资产总览 明细\")==执行成功]")
        time.sleep(3)
        functionLibrary.TouchTapL(562,283,3) 
        functionLibrary.log("[TouchTapL==562==283==3==执行成功]")
        time.sleep(3)
        functionLibrary.get_screen_bsb()
        functionLibrary.log("[get_screen_bsb====执行成功]")
        zaituzichan = functionLibrary.getvalue_ocr() 
        functionLibrary.log("[getvalue_ocr====执行成功]")
        functionLibrary.mem("zichani",zaituzichan) 
        functionLibrary.log("[mem==zichani=={val}==执行成功]")
        functionLibrary.get_screen("手机银行账户在途信息截图")
        functionLibrary.log("[ScreenShot==手机银行账户在途信息截图==执行成功]")
        functionLibrary.quitDriver("")
        #设置为全局变量，执行案例时设置为0，调试时设置为1
        #为0时保留session，为1时强制删除session
        #functionLibrary.log("[quitDriver==执行成功]")

####-----------scripte end ----------####      
if __name__ == "__main__":
        #是否monkey安装app
        testMonkey=FunctionLibrary()
        if  ifInstallMonkey!=None:
            testMonkey.ifInstall_monkey(ifInstallMonkey)
        Procedure().mainTest()
        file=FileTools(path)
        file.fileSplice()

