# -*- coding: utf-8 -*-

# @File  : db.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  : 存储proxy

from redis import StrictRedis
from settings import *
import json


class RedisClient(object):
    def __init__(self, host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=4, **kwargs):
        # if set connection_string, just use it

        self.db = StrictRedis(
            host=host, port=port, password=password, db=db, decode_responses=True, **kwargs)

    def random(self):
        key = self.db.randomkey()
        if key:
            proxy = self.db.get(key)
            proxy = json.loads(proxy)
            return proxy
        return None

    def add(self, name, value, ex):
        return self.db.set(name, value, ex=ex)

    def delete(self, key):
        if self.db.exists(key):
            return self.db.delete(key)
        return None

    def count(self):
        return self.db.dbsize()


if __name__ == '__main__':
    redis = RedisClient()
    print(redis.random())
