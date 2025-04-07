FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# cron 설치 + crontab 설정
RUN apt-get update && apt-get install -y cron \
 && echo "*/2 * * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/monitor-cron \
 && chmod 0644 /etc/cron.d/monitor-cron \
 && crontab /etc/cron.d/monitor-cron

CMD ["cron", "-f"]
