# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Book:
    """小说"""

    def __init__(self, bookname):
        self.book_name = bookname
        self.sections = []

    def add_section(self, chapter_name, chapter_content):
        self.sections.append((chapter_name, chapter_content))


class BookConfig:
    def __init__(self, config):
        self.book_name = config["name"]
        self.url = config["url"]
        try:
            self.limit = config["count"]
        except:
            self.limit = 3

    def __str__(self):
        return u"书名:%s\n目录页链接:%s\n最少发送章节数:%s\n\n" % (self.book_name, self.url, self.limit)
