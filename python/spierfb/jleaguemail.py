import datetime
import smtplib
import time
import mysql.connector
import yaml
import re
import os
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from email.mime.text import MIMEText  # 邮件文本
import undetected_chromedriver as uc
# from selenium import webdriver


"""
1，先获取每一轮的比赛赔率 selenium
2，使用sql查询历史数据   mysql
3，使用sina邮件，每周定时给自己邮件发送信息
4, log 保存赔率，方便下次插入
"""

match = {
    "j1": "https://www.365-288.com/#/AC/B1/C1/D1002/E85703783/G938/",
    "j2": "https://www.365-288.com/#/AC/B1/C1/D1002/E85703811/G938/",
    "j3": "https://www.365-288.com/#/AC/B1/C1/D1002/E86296643/G938/",
    # "jc": "https://www.365-288.com/#/AC/B1/C1/D1002/E90147428/G938/",
}


JTeam = {  # bet365 上面与 数据库中的比赛  对应关系
    "浦和红钻": "浦和", "大阪樱花": "Ｃ大阪", "鹿岛鹿角": "鹿島", "名古屋鲸鱼": "名古屋", "鸟栖沙岩": "鳥栖",
    "广岛三箭": "広島", "清水心跳": "清水", "FC东京": "FC東京", "大阪飞脚": "Ｇ大阪", "川崎前锋": "川崎Ｆ",
    "磐田喜悦": "磐田", "仙台维加泰": "仙台", "神户胜利船": "神戸", "长崎成功丸": "長崎", "枥木SC": "栃木",
    "横滨水手": "横浜FM", "札幌冈萨多": "札幌", "柏雷索尔": "柏", "湘南比马": "湘南", "FC横滨": "横浜FC",
    "福冈黄蜂": "福岡", "水戶霍利克": "水戸", "金泽塞维根": "金沢", "松本山雅": "松本", "东京绿茵": "東京Ｖ",
    "千叶市原": "千葉", "冈山雉鸡": "岡山", "德岛漩涡": "徳島", "山形蒙迪奥": "山形", "北九州向日葵":"北九州",
    "爱媛FC": "愛媛", "山口雷诺法": "山口", "甲府风林": "甲府", "大宫亚迪嘉": "大宮", "秋田蓝闪电": "秋田",
     "大分": "大分", "町田泽维亚": "町田", "新泻天鵝": "新潟", "相模原SC": "相模原", "岐阜FC":"岐阜",
    "京都不死鸟": "京都", "赞岐釜玉": "讃岐", "熊本深红": "熊本", "草津温泉": "群馬", "琉球FC": "琉球",
    "Iwaki SC": "いわき", "藤枝MYFC": "藤枝",
    "FC琉球":"琉球",
    "相模原":"相模原",
    "鹿儿岛联":"鹿児島",
    "YSCC":"YS横浜",
    "奈良俱乐部":"奈良",
    "宫崎特格瓦雅罗":"宮崎",
    "FC今治":"今治",
    "卡马塔马尔赞岐":"讃岐",
    "爱嫒FC":"愛媛",
    "Vanraure Hachinohe":"八戸",
    "鸟取SC":"鳥取",
    "FC大阪":"FC大阪",
    "富山胜利":"富山",
    "松本山雅FC":"松本",
    "长野帕塞罗":"長野",
    "福岛联":"福島",
    "沼津青蓝":"沼津",
    "盛冈仙鹤":"岩手"

}


def str2date(s):
    b = re.findall(r"[1-9]+\.?[0-9]*", s)
    new =''
    for i in b:
        if len(i) < 2:
            new_ = '0' + i
            new = new + new_
        else:
            new += i
    return new


def ryaml(key, peer="control"):
    # read yaml file
    homept = os.path.expanduser('~')
    _f = open(f"./run.yml", "r", encoding="utf8")
    config = yaml.load(_f.read(), Loader=yaml.Loader)
    conf = config[peer]
    _f.close()
    return conf[key]


def __split(list_collection, n=3):
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]


def logconfig(log_name='s'):
    # 创建logger对象。传入logger名字
    log_obj = logging.getLogger(log_name)
    # homept = os.path.expanduser('~')
    log_path = "./jmail.log"
    log_obj.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="W6", interval=1, backupCount=3
    )
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    file_handler.setFormatter(  # 定义日志输出格式
        logging.Formatter("%(asctime)s - %(levelname)s- %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    )
    log_obj.addHandler(file_handler)
    return log_obj


log = logconfig()


def Logi(msg):
    log.info(msg)


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


m = msq()


def get_all_match_peilv(level, urlu):
    # option = webdriver.ChromeOptions()
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #
    # # option.add_argument('--no-sandbox')  # 停用沙箱
    # option.add_argument('--disable-gpu')  # 禁用GPU实现加速
    # option.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    # # option.add_argument('–hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 禁用浏览器正在被自动化程序控制的提示
    # option.add_argument('–incognito')  # 隐身模式(无痕模式)
    # option.add_argument('--disable-dev-shm-usage')
    #
    # s = webdriver.Chrome(options=option)
    # s.get(j1)
    # s.maximize_window()
    # script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
    #
    # # 运行Javascript
    # s.execute_script(script)
    # time.sleep(200)
    # sql = """
    # var oodsdata = new Array();
    # var q = document.getElementsByClassName('src-ParticipantCenteredStacked48_Odds');
    # for (i = 0; i < q.length; i++) {
    #      var ele = q[i].innerText;
    #      oodsdata[i] = ele;
    # }
    # return oodsdata;
    # """
    # oods_list = s.execute_script(sql)
    # print(oods_list)
    # Logi(f"find data is := {oods_list}")
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # browser = webdriver.Chrome(options=options)
    # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #             Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #     })
    #
    #     """
    # })
    #
    # browser.execute_cdp_cmd('Network.setUserAgentOverride',
    #                         {
    #                             "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    # browser.get(j1)
    # time.sleep(300)

    driver = uc.Chrome()
    driver.execute_script(f"""setTimeout(() => window.location.href="{urlu}", 100)""")
    # time.sleep(20)
    peilvsql = """
    var oodsdata = new Array();
    var q = document.getElementsByClassName('src-ParticipantCenteredStacked48_Odds');
    for (i = 0; i < q.length; i++) {
         var ele = q[i].innerText;
         oodsdata[i] = ele;
    }
    return oodsdata;
    """

    team_oops = """
    var oodsdata = new Array();
    var q = document.getElementsByClassName('src-ParticipantFixtureDetailsExtraLineHigher_TeamWrapper');
    for (i = 0; i < q.length; i++) {
         var ele = q[i].innerText;
         oodsdata[i] = ele;
    }
    return oodsdata;
    """

    match_time = """
    var timelist = new Array();
    var q = document.getElementsByClassName('rcl-MarketHeaderLabel-isdate');
    for (i =0 ; i < q.length ; i++ ){
        var ele = q[i].innerText;
        timelist[i] = ele;
    }
    return timelist;
    """
    driver.service.stop()
    # time.sleep(10)
    driver.reconnect()
    oods_list = None
    try:
        oods_list = driver.execute_script(peilvsql)
        team_list = driver.execute_script(team_oops)
        time_list = driver.execute_script(match_time)
        print(oods_list)
        print(team_list)
        print(time_list)
        time.sleep(5)
        driver.quit()
        return oods_list, team_list, time_list
    except(Exception,):
        return oods_list


def mail_163(level, msg='新年快乐！'):
    # 邮件构建

    subject = f"BET365 {level} 每日赔率查询"                  # 邮件标题
    sender = "13716697293@163.com"  # 发送方
    content = msg  # 内容
    recver = "13716697293@sohu.com"  # 接收方
    password = "MVBLHTAAQLKPMVQJ"

    message = MIMEText(content, "plain", "utf-8")
    message['Subject'] = subject  # 邮件标题
    message['To'] = recver  # 收件人
    message['From'] = sender  # 发件人

    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)            # 实例化smtp服务器
    smtp.login(sender, password)  # 发件人登录
    smtp.sendmail(sender, [recver], message.as_string())    # as_string 对 message 的消息进行了封装


def create_msg(l, u):
    # 邮件内容
    content = '\r\n'
    # oop_list = ['2.45', '2.70', '3.30', '1.70', '4.33', '3.75', '1.75', '4.20', '3.50', '3.75', '1.90', '3.30', '3.80', '1.85', '3.40', '1.60', '5.00', '4.00', '2.50', '2.60', '3.25', '1.70', '4.50', '3.75', '1.70', '4.50', '3.75', '1.825', '2.025', '', '1.950', '1.900', '', '1.825', '2.025', '', '1.875', '1.975', '', '1.950', '1.900', '', '2.025', '1.825', '', '1.875', '1.975', '', '1.900', '1.950', '', '1.950', '1.900', '', '1.925', '1.925', '', '1.850', '2.000', '', '2.000', '1.850', '', '1.825', '2.025', '', '1.975', '1.875', '', '1.900', '1.950', '', '1.975', '1.875', '', '1.850', '2.000', '', '1.900', '1.950', '']
    # team_list = ['', '平局', '', '', '平局']
    oop_list, team_list, time_list = get_all_match_peilv(l, u)  # print(time_list)
    match_count = len(oop_list) // 9    # print(match_count)
    peilv_list = oop_list[:match_count*3]
    s = f"今天{match_count}场{l}比赛\r\n"
    content += s
    content += "\r\n"

    idx = 0
    for k in __split(peilv_list):
        result = m.search(f"select * from view_school_all where win='{k[0]}' and lose='{k[1]}' and draw='{k[2]}'")
        # print(result)
        content += f"oods:={k[0]} {k[2]} {k[1]} \r\n"
        content += f"\r\n"
        content += "<---sql---\r\n"
        sql = f"update j23 set win={k[0]},draw={k[2]},lose={k[1]},asia='' where zhu='{JTeam[team_list[idx]]}' and date like '{str2date(time_list[0])}__';\r\n"    # asia
        # print(sql)
        Logi(f"sql:= {sql}")
        content += sql
        content += f"\r\n"
        content += "---sql--->\r\n"
        content += f"\r\n"
        content += f"history data--\r\n"

        if result:
            for i in result:
                # print(f'{i}\r')
                content += f'{i}\r\n'
                content += '\r\n'
                # content += '<td scope="col">' + '%s' % i + '</td>'
        else:
            error_msg = 'This Oops haven\'t history data \r\n'
            content += error_msg
            content += '\r\n'
        idx += 3
    return content


def run():
    for j, url in match.items():
        email_msg = create_msg(j, url)
        mail_163(j, email_msg)
        time.sleep(30)


if __name__ == '__main__':
    run()