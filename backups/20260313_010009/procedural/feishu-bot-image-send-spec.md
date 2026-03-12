# 飞书机器人图片推送技术规范（永久记录）

> 文档版本：飞书开放平台 IM v1 (2026-03-12)  
> 核心原则：飞书机器人不支持直接发送外网图片URL

---

## 核心逻辑

必须执行**"两阶段原子操作"**：
1. **阶段1**：上传资源换取 image_key
2. **阶段2**：引用 image_key 发送消息

---

## 阶段1：资源持久化 (Upload Image)

将图片流式上传至飞书服务端，获取 `image_key`。

**API endpoint：**
```
POST https://open.feishu.cn/open-apis/im/v1/images
```

**请求头：**
```
Authorization: Bearer {tenant_access_token}
Content-Type: multipart/form-data
```

**请求参数：**
- `image_type`: 图片类型（message/avatar等）
- `image`: 图片文件（二进制流）

**响应示例：**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "image_key": "img_v2_xxx"
  }
}
```

---

## 阶段2：消息下发 (Send Message)

使用获取到的 `image_key` 构建消息体发送。

**API endpoint：**
```
POST https://open.feishu.cn/open-apis/im/v1/messages
```

### 方式A：普通图片消息

**请求体：**
```json
{
  "receive_id": "ou_xxx",
  "content": {
    "image_key": "img_v2_xxx"
  },
  "msg_type": "image"
}
```

### 方式B：交互式卡片 (推荐)

**请求体：**
```json
{
  "receive_id": "ou_xxx",
  "msg_type": "interactive",
  "content": {
    "config": {
      "wide_screen_mode": true
    },
    "elements": [
      {
        "tag": "img",
        "img_key": "img_v2_xxx",
        "alt": {
          "tag": "plain_text",
          "content": "图片描述"
        }
      },
      {
        "tag": "div",
        "text": {
          "tag": "plain_text",
          "content": "图片说明文字"
        }
      }
    ]
  }
}
```

---

## 完整Python示例

```python
import requests
import json

# 配置
tenant_token = "your_tenant_access_token"
user_open_id = "ou_xxx"
image_path = "/path/to/image.jpg"

# 阶段1：上传图片获取image_key
upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
headers = {"Authorization": f"Bearer {tenant_token}"}

with open(image_path, 'rb') as f:
    files = {'image': f}
    data = {'image_type': 'message'}
    response = requests.post(upload_url, headers=headers, files=files, data=data)

result = response.json()
if result.get('code') == 0:
    image_key = result['data']['image_key']
    print(f"✅ 上传成功，image_key: {image_key}")
else:
    print(f"❌ 上传失败: {result.get('msg')}")
    exit(1)

# 阶段2：发送图片消息
send_url = "https://open.feishu.cn/open-apis/im/v1/messages"
params = {"receive_id_type": "open_id"}

message_data = {
    "receive_id": user_open_id,
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

response = requests.post(send_url, headers=headers, params=params, json=message_data)
if response.json().get('code') == 0:
    print("✅ 图片发送成功")
else:
    print(f"❌ 发送失败")
```

---

## 关键要点

| 要点 | 说明 |
|------|------|
| ❌ 禁止 | 直接发送外网图片URL |
| ✅ 必须 | 先上传获取image_key |
| ✅ 推荐 | 使用interactive卡片类型 |
| ⚠️ 注意 | image_key有效期有限，及时使用 |

---

## 常见错误

1. **直接发送URL**：飞书不会解析，用户看不到图片
2. **重复使用image_key**：每个消息需要重新上传
3. **格式错误**：必须使用multipart/form-data上传

---

## 记录时间
2026-03-12 学习并永久记录
