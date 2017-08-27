# send2kindle
用于获取小说并推送到kindle。

## 配置
- config/mail.yaml 将该目录下已有的mail.yaml.bak 去掉.bak后缀，并加入自己邮件的参数即可
- config/config.yaml 目前只支持[笔趣岛](http://www.biqudao.com)，将指定小说的目录页添加到配置中即可

## 运行方式：
本地运行，启动一下，然后更新kindle

推荐使用docker运行

`
  docker build -t send2kindle .
`

将下面的 /root/app 替换为本项目所在的路径

`
  docker run -i -t -v /root/app/send2kindle:/app/send2kindle send2kindle:latest
`

`
  docker run -d -v /root/app/send2kindle:/app/send2kindle send2kindle
`

`
docker build -t send2kindle . && docker run -d -v /root/app/send2kindle:/app/send2kindle send2kindle
`
