#!/bin/bash
if [ ! -e env ]
then
  virtualenv env --python=python3.7
fi
source env/bin/activate
pip install -r requirements.txt

cd ..

celery -A crawler worker --concurrency=5 --pool=gevent -l info