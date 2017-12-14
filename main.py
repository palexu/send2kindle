# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sender.novel import service
from util import config
from sender import calibre_driver


def run():
    settings = config.settings
    s = service.Service(settings)
    s.all_novels_latest_updates_2_kindle()

if __name__ == '__main__':
    # run()
    print("hello")