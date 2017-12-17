# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apscheduler.schedulers.blocking import BlockingScheduler
import main


def run():
    sched = BlockingScheduler()
    sched.add_job(main.run, "cron", hour="7,11,17")

    try:
        sched.start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
