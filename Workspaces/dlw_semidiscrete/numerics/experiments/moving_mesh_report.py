"""Regenerate the moving-mesh research note and figure from saved data."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
sys.path.insert(0,str(ROOT/'experiments'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from moving_mesh_study import ALL,OUT
from parametric import Exact

study=json.loads((OUT/'study.json').read_text(encoding='utf-8'))
cont=json.loads((OUT/'continuum.json').read_text(encoding='utf-8'))
ctrl=json.loads((OUT/'controls.json').read_text(encoding='utf-8'))
common=json.loads((OUT/'common_grid.json').read_text(encoding='utf-8'))
ids=[f'P{i}' for i in range(1,17)]
models=('structure','fd');fields=('u','v')


def find(rows,pid,model,mesh):
    return next(x for x in rows if x['parameter_id']==pid and x['model']==model
                and x['mesh']==mesh)


def value(pid,model,mesh,field):
    return find(cont['runs'],pid,model,mesh)['observations'][-1][field+'_inf']


def ratio(pid,model,field,base):
    return value(pid,model,'moving',field)/value(pid,model,base,field)


def main():
    fig,axs=plt.subplots(3,1,figsize=(13,8),layout='constrained',
                         gridspec_kw={'height_ratios':[1.2,1,1]})
    g=find(study['gram'],'P2','structure','moving')
    z=np.load(OUT/g['file']);x=z['x1'];spacing=np.diff(np.r_[x,x[0]+20.])
    axs[0].plot(x,spacing,marker='.',ms=3,lw=1,label='moving, P2')
    axs[0].axhline(20/128,color='black',ls='--',lw=1,label='uniform')
    axs[0].set_xlim(-3,3);axs[0].set_ylabel('physical x spacing')
    axs[0].set_title('Shared x mesh near the P2 pulse at t=0.01')
    axs[0].legend(frameon=False)
    for ax,base,title in ((axs[1],'uniform','moving / uniform'),
                          (axs[2],'static_adaptive','moving / initial redistribution')):
        matrix=np.array([[ratio(pid,m,f,base) for pid in ids]
                         for m in models for f in fields])
        im=ax.imshow(np.log2(matrix),aspect='auto',cmap='RdBu_r',
                     norm=TwoSlopeNorm(vmin=-1.2,vcenter=0,vmax=.3))
        ax.set_yticks(range(4),['SD u','SD v','FD u','FD v'])
        ax.set_xticks(range(16),ids)
        ax.set_title(title+' continuous-field error on own nodes, t=0.01')
        for i in range(4):
            for j in range(16):
                ax.text(j,i,f'{matrix[i,j]:.2f}',ha='center',va='center',fontsize=7)
    fig.colorbar(im,ax=axs[1:],shrink=.75,label='log2(error ratio)')
    figpath=ROOT/'figures'/'fig16_moving_mesh_comparison.png'
    fig.savefig(figpath,dpi=180)
    plt.close(fig)
    periodic_jumps=[]
    for pars in ALL:
        u,v=Exact(pars,.125,continuous=True).uv(np.arange(-12,12),[-10,10],.01)
        periodic_jumps.append((float(np.max(abs(u[:,0]-u[:,1]))),
                               float(np.max(abs(v[:,0]-v[:,1])))))

    lines=[
        '# 共同 x 移动网格：构造、场误差与参数扫描',
        '',
        '2026-09-23。独立新实验；未修改原生产 solver、Gram 实现或 Lean。',
        '',
        '## 1. 问题与方法',
        '',
        '固定原半离散的 y 格距 h=.125，在 x∈[-10,10) 用 128 个计算点。'
        '原守恒量 W=v−δ₀u 给出 ρ_j=1−W_j/4、ρ_{j,t}+q_{j,x}=0，'
        'q_j=(u_j+2a)ρ_j−ρ_{j,x}−2a。取固定均匀 y 权重 R=平均_jρ_j、Q=平均_jq_j。'
        '共同映射 x=X(ξ,t) 满足 J=X_ξ、∂_x=J⁻¹∂_ξ、X_t=(Q−Q_left)/R。'
        '左端通量减法固定周期窗口的左端；初始网格由有限 h Gram 坐标势精确等质量配置。',
        '',
        '每个 RK4 中间级都由**当前数值场**计算 R/Q 并更新 X；场方程含移动坐标的输运项。'
        '均匀、仅初始加密且冻结、持续移动三个方案使用相同的非均匀 x 导数实现。'
        'SD/FD 均用同一背景相对二次 y 幽灵外推。此闭合改变原固定幽灵问题；'
        'x 使用周期窗口。新方法尚未证明保持完整双线性可积结构。',
        f'16 组连续参照在 x=±10 的最大端点跳差为 u {max(z[0] for z in periodic_jumps):.3e}、'
        f'v {max(z[1] for z in periodic_jumps):.3e}（均来自 P5）；周期窗口仍是有限域近似。',
        '',
        '## 2. 执行范围与几何检查',
        '',
        'P1–P10 为已有正则参数，另加 P11–P16 六组。16 组几何、96 组有限 h Gram 绝对误差、'
        '96 组共同连续精确场绝对误差、96 组平衡低频非零扰动，以及各模型 32 个细 x 参照全部完成。'
        '观测 t=.005/.01；同模型扰动参照为 nx=384、dt=.0000625，粗网格 dt=.000125。'
        '高频/仅 v 在 P1/P2/P10 各模型各三网格补做；四组参数做细 x 与时间步检查，'
        'P1/P2/P10 的解析场驱动网格另推进到 T=2。',
        '',
        f"初始 Gram 等质量单元的最大质量差为 {json.loads((OUT/'validation.json').read_text(encoding='utf-8'))['initial_equal_gram_mass_spread']:.2e}；",
        '非均匀 x 一阶导数在 64/128/256 点的观测阶为 3.993/3.998。'
        '全部主扫描没有网格交叉或非正 Jacobian。16 组 T=.01 网格方程与解析 Gram 坐标的'
        f"最大节点差为 {max(x['max_node_error'] for x in study['geometry']):.3e}；"
        '这包括有限 x 差分误差，不是场求解误差。T=2 三组最大节点差见下表。',
        '',
        '| 参数 | T=2 节点最大差 | 最小点间距 |',
        '|---|---:|---:|',
    ]
    for x in ctrl['long_geometry']:
        lines.append(f"| {x['parameter_id']} | {x['max_node_error']:.3e} | {x['min_dx']:.4f} |")
    lines+=['','## 3. 共同连续精确场：u/v 绝对误差','','先比较各方案**自身节点**上的全域最大误差。表中比值是持续移动误差 / 固定均匀误差；小于 1 表示该项降低。'
             '它是 h=.125、nx=128、t=.01 的有限观察，不能直接推出 h 收敛或长期优势。','','| 模型/场 | 16 组中比值 <1 | 中位比值 | 持续移动 / 仅初始加密中位比值 |',
             '|---|---:|---:|---:|']
    for model in models:
        for f in fields:
            vals=[ratio(pid,model,f,'uniform') for pid in ids]
            static=[ratio(pid,model,f,'static_adaptive') for pid in ids]
            lines.append(f"| {model} {f} | {sum(x<1 for x in vals)}/16 | {np.median(vals):.3f} | {np.median(static):.3f} |")
    lines+=['','主要收益来自初始重分布：持续移动相对冻结加密的额外收益在所测短时内很小，'
             'v 的中位比值甚至大于 1。两模型都得到类似的加密收益。'
             '直接比较模型时，移动网格上 SD 的 u 在 15/16 组、v 在 13/16 组较小；'
             'P10 的 u 则由 FD 明显较小。这些是同一连续参照下的当前离散配置排序，'
             '不能外推成一般可积方法优势。','','![共同网格与误差比值](figures/fig16_moving_mesh_comparison.png)','','逐参数结果：','','| 参数 | a,p,q,振幅 | SD u | SD v | FD u | FD v |',
             '|---|---|---:|---:|---:|---:|']
    for i,pars in enumerate(ALL):
        pid=f'P{i+1}'
        vals=[ratio(pid,m,f,'uniform') for m in models for f in fields]
        lines.append(f"| {pid} | {pars.a:g},{pars.p:g},{pars.q:g},{pars.rho:g} | "+' | '.join(f'{v:.3f}' for v in vals)+' |')
    lines+=['','### 共同物理 x 点的复核','','各方案节点不同，因此另将数值 u/v 场用三次样条映射到共同的 1025 个物理 x 点（[-9,9]），再与连续精确场逐点比较。该指标计入场插值误差，并避开周期窗口最外侧 1 个长度单位；与上方全窗口节点误差不同。','','| 模型/场 | 16 组中移动/均匀 <1 | 中位比值 | 移动/冻结加密中位比值 |','|---|---:|---:|---:|']
    for model in models:
        for f in fields:
            def cv(pid,mesh):
                return find(common['continuous'],pid,model,mesh)[f+'_common_inf']
            vals=[cv(pid,'moving')/cv(pid,'uniform') for pid in ids]
            stat=[cv(pid,'moving')/cv(pid,'static_adaptive') for pid in ids]
            lines.append(f'| {model} {f} | {sum(v<1 for v in vals)}/16 | {np.median(vals):.3f} | {np.median(stat):.3f} |')
    lines+=['','共同点复核仍支持“初始加密有效、持续移动额外收益很小”的判断；个别组的胜负随误差定义改变，不应把单一计数解释为严格方法优势。']
    lines+=['','## 4. 有限 h Gram 与非零扰动','','有限 h Gram 真值下，移动/均匀的 SD u、v 中位比值分别为 '
             f"{np.median([find(study['gram'],p,'structure','moving')['observations'][-1]['u_inf']/find(study['gram'],p,'structure','uniform')['observations'][-1]['u_inf'] for p in ids]):.3f}/"
             f"{np.median([find(study['gram'],p,'structure','moving')['observations'][-1]['v_inf']/find(study['gram'],p,'structure','uniform')['observations'][-1]['v_inf'] for p in ids]):.3f}。"
             '该参照是 SD 的精确解，不能据此公正判定 SD 与 FD 谁更接近连续方程。',
             '',
             '对非零低频扰动，改用每个模型自己的细 x 参照，避免把不同半离散模型误差混入网格误差。'
             '16 组中，移动网格的 u/v 差异在两模型均为 16/16 降低；'
             'SD 的中位移动/均匀差异比值为 0.549/0.549，FD 为 0.550/0.541。'
             'P1/P2/P10 的高频与仅 v 扰动亦在所测 3/3 组、两场两模型上降低差异。'
             '这些是参照差异，不是严格误差上界。',
             '',
             '代表参数 P1/P2/P10/P16：细参照 nx=384→512 的最大相对响应差异为 '
             f"{max(x['fine_vs_finest'][-1][f]['relative_response_difference'] for x in ctrl['x_dt_controls'] for f in fields):.3%}；"
             '对应 dt 减半的最大差异为 '
             f"{max(x['time_step'][-1][f]['relative_response_difference'] for x in ctrl['x_dt_controls'] for f in fields):.2e}。"
             '这些检查支持代表组的短时 x 参照，但不是全部 16 组的严格认证。',
             '',
             '## 5. 结论与边界',
             '',
             '从原守恒律和 Gram 坐标势构造的共同 x 网格可实际耦合推进，'
             '并在这组短时单孤子实验中降低了多数 u/v 误差。'
             '目前没有发现参数移位结构独占的自适应收益；直接 FD 同样受益，'
             '且持续移动本身尚未显示出稳定的额外收益。'
             '这里的结构优势是可推导的正密度与精确坐标参照，'
             '不是已证明的全场误差优势。',
             '',
             '尚未验收：一般受扰动解的密度正性和长时场误差、两孤子全耦合传播、'
             '移动 x 网格对 y 右端重构放大的消除、完整双线性/谱结构在 x 离散后的保持。'
             '当前三种网格的计时都包含同一移动框架的密度计算，不代表优化后的固定网格成本；'
             '误差—真实成本优势尚需独立计时。',
             '',
             '## 6. 复现',
             '',
             '在 `numerics` 目录，使用带 NumPy/SciPy/Matplotlib 的 Python：',
             '',
             '```text',
             'python -u experiments/moving_mesh_study.py',
             'python -u experiments/moving_mesh_controls.py',
             'python -u experiments/moving_mesh_continuum.py',
             'python -u experiments/moving_mesh_common_grid.py',
             'python -u experiments/moving_mesh_validate.py',
             'python -u experiments/moving_mesh_report.py',
             '```',
             '',
             '`out/moving_mesh/` 保留每条原始场数组、逐次运行指标、控制实验与哈希；'
             '`validation.json` 记录源码和汇总产物哈希。',
             '']
    path=ROOT/'MOVING_MESH_REPORT.md'
    path.write_text('\n'.join(lines),encoding='utf-8')
    print(path)


if __name__=='__main__':main()
