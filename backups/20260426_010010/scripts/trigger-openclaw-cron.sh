#!/bin/bash
# OpenClaw Cron触发脚本 - 通过系统cron调用OpenClaw内置cron

JOB_ID="2e5158e4-fe65-4f20-b8ac-638b4c26065c"
LOG_FILE="/tmp/openclaw-cron-trigger.log"

echo "$(date): 触发OpenClaw cron job $JOB_ID" >> $LOG_FILE

# 调用OpenClaw cron run
/usr/local/bin/openclaw cron run $JOB_ID >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): 触发成功" >> $LOG_FILE
else
    echo "$(date): 触发失败" >> $LOG_FILE
fi
