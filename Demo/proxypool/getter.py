# -*- coding: utf-8 -*-

# @File  : getter.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  : 生成代理池
import json
import time
import hashlib
from storages import RedisClient
from proxypool.kdl import KdlCrawler
from TI.settings import PROXY_COUNT, PROXY_EX
from loguru import logger


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = KdlCrawler()

    def is_full(self):
        pass

    def run(self):
        while True:
            count = self.redis.count()
            if count < PROXY_COUNT:
                proxy = self.crawler.crawl()
                if proxy:
                    host = proxy.get('host')
                    md5 = hashlib.md5(host.encode(encoding='UTF-8')).hexdigest()
                    ex = int(proxy.get('expire')) - PROXY_EX
                    proxy['md5'] = md5
                    data = json.dumps(proxy, ensure_ascii=False)
                    if self.redis.add(md5, data, ex=ex):
                        logger.debug('Queue Add Success %s %s' % (proxy, count))
                    else:
                        logger.error('Queue Add Error %s %s' % (proxy, count))
            time.sleep(1)


if __name__ == '__main__':
    while 1:
        try:
            g = Getter()
            g.run()
        except Exception as err:
            print(err)
        time.sleep(1)
