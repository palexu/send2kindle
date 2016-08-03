#coding=utf-8
import sqlite3
import traceback

def createTableReaded():
	try:
		conn=sqlite3.connect("novel.db")
		conn.execute("""
			create table readed(
			bookid integer primary key autoincrement,
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
		conn=sqlite3.connect("novel.db")
		conn.execute("""
			create table chapters(
			chaTitle char(100) primary key,
			bookname char(50),
			chaContent text,
			foreign key(bookname) references readed(novelname)
			)
			""")
		conn.commit()
	except Exception as e:
		# print(e)
		traceback.print_exc()
	finally:
		conn.close()

def addNovel(bookname,bid=0,at=""):
	print("add "+bookname)
	try:
		conn=sqlite3.connect("novel.db")
		if bid==0:
			bid=None
		param=(bid,bookname,at,)
		conn.execute("""
			insert into readed
			values(?,?,?)
			""",param)
		conn.commit()
	except Exception as e:
		traceback.print_exc()
		# print(e)
	finally:
		conn.close()

def delNovel(bookname):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		conn.execute("""
			delete from readed
			where bookname=?
			""",param)
		conn.commit()
	except Exception as e:
		traceback.print_exc()
		# print(e)
	finally:
		conn.close()

def show():
	print('='*10+"show"+'='*10)
	conn=sqlite3.connect("novel.db")
	cursor=conn.execute("""
		select * from readed
		""")
	for row in cursor:
		for col in row:
			print(col)
	cursor.close()
	conn.close()
	print('='*10+"end-show"+'='*10)

def readAtChapter(bookname):
	"只用于查询下一个章节，只有当新的章节被推送成功时，才能修改at的值"
	if isBookExits(bookname)==False:
		print(bookname+" not exits,create one")
		addNovel(bookname)
		return 1
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		cursor=conn.execute("""
			select at from readed
			where bookname=?
			""",param)
		nowAt=cursor.fetchone()[0]
		return nowAt
	except Exception as e:
		traceback.print_exc()
		# print(e)
	finally:
		cursor.close()
		conn.close()
	
def setAtChapter(bookname,readAt):
	"设置最后推送的章节数"
	if isBookExits(bookname)==False:
		print(bookname+" not exits,create one")
		addNovel(bookname, bid=0, at=readAt)
	try:
		conn=sqlite3.connect("novel.db")
		param=(readAt,bookname,)
		conn.execute("""
			update readed 
			set at=?
			where bookname=?
			""",param)
		conn.commit()
	except Exception as e:
		# print(e)
		traceback.print_exc()

	conn.close()

def isBookExits(bookname):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		cursor=conn.execute("""
			select count(*) from readed
			where bookname=?
			""",param)
		if cursor.fetchone()[0]==0:
			print(bookname+" not in db")
			return False
		else:
			print(bookname+" in db")
			return True
	except Exception as e:
		traceback.print_exc()
		# print(e)
	finally:
		conn.close()

def addChapter(bookname,chaTitle,chaContent=""):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,chaTitle,chaContent,)
		conn.execute("""
			insert into chapters('bookname','chaTitle','chaContent')
			values(?,?,?)
			""",param)
		conn.commit()
	except Exception as e:
		traceback.print_exc()
		# print(e)
	finally:
		conn.close()

def hasChapter(bookname,chaTitle):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,chaTitle,)
		cursor=conn.execute("""
			select count(*) from chapters
			where bookname=? and chaTitle=?
			""",param)
		has=cursor.fetchone()[0]
		if has==1:
			return True
		else:
			return False
	except Exception as e:
		traceback.print_exc()
	finally:
		# cursor.close()
		conn.close()
if __name__ == '__main__':
	createTableChapters()
