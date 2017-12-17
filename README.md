# send2kindle
用于获取小说并推送到kindle。

## TODO

- 一键初始化
- 简化配置文件
- web 管理界面

## 下载以及安装

### 下载
`git clone https://github.com/palexu/send2kindle`

### 配置
将`config.json.bak`重命名为`config.json`，
打开该文件

添加你需要推送的小说,如：
```
{
      "name": "修真四万年",//小说名，只用于mobi内小说名的显示
      "url": "http://www.biqudao.com/bqge7946",//小说的目录页
      "count": 10//满10条推送
    }
```

配置你个人的smtp邮箱
```
    "mail": {
    "hostconf": {
       "163": {//只是一个标记
        "sender": "你的邮箱@163.com",
        "password": "你的密码",
        "host": "smtp.163.com"//smtp服务器地址
      }
    },
    "receiver": "xxxxxx@kindle.cn", //你的kindle邮箱地址，切记将上面的sender加入到信任列表
    "init_host_config": "163",//上面的key值
    "subject": "",//邮箱主题，留空即可
    "msgcontent": "deliver by send2kindle"
  }
```

经测试，支持126、163邮箱，其他邮箱的话，附件可能会被吞掉


非必填项:配置推送完成后的消息提醒,通过微信公众号serverChan进行消息推送，
详情见[Server酱](https://sc.ftqq.com/3.version)，申请一个key即可
```
  "serverChan": {
    "scKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
```

## 运行方式：
推荐使用docker以及docker-compose的方式运行

安装docker以及docker-compose

运行`docker-compose up -d`

可以通过`docker logs -f s2k`查看系统运行的日志

## 致谢
使用了kindleEar拆离的calibre的mobi、epub电子书生成模块,
使用了serverChan提供的消息推送服务