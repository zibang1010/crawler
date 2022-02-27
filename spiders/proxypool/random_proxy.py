# -*- coding: utf-8 -*-

# @File  : random_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
from redis import StrictRedis
from settings import *
from loguru import logger
db = StrictRedis(
    host="r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com",
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=7)


def get_proxy():
    try:
        key = db.randomkey()
        value = db.get(str(key, encoding='utf-8'))
        return eval(value)
    except Exception as err:
        logger.error(err)
        return None

# def get_proxy():
#     """
#     随机获取代理
#     :return:
#     """
#     result = db.rpoplpush(REDIS_PROXY_KEY, REDIS_PROXY_KEY)
#     return eval(result)


if __name__ == '__main__':
    print(get_proxy())
