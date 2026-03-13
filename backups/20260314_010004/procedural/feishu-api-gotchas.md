# 飞书 API 核心约束

> 这些知识是 API 文档不写但我必须知道的"坑"和最佳实践。

---

## 一、日历操作

### 1. user_open_id 为什么必填？

工具使用用户身份：日程创建在用户主日历上，用户本人能看到。

**但为什么还要传 user_open_id？** 将发起人也添加为参会人，确保：
- ✅ 发起人会收到日程通知
- ✅ 发起人可以回复 RSVP 状态
- ✅ 发起人出现在参会人列表中

**如果不传：**
- ⚠️ 用户能看到日程，但不会作为参会人
- ⚠️ 如果只有其他参会人，发起人不在列表中

---

### 2. 时间格式铁律

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| Unix 时间戳 | ISO 8601 带时区 |
| `1742264400` | `2026-03-13T14:00:00+08:00` |
| `2026-03-13 14:00` | `2026-03-13T14:00:00+08:00` |

**时区固定：** `Asia/Shanghai` (UTC+8)

---

### 3. attendees 参数强烈建议

如果不传 attendees：
- 日程只在自己日历上
- 其他人看不到
- 没有邀请通知

**推荐传法：**
```json
{
  "attendees": [
    {"open_id": "ou_xxx", "ability": "can_modify_event"}
  ]
}
```

`can_modify_event` 让参会人能编辑日程。

---

## 二、多维表格（Bitable）操作

### 1. 字段值格式速查表

| 字段类型 | 格式 | 示例 |
|---------|------|------|
| 文本 | 字符串 | `"这是文本"` |
| 数字 | 数字 | `123` |
| 单选 | 字符串 | `"选项名"` |
| 多选 | 字符串数组 | `["选项1", "选项2"]` |
| 人员 | 数组对象 | `[{"id": "ou_xxx"}]` |
| 日期 | 毫秒时间戳 | `1772121600000` |
| 超链接 | 对象 | `{"link": "URL", "text": "显示文本"}` |
| 复选框 | 布尔 | `true` / `false` |

---

### 2. 常见错误

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 人员字段传字符串 `"ou_xxx"` | 人员字段用数组对象 `[{"id": "ou_xxx"}]` |
| 日期字段传字符串 `"2026-03-13"` | 日期字段用毫秒时间戳 `1742227200000` |
| 批量写入超过 500 条 | 分批处理，每批 ≤ 500 条 |

---

### 3. 获取字段 ID 的方法

**步骤：**
1. 先调用 `GET /bitable/v1/apps/{app_token}/tables/{table_id}/fields`
2. 找到对应字段的 `field_id`
3. 写入时使用 `field_id` 而非字段名

**示例：**
```python
# 获取字段列表
fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
resp = requests.get(fields_url, headers={"Authorization": f"Bearer {token}"})
fields = resp.json()['data']['items']

# 找到目标字段
for field in fields:
    if field['field_name'] == '事项名称':
        target_field_id = field['field_id']
```

---

## 三、消息操作

### 1. 消息类型选择

| 场景 | 推荐工具 | 说明 |
|------|---------|------|
| 发消息到当前对话 | `message` 工具 | 自动路由到来源渠道 |
| 以用户身份发消息 | `feishu_im_user_message` | 显示为用户发送 |
| 回复消息 | `message` 工具的 reply action | 带引用回复 |

---

### 2. 图片发送铁律

**两阶段原子操作：**

```
阶段1: 上传图片 → 获取 image_key
阶段2: 使用 image_key → 发送消息
```

**禁止：**
- ❌ 直接发送外网图片 URL → 用户看不到
- ❌ 使用 `text` 类型发图片 → 显示为文本链接

**正确：**
```python
# 阶段1：上传
upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
files = {'image': open(image_path, 'rb')}
data = {'image_type': 'message'}
resp = requests.post(upload_url, headers=headers, files=files, data=data)
image_key = resp.json()['data']['image_key']

# 阶段2：发送
message = {
    "msg_type": "interactive",
    "content": json.dumps({
        "config": {"wide_screen_mode": True},
        "elements": [{"tag": "img", "img_key": image_key}]
    })
}
```

---

### 3. 投递目标格式铁律

| ❌ 错误 | ✅ 正确 | 说明 |
|--------|--------|------|
| `"to": "ou_xxx"` | `"to": "user:ou_xxx"` | 单聊用户 |
| `"to": "oc_xxx"` | `"to": "chat:oc_xxx"` | 群组 |

**这是血的教训！** 投递失败的常见原因就是少了 `user:` 或 `chat:` 前缀。

---

## 四、文档操作（Docx）

### 1. Markdown 不能直接写入

飞书新版文档（Docx）**不支持直接解析 Markdown 字符串**。

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| `text` 块中使用 `#` 或加粗模拟标题 | 使用 `block_type: 3-11` (heading1-heading9) |
| 文本中使用 `-` 或 `1.` 模拟列表 | 使用 `block_type: 12` (无序) 或 `13` (有序) |
| Markdown 表格字符串直接写入 | 三层嵌套：Table -> Table Cell -> Content Block |

---

### 2. Block Type 速查表

| 类型 | Block Type | 构造函数 |
|------|------------|----------|
| 文本段落 | 2 | `create_text(text)` |
| 一级标题 | 3 | `create_heading1(text)` |
| 二级标题 | 4 | `create_heading2(text)` |
| 三级标题 | 5 | `create_heading3(text)` |
| 无序列表 | 12 | `create_bullet(text)` |
| 有序列表 | 13 | `create_numbered(text)` |
| 代码块 | 14 | `create_code_block(code, lang)` |
| 表格 | 31 | `create_table(rows, header=True)` |
| 表格单元格 | 32 | `create_table_cell(text)` |

---

### 3. 表格三层嵌套模型

```
Table (block_type: 31)
├── property: {row_size, column_size, header_row}
└── children: [
    Table Cell (block_type: 32)
    └── children: [
        Content Block (block_type: 2)  # 实际文本
    ]
]
```

---

## 五、权限与身份

### 1. 机器人身份 vs 用户身份

| 身份 | 权限范围 | 适用场景 |
|------|---------|---------|
| 机器人身份 | App ID/Secret 定义的权限 | 公共文档、机器人消息 |
| 用户身份 (OAuth) | 用户本人权限 | 私有文档、私密日历、以用户身份发消息 |

**当前配置：** 机器人身份

---

### 2. 检查权限的方法

```python
# 获取机器人信息
resp = requests.get(
    "https://open.feishu.cn/open-apis/bot/v3/info",
    headers={"Authorization": f"Bearer {tenant_token}"}
)
```

---

## 六、分页与批量操作

### 1. 分页参数

| 参数 | 说明 |
|------|------|
| `page_size` | 每页数量，默认 20，最大 50 |
| `page_token` | 下一页标记，从上次响应获取 |

---

### 2. 批量操作限制

| 操作 | 限制 |
|------|------|
| Bitable 记录批量创建 | 单次 ≤ 500 条 |
| Docx Block 批量写入 | 单次 ≤ 100 个 |
| 图片上传 | 单个 < 10MB |

---

*更新时间：2026-03-13*
*维护者：虾米 (CLO)*
