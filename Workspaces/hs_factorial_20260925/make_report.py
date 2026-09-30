"""Render the completed comparison from saved JSON, never rerun solvers."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'
data=json.loads((OUT/'factorial_results.json').read_text(encoding='utf-8'))
spatial=json.loads((OUT/'spatial_audit.json').read_text(encoding='utf-8'))
domain=json.loads((OUT/'domain_audit.json').read_text(encoding='utf-8'))
SPACES=('integrable_moving','ordinary_moving','fixed_difference')
METHODS=('euler','heun','rk4','rk8')
NAMES={'integrable_moving':'论文可积半离散＋ρ 动网格',
       'ordinary_moving':'普通差分＋ρ 动网格',
       'fixed_difference':'固定物理网格差分'}
MNAMES={'euler':'Euler（1）','heun':'Heun（2）','rk4':'RK4（4）','rk8':'DOP853 主公式（8）'}
PLOT_NAMES={'integrable_moving':'Integrable semi-discrete + rho mesh',
            'ordinary_moving':'Ordinary difference + rho mesh',
            'fixed_difference':'Fixed-grid difference'}
PLOT_METHODS={'euler':'Euler (1)','heun':'Heun (2)',
              'rk4':'RK4 (4)','rk8':'DOP853 (8)'}
COLORS={'euler':'#aa3a3a','heun':'#b77b1f','rk4':'#2a7391','rk8':'#654e9c'}

def row(space,method,dt):
    return next(x for x in data['rows'] if x['space']==space and
                x['method']==method and x['dt_requested']==dt)

plt.rcParams.update({'font.family':'DejaVu Sans','axes.grid':True,'grid.alpha':.25,
                     'font.size':10,'figure.dpi':150})
fig,axes=plt.subplots(2,3,figsize=(13,7),sharex=True)
for col,s in enumerate(SPACES):
    for m in METHODS:
        rr=[row(s,m,dt) for dt in (.05,.025,.0125,.00625)]
        for line,field in enumerate(('u_linf','rho_linf')):
            vals=[r['observations']['0.25']['common']['core'][field] for r in rr]
            axes[line,col].loglog([.05,.025,.0125,.00625],vals,'o-',
                    color=COLORS[m],label=PLOT_METHODS[m],lw=1.4,ms=3)
    axes[0,col].set_title(PLOT_NAMES[s])
    axes[1,col].set_xlabel('Time step')
axes[0,0].set_ylabel('Common-core max error: u')
axes[1,0].set_ylabel('Common-core max error: rho')
axes[0,0].legend(fontsize=7)
fig.suptitle('2HS: total error versus time step, T=0.25')
fig.tight_layout()
fig.savefig(OUT/'fig1_total_error.png',bbox_inches='tight')
plt.close(fig)

fig,axes=plt.subplots(1,3,figsize=(13,3.8),sharex=True)
for ax,s in zip(axes,SPACES):
    for m in METHODS:
        rr=[row(s,m,dt) for dt in (.05,.025,.0125,.00625)]
        ax.loglog([.05,.025,.0125,.00625],
                  [r['temporal_state_linf'] for r in rr],'o-',
                  color=COLORS[m],label=PLOT_METHODS[m],lw=1.4,ms=3)
    ax.set_title(PLOT_NAMES[s]);ax.set_xlabel('Time step')
axes[0].set_ylabel('State error vs same-model fine RK8')
axes[0].legend(fontsize=7)
fig.suptitle('Time integration separated from spatial/model error')
fig.tight_layout()
fig.savefig(OUT/'fig2_temporal_error.png',bbox_inches='tight')
plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(9,4))
for s in SPACES:
    rr=sorted([r for r in spatial['rows'] if r['space']==s],key=lambda r:r['edges'])
    for ax,field in zip(axes,('u_linf','rho_linf')):
        ax.loglog([r['edges'] for r in rr],[r['core'][field] for r in rr],
                  'o-',label=PLOT_NAMES[s],lw=1.5)
for ax,title in zip(axes,('u','rho')):
    ax.set_title(title);ax.set_xlabel('Number of physical intervals')
    ax.set_ylabel('Common-core max error')
axes[0].legend(fontsize=8)
fig.suptitle('Spatial refinement at fixed RK8 step')
fig.tight_layout()
fig.savefig(OUT/'fig3_spatial_refinement.png',bbox_inches='tight')
plt.close(fig)

lines=['# 2HS：三种空间方法 × 四种时间推进的实际数值对照','',
'2026-09-25。本报告来自本轮新运行的 48 条时间步扫描轨道、3 条同空间模型精细时间参照、9 条空间加密轨道和 6 条区域扩大核查。完整逐次数据见 [主数据](out/factorial_results.json)、[空间加密](out/spatial_audit.json)、[区域检查](out/domain_audit.json)。代码入口为 [主实验](run_factorial.py)、[空间检查](spatial_audit.py)、[区域检查](domain_audit.py)、[图表生成](make_report.py)。',
'',
'## 1. 固定了什么，为什么','',
'| 固定项 | 本轮取值 | 依据与作用 |','|---|---|---|',
'| 原方程分支 | 2HS 原文式 (11) 的负 μ、光滑正密度分支 | 与现有论文半离散解和数值程序一致；不推广到其他符号分支 |',
'| 孤子参数 | c=1，p=5，q=1.25；相位与平移常数为 0 | 原论文图 1/3 使用的光滑单孤子组；q=p/(cp−1) 满足约化 |',
'| 初态 | t=0 的同一连续孤子场，采样到各方法的自然节点 | 排除可积格式用自身有限格距精确初值所获得的特殊优势；固定网格在物理 x 点采样，动网格在等距 X 标签采样 |',
'| 空间预算 | 400 个区间、401 个节点；动网格 a=.02 且 X∈[−4,4]，固定网格 Δx=.02 且 x∈[−4,4] | 相同格点数与名义标尺；动网格的物理右端在 t=0 约 4.6，因此主比较使用共同内部 x∈[−2,2] |',
'| 终点与观察 | t=.05、.10、.25；t=.25 为主表 | 光滑短时窗，已有审计显示此时两种动网格完成且可做空间加密；三个时刻防止只看单一终点 |',
'| 时间步 | 主表 Δt=.00625；另外 .05、.025、.0125、.00625 | 四档都是观察时刻的整除步长；共同主表控制时间步，扫描单独估计时间误差 |',
'| 精细时间参照 | 各自空间模型以固定步长 DOP853 八阶主公式、Δt=.000390625 积分 | 只用于同一半离散 ODE 的时间误差；不当作连续 2HS 真解 |',
'| 边界 | 动网格每级施加左端连续精确 u；固定网格每级施加两端连续精确 u 与 ρ/m 幽灵数据 | 沿用现有三个已核验求解器；这是三条路线尚未完全同边界的限制，区域扩大检查提供敏感度信息 |',
'| 误差区域 | 共同物理核心 x∈[−2,2]，801 个评价点；另有 [−3.5,3.5] 与各自原生节点 | 避免不同网格节点处最大值的采样偏差；离边界保持距离 |',
'',
'初始 u 最大偏差：三路线均低于 4.2×10⁻¹⁵。动网格初始边平均密度与连续精确边平均值的最大差约 4.53×10⁻¹⁴；固定网格的 ρ 初态按连续点值精确采样。动网格保持 a=ρ_k d_k 是变量重构恒等式，不能作为精度证据。所有 48 条扫描轨道都到达 t=.25，且没有拒步。',
'',
'## 2. 十二个组合：共同物理核心的连续解总误差','',
'每个主表数值是 t=.25、Δt=.00625 的 L∞ 误差。u 在动网格节点，ρ 在格边平均；为了作共同点比较，对 u 用三次样条，对边平均 ρ 先作二阶导数修正再用三次样条。固定网格的 ρ 在节点。所有方案用同样的 801 个物理点；重构地板见 §4。这里的总误差同时包含空间模型与时间推进误差。',
'',
'| 空间方法 | 时间法 | u 核心 L∞ | ρ 核心 L∞ | u 原生节点 L∞ | ρ 原生位置 L∞ | 同模型时间误差* | 推进秒数 |',
'|---|---|---:|---:|---:|---:|---:|---:|']
for s in SPACES:
    for m in METHODS:
        r=row(s,m,.00625); z=r['observations']['0.25']
        co=z['common']['core'];nat=z['native']
        lines.append(f"| {NAMES[s]} | {MNAMES[m]} | {co['u_linf']:.6g} | {co['rho_linf']:.6g} | {nat['u_linf']:.6g} | {nat['rho_linf']:.6g} | {r['temporal_state_linf']:.3g} | {r['seconds']:.3f} |")
lines += ['', '*同模型时间误差是最终状态向量相对于该空间模型精细时间参照的最大差，不是场的连续解误差。三种空间模型的状态变量不同，其时间误差数值只用于各自时间收敛判断。秒数来自本机一次推进，包含右端/边界计算，不含参照评估、重构和画图；单次计时只作成本线索。',
'',
'![总误差与时间步](out/fig1_total_error.png)',
'',
'## 3. 时间阶与空间误差地板','',
'下表给出同一空间模型状态向量相对精细时间参照的四档误差；括号中的 p 是最后两个非地板点的 log₂ 误差比。它检验时间推进；不要从总误差曲线直接读时间阶。',
'',
'| 空间方法 | 方法 | Δt=.05 | .025 | .0125 | .00625 | 末级观测 p |',
'|---|---|---:|---:|---:|---:|---:|']
for s in SPACES:
    for m in METHODS:
        vals=[row(s,m,dt)['temporal_state_linf'] for dt in (.05,.025,.0125,.00625)]
        p=math.log2(vals[-2]/vals[-1]) if vals[-1]>3e-14 and vals[-2]>3e-14 else None
        label=f'{p:.3f}' if p is not None else '舍入地板'
        lines.append(f"| {NAMES[s]} | {MNAMES[m]} | " +
                     ' | '.join(f'{v:.3g}' for v in vals) + f' | {label} |')
lines += ['',
'一阶 Euler 的末级观测阶接近 1，二阶 Heun 接近 2，RK4 接近 4。DOP853 在这些短时步长上已触及约 10⁻¹⁴ 的浮点地板，**本表不能从观测误差单独确认八阶**；“八阶”指其所用 DOP853 主步进公式的已知形式阶。主表中 RK4 与 DOP853 的连续解总误差几乎重合，说明空间/模型误差主导，增加时间阶没有明显改善该设置下的总误差。',
'',
'![同模型时间误差](out/fig2_temporal_error.png)',
'',
'## 4. 空间加密、边界与重构检查','',
'以同一 RK8、Δt=.00625、t=.25，保持初态、参数、共同核心区域和边界定义，空间区间数取 200、400、800（对应 a 或 Δx 为 .04、.02、.01）：','',
'| 空间方法 | u: 200 / 400 / 800 | u 末级观测阶 | ρ: 200 / 400 / 800 | ρ 末级观测阶 |',
'|---|---:|---:|---:|---:|']
for s in SPACES:
    rr=sorted((r for r in spatial['rows'] if r['space']==s),key=lambda r:r['edges'])
    u=[r['core']['u_linf'] for r in rr];rh=[r['core']['rho_linf'] for r in rr]
    lines.append(f"| {NAMES[s]} | " + ' / '.join(f'{z:.3g}' for z in u) +
                 f" | {math.log2(u[1]/u[2]):.3f} | " +
                 ' / '.join(f'{z:.3g}' for z in rh) +
                 f" | {math.log2(rh[1]/rh[2]):.3f} |")
lines += ['',
'这组单孤子下，论文半离散模型相对连续解约一阶；普通动网格与固定差分约二阶。这是有限范围的观测阶，不是普遍误差定理。两种动网格的质量密度在波峰附近低于背景，**自然网格在峰处更疏**，不能把差异解释为峰处自动加密。',
'',
'![空间加密](out/fig3_spatial_refinement.png)',
'',
't=.25 主表的共同核心重构地板：动网格 u <4.8×10⁻⁹、ρ <9.1×10⁻⁹；固定网格 u <8.1×10⁻¹⁰、ρ <3.3×10⁻⁹。数值来自对同一精确场先采样再按完全相同流程重构，与真正误差分开。固定网格 u 的主误差约 6.34×10⁻⁷，重构地板比它低约三个数量级。',
'',
'固定 a=.02、Δx=.02 将计算半宽从 4 扩到 5，仍在 [-2,2] 比较：','',
'| 空间方法 | 半宽 4: u / ρ | 半宽 5: u / ρ |',
'|---|---:|---:|']
for s in SPACES:
    r4=next(r for r in domain['rows'] if r['space']==s and r['half_width']==4.)
    r5=next(r for r in domain['rows'] if r['space']==s and r['half_width']==5.)
    lines.append(f"| {NAMES[s]} | {r4['u_core_linf']:.3g} / {r4['rho_core_linf']:.3g} | {r5['u_core_linf']:.3g} / {r5['rho_core_linf']:.3g} |")
lines += ['',
'扩大窗口后排序不变；固定网格 u 的绝对误差有可见边界敏感性，不能据此忽略它的双端解析边界优势。',
'',
'## 5. 可以从这些数据得出的结论','',
'1. **这组连续解上没有单一双场赢家。** 固定差分的 u 误差最低；普通 ρ 动网格的 ρ 误差最低。论文可积半离散在当前连续总误差上较大，主要是有限 a 空间模型差，不能归咎于时间积分器。',
'2. **可积半离散精确性与连续精度是两件事。** 论文格式有对应有限 a 的精确孤子；本轮让所有方法从同一连续初态出发，因此表中没有用该精确有限 a 解充当其初态。若专门测“求解器能否跟踪自己的半离散精确解”，应单列，不能与本表的连续总误差混用。',
'3. **时间法的作用可分辨，但高阶不会消除空间地板。** Euler/Heun/RK4 的同模型自收敛阶符合预期。RK8 在本短窗内过早触及舍入地板；增加时间阶数对主表 u/ρ 总误差改善极小，成本却上升。',
'4. **这里不是完全同边界条件的三算法竞赛。** 固定格使用两端解析边界和鬼点，动网格只用左端解析 u；内部短时排序通过扩域核查仍保持，但不能从本表断言任意初边值问题上固定差分必然更优。',
'',
'## 6. 复现与产物范围','',
'在工作区根目录依次运行 `python Workspaces/hs_factorial_20260925/run_factorial.py`、`python Workspaces/hs_factorial_20260925/spatial_audit.py`、`python Workspaces/hs_factorial_20260925/domain_audit.py`、`python Workspaces/hs_factorial_20260925/make_report.py`。主 JSON 保存 NumPy/SciPy/Python 版本、输入、每次运行状态、拒步、耗时与核心源码 SHA-256。没有修改既有 HS 求解器、DLW 工程或 Lean 文件。'
]
(HERE/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Wrote REPORT.md and 3 figures')
