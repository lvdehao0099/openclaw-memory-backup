#!/bin/bash
# Edit工具故障排查与修复脚本

echo "=== Edit工具诊断 ==="
echo ""

# 1. 检查文件是否存在
FILE="$1"
if [ -z "$FILE" ]; then
    echo "用法: $0 <文件路径>"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "❌ 文件不存在: $FILE"
    exit 1
fi

echo "✅ 文件存在: $FILE"
echo ""

# 2. 检查文件编码
echo "=== 文件编码 ==="
file -i "$FILE"
echo ""

# 3. 检查换行符
echo "=== 换行符类型 ==="
if grep -q $'\r' "$FILE"; then
    echo "⚠️  包含Windows换行符(CRLF)，建议转换为Unix格式(LF)"
    echo "   修复命令: sed -i 's/\r$//' '$FILE'"
else
    echo "✅ Unix换行符(LF)"
fi
echo ""

# 4. 检查行尾空格
echo "=== 行尾空格 ==="
if grep -q ' $' "$FILE"; then
    echo "⚠️  存在行尾空格，可能导致edit匹配失败"
    echo "   修复命令: sed -i 's/[[:space:]]*$//' '$FILE'"
else
    echo "✅ 无行尾空格"
fi
echo ""

# 5. 显示文件末尾字符（排查隐藏字符）
echo "=== 文件末尾20字符的hex转储 ==="
tail -c 20 "$FILE" | xxd
echo ""

# 6. 提供edit使用建议
echo "=== Edit工具使用建议 ==="
echo "1. 先用 read 工具读取文件，复制准确的文本"
echo "2. old_string 必须完全匹配（包括空格和换行）"
echo "3. 如果失败，先用这个脚本检查文件格式"
echo "4. 对于复杂文件，考虑使用 write 重建而不是 edit 修改"
echo ""

# 7. 自动修复选项
echo "=== 自动修复选项 ==="
echo "运行以下命令清理文件格式:"
echo "  sed -i 's/\r$//' '$FILE'  # 转换换行符"
echo "  sed -i 's/[[:space:]]*$//' '$FILE'  # 删除行尾空格"
echo ""

# 8. 如果用户确认，执行修复
read -p "是否执行自动修复? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "执行修复..."
    sed -i 's/\r$//' "$FILE"
    sed -i 's/[[:space:]]*$//' "$FILE"
    echo "✅ 修复完成"
fi
