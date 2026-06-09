#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书 Docx API Block 构造函数库
基于飞书开放平台 Docx v1 规范
核心原则：Markdown 必须拆解为结构化 Block

作者: 虾米 (CLO)
更新日期: 2026-03-12
"""

import json
import re
import urllib.request
from typing import List, Dict, Any, Optional


# ============================================================================
# Block Type 常量定义
# ============================================================================

class BlockType:
    """飞书文档 Block 类型常量"""
    TEXT = 2                    # 普通文本段落
    HEADING_1 = 3               # 一级标题
    HEADING_2 = 4               # 二级标题
    HEADING_3 = 5               # 三级标题
    HEADING_4 = 6               # 四级标题
    HEADING_5 = 7               # 五级标题
    HEADING_6 = 8               # 六级标题
    HEADING_7 = 9               # 七级标题
    HEADING_8 = 10              # 八级标题
    HEADING_9 = 11              # 九级标题
    BULLETED_LIST = 12          # 无序列表
    NUMBERED_LIST = 13          # 有序列表
    CODE_BLOCK = 14             # 代码块
    TABLE = 31                  # 表格
    TABLE_CELL = 32             # 表格单元格


# ============================================================================
# 语言代码映射（常用）
# ============================================================================

LANGUAGE_MAP = {
    'plain': 1, 'plaintext': 1, 'text': 1,
    'python': 58, 'py': 58,
    'javascript': 35, 'js': 35,
    'typescript': 72, 'ts': 72,
    'java': 34,
    'go': 29, 'golang': 29,
    'rust': 62, 'rs': 62,
    'sql': 68,
    'bash': 67, 'shell': 67, 'sh': 67,
    'json': 38,
    'yaml': 79, 'yml': 79,
    'markdown': 47, 'md': 47,
    'html': 32,
    'css': 22,
    'cpp': 11, 'c++': 11,
    'c': 9,
    'php': 55,
    'ruby': 61, 'rb': 61,
    'swift': 71,
    'kotlin': 39, 'kt': 39,
}


# ============================================================================
# Block 构造函数
# ============================================================================

def create_text_run(content: str, bold: bool = False, italic: bool = False, 
                    code: bool = False, underline: bool = False, 
                    strikethrough: bool = False) -> Dict[str, Any]:
    """
    创建文本运行元素
    
    Args:
        content: 文本内容
        bold: 是否加粗
        italic: 是否斜体
        code: 是否行内代码
        underline: 是否下划线
        strikethrough: 是否删除线
    
    Returns:
        text_run 字典
    """
    return {
        "text_run": {
            "content": content,
            "text_element_style": {
                "bold": bold,
                "italic": italic,
                "inline_code": code,
                "underline": underline,
                "strikethrough": strikethrough
            }
        }
    }


def create_text(content: str, bold: bool = False, italic: bool = False,
                align: int = 1, folded: bool = False) -> Dict[str, Any]:
    """
    创建文本段落 Block
    
    Args:
        content: 文本内容
        bold: 是否加粗
        italic: 是否斜体
        align: 对齐方式 (1=左对齐, 2=居中, 3=右对齐)
        folded: 是否折叠
    
    Returns:
        Block 字典
    """
    return {
        "block_type": BlockType.TEXT,
        "text": {
            "elements": [create_text_run(content, bold, italic)],
            "style": {
                "align": align,
                "folded": folded
            }
        }
    }


def create_heading(level: int, content: str, align: int = 1) -> Dict[str, Any]:
    """
    创建标题 Block
    
    Args:
        level: 标题级别 (1-9)
        content: 标题内容
        align: 对齐方式 (1=左对齐, 2=居中, 3=右对齐)
    
    Returns:
        Block 字典
    """
    if not 1 <= level <= 9:
        raise ValueError(f"标题级别必须在 1-9 之间，当前: {level}")
    
    block_type = BlockType.HEADING_1 + level - 1
    heading_key = f"heading{level}"
    
    return {
        "block_type": block_type,
        heading_key: {
            "elements": [{"text_run": {"content": content}}],
            "style": {"align": align}
        }
    }


# 快捷函数
def create_heading1(content: str, align: int = 1) -> Dict[str, Any]:
    """创建一级标题"""
    return create_heading(1, content, align)


def create_heading2(content: str, align: int = 1) -> Dict[str, Any]:
    """创建二级标题"""
    return create_heading(2, content, align)


def create_heading3(content: str, align: int = 1) -> Dict[str, Any]:
    """创建三级标题"""
    return create_heading(3, content, align)


def create_heading4(content: str, align: int = 1) -> Dict[str, Any]:
    """创建四级标题"""
    return create_heading(4, content, align)


def create_bullet(content: str) -> Dict[str, Any]:
    """
    创建无序列表项 Block
    
    Args:
        content: 列表项内容
    
    Returns:
        Block 字典
    """
    return {
        "block_type": BlockType.BULLETED_LIST,
        "bullet": {
            "elements": [{"text_run": {"content": content}}]
        }
    }


def create_numbered(content: str) -> Dict[str, Any]:
    """
    创建有序列表项 Block
    
    Args:
        content: 列表项内容
    
    Returns:
        Block 字典
    """
    return {
        "block_type": BlockType.NUMBERED_LIST,
        "numbered": {
            "elements": [{"text_run": {"content": content}}]
        }
    }


def create_code_block(code: str, language: str = 'plain') -> Dict[str, Any]:
    """
    创建代码块 Block
    
    Args:
        code: 代码内容
        language: 语言 (如 'python', 'javascript', 'json' 等)
    
    Returns:
        Block 字典
    """
    lang_code = LANGUAGE_MAP.get(language.lower(), 1)
    
    return {
        "block_type": BlockType.CODE_BLOCK,
        "code": {
            "elements": [{"text_run": {"content": code}}],
            "style": {
                "language": lang_code,
                "wrap": False
            }
        }
    }


def create_table_cell(content: str, bold: bool = False) -> Dict[str, Any]:
    """
    创建表格单元格 Block (第三层)
    
    ⚠️ 强制约束（解决首行空行问题）：
    1. 对文本内容执行 str().strip() 去除首尾空格和换行符
    2. 每个 table_cell 仅包含一个 text 块（单块原则）
    
    Args:
        content: 单元格内容
        bold: 是否加粗
    
    Returns:
        Block 字典
    """
    # 🔧 修复：强制执行 strip() 去噪，解决飞书表格首行空行问题
    cleaned_content = str(content).strip()
    
    return {
        "block_type": BlockType.TABLE_CELL,
        "table_cell": {
            "children": [
                {
                    "block_type": BlockType.TEXT,
                    "text": {
                        "elements": [create_text_run(cleaned_content, bold=bold)]
                    }
                }
            ]
        }
    }


def create_table(rows: List[List[str]], header_row: bool = True,
                 column_widths: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    创建表格 Block (三层嵌套模型)
    
    Table -> Table Cell -> Content Block
    
    Args:
        rows: 二维数组，每个元素是单元格内容
        header_row: 首行是否为标题行
        column_widths: 列宽数组，默认所有列 100
    
    Returns:
        Block 字典
    
    Example:
        >>> rows = [
        ...     ["年份", "市场规模"],
        ...     ["2023", "100亿"],
        ...     ["2024", "150亿"]
        ... ]
        >>> block = create_table(rows, header_row=True)
    """
    if not rows:
        raise ValueError("表格行数不能为 0")
    
    row_size = len(rows)
    column_size = len(rows[0])
    
    # 验证每行列数一致
    for i, row in enumerate(rows):
        if len(row) != column_size:
            raise ValueError(f"第 {i+1} 行列数不一致，期望 {column_size}，实际 {len(row)}")
    
    # 构建所有单元格
    cells = []
    for row_idx, row in enumerate(rows):
        for col_idx, cell_content in enumerate(row):
            # 首行且 header_row=True 时加粗
            is_header = header_row and row_idx == 0
            cells.append(create_table_cell(str(cell_content), bold=is_header))
    
    # 构建表格属性
    property_dict = {
        "row_size": row_size,
        "column_size": column_size,
        "header_row": header_row
    }
    
    if column_widths:
        property_dict["column_width"] = column_widths
    
    return {
        "block_type": BlockType.TABLE,
        "table": {
            "property": property_dict
        },
        "children": cells
    }


# ============================================================================
# Markdown 解析器
# ============================================================================

class MarkdownParser:
    """Markdown 到飞书 Block 的解析器"""
    
    @staticmethod
    def parse(markdown_text: str) -> List[Dict[str, Any]]:
        """
        将 Markdown 文本解析为飞书 Block 数组
        
        Args:
            markdown_text: Markdown 格式文本
        
        Returns:
            Block 字典列表
        """
        blocks = []
        lines = markdown_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # 空行跳过
            if not stripped:
                i += 1
                continue
            
            # 标题解析
            if stripped.startswith('# '):
                blocks.append(create_heading1(stripped[2:]))
            
            elif stripped.startswith('## '):
                blocks.append(create_heading2(stripped[3:]))
            
            elif stripped.startswith('### '):
                blocks.append(create_heading3(stripped[4:]))
            
            elif stripped.startswith('#### '):
                blocks.append(create_heading4(stripped[5:]))
            
            # 无序列表
            elif stripped.startswith('- ') or stripped.startswith('* '):
                blocks.append(create_bullet(stripped[2:]))
            
            # 有序列表
            elif re.match(r'^\d+\.\s', stripped):
                content = re.sub(r'^\d+\.\s', '', stripped)
                blocks.append(create_numbered(content))
            
            # 代码块
            elif stripped.startswith('```'):
                language = stripped[3:].strip() or 'plain'
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                code_text = '\n'.join(code_lines)
                blocks.append(create_code_block(code_text, language))
            
            # 表格
            elif '|' in stripped and i + 1 < len(lines):
                # 检查下一行是否是分隔线
                next_line = lines[i + 1].strip()
                if re.match(r'^\|?[\s\-:|]+\|?$', next_line):
                    table_lines = [stripped]
                    i += 2  # 跳过分隔线
                    while i < len(lines) and '|' in lines[i]:
                        table_lines.append(lines[i].strip())
                        i += 1
                    blocks.append(MarkdownParser._parse_table(table_lines))
                    continue  # 跳过 i += 1
            
            # 普通文本（支持粗体和斜体）
            else:
                blocks.append(MarkdownParser._parse_text(stripped))
            
            i += 1
        
        return blocks
    
    @staticmethod
    def _parse_text(text: str) -> Dict[str, Any]:
        """解析文本，支持粗体和斜体"""
        # 检测是否全为粗体
        if text.startswith('**') and text.endswith('**') and text.count('**') == 2:
            return create_text(text[2:-2], bold=True)
        
        # 检测是否全为斜体
        if text.startswith('*') and text.endswith('*') and text.count('*') == 2:
            return create_text(text[1:-1], italic=True)
        
        # 检测是否全为行内代码
        if text.startswith('`') and text.endswith('`') and text.count('`') == 2:
            return create_text(text[1:-1], code=True)
        
        # 普通文本
        return create_text(text)
    
    @staticmethod
    def _parse_table(lines: List[str]) -> Dict[str, Any]:
        """
        解析 Markdown 表格
        
        🔧 修复：规避 Markdown 转换器的"换行陷阱"
        - 忽略单元格内部的起始换行符
        - 对每个单元格内容执行 strip()
        """
        rows = []
        for i, line in enumerate(lines):
            # 跳过分隔线
            if i == 1 and re.match(r'^\|?[\s\-:|]+\|?$', line):
                continue
            
            # 解析单元格 - 关键：strip() 去除首尾换行符
            cells = [cell.strip() for cell in line.split('|')]
            # 过滤空字符串（首尾可能有空单元格）
            cells = [c for c in cells if c]
            if cells:
                rows.append(cells)
        
        return create_table(rows, header_row=True)


# ============================================================================
# 飞书文档 API 客户端
# ============================================================================

class FeishuDocClient:
    """飞书文档 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None
    
    def _get_tenant_access_token(self) -> str:
        """获取 tenant access token"""
        if self.token:
            return self.token
        
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
        data = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            self.token = result['tenant_access_token']
            return self.token
    
    def create_document(self, title: str, folder_token: Optional[str] = None) -> str:
        """
        创建空白文档
        
        Args:
            title: 文档标题
            folder_token: 文件夹 token（可选）
        
        Returns:
            文档 ID
        """
        url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
        
        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._get_tenant_access_token()}'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['data']['document']['document_id']
    
    def add_permission(self, doc_id: str, user_open_id: str, perm: str = 'full_access'):
        """
        添加文档权限
        
        Args:
            doc_id: 文档 ID
            user_open_id: 用户 OpenID
            perm: 权限类型 (full_access/edit/read)
        """
        url = f'https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/members/batch_create?type=docx'
        
        data = json.dumps({
            "members": [{
                "member_type": "openid",
                "member_id": user_open_id,
                "perm": perm
            }]
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._get_tenant_access_token()}'
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req):
                pass
        except Exception as e:
            print(f"添加权限失败: {e}")
    
    def write_blocks(self, doc_id: str, blocks: List[Dict[str, Any]], 
                     batch_size: int = 50) -> bool:
        """
        批量写入 Blocks 到文档
        
        Args:
            doc_id: 文档 ID
            blocks: Block 字典列表
            batch_size: 每批写入数量（最大 100）
        
        Returns:
            是否全部写入成功
        """
        if batch_size > 100:
            batch_size = 100
        
        url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children'
        
        success = True
        for i in range(0, len(blocks), batch_size):
            batch = blocks[i:i + batch_size]
            
            data = json.dumps({"children": batch}).encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self._get_tenant_access_token()}'
                },
                method='POST'
            )
            
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if result.get('code') != 0:
                        print(f"写入失败 ({i}-{i+len(batch)}): {result.get('msg')}")
                        success = False
                    else:
                        print(f"✅ 写入成功 ({i+1}-{i+len(batch)})")
            except Exception as e:
                print(f"写入异常 ({i}-{i+len(batch)}): {e}")
                success = False
        
        return success
    
    def create_document_from_markdown(self, title: str, markdown: str,
                                      folder_token: Optional[str] = None,
                                      owner_open_id: Optional[str] = None) -> str:
        """
        从 Markdown 创建完整文档
        
        Args:
            title: 文档标题
            markdown: Markdown 内容
            folder_token: 文件夹 token
            owner_open_id: 所有者 OpenID（用于添加权限）
        
        Returns:
            文档 ID
        """
        # 1. 创建空白文档
        doc_id = self.create_document(title, folder_token)
        print(f"✅ 文档创建: {doc_id}")
        
        # 2. 添加权限
        if owner_open_id:
            self.add_permission(doc_id, owner_open_id)
            print(f"✅ 权限已添加")
        
        # 3. 解析 Markdown
        blocks = MarkdownParser.parse(markdown)
        print(f"✅ Markdown 解析完成: {len(blocks)} blocks")
        
        # 4. 写入 Blocks
        success = self.write_blocks(doc_id, blocks)
        
        if success:
            print(f"✅ 文档写入完成")
        else:
            print(f"⚠️ 部分写入失败")
        
        return doc_id


# ============================================================================
# 便捷函数
# ============================================================================

def quick_create_document(title: str, markdown: str, 
                          config_path: str = '/root/.openclaw/openclaw.json',
                          folder_token: Optional[str] = None,
                          owner_open_id: Optional[str] = None) -> str:
    """
    快速创建文档（从配置文件读取凭据）
    
    Args:
        title: 文档标题
        markdown: Markdown 内容
        config_path: OpenClaw 配置文件路径
        folder_token: 文件夹 token
        owner_open_id: 所有者 OpenID
    
    Returns:
        文档 ID
    
    Example:
        >>> doc_id = quick_create_document(
        ...     "测试文档",
        ...     "# 标题\\n\\n这是正文",
        ...     folder_token="Thhrfa3QglB5amdIMpEcY2tAndd",
        ...     owner_open_id="ou_xxx"
        ... )
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    feishu = config.get('channels', {}).get('feishu', {})
    app_id = feishu.get('appId')
    app_secret = feishu.get('appSecret')
    
    client = FeishuDocClient(app_id, app_secret)
    return client.create_document_from_markdown(
        title, markdown, folder_token, owner_open_id
    )


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == '__main__':
    # 测试 Block 构造函数
    print("=" * 60)
    print("测试 Block 构造函数")
    print("=" * 60)
    
    # 测试标题
    h1 = create_heading1("这是一级标题")
    print(f"\n一级标题: {json.dumps(h1, ensure_ascii=False, indent=2)}")
    
    # 测试文本
    text = create_text("这是普通文本", bold=True)
    print(f"\n加粗文本: {json.dumps(text, ensure_ascii=False, indent=2)}")
    
    # 测试表格
    table = create_table([
        ["姓名", "年龄", "城市"],
        ["张三", "25", "北京"],
        ["李四", "30", "上海"]
    ], header_row=True)
    print(f"\n表格: {json.dumps(table, ensure_ascii=False, indent=2)[:500]}...")
    
    # 测试 Markdown 解析
    print("\n" + "=" * 60)
    print("测试 Markdown 解析")
    print("=" * 60)
    
    markdown = """# 文档标题

## 二级标题

这是普通段落。

- 列表项 1
- 列表项 2
- 列表项 3

1. 有序项 1
2. 有序项 2

| 姓名 | 年龄 |
|------|------|
| 张三 | 25   |
| 李四 | 30   |

```python
print("Hello World")
```
"""
    
    blocks = MarkdownParser.parse(markdown)
    print(f"\n解析结果: {len(blocks)} blocks")
    for i, block in enumerate(blocks):
        print(f"  [{i}] Type: {block['block_type']}")
