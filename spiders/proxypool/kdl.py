# -*- coding: utf-8 -*-

# @File  : kdl.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  : 获取代理
import time

import requests
from loguru import logger
from settings import KDL_URL

MAX_COUNT = 1


class KdlCrawler(object):
    def __init__(self):
        pass

    def fetch(self) -> dict:
        try:
            res = requests.get(KDL_URL)
            return res.json()
        except Exception as err:
            logger.error("API获取IP异常，请检查订单 %s" % res.status_code)
        return None

    def parse(self, response) -> dict:
        """
        :param response:
        :return:
        """
        try:
            data = response.get('data')
            proxy_list = data.get('proxy_list')[0]
            proxy_list = str(proxy_list).split(',')
            host = str(proxy_list[0]).split(':')
            proxy = {
                'host': proxy_list[0],
                'ip': host[0],
                'port': host[1],
                'address': proxy_list[1],
                'expire': proxy_list[2],
                'operator': proxy_list[3],
            }
            return proxy
        except Exception as err:
            logger.error(err)
            time.sleep(20)
            return None

    def crawl(self):
        response = self.fetch()
        if response:
            proxy = self.parse(response)
            return proxy


if __name__ == '__main__':
    kdl = KdlCrawler()
    proxy = kdl.crawl()
    print(proxy)
