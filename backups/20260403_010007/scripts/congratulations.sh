#!/bin/bash
# 一次性祝福任务

openclaw message send \
  --channel feishu \
  --target "user:ou_12dd9e55259701aeb2701dccf7f1ee54" \
  --message "🧧 吕总，恭喜发财！大吉大利，生意兴隆！💰"

# 执行后从crontab中删除自己
(crontab -l 2>/dev/null | grep -v "congratulations.sh") | crontab -
