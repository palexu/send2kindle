# coding=utf-8
import smtplib
import logging
import logging.config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formatdate
import time

logging.config.fileConfig("config/logging.conf")


# sender = 'cnxujunyu@126.com'
# receiver = 'cnxujunyu@kindle.cn'
# reportReceiver = '1098672878@qq.com√'
# password = "xujunyu520"
# host = 'smtp.126.com'


# sender = '15957180610@163.com'
# # receiver = 'cnxujunyu@kindle.cn'
# receiver = '1098672878@qq.com'
# reportReceiver = '1098672878@qq.com'
# password = "xujunyu520"
# host = 'smtp.163.com'


# sender   = 'cnxujunyu@sina.com'
# receiver = 'cnxujunyu@kindle.cn'
# reportReceiver='1098672878@qq.com'
# password = "125108xu"
# host     = 'smtp.sina.com'
# 由于长期使用同一个内容，很容易被认为是垃圾邮件，所以需要定期修改内容

class Mail:
    def __init__(self):
        self.hostconf = {
            "163": {
                "sender": '15957180610@163.com',
                "password": "xujunyu520",
                "host": 'smtp.163.com',
            },
            "126": {
                "sender": 'cnxujunyu@126.com',
                "password": "xujunyu520",
                "host": 'smtp.126.com',
            }
        }
        self.sender = ""
        self.password = ""
        self.host = ""

        self.receiver = 'cnxujunyu@kindle.cn'
        self.reportReceiver = '1098672878@qq.com'
        self.init_host_config("126")

        self.subject = "请问为什么把我标记了？"
        self.msgcontent = "见附件"

    def init_host_config(self, hostname):
        self.sender = self.hostconf[hostname]["sender"]
        self.password = self.hostconf[hostname]["password"]
        self.host = self.hostconf[hostname]["host"]

    def set_receiver(self, receiver):
        self.receiver = receiver

    def send2kindle(self, novellist):
        # 创建一个带附件的实例
        with smtplib.SMTP_SSL(self.host) as s:
            s.login(self.sender, self.password)
            try:
                message = self.writeMail(novellist)
                s.sendmail(self.sender, self.receiver, message.as_string())
                logging.info("[%s]发送成功" % novellist)
            except smtplib.SMTPDataError as re:
                logging.error("邮件发送失败:%s" % re)

    def writeMail(self, filelist):
        """
        制作一封信
        :param filelist:文件列表
        :return:
        """

        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['from'] = self.sender
        message['to'] = self.receiver

        message.attach(MIMEText(self.msgcontent, 'plain', 'utf-8'))
        for filename in filelist:
            logging.debug("%s add to message" % filename)
            message.attach(self.getAtt(filename))

        logging.debug("using mail:%s"%self.host)
        logging.debug("subject: %s" % message['Subject'])
        logging.debug("from:    %s" % message['from'])
        logging.debug("to:      %s" % message['to'])
        logging.debug("邮件内容  :%s" % self.msgcontent)

        return message

    def getAtt(self, filename):
        """
        添加附件
        :param filename:文件名
        """
        # att1 = MIMEText(open(filename, "r").read(), _charset = "utf-8")
        try:
            bf = open(filename, 'rb')
            att = MIMEText(bf.read(), 'base64', 'utf-8')
            bf.close()
            att["Content-Type"] = 'application/octet-stream'
            # att1["Content-Disposition"] = 'attachment; filename="%s"' % filename
            att["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(filename, 'utf-8')
            logging.debug("make %s" % filename)
            return att
        except Exception as e:
            logging.warning(e)
