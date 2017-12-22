# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, jsonify
from sender.dal.service import MailConfigService

from . import app


@app.route('/test')
def test():
    return "test..."


@app.route('/api/mail/update', methods=['post'])
def update_mail():
    mail_config = request.get_json()
    MailConfigService.write_mail(mail_config)
    return jsonify({
        "isSuccess": True
    })


@app.route('/api/mail')
def read_mail():
    mail_config = MailConfigService.read_mail()
    print(mail_config)
    return jsonify(mail_config)
