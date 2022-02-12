# -*- coding: utf-8 -*-

# @File  : trace_viewer.py
# @Author: zibang
# @Time  : 2月 05,2022
# @Desc     打开保存跟踪 playwright show-trace trace.zip
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context()
        # 在创建/导航页面之前开始跟踪
        await context.tracing.start(screenshots=True, snapshots=True)
        page = await context.new_page()
        await page.goto('https://www.ti.com.cn/')
        # https://www.ti.com.cn/
        await context.tracing.stop(path="trace.zip")
        await browser.close()

asyncio.run(main())