# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests
import logging
import logging.config
import re

from sender import dal
from sender.novel import novel_handler
from sender.novel.model import Book

logging.config.fileConfig("config/logging.conf")


def check_is_dumplicate(set, obj):
    size_before = len(set)
    set.add(obj)
    if size_before == len(set):
        return False
    else:
        return True


def get_book_name_chi(index_page):
    return index_page.find("div", {"id": "info"}).h1.get_text()


class BiqugeSpider:
    """
    爬取小说内容.
    对于单网站的多小说通用
    """

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def get_update(self, bookname, pageUrl, checknum):
        """
        获得最近更新的小说
        :param pageUrl:小说目录链接
        :param checknum:小于该数字的更新数，不发送
        :return:
        """
        book = Book(bookname)
        dataService = dal.DataService(bookname)
        now_at = dataService.now_read_at()

        url_name_pair = self.get_new_chapter(pageUrl, now_at)
        new_chapter_size = len(url_name_pair)

        if new_chapter_size == 0:
            logging.info("无新章节")
            return None

        newest_at = (url_name_pair[-1])[1]

        logging.info("小说标题:%s" % bookname)
        logging.info("当前已读到%s" % now_at)
        logging.info("最新章节为%s" % newest_at)

        if checknum > new_chapter_size:
            logging.info("[暂不发送]:当前小说更新了%d章...[%d/%d]" % new_chapter_size, new_chapter_size, checknum)
            return None

        for title, content in self.download(url_name_pair):
            book.add_section(title, content)

        dataService.now_read_at(newest_at)
        return book

    def get_new_chapter(self, page_url, nowat):
        nowat = nowat.strip()

        all_chapter = self.get_all_chapter_links(page_url)
        url_name_pair = []

        isnew = False
        for url, name in all_chapter:
            name = name.strip()
            # 两个if顺序不能改变，即从当前阅读到的下一章开始添加
            if isnew:
                url_name_pair.append((url, name))
            if name == nowat:
                isnew = True

        return url_name_pair

    def get_all_chapter_links(self, page_url):
        """
        根据小说目录链接，获得所有章节页面的链接
        :param page_url: 小说的目录链接
        :return: list[(str)link]
        """
        logging.info("正在访问小说目录链接:%s" % page_url)
        html = self.session.get(page_url, headers=self.headers).text.encode("ISO-8859-1").decode("utf8")
        bsObj = BeautifulSoup(html, "html.parser")
        linksList = []

        novelList = bsObj.findAll("dd")
        is_dumplicate_set = set()
        pattern = re.compile(r'\.html')

        # 适配biqudao的特殊页面，开头有12个最新章节
        novelList = novelList[12:]

        for novel in novelList:
            try:
                link = novel.a['href']
                name = novel.get_text()
                match = pattern.search(link)
                if match and check_is_dumplicate(is_dumplicate_set, link):
                    linksList.append([novel_handler.BiqugeHandler.get_base_url() + link, name])
            except Exception as e:
                logging.error("get_all_chapter_links:error  " + str(e))
        linksList = linksList[:-1]
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
        return title, content

    def get_content_from_page(self, bs_obj):
        """
        从页面中获取文章内容
        :param bs_obj:
        :return: str 文章内容
        """
        content = bs_obj.find("div", {"id": "content"})

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

    def format_content(self, content):
        """
        格式化文章内容
        :param content:
        :return:
        """
        c = ""
        for text in content.stripped_strings:
            c = c + text + "\n"
        return c

    def download(self, url_name_pair):
        """
        根据抓取links中的所有章节
        :param url_name_pair:待抓取的章节链接
        :param filename:以该文件名保存小说
        :return:无
        """
        for url, name in url_name_pair:
            try:
                logging.info("download:%s" % name)
                yield self.get_one_chapter(url)
            except Exception as e:
                logging.error(e)
