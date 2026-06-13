#!/usr/bin/env python3
"""批量生成小红书图片 - 带速率控制"""

import subprocess
import time
import os

# 设置环境变量
os.environ['VOLCENGINE_AK'] = 'AKLTYzQ2YTA0NWMxZjQ5NGZjM2FkODNhNWQ2NGI5ZDcwMmY'
os.environ['VOLCENGINE_SK'] = 'T0RNMlpETmtZemhrWlRJek5HWTBZbUkwT0RJNU1qWmxObVprT1RjMVpEUQ=='

# 图片配置
images = [
    # 第一套：维修工揭秘视角
    ("第一套-P1-封面", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。老板拿着3万元账单苦笑，维修工离开背影，画面中央大字'10分钟'和'6天'对比"),
    ("第一套-P2-维修工视角", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。维修工背对镜头站在机床旁，嘴角带笑，手里拿着扳手，左侧小窗口显示松动的连接管"),
    ("第一套-P3-老板被动", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。老板站在维修工旁边，表情困惑又无奈，维修工蹲在地上'忙碌'检查"),
    ("第一套-P4-结账时刻", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。特写老板的手在账单上签字，账单金额'30000元'用红色突出，手微微发抖"),
    ("第一套-P5-后续", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。酒桌场景，老板和维修工碰杯，老板笑容勉强，维修工笑容满面"),
    ("第一套-P6-觉醒", "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。年轻员工拿着平板电脑，屏幕上显示维修指引，表情自信专注"),
    
    # 第二套：老板反思视角
    ("第二套-P1-封面", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。老板办公室桌面俯视视角，散落着财务报表、计算器、一杯咖啡、眼镜，画面中央大字'开工厂15年'和'去年才明白'"),
    ("第二套-P2-资产清单", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。手指指着财务报表局部特写，厂房800万✓ 设备600万✓ 原材料200万✓"),
    ("第二套-P3-发现问题", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。中年老板坐在办公桌前，看着窗外，侧脸表情复杂（若有所思+轻微苦笑）"),
    ("第二套-P4-知识资产", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。左右拼图形式，左边老师傅离职交接单，右边年轻工程师困惑表情"),
    ("第二套-P5-算账时刻", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。计算器特写，屏幕显示数字累计动画效果，旁边是堆叠的维修账单"),
    ("第二套-P6-对比解决", "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。左右对比画面，左边老师傅带徒弟，右边年轻员工拿着平板电脑显示维修指引"),
]

print("="*60)
print("开始批量生成12张小红书图片")
print("预计总时间：约60-90分钟（每张5-8分钟，含等待）")
print("="*60)

results = []

for i, (name, prompt) in enumerate(images, 1):
    print(f"\n[{i}/12] 正在生成: {name}")
    print(f"提示词: {prompt[:50]}...")
    
    # 生成图片
    cmd = [
        'npx', 'ts-node', 'scripts/text2image.ts',
        prompt,
        '--version', 'v31',
        '--ratio', '3:4',
        '--count', '1'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if 'success' in result.stdout.lower() or '任务已提交' in result.stdout:
            print(f"✅ {name} - 提交成功")
            results.append((name, "成功"))
        else:
            print(f"⚠️ {name} - 需要重试")
            results.append((name, "需重试"))
    except Exception as e:
        print(f"❌ {name} - 错误: {e}")
        results.append((name, "失败"))
    
    # 等待间隔（避免429错误）
    if i < len(images):
        wait_time = 180  # 3分钟间隔
        print(f"⏳ 等待 {wait_time} 秒后生成下一张...")
        time.sleep(wait_time)

print("\n" + "="*60)
print("生成任务完成！")
print("="*60)
for name, status in results:
    print(f"{name}: {status}")
