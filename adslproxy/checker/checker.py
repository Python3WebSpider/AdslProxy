import time
from requests import ReadTimeout
from adslproxy.db import RedisClient
import requests
from adslproxy.settings import *
from collections import defaultdict


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
            response = requests.get(TEST_URL, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False
    
    def run(self):
        proxies = self.db.all()
        for proxy in proxies:
            # 检测无效
            if not self.check(proxy):
                self.counts[proxy] += 1
            if self.counts.get(proxy) > TEST_MAX_ERROR_COUNT:
                self.db.remove(proxy)
    
    def loop(self):
        while True:
            self.run()
            time.sleep(TEST_CYCLE)


def check(loop=False):
    """
    check proxies
    :param loop:
    :return:
    """
    checker = Checker()
    checker.loop() if loop else checker.run()


if __name__ == '__main__':
    check()
