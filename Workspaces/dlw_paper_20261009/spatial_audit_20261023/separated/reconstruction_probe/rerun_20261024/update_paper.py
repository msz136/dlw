from pathlib import Path
import json,re,math,shutil,datetime,csv,subprocess
import markdown
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
THEORY=ROOT/'Workspaces/dlw_paper_20261009/integration_20261022/sections_2_3.md'
PAPER=ROOT/'dlw-paper.html'
BACK=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
BACK.mkdir(parents=True,exist_ok=True)
for p in [THEORY,PAPER]:shutil.copy2(p,BACK/p.name)
theory=THEORY.read_text(encoding='utf8')
theory=re.sub(r'### 3\.2 [\s\S]*?(?=### 3\.3)',lambda m:(HERE/'section_3_2.md').read_text(encoding='utf8')+'\n\n',theory)
theory=theory[:theory.index('### 3.4')]+(HERE/'section_3_4.md').read_text(encoding='utf8')
start=theory.index('### 3.3');end=theory.index('### 3.4');lax=theory[start:end]
for old,new in [(r'v_{k-1}-\delta_0u_{k-1}',r'w_{k-1}'),(r'v_k-\delta_0u_k',r'w_k'),(r'u_{k-1}',r'U_{k-1}'),(r'u_k',r'U_k')]:lax=lax.replace(old,new)
lax=lax.replace('with the physical fields defined in (32)–(33)','with U and w defined in (33)')
lax=lax.replace('the reconstruction identities (34)','the logarithmic identities following (33)')
lax=lax.replace('Combining it with the forward-shifted equation (48) and the preceding evolution equation recovers the first Centered-SD equation in (35).','Combining it with the forward-shifted equation (48) recovers (38). The full-potential reconstruction (34) then gives the first physical-field equation in (35); differentiating its reconstruction constraint gives the V equation. These coefficients are expressed through U and the auxiliary w. Their expression through U,V alone uses the selected inverse branch of that constraint.')
theory=theory[:start]+lax+theory[end:]
theory=theory.replace('For Centered-SD, we also derive explicit leading error coefficients for the second-order field approximation, providing an analytical basis for interpreting the numerical results that follow.','For Centered-SD, we match the exact Gram fields to the continuous solution and identify the shared initial U-derivative coefficient that will guide the spatial comparisons.')

S=json.loads((HERE/'baselines.json').read_text())+[json.loads(p.read_text()) for p in sorted(HERE.glob('spatial_*.json'))]
T=[json.loads((HERE/f'time_{c}_{a}.json').read_text()) for c in 'ABCD' for a in ['Euler','RK4','CN']]
assert len(S)==60 and len(T)==12 and all(r['status']=='complete' for r in S+T)
labels={'A':'A<br><small>One soliton<br>(1, 2)</small>','B':'B<br><small>One soliton<br>(4, −3)</small>','C':'C<br><small>Two solitons<br>(6, −5), (4, −3)</small>','D':'D<br><small>Two solitons<br>(1, 2), (4, −3)</small>'}
methods=['Endpoint-SD','Centered-SD','FD']
def num(x):
 a,b=f'{x:.3e}'.split('e');return f'{a} × 10<sup>{int(b)}</sup>'
def cell(v,best):return ' / '.join(('<strong>'+num(x)+'</strong>') if f'{x:.3e}'==f'{best[i]:.3e}' else num(x) for i,x in enumerate(v))
def table(axis,number):
 other='dx' if axis=='h' else 'h';symbol='h' if axis=='h' else 'Δx';fixed='Δx' if axis=='h' else 'h'
 s=f'<table class="paper-table"><caption>Table {number}. Complete initial derivative defects, u / v, as {symbol} varies at {fixed} = 0.1.</caption><thead><tr><th>Case</th><th>{symbol}</th>'+''.join('<th>'+m+'</th>' for m in methods)+'</tr></thead><tbody>'
 for c in 'ABCD':
  for i,val in enumerate([.1,.05,.025]):
   rr=[next(r for r in S if r['case']==c and r['method']==m and r[axis]==val and r[other]==.1) for m in methods]
   best=[min(r['total'][j] for r in rr) for j in [0,1]]
   s+='<tr>'+('<th rowspan="3" scope="rowgroup">'+labels[c]+'</th>' if i==0 else '')+'<td>'+str(val)+'</td>'+''.join('<td>'+cell(r['total'],best)+'</td>' for r in rr)+'</tr>'
 return s+'</tbody></table>'
oldexp=(HERE.parents[1]/'experiments.md').read_text(encoding='utf8')
cases=re.search(r'<table class="paper-table"><caption>Table 1\.[\s\S]*?</table>',oldexp)[0]
exp=r'''## 5. Numerical experiments

We use four exact soliton solutions to examine the spatial formulations and their subsequent time evolution. Section 5.1 specifies the waves and error measures. In Section 5.2, we evaluate the initial derivative defects while varying either h or the x resolution. Section 5.3 then compares three time integrators for the full-potential Centered-SD formulation.

### 5.1 Test problems and error measures

The continuous determinant solutions in Section 2.1 provide the reference fields. We set \(a=2\), \(\lambda=-2\) and \(\rho_i=1\), without phase shifts. Cases A and B are one-soliton solutions; C and D are two-soliton solutions. Case D combines the spectral pairs used separately in A and B.

'''+cases+r'''

The regions contain the principal wave profiles, with computational boundaries placed farther out. The y interval has the same half-width L as the x interval. We use u nodes \(y_k=-L+h/2+kh\). Both semi-discrete formulations place v at edge midpoints; Centered-SD reconstructs the internal edges. FD uses both fields at the u nodes. Errors are measured at native field locations within \(|x|\le R\), \(|y|<R\).

For the spatial comparisons, the physical initial fields are samples of the same continuous exact solution. Centered-SD determines its auxiliary initial values from the reconstruction constraint in Section 4.2. We compute the complete initial derivative defect
\[
r=F^{\mathrm{phys}}_{h,\Delta x}[q^*(0)]-q_t^*(0),\qquad q^*=(u^*,v^*),
\]
where the physical right-hand side includes the prescribed lower derivative, lattice summation and, for Centered-SD, auxiliary inversion and the chain rule for v. The reference time derivatives are evaluated analytically from the tau functions. The initial field errors are zero; r measures the difference between their numerical and exact time derivatives.

Both refinement tables report \(\|r_u\|_\infty/\|r_v\|_\infty\) with the complete Fourier operators and numerical primitive retained. Thus the scans show the response to h and x refinement, respectively, without treating the second table as an isolated x-error contribution. Bold values mark the smallest component at the displayed precision, including ties.

For the time study, we measure \(E_u(T)=\max|u^{\mathrm{num}}(T)-u^*(T)|\) and \(E_v(T)=\max|v^{\mathrm{num}}(T)-v^*(T)|\) on the same region. The reference remains the continuous solution throughout.

### 5.2 Comparison of spatial formulations

We first vary \(h=0.1,0.05,0.025\) at fixed \(\Delta x=0.1\), without advancing in time. Table 2 places the three formulations side by side for each wave and spacing.

'''+table('h',2)+r'''

The full-potential reconstruction gives Centered-SD the same initial u defect as Endpoint-SD to the numerical precision of the calculation. This agreement follows from their identical first equation and common boundary derivative: both obtain \(u_t\) by midpoint summation of \(v_{xx}\). Their analytic-x leading coefficient is therefore \([v_{xxy}]_{y_0}^{y}/24\), as derived in Section 3.4. In A, C and D, halving h reduces this component by approximately four. In B, the decrease levels off on the finest lattice, where the common finite-interval x approximation is no longer negligible.

The second field separates the two semi-discrete formulations. Centered-SD gives an approximately fourfold reduction of its v defect whenever h is halved, whereas Endpoint-SD gives an approximately twofold reduction. Centered-SD also has a smaller v defect than FD in A and D, while FD remains more accurate in B and C. The reconstruction therefore combines the shared first-equation behaviour with second-order refinement of the second field; its v coefficient still depends on the wave profile.

We next keep \(h=0.1\) and vary \(\Delta x=0.1,0.05,0.025\). Table 3 reports the complete derivative defects under this second scan.

'''+table('dx',3)+r'''

The defects change little over these x resolutions, in contrast to their response to lattice refinement. Since h remains fixed, the table retains the y approximation error. Refining x therefore does not produce a corresponding fourfold reduction of the complete defect. Small changes also reflect the sampling of its maximum on different x grids. These results support treating h refinement and x resolution separately when assessing the physical-field approximation.

### 5.3 Comparison of time integrators

We now advance the full-potential Centered-SD formulation to \(T=0.01\), using \(h=\Delta x=0.1\) and \(\Delta t=10^{-4}\) for all four waves. Euler, RK4 and Crank–Nicolson advance the same u,w initial state and recover v through the same map. Table 4 gives the final physical-field errors.

'''
exp+='<table class="paper-table"><caption>Table 4. Final u / v field errors for full-potential Centered-SD at T = 0.01.</caption><thead><tr><th>Case</th><th>Euler</th><th>RK4</th><th>Crank–Nicolson</th></tr></thead><tbody>'
for c in 'ABCD':
 rr=[r for r in T if r['case']==c];best=[min(r['error'][j] for r in rr) for j in [0,1]]
 exp+='<tr><th scope="row">'+labels[c]+'</th>'+''.join('<td>'+cell(r['error'],best)+'</td>' for r in rr)+'</tr>'
exp+='</tbody></table>\n\n'
exp+=r'''In A, RK4 and Crank–Nicolson give closely matched final errors, while Euler has slightly smaller maxima. Case B shows a much stronger dependence on the integrator: its u error is approximately 0.075 with Euler, 0.163 with RK4 and 0.167 with Crank–Nicolson. The improved initial u defect has therefore not removed the large final discrepancy in this case. The first-equation coefficient explains the initial spatial comparison, but does not by itself determine the subsequent error growth.

'''
for c in 'CD':
 rr=[r for r in T if r['case']==c]
 winners=[min(rr,key=lambda r:r['error'][j])['method'].replace('CN','Crank–Nicolson') for j in [0,1]]
 exp+=f"In {c}, {winners[0]} gives the smallest u error and {winners[1]} the smallest v error. "
exp+=r'''

These fixed-step results measure the combined spatial and temporal error in the physical fields. A smaller Euler error at a particular final time is not a measurement of temporal order. All Crank–Nicolson runs reached the final time with the prescribed implicit residual tolerance. The comparison also specifies the evolved variables, since applying a time integrator to u,w and then reconstructing v is generally different from applying it directly to u,v.
'''
(HERE/'experiments.md').write_text(exp,encoding='utf8')
(HERE/'spatial.json').write_text(json.dumps(S,indent=2))
(HERE/'temporal.json').write_text(json.dumps(T,indent=2))
for name,rows,header,get in [('spatial',S,['case','method','dx','h','defect_u','defect_v'],lambda r:[r['case'],r['method'],r['dx'],r['h'],*r['total']]),('temporal',T,['case','method','dx','h','dt','T','error_u','error_v'],lambda r:[r['case'],r['method'],r['dx'],r['h'],r['dt'],r['T'],*r['error']])]:
 with (HERE/f'{name}.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(get(r) for r in rows)

source=theory+'\n\n'+(HERE/'methods.md').read_text(encoding='utf8')+'\n\n'+exp
formulas=[]
def protect(m):
 s=m[0];formulas.append(dict(tex=s[2:-2],display=s.startswith('\\[')));return f'MATHPLACEHOLDER{len(formulas)-1}END'
protected=re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,source)
js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formulas),text=True,encoding='utf8',capture_output=True,check=True)
rendered=json.loads(out.stdout);sections={};intros={};titles={}
parts=re.split(r'(?m)^(## |### )',protected)
for i in range(1,len(parts),2):
 title,body=parts[i+1].split('\n',1);n=title.split()[0].rstrip('.');titles[n]=title
 html=markdown.markdown(body,extensions=['tables'])
 for j,r in enumerate(rendered):
  token=f'MATHPLACEHOLDER{j}END';tag=re.search(r'\\tag\{(\d+)\}',formulas[j]['tex']);attr=f' id="eq-{tag[1]}"' if tag else ''
  html=html.replace('<p>'+token+'</p>',f'<div class="equation"{attr}>'+r+'</div>' if formulas[j]['display'] else '<p>'+r+'</p>').replace(token,r)
 if parts[i]=='## ':intros[n]=html
 else:sections[n]=f'<section id="section-{n}"><h3>{title}</h3>'+html+'</section>'
text=PAPER.read_text(encoding='utf8')
for n,html in sections.items():
 text,count=re.subn(r'<section id="section-'+re.escape(n)+r'">[\s\S]*?</section>',lambda m:html,text,count=1);assert count==1,n
for n,html in intros.items():
 text,count=re.subn(r'(<section id="section-'+n+r'"><h2>[^<]*</h2>)[\s\S]*?(?=<section id="section-'+n+r'\.)',lambda m:m[1]+html,text,count=1);assert count==1,n
# Editorial status is separate from manuscript prose.
text=re.sub(r'(<section class="guide" id="appendix-G"[\s\S]*?<p class="status">)[\s\S]*?</p>',lambda m:m[1]+'2026-10-24：已更新完整势Centered-SD重构、Lax变量、连续极限与匹配Gram场二阶说明，以及4.1–4.2和5.1–5.3。新实验为60组完整初始缺陷与12组时间推进。旧解析x误差分解及旧表示数据保留在项目归档；4.3–4.4、5.4–5.5及其余占位章节待续。</p>',text,count=1)
text=text.replace('2026-10-23已补充四孤子的初始空间缺陷与时间算法比较；Section 4.3–4.4及5.4–5.5仍待处理。','2026-10-24已更新完整势Centered-SD与四孤子的空间、时间实验；Section 4.3–4.4及5.4–5.5仍待处理。')
for old,new in [
 ('直接用 u、v 定义交错物理场；对照3.1展开同点和跨点关系，取格点差消去辅助对数项。不设独立势表示小节。','保留对称双线性系统，沿同点/跨点展开定义完整势及边场V；明确非局部原函数、辅助w约束和逆分支。'),
 ('方程相容性已写入；下一步匹配精确解族，再写物理场收敛及首项系数。','已写入光滑分支上的方程相容性、匹配Gram场二阶逼近，以及共同初值下U时间导数的首项系数。'),
 ('本轮采用四组孤子。空间部分在t=0分离解析x下的y缺陷与Fourier x附加缺陷；时间部分固定Centered-SD比较Euler/RK4/C–N。Gaussian和正弦初值暂缓。','本轮采用四组孤子；t=0分别扫描h和Δx，表内均为完整初始导数缺陷。旧解析x分解保留为历史对照。时间推进U,w并重构V，比较Euler/RK4/C–N。Gaussian和正弦暂缓。'),
 ('同一 Fourier x 微分及时间推进下，正式比较','同一 Fourier x 微分下，在t=0比较'),
 ('Centered-SD 正文统一采用 u、v 物理场表示。','Centered-SD采用完整势定义的U,V物理场；数值推进U,w，再由固定映射恢复V。'),
 ('时间法比较以两种半离散方法为对象；保留 C–N 的前提是隐式求解已核验。','本轮时间法比较采用完整势Centered-SD；C–N隐式残差已核验。')]:text=text.replace(old,new)
soup=BeautifulSoup(text,'html.parser');ids=[e['id'] for e in soup.select('[id]')]
assert len(ids)==len(set(ids)) and 'MATHPLACEHOLDER' not in text and 'katex-error' not in text
assert all(a['href'][1:] in ids for a in soup.select('a[href^="#"]'))
tags=[int(n) for n in re.findall(r'\\tag\{(\d+)\}',theory)];assert tags==list(range(1,54)),tags
THEORY.write_text(theory,encoding='utf8');PAPER.write_text(text,encoding='utf8')
head=text[text.index('<head>')+6:text.index('</head>')].replace('href="Workspaces/','href="../Workspaces/')
report=ROOT/'report/dlw_full_potential_experiments_20261024.html'
report.write_text('<!doctype html><html lang="en"><head>'+head+'</head><body><article><h1>Full-potential Centered-SD: numerical experiments</h1>'+intros['5']+''.join(sections[n] for n in ['5.1','5.2','5.3'])+'</article></body></html>',encoding='utf8')
new=[r for r in S if r['method']=='Centered-SD']
comparison=max(abs(r['total'][0]-next(e for e in S if e['case']==r['case'] and e['dx']==r['dx'] and e['h']==r['h'] and e['method']=='Endpoint-SD')['total'][0]) for r in new)
validation=dict(spatial_records=len(S),time_records=len(T),endpoint_u_max_difference=comparison,max_map_residual=max(r['checks']['map_residual'] for r in new),max_first_equation_identity=max(r['checks']['first_equation_identity'] for r in new),max_chain_rule_difference=max(r['checks']['chain_rule_difference'] for r in new),max_cn_residual=max(r['cn_max_residual'] for r in T),formulas=len(formulas),numbered_equations=len(tags),backup=str(BACK),paper=str(PAPER),report=str(report))
(HERE/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2))
