import os
import random
from celery import states
from celery.exceptions import Ignore

from worker import celery_app

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


def set_file_name_by_speed(speed):
    file_name = "normal.log"
    if speed < 40:
        file_name = "slow.log"
    elif 140 <= speed:
        file_name = "fast.log"
    return file_name


def get_train_speed():
    return round(random.uniform(0, 180), 1)


def get_near_station():
    return random.choice(STATIONS)


@celery_app.task(bind=True, name='post_train_speed', queue='train_beat')
def post_train_speed(self):
    train_speed = get_train_speed()

    try:
        file_name = set_file_name_by_speed(train_speed)
        with open(os.path.join(os.environ['LOG_FILES_PATH'], file_name), "a") as file:
            file.write(str(train_speed)+"\n")
            file.close()
        return train_speed

    except Exception as e:
        raise TaskFailure(self, e)


@celery_app.task(bind=True, name='post_train_near_station', queue='train_beat')
def post_train_near_station(self):
    station = get_near_station()
    return station


class TaskFailure(Exception):
    def __init__(self, task, exception):
        task.update_state(
            state=states.FAILURE,
            meta={
                'exc_message': (type(exception).__name__, ),
                'custom': '', 'exc_type': '',
            })
        raise Ignore()
