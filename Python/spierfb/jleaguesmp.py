# coding: utf-8
import mysql.connector
import re,time,mysql.connector,requests,sys
import logging
import logging.handlers

import pyquery
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

import datetime,time,mysql.connector,configparser,re,requests,yaml
import lxml.html
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def logConfig():

    logger = logging.getLogger("j")
    logger.setLevel(logging.DEBUG)                      # 全局默认级别WARNING
    ch = logging.StreamHandler()                        # 生成Handler对象
    ch.setLevel(logging.DEBUG)
    # fh = logging.FileHandler("./" + "//log//log.txt", encoding="utf8")
    fh = logging.FileHandler("./log.log", encoding="utf8")
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")# 把formatter对象 绑定到Handler对象
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)
    logger.addHandler(ch)                               # 把Handler对象 绑定到logger
    logger.addHandler(fh)
    return logger

log = logConfig()

def Logd(msg):
    log.debug(msg)

def Logi(msg):
    log.info(msg)

def Logw(msg):
    log.warning(msg)

def Loge(msg):
    log.error(msg)

def Logc(msg):
    log.critical(msg)




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
cf.read("./peizhi.ini")


file = open("./run.yml", "r", encoding="utf8")
conff = yaml.load(file.read(), Loader=yaml.Loader)
conf = conff['control']


def rt():
    import random
    t = [1.6,1.5,2.0,1.6,1,1.1,1.2,1.3,1.4]
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
        self.cursor = self.conn.cursor()
    def search(self, sql):

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

class GetOldData(object):
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
        self.start_url = "https://www.jleague.jp/match/j2/2020/{}/live/"
        self.headers   = j_headle
        self.proxies   = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}

    def run(self):
        startcount = conf['startcount']
        for l in startcount:
            n = 0
            while n < 13:
                n += 1
                l += 1
                starturl = self.start_url.format("%06d" % (l))
                self.get_update_sql(starturl)
        Logi("j all sql update done" )

    @staticmethod
    def _get_level(txt):
        level_pool = {"Ｊ１": "A", "Ｊ２": "B", "Ｊ３": "C", "天皇杯": "K", "YBC": "L"}
        for key in level_pool:
            if key in txt:
                return level_pool.get(key)

    def get_update_sql(self,url):
        n = 0
        Logi("start request {}".format(url))
        try:
            self.html = requests.get(url, verify=False, headers = self.headers)                 # , proxies=self.proxies
            # print(self.html.text)
        except (Exception) as e:
            Loge(e)
            Loge("{} request error".format(url))
            return

        Logi("request stutas:={}".format(self.html.status_code))
        if self.html.status_code != 200:
            Loge("{} not exist".format(url))
            self.html.close()
            return False
        time.sleep(rt())
        selector =lxml.html.fromstring(self.html.text)
        soup = BeautifulSoup(self.html.text, 'lxml')

        # get match info
        info = selector.cssselect("p span")

        # if (len(re.findall("\d+", "".join(selector.xpath(cf.get("css", "level_css"))), re.S)) == 0):return False
        jicon = re.findall("\d+", "".join(selector.xpath(cf.get("css", "level_css"))), re.S)
        # print(jicon)
        if len(jicon) == 1: return False

        self.zhu = info[0].text    # 主
        self.ke = info[-2].text   # 客
        self.bc = info[3].text + "-" + info[5].text   # 半场 zj
        self.zc = info[6].text    # zc
        self.kc = info[14].text   # kc
        self.zj = selector.cssselect(".leagLeftScore")[0].text # zj
        self.kj = selector.cssselect(".leagRightScore")[0].text # kj

        self.round = re.findall("\d+", "".join(selector.xpath(cf.get("css", "level_css"))), re.S)[1]

        self.level = self._get_level("".join(selector.xpath(cf.get("css","level_css"))))

        self.date = re.findall("2020/(.*?)/live", soup.link['href'])[0]

        # get weather
        weatherUrl = url.replace("live/","ajax_live?_={}T{}")                                      #天气信息ajax动态加载的.拼ajax的url
        weatherUrl.format(datetime.date.today(),time.strftime('%H:%M',time.localtime(time.time())))
        weather_page = requests.get(weatherUrl, verify=False, headers=self.headers).content.decode()
        weather_info = lxml.html.fromstring(weather_page)
        weather_info_list = weather_info.cssselect(".bgGray + td")

        self.weather = "".join(re.findall("(.*?)\/", weather_info_list[5].text))[:1]

        # get start time
        ss = pyquery.PyQuery(self.html.text)
        sk = ss.find(cf.get("css","sj_css")).text()
        self.st = re.findall("\d+\:\d+", sk)[0].replace(":","")

        _insertsql = "INSERT INTO `j8` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,
            self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")
        Logi("sql:={}".format(_insertsql))
        self.html.close()
        self.write2Db(_insertsql)
        return True


    def write2Db(self,sqlyuju):
        sql_lan = sqlyuju
        if sql_lan is []: Loge("sql is empty [] ")

        data = re.findall("\'(.*?)\'\,",sql_lan)
        if data is []:
            Loge("匹配数据失败")
        _date = data[0]
        if ms.search("select * from j8 where date ='%s'" % _date) != []:
            Logi("{} exist,don't insert".format(_date))

        else:
            try:
                ms.update(sql_lan)
                Logi("j data insert successfully")
            except (Exception ) as e:
                Loge("{} insert fail".format(sql_lan))


class Get500Data(object):
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

    def run(self):

        for i in self.get5url():
            self._getdata(i)
        Logi("all sql update done")

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
            Logi("主:={}&客:={}".format(self._zhu,self._ke))
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
                self.writeSql(updatesql)
                return
            else:
                Loge("{} not found data".format(url))
                return
    def writeSql(self, sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is []: Loge("sql not found ")

        zhu_team = re.findall("zhu=\'(.*?)\'",sql_lan,re.S)[0]
        left_date = re.findall("\)=\'(.*?)\'",sql_lan,re.S)[0]
        Logi("{} {} Exist ?".format(left_date,zhu_team))
        if zhu_team is not []:
            if ms.search("select asia from j8 where zhu ='%s' and left(date,4)='%s' " % (zhu_team, left_date))[0][0] != "":
                Logi("data exist don't insert  {}".format(sql_lan))
            else:
                try:
                    ms.update(sql_lan)
                    Logi("500 insert success")
                except (Exception) as e:
                    Loge("{} fail".format(sql_lan))
        else:
            Loge("zhu列匹配数据失败")

def main():
    # GetOldData().run()
    Get500Data().run()

if __name__ == '__main__':
    main()

