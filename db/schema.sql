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