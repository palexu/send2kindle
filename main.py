# coding=utf-8
import Novel

# 默认发送每三章节发送一次
# 0，1：一有新章节就发送
# 2-n：累积n章节后发送

if __name__ == '__main__':
    settings = [
        ["http://www.shumilou.co/xiuzhensiwannian", 0],
        ["http://www.shumilou.co/jingsongleyuan", ],
        ["http://www.shumilou.co/zoujinxiuxian", 0],
        ["http://www.shumilou.co/heianxueshidai", ],
        ["http://www.shumilou.co/zhongshengzhishenjixueba", ],
    ]
    service = Novel.Service()
    for link in settings:
        service.add_novel(link)
    service.all_novels_latest_updates_2_kindle()

