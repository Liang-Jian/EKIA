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

# server = 'http://101.201.81.174:4444/wd/hub'
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-infobars")
# driver = webdriver.Remote(command_executor=server, options=options)
# # driver.get("http://csdn.net")
# driver.get("https://www.baidu.com")
# time.sleep(3)
# driver.quit()

match = {
    "j1": "https://www.365-288.com/#/AC/B1/C1/D1002/E85703783/G938/",
    "j2": "https://www.365-288.com/#/AC/B1/C1/D1002/E85703811/G938/",
    "j3": "https://www.365-288.com/#/AC/B1/C1/D1002/E86296643/G938/",
    # "jc": "https://www.365-288.com/#/AC/B1/C1/D1002/E90147428/G938/",
}


def get_all_match_peilv(level, urlu):


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


get_all_match_peilv("A", match["j1"])