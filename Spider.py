from bs4 import BeautifulSoup
import requests
import traceback
import logging
import logging.config
import re

logging.config.fileConfig("logging.conf")

class Spider:
    """
    爬取小说内容
    """

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def getAllChapterLinks(self, pageUrl):
        """
        根据小说目录链接，获得所有章节页面的链接
        :param pageUrl: 小说的目录链接
        :return: list[(str)link]
        """
        logging.info("正在访问小说目录链接:%s" % pageUrl)
        html = self.session.get(pageUrl, headers=self.headers)
        bsObj = BeautifulSoup(html.text, "html.parser")

        novelList = bsObj.findAll("li")
        linksList = []
        regx = pageUrl.replace("http://www.shumilou.co", "")
        pattern = re.compile(regx)
        for novel in novelList:
            try:
                link = novel.a['href']
                name = novel.get_text()
                match = pattern.search(link)
                if match:
                    # print(link)
                    l = ["http://www.shumilou.co" + link, name]
                    linksList.append(l)
            except Exception as e:
                # print("getAllChapterLinks:error  "+str(e))
                pass
        linksList = linksList[:-1]
        return linksList

    def getNovelName_chi(self, pageUrl):
        html = self.session.get(pageUrl, headers=self.headers)
        bsObj = BeautifulSoup(html.text, "html.parser")
        name = bsObj.find("div", {"class": "tit"}).b.get_text()
        return name

    def getNovelName_en(self, pageUrl):
        '''
        >>> getNovelName_en("http://www.shumilou.co/test")
        'test'
        '''
        name = pageUrl.replace("http://www.shumilou.co/", "")
        return name

    def getOneChapter(self, link):
        """
        通过提供的章节页面获得其正文
        :param link:指定章节的链接
        :return:(str)novel
        """
        pattern = re.compile(r'shumilou')

        html = self.session.get(link, headers=self.headers)
        bsObj = BeautifulSoup(html.text, "html.parser")

        content = bsObj.findAll("p")
        title = bsObj.find("div", {"class": "title"}).h2.get_text()
        novel = "\n>>>" + title + "<<<\n"

        for p in content:
            match = pattern.search(p.get_text())
            if match:
                pass
            else:
                novel = novel + p.get_text()

        novel = novel + "\n\n"
        return novel

    def download(self, links, filename):
        """
        根据抓取links中的所有章节
        :param links:待抓取的章节链接
        :param filename:以该文件名保存小说
        :return:无
        """
        for link in links:
            try:
                url = link[0]
                logging.info("download:%s" % link[1])
                content = self.getOneChapter(url)
                self.__save2file(filename, content)
                # time.sleep(500)
            except Exception as e:
                traceback.print_exc()

    def __save2file(self, filename, content):
        try:
            filename = filename
            f = open(filename, 'at', encoding="utf-8")
            f.write(content)
            f.close()
        except Exception as e:
            traceback.print_exc()
