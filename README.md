# semantive_microservice

## Setup

Build and run the app with Compose
```bash
docker-compose up -d --build
```

## Usage

API Endpoints:

| Endpoint | Method | Params | Description |
| -------- | ------ | ------ | ----------- |
| /text | POST | url | Create a task for text grabbing |
| /images | POST | url | Create a task for image grabbing |
| /task | GET | task_id | Check status of created task |
| /download | GET | task_id | Download task results |


## Testing

List all running containers
```bash
docker container ls
CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                    NAMES
b1437acf7ed3        micro_train_lineman_api              "gunicorn --bind 0.0…"   About an hour ago   Up About an hour    0.0.0.0:5002->5002/tcp   mikrotrain_lineman_api_1
ea3cd3gc3310        micro_train_celery_train             "celery -A tasks wor…"   About an hour ago   Up About an hour                             mikrotrain_celery_train_1
e2cdb31c2418        micro_train_celery_queue             "celery -A tasks wor…"   About an hour ago   Up About an hour                             mikrotrain_celery_queue_1
af5c8d3eaed2        redis                                "docker-entrypoint.s…"   About an hour ago   Up About an hour    0.0.0.0:6379->6379/tcp   mikrotrain_redis_1
```

Run tests on LINEMAN API containter
```bash
docker exec -it b1437acf7ed3 pytest test_app.py -vvv
```

Run tests on Celery containter
```bash
docker exec -it e2cdb31c2418 pytest test_tasks.py -vvv
```
## Summary [PL]
Rozwiązanie zostało zaimplementowane w oparciu o 4 kontenery:
 * API - stworzone z wykorzystaniem frameworku Flask
 * Scheduler zadań - oparty na Celery Beat
 * Worker kolejki zadań - oparty na Celery
 * Baza kolejki zadań - wykorzystująca Redis
 
Do zmiany:
 * dodać testy dla Celery Beat
