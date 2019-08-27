import datetime
import time
import mysql.connector
import configparser
import re
import lxml.html
import requests
from bs4 import BeautifulSoup

from bet.duqiu.logmodule import logger_info,logger_warning,logger_debug
from abc import ABCMeta,abstractclassmethod


from selenium import webdriver
from selenium.webdriver.support.ui  import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
def getkey(_dict,_value):
    return list(_dict.keys())[list(_dict.values()).index(_value)]

class shujuku(metaclass=ABCMeta):

    @abstractclassmethod
    def search_db(self,*args):
        pass
    @abstractclassmethod
    def update_db(self,*args):
        pass
    @classmethod
    def close_db(self):
        pass

class mysqlOP(shujuku):

    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='root', database='jleague',
                                            use_unicode=True)

    def search_db(self,sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        logger_info("查询结果{}".format(select_data))
        return select_data

    def update_db(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close_db(self):
        if self.conn != None:
            self.conn.close()
        if self.cursor !=None:
            self.cursor.close()

cf = configparser.ConfigParser()
cf.read("/home/sct/workspace/java-eslworking/pythoncode/bet/spierfb/peizhi.ini")
class GetJleagueData(mysqlOP):
    #需要修改start_url ,_get1url中start ,end轮数
    def __init__(self):
        super(GetJleagueData,self).__init__()

        self.start_roud= 27  #开始轮数
        self.end_round = 42  #结束轮数
        self.level     = "A"
        self.round     = ""
        self.st        = ""
        self.status    = False
        self.bc        = ""
        self.zhu       = ""
        self.ke        = ""
        self.zc        = ""
        self.kc        = ""
        self.start_url = "https://www.jleague.jp/match/section/{}/{}/"
        self.headers   = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.proxies   = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}

    def _get1url(self,):
        #第一级URL start开始轮数
        _firstURL = []
        if   self.level == "A":Level = "j1"
        elif self.level == "B":Level = "j2"
        for i in range(self.start_roud,self.end_round):
            _firstURL.append(self.start_url.format(Level,i))
        logger_info("一级URL获取完成")
        return _firstURL

    def _get2url(self):
        #第二级URL
        secondURL= []
        _str = "https://www.jleague.jp"
        for i in self._get1url():
            html = requests.get(i, proxies=self.proxies, verify=True, headers=self.headers)
            k = re.findall("href=\"(.*?)\">試合詳細",html.text)
            print(k)
            if k != []:
                for s in k:
                    secondURL.append(_str+s)
        logger_info("二级URL获取完成")
        return secondURL

    @staticmethod
    def _get_level(txt):
        level_pool = {"Ｊ１": "A", "Ｊ２": "B", "Ｊ３": "C", "天皇杯": "K", "YBC": "L"}
        for key in level_pool:
            if key in txt:
                return level_pool.get(key)

    def get_sql(self,url):
        self.html = requests.get(url, proxies=self.proxies, verify=True, headers=self.headers)
        selector =lxml.html.fromstring(self.html.text)
        soup = BeautifulSoup(self.html.text, 'lxml')

        new_url = url.replace("live/","ajax_live?_={}T{}") #天气信息ajax动态加载的.拼ajax的url
        new_url.format(datetime.date.today(),time.strftime('%H:%M',time.localtime(time.time())))
        weather_web = requests.get(new_url, proxies=self.proxies, verify=True, headers=self.headers).content.decode()
        weather_soup = BeautifulSoup(weather_web, 'lxml')
        _zhu = weather_soup.table.strings
        s = []
        for i in _zhu:
            s.append(i)
        while "\n" in s:
            s.remove("\n")
        self.zhu     = "".join(selector.xpath(cf.get("css","zhu_css")))
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
        self.weather = "".join(re.findall("(.*?)\/", s[-3])[0].split())[0:1]

        _insertsql = "INSERT INTO `j8` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,
            self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")
        logger_info("creatsql {}".format(_insertsql))
        return  _insertsql

    def _writeDB(self, sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is None:
            logger_warning("sql语句无数据")
        data = re.findall("\'(.*?)\'\,",sql_lan)
        if data is []:
            logger_warning("匹配数据失败")
        _date = data[0]
        if self.search_db("select * from j8 where date ='%s'" % _date) != []:
            logger_info("'%s'数据库中已存在" % _date)
        else:
            self.update_db(sql_lan)
            logger_info("数据插入成功")

    def _get_all_sql(self):#返回所有的sql语句
        all_sql = []
        for i in self._get2url():
            try:
                all_sql.append(self.get_sql(i))
            except:
                raise("数据返回失败")
        logger_info("全部sql返回成功" + self._get_all_sql.__name__+ "")
        return all_sql

    def run(self):
        for k in self._get_all_sql():
            try:
                self._writeDB(k)
            except:
                logger_warning("{}插入失败".format(k))
'''
class UIGetWeatherData(mysqlOP):#通过selenium获取天气信息 ,现在不用了.可以通过get ajaxurl来去数据
    weather_css = "#loadArea > table > tbody > tr:nth-child(3) > td:nth-child(2)"
    def __init__(self):

        super(UIGetWeatherData, self).__init__()
        profile_dir = "/home/sct/.mozilla/firefox/291hkm8s.sct"
        profile = webdriver.FirefoxProfile(profile_dir)
        self.driver = webdriver.Firefox(profile)
        self.timeout= 30
        self._level = "A"
    def _geturl(self):
        #查找天气为空的比赛
        __url = []
        if   self._level == "A":
            url_model = "https://www.jleague.jp/match/j1/2018/{}/live/#live"   #j1修改如果是
        elif self._level == "B":
            url_model = "https://www.jleague.jp/match/j2/2018/{}/live/#live"
        _sql = "select weather,date from j8 where  level='%s'" % self._level
        data = self.search_db(_sql)
        _del = []
        for i in data:
            if i[0] == "":
                _del.append(i[1])
        for s in _del:
            _s = str(s)
            if len(_s) < 6:
                _s = "0"+str(_s)
                _j_url = url_model.format(_s)
            __url.append(_j_url)
            logger_info("JURL拼接成功{}".format(_j_url))
        return __url

    def _openB_getW(self,url):
        #开浏览器获取数据,返回单个sql语句
        self.driver.maximize_window()
        self.driver.get(url)
        _weather_text = WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, UIGetWeatherData.weather_css))).text
        # print(_weather_text)
        logger_info("天气获取成功{}".format(_weather_text))
        try:
            weather_text = "".join(re.findall("(.*?)\/", _weather_text)[0].split())[0:1]
            update_sql = "update j8 set weather='%s' where date='%s'" % (weather_text,re.findall("2018/(.*?)/live",url)[0])
            logger_info("天气更新语句生成成功{}".format(update_sql))
            return update_sql
        except:
            logger_warning("天气更新语句生成失败{}".format(update_sql))

    def _get_insert_sql(self):
        #返回所有sql语句列表
        insert_sql = []
        for i in self._geturl():
            insert_sql.append(self._openB_getW(i))
        return insert_sql
    def run(self):
        #插入数据
        for i in self._get_insert_sql():
            try:
                self.update_db(i)
            except:
                logger_warning("{}插入失败".format(i))
        self.driver.quit()
'''
class Get500Data(mysqlOP):
    #需要修改self._level 的级别
    def __init__(self):
        super(Get500Data, self).__init__()

        self.headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self._level  = "A"
        self._zhu    = ""
        self._date   = ""
        self._asia   = ""
        self._win    = ""
        self._draw   = ""
        self._lose   = ""
        self._timeout= 30
    def _getmatchtime(self):
        #数据库中查找asia为空的数据的所有数据,返回date % 0224列表
        match_date = []
        list_ = self.search_db("select distinct(left(date,4)),asia from j8 where level ='%s'" % self._level)
        # print (list_)
        for i in list_:
            if i[1] == "":
                match_date.append(i[0])
        logger_info("查找asia字段成功{}".format(match_date))
        return match_date

    def _get5url(self):

        pin_all_url = []
        url_tmp = "http://live.500.com/?e=2018-"
        for i in self._getmatchtime():
            _url_ = url_tmp+i[0:2]+"-"+i[2:4]
            pin_all_url.append(_url_)
            logger_info("500url生成成功{}".format(_url_))
        return pin_all_url

    def _getupdatesql(self):
        update_sql = []
        for i in self._get5url():
            update_sql +=self._getdata(i)
        # print(update_sql)
        logger_info("全部sql生成成功")
        return  update_sql

    @staticmethod
    def getzhuandke(self):
        #查到主客队信息,格式如下{'Ｃ大阪': '横浜FM'}
        dist ={}
        _zhu_info =[]
        _sql = "select zhu,ke from j8 where asia = '' and left(date,4)={} and level='{}';"
        for i in self._getmatchtime():
            _zhu_info += self.search_db(_sql.format(i,self._level))
        for i in _zhu_info:
            dist.update({i[0]: i[1]})
        logger_info("主客队生成成功"+self.getzhuandke.__name__)
        return dist

    def _getdata(self,url):
        _urll = []
        file_txt = requests.get(url=url,headers=self.headers).content.decode("gbk").encode("utf-8").decode("utf-8")
        date4 = url[-5::].replace("-","")

        team = self.getzhuandke(self)
        for key,val in team.items():
            self._zhu =getkey(Team_A,key)
            self._ke  =getkey(Team_A,val)
            # logger_info("主队 {},客队 {}".format(self._zhu,self._ke))
            _datadict = eval(re.findall("liveOddsList=(.*?);", file_txt, re.S)[0]) #所有赔率列表
            k = re.findall("<tr(.*?)"+self._zhu+","+self._ke,file_txt)
            # print(k)
            if k !=[]:
                id_number = re.findall("id=\"a(.*?)\"",k[0])[0]
                _peilv =_datadict.get(id_number)['3']#赔率列表
                level1 = re.findall(id_number + "&r=1\"" + "(.*?)"+"</a>",file_txt,re.S)[1]#查找亚洲盘
                logger_info("{}id={}赔率:{}".format(self._zhu, id_number,_peilv))
                self._win  = "%.2f" % _peilv[0]
                self._draw = "%.2f" % _peilv[1]
                self._lose = "%.2f".format(_peilv[2])
                self._asia = re.findall("\">(.*?)$",level1)[0]
                updatesql = (
                            "update j8 set asia='%s',win='%s',draw='%s',lose='%s' where zhu='%s' and left(date,4)='%s'" % (
                    self._asia, self._win, self._draw, self._lose, Team_A[self._zhu], date4))
                _urll.append(updatesql)
                logger_info("sql增加成功{}".format(updatesql))
            else:
                pass
        return(_urll)
    def _writeDb(self,sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is None:
            logger_warning("sql语句无数据")
        _zhu = re.findall("zhu=\'(.*?)\'",sql_lan,re.S)[0]
        _left_date = re.findall("\)=\'(.*?)\'",sql_lan,re.S)[0]
        logger_info("插入前查询{} {}".format(_zhu,_left_date))
        if _zhu is not []:
            if self.search_db("select asia from j8 where zhu ='%s' and left(date,4)='%s' " % (_zhu,_left_date))[0][0] != "":
                logger_info("数据不为空 {}".format(sql_lan))
            else:
                self.update_db(sql_lan)
                logger_info("数据插入成功 {}".format(sql_lan))
        else:
            logger_warning("zhu列匹配数据失败")
    def run(self):
        for i in self._getupdatesql():
            self._writeDb(i)
def main():
    GetJleagueData().run()
    Get500Data().run()

if __name__ == '__main__':
    main()