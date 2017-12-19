# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import app


@app.route('/init/index')
def init_index():
    """
    初始化界面，主要介绍一下有哪些功能，需要初始化多少时间
    引导去star和提issue
    :return:
    """
    bcs = []
    # for b in books():
    #     bc = BookConfig(b)
    #     bcs.append(bc)
    return ""


@app.route('/init/mail')
def init_mail():
    """
    邮件的初始化
    :return:
    """
    return ""


@app.route('/init/notify')
def init_notify():
    """
    消息推送的初始化
    :return:
    """
    return ""
