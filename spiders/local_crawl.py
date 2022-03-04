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
from db.mongo import insert_log, insert_history
from redis import StrictRedis
from config.start_profile import start_profile
from config.stop_profile import stop_profile
from pprint import pprint
from config.delete_profile import delete
from config.create_start_profiles import local_create
from config.stop_profile import stop_profile


class LocalCrawl(object):
    def __init__(self):
        self.profileId = None
        self.status_code = None
        self.proxy = None
        self.response = True

        # 测试profile
        self.db = StrictRedis(
            host='r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com',
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=6)

        # 测试 proxy
        self.db2 = StrictRedis(
            host='r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com',
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=7)

        # 生产 广播
        self.db3 = StrictRedis(
            host='r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com',
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=0)

        self.task = None
        self.product = None
        self.host_name = socket.getfqdn(socket.gethostname())
        self.number = None

    def on_log(self):
        """
        整理log --> Redis Log --> ES log:
        :return:
        """
        log = {
            'profileId': self.profileId,
            'host_name': self.host_name,
            'cts': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'status_code': self.status_code,
            'ip': self.proxy.get('ip'),
            'port': self.proxy.get('port'),
            'address': self.proxy.get('address'),
            'operator': self.proxy.get('operator'),
        }
        if self.db.rpush(REDIS_LOG_KEY, json.dumps(log)):
            logger.debug(f'Send log: {json.dumps(log, ensure_ascii=False)}')

    def on_publish(self, data):
        """
        发布广播/订阅  MongoLog(间隔log和成功log)
        :param data:
        :return:
        """
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
            if self.db3.publish(REDIS_CHANNEL, json.dumps(item)):
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

    def on_response(self, response):
        url = response.url
        if 'occservices/v2/ti/addtocart' in url:
            self.response = True
            self.status_code = str(response.status)
            if self.status_code == '200':
                data = response.json()
                logger.debug(f'Result: {data}')
                # ---> 广播/订阅
                self.on_publish(data)
                # ---> 加分 TODO
                if self.db.zincrby(REDIS_PROFILE_SCORE_KEY, +1, self.profileId):
                    pass

            logger.warning(f'Status: {self.status_code},{url}')
            self.on_log()

    def remove_proxy(self):
        if self.db2.delete(self.proxy.get('md5')):
            logger.debug('Access Denied: Remove proxy...')
        else:
            logger.error('Error: delete proxy')

    def execute_js(self, page):
        count_403 = 0
        count_200 = 0
        count_428 = 0  # 60s
        count_503 = 0  # 维护
        for num in range(1, 50):
            self.response = False
            content = page.content()
            if 'Access Denied' in content or 'doing site maintenance' in content or '未连接到互联网' in content:
                # 拒绝访问  移除proxy
                self.status_code = '404'
                self.remove_proxy()
                self.on_log()
                return

            data = self.db3.rpoplpush(REDIS_TASK_KEY, REDIS_TASK_KEY)
            if data:
                self.task = eval(data)
                logger.debug(f'Get Task: {self.task}')
                for self.product, self.number in self.task.items():
                    logger.debug(f'----> {num}')

                    if num % 3 == 0:
                        if not count_200 and not count_428 and count_403:
                            logger.warning('进入假死状态....')
                            return

                    # page.mouse.click(748, 456, click_count=1)
                    try:
                        page.click(selector='//div[@class="product-resources"]', click_count=1)
                        page.click(selector='//div[@class="product-header-info"]', click_count=2)
                        page.click(selector='//div[@class="product-header-info"]', click_count=4)
                        page.click(selector='//div[@class="product-header-info"]', click_count=3)
                    except Exception as err:
                        pass
                    # page.click(selector='//div[@class="add-to-cart"]', click_count=3)
                    # page.click(selector='//div[@class="add-to-cart"]', click_count=4)

                    # page.mouse.click(748, 456, click_count=3)
                    # page.mouse.click(748, 456, click_count=4)
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

                        if count_428 == 1 and count_200 == 4:
                            # 不需要继续访问
                            return

                        if count_403 == 2:
                            if not count_200:
                                return
                            return

                    if self.status_code == '404':
                        # 禁止访问 移除代理
                        self.remove_proxy()
                        return

                    if not self.response:
                        logger.warning('假死状态...')
                        return
                    page.wait_for_timeout(random.randint(6, 10))

            else:
                logger.error(f'No Task: {data}')

    def run(self):
        try:
            # 获取随机创建的配置文件并启动
            local_server = local_create()
            if local_server:
                self.profileId = local_server.get('profileId')
                host = local_server.get('host')
                self.proxy = local_server.get('proxy')
                if host and self.profileId:
                    time.sleep(5)  # 缓冲
                    with sync_playwright() as p:
                        browser = p.chromium.connect_over_cdp(endpoint_url=host)
                        context = browser.contexts[0]
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
                        page = context.pages[0]
                        page.on('response', self.on_response)
                        part = str(self.db.srandmember(REDIS_PRODUCT_KEY), encoding='utf-8')
                        page.goto(f"https://www.ti.com.cn/store/ti/zh/p/product/?p={part}", timeout=30 * 1000)  # 防止代理超时
                        # page.goto(f"https://www.baidu.com")
                        page.wait_for_timeout(5 * 1000)
                        self.execute_js(page)
                        page.wait_for_timeout(random.randint(2, 5) * 1000)
            else:
                logger.error("请检查代理...")
        except Exception as err:
            logger.error(err)
            if 'connect ECONNREFUSED' in str(err) or 'Timeout' in str(err):
                # 代理测试失败！
                # self.remove_proxy()
                time.sleep(3)

        finally:
            time.sleep(2)
            stop_profile(self.profileId)


if __name__ == '__main__':
    while 1:
        s_time = time.time()
        logger.warning('>>>>>>>' * 16)
        c = LocalCrawl()
        c.run()
        e_time = time.time()
        logger.debug('程序耗时 %ss' % int(e_time - s_time))
        time.sleep(1.5)
