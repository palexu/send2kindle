# send2kindle
用于获取小说并推送到kindle。

## TODO

- 完成通知功能
- web 管理界面

## 配置
- config/config.yaml 目前只支持[笔趣岛](http://www.biqudao.com)，将指定小说的目录页添加到配置中即可

## 运行方式：
推荐使用docker运行

首先cd到代码根目录下，然后构建一个镜像
`
  docker build -t send2kindle .
`


将下面的 /root/app 替换为本项目所在的路径

`
  docker run -d -v 你的代码路径:/app send2kindle
`