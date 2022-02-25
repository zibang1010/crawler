# -*- coding: utf-8 -*-

# @File  : crawl.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :

from playwright.sync_api import sync_playwright
from loguru import logger
import time
import random
from settings import *
import json
import socket
# from mongo_db import insert_log, insert_history

from redis import StrictRedis
from config.start_profile import start_profile
from config.stop_profile import stop_profile
from pprint import pprint


class Cart(object):
    def __init__(self):
        self.profileId = None
        self.status_code = None
        self.proxy = None
        self.db = StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=6)
        self.task = None
        self.status_code_200 = 0
        self.status_code_428 = 0
        self.status_code_500 = 0
        self.status_code_403 = 0

        # ------------------------
        self.status_code_404 = 0
        self.status_code_503 = 0


    def on_log(self):
        log = {
            'status_code_200': self.status_code_200,
            'status_code_428': self.status_code_428,
            'status_code_500': self.status_code_500,
            'status_code_503': self.status_code_503,
            'status_code_404': self.status_code_404,
            'proxy': self.proxy,
            'profileId': self.profileId,

        }
        pprint(log)

    def on_response(self, response):
        url = response.url
        if 'occservices/v2/ti/addtocart' in url:
            self.status_code = str(response.status)
            if self.status_code == '200':
                self.status_code_200 = self.status_code_200 + 1
                data = response.json()
                logger.debug(f'Result: {data}')
                # push log
            elif self.status_code == '428':
                self.status_code_428 = self.status_code_428 + 1
            elif self.status_code == '500':
                self.status_code_500 = self.status_code_500 + 1
            elif self.status_code == '403':
                self.status_code_403 = self.status_code_403 + 1
            logger.warning(f'Status: {self.status_code},{url}')

    def remove_proxy(self):
        pass

    def execute_js(self, page):
        count_403 = 0
        count_200 = 0
        count_428 = 0  # 60s
        count_503 = 0  # 维护
        for num in range(1, 50):
            content = page.content()
            if 'Access Denied' in content:
                self.status_code_403 = self.status_code_403 + 1
                print('删除代理...')
                return

            if 'doing site maintenance' in content:
                self.status_code_503 = self.status_code_503 + 1
                logger.warning('Sorry! We are currently doing site maintenance.')
                print('删除代理')
                return

            if '未连接到互联网' in content:
                logger.warning('未连接到互联网')
                print('删除代理...')
                return

            data = self.db.rpoplpush(REDIS_TASK_KEY, REDIS_TASK_KEY)
            logger.debug(f'Get Task: {data}')
            self.task = eval(data)
            for self.product, self.number in self.task.items():
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
                    count_200 = count_200 + 1
                    count_403 = 0

                if self.status_code == '428':
                    count_428 = count_428 + 1
                    print('wait fo 65s')
                    page.wait_for_timeout(65 * 1000)
                    count_403 = 0

                if self.status_code == '403':
                    count_403 = count_403 + 1
                    if count_403 == 2:
                        print('删除指纹...')
                        return
                if self.status_code == '404':
                    print('删除代理...')
                    return

            time.sleep(8)

    def run(self):
        try:
            local_server = start_profile()
            self.profileId = local_server.get('profileId')
            host = local_server.get('host')
            self.proxy = local_server.get('proxy')
            if host and self.profileId:
                time.sleep(5)  # 缓冲
                with sync_playwright() as p:
                    browser = p.chromium.connect_over_cdp(endpoint_url=host)
                    context = browser.new_context()
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
                    page = context.new_page()
                    page.on('response', self.on_response)
                    page.goto(PRODUCT_URL, timeout=0)
                    page.wait_for_timeout(5 * 1000)
                    self.execute_js(page)
                    self.on_log()
                    page.wait_for_timeout(random.randint(2, 5) * 1000)

            # 缓冲报错
            else:
                print(host)
                print(self.profileId)

        except Exception as err:
            logger.error(err)
            print('删除代理...')
        finally:
            stop_profile(self.profileId)


if __name__ == '__main__':
    c = Cart()
    c.run()
