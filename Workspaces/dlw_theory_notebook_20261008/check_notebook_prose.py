from pathlib import Path
import json,re,subprocess
import nbformat,mistune
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
n=nbformat.read(ROOT/'notebook/DLW理论.ipynb',as_version=4)
maths=[]
def store(m):
    display=m[0].startswith('$$')
    maths.append({'tex':m[0][2:-2] if display else m[0][1:-1],'display':display})
    return 'FORMULAPLACEHOLDER'+str(len(maths)-1)+'END'
sections=[]
for c in n.cells:
    if c.cell_type!='markdown':continue
    source=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',store,c.source)
    rendered=mistune.html(source)
    soup=BeautifulSoup(rendered,'html.parser')
    for x in soup.select('code'):x.decompose()
    assert '**' not in soup.get_text(),c.id
    sections.append('<section id="'+c.id+'">'+rendered+'</section>')
(HERE/'notebook_math.json').write_text(json.dumps(maths,ensure_ascii=False),encoding='utf-8')
subprocess.run(['node',str(HERE/'notebook_render.cjs')],check=True)
rendered=json.loads((HERE/'notebook_math_rendered.json').read_text(encoding='utf-8'))
body=re.sub(r'FORMULAPLACEHOLDER(\d+)END',lambda m:rendered[int(m[1])],'\n'.join(sections))
css=(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.css').as_uri()
(HERE/'notebook_prose_preview.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><link rel="stylesheet" href="'+css+'"><style>body{margin:0;background:white;color:#222;font:16px/1.75 "Microsoft YaHei",sans-serif}main{max-width:1060px;margin:auto;padding:30px}h2{margin-top:35px}.eq{overflow:auto;padding:8px}p{margin:12px 0}.katex{font-size:1.08em}table{border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #ccc}</style><main>'+body+'</main></html>',encoding='utf-8')
record=json.loads((HERE/'notebook_prose_validation.json').read_text(encoding='utf-8'))
record.update(commonmark_bold_markers='No literal ** remains in rendered prose',latex_formulas_checked=len(maths))
(HERE/'notebook_prose_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('CommonMark rendering and',len(maths),'LaTeX formulas passed')
