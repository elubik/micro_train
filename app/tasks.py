import time
import requests
import logging
import os
import random
from celery import states
from celery.exceptions import Ignore

from worker import celery_app

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5002)

logger = logging.getLogger('stations')
fh = logging.FileHandler(os.path.join(os.environ['LOG_FILES_PATH'], 'stations.log'))
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

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
    station_name = get_near_station()
    logger.info(f'Train is getting to {station_name} station')

    station = requests.get(f'http://{HOST}:{PORT}/{station_name}')
    try:
        # TODO: refactor - put into function
        station = station.json()
        # station['Message'] = station['Message'].json()
        if station['Message'].get('empty'):
            requests.put(f'http://{HOST}:{PORT}/{station_name}', data={'barrier_state': 'down'})
            logger.info(f'Barriers in {station_name} go down')
        elif station['Message'].get('barrier_state') == 'up':
            requests.put(f'http://{HOST}:{PORT}/{station_name}', data={'barrier_state': 'down'})
            logger.info(f'Barriers in {station_name} go down')
        elif station['Message'].get('barrier_state') == 'down':
            logger.warning(f'Barriers in {station_name} already down')

        time.sleep(10)
        requests.put(f'http://{HOST}:{PORT}/{station_name}', data={'barrier_state': 'up'})
        logger.info(f'Barriers in {station_name} go up')
    except Exception as ex:
        raise Exception(f'Sorry, post_train_near_station() crashed during execution.\n{ex}')

    return True


class TaskFailure(Exception):
    def __init__(self, task, exception):
        task.update_state(
            state=states.FAILURE,
            meta={
                'exc_message': (type(exception).__name__, ),
                'custom': '', 'exc_type': '',
            })
        raise Ignore()
