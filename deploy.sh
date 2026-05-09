#!/bin/bash

# 霓虹尘埃 — 一键部署脚本
# 使用：./deploy.sh

cd "$(dirname "$0")"

echo "📝 检查更改..."
git status --short

echo ""
echo "📦 添加所有更改..."
git add -A

echo ""
echo "💾 提交更改..."
git commit -m "更新：$(date '+%Y-%m-%d %H:%M')"

echo ""
echo "🚀 推送到 GitHub..."
git push

echo ""
echo "✅ 完成！GitHub Pages 将在 1-2 分钟内自动更新"
echo "📱 访问：https://deadlyjoker.github.io/novel-neon-dust/"
