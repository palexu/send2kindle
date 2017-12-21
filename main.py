# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sender.service import run

if __name__ == '__main__':
    # run()
    from sender.util.config import *
    mail_config = mail()
    mail_config["receiver2"]="hhh"
    print(mail_config)

    write_mail(mail_config)
