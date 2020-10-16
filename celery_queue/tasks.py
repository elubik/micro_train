from tempfile import NamedTemporaryFile
from celery.exceptions import Ignore
from celery import Celery, states
from kombu import Queue
from zipfile import ZipFile
import requests
import imghdr
import os

TIMEOUT = 5
FORBIDDEN_TAGS = ["script", "style", "table", "a", "img", "button", "header", "footer", "nav"]

CELERY_BROKER = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
celery_app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER)

celery_app.conf.result_backend = CELERY_RESULT_BACKEND
celery_app.conf.timezone = "UTC"
celery_app.conf.worker_redirect_stdouts = True
celery_app.conf.worker_hijack_root_logger = False
celery_app.conf.task_queues = (
    Queue("train_beat"),
    Queue("train_default")
)
celery_app.conf.task_default_queue = "train_default"


def set_file_name_by_speed(speed):
    file_name = "normal.log"
    if speed < 40:
        file_name = "slow.log"
    elif 140 <= speed:
        file_name = "fast.log"
    return file_name


def log_train_speed(train_speed):
    file_name = set_file_name_by_speed(train_speed)
    file = open(file_name, 'a')
    file.write(train_speed)
    file.close()


def post_train_near_station(station):
    return station


# @celery_app.task(bind=True)
# def log_train_speed(self, train_speed):
#     try:
#         return train_speed
#
#     except Exception as e:
#         raise TaskFailure(self, e)
#
#
# @celery_app.task(bind=True)
# def post_train_near_station(self, station):
#     try:
#         return station
#
#     except Exception as e:
#         raise TaskFailure(self, e)
#
#
# def get_url_domain(url):
#     return '/'.join(url.split('/')[:3])
#
#
# def fix_relative_urls(urls, domain):
#     return [*map(lambda url: domain + url if url[0] == '/' else url, urls)]
#
#
# def add_image_to_zip_object(img_bytes, filename, zip_object,):
#     with NamedTemporaryFile() as img_file:
#         img_file.write(img_bytes)
#         img_type = imghdr.what(img_file.name)
#         if img_type:
#             zip_object.write(img_file.name, f'{filename}.{img_type}')
#
#
# class TaskFailure(Exception):
#     def __init__(self, task, exception):
#         task.update_state(
#             state=states.FAILURE,
#             meta={
#                 'exc_message': (type(exception).__name__, ),
#                 'custom': '', 'exc_type': '',
#             })
#         raise Ignore()
