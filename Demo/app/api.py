# -*- coding: utf-8 -*-

# @File  : vmlogin_api.py
# @Author: zibang
# @Time  : 2月 11,2022
# @Desc  : PoxyPool API

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from redis import StrictRedis
from settings import *

db = StrictRedis(host=REDIS_TEST_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)


class KeyItem(BaseModel):
    key: str


app = FastAPI()

log = {
    'message': 'ERROR',
    'result': None,
    'statusCode': 404,
}


@app.get("/api/v1")
async def index():
    return {"message": "Welcome to proxypool!"}


@app.get("/api/v1/random")
async def random():
    """随机返回"""
    key = db.randomkey()
    if key:
        reuslt = db.get(key)
        proxy_list = eval(reuslt)
        ip = proxy_list[0]
        port = proxy_list[1]
        item = {
            'ip': ip,
            'port': port,
            'adress': proxy_list[1],
        }
        log['message'] = 'SUCCESS'
        log['result'] = item
        log['statusCode'] = 200
        return log
    return log


@app.get("/api/v1/remove")
async def remove(data: KeyItem):
    """移除key"""
    item = data.dict()
    key = item.get('key')
    if db.exists(key):
        if db.delete(key):
            log['message'] = 'SUCCESS'
            log['statusCode'] = 200
            return log
    else:
        return log
    return log


if __name__ == '__main__':
    uvicorn.run(app='api:app', host='0.0.0.0', port=8080, reload=True)
