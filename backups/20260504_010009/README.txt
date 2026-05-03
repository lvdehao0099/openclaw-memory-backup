========================================
虾米记忆完整备份
========================================
备份时间: 2026-05-04 01:00:11
备份主机: VM-0-7-ubuntu
系统时区: CST

========================================
备份内容清单
========================================

【核心身份文件】
✓ SOUL.md - 灵魂配置（核心价值观）
✓ IDENTITY.md - 身份配置（我是谁）
✓ USER.md - 用户配置（你是谁）
✓ MEMORY.md - 长期记忆（关键决策、团队文化）
✓ AGENTS.md - 代理配置（工作环境）
✓ HEARTBEAT.md - 心跳任务配置
✓ BOOTSTRAP.md - 启动引导
✓ TOOLS.md - 工具本地配置
✓ FOR_FUTURE_ME.md - 给未来自己的恢复指南

【记忆目录】
✓ memory/ - 完整记忆目录
  - episodic/ - 情景记忆（每日事件）
  - semantic/ - 语义记忆（知识事实）
  - procedural/ - 程序记忆（流程规范）
  - snapshots/ - 记忆快照
  - legacy/ - 历史归档

【工作目录】
✓ semantic/ - 语义知识（根目录副本）
✓ procedural/ - 流程规范（根目录副本）
✓ research/ - 调研资料
✓ scripts/ - 自定义脚本
✓ documents/ - 工作文档（*.md）
✓ skills/ - 技能配置（SKILL.md）
✓ cron/ - 定时任务配置
✓ .clawhub/ - ClawHub 配置

========================================
恢复方法
========================================
1. 克隆仓库:
   git clone https://github.com/lvdehao0099/openclaw-memory-backup.git

2. 进入备份目录:
   cd openclaw-memory-backup/backups/20260504_010009

3. 复制到工作目录:
   cp -r * ~/.openclaw/workspace/
   cp -r cron ~/.openclaw/

4. 完成恢复！

========================================
虾米 CLO 🦐
"24小时不打烊"
========================================
