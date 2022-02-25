# -*- coding: utf-8 -*-

# @File  : random_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
from redis import StrictRedis
from settings import *

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=4)


def get_proxy():
    key = db.randomkey()
    value = db.get(str(key, encoding='utf-8'))
    return eval(value)


# def get_proxy():
#     """
#     随机获取代理
#     :return:
#     """
#     result = db.rpoplpush(REDIS_PROXY_KEY, REDIS_PROXY_KEY)
#     return eval(result)


if __name__ == '__main__':
    print(get_proxy())
