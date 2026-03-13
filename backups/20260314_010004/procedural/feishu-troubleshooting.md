# 飞书 API 错误排查手册

> 遇到错误时，先查这个表。

---

## 一、日历错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `invalid start_time format` | 时间格式错误 | 改用 ISO 8601 带时区：`2026-03-13T14:00:00+08:00` |
| `calendar not found` | 日历 ID 错误或无权限 | 检查 `calendar_id`，确认机器人有访问权限 |
| `user_open_id required` | 未传用户 ID | 从消息上下文的 `sender_id` 获取 |
| `attendee limit exceeded` | 参会人超过限制 | 减少参会人数量（单次最多 200 人） |
| `time conflict` | 时间冲突 | 检查用户该时间段是否已有日程 |

---

## 二、多维表格（Bitable）错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `field not found` | 字段 ID 错误 | 先调用 GET /fields 获取正确的 field_id |
| `invalid field value` | 字段值格式错误 | 参见 feishu-api-gotchas.md 的字段格式表 |
| `record not found` | 记录 ID 错误 | 检查 `record_id` 是否正确 |
| `permission denied` | 无权限 | 检查机器人是否有表格访问权限 |
| `batch size exceeded` | 批量操作超限 | 每批 ≤ 500 条，分批处理 |
| `table not found` | 表格 ID 错误 | 检查 `table_id` 和 `app_token` |

### 字段值格式错误速查

| 字段类型 | 错误示例 | 正确示例 |
|---------|---------|---------|
| 人员 | `"ou_xxx"` | `[{"id": "ou_xxx"}]` |
| 日期 | `"2026-03-13"` | `1742227200000` |
| 多选 | `"选项1"` | `["选项1", "选项2"]` |
| 超链接 | `"https://xxx.com"` | `{"link": "https://xxx.com", "text": "链接"}` |

---

## 三、消息错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `receive_id not found` | 接收者 ID 错误 | 检查 `receive_id` 和 `receive_id_type` |
| `message too long` | 消息过长 | 文本消息 ≤ 30KB，卡片消息 ≤ 100KB |
| `image not found` | 图片 key 无效 | 重新上传图片获取新的 image_key |
| `invalid msg_type` | 消息类型错误 | 检查 `msg_type` 是否正确：text/post/interactive/image |
| `delivery failed` | 投递失败 | 检查 `to` 字段是否带 `user:` 或 `chat:` 前缀 |

### 投递失败排查步骤

1. 检查 `to` 字段格式
   - ❌ `"to": "ou_xxx"` 
   - ✅ `"to": "user:ou_xxx"`

2. 检查 `channel` 字段
   - 必须指定 `"channel": "feishu"`

3. 检查用户 Open ID 是否正确
   - 从消息上下文的 `sender_id` 获取

---

## 四、文档错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `document not found` | 文档 ID 错误 | 检查 `document_id` 是否正确 |
| `block not found` | Block ID 错误 | 检查 `block_id` 是否正确 |
| `invalid block type` | Block 类型错误 | 检查 `block_type` 是否在有效范围内 |
| `block limit exceeded` | Block 数量超限 | 单次写入 ≤ 100 个 Block |
| `permission denied` | 无权限 | 检查机器人是否有文档编辑权限 |

### Block 构造错误速查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 标题不显示 | 用 text block 模拟 | 改用 heading block (type 3-11) |
| 列表不显示 | 用 text block 模拟 | 改用 bullet/numbered block (type 12/13) |
| 表格格式错乱 | 未用三层嵌套 | Table -> Table Cell -> Content Block |
| Markdown 原样显示 | 直接写入 text block | 使用 Block 构造函数解析 |

---

## 五、认证错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `invalid app_id or app_secret` | 配置错误 | 检查 openclaw.json 中的 appId 和 appSecret |
| `tenant_access_token expired` | Token 过期 | 重新获取 tenant_access_token |
| `permission denied` | 权限不足 | 检查飞书应用的权限配置 |
| `rate limit exceeded` | 请求频率超限 | 降低请求频率，参考 API 限流规则 |

### Token 获取流程

```python
import requests

token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
resp = requests.post(token_url, json={
    "app_id": "cli_xxx",
    "app_secret": "xxx"
})
token = resp.json()["tenant_access_token"]
```

---

## 六、通用排查步骤

### Step 1: 检查配置
```bash
# 检查飞书配置
cat ~/.openclaw/openclaw.json | grep -A 5 "feishu"
```

### Step 2: 验证 Token
```python
# 测试 token 是否有效
resp = requests.get(
    "https://open.feishu.cn/open-apis/bot/v3/info",
    headers={"Authorization": f"Bearer {token}"}
)
print(resp.json())
```

### Step 3: 检查权限
- 飞书开放平台 → 应用详情 → 权限管理
- 确认所需权限已开通

### Step 4: 查看日志
```bash
# 查看最近错误日志
tail -100 ~/.openclaw/logs/error.log
```

---

## 七、常用诊断命令

```bash
# 测试飞书连接
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'

# 检查多维表格权限
curl -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}" \
  -H "Authorization: Bearer {token}"

# 检查文档权限
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}" \
  -H "Authorization: Bearer {token}"
```

---

*更新时间：2026-03-13*
*维护者：虾米 (CLO)*
