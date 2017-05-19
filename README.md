# ADSL拨号服务器代理设置

## 服务端

服务端即远程主机

### 安装Python

Python3版本


### 安装库

```
pip3 install redis tornado
```

### Clone项目

```
git clone https://github.com/Germey/ADSLProxyPool.git
```

### 安装Redis

安装Redis并启动服务

### 修改配置

```
cd server
vi config.py
```

根据注释修改配置文件

### 运行

根目录运行

```
python3 server.py
```

## 客户端

客户端即拨号主机

### 安装Python

Python3版本


### 安装库

```
pip3 install requests
```

### Clone项目

```
git clone https://github.com/Germey/ADSLProxyPool.git
```


### 修改配置

```
cd server
vi config.py
```

根据注释修改配置文件

### 运行

根目录运行

```
python3 client.py
```