#!/usr/bin/env python3
"""
热点数据批量写入飞书 Bitable - 2026-03-13 晚班
"""
import json
import urllib.request
import sys
from datetime import datetime, timedelta

# 配置
FEISHU_APP_ID = "cli_a92780ca08b89bb6"
FEISHU_APP_SECRET = "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"
APP_TOKEN = "Xb0abYaXlayTnNsU2Oocrp42nUh"
TABLE_ID = "tblYm8TbPyjqxxEJ"

def get_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
    data = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['tenant_access_token']

def create_record(title, source, url, rank, suggestion):
    """创建单条记录"""
    expire_time = int((datetime.now() + timedelta(days=14)).timestamp() * 1000)
    
    record = {
        "fields": {
            "热点标题": title,
            "来源": source,
            "热度排名": rank,
            "相关度": "待评估",
            "状态": "待处理",
            "选题建议": suggestion,
            "过期时间": expire_time,
            "原文链接": {"text": "查看原文", "link": url} if url else None
        }
    }
    return record

def batch_create_records(token, records):
    """批量写入记录"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create'
    
    data = json.dumps({"records": records}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        return {"code": -1, "msg": str(e)}

if __name__ == '__main__':
    print("=" * 60)
    print("微信热点写入 - 2026-03-13 20:00 晚班")
    print("=" * 60)
    
    # 从JSON文件读取热点数据
    with open('scripts/hotspot_data_20260313.json', 'r', encoding='utf-8') as f:
        hotspots = json.load(f)
    
    # 获取token
    print(f"\n📡 获取飞书 Token...")
    token = get_token()
    print("✅ Token 获取成功")
    
    # 构造记录
    records = []
    for h in hotspots:
        records.append(create_record(h['title'], h['source'], h['url'], h['rank'], h['suggestion']))
    
    # 批量写入
    print(f"\n💾 写入 {len(records)} 条热点到 Bitable...")
    result = batch_create_records(token, records)
    
    if result.get('code') == 0:
        print(f"✅ 成功写入 {len(records)} 条热点")
        print(f"📊 表格地址: https://ai-zhineng.feishu.cn/base/{APP_TOKEN}")
    else:
        print(f"❌ 写入失败: {result.get('msg')}")
        print(f"详细错误: {json.dumps(result, ensure_ascii=False, indent=2)}")
        sys.exit(1)
