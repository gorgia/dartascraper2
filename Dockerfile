FROM python:3
LABEL Maintainer="gorgia@fastwebnet.it"

WORKDIR /usr/app/src

COPY requirements.txt ./

#RUN apt-get update && apt-get install -y cron
#RUN apk --update add --no-cache g++

RUN apt-get update && apt-get install -y cron \
    && pip3 install --upgrade pip  \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY cronjob /etc/crontab

RUN ["chmod", "+x", "/usr/app/src/loop.sh"]

#ENTRYPOINT ["/usr/sbin/cron", "-f"]
ENTRYPOINT ["/usr/app/src/loop.sh"]