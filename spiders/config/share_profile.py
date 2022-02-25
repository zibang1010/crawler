# -*- coding: utf-8 -*-

# @File  : random_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from redis import StrictRedis
from settings import *
import requests
from loguru import logger

db = StrictRedis(
    host=REDIS_HOST,
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


def get_profile():
    """
       获取配置文件
       :return:
   """
    result = db.rpoplpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
    print(result)
    # return eval(result)


def run():
    profile_list = list_all()
    print(profile_list)


if __name__ == '__main__':
    run()
