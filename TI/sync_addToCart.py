# -*- coding: utf-8 -*-

# @File  : addToCart.py
# @Author: zibang
# @Time  : 1月 20,2022
# @Desc  :
import random

from playwright.sync_api import sync_playwright
import datetime
from loguru import logger
import time

part_list = ['OPA2171AIDGKR',
             'TPS53219ARGTT',
             'TPS59641RSLT',
             'SN74AUP1T34DRYR',
             'TPS24751RUVR',
             'TPS65218D0RSLR',
             'TPS40170QRGYRQ1',
             'TPS53511RGTR',
             'TPS2557DRBR',
             'DRV8304HRHAR',
             'TL431BQDBZRQ1',
             'LM53601MQDSXTQ1',
             'TLV62585RWTT',
             'TLC5926IPWPR',
             'LM94023BITMX/NOPB',
             'LM3886TF/NOPB',
             'CSD87335Q3D',
             'TPS53319DQPT',
             'TPS54308DDCT',
             'TPS548D22RVFT', ]


def on_request(request):
    print('Request:', request.method, request.status, request.url)


def on_response(response):
    # if '/occservices/v2/ti/addtocart' in response.url:
    #     if response.status == 200:
    #         logger.debug(f'Statue {response.status}: {response.url}')
    #         logger.debug(response.text())
    #     elif response.status == 403:
    #         logger.error(f'Forbidden {response.status}: {response.url}')
    #     elif response.status == 428:
    #         logger.error(f'Statue {response.status}: {response.url}')
    #     elif response.status == 400:
    #         logger.error(f'Statue {response.status}: {response.url}')
    #     elif '/v1/geoip' in response.url or '/v1/ua-parser' in response.url:
    #         data = response.json()
    #         print('Response:', response.status, response.url, data)

    print('Response:', response.status, response.url)


def run():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False,
                channel="chrome",
                # ignore_default_args=['--enable-automation'],
                args=['--disable-blink-features=AutomationControlled'],

            )
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
            page = browser.new_page()
            # page.on('response', on_response)
            page.on("request", lambda request: print(">>", request.method, request.status,request.url))
            page.goto("https://www.ti.com/store/ti/zh/p/product/?p=LM385M3X-1.2/NOPB", timeout=0)
            # page.goto("https://fingerprintjs.github.io/fingerprintjs/", timeout=0)
            logger.debug('加载完成...')
            # page.wait_for_timeout(5 * 1000)
            # try:
            #     page.mouse.click(748, 456, click_count=1)
            #     page.mouse.click(748, 460, click_count=2)
            #     page.mouse.click(748, 470, click_count=3)
            #     page.mouse.click(748, 456, click_count=4)
            #     page.wait_for_timeout(2 * 1000)
            #     page.evaluate(
            #         '''
            #         var aa = {"cartRequestList":[{"opnId":"%s","quantity":"2000","packageOption":null,"tiAddtoCartSource":"ti.com-quickcart", "customRefNo": ''}],"currency":"USD"};fetch("/occservices/v2/ti/addtocart", {
            #             credentials: 'include',
            #               headers: {
            #                   'Cache-Control': 'no-store, must-revalidate',
            #                   Expires: '0',
            #                   'Content-Type': 'application/json'
            #               },
            #               method: 'POST',
            #               body: JSON.stringify(aa)
            #           }).then(response => response.ok ? response.json() : error(response)).then(data => {
            #               console.log(data)
            #         }).catch({})''' % random.choice(part_list))
            # except Exception as err:
            #     logger.error(err)
            page.wait_for_timeout(20 * 1000)
            page.close()
            browser.close()
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    run()
    endtime = datetime.datetime.now()
    logger.debug(f"完成时间: {(endtime - starttime).seconds} s")
    time.sleep(5)
