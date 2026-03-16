#!/usr/bin/env python3
"""
CRON测试邮件发送脚本
从.env.smtp文件读取配置，发送测试邮件
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_env_from_file(filepath):
    """从.env文件加载环境变量"""
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def send_test_email():
    # 加载SMTP配置
    env_path = '/root/.openclaw/workspace/.env.smtp'
    env_vars = load_env_from_file(env_path)
    
    smtp_server = env_vars.get('SMTP_SERVER', 'smtp.163.com')
    smtp_port = int(env_vars.get('SMTP_PORT', 465))
    smtp_user = env_vars.get('SMTP_USER', '')
    smtp_pass = env_vars.get('SMTP_PASS', '')
    use_ssl = env_vars.get('SMTP_SSL', 'true').lower() == 'true'
    
    # 收件人
    to_email = '75623116@qq.com'
    
    # 邮件内容
    subject = 'Cron测试邮件-11:00'
    body = '''这是使用系统环境变量配置的定时任务测试，验证Cron系统正常工作

发送时间：{send_time}
发送方：{sender}
接收方：{receiver}

此邮件由OpenClaw Cron系统自动发送。'''.format(
        send_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        sender=smtp_user,
        receiver=to_email
    )
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # 连接SMTP服务器并发送
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.starttls()
        
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        print(f"   收件人: {to_email}")
        print(f"   主题: {subject}")
        print(f"   发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False

if __name__ == '__main__':
    success = send_test_email()
    exit(0 if success else 1)
