# 飞书表格：零空行终极清洗补丁 (Zero-Newline Patch)

> 2026-03-13 吕总指令

## 问题
表格单元格内存在起始空行，影响美观。

## 根本原因
1. 字符串处理不当，content 里包含看不见的换行符（\n）
2. 可能多次注入 text block
3. Markdown 转换时添加了多余空白

## 解决方案：三位一体清洗逻辑

```python
# 必须先 strip 去除首尾空白，再 replace 掉内部可能残留的非法换行
clean_content = str(data_value).strip().replace('\r', '').replace('\n', '')
```

## 完整注入代码模板

```python
for i, cell_id in enumerate(cell_ids):
    # 三位一体清洗
    clean_content = str(data[i]).strip().replace('\r', '').replace('\n', '')
    
    # 只调用一次 POST
    requests.post(
        f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{cell_id}/children',
        headers=headers,
        json={"children": [{
            "block_type": 2,
            "text": {"elements": [{"text_run": {"content": clean_content}}]}
        }]}
    )
```

## 检查清单

- [ ] 是否执行了 `.strip().replace('\r', '').replace('\n', '')`？
- [ ] 每个 cell_id 是否只调用了一次 POST？
- [ ] 是否禁用了 Markdown 模拟行为（如 `| 内容 |` 变成 `\n内容\n`）？

---

**铁律：飞书 API 需要的是纯净的、无修饰的字符串。**
