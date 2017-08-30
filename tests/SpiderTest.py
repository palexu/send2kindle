import unittest
from send2kindle import Sql
from send2kindle import Novel
import unittest.mock as mock


class SpiderTest(unittest.TestCase):
    def testGetOneCha(self):
        pass
        # spider = novel.Spider()
        # spider.get_one_chapter("http://www.shumilou.co/zhongshengzhishenjixueba/zhongshengzhishenjixueba/6933214.html")


class ScrapyTest(unittest.TestCase):
    @mock.patch('Kmail.Mail')
    def testScrapy(self, mock_Mail):
        settings = [
            ["http://www.shumilou.co/zhongshengzhishenjixueba", 0],
            ["http://www.shumilou.co/xiuzhensiwannian", 0],
            ["http://www.shumilou.co/zoujinxiuxian", 0],
        ]
        Sql.set_read_at("重生之神级学霸", "第1085章 优势")
        Sql.set_read_at("走进修仙", "第一百五十七章 问题")
        Sql.set_read_at("修真四万年", "第1697章 召唤，降临！")
        Sql.test_delChapter()

        service = Novel.Service()
        service.mailSender = mock_Mail()
        service.mailSender.set_receiver("1098672878@qq.com")
        service.mailSender.init_host_config('163')

        for link in settings:
            service.add_novel(link)
        service.all_novels_latest_updates_2_kindle()
