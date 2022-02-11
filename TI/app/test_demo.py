# -*- coding: utf-8 -*-

# @File  : test_demo.py
# @Author: zibang
# @Time  : 2月 11,2022
# @Desc  :
from test_proxy import get_kdl_proxy
from playwright.sync_api import sync_playwright

proxy = get_kdl_proxy()
print('proxy', proxy)
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=[],
        proxy = {'server': ''}
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.ip138.com/')
    page.wait_for_timeout(10 * 100)
