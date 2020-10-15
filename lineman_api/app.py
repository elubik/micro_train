from flask_restful import Resource, Api, reqparse
from celery.result import AsyncResult
from flask import Flask, send_file
from celery.states import SUCCESS
from celery import Celery
import os

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5002)
CELERY_BROKER = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379')
CELERY_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

app = Flask(__name__)
api = Api(app)
celery_app = Celery('tasks', backend=CELERY_BACKEND, broker=CELERY_BROKER)


class Lineman(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.url_param = 'url'
        self.task_param = 'task_id'
        self.parser.add_argument(self.url_param)

    def post(self):
        action = self.parser.parse_args().get(self.url_param)
        if action:
            task = celery_app.send_task('tasks.post_barrier_action', args=[action], kwargs={})
            return {'Response': 'OK',
                    'Message': f'http://{HOST}:{PORT}/task?task_id={task.task_id}'}
        else:
            return {'Response': 'ERROR',
                    'Message': 'Incorrect param'}

    def get(self):
        task_id = self.parser.parse_args().get(self.task_param)
        if task_id:
            result = AsyncResult(task_id, app=celery_app)

            if result.status == SUCCESS:
                return {'Response': result.status,
                        'Message': result}
                # return {'Response': result.status,
                #         'Message': f'http://{HOST}:{PORT}/download?task_id={task_id}'}
            else:
                return {'Response': result.status,
                        'Message': str(result.info)}
        else:
            return {'Response': 'ERROR',
                    'Message': 'Incorrect param'}


# class TaskResource(Resource):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.task_param = 'task_id'
#         self.parser.add_argument(self.task_param)
#
#     def get(self):
#         task_id = self.parser.parse_args().get(self.task_param)
#         if task_id:
#             result = AsyncResult(task_id, app=celery_app)
#
#             if result.status == SUCCESS:
#                 return {'Response': result.status,
#                         'Message': f'http://{HOST}:{PORT}/download?task_id={task_id}'}
#             else:
#                 return {'Response': result.status,
#                         'Message': str(result.info)}
#         else:
#             return {'Response': 'ERROR',
#                     'Message': 'Incorrect param'}


# class DownloadResource(Resource):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.task_param = 'task_id'
#         self.parser.add_argument(self.task_param)
#
#     def get(self):
#         task_id = self.parser.parse_args().get(self.task_param)
#         if task_id:
#             result = AsyncResult(task_id, app=celery_app)
#             file_type = result.result.split('.')[-1]
#
#             if result.status == SUCCESS:
#                 return send_file(
#                     result.result,
#                     attachment_filename=f'{task_id}.{file_type}',
#                     as_attachment=True)
#
#         return {}


api.add_resource(Lineman, '/barrier')
# lineman_api.add_resource(TaskResource, '/task')
# lineman_api.add_resource(DownloadResource, '/download')

if __name__ == '__main__':
    app.run(port=str(PORT))
