# coding=utf-8

import re
import cnconvert as cn2
import sql
import Kmail
from Spider import Spider
import logging
import logging.config

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='[%H:%M:%S]', )
logging.config.fileConfig("logging.conf")

class Title:
    def __chinese(self, chapter):
        """
        中文标题:如第一百章
        :param chapter:
        :return:

        >>> getNumOfTitle_chi("第两百零一章")
        201
        >>> getNumOfTitle_chi("第两百测零试一章")
        201
        >>> getNumOfTitle_chi("两百")
        -1
        """
        num = -1
        pattern_chi = re.compile(r'第.+章')
        match_chi = pattern_chi.search(chapter)
        if match_chi:
            chapter = match_chi.group()[1:-1]

            if "两" in chapter:
                chapter = chapter.replace("两", "二")
            try:
                num = cn2.c2n(chapter)

            # 如果无法从中文转为数字，说明章节名混入了奇怪的字符
            except Exception as e:
                string = ""
                pat = re.compile(r'[零一二三四五六七八九十百千两]+')
                match_chi = pat.findall(chapter)
                for i in match_chi:
                    string += i
                num = cn2.c2n(string)
        return num

    def __digit(self, chapterTitle):
        '''
        数字标题:如第100章

        >>> getNumOfTitle_d("第1029章")
        1029
        '''
        num = -1
        pattern_d = re.compile(r'第\d+章')
        cha = pattern_d.search(chapterTitle)
        if cha:
            rs = cha.group()[1:-1]
            if len(str(rs)) >= 1:
                num = int(rs)
        return num

    def getNumOfTitle(self, chapter):
        '''
        获得章节编号

        >>> getNumOfTitle("第1029章")
        1029
        >>> getNumOfTitle("第两百零一章")
        201
        >>> getNumOfTitle("第两百测零试一章")
        201
        '''
        num = -1
        # 若全数字
        pattern_d = re.compile(r'第\d+章')
        cha = pattern_d.search(chapter)
        if cha:
            num = self.__digit(chapter)
        # 若其他
        else:
            num = self.__chinese(chapter)
        return num


def suffix(start, end):
    '''
    start(int) end(int) 构造待发送的文件名后缀：230-235 表示从230章到235章

    >>> suffix(23,90)
    '23-90'
    '''
    suf = ""
    if start == end:
        suf = str(start)
    else:
        suf = str(start) + "-" + str(end)
    return suf


def is_chi(self, text):
    "判断是否为中文"
    return all('\u4e00' <= char <= '\u9fff' for char in text)


# +++++++++++++++++++++++++++++++++++++++++
class Novel():
    """
    负责封装下载小说的基本操作
    """

    def __init__(self):
        self.spider = Spider()
        self.FilenameCharset = "en"

    def setFilenameCharset(self, charset):
        self.FilenameCharset = charset

    def get_latest_updates(self, pageUrl, checknum):
        """
        获得最近更新的小说
        :param pageUrl:小说目录链接
        :param checknum:小于该数字的更新数，不发送
        :return:
        """
        lists = self.spider.getAllChapterLinks(pageUrl)
        novelname_chi = self.spider.getNovelName_chi(pageUrl)
        # 当前读到了
        nowat = sql.readAtChapter(novelname_chi)

        # 设置文件名语言en or chi
        if self.FilenameCharset == "en":
            filename = self.spider.getNovelName_en(pageUrl)
        else:
            filename = novelname_chi

        l = []
        isnew = False

        # 将新章节的url和name放入l
        for i in lists:
            if i[1] == nowat:
                isnew = True
                continue
            if isnew:
                if not sql.hasChapter(novelname_chi, i[1]):
                    l.append(i)

        logging.info("小说标题:%s" % novelname_chi)
        # checknum=0 一有新的章节就更新 checknum=3 累积三章以上再推送
        try:
            newest = l[-1][1]
            logging.info("当前已读到%s" % nowat)
            logging.info("最新章节为%s" % newest)
        except Exception as e:
            logging.info("无新章节")
            return ""
        if checknum != 0 and len(l) != 0 and checknum > len(l):
            logging.info("[暂不发送]:当前小说更新了%d章...[%d/%d]" % (len(l), len(l), checknum))
            return ""
        else:
            for i in l:
                sql.addChapter(novelname_chi, i[1])

        # 构造待发送的文件名：该处理很不健壮！！
        cleanlist = self.__washNovelList(l)
        start = cleanlist[1]
        end = cleanlist[2]
        # 构造文件名
        suf = suffix(start, end)
        filename = filename + "#" + suf + ".txt"
        # 抓取l内的文章
        self.spider.download(l, filename)
        logging.info("下载文件成功...")
        sql.setAtChapter(novelname_chi, newest)
        return filename

    def __washNovelList(self, lists):
        l = []
        mx = 0
        mi = 1000000
        logging.info(">" * 5 + "正在处理章节信息" + "<" * 5)

        newcircle = False
        numOfChapterOne = 0

        ERROR_RANGE = 10
        # ERROR_PROBABILITY=0.85

        logging.info("待处理章节数%d" % len(lists))
        tit = Title()
        if len(lists) == 1:
            num = tit.getNumOfTitle(lists[0][1])
            mx = num
            mi = num
        else:
            for item in lists:
                try:
                    chapter = item[1]
                    # print("wash "+chapter)
                    num = tit.getNumOfTitle(chapter)

                    # 某些章节出现从1到200又从1开始，
                    # 如 1 2 3 4 …… 368 1 2 3 ……256 ，
                    # 因为分了卷名之类，所以检测是否章节名循环
                    # 如果进入新的循环，那么重置计数器
                    # mx=0 mi=1000000 newcircle=False

                    # 判断小说是否含有多个卷：当前为第一章
                    if 1 == num:
                        # 若第一章的计数不为0，说明存在多个第一章 即进入新的【卷】
                        if numOfChapterOne != 0:
                            newcircle = True
                            numOfChapterOne += 1
                    # 如果小说为正常序号：第1章~第n章
                    if not newcircle:
                        if num >= mx:
                            mx = num
                        if num <= mi:
                            mi = num
                    # 如果小说按卷等分别标序号：第一卷第1章~第二卷第30章
                    else:
                        mx = 0
                        mi = 1000000
                        newcircle = False

                    l.append(item)
                except Exception as e:
                    print(e)
        # print(">>"*20)
        logging.debug("max:%d min:%d" % (mx, mi))
        return l, mi, mx

    def run(self):
        pass


class Service:
    """
    向外提供服务
    """

    def __init__(self):
        self.novel = Novel()
        self.mail = Kmail.Mail()
        self.checknum = 3
        self.novelList=[]
        self.novels=[]

    def all_novels_latest_updates_2_kindle(self):
        """
        发送最近更新的小说(未阅读)到kindle中
        :param novelUrl: 小说目录链接
        :param checknum:
        :return:
        """
        for noveltouple in self.novels:
            fname = self.novel.get_latest_updates(noveltouple[0], self.checknum)
            if fname!="":
                self.novelList.append(fname)
        self.mail.send2kindle(self.novelList)

    def add_novel(self,noveltouple):
        self.novels.append(noveltouple)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
