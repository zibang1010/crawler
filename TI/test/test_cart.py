# -*- coding: utf-8 -*-

# @File  : test_cart.py
# @Author: zibang
# @Time  : 2月 13,2022
# @Desc
import requests
from playwright.sync_api import sync_playwright
from loguru import logger
import time
import random
from settings import *
from db import RedisClient
import multiprocessing
import os
import json
import socket

db = RedisClient(
    host=REDIS_TEST_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB)

db2 = RedisClient(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB)


class Cart(object):
    def __init__(self):
        self.status_code = 0  # 状态码
        self.host_name = socket.getfqdn(socket.gethostname())
        self.s_cts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.flag = False
        self.msg = {
            'host_name': self.host_name,
            'file_name': os.path.basename(__file__).split('.')[0],
            'status_code': {}
        }

    def on_send(self):
        """
            data send back
        """
        data_json = json.dumps(self.task)  # str
        if self.flag:
            # Scucess
            result = db.ladd(REDIS_TASK_KEY, data_json)
            if result:
                logger.warning(f"Task {result} -> left push: {data_json}")
            else:
                logger.error(f"Error: Task {result} -> left push")
            self.flag = False
        else:
            # Failed
            result = db.radd(REDIS_TASK_KEY, data_json)
            if result:
                logger.warning(f"Task {result} -> right push: {data_json}")
            else:
                logger.error(f"Error: Task {result} -> right push")

    def on_log(self):
        """
            host name count
        """
        self.msg['s_cts'] = self.s_cts
        self.msg['e_cts'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if db.radd(REDIS_LOG_KEY, json.dumps(self.msg)):
            logger.debug(f'Success log: {json.dumps(self.msg, indent=1, ensure_ascii=False)}')
        else:
            logger.error(f'Error log: {self.msg}')

    def on_response(self, response):
        if '/occservices/v2/ti/addtocart' in response.url:
            self.status_code = str(response.status)
            res_url = response.url
            if self.status_code == '200':
                self.flag = True
                logger.warning(f'Status: {self.status_code},{res_url}')
                data = response.json()
                logger.debug(f'Result: {data}')
                current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                status_type = data.get('statusType')
                if status_type == 'SUCCESS':
                    # 发布-订阅
                    item = [{
                        "orderable_number": f"{self.product}",  # 型号
                        "inventory": f"{self.number}",  # 推送的数量
                        "minpage": f"{self.number}",  # 最小包装
                        "from": self.host_name,  # 哪台探测机器探测到的
                        "send": "true",  # 遗留字段，不用管
                        "sendTime": f'{current_date}'  # 推送时间
                    }]
                    if db2.publish(REDIS_CHANNEL, json.dumps(item)):
                        logger.debug(f"Suceess publish: {item}")
                    else:
                        logger.error("Redis Error: publish")
                else:
                    cart_response = data.get('cartResponsetList')[0]
                    if db.radd(REDIS_SUCCESS_KEY, json.dumps(cart_response)):
                        # 200 成功统计
                        logger.debug(f"Suceess REDIS_SUCCESS_KEY: {data}")
                    else:
                        logger.error(f"Error REDIS_SUCCESS_KEY: {data}")
            else:
                logger.debug(f'Status: {self.status_code},{res_url}')

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

    def clear_cookies(self, context, page):
        context.clear_cookies()
        page.wait_for_timeout(2 * 1000)
        self.add_cookies(context)
        page.goto('https://www.ti.com.cn/product/cn/TLV9041', timeout=0)
        page.wait_for_timeout(5 * 1000)
        page.go_back()
        page.wait_for_timeout(5 * 1000)

    def run(self, profile, proxy=None):
        try:
            local_server = self.on_local_start(profile, proxy)
            print(local_server)
            if not local_server:
                print("资源启动失败...")
                return
            time.sleep(5)
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(endpoint_url=local_server)
                context = browser.new_context()
                self.add_cookies(context)
                page = context.new_page()

                page.on('response', self.on_response)
                page.goto(
                    # 'https://www.ti.com.cn/zh-cn/amplifier-circuit/op-amps/general-purpose/products.html#p1261max=3;5.5&~p78=In;Out&sort=p1130;asc', timeout=0)
                    'https://www.ti.com/store/ti/zh/p/product/?p=TLV9041UIDBVR', timeout=0)
                page.wait_for_timeout(5 * 1000)
                count = 0
                while True:
                    if 'Access Denied' in page.content():
                        print('IP被封~~~')
                        return

                    logger.debug('>>' * 30)
                    page.mouse.click(748, 456, click_count=1)
                    page.mouse.click(748, 456, click_count=2)
                    page.mouse.click(748, 456, click_count=3)
                    page.mouse.click(748, 456, click_count=4)
                    page.evaluate(
                        '''
                         var data = {
                            "cartRequestList": [{
                                "packageOption": "CTX",
                                "opnId": "TLV9041UIDBVR",
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
                        '''
                    )

                    if self.status_code == '200':
                        count = 0  # 清零处理

                    if self.status_code == '428':
                        logger.debug('wait fo 65s')
                        page.wait_for_timeout(65 * 1000)

                    if self.status_code == '403':
                        count = count + 1
                        if count == 2:
                            print("失败2次...")
                            self.clear_cookies(context, page)
                            page.wait_for_timeout(5 * 1000)

                        if count == 4:
                            print('结束了...')
                            page.wait_for_timeout(random.randint(2, 6) * 1000)
                            return
                    self.on_log()
                    page.wait_for_timeout(2 * 1000)


        except Exception as err:
            logger.error("Error: %s" % err)
        finally:
            self.on_local_stop(profile)

    def on_local_start(self, profileId, proxy):
        if not proxy:
            api_url = f"http://localhost:35000/api/v1/profile/start?automation=true&profileId={profileId}"
        else:
            ip = proxy.get('ip')
            port = proxy.get('port')
            proxy_params = f'&proxytype=http&proxyserver={ip}&proxyport={port}'
            api_url = f"http://localhost:35000/api/v1/profile/start?automation=true&profileId={profileId}{proxy_params}"

        resp = requests.get(api_url, timeout=30)
        status_code = resp.status_code
        if status_code == 200:
            data = resp.json()
            status = data.get('status')
            if status == 'ERROR':
                # local api bug
                print(data)
                logger.warning('未找到配置文件进程')
                return None
            local_server = data.get('value')
            return local_server
        else:
            raise Exception(f"{status_code}: Please check local api !!!")

    def on_local_stop(self, profile):
        api_url = f"http://localhost:35000/api/v1/profile/stop?automation=true&profileId={profile}"
        resp = requests.get(api_url, timeout=30)
        status_code = resp.status_code
        if status_code == 200:
            data = resp.json()
            status = data.get('status')
            if status == 'ERROR':
                time.sleep(10)
            local_server = data.get('value')
            return local_server
        else:
            raise Exception(f"{status_code}: Please check local api !!!")


def start():
    profile = db.rpop_lpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
    proxy = db.spop(REDIS_PROXY_KEY)
    logger.debug('profile: %s' % profile)
    logger.debug('proxy: %s' % proxy)

    if proxy and profile:
        c = Cart()
        c.run(profile, proxy)


if __name__ == '__main__':
    # proxy = {
    #     'ip': '121.205.231.140',
    #     'port': '16931',
    #     'adress': '湖南省常德市',
    # }
    start()
