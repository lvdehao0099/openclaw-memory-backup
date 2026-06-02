#!/usr/bin/env python3
"""
热点数据批量写入飞书 Bitable - 2026-03-14 晚班
"""
import json
import urllib.request
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
            "来源": "微信搜一搜",
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
    print("微信热点写入 - 2026-03-14 晚班")
    print("=" * 60)
    
    # 今天搜索到的数据（已去重）
    hotspots = [
        # 热点关键词
        {
            "title": "热点消失后,我们还记得什么?",
            "source": "白同学的碎碎念",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcVoMS6r9lRbyuyKbkxARmc1qXa8Fplpd9Tmy0HKOy1m1gXjs-T19Iv0rHQQRliBwMeeM6HHtaTju6yiig75WLiNdsvvSYzuk0XvgeFGTzbBNHDdW5NJUuwo3lSEL0IPvumjYTL8e5vRSsI4PwIyK7Xg5wB7TMEEsouSywoPDQ_UgTCVXSLNjB5JJ44xnrcnfqbaQS5E4Q_ou54z_tGSZTqA..&type=2&query=%E7%83%AD%E7%82%B9&token=8F5E4A4337075DF4E0E6AC1A5BE1769FE0AFCF7269B54DDC",
            "rank": 1,
            "suggestion": "暂不跟进（热点反思类，与工业AI关联度低）"
        },
        {
            "title": "热点预测·272期丨滥用AI退款(260314)",
            "source": "刘鑫学长",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcVoMS6r9lRbyuyKbkxARmc1qXa8Fplpd91p_uSdMs5pv2_OFn4_LAbj1Md3-DP6C0OcsAgDPsXnB38skS0W9z2U4-Rtl8HhNxspBpCeQLPIobBbOkwXqbrg-iqMJpcMGFakdyhNQNoAekzJt67tvXgoOowM2ZC_s4bNJ9ctGPbvMnKHDXDFdlpL6PXgGJDf0ke-QmXW89tZzRtmyIGw2VAg..&type=2&query=%E7%83%AD%E7%82%B9&token=8F5E4A4337075DF4E0E6AC1A5BE1769FE0AFCF7269B54DDC",
            "rank": 2,
            "suggestion": "《AI滥用现象：工业场景如何避免AI误用？》热点+行业警示"
        },
        # 两会关键词
        {
            "title": "两会结束,国务院立刻行动",
            "source": "中桥政研信息咨询",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcFBwpq8RjNs2uyKbkxARmc1qXa8Fplpd9p7fcPcRCjEj15YpammGzc-p2cu-KN6Aev9tpKNj6GMwI5S0_0XkeA2WWGstOp5nkOeyyVCHb4YkMCZ6YwPBk76xAHw7zJpqtM19-m94fXSH9OPlTHE_KHD91_5oxuAphf1GhiEoJFEVnqP7d46V9nnDsygKIAfutPfGxcCf4RZD6zvkPgoArRQ..&type=2&query=%E4%B8%A4%E4%BC%9A&token=8F5E518A8AB9DF765D5B11A7E53FFB8E5ED140E369B54DDD",
            "rank": 3,
            "suggestion": "《两会后政策落地：制造业智能化转型的政策红利》政策角度+机会分析"
        },
        {
            "title": "两会收官,逐梦笃行——我校学子热议全国两会奋进新征程",
            "source": "青春黄职",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcFBwpq8RjNs2uyKbkxARmc1qXa8Fplpd9LVvPEl7em_QntaYRpBV7JehGyGOjnPHm3UqOPvdoXwrIBsQaNTOP03x1z2f51ox4Vhag7IGabin_sGA3bcNplgDDNRT10LJyN8259EjeT5_HDXitn6yVkCo3SuWhBrcjddW_vifeUNf6dOVwhfaL49iUwIyUuynr4rMHFMQNN0BQ_LeJW-Rhtg..&type=2&query=%E4%B8%A4%E4%BC%9A&token=8F5E518A8AB9DF765D5B11A7E53FFB8E5ED140E369B54DDD",
            "rank": 4,
            "suggestion": "暂不跟进（学校新闻类，与工业AI关联度低）"
        },
        # AI 人工智能关键词
        {
            "title": "马斯克,AI新项目曝光!",
            "source": "青岛日报",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcdqbvODrXLJKuyKbkxARmc1qXa8Fplpd9gImPsxMCFXTEOs3DnKT0ho3V3xwMbGRTto8l3Wx9hDkZ-ntJTzutE7NWQbdKJPy688OT4Kr7nA_p77TaT7-pitJbQ3upMxKHhksVskETKQQcX34U2u0WX70PtKtY8yydq0oaBANpsGAUQFtou50m5LFP9WITP01KmC3tkhsyINzyPfCoem7FzA..&type=2&query=AI %E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&token=8F5E5FBF261673DBF0F7BC0A4A854121F1DAE49E69B54DE0",
            "rank": 5,
            "suggestion": "《马斯克AI新动向：工业AI能否借鉴特斯拉智能体思路？》热点+技术趋势"
        },
        {
            "title": "金华金漪湖2026人工智能产业融合发展大会开幕",
            "source": "金华发布",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcdqbvODrXLJKuyKbkxARmc1qXa8Fplpd9N1x0M9gX-X9ujnTInV9Ef9nbbuN_z43ufg7Xx4BeOscOQ7YoAoT7YSfwbR38DCcLrfjMnPizVXcDFX_rbu1xwSucoamU7oqKjFvlklWnmXHoTH9VrADbNScXl1YB58cor6vKf-irnNavB4FWDcMPYP9V6uU5kmJ17hSczvZtdi5Cy6umSSPEsg..&type=2&query=AI %E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&token=8F5E5FBF261673DBF0F7BC0A4A854121F1DAE49E69B54DE0",
            "rank": 6,
            "suggestion": "《地方AI产业大会：金华模式对工业AI落地的启示》区域发展+案例"
        },
        {
            "title": "能否为人工智能设计出更好的智商测试?",
            "source": "人工智能学家",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVcdqbvODrXLJKuyKbkxARmc1qXa8Fplpd90o96PzJ8Wl48NyJxySpCwPlOM_GRONUGy9XZaLqmk0kDZWxIgVYpIpOEy0Vq6yVmtPLhOYgA9E6rEAzo3xH5SSvSYaLlMe9g0ULzCoCZDls9Nque-5VsrENFo8z9Zilm_-CTCSDFGrgH6YVGqJtO8set2nsIegvDukb4TEWCQSPFcvUoAZZH7Q..&type=2&query=AI %E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&token=8F5E5FBF261673DBF0F7BC0A4A854121F1DAE49E69B54DE0",
            "rank": 7,
            "suggestion": "《AI智商测试：工业AI如何评估实际效能？》技术深度+评估方法"
        },
        # 智能制造关键词
        {
            "title": "两会之声 | 孙景南谈职业教育与智能制造人才培养",
            "source": "中国中车",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVc5xp6rmhfkjmuyKbkxARmc1qXa8Fplpd9agNUNFb5eYazzJcOQC7qiaICZYaXTQ-ChXggHTjuXU2E-dR0sLc5u-dNWhA7K-dwfjytn4oKIvqinC8VXmR0xt3G5RY6wDa1bkJ2srraZbZsMv9GRN3PTclWVKytstys0ZC4wfixj5LjkjaHU9Arq3dwaG-6cqB1B2bS7-RKYCfS-e4Yz84xMA..&type=2&query=%E6%99%BA%E8%83%BD%E5%88%B6%E9%80%A0&token=8F5E69B46757339BB1B7FD4A0A292691B1B22EAB69B54DE1",
            "rank": 8,
            "suggestion": "《智能制造人才培养：AI老师傅如何填补技能缺口？》两会+人才痛点"
        },
        {
            "title": "十五五职业技能培训规划 智能制造暨工业机器人培训再就业计划",
            "source": "燕赵招聘网",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVc5xp6rmhfkjmuyKbkxARmc1qXa8Fplpd91CNnU-LLnkCZcqLSdMmZpbybxw9rnWjrgXhbVwXjgpuq9plwjY-x9FAcy_sqHrYubjfE4feUKFDoUT5-oOhcyBASHfFpJnuySmztsipIQjZh9mAGSWcioDYr5k_o_IvjJC1_qSs1bIfoE6L24gdhGJEgLWeuKSwIskcgB5_5Pttf_71bqkOtiw..&type=2&query=%E6%99%BA%E8%83%BD%E5%88%B6%E9%80%A0&token=8F5E69B46757339BB1B7FD4A0A292691B1B22EAB69B54DE1",
            "rank": 9,
            "suggestion": "《工业机器人培训热：技能转型背后的市场需求》培训市场+职业转型"
        },
        {
            "title": "智能制造学院召开2025年度教职工述职大会",
            "source": "长科智能",
            "url": "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS3Rtt5wcBNVc5xp6rmhfkjmuyKbkxARmc1qXa8Fplpd9mjr-XRBI_QIpmDTLReWahtoXHQEKaPxNf2nIR9AZDTkyW_xjTCq79Oznmk8rVpoarnuQOpXuG6FK_oBwNPle2OXJLN48zJj8Ni9bP2CFbC5L3KjIDVY4kGH-5tCcBWdgIPVrkweWy9YBNbhOsYm9VsgQmTolnxqQ2I5rVxIB3w2E8RsmObDbtQ..&type=2&query=%E6%99%BA%E8%83%BD%E5%88%B6%E9%80%A0&token=8F5E69B46757339BB1B7FD4A0A292691B1B22EAB69B54DE1",
            "rank": 10,
            "suggestion": "暂不跟进（学院新闻类，与工业AI关联度低）"
        }
    ]
    
    # 获取token
    print("\n📡 获取飞书 Token...")
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
        print(f"详细结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
