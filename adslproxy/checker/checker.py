import time
from requests import ReadTimeout
from adslproxy.db import RedisClient
import requests
from adslproxy import settings
from collections import defaultdict
from loguru import logger


class Checker(object):
    
    def __init__(self):
        self.db = RedisClient()
        self.counts = defaultdict(int)
    
    def check(self, proxy):
        """
        测试代理，返回测试结果
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            response = requests.get(settings.TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=settings.TEST_TIMEOUT)
            logger.debug(f'Using {proxy} to test {settings.TEST_URL}...')
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False
    
    def run(self):
        """
        测试一轮
        :return:
        """
        proxies = self.db.all()
        logger.info(f'Try to get all proxies {proxies}')
        for name, proxy in proxies.items():
            # 检测无效
            if not self.check(proxy):
                logger.info(f'Proxy {proxy} invalid')
                self.counts[proxy] += 1
            else:
                logger.info(f'Proxy {proxy} valid')
            count = self.counts.get(proxy) or 0
            logger.debug(f'Count {count}, TEST_MAX_ERROR_COUNT {settings.TEST_MAX_ERROR_COUNT}')
            if count >= settings.TEST_MAX_ERROR_COUNT:
                self.db.remove(name)
    
    def loop(self):
        """
        循环测试
        :return:
        """
        while True:
            logger.info('Check for infinite')
            self.run()
            logger.info(f'Tested, sleeping for {settings.TEST_CYCLE}s...')
            time.sleep(settings.TEST_CYCLE)


def check(loop=True):
    """
    check proxies
    :param loop:
    :return:
    """
    if not loop:
        settings.TEST_MAX_ERROR_COUNT = 1
    checker = Checker()
    checker.loop() if loop else checker.run()


if __name__ == '__main__':
    check()
