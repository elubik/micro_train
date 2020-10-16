from celery.result import AsyncResult
from celery import Celery
from time import sleep
import os
import random

from celery_queue.tasks import celery_app


class TestTrain:
    def test_empty(self):
        assert True

    # def test_post_train_speed(self):
    #     train_speed = round(random.uniform(0, 180), 2)
    #     task = celery_app.send_task('tasks.log_train_speed', args=[train_speed])
    #     result = AsyncResult(task.task_id, app=celery_app).get()
    #     while task.status == 'PENDING':
    #         sleep(0.1)
    #     print(result)
    #     assert task.status == 'SUCCESS'
    #     assert result == train_speed
    #
    # def test_post_train_near_station(self):
    #     station = random.choice(["Białystok", "Łowicz", "Nieborów", "Warszawa"])
    #     task = celery_app.send_task('tasks.post_train_near_station', args=[station])
    #     result = AsyncResult(task.task_id, app=celery_app).get()
    #     while task.status == 'PENDING':
    #         sleep(0.1)
    #     print(result)
    #     assert task.status == 'SUCCESS'
    #     assert result == station


    # def test_non_existing_page(self):
    #     url = 'http://thispagedoesntexist.com/'
    #     task = celery_app.send_task('tasks.get_url_text', args=[url], kwargs={})
    #     while task.status == 'PENDING':
    #         sleep(0.1)
    #     assert task.status == 'FAILURE'
    #
    # def test_timeout(self):
    #     url = 'http://www.google.com:81/'
    #     task = celery_app.send_task('tasks.get_url_text', args=[url], kwargs={})
    #     while task.status == 'PENDING':
    #         sleep(0.1)
    #     assert task.status == 'FAILURE'
