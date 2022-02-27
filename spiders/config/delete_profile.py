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
from config.list_profiles import list_all

"""

"""
db = StrictRedis(
    host='r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com',
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


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
    print('Remove Profile %s' % profile)


def clear():
    result = db.delete(REDIS_PROFILE_KEY)
    result = db.delete(REDIS_PROFILE_SCORE_KEY)
    # result = db.delete("ti_task:profile")
    print("redis: ", result)


if __name__ == '__main__':
    clear()
    profile_list = list_all()
    for num, profile in enumerate(profile_list):
        delete(profile)

    clear()
