import mysql.connector,datetime,time,re,requests,yaml,lxml.html,pyquery
from bs4 import BeautifulSoup
from Python.spierfb.logmodule import Logi,Loge
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


Team_A = {  # all j team
    "浦和红钻":"浦和","大阪樱花":"Ｃ大阪","鹿岛鹿角":"鹿島","名古屋鲸":"名古屋","鸟栖沙岩":"鳥栖",
    "广岛三箭":"広島","清水鼓动":"清水","东京FC":"FC東京","大阪钢巴":"Ｇ大阪","川崎前锋":"川崎Ｆ",
    "磐田喜悦":"磐田","仙台七夕":"仙台","神户胜利":"神戸","长崎航海":"長崎","枥木SC":"栃木",
    "横滨水手":"横浜FM","札幌冈萨":"札幌","柏太阳神":"柏","湘南海洋":"湘南","横滨FC":"横浜FC",
	"福冈黄蜂":"福岡","水户蜀葵":"水戸","金泽塞维":"金沢","松本山雅":"松本","东京绿茵":"東京Ｖ",
    "千叶市原":"千葉","冈山绿雉":"岡山","德岛漩涡":"徳島","山形山神":"山形","北九州":"北九州",
    "爱媛FC":"愛媛","山口雷诺":"山口","甲府风林":"甲府","大宫松鼠":"大宮","秋田闪电":"秋田",
    "岐阜FC":"岐阜","大分三神":"大分","町田泽维":"町田","新泻天鹅":"新潟","相模原SC":"相模原",
    "京都":"京都","赞岐釜玉":"讃岐","熊本深红":"熊本","群马温泉":"群馬","琉球FC":"琉球"

}

j_headle ={ # j header
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


def getkey(_dict,_value):
    return list(_dict.keys())[list(_dict.values()).index(_value)]

def ryaml(key, peer="control"): # read yaml file
    # read yaml file
    file = open("../spierfb/run.yml", "r", encoding="utf8")
    config = yaml.load(file.read(), Loader=yaml.Loader)
    conf = config[peer]
    return conf[key]

def rt():  # random jiange time
    import random
    t = [1.2,2.3,1.4,1.5,1.6,1.7,1.8,1.9,1]
    s = random.choice(t)
    return s

def getlevel(txt):
    level_pool = {"Ｊ１": "A", "Ｊ２": "B", "Ｊ３": "C", "天皇杯": "K", "YBC": "L"}
    for key in level_pool:
        if key in txt:
            return level_pool.get(key)

class MsqService(object):

    def __init__(self):
        self.conn = mysql.connector.connect(host=ryaml("host","db"), user=ryaml("user","db"), password=ryaml("password","db"),
                                            database=ryaml("dbname","db"),use_unicode=True)
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
        try:
            self.conn.close()
            self.cursor.close()
        except:
            pass

ms = MsqService()

class GetJleague():
    def __init__(self):
        self.level     = ryaml('level')
        self.round     = ""
        self.st        = ""
        self.status    = False
        self.bc        = ""
        self.zhu       = ""
        self.ke        = ""
        self.zc        = ""
        self.kc        = ""
        self.roundUrl  = "https://www.jleague.jp/match/section/j1/{}/"
        self.headers   = j_headle
        self.proxies   = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}

    def run(self):
        _url = self.getUrl()
        for l in _url:
            self.get_update_sql(l)
        Logi("j update done")

    def get_update_sql(self,url):

        Logi("start request {}".format(url))
        try:
            self.html = requests.get(url, verify=False, headers = self.headers)                 # , proxies=self.proxies
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

        jicon = re.findall("\d+", "".join(selector.xpath(ryaml("level_css", "css"))), re.S)
        if len(jicon) == 1: return False

        self.zhu = info[0].text    # 主
        self.ke = info[-2].text    # 客
        self.bc = info[3].text + "-" + info[5].text   # 半场 bc
        self.zc = info[12].text    # zc
        self.kc = info[14].text    # kc
        self.zj = selector.cssselect(".leagLeftScore")[0].text # zj 主进
        self.kj = selector.cssselect(".leagRightScore")[0].text # kj 客进
        self.round = re.findall("\d+", "".join(selector.xpath(ryaml("level_css", "css"))), re.S)[1]
        self.level = getlevel("".join(selector.xpath(ryaml("level_css","css"))))
        self.date = re.findall("2021/(.*?)/live", soup.link['href'])[0]

        # get weather
        weatherUrl = url.replace("live/","ajax_live?_={}T{}")                                      #天气信息ajax动态加载的.拼ajax的url
        weatherUrl.format(datetime.date.today(),time.strftime('%H:%M',time.localtime(time.time())))
        weather_page = requests.get(weatherUrl, verify=False, headers=self.headers).content.decode()
        weather_info = lxml.html.fromstring(weather_page)
        weather_info_list = weather_info.cssselect(".bgGray + td")

        self.weather = "".join(re.findall("(.*?)\/", weather_info_list[4].text))[:1]

        # get start time
        ss = pyquery.PyQuery(self.html.text)
        sk = ss.find(ryaml("sj_css","css")).text()
        self.st = re.findall("\d+\:\d+", sk)[0].replace(":","")

        _insertsql = "INSERT INTO `j21` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            self.date, self.st, self.level, self.round, self.weather, self.zhu, "", self.ke, self.bc,self.zj, self.kj, self.zc, self.kc, "9.99", "9.99", "9.99")

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
        if ms.search("select * from j21 where date ='%s'" % _date) != []:
            Logi("{} exist,don't insert".format(_date))

        else:
            try:
                ms.update(sql_lan)
                Logi("j data insert successfully")
            except (Exception ) as e:
                Loge("{} insert fail".format(sql_lan))

    def getUrl(self):
        allUrl = list()
        _url = self.roundUrl.format(ryaml("round"))
        indexhtml = requests.get(url=_url, verify=False, headers=self.headers)
        selector = lxml.html.fromstring(indexhtml.text)
        info = selector.cssselect("li a")
        for i in info:
            if i.text == '試合詳細':
                allUrl.append("https://www.jleague.jp"+i.get("href"))
        return allUrl

class Get500Data(object):
    #需要修改self._level 的级别
    def __init__(self):

        self.headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self._level  = ryaml('level')
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
        list_ = ms.search("select distinct(left(date,4)),asia from j21 where level ='%s'" % self._level)
        # print (list_)
        for i in list_:
            if i[1] == "":
                match_date.append(i[0])
        Logi("asia null date:={}".format(match_date))
        return match_date

    def get5url(self):
        # return all 500 url -> list()
        url_500 = []
        url_tmp = "http://live.500.com/?e={}-".format(ryaml('year'))
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
        update_sql = "select zhu,ke from j21 where asia = '' and left(date,4)={} and level='{}';"
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
                            "update j21 set asia='%s',win='%s',draw='%s',lose='%s' where zhu='%s' and left(date,4)='%s'" % (
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
            if ms.search("select asia from j21 where zhu ='%s' and left(date,4)='%s' " % (zhu_team, left_date))[0][0] != "":
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
    # GetJleague().run()
    Get500Data().run()

if __name__ == '__main__':
    main()
