import sys
import http.client
import json
import re
import os
import threading
import time
import datetime
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler

""" 指定EL整发整收 循环更新压力脚本 电量查询脚本

step1: 复制white_list.txt -> white_list_bak.txt 文件
step2: 修改ew_fp为自己的路径
step3: 检查有无/var/log/ 路径
step4: 执行电量查询脚本，获取初始电量
step5: 执行


#----mvlog.sh ----#
# 1 1 * * *  bash /media/mvlog.sh
# 备份log文件
#! /bin/bash
mv /usr/local/{ew}/log/*.log.gz /usr/local/{ew}/logbak/
echo 'log mv over'

"""

####################

EW = '172.17.120.25:9070'
HEADERS = {'Content-Type': 'application/json'}
UC = 'default'
CI = 'mongodb://172.17.120.26:27017/'
DB = 'esl17yace9'
COLLECT = 'esl'
BAK_URL = 'http://10.11.163.211:8080/shopweb/ogi/ew/httpHandler'
####################


os_ = sys.platform

print(os_)
if os_ == "win32":
    ew_fp = r"D:\BBIT_ROUND2\eslw-5.0.2rc0"
    log_path_ = f"{ew_fp}\\run.log"
    ew_wl = fr"{ew_fp}\config\white_list_bak.txt"
    ew_log_path = fr"{ew_fp}\log\eslworking.log"
    api_log_fp = fr"{ew_fp}\log\\api.log"
    battery_fp = f"{ew_fp}\\battery.log"
    battery_api_fp = f"{ew_fp}\\batteryapi.log"
elif os_ == "linux":
    ew_fp = "/usr/local/eslw_5.0.2rc3yace"              # app_home
    log_path_ = f"{ew_fp}/run.log"                      # run.log
    ew_wl = f"{ew_fp}/config/white_list_bak.txt"        # esl list
    ew_log_path = f"{ew_fp}/log/eslworking.log"         # ew log fp
    api_log_fp = rf"{ew_fp}/log/api.log"                # ew api fp
    battery_fp = "/var/log/battery.log"                 # battery info 查询精确电量
    battery_api_fp = "/var/log/batteryapi.log"          # battery api info 查询三代价签电量,非精确


def get_esl(f=ew_wl):
    # 过滤 ESLID
    s = open(f, encoding='utf8')
    esl_list = [x.replace("\n", "").replace(f"={UC}", "") for x in s if not x.startswith("#")]
    print(f"esl list len = {len(esl_list)}")
    s.close()
    return esl_list


def isDuring(st, et):
    # 是否在时间段内
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + st, '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + et, '%Y-%m-%d%H:%M')
    now_time = datetime.datetime.now()
    if start_time < now_time < end_time:
        return True
    return False


def get_file_seek():
    f = open(api_log_fp, mode='r')
    size = f.seek(0, os.SEEK_END)
    f.close()
    Logi(f"current file seek {size}")
    return size


def _get_one_pid(pid="30003000"):
    # make api.log file
    conn = http.client.HTTPConnection(EW)
    conn.request('GET', f'/api3/{UC}/esls/product/{pid}', headers=HEADERS)
    res = conn.getresponse()
    Logi("create api file finish!")


def _send_battery_api():
    # post battery api
    esl_list = get_esl()
    parse = list()
    for e in esl_list:
        _d = {
            "esl_id": e,
            "sid": "12345678",
            "type": 53,
            "back_url": BAK_URL
            }
        parse.append(_d)
    _data = {"data": parse}
    conn = http.client.HTTPConnection(EW)
    conn.request('PUT', f'/api3/{UC}/esls/query/statistics', json.dumps(_data), headers=HEADERS)
    res = conn.getresponse()
    Logi("post battery api finish")


def _get_battery_info(file_max_seek):
    #
    esl_id = get_esl()
    f = open(battery_fp, mode='a+', encoding='utf8', errors='ignore')
    Logi("write battery start")

    def __get_battery(esl):
        bi = {esl: 0}
        dt = datetime.datetime.now()

        with open(api_log_fp, mode='r', encoding='utf8', errors='ignore') as _f:
            _f.seek(file_max_seek, 0)
            while True:
                line = _f.readline()
                if not line:
                    break
                if "category=api,action=prepare_ack,cmd=ESL_STATISTICS_QUERY_ACK" in line and f"esl_id={esl}" in line:
                    battery_info = re.search(',query_type=53,battery=(.*?),sid=', line)
                    if battery_info:
                        _power = battery_info.group(1)
                        bi[esl] = _power
                        dt = line[:23]
                        break
        _f.close()

        f.write(f"{dt} - esl={esl};battery={bi[esl]}\n")
        Logi(f"{dt} - esl={esl};battery={bi[esl]}")

    for e in esl_id:
        __get_battery(e)
    f.close()
    Logi("write battery finish")


def _get_battery_db():
    import requests
    esl_list = get_esl()
    f = open(battery_api_fp, mode='a+', encoding='utf8', errors='ignore')
    Logi("write battery api start db")
    for e in esl_list:
        req = requests.get(f'http://{EW}/api3/esls/{e}', headers=HEADERS)
        try:
            req_json = req.json().get('data').get('battery')
            f.write(f"{datetime.datetime.now()};esl={e};battery={req_json}\n")
        except(Exception,):
            f.write(f"{datetime.datetime.now()};esl={e};battery=None\n")
    Logi("write battery api finsh db")
    f.close()


def search_battery():
    # 电量查询主入口
    status = True
    while status:
        time.sleep(1)
        if isDuring("00:01", "00:03"):
            Logi(f"search battery info start")
            _get_one_pid()
            time.sleep(2)
            current_seek = get_file_seek()
            time.sleep(1)
            _send_battery_api()
            time.sleep(240)
            _get_battery_info(current_seek)
            _get_battery_db()
            break
    Logi(f"search battery info finish")


def logconfig(log_name='s'):
    # 创建logger对象。传入logger名字
    log_obj = logging.getLogger(log_name)
    log_path = log_path_
    log_obj.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(filename=log_path, when="W6", interval=1, backupCount=3)
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    file_handler.setFormatter(  # define log output formart
        logging.Formatter("%(asctime)s - %(threadName)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    )
    log_obj.addHandler(file_handler)
    return log_obj


log = logconfig()


def Logi(msg):
    log.info(msg)


class foreverUpdate:
    def __init__(self, fp):
        self.ew_log_fp = fp                     # ew log
        self._update_price = 0                  # start price
        self.seek = 0                           # file seek
        self.esl_list = get_esl()               # update esl

    def check_info_esl(self):
        """ 整发整收 """
        t = 2
        while True:
            receive_esl = list()
            release_esl = list()
            receive_ = re.compile(r"category=esl,action=receive,user_code=(%s),eslid=(.*),payload_type=UPDATE,payload_retry_time=" % UC)
            release_ = re.compile(r"category=esl,action=esl_update_finished,user_code=(%s),eslid=(.*),status=" % UC)

            with open(self.ew_log_fp, mode='r', encoding='utf8', errors='ignore') as _f:
                _f.seek(self.seek, 0)
                Logi("search start")
                while True:
                    line = _f.readline()
                    if not line:
                        break

                    receive = receive_.search(line)
                    release = release_.search(line)

                    if receive:
                        esl = receive.group(2)
                        if esl in self.esl_list and esl not in receive_esl:
                            receive_esl.append(esl)

                    elif release and len(receive_esl) == len(self.esl_list):
                        esl = release.group(2)
                        if esl in self.esl_list and esl not in release_esl:
                            release_esl.append(esl)

                        if len(release_esl) == len(receive_esl):
                            if isDuring("23:57", "23:59"):                                  # 冷冻时间拉长到4min
                                Logi(f"time = {datetime.datetime.now()}; script pause log file waiting change")
                                threading.Thread(target=search_battery, args=(), name='batteryClass').start()    # 启动电量查询
                                time.sleep(300)
                                self.seek = 0                                               
                                Logi("reset file seek set 0 ")
                                self._update()
                                break
                            else:
                                _f.readline()
                                self.seek = _f.tell()
                                Logi(f"file seek is {self.seek}")
                                self._update()
                                break
                Logi(f"receive:={len(receive_esl)} ; finished:= {len(release_esl)} ; esl_list:={len(self.esl_list)}")
            _f.close()
            Logi(f"search finish , waiting {t}s for next search !")
            time.sleep(t)

    def _update(self):
        """ update """
        params = list()
        for i in self.esl_list:
            data = {
                "sid": "3984799300029881",
                "priority": 10,
                "esl_id": i,
                "back_url": BAK_URL,
                "template": "NORMAL_250122213-BLACK-WHITE-RED",
                "price2": str(self._update_price)
            }
            params.append(data)
        data = {"data": params}
        conn = http.client.HTTPConnection(EW)
        conn.request('PUT', f'/api3/{UC}/esls', json.dumps(data), HEADERS)
        res = conn.getresponse()
        self._update_price += 1
        Logi(f"update finish  and next price is {self._update_price}")

    def run(self):
        self._update()
        time.sleep(70)
        self.check_info_esl()


if __name__ == '__main__':
    foreverUpdate(ew_log_path).run()

