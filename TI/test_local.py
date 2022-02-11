# -*- coding: utf-8 -*-

# @File  : test_local.py
# @Author: zibang
# @Time  : 2月 10,2022
# @Desc  : 根据 proxya params 启动浏览器
import requests
import time
from test_proxy import on_proxy
from loguru import logger


def on_local_start(profileId, proxy_server):
    proxy_ip = proxy_server.get('ip')
    proxy_port = proxy_server.get('port')
    proxy_params = f'&proxytype=http&proxyserver={proxy_ip}&proxyport={proxy_port}'
    api_url = f"http://localhost:35000/api/v1/profile/start?automation=true&profileId={profileId}{proxy_params}"
    resp = requests.get(api_url, timeout=30)
    status_code = resp.status_code
    if status_code == 200:
        data = resp.json()
        status = data.get('status')
        if status == 'ERROR':
            # local api bug
            logger.warning('未找到配置文件进程')
            return None
        local_server = data.get('value')
        return local_server
    else:
        raise Exception(f"{status_code}: Please check local api !!!")


def on_local_stop(profile):
    api_url = f"http://localhost:35000/api/v1/profile/stop?automation=true&profileId={profile}"
    resp = requests.get(api_url, timeout=30)
    status_code = resp.status_code
    if status_code == 200:
        data = resp.json()
        status = data.get('status')
        if status == 'ERROR':
            # local api bug
            # print('未找到配置文件进程')
            # return None
            time.sleep(10)
        local_server = data.get('value')
        return local_server
    else:
        raise Exception(f"{status_code}: Please check local api !!!")


def on_local(profileId):
    try:
        proxy_server = on_proxy()
        if proxy_server:
            local_server = on_local_start(profileId, proxy_server)
            if local_server:
                logger.debug(f'local_server: {local_server}')
                return local_server
        return None
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    on_local()
