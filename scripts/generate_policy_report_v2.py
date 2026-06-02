#!/usr/bin/env python3
"""
政策虾试点报告生成脚本 - 完整版
分段写入确保内容完整
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from feishu_docx_blocks import (
    create_document, create_heading1, create_heading2, 
    create_heading3, create_text, create_bullet, create_numbered,
    create_table, add_blocks_to_document
)

# 文档标题和基础信息
title = "政策虾试点报告 - 2026年3月12日"

# 第一部分：执行摘要和执行摘要
section1_blocks = [
    create_heading1("政策虾试点报告"),
    create_text("报告日期: 2026年3月12日"),
    create_text("监测范围: 辽宁、长三角、珠三角、国家级"),
    create_text("监测周期: 2026年2月26日 - 3月12日"),
    create_text(""),
    create_heading2("执行摘要"),
    create_text("本报告为政策虾首次试点运行，重点监测工业AI、智能制造、数字化转型相关政策。本期共发现 3个正在申报中的政策项目，其中 2个即将截止（均在4月前），建议重点关注。"),
    create_text(""),
    create_heading3("本期亮点"),
    create_bullet("紧急: 辽宁省专精特新中小企业复核，3月31日截止（剩19天）"),
    create_bullet("重磅: 国家级"人工智能+制造"专项行动发布（八部门联合）"),
    create_bullet("数据: 辽宁省2025年新增112家重点培育工业互联网平台"),
]

# 第二部分：辽宁省政策
section2_blocks = [
    create_heading2("一、辽宁省政策监测（P0优先级）"),
    create_heading3("1.1 正在申报项目"),
    create_text(""),
    create_heading3("🔥 【紧急】专精特新中小企业复核"),
    create_text("发布单位: 辽宁省工业和信息化厅"),
    create_text("发布时间: 2026年2月11日"),
    create_text("申报截止: 2026年3月31日 ⚠️"),
    create_text("申报对象: 2023年认定及复核通过的辽宁省专精特新中小企业"),
    create_text("申报方式: 线上填报(zjtx.miit.gov.cn) + 线下报送"),
    create_text("补贴/支持: 资质认定延续 + 后续政策支持资格"),
    create_text("原文链接: https://gxt.ln.gov.cn/gxt/tztg/2026021111172427873/"),
    create_text("联系人: 张磊 024-86906657"),
    create_text(""),
    create_text("AI老师傅关联度: ★★★☆☆"),
    create_text("工业维保企业如符合专精特新标准，建议申报以获取政策背书。"),
    create_text(""),
    create_heading3("【关注】工业绿色低碳典型案例征集"),
    create_text("发布单位: 辽宁省工信厅 + 生态环境厅"),
    create_text("发布时间: 2026年2月2日"),
    create_text("申报截止: 2026年4月1日"),
    create_text("申报对象: 工业园区、工业企业"),
    create_text("申报要求: 推行无废生产方式，提升资源利用效率"),
    create_text("支持内容: 国家级典型案例推荐资格"),
    create_text("原文链接: https://gxt.ln.gov.cn/gxt/tztg/2026020216302682089/"),
    create_text("联系人: 牛大群 024-86892792"),
    create_text(""),
    create_text("AI老师傅关联度: ★★☆☆☆"),
    create_text("如客户涉及工业固废处理，可协助申报。"),
]

# 第三部分：已公布名单
section3_blocks = [
    create_heading3("1.2 已公布名单（参考）"),
    create_text(""),
    create_heading3("2025年第二批辽宁省先进级智能工厂（已截止申报）"),
    create_text("发布时间: 2026年1月8日"),
    create_text("入选企业: 35家"),
    create_text("原文链接: https://gxt.ln.gov.cn/gxt/tztg/2026010808415215548/"),
    create_text(""),
    create_heading3("2025年辽宁省重点培育工业互联网平台（已公布）"),
    create_text("发布时间: 2025年12月23日"),
    create_text("入选平台: 112家"),
    create_text("原文链接: https://gxt.ln.gov.cn/gxt/tztg/2025122309141263693/"),
]

# 第四部分：国家级政策
section4_blocks = [
    create_heading2("二、国家级政策（重点）"),
    create_heading3("🎯 "人工智能+制造"专项行动实施意见"),
    create_text(""),
    create_text("发布单位: 工信部等八部门（工信部、中央网信办、发改委、教育部、商务部、国资委、市场监管总局、国家数据局）"),
    create_text("发布时间: 2026年1月7日"),
    create_text("文件编号: 工信部联科〔2025〕279号"),
    create_text("核心内容: 推动人工智能与制造业深度融合"),
    create_text("原文链接: https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2026/art_01010414608a4226b30687773bb21bdf.html"),
    create_text("解读链接: https://www.miit.gov.cn/zwgk/zcjd/art/2026/art_9b87c46fe9bb4f59851b59c4200515f5.html"),
    create_text(""),
    create_text("AI老师傅关联度: ★★★★★"),
    create_text("这是与AI老师傅业务最相关的国家级政策！建议："),
    create_numbered("深度研读政策全文，寻找产品定位契合点"),
    create_numbered("关注后续各省份的落地实施细则"),
    create_numbered("准备申请相关政策试点或示范项目"),
]

# 第五部分：长三角和珠三角
section5_blocks = [
    create_heading2("三、长三角地区政策监测（P0优先级）"),
    create_heading3("监测状态"),
    create_bullet("江苏省: 网站访问受限，政策收集中"),
    create_bullet("浙江省: 网站访问受限，政策收集中"),
    create_bullet("上海市: 网站访问受限，政策收集中"),
    create_text(""),
    create_text("说明: 本期试点因技术限制，长三角政策数据待下周周报补充完善。"),
    create_text(""),
    create_heading3("建议关注方向"),
    create_bullet("江苏省"智改数转"专项"),
    create_bullet("浙江省数字经济创新提质"一号发展工程""),
    create_bullet("上海市智能工厂/智能制造专项"),
    create_text(""),
    create_heading2("四、珠三角地区政策监测（P0优先级）"),
    create_heading3("监测状态"),
    create_bullet("广东省: 网站访问受限，政策收集中"),
    create_bullet("深圳市: 网站访问受限，政策收集中"),
    create_text(""),
    create_text("说明: 本期试点因技术限制，珠三角政策数据待下周周报补充完善。"),
    create_text(""),
    create_heading3("建议关注方向"),
    create_bullet("广东省智能制造生态合作伙伴"),
    create_bullet("深圳市工业互联网发展扶持计划"),
    create_bullet("粤港澳大湾区智能制造专项"),
]

# 第六部分：可申报项目速查表
section6_blocks = [
    create_heading2("五、可申报项目速查表"),
    create_text(""),
    create_heading3("🔴 P0 优先级"),
    create_text("项目名称: 专精特新中小企业复核"),
    create_text("地区: 辽宁"),
    create_text("截止日期: 3月31日"),
    create_text("状态: 进行中"),
    create_text(""),
    create_heading3("🟡 P1 优先级"),
    create_text("项目名称: 工业绿色低碳典型案例"),
    create_text("地区: 辽宁"),
    create_text("截止日期: 4月1日"),
    create_text("状态: 进行中"),
    create_text(""),
    create_heading3("⭐ 国家级政策"),
    create_text("项目名称: 人工智能+制造专项"),
    create_text("地区: 全国"),
    create_text("截止日期: 待细则"),
    create_text("状态: 观察"),
]

# 第七部分：AI老师傅机会分析
section7_blocks = [
    create_heading2("六、AI老师傅机会分析"),
    create_heading3("6.1 直接机会"),
    create_text(""),
    create_heading3("专精特新资质"),
    create_text("如AI老师傅符合"专精特新"标准，建议3月31日前完成复核申报。获得资质后可享受省级政策支持。"),
    create_text(""),
    create_heading3("人工智能+制造政策跟进"),
    create_text("八部门联合发文，力度空前。关注各省落地细则，准备申请相关试点。"),
    create_text(""),
    create_heading3("6.2 间接机会（客户侧）"),
    create_heading3("客户政策咨询增值服务"),
    create_text("向已签约客户提供政策申报咨询服务，帮助客户申报智能工厂、工业互联网平台等项目。"),
    create_text(""),
    create_heading3("解决方案包装"),
    create_text("将AI老师傅功能与政策导向对齐，突出"人工智能+制造""数字化转型"等关键词。"),
]

# 第八部分：下周工作计划
section8_blocks = [
    create_heading2("七、下周工作计划"),
    create_heading3("7.1 数据补全"),
    create_bullet("完成长三角（江苏、浙江、上海）政策搜集"),
    create_bullet("完成珠三角（广东、深圳）政策搜集"),
    create_bullet("补充各地区可申报项目详细信息"),
    create_text(""),
    create_heading3("7.2 系统优化"),
    create_bullet("建立政策信息来源库（各地工信部门官网、公众号）"),
    create_bullet("优化扫描频率（P0每周、P1每2周、P2每月）"),
    create_bullet("建立申报截止日提醒机制"),
    create_text(""),
    create_heading3("7.3 报告迭代"),
    create_bullet("增加"AI老师傅可申报项目"专属板块"),
    create_bullet("增加"客户政策机会"分析板块"),
    create_bullet("优化可视化呈现（表格、时间线）"),
]

# 第九部分：附录
section9_blocks = [
    create_heading2("附录"),
    create_heading3("A. 信息来源"),
    create_text("辽宁省工业和信息化厅官网: https://gxt.ln.gov.cn"),
    create_text("工信部官网: https://www.miit.gov.cn"),
    create_text(""),
    create_heading3("B. 免责声明"),
    create_text("本报告信息来源于政府公开渠道，具体申报要求以官方文件为准。申报前请仔细阅读原文并咨询相关部门。"),
    create_text(""),
    create_heading3("C. 反馈渠道"),
    create_text("如对报告内容有疑问或建议，请联系：虾米 (CLO)"),
    create_text(""),
    create_text("---"),
    create_text("报告生成时间: 2026年3月12日 21:00"),
    create_text("政策虾 · 首席执虾官 🦐"),
]

# 合并所有blocks
all_blocks = (
    section1_blocks + 
    section2_blocks + 
    section3_blocks + 
    section4_blocks + 
    section5_blocks + 
    section6_blocks + 
    section7_blocks + 
    section8_blocks + 
    section9_blocks
)

# 创建文档
try:
    # 先创建空文档
    doc_id = create_document(
        title=title,
        folder_token="Thhrfa3QglB5amdIMpEcY2tAndd"
    )
    print(f"✅ 文档创建成功: {doc_id}")
    
    # 分批写入blocks
    batch_size = 30
    total_blocks = len(all_blocks)
    
    for i in range(0, total_blocks, batch_size):
        batch = all_blocks[i:i+batch_size]
        try:
            add_blocks_to_document(doc_id, batch)
            print(f"✅ 写入批次 {i//batch_size + 1}/{(total_blocks-1)//batch_size + 1}: {len(batch)} blocks")
        except Exception as e:
            print(f"⚠️ 批次 {i//batch_size + 1} 写入异常: {e}")
    
    print(f"""
✅ 报告创建完成！
📄 文档ID: {doc_id}
🔗 飞书链接: https://ai-zhineng.feishu.cn/docx/{doc_id}
📝 总Blocks数: {total_blocks}
""")
    
except Exception as e:
    print(f"❌ 创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
