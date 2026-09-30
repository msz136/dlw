"""Render the numerical paper using the existing Report.html typography."""
from pathlib import Path
import re, html, shutil
import markdown
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BACKUP=ROOT/'Workspaces/dlw_error_inventory_20260929/before_paper_rewrite'
BACKUP.mkdir(exist_ok=True)
for p,name in ((HERE/'_src/index.src.html','index.src.html'),(ROOT/'index.html','index.html'),(ROOT/'Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md','CONTROLLED_RESULTS.md')):
    if not (BACKUP/name).exists():shutil.copy2(p,BACKUP/name)

source=(HERE/'_src/index.md').read_text(encoding='utf-8')
formulas=[]
def protect(m):
    formulas.append(m[0]);return f'MATHPLACEHOLDER{len(formulas)-1}END'
body=markdown.markdown(re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,source),extensions=['tables','md_in_html'])
for i,f in enumerate(formulas):body=body.replace(f'MATHPLACEHOLDER{i}END',html.escape(html.unescape(f),quote=False))
soup=BeautifulSoup(body,'html.parser')
for i,heading in enumerate(soup.find_all('h2'),1):heading['id']=f'section-{i}'
for i,table in enumerate(soup.find_all('table'),1):
    table['id']=f'table-{i}'
    wrapper=soup.new_tag('div',attrs={'class':'table-wrap','tabindex':'0','role':'region','aria-label':f'表{i}，可横向滚动'})
    table.wrap(wrapper)
    for th in table.find_all('th'):th['scope']='col'
for p in soup.find_all('p'):
    if p.get_text().strip().startswith('$$'):p['class']=['equation']

reference=(HERE/'_src/Report.src.html').read_text(encoding='utf-8')
css=next(c for c in re.findall(r'<style>(.*?)</style>',reference,flags=re.S) if '@@KATEX_CSS@@' not in c)
css+='''
h1,h2{text-wrap:balance}p{text-wrap:pretty}table{font-variant-numeric:tabular-nums}
.abstract{text-indent:0;font-size:11pt;line-height:1.8;margin:0 0 24px}
.caption{text-indent:0;margin:20px 0 8px}
.table-wrap{overflow-x:auto;margin:0 0 20px}
.table-wrap table{margin:0;min-width:510px}
.table-wrap:focus-visible{outline:2px solid #555;outline-offset:3px}
.equation{text-indent:0}.references p{text-indent:0;font-size:10.5pt;line-height:1.7}
.table-note{text-indent:0;font-size:10pt;line-height:1.65;margin:6px 0 16px}
@media(max-width:650px){.table-wrap table{min-width:510px}.abstract{font-size:10.5pt}}
@media print{.table-wrap{overflow:visible}.table-wrap table{min-width:0}a{text-decoration:none}}
'''
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 孤子数值解的误差比较</title><style>@@KATEX_CSS@@</style><style>'''+css+'''</style></head><body><main>'''+str(soup)+'''</main><script>@@KATEX_JS@@</script><script>renderMathInElement(document.querySelector("main"),{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});</script></body></html>'''
(HERE/'_src/index.src.html').write_text(page,encoding='utf-8')
(ROOT/'Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md').write_text(source.replace('href="Workspaces/','href="../'),encoding='utf-8')
print(f'Paper written: {len(formulas)} mathematical expressions, {len(soup.find_all("table"))} tables; typography from Report.src.html.')
