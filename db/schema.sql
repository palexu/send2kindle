CREATE TABLE readed(
			bookid INTEGER PRIMARY KEY AUTOINCREMENT,
			bookname char(50),
			at char(100)
			)
CREATE TABLE chapters(
			chaTitle char(100) PRIMARY KEY,
			bookname char(50),
			chaContent TEXT,
			FOREIGN KEY(bookname) REFERENCES readed(novelname)
			)
-- 任务日志
CREATE TABLE task_log(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      biz_no varchar(64) DEFAULT NULL ,
      content TEXT DEFAULT "",
      gmt_create datetime DEFAULT NULL
      )
-- 每次发送的任务情况
CREATE TABLE send_task(
      id INTEGER  PRIMARY KEY AUTOINCREMENT,
      biz_no varchar(64) DEFAULT NULL ,
      start datetime DEFAULT NULL,
      `end` datetime DEFAULT NULL,
      `status` int DEFAULT 0
)