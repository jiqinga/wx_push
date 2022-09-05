FROM python:3.6-alpine
ENV ENV="/etc/profile"
ENV  TIME_ZONE Asia/Shanghai
COPY src /src
COPY pip.conf  /root/.pip/pip.conf
WORKDIR /src
RUN set -ex && sed -i 's/dl-cdn.alpinelinux.org\/alpine\/v3.15/mirrors.tuna.tsinghua.edu.cn\/alpine\/v3.15/g' /etc/apk/repositories && \
    apk update && apk add --no-cache tzdata gcc g++ && \
    pip3 install --no-cache-dir -r requirements.txt && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo ${TIME_ZONE} > /etc/timezone && cd /root && \
    echo "export PS1='\[\033[01;32m\]\u@\[\033[01;35m\]\h\[\033[01;33m\] \W\[\033[01;34m\]\:\[\033[00m\]\# \'" >>/etc/profile && \
    rm -rf /root/.cache /var/cache/apk/* /tmp/*
ENTRYPOINT ["python3", "bot.py"]
