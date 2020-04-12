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

此时有效代理就会发送到 Redis。

