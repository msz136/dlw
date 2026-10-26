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

preserved = read(HERE / 'preservation.json')
paper_hash = hashlib.sha256((ROOT / 'dlw-paper.html').read_bytes()).hexdigest()
assert paper_hash == preserved['paper_sha256'], 'Main paper changed since this report task started'
assert (ROOT / preserved['report_backup']).exists()

spatial = [r for r in read(RUN/'baselines.json') if r['h'] == .1 and r['dx'] == .1]
spatial += [read(RUN/f'spatial_{c}_0.1_0.1.json') for c in 'ABCD']
spatial += read(HERE/'initial_nonsoliton.json')
temporal = read(HERE/'rk4_spatial/results.json')
certificates = read(HERE/'initial_non_soliton_reference_certificate.json')
assert len(spatial) == 18 and len(temporal) == 12
assert all(r['status']=='complete' and r['h']==.1 and r['dx']==.1 for r in spatial+temporal)
assert all(r['T']==.01 and r['dt']==1e-4 and r['reached']==.01 and r['integrator']=='RK4' for r in temporal)
assert all(float(r['rigorous_uniform_sample_bound_ut'])<=1e-14 and float(r['rigorous_uniform_sample_bound_vt'])<=1e-14 for r in certificates)

with (HERE/'table1_initial_derivative_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['case','method','h','dx','t','error_ut','error_vt'])
    for r in spatial: w.writerow([r['case'],r['method'],r['h'],r['dx'],0,*r['total']])
with (HERE/'table2_final_field_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['case','space','integrator','h','dx','dt','T','error_u','error_v'])
    for r in temporal: w.writerow([r['case'],r['method'],r['integrator'],.1,.1,1e-4,.01,*r['error']])

labels = {
    'A': ('A','单孤子 · (1, 2)'), 'B': ('B','单孤子 · (4, −3)'),
    'C': ('C','双孤子 · (6, −5), (4, −3)'), 'D': ('D','双孤子 · (1, 2), (4, −3)'),
    'Gaussian': ('周期高斯','解析初值'), 'Sinusoidal': ('正弦','解析初值')}
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

linkroot='Workspaces/dlw_paper_20261009/report_refresh_20261024'
body=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DLW 初始导数与短时物理场误差</title>
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
<header><p class="eyebrow">DLW · Numerical comparisons · 2026-10-24</p>
<h1>初始导数与短时物理场误差</h1>
<p class="lead">先比较相同初始物理场下各空间格式给出的时间导数，再统一使用 RK4，比较三种空间格式对四个孤子的短时演化。其中 Centered-SD 均采用当前的完整势表示。</p>
<p class="meta">共同空间参数：{math(r'h=\Delta x=0.1')}。{math('x')} 方向采用 Fourier 微分。表中粗体标记同一算例、同一分量在所列方法中的最小值；显示精度相同时并列加粗。</p></header>

<section id="initial-rates"><h2>1. {math('t=0')}：初始时间导数误差</h2>
<p>将同一连续初值采样到各格式的物理场位置，计算其给出的 {math('u_t,v_t')}，并与连续方程的解析初始右端比较。初始物理场误差为零，表 1 测量的是时间导数的空间离散缺陷。</p>
<div class="equation">{math(r'E_{u_t}=\max_{\mathcal G_u}|u_t^{\mathrm{num}}(0)-u_t^{\mathrm{ref}}(0)|,\qquad E_{v_t}=\max_{\mathcal G_v}|v_t^{\mathrm{num}}(0)-v_t^{\mathrm{ref}}(0)|.',True)}</div>
<div class="table-wrap"><table id="table-initial"><caption>表 1. 初始时间导数的绝对最大误差，{math(r'h=\Delta x=0.1')}。</caption>
<thead><tr><th rowspan="2" scope="col">算例</th><th colspan="2" scope="colgroup">Endpoint-SD</th><th colspan="2" scope="colgroup">Centered-SD</th><th colspan="2" scope="colgroup">FD</th></tr>
<tr><th scope="col">{math('E_{u_t}')}</th><th scope="col">{math('E_{v_t}')}</th><th scope="col">{math('E_{u_t}')}</th><th scope="col">{math('E_{v_t}')}</th><th scope="col">{math('E_{u_t}')}</th><th scope="col">{math('E_{v_t}')}</th></tr></thead>
<tbody>{rows(spatial,['A','B','C','D','Gaussian','Sinusoidal'],['Endpoint-SD','Centered-SD','FD'],'total')}</tbody></table></div>
<p class="note">{math(r'\mathcal G_u,\mathcal G_v')} 是各物理场在指定区域内的原生采样点。两个 SD 格式的 {math('v')} 位于边中点，FD 的 {math('v')} 位于节点。最大值取这些采样点，未作连续区域最大值的区间包围。</p>
<p><strong>高斯和正弦在这一时刻有可保证精度的解析参考值。</strong>它们由给定初值直接代入连续方程得到，无需数值时间推进。逐点区间复核给出的参考求值误差均小于 {math('10^{-14}')}，包括周期高斯无穷求和的截断尾项；远小于表中最小约 {math(r'8.9\times10^{-7}')} 的缺陷。</p>
<p class="note">这里的 {math('10^{-14}')} 只保证解析参考值的求值，不包括离散算法的浮点舍入与辅助变量求解误差，也不代表正时间连续解已得到认证。</p>
<p>六个算例中，Centered-SD 与 Endpoint-SD 的初始 {math('u_t')} 误差在显示精度内一致。{math('v_t')} 的表现随初值改变：Centered-SD 在 A、D 中最小，FD 在 B、C、高斯和正弦中最小。</p>
<p class="downloads"><a href="{linkroot}/table1_initial_derivative_errors.csv">下载表 1 数据 CSV</a> · <a href="{linkroot}/initial_non_soliton_reference_certificate.json">高斯与正弦参考求值界</a></p></section>

<section id="final-fields"><h2>2. 统一 RK4：{math('T=0.01')} 的空间格式比较</h2>
<p>Endpoint-SD、Centered-SD 和 FD 均使用 RK4，固定 {math(r'h=\Delta x=0.1')}、{math(r'\Delta t=10^{-4}')}，从相同的连续初始物理场推进至 {math('T=0.01')}。参考值为同一时刻的连续精确孤子解。</p>
<div class="equation">{math(r'E_u(T)=\max_{\mathcal G_u}|u^{\mathrm{num}}(T)-u^*(T)|,\qquad E_v(T)=\max_{\mathcal G_v}|v^{\mathrm{num}}(T)-v^*(T)|.',True)}</div>
<div class="table-wrap"><table id="table-final"><caption>表 2. 统一 RK4 下，三种空间格式在 {math('T=0.01')} 的物理场绝对最大误差。</caption>
<thead><tr><th rowspan="2" scope="col">算例</th><th colspan="2" scope="colgroup">Endpoint-SD</th><th colspan="2" scope="colgroup">Centered-SD</th><th colspan="2" scope="colgroup">FD</th></tr>
<tr><th scope="col">{math('E_u')}</th><th scope="col">{math('E_v')}</th><th scope="col">{math('E_u')}</th><th scope="col">{math('E_v')}</th><th scope="col">{math('E_u')}</th><th scope="col">{math('E_v')}</th></tr></thead>
<tbody>{rows(temporal,list('ABCD'),['Endpoint-SD','Centered-SD','FD'],'error')}</tbody></table></div>
<p>Endpoint-SD 与 FD 推进 {math('(u,v)')}；Centered-SD 推进 {math('(u,w)')}，再按完整势映射恢复 {math('v')}。各格式使用相同的连续初值和边界参考数据，误差在各物理场的原生位置上计算。</p>
<p class="note">表 2 比较统一 RK4 下三种空间格式的实际演化结果。所列值是最终物理场总误差，仍包含固定时间步长及各自变量表示、边界闭合的影响，不是单独抽出的空间截断误差。全部十二组结果均已保存并重新核对。</p>
<p class="downloads"><a href="{linkroot}/table2_final_field_errors.csv">下载表 2 数据 CSV</a> · <a href="{linkroot}/rk4_spatial/results.json">RK4 比较数据与核验</a></p></section>

<details id="reference-details"><summary>初值、解析参考与采样区域</summary>
<h3>高斯与正弦的解析初始右端</h3>
<p>参数为 {math(r'a=2,\ \lambda=-2')}。令 {math(r'e(y)=\sin[\kappa(y+2)]')}，{math(r'\kappa=\pi/4')}，写作 {math(r'u_0=Ae(y)F(x),\quad v_0=Be(y)H(x)')}。</p>
<ul class="profiles"><li>周期高斯：{math(r'A=0.05,\ B=0.03,\quad F=H=G_{\mathrm{per}}(x)=\sum_{m\in\mathbb Z}e^{-((x+192m)/6)^2}')}。</li>
<li>正弦：{math(r'A=0.03,\ B=0.02,\quad F(x)=\cos(\pi x/12),\quad H(x)=\sin(\pi x/12)')}。</li></ul>
<p>采用 {math(r'u(x,-2,t)=0')} 的下边界条件，并令 {math(r'P(y)=\int_{-2}^{y}e(s)\,ds=[1-\cos(\kappa(y+2))]/\kappa')}。连续方程确定的精确初始右端为</p>
<div class="equation">{math(r'\begin{aligned}u_t^{\mathrm{ref}}(0)&=-BP(y)H^{\prime\prime}(x)-Ae(y)\,[Ae(y)F(x)+4]F^\prime(x),\\v_t^{\mathrm{ref}}(0)&=-Ae^\prime(y)F^{\prime\prime}(x)-ABe(y)^2[F^\prime H+FH^\prime]-4Be(y)H^\prime(x)+4Ae(y)F^\prime(x).\end{aligned}',True)}</div>
<p class="note">严格说，表 1 检验的是连续方程在给定初值上的右端。如果相应经典解存在，这就是它的初始时间导数。该右端的解析求值不依赖正时间解的存在性或误差认证。区间核验使用 80 位十进制精度，对每个算例检查 380,160 个导数值；周期高斯遗漏尾项对参考导数的贡献小于 {math('10^{-990}')}。</p>
<h3>区域与参考口径</h3>
<p class="case-regions">孤子 A、B、C、D 的谱参数已列于表中，均取 {math(r'\rho_i=1')} 且无相位平移。区域为 {math(r'|x|\le R,\ |y|<R')}，依次取 {math('R=5,10,30,30')}，包含主要波形；计算边界位于更远处。对应周期 {math('x')} 区间为 {math('[-L,L)')}，{math('L=10,20,40,40')}。两张表中的孤子结果使用相同区域。</p>
<p class="case-regions">高斯与正弦采用周期 {math(r'x\in[-96,96)')}、{math(r'y\in[-2,2]')}；表 1 在全部 {math('x')} 节点及 {math(r'|y|\le1.8')} 的原生场位置上取最大值。边中点与节点分别按各格式的物理场位置采样。</p>
<p class="note">孤子参考由连续 τ 函数解析公式计算，末时数据已重新复核。高斯与正弦的 {math('10^{-14}')} 区间求值界只适用于本次核验的初始参考采样值，未扩展为孤子求值或整个数值算法的区间认证。</p>
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
