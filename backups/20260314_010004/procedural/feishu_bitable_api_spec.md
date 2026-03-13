# Feishu Bitable API 技术规范

> 用于操作飞书多维表格（Bitable）
> 热点雷达追踪表使用此API

---

## 一、核心概念

### Bitable vs Docx 区别
| 产品 | API类型 | 用途 |
|------|---------|------|
| **Docx** | 文档API | 创建文字文档（Block结构）|
| **Bitable** | 多维表格API | 创建数据表（字段+记录）|

### Bitable 核心概念
- **App**：一个Bitable文件（如"热点雷达追踪表"）
- **Table**：数据表（一个App可以有多个表）
- **Field**：字段/列（如"标题"、"热度"）
- **Record**：记录/行（每条热点数据）

---

## 二、热点雷达追踪表结构

### 2.1 字段定义

| 字段名 | 字段类型 | 说明 |
|--------|----------|------|
| 标题 | 文本 | 热点标题 |
| 热度 | 数字 | 微信热度指数 |
| 分类 | 文本 | 热点分类标签 |
| 采集时间 | 日期时间 | 精确到分钟 |
| 原文链接 | 链接 | 溯源URL |
| 相关度 | 数字 | ★1-10分 |
| 话题头脑风暴 | 文本 | 文案虾拟的选题方向 |
| 爆款潜力分 | 数字 | 🔥1-10分（8-10分优先）|

### 2.2 飞书Bitable字段类型映射

| 我们的字段 | Bitable类型 | API字段类型 |
|------------|-------------|-------------|
| 标题 | 文本 | 1 |
| 热度 | 数字 | 2 |
| 分类 | 文本 | 1 |
| 采集时间 | 日期时间 | 5 |
| 原文链接 | 超链接 | 15 |
| 相关度 | 数字 | 2 |
| 话题头脑风暴 | 文本 | 1 |
| 爆款潜力分 | 数字 | 2 |

---

## 三、API操作示例

### 3.1 添加记录

```python
import json
import urllib.request

def add_record_to_bitable(app_token, table_id, fields, token):
    """
    向Bitable添加一条记录
    
    Args:
        app_token: Bitable App Token
        table_id: 表ID
        fields: 字段数据字典
        token: Tenant Access Token
    
    Returns:
        记录ID
    """
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records'
    
    data = json.dumps({
        "fields": fields
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['data']['record']['record_id']

# 使用示例
fields = {
    "标题": "某AI产品发布",
    "热度": 9850000,
    "分类": "科技",
    "采集时间": 1773316800000,  # 时间戳毫秒
    "原文链接": {"text": "查看原文", "link": "https://..."},
    "相关度": 8,
    "话题头脑风暴": "工业场景应用分析",
    "爆款潜力分": 9
}

record_id = add_record_to_bitable(
    app_token="Xb0abYaXlayTnNsU2Oocrp42nUh",
    table_id="tblxxx",
    fields=fields,
    token=tenant_token
)
```

### 3.2 批量添加记录

```python
def batch_add_records(app_token, table_id, records, token):
    """
    批量添加记录（每次最多500条）
    """
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'
    
    data = json.dumps({
        "records": [{"fields": r} for r in records]
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['data']['records']
```

### 3.3 查询记录

```python
def query_records(app_token, table_id, token, filter_str=None, sort=None):
    """
    查询记录
    
    Args:
        filter_str: 筛选条件（可选）
        sort: 排序规则（可选）
    """
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records'
    
    params = []
    if filter_str:
        params.append(f'filter={filter_str}')
    if sort:
        params.append(f'sort={sort}')
    
    if params:
        url += '?' + '&'.join(params)
    
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {token}'},
        method='GET'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['data']['items']
```

---

## 四、热点雷达工作流程（Bitable版）

```python
def save_hotspots_to_bitable(hotspots):
    """
    将采集的热点保存到Bitable
    
    Args:
        hotspots: 热点列表，每项包含标题、热度、分类、链接
    """
    # 配置
    app_token = "Xb0abYaXlayTnNsU2Oocrp42nUh"  # 热点雷达追踪表App Token
    table_id = "tblxxx"  # 表ID（需从飞书获取）
    
    # 获取token
    token = get_tenant_access_token()
    
    # 准备记录
    records = []
    current_time = int(datetime.now().timestamp() * 1000)
    
    for hotspot in hotspots:
        record = {
            "标题": hotspot['title'],
            "热度": hotspot['hotness'],
            "分类": hotspot['category'],
            "采集时间": current_time,
            "原文链接": {
                "text": "查看原文",
                "link": hotspot['url']
            },
            "相关度": None,  # 待文案虾填写
            "话题头脑风暴": None,  # 待文案虾填写
            "爆款潜力分": None  # 待文案虾填写
        }
        records.append(record)
    
    # 批量写入
    batch_add_records(app_token, table_id, records, token)
    print(f"✅ 已写入 {len(records)} 条热点到Bitable")
```

---

## 五、注意事项

1. **Bitable App Token** 在飞书表格URL中获取：`/base/{app_token}`
2. **Table ID** 需要调用API获取或从飞书开发者工具查看
3. **日期时间字段** 使用时间戳（毫秒）
4. **超链接字段** 格式：`{"text": "显示文本", "link": "URL"}`
5. **批量写入限制**：单次最多500条记录

---

## 六、与Docx API的区别总结

| 场景 | 使用API | 关键区别 |
|------|---------|----------|
| 写政策报告 | **Docx API** | Block结构、标题/段落/表格 |
| 写热点追踪 | **Bitable API** | 字段+记录、数据表结构 |

---

*创建时间: 2026-03-12*  
*用途: 热点雷达追踪表数据写入*
