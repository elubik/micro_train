from worker import celery_app


def set_file_name_by_speed(speed):
    file_name = "normal.log"
    if speed < 40:
        file_name = "slow.log"
    elif 140 <= speed:
        file_name = "fast.log"
    return file_name


@celery_app.task(bind=True, name='post_train_speed', queue='train_beat')
def post_train_speed(train_speed):
    file_name = set_file_name_by_speed(train_speed)
    file = open(file_name, 'a')
    file.write(train_speed)
    file.close()


@celery_app.task(bind=True, name='post_train_near_station', queue='train_beat')
def post_train_near_station(station):
    return station
