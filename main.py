# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sender.engine import novelEngine


def run():
    s = novelEngine.NovelEngine()
    s.all_novels_latest_updates_2_kindle()


if __name__ == '__main__':
    run()
    pass
    from util import kmail

    m = kmail.Mail()
    print(m.mail_config)

    with open("test/m90.mobi", "rb") as f:
        m.send2kindle("m90.mobi", f.read())
