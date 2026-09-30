"""Data-derived report and tables for the second density class."""
from pathlib import Path
import json
from analyze import load_rows
from experiment import OUT,CASES

HERE=Path(__file__).resolve().parent
new,_,old=load_rows();rows={**old,**new['rows']}
audit=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))

def e(case,route,branch,phase,t=.01):
    return rows[f'{case}_{route}_{branch}_{phase}'].get('snapshots',{}).get(str(t),{}).get('errors')
def cell(v):return '未完成' if v is None else f'{v["u"]:.3e} / {v["v"]:.3e}'
def table(route,phase='main',cases=CASES,t=.01):
    lines=['| 参数 (a,p,q) | 固定 | r− | r+ | 对称 |','|---|---:|---:|---:|---:|']
    for case in cases:
        p=CASES[case]
        lines.append(f'| {case} ({p.a:g},{p.p:g},{p.q:g}) | '+' | '.join(cell(e(case,route,b,phase,t)) for b in ('fixed','minus','plus','symmetric'))+' |')
    return '\n'.join(lines)
def p6(phase):
    lines=['| 网格 | 普通差分 u / v | 可积半离散 u / v |','|---|---:|---:|']
    for b,label in [('fixed','固定'),('minus','r− 持续移动'),('plus','r+ 持续移动'),('symmetric','对称持续移动')]:
        lines.append(f'| {label} | {cell(e("P6","fd",b,phase))} | {cell(e("P6","sd",b,phase))} |')
    return '\n'.join(lines)
def gains():
    lines=['| 参数 | FD 对称/固定，u / v | SD 对称/固定，u / v |','|---|---:|---:|']
    for case in CASES:
        cells=[]
        for route in ('fd','sd'):
            sym,base=e(case,route,'symmetric','main'),e(case,route,'fixed','main')
            cells.append(f'{sym["u"]/base["u"]:.3f} / {sym["v"]/base["v"]:.3f}')
        lines.append('| '+case+' | '+' | '.join(cells)+' |')
    return '\n'.join(lines)
def seeds():
    lines=['| P2，Nx=1024，Δt=6.25e−6 | 无扰动，对称 | 加 1e−12 扰动，对称 | 同扰动，旧 r+ |','|---|---:|---:|---:|']
    for route in ('fd','sd'):
        lines.append(f'| {route.upper()} | {cell(e("P2",route,"symmetric","fine_half"))} | {cell(e("P2",route,"symmetric","fine_seed"))} | {cell(e("P2",route,"plus","fine_seed"))} |')
    return '\n'.join(lines)

text=r'''# DLW 第二类密度：对称守恒密度的持续动网格实验

日期：2026-09-26。沿用上一轮 Euler、同一连续物理参照和全部主参数；新增对称密度轨道，与已冻结的固定/r−/r+ 轨道匹配比较。

## 1. 当前结论

**对称密度有明确的局部精度价值，尤其能改善某些配置下的 v；它是有用的取舍方案，还不能取代负支成为统一默认选择。**

- 主配置中，普通差分 FD 在 8/8 组参数上双场优于固定网格；可积半离散 SD 为 6/8。主配置减半 Euler 步长，以上双场改善判断不变。
- P6=(4,1,3) 的 SD 对称网格，主配置 u/v 总误差比固定网格低约 65.9%/66.9%。其 v 比负支低约 33.7%、比正支低约 21.7%；u 则低于负支、但高于正支。
- 没有一组主参数显示对称网格在两个场上同时胜过两个单独分支。某些场有改进，不意味着整套方案支配所有其他候选。
- P6 细 x 网格上，对称 SD 的 u 改善仍约 17.5%；v 收益由约 1.2% 随减步降至接近零，四分之一步长下误差略增约 .065%。负支在该配置仍改善两个场。因此暂不能把对称密度称为比负支更稳健。
- 对称组合减轻了部分 P2 细网格增长的幅度，但没有消除高频敏感性；P10 细动网格仍未完成，减半时间步也未修复。

新增 72 条轨道：66 完成，6 未完成，全部保留完整或失败前的数值状态。旧实验未重算、未改写，比较前核对了其源码和数据哈希。

## 2. 本轮实际使用的密度与算法

连续对称密度是 \(r_0=1-v/4\)。对于当前 c=κ=0 的有限 y 格距系统，本轮使用精确对齐后的版本：

\[
\boxed{r^{\mathrm{sym}}_j
=\frac{r^-_j+\widehat r^+_j}{2}
=1-\frac{v_j}{4}
-\frac{w_{j+1}-2w_j+w_{j-1}}{32}},
\qquad w=v-\delta_0u.
\]

正支先平均到 F 层，两支在同一组内部 y 层等权聚合，取

\[
R_0=(R_-+R_+)/2,\qquad Q_0=(Q_-+Q_+)/2,
\qquad \dot X_i=\frac{Q_{0,i}-Q_{0,L}}{R_{0,i}}.
\]

密度与通量先混合，再计算速度。在同一当前状态和网格上，该速度也可写成密度加权速度平均：

\[
V_0=\frac{R_-V_-+R_+V_+}{R_-+R_+}.
\]

这并不意味着最终数值解或误差等于旧两条轨道的平均。网格位置、物理 x 导数、右端和随后状态会持续相互影响；新轨道必须实际求解。

从解析初始密度积分反演初始等质量网格，之后每一步重新由当前数值场计算 R,Q。物理 P=δ−u、v 与节点位移同步采用 Euler，含 ALE 传输项。所有 y 层共用一套 x 网格，β=1，不拟合参数，不做滤波、内部精确回填或冻结网格。

对 SD，该对称组合继承两支的精确半离散局部守恒关系；对 FD，相同 R,Q 作为共同网格控制规则，不宣称 FD 拥有同一个精确局部守恒律。最终 x 差分＋Euler 系统的完整可积性仍未证明。

| 项目 | 固定设置 |
|---|---|
| 空间方法 | 原始可积 SD 与普通 FD，c=κ=0；映射 x 四阶中心 D1，D2=D1D1 |
| 主网格 | x∈[−20,20)，Nx=512；y 格距 h=1/8，24 个 F 层 |
| 主时间推进 | Euler，Δt=1.25e−5，T=.005/.01 |
| 主误差 | 同一连续 u/v 的 L∞ 总误差；共同物理核心 x∈[−10,10)、\(\lvert y\rvert<1.5\) |
| 初态与边界 | 与旧实验同一连续单孤子、同一重构和 y 边界；谱幅值 ρ=p+q |
| 敏感性检查 | 全部主参数减半时间步、x 加密；P1/P2/P6/P10 加密 y 与细 x 减步；P6/P5 重点四分之一步长 |

## 3. 主表：每格为 u / v 的 L∞ 总误差

Nx=512、h=1/8、Δt=1.25e−5、T=.01。

### 普通差分 FD

@@FD@@

### 可积半离散 SD

@@SD@@

相对各自固定网格的误差比，小于 1 表示改善：

@@GAINS@@

![对称密度相对固定网格](symmetric_benefits.png)

P5 的 SD 对称网格仍使 u 略变差，P10 的 SD 对称网格仍使 v 变差。不能将对称性本身当成双场精度保证。

## 4. P6：主网格对 v 很有效，细网格收益需要收窄表述

主配置：

@@P6MAIN@@

SD 对称网格的 u/v 相对固定网格分别减少约 65.9%/66.9%；其 v 是三种动网格中最小的，但 u 仍比正支高约 29.7%。普通差分中也有相似的 u/v 取舍。

Nx=1024、Δt=3.125e−6，仍为同一个 T=.01：

@@P6FINE@@

细网格上，FD 对称密度双场改善约 46.5%/41.2%；SD 的 u 改善约 17.5%，v 约不变（略增 .065%）。此时 SD 的负支同时优于对称密度的两个场；相同对称网格规则下，FD 的两个场也都比 SD 小。

为了排除“v 的收益仅仅很小但真实存在”的误读，已在相同已保存末态上将共同物理评价点和重构密度大幅加密：

| P6，SD，Nx=1024 | 对称/固定 u | 对称/固定 v |
|---|---:|---:|
| Δt=1.25e−5 | .823983 | .988200 |
| Δt=6.25e−6 | .824855 | .996486 |
| Δt=3.125e−6 | .825313 | 1.000651 |

表中取64倍评价/重构采样；从32倍增到64倍，误差变化最多约 .00165%。这支持“v 没有保持可确认的改善”，不宜把 .065% 的劣势宣传成重要退化。该数据只覆盖所测时间步，也不是 Δt→0 的严格极限证明。

![P6的双场取舍](p6_tradeoff.png)

图中横纵坐标分别为相对于各自固定网格的 u/v 误差比，越靠左下越好。对称密度主网格可优于负支，但这一关系在细网格的 SD 中反转。

## 5. 细网格、增长与未完成轨道

### x 加密的原始比较

Nx=1024、Δt=1.25e−5、T=.01：

普通差分：

@@FINEXFD@@

可积半离散：

@@FINEXSD@@

P2 的对称网格误差明显小于两支单独密度，但不应据此宣称已解决不稳定增长。加入幅度1e−12的相同计算坐标高频初值扰动，得到：

@@SEED@@

对称网格的扰动后误差约为旧 r+ 的三分之一，但仍比其未扰动轨道大很多。该对照说明对称化缓和了此配置的敏感性，没有消除它；不据此证明全部未扰动误差来自浮点舍入。

P10 的对称网格，Nx=1024 时 FD/SD 最后有效时间约 .008963/.008638；减半时间步后约 .008788/.008544，均在 T=.01 前发生节点交叉。加入同样的微小高频扰动后，最后有效时间约 .006913/.006888。全部失败前状态保留，没有用较早时刻的误差填补终点。

对称平均并不是耗散或高频抑制机制。当前 DLW 线性化已有高波数增长分支，网格聚集改变了可解析波数及增长尺度，因此守恒与正性仍不能替代稳定性检查。

### y 加密

保持 Nx=512、Δt=1.25e−5，h=1/16：

普通差分：

@@FINEYFD@@

可积半离散：

@@FINEYSD@@

P6 对称 SD 的双场改善保留，P10 的 SD v 变差也保留。与旧实验一致，y 平均按内部层规则构造，其有效边缘随 h 略变；此组不用于单独拟合纯 y 误差阶。

## 6. 核验与结论的精度边界

- 23 项对称实现核验通过：两支平均等于含二阶修正的直接密度；初始积分反演与原函数微分；扰动态下密度时间链式法则；SD 局部守恒；同规则 FD/SD 初态与速度一致；原固定/负/正支继承结果完全一致。
- 72 个新 NPZ、204 个旧完整或部分 NPZ 的哈希均通过；新旧源码及比较清单哈希通过。全部已保存新字段与总误差回读差为0。
- 主表16条对称轨道均每步移动；相对于各自初始节点，终点最大位移范围约1.54e−4至3.07e−3。最小J约.52875，密度最小值约1，无节点交叉。计算质量相对漂移≤6.83e−10，等分布缺陷≤1.31e−4。
- 主表SD的物理局部守恒残差≤5.63e−14；FD对应残差最大约.01695，符合两者局部守恒身份不同的预期。
- 主表初始输出误差≤3.91e−11，逐例至多约为所测终点/中点误差的2.87e−6。没有使用不同的连续初值或SD自身精确解作参照。
- 主表评价点加倍使误差最多变化约.694%；重构加倍≤.00240%；独立物理x七次样条重评变化≤.00400%。
- 时间减半没有改变主表相对固定网格的收益判断，也没有改变对称SD/FD的字段排名。但P5的FD对称/r+在u上的极小差距发生翻转；评价点加倍还使P10的SD对称/r+在u上的极小差距翻转。因此不将这些接近相等的比较计为可靠优胜。
- 全部控制中评价加倍变化≤2.46%、重构加倍≤.00248%；增长轨道只作敏感性证据，不将细小排序解释为收敛后精度优势。

这是同节点数和时间步下的确定性比较，没有等墙钟预算结论，也没有总体统计显著性结论。

## 7. 如何使用这个结果

对称密度可作为一个有价值的候选，尤其当重点关注当前 P6 主网格下的 v 精度，或希望比较两支覆盖区域的平衡效果时。它还让 P2 主配置的SD双场都胜过采用同一对称规则的FD。

若目标是在已测网格和时间步下保持P6双场改善，目前负支仍是更稳妥的默认候选。对称密度尚未展示足以替换负支的跨分辨率证据，也没有修复P10的细网格失败。

## 8. 复现与文件

依次运行 `python verify.py`、`python experiment.py --workers 4`、`python analyze.py`、`python refine_peaks.py`、`python plot.py`、`python make_report.py`。已有冻结轨道会跳过，源码或比较清单变化会拒绝混写。

- [新增轨道误差CSV](out/errors.csv)
- [核验与逐参数比较](out/summary.json)
- [P6细网格稠密评价](out/p6_dense_peak_check.json)
- [新实现核验](validation.json)
- [上一轮两支密度完整报告](../dlw_branch_mesh_euler_20260926/REPORT.md)
- [密度理论推导](../dlw_mesh_densities_20260926/REPORT.md)

原实验代码与数据、根HTML和Lean均未修改。

## 附表：T=.005主配置

普通差分：

@@EARLYFD@@

可积半离散：

@@EARLYSD@@
'''
subs={'@@FD@@':table('fd'),'@@SD@@':table('sd'),'@@GAINS@@':gains(),'@@P6MAIN@@':p6('main'),'@@P6FINE@@':p6('fine_quarter'),
      '@@FINEXFD@@':table('fd','space_x'),'@@FINEXSD@@':table('sd','space_x'),
      '@@FINEYFD@@':table('fd','space_y',['P1','P2','P6','P10']),'@@FINEYSD@@':table('sd','space_y',['P1','P2','P6','P10']),
      '@@SEED@@':seeds(),'@@EARLYFD@@':table('fd',t=.005),'@@EARLYSD@@':table('sd',t=.005)}
for a,b in subs.items():text=text.replace(a,b)
(HERE/'REPORT.md').write_text(text,encoding='utf-8')
(OUT/'main_tables.md').write_text('普通差分\n\n'+table('fd')+'\n\n可积半离散\n\n'+table('sd')+'\n',encoding='utf-8')
print('Generated REPORT.md and main_tables.md')
