# -*- coding: utf-8 -*-

# @File  : tools.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  :

from db import RedisClient
from settings import *
from loguru import logger
import requests

db = RedisClient(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=5)

db2 = RedisClient(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=4)


def get_proxy():
    proxy = db2.random_proxy()
    logger.debug('Get Proxy: %s' % proxy)
    return proxy

def decrease_profile(profile):
    db.decrease_profile(profile)
    # reqeust delete
    pass


def get_profile():
    profile = db.random_profile()
    logger.debug('Get profile: %s' % profile)

    return profile




def delete_proxy(key):
    return db2.delete_proxy(key)


def on_start(profile, proxy):
    if not proxy:
        api_url = f"http://localhost:35000/api/v1/profile/start?automation=true&profileId={profile}"
    else:
        ip = proxy.get('ip')
        port = proxy.get('port')
        proxy_params = f'&proxytype=http&proxyserver={ip}&proxyport={port}'
        api_url = f"http://localhost:35000/api/v1/profile/start?automation=true&profileId={profile}{proxy_params}"

    resp = requests.get(api_url, timeout=30)
    status_code = resp.status_code
    if status_code == 200:
        data = resp.json()
        status = data.get('status')
        if status == 'ERROR':
            # local api bug
            logger.error('未找到配置文件进程')
            return None
        local_server = data.get('value')
        return local_server
    else:
        raise Exception(f"{status_code}: Please check local api !!!")


def on_stop(profile):
    api_url = f"http://localhost:35000/api/v1/profile/stop?automation=true&force=true&profileId={profile}"
    resp = requests.get(api_url, timeout=30)
    status_code = resp.status_code
    if status_code == 200:
        data = resp.json()
        status = data.get('status')
        if status == 'ERROR':
            pass
        local_server = data.get('value')
        return local_server
    else:
        raise Exception(f"{status_code}: Please check local api !!!")
