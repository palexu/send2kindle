#!/bin/zsh

# # 记录一下开始时间
echo `date` >> $HOME/log &&
# 进入 /Users/hanks/spider 目录
say 'start send to kindle' &&
cd /Users/xj/code/python/py3 &&
# 激活 python 虚拟环境 virtualenv
source bin/activate &&
cd send2kindle &&
# 运行爬虫脚本
echo `date` >>log.log &&
python main.py >>log.log &&
# 运行完成
echo 'finish' >> $HOME/log
