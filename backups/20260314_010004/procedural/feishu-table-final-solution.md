# 飞书表格终极方案：零空行整装推送

> 2026-03-13 吕总确认的满分答案

## 核心原理

### 为什么这个方案没有空行？

1. **抢占先机（ID Pre-binding）**：在 table 块里显式写了 `children: ["temp_cell_0", ...]`，相当于盖房子时已经把门牌号定死了
2. **原子化交付（Atomic Delivery）**：飞书解析 descendants 时，发现单元格里已经住了内容块，不会启动"默认装修预案（生成空行）"
3. **引用闭环（The Loop）**：
   - table.children → 引用 cell_id
   - cell.children → 引用 text_id
   - ID不错位，表格100行也能一次性推过去

## 最终JSON结构

```json
{
  "children": [
    {
      "block_id": "temp_table",
      "block_type": 31,
      "table": { "property": { "row_size": 4, "column_size": 2 } },
      "children": ["temp_cell_0", "temp_cell_1", ...]  // 关键：提前占领！
    }
  ],
  "descendants": [
    { "block_id": "temp_cell_0", "block_type": 32, "children": ["temp_text_0"] },
    { "block_id": "temp_text_0", "block_type": 2, "text": { "elements": [{ "text_run": { "content": "内容" }}] } },
    ...
  ]
}
```

## Python代码模板

```python
def create_table_with_content(doc_id, data, rows, cols):
    """
    一次性创建带内容的表格，零空行
    
    Args:
        doc_id: 文档ID
        data: 平铺的数据列表，长度 = rows * cols
        rows: 行数
        cols: 列数
    """
    table_id = "temp_table"
    table_children = []
    descendants = []
    
    for i in range(rows * cols):
        cell_id = f"temp_cell_{i}"
        text_id = f"temp_text_{i}"
        
        # Table 引用 Cell
        table_children.append(cell_id)
        
        # Cell 引用 Text
        descendants.append({
            "block_id": cell_id,
            "block_type": 32,
            "children": [text_id]
        })
        
        # Text 内容
        clean = str(data[i]).strip().replace('\r', '').replace('\n', '')
        is_header = (i < cols)  # 第一行是表头
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
    
    # 完整请求
    payload = {
        "children": [{
            "block_id": table_id,
            "block_type": 31,
            "table": {"property": {"row_size": rows, "column_size": cols}},
            "children": table_children
        }],
        "descendants": descendants
    }
    
    return payload
```

## 临门一脚：复核清单

- [ ] **ID唯一性**：所有 `temp_cell_n` 和 `temp_text_n` 在同一个 descendants 列表中必须唯一，别重名
- [ ] **内容清洗**：填入 content 之前，执行 `str(val).strip().replace('\r', '').replace('\n', '')`
- [ ] **表头加粗**：第一行使用 `"text_element_style": {"bold": true}`

## 对比：旧方案 vs 新方案

| 方案 | 方式 | 结果 |
|------|------|:----:|
| 旧方案 | 分步创建（空表→填内容） | ❌ 有空行 |
| 新方案 | 整装推送（children + descendants） | ✅ 零空行 |

---

**铁律：飞书 API 需要的是"基因里就带了内容"的表格，不是"后装修"的表格。**
