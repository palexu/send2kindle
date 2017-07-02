# coding=utf-8
import sqlite3
import traceback
import logging
import logging.config
logging.config.fileConfig("config/logging.conf")

def createTableReaded():
    try:
        conn = sqlite3.connect("novel.db")
        conn.execute("""
			CREATE TABLE readed(
			bookid INTEGER PRIMARY KEY AUTOINCREMENT,
			bookname char(50),
			at char(100)
			)
			""")
        conn.commit()
    except Exception as e:
        # print(e)
        traceback.print_exc()
    finally:
        conn.close()


def createTableChapters():
    try:
        conn = sqlite3.connect("novel.db")
        conn.execute("""
			CREATE TABLE chapters(
			chaTitle char(100) PRIMARY KEY,
			bookname char(50),
			chaContent TEXT,
			FOREIGN KEY(bookname) REFERENCES readed(novelname)
			)
			""")
        conn.commit()
    except Exception as e:
        # print(e)
        traceback.print_exc()
    finally:
        conn.close()


def addNovel(bookname, bid=0, at=""):
    print("add " + bookname)
    try:
        conn = sqlite3.connect("novel.db")
        if bid == 0:
            bid = None
        param = (bid, bookname, at,)
        conn.execute("""
			INSERT INTO readed
			VALUES(?,?,?)
			""", param)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
    # print(e)
    finally:
        conn.close()


def delNovel(bookname):
    try:
        conn = sqlite3.connect("novel.db")
        param = (bookname,)
        conn.execute("""
			DELETE FROM readed
			WHERE bookname=?
			""", param)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
    # print(e)
    finally:
        conn.close()


def show():
    print('=' * 10 + "show" + '=' * 10)
    conn = sqlite3.connect("novel.db")
    cursor = conn.execute("""
		SELECT * FROM readed
		""")
    for row in cursor:
        for col in row:
            print(col)
    cursor.close()
    conn.close()
    print('=' * 10 + "end-show" + '=' * 10)


def readAtChapter(bookname):
    "只用于查询下一个章节，只有当新的章节被推送成功时，才能修改at的值"
    if not isBookExits(bookname):
        print(bookname + " not exits,create one")
        addNovel(bookname)
        return 1
    try:
        conn = sqlite3.connect("novel.db")
        param = (bookname,)
        cursor = conn.execute("""
			SELECT at FROM readed
			WHERE bookname=?
			""", param)
        nowAt = cursor.fetchone()[0]
        return nowAt
    except Exception as e:
        traceback.print_exc()
    # print(e)
    finally:
        # cursor.close()
        conn.close()


def setAtChapter(bookname, readAt):
    "设置最后推送的章节数"
    if isBookExits(bookname) == False:
        print(bookname + " not exits,create one")
        addNovel(bookname, bid=0, at=readAt)
    try:
        conn = sqlite3.connect("novel.db")
        param = (readAt, bookname,)
        conn.execute("""
			UPDATE readed
			SET at=?
			WHERE bookname=?
			""", param)
        conn.commit()
    except Exception as e:
        # print(e)
        traceback.print_exc()

    conn.close()


def isBookExits(bookname):
    try:
        conn = sqlite3.connect("novel.db")
        param = (bookname,)
        cursor = conn.execute("""
			SELECT count(*) FROM readed
			WHERE bookname=?
			""", param)
        if cursor.fetchone()[0] == 0:
            # print(bookname+" not in db")
            return False
        else:
            # print(bookname+" in db")
            return True
    except Exception as e:
        traceback.print_exc()
    # print(e)
    finally:
        conn.close()


def addChapter(bookname, chaTitle, chaContent=""):
    try:
        conn = sqlite3.connect("novel.db")
        param = (bookname, chaTitle, chaContent,)
        conn.execute("""
			INSERT INTO chapters('bookname','chaTitle','chaContent')
			VALUES(?,?,?)
			""", param)
        conn.commit()
    except Exception as e:
        traceback.print_exc()
    # print(e)
    finally:
        conn.close()


def hasChapter(bookname, chaTitle):
    try:
        conn = sqlite3.connect("novel.db")
        param = (bookname, chaTitle,)
        cursor = conn.execute("""
			SELECT count(*) FROM chapters
			WHERE bookname=? AND chaTitle=?
			""", param)
        has = cursor.fetchone()[0]
        if has == 1:
            return True
        else:
            return False
    except Exception as e:
        traceback.print_exc()
    finally:
        # cursor.close()
        conn.close()


def test_delChapter():
    try:
        conn = sqlite3.connect("novel.db")
        conn.execute("""
			DELETE FROM chapters
			""")
        logging.debug("clear data in sqltable[chapters]...")
        conn.commit()
    except Exception as e:
        traceback.print_exc()
    finally:
        # cursor.close()
        conn.close()


if __name__ == '__main__':
    createTableChapters()
    createTableReaded()
