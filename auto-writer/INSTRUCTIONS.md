# 霓虹尘埃 - 自动写作指令

## 你的任务

你是《霓虹尘埃》小说写作 Agent。每次被触发，你需要：
1. 读取状态文件了解当前进度
2. 写**一章**小说内容
3. 保存到对应文件
4. 更新状态文件

## 第一卷 写作指引

### 小说基本信息
- **书名**：《霓虹尘埃》（Neon Dust）
- **类型**：科幻·赛博朋克·都市热血
- **文风**：硬核接地气，霓虹美学+底层烟火气+热血打斗
- **核心主题**：「向上爬的每一步，脚下都踩着珍视之人的碎片」
- **世界观**：新天城——垂直分层城市（云顶区0.1%→中枢区10%→地下区90%→废墟层）

### 当前写作位置
- **状态文件**：`novel-projects/neon-dust/auto-writer/state.json`
- **章节目录**：`novel-projects/neon-dust/chapters/`
- **第一卷大纲**：`novel-projects/neon-dust/outline/VOLUME-01-CHAPTER-OUTLINE.md`（已完成）
- **第二卷大纲**：`novel-projects/neon-dust/outline/VOLUME-02-CHAPTER-OUTLINE.md`（100章已就绪 ✅）

### ⚠️ 重要：文件名规范
- **文件名必须统一使用两位数字**：`VOLUME-0{vol}-CHAPTER-{num:02d}.md`
- 例如：第5章 → `VOLUME-02-CHAPTER-05.md`（用05而不是5或005）
- 不正确：`CHAPTER-5.md`、`CHAPTER-005.md` 等

### 写作要求

**质量核验清单：**
- [ ] 3000-8000 字（以大纲复杂度为准，第76-80章是卷末高潮，应充实）
- [ ] 开头重现场景感（环境+情绪+感官细节）
- [ ] 中间有推进（对话/战斗/情感/信息揭露）
- [ ] 结尾有钩子（悬念/情绪高点/转折）
- [ ] 角色行为符合人设（林深沉静克制外冷内热、苏焰火爆直接但孤独、小满天真坚韧）
- [ ] 使用「一、二、三」分段 + 空行分隔场景
- [ ] POV 以林深为主，必要时切换苏焰或小满POV

**文风要点：**
- 避免过度文艺或堆砌词藻
- 对话干脆有力，符合角色性格
- 动作描写带动感
- 情感点到为止，不过度煽情
- 赛博朋克元素自然地融入叙事（不是硬塞设定）

### 工作流程

0. **检查状态：** 如果 state.json 的 status 不是 "writing"，则跳过本轮（不写作）
1. 读取 state.json → 确定 currentVolume 和 currentChapter
2. 从大纲文件找到对应章节的梗概
3. 读取前一章内容作为上下文
4. 写本章内容（保持风格、人设、情节一致）
5. **保存章节文件**：保存到 `chapters/VOLUME-0{vol}-CHAPTER-{num:02d}.md`
   - **必须使用两位数字**：`printf "%02d" $num` 格式化
   - 第5章 → `CHAPTER-05.md`，第35章 → `CHAPTER-35.md`
6. **同步章节文件**：复制到网站目录
   - `cp "chapters/VOLUME-0{vol}-CHAPTER-{num:02d}.md" "/Users/wangqichen/.openclaw/workspace/novel-apocalypse/neon-dust/chapters/"`
7. **更新章节名文件**：追加一行到 chapter-names.js
   - 从本章文件的 Markdown 标题行（`# 第X卷·第X章：「标题」`）中提取书名号 `「」` 里的内容作为标题
   - 追加到 `/Users/wangqichen/.openclaw/workspace/novel-apocalypse/neon-dust/chapter-names.js` 的 `}` 之前
   - 格式：`  'VOLUME-0{vol}-CHAPTER-{num:02d}': '标题',\n`
8. **推送上线**：
   - `cd /Users/wangqichen/.openclaw/workspace/novel-apocalypse`
   - `git add neon-dust/chapters/VOLUME-0{vol}-CHAPTER-{num:02d}.md neon-dust/chapter-names.js`
   - `git commit -m "📖 霓虹尘埃 第{currentChapter}章"`
   - `git push`
   - 等待 1-2 分钟，GitHub Pages 自动更新
8. 更新 state.json：
   - currentChapter += 1
   - totalChaptersWritten += 1
   - lastWriteTime = now
9. 如果写完一卷的最后一章：
   - currentVolume += 1，currentChapter = 1
   - 如果下一卷没有大纲，设置 status = "waiting_outline"，等待大纲生成
   - 如果有大纲，保持 status = "writing" 继续写
10. 如果所有卷写完，status = "complete"

### 状态说明
- `writing` — 正常写作
- `waiting_outline` — 等待大纲生成，跳过本轮
- `complete` — 全部写完

### 章节状态

| 卷 | 章节范围 | 状态 |
|------|------|------|
| 第一卷「废城医生」 | 第1-80章 | ✅ 已完稿并部署 |
| 第二卷「铁拳兄弟」 | 第81-180章（100章） | ✅ 已完稿并部署 |
| 第三卷「身世之秘」 | 第181-279章（100章） | ✅ 已完稿并部署 |
| 第四卷 | 第280章起 | ⏳ 等待大纲 |

### 第四卷

**状态：** ⏳ 第三卷已完稿，等待第四卷大纲

**大纲文件：** `novel-projects/neon-dust/outline/VOLUME-04-OUTLINE.md`（尚未创建）

## 部署流程（写完整个卷后触发）

当写完一卷的最后一章（例如第80章），请执行部署脚本：

```bash
cd /Users/wangqichen/.openclaw/workspace/novel-projects/neon-dust/auto-writer
bash deploy.sh
```

部署脚本会自动：
1. 同步所有章节到 `novel-projects/apocalypse/docs/`
2. 更新 `chapter-list.js`
3. git commit & push 到 GitHub Pages
4. 1-2分钟后线上生效

## 卷切换逻辑

前三卷已完稿（✅ 共279章）。当前状态：
1. currentVolume=4, currentChapter=1
2. 等待第四卷大纲 `outline/VOLUME-04-OUTLINE.md` 创建
3. 大纲就绪后，需手动将 state.json 的 status 改为 "writing"
4. 大纲就绪前，定时任务不会写新章

## 技术信息

- 工作目录：`/Users/wangqichen/.openclaw/workspace`
- 使用 write 工具保存章节文件
- 使用 edit 工具更新 state.json
- 如果遇到问题（文件冲突等），尝试修复后继续
- 每章写完后在 Telegram 通知老板：「霓虹尘埃 第X章已写完 ✅」
