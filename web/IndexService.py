# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import send_from_directory
from . import app


@app.route('/test')
def test():
    return "test..."


@app.route('/')
def index():
    return send_from_directory('templates', "index.html")
