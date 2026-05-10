#!/bin/bash
# 霓虹尘埃 — 章节同步部署脚本
# 将 source chapters 同步到 docs/ 部署目录

cd "$(dirname "$0")"

echo "📂 同步第一卷章节到部署目录..."
for i in $(seq -w 1 80); do
  src="chapters/VOLUME-01-CHAPTER-${i}.md"
  for dst in docs/chapters docs/neon-dust/chapters; do
    if [ -f "$src" ]; then
      cp "$src" "${dst}/Ch${i}.md"
    fi
  done
done

echo "📂 同步第二卷章节到部署目录..."
vol2_num=1
for i in $(seq -w 81 127); do
  src_num=$(echo $vol2_num | sed 's/^0*//')
  src="chapters/VOLUME-02-CHAPTER-$(printf '%02d' $src_num).md"
  for dst in docs/chapters docs/neon-dust/chapters; do
    if [ -f "$src" ]; then
      cp "$src" "${dst}/Ch${i}.md"
    fi
  done
  vol2_num=$((vol2_num + 1))
done

echo "📂 同步 chapter-list.js..."
cp docs/chapter-list.js docs/neon-dust/chapter-list.js

echo "✅ 同步完成"
echo "📊 章节数：$(ls docs/chapters/Ch*.md 2>/dev/null | wc -l)"
