import os
import random
from celery import Celery

STATIONS = [
    "Warszawa Zachodnia",
    "Warszawa Włochy",
    "Warszawa Ursus",
    "Warszawa Gołąbki",
    "Ożarów Mazowiecki",
    "Płochocin",
    "Błonie",
    "Witanów",
    "Boża Wola",
    "Seroki",
    "Teresin Niepokalanów",
    "Piasecznica",
    "Sochaczew",
    "Kornelin",
    "Nowa Sucha",
    "Kęszyce",
    "Jasionna",
    "Bednary",
    "Mysłaków",
    "Arkadia",
    "Łowicz Główny"
]

CELERY_BROKER = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
# CELERY_ALWAYS_EAGER = False
celery_app = Celery('tasks', backend=CELERY_BACKEND, broker=CELERY_BROKER)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    train_speed = round(random.uniform(0, 180), 2)
    sender.add_periodic_task(10, post_train_speed.s(train_speed), name='post train speed every 10 seconds')
    station = random.choice(STATIONS)
    sender.add_periodic_task(180, post_train_near_station.s(station), name='post train speed every 180 seconds')


@celery_app.task
def post_train_speed(train_speed):
    return train_speed


@celery_app.task
def post_train_near_station(station):
    return station


# @celery.task(name='tasks.add')
# def beat_speed():
#     train_speed = round(random.uniform(0, 180), 2)
#     task = celery_app.send_task('tasks.post_train_speed', args=[train_speed])
#
#
# @celery.task(name='tasks.add')
# def beat_station():
#     station = random.choice(STATIONS)
#     task = celery_app.send_task('tasks.post_train_near_station', args=[station])
