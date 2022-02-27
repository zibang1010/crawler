# -*- coding: utf-8 -*-

# @File  : db.py
# @Author: zibang
# @Time  : 2月 08,2022
# @Desc  :
import json
import redis
from settings import *
from random import choice
from loguru import logger
import requests

MAX_SCORE = 100


def detail(name):
    """浏览器配置文件详情"""
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/detail'
    result = requests.get(url, params)
    data = result.json()
    print(data)
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return data


def release(name):
    """释放文件"""
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/release'
    result = requests.get(url, params)
    data = result.json()
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return True


def remove(name):
    """
    移除profile
    :return: {'status': 'OK', 'value': 191432}
    """
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/remove'
    result = requests.get(url, params)
    data = result.json()
    print(data)
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return True


class RedisClient(object):
    def __init__(self, host, port, password, db):
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db,
                                    decode_responses=True)

    def increase_profile(self, profile: str):
        self.db.zincrby(REDIS_PROFILE_KEY, +10, profile)
        score = self.db.zscore(REDIS_PROFILE_KEY, profile)
        logger.warning(f"{profile} Current Score： {score}")

    def decrease_profile(self, profile: str) -> int:
        """
            降低分数，如果分数==0 删除
        """
        self.db.zincrby(REDIS_PROFILE_KEY, -10, profile)
        score = self.db.zscore(REDIS_PROFILE_KEY, profile)
        # if score <= 0:
        #     if self.db.zrem(REDIS_PROFILE_KEY, profile):
        #         logger.warning(f"Decrease score：{score}, {profile}")
                # requests delete
                # if remove(profile):
                #     # logger.warning(f"Delete profile：{profile}")
                #     pass

    def random_profile(self):
        """
        随机获取指纹
        """
        result = self.db.zrangebyscore(REDIS_PROFILE_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            # return str(choice(result), encoding='utf-8')
            return str(choice(result))
        else:
            result = self.db.zrevrange(REDIS_PROFILE_KEY, 0, 100)
            if len(result):
                # return str(choice(result), encoding='utf-8')
                return str(choice(result))
            else:
                return None

    def random_proxy(self):
        key = self.db.randomkey()
        if key:
            proxy = self.db.get(key)
            proxy = json.loads(proxy)
            return proxy
        return None

    def delete_proxy(self, key):
        if self.db.exists(key):
            return self.db.delete(key)

        return None

    def spop(self, name):
        return json.loads(self.db.spop(name))

    def radd(self, name, value):
        """rpush 末尾添加"""
        return self.db.rpush(name, value)

    def ladd(self, key, data):
        """lpush 头部添加"""
        return self.db.lpush(key, data)

    def left_pop(self, name):
        """delete 首元素"""
        return self.db.lpop(name)

    def right_pop(self, name):
        ''' delete 尾元素 '''
        return self.db.rpop(name)

    def publish(self, channel, message):
        """订阅"""
        return self.db.publish(channel, message)

    def len(self, name):
        return self.db.llen(name)

    def range(self, name, start, end=-1):
        """返回列表中 start 至 end 之间的元素"""
        return self.db.lrange(name, start, end)

    def rpop_lpush(self, src, dst):
        """删除尾部->添加头部"""
        return self.db.rpoplpush(src, dst)
