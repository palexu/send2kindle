# coding=utf-8
from __future__ import unicode_literals
from .dao import *
from datetime import datetime


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


class BookService:
    def __init__(self):
        self.bookDAO = BookDAO()

    def add_book(self, book):
        """
        :param book:dict()
        :return:
        """
        self.bookDAO.insert()

    def select_all(self):
        return self.bookDAO.select_all()

    def delete_by_id(self, id):
        self.bookDAO.delete(id)

    def update_by_id(self, book):
        pass


class TaskDataService:
    def __init__(self, task_type):
        """
        :param task_type: novel or rss
        """
        self._task_dao = SendTaskDAO()
        self._task_log_dao = LogDAO()

        self.task_type = task_type
        self.biz_no = self._gen_biz_no()
        self.content = []

        self._is_task_start = False

    def _gen_biz_no(self):
        biz_no = "%s [%s]" % (str(datetime.now())[:-7], self.task_type)
        return biz_no

    def start_task(self):
        # 0:失败 1:成功

        try:
            self._task_dao.insert(self.biz_no, start=datetime.now(), status=0)
            self._is_task_start = True
        except Exception as e:
            logger.error(e)

    def info(self, info, log=None):
        if not self._is_task_start:
            self.start_task()
        if log:
            log.info(info)
        self.content.append(info)

    def error(self, info, log=None):
        if not self._is_task_start:
            self.start_task()
        if log:
            log.info(info)
        self.content.append(info)

    def end_task(self, status):
        if not self._is_task_start:
            raise Exception(u"end_task is not allowed before task start.")
        try:
            for info in self.content:
                self._task_log_dao.insert(self.biz_no, info)
            self._task_dao.update(self.biz_no, end=datetime.now(), status=status)
        except Exception as e:
            logger.error(e)
