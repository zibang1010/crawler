# -*- coding: utf-8 -*-

# @File  : mongo.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from pymongo import MongoClient
import time
from datetime import datetime
from loguru import logger

client = MongoClient(
    'mongodb://root:sBv3hzO1Kzsj2FKhZXqN@dds-wz9b2269c38e3c943380-pub.mongodb.rds.aliyuncs.com:3717/admin')
ti_db = client['Ti']
zb_db = client['ZB_LOG']


def insert_history(data):
    try:
        conllection = ti_db['zb_history']
        conllection.insert_one(data)
    except Exception as err:
        logger.error(err)

def insert_count_log(data):
    try:
        conllection = zb_db['count_log']
        conllection.insert_one(data)
    except Exception as err:
        logger.error(err)


def insert_log(data):
    try:
        current_date = time.strftime("%Y-%m-%d %H", time.localtime()) + '点'
        collection = zb_db[current_date]
        collection.insert_one(data)
    except Exception as err:
        logger.error(err)
