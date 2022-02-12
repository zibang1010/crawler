# -*- coding: utf-8 -*-

# @File  : usage.py
# @Author: zibang
# @Time  : 2月 05,2022
# @Desc
import asyncio

from playwright.async_api import async_playwright
from pprint import pprint
from loguru import logger
import json


async def on_response(response):
    if '/v1/geoip' in response.url or '/v1/ua-parser' in response.url or '/ti/addtocart' in response.url:
        data = await response.text()
        stauts = response.status
        print('Response:', response.status, response.url)
        if stauts == 200:
            print(json.loads(data))
        elif stauts == 403:
            logger.warning('反爬了...')



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel='chrome',
            headless=False,
            slow_mo=50,
            # devtools=True,
            args=['--disable-blink-features=AutomationControlled'],
            # proxy={
            #     "server": "http://myproxy.com:3128",
            #     "username": "usr",
            #     "password": "pwd"
            # }
        )
        context = await browser.new_context(
            user_agent='Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
            # locale='zh-CN',
            # timezone_id='Asia/Shanghai',
            # geolocation={'longitude': 12.492507, 'latitude': 41.889938},
            # permissions=['geolocation'],
            # color_scheme='dark',
        )
        await context.add_cookies([
            {"name": "pf-accept-language", "value": "zh-CN", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_language", "value": "\"zh-CN\"", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_shipTo", "value": "\"CN\"", "domain": ".ti.com", "path": '/'},
            {"name": "user_pref_currency", "value": "\"CNY\"", "domain": ".ti.com", "path": '/'},
            {"name": "pf-accept-language", "value": "zh-CN", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_language", "value": "\"zh-CN\"", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_shipTo", "value": "\"CN\"", "domain": ".ti.com.cn", "path": '/'},
            {"name": "user_pref_currency", "value": "\"CNY\"", "domain": ".ti.com.cn", "path": '/'},
        ])
        page = await context.new_page(
            # viewport={
            #     'width': 1920,
            #     'height': 1080,
            # },
        )
        page.on('response', on_response)
        await page.goto('https://www.ti.com/store/ti/zh/p/product/?p=LM385M3X-1.2/NOPB', timeout=0)
        # await page.goto('https://bot.sannysoft.com/', timeout=0)
        print('Title:', await page.title())
        js = '() => window.navigator.webdriver'
        result = await page.evaluate(js)
        print('Navigator Result:', result)
        await page.wait_for_timeout(5 * 1000)
        try:
            await page.mouse.click(748, 456, click_count=1)
            await page.mouse.click(748, 460, click_count=2)
            await page.mouse.click(748, 470, click_count=3)
            await page.mouse.click(748, 456, click_count=4)
            await page.wait_for_timeout(2 * 1000)
            await page.evaluate(
                '''
                var data = {"cartRequestList":[{"opnId":"LM358DR","quantity":"2000","packageOption":null,"tiAddtoCartSource":"ti.com-quickcart", "customRefNo": ''}],"currency":"USD"};fetch("/occservices/v2/ti/addtocart", {
                    credentials: 'include',
                      headers: {
                          'Cache-Control': 'no-store, must-revalidate',
                          'Expires': '0',
                          'Content-Type': 'application/json'
                      },
                      method: 'POST',
                      body: JSON.stringify(data)
                  }).then(response => response.ok ? response.json() : error(response)).then(data => {
                      console.log(data)
                }).catch({})''')
        except Exception as err:
            print(err)
        await page.wait_for_timeout(20 * 1000)
        await page.screenshot(path='async_usage.png')
        await browser.close()


asyncio.run(main())
