"""Build the five research figures and narrative from saved measurements."""
from dynamics_study import ROOT, OUT, Reference, write
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIG=ROOT/'figures'
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})


def load(name):return json.loads((OUT/(name+'.json')).read_text(encoding='utf-8'))['data']
def select(rows,**kw):
    return next(r for r in rows if all(r['config'][k]==v for k,v in kw.items()))
def at(r,t):return min(r['history'],key=lambda z:abs(z['t']-t))
def save(fig,name):
    fig.tight_layout();fig.savefig(FIG/name,dpi=160);plt.close(fig)
def table(head,rows):
    return '\n'.join(['| '+' | '.join(head)+' |','|'+'|'.join(['---']*len(head))+'|']+
                      ['| '+' | '.join(str(v) for v in r)+' |' for r in rows])


def model_limit():
    rows=[]
    for case in ('A','B'):
        for t in (0.,.2,-.35):
            for h in (.25,.125,.0625,.03125,.015625):
                js=np.arange(-round(1.5/h),round(1.5/h));x=np.linspace(-1.5,1.5,301)
                a=Reference(case,h).uv(js,x,t);b=Reference(case,h,True).uv(js,x,t)
                row=dict(case=case,t=t,h=h)
                for key,z,w in zip(('u','v'),a,b):
                    e=z-w;weights=np.ones(len(x));weights[[0,-1]]=.5
                    row[key]=dict(inf=float(np.max(abs(e))),l2=float(np.sqrt(.01*h*np.sum(e*e*weights))))
                rows.append(row)
    write('dynamics_model_limit',rows)
    return rows


def main():
    prop,comp,sens,cost=[load('dynamics_'+k) for k in ('propagation','comparison','sensitivity','cost')]
    lim=model_limit();short=load('dynamics_short_controls')
    base={c:select(prop,case=c,nx=256,h=.25,L=20.,T=.05,dt=.00025,yhalf=1.5) for c in ('A','B')}
    # 1. Compare profiles through the measured valid time, not through blow-up.
    fig,axs=plt.subplots(2,2,figsize=(11,7))
    for row,c in enumerate(('A','B')):
        r=base[c];end=r['valid_through']
        for col,z in enumerate(('u','v')):
            ax=axs[row,col]
            for t,color in zip((0,end/2,end),('0.6','#2579a8','#b74736')):
                s=min(r['snapshots'],key=lambda q:abs(q['t']-t));x=np.array(r['x']);mask=abs(x)<2
                ax.plot(x[mask],np.array(s['exact_'+z])[mask],color=color,label=f'exact t={s["t"]:.3f}')
                ax.plot(x[mask][::2],np.array(s[z])[mask][::2],'.',color=color,ms=4)
            ax.set(title=f'{c}: {z}, line=exact / dots=solver',xlabel='x',ylabel=z)
            ax.legend(fontsize=8)
    save(fig,'fig5_dynamics_profiles.png')
    # 2. Total errors, position and aligned shape; late failed fits excluded.
    fig,axs=plt.subplots(2,3,figsize=(13,7))
    for i,c in enumerate(('A','B')):
        r=base[c];hist=r['history'];t=[q['t'] for q in hist]
        for z in ('u','v'):
            axs[i,0].semilogy(t,[max(q[z]['relative_inf'],1e-15) for q in hist],label=z)
            good=[q for q in hist if q[z]['fit_interpretable']]
            axs[i,1].plot([q['t'] for q in good],[q[z]['shift'] for q in good],label=z)
            axs[i,2].semilogy([q['t'] for q in good],[max(q[z]['aligned_profile_inf'],1e-15) for q in good],label=z)
        axs[i,0].axhline(.01,color='black',ls=':',label='1% threshold')
        for j,title in enumerate(('global relative error','central profile shift','aligned profile error')):
            axs[i,j].set(title=f'{c}: {title}',xlabel='t');axs[i,j].legend(fontsize=8)
    save(fig,'fig6_dynamics_errors.png')
    # 3. Independent x, time and h effects: retain fixed-time failures.
    fig,axs=plt.subplots(2,3,figsize=(13,7))
    for i,c in enumerate(('A','B')):
        for z,style in (('u','-o'),('v','--s')):
            rs=[select(prop,case=c,nx=n,h=.25,L=20.,T=.05,dt=.00025,yhalf=1.5) for n in (128,256,512)]
            axs[i,0].loglog([20/n for n in (128,256,512)],[at(r,.005)[z]['inf'] for r in rs],style,label=f'{z}, t=.005')
            a=base[c];b=select(prop,case=c,nx=256,h=.25,L=20.,T=.05,dt=.000125,yhalf=1.5)
            axs[i,1].semilogy([q['t'] for q in a['history']],[max(q[z]['inf'],1e-15) for q in a['history']],label=f'{z}, dt=.00025')
            axs[i,1].semilogy([q['t'] for q in b['history']],[max(q[z]['inf'],1e-15) for q in b['history']],':',label=f'{z}, dt/2')
            rr=[q for q in lim if q['case']==c and q['t']==.2]
            axs[i,2].loglog([q['h'] for q in rr],[q[z]['inf'] for q in rr],style,label=f'{z}, exact model')
        for j,title in enumerate(('x refinement: common early time','time halving: same spatial grid','finite h vs continuum, t=.2')):
            axs[i,j].set(title=f'{c}: {title}',xlabel=('dx','t','h')[j]);axs[i,j].legend(fontsize=7)
    save(fig,'fig7_dynamics_refinement.png')
    # 4. Matched continuous problem / cost. Timing gathered sequentially.
    fig,axs=plt.subplots(2,2,figsize=(11,7))
    for i,c in enumerate(('A','B')):
        for model,marker in (('structure','o'),('fd','s')):
            rr=[r for r in comp if r['config']['case']==c and r['config']['nx']==256 and r['config']['dt']==.00025]
            rr=[r for r in rr if r['config']['model']==model]
            for z,ls in (('u','-'),('v','--')):
                axs[i,0].loglog([r['config']['h'] for r in rr],[at(r,.005)[z]['inf'] for r in rr],ls+marker,label=f'{model} {z}')
            rr=[r for r in cost if r['case']==c and r['model']==model]
            axs[i,1].scatter([r['median_seconds'] for r in rr],[max(r['errors'][z]['inf'] for z in ('u','v')) for r in rr],marker=marker,label=model)
        axs[i,0].set(title=f'{c}: common continuous reference, t=.005',xlabel='h',ylabel='absolute error')
        axs[i,1].set(title=f'{c}: 3-repeat median evolution cost',xlabel='seconds',ylabel='max absolute error (u,v)',xscale='log',yscale='log')
        for ax in axs[i]:ax.legend(fontsize=8)
    save(fig,'fig8_dynamics_comparison.png')
    # 5. Actual trajectory response and its relation to error; beyond validity marked.
    fig,axs=plt.subplots(2,2,figsize=(11,7))
    for i,c in enumerate(('A','B')):
        for mode in (2,16):
            rr=[r for r in sens if r['case']==c and r['mode']==mode]
            for r in rr:
                axs[i,0].semilogy(r['times'],r['gain'],label=f'k={r["k"]:.2f}, eps={r["eps"]:g}, dt={r["dt"]:g}',alpha=.65)
        r=base[c]
        axs[i,0].axvline(r['valid_through'],color='black',ls=':')
        for z in ('u','v'):
            axs[i,1].semilogy([q['t'] for q in r['history']],[max(q[z]['high_frequency_rms'],1e-16) for q in r['history']],label=z)
        axs[i,0].set(title=f'{c}: paired trajectory response (P,W)',xlabel='t',ylabel='gain, initial state norm = 1')
        axs[i,1].set(title=f'{c}: error above 75% Nyquist',xlabel='t',ylabel='Fourier error indicator')
        axs[i,0].legend(fontsize=5);axs[i,1].legend()
    save(fig,'fig9_dynamics_sensitivity.png')
    # Secondary all-domain view, explicitly taken after threshold crossing.
    fig,axs=plt.subplots(2,2,figsize=(11,6))
    for i,c in enumerate(('A','B')):
        f=np.load(OUT/base[c]['field_array'])
        for j,z in enumerate(('u','v')):
            im=axs[i,j].pcolormesh(f['x'],f['y'],abs(f[z]-f['exact_'+z]),shading='auto',cmap='magma')
            axs[i,j].set(xlim=(-3,3),title=f'{c}: |error {z}| at t={float(f["t"]):.3f} (failed 1% gate)',xlabel='x',ylabel='y')
            fig.colorbar(im,ax=axs[i,j])
    save(fig,'fig10_dynamics_error_maps.png')

    # Tables and quantitative checks supporting the prose.
    refinement=[];bounds=[];decomp=[];boundary=[];match=[];resp=[];limits=[]
    for c in ('A','B'):
        previous=None
        for n in (128,256,512):
            r=select(prop,case=c,nx=n,h=.25,L=20.,T=.05,dt=.00025,yhalf=1.5)
            e=at(r,.005);orders=['—','—'] if previous is None else [f'{np.log2(previous[z]["inf"]/e[z]["inf"]):.3f}' for z in ('u','v')]
            refinement.append([c,n,f'{e["u"]["inf"]:.3e}',f'{e["v"]["inf"]:.3e}',*orders,
                               '完成' if r['complete'] else f'停止于 {r["final_t"]:.5f}'])
            previous=e
            g=Reference(c);x=np.linspace(-5,5,10001);u=g.uv([0],x,0)[0][0];mask=abs(u)>=.5*np.max(abs(u));width=x[mask][-1]-x[mask][0]
            bounds.append([c,n,f'{r["valid_through"]:.3f}',f'{r["first_failed_observation"]:.3f}',f'{width:.3f}',f'{r["valid_through"]/width:.3f}'])
        r=base[c]
        for h in (.25,.125,.0625):
            r=select(short,case=c,nx=256,h=h,L=20.,T=.005,dt=.00025,yhalf=1.5)
            for z in ('u','v'):
                d=r['decomposition'][z]
                decomp.append([c,h,z,f'{d["solver"]["inf"]:.3e}',f'{d["model"]["inf"]:.3e}',f'{d["total"]["inf"]:.3e}'])
        for L,n,y in ((20.,256,1.5),(30.,384,1.5),(20.,256,2.5)):
            r=select(prop,case=c,nx=n,h=.25,L=L,T=.05,dt=.00025,yhalf=y)
            e=at(r,.01)
            assert abs(e['t']-.01)<1e-12
            boundary.append([c,L,y,f'{e["u"]["common_region_inf"]:.3e}',f'{e["v"]["common_region_inf"]:.3e}',f'{e["exact_endpoint_mismatch"]:.2e}'])
        for model in ('structure','fd'):
            for h in (.25,.125,.0625):
                r=select(comp,case=c,nx=256,h=h,model=model,dt=.00025)
                e=at(r,.005);last=r['history'][-1]
                match.append([c,model,h,f'{e["u"]["inf"]:.3e}',f'{e["v"]["inf"]:.3e}',f'{last["t"]:.3f}',f'{last["u"]["relative_inf"]:.2e}',f'{last["v"]["relative_inf"]:.2e}'])
        for t in (0.,.2,-.35):
            rr=[r for r in lim if r['case']==c and r['t']==t]
            a,b=rr[-2:]
            limits.append([c,t,*[f'{b[z][norm]:.3e} / {np.log2(a[z][norm]/b[z][norm]):.4f}' for z in ('u','v') for norm in ('inf','l2')]])
        for mode in (2,16):
            rr=[r for r in sens if r['case']==c and r['mode']==mode]
            ref=next(r for r in rr if r['eps']==5e-6 and r['dt']==.000125)
            arr=np.load(OUT/ref['array'])['response'];idx=ref['times'].index(.01)
            dif=[]
            for r in rr:
                a=np.load(OUT/r['array'])['response'][r['times'].index(.01)]
                dif.append(float(np.linalg.norm(a-arr[idx])/np.linalg.norm(arr[idx])))
            resp.append([c,f'{ref["k"]:.5f}',f'{ref["gain"][idx]:.6f}',f'{max(dif):.3e}',f'{ref["times"][-1]:.3f}', '停止' if not ref['complete'] else '完成'])
    # Research outcomes are NOT changed into success checks.
    checks={
        'propagation_config_count':len(prop),'short_control_count':len(short),'comparison_config_count':len(comp),
        'paired_response_config_count':len(sens),'cost_config_count':len(cost),
        'all_initial_errors_small':all(r['history'][0][z]['inf']<1e-12 for r in prop+comp for z in ('u','v')),
        'error_vector_identity':all(r['decomposition'][z]['identity_residual']<1e-10 for r in prop+comp for z in ('u','v')),
        'relative_response_repeatability_at_001':all(float(r[3])<1e-3 for r in resp),
        'complete_propagation_runs':sum(r['complete'] for r in prop),
        'complete_comparison_runs':sum(r['complete'] for r in comp),
    }
    assert checks['all_initial_errors_small'] and checks['error_vector_identity'] and checks['relative_response_repeatability_at_001']
    report='''# 从精确半离散结构到可验证的孤子动力学

2026-09-23。根据“论文数值分析梳理”会话，已实际补做单孤子传播、误差分离、同问题模型比较、孤子背景扰动和边界敏感性。**结果支持很短时间内的精度与误差阶，但当前未经滤波的求解器尚未通过可辨认距离的孤子传播验收。**实验失败和停止原因全部保留；不能据此宣布长时间稳定、一般初值收敛或结构方案优于常规差分。

## 1. 实际求解的问题与事先固定的判据

核心问题是：有限格距的精确结构能否被数值演化再现，误差来自何处，与连续模型和普通差分有什么差别？有限 h 精确参照检验求解器；连续精确参照检验模型逼近；二者分开。

| 设置 | 内容 |
|---|---|
| A / B | a=4；A: p=1,q=2,rho=3；B: p=2,q=3,rho=5 |
| 物理位置 | y=(j+1/2)h；共同中点积分区域 y∈[-1.5,1.5] |
| 主格距 | h=1/4；另测 1/8、1/16；x 区间 [-10,10)，nx=128/256/512 |
| x 与时间 | 四阶周期 D1，D2=D1²；RK4，dt=0.00025；独立减半至 0.000125 |
| 时间 | 共同目标 T=0.05；另尝试 T=0.4；每 0.005 观察一次 |
| 边界 | 每个 RK 阶段更新解析左端基值、u 鬼点和结构模型外侧 P；内部只由方程推进 |
| 精度判据 | u、v 的全域最大误差分别不超过各自初始精确峰值的 1% |
| 停止判据 | 非有限状态，或 P/Q 最大绝对值超过 1000；未到目标时刻不得记为完成 |
| 数值设置 | Float64；无滤波、阻尼或精确内部场重置 |

结构模型推进 P=δ₋u、W=v−δ₀u，u 由左端基值累加重构。新增常规基线推进 P=δ₋u、v：P_t=−δ₋∂x(u²/2+2au)−∂xx M₋v；v_t=−∂x((u+2a)v)−∂xxδ₀u+4∂xu。这是连续 DLW 的二阶交错 y 差分，并非此前固定边界 E7 的直接拼接。两模型比较时，从同一个连续解取完全相同的 u/v 初值和时变边界，初始重构误差小于 1e-12。

新基线独立通过 y 加密残差和固定网格时间自收敛检查。稳定的一孤子闭式求值与已有 GramRef / ContRef 逐点核对；快速局部差分与原矩阵 D1/D2 及完整非线性 RHS 核对。没有改变原生产求解器或 Lean 定理。

## 2. 单孤子再现：短时准确不等于传播验收

图中实线为有限 h 精确解，点为真实推进结果。只展示通过门槛时间段内的剖面；同时保留全域未对齐误差。对中央剖面拟合完整的 x 平移，独立报告位置偏差及对齐后形状误差；大失真或拟合触及边界时不解释位置值。

![单孤子剖面对照](figures/fig5_dynamics_profiles.png)
![总误差、位置和波形](figures/fig6_dynamics_errors.png)

下表的“通过到”只表示此前所有已观察时刻通过。采样间隔为 0.005；不排除采样间隔内曾更早越界，不能称为连续时间保证或精确最大可计算时间。传播距离按 |p−q|t=t 计算；宽度是 j=0 精确 u 的半高全宽。

'''
    report+=table(['算例','nx','通过到','首个失败观察','u 半高全宽','已通过距离/宽度'],bounds)
    report+='''

**这些通过区间内的位移只占波宽很小一部分，尚未达到会话要求的“经历可辨认传播后仍准确”。**延长时间会明显失真或触发停止。因此主实验得到的是短时再现和明确的失败记录，而非成功的长距离孤子传播。

## 3. 误差来源：早期空间阶成立，稍晚加密反而可能更差

固定 h=1/4，在共同早期时刻 t=0.005 比较全域误差。末列单独记录尝试推进到 T=0.05 的结果，未用较短失败时刻代替共同终止时刻来计算空间阶。

'''+table(['算例','nx','u 最大误差','v 最大误差','u 观测阶','v 观测阶','T=.05 推进'],refinement)
    report+='''

![独立加密与误差来源](figures/fig7_dynamics_refinement.png)

A 的早期空间阶接近四阶；B 的粗网格仍处于渐近区前段。T=0.05 时，细网格的误差可显著增大，部分未完成。dt 减半后的曲线几乎重合，说明在这些参数上，仅减小时间步无法消除失真；这不是一般时间稳定性的证明。

有限 h 精确解与连续精确解另在固定 x,y∈[-1.5,1.5]、t=0/0.2/−0.35 比较；x 用含端点梯形权重，y 用中点权重。下表给最细 h=1/64 的绝对误差和最后一次减半观测阶，两个场、两个范数均保留。

'''+table(['算例','t','u Linf 误差/阶','u L2 误差/阶','v Linf 误差/阶','v L2 误差/阶'],limits)
    report+='''

两种精确解的固定 j 传播速度均为 p−q，与 h 无关，但波形及 y 相位改变。上述结果只支持测试解族的二阶逼近。

下表在 nx=256、共同 T=0.005 分开报告求解误差、模型误差、实际总误差，参照都位于同一物理点。误差向量之和逐点核对；**范数不能直接相加当等式**。粗 h 的部分指标由模型误差主导；h 变小时求解误差占比上升，尚未形成完整的实际求解器二阶收敛验收。

'''+table(['算例','h','场','求解误差 Linf','模型误差 Linf','总误差 Linf'],decomp)
    report+='''

## 4. 同一连续问题上的模型比较与成本

两模型使用同一网格、RK4、时间步、连续初值与连续时变边界，最终都对照连续解。下表早期误差取共同 t=0.005；后面保留最后观察时刻和相对误差，用来揭示失真，不能把完成运行等同于精度通过。

'''+table(['算例','模型','h','早期 u 误差','早期 v 误差','最后观察 t','末时 u 相对误差','末时 v 相对误差'],match)
    report+='''

![模型比较与成本](figures/fig8_dynamics_comparison.png)

成本采用额外的顺序运行：每个配置独立重复三次并交替模型次序，取推进耗时中位数；排除初始化、绘图和诊断，包含 RHS 内边界求值。两者都为 T=0.005、20 步、80 次 RHS，扫描两档 h 与 nx。散点保留实际误差—成本关系；没有由一次计时宣布效率优越。结构模型在部分指标上更好、部分更差；本轮没有形成统一胜者，更不能把差别唯一归因于可积性。完整耗时、两场范数和各次重复保存在 JSON。

## 5. 增长、边界与可验证范围

在精确孤子初态上施加相容的 ±ε 扰动：先令 u 的扰动在两端为零，再由相邻差分得到 P 扰动，W 扰动为零；物理 v 由重构得到，未独立乱改四个变量。初始 (P,W) 欧氏范数归一化为 1。物理波数 k=2πm/20，m=2/16；ε=1e-5/5e-6；dt=0.00025/0.000125。两轨道中心差商给出沿数值轨道的响应。

'''+table(['算例','k','t=.01 响应增益','幅度/步长对照最大相对差','最后成对观察 t','目标 .1'],resp)
    report+='''

![扰动响应与误差高频指标](figures/fig9_dynamics_sensitivity.png)

较高波数的短时响应更强；幅度与步长变化后的早期响应一致。图中竖线标记无扰动主实验通过到的时刻，竖线之后是已不够准确的数值轨道附近响应，**不能再解释为精确孤子背景的稳定性结论**。高频指标取误差 Fourier 系数中高于 75% Nyquist 的部分，作为趋势诊断，不是谱范数定理。两档扰动没有覆盖任意方向；零背景谱也不能直接替代这里的孤子背景实验。

扩大 x 区域时保持 dx 不变；扩大 y 区域时保持 h 不变。下表均限制在共同区域 x∈[-10,10)、y∈[-1.5,1.5]、共同已到达时刻 T=0.01 计算误差。末列是精确解在相同物理 x 左右端点的周期不匹配，不是相邻网格值之差。更晚的失败记录另保留在 JSON，未用不同停止时刻作扩域比较。

'''+table(['算例','x 长度','y 半宽','共同区域 u 误差','共同区域 v 误差','精确周期端点差'],boundary)
    report+='''

x 扩域并未实质消除误差；y 扩域可改变误差放大，说明开链重构及区域大小也是当前计算问题的一部分。不能仅靠 x 端点残差很小就排除全部边界影响。尚未做提高算术精度的系统扫描，本轮不把失真唯一归因为舍入误差。

![全域误差图：明确标记为门槛失败后的时刻](figures/fig10_dynamics_error_maps.png)

## 6. 本轮结论与两孤子增强项

本轮把“能运行、有时间阶”推进到了可复查的动力学误差、模型比较和失败边界：早期空间精度与精确解族二阶极限成立；固定终点的长一些计算受明显增长影响；步长减半和 x 扩域并未解决；结构方案没有统一数值优势。

**研究主线尚未完成的是：足够传播距离的准确单孤子演化，以及由此支持的两孤子完整散射。**当前 A/B 的可验证位移远小于波宽，未满足进入完整散射实验的前置条件。本轮不把已有解析两孤子相移改称求解器相移，也没有声称两孤子在所有方法下都不可能计算。依照会话，两孤子是有条件的增强项，暂不强行跑出一个无误差控制的相移。

下一步应针对已定位的增长与开链重构敏感性研究可控计算设置，再判断能否获得较长传播窗口。若引入限带、滤波、附加阻尼或新的边界闭合，须分别记录修改后的方程/计算设置，并重新做共同初边值、空间阶和动力学验收；不能悄悄算入原模型成绩。

## 7. 复现、验证与数据

在 numerics 目录依次运行（成本实验须在其他实验结束后运行）：

```powershell
python -u experiments/dynamics_study.py all
python -u experiments/dynamics_controls.py
python -u experiments/dynamics_cost.py
python -u experiments/dynamics_report.py
python -u experiments/check_regressions.py
```

新增数据为 out/dynamics_*.json、out/dynamics_field_*.npz、out/response_*.npz；各配置有原始历史、两场范数、拟合值、RHS 次数、停止原因和源码哈希。五组主体图加全域误差补图直接从这些数据生成。失败实验属于研究结果，不伪装成回归通过。最早全量尝试的扰动部分曾因非有限值触发断言，保留 dynamics_run_log.txt；现改为显式记录科学失败并完成全配置检查，最终日志分项保存。
'''
    (ROOT/'DYNAMICS_REPORT.md').write_text(report,encoding='utf-8')
    baseline=(ROOT/'BASELINE_REPORT_20260922.md').read_text(encoding='utf-8')
    baseline='\n'.join('#'+line if line.startswith('##') else line
                       for line in baseline.splitlines()[1:])
    appendix='\n\n## 附录：2026-09-22 基础验收记录\n\n以下保留先前 E0–E7 与时间阶验收的范围和原始表格。最新研究结论以前面的 2026-09-23 主体为准。\n\n'
    (ROOT/'REPORT.md').write_text(report+appendix+baseline+'\n',encoding='utf-8')
    write('dynamics_checks',checks)
    print('REPORT GENERATED',checks)


if __name__=='__main__':main()
