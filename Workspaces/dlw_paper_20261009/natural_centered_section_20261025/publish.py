from pathlib import Path
import re,json,subprocess,hashlib
import markdown
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
paper=ROOT/'dlw-paper.html'
theory=ROOT/'Workspaces/dlw_paper_20261009/integration_20261022/sections_2_3.md'
section_source=ROOT/'Workspaces/dlw_paper_20261009/spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024/section_3_2.md'
src=(HERE/'section_3_2.md').read_text(encoding='utf-8')
formulas=[]
def protect(m):
    formulas.append(dict(tex=m[0][2:-2],display=m[0].startswith('\\[')))
    return f'MATHSLOT{len(formulas)-1}END'
protected=re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,src)
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
rendered=json.loads(subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formulas),text=True,encoding='utf-8',capture_output=True,check=True).stdout)
html=markdown.markdown(protected)
for i,value in enumerate(rendered):
    token=f'MATHSLOT{i}END';tag=re.search(r'\\tag\{(\d+)\}',formulas[i]['tex'])
    attr=f' id="eq-{tag[1]}"' if tag else ''
    if formulas[i]['display']:html=html.replace('<p>'+token+'</p>',f'<div class="equation"{attr}>{value}</div>')
    html=html.replace(token,value)
section='<section id="section-3.2">'+html+'</section>'
old=paper.read_text(encoding='utf-8')
pattern=r'<section id="section-3\.2">[\s\S]*?</section>'
new,n=re.subn(pattern,lambda m:section,old,count=1);assert n==1
assert re.sub(pattern,'SECTION',old,count=1)==re.sub(pattern,'SECTION',new,count=1)
s=BeautifulSoup(new,'html.parser');ids=[e['id'] for e in s.select('[id]')]
assert len(ids)==len(set(ids)) and 'MATHSLOT' not in new and 'katex-error' not in new
assert all(a['href'][1:] in ids for a in s.select('a[href^="#"]'))
assert re.findall(r'\\tag\{(\d+)\}',src)==[str(i) for i in range(32,40)]
t=theory.read_text(encoding='utf-8');t,n=re.subn(r'### 3\.2 [\s\S]*?(?=### 3\.3)',lambda m:src+'\n\n',t,count=1);assert n==1
paper.write_text(new,encoding='utf-8');theory.write_text(t,encoding='utf-8');section_source.write_text(src,encoding='utf-8')
result=dict(section='3.2',formulas=len(formulas),equation_numbers=list(range(32,40)),outside_section_unchanged=True,links_valid=True,duplicate_ids=False,proposition_evolution_equations=2,auxiliary='omega=(R-r)_x without normalization',paper_sha256=hashlib.sha256(paper.read_bytes()).hexdigest(),scope='Only nonlinearization section replaced; downstream full-potential Lax/consistency/numerical text still requires separate synchronization')
(HERE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
