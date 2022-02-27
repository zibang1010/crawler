# -*- coding: utf-8 -*-

# @File  : create_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc  :

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


def list_all():
    """
    列出所有的配置文件
    :return:
    """
    params = {
        'token': VM_TOKEN,
    }
    url = f'{VM_URL}/profile/list'
    profiles_list = []
    result = requests.get(url, params)
    data_list = result.json().get('data')
    for data in data_list:
        sid = data.get('sid')
        profiles_list.append(sid)
    logger.debug('配置文件数量 : %s' % len(profiles_list))
    return profiles_list


def create():
    """
    列出在线所有的配置文件
    清空Queue
    添加到redis中...
    :return:
    """
    if db.delete(REDIS_PROFILE_KEY):
        logger.debug('Clear Queue Profile...')
    for profile in list_all():
        if db.lpush(REDIS_PROFILE_KEY, profile):
            if db.zadd(REDIS_PROFILE_SCORE_KEY, {profile: 0}):
                logger.debug('Add Profile: %s' % profile)


# def get_profiles():
#     """
#        获取配置文件
#        :return:
#    """
#     result = db.rpoplpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
#     print(result)
#     # return eval(result)
#
#
# def run():
#     profile_list = list_all()
#     print(profile_list)


if __name__ == '__main__':
    create()
