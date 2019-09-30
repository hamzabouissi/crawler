FROM ubuntu:18.04


RUN \
apt-get update -qq && \
apt-get install -y \
build-essential \
apt-utils &&\
apt-get install -y \
aptdaemon \
ed git \
libcairo-dev \
libedit-dev \
libapparmor1 \
libpq-dev \
libedit2 \
libssl1.0.0 \
libcurl4-gnutls-dev \
libssl-dev \
curl \
sudo \
wget &&\
apt-get install -y \
libzbar-dev \
imagemagick \
xvfb &&\
rm -rf /var/lib/apt/lists/*


RUN \
apt-get update -qq && \
apt-get install -y \
python3-pip  python3-dev python3.7 libssl-dev firefox &&\
pip3 --no-cache-dir install virtualenv --upgrade && \
pip3 install gevent && \
#easy_install distribute && \
rm -rf /var/lib/apt/lists/*

COPY geckodriver /usr/local/bin/geckodriver

WORKDIR /home/crawler

#RUN chmod +x /home/crawler/geckodriver

#RUN cp /home/crawler/geckodriver /usr/local/bin/geckodriver






