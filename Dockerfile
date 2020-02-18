FROM python:3.7.4

RUN set -x \
  && echo "Preparing system..." \
  && useradd -ms /bin/bash -d /app app \
  && apt-get -y update \
  && apt-get -y install \
    cron \
    sudo

ADD requirements.txt /app/requirements.txt
RUN set -x \
  && echo "Installing python dependencies..." \
  && pip install -r /app/requirements.txt \
  && rm /app/requirements.txt

ENV CRON=
ENV FORCE_CRON=
ENV MARATHON_URL=
ENV MARATHON_USERNAME=
ENV MARATHON_PASSWORD=
ADD .env.example /app/.env.example

ADD entrypoint.sh /app/entrypoint.in.sh
RUN set -x \
  && bash -c 'cat <(echo "#!/bin/bash") <(cat /app/entrypoint.in.sh) > /app/entrypoint.sh' \
  && chmod +x /app/entrypoint.sh \
  && rm /app/entrypoint.in.sh

ADD healthcheck.py /app/healthcheck.in.py
RUN set -x \
  && bash -c 'cat <(echo "#!/usr/local/bin/python") <(cat /app/healthcheck.in.py) > /app/healthcheck.py' \
  && chmod +x /app/healthcheck.py \
  && rm /app/healthcheck.in.py

ENTRYPOINT [ "/app/entrypoint.sh" ]
