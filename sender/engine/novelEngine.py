# coding=utf-8
from __future__ import unicode_literals

import logging
import logging.config

from sender import calibre_driver
from sender.engine import biqugespider
from sender.engine.base import BaseEngine
from util import config
from util import kmail

logging.config.fileConfig("config/logging.conf")


class NovelEngine(BaseEngine):
    """
    小说下载器
    """

    def __init__(self):
        self.books_config = config.books()
        self.mailSender = kmail.Mail()

    def push_updates(self):
        """
        发送最近更新的小说(未阅读)到kindle中
        :return:
        """
        ebook = calibre_driver.Ebook("today's_novel.mobi")
        books = self.get_updates()
        self._insert_ebook(ebook, books)
        self.mailSender.send2kindle(ebook.ebook_name, ebook.get_byte_book())

    def get_updates(self):
        return dispacher(self.books_config)

    def _insert_ebook(self, ebook, books):
        for book in books:
            try:
                if book and len(book.sections) > 0:
                    ebook.add_sections(book.book_name, book.sections)
            except Exception as e:
                logging.error(e)


def dispacher(config):
    books = []
    # 暂时只支持这个呗
    spider = biqugespider.BiqugeSpider()
    for item in config:
        bookname = item["name"]
        url = item["url"]
        count = item["count"]

        book = spider.get_update(bookname, url, count)
        if book:
            books.append(book)
    return books
