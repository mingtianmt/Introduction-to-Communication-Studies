#!/usr/bin/env python3
# 读取 assignments/html/*.html，解析 <title> 和纯文本，生成 assignments/index.json
import os, re, json, glob

out = []
html_dir = "assignments/html"
for path in sorted(glob.glob(os.path.join(html_dir, "*.html"))):
    name = os.path.basename(path)
    url = f"{html_dir}/{name}"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        s = f.read()
    title_m = re.search(r"<title[^>]*>(.*?)</title>", s, re.I|re.S)
    title = title_m.group(1).strip() if title_m else os.path.splitext(name)[0]
    # 去除标签，取得纯文本
    text = re.sub(r"<script.*?>.*?</script>", "", s, flags=re.I|re.S)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.I|re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    excerpt = text[:300] + ("…" if len(text) > 300 else "")
    out.append({"title": title, "url": url, "excerpt": excerpt})

os.makedirs(os.path.dirname("assignments/index.json"), exist_ok=True)
with open("assignments/index.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("wrote assignments/index.json with", len(out), "entries")
