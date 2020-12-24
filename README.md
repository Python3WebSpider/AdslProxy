## 更新和优化(相对于崔大神原脚本)
1. 增加邮件提醒
2. 修正拨号间隔错误,原脚本的小bug,拨号间隔会是settings中的两倍
3. 增加拨号统计:每次拨出的IP放入redis,每拨一次value +1,如果是2会重新拨号,防止重复IP出现.如果需要可以重置下这个频次的值,参考proxy_reset.py.这个考虑到平台对IP的封禁并非长期,通常24小时后能解封
4. 增加拨号日志可视化监控,在本地运行proxy_stats.py读取远程拨号服务器日志并可视化展示拨号状态,比如这里的adsl1_proxy_quality_monitor.jpg
![image](https://raw.githubusercontent.com/chenxuzhen/AdslProxy/master/adsl1_proxy_quality_monitor.jpg)
5. 连续三次拨号无效IP系统会重启,因为这时候服务器已经不能继续拨号了
6. 从redis删除IP失败系统会重启,这个时候一般都是无法拨号了
7. 更新proxy检测方式为ping,拨号一次只需要6-7秒(当然和代理商有关系).这个针对单地区adsl vps特别有效,因为单地区拨号服务器带宽都没问题,拨出的IP都很稳定,只要能ping通都是高速可用的.个人建议
抛弃混拨服务器,带宽低而且拨号慢,不如多个地区的组合.本人测试过三家的拨号服务器,如有需要可提供免费建议.
8. service.sh放到/etc/init.d目录下, /bin/bash /etc/init.d/service.sh放在/etc/rc.local最后,系统重启后会自动运行拨号脚本.
9. 基于以上更新,脚本可以长期运行

Field                                     Value
czhen:proxy_password@125.121.137.70:3389  1

## 拨号主机设置

首先配置好代理，如使用 Squid，运行在 3128 端口，并设置好用户名和密码。

配置好代理之后，即可使用本工具定时拨号并发送至 Redis。

### 安装 ADSLProxy

```
pip3 install -U adslproxy
```

### 设置环境变量

```
# Redis 数据库地址和密码
export REDIS_HOST=
export REDIS_PASSWORD=
# 本机配置的代理端口
export PROXY_PORT=
# 本机配置的代理用户名，无认证则留空
export PROXY_USERNAME=
# 本机配置的代理密码，无认证则留空
export PROXY_PASSWORD=
```

### 执行

```
adslproxy send
```

运行结果：


```
pip3 install -U adslproxy
```

### 设置环境变量

```
# Redis 数据库地址和密码
export REDIS_HOST=
export REDIS_PASSWORD=
# 本机配置的代理端口
export PROXY_PORT=
# 本机配置的代理用户名，无认证则留空
export PROXY_USERNAME=
# 本机配置的代理密码，无认证则留空
export PROXY_PASSWORD=
```

### 执行

```
adslproxy send
```

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

