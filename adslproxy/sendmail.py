
# -*- coding: utf-8 -*-
import time
# from playsound import playsound
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class EmailClient(object):
    def __init__(self):
        """
        初始化邮件列表     
                 
        """
        self.to_list = [SENDER_EMAIL, RECEIVER_EMAIL]
    def notification(self, body, subj):
        sender = SENDER_EMAIL  # 邮件发送人
        receiver = RECEIVER_EMAIL  # 邮件收件人
        subject = 'adslproxy notification: ' + subj + ' ' + str(datetime.today())[:16]  # 主题
        smtpserver = 'smtp.163.com'  # 网易的STMP地址 默认端口号为25
        username = EMAIL  # 发送邮件的人
        password = PASS  # 你所设置的密码.网易在开通SMTP服务后会有个密码设置

        # 中文需参数‘utf-8'，单字节字符不需要
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')  # 头部信息:标题
        msg['From'] = 'user<SENDER_EMAIL>'  # 头部信息:名称<发件人的地址>
        msg['To'] = ",".join(self.to_list)  # 头部信息:收件人地址
        m = 0
        while m < 3:
            try:        
                smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
                smtp.login(username, password)
                smtp.sendmail(sender, receiver, msg.as_string())
                smtp.quit()
                print('success')
                m += 1
                break
            except smtplib.SMTPException as e:
                print('Error: ', e)
                m += 1
                time.sleep(25)
