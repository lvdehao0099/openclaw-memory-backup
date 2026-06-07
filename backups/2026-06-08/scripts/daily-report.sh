#!/bin/bash
# 虾秘早报生成脚本

# 获取日期
DATE_STR=$(date '+%Y年%m月%d日 %A')

# 构建早报内容
REPORT="🦐 虾秘早报 | ${DATE_STR}

📅 今日核心待办：
1. 苏浙市场调研：跟进江浙沪工业维保客户线索
2. 创新案例申报：整理AI老师傅产品功能亮点  
3. 团队同步：上午10点项目站会
4. 瓦轴合同跟进：提醒销售团队

🚀 战役进度：
• Q2苏浙市场：待更新（飞书表格查看最新）
• 软件协会案例申报：3月18日截止

💪 玩命干，往死干，24小时不打烊！
（详细数据请查阅飞书表格）"

# 使用OpenClaw CLI发送到飞书
openclaw message send \
  --channel feishu \
  --target "user:ou_12dd9e55259701aeb2701dccf7f1ee54" \
  --message "$REPORT" 2>/dev/null || echo "CLI发送失败"

echo "早报已生成: $DATE_STR"
