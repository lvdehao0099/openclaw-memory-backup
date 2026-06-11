#!/bin/bash
# 批量生成小红书图片脚本

export VOLCENGINE_AK="AKLTYzQ2YTA0NWMxZjQ5NGZjM2FkODNhNWQ2NGI5ZDcwMmY"
export VOLCENGINE_SK="T0RNMlpETmtZemhrWlRJek5HWTBZbUkwT0RJNU1qWmxObVprT1RjMVpEUQ=="
cd ~/.openclaw/workspace/skills/jimeng-ai

echo "========== 第一套：维修工揭秘视角 =========="

# P1封面
echo "生成 P1 封面..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。老板拿着3万元账单苦笑，维修工离开背影，画面中央大字'10分钟'和'6天'对比" --version v31 --ratio 3:4 --count 1

# P2维修工视角
echo "生成 P2 维修工视角..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。维修工背对镜头站在机床旁，嘴角带笑，手里拿着扳手，左侧小窗口显示松动的连接管" --version v31 --ratio 3:4 --count 1

# P3老板被动
echo "生成 P3 老板被动..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。老板站在维修工旁边，表情困惑又无奈，维修工蹲在地上'忙碌'检查" --version v31 --ratio 3:4 --count 1

# P4结账时刻
echo "生成 P4 结账时刻..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。特写老板的手在账单上签字，账单金额'30000元'用红色突出，手微微发抖" --version v31 --ratio 3:4 --count 1

# P5后续
echo "生成 P5 后续..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。酒桌场景，老板和维修工碰杯，老板笑容勉强，维修工笑容满面" --version v31 --ratio 3:4 --count 1

# P6觉醒
echo "生成 P6 觉醒..."
npx ts-node scripts/text2image.ts "现代职场漫画风格，干净线稿，冷色调工业蓝灰，3:4竖图。年轻员工拿着平板电脑，屏幕上显示维修指引，表情自信专注" --version v31 --ratio 3:4 --count 1

echo "========== 第二套：老板反思视角 =========="

# P1封面
echo "生成 P1 封面..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。老板办公室桌面俯视视角，散落着财务报表、计算器、一杯咖啡、眼镜，画面中央大字'开工厂15年'和'去年才明白'" --version v31 --ratio 3:4 --count 1

# P2资产清单
echo "生成 P2 资产清单..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。手指指着财务报表局部特写，厂房800万✓ 设备600万✓ 原材料200万✓" --version v31 --ratio 3:4 --count 1

# P3发现问题
echo "生成 P3 发现问题..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。中年老板坐在办公桌前，看着窗外，侧脸表情复杂（若有所思+轻微苦笑）" --version v31 --ratio 3:4 --count 1

# P4知识资产
echo "生成 P4 知识资产..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。左右拼图形式，左边老师傅离职交接单，右边年轻工程师困惑表情" --version v31 --ratio 3:4 --count 1

# P5算账时刻
echo "生成 P5 算账时刻..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。计算器特写，屏幕显示数字累计动画效果，旁边是堆叠的维修账单" --version v31 --ratio 3:4 --count 1

# P6对比解决
echo "生成 P6 对比解决..."
npx ts-node scripts/text2image.ts "伪随手拍风格，手机实拍角度，办公室暖光环境，3:4竖图。左右对比画面，左边老师傅带徒弟，右边年轻员工拿着平板电脑显示维修指引" --version v31 --ratio 3:4 --count 1

echo "========== 全部生成完成！=========="
