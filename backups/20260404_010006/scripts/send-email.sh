#!/bin/bash
# 邮件发送脚本 - 供定时任务调用

# 加载SMTP配置
source ~/.openclaw/smtp-config.sh

# 参数：收件人 主题 内容
TO=$1
SUBJECT=$2
BODY=$3

python3 << PYEOF
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

try:
    smtp_user = os.environ.get('SMTP_USER', 'm13998517880@163.com')
    smtp_pass = os.environ.get('SMTP_PASS', 'VXPj4h3GDjGtZXsq')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.163.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 465))
    
    to = "$TO"
    subject = "$SUBJECT"
    body = """$BODY"""
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = smtp_user
    msg['To'] = to
    
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    smtp.login(smtp_user, smtp_pass)
    smtp.sendmail(smtp_user, [to], msg.as_string())
    print(f"✅ 邮件已发送到 {to}")
    smtp.quit()
except Exception as e:
    print(f"❌ 发送失败: {e}")
    exit(1)
PYEOF
