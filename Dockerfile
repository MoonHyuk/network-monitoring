FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

COPY main.py main.py

CMD crond -f