import csv
import datetime
import smtplib
import ssl
import time
import mysql.connector
import requests
import yaml
import re
import os
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from email.mime.text import MIMEText  # 邮件文本


'''
1，10min获取一次系统upate 。 记录上次time并做减法。如果小于<0 说明重启，马上就发送提醒给相关人
2，
3，每天8点半一发 。并且清空数据。保存csv文件
4，守护线程监控请求状态。如过happ服务挂掉，延长重试时间。1 2 4 8 16 32 64 128 
'''

MAC_LIST = [
    "4A:F7:1A:EA:AE:47",
    "42:D4:A0:C6:D4:82",
    "96:F0:51:23:8A:53",
    "C6:94:EE:02:7A:37",
    "8E:9A:37:E0:9F:C0",
    "2A:47:1C:B7:34:7C"
]

IP_LIST_SEVEN = [
    "10.10.82.96",
    "10.12.70.16",
    "10.12.70.21",
    "10.12.70.17",
    "10.10.82.97",
    "10.12.70.18",

]


def a():
    d = {}
    for m in MAC_LIST:
        d[m] = 0
    return d


def isDuring(st, et):
    # 是否在时间段内
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + st, '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + et, '%Y-%m-%d%H:%M')
    now_time = datetime.datetime.now()
    if start_time < now_time < end_time:
        return True
    return False


class check_big:
    # {mac:time:value}
    def __init__(self):
        self.url = "http://172.16.127.72:9900/api/cluster/devices/{}/rpc/sysctrl/cmd/exec"
        self.up_one = None
        self.now_one = None
        self.info_dict = a()
        self.isSend = False
        self.isMakecsv = False
        self.template = """
        <!DOCTYPE html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <html>
        <body>
          <h1 style="text-align: 40%"> 嘉兴大场景Pro基站重启监测</h1>
          <table style="border-collapse: collapse;">
        """
        # table-layout: auto;
        self.template_end = """
                </table>
            </body>
        </html>
        """

    def check(self):

        #

        self.template += "<tr>"

        search_data = {
            "cmd": "cat",
            "args": ["/proc/uptime"]
        }
        logfile = open('heartbead' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv', mode='w')
        val_list = []
        col_list = []
        search_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.template += f"<td style='border: 2px solid black; padding: 10px; text-align: center;'>{search_time}</td>"
        for m in MAC_LIST:
            req = requests.post(self.url.format(m), json=search_data).json().get('msg')
            if req:
                time = req.split(" ")[0]
                print(f"{m}", ",", f"{search_time}", ",", f"{time}")
                val_list.append(int(float(time)))

                if int(float(time)) - self.info_dict[m] > 0:  # 如果大于则正常
                    # col_list.append(False)
                    self.template += f"""
                    <td style="border: 2px solid black; padding: 10px; text-align: center; ">{int(float(time))}</td>

                    """
                else:  # # 如果小于则说明异常,发送为true　
                    # col_list.append(True)
                    # add c
                    self.isSend = True
                    self.template += f"""
                    <td style="border: 2px solid black; padding: 10px; text-align: center; color:red;">{int(float(time))}</td>
                    """
                self.info_dict[m] = int(float(time))  # 比较完在赋值
            else:
                print(f"{m}", ",", f"{search_time}", ",", f"None")

        self.template += "<tr>"

        # 将val-list追加到csv文件中
        if self.isSend:
            self.send_msg(self.template + self.template_end)
            self.isSend = not self.isSend

    def w2f(self, data):

        # 写入文件
        data = ['2020-2-2', '23', '23', '23', '23', '23', '23']
        # data = ['2020', ',', '23', ',', '23', ',', '23',',', '23',',','23']
        if os.path.exists("file.csv"):
            with open("file.csv", mode='a', newline='', encoding='utf8') as f:
                w = csv.writer(f)
                # for d in data:
                w.writerow(data)
            f.close()

    def _mvfile(self):
        # 获取昨天的数据，并创建新的file.csv
        _today = datetime.date.today()  # 2024-04-22
        yesterday = str(_today - datetime.timedelta(days=1))
        try:
            os.system(f"mv ./file.csv .{yesterday}.csv")
            time.sleep(2)
            os.system("touch file.csv")
        except(Exception,):
            print("error")
            os.system("touch error.log")

    def email_msg(l, u):
        # 邮件内容
        content = '\r\n'
        """
        <!DOCTYPE html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <html>
        <body>
          <h1 style="text-align: center">嘉兴大场景Pro基站重启监测情况</h1>
          <table style="border-collapse: collapse;">
            <tr>
              <th style="border: 2px solid black; padding: 12px;">Time/MAC</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac1}}</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac2}}</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac3}}</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac4}}</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac5}}</th>
              <th style="border: 2px solid black; padding: 20px;">{{Mac6}}</th>
            </tr>
            <!-- 数据放到这里。-->
            <tr>
              <td style="border: 2px solid black; padding: 20px;text-align:  color:red;">张三</td>
              <td style="border: 2px solid black; padding: 20px;text-align: color:red;">{{}}}</td>
            </tr>


        """

        end = """

        </table>
        </body>
        </html>
        """

        return content

    def send_msg(level, msg='新年快乐！'):
        # 邮件构建

        subject = f"365 {level} 每"  # 邮件标题
        sender = "13716697293@163.com"  # 发送方
        content = msg  # 内容
        recver = "13716697293@sohu.com"  # 接收方
        password = "MVBLHTAAQLKPMVQJ"
        cc = "hanchao.gu@hanshow.com"
        message = MIMEText(content, "plain", "utf-8")
        message['Subject'] = subject  # 邮件标题
        message['To'] = recver  # 收件人
        message['From'] = sender  # 发件人
        message['cc'] = cc  # 发件人

        smtp = smtplib.SMTP_SSL("smtp.163.com", 465)  # 实例化smtp服务器
        smtp.login(sender, password)  # 发件人登录
        smtp.sendmail(sender, recver, message.as_string())  # as_string 对 message 的消息进行了封装

    def msg_head(self):
        # 添加Mac
        self.template += """<tr> 
                <th style="border: 2px solid black; padding: 12px;">Time\MAC</th>
            """
        for m in MAC_LIST:
            self.template += f'<th style="border: 2px solid black; padding: 30px;">{m}</th>'

        self.template += "</tr>"

        # 添加IP
        self.template += """<tr> 
                <th style="border: 2px solid black; padding: 12px;">IP</th>
            """
        for p in IP_LIST_SEVEN:
            self.template += f'<th style="border: 2px solid black; padding: 30px;">{p}</th>'
        self.template += "</tr>"

    def run(self):
        while True:
            time.sleep(30)
            self.check()
            if isDuring("8:50", "9:01"):    # 在这个时间点发送邮件、恢复设置
                self.send_msg(self.template + self.template_end)
                self.info_dict = a()        # 将数据恢复为默认值
                # make new file


if __name__ == '__main__':
    check_big().w2f('')
    # check_big().run()