## 拨号主机设置

首先配置好代理，如使用 Squid，运行在 3128 端口，并设置好用户名和密码。

配置好代理之后，即可使用本工具定时拨号并发送至 Redis。

### 安装 ADSLProxy

```
pip3 install -U adslproxy
```

### 设置环境变量

```
# Redis 数据库地址、端口和密码
export REDIS_HOST=
export REDIS_PORT=
export REDIS_PASSWORD=
# 拨号云主机配置的代理端口
export PROXY_PORT=
# 拨号云主机的代理用户名，无认证则留空
export PROXY_USERNAME=
# 拨号云主机配置的代理密码，无认证则留空
export PROXY_PASSWORD=
```

### 执行

```
adslproxy send
```

运行结果：

运行结果：

```
2020-04-13 01:39:30.811 | INFO     | adslproxy.sender.sender:loop:90 - Starting dial...
2020-04-13 01:39:30.812 | INFO     | adslproxy.sender.sender:run:99 - Dial Started, Remove Proxy
2020-04-13 01:39:30.812 | INFO     | adslproxy.sender.sender:remove_proxy:62 - Removing adsl1...
2020-04-13 01:39:30.893 | INFO     | adslproxy.sender.sender:remove_proxy:69 - Removed adsl1 successfully
2020-04-13 01:39:37.034 | INFO     | adslproxy.sender.sender:run:108 - Get New IP 113.128.9.239
2020-04-13 01:39:42.221 | INFO     | adslproxy.sender.sender:run:117 - Valid proxy 113.128.9.239:3389
2020-04-13 01:39:42.458 | INFO     | adslproxy.sender.sender:set_proxy:82 - Successfully Set Proxy
2020-04-13 01:43:02.560 | INFO     | adslproxy.sender.sender:loop:90 - Starting dial...
2020-04-13 01:43:02.561 | INFO     | adslproxy.sender.sender:run:99 - Dial Started, Remove Proxy
2020-04-13 01:43:02.561 | INFO     | adslproxy.sender.sender:remove_proxy:62 - Removing adsl1...
2020-04-13 01:43:02.630 | INFO     | adslproxy.sender.sender:remove_proxy:69 - Removed adsl1 successfully
2020-04-13 01:43:08.770 | INFO     | adslproxy.sender.sender:run:108 - Get New IP 113.128.31.230
2020-04-13 01:43:13.955 | INFO     | adslproxy.sender.sender:run:117 - Valid proxy 113.128.31.230:3389
2020-04-13 01:43:14.037 | INFO     | adslproxy.sender.sender:set_proxy:82 - Successfully Set Proxy
2020-04-13 01:46:34.216 | INFO     | adslproxy.sender.sender:loop:90 - Starting dial...
2020-04-13 01:46:34.217 | INFO     | adslproxy.sender.sender:run:99 - Dial Started, Remove Proxy
2020-04-13 01:46:34.217 | INFO     | adslproxy.sender.sender:remove_proxy:62 - Removing adsl1...
2020-04-13 01:46:34.298 | INFO     | adslproxy.sender.sender:remove_proxy:69 - Removed adsl1 successfully
```

此时有效代理就会发送到 Redis。

