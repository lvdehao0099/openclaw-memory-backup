# 飞书技术白皮书（Master Spec）

> **唯一权威文档** - 所有飞书相关技术规范、API映射、代码模板、踩坑经验
> **执行飞书操作前，必须实时查阅本文件，禁止依赖历史记忆。**

---

## 📋 核心配置索引

| 用途 | app_token | table_id | URL |
|------|-----------|----------|-----|
| 待办追踪表 | `O2rAb69hOa16aks5QHucOajSnWh` | `tbldg2S9P76Ig1l0` | https://ai-zhineng.feishu.cn/base/O2rAb69hOa16aks5QHucOajSnWh |
| 热点雷达追踪表 | `Xb0abYaXlayTnNsU2Oocrp42nUh` | `tblYm8TbPyjqxxEJ` | https://ai-zhineng.feishu.cn/base/Xb0abYaXlayTnNsU2Oocrp42nUh |
| **AI老师傅客户拜访备忘录** | `C4q0bLUWiaFUGJsy3rDclZJvnpg` | `tblWxIik6Nbeyp9W` | https://ai-zhineng.feishu.cn/base/C4q0bLUWiaFUGJsy3rDclZJvnpg?table=tblWxIik6Nbeyp9W |
| 文档目标文件夹 | folder_token: `Thhrfa3QglB5amdIMpEcY2tAndd` | - | https://ai-zhineng.feishu.cn/drive/folder/Thhrfa3QglB5amdIMpEcY2tAndd |

**⚠️ 重要：所有AI老师傅相关的客户信息，必须同步写入「AI老师傅客户拜访备忘录」表格！**

**用户 OpenID:** `ou_12dd9e55259701aeb2701dccf7f1ee54`

---

## 第一章：基础配置与认证

### 1.1 App 配置

| 配置项 | 值 |
|--------|-----|
| App ID | `cli_a92780ca08b89bb6` |
| App Secret | `6gzhCcNYlHc7vOnGCCdvpbik27O85uz0` |
| Domain | `feishu` |

### 1.2 Token 获取

```python
import requests

token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
resp = requests.post(token_url, json={
    "app_id": "cli_a92780ca08b89bb6",
    "app_secret": "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"
})
token = resp.json()["tenant_access_token"]
```

### 1.3 权限说明

| 身份 | 权限范围 | 适用场景 |
|------|---------|---------|
| 机器人身份 | App ID/Secret 定义的权限 | 公共文档、机器人消息 |
| 用户身份 (OAuth) | 用户本人权限 | 私有文档、私密日历、以用户身份发消息 |

**当前配置：** 机器人身份

---

## 第二章：日历操作

### 2.1 时间格式铁律

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| Unix 时间戳 | ISO 8601 带时区 |
| `1742264400` | `2026-03-13T14:00:00+08:00` |
| `2026-03-13 14:00` | `2026-03-13T14:00:00+08:00` |

**时区固定：** `Asia/Shanghai` (UTC+8)

### 2.2 user_open_id 必填原因

工具使用用户身份：日程创建在用户主日历上。但还要传 user_open_id 确保：
- ✅ 发起人会收到日程通知
- ✅ 发起人可以回复 RSVP 状态
- ✅ 发起人出现在参会人列表中

### 2.3 attendees 参数

**推荐传法：**
```json
{
  "attendees": [
    {"open_id": "ou_xxx", "ability": "can_modify_event"}
  ]
}
```

`can_modify_event` 让参会人能编辑日程。

### 2.4 日历错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `invalid start_time format` | 时间格式错误 | 改用 ISO 8601 带时区 |
| `calendar not found` | 日历 ID 错误或无权限 | 检查 calendar_id 和权限 |
| `user_open_id required` | 未传用户 ID | 从 sender_id 获取 |
| `time conflict` | 时间冲突 | 检查用户该时间段是否已有日程 |

---

## 第三章：多维表格（Bitable）操作

### 3.1 字段值格式速查表

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

### 3.2 常见错误

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 人员字段传字符串 `"ou_xxx"` | 人员字段用数组对象 `[{"id": "ou_xxx"}]` |
| 日期字段传字符串 `"2026-03-13"` | 日期字段用毫秒时间戳 `1742227200000` |
| 批量写入超过 500 条 | 分批处理，每批 ≤ 500 条 |

### 3.3 获取字段 ID

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

### 3.4 添加记录

```python
def add_record_to_bitable(app_token, table_id, fields, token):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records'
    
    data = json.dumps({"fields": fields}).encode('utf-8')
    
    req = urllib.request.Request(
        url, data=data,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['data']['record']['record_id']
```

### 3.5 批量添加记录

```python
def batch_add_records(app_token, table_id, records, token):
    """批量添加记录（每次最多500条）"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'
    
    data = json.dumps({"records": [{"fields": r} for r in records]}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={...}, method='POST')
    # ...
```

### 3.6 创建表格后必删空列

**致命错误：保留空列不删除**
- ❌ 错误：创建表格后保留默认空字段（"单选"、"日期"、"附件"）
- ✅ 正确：创建后立即删除不需要的默认字段

```python
fields_to_delete = ['单选', '日期', '附件']  # 默认空字段
for field in fields:
    if field['field_name'] in fields_to_delete and not field.get('is_primary'):
        delete_field(field['field_id'])
```

### 3.7 Bitable 错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `field not found` | 字段 ID 错误 | 先调用 GET /fields 获取正确的 field_id |
| `invalid field value` | 字段值格式错误 | 参见字段格式表 |
| `batch size exceeded` | 批量操作超限 | 每批 ≤ 500 条 |
| `table not found` | 表格 ID 错误 | 检查 table_id 和 app_token |

---

## 第四章：文档操作（Docx）

### 4.1 核心原则

**致命错误：将 Markdown 直接作为文本写入**
- ❌ 错误：将 Markdown 字符串直接写入 text block
- ✅ 正确：使用 Block 构造函数，将 Markdown 拆解为结构化 Block

飞书新版文档（Docx）**不支持直接解析 Markdown 字符串**。

### 4.2 Block Type 映射表

| Block Type | 常量值 | 用途 |
|------------|--------|------|
| TEXT | 2 | 普通文本段落 |
| HEADING_1 | 3 | 一级标题（TOC可识别）|
| HEADING_2 | 4 | 二级标题 |
| HEADING_3 | 5 | 三级标题 |
| HEADING_4-9 | 6-11 | 四至九级标题 |
| BULLETED_LIST | 12 | 无序列表 |
| NUMBERED_LIST | 13 | 有序列表 |
| CODE_BLOCK | 14 | 代码块 |
| TABLE | 31 | 表格容器 |
| TABLE_CELL | 32 | 表格单元格 |

### 4.3 Block 构造函数

```python
def create_heading1(text):
    return {
        "block_type": 3,
        "heading1": {
            "elements": [{"text_run": {"content": text}}],
            "style": {"align": 1}
        }
    }

def create_text(text, bold=False, italic=False):
    return {
        "block_type": 2,
        "text": {
            "elements": [{
                "text_run": {
                    "content": text,
                    "text_element_style": {"bold": bold, "italic": italic}
                }
            }],
            "style": {"align": 1}
        }
    }

def create_bullet(text):
    return {
        "block_type": 12,
        "bulleted_list": {"elements": [{"text_run": {"content": text}}]}
    }

def create_numbered(text):
    return {
        "block_type": 13,
        "numbered_list": {"elements": [{"text_run": {"content": text}}]}
    }

def create_code_block(code_text, language=58):  # 58=Python
    return {
        "block_type": 14,
        "code": {
            "elements": [{"text_run": {"content": code_text}}],
            "style": {"language": language, "wrap": False}
        }
    }
```

### 4.4 表格三层嵌套模型

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

### 4.5 表格构造函数（零空行版）

```python
def create_table_cell(text):
    """表格单元格 - 强制 strip() 去除首尾空格和换行符"""
    cleaned_text = str(text).strip()
    
    return {
        "block_type": 32,
        "table_cell": {
            "children": [{
                "block_type": 2,
                "text": {"elements": [{"text_run": {"content": cleaned_text}}]}
            }]
        }
    }

def create_table(rows_data, header_row=True):
    """表格构造 - 三层嵌套模型"""
    row_size = len(rows_data)
    column_size = len(rows_data[0]) if rows_data else 0
    
    cells = []
    for row in rows_data:
        for cell_text in row:
            cells.append(create_table_cell(cell_text))
    
    return {
        "block_type": 31,
        "table": {
            "property": {
                "row_size": row_size,
                "column_size": column_size,
                "header_row": header_row
            }
        },
        "children": cells
    }
```

### 4.6 表格终极方案：整装推送（零空行）

```python
def create_table_with_content(doc_id, data, rows, cols):
    """一次性创建带内容的表格，零空行"""
    table_id = "temp_table"
    table_children = []
    descendants = []
    
    for i in range(rows * cols):
        cell_id = f"temp_cell_{i}"
        text_id = f"temp_text_{i}"
        
        table_children.append(cell_id)
        
        descendants.append({
            "block_id": cell_id,
            "block_type": 32,
            "children": [text_id]
        })
        
        clean = str(data[i]).strip().replace('\r', '').replace('\n', '')
        is_header = (i < cols)
        descendants.append({
            "block_id": text_id,
            "block_type": 2,
            "text": {
                "elements": [{
                    "text_run": {
                        "content": clean,
                        "text_element_style": {"bold": is_header}
                    }
                }]
            }
        })
    
    return {
        "children": [{
            "block_id": table_id,
            "block_type": 31,
            "table": {"property": {"row_size": rows, "column_size": cols}},
            "children": table_children
        }],
        "descendants": descendants
    }
```

### 4.7 Markdown 到 Block 转换

```python
def markdown_to_blocks(markdown_text):
    """将 Markdown 转换为飞书 Block 数组"""
    blocks = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            blocks.append(create_heading1(line[2:]))
        elif line.startswith('## '):
            blocks.append(create_heading2(line[3:]))
        elif line.startswith('### '):
            blocks.append(create_heading3(line[4:]))
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append(create_bullet(line[2:]))
        elif re.match(r'^\d+\. ', line):
            blocks.append(create_numbered(re.sub(r'^\d+\. ', '', line)))
        elif line.strip():
            blocks.append(create_text(line))
    
    return blocks
```

### 4.8 批量写入策略

```python
def write_blocks_to_document(doc_id, blocks, token, batch_size=50):
    """批量写入 blocks，单次最多 100 个"""
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        request_body = {"children": batch}
        # POST 到 /docx/v1/documents/{doc_id}/blocks/{doc_id}/children
```

### 4.9 文档错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `document not found` | 文档 ID 错误 | 检查 document_id |
| `block not found` | Block ID 错误 | 检查 block_id |
| `invalid block type` | Block 类型错误 | 检查 block_type 是否正确 |
| `block limit exceeded` | Block 数量超限 | 单次写入 ≤ 100 个 |

---

## 第五章：消息操作

### 5.0 消息发送铁律（最重要！）

**🚨 致命错误：手动调用飞书API发送消息到当前对话**

**场景区分：**

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| **在当前对话中回复用户** | 直接回复，系统自动路由 | ❌ 手动调用飞书消息API |
| **定时任务发送消息** | 使用 cron + delivery 投递 | ❌ 在任务中调用消息API |
| **跨会话发送消息** | 使用 sessions_send 工具 | ❌ 手动调用飞书API |

**核心原则：**
```
在当前对话中回复 = 自动发送到飞书
不需要手动调用任何消息API
```

**血的教训（2026-03-14）：**
- 我两次手动调用飞书消息API发送消息
- 使用 `receive_id: "ou_xxx"` + `receive_id_type: "open_id"`
- 结果消息发到了群聊 `oc_92f7b631416136f54047d09694a8ff8f`，而不是用户单聊
- 根本原因：飞书API在处理 open_id 时，优先路由到群聊

**正确理解：**
- 当前对话的 chat_id 格式：`user:ou_xxx`（单聊）或 `chat:oc_xxx`（群聊）
- 在这个对话中回复的内容，会自动发送到正确的位置
- **永远不要手动调用飞书消息API发送到当前对话**

---

### 5.1 投递目标格式铁律（仅用于定时任务）

**致命错误：投递目标格式错误**
- ❌ 错误：`"to": "ou_xxx"` → 投递失败
- ✅ 正确：`"to": "user:ou_xxx"` 或 `"to": "chat:oc_xxx"`

```json
{
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "user:ou_12dd9e55259701aeb2701dccf7f1ee54"
  }
}
```

**格式规则：**
- 单聊用户：`user:ou_xxx`
- 群组：`chat:oc_xxx`
- **永远不要**只写 `ou_xxx` 或 `oc_xxx`

### 5.2 图片发送铁律

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
message_data = {
    "receive_id": user_open_id,
    "msg_type": "interactive",
    "content": json.dumps({
        "config": {"wide_screen_mode": True},
        "elements": [{"tag": "img", "img_key": image_key}]
    })
}
```

### 5.3 消息错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `receive_id not found` | 接收者 ID 错误 | 检查 receive_id 和 receive_id_type |
| `message too long` | 消息过长 | 文本 ≤ 30KB，卡片 ≤ 100KB |
| `image not found` | 图片 key 无效 | 重新上传获取新 image_key |
| `delivery failed` | 投递失败 | 检查 to 字段是否带前缀 |

---

## 第六章：分页与批量操作

### 6.1 分页参数

| 参数 | 说明 |
|------|------|
| `page_size` | 每页数量，默认 20，最大 50 |
| `page_token` | 下一页标记，从上次响应获取 |

### 6.2 批量操作限制

| 操作 | 限制 |
|------|------|
| Bitable 记录批量创建 | 单次 ≤ 500 条 |
| Docx Block 批量写入 | 单次 ≤ 100 个 |
| 图片上传 | 单个 < 10MB |

---

## 第七章：语言代码映射

| 语言 | 代码值 |
|------|--------|
| Plain Text | 1 |
| Python | 58 |
| JavaScript | 35 |
| TypeScript | 72 |
| Java | 34 |
| Go | 29 |
| Rust | 62 |
| SQL | 68 |
| Bash/Shell | 67 |
| JSON | 38 |
| YAML | 79 |
| Markdown | 47 |
| HTML | 32 |
| CSS | 22 |
| C++ | 11 |
| PHP | 55 |

---

## 第八章：通用诊断命令

```bash
# 测试飞书连接
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a92780ca08b89bb6","app_secret":"6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"}'

# 检查多维表格权限
curl -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}" \
  -H "Authorization: Bearer {token}"

# 检查文档权限
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}" \
  -H "Authorization: Bearer {token}"
```

---

**最后更新：2026-03-14**
**维护者：虾米 (CLO)**
