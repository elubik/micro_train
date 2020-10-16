import random
from datetime import timedelta

from celery_queue.tasks import celery_app

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

CELERY_BEAT_SCHEDULE = {
    "post-train-speed-every-10-seconds": {
        "task": "celery_queue.tasks.log_train_speed",
        "schedule": timedelta(seconds=10),
        "args": [round(random.uniform(0, 180), 2)],
        "options": {
            "queue": "train_beat"
        }
    },
    "post-train-speed-every-180-seconds": {
        "task": "celery_queue.tasks.post_train_near_station",
        "schedule": timedelta(seconds=180),
        "args": [random.choice(STATIONS)],
        "options": {
            "queue": "train_beat"
        }
    }
}

celery_app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
celery_app.conf.task_routes["celery_queue.tasks.log_train_speed"] = {"queue": "train_beat"}
celery_app.conf.task_routes["celery_queue.tasks.post_train_near_station"] = {"queue": "train_beat"}
