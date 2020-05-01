# coding=utf-8
import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from adslproxy.db import RedisClient
from adslproxy.settings import *
import platform
from loguru import logger
from retrying import retry, RetryError
import redis

if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python version must be 2 or 3')


class Sender(object):
    """
    拨号并发送到 Redis
    """
    
    def extract_ip(self):
        """
        获取本机IP
        :param ifname: 网卡名称
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if not status == 0: return
        pattern = re.compile(DIAL_IFNAME + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
        result = re.search(pattern, output)
        if result:
            # 返回拨号后的 IP 地址
            return result.group(1)
    
    def test_proxy(self, proxy):
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
    
    @retry(retry_on_result=lambda x: x is not True, stop_max_attempt_number=10)
    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        logger.info(f'Removing {CLIENT_NAME}...')
        try:
            # 由于拨号就会中断连接，所以每次都要重新建立连接
            if hasattr(self, 'redis') and self.redis:
                self.redis.close()
            self.redis = RedisClient()
            self.redis.remove(CLIENT_NAME)
            logger.info(f'Removed {CLIENT_NAME} successfully')
            return True
        except redis.ConnectionError:
            logger.info(f'Remove {CLIENT_NAME} failed')
    
    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):
            logger.info(f'Successfully set proxy {proxy}')
    
    def loop(self):
        """
        循环拨号
        :return:
        """
        while True:
            logger.info('Starting dial...')
            self.run()
            time.sleep(DIAL_CYCLE)
    
    def run(self):
        """
        拨号主进程
        :return: None
        """
        logger.info('Dial started, remove proxy')
        try:
            self.remove_proxy()
        except RetryError:
            logger.error('Retried for max times, continue')
        # 拨号
        (status, output) = subprocess.getstatusoutput(DIAL_BASH)
        if not status == 0:
            logger.error('Dial failed')
        # 获取拨号 IP
        ip = self.extract_ip()
        if ip:
            logger.info(f'Get new IP {ip}')
            if PROXY_USERNAME and PROXY_PASSWORD:
                proxy = '{username}:{password}@{ip}:{port}'.format(username=PROXY_USERNAME,
                                                                   password=PROXY_PASSWORD,
                                                                   ip=ip, port=PROXY_PORT)
            else:
                proxy = '{ip}:{port}'.format(ip=ip, port=PROXY_PORT)
            time.sleep(10)
            if self.test_proxy(proxy):
                logger.info(f'Valid proxy {proxy}')
                # 将代理放入数据库
                self.set_proxy(proxy)
                time.sleep(DIAL_CYCLE)
            else:
                logger.error(f'Proxy invalid {proxy}')
        else:
            # 获取 IP 失败，重新拨号
            logger.error('Get IP failed, re-dialing')
            self.run()


def send(loop=True):
    sender = Sender()
    sender.loop() if loop else sender.run()


if __name__ == '__main__':
    send()
