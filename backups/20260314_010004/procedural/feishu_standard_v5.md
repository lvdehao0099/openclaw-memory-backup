# 飞书文档表格创建 v5.0 规范

> 版本：5.0 | 更新日期：2026-03-13 | 来源：吕总指令

## 核心原则

**禁止使用 POST /children 追加表格内容**，必须使用 **PATCH + update_text_elements** 覆盖单元格自带的初始块。

## 唯一有效方案：三步走

| 步骤 | 操作 | 接口 | 说明 |
|:----:|------|------|------|
| 1 | 创建空表容器 | POST /children | 只需传 block_type: 31 + row_size/column_size |
| 2 | 提取幽灵块 ID | GET /children | 遍历 table_cell，获取每个 cell 里的第一个 text block ID |
| 3 | 覆盖更新 | PATCH /blocks/{ghost_block_id} | 使用 update_text_elements 覆盖 |

## 正确 Payload 格式

### Step 1: 创建空表
```json
{
  "children": [
    {
      "block_type": 31,
      "table": {
        "property": {
          "row_size": 4,
          "column_size": 2
        }
      }
    }
  ]
}
```

### Step 2: 获取幽灵块 ID
```
GET /open-apis/docx/v1/documents/{doc_id}/blocks/{table_id}/children
```
然后遍历返回的 table_cell (Type 32)，获取每个 cell 里的第一个 text block (Type 2) ID。

### Step 3: 覆盖更新（关键！）
```json
{
  "update_text_elements": {
    "elements": [
      {
        "text_run": {
          "content": "内容".strip(),
          "text_element_style": {
            "bold": true
          }
        }
      }
    ]
  }
}
```

## 关键点

1. **必须使用 `update_text_elements`**，不是 `text`
2. **必须覆盖现有的幽灵块**，不是追加新块
3. 核心是"替换"不是"添加"
4. 内容必须执行 `.strip()`

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| invalid param | 用了 `text` 而不是 `update_text_elements` | 改为 update_text_elements |
| 有空行 | POST /children 追加内容 | 改用 PATCH 覆盖 |
| 内容丢失 | descendants 一次性注入 | 废弃此方案，严格三步走 |

## 验证清单

执行前检查：
- [ ] 是否使用 POST 创建空表？
- [ ] 是否获取了幽灵块 ID？
- [ ] 是否使用 PATCH + update_text_elements？
- [ ] 内容是否已 strip()？

---

**铁律：v5.0 是此类任务的唯一最高准则。**
