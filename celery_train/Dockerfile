FROM python:3.6.8

COPY . /celery_train
WORKDIR /celery_train

RUN pip install -r requirements.txt

CMD ["celery", "-A", "tasks", "beat", "--loglevel=info"]
