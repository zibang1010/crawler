# -*- coding: utf-8 -*-

# @File  : consume.py
# @Author: zibang
# @Time  : 2月 17,2022
# @Desc  :
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from redis import StrictRedis
from settings import *
from db.mongo import insert_count_log

db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=6)
from loguru import logger

es = Elasticsearch(hosts='http://127.0.0.1:9200/')

while True:
    try:
        if db.llen('lyt:log'):
            data = json.loads(db.lpop('lyt:log'))
            if data:
                status_code = data.get('status_code')
                cts = data.get('cts')
                data['timestamp'] = datetime.strptime(cts, "%Y-%m-%d %H:%M:%S")
                result = es.index(index="ti-task", body=data)
                if status_code == '200':
                    logger.warning(data)
                elif status_code == "428":
                    logger.error(data)
                else:
                    logger.info(data)
                insert_count_log(data)


            else:
                print('no log...')
                time.sleep(2)
    except Exception as err:
        print('error: ', err)
