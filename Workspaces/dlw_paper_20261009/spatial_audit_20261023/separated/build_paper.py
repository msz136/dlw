from pathlib import Path
import json, re, csv, math, datetime, shutil, subprocess
import markdown
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
METHODS=['Endpoint-SD','Centered-SD','FD']
CASELABELS={'A':'A<br><small>One soliton<br>(1, 2)</small>','B':'B<br><small>One soliton<br>(4, −3)</small>','C':'C<br><small>Two solitons<br>(6, −5), (4, −3)</small>','D':'D<br><small>Two solitons<br>(1, 2), (4, −3)</small>'}
S=json.loads((HERE/'spatial.json').read_text())

def num(x):
    a,b=f'{x:.3e}'.split('e');return f'{a} × 10<sup>{int(b)}</sup>'

def pair(v,mins=None):
    return ' / '.join(('<strong>'+num(x)+'</strong>') if mins is not None and x==mins[i] else num(x) for i,x in enumerate(v))

def table_spatial(key,axis,number,caption):
    other='dx' if axis=='h' else 'h'
    s=f'<table class="paper-table"><caption>Table {number}. {caption} Each entry gives the u / v component.</caption><thead><tr><th>Case</th><th>'+('h' if axis=='h' else 'Δx')+'</th>'+''.join('<th>'+m+'</th>' for m in METHODS)+'</tr></thead><tbody>'
    for c in 'ABCD':
      for i,val in enumerate([.1,.05,.025]):
        rows=[next(r for r in S if r['case']==c and r['method']==m and r[axis]==val and r[other]==.1) for m in METHODS]
        # Below 1e-8 derivative cancellation/roundoff makes ranking meaningless.
        mins=[min(r[key][j] for r in rows) for j in range(2)] if key!='X' else None
        s+='<tr>'+('<th rowspan="3" scope="rowgroup">'+CASELABELS[c]+'</th>' if i==0 else '')+'<td>'+str(val)+'</td>'+''.join('<td>'+pair(r[key],mins)+'</td>' for r in rows)+'</tr>'
    return s+'</tbody></table>'

def build():
    time_rows=[json.loads((HERE/f'time_{c}_{m}_0.0001.json').read_text()) for c in 'ABCD' for m in ['Euler','RK4','CN']]
    assert len(S)==60 and all(r['status']=='complete' for r in time_rows)
    with (HERE/'spatial.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['case','method','dx','h','Y_u','Y_v','X_u','X_v','total_u','total_v'])
        for r in S:writer.writerow([r['case'],r['method'],r['dx'],r['h'],*r['Y'],*r['X'],*r['total']])
    with (HERE/'temporal.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['case','method','dx','h','dt','T','error_u','error_v','implicit_residual'])
        for r in time_rows:writer.writerow([r['case'],r['method'],r['dx'],r['h'],r['dt'],r['T'],*r['error'],r['cn_max_residual']])
    text=r'''## 5. Numerical experiments

We use four exact soliton solutions to examine spatial approximation and time integration separately. Section 5.1 specifies the waves and the quantities measured. In Section 5.2, we evaluate the initial spatial defects without advancing in time, varying either the lattice spacing or the resolution in \(x\). We then retain Centered-SD in Section 5.3 and compare the computed fields after time integration with three methods.

### 5.1 Test problems and error measures

The continuous determinant solutions in Section 2.1 provide the reference fields for all four tests. We set \(a=2\), \(\lambda=-2\) and \(\rho_i=1\), with no additional phase shifts. Cases A and B are one-soliton solutions; Cases C and D combine two solitons. Their spectral parameters are listed in Table 1. In particular, Case D combines the spectral pairs used separately in A and B, allowing us to examine the same constituents in a two-wave field.

<table class="paper-table"><caption>Table 1. Parameters and regions for the four soliton tests.</caption><thead><tr><th>Case</th><th>Type</th><th>Spectral pairs (pᵢ,qᵢ)</th><th>Region |x|,|y| ≤ R</th><th>Periodic x interval</th></tr></thead><tbody><tr><td>A</td><td>One soliton</td><td>(1,2)</td><td>R = 5</td><td>[−10,10)</td></tr><tr><td>B</td><td>One soliton</td><td>(4,−3)</td><td>R = 10</td><td>[−20,20)</td></tr><tr><td>C</td><td>Two solitons</td><td>(6,−5), (4,−3)</td><td>R = 30</td><td>[−40,40)</td></tr><tr><td>D</td><td>Two solitons</td><td>(1,2), (4,−3)</td><td>R = 30</td><td>[−40,40)</td></tr></tbody></table>

We choose regions containing the principal wave profiles and place the computational boundaries farther out. The y interval has the same half-width as the x interval in Table 1. For each spacing, the u nodes are \(y_k=-L+h/2+kh\), where \(L\) is that half-width. Endpoint-SD uses the corresponding edge locations \(y_k-h/2\) for v. Exact fields and derivatives are evaluated at these physical locations. Reported maxima use the native nodes within \(|x|\le R\), \(|y|<R\).

For the spatial study, we compare the time derivatives supplied by each spatial formulation with the derivatives of the continuous exact solution at \(t=0\). Let \(q^*=(u^*,v^*)\), and let \(F_{h,\Delta x}\) denote the numerical right-hand side, including the prescribed lower derivative and the lattice summation. We also evaluate \(F_h\), the same right-hand side with analytic x derivatives. The two contributions are

\[
r_y=F_h[q^*(0)]-q_t^*(0),\qquad
r_x=F_{h,\Delta x}[q^*(0)]-F_h[q^*(0)],\qquad r=r_y+r_x.
\]

Thus, \(r_y\) measures the defect introduced by the y approximation under the chosen closure, while \(r_x\) measures the additional change caused by numerical x differentiation. We compute the analytic derivatives from the finite exponential sums in the tau functions. These quantities measure errors in the initial derivatives; the sampled initial fields themselves agree with the reference. The tables give the maximum absolute u and v components of each defect separately. The maxima of the two contributions need not add to the maximum of their sum.

For the time-integration study, we measure the final field errors \(E_u(T)=\max|u^{\mathrm{num}}(T)-u^*(T)|\) and \(E_v(T)=\max|v^{\mathrm{num}}(T)-v^*(T)|\) on the same region. This comparison retains the full spatial approximation and shows how changing the time integrator affects the computed continuous-wave approximation.

### 5.2 Comparison of spatial formulations

We first vary \(h=0.1,0.05,0.025\) at fixed \(\Delta x=0.1\), evaluating every quantity at \(t=0\). Table 2 reports the y contribution \(r_y\), obtained with analytic x derivatives. The three spacings are grouped under each test case, with the methods arranged in parallel columns; each entry gives the maximum u / v components. Bold values indicate the smallest component across methods at the same spacing.

'''
    text+=table_spatial('Y','h',2,'Initial y defects with analytic x derivatives, sampled on the Δx = 0.1 grid.')
    orders={}
    for m in METHODS:
        pp=[[],[]]
        for c in 'ABCD':
            rr=[next(r for r in S if r['case']==c and r['method']==m and r['dx']==.1 and r['h']==h) for h in [.1,.05,.025]]
            for j in range(2):pp[j].extend(math.log2(rr[k]['Y'][j]/rr[k+1]['Y'][j]) for k in [0,1])
        orders[m]=[[min(p),max(p)] for p in pp]
    (HERE/'observed_orders.json').write_text(json.dumps(orders,indent=2))
    text+=r'''

For Centered-SD and FD, halving h reduces both components by approximately a factor of four in every test. Endpoint-SD also gives a roughly fourfold reduction in the u component, whereas its v component decreases by approximately a factor of two. The two fields therefore show different refinement behaviour within Endpoint-SD. The comparisons also depend on the wave: Centered-SD gives a smaller v defect than FD in A and D, while FD gives the smaller v defect in B and C. Endpoint-SD has the smallest initial u defect in these tests, despite its larger v defect.

We next fix \(h=0.1\) and vary \(\Delta x=0.1,0.05,0.025\). Table 3 uses the same case grouping to display the additional contribution \(r_x\) from Fourier differentiation. In A, C and D, this contribution is already small at \(\Delta x=0.1\); the finer grids measure the remaining derivative differences rather than a clear algebraic convergence regime. Case B behaves differently: its u contribution remains of order \(10^{-5}\), and its v contribution remains of order \(10^{-7}\). These values include the finite-interval periodic representation used by the Fourier operators. We therefore retain the measured values without assigning an x convergence order.

'''
    text+=table_spatial('X','dx',3,'Initial x contributions at h = 0.1. No ranking is assigned to these small derivative differences.')
    text+=r'''

At the common setting \(h=\Delta x=0.1\), the y contribution is larger than the x contribution in both fields of every test. As h decreases, the persistent x contribution in B becomes comparable to, or larger than, the y contribution in its u component. The two scans therefore identify where refining the lattice continues to reduce the dominant initial defect and where the x approximation also becomes relevant. The maxima are sampled on each grid, so small changes can also result from a different sampling of the error peak.

'''
    text+=r'''

These initial comparisons distinguish the effect of the y formulation from the additional x approximation. They show both the different refinement rates of the fields and the dependence of the error magnitude on the wave profile. Since no time stepping enters these measurements, differences between the time integrators can be examined separately.

### 5.3 Comparison of time integrators

We now use Centered-SD for all four tests and advance the same continuous initial fields to \(T=0.01\). The spacings are fixed at \(h=\Delta x=0.1\), and forward Euler, RK4 and Crank–Nicolson all use \(\Delta t=10^{-4}\). Table 4 gives the final errors in the two physical fields. Bold entries mark the smallest measured component in each row.

'''
    text+='<table class="paper-table"><caption>Table 4. Final field errors E<sub>u</sub> / E<sub>v</sub> for Centered-SD at T = 0.01.</caption><thead><tr><th>Case</th><th>Euler</th><th>RK4</th><th>Crank–Nicolson</th></tr></thead><tbody>'
    for c in 'ABCD':
        rr=[r for r in time_rows if r['case']==c];mins=[min(r['error'][j] for r in rr) for j in [0,1]]
        text+='<tr><th scope="row">'+CASELABELS[c]+'</th>'+''.join('<td>'+pair(r['error'],mins)+'</td>' for r in rr)+'</tr>'
    text+='</tbody></table>\n\n'
    # Make data-driven descriptions after all runs finish.
    diffs={}
    for c in 'ABCD':
        zrk=__import__('numpy').load(HERE/f'time_{c}_RK4_0.0001.npz')['z']
        from run_separated import Model,norm
        m=Model(c,'Centered-SD',.1,.1)
        diffs[c]={alg:norm(m,__import__('numpy').load(HERE/f'time_{c}_{alg}_0.0001.npz')['z']-zrk) for alg in ['Euler','CN']}
    (HERE/'time_method_differences.json').write_text(json.dumps(diffs,indent=2))
    text+=r'''The effect of the time integrator varies substantially between the tests. In A, RK4 and Crank–Nicolson give closely matched errors, while Euler gives slightly smaller final maxima. In B, the differences are much larger: the u error is about 0.075 with Euler, 0.163 with RK4 and 0.167 with Crank–Nicolson. These errors are much larger than the initial spatial defects in Section 5.2. The initial defect alone therefore does not explain the final error magnitude in this case.

'''
    for c in 'CD':
        rr=[r for r in time_rows if r['case']==c]
        best=[min(rr,key=lambda r:r['error'][j])['method'].replace('CN','Crank–Nicolson') for j in [0,1]]
        text+=f"In {c}, {best[0]} gives the smallest measured u error and {best[1]} the smallest v error. The maximum differences between the Crank–Nicolson and RK4 fields are {num(diffs[c]['CN'][0])} in u and {num(diffs[c]['CN'][1])} in v. "
    text+=r'''

The final errors combine the spatial approximation with its subsequent numerical evolution. We interpret the fixed-step comparison as a measure of final-field accuracy and sensitivity to the time integrator; establishing temporal orders would require a separate step-size study. All Crank–Nicolson steps satisfy the prescribed implicit residual tolerance.
'''
    (HERE/'experiments.md').write_text(text,encoding='utf8')
    source=(HERE/'methods.md').read_text(encoding='utf8')+'\n\n'+text
    formulas=[]
    def protect(m):
        v=m[0];formulas.append(dict(tex=v[2:-2],display=v.startswith('\\[')));return 'MATHPLACEHOLDER'+str(len(formulas)-1)+'END'
    protected=re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)',protect,source)
    js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
    out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(formulas),text=True,encoding='utf8',capture_output=True,check=True)
    rendered=json.loads(out.stdout)
    parts=re.split(r'(?m)^(## |### )',protected);sections={};intros={};titles={}
    for i in range(1,len(parts),2):
        title,body=parts[i+1].split('\n',1);number=title.split()[0].rstrip('.');titles[number]=title
        html=markdown.markdown(body)
        for j,r in enumerate(rendered):
            html=html.replace('<p>MATHPLACEHOLDER'+str(j)+'END</p>','<div class="equation">'+r+'</div>' if formulas[j]['display'] else '<p>'+r+'</p>')
            html=html.replace('MATHPLACEHOLDER'+str(j)+'END',r)
        if parts[i]=='## ':intros[number]=html
        else:sections[number]='<section id="section-'+number+'"><h3>'+title+'</h3>'+html+'</section>'
    target=ROOT/'dlw-paper.html';old=target.read_text(encoding='utf8')
    backup=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S');backup.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup/target.name)
    for n,html in sections.items():
        old,count=re.subn(r'<section id="section-'+re.escape(n)+r'">[\s\S]*?</section>',lambda m:html,old,count=1);assert count==1
    for n,html in intros.items():
        old=re.sub(r'(<section id="section-'+n+r'"><h2>[^<]*</h2>)[\s\S]*?(?=<section id="section-'+n+r'\.)',lambda m:m[1]+html,old,count=1)
    css='<style id="numerical-tables">.paper-table{width:100%;border-collapse:collapse;margin:24px 0 30px;font-size:14px;line-height:1.5;font-variant-numeric:tabular-nums}.paper-table caption{text-align:left;font-size:15px;margin-bottom:9px}.paper-table th,.paper-table td{padding:7px 8px;text-align:center;vertical-align:middle}.paper-table thead{border-top:2px solid #222;border-bottom:1px solid #222}.paper-table tbody{border-bottom:2px solid #222}.paper-table td{white-space:nowrap}@media print{.paper-table{font-size:9px}.paper-table th,.paper-table td{padding:5px 3px}tr{break-inside:avoid}thead{display:table-header-group}}</style>'
    old=re.sub(r'<style id="numerical-tables">[\s\S]*?</style>','',old)
    old=old.replace('</head>',css+'</head>')
    # Keep unfinished sections, but update the now-obsolete editorial scope.
    old=old.replace('5.3 Time integration and exact-lattice benchmarks','5.3 Comparison of time integrators')
    old=old.replace('采用一个单孤子、一个双孤子、Gaussian 和正弦两类非精确初值。后两者不是随机噪声；若另加随机扰动，明确种子和谱。区分连续解误差、半离散解误差及无精确解时的加密差异。原四组孤子结果作历史证据，不直接冒充新 FFT 实验。','本轮采用四组孤子。空间部分在t=0分离解析x下的y缺陷与Fourier x附加缺陷；时间部分固定Centered-SD比较Euler/RK4/C–N。Gaussian和正弦初值暂缓。')
    old=old.replace('对 Endpoint-SD、Centered-SD 分别使用各自相容的半离散精确初边值验证求解器和时间阶；控制空间误差或明确误差平台，再比较 Euler/RK4/C–N 的误差及成本。不同精确场的误差不直接当作同一连续场误差比较。','本轮固定Centered-SD、h=dx=.1、dt=1e-4、T=.01，从连续精确初值推进。表中为最终场总误差，不是独立时间误差或时间阶验证。')
    old=old.replace('本轮同步已讨论的理论工作稿，尚未启动新一轮 FFT 数值实验。','2026-10-23已补充四孤子的初始空间缺陷与时间算法比较；Section 4.3–4.4及5.4–5.5仍待处理。')
    old=re.sub(r'(<section class="guide" id="appendix-G"[\s\S]*?<p class="status">)[\s\S]*?</p>',lambda m:m[1]+'2026-10-23：已保留第2节及3.1–3.4理论工作稿，补充4.1–4.2数值实现与5.1–5.3四孤子实验。3.4精确场收敛、4.3–4.4、5.4–5.5及其余占位章节待续。新表已核验数据与静态数学渲染；本次浏览器拒绝file协议，未完成视觉预览。</p>',old,count=1)
    for major in ['4','5']:
        old=re.sub(r'<a class="subsection" href="#section-'+major+r'\.[^"]*">[^<]*</a>','',old)
        link=re.search(r'<a href="#section-'+major+r'">[^<]*</a>',old)
        addition=''.join('<a class="subsection" href="#section-'+n+'">'+titles[n]+'</a>' for n in sections if n.startswith(major+'.'))
        old=old[:link.end()]+addition+old[link.end():]
    soup=BeautifulSoup(old,'html.parser');ids=[e['id'] for e in soup.select('[id]')]
    assert len(ids)==len(set(ids)) and 'MATHPLACEHOLDER' not in old and 'katex-error' not in old
    assert all(a['href'][1:] in ids for a in soup.select('a[href^="#"]'))
    target.write_text(old,encoding='utf8')
    # Dedicated reading view for the new experiments, using the same rendered text.
    report=ROOT/'report/dlw_separated_experiments_20261023.html'
    head=old[old.index('<head>')+6:old.index('</head>')].replace('href="Workspaces/','href="../Workspaces/')
    report.write_text('<!doctype html><html lang="en"><head>'+head+'</head><body><article><h1>Initial spatial defects and time integration</h1>'+intros['5']+''.join(sections[n] for n in ['5.1','5.2','5.3'])+'</article></body></html>',encoding='utf8')
    (HERE/'build_validation.json').write_text(json.dumps(dict(spatial_records=len(S),time_records=len(time_rows),rendered_formulas=len(formulas),cn_max_residual=max(r['cn_max_residual'] for r in time_rows),backup=str(backup),output=str(target)),indent=2))
    print('Updated',target,report)

if __name__=='__main__':build()
