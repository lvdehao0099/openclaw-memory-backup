# Feishu Docx API 结构化写入技术规范

> 基于飞书开放平台 Docx v1 (2026-03-12)
> 核心原则：飞书新版文档（Docx）不支持直接解析 Markdown 字符串，所有内容必须拆解为独立的 Block

---

## 一、核心原则

### 1. 禁止直接写入 Markdown
- ❌ 错误：将 Markdown 字符串直接作为文本写入
- ✅ 正确：将 Markdown 拆解为独立的 Block 结构

### 2. TOC 识别规则
- 飞书的目录系统（TOC）仅识别特定 `block_type` 的块
- 不要尝试在 `text` 块中通过 `#` 或加粗来模拟标题

### 3. 表格三层嵌套模型
- 禁止将 Markdown 表格作为字符串写入
- 原生表格必须遵循 **Table -> Table Cell -> Content Block** 的三层嵌套模型

---

## 二、Block Type 映射表

| Block Type | 常量值 | 用途 | 说明 |
|------------|--------|------|------|
| TEXT | 2 | 普通文本段落 | 基础文本块 |
| HEADING_1 | 3 | 一级标题 | TOC可识别 |
| HEADING_2 | 4 | 二级标题 | TOC可识别 |
| HEADING_3 | 5 | 三级标题 | TOC可识别 |
| HEADING_4 | 6 | 四级标题 | TOC可识别 |
| HEADING_5 | 7 | 五级标题 | TOC可识别 |
| HEADING_6 | 8 | 六级标题 | TOC可识别 |
| HEADING_7 | 9 | 七级标题 | TOC可识别 |
| HEADING_8 | 10 | 八级标题 | TOC可识别 |
| HEADING_9 | 11 | 九级标题 | TOC可识别 |
| BULLETED_LIST | 12 | 无序列表 | 子弹列表 |
| NUMBERED_LIST | 13 | 有序列表 | 数字列表 |
| CODE_BLOCK | 14 | 代码块 | 支持语言高亮 |
| TABLE | 31 | 表格 | 表格容器 |
| TABLE_CELL | 32 | 表格单元格 | 表格内容容器 |

---

## 三、Block 构造函数规范

### 3.1 标题构造

```python
# 一级标题
def create_heading1(text):
    return {
        "block_type": 3,
        "heading1": {
            "elements": [
                {
                    "text_run": {
                        "content": text,
                        "text_element_style": {}
                    }
                }
            ],
            "style": {"align": 1}  # 1=左对齐, 2=居中, 3=右对齐
        }
    }

# 二级标题
def create_heading2(text):
    return {
        "block_type": 4,
        "heading2": {
            "elements": [{"text_run": {"content": text}}],
            "style": {"align": 1}
        }
    }
```

### 3.2 文本段落构造

```python
def create_text(text, bold=False, italic=False, code=False):
    return {
        "block_type": 2,
        "text": {
            "elements": [
                {
                    "text_run": {
                        "content": text,
                        "text_element_style": {
                            "bold": bold,
                            "italic": italic,
                            "inline_code": code,
                            "strikethrough": False,
                            "underline": False
                        }
                    }
                }
            ],
            "style": {"align": 1, "folded": False}
        }
    }
```

### 3.3 列表构造

```python
# 无序列表
def create_bullet(text):
    return {
        "block_type": 12,
        "bulleted_list": {
            "elements": [{"text_run": {"content": text}}]
        }
    }

# 有序列表
def create_numbered(text):
    return {
        "block_type": 13,
        "numbered_list": {
            "elements": [{"text_run": {"content": text}}]
        }
    }
```

### 3.4 代码块构造

```python
def create_code_block(code_text, language=1):
    """
    language: 1=PlainText, 2=ABAP, 3=Ada, 4=Apache, 5=Apex, ...
    常见：7=Bash, 9=C, 11=C++, 17=CoffeeScript, 21=CSP, 22=CSS, 23=Dart,
         24=Django, 25=Dockerfile, 29=Go, 30=Groovy, 31=Haskell, 32=HTML,
         33=HTTP, 34=Java, 35=JavaScript, 38=JSON, 39=Kotlin, 42=LaTeX,
         43=Less, 44=Lisp, 45=Lua, 47=Markdown, 49=MATLAB, 50=Nginx,
         51=Objective-C, 53=Pascal, 54=Perl, 55=PHP, 56=PowerShell,
         57=Protobuf, 58=Python, 59=R, 61=Ruby, 62=Rust, 63=SAS, 64=Scala,
         65=Scheme, 66=SCSS, 67=Shell, 68=SQL, 71=Swift, 72=TypeScript,
         74=VBScript, 75=Verilog, 76=VHDL, 78=XML, 79=YAML
    """
    return {
        "block_type": 14,
        "code": {
            "elements": [{"text_run": {"content": code_text}}],
            "style": {"language": language, "wrap": False}
        }
    }
```

### 3.5 表格构造（三层嵌套）

#### ⚠️ 表格首行空行修复铁律（2026-03-12强制执行）

**根本原因：** 飞书的 `text_run.content` 只要包含一个 `\n`，文档就会多渲染一行空行。

**修复措施（三重保障）：**

1. **代码级修复：强制执行 `str().strip()`**
   ```python
   # ❌ 错误写法
   content = cell_data
   
   # ✅ 正确写法
   content = str(cell_data).strip()
   ```

2. **结构级修复：检查 children 数组长度**
   - 每个 `table_cell` (Type 32) 的 `children` 数组中，**有且只有一个** text 块
   - 排雷：检查是否先创建了空 text 块占位，又添加了新 text 块 → 合并它们

3. **Markdown 转换修复：忽略单元格内部起始换行符**
   - Markdown 表格解析时，为保持对齐会在单元格首尾保留 `\n`
   - 修复指令：`cell.strip()` 强制去除

```python
def create_table_cell(text):
    """表格单元格 - 第三层
    强制约束：
    1. 对文本内容执行 str().strip() 去除首尾空格和换行符（解决首行空行问题）
    2. 每个 table_cell 仅包含一个 text 块（单块原则，避免冗余空块）
    """
    # 🔧 修复：强制执行 strip() 去噪，解决飞书表格首行空行问题
    cleaned_text = str(text).strip()
    
    return {
        "block_type": 32,
        "table_cell": {
            "children": [
                {
                    "block_type": 2,
                    "text": {
                        "elements": [{"text_run": {"content": cleaned_text}}]
                    }
                }
            ]
        }
    }

def create_table(rows_data, header_row=True):
    """
    表格构造 - 三层嵌套模型
    rows_data: 二维数组，如 [["年份", "市场规模"], ["2023", "100亿"]]
    """
    row_size = len(rows_data)
    column_size = len(rows_data[0]) if rows_data else 0
    
    # 构建所有单元格
    cells = []
    for row in rows_data:
        for cell_text in row:
            # 单元格内容已在 create_table_cell 中自动执行 strip()，无需额外处理
            cells.append(create_table_cell(cell_text))
    
    return {
        "block_type": 31,
        "table": {
            "property": {
                "row_size": row_size,
                "column_size": column_size,
                "header_row": header_row,
                "column_width": [100] * column_size  # 默认列宽
            }
        },
        "children": cells
    }
```

---

## 四、Markdown 到 Block 转换逻辑

### 4.1 解析流程

```python
def markdown_to_blocks(markdown_text):
    """
    将 Markdown 文本转换为飞书 Block 数组
    """
    blocks = []
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 标题解析
        if line.startswith('# '):
            blocks.append(create_heading1(line[2:]))
        elif line.startswith('## '):
            blocks.append(create_heading2(line[3:]))
        elif line.startswith('### '):
            blocks.append(create_heading3(line[4:]))
        
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append(create_bullet(line[2:]))
        
        # 有序列表
        elif re.match(r'^\d+\. ', line):
            blocks.append(create_numbered(re.sub(r'^\d+\. ', '', line)))
        
        # 代码块
        elif line.startswith('```'):
            code_lines = []
            language = line[3:].strip() or 'plain'
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            blocks.append(create_code_block(code_text, language))
        
        # 表格（简化处理）
        elif '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
            table_lines = [line]
            i += 2  # 跳过分隔线
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            blocks.append(parse_markdown_table(table_lines))
            continue
        
        # 普通文本
        elif line.strip():
            blocks.append(create_text(line))
        
        i += 1
    
    return blocks
```

### 4.2 批量写入策略

```python
def write_blocks_to_document(doc_id, blocks, token, batch_size=50):
    """
    批量写入 blocks 到飞书文档
    注意：飞书 API 每次最多写入 100 个 block，建议分批
    """
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        
        request_body = {"children": batch}
        
        req = urllib.request.Request(
            f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children',
            data=json.dumps(request_body).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') != 0:
                print(f"写入失败: {result.get('msg')}")
            else:
                print(f"写入成功: {len(batch)} blocks")
```

---

## 五、完整示例代码

```python
import json
import urllib.request

def create_feishu_document(title, folder_token, markdown_content, token):
    """
    创建飞书文档并写入 Markdown 内容
    """
    # 1. 创建空文档
    doc_data = json.dumps({
        "title": title,
        "folder_token": folder_token
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/docx/v1/documents',
        data=doc_data,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        doc_id = result['data']['document']['document_id']
    
    # 2. 转换 Markdown 为 Blocks
    blocks = markdown_to_blocks(markdown_content)
    
    # 3. 批量写入
    write_blocks_to_document(doc_id, blocks, token)
    
    return doc_id
```

---

## 六、注意事项

1. **block_type 必须使用整数**，不是字符串
2. **children 数组** 用于嵌套结构（如表格、列表）
3. **text_run 中的 content** 不能包含换行符（代码块除外）
4. **表格必须先创建 table block**，然后创建 table_cell children
5. **批量写入限制**：单次请求最多 100 个 block，建议分批处理
6. **权限**：创建文档后记得添加用户权限，否则用户无法访问

---

## 七、语言代码映射（常用）

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
| C | 9 |
| PHP | 55 |
| Ruby | 61 |
| Swift | 71 |
| Kotlin | 39 |

完整列表参见飞书开放平台文档。
