"""Render selected-wave experiment from completed recorded data."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'/'parameter_scan'
d=json.loads((OUT/'evolution.json').read_text(encoding='utf-8'))
sp=json.loads((OUT/'spatial_controls.json').read_text(encoding='utf-8'))
dm=json.loads((OUT/'domain_controls.json').read_text(encoding='utf-8'))
lat=json.loads((OUT/'integrable_lattice_check.json').read_text(encoding='utf-8'))
SPACES=('integrable_moving','ordinary_moving','fixed_difference')
METHODS=('euler','heun','rk4','rk8')
CNAMES={'integrable_moving':'论文可积半离散＋ρ 动网格',
        'ordinary_moving':'普通差分＋ρ 动网格',
        'fixed_difference':'固定物理网格差分'}
ENAMES={'integrable_moving':'Integrable semi-discrete',
        'ordinary_moving':'Ordinary rho mesh',
        'fixed_difference':'Fixed-grid difference'}
MNAMES={'euler':'Euler 1 阶','heun':'Heun 2 阶',
        'rk4':'RK4 4 阶','rk8':'DOP853 8 阶主公式'}
COLORS={'integrable_moving':'#1f77b4','ordinary_moving':'#ff7f0e',
        'fixed_difference':'#2ca02c'}

def get(p,s,m='rk4',dt=.00625):
    return next(r for r in d['rows'] if r['p']==p and r['space']==s and
                r['method']==m and r['dt']==dt)

def metric(r,name='wave_window',t='0.25'):
    try:
        return r['observations'][t]['windows'][name]
    except KeyError:
        return None

plt.rcParams.update({'font.family':'DejaVu Sans','figure.dpi':150,
                     'axes.grid':True,'grid.alpha':.22,'font.size':10})
fig,axes=plt.subplots(1,3,figsize=(13,4))
for ax,field,title in zip(axes,('u_scaled_linf','rho_scaled_linf','joint_scaled_linf'),
                          ('u / initial peak','rho / initial dip','joint maximum')):
    for s in SPACES:
        vals=[metric(get(p,s))[field] for p in (3,5,12,20)]
        ax.semilogy((3,5,12,20),vals,'o-',label=ENAMES[s],color=COLORS[s],lw=1.5)
    ax.set_xlabel('Spectral parameter p');ax.set_title(title)
    ax.set_xticks((3,5,12,20))
axes[0].set_ylabel('Scaled max error on wave window')
axes[0].legend(fontsize=8)
fig.suptitle('2HS selected waves, RK4, dt=0.00625, T=0.25')
fig.tight_layout()
fig.savefig(OUT/'fig1_parameter_accuracy.png',bbox_inches='tight')
plt.close(fig)

matrix=np.array([[metric(get(p,s,m))['joint_scaled_linf']
                  for s in SPACES for m in METHODS] for p in (3,5,12,20)])
fig,ax=plt.subplots(figsize=(13,3.6))
im=ax.imshow(np.log10(matrix),aspect='auto',cmap='viridis_r')
ax.set_yticks(range(4),['p=3','p=5','p=12','p=20'])
ax.set_xticks(range(12),[ENAMES[s]+'\n'+m for s in SPACES for m in METHODS],
              rotation=45,ha='right',fontsize=7)
cb=fig.colorbar(im,ax=ax);cb.set_label('log10 joint scaled error')
fig.tight_layout()
fig.savefig(OUT/'fig2_all_combinations.png',bbox_inches='tight')
plt.close(fig)

fig,axes=plt.subplots(1,4,figsize=(17,3.6),sharey=True)
for ax,p in zip(axes,(3,5,12,20)):
    for s in SPACES:
        rr=sorted((r for r in sp['rows'] if r['p']==p and r['space']==s),
                  key=lambda r:r['a_or_dx'],reverse=True)
        ax.loglog([r['a_or_dx'] for r in rr],
                  [metric(r)['joint_scaled_linf'] for r in rr],
                  'o-',label=ENAMES[s],color=COLORS[s],lw=1.5)
    ax.set_title(f'p={p}');ax.set_xlabel('a or dx')
    ticks=(.005,.01,.02,.04) if p==20 else (.01,.02,.04)
    ax.set_xticks(ticks,[f'{v:g}' for v in ticks],fontsize=8)
axes[0].set_ylabel('Joint scaled max error')
axes[0].legend(fontsize=7)
fig.suptitle('Spatial refinement, DOP853, dt=0.00625')
fig.tight_layout()
fig.savefig(OUT/'fig3_spatial_control.png',bbox_inches='tight')
plt.close(fig)

lines=['# 2HS 单孤子选参后的三空间 × 四时间演化实验','',
'2026-09-25。本报告按 [选参报告](WAVE_PARAMETER_SELECTION.md)预先选定的 p=3、5、12 三组主例与 p=20 压力例运行。四组均实际推进 3 种空间方法 × 4 种时间算法；每组合再扫描 4 档时间步。原始数据：[演化](out/parameter_scan/evolution.json)、[格距控制](out/parameter_scan/spatial_controls.json)、[扩域](out/parameter_scan/domain_controls.json)、[有限 a 精确解核查](out/parameter_scan/integrable_lattice_check.json)。',
'',
'## 1. 因素与控制量','',
'独立比较因素：空间方法（论文可积半离散＋自然 ρ 动网格；普通差分＋同一自然 ρ 动网格；固定物理网格差分）、时间方法（Euler 1 阶；Heun 2 阶；RK4 4 阶；固定步长 DOP853 8 阶主公式）。p 是按解析波形预选的**测试情景**，不是看到数值误差之后调出来的参数。',
'',
'| p | 角色 | q=p/(p−1) | u 初峰 | ρ 初谷 | 物理半高全宽 L | T=.25 位移/L | 半计算域 H | a=Δx | 格数 |',
'|---:|---|---:|---:|---:|---:|---:|---:|---:|']
for p in (3,5,12,20):
    w=d['waves'][str(p)]
    r=get(p,'integrable_moving')
    role='压力例' if p==20 else '主例'
    lines.append(f"| {p} | {role} | {w['q']:.6g} | {w['u_peak']:.6g} | {w['rho_min']:.6g} | {w['u_fwhm']:.6g} | {w['physical_speed']*.25/w['u_fwhm']:.5f} | {r['half_width']:.1f} | .02 | {r['edges']} |")
lines += ['',
'所有组固定 c=1、相位 0、连续孤子初态、T=.05/.10/.25、主步长 .00625。依选参报告设 shift=−(1−2/p)/2，让初始峰在 x=0。每组的 a=Δx=.02，相同 p 内三方法的节点数一致；不同 p 根据波宽扩域，节点数因此不同，不能拿跨 p 的运行秒数直接比较成本。',
'',
'这些固定值延续原 p=5 基准的 c=1、a=Δx=.02 和短时间窗，使新增 p 扫描只改变预先声明的波形情景；相位和平移用于统一峰位置。a=.02 时四组均满足原文有限 a 正乘子条件 a·max(p,q)<1。半域按各组 3L 评价窗及边界缓冲设为 11/6.5/5/5；固定 a 使同一 p 的名义节点预算相同，但自然 ρ 网格在峰区的实际节点数较少。',
'',
'评价区间同时保存旧核心 [-2,2] 和每组专属、对所有算法固定的初态峰两侧各 3L，即 [-3L,3L]。主表用后者，避免 p=3 宽波只看峰附近。求解域半宽 H 大于 3L 并留边界缓冲。绝对误差与按初态 u_peak、1−rho_min 归一后的误差一并保存。自然质量网格保持 R=ρ；无其他密度、无重新调参。',
'',
'动网格使用左端连续精确 u 驱动边界，固定格使用两端解析 u 和 ρ/m 鬼点数据；这是既有求解器的边界差异。连续精确波只用于 t=0 内部采样、时变边界和事后误差评估，未用于重置内部演化。p=20 采用单调坐标查表加 Newton 反演，避免旧解析反演器在深凹陷处停滞；p≤12 的反演与原实现相同。',
'',
'## 2. 每组十二个组合：t=.25 的实际连续解误差','',
'以下为 Δt=.00625、共同波形区间的最大绝对误差。括号内是除以该组初始场幅度的相对误差；“合并”取两场相对误差的较大者。每个方法还运行了 .05、.025、.0125 三档时间步，完整轨道在 JSON 中。',
'']
for p in (3,5,12,20):
    lines += [f'### p={p} '+('压力例' if p==20 else '主例'),'','| 空间方法 | 时间方法 | u 误差（/峰值） | ρ 误差（/凹陷） | 合并相对误差 | 最小网格距 | 状态 |',
              '|---|---|---:|---:|---:|---:|---|']
    for s in SPACES:
        for m in METHODS:
            r=get(p,s,m);v=metric(r)
            if v is None or 'joint_scaled_linf' not in v:
                lines.append(f"| {CNAMES[s]} | {MNAMES[m]} | — | — | — | — | {r['status']}：{r['failure_reason']} |")
            else:
                mesh=r['observations']['0.25']['mesh']
                lines.append(f"| {CNAMES[s]} | {MNAMES[m]} | {v['u_linf']:.4g} ({v['u_scaled_linf']:.3g}) | {v['rho_linf']:.4g} ({v['rho_scaled_linf']:.3g}) | {v['joint_scaled_linf']:.4g} | {mesh['min_spacing']:.4g} | {r['status']} |")
    lines.append('')
lines += ['![各参数两场相对误差](out/parameter_scan/fig1_parameter_accuracy.png)',
          '',
          '![四参数全部组合](out/parameter_scan/fig2_all_combinations.png)',
          '',
          '## 3. 时间、空间与边界控制','',
          '每个 p、空间方法另以 Δt=.000390625 的 DOP853 轨道作同模型时间参照。下表列 RK4 主步长对该参照的状态最大差；这不是连续 PDE 真解误差。四档误差的时间阶和失败状态保留在原始 JSON。高阶到舍入地板时不强行拟合观测阶。',
          '',
          '| p | 论文式 RK4 时间状态差 | 普通动网格 RK4 | 固定差分 RK4 |',
          '|---:|---:|---:|---:|']
for p in (3,5,12,20):
    vals=[get(p,s)['temporal_state_linf'] for s in SPACES]
    lines.append(f"| {p} | "+' | '.join('—' if z is None else f'{z:.3g}' for z in vals)+' |')
lines += ['',
'空间加密固定 DOP853、Δt=.00625；普通三组取 a=Δx=.04/.02/.01，p=20 另取 .005，以检验报告提示的“压力例自然质量网格每波宽节点不足”。表中为波形区间的合并相对误差，斜率由相邻两档计算，只是所测区间的观测阶。',
'',
'| p | 空间方法 | .04 / .02 / .01（p=20 另有 .005） | 最后两档观测阶 |',
'|---:|---|---:|---:|']
for p in (3,5,12,20):
    for s in SPACES:
        rr=sorted((r for r in sp['rows'] if r['p']==p and r['space']==s),
                  key=lambda z:z['a_or_dx'],reverse=True)
        vals=[metric(r)['joint_scaled_linf'] for r in rr]
        slope=math.log2(vals[-2]/vals[-1])
        lines.append(f"| {p} | {CNAMES[s]} | "+' / '.join(f'{v:.3g}' for v in vals)+f' | {slope:.3f} |')
lines += ['',
'![空间格距控制](out/parameter_scan/fig3_spatial_control.png)',
'',
'各组 a=.02 把半域再扩大 1，其他量相同。下表给 RK8 波形区间合并相对误差，检查评价区是否受端点位置影响。',
'',
'| p | 空间方法 | 原半域 | 扩大半域 | 相对变化 |',
'|---:|---|---:|---:|---:|']
for p in (3,5,12,20):
    for s in SPACES:
        before=metric(get(p,s,'rk8'))['joint_scaled_linf']
        after=metric(next(r for r in dm['rows'] if r['p']==p and r['space']==s))['joint_scaled_linf']
        lines.append(f'| {p} | {CNAMES[s]} | {before:.4g} | {after:.4g} | {(after/before-1)*100:+.2f}% |')
lines += ['',
'共同点重构地板也逐次保存：把精确场采到相同节点，再走完全相同的三次样条和边平均反卷积。只有当实际误差明显高于重构地板，比较才有分辨力。主表 t=.25 的波形区间，重构地板/对应误差最大为 0.178；但部分 t=.05 的 p=20 密度误差和部分控制轨道已经接近或低于重构地板，不能逐项当作已分辨的 PDE 误差。原生节点的 u 与格边平均 ρ 误差也在 JSON，不只依赖共同网格插值。',
'',
'## 4. 对论文有限 a 精确孤子的单独核验','',
'为了区分“可积格式能否精确推进自己的有限格距孤子”和“对连续 2HS 解是否准确”，另以有限 a 精确孤子作初值及左端边界，RK8、Δt=.00625 推到 .25，比较同一有限 a 精确解。此表绝不与 §2 的共同连续初值误差合并。',
'',
'| p | u 求解误差 | ρ 求解误差 | 节点 x 误差 |',
'|---:|---:|---:|---:|']
for r in lat['rows']:
    if r['status']=='completed':
        lines.append(f"| {r['p']} | {r['u_solver_linf']:.3g} | {r['rho_solver_linf']:.3g} | {r['x_solver_linf']:.3g} |")
    else:
        lines.append(f"| {r['p']} | {r['status']} | {r['failure_reason']} | — |")
lines += ['',
'## 5. 结论与适用范围','',
'本节由保存数据生成，以下判断按 t=.25 的波形区间与空间控制解释。']
for p in (3,5,12,20):
    vals={s:metric(get(p,s))['joint_scaled_linf'] for s in SPACES}
    winner=min(vals,key=vals.get)
    lines.append(f"- p={p}：RK4 合并相对误差依次为论文 {vals['integrable_moving']:.4g}、普通动网格 {vals['ordinary_moving']:.4g}、固定格 {vals['fixed_difference']:.4g}；本例最低为{CNAMES[winner]}。")
lines += ['',
'这些只是指定光滑单孤子族、短时间窗、边界和格距的数值事实。p 增大同时改变幅度、宽度、速度与 ρ 凹陷，不能把误差变化单独归因于其中一个几何指标。T=.25 只传播约 0.014–0.029 个波宽，不支持长距离跟踪或碰撞优势声明。p=20 是仍正密度的压力例，不是 GSG 的环孤子类比。',
'',
'## 6. 复现','',
'按顺序运行 `python Workspaces/hs_factorial_20260925/run_parameter_scan.py`、`python Workspaces/hs_factorial_20260925/audit_parameter_scan.py`、`python Workspaces/hs_factorial_20260925/validate_parameter_scan.py`、`python Workspaces/hs_factorial_20260925/make_parameter_report.py`。主 JSON 保存源码 SHA-256、环境版本、所有时间步/失败/网格数据；失败不从扫描中删去。旧 p=5、shift=0 的 12 组合报告保留为历史基准，这次 shift 随 p 峰对齐，不能把两组表直接视作同一初态重跑。']
lines[2:2] = ['> **独立审查补充（2026-09-25）：** 见 [PARAMETER_SCAN_REVIEW.md](PARAMETER_SCAN_REVIEW.md)。独立参照与时间积分复现主误差，但三算法边界闭合不同；多个最大 u 误差位于右侧尾部，p=20 的小 rho 优势未充分越过重构/边界敏感性。新增同边界、同动网格公式的初始布点对照显示 p=5/12/20 可明显改善，不能将本表解释为“rho 动网格普遍无效”。', '', '> **后续研究：** [新守恒密度与局部参数搜索](NEW_DENSITIES_AND_LOCAL_P.md)推导 R=(u_xx+2)/(2rho) 的连续守恒律及光滑孤子正性；另运行11参数的33条原格式局部扫描和21条控制，未找到原可积式的误差胜出。新密度尚未用于演化。', '']
(HERE/'PARAMETER_SCAN_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Wrote parameter report and 3 figures')
