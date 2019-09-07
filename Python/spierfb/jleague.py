import mysql.connector
import re,time,mysql.connector,requests
from selenium import webdriver
from selenium.webdriver.support.ui  import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Firefox52 / Chrome55 + python3.4 + selenium 3.4 + centos7
# selenium get page data

Team_A = {
    "浦和红钻":"浦和","大阪樱花":"Ｃ大阪","鹿岛鹿角":"鹿島","名古屋鲸":"名古屋",
    "广岛三箭":"広島","清水鼓动":"清水","东京FC":"FC東京","大阪钢巴":"Ｇ大阪",
    "磐田喜悦":"磐田","仙台七夕":"仙台","神户胜利":"神戸","长崎航海":"長崎",
    "横滨水手":"横浜FM","札幌冈萨":"札幌","柏太阳神":"柏","湘南海洋":"湘南",
    "川崎前锋":"川崎Ｆ","鸟栖沙岩":"鳥栖",
	"福冈黄蜂":"福岡","水户蜀葵":"水戸","金泽塞维":"金沢","松本山雅":"松本",
    "千叶市原":"千葉","冈山绿雉":"岡山","德岛漩涡":"徳島","山形山神":"山形",
    "爱媛FC":"愛媛","山口雷诺":"山口","甲府风林":"甲府","大宫松鼠":"大宮",
    "岐阜FC":"岐阜","大分三神":"大分","町田泽维":"町田","新泻天鹅":"新潟",
    "京都":"京都","赞岐釜玉":"讃岐","熊本深红":"熊本","群马温泉":"群馬",
    "东京绿茵":"東京Ｖ","横滨FC":"横浜FC","枥木SC":"栃木"
}

class J:
    ##*css*##
    level_css = "#breadcrumbList > ol > li:nth-child(3) > a > span"  # 级别
    round_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > div > h3"  # 轮数
    wea_css = "#loadArea > table > tbody > tr:nth-child(3) > td:nth-child(2)"  # 天气
    zhu_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li:nth-child(1) > a > p"  # 主队
    ke_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li:nth-child(3) > a > p"  # 客队
    bc_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li.leagAccScore > div.leagCenterScore > p:nth-child(2)"  # 半场
    zj_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li.leagAccScore > div.leagLeftScore > p"  # 主队进球
    kj_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li.leagAccScore > div.leagRightScore > p"  # 客队进球
    zc_css = "#loadArea > section.matchResult.resultBorder > table > tbody > tr:nth-child(3) > td:nth-child(2)"  # 主队角球
    kc_css = "#loadArea > section.matchResult.resultBorder > table > tbody > tr:nth-child(3) > td:nth-child(3)"  # 客队角球
    tq_css = "#loadArea > table > tbody > tr:nth-child(3) > td:nth-child(2)"
    zbc_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li.leagAccScore > div.leagCenterScore > p:nth-child(2) > span:nth-child(1)"
    kbc_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li.leagAccScore > div.leagCenterScore > p:nth-child(2) > span:nth-child(3)"
    k_r_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > div > h3"
    k_ke_css = "body > div.content.clearfix > div.main > section > section.matchVsBox.boxCenterTime > ul.leagScoreColumn > li:nth-child(3) > p"
    ##*css*##
    def __init__(self):
        profile_dir = "/home/root/.mozilla/firefox/291hkm8s.sct"
        profile = webdriver.FirefoxProfile(profile_dir)
        self.driver = webdriver.Firefox(profile)
        self.level =  ""
        self.round =  ""
        self.st    =  ""
        self.weather= ""
        self.status = False
        self.bc = ""
        self.zhu = ""
        self.ke= ""
        self.zc= ""
        self.kc= ""
        self.date = ""
        self.timeout= 30
    def islive(self):
        for i in range(1,20):
            if i<10:
                i = "0"+str(i)
            __url ="https://www.jleague.jp/match/j1/2018/0425"+str(i)+"/live/"
            print (__url)
            self.date = __url[-12:-6]
            print (self.date)
            # s = requests.get(__url).status_code　　＃有些时候目标网站会被屏蔽。post的时候不用代理。所以无法返回200，
            # print(s)
            try:
                self.getdata(__url)
                self.writedb()
            except:
                print (__url+"\t error")
                self.closeweb()
            finally:
                self.closeweb()
    def getdata(self,gurl):
        self.driver.maximize_window()
        self.driver.get(gurl)
        level_text = WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, J.level_css))).text
        print (level_text)
        if "Ｊ１" in level_text:
            self.level = "A"
            print (self.level)
            self.status =True
        elif "Ｊ２" in level_text:
            self.level = "B"
            self.status=True
        elif "天皇杯" in level_text:
            self.level = "K"
            self.status = True
        elif "YBC" in level_text:
            self.level = "L"
            self.status = True
        else:
            self.status = False
        if self.status is  not True:
            print ('status is False')
        else:
            #轮数
            if self.level =='A' or self.level =='B' or self.level == 'L':
                round = self.driver.find_element_by_css_selector(J.round_css).text
                s = re.findall("\d+",round)
                print (s)
                self.round = s[0]
                print (self.round)
                #比赛时间
                self.st = s[-2]+s[-1]
                print (self.st)
            elif self.level =='K':
                round = self.driver.find_element_by_css_selector(J.k_r_css).text.encode("utf-8")
                print (round)
                self.round = round[12:15]
                print (self.round)
                s = re.findall("\d+",round)
                print (s)
                self.st = s[-2]+s[-1]
                print (self.st)
            #主队进球
            self.zj = self.driver.find_element_by_css_selector(J.zj_css).text
            print (self.zj)
            #客队进球
            self.kj = self.driver.find_element_by_css_selector(J.kj_css).text
            print (self.kj)
            #天气
            weather = self.driver.find_element_by_css_selector(J.tq_css).text
            print (weather)
            self.weather = weather[0:1]
            print (self.weather,type(self.weather))
            #主队
            self.zhu = self.driver.find_element_by_css_selector(J.zhu_css).text
            print (self.zhu)
            #客队
            if self.level =='A' or self.level =='B' or self.level == 'L':
                self.ke = self.driver.find_element_by_css_selector(J.ke_css).text
                print (self.ke)
            elif self.level == 'K':
                self.ke = self.driver.find_element_by_css_selector(J.k_ke_css).text
                print (self.ke)
            #半场进球数
            zbc = self.driver.find_element_by_css_selector(J.zbc_css).text
            kbc = self.driver.find_element_by_css_selector(J.kbc_css).text
            self.bc = zbc+"-"+kbc
            print (self.bc)
            #主队角球
            self.zc = self.driver.find_element_by_css_selector(J.zc_css).text
            print (self.zc)
            #客队角球
            self.kc =self.driver.find_element_by_css_selector(J.kc_css).text
            print (self.kc)
    def closeweb(self):
        self.driver.close()
    def writedb(self):
        if self.status != True:
            print('status is not True')
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='root', database='jleague',use_unicode=True)
            cursor = conn.cursor()
            cursor.execute("select * from j8 where date ='%s'" % self.date)
            list = cursor.fetchall()
            print(list)
            if list != []:
                print("date '%s' hava been esixt" % self.date)
            else:
                insertsql = "INSERT INTO `j8` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                ";" % (
                                self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,
                                self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")
                cursor.execute(insertsql)
                cursor.close()
                conn.commit()
                conn.close()

    def run(self):
        self.islive()
class Du500:
    asic_css = "#link112"  # 亚盘
    zhu_d = "#link110"
    win_css = "#a648232 > td.bf_op > span:nth-child(1)"
    draw_css = "#a648232 > td.bf_op > span:nth-child(2)"
    loss_css = "#a648232 > td.bf_op > span.op4"
    win1_css = "#a648231 > td.bf_op > span:nth-child(1)"
    def __init__(self):
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.PhantomJS('/home/root/program/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.level =  ""
        self.round =  ""
        self.status = False
        self.zhu = ""
        self.date = ""
        self.asia =""
        self.win =""
        self.draw =""
        self.lose=""
        self.timeout=30

    def get_match_day(self,level,round):
        #获得比赛时间
        match_date = []
        self.round  = round
        self.level  = level
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='jleague',use_unicode=True)
        cursor = conn.cursor()
        cursor.execute("select distinct(left(date,4)) from j8 where level ='%s' and round ='%s'" % (level,round))
        list = cursor.fetchall()
        # print (list)
        for i in list:
            for k in i:
                match_date.append(k)
        return match_date
    def get_500_url(self):
        #根据数据查找500上的网址 list,level & round
        pin_all_url = []
        url_tmp = "http://live.500.com/?e=2018-"
        bs_date = self.get_match_day('B',10) #需要修改leve&
        # print(bs_date)
        for i in bs_date:
            pin_all_url.append(url_tmp+i[0:2]+"-"+i[2:4])
        return pin_all_url
    def getdata(self,url):

        self.driver.maximize_window()
        self.driver.get(url)

        WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#btn_league"))).click()# 点赛事选择
        WebDriverWait(self.driver,self.timeout,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#btn_league_opp"))).click()#反选

        if self.level =='A':#j1
            WebDriverWait(self.driver,self.timeout,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ck_l_39"))).click()
        elif self.level == 'B':#j2
            WebDriverWait(self.driver,self.timeout,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ck_l_352"))).click()
        elif self.level == 'L':#L
            WebDriverWait(self.driver,self.timeout,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ck_l_135"))).click()

        WebDriverWait(self.driver,self.timeout,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#btn_league_close"))).click()#关闭
        ser = Select(self.driver.find_element_by_css_selector("select[id='sel_odds']"))
        ser.select_by_index(5)

        s = []
        ele1 =self.driver.find_elements_by_css_selector("tr[status='4']")
        for k in ele1:
            s.append(k.text)

        while "" in s:#去掉list里面的空字符串
            s.remove("")
        # print (s)
        for key,val in Team_A.items():
            for i in s:
                if key in i :
                    _str = re.findall(r'完.*[0-9]',''.join(i.split()).replace('.',''))[0].replace('[','').replace(']','').replace('完','9')

                    self.zhu = re.findall("[0-9]*([\\u4e00-\\u9fa5|[A-Z]*)",_str)[0]
                    self.asia = (i.split('\n')[2])  # 亚盘
                    self.lose  = (_str[-3:-2] + '.' + _str[-2::])
                    self.draw  = (_str[-6:-5] + '.' + _str[-5:-3])
                    self.win   = (_str[-9:-8] + '.' + _str[-8:-6])
                    # print (self.zhu,self.win,self.draw,self.lose,self.asia)
                    self.write_data()
    def closeweb(self):
        self.driver.close()
    def write_data(self):
        conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='root', database='jleague')
        cursor = conn.cursor()
        cursor.execute("select asia from j8 where  zhu ='%s' and round = '%s' and level='%s'" % (Team_A[self.zhu],self.round,self.level))
        list = cursor.fetchall()

        # print(list)
        if list[0][0] =="":
            updatesql = ("update j8 set asia='%s',win='%s',draw='%s',lose='%s' where zhu='%s' and round='%s' and level ='%s'" % (self.asia,self.win,self.draw,self.lose,Team_A[self.zhu],self.round,self.level))
            cursor.execute(updatesql)
            cursor.close()
            conn.commit()
            conn.close()
            # 插入数据
        else:
            print("data already esixt")
            conn.close()

    def run(self):
        url = self.get_500_url()
        for u in url:
            s = requests.get(u).status_code
            if s != 200:
                print(" %s has error" % u)
                continue
            else:
                self.getdata(u)
        self.closeweb()
if __name__ == '__main__':
    Du500().run()