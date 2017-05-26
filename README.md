## 拨号主机设置

### 1.拨号上网

根据云主机拨号教程拨号上网，示例命令：

```
sh ppp.sh
adsl-start
```

### 2.配置代理

以CentOS上TinyProxy为例：

#### 安装

```
yum install -y epel-release
yum update -y
yum install -y tinyproxy
```

#### 配置

```
vi /etc/tinyproxy/tinyproxy.conf
```

取消注释

```
Allow 127.0.0.1
```

#### 启动

```
systemctl enable tinyproxy.service
systemctl restart  tinyproxy.service
```

#### 测试

```
curl -x IP:PORT www.baidu.com
```

IP为拨号主机IP，PORT为代理端口

#### 防火墙

如不能访问可能是防火墙问题，可以放行端口

```
iptables -I INPUT -p tcp --dport 8888 -j ACCEPT
```

或直接关闭防火墙

```
systemctl stop firewalld.service
```

### 3.安装Python3

#### CentOS

```
sudo yum groupinstall -y development tools
sudo yum install -y epel-release python34-devel  libxslt-devel libxml2-devel openssl-devel
sudo yum install -y python34 python34-setuptools
sudo easy_install-3.4 pip
```

#### Ubuntu

```
sudo apt-get install -y python3-dev build-essential libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev
sudo apt-get install -y python3 python3-pip
```

### 4.安装库

```
pip3 install redis tornado requests
```

### 5.Clone项目

```
git clone https://github.com/Germey/ADSLProxy.git
```

### 6.Redis

Redis数据库可以配置在某台固定IP的VPS，也可以购买Redis独立服务，如阿里云、腾讯云等。

### 7.修改配置

配置文件是 adslproxy/config.py

根据注释修改配置文件，主要修改要点如下：

> #### ADSL_BASH
>
> 拨号命令，不同主机可能不同，默认 adsl-stop;adsl-start
>
> #### PROXY_PORT
>
> 拨号主机代理端口，使用TinyProxy则默认为8888，使用Squid则默认3128，默认8888
>
> #### CLIENT_NAME
>
> 客户端唯一标识，不同拨号主机请设置不同的名称，默认adsl1
>
> #### ADSL_IFNAME 
>
> 拨号网卡名称，主要根据`ifconfig`命令获取拨号后该网卡的IP，默认ppp0
>
> #### REDIS_HOST
>
> Redis数据库地址，请修改为固定IP的Redis Host，默认localhost
>
> #### REDIS_PASSWORD
>
> Redis数据库密码，如无则填None，默认None
>
> #### REDIS_PORT
>
> Redis数据库端口，默认6379
>
> #### PROXY_KEY
>
> Redis代理池键名开头，默认为adsl

### 8.运行

```
python3 run.py
```

守护运行

```
(python3 run.py > /dev/null &)
```

## 程序使用

### 1.安装ADSLProxy

```
pip3 install adslproxy
```

### 2.Redis直连使用

```python
from adslproxy import RedisClient, server

client = RedisClient(host='', password='', port='')
random = client.random()
all = client.all()
first = client.first()
keys = client.keys()
count = client.count()


print('RANDOM:', random)
print('ALL:', all)
print('FIRST:', first)
print('KEYS:', keys)
print('COUNT:', count)
```

参数说明如下：

> #### host
>
> 即Redis数据库IP，默认localhost
>
> #### password
>
> 即Redis数据库密码，默认None
>
> #### port
>
> 即Redis数据库端口，默认6379
>
> #### proxy_key
>
> 即Redis数据库代理键名开头，默认adsl

方法说明如下：

> #### random()
>
> 从Redis代理池取随机代理
>
> #### all()
>
> 从Redis代理池取所有可用代理，返回list
>
> #### first()
>
> 从Redis代理池取第一个代理
>
> #### keys()
>
> 从Redis代理池取所有主机名称
>
> #### count()
>
> 从Redis代理池取所有可用主机数量

运行结果：

```python
RANDOM: 118.124.38.119:8888
ALL: [{'name': 'adsl2', 'proxy': '112.84.20.161:8888'}, {'name': 'adsl1', 'proxy': '118.124.38.119:8888'}]
FIRST: 112.84.20.161:8888
KEYS: ['adsl2', 'adsl1']
COUNT: 2
```

代码使用：

```python
import requests
proxies  = {
  'http': 'http://' + client.random()
}
r = requests.get('http://httpbin.org/get', proxies=proxies)
print(r.text)
```

### 3.API使用

```python
from adslproxy import RedisClient, server
client = RedisClient(host='', password='', port='')
server(client, port=8000)
```

运行后会在8000端口监听，访问API即可取到相应代理

获取代理：

```python
import requests

def get_random_proxy():
    try:
        url = 'http://localhost:8000/random'
        return requests.get(url).text
    except requests.exceptions.ConnectionError:
        return None
```

代码使用：

```python
import requests
proxies  = {
  'http': 'http://' + get_random_proxy()
}
r = requests.get('http://httpbin.org/get', proxies=proxies)
print(r.text)
```