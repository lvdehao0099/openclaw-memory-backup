# 飞书文档表格技术限制说明

## 问题背景
2026-03-13 尝试在飞书 Docx 中创建表格时遇到 API 限制。

## 研究发现

### 1. 表格创建流程（已验证可行）
```
步骤1: POST /docx/v1/documents/{doc_id}/blocks/{doc_id}/children
       创建 Table Block (block_type: 31)，指定行列数
       
步骤2: 飞书自动创建 TableCell Blocks (block_type: 32)
       返回 cells 数组，包含每个单元格的 block_id
       
步骤3: 获取每个 cell 的 children (默认包含一个空的 text block)

步骤4: PATCH /docx/v1/documents/{doc_id}/blocks/{text_block_id}
       尝试更新 text block 内容 → ❌ 失败，报 "invalid param"
```

### 2. 错误分析
- 创建 Table Block：✅ 成功
- 读取 Cell 结构：✅ 成功
- 更新 Cell 内容：❌ 失败

错误信息：`{"code": 1770001, "msg": "invalid param"}`

尝试过的更新方式：
1. 更新整个 block (PATCH with block_type + text) → 失败
2. 只更新 elements (PATCH with elements only) → 失败

### 3. 可能的原因
飞书 Docx API 的表格单元格更新可能需要：
- 特殊的权限或 scope
- 不同的 API endpoint
- 特定的请求格式（非标准 block update）

### 4. 替代方案

| 方案 | 实现难度 | 适用场景 |
|------|:--------:|----------|
| **列表替代** | 低 | 一图读懂、速览类内容 |
| **飞书 Sheets** | 中 | 需要复杂表格计算 |
| **截图插入** | 低 | 复杂表格，一次性展示 |

## 当前结论
**暂时无法在飞书 Docx 中通过 API 更新表格单元格内容。**

建议：
1. 简单表格用「无序列表」「有序列表」「引用块」替代
2. 复杂表格用飞书 Sheets 创建，然后在 Docx 中插入链接
3. 如有强需求，可联系飞书开放平台确认表格更新 API 的正确用法

## 相关文档
- `scripts/feishu_table_writer.py` - 研究代码（创建表格成功，更新失败）
- `procedural/feishu_docx_api_spec.md` - Block 构造规范

---
记录时间：2026-03-13
记录人：虾米 (CLO)
