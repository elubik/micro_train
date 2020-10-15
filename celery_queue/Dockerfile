FROM python

COPY . /celery_queue
WORKDIR /celery_queue

RUN pip install -r requirements.txt

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
