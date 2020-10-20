import errno
import os
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

        result = post_train_speed()
        print(result)
        assert result

    def test_post_train_near_station(self):
        result = post_train_near_station()
        print(result)
        assert result


class TestCeleryOperations:
    def test_celery_post_train_speed(self):
        task = celery_app.send_task('post_train_speed', args=[])
        result = AsyncResult(task.task_id, app=celery_app).get()
        while task.status == 'PENDING':
            sleep(0.1)
        print(result)
        assert task.status == 'SUCCESS'

    def test_celery_post_train_near_station(self):
        task = celery_app.send_task('post_train_near_station', args=[])
        result = AsyncResult(task.task_id, app=celery_app).get()
        while task.status == 'PENDING':
            sleep(0.1)
        print(result)
        assert task.status == 'SUCCESS'
