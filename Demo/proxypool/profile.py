# -*- coding: utf-8 -*-

# @File  : profile.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  :
import json

import redis
from TI.settings import *
import requests
from loguru import logger
import time
from random import choice

token = '068ff736efe8c0b21bb6ece6980d68ae'
base_url = 'https://api.vmlogin.com/v1'
MAX_SCORE = 100


class Profile(object):
    def __init__(self):
        self.db = redis.StrictRedis(
            host=REDIS_TEST_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=5)

    def get_profile(self):
        """
        获取浏览器配置文件的列表/profile/list
        """
        params = {
            'token': token,
            # 'tag': 'mac'
        }
        url = f'{base_url}/profile/list'
        result = requests.get(url, params)
        return result.json()

    def add_profile(self, profile):
        """
        添加新的project
        :param profile:
        :return:
        """
        item = {
            profile: 10,
        }
        return self.db.zadd(REDIS_PROFILE_KEY, item)

    def random_profile(self):
        """
        优先返回分数最高的profile
        :return:
        """
        result = self.db.zrangebyscore(REDIS_PROFILE_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return str(choice(result), encoding='utf-8')
        else:
            result = self.db.zrevrange(REDIS_PROFILE_KEY, 20, 100)
            if len(result):
                return str(choice(result), encoding='utf-8')
            else:
                return None

    def count_profile(self) -> int:
        """统计profile数量"""
        return self.db.zcard(REDIS_PROFILE_KEY)

    def decrease_profile(self, profile: str) -> int:
        """
            降低分数，如果分数==0 删除
        """
        self.db.zincrby(REDIS_PROFILE_KEY, -10, profile)
        score = self.db.zscore(REDIS_PROFILE_KEY, profile)
        if score <= 0:
            self.db.zrem(REDIS_PROFILE_KEY, profile)
            logger.warning(f"Remove score：{score}, {profile}")

    def increase_profile(self, profile: str):
        self.db.zincrby(REDIS_PROFILE_KEY, +10, profile)
        score = self.db.zscore(REDIS_PROFILE_KEY, profile)
        logger.warning(f"{profile} Current Score： {score}")


if __name__ == '__main__':
    p = Profile()
    """add"""
    result = p.get_profile()
    print(result)
    data_list = result.get('data')
    for data in data_list:
        sid = data.get('sid')
        print(sid)
        print(p.add_profile(sid))
    """random"""
    # print(p.random_profile())

    """count"""
    print(p.count_profile())

    # print(p.decrease_profile('B7B8544C-6382-433A-A03C-54829D1FEFDE'))
