#!/bin/bash
# 虾秘早报系统 - 最终可靠方案

DATE_STR=$(date '+%Y年%m月%d日 %A')
LOG_FILE="/tmp/morning-wake-up.log"

echo "$(date): 开始执行早报唤醒" >> $LOG_FILE

# 使用OpenClaw CLI发送消息
openclaw message send \
  --channel feishu \
  --target "user:ou_12dd9e55259701aeb2701dccf7f1ee54" \
  --message "🦐 虾秘早报唤醒 | ${DATE_STR}

早安吕总！

我已在8:00准时上线，准备为您生成今日早报。

请回复\"早报\"或任意消息，我将立即为您生成包含真实数据的完整早报：
• 今日待办（从飞书读取）
• Q2苏浙市场进度
• 软件协会案例申报进度  
• 团队工作安排
• 大连+海南天气

🦐 等待您的指令..."

echo "$(date): 消息发送完成，返回码: $?" >> $LOG_FILE
