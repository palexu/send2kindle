# coding=utf-8
import sqlite3

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from sender.util.config import *

db = SqliteExtDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db


class BookMeta(BaseModel):
    """
    对应于书籍元信息
    """
    id = IntegerField(primary_key=True)
    name = CharField()
    author = CharField()
    url = CharField()
    limit = IntegerField()
    read_at = TextField()
    send_rate = CharField()
    status = IntegerField()
    remark = TextField()

    class Meta:
        db_table = "book"

    def parse(self, book):
        """
        接受dict与成员变量

        :param book:
        :return:
        """
        if isinstance(book, dict):
            from bunch import bunchify
            book = bunchify(book)
        try:
            self.id = book.id
            self.name = book.name
            self.author = book.author
            self.url = book.url
            self.limit = book.limit
            self.read_at = book.read_at
            self.send_rate = book.send_rate
            self.status = book.status
            self.remark = book.remark
            return True
        except Exception as e:
            logger.error(e)
            return False

    def to_dict(self):
        return self._data


class ReadedDao:
    def __init__(self):
        pass

    def del_novel(self, bookname):
        return BookMeta.delete().where(BookMeta.name == bookname)

    def load_novel(self, bookname):
        return BookMeta.select().where(BookMeta.name == bookname)

    def is_book_exits(self, bookname):
        return BookMeta.select().where(BookMeta.name == bookname)

    def load_read_at(self, bookname):
        book = BookMeta.select().where(BookMeta.name == bookname).get()
        return book.read_at

    def set_read_at(self, bookname, readAt):
        book = BookMeta.select().where(BookMeta.name == bookname).get()
        book.read_at = readAt
        return book.save()


class Chapter(BaseModel):
    id = IntegerField(primary_key=True)
    bookname = CharField()
    chaTitle = CharField()
    chaContent = TextField()


class ChapterDao:
    def __init__(self):
        pass

    def add_chapter(self, bookname, chaTitle, chaContent=""):
        c = Chapter()
        c.bookname = bookname
        c.chaTitle = chaTitle
        c.chaContent = chaContent

    def has_chapter(self, bookname, chaTitle):
        return Chapter().select(fn.Count(Chapter.bookname)).where(
            Chapter.bookname == bookname and Chapter.chaTitle == chaTitle)

    def delete_chapter(self, bookname, chaTitle):
        return Chapter().delete().where(Chapter.bookname == bookname and Chapter.chaTitle == chaTitle)


class LogDAO:
    def __init__(self):
        self.table = "task_log"

    def insert(self, biz_no, content):
        from datetime import datetime
        try:
            with sqlite3.connect(db_path) as conn:
                param = (biz_no, content, datetime.now())
                conn.execute("""
                   insert into %s(biz_no,content,gmt_create)
                   VALUES (?,?,?)
                """ % self.table, param)
                conn.commit()
        except Exception as e:
            logger.error(e)


class SendTaskDAO:
    def __init__(self):
        self.table = "send_task"

    def insert(self, biz_no, start="", status=0):
        try:
            with sqlite3.connect(db_path) as conn:
                param = (biz_no, start, status)
                conn.execute("""
                   insert into %s(biz_no,start,status)
                   VALUES (?,?,?)
                """ % self.table, param)
                conn.commit()
        except Exception as e:
            logger.error(e)

    def update(self, biz_no, end, status=1):
        try:
            with sqlite3.connect(db_path) as conn:
                param = (end, status, biz_no)
                conn.execute("""
                   update %s
                   set end=?,status=?
                   where biz_no=?
                """ % self.table, param)
                conn.commit()
        except Exception as e:
            logger.error(e)


class BookDAO:
    def __init__(self):
        pass

    def insert(self, book):
        try:
            bm = BookMeta()
            if not bm.parse(book):
                return False
            return bm.save()
        except Exception as e:
            logger.error(e)
        return False

    def select_all(self):
        return BookMeta.select()

    def delete(self, id):
        return BookMeta.delete().where(BookMeta.id == id)

    def update(self, id, book):
        try:
            bm = BookMeta()
            if not bm.parse(book):
                return False
            bm.id = id
            return bm.update()
        except Exception as e:
            logger.error(e)
        return False
