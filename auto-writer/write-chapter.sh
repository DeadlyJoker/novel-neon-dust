#!/bin/bash
# 霓虹尘埃自动写作脚本
# 用途：写入下一章并更新状态

WORKSPACE="/Users/wangqichen/.openclaw/workspace"
STATE_FILE="$WORKSPACE/novel-projects/neon-dust/auto-writer/state.json"
CHAPTERS_DIR="$WORKSPACE/novel-projects/neon-dust/chapters"
OUTLINE_FILE="$WORKSPACE/novel-projects/neon-dust/outline/VOLUME-01-CHAPTER-OUTLINE.md"
VOL2_OUTLINE="$WORKSPACE/novel-projects/neon-dust/auto-writer/volume2-outline.md"

STATE=$(cat "$STATE_FILE")
CURRENT_VOLUME=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['currentVolume'])")
CURRENT_CHAPTER=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['currentChapter'])")
VOL1_LAST=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['volume1LastChapter'])")
STATUS=$(echo "$STATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

echo "=== 霓虹尘埃自动写作 ==="
echo "当前状态: $STATUS"
echo "当前卷: $CURRENT_VOLUME | 当前章: $CURRENT_CHAPTER | 卷末: $VOL1_LAST"
