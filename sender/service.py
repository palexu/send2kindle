# coding=utf-8
from __future__ import unicode_literals
from engine.novelEngine import NovelEngine


def run():
    ne = NovelEngine()
    ne.get_updates()
