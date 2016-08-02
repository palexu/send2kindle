#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formatdate

sender = 'cnxujunyu@126.com'
receiver = 'cnxujunyu@kindle.cn'
password= "xujunyu520"
host= 'smtp.126.com'

def send2kindle(filename):
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['Subject'] = "Convert"
    message['from'] = sender
    message['to'] = receiver
    message["Date"] = formatdate(localtime=True)

    message.attach(MIMEText('你好，这是我的附件，请查收~ ', 'plain', 'utf-8'))
    att1 = MIMEText(open(filename, "r").read(), _charset = "utf-8")
    # att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # att1["Content-Disposition"] = 'attachment; filename="%s"' % filename
    att1["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(filename,'utf-8')
    # att1["Content-Description"] = filename
    print(att1["Content-Disposition"])
    # print(att1["Content-Description"])
    message.attach(att1)

    s=smtplib.SMTP_SSL(host)
    s.login(sender,password)
    s.sendmail(sender, receiver, message.as_string())
    s.close()
    print("邮件发送成功")

if __name__ == '__main__':
    print("test:send2kindle.py send2kindle()")
    send2kindle("text.txt")
