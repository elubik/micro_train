# micro_train

## Setup & run

Build and run the app with docker-compose
```bash
docker-compose up -d --build
```

## Usage & live check

####API Endpoints:
To check or set barrier state at given station name

| Endpoint | Method | Params | Description |
| -------- | ------ | ------ | ----------- |
| /<station_name> | GET | n/a | Get barrier state |
| /<station_name> | PUT | barrier_state | Set barrier state |

#### e.g. http://127.0.0.1:5002/Sochaczew

####Checking generated logs:
All files are stored in Celery Worker container /worker/logfiles/
```bash
docker-compose exec -it c8926dc61a7b bash
# ls -lah logfiles/
# cat logfiles/stations.log
# cat logfiles/slow.log
# cat logfiles/normal.log
# cat logfiles/fast.log
```

####Checking database:
Database is SQLite placed in /tmp/test.db file in lineman_api container.
```bash
docker exec -it d6c20ed23c3b python
>>> import sqlite3
>>> conn = sqlite3.connect('////tmp/test.db')
>>> c = conn.cursor()
>>> c.execute("SELECT * FROM Station")
```
Last two commands can be repeated to get latest data from db.

## Running tests inside containers

List all running containers
```bash
docker container ls
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                      NAMES
d6c20ed23c3b        micro_train_lineman_api   "gunicorn --bind=10.…"   6 minutes ago       Up 6 minutes        127.0.0.1:5002->5002/tcp   micro_train_lineman_api_1
8c8e45e01b49        worker                    "celery beat --app=w…"   36 minutes ago      Up 36 minutes                                  micro_train_beat_1
c8926dc61a7b        worker                    "celery worker --app…"   36 minutes ago      Up 36 minutes                                  micro_train_worker_1
a5d04541f565        redis                     "docker-entrypoint.s…"   13 hours ago        Up About an hour    127.0.0.1:6379->6379/tcp   micro_train_redis_1
```

Run tests on Lineman API containter
```bash
docker exec -it d6c20ed23c3b pytest /lineman_api/tests_resources.py -vvv
```

Run tests on Celery Worker containter
```bash
docker exec -it c8926dc61a7b pytest /app/tests_tasks.py -vvv
```

## Development
Define environment variables in your IDE
```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TRAIN_SPEED_SCHEDULE=10
STATIONS_SCHEDULE=180
LOG_FILES_PATH=~/micro_train/app/logfiles
HOST=localhost
PORT=5003
```

## Summary
Solution has been implemented with usage of 4 Docker container:
 * Tasks Scheduler - Celery Beat
 * Tasks Worker - Celery
 * DB broker ("the queue") - Redis
 * API REST - Flask-RESTfull
