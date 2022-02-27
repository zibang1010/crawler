# -*- coding: utf-8 -*-

# @File  : crawl.py
# @Author: zibang
# @Time  : 2月 13,2022
# @Desc

from playwright.sync_api import sync_playwright
from loguru import logger
import time
import random
from settings import *
import json
import socket
from tools import get_profile, get_proxy, on_start, on_stop, delete_proxy, decrease_profile
from db import RedisClient
from mongo_db import insert_log, insert_history

class Cart:
    def __init__(self):
        self.db = RedisClient(
            host=REDIS_TEST_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=5)

        self.db2 = RedisClient(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=0)

        self.host_name = socket.getfqdn(socket.gethostname())
        self.profile = None
        self.proxy = None
        self.flag = False
        self.task = None
        self.status_code = 0  # 状态码
        self.s_cts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.product = None
        self.number = None

    def on_publish(self, data):
        current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status_type = data.get('statusType')
        product_log = {
            'from': self.host_name,
            'in_cart': False,
            'inventory': 0,
            'load_time': current_date,
            'name': self.product,
        }

        if status_type == 'SUCCESS':
            item = [{
                "orderable_number": f"{self.product}",  # 型号
                "inventory": f"{self.number}",  # 推送的数量
                "minpage": f"{self.number}",  # 最小包装
                "from": self.host_name,  # 哪台探测机器探测到的
                "send": "true",  # 遗留字段，不用管
                "sendTime": f'{current_date}'  # 推送时间
            }]
            # 发布-订阅
            if self.db.publish(REDIS_CHANNEL, json.dumps(item)):
                logger.warning(f"Suceess publish: {item}")
            else:
                logger.error("Redis Error: publish")

            # push mongoDB
            product_log['inventory'] = self.number
            insert_log(product_log)
            insert_history(product_log)
            logger.warning(product_log)
        else:
            # push mongoDB
            insert_log(product_log)
            logger.warning(product_log)

    def on_log(self):
        """
            msg log
        """
        log = {
            'host_name': self.host_name,
            'cts': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'status_code': self.status_code if self.status_code else '404',
            'profile': self.profile,
            'ip': self.proxy.get('ip'),
            'port': self.proxy.get('port'),
            'address': self.proxy.get('address'),
            'operator': self.proxy.get('operator'),
        }

        if self.db.radd(REDIS_LOG_KEY, json.dumps(log)):
            logger.debug(f'Send msg log: {json.dumps(log, ensure_ascii=False)}')

    def on_response(self, response):
        if '/occservices/v2/ti/addtocart' in response.url:
            self.status_code = str(response.status)
            res_url = response.url
            if self.status_code == '200':
                self.flag = True
                logger.warning(f'Status: {self.status_code},{res_url}')
                data = response.json()
                logger.debug(f'Result: {data}')
                self.on_publish(data)
            else:
                logger.debug(f'Status: {self.status_code},{res_url}')

            self.on_log()

    def add_cookies(self, context):
        context.add_cookies([
            {"name": "pf-accept-language", "value": "zh-CN", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_language", "value": "\"zh-CN\"", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_shipTo", "value": "\"CN\"", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_currency", "value": "\"CNY\"", "domain": ".ti.com", "path": '/'},
            {"name": "pf-accept-language", "value": "zh-CN", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_language", "value": "\"zh-CN\"", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_shipTo", "value": "\"CN\"", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_currency", "value": "\"CNY\"", "domain": ".ti.com.cn", "path": '/'},
        ])

    def on_wait(self, page):
        """60s盾"""
        content = page.content()
        for _ in range(65):
            if "Checking available inventory" in content:
                logger.warning(
                    'Checking available inve')
            else:
                pass
            time.sleep(1)

    def execute(self, page):
        count_403 = 0
        count_428 = 0
        count_200 = 0
        for num in range(1, 100):
            content = page.content()
            data = self.db.rpop_lpush(REDIS_TASK_KEY, REDIS_TASK_KEY)
            if data:
                logger.debug(f'Get Task: {data}')
                self.task = eval(data)
                for self.product, self.number in self.task.items():
                    if 'Access Denied' in content:
                        # logger.warning(f"Access Denied")
                        # delete proxy
                        if delete_proxy(self.proxy.get('md5')):
                            logger.debug('Access Denied delete proxy...')
                        else:
                            logger.error('Error: delete proxy')
                        self.on_log()
                        return

                    if 'Sorry! We are currently doing site maintenance.' in content:
                        logger.warning('Sorry! We are currently doing site maintenance.')
                        return

                    if '未连接到互联网' in content:
                        logger.warning('未连接到互联网')
                        return

                    logger.debug('----> %s' % num)
                    page.mouse.click(748, 456, click_count=1)
                    page.mouse.click(748, 456, click_count=2)
                    page.mouse.click(748, 456, click_count=3)
                    page.mouse.click(748, 456, click_count=4)
                    page.evaluate(
                        '''
                         var data = {
                            "cartRequestList": [{
                                "packageOption": "CTX",
                                "opnId": "%s",
                                "quantity": "1",
                                "tiAddtoCartSource": "ti.com-productfolder",
                                "dienCode": "",
                                "year": "",
                                "week": "",
                                "batchCode": "",
                                "pcrCode": "",
                                "sparam": ""
                            },], "currency": "USD"
                        };
                        fetch("/occservices/v2/ti/addtocart", {
                            "headers": {
                                "content-type": "application/json",
                                "expires": "0",
                                "x-sec-clge-req-type": "ajax"
                            },
                            "body": JSON.stringify(data),
                            "method": "POST",
                            "mode": "cors",
                            "credentials": "include"
                        }).then(function(response) {
                          console.log(response.json())
                        }).catch(function(err) {
                          console.log(err)
                        });
                        ''' % self.product
                    )

                    if self.status_code == '200':
                        count_428 = 0  # 清零处理
                        count_403 = 0

                    if self.status_code == '428':
                        count_428 = count_428 + 1
                        # if count_428 == 3:
                        #     break
                        logger.debug('wait fo 65s')
                        self.on_wait(page)
                        count_403 = 0

                    if self.status_code == '403':
                        count_403 = count_403 + 1
                        if count_403 == 2:
                            return
                    page.wait_for_timeout(random.randint(2, 3) * 1000)
            else:
                logger.warning('No Task...')
                break

    def run(self):
        self.profile = get_profile()
        self.proxy = get_proxy()
        if self.profile and self.proxy:
            try:
                local_server = on_start(self.profile, self.proxy)
                if local_server:
                    time.sleep(5)
                    with sync_playwright() as p:
                        browser = p.chromium.connect_over_cdp(endpoint_url=local_server)
                        context = browser.new_context()
                        self.add_cookies(context)
                        page = context.new_page()
                        page.on('response', self.on_response)
                        page.goto(PRODUCT_URL, timeout=0)
                        # page.wait_for_timeout(60 * 1000 * 2)
                        self.execute(page)
                        page.wait_for_timeout(1000 * 2)
            except Exception as err:
                logger.error(err)
            finally:
                on_stop(self.profile)
        time.sleep(1)


if __name__ == '__main__':
    while True:
        c = Cart()
        c.run()
        time.sleep(1)
