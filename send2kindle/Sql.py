# coding=utf-8
import sqlite3
import traceback
import logging
import os
import logging.config

logging.config.fileConfig("../config/logging.conf")
db = os.path.abspath(r'../db/novel.db')
print(db)


class ReadedDao:
    def __init__(self):
        self.table = "readed"

    def add_novel(self, bookname, bid=None, at=""):
        """
        默认设置bookid自增，at为""
        :param bookname:书名
        :param bid:书id
        :param at:书读到章节
        :return:None
        """
        try:
            with sqlite3.connect(db) as conn:
                param = (bid, bookname, at,)
                conn.execute("""
                    INSERT INTO
                    %s(bookid, bookname, at)
                    VALUES(?,?,?)
                    """ % self.table, param)
                conn.commit()
        except Exception as e:
            traceback.print_exc()

    def del_novel(self, bookname):
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname,)
                conn.execute("""
                    DELETE FROM
                    %s
                    WHERE bookname=?
                    """ % self.table, param)
                conn.commit()
        except Exception as e:
            traceback.print_exc()

    def load_novel(self, bookname):
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname,)
                cursor = conn.execute("""
                                SELECT * FROM
                                %s
                                WHERE bookname=?
                                """ % self.table, param)
                conn.commit()
                rs = cursor.fetchone()
                return rs
        except Exception as e:
            traceback.print_exc()

    def is_book_exits(self, bookname):
        try:
            return self.load_novel(bookname)[0] > -1
        except Exception as e:
            return False

    def load_read_at(self, bookname):
        "只用于查询下一个章节，只有当新的章节被推送成功时，才能修改at的值"
        if not self.is_book_exits(bookname):
            logging.info(bookname + " not exits,create one")
            self.add_novel(bookname)
            return 1
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname,)
                cursor = conn.execute("""
                    SELECT at FROM %s
                    WHERE bookname=?
                    """ % self.table, param)
                return cursor.fetchone()[0]
        except Exception as e:
            traceback.print_exc()

    def set_read_at(self, bookname, readAt):
        "设置最后推送的章节数"
        if not self.is_book_exits(bookname):
            logging.info(bookname + " not exits,create one")
            self.add_novel(bookname, bid=0, at=readAt)
        try:
            with sqlite3.connect(db) as conn:
                param = (readAt, bookname,)
                conn.execute("""
                    UPDATE %s
                    SET at=?
                    WHERE bookname=?
                    """ % self.table, param)
                conn.commit()
        except Exception as e:
            traceback.print_exc()


class ChapterDao():
    def __init__(self):
        self.table = "chapters"

    def add_chapter(self, bookname, chaTitle, chaContent=""):
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname, chaTitle, chaContent,)
                conn.execute("""
                    INSERT INTO %s('bookname','chaTitle','chaContent')
                    VALUES(?,?,?)
                    """ % self.table, param)
                conn.commit()
        except Exception as e:
            traceback.print_exc()

    def has_chapter(self, bookname, chaTitle):
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname, chaTitle,)
                cursor = conn.execute("""
                    SELECT count(*) FROM %s
                    WHERE bookname=? AND chaTitle=?
                    """ % self.table, param)
                has = cursor.fetchone()[0]
                if has == 1:
                    return True
                else:
                    return False
        except Exception as e:
            traceback.print_exc()

    def delete_chapter(self, bookname, chaTitle):
        try:
            with sqlite3.connect(db) as conn:
                param = (bookname, chaTitle,)
                conn.execute("""
                    delete from %s
                    WHERE bookname =? AND chaTitle =?
                """ % self.table, param)
                conn.commit()
        except Exception as e:
            traceback.print_exc()
