# -*- coding: utf-8 -*-

# @File  : db.py
# @Author: zibang
# @Time  : 2月 08,2022
# @Desc  :
import json
import redis
from settings import *

"""
尾部获取
    -> 成功 -> 头部
    -> 失败 -> 尾部
"""


class RedisClient(object):
    def __init__(self, host, port, password, db):
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db,
                                    decode_responses=True)

    def sadd(self, name, value):
        return self.db.sadd(name, value)

    def spop(self, name):
        return json.loads(self.db.spop(name))

    def len(self, name):
        return self.db.llen(name)

    def delete(self, name, num, value):
        return self.db.lrem(name, num, value)

    def radd(self, name, value):
        """rpush 末尾添加"""
        return self.db.rpush(name, value)

    def ladd(self, key, data):
        """lpush 头部添加"""
        return self.db.lpush(key, data)

    def left_pop(self, name):
        """delete 首元素"""
        return self.db.lpop(name)

    def right_pop(self, name):
        ''' delete 尾元素 '''
        return self.db.rpop(name)

    def publish(self, channel, message):
        """订阅"""
        return self.db.publish(channel, message)

    def len(self, name):
        return self.db.llen(name)

    def range(self, name, start, end=-1):
        """返回列表中 start 至 end 之间的元素"""
        return self.db.lrange(name, start, end)

    def rpop_lpush(self, src, dst):
        """删除尾部->添加头部"""
        return self.db.rpoplpush(src, dst)


def test_demo():
    # rc = RedisClient(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    rc1 = RedisClient(host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    db = rc1.db
    key = 'test:expire'
    print(db.sadd(key, 'haha'))
    print(db.expire(key, 60))
    # item = [{"TPS2553DBVT-1": "250"}]
    # result = rc1.publish(REDIS_CHANNEL, json.dumps(item))
    # result = rc1.right_pop(REDIS_TASK_KEY)
    # print(result)
    # print(type(result))
    # if result:
    #     print(result)
    # else:
    #     print('0000000')
    # print(result)
    # result = rc.radd(REDIS_TASK_KEY, json.dumps(item))
    # result = rc.len(REDIS_TASK_KEY)
    # result = rc.rpop_lpush(REDIS_TASK_KEY, REDIS_TASK_KEY)
    # result_list = rc.range(REDIS_TASK_KEY, start=0)
    # for i in result_list:
    #     result = rc1.radd(REDIS_TASK_KEY, i)
    #     # result = json.loads(result)
    #     print(result)


if __name__ == '__main__':
    test_demo()
    # rc1 = RedisClient(host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    # print(rc1)
