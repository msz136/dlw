"""Produce cream HTML and Markdown full tables from audited continuous mesh runs."""
import json
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_dynamic_mesh_table import HERE,OUT,PS,ROUTES,TIMES,engine

saved=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
rows=list(saved['rows'].values())
labels=['原可积<br>ρ 动网格','校准可积<br>ρ 动网格','普通同变量<br>ρ 动网格',
        '普通 ALE<br>ρ 动网格','普通 ALE<br>Rₘ 动网格','普通 ALE<br>固定网格']
def get(p,r,method='rk4'):
    return next(row for row in rows if row['spec']['p']==p and row['spec']['route']==r and row['spec']['purpose']==method)
def errors(p,r,method,t,region='core'):
    return get(p,r,method)['snapshots'][str(t)]['errors'][region]
def wrap(headers,body,caption):
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="'+caption+'"><table class="numeric"><caption>'+caption+'</caption><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+str(r[0])+'</th>'+''.join('<td>'+str(v)+'</td>' for v in r[1:])+'</tr>' for r in body)+'</tbody></table></div>'
def table(method,t,region='core'):
    body=[]
    for p in PS:
        ee=[errors(p,r,method,t,region) for r in ROUTES]
        best={f:min(e[f] for e in ee) for f in ('u','rho')}
        cells=[]
        for e in ee:
            cells.append(' / '.join((f'<strong>{e[f]:.3e}</strong>' if e[f]==best[f] else f'{e[f]:.3e}') for f in ('u','rho')))
        body.append([int(p)]+cells)
    return wrap(['p']+labels,body,f'{method.upper()} · t = {t:g} · '+('共同物理核心 [−2, 2]' if region=='core' else '波峰区域 |θ| ≤ 1')+' · 每格 u / ρ')
def ratio(p,a,b,method='rk4',t=.5):
    aa,bb=errors(p,a,method,t),errors(p,b,method,t)
    return ' / '.join(f'{aa[f]/bb[f]:.3f}' for f in ('u','rho'))
ratios=wrap(['p','校准 / 同变量普通','普通 ρ 动格 / 固定格','普通 Rₘ 动格 / 固定格','普通 Rₘ / 普通 ρ 动格'],
            [[int(p),ratio(p,ROUTES[1],ROUTES[2]),ratio(p,ROUTES[3],ROUTES[5]),
              ratio(p,ROUTES[4],ROUTES[5]),ratio(p,ROUTES[4],ROUTES[3])] for p in PS],
            'RK4 · t = 0.5 · 共同核心误差比，u / ρ；小于 1 为改善')
motion=summary['full_step_audit']['rows']
motion_table=wrap(['方案','Euler 更新步数','RK4 更新步数','RK4 最大节点位移'],
            [[labels[i].replace('<br>',' · ')]+[f"{next(r['moving_steps'] for r in motion if r['route']==route and r['method']==m)} / 160" for m in ('euler','rk4')]+[f"{next(r['node_displacement_linf'] for r in motion if r['route']==route and r['method']=='rk4'):.6f}"] for i,route in enumerate(ROUTES)],
            'p = 14，N = 400，Δt = 0.003125；直接检查每一步的节点位置')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                    'figure.facecolor':'#fffdf9','axes.facecolor':'#fffdf9','svg.fonttype':'path'})
fig,axes=plt.subplots(3,1,figsize=(10,6.2),sharex=True,layout='constrained')
for ax,route,title in zip(axes,ROUTES[3:],('Ordinary ALE / rho mesh','Ordinary ALE / Rm mesh','Ordinary ALE / fixed mesh')):
    row=get(14.,route);profile=np.load(row['profile'])
    sol,system,state,_,_=engine.initialize(14.,route,400,4.)
    x0=engine.fields(sol,system,state,0.)[0]
    xx=[x0,profile['t0.25_x'],profile['t0.5_x']]
    keep=np.where((x0>-.65)&(x0<.65))[0]
    for k in keep:ax.plot([x[k] for x in xx],[0,.25,.5],color='#b5aa9b',lw=.5)
    for x,t in zip(xx,(0,.25,.5)):
        mask=(x>-.65)&(x<.65)
        ax.scatter(x[mask],np.full(np.count_nonzero(mask),t),color='#8a5a2b',marker='|',s=58)
    ax.set(title=title,ylabel='time',yticks=[0,.25,.5],ylim=(-.065,.565),xlim=(-.65,.65))
axes[-1].set_xlabel('physical x')
fig.savefig(HERE/'dynamic_mesh_positions.svg',bbox_inches='tight')
fig.savefig(HERE/'dynamic_mesh_positions.pdf',bbox_inches='tight')
fig.savefig(HERE/'dynamic_mesh_positions.png',dpi=160,bbox_inches='tight')
plt.close(fig)
svg=(HERE/'dynamic_mesh_positions.svg').read_text(encoding='utf-8');svg=svg[svg.index('<svg'):]
svg=svg.replace('<svg ','<svg role="img" aria-label="三种普通差分网格在三个时刻的实际节点位置" ',1)

body=r'''
<header id="top"><div class="eyebrow">2HS 数值实验 · 持续动网格完整对照</div><h1>把持续动网格放进同一张大表</h1><p class="subtitle">13 个参数 · 六种方案 · Euler / RK4 · u 与 ρ 同格</p><p class="date">2026 年 9 月 26 日 · N = 400，Δt = 0.003125</p></header>
<p class="lede">每种动网格方案都将位置或格距与场变量一起推进，持续到终点。这里比较完整演化后的连续解总误差，保持之前的表格形式：每行一个 $p$，每格先 $u$、后 $\rho$。</p>
<div class="key"><p><strong>先明确已有结果：</strong>原可积、校准可积和同变量普通差分，本来就在按 $\dot x_k=-u_k$ 持续移动网格。上一轮约 41% 的全域 $u$ 改善和约 57% 的峰区改善已包含这部分运动。此次补齐普通 $\rho$ 动网格列，并把旧九参数与新参数合并；没有把已有结果重新算作额外动网格收益。</p><p>本轮大表显示：$R_m$ 持续动网格的 $\rho$ 精度收益较稳定；$u$ 的收益随参数和时间改变。普通 $\rho$ 动网格在这批共同核心主比较中，两场均未胜固定网格。</p></div>
<nav class="toc" aria-label="报告目录"><p>直接查看</p><ol><li><a href="#euler">Euler 大表</a><small>t = 0.25 与 0.5</small></li><li><a href="#rk4">RK4 大表</a><small>t = 0.25 与 0.5</small></li><li><a href="#mesh">网格怎样持续移动</a><small>GSG 做法、2HS 网格方程、实际位置</small></li><li><a href="#comparison">误差比与核查</a><small>收益范围、加密及时间敏感性</small></li></ol></nav>
<section class="part" id="setup"><h2>表格怎样读</h2>
<p>固定 $c_{\rm phys}=1$，使用连续光滑单孤子的同一解析参照。主表取共同物理核心 $[-2,2]$，在 16001 个公共物理点上比较分段线性重构后的最大绝对误差。未校准 / 校准 / 普通同变量三路的初态哈希相同，且共用左端闭合；普通 ALE 三路共用场差分、Poisson 求解和物理边界，只采用不同的完整网格方案。</p>
<p>三条同变量路线从均匀质量坐标 $X\in[-4,4]$ 出发，$a=0.02$；普通 ALE 使用物理区间 $[-4,4]$，以相应密度作初始等分并随后持续推进。初始布点是完整方案的一部分，没有增加“仅初始调整、随后冻结”的实验组。ALE 两端固定，内部点按网格速度移动；同变量三路的端点遵循其开链规则，因此跨这两类实现的比较是完整方案比较。</p>
<p><strong>所有格子均为 $u\;/\;\rho$；粗体表示该行该物理场的最小误差。</strong>两场分别标记，不能据单个粗体判定一条方案双场都最优。误差包括空间、时间及重构贡献。宽表在窄屏上可横向滚动。</p></section>
<section class="part" id="euler"><div class="part-label">一阶时间推进</div><h2>Euler：持续动网格大表</h2>
@@EULER025@@
@@EULER05@@
</section>
<section class="part" id="rk4"><div class="part-label">四阶时间推进</div><h2>RK4：同样的空间与网格配置</h2>
@@RK4025@@
@@RK405@@
<details><summary>展开对应的波峰区域大表</summary><p>区域沿用上一轮预先确定的 $|\theta|\le1$，中心为连续孤子的解析峰位，仅用于评价；没有在求解过程中拟合、平移或修正数值相位。</p>@@PEAKTABLES@@</details>
</section>
<section class="part" id="mesh"><div class="part-label">与 GSG 一致的持续更新思路</div><h2>场变量与网格同时推进</h2>
<p>GSG 原文 §4 的 Scheme 1–4 都在每个时间步更新场差 $p_k$ 和格距 $\delta_k$；例如 Scheme 3 的式 (4.8) 是</p>
<div class="mathblock">$$\delta_k^{n+1}=\delta_k^n+\Delta t(\cos u_{k+1}^n-\cos u_k^n).$$</div>
<p>因此我们沿用“网格是演化未知量、与场耦合更新”的方式。2HS 的速度由自身守恒关系决定；GSG 的余弦速度属于另一套方程，不能直接代入 2HS。本表 Euler / RK4 推进的是现有 2HS 半离散系统，并非逐字复现 GSG 的半隐式时间公式。</p>
<h3>三种网格更新规则</h3>
<div class="mathblock">$$\begin{aligned}
\rho\text{ 网格}:&\quad \dot x_k=-u_k,\qquad\dot d_k=-(u_{k+1}-u_k),\\
R_m\text{ 网格}:&\quad \dot x_k=-u_k-\frac{\rho_k-1}{2R_{m,k}},
\qquad R_m=\frac{m}{2\rho},\quad m=u_{xx}+2,\\
\text{固定网格}:&\quad\dot x_k=0.
\end{aligned}$$</div>
<p>$\rho$ 满足 $\rho_t=(u\rho)_x$；由 2HS 方程可得 $(R_m)_t=(uR_m+\rho/2)_x$。取远场零网格通量后，上式第二行就是相应的守恒密度运动速度。每个时间步、每个 RK4 阶段，都使用当前数值场更新速度，而不是按精确解预先规定轨迹。</p>
<p>原可积与校准可积的 $\dot d=-v$ 是其半离散方程的一部分；因此表中两者使用原生 $\rho$ 网格。若把它强行替换成 $R_m$ 速度，就已经改变这套可积离散方程。这里比较有明确方程定义的六条方案，没有虚构“同一可积式任意换网格”的组合。</p>
@@MOTION@@
<figure>@@FIGURE@@<figcaption>p = 14、RK4；短竖线是 t = 0、0.25、0.5 的实际数值节点位置，细线连接同一个节点的三个位置。图只展示中心区域；逐步核查覆盖全部 160 步。</figcaption></figure>
</section>
<section class="part" id="comparison"><div class="part-label">收益放在哪个量上</div><h2>Rₘ 帮助 ρ，u 仍需要分参数判断</h2>
@@RATIOS@@
<p>在 13 个参数 × 两种时间算法 × 两个时刻的 <strong>52 个共同核心主比较</strong>中，普通 $R_m$ 相对普通固定网格的 $\rho$ 误差全部更小，$u$ 则有 24 个更小；普通 $R_m$ 相对普通 $\rho$ 动网格，两场在 52 个比较中都更小。这些格子共享参数和轨道，不是 52 个独立统计样本，也不产生新的统计显著性结论。</p>
<p>例如 RK4、$p=22$、$t=0.5$：$R_m$ 动网格的 $\rho$ 误差为固定网格的 0.536 倍，降低约 46%；但 $u$ 误差为 2.933 倍。另一个方向，校准可积相对同变量普通差分仍保留此前的 $u$ 优势，却尚未优于固定 / $R_m$ 普通 ALE 的绝对精度。</p>
<p>因此当前可并列保留两项结论：<strong>校准改善可积式的 $u$ 误差；选择 $R_m$ 持续动网格改善普通差分的 $\rho$ 误差。</strong>它们目前在不同方案中实现，不能把两个百分比相乘，或直接声称已经得到同时享有两项收益的可积算法。</p>
<h3>数值可信度与控制实验</h3>
<p>本表含 156 条主轨道；连同空间加密、时间减半与扩域共 414 条记录，其中 392 条是源码哈希和参数完全匹配的已有轨道，22 条为此次补算的普通 $\rho$ 动网格。所有记录重新用同一稳健反演和公共评价点计算两场误差。另新增 12 条逐步网格核查；没有改写旧冻结求解器。</p>
@@VALIDATION@@
<p>四组配对分别是校准 / 同变量普通、普通 $R_m$ / 固定、普通 $\rho$ / 固定、普通 $R_m$ / 普通 $\rho$。空间加密、RK4 减步、扩域和评价点加密均未改变这些配对的胜负方向。Euler 减步有 12 个单场区域比较翻转，全部发生在 $u$；例如 $p=3$ 的普通 $R_m$ / 固定格，或 $p=10$、$t=0.25$ 的校准 / 同变量普通。因此不能把粗 Euler 的所有细小优势解释为空间或动网格优势。</p>
<p>这里没有做运行成本等价比较，结论限于给定 $N$、$\Delta t$、精确边界和光滑单孤子族。局部与全域结果都保留在数据中。</p>
<p class="download"><a href="DYNAMIC_MESH_REPORT.md">Markdown 大表</a> · <a href="out_dynamic_mesh/all_errors.csv">全部误差 CSV</a> · <a href="out_dynamic_mesh/results.json">逐轨道数据与来源</a> · <a href="out_dynamic_mesh/summary.json">配对比值及敏感性</a> · <a href="out_dynamic_mesh/motion_audit.json">逐步运动核查</a> · <a href="dynamic_mesh_positions.pdf">网格图 PDF</a></p>
</section>
<footer><p><a href="index.html">返回误差系数理论报告</a> · <a href="../../Paper/sources/gsg.txt">GSG 原文文本 §4</a> · <a href="run_dynamic_mesh_table.py">运行脚本</a> · <a href="summarize_dynamic_mesh.py">读回验证</a> · <a href="build_dynamic_mesh.ps1">构建脚本</a> · <a href="#top">回到顶部</a></p></footer>
'''
validation=wrap(['检查','结果'],[
 ['空间加密','N = 400 → 800；普通 ρ 动网格观测阶 1.851–2.082，Rₘ 为 1.954–2.021'],
 ['RK4 减步',f"N = 800，Δt 减半；误差相对变化最多 {summary['controls']['time']['max_relative_error_change']:.2e}"],
 ['评价点加密',f"16001 → 32001；误差相对变化最多 {100*summary['max_eval_relative_change']:.3f}%；配对方向无翻转"],
 ['扩域',f"p = 3、8、20、22；L = 4 → 5，N = 400 → 500；跨路线误差变化最多 {100*summary['controls']['domain']['max_relative_error_change']:.2f}%"],
 ['Euler 减步','Δt = 0.003125 → 0.0015625；12 个 u 比较翻转，ρ 比较未翻转'],
 ['实际运动','12 条逐步核查：五种动网格各 160 / 160 步移动，固定格 0 / 160 步'],
 ['正性',f"全部记录最小格距 {summary['min_h']:.6f}，最小密度 {summary['min_rho']:.6f}"],
 ],'核查覆盖共同核心及波峰区域、u 与 ρ；所有轨道完成。')
replacements={'EULER025':table('euler',.25),'EULER05':table('euler',.5),
              'RK4025':table('rk4',.25),'RK405':table('rk4',.5),
              'PEAKTABLES':''.join(table(m,t,'peak') for m in ('euler','rk4') for t in TIMES),
              'MOTION':motion_table,'FIGURE':svg,'RATIOS':ratios,'VALIDATION':validation}
for k,v in replacements.items():body=body.replace('@@'+k+'@@',v)
theme=(HERE.parent/'gsg_project/dlw_report/_src/miura_dlw.src.html').read_text(encoding='utf-8')
theme=re.findall(r'<style>([\s\S]*?)</style>',theme)[1]
extra='''.page{max-width:1160px;padding-inline:52px}table.numeric{font-size:.82rem;font-variant-numeric:tabular-nums}table.numeric td{white-space:nowrap;padding:9px 8px}table.numeric tbody th{border-top:0;font-weight:normal}caption{text-align:left;color:var(--muted);font-size:.87rem;margin-bottom:10px}.table-wrap:focus-visible{outline:2px solid var(--accent)}figure{margin:28px 0}figure svg{max-width:100%;height:auto;display:block}figcaption,.download{font-size:.86rem;color:var(--muted)}@media(max-width:700px){.page{padding-inline:22px}.table-wrap{margin-inline:-8px}table.numeric{font-size:.82rem}}'''
header='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="2HS 六种持续动网格与固定网格方案，13参数、Euler/RK4的双场总误差大表。"><title>2HS 持续动网格大表</title><style>@@KATEX_CSS@@</style><style>'''+theme+extra+'''</style></head><body><a class="skip" href="#main">跳到正文</a><main id="main" class="page">'''
footer='''</main><script>@@KATEX_JS@@</script><script>document.addEventListener('DOMContentLoaded',function(){renderMathInElement(document.querySelector('main'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],ignoredTags:['script','noscript','style','textarea','pre','code','option'],throwOnError:false});});</script></body></html>'''
(HERE/'_src/dynamic_mesh.src.html').write_text(header+body+footer,encoding='utf-8')

md=['# 2HS：持续动网格大表','',
    '2026-09-26。N=400，dt=0.003125，c_phys=1。每格为 u / rho 的连续解总误差；共同物理核心 [-2,2]，16001 点评价。',
    '',
    '原可积、校准可积、普通同变量三路原本就使用持续 rho 动网格。普通 ALE 三路分别使用持续 rho 网格、持续 R_m 网格及固定网格；没有仅初始布点分组。',
    '',
    '主表 156 条轨道；含控制共 414 条（复用 392，补算 22），另有 12 条逐步运动核查。全部完成。',
    '']
for method in ('euler','rk4'):
    for t in TIMES:
        md += [f'## {method.upper()}，t={t:g}','',
               '| p | 原可积＋rho动格 | 校准可积＋rho动格 | 普通同变量＋rho动格 | 普通ALE＋rho动格 | 普通ALE＋Rm动格 | 普通ALE＋固定格 |',
               '|---:|---:|---:|---:|---:|---:|---:|']
        for p in PS:
            cells=[' / '.join(f'{errors(p,r,method,t)[f]:.3e}' for f in ('u','rho')) for r in ROUTES]
            md.append('| '+str(int(p))+' | '+' | '.join(cells)+' |')
        md+=['']
md += ['## 结论与限制','',
       '- 52个主比较（13参数×2时间算法×2时刻）中，Rm/固定网格的rho误差52个改善，u误差24个改善；这些比较不独立，不是新统计检验。',
       '- 普通rho动网格在这52个主比较中，两场均未优于固定网格；Rm相对rho动网格则两场全部改善。',
       '- 原可积和校准式的rho网格是其方程组成部分，不能直接改成Rm速度后仍称同一可积格式。',
       '- 网格加密、RK4减步、评价加密和扩域不改变四组配对方向。Euler减步出现12个u比较翻转，rho无翻转。',
       '- 校准与同变量普通的比较保持已有u优势；跨可积/普通ALE的比较还含变量、密度位置及边界闭合差异。',
       '',
       '详细峰区表、运动图、方程和核验见 [HTML](DYNAMIC_MESH_REPORT.html)。原始数据：`out_dynamic_mesh/`。',
       '']
(HERE/'DYNAMIC_MESH_REPORT.md').write_text('\n'.join(md),encoding='utf-8')
print(HERE/'_src/dynamic_mesh.src.html')
