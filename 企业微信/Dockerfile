FROM python:3.6-alpine
ENV ENV="/etc/profile"
ENV TIME_ZONE Asia/Shanghai
COPY pip.conf  /root/.pip/pip.conf
COPY py.cron /var/spool/cron/crontabs/root
WORKDIR /src
RUN set -ex && sed -i 's/dl-cdn.alpinelinux.org\/alpine\/v3.15/mirrors.tuna.tsinghua.edu.cn\/alpine\/v3.15/g' /etc/apk/repositories && \
    apk update && apk add --no-cache tzdata gcc g++ git && \
    git clone https://hub.njuu.cf/jiqinga/wx_push.git /tmp/qywx && \
    mv /tmp/qywx/企业微信/src /src && rm -rf  /tmp/qywx && \
    pip3 install --no-cache-dir -r requirements.txt && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo ${TIME_ZONE} > /etc/timezone && cd /root && \
    echo "export PS1='\[\033[01;32m\]\u@\[\033[01;35m\]\h\[\033[01;33m\] \W\[\033[01;34m\]\:\[\033[00m\]\# \'" >>/etc/profile && \
    rm -rf /root/.cache /var/cache/apk/* /tmp/*
ENTRYPOINT ["python3", "bot.py"]
