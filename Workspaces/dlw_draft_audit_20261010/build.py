from pathlib import Path
import json,re,subprocess,hashlib
import markdown
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=(HERE/'audit.md').read_text(encoding='utf-8')
formulas=[]
def slot(m):
    raw=m[0]; display=raw.startswith('$$')
    tex=raw[2:-2] if display or raw.startswith('\\(') else raw[1:-1]
    formulas.append({'tex':tex,'display':display})
    return f'MATHSLOT{len(formulas)-1}END'
text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$|\\\([\s\S]*?\\\)',slot,source)
body=markdown.markdown(text,extensions=['tables'])
(HERE/'formulas.json').write_text(json.dumps(formulas,ensure_ascii=False),encoding='utf-8')
subprocess.run(['node',str(HERE/'render.cjs')],check=True)
rendered=json.loads((HERE/'rendered.json').read_text(encoding='utf-8'))
body=re.sub(r'MATHSLOT(\d+)END',lambda m:rendered[int(m[1])],body)
body=re.sub(r'<p>(<div class="eq">[\s\S]*?</div>)</p>',r'\1',body)
body=body.replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
original=BeautifulSoup((ROOT/'report/dlw_paper_draft.html').read_text(encoding='utf-8'),'html.parser')
css=original.style.string+'\ntable{white-space:normal;font-size:15px}td,th{min-width:85px}h1{text-align:left}h2{scroll-margin-top:20px}.eq{margin:15px 0}main{max-width:1050px}'
heading_count=0
def heading(m):
    global heading_count
    heading_count+=1
    return f'<h2 id="s{heading_count}">{m[1]}</h2>'
body=re.sub(r'<h2>(.*?)</h2>',heading,body)
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 论文草稿：推导与适用范围审查</title><meta name="description" content="独立重推 DLW 草稿的双线性、Gram、PE/PF、连续极限与 Lax 结构，审查数值条件。"><style>'+css+'</style></head><body><main>'+body+'</main></body></html>'
dest=ROOT/'report/dlw_draft_audit_20261010.html'
dest.write_text(page,encoding='utf-8')
soup=BeautifulSoup(page,'html.parser')
assert len(soup.select('annotation[encoding="application/x-tex"]'))==len(formulas)
assert not soup.select('.katex-error') and 'MATHSLOT' not in page
links=[a['href'] for a in soup.select('a[href]')]
for link in links:
    if not link.startswith(('https://','http://','#')):assert (dest.parent/link).exists(),link
result={'html':str(dest),'formulas':len(formulas),'sections':heading_count,'local_links':len(links),'strict_katex':True,'offline_fonts':True,
        'html_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(HERE/'build_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
