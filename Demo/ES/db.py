# -*- coding: utf-8 -*-

# @File  : db.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  : 存储proxy

from redis import StrictRedis
from settings import *
import json


class RedisClient(object):
    def __init__(self, host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=5, **kwargs):
        self.db = StrictRedis(
            host=host, port=port, password=password, db=db, decode_responses=True, **kwargs)

    def get_value(self):
        result = self.db.lpop(REDIS_LOG_KEY)
        if result:
            return json.loads(result)
        return None

