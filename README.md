# ADSL拨号服务器代理设置

## 服务端

服务端即远程主机

### 安装Python

Python3


### 安装库

```
pip3 install redis tornado requests
```

### Clone项目

```
git clone https://github.com/Germey/ADSLProxy.git
```

### 安装Redis

安装Redis并启动服务

### 修改配置

```
cd adslproxy
vi config.py
```

根据注释修改配置文件

### 运行

#### 拨号程序运行

```
python3 run.py
```

#### API运行


```
python3 api.py
```




