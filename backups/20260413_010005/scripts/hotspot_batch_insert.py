#!/usr/bin/env python3
"""
热点数据批量写入飞书 Bitable
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

def create_record(token, title, source, url, rank, suggestion):
    """创建单条记录"""
    expire_time = int((datetime.now() + timedelta(days=14)).timestamp() * 1000)
    
    record = {
        "fields": {
            "热点标题": title,
            "来源": source,
            "热度排名": rank,  # 数字类型
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
    print("微信热点写入 - 2026-03-12 20:45")
    print("=" * 60)
    
    # 准备数据
    hotspots = [
        {
            "title": "追Ai热点的投资并不理性!",
            "source": "楠叔物理高效课堂",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9QzbJ7ynLcQDiaKarEkm-aVa8yhAK5XC7BU99JGpxMh8_taxbhFME1VFzkhNZ5zAHr4R5Juap1bE3NStts-j7haUm4I95XBGlxfTCIOBdfRGdxhISIYytSJ2-gf_7UC8ACCeJMXopfjD0k0U6I3qVg02jH9yDBzsZ2X112q4GnC5j32-j2KiwUw..",
            "rank": 1,
            "suggestion": "《AI投资热潮下，工业AI如何避免泡沫？》反焦虑角度+AI老师傅落地案例"
        },
        {
            "title": "聚焦两会:民营会成为制造业的主力军吗?",
            "source": "行走猎奇PY",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUk771UK9N0gps-Ev5dhNY6FqXa8Fplpd9fx9pvbPNbniYCNUShCcCH6Jyv4j8lcoAd8OWMtfE33Ap7_Df1n3Pnd_YOyEmmPyqNIeDPOZ-StQSXjmWln_MrIZL-LqrvyRml_QcyfgcD_8jqoT-cRkRq_KX7cz_0gQw7_x9k6b0gIigbMvdajoaZH6aoP0q4EEBis2_znk4pSRCy6umSSPEsg..",
            "rank": 2,
            "suggestion": "《民营制造业主力军：AI老师傅如何帮助中小企业降本增效？》两会热点+政策机会"
        },
        {
            "title": "提升青少年人工智能素养、探索新型育人模式...直面AI时代育人之问",
            "source": "人民教育",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUsFwUawV8rtRs-Ev5dhNY6FqXa8Fplpd9g4NyZ0fy-9Rmi6ulQr9CIaPZB9cl9J7iXJD1JmpSAxHCEyCYTrVz1ZqG4RPtBTXfcqCAiuzjj6iabuj2WZcjpHaTWZwmEcmIreclMQ-FSyJptAI8n3WhF-BGFXqE7yHKeK04o1mUH1AqIjQ8QLN-Oz3yUSMmLQvNVo5YocxxjifdrgozfSg6bw..",
            "rank": 3,
            "suggestion": "《AI时代育人：从学校到工厂，技术传承的新路径》教育角度+工业培训场景"
        },
        {
            "title": "丝路外贸热点 | 美对中国等16个经济体启动新一轮301调查",
            "source": "新丝路数字外贸研究院",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9mQbmMi4bfbjzfGix6rKJ47FFwphM_rKa27BqkfXjqX05e-8mkuwcWb3Q_Tz8mFGVrDaVs15FDfh3oththS_ZFmDLRkPiQRcMiVduIStWbyOYkjkcAuCDwYQB3Ih5lgLf5shkrFX6Np7iak3sMpTK2qZ-reAR8OtI7ZAGVp8b6DPuL0unUdKkuw..",
            "rank": 4,
            "suggestion": "《贸易战背景下，中国制造如何用AI提升核心竞争力？》宏观角度+技术自主"
        },
        {
            "title": "记者听两会 制造业\"智\"变",
            "source": "湖南卫视新闻联播",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUk771UK9N0gps-Ev5dhNY6FqXa8Fplpd9eLUGDl1UJEjLgSvzLOnX340728jkEpyYwlUP1ilObD8SLQ1oZIQ3pcn6ULmNFAqmm619qqENEkioACammeV3MPCoXXg0bVbAeQpgxxoHy9VzVDskrCaKeqUgUttPHNPS6ukJ6VJjpA58ZpqNUIpaD8Qyj3w4lTUCitfPnZVrZFDvzHZXxeLdyg..",
            "rank": 5,
            "suggestion": "《制造业\"智\"变：湖南案例与AI老师傅的全国机会》地方政策+落地案例"
        },
        {
            "title": "【26-3-12】热点记录 板池整理!(附 技术的开窍理解)",
            "source": "饶哥果园",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9K_7YT2cq_a5d_nrjmMjAwUoQ0dI64RmEx95vNdooCAqnHV2_RvShSwVm4wjYFy_4JUx8XUfpft-kEmHyOOpEtWn8tj5P3wK1E-3H7a-uaHPlAiDGZEYRTBk-EZhItzxpC7Bcqz2lIT7G597GZ7r4XRyYElZZcxyor7YWkSkHNTACYioxHkzTmA..",
            "rank": 6,
            "suggestion": "暂不跟进（股市热点，与工业AI关联度低）"
        },
        {
            "title": "等待新热点",
            "source": "奶爸V全职十年",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9NYZDx_WWhHP6o3HDQ_4uE7_I-GKa5xF-czG0LmoHIhwi7v-86WtVJzOzUkMflN_M70SfA-gCFymO-qTTioHiFnXdeNuDWDWx3EYfOQhh63fTKtUfJkBv8MjRwc2lFRapLWbXqeVdeg5jW4Q8m4EwSQBnKYgHZihLtGLLtj2nTs9e0WC6Sbi7DA..",
            "rank": 7,
            "suggestion": "暂不跟进（投资心态类，与工业AI关联度低）"
        },
        {
            "title": "别被生物热点冲昏头!生物科学报考,家长必须看清真相",
            "source": "小友伴学生涯",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9BiIFNgnhlSGiN7nPlld5LzooYGUYURbFYzv3haR7tgN7yTaTTtXCFup5pgJDrHxcLnhFFHfjaVlP0TqxqSgDk9HXbRW9TeD-sg_nXSLkpuwf9WGqmfxyR_Wpma5B4Wq9p15o2XrpCl1eW_bR8NqP5DUUOM8DVcfQRI-2-QYCHCn6zvkPgoArRQ..",
            "rank": 8,
            "suggestion": "暂不跟进（教育报考类，与工业AI关联度低）"
        },
        {
            "title": "申论热点 | 培育壮大县域富民产业",
            "source": "吉林华图基层考试资讯中心",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd9hzd7y5hg2QHynvsTTBxrE89YiWEf0mM-2V99fRGOZ--_JjVcSda_mhJ1oppKmxz_PjVTB2mj3tdRI_hqK8vThkhxvD3C_kk2hOxPr73xiDr6zv4O39atAFmbps0UE2086ZJmbf3xwxQFve6NfaBgrrsOyBd3Y4qXy8164JeDxDPyPfCoem7FzA..",
            "rank": 9,
            "suggestion": "暂不跟进（公考类，与工业AI关联度低）"
        },
        {
            "title": "26文博考研复试,抽空再过一遍热点~",
            "source": "尚书文博辅导",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7U7JtyZ3kMUJXFR5eTzsxRs-Ev5dhNY6FqXa8Fplpd93uaxmo0AFYPH32XIJwo7RSJRDSwox8TMI75HIHXXWPRgNtFBlKTsb7DCjmKqo__eYncKUzR8BD0TcE-7fYdeSHFyOUERV64SOvbCCeOyeYh76AJcBcDE7IVuo2SPcGSPreSUKT-tTSHRRYmnI5Pe07cMeXg3ewrYaL3fawr-ANFe0WC6Sbi7DA..",
            "rank": 10,
            "suggestion": "暂不跟进（考研类，与工业AI关联度低）"
        }
    ]
    
    # 获取token
    print("\n📡 获取飞书 Token...")
    token = get_token()
    print("✅ Token 获取成功")
    
    # 构造记录
    records = []
    for h in hotspots:
        records.append(create_record(token, h['title'], h['source'], h['url'], h['rank'], h['suggestion']))
    
    # 批量写入
    print(f"\n💾 写入 {len(records)} 条热点到 Bitable...")
    result = batch_create_records(token, records)
    
    if result.get('code') == 0:
        print(f"✅ 成功写入 {len(records)} 条热点")
        print(f"📊 表格地址: https://ai-zhineng.feishu.cn/base/{APP_TOKEN}")
    else:
        print(f"❌ 写入失败: {result.get('msg')}")
        sys.exit(1)
