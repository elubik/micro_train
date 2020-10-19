# micro_train

## Setup

Build and run the app with docker-compose
```bash
docker-compose up -d --build
```
Define environment variables in your IDE
```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TRAIN_SPEED_SCHEDULE=10
STATIONS_SCHEDULE=180
LOG_FILES_PATH=~/micro_train/app/logfiles
```

## Usage

API Endpoints:

| Endpoint | Method | Params | Description |
| -------- | ------ | ------ | ----------- |
| /<station_name> | GET | n/a | Get barrier state |
| /<station_name> | PUT | barrier_state | Set barrier state |


## Testing

List all running containers
```bash
docker container ls
CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                    NAMES
b1437acf7ed3        micro_train_lineman_api              "gunicorn --bind 0.0…"   About an hour ago   Up About an hour    0.0.0.0:5002->5002/tcp   mikrotrain_lineman_api_1
ea3cd3gc3310        worker                               "celery worker --app…"   About an hour ago   Up About an hour                             micro_train_worker_1
e2cdb31c2418        worker                               "celery beat --app=w…"   About an hour ago   Up About an hour                             micro_train_beat_1
af5c8d3eaed2        redis                                "docker-entrypoint.s…"   About an hour ago   Up About an hour    0.0.0.0:6379->6379/tcp   mikrotrain_redis_1
```

[TBD] Run tests on Lineman API containter
```bash
docker exec -it b1437acf7ed3 pytest /lineman_api/tests_api.py -vvv
```

Run tests on Celery Worker containter
```bash
docker exec -it e2cdb31c2418 pytest /app/tests.py -vvv
```
## Summary [PL]
Rozwiązanie zostało zaimplementowane w oparciu o 4 kontenery:
 * Scheduler zadań - oparty na Celery Beat
 * Worker kolejki zadań - oparty na Celery
 * Baza kolejki zadań - wykorzystująca Redis
 * API REST do zarządzania stanem szlabanu
 
Do zmiany:
 * refactor
