# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sender.engine import novelEngine


def run():
    s = novelEngine.NovelEngine()
    s.push_updates()


if __name__ == '__main__':
    run()
