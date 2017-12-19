# coding=utf-8
import re
from sender.util import cnconvert as cn2


def suffix(start, end):
    """
    start(int) end(int) 构造待发送的文件名后缀：230-235 表示从230章到235章
    """
    suf = ""
    if start == end:
        suf = str(start)
    else:
        suf = str(start) + "-" + str(end)
    return suf


def is_chi(text):
    """判断是否为中文"""
    return all('\u4e00' <= char <= '\u9fff' for char in text)


def wash_novel_list(lists, logging):
    l = []
    mx = 0
    mi = 1000000
    logging.info(">" * 5 + "正在处理章节信息" + "<" * 5)
    newcircle = False
    numOfChapterOne = 0
    ERROR_RANGE = 10
    # ERROR_PROBABILITY=0.85
    logging.info("待处理章节数%d" % len(lists))
    if len(lists) == 1:
        num = getNumOfTitle(lists[0][1])
        mx = num
        mi = num
    else:
        for item in lists:
            try:
                chapter = item[1]
                # print("wash "+chapter)
                num = getNumOfTitle(chapter)
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
                logging.error(e)
    logging.debug("max:%d min:%d" % (mx, mi))
    return l, mi, mx


def __chinese(self, chapter):
    """
    中文标题:如第一百章
    :param chapter:
    :return:
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


def __digit(chapterTitle):
    """
    数字标题:如第100章
    """
    num = -1
    pattern_d = re.compile(r'第\d+章')
    cha = pattern_d.search(chapterTitle)
    if cha:
        rs = cha.group()[1:-1]
        if len(str(rs)) >= 1:
            num = int(rs)
    return num


def getNumOfTitle(chapter):
    """
    获得章节编号
    """
    num = -1
    # 若全数字
    pattern_d = re.compile(r'第\d+章')
    cha = pattern_d.search(chapter)
    if cha:
        num = __digit(chapter)
    # 若其他
    else:
        num = __chinese(chapter)
    return num
