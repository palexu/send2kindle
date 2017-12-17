# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from util import config
from sender.dal import *
from sender.novel.model import BookConfig


def add_novel(book_name, read_at):
    r = ReadedDao()
    r.add_novel(book_name, at=read_at)


if __name__ == '__main__':
    book_configs = []
    for book in books():
        bc = BookConfig(book)
        book_configs.append(bc)

    print("当前已配置的小说如下:")
    for i in book_configs:
        print(i)

    y = input("""
    添加新的小说? yN
    """)

# add_novel("惊悚乐园", "第1293章 至黑之夜 1")
