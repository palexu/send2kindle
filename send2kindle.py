#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formatdate

sender   = 'cnxujunyu@126.com'
receiver = 'cnxujunyu@kindle.cn'
reportReceiver='1098672878@qq.com'
password = "xujunyu520"
host     = 'smtp.126.com'
#由于长期使用同一个内容，很容易被认为是垃圾邮件，所以需要定期修改内容


def send2kindle(filename):
    #创建一个带附件的实例
    s=smtplib.SMTP_SSL(host)
    s.login(sender,password)
    try:
        message=writeMail(filename)
        s.sendmail(sender, receiver, message.as_string())
        print("[%s]发送成功......" % filename)
    except smtplib.SMTPResponseException as re:
        print("邮件发送异常,错误报告详情:\n")
        print(re)
        print("正在尝试重新发送....")
        tryCount=2
        while tryCount>=0:
            tryCount-=1
            try:
                s.sendmail(sender, receiver, message.as_string())
            except smtplib.SMTPResponseException as e:
                print("剩余尝试%i次,错误报告详情:\n" % tryCount)
                print(e)
                if tryCount==0:
                    msg=MIMEText(e)
                    msg['Subject']="[失败]%s发送失败" % filename
                    msg['From']=sender
                    msg['To']=reportReceiver
                    s.sendmail(sender, reportReceiver, msg)
    finally:
        s.close()

def writeMail(filename):
    message = MIMEMultipart()
    message['Subject'] = "Convert"
    message['from'] = sender
    message['to'] = receiver
    message["Date"] = formatdate(localtime=True)

    message.attach(MIMEText('你好呀，这是我要发送的附件:[%s]，请注意查收~\n祝健康 ' % filename, 'plain', 'utf-8' ))
    att1 = MIMEText(open(filename, "r").read(), _charset = "utf-8")
    # att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # att1["Content-Disposition"] = 'attachment; filename="%s"' % filename
    att1["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(filename,'utf-8')
    message.attach(att1)
    return message

if __name__ == '__main__':
    print("test:send2kindle.py send2kindle()")
    send2kindle("test.txt")
