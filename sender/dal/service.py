# coding=utf-8
from __future__ import unicode_literals
from .dao import *


class DataService:
    def __init__(self, book_name):
        self.book_name = book_name
        self.readedDao = ReadedDao()
        self.chapterDao = ChapterDao()

    def now_read_at(self, now_read_at=None):
        """获取或更新当前所阅读到的章节"""
        if now_read_at is None:
            return self.readedDao.load_read_at(self.book_name)
        else:
            self.readedDao.set_read_at(self.book_name, now_read_at)
            return now_read_at

    def add_chapters(self, url_name_pair):
        for url, name in url_name_pair:
            self.chapterDao.add_chapter(self.book_name, name)
