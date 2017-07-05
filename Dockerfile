FROM python:3.5
RUN apt-get update && apt-get install -y cron
WORKDIR /app

COPY requirements.txt ./
COPY run.sh ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod 777 ./run.sh

#add crontab
COPY crontab /var/spool/cron/crontabs/root
RUN chown -R root:crontab /var/spool/cron/crontabs/root && chmod 600 /var/spool/cron/crontabs/root
RUN touch /var/log/cron.log

CMD /app/cmd.sh
