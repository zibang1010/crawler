# -*- coding: utf-8 -*-

# @File  : main.py
# @Author: zibang
# @Time  : 2月 10,2022
# @Desc  :
import json

from test_local import on_local, on_local_stop
from playwright.sync_api import sync_playwright
from loguru import logger
from db import RedisClient
from settings import *
import time
import socket
import os

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

logger.add('addToCart.log', level="DEBUG")


class addToCart:
    def __init__(self, profileId):
        self.profileId = profileId
        self.host_name = socket.getfqdn(socket.gethostname())
        self.page = None
        self.task = None
        self.product = None
        self.number = 0
        self.flag = False
        self.status_code = None
        self.break_flag = False
        self.start_time = time.time()
        self.s_cts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.runTime = None
        self.msg = {
            'host_name': self.host_name,
            'file_name': os.path.basename(__file__).split('.')[0],
            'status_code': {}
        }

    def on_log(self):
        """
            host name count
        """
        self.msg['s_cts'] = self.s_cts
        self.msg['e_cts'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.msg['run_time'] = round(time.time() - self.start_time, 2)
        if db.radd(REDIS_LOG_KEY, json.dumps(self.msg)):
            logger.debug(f'Success log: {json.dumps(self.msg, indent=1, ensure_ascii=False)}')
        else:
            logger.error(f'Error log: {self.msg}')

    def on_send(self):
        """
            data send back
        """
        data_json = json.dumps(self.task)  # str
        # send back
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

    def on_success(self, data):
        """
            状态200 -> Queue
        """
        current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status_type = data.get('statusType')
        cart_response = data.get('cartResponsetList')[0]
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

        if db.radd(REDIS_SUCCESS_KEY, json.dumps(cart_response)):
            # 200 成功统计
            logger.debug(f"Suceess REDIS_SUCCESS_KEY: {data}")
        else:
            logger.error(f"Error REDIS_SUCCESS_KEY: {data}")

        # [{'opnId': 'TPS63060DSCR', 'status': 'error', 'statusCode': '404', 'message': 'Product is an out of stock'}]
        cart_response['cts'] = current_date
        cart_response['host_name'] = self.host_name
        if db.radd(REDIS_ERROR_KEY, json.dumps(data)):
            # 200 成功统计
            logger.debug(f"Suceess REDIS_ERROR_KEY: {data}")
        else:
            logger.error(f"Error REDIS_ERROR_KEY: {data}")

    def on_response(self, response):
        if '/occservices/v2/ti/addtocart' in response.url:
            self.status_code = str(response.status)
            res_url = response.url
            logger.debug(f'Status: {self.status_code},{res_url}')

            result = self.msg.get('status_code').get(self.status_code)
            if not result:
                self.msg['status_code'][self.status_code] = 1
            else:
                self.msg['status_code'][self.status_code] = result + 1

            if self.status_code == '200':
                # {"cartId":"a77728ba-6539-4f5e-8ede-023098c9f4aa","statusType":"SUCCESS","statusCode":"200","message":"1 - Items added to the cart","errorType":null,"placeholderMap":null,"cartResponsetList":null}
                self.flag = True
                data = response.json()
                self.on_success(data)


    def on_handler(self):
        count = 0
        for num in range(1, 100):
            logger.debug('--' * 30)
            if self.break_flag:
                break

            data = db.right_pop(REDIS_TASK_KEY)
            if data:
                logger.debug(f'Get Task: {data}')
                self.task = json.loads(data)  # dict
                for self.product, self.number in self.task.items():
                    logger.debug('>>>>>')
                    self.page.mouse.click(748, 456, click_count=1)
                    self.page.mouse.click(748, 456, click_count=2)
                    self.page.mouse.click(748, 456, click_count=3)
                    self.page.mouse.click(748, 456, click_count=4)
                    self.page.evaluate(
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
                                }], "currency": "USD"
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
                        ''' % self.product)
                    try:
                        if self.status_code == "428":
                            logger.debug('wait for 70s..')
                            self.page.wait_for_timeout(70 * 1000)

                        if self.status_code == '200':
                            # 403 清零
                            count = 0

                        if self.status_code == "403":
                            count = count + 1
                            if count == 2:
                                logger.warning(f"Return Error:{self.status_code}")
                                self.break_flag = True
                                break

                            self.page.wait_for_timeout(5 * 1000)

                    except Exception as e:
                        logger.error(e)
                self.on_send()
                time.sleep(8)
            else:
                logger.error("Error: No data...")
                break

    def on_launch(self, local_server):
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(local_server)
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
            self.page = context.new_page()
            self.page.on('response', self.on_response)
            self.page.goto('https://www.ti.com.cn/store/ti/zh/p/product/?p=LM358DR', timeout=60 * 1000)
            # self.page.goto('https://www.ip138.com/')
            self.page.wait_for_timeout(5 * 1000)
            if 'Access Denied' in self.page.content():
                logger.warning('反爬-->IP风控->记录IP...')
                return
            self.on_handler()
            self.page.wait_for_timeout(2 * 1000)
            self.on_log()

    def on_run(self):
        try:
            local_server = on_local(self.profileId)
            if local_server:
                time.sleep(5)
                self.on_launch(local_server)

                logger.debug(f'Run Time: {self.runTime}s')
            else:
                pass

        except Exception as err:
            logger.error(err)
        finally:
            # 释放资源 profile
            on_local_stop(self.profileId)


if __name__ == '__main__':
    while True:
        try:
            profileId = db.rpop_lpush(REDIS_PROFILE_KEY, REDIS_PROFILE_KEY)
            if profileId:
                logger.debug(f'Get profileId: {profileId}')
                addToCart(profileId).on_run()
            else:
                logger.debug('指纹池为空...')
        except Exception as err:
            logger.error(err)
        time.sleep(2)
