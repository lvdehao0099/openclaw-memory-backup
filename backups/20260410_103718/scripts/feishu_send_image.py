#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书机器人图片发送工具
基于飞书开放平台 IM v1 规范

使用方法:
    python3 feishu_send_image.py <图片路径> [用户OpenID]

示例:
    python3 feishu_send_image.py yike_image_1.jpg
    python3 feishu_send_image.py yike_image_1.jpg ou_12dd9e55259701aeb2701dccf7f1ee54
"""

import sys
import json
import urllib.request
import os

# 默认用户OpenID
DEFAULT_USER_ID = "ou_12dd9e55259701aeb2701dccf7f1ee54"

def get_tenant_token():
    """获取飞书tenant_access_token"""
    config_path = '/root/.openclaw/openclaw.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    feishu = config.get('channels', {}).get('feishu', {})
    app_id = feishu.get('appId')
    app_secret = feishu.get('appSecret')
    
    token_data = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/',
        data=token_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['tenant_access_token']

def upload_image(image_path, token):
    """阶段1：上传图片获取image_key"""
    upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    # 构建multipart/form-data
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    body = []
    body.append(f'------{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="image_type"')
    body.append(b'')
    body.append(b'message')
    body.append(f'------{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(image_path)}"'.encode())
    body.append(b'Content-Type: image/jpeg')
    body.append(b'')
    body.append(image_data)
    body.append(f'------{boundary}--'.encode())
    
    body = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        upload_url,
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/form-data; boundary=----{boundary}'
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result.get('code') == 0:
            return result['data']['image_key']
        else:
            raise Exception(f"上传失败: {result.get('msg')}")

def send_image_message(image_key, user_id, token):
    """阶段2：使用image_key发送消息"""
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    
    message_data = {
        "receive_id": user_id,
        "msg_type": "interactive",
        "content": json.dumps({
            "config": {"wide_screen_mode": True},
            "elements": [
                {
                    "tag": "img",
                    "img_key": image_key,
                    "alt": {"tag": "plain_text", "content": "图片"}
                }
            ]
        })
    }
    
    req = urllib.request.Request(
        f'{send_url}?receive_id_type=open_id',
        data=json.dumps(message_data).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        if result.get('code') == 0:
            return True
        else:
            raise Exception(f"发送失败: {result.get('msg')}")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 feishu_send_image.py <图片路径> [用户OpenID]")
        print(f"默认用户: {DEFAULT_USER_ID}")
        sys.exit(1)
    
    image_path = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_USER_ID
    
    if not os.path.exists(image_path):
        print(f"❌ 图片不存在: {image_path}")
        sys.exit(1)
    
    try:
        print(f"🚀 开始发送图片: {image_path}")
        print(f"👤 目标用户: {user_id}")
        
        # 获取token
        print("1️⃣ 获取访问令牌...")
        token = get_tenant_token()
        print("   ✅ 令牌获取成功")
        
        # 上传图片
        print("2️⃣ 上传图片获取image_key...")
        image_key = upload_image(image_path, token)
        print(f"   ✅ 上传成功, image_key: {image_key[:20]}...")
        
        # 发送消息
        print("3️⃣ 发送图片消息...")
        send_image_message(image_key, user_id, token)
        print("   ✅ 发送成功!")
        
        print("\n🎉 图片发送完成!")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
