# 邮箱配置信息（永久记录）

## 163邮箱SMTP配置

**发件邮箱：** m13998517880@163.com  
**收件邮箱：** 75623116@qq.com  
**SMTP服务器：** smtp.163.com:465  
**授权码：** VXPj4h3GDjGtZXsq

## 使用方法

```python
import smtplib
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP_SSL('smtp.163.com', 465)
server.login('m13998517880@163.com', 'VXPj4h3GDjGtZXsq')
# 发送邮件...
server.quit()
```

## 配置时间
2026-03-09 首次配置  
2026-03-12 永久记录

## 用途
- 发送周报
- 系统通知
- 图片/文件传输
