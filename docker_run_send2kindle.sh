#!/bin/bash
echo `date`
echo 'crontab job start....'
docker run -v  /root/app/send2kindle:/app/send2kindle send2kindle:latest
