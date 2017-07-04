FROM python:3.5

WORKDIR /app

COPY requirements.txt ./
COPY run.sh ./
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod 777 ./run.sh

CMD /app/run.sh
