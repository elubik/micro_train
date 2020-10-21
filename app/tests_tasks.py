import errno
import os
from time import sleep
from celery.result import AsyncResult

from worker import celery_app
from tasks import notify_about_train_speed, notify_about_train_near_station, logger
from requests_handler import barrier_get, barrier_post


class TestRawOperations:
    def test_notify_about_train_speed(self):
        try:
            os.makedirs(os.environ['LOG_FILES_PATH'])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        result = notify_about_train_speed()
        print(result)
        assert result

    def test_notify_about_train_near_station(self):
        result = notify_about_train_near_station()
        print(result)
        assert result


class TestCeleryOperations:
    def test_celery_notify_about_train_speed(self):
        task = celery_app.send_task('notify_about_train_speed', args=[])
        result = AsyncResult(task.task_id, app=celery_app).get()
        while task.status == 'PENDING':
            sleep(0.1)
        print(result)
        assert task.status == 'SUCCESS'

    def test_celery_notify_about_train_near_station(self):
        task = celery_app.send_task('notify_about_train_near_station', args=[])
        result = AsyncResult(task.task_id, app=celery_app).get()
        while task.status == 'PENDING':
            sleep(0.1)
        print(result)
        assert task.status == 'SUCCESS'


class TestRequestsHandlers:
    def test_barrier_get(self):
        response = barrier_get("Białystok", logger)
        assert response['Response'] == 'OK'

    def test_barrier_post(self):
        response = barrier_post("Białystok", {'barrier_state': 'down'}, logger)
        assert response.get('Response') == 'OK'
