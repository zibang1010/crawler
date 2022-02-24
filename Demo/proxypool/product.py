# -*- coding: utf-8 -*-

# @File  : product.py
# @Author: zibang
# @Time  : 2月 17,2022
# @Desc  :
from db import RedisClient
from settings import *


def add_product():
    rc = RedisClient(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    rc1 = RedisClient(host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=5)
    result_list = rc.range(REDIS_TASK_KEY, start=0)
    for i in result_list:
        result = rc1.radd(REDIS_TASK_KEY, i)
        # result = json.loads(result)
        print(result)


if __name__ == '__main__':
    add_product()