import errno
import os
import random
from time import sleep
from celery.result import AsyncResult

from worker import celery_app
from tasks import post_train_speed, post_train_near_station


class TestRawOperations:
    def test_post_train_speed(self):
        try:
            os.makedirs(os.environ['LOG_FILES_PATH'])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        train_speed = 30.00  # round(random.uniform(0, 180), 2)
        result = post_train_speed(train_speed)
        print(result)
        assert result == train_speed


class TestCeleryOperations:
    def test_celery_post_train_speed(self):
        train_speed = 30.00  # round(random.uniform(0, 180), 2)
        task = celery_app.send_task('post_train_speed', args=[train_speed])
        result = AsyncResult(task.task_id, app=celery_app).get()
        while task.status == 'PENDING':
            sleep(0.1)
        print(result)
        assert task.status == 'SUCCESS'
        assert result == train_speed
