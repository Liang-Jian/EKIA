import mysql.connector, datetime, time, re, requests, yaml, lxml.html, pyquery, logging, logging.handlers, os, sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.support.select import Select

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from selenium import webdriver
import concurrent.futures
import threading

JTeam = {  # all j team
    "浦和红钻": "浦和", "大阪樱花": "Ｃ大阪", "鹿岛鹿角": "鹿島", "名古屋鲸": "名古屋", "鸟栖沙岩": "鳥栖",
    "广岛三箭": "広島", "清水鼓动": "清水", "东京FC": "FC東京", "大阪钢巴": "Ｇ大阪", "川崎前锋": "川崎Ｆ",
    "磐田喜悦": "磐田", "仙台七夕": "仙台", "神户胜利": "神戸", "长崎航海": "長崎", "枥木SC": "栃木",
    "横滨水手": "横浜FM", "札幌冈萨": "札幌", "柏太阳神": "柏", "湘南海洋": "湘南", "横滨FC": "横浜FC",
    "福冈黄蜂": "福岡", "水户蜀葵": "水戸", "金泽塞维": "金沢", "松本山雅": "松本", "东京绿茵": "東京Ｖ",
    "千叶市原": "千葉", "冈山绿雉": "岡山", "德岛漩涡": "徳島", "山形山神": "山形", "北九州": "北九州",
    "爱媛FC": "愛媛", "山口雷诺": "山口", "甲府风林": "甲府", "大宫松鼠": "大宮", "秋田闪电": "秋田",
    "岐阜FC": "岐阜", "大分三神": "大分", "町田泽维": "町田", "新泻天鹅": "新潟", "相模原SC": "相模原",
    "京都": "京都", "赞岐釜玉": "讃岐", "熊本深红": "熊本", "群马温泉": "群馬", "琉球FC": "琉球"

}

Team_PL = {  # all 007 team
    "浦和红钻": "浦和", "大阪樱花": "Ｃ大阪", "鹿岛鹿角": "鹿島", "名古屋鲸八": "名古屋", "鸟栖沙岩": "鳥栖",
    "广岛三箭": "広島", "清水鼓动": "清水", "FC东京": "FC東京", "大阪钢巴": "Ｇ大阪", "川崎前锋": "川崎Ｆ",
    "磐田喜悦": "磐田", "仙台维加泰": "仙台", "神户胜利船": "神戸", "长崎航海": "長崎", "枥木SC": "栃木",
    "横滨水手": "横浜FM", "札幌冈萨多": "札幌", "柏太阳神": "柏", "湘南海洋": "湘南", "横滨FC": "横浜FC",
    "福冈黄蜂": "福岡", "水户蜀葵": "水戸", "金泽塞维": "金沢", "松本山雅": "松本", "东京绿茵": "東京Ｖ",
    "千叶市原": "千葉", "冈山绿雉": "岡山", "德岛漩涡": "徳島", "山形山神": "山形", "北九州": "北九州",
    "爱媛FC": "愛媛", "山口雷诺": "山口", "甲府风林": "甲府", "大宫松鼠": "大宮", "秋田闪电": "秋田",
    "岐阜FC": "岐阜", "大分三神": "大分", "町田泽维": "町田", "新泻天鹅": "新潟", "相模原SC": "相模原",
    "京都不死鸟": "京都", "赞岐釜玉": "讃岐", "熊本深红": "熊本", "群马温泉": "群馬", "FC琉球": "琉球","群马草津温泉":"群馬",
    "町田泽维亚":"町田","山口雷法":"山口","长崎成功丸":"長崎"

}

J_Header = {  # j header
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
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


def ryaml(key, peer="control"):
    # read yaml file
    homept = os.path.expanduser('~')
    _f = open(f"{homept}/EKIA/python/spierfb/run.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    conf = config[peer]
    _f.close()
    return conf[key]


class msq:

    def __init__(self):
        self.conn = mysql.connector.connect(host=ryaml("host", "db"), user=ryaml("user", "db"),
                                            password=ryaml("password", "db"),
                                            database=ryaml("dbname", "db"), use_unicode=True)
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
        finally:
            pass


def logconfig():
    logger = logging.getLogger("s")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    homept = os.path.expanduser('~')
    fh = logging.FileHandler(f"{homept}/EKIA/python/spierfb/log.log", encoding="utf8")
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%H-%M-%S')
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%H-%M-%S')
    ch.setFormatter(console_formatter)
    fh.setFormatter(file_formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def Logi(msg):
    log.info(msg)


def Loge(msg):
    log.error(msg)


def getkey(_dict, _value):
    return list(_dict.keys())[list(_dict.values()).index(_value)]


def getlevel(txt):
    level_pool = {"j1": "A", "j2": "B", "j3": "C", "天皇杯": "K", "leaguecup": "L"}
    for key in level_pool:
        if key in txt:
            return level_pool.get(key)


def getUrl():
    all_url = list()
    indexhtml = requests.get(
        url='https://www.jleague.jp/match/', verify=False, headers=J_Header, timeout=60)

    # indexhtml = requests.get(url='https://www.jleague.jp/match/section/j3/2/',verify=False,headers=J_Header)
    selector = lxml.html.fromstring(indexhtml.text)
    info = selector.cssselect("li a")
    for i in info:
        if i.text == '試合詳細':
            all_url.append(i.get("href"))
    return all_url


log = logconfig()
ms = msq()
lock = threading.Lock()


def w2db(_sql):
    lock.acquire()  # sql insert need source
    if _sql is None: Loge("sql is empty [] ")
    data = re.findall("\'(.*?)\'\,", _sql)
    if data is []: Loge("匹配数据失败")
    _date = data[0]
    if ms.search("select * from j22 where date ='{}'".format(_date)) != []:
        Logi("{} exist,don't insert".format(_date))
    else:
        try:
            ms.update(_sql)
            Logi("j data insert successfully")
        except (Exception,):
            Loge("fail {}".format(_sql))
    lock.release()


def get_every_j_data(_url):
    url = "https://www.jleague.jp{}".format(_url)
    __level = getlevel(re.findall('/match/(.*)/2022', _url)[0])
    __round = ""
    __st = ""
    __status = False
    __bc = ""
    __zhu = ""
    __ke = ""
    __zc = ""
    __kc = ""
    Logi("start request {}".format(url))
    try:
        html = requests.get(url, verify=False, headers=J_Header, timeout=23)  # , proxies=self.proxies
    except(Exception,):
        Loge("{} request error".format(url))
        return
    Logi("request stutas:={}".format(html.status_code))
    time.sleep(.1)
    selector = lxml.html.fromstring(html.text)
    soup = BeautifulSoup(html.text, 'lxml')
    # get match info
    info = selector.cssselect("p span")
    __zhu = info[0].text  # 主
    __ke = info[-2].text  # 客
    __bc = info[3].text + "-" + info[5].text  # 半场 bc
    __zc = info[12].text  # zc
    __kc = info[14].text  # kc
    __zj = selector.cssselect(".leagLeftScore")[0].text  # zj 主进
    __kj = selector.cssselect(".leagRightScore")[0].text  # kj 客进
    __round = re.findall("第(.*?)節", "".join(selector.xpath('//span[@class=\'matchVsTitle__league\']/text()')))[-1]
    __date = re.findall("2022/(.*?)/live", soup.link['href'])[0]
    # get weather
    weather_url = url.replace("live/", "ajax_live?_={}T{}")  # 天气信息ajax动态加载的.拼ajax的url
    weather_url.format(datetime.date.today(), time.strftime('%H:%M', time.localtime(time.time())))
    weather_page = requests.get(weather_url, verify=False, headers=J_Header).content.decode()
    time.sleep(1)
    weather_info = lxml.html.fromstring(weather_page)
    weather_info_list = weather_info.cssselect(".bgGray + td")
    weather = "".join(re.findall("(.*?)\/", weather_info_list[4].text))[:1]
    # get start time
    ss = pyquery.PyQuery(html.text)
    sk = ss.find(ryaml("sj_css", "css")).text()
    st = re.findall("\d+\:\d+", sk)[0].replace(":", "")
    _sql = "INSERT INTO `j22` VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
        __date, st, __level, str(int(__round)), weather, __zhu, "", __ke, __bc, __zj, __kj, __zc, __kc, "9.99", "9.99",
        "9.99")
    Logi(f"sql:={_sql}")
    html.close()
    w2db(_sql)
    return True



L = 'A'
class GetPeilv:
    from selenium import webdriver
    def __init__(self):
        '''
        从球探上获取数据，取代500 . 先用webdriver -> pagesource -> id,name -> peilv -> create sql -> done
        '''
        self.A = "http://zq.win007.com/cn/SubLeague/2022/25.html"
        self.B = "http://zq.win007.com/cn/SubLeague/2022/284.html"
        self.durl = "http://zq.win007.com/League/LeagueOddsAjax"
        self.level = L
        self.page_source = ""
        self.zhu = ""
        self.win = ""
        self.draw = ""
        self.lose = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}


    def insert_before(self):
        #
        sql_list = ms.search("select distinct(round) from j22 where level='%s' and win='9.99'" % self.level)
        round_list = [x[0] for x in sql_list]
        args = (self.level, round_list)
        return args

    def run(self):
        level,round_l = self.insert_before()
        print(round_l)
        if round_l is []: return
        win007_index = webdriver.Chrome('/usr/local/bin/chromedriver')
        if level == 'A':
            win007_index.get(self.A)
            time.sleep(1)
            win007_index.find_element_by_css_selector('#leagueDiv2 > ul > li:nth-child(1) > a').click()
            time.sleep(1)
            for r in round_l:
                win007_index.find_element_by_css_selector(f'#Table2 > tbody > tr:nth-child(1) > td:nth-child({1+int(r)})').click()
                time.sleep(4)
                self.page_source = win007_index.page_source
                peilvstr = re.compile('<tr (.*?)</a><sup')
                infolist = peilvstr.findall(self.page_source)
                # print(infolist)
                for k in infolist:
                    _id = re.findall("\d+", k)[0]  # id
                    _zhu = re.findall("k\">(.*)", k)[0]  # 主队
                    print(_id, _zhu)
                    self.getPeilv(_id, _zhu, r)
        elif level == 'B':
            win007_index.get(self.B)
            time.sleep(1)
            win007_index.find_element_by_css_selector('#leagueDiv2 > ul > li:nth-child(2) > a').click()
            time.sleep(1)
            for r in round_l:
                win007_index.find_element_by_css_selector(f'#Table2 > tbody > tr:nth-child(1) > td:nth-child({1+int(r)})').click()
                time.sleep(1)
                self.page_source = win007_index.page_source
                peilvstr = re.compile('<tr (.*?)</a><sup')
                infolist = peilvstr.findall(self.page_source)
                # print(infolist)
                for k in infolist:
                    _id = re.findall("\d+", k)[0]  # id
                    _zhu = re.findall("k\">(.*)", k)[0]  # 主队
                    print(_id, _zhu)
                    self.getPeilv(_id, _zhu, r)


    def getPeilv(self, id, zhu, round):
        requestdata = {
            "sclassId": '25',
            "subSclassId": "943",
            "matchSeason": "2022",
            "round": str(round),
            "flesh": "0.23699970411978874"
        }
        int = id
        if self.level =='B':
            requestdata['sclassId'] = '284'
            requestdata['subSclassId'] = '808'
        peilv = requests.get(url=self.durl, params=requestdata, headers=self.headers)
        print(peilv.text)
        recompile = re.compile('oddsData\[\"O_{}\"\]=(.*?)]]'.format(int))  # 正则对象
        findStr = recompile.search(peilv.text)
        if findStr is None: return
        findStr1 = recompile.search(peilv.text).group()[22::]
        finddict = eval(findStr1)
        for key in finddict:
            if key[0] == 281:
                # print(key[1], key[2], key[3])
                self.win = key[1]
                self.draw = key[2]
                self.lose = key[3]
                updatesql = (
                        "update j22 set win='%s',draw='%s',lose='%s' where zhu='%s' and round='%s'" % (
                    self.win, self.draw, self.lose, Team_PL[zhu], round))
                Logi(updatesql)
                self.writeSql(zhu, updatesql, round)

    def writeSql(self, zhu_, sqlyuju, round):
        sql_lan = sqlyuju
        if sql_lan is []:
            Loge("sql not found ")
        else:
            try:
                if ms.search("select win from j22 where zhu ='%s' and round='%s' " % (Team_PL[zhu_], round))[0][0] != 9.99:
                    Logi("peil exist don't insert")
                else:
                    ms.update(sql_lan)
                    Logi("pv update succ={}\n".format(sql_lan))
            except(IndexError,):
                print(f'{sql_lan} error')


class GetAsia:
    from selenium import webdriver
    requestdata = {
        "sclassId": "25",
        "subSclassId": "943",
        "matchSeason": "2022",
        "round": ryaml("round"),
        "flesh": "0.29982359072620323"
    }

    '''
    1，查询赔率为空的所有set， 轮数 和 level
    2，打开球探根据set进行查找
    3，写库exit出
    '''
    def __init__(self):
        '''
        从球探上获取数据，取代500 . 先用webdriver -> pagesource -> id,name -> peilv -> create sql -> done
        '''
        self.url = "http://zq.win007.com/cn/SubLeague/2022/25.html"
        self.urlB = "http://zq.win007.com/cn/SubLeague/2021/284.html"
        self.durl = "http://zq.win007.com/League/LeagueOddsAjax"
        self.page_source = ""
        self.zhu = ""
        self.win = ""
        self.draw = ""
        self.lose = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

    def run(self):
        win007_index = webdriver.Chrome('/usr/local/bin/chromedriver')
        win007_index.get(self.url)
        time.sleep(2)
        win007_index.find_element_by_css_selector('#leagueDiv2 > ul > li:nth-child(1) > a').click()
        time.sleep(1)
        win007_index.find_element_by_css_selector('#Table2 > tbody > tr:nth-child(1) > td:nth-child(2)').click()
        self.page_source = win007_index.page_source
        Select(win007_index.find_element_by_css_selector("select#oddsCompany")).select_by_index(2)  # 是否水淹车 否
        time.sleep(1)
        soup = BeautifulSoup(win007_index.page_source)
        # for i in soup.findAll('tr'):
        _l = list()
        for i in soup.find_all(id=re.compile('\d{7}')):
            print(i)
            # print(re.findall(r'[\u4e00-\u9fa5]+', str(i)),end='\r\n')

    def writeSql(self, zhu_, sqlyuju):
        sql_lan = sqlyuju
        if sql_lan is []:
            Loge("sql not found ")
        else:
            if ms.search("select win from j22 where zhu ='%s' and round='%s' " % (Team_PL[zhu_], ryaml('round')))[0][0] != 9.99:
                Logi("peil exist don't insert")
            else:
                ms.update(sql_lan)
                Logi("pv update succ={}\n".format(sql_lan))

def run():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_every_j_data, getUrl())

# if __name__ == '__main__':
run()
    # GetAsia().run()