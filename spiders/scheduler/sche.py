# -*- coding: utf-8 -*-

# @File  : sche.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  调度


import time
from apscheduler.schedulers.blocking import BlockingScheduler


def delete_profile_job():
    """
    自动删除分数低的profiles
    :return:
    """
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(t)


def create_profile_job():
    """
    自动创建profiles
    :return:
    """


def create_proxy_job():
    """
    自动添加代理proxy
    :return:
    """


def remove_proxy_job():
    """
    自动移除代理
    :return:
    """


def check_proxy_job(text):
    time.sleep(4)
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))


def es_log_job(text):
    """
    es log 统计
    :return:
    """
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} --- {}'.format(text, t))


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每隔 1分钟 运行一次 job 方法
    scheduler.add_job(es_log_job, 'interval', minutes=1, args=['ES Log Count'])
    scheduler.add_job(check_proxy_job, 'interval', max_instances=10, seconds=1, args=['Check Proxy'])

    scheduler.start()
