FROM python:3.5

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src
CMD [ "python", "main.py" ]
