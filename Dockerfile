# DO NOT RUN PROJECT UNTIL THIS IS EDITED OR REMOVED (04/16/20)
# Take From https://github.com/docker/compose/blob/master/Dockerfile 
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
FROM ubuntu:18.04


RUN apt-get update && apt-get install -y python3 python3-pip \
    build-essential software-properties-common byobu curl git htop man unzip vim wget && \
    cd /tmp && \
    wget http://download.redis.io/redis-stable.tar.gz && \
    tar xvzf redis-stable.tar.gz && \
    cd redis-stable && \
    make && \
    make install && \
    cp -f src/redis-sentinel /usr/local/bin && \
    mkdir -p /etc/redis && mkdir /data && \
    cp -f *.conf /etc/redis && \
    rm -rf /tmp/redis-stable* && \
    sed -i 's/^\(bind .*\)$/# \1/' /etc/redis/redis.conf && \
    sed -i 's/^\(daemonize .*\)$/# \1/' /etc/redis/redis.conf && \
    sed -i 's/^\(dir .*\)$/# \1\ndir \/data/' /etc/redis/redis.conf && \
    sed -i 's/^\(logfile .*\)$/# \1/' /etc/redis/redis.conf

VOLUME /code
WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY . .

EXPOSE 6379


