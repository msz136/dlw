"""Append the Section 5 rewrite note to the manuscript's editorial guide."""
from pathlib import Path
import hashlib, re

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2] / 'dlw-paper.html'
text = PAPER.read_text(encoding='utf-8')

old = '<p class="status">2026-10-25：5.3补入'
new = ('<p class="status">2026-10-25（Section 5 重写）：5.1–5.4 的叙述按用户提供的 Gemini 稿整节替换，'
       'Table 1–5 与 Figure 1–28 的原块、原图注与 PDF 链接原样保留，按新叙述的位置摆放；'
       '5.1 的“粗体表示最小值”说明与表4对齐（并列最小值同时加粗）。其余章节字节不变。</p>'
       '<p class="status">2026-10-25：5.3补入')
assert text.count(old) == 1
text = text.replace(old, new, 1)
PAPER.write_text(text, encoding='utf-8')
print('ok', hashlib.sha256(PAPER.read_bytes()).hexdigest())
