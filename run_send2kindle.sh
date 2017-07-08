#!/bin/bash
#while in docker, do follow things
cd /app/send2kindle/src &&
/usr/local/bin/python main.py &&
rm *.txt
