
# coding=utf-8
#!/bin/bash
# service.sh文件放在/etc/init.d目录下并且在/etc/rc.local最后添加bash /etc/init.d/service.sh,系统重启后会自动运行拨号脚本.
while ! ping -c1 www.baidu.com &>/dev/null
        do echo "Ping Fail - `date`"
        sleep 6
        adsl-start
done
export PATH="$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
nohup /usr/bin/python3 /root/AdslProxy/adslproxy/sender/sender.py >> /root/proxy_reboot.log 2>&1 &
