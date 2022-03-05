# -*- coding: utf-8 -*-

# @File  : local_cart.py
# @Author: zibang
# @Time  : 3月 05,2022
# @Desc  :
# -*- coding: utf-8 -*-

# @File  : cart.py
# @Author: zibang
# @Time  : 3月 05,2022
# @Desc  :
from playwright.sync_api import sync_playwright
import time
from loguru import logger


class AddToCart(object):
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = None
        self.response_status_code = None

    def on_error(self):
        pass

    def on_success(self):
        pass

    def on_execute(self):
        pass

    def on_response(self):
        pass

    def on_remove(self):
        """
        移除代理
        :return:
        """
        logger.warning('[Access Denied] remove proxy')

    def start_requests(self):
        """
        本地api连接，异常重试
        :return:
        """
        try:
            start_time = time.time()
            context = self.playwright.chromium.connect_over_cdp(
                endpoint_url='http://192.168.1.5:35000',
                timeout=60 * 1000
            )
            page = context.new_page()
            page.goto('https://www.ti.com.cn/product/cn/OPA2328?jktype=homepageproduct', timeout=60 * 1000,
                      referer='https://www.ti.com.cn')

            content = page.content()
            # 判断404
            if 'Access Denied' in content or 'doing site maintenance' in content or '未连接到互联网' in content:
                # 拒绝访问
                self.on_remove()
                self.response_status_code = '404'
                return

            end_time = time.time()
            logger.debug('Run Time: %ss' % int(end_time - start_time))
            page.close()
        except Exception as err:
            logger.error(err)
            raise
            # time.sleep(10)

    def run(self):
        pass

    def __del__(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == '__main__':
    atc = AddToCart()
    atc.start_requests()
