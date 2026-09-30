"""Generate tables, scientific figures and a qualified p-region report."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import load, key, BRANCHES, PVALUES, OUT

HERE=Path(__file__).resolve().parent
LABEL={'fixed':'固定','minus':'负支','plus':'正支','symmetric':'对称'}
EN={'fixed':'Fixed','minus':r'$r_-$','plus':r'$r_+$','symmetric':'Symmetric'}
COLORS={'fixed':'#6b7280','minus':'#167d9a','plus':'#c26520','symmetric':'#7b4d9e'}


def main():
    _,rows=load(); summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    readback=summary['readback'];audit=summary['audit']
    def error(p,route,b,c,t=.01):return readback[key(p,route,b,c)]['snapshots'][str(t)]['errors']
    def ratio(p,route,b,c,base_route,base_b,t=.01):
        a,z=error(p,route,b,c,t),error(p,base_route,base_b,c,t)
        return {f:a[f]/z[f] for f in ('u','v')}
    def pair(e,fmt='.3f'):return ' / '.join(format(e[f],fmt) for f in ('u','v'))
    def mdtable(headers,lines):
        return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+
                         ['| '+' | '.join(str(v) for v in line)+' |' for line in lines])
    def ratio_table(c,route='sd',what='sd_fd'):
        return mdtable(['p']+[LABEL[b]+'，u / v' for b in BRANCHES],
            [[f'{p:g}']+[pair(ratio(p,route,b,c,'fd' if what=='sd_fd' else route,b if what=='sd_fd' else 'fixed')) for b in BRANCHES] for p in PVALUES])
    def winners_table(c):
        result=[]
        for p in PVALUES:
            result.append([f'{p:g}']+[' / '.join(LABEL[b] for b in summary['winners'][f'{p}_{r}_{c}']['strict'].values()) for r in ('fd','sd')])
        return mdtable(['p','FD 最小误差网格，u / v','SD 最小误差网格，u / v'],result)
    full=[]
    for c in ('main','time_half','fine_half','fine_quarter'):
        for route in ('fd','sd'):
            ps=sorted({r['spec']['p'] for r in rows.values() if r['spec']['config']==c and r['spec']['route']==route})
            rr=[]
            for p in ps:
                rr.append([f'{p:g}']+[pair(error(p,route,b,c),'.6e') if key(p,route,b,c) in rows else '未测' for b in BRANCHES])
            full.extend([f'## {c} / {route.upper()}','',mdtable(['p']+[LABEL[b]+' u / v' for b in BRANCHES],rr),''])
    (OUT/'full_tables.md').write_text('# 全部物理场 L∞ 总误差\n\n8Nx 共同物理点评价；所有轨道完成。完成不代表稳定。\n\n'+'\n'.join(full),encoding='utf-8')

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(2,2,figsize=(11,7.8),sharex=True,layout='constrained')
    for i,c in enumerate(('main','fine_half')):
        for j,f in enumerate(('u','v')):
            ax=axs[i,j]
            for b in BRANCHES:
                yy=[ratio(p,'sd',b,c,'fd',b)[f] for p in PVALUES]
                if c=='fine_half' and b!='fixed':
                    ax.plot(PVALUES[:5],yy[:5],'-o',ms=4,color=COLORS[b],label=EN[b])
                    ax.plot(PVALUES[4:],yy[4:],'--o',ms=4,mfc='white',color=COLORS[b])
                else:ax.plot(PVALUES,yy,'-o',ms=4,color=COLORS[b],label=EN[b])
            ax.axhline(1,c='black',ls=':',lw=1);ax.grid(alpha=.18)
            ax.set_title(f'{"512 nodes" if i==0 else "1024 nodes"}: {f}')
            ax.set_ylabel(r'$E_{SD}/E_{FD}$, same mesh rule')
            if i==1:ax.set_xlabel('p (a=4, q=3)')
    axs[0,0].legend(ncols=2,fontsize=9)
    fig.suptitle('DLW / Euler / T=0.01: lower than 1 favors SD\nDashed moving-mesh segments: large-p growth diagnostics; not a certified accuracy region',fontsize=12)
    for ext in ('png','pdf'):fig.savefig(HERE/f'sd_fd_regions.{ext}',dpi=180)
    plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
    for j,f in enumerate(('u','v')):
        ax=axs[j]
        for c,marker in (('main','o'),('fine_half','s')):
            yy=[ratio(p,'sd','symmetric',c,'sd','fixed')[f] for p in PVALUES]
            ax.semilogy(PVALUES,yy,'-'+marker,label='512 nodes' if c=='main' else '1024 nodes',ms=5)
        ax.axhline(1,c='black',ls=':',lw=1);ax.grid(alpha=.18,which='both')
        ax.set_title(f'{f} total error');ax.set_xlabel('p (a=4, q=3)')
        ax.set_ylabel(r'$E_{SD,sym}/E_{SD,fixed}$');ax.legend()
    fig.suptitle('Symmetric moving mesh: its main-grid benefit does not persist at all resolutions',fontsize=12)
    for ext in ('png','pdf'):fig.savefig(HERE/f'symmetric_regions.{ext}',dpi=180)
    plt.close(fig)

    candidate=[]
    for p in (.75,.9,.95,1.,1.05,1.1,1.25):
        line=[f'{p:g}',pair(ratio(p,'sd','minus','main','fd','minus')),
              pair(ratio(p,'sd','minus','fine_half','fd','minus'))]
        line.append(pair(ratio(p,'sd','minus','fine_quarter','fd','minus')) if key(p,'sd','minus','fine_quarter') in rows else '未测')
        candidate.append(line)
    symtab=mdtable(['p','主 SD 对称/固定，u / v','细 SD 对称/固定，u / v'],
        [[f'{p:g}',pair(ratio(p,'sd','symmetric','main','sd','fixed')),pair(ratio(p,'sd','symmetric','fine_half','sd','fixed'))] for p in PVALUES])
    earlier=mdtable(['p','细网格 T=.005，SD−/FD−','细网格 T=.01，SD−/FD−'],
        [[f'{p:g}',pair(ratio(p,'sd','minus','fine_half','fd','minus',.005)),pair(ratio(p,'sd','minus','fine_half','fd','minus'))] for p in (.9,.95,1.,1.05,1.1)])
    growth=mdtable(['p','细 SD 对称 E_u / E_v','T=.01/.005 误差增长，u / v','高频分量/总节点误差，u / v'],[
        [f'{p:g}',pair(error(p,'sd','symmetric','fine_half'),'.3e'),
         pair({f:error(p,'sd','symmetric','fine_half')[f]/error(p,'sd','symmetric','fine_half',.005)[f] for f in ('u','v')},'.2f'),
         pair({f:readback[key(p,'sd','symmetric','fine_half')]['snapshots']['0.01']['bands'][f]['high_band_nodal']/readback[key(p,'sd','symmetric','fine_half')]['snapshots']['0.01']['bands'][f]['total_nodal'] for f in ('u','v')})] for p in (1.,1.5,1.75,2.,2.25,2.5)])
    report=r'''# DLW 的 p 参数优势带：持续动网格与 FD/SD 的受控比较

日期：2026-09-26。所有数据为实际 Euler 演化结果；原求解器、历史轨道、根 HTML 和 Lean 未改。

## 1. 可以给出的结论

**可以给出固定条件下的采样优势带。当前证据不支持一条仅由 p 决定、跨网格分辨率和演化时间都成立的方案排名。**

1. **密度选择有分区。** 在主配置 Nx=512、T=.01，SD 的 p=.75、1、1.25、1.5 中，正支给出最小 u 误差，对称密度给出最小 v 误差；p=2、2.25、2.5 则是对称的 u 最小、正支的 v 最小。主时间步减半后这些具体排名保持。它们通常是双场取舍，而非单一方案同时支配两个场。
2. **对称密度具有局部价值，但收益依赖分辨率。** 主配置 SD 对称网格在全部 9 个 p 采样点均双场胜过自己的固定网格。細 x 配置只有 p=.5、.75 的双场改善有清楚余量；p=1 的 v 仅接近持平，既有四分之一步长检查甚至轻微反转；p=1.25、1.5 是双场取舍；p≥1.75 的所测点上对称不再双场胜过固定，且后面逐步出现强增长。
3. **有可积方案的候选优势带。** a=4、q=3、p∈{.9,.95,1,1.05,1.1}，在 T=.01 的主网格、主网格减步、细 x 配置上，SD+r− 均双场优于 FD+r−。细网格误差比分别落在 u=.896–.952、v=.834–.969；p=.9、1、1.1 再减半时间步仍保持双场优势。这是与同一密度 FD 的比较，不能称为所有八种方案中的统一最优。
4. **观测时间是结论条件。** 同一候选带的细网格在 T=.005 时，SD+r− 的 u 全部较差；p=.9、.95 的 v 也较差。因而不能把 T=.01 的发现写成整个时间段上的优势。

本轮共 **276 条记录，224 条新演化＋52 条完全匹配的历史复用**，全部算到 T=.01。部分大 p 细网格结果虽完成，但误差强烈增长，不能用于宣称稳定精度优势。没有进行随机总体抽样或统计显著性检验，也没有认证连续区间端点。

## 2. GSG 原文实际支持什么

Feng–Sheng–Yu 的 GSG 原文 §4.2，印刷页 365–367，确实有波形分类：

\[
0<p<1/\sqrt2:\text{规则 kink},\qquad
1/\sqrt2<p<1:\text{不规则 kink},\qquad
p>1:\text{loop}.
\]

但精度比较使用的是 **p=.8/√2、.9、2 三个代表值**。原文说非可积方法在 kink/不规则 kink 示例有优势、可积 scheme 1 在 loop 示例更好；这不等于证明每个连续区间内所有 p 的误差排名一致。

原文依据：[gsg.txt](../../Paper/sources/gsg.txt)，搜索 “according to values of p1” 和 “simulation for kink and irregular kink”。本轮 DLW 的 p 取值一直在同一个正则单孤子族内，没有套用 GSG 的 kink/loop 阈值。

## 3. 冻结设置与比较对象

\[
\boxed{a=4,\ q=3,\ \rho=p+q,\ c=\kappa=0,\ \beta=1,\ h=1/8,\ T=.01.}
\]

ρ 随 p 取 p+q，是为了保持 tau 的初始相位常数 log(ρ/(p+q))=0；不是单独优化幅值。只改变形状参数 p。

| 设置 | Nx | Euler Δt | p 样本 |
|---|---:|---:|---|
| main | 512 | 1.25e−5 | .5:.25:2.5，加 .9/.95/1.05/1.1 的固定与负支 |
| time_half | 512 | 6.25e−6 | 同上 |
| fine_half | 1024 | 6.25e−6 | 同上 |
| fine_quarter | 1024 | 3.125e−6 | .9/1/1.1，只测固定与负支 |

主扫描 9×8×3=216 条；局部加密与减步 60 条。8 种方法为 FD/SD × 固定/负支/正支/对称。所有 y 层共用一套持续移动的 x 网格，Lx=40，yhalf=1.5。映射 x 导数为四阶中心 D1，D2=D1D1；y 的两种方法均二阶一致。

半离散 SD 是原始有限 h 结构。令 P=δ−u、w=v−δ0u，

\[
H=u^2/2+2au+h^2(w^2/32-w/4),\qquad
P_t=-\delta_-H_x-(P+M_-w)_{xx},
\]
\[
w_t=-[(u+2a)w-4u]_x+w_{xx},\qquad v=w+\delta_0u.
\]

FD 为同物理变量的普通交错差分：

\[
P_t=-\delta_-(u^2/2+2au)_x-(M_-v)_{xx},\qquad
v_t=-[(u+2a)v-4u]_x-(\delta_0u)_{xx}.
\]

两者最终都推进 P/v。对称密度使用有限 h 修正

\[
r^{sym}_j=1-\frac{v_j}{4}-\frac{w_{j+1}-2w_j+w_{j-1}}{32},
\quad R_{sym}=(R_-+R_+)/2,\quad Q_{sym}=(Q_-+Q_+)/2,
\]
\[
\dot X=(Q-Q_L)/R.
\]

负/正支见[密度推导](../dlw_mesh_densities_20260926/REPORT.md)。每步从当前数值场重算 R/Q，同步 Euler 推进网格和场，包含 ALE 传输；没有冻结网格、滤波或内部精确回填。相同密度规则用于 FD/SD，局部半离散守恒恒等式属于 SD；不宣称最终 x 差分＋Euler＋动网格算法整体可积。

两路从相同连续物理初值、同一 y 边界开始。不同密度初始等质量网格不同，但参照解相同。误差为

\[
E_f(T)=\max_{x\in\mathcal X_{8N_x},\ |y_j|<1.5}
|f_{num}(x,y_j,T)-f_{cont}(x,y_j,T)|,\quad f=u,v,
\]

物理评价核心 x∈[−10,10)，共同均匀物理点；这仍是 L∞ 的离散逼近，不是解析全域上确界。所有主排名统一采用 **8Nx 评价**；历史报告多采用 4Nx，因此小数会有变化。包括空间、Euler 和输出重构贡献的总误差，没有相位对齐或减掉离散模型偏差。这里比较同配置下的精度，没有做相同运行时间的算力比较。

## 4. 密度怎样随 p 选：两个场分别给出答案

下面是四种网格中各场误差严格最小的网格，未把 u/v 合成任意权重的总分。

### 主配置 Nx=512

{MAIN_WINNERS}

p=.5 的 SD v，负支与对称很接近，减半时间步后排序改变；p=.75 的 FD v 也有正支/对称的近似持平翻转。它们不应被解释为明确分界。可复现数据同时保存“距离最小误差 2% 内”的近似并列方案；2% 是展示容差，不是置信区间。

### 细 x 配置 Nx=1024

{FINE_WINNERS}

p=.5/.75/1 中 SD 负支的原始数值均最小，但 p=1 的 u 相对于对称只小约 .57%，属于近似并列。p=1.5 的 SD 固定/对称 u 仅差约 1.9%。p≥1.75 的表格仍诚实列出最小值，但需要连同第 7 节的增长诊断阅读，不赋予渐近精度含义。

## 5. 专门回答对称密度：相对自己的固定网格

比值小于 1 表示动网格改善；每格 u / v。

{SYMMETRIC_TABLE}

![对称密度随 p 和分辨率的收益变化](symmetric_regions.png)

这说明主配置中对称密度的作用真实存在，而不是只在原先单个 P6 上偶然出现；但细 x 配置的 y 离散/传播误差和数值增长改变了主导项，不能把主表的收益直接外推。

尤其 p=1 的细网格 v 比值约 .997，余量太小；既有 [P6 64倍评价与四分之一步长复核](../dlw_symmetric_mesh_euler_20260926/REPORT.md)给出该值最终约 1.000651。本轮不把它算成稳健双场优势。

## 6. 可积性对应的比较：同一种网格规则下 SD/FD

### 主配置：E_SD / E_FD

{MAIN_RATIOS}

主配置中：固定 SD 在 9/9 点双场胜 FD；负支和对称分别在 8/9 点双场胜（对称 p=.5 的 v 只微小领先，减步后仍微小领先）；正支则低 p 的 v 较差、高 p 的 u 较差，中间 p=1、1.25、1.5 双场胜。主配置时间步减半后所有上述 SD/FD 逐场优劣符号保持，仍不能扩展成跨分辨率定律。

### 细 x 配置：E_SD / E_FD

{FINE_RATIOS}

![同监测网格下 SD/FD 误差比](sd_fd_regions.png)

例如 p=1，对称 SD/FD≈1.105/1.048，两个场都较差；负支则≈.917/.895，两个场都较好。**“对称动网格改善了 SD 自己”与“SD 比同密度 FD 更好”是两个不同结论。**

### 加密确认的负支候选带

{CANDIDATE}

这里 .9/.95/1.05/1.1 是看到粗扫描交叉后补充的探索性点，不是假装事前指定的统计验证样本。五个点的三个共同配置全双场胜 FD；端点和中心的第四配置亦保持，32Nx/32倍重构评价也不改变该判断。细配置 p=.75 的 v 较差，p=1.25 的 u 较差。因此可以把 **[.9,1.1] 称为“已采样支持的候选优势带”**，但 .9 和 1.1 不是实际交叉点，更没有对区间内每个实数作保证。

还需保留观测时刻限制：

{EARLIER}

这不是一个全时间精度优势。当前误差来自各源项在有限时间内的传播和相消，演化时间本身能改变排名。没有因为中间时刻不支持优势而删掉这些数据。

## 7. 大 p：完成轨道也可能失去精度

以下固定细 x 配置、SD 对称网格，列出 T=.005 到 .01 的变化。高频定义为超过计算坐标 Nyquist 频率 40% 的误差 Fourier 分量。

{GROWTH}

高频分量/全误差的两个 L∞ 范数之比可能大于 1，它不是能量占比。不能单独用“超过 .1”判定不稳定；主网格截断误差本来也可能有较大高频分量。但这里 p=2、2.25、2.5 同时出现非常大的时间增长、空间加密恶化，且旧 P2 的 1e−12 初值扰动实验显示强敏感性，足以要求收窄精度解读。p=1.75 是已出现明显增长迹象的采样点，不是认证的稳定性边界。

对称网格降低了相对负支/正支的某些增长幅度，但没有消除问题。例如 p=2.5 时对称误差仍约 .545/.876，固定为 .001767/.001693。即使所有276条都完成，也绝不能把后面的有限数字称为可接受的精度或稳定性证据。

## 8. 为什么 p 会改变排名：可证明的参数依赖与机制解释

在这条切片上，连续孤子的相位和形状参数为

\[
k=p+3,\quad \ell=\frac1{p-4}+\frac17=-\frac{p+3}{7(4-p)},
\quad\gamma=\frac{4-p}{7},\quad c_{wave}=p-3.
\]

连续正则条件 p<4；当前有限 h 原式的正 Gram 分支充分条件是 p<4−h/2=3.9375。所有 .5≤p≤2.5 样本满足，因而本轮交叉不是波形从 kink 变 loop。

令 σ(z)=1/(1+e^(−z))，连续分支密度在每一 y 层分别是

\[
r^-=1-k\ell\,\sigma'(\theta),\qquad
r^+=1-k\ell\,\sigma'(\theta+\log\gamma),
\]
\[
\max_x r^\pm=1+\frac{(p+3)^2}{28(4-p)},\qquad
\frac{d}{dp}(\max_xr^\pm-1)=\frac{(p+3)(11-p)}{28(4-p)^2}>0.
\]

连续两密度中心相隔 |log γ|/k；对称组合对两处加密作折中。该最大值公式针对连续单层密度，不是已对齐/平均后有限 h 数值监测函数的精确峰值。

随 p 增加，x 方向变窄，|ℓ| 增大、y 方向变化增强，密度峰值也从 1.125 增至约 1.72024。于是：

- 两种密度对 u/v 的高曲率区覆盖不同，能出现“正支更利于 u、对称更利于 v”的取舍；密度越对称并不自动使两个场都更准。
- 同一 Nx 下网格局部压缩改变物理 x 差分误差以及线性化数值传播。x 加密后，原先降低 x 截断误差的收益可能变弱，有限 h 的 y 误差反而显现。
- 非均匀 x 四阶公式的首项还含映射导数，不能只用 Δx^4 或密度峰值计算误差常数。Euler 的 O(Δt)、y 的 O(h²)、映射 x 的 O(Δξ⁴) 经耦合演化后有带符号的相消/相长；p 和 T 均会改变这种配合。

这些是参数影响途径；本轮尚未完成对每个动网格交叉点的误差源定量分解，不能把上述直觉写成已证实的完整因果解释。此前[固定网格的受迫误差分解](../dlw_advantage_regions_20260926/REPORT.md)提供分析方法，但动网格需把节点自由度一起线性化，不能直接挪用旧系数。

### 能否严格说存在某个优势邻域？可以，但需附条件

对固定 h/Nx/Δt/T、固定边界和评价规则，假设邻域中 R>0、J>0、重构保持光滑。Euler 有限步映射及误差随 p 连续。记

\[
D_f(p)=E_{B,f}(p)-E_{A,f}(p),\quad f=u,v.
\]

若某 p₀ 的两个 D_f(p₀)>0，连续性保证存在一个未定大小的开邻域，两场仍由 A 更准。这是严格的条件结论，不能单凭样本反推该邻域恰好覆盖 [.9,1.1]。

若进一步获得经过认证的数值误差界 η_f 与邻域 Lipschitz 界 L_f，使真实 D_f(p₀)≥D_f^calc(p₀)−η_f>0，则任何

\[
|p-p_0|<\min_{f=u,v}\frac{D_f^{calc}(p_0)-\eta_f}{L_f}
\]

内可得双场优势。本轮未计算经认证的 L_f/η_f，只有实际网格与时间敏感性检查；因此结果是采样证据，不是区间算术认证或数学误差排名定理。

## 9. 实现、指标与数据审核

{AUDIT}

所有138组同 p/密度/配置的 FD–SD 配对都重新构造初态，并逐元素核对一致；不同密度之间比较同一物理解而非同一节点数组。276个 NPZ 和18个源码/比较清单哈希通过；552个快照的 8Nx 物理误差重新读取计算，最大差0。

初始输出重构误差相对最终误差在各主/细配置中都低于 4.04e−6。4Nx→8Nx 的全量最大变化5.735%发生在误差增长配置，因此统一报告8Nx结果；8Nx→32Nx的所测点最大变化 .564%，候选带不超过 .149%。32Nx只是加密检查，不构成严格上确界认证。

新轨道的非固定网格每步都有非零速度；全量最小 J 为 .255076，快照最小 R 为 .853138。正性与无节点交叉只保证几何可用，不等于误差小。所有失败列表为空，所有大误差轨道照常保留，未作幸存者筛选。旧源码哈希校验成功；本轮没有修改旧求解器、旧实验或任何 Lean/根报告。

原始全表：[out/full_tables.md](out/full_tables.md)；机器可读：[errors.csv](out/errors.csv)、[ratios.csv](out/ratios.csv)、[summary.json](out/summary.json)。

## 10. 复现与可继续推进的工作

```powershell
python Workspaces/dlw_p_regions_20260926/scan.py --workers 4
python Workspaces/dlw_p_regions_20260926/refine.py --workers 4
python Workspaces/dlw_p_regions_20260926/analyze.py
python Workspaces/dlw_p_regions_20260926/make_report.py
```

运行器检查已冻结的计划、源码与历史清单，只补缺失记录；不会重写已完成轨道。下一步应先以 (p,T) 误差符号图定位可重复的候选带，并同时线性化场和网格，解释相消项及大 p 增长来源；之后才能考虑给出可认证的区间边界。本轮没有执行这些后续工作，也没有改变 Euler 或引入额外调参维度。
'''
    audit_table=mdtable(['检查','结果'],[
        ['轨道/新增/复用',f"{audit['records']} / {audit['new']} / {audit['reused']}"],
        ['完成/失败',f"{audit['completed']} / {len(audit['failures'])}"],
        ['NPZ核验 / FD–SD同初态配对',f"{audit['verified_profiles']} / {audit['paired_initial_states']}"],
        ['误差回读最大绝对差',str(audit['error_readback_max'])],
        ['4Nx→8Nx评价最大变化',f"{100*audit['evaluation_change']:.4f}%"],
        ['16→32倍重构最大变化（4Nx评价）',f"{100*audit['reconstruction_change']:.6f}%"],
        ['主配置Euler减步最大误差变化',f"{100*audit['all_main_time_change']:.4f}%"],
        ['局部细配置再减步最大误差变化',f"{100*audit['all_fine_time_change']:.4f}%"]])
    for token,value in dict(MAIN_WINNERS=winners_table('main'),FINE_WINNERS=winners_table('fine_half'),
         SYMMETRIC_TABLE=symtab,MAIN_RATIOS=ratio_table('main'),FINE_RATIOS=ratio_table('fine_half'),
         CANDIDATE=mdtable(['p','主配置 SD−/FD−','细配置 SD−/FD−','细配置再减步 SD−/FD−'],candidate),
         EARLIER=earlier,GROWTH=growth,AUDIT=audit_table).items():
        report=report.replace('{'+token+'}',value)
    (HERE/'REPORT.md').write_text(report,encoding='utf-8')
    print('Generated REPORT.md, out/full_tables.md and two PNG/PDF figures.')


if __name__=='__main__':main()
