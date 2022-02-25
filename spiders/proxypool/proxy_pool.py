# -*- coding: utf-8 -*-

# @File  : proxy_pool.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
# !/usr/bin/env python
# -*- encoding: utf-8 -*-


import time
import random
import threading
from settings import *
import requests
from redis import StrictRedis
import json
from loguru import logger


class ProxyPool():

    def __init__(self):
        self.proxy_count = PROXY_POOL_COUNT  # 池子维护的IP总数，建议一般不要超过50
        self.alive_proxy_list = []  # 活跃IP列表
        self.db = StrictRedis(
            host=REDIS_TEST_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=6)

    def fetch_proxy_list(self, count):
        """调用快代理API获取代理IP列表"""
        try:
            res = requests.get(
                "http://dps.kdlapi.com/api/getdps/?orderid=%s&num=%s&signature=bfveudiqg9036cie2tzt9pt62gocv6pz&pt=1&st=5&f_loc=1&f_et=1&f_carrier=1&format=json&sep=1" % (
                    PROXY_ORDER_ID, count))
            data = res.json().get('data')
            proxy_list = data.get('proxy_list')
            alive = []
            for proxy in proxy_list:
                p_l = str(proxy).split(',')
                ip, port = str(p_l[0]).split(':')
                item = {
                    'host': p_l[0],
                    'ip': ip,
                    'port': port,
                    'address': p_l[1],
                    'expire': p_l[2],
                    'operator': p_l[3],
                }
                # push redis Queue
                self.db.rpush(REDIS_PROXY_KEY, json.dumps(item, ensure_ascii=False))
                alive.append(item)
                logger.debug(f'Add Proxy: {item}')
            return alive
        except Exception as err:
            logger.warning(f"{err}")
        return []

    def _init_proxy(self):
        """初始化IP池"""
        self.alive_proxy_list = self.fetch_proxy_list(self.proxy_count)

    def add_alive_proxy(self, add_count):
        """导入新的IP, 参数为新增IP数"""
        self.alive_proxy_list.extend(self.fetch_proxy_list(add_count))

    def start(self):
        sleep_seconds = 1
        self._init_proxy()
        while True:
            for proxy in self.alive_proxy_list:
                proxy['expire'] = float(proxy.get('expire')) - sleep_seconds
                if proxy['expire'] <= 60:
                    self.alive_proxy_list.remove(proxy)
                    # 移除redis queue proxy
                    self.db.lrem(REDIS_PROXY_KEY, 1, json.dumps(proxy, ensure_ascii=False))
                    logger.warning(f"Remove Proxy: {proxy}")
            if len(self.alive_proxy_list) < self.proxy_count:
                self.add_alive_proxy(self.proxy_count - len(self.alive_proxy_list))
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    proxy_pool = ProxyPool()
    proxy_pool.start()
