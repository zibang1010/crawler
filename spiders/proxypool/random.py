# -*- coding: utf-8 -*-

# @File  : random.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
from redis import StrictRedis
from settings import *

db = StrictRedis(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def get_proxy():
    """
    随机获取代理
    :return:
    """
    result = db.rpoplpush(REDIS_PROXY_KEY, REDIS_PROXY_KEY)
    return eval(result)


if __name__ == '__main__':
    print(get_proxy())
