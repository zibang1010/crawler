# -*- coding: utf-8 -*-

# @File  : random_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from redis import StrictRedis
from settings import *
import requests
from loguru import logger

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def get_profile():
    """
       获取配置文件
       :return:
   """
    result = db.rpoplpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
    # return eval(result)
    return str(result, encoding='utf-8')


if __name__ == '__main__':
    print(get_profile())
