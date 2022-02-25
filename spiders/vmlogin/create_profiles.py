# -*- coding: utf-8 -*-

# @File  : create_start_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
from redis import StrictRedis
import requests
from loguru import logger

"""
   list:
        list all profiles

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
    """
    列出所有的配置文件
    :return:
    """
    params = {
        'token': VM_TOKEN,
    }
    url = f'{VM_URL}/config/list'
    profiles_list = []
    result = requests.get(url, params)
    data_list = result.json().get('data')
    for data in data_list:
        sid = data.get('sid')
        profiles_list.append(sid)
    logger.debug('配置文件数量 : %s' % len(profiles_list))
    return profiles_list
    # return result.json()


def delete(profile):
    """
    删除server配置文件
    :param profile:
    :return:
    """
    params = {
        "token": VM_TOKEN,
        "profileId": profile
    }
    url = 'https://api.vmlogin.com/v1/profile/remove'
    result = requests.get(url, params)
    data = result.json()
    logger.debug("Delete: %s" % data)


def clear():
    if db.delete(REDIS_PROFILE_KEY):
        logger.debug("Clear Queue ", )


def create():
    pass


def share(profile_params):
    account_list = [
        'jxgl001@163.com',
        'jxgl002@163.com',
        'jxgl003@163.com',
        'jxgl004@163.com',
    ]
    for account in account_list:
        params = {
            "token": VM_TOKEN,
            "profileId": profile_params,
            "account": account
        }
        url = f'{VM_URL}/config/share'
        result = requests.get(url, params=params)
        print(result.json())


def push(profile):
    if db.lpush(REDIS_PROFILE_KEY, profile):
        logger.debug('Push Queue: %s' % profile)


def start():
    profile_list = list_all()
    for profile in profile_list:
        # TODO delete()
        delete(profile)
    # TODO clear()
    clear()
    # TODO 创建config

    # TODO share()
    # profile_list = list_all()
    # profile_params = ''
    # for config in profile_list:
    #     profile_params = profile_params + config + ','
    #
    # profile_params = profile_params[:-1]
    # share(profile_params)
    # for config in profile_list:
        # push(config)


if __name__ == '__main__':
    start()
