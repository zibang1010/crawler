# -*- coding: utf-8 -*-

# @File  : test_demo2.py
# @Author: zibang
# @Time  : 2月 13,2022
# @Desc
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('http://www.baidu.com')
    page.goto('http://www.sogou.com')
    page.go_back()
    page.wait_for_timeout(20 * 1000)
