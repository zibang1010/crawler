# -*- coding: utf-8 -*-

# @File  : delete_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import time
from loguru import logger
from settings import *
from redis import StrictRedis
import requests

"""
定时任务 --> 删除低分指纹
1、获取分数低 profile 0 >= profile <= 60
2、删除redis queue
3、删除server
"""
db = StrictRedis(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=5)


def delete(profile):
    """
    移除profile
    :return: {'status': 'OK', 'value': 191432}
    """
    params = {
        "token": VM_TOKEN,
        "profileId": profile
    }
    url = 'https://api.vmlogin.com/v1/profile/remove'
    result = requests.get(url, params)
    data = result.json()
    print("VMLogin: ", data)


def remove(profile):
    result = db.zrem(REDIS_PROFILE_KEY, profile)
    print("redis: ", result)


if __name__ == '__main__':
    profile_list = db.zrangebyscore(REDIS_PROFILE_KEY, -10, 100)
    print(len(profile_list))
    for num, profile in enumerate(profile_list):
        print('--' * 20)
        num = num + 1
        profile = str(profile, encoding='utf-8')
        print(num, profile)
        remove(profile)
        delete(profile)
        print('--' * 20)
