from tempfile import NamedTemporaryFile
from celery.exceptions import Ignore
from celery import Celery, states
from kombu import Queue
from zipfile import ZipFile
import requests
import imghdr
import os
import random

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

celery_app = Celery(include=('tasks',))

celery_app.conf.result_backend = os.environ['CELERY_RESULT_BACKEND']
celery_app.conf.timezone = "UTC"
celery_app.conf.worker_redirect_stdouts = True
celery_app.conf.worker_hijack_root_logger = False
celery_app.conf.task_queues = (
    Queue("train_beat"),
    Queue("train_default")
)
celery_app.conf.beat_schedule = {
    "post-train-speed-every-10-seconds": {
        "task": "post_train_speed",
        "schedule": float(os.environ['TRAIN_SPEED_SCHEDULE']),
        "args": [round(random.uniform(0, 180), 2)],
        "options": {
            "queue": "train_beat"
        }
    },
    "post-train-speed-every-180-seconds": {
        "task": "post_train_near_station",
        "schedule": float(os.environ['STATIONS_SCHEDULE']),
        "args": [random.choice(STATIONS)],
        "options": {
            "queue": "train_beat"
        }
    }
}
celery_app.conf.task_default_queue = "train_default"
