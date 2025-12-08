
import mysql.connector, datetime, time, re, requests, yaml, lxml.html, pyquery, logging, logging.handlers, os, sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.support.select import Select
from logging.handlers import TimedRotatingFileHandler

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
    _f = open(f"run.yml", "r", encoding="utf8")
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


def logconfig(log_name='s'):
    #
    log_obj = logging.getLogger(log_name)
    homept = os.path.expanduser('~')
    # fh = logging.FileHandler(f"{homept}/EKIA/python/spierfb/log.log", encoding="utf8")
    log_path = os.path.join(f"log.log")

    log_obj.setLevel(logging.INFO)
    # interval 滚动周期，
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="W6", interval=1, backupCount=1
    )
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    file_handler.setFormatter(# 定义日志输出格式
        logging.Formatter("%(asctime)s - %(levelname)s- %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    )
    log_obj.addHandler(file_handler)
    return log_obj


def Logi(msg):
    log.info(msg)



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
    selector = lxml.html.fromstring(indexhtml.text)
    info = selector.cssselect("li a")
    for i in info:
        if i.text == '試合詳細':
            all_url.append(i.get("href"))
    if len(all_url) == 0:
        Logi("not found match url")
    else:
        Logi("found match url")
    return all_url


log = logconfig()
ms = msq()
lock = threading.Lock()


def w2db(_sql):
    lock.acquire()  # sql insert need source
    if _sql is None: Logi("sql is empty [] ")
    data = re.findall("\'(.*?)\'\,", _sql)
    print(data)
    if data is []: Logi("匹配数据失败")
    _date = data[0]
    if ms.search("select * from j24 where date ='{}'".format(_date)) != []:
        Logi("{} exist,don't insert".format(_date))
    else:
        try:
            ms.update(_sql)
            Logi("j data insert successfully")
        except (Exception,):
            Logi("fail {}".format(_sql))
    lock.release()


def get_every_j_data(_url):
    url = "https://www.jleague.jp{}".format(_url)
    __level = getlevel(re.findall('/match/(.*)/2024', _url)[0])
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
        Logi("{} request error".format(url))
        return
    __headers = html.headers
    Logi("request stutas:={}".format(html.status_code))
    time.sleep(.1)
    selector = lxml.html.fromstring(html.text)
    # print(html.text)
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
    __round = re.findall("第(.*?)節", "".join(selector.xpath('//span[@class=\'matchVsTitle__league\']/text()')))[0]
    __date = re.findall("2024/(.*?)/live", soup.link['href'])[0]
    time.sleep(1)

    # get weather
    replace = url.replace('https://www.jleague.jp','').replace('live/','')
    dictd = {"url": replace}
    weather = "空"
    # get start time
    ss = pyquery.PyQuery(html.text)
    sk = ss.find(ryaml("sj_css", "css")).text()
    st = re.findall("\d+\:\d+", sk)[0].replace(":", "")
    _sql = f"INSERT INTO `j24` VALUES ('{__date}', '{st}', '{__level}', '{str(int(__round))}', '{weather}', '{__zhu}', '', '{__ke}', '{__bc}', '{__zj}', '{__kj}', '{__zc}', '{__kc}', '9.99', '9.99', '9.99');"
    Logi(f"sql:={_sql}")
    html.close()
    w2db(_sql)
    return True


def run():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_every_j_data, getUrl())


if __name__ == '__main__':
    run()
