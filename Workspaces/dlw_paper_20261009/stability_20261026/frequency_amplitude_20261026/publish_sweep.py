"""Publish the completed frequency/amplitude sweep, preserving unrelated manuscript bytes."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAPER = ROOT / 'dlw-paper.html'
REPORT = ROOT / 'report/dlw_perturbation_sweep_20261026.html'
CASES = ['A', 'D', 'Gaussian', 'Sinusoidal']
EN = dict(A='One-soliton', D='Two-soliton', Gaussian='Gaussian', Sinusoidal='Sinusoidal')
ZH = dict(A='一孤子', D='双孤子', Gaussian='高斯', Sinusoidal='正弦')
data = {c: json.loads((HERE / (c+'.json')).read_text(encoding='utf-8')) for c in CASES}
controls = {c: json.loads((HERE / (c+'_half_step.json')).read_text(encoding='utf-8')) for c in CASES}
theory = json.loads((HERE/'audit/constant_response.json').read_text(encoding='utf-8'))['rows']
summary = json.loads((HERE/'summary.json').read_text(encoding='utf-8'))
assert summary['completed_trajectories'] == 72 and len(summary['time_controls']) == 8
audit = json.loads((HERE/'audit/output_validation.json').read_text(encoding='utf-8'))
assert audit['independent_array_audit_passed'] and len(audit['half_step_controls']) == 8
time_change = max(max(r['terminal_physical_field_difference']) for r in summary['time_controls'])
for c, d in data.items():
    assert d['status'] == 'complete' and d['reached'] == .01 and len(d['records']) == 18
    assert controls[c]['status'] == 'complete' and controls[c]['reached'] == .01
    assert hashlib.sha256((HERE/(c+'.npz')).read_bytes()).hexdigest() == d['artifact_sha256']

maths = []
def m(tex, display=False):
    maths.append(dict(tex=tex, display=display))
    return f'SWEEPMATH{len(maths)-1}END'
def text(s):
    p = s.split('$')
    assert len(p)%2 == 1, s
    return ''.join(m(t) if i%2 else t for i,t in enumerate(p))
def p(s): return '<p>'+text(s)+'</p>\n'
def eq(s): return '<div class="equation">'+m(s,True)+'</div>\n'
def get(c,k,comp,ej=1):
    return next(r for r in data[c]['records'] if r['k_index']==k and r['epsilon_index']==ej and r['component']==comp)
def const(c,k,comp):
    return next(r for r in theory if r['case']==c and r['kappa_factor_of_pi_over_2']==[1,2,4][k] and r['component']==comp)
def f(x): return f'{x:.5f}'
def sci(x):
    a,b=f'{x:.2e}'.split('e')
    return a+r'\times10^{'+str(int(b))+'}'
spread = {c: max(r['relative_pair_max_difference_all_time'] for r in data[c]['records']) for c in CASES}

def table(c,number,language):
    ident='table-perturbation' if c=='A' else 'table-perturbation-'+c.lower()
    cap=(f'Table {number}. Wavenumber and amplitude dependence for the {EN[c].lower()} case at $T=0.01$.'
         if language=='en' else f'表 {number}．{ZH[c]}算例在 $T=0.01$ 的扰动响应。')
    s='<div class="table-wrap"><table id="'+ident+'"><caption>'+text(cap)+'</caption><thead><tr>'
    s+='<th rowspan="2" scope="col">'+m(r'\kappa')+'</th><th rowspan="2" scope="col">'+m(r'\varepsilon')+'</th>'
    s+='<th colspan="3" scope="colgroup">'+text('$u_0$ only' if language=='en' else '仅扰动 $u_0$')+'</th>'
    s+='<th colspan="3" scope="colgroup">'+text('$v_0$ only' if language=='en' else '仅扰动 $v_0$')+'</th></tr><tr>'
    s+=''.join('<th scope="col">'+m(t)+'</th>' for t in ['P_u','P_v','G_2']*2)+'</tr></thead><tbody>'
    for k in range(3):
        for ej in range(3):
            s+='<tr>'
            if ej==0:s+='<th scope="rowgroup" rowspan="3">'+m([r'\pi/2',r'\pi',r'2\pi'][k])+'</th>'
            s+='<th scope="row">'+m('10^{'+str([-7,-6,-5][ej])+'}')+'</th>'
            for component in ['u','v']:
                r=get(c,k,component,ej)
                s+=''.join(f'<td>{v:.6f}</td>' for v in [*r['final_max_normalized'],r['l2_pair_gain']])
            s+='</tr>'
    return s+'</tbody></table></div>\n'

def analysis(c,language):
    us=[get(c,k,'u') for k in range(3)];vs=[get(c,k,'v') for k in range(3)]
    vtu=[r['final_max_normalized'][0] for r in vs]
    utv=[r['final_max_normalized'][1] for r in us]
    pred=[const(c,k,'v')['terminal_u_over_epsilon'] for k in range(3)]
    if language=='en':
        if c=='A':
            s=p(r'Increasing the wavenumber strengthens transfer between the fields. At $\varepsilon=10^{-6}$, the normalized $v$-to-$u$ responses are '
                +', '.join('$'+f(v)+'$' for v in vtu)+r' for $\kappa=\pi/2,\pi,2\pi$, respectively. '
                +'The constant-background formula on the same grid gives '+', '.join('$'+f(v)+'$' for v in pred)+'. '
                +r'The transverse primitive accounts for much of this transfer, while the difference from the constant-background prediction becomes more visible at the largest wavenumber. '
                +r'The reverse $u$-to-$v$ response rises from $'+f(utv[0])+'$ to $'+f(utv[-1])+r'$. Over these samples, doubling the wavenumber approximately doubles this reverse response, while the $v$-to-$u$ response increases about fourfold. The two transfer directions therefore exhibit different frequency dependence on the soliton background.')
        elif c=='D':
            s=p(r'The two-soliton case exhibits the largest $v$-to-$u$ response. Its normalized magnitude increases from $'+f(vtu[0])+'$ to $'+f(vtu[1])+'$ and $'+f(vtu[2])+'$, '
                +r'and the corresponding pair gain increases from $'+f(vs[0]['l2_pair_gain'])+'$ to $'+f(vs[2]['l2_pair_gain'])+'$. '
                +r'The constant-background predictions are $'+f(pred[0])+'$, $'+f(pred[1])+'$ and $'+f(pred[2])+r'$ on this domain. '
                +r'The wider transverse envelope and its accumulated primitive make the transfer larger than in the one-soliton case. '
                +r'For $u_0$ input, the $v$ response increases from $'+f(utv[0])+'$ to $'+f(utv[2])+r'$. At $\kappa=2\pi$, the initially perturbed components also respond more strongly: $P_u='+f(us[2]['final_max_normalized'][0])+r'$ for $u_0$ input and $P_v='+f(vs[2]['final_max_normalized'][1])+r'$ for $v_0$ input. Their constant-background counterparts are $'+f(const(c,2,'u')['terminal_u_over_epsilon'])+'$ and $'+f(const(c,2,'v')['terminal_v_over_epsilon'])+r'$. The background therefore has a substantial effect on the same-field response at this shorter wavelength.')
        elif c=='Gaussian':
            s=p(r'The Gaussian case shows a clear increase in the pair gain as the wavelength decreases. For $u_0$ input, $G_2$ rises from $'+f(us[0]['l2_pair_gain'])+'$ to $'+f(us[2]['l2_pair_gain'])+r'$; for $v_0$ input, it rises from $'+f(vs[0]['l2_pair_gain'])+'$ to $'+f(vs[2]['l2_pair_gain'])+'$. '
                +r'The cross-field responses increase from $'+f(utv[0])+'$ to $'+f(utv[2])+r'$ in $v$, and from $'+f(vtu[0])+'$ to $'+f(vtu[2])+r'$ in $u$. '
                +r'These changes follow the increasing $\sinh(\kappa^2T)$ factor in the constant-background response. '
                +r'The native-node maxima also contain the effect of translation relative to the sampling grid, so the pair norm helps distinguish amplitude growth from peak displacement.')
        else:
            s=p(r'The sinusoidal case gives a frequency dependence close to that of the Gaussian case. At $\kappa=2\pi$, the pair gains are $'+f(us[2]['l2_pair_gain'])+'$ and $'+f(vs[2]['l2_pair_gain'])+r'$ for $u_0$ and $v_0$ input, respectively. '
                +r'The corresponding cross-field responses are $'+f(utv[2])+r'$ in $v$ and $'+f(vtu[2])+r'$ in $u$. '
                +r'The similar response on these two backgrounds is consistent with their common transverse envelope and the same linear growth and transfer mechanism.')
        s+=p(r'Across the three amplitudes, the largest relative difference between the normalized physical fields and the corresponding $\varepsilon=10^{-6}$ run is approximately $'+sci(spread[c])+r'$ over the recorded interval. These results show nearly proportional responses to the prescribed perturbation amplitudes.')
    else:
        if c in ['A','D']:
            s=p(r'在 $\varepsilon=10^{-6}$ 时，波数依次取 $\pi/2,\pi,2\pi$，$v\to u$ 的归一化响应为 '
                +'、'.join('$'+f(v)+'$' for v in vtu)+'；相同网格与观测区域上的常背景预测为 '
                +'、'.join('$'+f(v)+'$' for v in pred)+r'。横向积分解释了这一路径的主要响应；波数增大后，背景波形的影响也更明显。'
                +r'反向 $u\to v$ 响应从 $'+f(utv[0])+'$ 增至 $'+f(utv[2])+'$。')
            if c=='A':s+=p(r'这三个波数下，波数翻倍时 $u\to v$ 响应约翻倍，而 $v\to u$ 响应约增至四倍。两个传递方向表现出不同的频率依赖，孤子背景对反向传递的影响更明显。')
            if c=='D':s+=p(r'双孤子的 $v_0$ 输入对应配对增益从 $'+f(vs[0]['l2_pair_gain'])+'$ 增至 $'+f(vs[2]['l2_pair_gain'])+r'$，其中较大的交叉分量与更宽的横向扰动包络及其累积积分密切相关。最高波数下，直接受扰分量自身的响应也明显增大：$u_0$ 输入的 $P_u='+f(us[2]['final_max_normalized'][0])+r'$，$v_0$ 输入的 $P_v='+f(vs[2]['final_max_normalized'][1])+r'$；常背景预测分别为 $'+f(const(c,2,'u')['terminal_u_over_epsilon'])+'$ 和 $'+f(const(c,2,'v')['terminal_v_over_epsilon'])+r'$。在这一短波扰动下，双孤子背景对自身分量的响应也有显著影响。')
        else:
            s=p(r'波数从 $\pi/2$ 增至 $2\pi$ 时，$u_0$ 输入对应的配对增益从 $'+f(us[0]['l2_pair_gain'])+'$ 增至 $'+f(us[2]['l2_pair_gain'])+r'$；$v_0$ 输入对应的配对增益从 $'+f(vs[0]['l2_pair_gain'])+'$ 增至 $'+f(vs[2]['l2_pair_gain'])+'$。'
                +r'$u\to v$ 响应从 $'+f(utv[0])+'$ 增至 $'+f(utv[2])+r'$，$v\to u$ 响应从 $'+f(vtu[0])+'$ 增至 $'+f(vtu[2])+r'$。两类非孤子背景呈现相近的波数依赖，与常背景公式中的双曲函数增长相符。节点最大值同时受到波峰平移的采样影响，配对范数补充描述了整体扰动的变化。')
        s+=p(r'比较整个记录区间内的归一化物理场，三个幅值相对 $\varepsilon=10^{-6}$ 结果的最大相对差异为 $'+sci(spread[c])+r'$。在本次幅值范围内，扰动响应近似按初始幅值成比例变化。')
    return s

before=PAPER.read_bytes();src=before.decode('utf-8')
match=re.search(r'<section id="section-6\.2">.*?</section>',src,re.S)
assert match and 'Wavenumber and amplitude dependence for the' not in match[0]
old=match[0]
figure=re.search(r'<figure\b.*?</figure>',old,re.S)[0]
new='<section id="section-6.2">\n<h3>6.2 Independent physical-field perturbations</h3>\n'
new+=p(r'We examine how the wavelength and amplitude of an initial perturbation affect the computed Centered-SD evolution. Each of the four backgrounds in Section 5.1 is evolved with $h=\Delta x=0.1$, RK4, $\Delta t=10^{-4}$, and $T=0.01$. In separate experiments, we add $\varepsilon\Phi$ to $u_0$ or to $v_0$, where')
new+=eq(r'\Phi(x,y)=\sin^2\!\left(\frac{\pi(y-y_L)}{y_R-y_L}\right)\cos(\kappa x),\qquad \kappa\in\{\pi/2,\pi,2\pi\},\qquad \varepsilon\in\{10^{-7},10^{-6},10^{-5}\}.')
new+=p(r'The same physical wavenumbers are used on all four backgrounds. The envelope and its first derivative vanish at the transverse endpoints. Each perturbation is imposed at the native physical-field locations, and the auxiliary values are recovered through the Centered-SD recurrence with zero initial lower auxiliary perturbation. The perturbed and unperturbed trajectories share the prescribed lower $u$ trace. The transverse node intervals are $[-9.95,9.95]$ for the one-soliton case, $[-39.95,39.95]$ for the two-soliton case, and $[-2,2]$ for the Gaussian and sinusoidal cases.')
new+=p(r'Let $\delta u_h$ and $\delta v_h$ denote the differences between perturbed and unperturbed numerical trajectories. Their algebraically subtracted nonlinear equations are evolved together with the background at every RK4 stage. We report the terminal responses $P_u=\|\delta u_h(T)\|_\infty/\varepsilon$ and $P_v=\|\delta v_h(T)\|_\infty/\varepsilon$ in the observation regions of Section 5.1, together with the pair gain')
new+=eq(r'G_2(t)=\frac{\bigl(\|\delta u_h(t)\|_{2,h}^2+\|\delta v_h(t)\|_{2,h}^2\bigr)^{1/2}}{\bigl(\|\delta u_h(0)\|_{2,h}^2+\|\delta v_h(0)\|_{2,h}^2\bigr)^{1/2}},\qquad \|f\|_{2,h}^2=h\Delta x\sum_{j,k}|f_{j,k}|^2.')
new+=p(r"The sum covers the full periodic $x$ interval and the same interior $y$ region, separately at each field's native sites."
       +r' To assess amplitude scaling, we compare the complete fields $(\delta u_h,\delta v_h)/\varepsilon$ against the corresponding $\varepsilon=10^{-6}$ run at every recorded time, fixing the wavenumber and the initially perturbed field. The relative difference is the largest componentwise discrepancy in the observation region, divided by the largest componentwise response of that reference run over $0\le t\le T$.')
new+=p(r'Figure 29 shows the response histories for $\kappa=\pi/2$ and $\varepsilon=10^{-6}$. Tables 6&ndash;9 extend the comparison to all nine wavenumber and amplitude combinations for each background.')
new+=figure+'\n'
for i,c in enumerate(CASES):
    new+='<h4>'+EN[c]+' case</h4>\n'+table(c,6+i,'en')+analysis(c,'en')
new+=p(r'Across the four backgrounds, changing the initial amplitude primarily rescales the response within the tested range, whereas shortening the wavelength strengthens transfer between the physical fields and increases the pair gain. The $\sinh(\kappa^2t)$ factor in Section 6.1 provides a quantitative comparison for this transfer. The soliton results also show how the background wave changes the frequency dependence of the response, particularly for an initial perturbation of $u$.')
new+=p(r'We also halve the time step at $\kappa=2\pi$ and $\varepsilon=10^{-5}$ for each background and both input fields. The largest observed change in the terminal perturbation fields is approximately $'+sci(time_change)+r'$ in absolute value over the observation region.')
new+='</section>'

report='<header><p class="eyebrow">DLW · Centered-SD · RK4</p><h1>扰动波长与幅值：四个算例的响应</h1></header>'
report+=p(r'四个背景分别进行独立 $u_0$ 与 $v_0$ 扰动。取 $\kappa=\pi/2,\pi,2\pi$，$\varepsilon=10^{-7},10^{-6},10^{-5}$，共72条非线性扰动轨道，均以 $h=\Delta x=0.1$、RK4、$\Delta t=10^{-4}$ 演化至 $T=0.01$。本节比较同一离散系统中受扰轨道与背景轨道的差。')
report+='<nav>'+''.join(f'<a href="#case-{c}">{ZH[c]}</a>' for c in CASES)+'</nav>'
report+=p(r'各表记 $P_u=\|\delta u_h(T)\|_\infty/\varepsilon$、$P_v=\|\delta v_h(T)\|_\infty/\varepsilon$。最大值使用论文中的物理场原生节点及观测区域；$G_2$ 为两个物理场组成的离散 $L^2$ 配对范数相对于其初始值的比。配对范数覆盖完整周期 $x$ 区间及相同内部 $y$ 区域。')
report+=p(r'扰动为 $\varepsilon\sin^2(\pi(y-y_L)/(y_R-y_L))\cos(\kappa x)$。幅值缩放的比较固定波数和初始受扰分量，使用每个记录时刻的完整归一化物理场，相对基准取 $\varepsilon=10^{-6}$；相对差异以该基准在整个记录区间内的最大分量响应归一化。')
for i,c in enumerate(CASES):
    report+=f'<section id="case-{c}"><h2>{i+1}. {ZH[c]}算例</h2>'+table(c,i+1,'zh')+analysis(c,'zh')+'</section>'
report+='<h2>波长与幅值的作用</h2>'
report+=p(r'改变幅值主要使响应成比例缩放；缩短波长则显著增强场间传递。三个波数对应 $\kappa^2T=0.024674,0.098696,0.394784$，常背景公式中的 $\sinh(\kappa^2T)$ 分别约为 $0.024677,0.098856,0.405119$。横向积分和差分将这个频率依赖传递到物理场；不同背景进一步改变两场的响应幅度。')
report+=p(r'对每个背景的 $\kappa=2\pi$、$\varepsilon=10^{-5}$ 两种输入另做时间步减半检查。终态扰动物理场在观测区域内的最大绝对变化为 $'+sci(time_change)+r'$。四个背景轨道均复现已有RK4结果；本轮同时核对了初值重构、非线性差分方程、终态范数和表格数值。')
report+='<p><a href="../dlw-paper.html#section-6.2">主论文 Section 6.2</a> · <a href="../Workspaces/dlw_paper_20261009/stability_20261026/frequency_amplitude_20261026/terminal_rows.csv">完整终态数据</a></p>'
style='''body{max-width:1080px;margin:44px auto;padding:0 24px;font:17px/1.8 Georgia,"Times New Roman","Microsoft YaHei",serif;color:#222;background:#fff}h1{font-size:29px;line-height:1.4}h2{font-size:23px;margin-top:38px}a{color:#245c7b}.eyebrow{font-size:14px;color:#666}nav{display:flex;gap:28px;padding:12px 0;border-block:1px solid #ccc}.table-wrap{overflow-x:auto;margin:24px 0}table{width:100%;border-collapse:collapse;border-top:2px solid #222;border-bottom:2px solid #222;font:14px/1.55 Georgia,"Times New Roman",serif;font-variant-numeric:tabular-nums}caption{text-align:left;font:16px/1.6 Georgia,"Microsoft YaHei",serif;padding-bottom:12px}thead{border-bottom:1px solid #222}th,td{padding:9px 8px;white-space:nowrap}th{font-weight:normal;text-align:center}td{text-align:right}.katex{font-size:1.02em}@media print{body{margin:0;max-width:none;padding:0;font-size:11pt}nav{display:none}table{font-size:8pt}tr{break-inside:avoid}thead{display:table-header-group}h2{break-after:avoid}.table-wrap{overflow:visible}}'''
report='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 扰动波长与幅值比较</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body>'+report+'</body></html>'

js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));"
out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf-8',capture_output=True,check=True)
rendered=json.loads(out.stdout)
def render(s):return re.sub(r'SWEEPMATH(\d+)END',lambda x:rendered[int(x[1])],s)
new,report=render(new),render(report)
updated=src[:match.start()]+new+src[match.end():]
assert updated.count('<caption>Table 7. Control runs for Section 5.')==1
updated=updated.replace('<caption>Table 7. Control runs for Section 5.','<caption>Table 10. Control runs for Section 5.')
assert re.findall(r'<figure\b.*?</figure>',src,re.S)==re.findall(r'<figure\b.*?</figure>',updated,re.S)
rest_before=src[:match.start()]+src[match.end():]
newmatch=re.search(r'<section id="section-6\.2">.*?</section>',updated,re.S)
rest_after=(updated[:newmatch.start()]+updated[newmatch.end():]).replace('<caption>Table 10. Control runs for Section 5.','<caption>Table 7. Control runs for Section 5.')
assert rest_before==rest_after
for html,nt in [(updated,10),(report,4)]:
    soup=BeautifulSoup(html,'html.parser')
    assert not soup.select('.katex-error') and len(soup.find_all('table'))==nt
    ids=[el['id'] for el in soup.find_all(id=True)]
    assert len(ids)==len(set(ids))
assert PAPER.read_bytes()==before,'Concurrent main-paper edit; reread before retrying.'
backup=HERE/('before_publication_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir()
(backup/'dlw-paper.html').write_bytes(before)
if REPORT.exists():(backup/REPORT.name).write_bytes(REPORT.read_bytes())
PAPER.write_bytes(updated.encode('utf-8'));REPORT.write_text(report,encoding='utf-8')
(HERE/'section62.html').write_text(new,encoding='utf-8')
full6=re.search(r'<section id="section-6".*?(?=<section id="section-7">)',updated,re.S)[0]
(HERE.parent/'section6.html').write_text(full6,encoding='utf-8')
validation=dict(date='2026-10-26',trajectories=72,all_reached_T=True,main_tables=10,main_figures=29,report_tables=4,katex_errors=0,
    changed_sections=['6.2','control table caption number 7→10'],unchanged_figure_bytes=True,protected_rest_exact=True,
    max_relative_amplitude_field_difference=spread,continuous_reference_certified=False,
    before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),report=str(REPORT),backup=str(backup))
(HERE/'publication_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False,indent=2))
