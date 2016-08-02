#coding=utf-8
import sqlite3

def createTable():
	try:
		conn=sqlite3.connect("novel.db")
		conn.execute("""
			create table readed(
			id int,
			novelname char(50),
			at int
			)
			""")
	except Exception as e:
		print(e)
	finally:
		conn.close()

def addNovel(bookname,bid=0,at=0):
	print("add "+bookname)
	try:
		conn=sqlite3.connect("novel.db")
		param=(bid,bookname,at,)
		conn.execute("""
			insert into readed
			values(?,?,?)
			""",param)
		conn.commit()
	except Exception as e:
		print(e)
	finally:
		conn.close()

def delNovel(bookname):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		conn.execute("""
			delete from readed
			where novelname=?
			""",param)
		conn.commit()
	except Exception as e:
		print(e)
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

def nextChapter(bookname):
	"只用于查询下一个章节，只有当新的章节被推送成功时，才能修改at的值"
	if isExits(bookname)==False:
		print(bookname+" not exits,create one")
		addNovel(bookname, bid=0, at=0)
		return 1
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		cursor=conn.execute("""
			select at from readed
			where novelname=?
			""",param)
		nowAt=cursor.fetchone()[0]
		return nowAt+1
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	
def setAtChapter(bookname,num):
	"设置最后推送的章节数"
	if isExits(bookname)==False:
		print(bookname+" not exits,create one")
		addNovel(bookname, bid=0, at=num)
	try:
		conn=sqlite3.connect("novel.db")
		param=(num,bookname,)
		conn.execute("""
			update readed 
			set at=?
			where novelname=?
			""",param)
		conn.commit()
	except Exception as e:
		print(e)

	conn.close()

def isExits(bookname):
	try:
		conn=sqlite3.connect("novel.db")
		param=(bookname,)
		cursor=conn.execute("""
			select count(*) from readed
			where novelname=?
			""",param)
		if cursor.fetchone()[0]==0:
			print(bookname+" not in db")
			return False
		else:
			print(bookname+" in db")
			return True
	except Exception as e:
		print(e)
	finally:
		conn.close()

if __name__ == '__main__':
	print("test:add & del")
	show()
	addNovel("test")
	show()
	delNovel("test")
	show()

