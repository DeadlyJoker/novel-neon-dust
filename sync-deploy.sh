#!/bin/bash
# 霓虹尘埃 — 章节同步部署脚本
cd "$(dirname "$0")"

V1_COUNT=80
V2_COUNT=$(ls chapters/VOLUME-02-CHAPTER-*.md 2>/dev/null | wc -l | tr -d ' ')

echo "📂 同步章节 (V1: ${V1_COUNT}章 + V2: ${V2_COUNT}章)..."

for d in docs/chapters docs/neon-dust/chapters; do
  mkdir -p "$d"
  rm -f "$d"/Ch*.md
done

for i in $(seq 1 $V1_COUNT); do
  src="chapters/VOLUME-01-CHAPTER-$(printf '%02d' $i).md"
  [ -f "$src" ] || continue
  for d in docs/chapters docs/neon-dust/chapters; do
    cp "$src" "${d}/Ch$(printf '%03d' $i).md"
  done
done

for i in $(seq 1 $V2_COUNT); do
  src="chapters/VOLUME-02-CHAPTER-$(printf '%02d' $i).md"
  [ -f "$src" ] || continue
  for d in docs/chapters docs/neon-dust/chapters; do
    cp "$src" "${d}/Ch$(printf '%03d' $((80 + i))).md"
  done
done

cp docs/chapter-list.js docs/neon-dust/chapter-list.js

echo "✅ 同步完成 ($(ls docs/neon-dust/chapters/Ch*.md 2>/dev/null | wc -l | tr -d ' ') 章)"
