# -*- coding: utf-8 -*-

# @File  : update_task.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
from redis import StrictRedis


def update():
    db = StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=5)
    db2 = StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=6)

    task_list = db.lrange('ti_task:lyt', 0, 500)
    db2.delete(REDIS_TASK_KEY)
    for task in task_list:
        db2.lpush(REDIS_TASK_KEY, task)
        print(task)
        print(eval(task))

if __name__ == '__main__':
    update()