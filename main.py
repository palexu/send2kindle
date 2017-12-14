# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sender.Novel as Novel
from util import config


def run():
    settings = config.settings
    service = Novel.Service(settings)
    service.all_novels_latest_updates_2_kindle()


def hello():
    print("hello world")


if __name__ == '__main__':
    run()