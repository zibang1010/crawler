# -*- coding: utf-8 -*-

# @File  : prof_auto.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
from profile.create_profile import create_profile
from profile.share_profiles import share
from redis import StrictRedis
from settings import *

class ProfilesAuto:
    def __init__(self):
        self.db = StrictRedis(
            host=REDIS_TEST_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=5)

    def on_run(self):
        value = create_profile()
        if value:
            share(value)
            item = {
                value: 10,
            }
            self.db.zadd(REDIS_PROFILE_KEY, item)
            print(f"{value} Sucess!!")


if __name__ == '__main__':
    # while True:
    for _ in range(5):
        pa = ProfilesAuto()
        pa.on_run()
