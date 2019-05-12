FROM python:3.7-alpine

COPY crontab /etc/cron.d/hello-cron
RUN find /etc/cron.d/ -type f -print0 | xargs -0 dos2unix
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

COPY main.py main.py

CMD crond -f