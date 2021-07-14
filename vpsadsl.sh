
#/usr/bin/bash
sed -i "s/Port 3389/#Port 3389/" /etc/ssh/sshd_config
service sshd restart

# 时间同步很重要，不然没法判断代理IP存活时间
cd /etc/yum.repos.d/

mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup
# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo 
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
curl -O  http://mirrors.aliyun.com/repo/epel-7.repo
sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo

yum clean all
yum makecache
cd ~/
yum install -y ntpdate
yum -y install wget
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
yes | cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ntpdate cn.pool.ntp.org
crontab -l >/tmp/crontab.bak
echo "*/10 * * * * /usr/sbin/ntpdate cn.pool.ntp.org | logger -t NTP" >> /tmp/crontab.bak
crontab /tmp/crontab.bak

yum update -y
yum install epel-release -y
yum install --enablerepo="epel" ufw -y
yum install python3 -y

# 配置pip国内源
mkdir ~/.pip && cd .pip && touch pip.conf
echo "
[global]
index-url = https://mirrors.aliyun.com/pypi/simple
" > ~/.pip/pip.conf
cd ~/

# 安装denyhosts
wget http://soft.vpser.net/lnmp/lnmp1.4beta.tar.gz && tar zxf lnmp1.4beta.tar.gz && cd lnmp1.4/tools/ && bash denyhosts.sh

# 安装squid
yum install squid httpd -y
echo "
#
# Recommended minimum configuration:
#

# Example rule allowing access from your local networks.
# Adapt to list your (internal) IP networks from where browsing
# should be allowed
acl localnet src 10.0.0.0/8	# RFC1918 possible internal network
acl localnet src 172.16.0.0/12	# RFC1918 possible internal network
acl localnet src 192.168.0.0/16	# RFC1918 possible internal network
acl localnet src fc00::/7       # RFC 4193 local private network range
acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines

acl SSL_ports port 443
acl Safe_ports port 80		# http
acl Safe_ports port 21		# ftp
acl Safe_ports port 443		# https
acl Safe_ports port 70		# gopher
acl Safe_ports port 210		# wais
acl Safe_ports port 1025-65535	# unregistered ports
acl Safe_ports port 280		# http-mgmt
acl Safe_ports port 488		# gss-http
acl Safe_ports port 591		# filemaker
acl Safe_ports port 777		# multiling http
acl CONNECT method CONNECT

#
# Recommended minimum Access Permission configuration:
#
# Deny requests to certain unsafe ports
http_access allow !Safe_ports

# Deny CONNECT to other than secure SSL ports
http_access allow CONNECT !SSL_ports

# Only allow cachemgr access from localhost
http_access allow localhost manager
http_access deny manager

# We strongly recommend the following be uncommented to protect innocent
# web applications running on the proxy server who think the only
# one who can access services on "localhost" is a local user
#http_access deny to_localhost

#
# INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS
#

# Example rule allowing access from your local networks.
# Adapt localnet in the ACL section to list your (internal) IP networks
# from where browsing should be allowed
http_access allow localnet
http_access allow localhost

# And finally deny all other access to this proxy
# http_access allow all
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm czhen's squid server
auth_param basic credentialsttl 2 hours
acl czhen proxy_auth REQUIRED
http_access allow czhen
#http_access deny all

# Squid normally listens to port 3128
http_port 3389

# Uncomment and adjust the following to add a disk cache directory.
#cache_dir ufs /var/spool/squid 100 16 256

# Leave coredumps in the first cache dir
coredump_dir /var/spool/squid

#
# Add any of your own refresh_pattern entries above these.
#
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern .		0	20%	4320

#include /etc/squid/peers.conf

# 配置高匿，不允许设置任何多余头信息，保持原请求header，可在最后加上此两句
request_header_access Via deny all
request_header_access X-Forwarded-For deny all
" > /etc/squid/squid.conf
sudo systemctl enable squid
service squid start

# 配置ufw
# yes | ufw enable 
# ufw default allow outgoing 
# ufw default deny incoming 
# ufw allow http 
# ufw allow 22
# ufw allow 5900
# ufw allow 3389
# ufw allow from 
# ufw status

# 配置github访问
# set up hosts for github visit. GFW blocked the parsing of these DNS
echo "
# GitHub Start
140.82.113.4      github.com
140.82.113.4      gist.github.com
140.82.114.5      api.github.com
185.199.111.153   assets-cdn.github.com
199.232.96.133    raw.githubusercontent.com
199.232.96.133    gist.githubusercontent.com
199.232.96.133    cloud.githubusercontent.com
199.232.96.133    camo.githubusercontent.com
199.232.96.133    avatars0.githubusercontent.com
199.232.96.133    avatars1.githubusercontent.com
199.232.96.133    avatars2.githubusercontent.com
199.232.96.133    avatars3.githubusercontent.com
199.232.96.133    avatars4.githubusercontent.com
199.232.96.133    avatars5.githubusercontent.com
199.232.96.133    avatars6.githubusercontent.com
199.232.96.133    avatars7.githubusercontent.com
199.232.96.133    avatars8.githubusercontent.com
# GitHub End
" >> /etc/hosts
cd /root/AdslProxy/
read -p "Enter adsl client name. eg. adsl1 or adsl2: " adsl
sudo sed -i "s/adsl1/"$adsl"/" /root/AdslProxy/adslproxy/settings.py
sudo sed -i "s/22457/"$adsl"/" /root/AdslProxy/adslproxy/sender/sender.py
yes | python3 /root/AdslProxy/setup.py install
echo 'copy service.sh to /etc/init.d'
cp /root/AdslProxy/service.sh /etc/init.d/ && chmod 777 /etc/init.d/service.sh
echo 'bash /etc/init.d/service.sh' >> /etc/rc.local
sudo service firewalld start
sudo firewall-cmd --permanent --add-port=3128/tcp
firewall-cmd --zone=public --add-port=22/tcp --permanent
firewall-cmd --zone=public --add-port=30050/tcp --permanent

firewall-cmd --reload
sudo service firewalld restart
sudo service squid restart
sudo systemctl enable firewalld
echo 'you need to RUN htpasswd -c /etc/squid/passwd czhen   to set passwd for squid'
echo 'check if squid proxy works and start adslproxy send.'
htpasswd -c /etc/squid/passwd czhen
echo 'double check adslproxy settings.py. make sure adsl client name is setup as expected'
