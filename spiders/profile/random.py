# -*- coding: utf-8 -*-

# @File  : random.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from redis import StrictRedis
from settings import *

db = StrictRedis(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def get_profile():
    """
       获取配置文件
       :return:
   """
    result = db.rpoplpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
    return eval(result)


if __name__ == '__main__':
    pass
