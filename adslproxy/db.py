import redis
import random
from adslproxy.config import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, proxy_key=PROXY_KEY):
        self.db = redis.Redis(host=host, port=port, password=password)
        self.proxy_key = proxy_key
    
    def key(self, name):
        return '{key}:{name}'.format(key=self.proxy_key, name=name)
    
    def set(self, name, proxy):
        return self.db.set(self.key(name), proxy)

    def get(self, name):
        return self.db.get(self.key(name)).decode('utf-8')

    def count(self):
        return len(self.db.keys(self.key('*')))
    
    def remove(self, name):
        return self.db.delete(self.key(name))

    def keys(self):
        return [key.decode('utf-8').replace(self.proxy_key + ':', '') for key in self.db.keys(self.key('*'))]

    def all(self):
        keys = self.keys()
        proxies = [{'name': key, 'proxy': self.get(key)} for key in keys]
        return proxies

    def random(self):
        items = self.all()
        return random.choice(items).get('proxy')

    def list(self):
        keys = self.keys()
        proxies = [self.get(key) for key in keys]
        return proxies

    def first(self):
        return self.get(self.keys()[0])
