# python-crawler
a simple python crawler that use celery for parallel running 

docker-compose build && docker-compose up;docker exec -it crawler_workers_1 bash ;source env/bin/activate;cd .. ;python -m crawler.run_tasks