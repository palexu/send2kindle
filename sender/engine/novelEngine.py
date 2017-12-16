# coding=utf-8
from __future__ import unicode_literals

import logging
import logging.config

from sender import calibre_driver
from sender import dal
from sender.engine import biqugespider
from sender.novel.model import Book
from util import config
from util import kmail
from util import server_chan

logging.config.fileConfig("config/logging.conf")


class NovelEngine:
    """
    小说下载器
    """

    def __init__(self):
        self.spider = biqugespider.BiqugeSpider()
        self.readedDao = dal.ReadedDao()
        self.chapterDao = dal.ChapterDao()
        self.config = config.settings
        self.mailSender = kmail.Mail()
        self.novels = []

    def all_novels_latest_updates_2_kindle(self):
        """
        发送最近更新的小说(未阅读)到kindle中
        :return:
        """
        ebook = calibre_driver.Ebook("today's_novel")

        isUpdated = False
        booknames = ""
        for item in self.config["urls"]:
            bookname = item["name"]
            url = item["url"]
            count = item["count"]
            booknames = bookname + " "
            book = self.get_latest_updates(bookname, url, count)
            for title, content in book.sections:
                ebook.add_section(bookname, title, content)
                isUpdated = True

        if not isUpdated:
            logging.info("nothing to send")
            return

        # logging.debug("%s wait to be send..." % books)
        byteBook = ebook.get_byte_book()
        with open("n.mobi","w+") as f:
            f.write(byteBook)
        if self.mailSender.send2kindle(ebook.ebook_name, byteBook):
            scKey = config.server_chan()
            server_chan.send(scKey, "小说发送成功", booknames)

    def get_latest_updates(self, bookname, pageUrl, checknum):
        """
        获得最近更新的小说
        :param pageUrl:小说目录链接
        :param checknum:小于该数字的更新数，不发送
        :return:
        """
        book = Book()

        lists = self.spider.get_all_chapter_links(pageUrl)

        # 当前读到了
        nowat = self.readedDao.load_read_at(bookname)

        url_name_pair = []
        isnew = False

        # 将新章节的url和
        # name放入l
        for url, name in lists:
            if name in nowat or nowat in name:
                isnew = True
                continue
            if isnew:
                if not self.chapterDao.has_chapter(bookname, name):
                    url_name_pair.append((url, name))

        logging.info("小说标题:%s" % bookname)
        try:
            newest = url_name_pair[-1][1]
            logging.info("当前已读到%s" % nowat)
            logging.info("最新章节为%s" % newest)
        except Exception as e:
            logging.info("无新章节")
            return book
        if checknum != 0 and len(url_name_pair) != 0 and checknum > len(url_name_pair):
            logging.info("[暂不发送]:当前小说更新了%d章...[%d/%d]" % (len(url_name_pair), len(url_name_pair), checknum))
            return book
        else:
            for url, name in url_name_pair:
                self.chapterDao.add_chapter(bookname, url, name[1])

        book.book_name = bookname

        for title, content in self.spider.download(url_name_pair):
            book.add_section(title, content)

        logging.info("下载文件成功...")
        # self.readedDao.set_read_at(novelname_chi, newest)
        return book
#
# class Acceptor:
#     def selcet(self):
#
