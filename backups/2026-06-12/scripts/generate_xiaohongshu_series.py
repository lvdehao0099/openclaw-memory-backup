#!/usr/bin/env python3
"""
生成小红书风格的小图系列
"""

import requests
import json
from scripts.feishu_table_manager import FeishuTableManager

APP_ID = "cli_a92780ca08b89bb6"
APP_SECRET = "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"
FOLDER_TOKEN = "Thhrfa3QglB5amdIMpEcY2tAndd"

manager = FeishuTableManager(APP_ID, APP_SECRET)

# 创建文档
res = requests.post('https://open.feishu.cn/open-apis/docx/v1/documents',
                    headers=manager.headers,
                    json={'title': '小红书-两会AI政策系列(6张图)', 'folder_token': FOLDER_TOKEN})
doc_id = res.json()['data']['document']['document_id']
print(f"✅ 创建文档: https://feishu.cn/docx/{doc_id}\n")

# ====== 图1：封面 ======
print("【图1：封面】")
blocks1 = [
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "2026两会AI政策"}}]}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "一图读懂AI红利在哪"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "一句话结论"}}]}},
    {"block_type": 15, "callout": {"elements": [{"text_run": {"content": "从技术研发转向落地应用"}}]}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "不再只拼大模型，而是拼谁能先把AI用在实体经济上"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "3分钟get政策红利"}}]}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks1})

# ====== 图2：三大信号 ======
print("【图2：三大信号】")
blocks2 = [
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "三大政策信号"}}]}},
    {"block_type": 22, "divider": {}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks2})

data2 = [
    ["政策词", "什么意思"],
    ["人工智能+", "AI要和制造业、医疗、教育等行业深度结合，不能只待在实验室"],
    ["场景驱动", "谁有真实应用场景，谁能拿到政策支持"],
    ["普惠AI", "降低中小企业用AI的门槛"]
]
manager.batch_update_content(doc_id, data2, header_bold=True)

# ====== 图3：对普通人的影响 ======
print("【图3：对普通人的影响】")
blocks3 = [
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "对普通人的影响"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "不是取代，是放大"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "AI成为你的超级助手"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "替代重复劳动"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "把你从繁琐工作中解放出来"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "典型应用场景"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "设计师：AI出初稿，你负责审美"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "销售：AI分析客户，你负责谈单"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "生产：AI监控设备，你负责处理"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "教育：AI批改作业，你负责育人"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 15, "callout": {"elements": [{"text_run": {"content": "会AI的人，价值会越来越高"}}]}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks3})

# ====== 图4：机会1 ======
print("【图4：机会1-行业AI】")
blocks4 = [
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "机会1：行业AI解决方案"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "门槛 中  收益 高"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "适合：有特定行业经验的人"}}]}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "（制造业/医疗/教育/销售等）"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "怎么做"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "找到行业的痛点"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "用现成的大模型"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "做成解决方案"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "案例：工业维保AI"}}]}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks4})

# ====== 图5：机会2+3 ======
print("【图5：机会2+3】")
blocks5 = [
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "机会2+3"}}]}},
    {"block_type": 22, "divider": {}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks5})

data5 = [
    ["机会", "门槛", "收益", "怎么做"],
    ["AI应用创业", "高", "高", "做一个垂直场景的AI工具"],
    ["AI技能培训", "低", "中", "教别人用AI提高效率"]
]
manager.batch_update_content(doc_id, data5, header_bold=True)

# ====== 图6：总结 ======
print("【图6：总结】")
blocks6 = [
    {"block_type": 22, "divider": {}},
    {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "总结"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 15, "callout": {"elements": [{"text_run": {"content": "AI是未来10年最确定的方向"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "不会用AI = 被淘汰"}}]}},
    {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": "会用AI放大自己 = 获得红利"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 15, "callout": {"elements": [{"text_run": {"content": "想到的都是问题，去做才能有答案"}}]}},
    {"block_type": 22, "divider": {}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "关注我，持续分享AI干货"}}]}},
]
requests.post(f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children', 
              headers=manager.headers, json={"children": blocks6})

print(f"\n🎉 小红书系列完成！共6张图")
print(f"📄 文档链接: https://feishu.cn/docx/{doc_id}")
