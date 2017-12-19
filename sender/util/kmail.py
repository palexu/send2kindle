# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sender.util.config import *
from sender.util import server_chan


class Mail:
    def __init__(self):
        config = mail()
        self.mail_config = config["hostconf"]
        self.receiver = config["receiver"]
        self.subject = config["subject"]
        self.msgcontent = config["msgcontent"]

    def send2kindle(self, filename, byteFile):
        """
        发送小说到kindle
        :param byteFile:
        :return: true or false
        """
        if (not byteFile) or (not filename):
            logger.error(u"文件名或文件内容为空,发送失败")
            return

        host = self.mail_config["host"]
        if "port" in self.mail_config:
            port = self.mail_config["port"]
            s = smtplib.SMTP(host, port)
            s.ehlo()
            s.starttls()
        else:
            s = smtplib.SMTP_SSL(host)

        s.login(self.mail_config["sender"], self.mail_config["password"])
        try:
            message = self.make_kindle_mail(filename, byteFile)
            # message = self.make_plain_mail("这是一封测试用的邮件")
            s.sendmail(self.mail_config["sender"], self.receiver, message.as_string())
            logger.info(u"[%s]发送成功" % filename)
            server_chan.send(u"小说发送成功")
            return True
        except smtplib.SMTPDataError as re:
            logger.error(u"邮件发送失败:%s" % re)
            server_chan.send(u"邮件发送失败:%s" % re)
            return False
        finally:
            s.close()

    def make_kindle_mail(self, filename, bytefile):
        """
        :param bytefile:文件列表
        :return:
        """

        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['from'] = self.mail_config["sender"]
        message['to'] = self.receiver

        message.attach(MIMEText(self.msgcontent, 'plain', 'utf-8'))
        message.attach(self.getAtt(filename, bytefile))

        logger.info("=================================")
        logger.info("using mail config:%s" % self.mail_config)
        logger.info("subject: %s" % message['Subject'])
        logger.info("from:    %s" % message['from'])
        logger.info("to:      %s" % message['to'])
        logger.info("邮件内容  :%s" % self.msgcontent)
        logger.info("=================================")

        return message

    def make_plain_mail(self, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = "[sender] report"
        message['from'] = self.mail_config["sender"]
        message['to'] = self.receiver

        return message

    def getAtt(self, filename, bytefile):
        """
        添加附件
        :param bytefile:文件名
        """
        try:
            att = MIMEText(bytefile, 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(filename, 'utf-8')
            logger.debug("make %s" % filename)
            return att
        except Exception as e:
            logger.warning(e)
