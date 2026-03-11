# HEARTBEAT.md

## 系统事件处理

当收到系统事件时，根据事件内容执行对应操作：

### 事件: "生成今日早报并发送给吕总"
1. 获取今日日期（Asia/Shanghai时区）
2. 读取飞书任务表格获取今日待办
3. 读取项目进度（Q2苏浙市场、软件协会创新案例申报）
4. 生成早报内容并发送到飞书当前会话

### 事件: "发送提醒：跟进瓦轴项目合同签署进度"
发送提醒消息："🦐 虾米提醒：请跟进瓦轴项目合同签署进度，确认回款时间节点。"

### 事件: "运行记忆整理脚本"
运行: ~/.openclaw/workspace/skills/memory-manager/organize.sh

## 常规心跳检查 (每30分钟)

### Memory Management
1. 运行: ~/.openclaw/workspace/skills/memory-manager/detect.sh
2. 如果警告/危险: ~/.openclaw/workspace/skills/memory-manager/snapshot.sh
