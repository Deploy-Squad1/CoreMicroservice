FROM debian:trixie

RUN apt update \
 && apt install -y --no-install-recommends \
    cron \
    curl \
 && rm -rf /var/lib/apt/lists/*

COPY crontab /etc/cron.d/scheduler-cron
RUN chmod 0644 /etc/cron.d/scheduler-cron
RUN crontab /etc/cron.d/scheduler-cron

COPY start-cron.sh /start-cron.sh
RUN chmod 0755 /start-cron.sh

CMD ["/start-cron.sh"]
