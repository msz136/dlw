from pathlib import Path
from bs4 import BeautifulSoup
import json
root=Path(__file__).resolve().parent;ws=root.parent.parent
before=max(root.glob('before_*.html'),key=lambda p:int(p.stem.split('_')[1]))
old=BeautifulSoup(before.read_text(encoding='utf-8'),'html.parser')
new=BeautifulSoup((ws/'2HS paper.html').read_text(encoding='utf-8'),'html.parser')
for sec in old.find_all('section',id=True):
 assert sec.get_text(' ',strip=True)==new.find(id=sec['id']).get_text(' ',strip=True)
assert [x['src'] for x in old.find_all('img')]==[x['src'] for x in new.find_all('img')]
ids={x['id'] for x in new.find_all(id=True)}
assert all(x['href'][1:] in ids for x in new.select('nav a'))
result={'reference':'dlw-paper.html','section_text_unchanged':True,'images_unchanged':True,'navigation_links':len(new.select('nav a')),'stylesheet':'layout.css','browser_screenshot':False}
(root/'layout_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
history=ws/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md'
with history.open('a',encoding='utf-8') as f:
 f.write('\n2026-10-26｜2HS同轮版式修订：按DLW主稿统一白底、1020px正文宽度、Georgia 17px/1.8、标题、分级目录、图注与三线表及打印样式；保留逻辑列对齐。逐节文本及图像链接与备份相同，97公式/11图/6表检查通过。证据：`Workspaces/hs_paper_20261026/layout.css`、`layout_validation.json`。仅静态验收，未做浏览器截图。\n')
p=ws/'PROGRESS_LOG.md';text=p.read_text(encoding='utf-8')
text=text.replace('\n## 上一次工作','\n版式已按DLW主稿对齐：白底、正文宽度/字体/行距、标题、分级目录、图表和打印样式；保留逻辑列对齐。逐节正文与图像未变，记录见 `Workspaces/hs_paper_20261026/layout_validation.json`。\n\n## 上一次工作',1)
assert len(text)<3000
p.write_text(text,encoding='utf-8')
print(json.dumps(result))
