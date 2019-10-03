FROM ubuntu:18.04


RUN \
apt-get update -qq && \
apt-get install -y \
build-essential \
apt-utils &&\
apt-get install -y \
curl \
sudo \
wget \
unzip

RUN \
apt-get install -y \
python3.7 python3 python3-pip firefox &&\
pip3 --no-cache-dir install virtualenv --upgrade && \
pip3 install gevent && \
rm -rf /var/lib/apt/lists/*

#COPY ./geckodriver /usr/local/bin
RUN wget -qO- https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz | tar xvz -C /usr/local/bin


WORKDIR /home/crawler







