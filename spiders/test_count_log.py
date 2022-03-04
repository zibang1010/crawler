# -*- coding: utf-8 -*-

# @File  : test_count_log.py
# @Author: zibang
# @Time  : 3月 03,2022
# @Desc  :
from pymongo import MongoClient
import time
from datetime import datetime
from loguru import logger

client = MongoClient(
    'mongodb://root:sBv3hzO1Kzsj2FKhZXqN@dds-wz9b2269c38e3c943380-pub.mongodb.rds.aliyuncs.com:3717/admin')
ti_db = client['ZB_LOG']


def count(query):
    conllection = ti_db['count_log']
    return conllection.find(query).count()


def insert_log(data):
    try:
        conllection = ti_db['count_log']
        conllection.insert_one(data)
    except Exception as err:
        logger.error(err)


def start():
    pass


if __name__ == '__main__':
    a_list = [
        {'profileId': '63C8B42E-0666-42AE-8CCD-DB94CFDC79DE', 'host_name': 'zibang-002', 'cts': '2022-03-03 16:41:06',
         'status_code': '200', 'ip': '223.198.227.175', 'port': '20143', 'address': '海南省三亚市', 'operator': '电信'}
    ]
    for a in a_list:
        insert_log(a)
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    print(current_date)
    print(type(current_date))
