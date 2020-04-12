# coding=utf-8
from environs import Env

env = Env()

# 拨号间隔，单位秒
DIAL_CYCLE = env.int('DIAL_CYCLE', 100)
# 拨号出错重试间隔
DIAL_ERROR_CYCLE = env.int('DIAL_ERROR_CYCLE', 5)
# 拨号命令
DIAL_BASH = env.str('DIAL_BASH', 'adsl-stop;adsl-start')
# 拨号网卡
DIAL_IFNAME = env.str('DIAL_IFNAME', 'ppp0')

# 客户端唯一标识
CLIENT_NAME = env.str('CLIENT_NAME', 'adsl1')

# Redis数据库IP
REDIS_HOST = env.str('REDIS_HOST', 'localhost')
# Redis数据库密码, 如无则填None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', 'foobared')
# Redis数据库端口
REDIS_PORT = env.int('REDIS_PORT', 6379)
# 代理池键名
REDIS_KEY = env.str('REDIS_KEY', 'adsl')

# 测试URL
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
# 测试最大失败次数
TEST_MAX_ERROR_COUNT = env.int('TEST_MAX_ERROR_COUNT', 10)
# 测试超时时间
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 20)
# 测试周期
TEST_CYCLE = env.int('TEST_CYCLE', 100)

# 服务器端口
SERVER_PORT = env.int('SERVER_PORT', 8425)
SERVER_HOST = env.str('SERVER_HOST', '0.0.0.0')

# 代理端口
PROXY_PORT = env.int('PROXY_PORT', 3128)
PROXY_USERNAME = env.str('PROXY_USERNAME', '')
PROXY_PASSWORD = env.str('PROXY_PASSWORD', '')
