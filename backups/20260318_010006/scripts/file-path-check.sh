#!/bin/bash
# 文件创建拦截脚本
# 在创建文件前检查路径是否正确

FILE_PATH="$1"

# 检查是否是根目录创建
if [[ "$FILE_PATH" == "/root/.openclaw/workspace/"* ]] && [[ "$FILE_PATH" != *"/"* ]]; then
    echo "❌ 错误：你正在尝试在 workspace 根目录创建文件！"
    echo "文件路径: $FILE_PATH"
    echo ""
    echo "请使用正确的目录："
    echo "  - 日记/日志 → memory/"
    echo "  - 流程规范 → procedural/"
    echo "  - 知识记录 → semantic/"
    echo "  - 调研资料 → research/"
    echo "  - 飞书文档 → 直接用 feishu_doc 工具"
    exit 1
fi

# 检查是否指定了完整路径
if [[ ! "$FILE_PATH" =~ ^/root/.openclaw/workspace/ ]]; then
    echo "⚠️ 警告：路径不是以 /root/.openclaw/workspace/ 开头"
    echo "完整路径: $FILE_PATH"
    exit 1
fi

echo "✅ 路径检查通过: $FILE_PATH"
exit 0
