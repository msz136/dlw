"""Render the numerical paper using the existing Report.html typography."""
from pathlib import Path
import re, html, shutil, base64
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
body=markdown.markdown(re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,source),extensions=['tables','md_in_html','fenced_code'])
for i,f in enumerate(formulas):body=body.replace(f'MATHPLACEHOLDER{i}END',html.escape(html.unescape(f),quote=False))
soup=BeautifulSoup(body,'html.parser')
for image in soup.find_all('img'):
    source_path=ROOT/image['src']
    if source_path.is_file() and source_path.suffix.lower()=='.png':
        image['src']='data:image/png;base64,'+base64.b64encode(source_path.read_bytes()).decode('ascii')
        from PIL import Image
        with Image.open(source_path) as picture:
            image['width'],image['height']=picture.size
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
.field-details{margin:24px 0;border-top:1px solid #bbb;padding-top:12px}
.field-details summary{cursor:pointer;font-weight:bold}
.field-details summary:focus-visible{outline:2px solid #1776bc;outline-offset:4px}
.field-figure{margin:24px 0 32px}.field-figure img{display:block;max-width:100%}
@media(max-width:650px){.table-wrap table{min-width:510px}.abstract{font-size:10.5pt}}
@media print{.table-wrap{overflow:visible}.table-wrap table{min-width:0}a{text-decoration:none}}
h3{text-wrap:balance;font-size:12pt;margin:28px 0 12px}
pre{margin:16px 0 22px;padding:14px 16px;border:1px solid #ddd;background:#fafafa;overflow-x:auto;text-align:left;font-size:10pt;line-height:1.65;tab-size:4;break-inside:avoid}
pre code{font-family:Consolas,"Microsoft YaHei",monospace;white-space:pre}
.algorithm-label{text-indent:0;margin-top:24px;margin-bottom:8px;font-weight:600}
.result-table{min-width:0!important;font-size:10.5pt;line-height:1.55}
.result-table th,.result-table td{padding:9px 10px;white-space:nowrap}
.result-table thead th{text-align:center;vertical-align:bottom}
.result-table tbody th{border-bottom:0;font-weight:400}
.result-table .case-label,.result-table .scheme-label{text-align:left;vertical-align:middle}
.result-table .field-label{text-align:center;vertical-align:middle}
.result-table .case-label{font-weight:600}
.result-table .error-value{text-align:right;font-variant-numeric:tabular-nums}
.result-table strong{font-weight:700;color:#000}
.result-table sup{font-size:.7em;line-height:0;margin-left:2px}
.result-table .case-start:not(:first-child)>*{border-top:1px solid #999}
.result-table .pair-start>*{border-top:1px solid #e0e0e0}
.field-figure{margin:20px 0 32px}
.field-figure figcaption{margin-top:8px}
@media(max-width:650px){.result-table{font-size:9pt}.result-table th,.result-table td{padding:8px 6px}.field-figure{margin:20px -8px 28px}.field-figure figcaption{margin-left:8px;margin-right:8px}pre{font-size:9pt;padding:12px}}

'''
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 孤子数值解的误差比较</title><style>@@KATEX_CSS@@</style><style>'''+css+'''</style></head><body><main>'''+str(soup)+'''</main><script>@@KATEX_JS@@</script><script>renderMathInElement(document.querySelector("main"),{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});</script></body></html>'''
(HERE/'_src/index.src.html').write_text(page,encoding='utf-8')
(ROOT/'Workspaces/dlw_error_inventory_20260929/CONTROLLED_RESULTS.md').write_text(source.replace('href="Workspaces/','href="../'),encoding='utf-8')
print(f'Paper written: {len(formulas)} mathematical expressions, {len(soup.find_all("table"))} tables; typography from Report.src.html.')
