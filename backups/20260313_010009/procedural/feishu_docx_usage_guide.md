# 飞书 Docx Block 构造函数使用示例

## 快速开始

### 方法1: 使用便捷函数（推荐）

```python
from scripts.feishu_docx_blocks import quick_create_document

# 准备 Markdown 内容
markdown = """
# AI维保产品全球市场分析报告

## 一、市场概览

全球预测性维护市场规模持续增长。

### 1.1 市场规模

- 2023年: 302亿人民币
- 2028年: 1,138亿人民币
- 年复合增长率: 30.3%

## 二、竞品分析

| 厂商 | 定价模式 | 单价 |
|------|----------|------|
| Augury | 订阅制 | 28,800-36,000 |
| Uptake | 订阅+实施 | 21,600-28,800 |

"""

# 创建文档
doc_id = quick_create_document(
    title="竞品分析报告",
    markdown=markdown,
    folder_token="Thhrfa3QglB5amdIMpEcY2tAndd",
    owner_open_id="ou_12dd9e55259701aeb2701dccf7f1ee54"
)

print(f"文档创建成功: https://ai-zhineng.feishu.cn/docx/{doc_id}")
```

---

### 方法2: 使用客户端类

```python
from scripts.feishu_docx_blocks import FeishuDocClient, MarkdownParser

# 初始化客户端
client = FeishuDocClient(app_id="cli_xxx", app_secret="xxx")

# 1. 创建空白文档
doc_id = client.create_document(
    title="测试文档",
    folder_token="Thhrfa3QglB5amdIMpEcY2tAndd"
)

# 2. 解析 Markdown
blocks = MarkdownParser.parse("# 标题\n\n正文内容")

# 3. 写入 Blocks
client.write_blocks(doc_id, blocks)

# 4. 添加权限
client.add_permission(doc_id, "ou_xxx")
```

---

### 方法3: 手动构造 Blocks

```python
from scripts.feishu_docx_blocks import (
    create_heading1, create_heading2, create_text,
    create_bullet, create_table, FeishuDocClient
)

# 手动构造 blocks
blocks = [
    create_heading1("一级标题"),
    create_heading2("二级标题"),
    create_text("这是普通文本"),
    create_bullet("列表项"),
    create_table([
        ["列1", "列2"],
        ["数据1", "数据2"]
    ])
]

# 写入文档
client = FeishuDocClient(app_id="xxx", app_secret="xxx")
doc_id = client.create_document("手动构造文档")
client.write_blocks(doc_id, blocks)
```

---

## Block 构造函数一览

| 函数 | 用途 | 示例 |
|------|------|------|
| `create_heading1(text)` | 一级标题 | `# 标题` |
| `create_heading2(text)` | 二级标题 | `## 标题` |
| `create_heading3(text)` | 三级标题 | `### 标题` |
| `create_text(text, **styles)` | 文本段落 | 普通文字 |
| `create_bullet(text)` | 无序列表 | `- 项目` |
| `create_numbered(text)` | 有序列表 | `1. 项目` |
| `create_code_block(code, lang)` | 代码块 | ```` ```python ```` |
| `create_table(rows, **opts)` | 表格 | `\| a \| b \|` |

---

## 支持的 Markdown 语法

### 标题
```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
```

### 列表
```markdown
- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2
```

### 表格
```markdown
| 表头1 | 表头2 |
|-------|-------|
| 数据1 | 数据2 |
| 数据3 | 数据4 |
```

### 代码块
```markdown
```python
def hello():
    print("Hello")
```
```

### 文本样式
```markdown
**粗体文本**
*斜体文本*
`行内代码`
```

---

## 完整示例：创建竞品分析报告

```python
from scripts.feishu_docx_blocks import quick_create_document

markdown = """
# AI维保产品全球市场分析报告

## Executive Summary

本报告分析了全球预测性维护市场的主要竞品。

## 一、市场概览

### 1.1 市场规模

全球预测性维护市场快速增长：

- **2023年**: 42亿美元（约302亿人民币）
- **2028年**: 158亿美元（约1,138亿人民币）
- **CAGR**: 30.3%

### 1.2 技术趋势

1. AI/ML 算法成熟化
2. 边缘计算普及
3. 数字孪生应用

## 二、竞品分析

### 2.1 定价对比

| 厂商 | 定价模式 | 单价(人民币/年/点) | 备注 |
|------|----------|-------------------|------|
| Augury | 订阅制 | 28,800-36,000 | 高端制造业 |
| Uptake | 订阅+实施 | 21,600-28,800 | 企业级客户 |
| Fiix | SaaS订阅 | 按用户收费 | 约72,000/5用户 |
| 蘑菇物联 | 订阅制 | 21,600-36,000 | 空压站场景 |

### 2.2 技术评分

| 厂商 | AI能力 | 易用性 | 性价比 |
|------|--------|--------|--------|
| Augury | 95 | 80 | 70 |
| Uptake | 88 | 75 | 75 |
| Fiix | 75 | 90 | 85 |

## 三、战略建议

基于以上分析，我们建议：

- 定价策略：定位 50% 于国际竞品
- 差异化：本地 7×24 服务
- 目标市场：轴承行业、空压站

"""

doc_id = quick_create_document(
    title="AI维保产品全球市场分析报告",
    markdown=markdown,
    folder_token="Thhrfa3QglB5amdIMpEcY2tAndd",
    owner_open_id="ou_12dd9e55259701aeb2701dccf7f1ee54"
)

print(f"✅ 文档创建成功!")
print(f"🔗 https://ai-zhineng.feishu.cn/docx/{doc_id}")
```

---

## 注意事项

1. **批量写入限制**: 单次最多 100 个 block，脚本自动分批处理
2. **表格必须对齐**: Markdown 表格的列数必须一致
3. **代码块语言**: 支持 python/javascript/java/go/rust 等常见语言
4. **权限设置**: 创建后记得添加权限，否则用户无法访问

---

## 参考文档

- **详细规范**: `procedural/feishu_docx_api_spec.md`
- **源码文件**: `scripts/feishu_docx_blocks.py`
- **行为规范**: `AGENTS.md` - 飞书文档 Block 构造函数规范
