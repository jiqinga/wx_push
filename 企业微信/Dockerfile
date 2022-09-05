FROM python:3.6-alpine
COPY src /src
COPY pip.conf  /root/.pip/pip.conf
WORKDIR /src
RUN set -ex && sed -i 's/dl-cdn.alpinelinux.org\/alpine\/v3.15/mirrors.tuna.tsinghua.edu.cn\/alpine\/v3.15/g' /etc/apk/repositories && \
    apk update && apk add --no-cache gcc g++ && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache /var/cache/apk/* /tmp/*
ENTRYPOINT ["python3", "bot.py"]
