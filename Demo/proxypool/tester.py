# -*- coding: utf-8 -*-

# @File  : tester.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  : 测试代理。。
from Demo.proxypool.storages import StrictRedis
import requests
from loguru import logger


class Tester(object):
    def __init__(self):
        self.redis = StrictRedis()

    def test(self, host):
        # host = proxy.get('host')
        proxies = {
            'http': 'http://' + host,
            'https': 'https://' + host,
        }
        try:
            response = requests.get('http://httpbin.org/get', proxies=proxies, timeout=5)
            if response.status_code == 200:
                logger.debug(f'Test Proxy Sucess {host}')
                return host
            else:
                self.redis.delete(host)
                logger.error(f'Proxy invalid {host}')
                return None
        except requests.exceptions.ConnectionError as e:
            self.redis.delete(host)
            logger.error(f'Proxy invalid {host}')
        return None


if __name__ == '__main__':
    t = Tester()
    t.test('124.227.82.95:19248')