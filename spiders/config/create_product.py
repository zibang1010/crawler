# -*- coding: utf-8 -*-

# @File  : create_product.py
# @Author: zibang
# @Time  : 2月 26,2022
# @Desc
from redis import StrictRedis
from settings import *
import requests
from loguru import logger

"""
清空redis  Queue
获取在线所有的profiles
推送Redis Queue
"""
db = StrictRedis(
    host='r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com',
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def create():
    product = 'DLP3020AFQRQ1'
    if db.sadd(REDIS_PRODUCT_KEY, product):
        pass


if __name__ == '__main__':
    create()
