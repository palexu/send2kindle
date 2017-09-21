FROM python:3.5
RUN rm /etc/apt/sources.list && touch /etc/apt/sources.list && echo 'deb http://mirrors.aliyun.com/debian wheezy main contrib non-free' >> /etc/apt/sources.list && echo 'deb-src http://mirrors.aliyun.com/debian wheezy main contrib non-free' >> /etc/apt/sources.list && echo 'deb http://mirrors.aliyun.com/debian wheezy-updates main contrib non-free' >> /etc/apt/sources.list && echo 'deb-src http://mirrors.aliyun.com/debian wheezy-updates main contrib non-free' >> /etc/apt/sources.list && echo 'deb http://mirrors.aliyun.com/debian-security wheezy/updates main contrib non-free' >> /etc/apt/sources.list && echo 'deb-src http://mirrors.aliyun.com/debian-security wheezy/updates main contrib non-free' >> /etc/apt/sources.list
RUN mkdir ~/.pip && touch ~/.pip/pip.conf && echo '[global]' >> ~/.pip/pip.conf && echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.pip/pip.conf
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/send2kindle
CMD /usr/local/bin/python Schedule.py
