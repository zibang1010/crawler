# -*- coding: utf-8 -*-

# @File  : cart.py
# @Author: zibang
# @Time  : 3月 05,2022
# @Desc  :
from playwright.sync_api import sync_playwright
import time
from loguru import logger
from settings import *


class AddToCart(object):
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            ignore_default_args=[
                '--enable-automation'
            ],
            devtools=True
        )

    def on_error(self):
        pass

    def on_success(self):
        pass

    def on_execute(self):
        pass

    def start_requests(self):
        # while True:
        # url = 'https://www.ip138.com/'
        url = 'https://www.ti.com.cn/product/cn/OPA2328?jktype=homepageproduct'
        start_time = time.time()
        context = self.browser.new_context(
            # proxy={
            #     'server': 'http://119.41.199.171:17409',
            #     # "bypass": 'HTTP',
            #     "username": PROXY_USERNAME,
            #     "password": PROXY_PASSWORD,
            # }
        )
        # context.add_init_script(path='/Users/zibang/Documents/jxgl/crawler/spiders/fingerprint.js')
        page = context.new_page()
        # page.goto('https://www.ti.com.cn/product/cn/OPA2328?jktype=homepageproduct', timeout=60 * 1000,
        #           referer='https://www.ti.com.cn')
        page.goto(url, timeout=60 * 1000)
        page.add_init_script("""
        var browser = "";
        for (var name in navigator){
            browser += name;
        }
        var browser ="<h2>navigator对象的各项属性值</h2><hr/>";//声明输出变量
for(var proname in navigator){//利用for循环，声明变量proname获取并存储navigator对象的所有属性值
browser +="<b>"+ proname +"</b>:"+ navigator[proname]+"<br/>";//利用‘+=’运算符实现连续输出
}
document.write(browser);
        """)
        content = page.content()
        # with open('../response.html', 'a') as f:
        #     f.write(content)
        # page.screenshot(path='../response.jpg', full_page=True)
        end_time = time.time()
        logger.debug('Run Time: %ss' % int(end_time - start_time))
        time.sleep(5000)
        page.close()

    def __del__(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == '__main__':
    atc = AddToCart()
    atc.start_requests()
