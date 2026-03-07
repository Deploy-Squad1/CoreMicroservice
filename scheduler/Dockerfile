FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    cron \
    curl \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY scheduler/crontab /etc/cron.d/scheduler-cron
RUN chmod 0644 /etc/cron.d/scheduler-cron
RUN crontab /etc/cron.d/scheduler-cron

COPY scheduler/start-cron.sh /start-cron.sh
RUN chmod +x /start-cron.sh

CMD ["/start-cron.sh"]
