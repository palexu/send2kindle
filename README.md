# send2kindle
用于获取小说并推送到kindle

## 运行方式：
本地运行，启动一下，然后更新kindle

推荐使用docker运行

`
  docker build -t send2kindle .
`


`
  docker run -i -t -v /your/path/send2kindle:/app/send2kindle send2kindle:latest
`
