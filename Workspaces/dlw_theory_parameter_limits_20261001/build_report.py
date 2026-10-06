"""Build the standalone paper from this topic's source and shared read-only assets."""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
import markdown
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=HERE/'REPORT.md'
ASSETS=ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist'
source=SOURCE.read_text(encoding='utf-8')
formulas=[]
eq_count=0
def protect(match):
    global eq_count
    value=match[0]; display=value.startswith('$$')
    if display:
        eq_count+=1
        value=value[:-2].rstrip()+rf'\tag{{{eq_count}}}'+'\n$$'
    formulas.append({'text':value,'display':display})
    return f'MATHPLACEHOLDER{len(formulas)-1}END'
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,source)
assert '$' not in protected
body=markdown.markdown(protected,extensions=['tables'])
for i,item in enumerate(formulas):
    body=body.replace(f'MATHPLACEHOLDER{i}END',html.escape(item['text'],quote=False))
soup=BeautifulSoup(body,'html.parser')
soup.find('h1').find_next_sibling('p')['class']=['date']
for p in soup.find_all('p'):
    if p.get_text().startswith('摘要。'):
        p['class']=['abstract']
    if p.get_text().strip().startswith('$$'):
        p['class']=['equation']
toc=[]
for i,h in enumerate(soup.find_all('h2'),1):
    h['id']=f'section-{i}'
    toc.append(f'<li><a href="#section-{i}">{html.escape(h.get_text())}</a></li>')
soup.find('h2').insert_before(BeautifulSoup('<nav aria-label="文章目录"><ol>'+''.join(toc)+'</ol></nav>','html.parser'))
for i,t in enumerate(soup.find_all('table'),1):
    wrap=soup.new_tag('div',attrs={'class':'table-wrap','tabindex':'0','role':'region','aria-label':f'表{i}，可横向滚动'})
    t.wrap(wrap)
    for th in t.find_all('th'):
        th['scope']='col'
for a in soup.find_all('a',href=True):
    href=a['href']
    if href.startswith('#') or re.match(r'^https?://',href):
        continue
    target=(SOURCE.parent/href).resolve()
    assert target.is_file(),target
    a['href']=target.relative_to(ROOT).as_posix()
css=(ASSETS/'katex.min.css').read_text(encoding='utf-8')
font_count=0
def font_embed(match):
    global font_count
    path=ASSETS/'fonts'/match[1]
    assert path.is_file(),path
    font_count+=1
    mime={'.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf'}[path.suffix]
    return 'url(data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+')'
css=re.sub(r'url\(["\']?fonts/([A-Za-z0-9_.\-]+)["\']?\)',font_embed,css)
js=(ASSETS/'katex.min.js').read_text(encoding='utf-8')+'\n'+(ASSETS/'contrib/auto-render.min.js').read_text(encoding='utf-8')
style='''
*{box-sizing:border-box}body{margin:0;background:#f1f0ed;color:#191919;font:17px/1.95 "Times New Roman","SimSun",serif}
main{max-width:1020px;margin:30px auto;padding:56px 70px 68px;background:#fff}h1{font-size:28px;line-height:1.5;text-align:center;margin:0 0 10px}
.date{text-align:center;color:#666;font-size:14px}.abstract{border-block:1px solid #888;padding:17px 0;font-size:16px}
h2{font-size:22px;line-height:1.6;margin:39px 0 15px;break-after:avoid}p{margin:12px 0;text-align:justify;overflow-wrap:break-word}
a{color:#254e68;text-underline-offset:3px}a:focus-visible,.table-wrap:focus-visible{outline:2px solid #254e68;outline-offset:4px}
nav{font-size:14px;border-bottom:1px solid #ccc;margin:22px 0 28px;padding-bottom:13px}nav ol{list-style:none;padding:0;columns:2;column-gap:30px}nav li{break-inside:avoid;margin:4px 0}
.equation{margin:17px 0}.katex{font-size:1.02em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:10px 3px;font-size:.94em;margin:.5em 0}
.katex-display>.katex>.katex-html{display:flex;align-items:center;width:max-content;min-width:100%}.formula-body{display:inline-block;margin-inline:auto}.katex-display .katex-tag{position:static;flex:none;margin-left:2em}
.table-wrap{overflow-x:auto;margin:22px 0}table{border-collapse:collapse;width:100%;min-width:580px;font-size:15px;line-height:1.8;border-block:1.3px solid #444}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #ddd}th{border-bottom:1px solid #777}tr:last-child td{border:0}
ol{font-size:14px;line-height:1.85;padding-left:25px}li{margin:6px 0}
@media(max-width:700px){body{background:#fff;font-size:16px;line-height:1.85}main{margin:0;padding:28px 19px 40px}h1{font-size:24px}h2{font-size:20px}.abstract{font-size:15px}nav ol{columns:1}.katex-display{font-size:.83em}}
@media print{@page{size:A4;margin:19mm}body{background:white;font-size:10.5pt}main{margin:0;padding:0;max-width:none}h1{font-size:18pt}h2{font-size:13pt}nav{display:none}.date,ol{font-size:9pt}.abstract{font-size:10pt}table{min-width:0;font-size:9pt}.table-wrap{overflow:visible}.katex-display{font-size:.85em}a{color:inherit;text-decoration:none}}
'''
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="DLW两结构参数的最佳谱校准、有限步长余项、物理质量见证与共同初值短时限制。"><title>DLW：两个结构参数的谱范围限制</title>
<style>'''+css+'</style><style>'+style+'</style></head><body><main>'+str(soup)+'</main><script>'+js+'''</script><script>
renderMathInElement(document.querySelector('main'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,strict:'ignore'});
document.querySelectorAll('.katex-display>.katex>.katex-html').forEach(c=>{const t=c.querySelector(':scope>.katex-tag');if(!t)return;const b=document.createElement('span');b.className='formula-body';Array.from(c.childNodes).filter(n=>n!==t).forEach(n=>b.appendChild(n));c.prepend(b)});
document.documentElement.dataset.mathReady='true';</script></body></html>'''
page=page.replace('href="Workspaces/', 'href="../../Workspaces/')
(HERE/'report.html').write_text(page,encoding='utf-8')
(HERE/'report_source.html').write_text(str(soup),encoding='utf-8')
manifest={'title':'DLW：两个结构参数的谱范围限制','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'html_sha256':hashlib.sha256(page.encode()).hexdigest(),'equation_count':eq_count,'math_count':len(formulas),'section_count':len(toc),'font_count':font_count,'formulas':formulas,'new_pde_runs':0}
(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['equation_count','math_count','section_count','font_count']}))
