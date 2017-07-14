# coding=utf-8
from adslproxy.api import server
from adslproxy.db import RedisClient

if __name__ == '__main__':
    redis = RedisClient(host='', password='')
    server(redis=redis)
