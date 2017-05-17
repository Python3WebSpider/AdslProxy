import redis
import random
from server.config import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.db = redis.Redis(host=host, port=port, password=REDIS_PASSWORD)
        self.proxy_key = PROXY_KEY

    def get(self):
        return self.db.lindex(self.proxy_key, 0)

    def add(self, proxy):
        self.remove(proxy)
        return self.db.lpush(self.proxy_key, proxy)

    def remove(self, proxy):
        return self.db.lrem(self.proxy_key, proxy, 0)

    def flush(self):
        return self.db.flushall()

    def all(self):
        return [proxy.decode('utf-8') for proxy in self.db.lrange(self.proxy_key, 0, -1)]


if __name__ == '__main__':
    client = RedisClient()
    client.add('abc')
    client.add('abc2')
    client.add('abc3')
    client.add('abc4')
    client.remove('abc4')
    result = client.get()
    print(client.all())
    print(result)
