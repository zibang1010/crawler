# -*- coding: utf-8 -*-

# @File  : es_count.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :  统计es 状态码 -->  redis queue log

import time
from loguru import logger
from settings import *
from db.update_task import RedisClient
from elasticsearch import Elasticsearch
import datetime


class ESCount:
    def __init__(self):
        self.db = RedisClient(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=0)
        self.es = Elasticsearch(hosts=ES_HOST)

    def push(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        today_time = today.strftime("%Y-%m-%d %H:%M:%S")
        tomorrow_time = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        cts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dsl = {
            "size": 0,
            "query": {
                "constant_score": {
                    "filter": {
                        "range": {
                            "timestamp": {
                                "gte": today_time,
                                "lte": tomorrow_time,
                                "format": "yyyy-MM-dd HH:mm:ss"
                            }
                        }
                    }
                }
            },
            "aggs": {
                "status_count": {
                    "terms": {
                        "field": "status_code"
                    }
                }
            }

        }
        result = self.es.search(index="ti-task", body=dsl, ignore=[404, 400])
        aggregations = result.get('aggregations')
        status_count = aggregations.get('status_count')
        buckets = status_count.get('buckets')
        log = {}
        for info in buckets:
            log[info.get('key')] = info.get('doc_count')
        log['cts'] = cts
        self.db.push_es_log(log)

    def start(self):
        while 1:
            try:
                self.push()
                time.sleep(60)
            except Exception as err:
                logger.error(err)


if __name__ == '__main__':
    sec = ESCount()
    sec.start()
