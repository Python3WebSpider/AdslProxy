# coding=utf-8
# 采用了新的proxy验证方式,ping一次速度更快
# 修正了原来版本的几个小bug，比如拨号间隔原来实际上是设定值的两倍，如果proxy无效等待时间太长（改成6秒或者其他最低拨号间隔即可)
# IP与上次的相同会自动会重新拨号
# 连续三次拨号失败自动重启(ADSL VPS这种情况下基本上等于无法继续拨号了)
# 增加邮件提醒
# 每次拨出的IP存入redis,方便统计和去重.IP出现2次以上会重新拨号
# 从redis移除移除IP失败立即重启,这个情况下VPS通常已经无法拨号了

import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from adslproxy.db import RedisClient
from adslproxy.settings import *
from adslproxy.sendemail import EmailClient
import platform
from loguru import logger
from retrying import retry, RetryError
import redis
import datetime
import os
import random

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
    ip_pre = ''
    invalid_ip_list = []
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
        :ping一次测试速度更快，只需要几十毫秒
        """
        # try:
        #    response = requests.get(TEST_URL, proxies={
        #        'http': 'http://' + proxy,
        #        'https': 'https://' + proxy
        #    }, timeout=TEST_TIMEOUT)
        #    if response.status_code == 200:
        #        logger.info(f'proxy: {proxy}')
        #        return True
        #except (ConnectionError, ReadTimeout):
        #    return False
        con = os.system('ping -c 1 www.baidu.com')
        print(con)
        if con==0:
            return True
        else:
            return False
    
    @retry(retry_on_result=lambda x: x is not True, stop_max_attempt_number=10)
    def remove_proxy(self):
        """
        移除代理
        :return: None
        通常情况下，连续拨号失败几次就需要重启机器了，这时候VPS已经无法成功拨号连接互联网了
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
            logger.error('删除IP失败!从代理池删除IP并重启系统.......')
            os.system('/usr/sbin/shutdown -r now')      
    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        self.db = RedisClient().db
        # 哈希表来统计拨号VPS的IP
        if not self.db.hexists('dialed_IPs', proxy):            
            self.db.hset('dialed_IPs', proxy, 1)
            # 往IP池里插入数据
            if self.redis.set(CLIENT_NAME, proxy):
                logger.info(f'Successfully set proxy {proxy}')             
            return True
        else:
            num = int(self.db.hget('dialed_IPs', proxy))
            logger.info(f'{proxy} in proxy pools {num} times already')
            if num <2:
                self.db.hset('dialed_IPs', proxy, num+1)
                # 往IP池里插入数据
                if self.redis.set(CLIENT_NAME, proxy):
                    logger.info(f'Successfully set proxy {proxy}')   
                return True
            else:
                
                return False
    
    def loop(self):
        """
        循环拨号
        :return:
        """
        while True:
            logger.info('Starting dial...')
            now = datetime.datetime.now()
            if now.minute%5==0 and now.second==0:
                logger.info('dial time: %s', now.strftime('%Y-%m-%d %H:%M:%S'))
            
            new_ip = self.run()
            if new_ip != self.ip_pre:
                
                self.ip_pre = new_ip
            else:
                logger.info('IP和上次相同，等待重播......')
                self.run()
    
    def run(self):
        """
        拨号主进程
        :return: None
        """
        #time.sleep(10) #给正在运行的作业留出时间结束
        logger.info('Dial started, remove proxy')
        try:
            self.remove_proxy()
        except RetryError:
            logger.error('Retried for max times, continue')
            self.emailclient = EmailClient()
            self.emailclient.notification(f'failed too many times {datetime.datetime.now().strftime("%m-%d-%H-%M")}', f'Warning{random.randint(1000,299999)}: 22457 retry error {datetime.datetime.now().strftime("%m-%d-%H-%M")}')

        for i in range(3):
            # 拨号
            (status, output) = subprocess.getstatusoutput('adsl-stop;adsl-start')
            if not status == 0:
                logger.error('Dial failed')
                time.sleep(20)
            else:
                break 
        if not status == 0:
            print('连续三次拨号失败,系统重启......')
            os.system('sudo reboot')
            
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
            # time.sleep(1)
            if self.test_proxy(proxy):
                logger.info(f'Valid proxy {proxy}')
                self.ip_validity_statistics('valid')
                # 将代理放入数据库
                if self.set_proxy(proxy):
                    time.sleep(DIAL_CYCLE)                                                      
            else:
                logger.error(f'Proxy invalid {proxy}')
                # 连续三次拨号无效
                self.ip_validity_statistics('invalid')                                   
                if len(self.invalid_ip_list) > 0:
                    if self.invalid_ip_list.count('invalid') == 3:
                        logger.error('连续三次拨号失败!从代理池删除IP并重启系统.......')
                        self.remove_proxy()
                        os.system('/usr/sbin/shutdown -r now')                        
                time.sleep(DIAL_ERROR_CYCLE)
        else:
            # 获取 IP 失败，重新拨号
            logger.error('Get IP failed, re-dialing')
            ip = ''
            time.sleep(DIAL_ERROR_CYCLE)
            self.run()
        return ip
    def ip_validity_statistics(self, ele):
        if len(self.invalid_ip_list) < 3:
            self.invalid_ip_list.append(ele)
        else:
            self.invalid_ip_list.pop(0)
            self.invalid_ip_list.append(ele)
                    
def send(loop=True):
    sender = Sender()
    sender.loop() if loop else sender.run()


if __name__ == '__main__':
    try:
        emailclient = EmailClient()
        emailclient.notification(f'{datetime.datetime.now().strftime("%m-%d-%H:%M")} {random.randint(300, 9999)} proxy restarted', f'{datetime.datetime.now().strftime("%m-%d-%H:%M")} 22457 proxyserver is back {random.randint(300, 9999)}')
        print('email test success')
    except Exception as e:
        print(e)
    while True:
        con = os.system('ping -c 1 www.baidu.com')
        print(con)
        if con==0:
            time.sleep(6)
            send()
            break
        else:
            time.sleep(1)

