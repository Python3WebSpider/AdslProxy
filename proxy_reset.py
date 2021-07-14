# coding=utf-8
# 因为网站封禁IP并非长期,24小时后可以运行该脚本减小拨号出现次数的值,提高IP利用率
import redis
import random
import time
import redis
import re

client = redis.Redis(host=REDIS_HOST, port=7379, db=0, password=REDIS_PASSORD)
client.hvals('dialed_IPs')
client.hkeys('dialed_IPs')
for i in client.hkeys('dialed_IPs'):
    num = int(client.hget('dialed_IPs', i))
    if num >=1:
        client.hset('dialed_IPs', i, num-1)
