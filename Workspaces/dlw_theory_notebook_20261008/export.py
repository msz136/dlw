"""Create an offline reading copy and check every displayed formula with KaTeX."""
from pathlib import Path
import json,re,html,subprocess,sys,base64
import nbformat,markdown
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=(HERE/'paper.src.md').read_text(encoding='utf-8')
formula=[]
def mathstore(match):
    display=match.group().startswith('$$')
    tex=match.group()[2:-2] if display else match.group()[1:-1]
    index=len(formula)
    formula.append({'tex':tex,'display':display})
    return f'MATHPLACEHOLDER{index}END'
text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',mathstore,source)
parts=[markdown.markdown(text,extensions=['tables'])]
(HERE/'formulas.json').write_text(json.dumps(formula,ensure_ascii=False),encoding='utf-8')
subprocess.run(['node',str(HERE/'render_math.cjs')],check=True)
rendered=json.loads((HERE/'rendered_math.json').read_text(encoding='utf-8'))
body='\n'.join(parts)
body=re.sub(r'MATHPLACEHOLDER(\d+)END',lambda m:rendered[int(m[1])],body)
assets=ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist'
kcss=(assets/'katex.css').read_text(encoding='utf-8')
kcss=re.sub(r'src: (url\([^)]*\.woff2\) format\("woff2"\))[^;]*;',r'src: \1;',kcss)
kcss=re.sub(r'url\(([^)]+)\)',lambda m:'url(data:font/woff2;base64,'+base64.b64encode((assets/m[1]).read_bytes()).decode()+')',kcss)
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
font=TTFont('C:/Windows/Fonts/NotoSerifSC-VF.ttf')
font=instantiateVariableFont(font,{'wght':400},inplace=True)
options=subset.Options()
sub=subset.Subsetter(options=options)
sub.populate(text=source)
sub.subset(font)
font.flavor='woff'
font.save(HERE/'paper-serif.woff')
fontcss="@font-face{font-family:PaperSerif;src:url(data:font/woff;base64,"+base64.b64encode((HERE/'paper-serif.woff').read_bytes()).decode()+") format('woff');font-weight:400;font-style:normal;font-display:block}"
css=kcss+fontcss+"""
*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#000}
body{font-family:KaTeX_Main,PaperSerif,serif;font-size:16px;line-height:1.85;font-weight:400}
main{width:100%;max-width:960px;margin:0 auto;padding:60px 48px 88px}
h1{font-family:PaperSerif,serif;font-size:25px;line-height:1.6;font-weight:600;text-align:center;margin:0 0 28px;letter-spacing:.04em}
h2{font-size:19px;line-height:1.6;margin:30px 0 13px;font-weight:600}
h3{font-size:16px;margin:22px 0 10px;font-weight:600}
p{margin:10px 0;text-align:justify;overflow-wrap:break-word}
.abstract{font-size:14px;line-height:1.8;margin:0 32px 28px;text-align:justify}
.abstract-label{font-weight:600;margin-right:1em}
strong{font-weight:600}.eq{display:block;overflow-x:auto;overflow-y:hidden;padding:8px 1px;margin:4px 0}
.katex{font-size:1.04em}.katex-display{margin:.65em 0}.katex-display>.katex{white-space:nowrap}
@media(max-width:650px){main{padding:28px 18px 50px}body{font-size:15px}h1{font-size:21px}.abstract{margin:0 4px 24px}h2{font-size:18px}}
@page{size:A4;margin:20mm 18mm}
@media print{body{font-size:10.5pt;line-height:1.7}main{max-width:none;padding:0 3px}h1{font-size:16pt}h2{font-size:12pt;break-after:avoid}.eq{overflow:visible;break-inside:avoid}p{orphans:3;widows:3}.abstract{font-size:9.5pt}}
"""
dest=HERE/'preview.html' if '--input' in sys.argv else ROOT/'report/dlw_theory.html'
dest.write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 方程的半离散化、τ 函数与连续极限</title><style>'+css+'</style><main>'+body+'</main></html>',encoding='utf-8')
print('Offline HTML:',dest,'formulas:',len(formula))
