#!/usr/bin/env python3
"""
微信热点采集脚本 - 2026-03-12
从 tophub.today 采集微信24h热文榜
"""

import sys
import json
import urllib.request
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

def get_tenant_access_token():
    """获取飞书tenant access token"""
    with open('/root/.openclaw/openclaw.json', 'r') as f:
        config = json.load(f)
    
    feishu = config.get('channels', {}).get('feishu', {})
    app_id = feishu.get('appId')
    app_secret = feishu.get('appSecret')
    
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
    data = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['tenant_access_token']

def fetch_tophub_wechat():
    """
    从 tophub.today 采集微信热榜
    由于网站可能有反爬，先尝试直接请求
    """
    url = 'https://tophub.today/n/WnBe01o371'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"采集失败: {e}")
        return None

def parse_hotspots(html):
    """
    解析HTML提取热点数据
    由于网站结构可能变化，这里使用简单的正则匹配
    """
    import re
    
    hotspots = []
    
    # 尝试匹配标题和链接
    # 注意：实际解析需要根据网站具体HTML结构调整
    pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for i, (link, title) in enumerate(matches[:10]):
        if title.strip() and len(title.strip()) > 5:
            hotspots.append({
                'title': title.strip(),
                'url': link if link.startswith('http') else f"https://tophub.today{link}",
                'hotness': 1000000 - i * 50000,  # 模拟热度
                'category': '待分类'
            })
    
    return hotspots[:10]

def save_to_bitable(hotspots):
    """保存到飞书Bitable热点雷达追踪表"""
    
    # 配置信息
    app_token = "Xb0abYaXlayTnNsU2Oocrp42nUh"  # 需要从飞书获取
    table_id = "tblxxx"  # 需要从飞书获取
    
    token = get_tenant_access_token()
    current_time = int(datetime.now().timestamp() * 1000)
    
    records = []
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
            "相关度": None,
            "话题头脑风暴": None,
            "爆款潜力分": None
        }
        records.append(record)
    
    # 批量写入Bitable
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
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ 成功写入 {len(records)} 条热点到Bitable")
            return True
    except Exception as e:
        print(f"❌ 写入Bitable失败: {e}")
        # 如果Bitable写入失败，先保存到本地
        with open('/tmp/hotspots_backup_20260312.json', 'w') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"📁 已备份到本地: /tmp/hotspots_backup_20260312.json")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("微信热点采集 - 2026-03-12")
    print("=" * 60)
    
    # 采集
    print("\n📡 正在采集 tophub.today...")
    html = fetch_tophub_wechat()
    
    if html:
        hotspots = parse_hotspots(html)
        print(f"\n📊 采集到 {len(hotspots)} 条热点:\n")
        
        for i, h in enumerate(hotspots, 1):
            print(f"{i}. {h['title'][:40]}...")
        
        # 保存
        print("\n💾 正在保存到飞书Bitable...")
        save_to_bitable(hotspots)
    else:
        print("❌ 采集失败，请检查网络或网站状态")
        sys.exit(1)
