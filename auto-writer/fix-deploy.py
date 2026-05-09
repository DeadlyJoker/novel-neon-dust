#!/usr/bin/env python3
"""部署同步脚本：多卷支持，章节数据嵌入 reader.html"""

import os, re, shutil

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SRC_DIR = os.path.join(WORKSPACE, "novel-projects/neon-dust/chapters")
DEPLOY_DIR = os.path.join(WORKSPACE, "novel-projects/apocalypse/docs/neon-dust/chapters")
CHAPTER_LIST = os.path.join(WORKSPACE, "novel-projects/apocalypse/docs/neon-dust/chapter-list.js")
READER_HTML = os.path.join(WORKSPACE, "novel-projects/apocalypse/docs/reader.html")
INDEX_HTML = os.path.join(WORKSPACE, "novel-projects/apocalypse/docs/index.html")

VOLUME_NAMES = {
    1: "第一卷：地下医生",
    2: "第二卷：钢铁兄弟",
    3: "第三卷：身世之秘",
    4: "第四卷：钢铁王座",
    5: "第五卷：霓虹尽头",
}

CN = ["零","一","二","三","四","五","六","七","八","九"]

def num_to_cn(n):
    if n < 10: return CN[n]
    if n == 10: return "十"
    if n < 20: return "十" + (CN[n % 10] if n % 10 else "")
    s = str(n)
    r = ""
    for i, c in enumerate(s):
        d = int(c)
        p = len(s) - i - 1
        if d > 0:
            r += CN[d]
            if p == 1: r += "十"
            elif p == 2: r += "百"
        elif r and not r.endswith("零"):
            r += "零"
    return r.rstrip("零")

def get_title(path):
    with open(path, encoding="utf-8") as f:
        fl = f.readline().strip()
    m = re.search(r'[：:]\s*「([^」]*)」', fl)
    if m: return m.group(1)
    m = re.search(r'「([^」]*)」', fl)
    if m: return m.group(1)
    m = re.search(r'[：:]\s*(.*)', fl)
    if m: return m.group(1).strip()
    return fl.replace("# ", "").strip()

def main():
    # 列出所有源文件
    files = [f for f in os.listdir(SRC_DIR) if f.startswith("VOLUME-") and f.endswith(".md")]
    files.sort(key=lambda f: (
        int(re.search(r"VOLUME-(\d+)", f).group(1)),
        int(re.search(r"CHAPTER-(\d+)", f).group(1))
    ))
    print(f"找到 {len(files)} 个源文件")

    # 计算各卷偏移量
    offsets = {}
    for f in files:
        v = int(re.search(r"VOLUME-(\d+)", f).group(1))
        if v not in offsets:
            prevs = [x for x in files if x.startswith(f"VOLUME-{v-1:02d}-")]
            offsets[v] = max((int(re.search(r"CHAPTER-(\d+)", x).group(1)) for x in prevs), default=0)

    # 清理部署目录
    os.makedirs(DEPLOY_DIR, exist_ok=True)
    for old in os.listdir(DEPLOY_DIR):
        if old.endswith(".md"):
            os.remove(os.path.join(DEPLOY_DIR, old))

    # 复制文件，构建章节数据
    chapters = []
    for fname in files:
        v = int(re.search(r"VOLUME-(\d+)", fname).group(1))
        c = int(re.search(r"CHAPTER-(\d+)", fname).group(1))
        g = offsets.get(v, 0) + c
        dname = f"Ch{g:03d}.md"
        shutil.copy2(os.path.join(SRC_DIR, fname), os.path.join(DEPLOY_DIR, dname))
        title = get_title(os.path.join(SRC_DIR, fname))
        chapters.append({"id": f"Ch{g:03d}", "vol": v,
            "title": f"第{num_to_cn(v)}卷第{num_to_cn(c)}章 {title}",
            "file": f"neon-dust/chapters/{dname}"})
        print(f"  Ch{g:03d} (V{v}Ch{c:02d})")

    # 生成 chapter-list.js
    def gen_js(chs):
        lines = ['var CHAPTER_LIST={title:"《霓虹尘埃》",author:"苏苏工作室",volumes:[']
        vols = {}
        for ch in chs:
            vols.setdefault(ch["vol"], []).append(ch)
        for vn in sorted(vols):
            vname = VOLUME_NAMES.get(vn, f"第{num_to_cn(vn)}卷")
            lines.append(f'{{title:"{vname}",chapters:[')
            for i, ch in enumerate(vols[vn]):
                t = ch["title"].replace('"', '\\"')
                comma = "," if i > 0 else ""
                lines.append(f'{comma}{{id:"{ch["id"]}",title:"{t}",file:"{ch["file"]}"}}')
            lines.append("]},")
        lines.append("]};")
        return "\n".join(lines)

    js = gen_js(chapters)
    with open(CHAPTER_LIST, "w", encoding="utf-8") as f:
        f.write(js + "\n")
    print(f"\n✅ chapter-list.js 生成完毕，共 {len(chapters)} 章")

    # 嵌入 reader.html
    with open(READER_HTML, encoding="utf-8") as f:
        html = f.read()

    # 用正则替换内联 CHAPTER_LIST
    pattern = r'var CHAPTER_LIST=\{title:"[^"]*",author:"[^"]*",volumes:\[.*?\}\]\};'
    replacement = js.strip()
    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
        print(f"✅ reader.html 章节数据已替换（{len(chapters)}章）")
    else:
        # 首次：替换动态加载
        old = '''  function loadChapterData() {\\n    return new Promise(function(resolve) {\\n      var script = document.createElement('script');\\n      script.src = bookId + '/chapter-list.js';\\n      script.onload = function() {\\n        if (typeof CHAPTER_LIST !== 'undefined' && CHAPTER_LIST && CHAPTER_LIST.volumes && CHAPTER_LIST.volumes.length > 0) {\\n          resolve(CHAPTER_LIST);\\n        } else {\\n          resolve(null);\\n        }\\n      };\\n      script.onerror = function() { resolve(null); };\\n      document.head.appendChild(script);\\n      // Timeout for slow network\\n      setTimeout(function() { resolve(null); }, 2000);\\n    });\\n  }'''
        new_block = f'''  // ══════════════════════════════════════════════
  //  内联章节数据（部署时自动生成，杜绝缓存问题）
  // ══════════════════════════════════════════════
{js}

  function loadChapterData() {{
    return new Promise(function(resolve) {{
      // 直接使用内联数据，无外部请求
      if (typeof CHAPTER_LIST !== 'undefined' && CHAPTER_LIST && CHAPTER_LIST.volumes && CHAPTER_LIST.volumes.length > 0) {{
        resolve(CHAPTER_LIST);
      }} else {{
        resolve(null);
      }}
    }});
  }}'''
        html = html.replace(old, new_block)
        print(f"✅ reader.html 首次嵌入章节数据（{len(chapters)}章）")

    with open(READER_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    # 更新 index.html
    total_chars = sum(
        os.path.getsize(os.path.join(DEPLOY_DIR, ch["id"] + ".md"))
        for ch in chapters
        if os.path.exists(os.path.join(DEPLOY_DIR, ch["id"] + ".md"))
    )
    words = f"约{total_chars // 10000}万字"
    with open(INDEX_HTML, encoding="utf-8") as f:
        idx = f.read()
    def repl(m):
        return f'{m.group(1)}chapters: {len(chapters)},\\n    words: "{words}",'
    idx = re.sub(
        r'(id: "neon-dust",\\s*\\n\\s*title: "霓虹尘埃",[^}]*?chapters: )\\d+,\\s*\\n\\s*words: "[^"]*",',
        repl, idx, flags=re.DOTALL
    )
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(idx)
    print(f"✅ index.html 更新：{len(chapters)}章 · {words}")

if __name__ == "__main__":
    main()
