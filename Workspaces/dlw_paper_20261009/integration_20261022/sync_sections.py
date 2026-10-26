"""Render the reviewed English sections with local, static KaTeX."""
from pathlib import Path
import datetime, json, re, subprocess, shutil
import markdown
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
TARGET=ROOT/'dlw-paper.html'
text=TARGET.read_text(encoding='utf-8')
backup=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup.mkdir(parents=True,exist_ok=True)
shutil.copy2(TARGET,backup/TARGET.name)
source=(HERE/'sections_2_3.md').read_text(encoding='utf-8')
formulas=[]
def protect(m):
    value=m.group(0)
    formulas.append({'tex':value[2:-2], 'display':value.startswith('\\[')})
    return 'MATHPLACEHOLDER'+str(len(formulas)-1)+'END'
protected=re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,source)
js="""const fs=require('fs');const k=require(process.argv[1]);
const input=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(input.map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error',output:'htmlAndMathml'}))));"""
result=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formulas),text=True,encoding='utf-8',capture_output=True,check=True)
rendered=json.loads(result.stdout)
parts=re.split(r'(?m)^(## |### )',protected)
out=[]; major=False; minor=False; headings=[]
for i in range(1,len(parts),2):
    level=parts[i]; title,body=parts[i+1].split('\n',1)
    number=title.split()[0].rstrip('.')
    if level=='## ':
        if minor: out.append('</section>'); minor=False
        if major: out.append('</section>')
        major=True
        out.append(f'<section id="section-{number}"><h2>{title}</h2>')
    else:
        if minor: out.append('</section>')
        minor=True
        out.append(f'<section id="section-{number}"><h3>{title}</h3>')
        headings.append((number,title))
    out.append(markdown.markdown(body))
if minor: out.append('</section>')
if major: out.append('</section>')
content='\n'.join(out)
for i,r in enumerate(rendered):
    token=f'MATHPLACEHOLDER{i}END'
    if formulas[i]['display']:
        tag=re.search(r'\\tag\{(\d+)\}',formulas[i]['tex'])
        attr=f' id="eq-{tag[1]}"' if tag else ''
        content=content.replace('<p>'+token+'</p>',f'<div class="equation"{attr}>{r}</div>')
    content=content.replace(token,r)
start=text.index('<section id="section-2">')
end=text.index('<section id="section-4">')
text=text[:start]+content+'\n'+text[end:]
text=re.sub(r'\bESD\b','Endpoint-SD',text)
text=re.sub(r'\bCSD\b','Centered-SD',text)
text=text.replace('Main text is a manuscript skeleton, not a completed proof.','Sections 2 and 3 contain the reviewed working draft; later sections remain planned.')
text=text.replace('当前仅建立章节骨架。以下是编写计划，不代表新的推导已经完成或证明已经通过核验。','已同步第2节与第3节工作稿，3.4目前写至非线性方程相容性；精确解族匹配与物理场误差首项待续。其余章节仍为计划，数学内容保留工作稿状态。')
text=text.replace('再导出两种闭合表示、可积结构和连续极限','再导出两类格点的物理场方程、可积结构和连续极限')
guide_start=text.index('<h3>3. 非线性表示与可积结构</h3>')
guide_end=text.index('<h3>4. 数值实现与线性稳定性</h3>',guide_start)
text=text[:guide_start]+'''<h3>3. 非线性表示与可积结构</h3>
<p><strong>3.1 Endpoint-SD</strong><br>端点物理场 U、V、同点与跨点推导以及格点差消元。</p>
<p><strong>3.2 Centered-SD</strong><br>直接用 u、v 定义交错物理场；对照3.1展开同点和跨点关系，取格点差消去辅助对数项。不设独立势表示小节。</p>
<p><strong>3.3 Darboux–Lax representations</strong><br>共同算子形式、两类物理场系数及相容性推导。</p>
<p><strong>3.4 Continuous limit and approximation of the physical fields</strong><br>方程相容性已写入；下一步匹配精确解族，再写物理场收敛及首项系数。</p>
'''+text[guide_end:]
text=text.replace('令 b=a+h/2、F_j=f_(j+1)、G_j=g_j，精确得到 B_(a−h/2)F_j·G_j=0、B_(a+h/2)F_j·G_(j+1)=0','令 b=a+h/2，保持 f_k、g_k 记号，得到对称参数配对；g_k 在 kh，f_k 在 (k−1/2)h')
text=text.replace('PF 非周期势的处理只在需要其辅助数值验证时讨论。','')
text=text.replace('（中心型半离散化，数值采用其 PE 表示）','（中心型半离散化）')
text=text.replace('Centered-SD 的 PE 表示','Centered-SD')
text=text.replace('Endpoint-SD/Centered-SD、Centered-SD 的 PE/PF 转换的详细代数','Endpoint-SD/Centered-SD 物理场转换的详细代数')
text=text.replace('PE/PF 分别表示 Centered-SD 的消势/势变量形式；数值表中的 Centered-SD 默认采用 PE 表示。','Centered-SD 正文统一采用 u、v 物理场表示。')
text=text.replace('PF 保留为理论辅助表示。','')
text=text.replace('推导物理场关系和 PE/PF，明确正向、逆向及边界条件。','推导物理场关系，明确正向重构及边界条件。')
text=text.replace('本轮先规划，不启动新一轮 FFT 数值实验。','本轮同步已讨论的理论工作稿，尚未启动新一轮 FFT 数值实验。')
refs='''<section id="references"><h2>References</h2><ol>
<li>Sheng and Yu (2022). Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. <em>Physica D</em> 432, 133140. <a href="https://doi.org/10.1016/j.physd.2021.133140">doi:10.1016/j.physd.2021.133140</a>.</li>
<li>Feng et al. (2024). Integrable Semi-Discretization for a Modified Camassa–Holm Equation with Cubic Nonlinearity. <em>SIGMA</em> 20, 091. <a href="https://doi.org/10.3842/SIGMA.2024.091">doi:10.3842/SIGMA.2024.091</a>.</li>
</ol><!-- Bibliographic details and additional references remain to be consolidated. --></section>'''
text=re.sub(r'<section id="references">[\s\S]*?</section>',lambda m:refs,text)
if 'katex.min.css' not in text:
    text=text.replace('</head>','<link rel="stylesheet" href="Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>.equation{overflow-x:auto;padding:8px 2px}.katex{font-size:1.02em}.katex-display{margin:.65em 0}nav .subsection{padding-left:20px;font-size:15px}section{scroll-margin-top:20px}@media print{.equation{overflow:visible}.katex{font-size:.92em}}</style></head>')
for major_num in ('2','3'):
    nav_link=re.search(r'<a href="#section-'+major_num+r'">[^<]*</a>',text)
    if nav_link:
        links=''.join(f'<a class="subsection" href="#section-{n}">{title}</a>' for n,title in headings if n.startswith(major_num+'.'))
        text=text[:nav_link.end()]+links+text[nav_link.end():]
tags=[int(x) for x in re.findall(r'\\tag\{(\d+)\}',source)]
assert tags==list(range(1,54)),tags
assert not re.search(r'\b(?:ESD|CSD|PF)\b',text)
assert 'MATHPLACEHOLDER' not in text
soup=BeautifulSoup(text,'html.parser')
ids=[e['id'] for e in soup.select('[id]')]
assert len(ids)==len(set(ids))
assert all(a['href'][1:] in ids for a in soup.select('a[href^="#"]'))
TARGET.write_text(text,encoding='utf-8')
(HERE/'sync_validation.json').write_text(json.dumps({'formulas':len(formulas),'numbered_equations':len(tags),'sections':headings,'backup':str(backup),'math_rendering':'static KaTeX, strict error checking','duplicate_ids':False,'broken_internal_links':False},indent=2),encoding='utf-8')
print(json.dumps({'formulas':len(formulas),'numbered_equations':len(tags),'output':str(TARGET)},ensure_ascii=False))
