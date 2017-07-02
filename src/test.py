# coding=utf-8
import unittest
import os
import logging
import Kmail
import sql
import Novel
import unittest.mock as mock

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    )


@unittest.skipIf(True, "only test when email cant run")
class Send2KindleTest(unittest.TestCase):
    def testSend(self):
        return
        logging.info("test send")

        newf = "奇怪.txt"
        newfc = "你真！！！"

        f = open(newf, "w")
        f.write(newfc)
        f.close()
        mail = Kmail.Mail()
        mail.set_receiver("1098672878@qq.com")
        mail.send2kindle([newf, ])

        os.remove(newf)

    def test126(self):
        # return
        logging.info("test send")

        newf = "奇怪.txt"
        newfc = "你真！！！"

        f = open(newf, "w")
        f.write(newfc)
        f.close()
        mail = Kmail.Mail()
        mail.set_receiver("1098672878@qq.com")
        mail.init_host_config("126")
        mail.send2kindle([newf, ])

        os.remove(newf)

    def test163(self):
        return
        logging.info("test send")

        newf = "奇怪.txt"
        newfc = "你真！！！"

        f = open(newf, "w")
        f.write(newfc)
        f.close()
        mail = Kmail.Mail()
        mail.set_receiver("1098672878@qq.com")
        mail.init_host_config("163")
        mail.send2kindle([newf, ])

        os.remove(newf)


class ScrapyTest(unittest.TestCase):
    @mock.patch('Kmail.Mail')
    def testScrapy(self, mock_Mail):
        settings = [
            ["http://www.shumilou.co/zhongshengzhishenjixueba", 0],
            ["http://www.shumilou.co/xiuzhensiwannian", 0],
            ["http://www.shumilou.co/zoujinxiuxian", 0],
        ]
        sql.setAtChapter("重生之神级学霸", "第1085章 优势")
        sql.setAtChapter("走进修仙", "第一百五十七章 问题")
        sql.setAtChapter("修真四万年", "第1697章 召唤，降临！")
        sql.test_delChapter()

        service = Novel.Service()
        service.mail = mock_Mail()
        service.mail.set_receiver("1098672878@qq.com")
        service.mail.init_host_config('163')

        for link in settings:
            service.add_novel(link)
        service.all_novels_latest_updates_2_kindle()


class SpiderTest(unittest.TestCase):
    def testGetOneCha(self):
        pass
        # spider = novel.Spider()
        # spider.get_one_chapter("http://www.shumilou.co/zhongshengzhishenjixueba/zhongshengzhishenjixueba/6933214.html")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
