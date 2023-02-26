import mysql.connector
import datetime
import time
import re
import requests
import yaml
import lxml.html
import pyquery
import logging
import logging.handlers
import os
import threading
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from logging.handlers import TimedRotatingFileHandler
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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


def logconfig(log_name="j"):
    log_obj = logging.getLogger(log_name)
    log_path = os.path.join(os.getcwd(), f"{log_name}_check.log")
    # 设置日志记录等级
    log_obj.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="MIDNIGHT", interval=1, backupCount=30
    )
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s- %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    )
    log_obj.addHandler(file_handler)
    return log_obj


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


def getUrlround(round=0, level='A'):
    # 获取指定轮数的url
    all_url = list()
    __URL = None
    if level == "A":
        __URL = f'https://www.jleague.jp/match/section/j1/{round}/'
    elif level == "B":
        __URL = f'https://www.jleague.jp/match/section/j2/{round}/'
    elif level == "C":
        __URL = f'https://www.jleague.jp/match/section/j3/{round}/'

    idx_html = requests.get(url=__URL, verify=False, headers=J_Header)
    selector = lxml.html.fromstring(idx_html.text)
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
        Logi(f"{_date} exist,don't insert")
    else:
        try:
            ms.update(_sql)
            Logi("j data insert successfully")
        except (Exception,):
            Loge(f"fail {_sql}")
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


def get_unfull_data(level='C'):
    # 检查每轮数据中不全的数据
    s = ms.search(f"select round,count(*) from j22 where level='{level}' group by round")
    url_list = list()
    _unfull_round = list()
    num = 0
    if level == 'A':
        num = 9
    elif level == 'B':
        num = 11
    elif level == 'C':
        num = 9
    else:
        Logi("level num is unsupported!")
    for _k, _v in dict(s).items():
        if int(_v) != num:
            _unfull_round.append(_k)
    # print(_unfull_round)
    if len(_unfull_round) > 0:
        Logi(f"level {level} at {_unfull_round} not in db, catch it ")
        for i in _unfull_round:
            url_list += getUrlround(i, level)
        Logi(url_list)
        for i in url_list:
            get_every_j_data(i)
    else:
        Logi(f"level {level} every round have been catch")


def get_unfull_data_round(level='C'):
    # 检查没有轮数的数据
    info = ms.search(f"select distinct(round) from j22 where level='{level}'")
    db_round = [x[0] for x in info]
    # print(db_round)
    match_round = []
    if level == 'A':
        match_round = [x for x in range(1, 34)]
    elif level == 'B':
        match_round = [x for x in range(1, 42)]
    elif level == 'C':
        match_round = [x for x in range(1, 34)]
    else:
        Logi("not found match round")
    unfound_round = list(set(match_round)-set(db_round))
    url_list = list()
    if len(unfound_round) > 0:
        Logi(f"level {level} at {unfound_round} not found in db, catch it")
        for i in unfound_round:
            url_list += getUrlround(i, level)
        for k in url_list:
            get_every_j_data(k)
    else:
        Logi(f"level {level} all round in data")


def check():
    level = ['A', 'B', 'C']
    for l in level:
        get_unfull_data(l)
        get_unfull_data_round(l)


if __name__ == '__main__':
    check()