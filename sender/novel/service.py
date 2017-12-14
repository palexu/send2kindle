#coding=utf-8
from sender.novel.novel_downloader import NovelDownloader
from util import kmail
from util import config
from util import server_chan

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")


class Service:
    """
    向外提供服务
    """

    def __init__(self, config):
        if self.check_config(config):
            self.config = config
        else:
            raise Exception("error while reading config")
        self.novelSpider = NovelDownloader()
        self.mailSender = kmail.Mail()
        self.novels = []

    def all_novels_latest_updates_2_kindle(self):
        """
        发送最近更新的小说(未阅读)到kindle中
        :return:
        """
        novelNameList = []
        for item in self.config["urls"]:
            fname = self.novelSpider.get_latest_updates(item["name"], item["url"], item["count"])
            if fname != "":
                novelNameList.append(fname)

        if len(novelNameList) == 0:
            logging.info("nothing to send")
        else:
            logging.debug("%s wait to be send..." % novelNameList)
            if self.mailSender.send2kindle(novelNameList):
                scKey = config.server_chan()
                server_chan.send(scKey, "小说发送成功", self.mailSender.make_report_message(novelNameList))

    def check_config(self, config):
        """
        加载配置文件
        :param config:
        :return:
        """
        # 判断配置文件结构
        return True
