# 热点雷达系统配置
# 自动追踪热点并记录到飞书

## 数据源配置

### RSS订阅源（工业/商业/AI相关）
- https://www.36kr.com/feed (36氪-商业)
- https://www.huxiu.com/rss/feed (虎嗅)
- https://www.leiphone.com/rss (雷锋网-AI)
- https://www.jiqizhixin.com/rss (机器之心-AI)
- https://rss.cnbeta.com/cnbeta.xml (cnBeta-科技)
- https://www.geekpark.net/rss (极客公园)

### 微信公众号监控（需手动）
- 智能制造IMS
- 工业互联网产业联盟
- 中国工业新闻网
- AI前线
- 机器之能

### 知乎热榜API
- https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total

## 飞书表格结构

表格名称：热点雷达追踪表
链接：https://ai-zhineng.feishu.cn/wiki/xxx

字段：
- 日期（日期）
- 热点标题（文本）
- 来源（单选：RSS/微博/知乎/公众号）
- 原文链接（URL）
- 相关度（单选：高/中/低）
- 关联业务（多选：AI老师傅/工业维保/创业/SaaS/其他）
- 选题建议（文本）
- 状态（单选：待讨论/已选题/已发布/已放弃）
- 备注（文本）

## 自动任务配置

### 每日任务（凌晨2:00执行）
1. 抓取各RSS源最新文章
2. AI分析每篇文章与业务的关联度
3. 高/中相关度文章写入飞书表格
4. 生成简报发送到飞书

### 每周任务（周日晚9:00执行）
1. 汇总本周所有热点
2. AI生成选题建议报告
3. 发送到飞书，供周一讨论

## 人工干预点
- 每日简报查看（5分钟）
- 每周选题会（30分钟）
- 热点手动标记状态

## 预期效果
- 不再为"写什么"发愁
- 选题有据可依（热点数据支撑）
- 蹭热点成功率提升
- 公众号自然流量增加
