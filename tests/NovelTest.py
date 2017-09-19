# coding=utf-8
import unittest
import os
import sys

sys.path.append("../")
from send2kindle.util import Kmail


@unittest.skipIf(True, "only tests when email cant run")
class MailTest(unittest.TestCase):
    def testSend(self):
        return

        newf = "奇怪.txt"
        newfc = "你真！！！"

        f = open(newf, "w")
        f.write(newfc)
        f.close()
        mail = Kmail.Mail()
        mail.set_receiver("1098672878@qq.com")
        mail.send2kindle([newf, ])

        os.remove(newf)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
