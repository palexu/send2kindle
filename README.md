#send2kindle
用于获取小说并推送到kindle
author:palexu

运行方式：
本地运行，启动一下，然后更新kindle
后期考虑docker化，数据库使用mysql
cd /path/send2kindle
docker build -t send2kindle .
//docker run -i -t -v ~/code/python/spider/send2kindle:/app send2kindle:latest
docker run -i -t -v /path/send2kindle:/app send2kindle:latest
