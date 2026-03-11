# 定时任务处理流程

## 触发条件
当吕总发布以下类型的任务时：
- "每天X点..."
- "每周X..."
- "定时..."
- "提醒..."
- "以后每天/每周..."
- 任何包含明确时间点的重复性任务

## 处理流程

### 1. 识别任务类型
- **一次性提醒**：使用 `openclaw cron add --at`
- **周期性任务**：使用系统crontab（更可靠）

### 2. 添加到Crontab
```bash
# 查看当前crontab
crontab -l

# 添加新任务（追加方式，保留已有任务）
(crontab -l 2>/dev/null; echo "定时规则 命令") | crontab -
```

### 3. 脚本存放位置
- 所有定时任务脚本统一存放在：`~/.openclaw/workspace/scripts/`
- 命名规范：`任务名.sh`（如 `daily-report.sh`, `wa-zhou-reminder.sh`）

### 4. 脚本模板
```bash
#!/bin/bash
# 描述：XXX提醒/任务

# 使用OpenClaw CLI发送飞书消息
openclaw message send \
  --channel feishu \
  --target "user:ou_12dd9e55259701aeb2701dccf7f1ee54" \
  --message "提醒内容"

# 记录日志
echo "$(date): 任务执行成功" >> /tmp/任务名.log
```

### 5. 验证
```bash
crontab -l  # 确认任务已添加
```

## 当前定时任务清单

| 时间 | 任务 | 脚本路径 | 状态 |
|------|------|---------|------|
| 每日8:00 | 早报生成 | ~/.openclaw/workspace/scripts/daily-report.sh | ✅ 运行中 |

## 注意事项
- 不要依赖OpenClaw内置的`openclaw cron`（isolated session模式不稳定）
- 优先使用系统crontab + OpenClaw CLI组合
- 所有脚本必须设置可执行权限：`chmod +x`
- 任务输出重定向到日志文件便于排查
