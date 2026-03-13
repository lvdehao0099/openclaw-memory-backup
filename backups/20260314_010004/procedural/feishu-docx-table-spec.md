# 飞书 Docx 表格内容填充技术规范 (2026-03-12 版)

## 核心痛点：为什么只创建了空表格？

**原因：** 表格（Type 31）由单元格（Type 32）组成，但单元格是容器型块。你只定义了容器，没有为容器定义子块（Children）。

---

## 1. 块级嵌套逻辑（必须严格遵守）

要让表格里有字，必须构建以下**三层树状结构**：

```
1. Table Block (Type 31): 定义行数、列数
        ↓
2. Table Cell Block (Type 32): 这是表格的格子
        ↓
3. Content Block (如 Type 2 - Text): 真正的文字内容，必须挂载在单元格下面
```

---

## 2. 推荐方案：使用"创建嵌套块 (Create Nested Blocks)"

**不要先创建表格再填内容**，那会导致 API QPS 频繁报 429。

**推荐使用 descendants（后代节点）模式**一次性推送到 `/children` 接口。

### AI 学习示例 (JSON 结构)

以下是一个 1 行 1 列且包含"数据加载中"文字的表格请求体：

```json
{
  "children": [
    {
      "block_type": 31,  // 第一层：表格
      "table": {
        "property": { "row_size": 1, "column_size": 1 }
      },
      "children": [  // ← 注意这里！表格直接包含单元格
        {
          "block_type": 32,  // 第二层：单元格容器
          "children": [  // ← 单元格包含内容
            {
              "block_type": 2,  // 第三层：真正的文本块
              "text": {
                "elements": [{ "text_run": { "content": "这里才是填内容的地方！" } }]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 3. 给 AI 开发助手的行动指南

### 3.1 数据映射
编写一个嵌套循环：
- **外层**：遍历行（Row）
- **内层**：遍历列（Column）

### 3.2 原子封装
每一个 cell 的 children 数组里，**必须至少包含一个 block_type: 2 (Text) 的对象**。

### 3.3 排雷（重要！）
**严禁**直接在 table_cell 级别尝试添加 text_run 属性，飞书后端会直接报错或忽略。

**内容必须包裹在 text 块内。**

### 3.4 性能优化
飞书单次请求建议块数量不超过 50 个。如果表格非常大（如超过 10x10）：
- 拆分请求
- 先创建表格空壳
- 获取 block_id 后
- 分批向单元格写入子块

---

## 4. Python 实现模板

```python
def create_cell(content):
    """创建表格单元格 - 包含文本内容"""
    return {
        "block_type": 32,  # Table Cell
        "children": [      # ← 直接children，不是table_cell.children
            {
                "block_type": 2,  # Text Block
                "text": {
                    "elements": [
                        {"text_run": {"content": content}}
                    ]
                }
            }
        ]
    }

def create_table(rows, cols, cell_data):
    """创建带内容的表格"""
    cells = []
    for r in range(rows):
        for c in range(cols):
            content = cell_data[r][c]  # 从二维数组获取内容
            cells.append(create_cell(content))
    
    return {
        "block_type": 31,  # Table Block
        "table": {
            "property": {
                "row_size": rows,
                "column_size": cols
            }
        },
        "children": cells   # ← 表格的children就是单元格列表
    }

# 使用示例
table_data = [
    ["年份", "市场规模", "增长", "备注"],
    ["2023", "302亿", "-", "基准年"],
    ["2024", "393亿", "+30%", "预测"],
]

table_block = create_table(3, 4, table_data)

# 一次性推送到API
requests.post(
    f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
    json={"children": [table_block]},
    headers={"Authorization": f"Bearer {token}"}
)
```

---

## 5. 常见错误对照

| 错误做法 | 正确做法 | 错误原因 |
|---------|---------|---------|
| 用文本ASCII字符画模拟表格 | 使用block_type 31+32 | 不是真正的表格 |
| 先创建空表格，再逐个填内容 | 使用descendants一次性推送 | 容易429，性能差 |
| `"table_cell": {"text_run": {...}}` | `"children": [{"block_type": 2, "text": {...}}]` | 内容必须包裹在text块内 |
| 表格的children放在table对象里 | 表格的children和table同级 | 结构层级错误 |

---

**记录时间：2026-03-12**
**学习来源：用户实战经验总结**
