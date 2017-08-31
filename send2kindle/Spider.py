# coding=utf-8
from bs4 import BeautifulSoup
import requests
import traceback
import logging
import logging.config
import re
from send2kindle import NovelHandler

logging.config.fileConfig("../config/logging.conf")


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
        self.book_name_chi = None

    def check_is_dumplicate(self, set, obj):
        size_before = len(set)
        set.add(obj)
        if size_before == len(set):
            return False
        else:
            return True

    def get_book_name_chi(self, index_page):
        return index_page.find("div", {"id": "info"}).h1.get_text()

    def get_all_chapter_links(self, pageUrl):
        """
        根据小说目录链接，获得所有章节页面的链接
        :param pageUrl: 小说的目录链接
        :return: list[(str)link]
        """
        logging.info("正在访问小说目录链接:%s" % pageUrl)
        html = self.session.get(pageUrl, headers=self.headers).text.encode("ISO-8859-1").decode("utf8")
        bsObj = BeautifulSoup(html, "html.parser")

        self.book_name_chi = self.get_book_name_chi(bsObj)
        logging.debug("book name is %s" % self.book_name_chi)

        novelList = bsObj.findAll("dd")
        linksList = []
        is_dumplicate_set = set()
        regx = r'\.html'
        pattern = re.compile(regx)

        # 适配biqudao的特殊页面，开头有12个最新章节
        novelList = novelList[12:]

        for novel in novelList:
            try:
                link = novel.a['href']
                name = novel.get_text()
                match = pattern.search(link)
                if match and self.check_is_dumplicate(is_dumplicate_set, link):
                    l = [NovelHandler.BiqugeHandler.get_base_url() + link, name]
                    linksList.append(l)
            except Exception as e:
                print("get_all_chapter_links:error  " + str(e))
                pass
        linksList = linksList[:-1]
        # logging.debug(linksList)
        return linksList

    def get_one_chapter(self, link):
        """
        通过提供的章节页面获得其正文
        :param link:指定章节的链接
        :return:(str)novel
        """
        # 获取内容
        html = self.session.get(link, headers=self.headers).text.encode("ISO-8859-1").decode("utf8")
        bs_obj = BeautifulSoup(html, "html.parser")

        # 读取信息
        content = self.get_content_from_page(bs_obj)
        title = self.get_title_from_page(bs_obj)

        # 格式化并返回
        return self.format_chapter(title, content)

    def get_content_from_page(self, bs_obj):
        """
        从页面中获取文章内容
        :param bs_obj:
        :return: str 文章内容
        """
        content = bs_obj.find("div", {"id": "content"}).get_text()
        return self.format_content(content)

    def get_title_from_page(self, bsObj):
        """
        从页面中获取标题
        :param bsObj:
        :return: str 标题
        """
        return bsObj.find("div", {"class": "bookname"}).h1.get_text()

    def gbk_2_utf8(self, gbk_str):
        # unicode = str(gbk_str).decode("gbk")
        # utf8 = unicode.encode("utf-8")
        s = gbk_str.encode("gbk")
        return s

    @staticmethod
    def format_chapter(title, content):
        """
        格式化每一章的显示内容
        :param title: 章节标题
        :return: str 完整的章节内容
        """
        novel = "\n>>>" + title + "<<<\n"
        novel = novel + content
        # logging.debug(novel)
        return novel

    def format_content(self, content):
        """
        格式化文章内容
        :param content:
        :return:
        """
        return content.strip().replace("  ", "\n")

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
                content = self.get_one_chapter(url)
                self.save_2_file(filename, content)
                # time.sleep(500)
            except Exception as e:
                traceback.print_exc()

    def save_2_file(self, filename, content):
        try:
            filename = filename
            f = open(filename, 'at', encoding="utf-8")
            f.write(content)
            f.close()
        except Exception as e:
            traceback.print_exc()
