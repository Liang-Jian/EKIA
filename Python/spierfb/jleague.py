import mysql.connector
import re,time,mysql.connector,requests,sys
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



import datetime,time,mysql.connector,configparser,re,requests,yaml
import lxml.html
import requests
from bs4 import BeautifulSoup
from Python.spierfb.logmodule import Logi,Loge,Logd,Logc
from abc import ABCMeta,abstractclassmethod
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# from selenium import webdriver
# from selenium.webdriver.support.ui  import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC



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
    "东京绿茵":"東京Ｖ","横滨FC":"横浜FC","枥木SC":"栃木","北九州":"北九州",
    "琉球FC":"琉球","鹿儿岛联":"鹿児島"
}
def getkey(_dict,_value):
    return list(_dict.keys())[list(_dict.values()).index(_value)]

cf = configparser.ConfigParser()
cf.read("../spierfb/peizhi.ini")


file = open("../spierfb/run.yml", "r", encoding="utf8")
conff = yaml.load(file.read(), Loader=yaml.Loader)
conf = conff['control']


def rt():
    import random
    t = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4]
    s = random.choice(t)
    return s


j_headle ={
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"cache-control": "max-age=0",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": None,
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}



class MsqService(object):

    def __init__(self):
        self.conn = mysql.connector.connect(host='118.25.78.198', user='root', password='root',
                                            database='jleague',use_unicode=True)
    def search(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        Logi("sql result:={}".format(select_data))
        return select_data

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        if self.conn != None:
            self.conn.close()

        if self.cursor !=None:
            self.cursor.close()

ms = MsqService()

class GetOldData():
    def __init__(self):
        self.start_roud= conf['startNo']  #开始轮数
        self.end_round = conf['endNo']    #结束轮数
        self.level     = conf['level']
        self.round     = ""
        self.st        = ""
        self.status    = False
        self.bc        = ""
        self.zhu       = ""
        self.ke        = ""
        self.zc        = ""
        self.kc        = ""
        self.start_url = "https://www.jleague.jp/match/j1/2018/{}/live/"
        # self.headers   = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        self.headers   = j_headle
        self.proxies   = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
        self.html      = None


    def _getupdatesql1(self): # 单
        all_sql = []
        n = 0
        startcount = conf['startcount']
        while n <= 7:
            n +=1
            startcount +=1
            starturl = self.start_url.format("%06d" % (startcount))
            all_sql += self.get_update_sql(starturl)
        Logi("j all sql:=%s" % all_sql)
        return all_sql


    def _getupdatesql(self):  # 多
        all_sql = list()
        startcount = conf['startcount']
        for l in startcount:
            n = 0
            while n < 11:
                n +=1
                l +=1
                starturl = self.start_url.format("%06d" % (l))
                all_sql += self.get_update_sql(starturl)
        Logi("j all sql:=%s" % all_sql)
        return all_sql
    @staticmethod
    def _get_level(txt):
        level_pool = {"Ｊ１": "A", "Ｊ２": "B", "Ｊ３": "C", "天皇杯": "K", "YBC": "L"}
        for key in level_pool:
            if key in txt:
                return level_pool.get(key)

    def get_update_sql(self,url):
        asql = list()
        time.sleep(rt())
        try:
            self.html = requests.get(url, verify=False, headers = self.headers)                 # , proxies=self.proxies
        except (Exception) as e:
            Loge(e)
            return []
        print(self.html.status_code)
        if self.html.status_code == 200:
            selector =lxml.html.fromstring(self.html.text)
            soup = BeautifulSoup(self.html.text, 'lxml')

            new_url = url.replace("live/","ajax_live?_={}T{}")                                  #天气信息ajax动态加载的.拼ajax的url
            new_url.format(datetime.date.today(),time.strftime('%H:%M',time.localtime(time.time())))
            weather_web = requests.get(new_url, verify=False, headers=self.headers).content.decode()
            weather_soup = BeautifulSoup(weather_web, 'lxml')
            _zhu = weather_soup.table.strings
            s = []
            for i in _zhu:
                s.append(i)
            while "\n" in s:
                s.remove("\n")
            self.zhu     = "".join(selector.xpath(cf.get("css","zhu_css")))
            # print(self.zhu)
            self.ke      = "".join(selector.xpath(cf.get("css","ke_css")))
            self.bc      = selector.xpath(cf.get("css","zjc_css"))[0]+"-"+selector.xpath(cf.get("css","kjc_css"))[0]
            self.kj      = "".join(selector.xpath(cf.get("css","kj_css")))
            self.zj      = "".join(selector.xpath('//div[@class="leagLeftScore"]/text()'))
            self.zc      = "".join(selector.xpath(cf.get("css","zc_css")))
            self.kc      = "".join(selector.xpath(cf.get("css","kc_css")))
            self.level   = self._get_level("".join(selector.xpath(cf.get("css","level_css"))))
            self.st      = "".join(selector.xpath(cf.get("css","sj_css"))).replace(":","")
            self.round   = re.findall("\d+","".join(selector.xpath(cf.get("css","level_css"))),re.S)[1]
            self.date    = re.findall("2018/(.*?)/live",soup.link['href'])[0]
            # print(re.findall("(.*?)\/", s[-3]))
            self.weather = "".join(re.findall("(.*?)\/", s[-3])[0].split())[0:1]

            _insertsql = "INSERT INTO `j8` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,
                self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")
            asql.append(_insertsql)
            Logi("sql:={}".format(_insertsql))
            self.html.close()
            return asql
        else:
            return []
    def write2Db(self,sqlyuju):
        sql_lan = sqlyuju
        if sql_lan is []: Loge("sql is empty [] ")

        data = re.findall("\'(.*?)\'\,",sql_lan)
        if data is []:
            Loge("匹配数据失败")
        _date = data[0]
        if ms.search("select * from j8 where date ='%s'" % _date) != []:
            Loge("{} exist,don't insert".format(_date))

        else:
            ms.update(sql_lan)
            Logi("j data insert successfully")
    def run(self):
        for i in self._getupdatesql():
            self.write2Db(i)

class Get500Data(object):
    #需要修改self._level 的级别
    def __init__(self):

        self.headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self._level  = conf['level']
        self._zhu    = ""
        self._date   = ""
        self._asia   = ""
        self._win    = ""
        self._draw   = ""
        self._lose   = ""
        self._timeout= 30
    def get_matchdate(self):
        #数据库中查找asia为空的数据的所有数据,返回date % 0224
        match_date = []
        list_ = ms.search("select distinct(left(date,4)),asia from j8 where level ='%s'" % self._level)
        # print (list_)
        for i in list_:
            if i[1] == "":
                match_date.append(i[0])
        Logi("asia null date:={}".format(match_date))
        return match_date

    def get5url(self):
        # return all 500 url -> list()
        url_500 = []
        url_tmp = "http://live.500.com/?e={}-".format(conf['year'])
        for i in self.get_matchdate():
            _url_ = url_tmp+i[0:2]+"-"+i[2:4]
            url_500.append(_url_)
            Logi("500 url={}".format(_url_))
        return url_500

    def _getupdatesql(self):
        update_sql = []
        for i in self.get5url():
            update_sql +=self._getdata(i)
        # Logi("all:=%s" % update_sql)
        Logi("all sql create success")
        return  update_sql

    def get_match_team(self,date):
        match_team_list = list()
        update_sql = "select zhu,ke from j8 where asia = '' and left(date,4)={} and level='{}';"
        match_team_list += ms.search(update_sql.format(date,self._level))
        match_team_dict = dict(match_team_list)

        return match_team_dict


    def _getdata(self,url):
        _urll = []
        file_txt = requests.get(url=url,headers=self.headers).content.decode("gbk","ignore").encode("utf-8").decode("utf-8")
        match_date = url[-5::].replace("-","")
        time.sleep(2)
        team = self.get_match_team(match_date)
        for key,val in team.items():
            self._zhu = getkey(Team_A,key)
            self._ke = getkey(Team_A,val)
            Logi("主队 {},客队 {}".format(self._zhu,self._ke))
            peilv_data_dict = eval(re.findall("var liveOddsList(.*?=\s?)(.*?);", file_txt, re.S)[0][1])

            k = re.findall("<tr(.*?)"+self._zhu+","+self._ke,file_txt)
            if k !=[]:
                id_number = re.findall("id=\"a(.*?)\"",k[0])[0]
                _peilv =peilv_data_dict.get(id_number)['3']                                     # 赔率列表
                level1 = re.findall(id_number + "&r=1\"" + "(.*?)"+"</a>",file_txt,re.S)[1]     # 查找亚洲盘
                Logi("{} id={} 赔率={}".format(self._zhu, id_number,_peilv))
                self._win  = "%.2f" % float(_peilv[0])
                self._draw = "%.2f" % float(_peilv[1])
                self._lose = "%.2f" % float(_peilv[2])
                self._asia = re.findall("\">(.*?)$",level1)[0]
                updatesql = (
                            "update j8 set asia='%s',win='%s',draw='%s',lose='%s' where zhu='%s' and left(date,4)='%s'" % (
                    self._asia, self._win, self._draw, self._lose, Team_A[self._zhu], match_date))
                _urll.append(updatesql)
                Logi("sql add success={}".format(updatesql))
            else:
                pass
        return(_urll)
    def writeSql(self, sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is []: Loge("sql not found ")

        zhu_team = re.findall("zhu=\'(.*?)\'",sql_lan,re.S)[0]
        left_date = re.findall("\)=\'(.*?)\'",sql_lan,re.S)[0]
        Logi("插入前查询{} {}".format(zhu_team,left_date))
        if zhu_team is not []:
            if ms.search("select asia from j8 where zhu ='%s' and left(date,4)='%s' " % (zhu_team, left_date))[0][0] != "":
                Logi("data exist don't insert  {}".format(sql_lan))
            else:
                ms.update(sql_lan)
                Logi("500 insert success={}".format(sql_lan))
        else:
            Loge("zhu列匹配数据失败")
    def run(self):
        for i in self._getupdatesql():
            self.writeSql(i)
def main():
    GetOldData().run()
    Get500Data().run()

if __name__ == '__main__':
    main()

