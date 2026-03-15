# HEARTBEAT.md

## 系统事件处理

当收到系统事件时，根据事件内容执行对应操作：

### 事件: "生成今日早报并发送给吕总"
1. 获取今日日期（Asia/Shanghai时区）
2. 读取戒烟记录文件 memory/quitting-smoking.md，获取连续戒烟天数（计算里程碑：7/14/30天）
3. 查询飞书待办追踪表（app_token: O2rAb69hOa16aks5QHucOajSnWh, table_id: tbldg2S9P76Ig1l0）：
   - **关键：使用「截止日期」字段判断时间，不依赖事项名称中的相对日期**
   - 根据截止日期计算：今天/明天/后天/M月D日
4. 查询cron jobs中未来48小时内即将触发的任务
5. 生成精简版早报（纯文本格式，无表格）：
   ```
   🦐 虾米早报 · YYYY年M月D日 星期X
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔴 私人待办（含戒烟里程碑提醒）
   🟡 工作待办（带优先级标识 + 根据截止日期显示今天/明天/日期）
   🟢 今日提醒（未来48小时定时任务）
   👥 团队事项（老于/皓子）
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📊 数据来源：戒烟记录 + 飞书待办表 + 定时任务
   ```
6. 发送早报内容到飞书当前会话

### 事件: "发送提醒：跟进瓦轴项目合同签署进度"
发送提醒消息："🦐 虾米提醒：请跟进瓦轴项目合同签署进度，确认回款时间节点。"

### 事件: "运行记忆整理脚本"
运行: ~/.openclaw/workspace/skills/memory-manager/organize.sh

## 常规心跳检查 (每30分钟)

### Memory Management
1. 运行: ~/.openclaw/workspace/skills/memory-manager/detect.sh
2. 如果警告/危险: ~/.openclaw/workspace/skills/memory-manager/snapshot.sh
