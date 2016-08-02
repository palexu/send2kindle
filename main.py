import novel
import sql
links=[
	"http://www.shumilou.co/xiuzhensiwannian",
	"http://www.shumilou.co/jingsongleyuan",
	"http://www.shumilou.co/zoujinxiuxian",
	"http://www.shumilou.co/heianxueshidai",
	"http://www.shumilou.co/zhongshengzhishenjixueba",
]
if __name__ == '__main__':
	# sql.setAtChapter("走进修仙",340)
	sql.setAtChapter("惊悚乐园",1188)
	sql.show()

	# for link in links:
	# 	novel.NewCapters2kindle(link)