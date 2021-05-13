import smtplib,os,time
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from autobase.FunctionLibray import readYaml,zipDir,deleteFile
from autobase.Logger import Logi

'''
sendmail , zip file

'''


_MAILSERVICE = readYaml("mailService", "Email")      # 邮箱服务器地址
_FROM = readYaml("sendName", "Email")                # 邮箱用户名
_PASSWORD = readYaml("password", "Email")            # 邮箱密码,需要使用授权码
_TO = readYaml("recvName", "Email")                  # 收件人，多个收件人用逗号隔开
_SUBJECT = readYaml("subject", "Email")              # 主题
_BODY = open(os.path.abspath("..")+ "/autodata/template/email.html",encoding='utf-8',errors='ignore').read() # 邮件正文



def LexueMail(S_COUNT,F_COUNT,SUBJECT=_SUBJECT, TO=_TO, FROM=_FROM):
    """With this function we send out our HTML email or Zip file"""

    zipDir(os.path.abspath('..') + "/autodata/records")

    succcount = int(S_COUNT) -1
    failcount = int(F_COUNT) -1
    all = succcount + failcount

    __BODY = _BODY

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    # MESSAGE.attach(MIMEText(__BODY, 'plain', 'utf-8'))     # 邮件内容为文本
    MESSAGE.attach(MIMEText(__BODY, 'html', 'utf-8'))      # 为html

    # Make attribute
    # att2 = MIMEText(open(os.path.abspath('..') + "/autodata/resultfile/线上执行报告.zip", 'rb').read(), 'base64', 'utf-8')
    att2 = MIMEApplication(open(os.path.abspath('..') + "/autodata/resultfile/线上执行报告.zip", 'rb').read())
    # att2["Content-Type"] = 'application/octet-stream'
    # att2["Content-Disposition"] = 'attachment; filename="线上执行报告.zip"'
    att2.add_header("Content-Disposition",'attachment',filename='test.zip')
    MESSAGE.attach(att2)

    # The actual sending of the e-mail
    server = smtplib.SMTP_SSL(host=_MAILSERVICE) # python37 use

    # Print debugging output when testing
    # if __name__ == "__main__":
    #     server.set_debuglevel(1)

    # Credentials (if needed) for sending the mail
    try:
        password = _PASSWORD
        server.connect(_MAILSERVICE)
        server.login(FROM, password)
        server.sendmail(FROM, TO, MESSAGE.as_string())
        server.quit()
        Logi("{} mail send success".format(TO))
    except Exception as e:
        print(e.__str__())

    time.sleep(1)
    deleteFile(os.path.abspath('../') + "/autodata/resultfile/线上执行报告.zip")
    deleteFile(os.path.abspath('../') + "/autodata/records")
    deleteFile(os.path.abspath('../') + "/msg")

# if __name__ == "__main__":
#     """Executes if the script is run as main script (for testing purposes)"""
#
#     LexueMail()