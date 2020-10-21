import logging
import random
import os

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


def set_logger(name: str) -> logging:
    logger = logging.getLogger(name)
    fh = logging.FileHandler(os.path.join(os.environ['LOG_FILES_PATH'], name + '.log'))
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def set_file_name_by_speed(speed: float) -> str:
    speed_limit_slow = 40
    speed_limit_normal = 140

    file_name = "normal.log"
    if speed < speed_limit_slow:
        file_name = "slow.log"
    elif speed_limit_normal <= speed:
        file_name = "fast.log"
    return file_name


def get_train_speed() -> float:
    return round(random.uniform(0, 180), 1)


def get_near_station() -> str:
    return random.choice(STATIONS)
