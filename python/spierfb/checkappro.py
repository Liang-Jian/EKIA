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


def a():
    d = {}
    for m in MAC_LIST:
        d[m] = 0
    return d


class check_big:
    # {mac:time:value}
    def __init__(self):
        self.url = "http://172.16.127.72:9900/api/cluster/devices/{}/rpc/sysctrl/cmd/exec"
        self.up_one = None
        self.now_one = None
        self.info_dict = a()
        self.template = """
        <!DOCTYPE html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <html>
        <body>
          <h1 style="text-align: 40%">     嘉兴大场景Pro基站重启监测</h1>
          <table style="border-collapse: collapse; table-layout: auto;">



        """
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
        logfile = open('noheartbeat_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv', mode='w')
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
                else:  # # 如果小于则说明异常
                    # col_list.append(True)
                    # add c
                    self.template += f"""
                    <td style="border: 2px solid black; padding: 10px; text-align: center; color:red;">{int(float(time))}</td>

                    """
                self.info_dict[m] = int(float(time))  # 比较完在赋值
            else:
                print(f"{m}", ",", f"{search_time}", ",", f"None")
        self.template += "<tr>"
        print(val_list[0], ',', val_list[1], ',', val_list[2], ',', val_list[3], ',', val_list[4], ',', val_list[5],
              file=logfile, flush=True)

    def w2f(self):
        # 写入晚间
        pass

    def _template(self):
        # 邮件模版
        html = '''
        <html>
        <body>
            <p style = "color:red;" > 这是一封带有红色字体的邮件! </p>
            <p style = "color:blue;" > 这是一封带有蓝色字体的邮件! </p>
        </body>
        </html>
        '''

    # def email_msg(l, u):
    #     # 邮件内容
    #     content = '\r\n'
    #     """
    #     <!DOCTYPE html>
    #     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    #     <html>
    #     <body>
    #       <h1 style="text-align: center">嘉兴大场景Pro基站重启监测情况</h1>
    #       <table style="border-collapse: collapse;">
    #         <tr>
    #           <th style="border: 2px solid black; padding: 12px;">Time/MAC</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac1}}</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac2}}</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac3}}</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac4}}</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac5}}</th>
    #           <th style="border: 2px solid black; padding: 20px;">{{Mac6}}</th>
    #         </tr>
    #         <tr>
    #           <td style="border: 2px solid black; padding: 20px;text-align: center">张三</td>
    #           <td style="border: 2px solid black; padding: 20px;text-align: center">{{}}}</td>
    #         </tr>
    #       </table>
    #     </body>
    #     </html>
    #
    #     """
    #     return content

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
        cc = "ganchao.gu@hanshow.com"
        message = MIMEText(content, "plain", "utf-8")
        message['Subject'] = subject  # 邮件标题
        message['To'] = recver  # 收件人
        message['From'] = sender  # 发件人
        message['cc'] = cc  # 发件人

        smtp = smtplib.SMTP_SSL("smtp.163.com", 465)  # 实例化smtp服务器
        smtp.login(sender, password)  # 发件人登录
        smtp.sendmail(sender, recver, message.as_string())  # as_string 对 message 的消息进行了封装

    def msg_head(self):
        self.template += """<tr> 
                <th style="border: 2px solid black; padding: 12px;">Time\MAC</th>"

            """

        for m in MAC_LIST:
            self.template += f'<th style="border: 2px solid black; padding: 30px;">{m}</th>'

        self.template += "</tr>"

    def run(self):
        self.msg_head()
        for i in range(132):
            self.check()
            time.sleep(300)
        self.send_msg(self.template + self.template_end)


if __name__ == '__main__':
    check_big().run()