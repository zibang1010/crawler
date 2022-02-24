# -*- coding: utf-8 -*-

# @File  : demo.py
# @Author: zibang
# @Time  : 2月 17,2022
# @Desc  :
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from db import RedisClient

db = RedisClient()

es = Elasticsearch(hosts='http://127.0.0.1:9200/')


while True:
    try:
        data = db.get_value()
        print(data)
        if data:
            cts = data.get('cts')
            data['timestamp'] = datetime.strptime(cts, "%Y-%m-%d %H:%M:%S")
            result = es.index(index="ti-task", body=data)

            print(result)
        else:
            print('no log...')
            time.sleep(2)
    except Exception as err:
        print('error: ', err)
