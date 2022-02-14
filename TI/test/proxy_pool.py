# -*- coding: utf-8 -*-

# @File  : settings.py
# @Author: zibang
# @Time  : 2月 10,2022
# @Desc  : proxy_pool
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import time
import random
import threading

import requests
from db import RedisClient
from settings import *


class ProxyPool():
    def __init__(self, orderid, proxy_count):
        self.orderid = orderid
        self.proxy_count = proxy_count if proxy_count < 5 else 5
        self.alive_proxy_list = []  # 活跃IP列表
        self.db = RedisClient(
            host=REDIS_TEST_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB)

    def _fetch_proxy_list(self, count):
        """调用快代理API获取代理IP列表"""
        try:
            # res = requests.get("http://dps.kdlapi.com/api/getdps/?orderid=%s&num=%s&pt=1&sep=1&f_et=1&format=json" % (
            res = requests.get(
                'http://dps.kdlapi.com/api/getdps/?orderid=%s&num=%s&signature=bfveudiqg9036cie2tzt9pt62gocv6pz&pt=1&f_loc=1&f_et=1&format=json&sep=1' %
                (self.orderid, count))
            return [proxy.split(',') for proxy in res.json().get('data').get('proxy_list')]
        except:
            print("API获取IP异常，请检查订单")
        return []

    def _init_proxy(self):
        """初始化IP池"""
        self.alive_proxy_list = self._fetch_proxy_list(self.proxy_count)

    def add_alive_proxy(self, add_count):
        """导入新的IP, 参数为新增IP数"""
        self.alive_proxy_list.extend(self._fetch_proxy_list(add_count))

    def get_proxy(self):
        """从IP池中获取IP"""
        return random.choice(self.alive_proxy_list)[0] if self.alive_proxy_list else ""

    def run(self):
        sleep_seconds = 1
        self._init_proxy()
        while True:
            for proxy in self.alive_proxy_list:
                proxy[2] = float(proxy[2]) - sleep_seconds  # proxy[1]代表此IP的剩余可用时间
                if proxy[2] <= 3:
                    self.alive_proxy_list.remove(proxy)  # IP还剩3s时丢弃此IP
            if len(self.alive_proxy_list) < self.proxy_count:
                self.add_alive_proxy(self.proxy_count - len(self.alive_proxy_list))
            time.sleep(sleep_seconds)
            print(self.alive_proxy_list)
            for proxy_list in self.alive_proxy_list:
                ip, port = str(proxy_list[0]).split(':')
                address = proxy_list[1]
                expire = proxy_list[2]
                item = {
                    'ip': ip,
                    'port': port,
                    'address': address,
                }
                self.db.sadd(REDIS_PROXY_KEY, json.dumps(item, ensure_ascii=False))
                # print('expire: %s' % expire)
                # print(item)

    def start(self):
        """开启子线程更新IP池"""
        t = threading.Thread(target=self.run)
        t.setDaemon(True)  # 将子线程设为守护进程，主线程不会等待子线程结束，主线程结束子线程立刻结束
        t.start()


if __name__ == '__main__':
    proxy_pool = ProxyPool('954480323287312', 15)  # 订单号, 池子中维护的IP数
    proxy_pool.start()
    time.sleep(1)  # 等待IP池初始化

    while True:
        time.sleep(1)
