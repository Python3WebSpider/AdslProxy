# coding=utf-8
import os

# 拨号间隔
ADSL_CYCLE = 100

# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 5

# ADSL命令
ADSL_BASH = 'pppoe-stop;adsl-start'

# 代理运行端口
PROXY_PORT = 8888

# 客户端唯一标识
CLIENT_NAME = os.getenv('CLIENT_NAME', 'adsl1')

# 拨号网卡
ADSL_IFNAME = 'ppp0'

# Redis数据库IP
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

# Redis数据库密码, 如无则填None
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'foobared')

# Redis数据库端口
REDIS_PORT = int(os.getenv('REDIS_PORT', 'localhost'))

# 代理池键名
PROXY_KEY = 'adsl'

# 测试URL
TEST_URL = 'http://www.baidu.com'

# 测试超时时间
TEST_TIMEOUT = 20

# API端口
API_PORT = 8000
