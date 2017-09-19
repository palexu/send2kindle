# coding=utf-8
import logging
import logging.config
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

logging.config.fileConfig("../config/logging.conf")


class Mail:
    def __init__(self):
        with open("../config/config.yaml") as f:
            config = yaml.load(f)["mail"]
            print(config)
        self.init_host = config["init_host_config"]
        self.host = config["hostconf"][self.init_host]
        self.receiver = config["receiver"]
        self.reportReceiver = config["reportReceiver"]
        self.subject = config["subject"]
        self.msgcontent = config["msgcontent"]

    def send2kindle(self, novellist):
        """
        发送小说到kindle 发送报告到接受者
        :param novellist:
        :return: true or false
        """
        with smtplib.SMTP_SSL(self.host["host"]) as s:
            s.login(self.host["sender"], self.host["password"])
            try:
                message = self.make_kindle_mail(novellist)
                s.sendmail(self.host["sender"], self.receiver, message.as_string())
                logging.info("[%s]发送成功" % novellist)
                report = self.make_report(novellist)
                s.sendmail(self.host["sender"], self.reportReceiver, report.as_string())
                logging.info("报告已发送到[%s]" % self.reportReceiver)
                return True
            except smtplib.SMTPDataError as re:
                logging.error("邮件发送失败:%s" % re)
                return False

    def make_kindle_mail(self, filelist):
        """
        :param filelist:文件列表
        :return:
        """

        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['from'] = self.host["sender"]
        message['to'] = self.receiver

        message.attach(MIMEText(self.msgcontent, 'plain', 'utf-8'))
        for filename in filelist:
            logging.debug("%s add to message" % filename)
            message.attach(self.getAtt(filename))

        logging.debug("=================================")
        logging.debug("using mail config:%s" % self.host)
        logging.debug("subject: %s" % message['Subject'])
        logging.debug("from:    %s" % message['from'])
        logging.debug("to:      %s" % message['to'])
        logging.debug("邮件内容  :%s" % self.msgcontent)
        logging.debug("=================================")

        return message

    def make_report(self, novel_list):
        s = self.make_report_message(novel_list)
        message = MIMEText(s, 'plain', 'utf-8')
        message['Subject'] = "[send2kindle] report"
        message['from'] = self.host["sender"]
        message['to'] = self.reportReceiver

        return message

    def make_report_message(self, novel_list):
        s = "下列更新已发送:\n"
        for i in novel_list:
            s = s + i + "\n"
        logging.debug("report content=%s" % s)
        return s

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


if __name__ == '__main__':
    m = Mail()
