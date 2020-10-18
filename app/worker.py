from celery import Celery, states
from kombu import Queue
from datetime import timedelta
import os

celery_app = Celery(broker=os.environ['CELERY_BROKER_URL'], include=('tasks',))

celery_app.conf.result_backend = os.environ['CELERY_RESULT_BACKEND']
celery_app.conf.timezone = "UTC"
celery_app.conf.worker_redirect_stdouts = True
celery_app.conf.worker_hijack_root_logger = False
celery_app.conf.task_queues = (
    Queue("train_beat"),
    Queue("train_default")
)
celery_app.conf.task_routes = {
    "post_train_speed": {
        "queue": "train_beat",
    },
    "post_train_near_station": {
        "queue": "train_beat",
    },
}
celery_app.conf.beat_schedule = {
    "post-train-speed-every-10-seconds": {
        "task": "post_train_speed",
        "schedule": timedelta(seconds=int(os.environ['TRAIN_SPEED_SCHEDULE'])),
        "args": [],  # [round(random.uniform(0, 180), 1)],
        "options": {
            "queue": "train_beat"
        }
    },
    "post-train-speed-every-180-seconds": {
        "task": "post_train_near_station",
        "schedule": timedelta(seconds=int(os.environ['STATIONS_SCHEDULE'])),
        "args": [],  # [random.choice(STATIONS)],
        "options": {
            "queue": "train_beat"
        }
    }
}
celery_app.conf.task_default_queue = "train_default"
