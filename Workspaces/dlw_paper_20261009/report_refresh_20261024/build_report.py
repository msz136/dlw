"""Build only the root Report.html; never publish or edit the main paper."""
from pathlib import Path
import csv
import hashlib
import html
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / 'Workspaces/dlw_paper_20261009/spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024'

def read(path):
    return json.loads(path.read_text(encoding='utf8'))

SELECTED = HERE/'natural_selection_20261025'
preserved = read(SELECTED/'report_preservation.json')
paper_hash = hashlib.sha256((ROOT/'dlw-paper.html').read_bytes()).hexdigest()
assert paper_hash == preserved['paper_sha256'], 'Main paper changed during this report task'
assert (ROOT/preserved['report_backup']).exists()

CASES=['A','D','Gaussian','Sinusoidal']
METHODS=['Endpoint-SD','Centered-SD','FD']
BASELINE_METHODS={'Endpoint-SD','FD'}
NEW=HERE/'nondegenerate_rk4_20261024'
spatial=[r for r in read(RUN/'baselines.json') if r['h']==r['dx']==.1 and r['method'] in BASELINE_METHODS]
spatial += [r for r in read(NEW/'initial_results.json') if r['method'] in BASELINE_METHODS]
spatial += read(SELECTED/'initial_results.json')
temporal=[r for r in read(HERE/'rk4_spatial/results.json') if r['method'] in BASELINE_METHODS]
temporal += [r for r in read(NEW/'results.json') if r['method'] in BASELINE_METHODS]
temporal += read(SELECTED/'results.json')
spatial=[r for r in spatial if r['case'] in CASES]
temporal=[r for r in temporal if r['case'] in CASES]
certificate=read(NEW/'reference_certificate.json')
assert certificate['status']=='verified_all_stored_sample_values'
ref_bound=certificate['uniform_bound_each']
ref_exponent=int(f'{ref_bound:.0e}'.split('e')[1])
assert ref_bound==10.**ref_exponent
assert len(spatial)==len(temporal)==12
assert all(r.get('status','complete')=='complete' and r['h']==r['dx']==.1 for r in spatial)
assert all(r['status']=='complete' and r['h']==r['dx']==.1 and r['T']==r['reached']==.01 and r['dt']==1e-4 and r['integrator']=='RK4' for r in temporal)
spatial.sort(key=lambda r:(CASES.index(r['case']),METHODS.index(r['method'])))
temporal.sort(key=lambda r:(CASES.index(r['case']),METHODS.index(r['method'])))

with (HERE/'table1_initial_derivative_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['case','method','h','dx','t','error_ut','error_vt'])
    for r in spatial: w.writerow([r['case'],r['method'],r['h'],r['dx'],0,*r['total']])
with (HERE/'table2_final_field_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['case','space','integrator','h','dx','dt','T','error_u','error_v'])
    for r in temporal: w.writerow([r['case'],r['method'],r['integrator'],.1,.1,1e-4,.01,*r['error']])

labels = {
    'A': ('One-soliton','单孤子 · (1, 2)'),
    'D': ('Two-soliton','双孤子 · (1, 2), (4, −3)'),
    'Gaussian': ('Gaussian','周期高斯初值'), 'Sinusoidal': ('Sinusoidal','正弦初值')}
def number(x, best=False):
    mantissa, exponent = f'{x:.3e}'.split('e')
    value=f'<span class="sci">{mantissa} × 10<sup>{int(exponent):d}</sup></span>'
    return f'<strong>{value}</strong>' if best else value

def rows(records, cases, methods, key):
    out=[]
    for case in cases:
        selected=[]
        for method in methods:
            match=[r for r in records if r['case']==case and r['method']==method]
            assert len(match)==1,(case,method)
            selected.append(match[0][key])
        minima=[min(v[j] for v in selected) for j in (0,1)]
        title,subtitle=labels[case]
        row=f'<tr><th scope="row">{title}<span class="case-note">{subtitle}</span></th>'
        for values in selected:
            for j,value in enumerate(values):
                best=f'{value:.3e}'==f'{minima[j]:.3e}'
                row+=f'<td data-value="{value:.17g}">{number(value,best)}</td>'
        out.append(row+'</tr>')
    return '\n'.join(out)

maths=[]
def math(tex, display=False):
    i=len(maths); maths.append(dict(tex=tex,display=display)); return f'MATHSLOT{i}END'

def table_header(fields,methods=METHODS,labels=None):
    groups=''.join(f'<th colspan="2" scope="colgroup">{method}</th>' for method in (labels or methods))
    columns=''.join(f'<th scope="col">{math(field)}</th>' for method in methods for field in fields)
    return f'<thead><tr><th rowspan="2" scope="col">算例</th>{groups}</tr><tr>{columns}</tr></thead>'

linkroot='Workspaces/dlw_paper_20261009/report_refresh_20261024'
body=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DLW 短时物理场的空间格式比较</title>
<link rel="stylesheet" href="Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css">
<style>
:root{{color-scheme:light;--ink:#1e293b;--muted:#475569;--line:#cbd5e1;--accent:#334155}}
*{{box-sizing:border-box}}body{{margin:0;background:#fff;color:var(--ink);font:17px/1.85 Georgia,"Noto Serif SC","Microsoft YaHei",serif}}
main{{max-width:1160px;margin:0 auto;padding:48px 32px 60px}}header{{margin-bottom:34px}}h1,h2,h3{{text-wrap:balance;font-weight:600}}h1{{font-size:30px;line-height:1.4;margin:8px 0 15px}}h2{{font-size:23px;margin:38px 0 12px}}h3{{font-size:18px;margin:25px 0 8px}}
p{{margin:12px 0;text-wrap:pretty}}.eyebrow,.meta,.note,footer{{color:var(--muted)}}.eyebrow{{font:14px/1.6 Arial,"Microsoft YaHei",sans-serif}}.meta{{font-size:15px}}.lead{{max-width:900px}}a{{color:var(--accent);text-underline-offset:3px}}a:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:4px}}
.equation{{overflow-x:auto;padding:3px 0}}.katex{{font-size:1.02em}}.table-wrap{{overflow-x:auto;margin:22px 0 10px}}
table{{width:100%;border-collapse:collapse;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);font-size:14px;font-variant-numeric:tabular-nums;line-height:1.5}}
caption{{caption-side:top;text-align:left;font-size:16px;font-weight:600;padding:0 0 12px;color:var(--ink)}}thead{{border-bottom:1px solid var(--ink)}}th,td{{padding:12px 9px;vertical-align:middle}}thead th{{text-align:center;font-weight:500}}thead tr:first-child th{{padding-bottom:5px}}thead tr:last-child th{{padding-top:5px}}tbody th{{text-align:left;font-weight:600;min-width:144px}}td{{text-align:right;white-space:nowrap}}.case-note{{display:block;font-size:11px;font-weight:400;color:var(--muted);margin-top:5px;white-space:nowrap}}.sci{{white-space:nowrap}}sup{{font-size:.75em}}strong{{font-weight:700}}.note{{font-size:14px;line-height:1.8}}.downloads{{font-size:14px;margin-top:10px}}
details{{border-top:1px solid var(--line);margin-top:36px;padding-top:18px}}summary{{cursor:pointer;font-size:18px;font-weight:600}}details p{{font-size:16px}}footer{{border-top:1px solid var(--line);margin-top:32px;padding-top:16px;font-size:13px}}.profiles{{padding-left:22px}}.profiles li{{margin:10px 0}}.case-regions{{font-size:15px}}
@media(max-width:760px){{main{{padding:28px 18px 40px}}h1{{font-size:25px}}h2{{font-size:21px}}body{{font-size:16px}}table{{min-width:880px}}th,td{{padding:10px 8px}}}}
@media print{{@page{{size:A4;margin:15mm}}main{{max-width:none;padding:0}}body{{font-size:10.5pt;line-height:1.6;color:#000}}h1{{font-size:20pt}}h2{{font-size:14pt}}table{{font-size:8pt;min-width:0}}th,td{{padding:7px 4px}}tbody th{{min-width:0}}.case-note{{font-size:7pt}}.table-wrap{{overflow:visible}}table,thead,tr{{break-inside:avoid}}.downloads{{display:none}}details{{break-before:auto}}a{{color:inherit}}}}
</style></head><body><main>
<header><p class="eyebrow">DLW · Numerical comparisons · 2026-10-25</p>
<h1>短时物理场的空间格式比较</h1>
<p class="downloads"><a href="dlw-paper.html#section-5.1">主论文与四算例图示</a></p>
<p class="lead">比较 Endpoint-SD、Centered-SD 与 FD 在单孤子、双孤子、高斯和正弦四个算例中计算物理场的精度。各格式使用同一初值与 RK4 参数，推进至 {math('T=0.01')} 后与连续解比较。Centered-SD 采用第 3.2 节的自然物理场定义 {math(r'v_k=\Delta_hZ_k')}。初始时间导数误差保留为一张诊断表，主要结果集中于演化后的 {math('u,v')}。</p>
<p class="meta">{math(r'h=\Delta x=0.1')}，{math('x')} 方向采用 Fourier 微分。粗体标记各算例、各分量的最小误差；显示精度相同时并列加粗。</p></header>

<section id="initial-rates"><h2>1. {math('t=0')}：初始时间导数误差</h2>
<p>在相同的连续初值上计算各格式的 {math('u_t,v_t')}，以连续方程的解析初始右端为参考，测量时间导数的空间离散误差。</p>
<div class="equation">{math(r'E_{u_t}=\max_{\mathcal G_u}|u_t^{\mathrm{num}}(0)-u_t^{\mathrm{ref}}(0)|,\qquad E_{v_t}=\max_{\mathcal G_v}|v_t^{\mathrm{num}}(0)-v_t^{\mathrm{ref}}(0)|.',True)}</div>
<div class="table-wrap"><table id="table-initial"><caption>表 1. 初始时间导数的绝对最大误差，{math(r'h=\Delta x=0.1')}。</caption>
{table_header(['E_{u_t}','E_{v_t}'])}
<tbody>{rows(spatial,CASES,METHODS,'total')}</tbody></table></div>
<p>表 1 记录各格式作用于相同连续初值时的空间误差，作为终态物理场比较的初始诊断。</p>
<p class="note">{math(r'\mathcal G_u,\mathcal G_v')} 为各物理场在指定区域内的采样点。Endpoint-SD 与 Centered-SD 的 {math('v')} 位于边中点，FD 的两个场均位于节点。</p>
<p class="downloads"><a href="{linkroot}/table1_initial_derivative_errors.csv">下载表 1 数据 CSV</a></p></section>

<section id="final-fields"><h2>2. 统一 RK4：{math('T=0.01')} 的空间格式比较</h2>
<p>各空间格式均使用 RK4，以 {math(r'\Delta t=10^{-4}')} 从相同的连续初值推进至 {math('T=0.01')}。以该时刻的连续解为参考，计算两个物理场的总误差。高斯与正弦的参考解由完整 DLW 方程的解析构造求得。</p>
<div class="equation">{math(r'E_u(T)=\max_{\mathcal G_u}|u^{\mathrm{num}}(T)-u^*(T)|,\qquad E_v(T)=\max_{\mathcal G_v}|v^{\mathrm{num}}(T)-v^*(T)|.',True)}</div>
<div class="table-wrap"><table id="table-final"><caption>表 2. 统一 RK4 下，各空间格式在 {math('T=0.01')} 的物理场绝对最大误差。</caption>
{table_header(['E_u','E_v'])}
<tbody>{rows(temporal,CASES,METHODS,'error')}</tbody></table></div>
<p>Centered-SD 在四个算例中均给出最小的 {math('v')} 误差。在单孤子和双孤子算例中，它的 {math('u')} 误差均约为 Endpoint-SD 的 36%，{math('v')} 误差分别约为 Endpoint-SD 的 1/72 和 1/70。FD 在这两个孤子算例中给出最小的 {math('u')} 误差。</p>
<p>高斯和正弦算例中，Centered-SD 的 {math('v')} 误差分别为 {math(r'6.967\times10^{-9}')} 和 {math(r'4.706\times10^{-9}')}，约为 FD 的三分之一；Endpoint-SD 给出最小的 {math('u')} 误差。这些结果显示出各空间格式对两个物理场精度的不同影响。</p>
<p class="note">Centered-SD 推进 {math(r'(u,\omega)')} 并由 {math(r'v_k=\Delta_hu_k+2(\omega_k+\omega_{k-1})/h')} 恢复第二场；Endpoint-SD 与 FD 推进 {math('(u,v)')}。各格式使用同一连续解提供初值和边界参考数据。</p>
<p class="note">高斯与正弦在两表中所用参考值的逐点绝对误差均小于 {math('10^{'+str(ref_exponent)+'}')}，包括解析截断与数值求值误差。</p>
<p class="downloads"><a href="{linkroot}/table2_final_field_errors.csv">下载表 2 数据 CSV</a> · <a href="{linkroot}/nondegenerate_rk4_20261024/reference_certificate.json">高斯／正弦参考值误差证书</a></p></section>

<details id="reference-details"><summary>初值、参考解与采样区域</summary>
<h3>高斯与正弦初值</h3>
<p>令 {math(r'z=y+2,\ \kappa=\pi/4')}，两组初值均取 {math(r'u_0=A\sin(\kappa z)F(x)')} 和 {math(r'v_0=4-3A\kappa\cos(\kappa z)F(x)')}。周期高斯取 {math(r'A=0.05,\ F(x)=\sum_{j\in\mathbb Z}\exp[-((x+192j)/6)^2]')}；正弦取 {math(r'A=0.03,\ F(x)=\cos(\pi x/12)')}。关系 {math(r'v_0=4-3\partial_yu_0')} 仅用于初始时刻，之后两个物理场按完整连续方程演化。</p>
<p>两条线性热方程与 Laplace 变换给出相应的连续参考解。解析分母界、截断估计与区间求值共同控制参考误差；构造与适用条件见<a href="report/dlw_nondegenerate_reference_20261024.html">基准说明</a>。</p>
<h3>Centered-SD 的物理场表示</h3>
<p>第 3.2 节的定义给出 {math(r'v_k=\Delta_hu_k+2(\omega_k+\omega_{k-1})/h')}，其中 {math(r'\omega_k=\partial_x\log(g_k/g_{k-1})')}。初始物理场确定相邻 {math(r'\omega')} 的和，配合下端值即可逐点重构。时间推进保留首方程中的 {math(r'\omega_k^2/2-h\omega_k')} 通量，并同时演化辅助场。</p>
<p>参数为 {math(r'a=2,\ \lambda=-2')}。各格式从连续解取初值，并在每个 RK4 阶段使用对应的边界参考数据。</p>
<h3>采样区域</h3>
<p class="case-regions">单孤子与双孤子均取 {math(r'\rho_i=1')}，无相位平移。采样区域为 {math(r'|x|\le R,\ |y|<R')}，分别取 {math('R=5,30')}，包含主要波形。计算边界位于更远处，周期 {math('x')} 区间为 {math('[-L,L)')}，分别取 {math('L=10,40')}。</p>
<p class="case-regions">高斯与正弦使用周期区间 {math(r'x\in[-96,96)')}、{math(r'y\in[-2,2]')}，下边界为 {math('u=0')}。误差在全部 {math('x')} 节点及 {math(r'|y|\le1.8')} 内的各场原生位置上取最大值。</p>
</details>
<footer>数据来源与复现说明：<a href="{linkroot}/README.md">本报告入口</a>。</footer>
</main></body></html>'''

js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));"
rendered=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf8',capture_output=True,check=True)
for i,value in enumerate(json.loads(rendered.stdout)):
    body=body.replace(f'MATHSLOT{i}END',value)
assert 'MATHSLOT' not in body and 'katex-error' not in body
(ROOT/'Report.html').write_text(body,encoding='utf8')
assert hashlib.sha256((ROOT/'dlw-paper.html').read_bytes()).hexdigest()==paper_hash
print(f'Wrote {ROOT / "Report.html"}; {len(spatial)} spatial records, {len(temporal)} time records, {len(maths)} formulas. Main paper unchanged.')
