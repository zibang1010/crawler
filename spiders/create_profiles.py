# -*- coding: utf-8 -*-

# @File  : create_c.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
from redis import StrictRedis
import requests
from loguru import logger


"""
   list:
        list all config

   delete:
       删除配置文件在线服务
       清空队列所有配置文件

   create:
       手动创建配置文件/自动化创建配置文件

   share:
       list 配置文件 批量共享所有用户

   Push:
       list 所有配置文件
       push Redis Qeueu

   """

# db = StrictRedis(
#     host=REDIS_TEST_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=5)

db = StrictRedis(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def list_all():
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
    logger.debug('Profile Count: %s' % len(profiles_list))
    return profiles_list
    # return result.json()


def delete(profile):
    params = {
        "token": VM_TOKEN,
        "profileId": profile
    }
    url = 'https://api.vmlogin.com/v1/profile/remove'
    result = requests.get(url, params)
    data = result.json()
    print("VMLogin: ", data)


def clear():
    db.delete(REDIS_PROFILE_KEY)


def create():
    pass


def share():
    pass


def push():
    pass


def pull():
    pass


def start():
    profile_list = list_all()
    profile_params = ''
    for profile in profile_list:
        # TODO delete()
        pass
        profile_params = profile_params + profile + ','
    # TODO clear()
    # TODO 创建config
    # TODO share()
    # TODO Push()

    print(profile_params[:-1])


if __name__ == '__main__':
    start()
