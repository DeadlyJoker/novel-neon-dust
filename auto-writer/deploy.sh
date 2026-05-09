#!/bin/bash
# 霓虹尘埃 一键部署脚本
# 使用 Python 脚本做同步（更可靠），bash 只负责 git push

WORKSPACE="/Users/wangqichen/.openclaw/workspace"
APOCALYPSE="$WORKSPACE/novel-projects/apocalypse"

echo "=== 霓虹尘埃 一键部署 ==="

# 用 Python 同步文件 + 生成章节列表
python3 "$WORKSPACE/novel-projects/neon-dust/auto-writer/fix-deploy.py" || exit 1

echo ""
echo "🚀 提交并推送到 GitHub..."
cd "$APOCALYPSE"

git add -A
git commit -m "📖 霓虹尘埃 批量部署：$(date '+%Y-%m-%d %H:%M')"
git push

echo ""
echo "✅ 部署完成！"
echo "📱 线上地址：https://deadlyjoker.github.io/novel-apocalypse/?book=neon-dust"
echo "   预计 1-2 分钟后更新生效"
