#!/usr/bin/env python3
"""
补充写入缺失的blocks
"""

import sys
import json
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from feishu_docx_blocks import (
    FeishuDocClient, create_heading2, create_heading3, create_text, create_bullet
)

# 补充缺失的内容（第50-75个blocks对应的部分）
supplement_blocks = [
    # 国家级政策详细内容
    create_heading2("二、国家级政策（重点）"),
    create_heading3("\"人工智能+制造\"专项行动实施意见"),
    create_text("发布单位: 工信部等八部门（工信部、中央网信办、发改委、教育部、商务部、国资委、市场监管总局、国家数据局）"),
    create_text("发布时间: 2026年1月7日"),
    create_text("文件编号: 工信部联科〔2025〕279号"),
    create_text("核心内容: 推动人工智能与制造业深度融合"),
    create_text("原文链接: https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2026/art_01010414608a4226b30687773bb21bdf.html"),
    create_text("解读链接: https://www.miit.gov.cn/zwgk/zcjd/art/2026/art_9b87c46fe9bb4f59851b59c4200515f5.html"),
    create_text("AI老师傅关联度: ★★★★★"),
    create_text("这是与AI老师傅业务最相关的国家级政策！建议："),
    create_bullet("深度研读政策全文，寻找产品定位契合点"),
    create_bullet("关注后续各省份的落地实施细则"),
    create_bullet("准备申请相关政策试点或示范项目"),
]

# 写入到现有文档
doc_id = "CczFdR2BhoWX1fxy5Nacryf4nvc"

try:
    with open('/root/.openclaw/openclaw.json', 'r') as f:
        config = json.load(f)
    
    feishu = config.get('channels', {}).get('feishu', {})
    app_id = feishu.get('appId')
    app_secret = feishu.get('appSecret')
    
    client = FeishuDocClient(app_id, app_secret)
    
    # 写入补充内容
    success = client.write_blocks(doc_id, supplement_blocks, batch_size=20)
    
    if success:
        print("✅ 补充内容写入成功")
    else:
        print("⚠️ 补充内容部分写入失败")
        
except Exception as e:
    print(f"❌ 补充写入失败: {e}")
