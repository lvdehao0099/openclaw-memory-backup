# 会话启动检查清单（每次会话强制执行）

## 会话开始前必须执行

### 1. 读取核心记忆（强制）
```
read path="~/.openclaw/workspace/MEMORY.md"
read path="~/.openclaw/workspace/memory/episodic/昨天日期.md"
read path="~/.openclaw/workspace/memory/episodic/前天日期.md"
```

### 2. 读取关键流程文件
```
read path="~/.openclaw/workspace/procedural/morning-report-rules.md"
read path="~/.openclaw/workspace/procedural/self-reliance-principle.md"
read path="~/.openclaw/workspace/procedural/file-edit-sop.md"
```

### 3. 检查当日待办
```
- 查看crontab今日任务
- 检查历史记录中的未完成事项
```

### 4. 确认已知信息（禁止询问）
- ✅ 早报格式（🔴🟡🟢👥）
- ✅ 团队进度（皓子APP UI、老于Web UI）
- ✅ 项目状态（Q2苏浙未开始、软件协会未开始）
- ✅ 客户信息（三协精密-李晓翠、夏总-下周跟进）

## 铁律
**如果信息在记忆文件里，禁止询问用户！**
不确定就查文件，查不到就标注"待确认"，绝不张嘴问。

## 检查机制
每次回复前问自己：
1. 这个信息在记忆文件里吗？→ 查文件
2. 这个任务已经设置cron了吗？→ 查cron list
3. 这个要求之前说过吗？→ 查历史记录

**目标：让用户零重复、零提醒**
