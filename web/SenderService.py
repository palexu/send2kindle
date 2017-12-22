# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import jsonify

from sender.service import run
from . import app


@app.route('/sender/push/novel')
def push_all_novel():
    run()
    return jsonify({
        "isSuccess": True
    })


@app.route('/sender/<biz_no>/info')
def runtime_info(biz_no):
    return "runtime info"


@app.route('/sender/info')
def info():
    """
    总信息，包括
    一共启动多少次，
    一共爬取多少次
    一共推送过多少次
    一共推送过多少书籍
    一共推送过多少章节

    :return:
    """
    return "info"
