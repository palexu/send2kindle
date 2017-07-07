FROM python:3.5
RUN apt-get update && apt-get install -y cron
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#add crontab
COPY crontab /var/spool/cron/crontabs/root
RUN chown -R root:crontab /var/spool/cron/crontabs/root && chmod 600 /var/spool/cron/crontabs/root
RUN touch /var/log/cron.log

COPY run_send2kindle.sh ./
RUN chmod 755 run_send2kindle.sh

CMD /app/run_send2kindle.sh
