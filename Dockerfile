FROM postgres:12.2

RUN apt-get update && apt-get install -y \
    cron \
    rsyslog \
    postgresql-client \
    ca-certificates

CMD mkdir /dumps

VOLUME /etc/cron.d
VOLUME /dumps

CMD service rsyslog start && service cron start && tail -f /var/log/syslog
