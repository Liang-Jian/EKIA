import sys
import http.client
import json
import re
import os
import time
import datetime
import logging
import logging.handlers
import base64
import random
# from logging.handlers import TimedRotatingFileHandler
# from io import BytesIO
# from PIL import Image, ImageDraw, ImageFont

####################config

EW = '127.0.0.1:9000'
HEADERS = {'Content-Type': 'application/json'}
UC = 'god.1'
BAK_URL = 'http://10.11.172.9:18080'
####################


os_ = sys.platform


if os_ == "win32":
    ew_fp = r"D:\BBIT_ROUND2\eslw-5.0.2rc0"
    log_path_ = f"{ew_fp}\\run.log"
    ew_wl = fr"{ew_fp}\config\white_list_bak.txt"
    ew_log_path = fr"{ew_fp}\log\eslworking.log"
    api_log_fp = fr"{ew_fp}\log\api.log"

elif os_ == "linux":
    ew_fp = "/root/eslworking-5.0.2"                    # app_home
    log_path_ = f"{ew_fp}/run.log"                      # run.log
    epd_wl = f"{ew_fp}/config/white_list_bak.txt"       # epd esl list
    ew_log_path = f"{ew_fp}/log/eslworking.log"         # ew log fp
    api_log_fp = rf"{ew_fp}/log/api.log"                # ew api fp


def get_esl(f):
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


def get_file_seek(fp):
    # get file size
    f = open(fp, mode='r', encoding='utf8')
    size = f.seek(0, os.SEEK_END)
    f.close()
    Logi(f"current file seek {size}")
    return size


def calc(start_t, end_t):
    start_t_split = start_t.split(":")[1]
    end_t_split = end_t.split(":")[1]
    st = (int(end_t_split) - int(start_t_split) + 1) * 60
    # print(st)
    return int(st)


def make_pic(price=1):
    # 随机生成图片，黑底白字，兼容冷冻价签
    bg_color = ['white', 'red', 'yellow', 'gray', 'green']
    image = Image.new('RGB', (296, 152), color=random.choice(bg_color))
    draw = ImageDraw.Draw(image)
    text = str(price)
    font = ImageFont.truetype('/root/SourceCodePro-Black.ttf', 110)
    text_width, text_height = draw.textsize(text, font)
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    buffer = BytesIO()
    image.save(buffer, format='bmp')
    image_data = buffer.getvalue()
    base64_data = base64.b64encode(image_data).decode('utf-8')
    image.close()
    return base64_data


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


# log = logconfig()


def Logi(msg):
    log.info(msg)


class foreverUpdate:
    def __init__(self):
        self.ew_log_fp = "/Users/shi/Desktop/eslworking.log"                     # ew log
        self._update_price = 34                 # start price
        self.seek = 0                           # file seek
        self.esl_list = get_esl("/Users/shi/Desktop/white_list_bak.txt")               # update esl
        self.start_update_time = None

    def check_info_esl(self):
        """ 整发整收 """
        t = 5
        receive_esl = list()
        release_esl = list()
        while True:

            receive_ = re.compile(r"category=esl,action=receive,user_code=(%s),eslid=(.*),payload_type=UPDATE,payload_retry_time=" % UC)
            release_ = re.compile(r"category=esl,action=esl_update_finished,user_code=(%s),eslid=(.*),status=" % UC)

            with open(self.ew_log_fp, mode='r', encoding='utf8', errors='ignore') as _f:
                _f.seek(self.seek, 0)
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

                    elif release and len(receive_esl) == 173:
                        esl = release.group(2)
                        if esl in self.esl_list and esl not in release_esl:
                            release_esl.append(esl)


                # Logi(f"receive:={len(receive_esl)} ; finished:= {len(release_esl)} ; esl_list:={len(self.esl_list)}")
            _f.close()
            time.sleep(t)
            print(len(receive_esl))
            print(list(set(receive_esl)-set(release_esl)))
            print(len(release_esl))
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
        self.start_update_time = datetime.datetime.now()
        Logi(f"update send over and next price is {self._update_price};loop update start time = {self.start_update_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")

    def _update_pic(self):
        params = list()
        img_data = make_pic(self._update_price)
        for e in self.esl_list:
            data = {
                "sid": "3984799300029881",
                "priority": 10,
                "esl_id": e,
                "back_url": BAK_URL,
                "screen": {
                    "name": "%s" % e,
                    "default_page": "normal",
                    "default_page_id": "0",
                    "pages": [
                        {
                            "id": 0,
                            "name": "normal",
                            "image": img_data
                        },
                    ]
                },
            }
            params.append(data)
        data = {"data": params}
        conn = http.client.HTTPConnection(EW)
        conn.request('PUT', f'/api3/{UC}/esls', json.dumps(data), HEADERS)
        res = conn.getresponse()
        self._update_price += 1
        self.start_update_time = datetime.datetime.now()
        Logi(f"update pic send over and next price is {self._update_price};loop update start time = {self.start_update_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")

    def run(self):
        # self._update_pic()
        # time.sleep(70)
        self.check_info_esl()


if __name__ == '__main__':
    foreverUpdate().run()



