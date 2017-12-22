# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from sender.service import run


def run_background():
    sched = BackgroundScheduler()
    sched.add_job(run, "cron", hour="7,11,17")

    try:
        sched.start()
    except KeyboardInterrupt:
        pass


def run_blocking():
    sched = BlockingScheduler()
    sched.add_job(run, "cron", hour="7,11,17")

    try:
        sched.start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run_blocking()
