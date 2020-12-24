%matplotlib qt
import os
import re
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
import time
import numpy as np

# %matplotlib notebook

# log_file = r'E:\splash\AdslProxy\proxy_reboot.log'
log_file = '/root/proxy_reboot.log'
class PROXY_MON(object):
    def __init__(self, hostname, port, username, password, adsl_num):
        #服务器信息，主机名（IP地址）、端口号、用户名及密码
        self.adsl=adsl_num
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password, compress=True, timeout=10)
        self.sftp_client = client.open_sftp()        
    def log_check(self):
        try:    
            with self.sftp_client.open(log_file, 'r') as file:
                contents = file.read().decode()
                print(contents[-200:])
                dial_times = re.findall('Dial started', contents)
                print(f'total IPs dialed: {len(dial_times)}')
                repeat_ips = re.findall('2 times', contents)
                print(f'num of repeat IPs: {len(repeat_ips)}')
                success_ips = re.findall('Successfully set', contents)
                print(f'num of successful IPs set to redis: {len(success_ips)}')
                dial_failed = re.findall('Get IP failed', contents)
                print(f'num of failed dialing: {len(dial_failed)}')
                valid_ip = re.findall('Valid proxy', contents)
                print(f'num of Valid proxy IPs: {len(valid_ip)}')
                invalid_ip = re.findall('Proxy invalid', contents)
                print(f'num of invalid proxy IPs: {len(invalid_ip)}')
                consec_ip_repeat = re.findall('IP和上次相同', contents)
                print(f'num of consecutive repeat IP dialed: {len(consec_ip_repeat)}')
                reboot_ip_del_failure = re.findall('删除IP失败!从代理池删除IP并重启系统', contents)
                print(f'num of reboot due to deleltion failure from redis: {len(reboot_ip_del_failure)}') 
                reboot_ip_3dial_failure = re.findall('连续三次拨号失败!从代理池删除IP并重启系统', contents)
                print(f'num of reboot due to 3 consecutive dial failures: {len(reboot_ip_3dial_failure)}')
        except Exception as e:
            print(e)
        finally:
            file.close()

        proxy_stats = [len(dial_times), len(repeat_ips), len(success_ips), len(dial_failed), len(valid_ip), len(invalid_ip), len(consec_ip_repeat), len(reboot_ip_del_failure), len(reboot_ip_3dial_failure)]
        column_names = ['dial_times', 'repeat_ips', 'success_ips', 'dial_failed', 'valid_ip', 'invalid_ip', 'consec_ip_repeat', 'reboot_ip_del_failure', 'reboot_ip_3dial_failure']
        data_list = [proxy_stats, column_names]
        df = pd.DataFrame (data_list).transpose()
        df.columns = ['proxy_stats', 'stats_names']
        df
        proxy_stats2 = [('server', self.adsl), ('dial_times',len(dial_times)), ('repeat_ips',len(repeat_ips)), 
                        ('success_ips',len(success_ips)), ('dial_failed',len(dial_failed)), ('valid_ip',len(valid_ip)),
                        ('invalid_ip',len(invalid_ip)), ('consec_ip_repeat',len(consec_ip_repeat)),
                        ('reboot_ip_del_failure',len(reboot_ip_del_failure)), ('reboot_ip_3dial_failure',len(reboot_ip_3dial_failure)), ('reg_date','2020')]
        proxy_stats3 = list(tuple((self.adsl,len(dial_times), len(repeat_ips), len(success_ips), len(dial_failed), len(valid_ip), len(invalid_ip), len(consec_ip_repeat), len(reboot_ip_del_failure), len(reboot_ip_3dial_failure), '2020')))

        proxy_stats = [self.adsl, len(dial_times), len(repeat_ips), len(success_ips), len(dial_failed), len(valid_ip), len(invalid_ip), len(consec_ip_repeat), len(reboot_ip_del_failure), len(reboot_ip_3dial_failure)]

        # 日志数据总结写入mysql,可以在本地或者远程服务器运行
        db_conn=pymysql.connect(host='IP',port=3306,user='root',passwd='MYSQL_PASSWD',db='proxy',charset='utf8mb4')
        cur = db_conn.cursor()  
        insert_sql="""INSERT IGNORE INTO stats(server, dial_times, repeat_ips, success_ips, dial_failed, valid_ip, invalid_ip,\
                consec_ip_repeat, reboot_ip_del_failure, reboot_ip_3dial_failure) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) AS new \
                ON DUPLICATE KEY UPDATE \
                dial_times=new.dial_times, repeat_ips=new.repeat_ips, success_ips=new.success_ips,\
                dial_failed=new.dial_failed, valid_ip=new.valid_ip, invalid_ip=new.invalid_ip,\
                consec_ip_repeat=new.consec_ip_repeat, reboot_ip_del_failure=new.reboot_ip_del_failure,\
                reboot_ip_3dial_failure=new.reboot_ip_3dial_failure"""
        cur.executemany(insert_sql, [proxy_stats])
        db_conn.commit()
#         figure = plt.figure(self.adsl, figsize=(16, 8)) 
        figure, ax = plt.subplots(1, 1, figsize=(16, 8))
        plt.ion()
        sns.barplot(x = 'stats_names',
                    y = 'proxy_stats',
                    data = df).set_title(self.adsl + '_proxy_quality_monitor')
        
        plt.xticks(rotation=30)
        plt.tight_layout()
        self.show_values_on_bars(ax)
        # Show the plot
        figure.show()        
        plt.pause(10)
        figure.savefig('E:/splash/AdslProxy/' + self.adsl + '_proxy_quality_monitor' + '.jpg')
        figure.clf()
        plt.close()
    def show_values_on_bars(self, axs):
        def _show_on_single_plot(ax):        
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = '{:.0f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center") 

        if isinstance(axs, np.ndarray):
            for idx, ax in np.ndenumerate(axs):
                _show_on_single_plot(ax)
        else:
            _show_on_single_plot(axs)

        
if __name__ == "__main__":
    # 这里是需要监控的拨号服务器ip, port, user, password, adsl_name(给每个服务器取得名字)
    servers = [('192.168.1.1', 22222, 'root', '88888', 'adsl1'),
    ('192.168.1.2', 22222, 'root', '88888', 'adsl2'),
    ]    
#     while True:
    for server in servers:
        proxy_monitor = PROXY_MON(*server)
        proxy_monitor.log_check()              
