# coding=utf-8
import redis
import random
from adslproxy.settings import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, redis_key=REDIS_KEY):
        """
        初始化Redis连接
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        :param redis_key: Redis 哈希表名
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.redis_key = redis_key
    
    def set(self, name, proxy):
        """
        设置代理
        :param name: 主机名称
        :param proxy: 代理
        :return: 设置结果
        """
        return self.db.hset(self.redis_key, name, proxy)
    
    def get(self, name):
        """
        获取代理
        :param name: 主机名称
        :return: 代理
        """
        return self.db.hget(self.redis_key, name)
    
    def count(self):
        """
        获取代理总数
        :return: 代理总数
        """
        return self.db.hlen(self.redis_key)
    
    def remove(self, name):
        """
        删除代理
        :param name: 主机名称
        :return: 删除结果
        """
        return self.db.hdel(self.redis_key, name)
    
    def names(self):
        """
        获取主机名称列表
        :return: 获取主机名称列表
        """
        return self.db.hkeys(self.redis_key)
    
    def proxies(self):
        """
        获取代理列表
        :return: 代理列表
        """
        return self.db.hvals(self.redis_key)
    
    def random(self):
        """
        随机获取代理
        :return:
        """
        proxies = self.proxies()
        return random.choice(proxies)
    
    def all(self):
        """
        获取字典
        :return:
        """
        return self.db.hgetall(self.redis_key)
    
    def close(self):
        """
        关闭 Redis 连接
        :return:
        """
        del self.db
