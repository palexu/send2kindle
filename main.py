import novel
import sql
links=[
	"http://www.shumilou.co/xiuzhensiwannian",
	"http://www.shumilou.co/jingsongleyuan",
	"http://www.shumilou.co/zoujinxiuxian",
	"http://www.shumilou.co/heianxueshidai",
]
if __name__ == '__main__':
	# # if sql.isExits("黑暗血时代")==True:
	# # 	print("exist")
	# # else:
	# # 	print("not")
	# # sql.nextChapter("走进修仙")
	# sql.setAtChapter("黑暗血时代",1166)
	# sql.setAtChapter("走进修仙",340)
	# sql.setAtChapter("惊悚乐园",1188)
	sql.show()
	
	for link in links:
		novel.NewCapters2kindle(link)