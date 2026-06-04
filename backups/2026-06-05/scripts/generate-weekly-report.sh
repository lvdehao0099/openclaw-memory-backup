# 周报生成与发送脚本
# 每周五晚上自动执行

WEEK_START=$(date -d "last saturday" +%Y-%m-%d)
WEEK_END=$(date +%Y-%m-%d)
WEEK_NUM=$(date +%U)
YEAR=$(date +%Y)

# 生成周报HTML
cat > /tmp/weekly_report.html << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>虾米🦞·每周运营简报</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px 0;
        }
        .container {
            max-width: 850px;
            margin: 0 auto;
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { font-size: 16px; opacity: 0.9; }
        .content { padding: 40px; }
        .section { margin-bottom: 35px; }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #764ba2;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f093fb;
        }
        .item {
            background: #f8f9fa;
            padding: 15px 20px;
            margin-bottom: 12px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .item-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        .item-desc {
            color: #5a6c7d;
            font-size: 14px;
            line-height: 1.5;
        }
        .tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
        }
        .tag-success { background: #d4edda; color: #155724; }
        .tag-progress { background: #fff3cd; color: #856404; }
        .tag-high { background: #f8d7da; color: #721c24; }
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin: 20px 0;
        }
        .stat-item { text-align: center; }
        .stat-number { font-size: 36px; font-weight: bold; }
        .stat-label { font-size: 14px; opacity: 0.9; }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 13px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦐 虾米·每周运营简报</h1>
            <p>\${WEEK_START} - \${WEEK_END} | 第\${WEEK_NUM}周</p>
        </div>
        <div class="content">
            <!-- 内容由AI动态生成 -->
            <div class="section">
                <div class="section-title">📊 本周数据概览</div>
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number" id="customer-count">--</div>
                        <div class="stat-label">客户总数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="visit-count">--</div>
                        <div class="stat-label">本周拜访</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="high-intent">--</div>
                        <div class="stat-label">高意向客户</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number" id="task-rate">--%</div>
                        <div class="stat-label">任务完成率</div>
                    </div>
                </div>
            </div>
            <div class="footer">
                <p>🦐 虾米 CLO | 首席执虾官</p>
                <p>本简报由 AI 自动生成 | \${YEAR}年</p>
            </div>
        </div>
    </div>
</body>
</html>
EOF

echo "周报模板已生成"
