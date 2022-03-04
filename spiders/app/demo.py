# -*- coding: utf-8 -*-

# @File  : demo.py
# @Author: zibang
# @Time  : 3月 04,2022
# @Desc  :

from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.connect_over_cdp('http://127.0.0.1:18682')
    context = browser.contexts[0]

    # Open new page
    page = context.pages[0]

    page.goto("https://www.ti.com.cn/store/ti/zh/p/product/?p=DLP3020AFQRQ1")
    page.wait_for_timeout(5 * 1000)

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
