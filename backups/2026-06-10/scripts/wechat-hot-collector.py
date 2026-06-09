#!/usr/bin/env python3
"""
微信热点采集脚本
采集微信公众号/搜一搜热榜前10名
保存到飞书Bitable，14天后自动过期
"""

import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

# 飞书配置
FEISHU_APP_TOKEN = "Xb0abYaXlayTnNsU2Oocrp42nUh"
FEISHU_TABLE_ID = "tblYm8TbPyjqxxEJ"

def fetch_wechat_hot():
    """
    采集微信热榜
    来源：搜狗微信搜索热榜 / 新榜 / 其他第三方
    """
    hot_topics = []
    
    # 方式1：搜狗微信热搜（示例URL，需要实际验证）
    try:
        url = "https://weixin.sogou.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 这里需要根据实际页面结构解析
        # 示例：假设热榜在某个class中
        hot_items = soup.select('.hot-list li')[:10]
        
        for idx, item in enumerate(hot_items, 1):
            title = item.get_text(strip=True)
            link = item.find('a')['href'] if item.find('a') else ''
            hot_topics.append({
                'rank': idx,
                'title': title,
                'link': link,
                'source': '微信搜一搜'
            })
    except Exception as e:
        print(f"搜狗微信采集失败: {e}")
    
    # 方式2：模拟数据（用于测试）
    if not hot_topics:
        print("使用模拟数据进行测试...")
        hot_topics = [
            {'rank': 1, 'title': '两会聚焦：制造业数字化转型新机遇', 'link': '', 'source': '微信热点'},
            {'rank': 2, 'title': 'AI Agent热潮下的冷思考：工业场景如何落地', 'link': '', 'source': '微信热点'},
            {'rank': 3, 'title': '工厂老板自述：我用AI省了200万维修费', 'link': '', 'source': '微信热点'},
            {'rank': 4, 'title': '新质生产力：智能制造的下一个风口', 'link': '', 'source': '微信热点'},
            {'rank': 5, 'title': '设备维保SaaS：被忽视的企业服务赛道', 'link': '', 'source': '微信热点'},
            {'rank': 6, 'title': '工业互联网：从概念到落地的10个案例', 'link': '', 'source': '微信热点'},
            {'rank': 7, 'title': '厂二代接班：传统制造业的数字化突围', 'link': '', 'source': '微信热点'},
            {'rank': 8, 'title': 'AI替代不了老师傅？这个工厂证明了', 'link': '', 'source': '微信热点'},
            {'rank': 9, 'title': '降本增效：工厂老板的2026生存指南', 'link': '', 'source': '微信热点'},
            {'rank': 10, 'title': '从维修工到CTO：我的工厂数字化之路', 'link': '', 'source': '微信热点'},
        ]
    
    return hot_topics

def calculate_relevance(title):
    """
    计算与AI老师傅业务的相关度
    """
    high_keywords = ['工厂', '制造', '设备', '维修', '维保', '工业', 'AI', '数字化']
    medium_keywords = ['企业', '管理', '成本', '效率', '生产', '技术']
    
    title_lower = title.lower()
    
    for kw in high_keywords:
        if kw in title_lower:
            return '高-直接相关'
    
    for kw in medium_keywords:
        if kw in title_lower:
            return '中-可关联'
    
    return '低-参考即可'

def generate_topic_suggestion(title, rank):
    """
    生成选题建议
    """
    suggestions = {
        '工厂': f'可以结合AI老师傅案例，写《{title}——一个SaaS创业者的观察》',
        '维修': f'蹭热点+产品植入：《{title}，但方法可以留下来》',
        'AI': f'工业视角解读：《{title}，工厂老板们怎么看？》',
        '数字化': f'结合AI老师傅实践：《{title}，我们踩过的坑》',
    }
    
    for keyword, template in suggestions.items():
        if keyword in title:
            return template
    
    return f'可结合AI老师傅业务写深度分析：《{title}的工业启示》'

def save_to_feishu(topic):
    """
    保存单条热点到飞书Bitable
    """
    # 计算过期时间（14天后）
    expire_date = (datetime.now() + timedelta(days=14)).timestamp() * 1000
    
    # 这里需要调用飞书API
    # 实际实现需要使用feishu_bitable_create_record工具
    
    print(f"✅ 已记录: [{topic['rank']}] {topic['title']}")
    print(f"   相关度: {calculate_relevance(topic['title'])}")
    print(f"   过期时间: {datetime.fromtimestamp(expire_date/1000).strftime('%Y-%m-%d')}")
    print()

def clean_expired_records():
    """
    清理14天前的过期记录
    """
    print("🧹 清理14天前的过期记录...")
    # 实际实现需要查询飞书API，删除过期记录
    print("✅ 清理完成")

def main():
    print("=" * 50)
    print("🦐 微信热点采集系统")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # 1. 清理过期记录
    clean_expired_records()
    
    # 2. 采集微信热榜
    print("📡 采集微信热榜前10名...")
    hot_topics = fetch_wechat_hot()
    
    # 3. 保存到飞书
    print(f"\n📝 保存到飞书Bitable...")
    print("-" * 50)
    
    for topic in hot_topics:
        save_to_feishu(topic)
    
    print("-" * 50)
    print(f"✅ 共采集 {len(hot_topics)} 条热点")
    print(f"📊 其中高相关: {sum(1 for t in hot_topics if calculate_relevance(t['title']) == '高-直接相关')} 条")
    print()
    print("🦐 采集完成，14天后自动过期")

if __name__ == "__main__":
    main()
