#!/bin/bash
# 虾秘早报触发脚本 - 触发AI生成动态早报

# 调用OpenClaw Gateway API触发主会话生成早报
# 这会唤醒我(虾米)来动态生成内容

curl -s -X POST "http://127.0.0.1:18789/api/v1/sessions/main/system-event" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "生成今日早报并发送给吕总",
    "timestamp": '"$(date +%s000)"',
    "requireResponse": false
  }' 2>/dev/null || echo "触发失败，Gateway可能未运行"

echo "$(date): 早报触发请求已发送" >> /tmp/daily-report-trigger.log
