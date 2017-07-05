#!/bin/bash
/etc/init.d/cron start 
cd /app/send2kindle/src &&
python3 main.py &&
rm *.txt
