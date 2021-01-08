
import datetime,time,mysql.connector,configparser,re,requests,yaml
import lxml.html
import requests
from bs4 import BeautifulSoup
from Python.spierfb.logmodule import Logi,Loge,Logd,Logc
from abc import ABCMeta,abstractclassmethod
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
    "东京绿茵":"東京Ｖ","横滨FC":"横浜FC","枥木SC":"栃木","北九州":"北九州",
    "琉球FC":"琉球"
}
def getkey(_dict,_value):
    return list(_dict.keys())[list(_dict.values()).index(_value)]

cf = configparser.ConfigParser()
cf.read("../spierfb/peizhi.ini")


file = open("../spierfb/run.yml", "r", encoding="utf8")
conff = yaml.load(file.read(), Loader=yaml.Loader)
conf = conff['control']



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



class GetJleagueData(MsqService):
    #需要修改start_url ,_get1url中start ,end轮数
    def __init__(self):
        super(GetJleagueData,self).__init__()

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
        Logi("一级URL获取完成")
        return _firstURL

    def _get2url(self):
        #第二级URL
        secondURL= []
        _str = "https://www.jleague.jp"
        for i in self._get1url():
            html = requests.get(i, verify=False, headers=self.headers) #proxies=self.proxies,
            # html = requests.get(i, verify=False, headers=self.headers, proxies=self.proxies) #
            k = re.findall("href=\"(.*?)\">試合詳細",html.text)
            # print(k)
            if k != []:
                for s in k:
                    secondURL.append(_str+s)
        Logi("二级URL获取完成")
        return secondURL

    @staticmethod
    def _get_level(txt):
        level_pool = {"Ｊ１": "A", "Ｊ２": "B", "Ｊ３": "C", "天皇杯": "K", "YBC": "L"}
        for key in level_pool:
            if key in txt:
                return level_pool.get(key)

    def get_sql(self,url):
        self.html = requests.get(url, verify=False, headers=self.headers)
        selector =lxml.html.fromstring(self.html.text)
        soup = BeautifulSoup(self.html.text, 'lxml')

        new_url = url.replace("live/","ajax_live?_={}T{}") #天气信息ajax动态加载的.拼ajax的url
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
        self.ke      = "".join(selector.xpath(cf.get("css","ke_css")))
        self.bc      = selector.xpath(cf.get("css","zjc_css"))[0]+"-"+selector.xpath(cf.get("css","kjc_css"))[0]
        self.kj      = "".join(selector.xpath(cf.get("css","kj_css")))
        self.zj      = "".join(selector.xpath('//div[@class="leagLeftScore"]/text()'))
        self.zc      = "".join(selector.xpath(cf.get("css","zc_css")))
        self.kc      = "".join(selector.xpath(cf.get("css","kc_css")))
        self.level   = self._get_level("".join(selector.xpath(cf.get("css","level_css"))))
        self.st      = "".join(selector.xpath(cf.get("css","sj_css"))).replace(":","")
        self.round   = re.findall("\d+","".join(selector.xpath(cf.get("css","level_css"))),re.S)[1]
        self.date    = re.findall("2020/(.*?)/live",soup.link['href'])[0]
        print(re.findall("(.*?)\/", s[-3]))
        self.weather = "".join(re.findall("(.*?)\/", s[-3])[0].split())[0:1]

        _insertsql = "INSERT INTO `j8` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,
            self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")
        Logi("sql:={}".format(_insertsql))
        return  _insertsql

    def _writeDB(self, sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is None:
            Loge("sql语句无数据")
        data = re.findall("\'(.*?)\'\,",sql_lan)
        if data is []:
            Loge("匹配数据失败")
        _date = data[0]
        if self.search("select * from j8 where date ='%s'" % _date) != []:
            Loge("'%s'数据库中已存在" % _date)
        else:
            self.update(sql_lan)
            Logi("j data insert successfully")

    def _get_all_sql(self): #返回所有的sql语句
        all_sql = []
        for i in self._get2url():
            try:
                all_sql.append(self.get_sql(i))
            except:
                raise("数据返回失败")
        Logi("all sql:=" % all_sql)
        return all_sql

    def run(self):
        for k in self._get_all_sql():
            try:
                self._writeDB(k)
            except:
                continue
                Loge("{} insert fail".format(k))
class Get500Data(MsqService):
    #需要修改self._level 的级别
    def __init__(self):
        super(Get500Data, self).__init__()

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
        list_ = self.search("select distinct(left(date,4)),asia from j8 where level ='%s'" % self._level)
        # print (list_)
        for i in list_:
            if i[1] == "":
                match_date.append(i[0])
        Logi("asia null date:={}".format(match_date))
        return match_date

    def get5url(self):
        # return all 500 url ,
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
        print(update_sql)
        Logi("A_sql:= {}".format(update_sql))
        return  update_sql

    def get_match_team(self,date):
        # match_team_dict = dict()
        match_team_list = list()
        update_sql = "select zhu,ke from j8 where asia = '' and left(date,4)={} and level='{}';"
        match_team_list += self.search(update_sql.format(date,self._level))
        match_team_dict = dict(match_team_list)

        return match_team_dict


    def _getdata(self,url):
        _urll = []
        file_txt = requests.get(url=url,headers=self.headers).content.decode("gbk").encode("utf-8").decode("utf-8")
        match_date = url[-5::].replace("-","")

        team = self.get_match_team(match_date)
        for key,val in team.items():
            self._zhu =getkey(Team_A,key)
            self._ke  =getkey(Team_A,val)
            # logger_info("主队 {},客队 {}".format(self._zhu,self._ke))
            # print(re.findall("var liveOddsList = (.*?);", file_txt, re.S)[0])
            try:
                _datadict = eval(re.findall("var liveOddsList = (.*?);", file_txt, re.S)[0])
            except Exception as e:
                print(e)
            k = re.findall("<tr(.*?)"+self._zhu+","+self._ke,file_txt)
            # print(k)
            if k !=[]:
                id_number = re.findall("id=\"a(.*?)\"",k[0])[0]
                _peilv =_datadict.get(id_number)['3']#赔率列表
                level1 = re.findall(id_number + "&r=1\"" + "(.*?)"+"</a>",file_txt,re.S)[1]#查找亚洲盘
                Logi("{} id={} 赔率={}".format(self._zhu, id_number,_peilv))
                self._win  = "%.2f" % float(_peilv[0])
                self._draw = "%.2f" % float(_peilv[1])
                self._lose = "%.2f" % float(_peilv[2])
                self._asia = re.findall("\">(.*?)$",level1)[0]
                updatesql = (
                            "update j8 set asia='%s',win='%s',draw='%s',lose='%s' where zhu='%s' and left(date,4)='%s'" % (
                    self._asia, self._win, self._draw, self._lose, Team_A[self._zhu], match_date))
                _urll.append(updatesql)
                Logi("sql增加成功{}".format(updatesql))
            else:
                pass
        return(_urll)
    def writeSql(self, sqlyuju):

        sql_lan = sqlyuju
        if sql_lan is None:
            Loge("sql语句无数据")
        _zhu = re.findall("zhu=\'(.*?)\'",sql_lan,re.S)[0]
        _left_date = re.findall("\)=\'(.*?)\'",sql_lan,re.S)[0]
        Logi("插入前查询{} {}".format(_zhu,_left_date))
        if _zhu is not []:
            if self.search("select asia from j8 where zhu ='%s' and left(date,4)='%s' " % (_zhu, _left_date))[0][0] != "":
                Logi("数据不为空 {}".format(sql_lan))
            else:
                try:
                    self.update(sql_lan)
                    Logi("数据插入成功 {}".format(sql_lan))
                except:
                    pass
        else:
            Loge("zhu列匹配数据失败")
    def run(self):
        for i in self._getupdatesql():
            self.writeSql(i)
def main():
    GetJleagueData().run()
    Get500Data().run()

if __name__ == '__main__':
    main()