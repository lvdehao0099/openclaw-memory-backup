#!/bin/bash
# 虾米启动自检脚本
# 每次会话启动时运行，确保核心规范已加载

echo "========================================"
echo "🦐 虾米启动自检"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# 检查核心文件是否存在
FILES=(
    "/root/.openclaw/workspace/SOUL.md"
    "/root/.openclaw/workspace/AGENTS.md"
    "/root/.openclaw/workspace/IDENTITY.md"
    "/root/.openclaw/workspace/USER.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $(basename $file)"
    else
        echo "❌ $(basename $file) 不存在！"
    fi
done

echo ""
echo "========================================"
echo "🚨 铁律背诵检查"
echo "========================================"
echo ""
echo "1. 文件创建前必须："
echo "   - 确定类型和目录"
echo "   - 说出完整路径"
echo "   - 确认工具选择"
echo ""
echo "2. 禁止行为："
echo "   - ❌ write file_path=\"文件名.md\" → 会扔到根目录"
echo "   - ❌ 在 workspace 根目录创建 .md 文件"
echo "   - ❌ 飞书文档先在本地写"
echo "   - ❌ 使用 edit 工具"
echo ""
echo "3. 飞书文档铁律："
echo "   - 必须用 feishu_doc"
echo "   - 必须指定 folder_token: Thhrfa3QglB5amdIMpEcY2tAndd"
echo "   - 禁止本地先写"
echo ""
echo "========================================"
echo "✅ 自检完成，开始工作"
echo "========================================"
