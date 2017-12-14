#coding=utf-8
import re
from util import cnconvert as cn2

class Title:
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

    def __digit(self, chapterTitle):
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

    def getNumOfTitle(self, chapter):
        """
        获得章节编号
        """
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