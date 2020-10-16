FROM python:3.6.8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY . /
WORKDIR /app

# COPY . /celery_train
# WORKDIR /celery_train
#
# RUN pip install -r requirements.txt
#
# CMD ["celery", "-A", "tasks", "beat", "--loglevel=info"]
# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
