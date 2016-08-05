#coding=utf-8
import novel
import sql

#默认发送每三章节发送一次
#0，1：一有新章节就发送
#2-n：累积n章节后发送
links=[
	["http://www.shumilou.co/xiuzhensiwannian",0],
	["http://www.shumilou.co/jingsongleyuan",],
	["http://www.shumilou.co/zoujinxiuxian",0],
	["http://www.shumilou.co/heianxueshidai",],
	["http://www.shumilou.co/zhongshengzhishenjixueba",],
]
if __name__ == '__main__':
	
	# sql.show()
	# sql.setAtChapter("走进修仙","第三百四十二章 我们的风格")
	# sql.setAtChapter("惊悚乐园","月初预告之1608")
	# sql.setAtChapter("重生之神级学霸","第九百二十二章 案例出现")
	# sql.setAtChapter("惊悚乐园","月初预告之1608")
	# sql.setAtChapter("黑暗血时代","第一千五百九十三章 围杀单元")
	# sql.test_delChapter("走进修仙")
	# sql.test_delChapter("惊悚乐园")
	# sql.test_delChapter("重生之神级学霸")
	# sql.test_delChapter("惊悚乐园")
	# sql.test_delChapter("黑暗血时代")
	for link in links:
		pageurl=link[0]
		if len(link)==1:
			novel.NewCapters2kindle(link[0])
		else:
			novel.NewCapters2kindle(link[0],link[1])