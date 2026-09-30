"""Build the human-readable report from frozen results and audit data."""
from pathlib import Path
import json
from run import CASES,OUT

HERE=Path(__file__).resolve().parent
docs={name:json.loads((OUT/(name+'.json')).read_text(encoding='utf-8')) for name in ('main','time_half','space_x','space_y','supplement')}
rows={k:r for d in docs.values() for k,r in d['rows'].items()}
audit=json.loads((OUT/'summary.json').read_text())

def err(case,route,branch,phase,t=.01):
    r=rows[f'{case}_{route}_{branch}_{phase}']
    return r.get('snapshots',{}).get(str(t),{}).get('errors')

def cell(e):return '未完成' if e is None else f'{e["u"]:.3e} / {e["v"]:.3e}'

def table(phase,cases,t=.01):
    lines=['| 参数 (a,p,q) | FD 固定 | FD r− | FD r+ | SD 固定 | SD r− | SD r+ |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for case in cases:
        p=CASES[case]
        vals=[cell(err(case,route,branch,phase,t)) for route in ('fd','sd') for branch in ('fixed','minus','plus')]
        lines.append(f'| {case} ({p.a:g},{p.p:g},{p.q:g}) | '+' | '.join(vals)+' |')
    return '\n'.join(lines)

def ratios():
    ans=['| 参数 | FD r−/固定 | FD r+/固定 | SD r−/固定 | SD r+/固定 |','|---|---:|---:|---:|---:|']
    for case in CASES:
        vals=[]
        for route in ('fd','sd'):
            base=err(case,route,'fixed','main')
            for branch in ('minus','plus'):
                e=err(case,route,branch,'main');vals.append(f'{e["u"]/base["u"]:.3f} / {e["v"]/base["v"]:.3f}')
        ans.append('| '+case+' | '+' | '.join(vals)+' |')
    return '\n'.join(ans)

def p6fine():
    ans=['| 网格 | 普通差分 u / v | 可积半离散 u / v | SD/FD，u / v |','|---|---:|---:|---:|']
    for branch,label in [('fixed','固定'),('minus','r− 持续移动'),('plus','r+ 持续移动')]:
        fd,sd=err('P6','fd',branch,'fine_quarter'),err('P6','sd',branch,'fine_quarter')
        ans.append(f'| {label} | {cell(fd)} | {cell(sd)} | {sd["u"]/fd["u"]:.3f} / {sd["v"]/fd["v"]:.3f} |')
    return '\n'.join(ans)

seedlines=['| P2 r+，Nx=1024，Δt=6.25e−6 | 未加扰动 u / v | 加 1e−12 高频扰动 u / v |','|---|---:|---:|']
for route in ('fd','sd'):seedlines.append(f'| {route.upper()} | {cell(err("P2",route,"plus","fine_half"))} | {cell(err("P2",route,"plus","fine_seed"))} |')

text=r'''# DLW 第一类密度：持续动网格与 Euler 的实际比较

日期：2026-09-26。代码、数据与本报告均位于 `Workspaces/dlw_branch_mesh_euler_20260926/`。

## 1. 结论先行

**两支自然密度都已完成持续动网格实现，并用于普通差分 FD 和原始可积半离散 SD。它们有明确的短时精度收益，但收益受参数、空间分辨率和增长模态限制。**

- 主配置中，FD 的 r−、r+ 在 8 组参数上均降低 u/v 两场误差；SD 的 r− 为 6/8 组双场改善，r+ 为 5/8。Euler 时间步减半未改变主表的动网格收益判断，也未改变相同网格规则下 SD/FD 的字段排名。这是所测确定性案例的计数，不是总体统计显著性。
- P6=(4,1,3) 的 SD+r− 是当前较稳妥的候选：主网格下 u/v 误差降低约 51.2%/50.1%；x 加密并将时间步降至四分之一后，仍降低约 17.6%/3.4%。y 加密也保留双场改善。
- P6 的 SD+r+ 在主网格上降约 73.7%/57.7%，但细 x 网格上 v 反增约 5.3%。不能把主表最好的分支直接当成跨分辨率最优选择。
- P2 的细 x 动网格误差出现快速增长和高频扰动敏感性；P10 的细 x 动网格在 T=.01 前终止，减半时间步也未修复。自然密度为正并不保证足够长时间的稳定精度。
- 可积优势和动网格优势需要分别读表：相同 r− 规则下，P6 的 SD 可优于 FD；相同 r+ 规则下，P6 到细网格时 FD 反而双场更好。没有得到可积方案统一更优的结论。

共 208 条正式/控制尝试：198 条完成，10 条未完成；另保存 12 条先导轨道。失败没有剔除或替换成成功结果，补测保留了失败前的状态。

## 2. 实际实现：两种空间方法、三种网格、统一 Euler

主实验只变化空间方法和网格选择。可积式固定 c=κ=0；自然强度 β=1，没有做密度强度或系数拟合。

| 固定项 | 本轮设置 |
|---|---|
| 连续模型和参照 | 同一连续 DLW 单孤子 u、v；参数 a,p,q 不变，ρ=p+q |
| 空间方法 | 原始 SD；相同交错 y 网格上的常规中心 FD |
| 网格选择 | 固定均匀；r− 持续移动；r+ 持续移动 |
| x 范围与节点数 | [−20,20)，Nx=512；细网格检查 Nx=1024 |
| y 网格 | h=1/8，24 个 F 层；4 组参数另检查 h=1/16 |
| 时间 | 显式 Euler，Δt=1.25e−5，观测 T=.005/.01；全主表减半，重点配置再减至四分之一 |
| 物理误差评价 | 同一个 x∈[−10,10)、\(\lvert y\rvert<1.5\) 核心区域，u/v 分别计算 L∞ 总误差 |
| 边界 | 既有解析左 y 基值及 ghost，右端相对解析背景的二次扰动外推；x 使用宽周期窗口 |

这里的“总误差”包括 y 半离散、x 差分、Euler 推进和结果重构相对于共同连续物理解的综合误差；没有换用 SD 自己的有限 h 精确孤子作参照。

状态统一为 P=δ−u 与物理 v。令 w=v−δ0u，两支实际监测函数与通量是：

\[
r^-_j=1-w_j/4,\qquad q^-_j=(u_j+2a)r^-_j-\partial_xr^-_j-2a;
\]

\[
S_j=2\delta_-u_j+M_-w_j,\quad
\widetilde u_j=M_-u_j+\frac{h^2}{8}\delta_-w_j,
\]

\[
r^+_j=1-S_j/4,\qquad
q^+_j=(\widetilde u_j+2a)r^+_j+\partial_xr^+_j-2a.
\]

正支先平均到 F 层，然后两支都在同一组 22 个内部 F 层做等权平均，得到 R,Q。连续极限分别为 1−(v−u_y)/4、1−(v+u_y)/4。

初始时，反演同一连续物理初态对应的离散密度积分，得到等质量节点，并将连续物理初值直接采样到这些节点。初始 FD/SD 的节点与状态逐字节一致。随后每一个 Euler 步都重新从当前数值场计算 R,Q，推进

\[
\boxed{\dot X_i=(Q_i-Q_0)/R_i},\qquad X(\xi,t)=\xi+s(\xi,t).
\]

这里对计算问题采用周期 x 条件，因此 Q_R=Q_L；未将任意有限区间通量都假设相等。连续参照在两端的 u、v 及时间导数不匹配量最大约 1.58e−13，宽窗口排除了旧 P5 短域的明显尾部污染。

物理导数和同步时间推进为

\[
J=1+D_\xi s,\quad D_x=J^{-1}D_\xi,\quad D_{xx}=D_xD_x,
\]

\[
P^{n+1}=P^n+\Delta t(F_P+\dot X D_xP),\quad
v^{n+1}=v^n+\Delta t(F_v+\dot X D_xv),\quad
s^{n+1}=s^n+\Delta t\dot X.
\]

Dξ 是四阶中心差分；两条空间路线只在既有 y 半离散方程上不同。没有滤波、人工耗散、精确解内部回填或每步重插值重置。网格持续移动，没有引入冻结或重布时机因素。

**公平性与守恒范围：**FD 与 SD 使用相同的密度及网格速度函数。SD 的两支局部守恒关系对当前 x 差分也满足代数恒等式；FD 上相同函数只是网格驱动，不具有相同的精确局部守恒式。因而本实验比较的是相同控制规则下的两套完整算法，并不把 FD 的网格也称为精确守恒坐标。Euler/ALE 全离散整体也没有被证明可积。

## 3. 主表：T=.01 的物理总误差

每格均为 **u / v 的 L∞ 误差**。Nx=512、h=1/8、Δt=1.25e−5。

@@MAIN@@

同一空间方法内，动网格误差除以固定网格误差如下；小于 1 表示改善。

@@RATIOS@@

![主配置下的动网格收益](main_error_ratios.png)

例如 P10 的 SD 两支网格虽然稍降 u 误差，v 却增加约 12.5%/12.7%；P5 的 SD 中 u 小幅变差；P7 的 SD+r+ 中 u 增加约 15.3%。这些都保留为反例，不能只展示收益大的 P2/P6。

## 4. 加密检查：主表收益不是分辨率无关的定理

### 4.1 Euler 时间步

对全部 48 条主轨道将 Δt 减半。两个观测时刻的误差相对变化最大约 2.23%，来自误差很小的 P5 v；主表 64 个动网格/固定字段比较与 48 个 SD/FD 字段比较均无排名翻转。P5 再减至四分之一步长也保留主结论。

### 4.2 x 加密

Nx=1024，h、初始时间步和所有其他规则不变：

@@FINEX@@

P2 的大误差是需要进一步诊断的增长信号，不应作为已进入空间收敛区间的优劣判据。P10 四条动网格未完成，不能用终止前某个较小误差替代 T=.01。

### 4.3 P6 的更小时间步确认

Nx=1024、Δt=3.125e−6、h=1/8，仍比较 T=.01：

@@P6FINE@@

相对各自固定网格，FD+r− 的 u/v 降约 35.8%/33.6%，SD+r− 降约 17.6%/3.4%。SD+r+ 的 u 降约 4.3%，但 v 增约 5.3%；FD+r+ 则双场改善约 53.2%/44.5%。

这组数据最清楚地区分了两个问题：自然密度对普通差分也有效；某个动网格很好，并不自动使可积方案成为其中最准确的方法。P6 的 SD+r− 在两档 x 网格及所测时间步下保持双场优于 FD+r−，但细网格优势较主表小。

### 4.4 y 加密

保持 Nx=512，改 h=1/16：

@@FINEY@@

这组保持了 P6 的 SD+r− 双场改善，以及 P10 的 SD 动网格 v 变差。y 加密仍按“内部层等权平均”规则生成监测函数，因此平均区域的边缘随格距略变；这是完整算法的 y 分辨率敏感性检查，未据此拟合纯 y 截断误差阶。

## 5. 细网格增长：时间减半没有解决，高频扰动验证了敏感性

P10 在 Nx=1024、Δt=6.25e−6 的补测中，FD r−/r+ 最后有效时间约 .008844/.008050，SD r−/r+ 约 .008506/.007794，均早于 T=.01。终止原因为过大状态或节点交叉。两条固定网格完成了 T=.01。

对 P2 的 r+ 配置，在相同初始节点上仅给物理 v 施加幅度 1e−12 的计算坐标高频正弦扰动，其他设置不变：

@@SEED@@

扰动频率为 round(.28 Nx)，随后的演化没有滤波。P10 的相同扰动诊断使 r+ 更早在约 .0062 终止。该试验说明细网格配置对微小初值扰动非常敏感；它没有单独证明未扰动误差全部来自舍入噪声。

![持续网格运动与细网格增长诊断](motion_and_growth.png)

图左使用真实保存的节点轨迹，展示的是相对于各自初始节点的后续位移；图中、右的“高频段”指计算坐标 Nyquist 频率 40% 以上的误差，仅用于诊断，没有从求解器中删去这些成分。

一个已有理论解释是：连续零背景线性化具有

\[
\lambda_\pm=-2ia\xi\pm\sqrt{\xi^4+4\xi^3/\eta}.
\]

在增长支上，高 x 波数的增长率可达到 O(ξ²)。局部网格聚集使有效物理波数约按 1/J 放大；冻结局部系数时，相应增长尺度可能按 1/J² 放大。P10 的主网格最小 J 已约 .506，因而“更多局部解析能力”也可能同时带来更强的小尺度增长。

这与观测到的加密后增长、减小时间步仍不修复、微扰敏感性相符，但不是非线性开链系统的完整稳定性证明。真实增长支上的 Euler 因子为 1+Δtλ，减步只更准确地逼近其增长，并不保证消除增长；不能把这些失败一律解释成普通 CFL 步长选大了。

## 6. 实现与指标核验

- 23 项实现核验通过：固定网格退化至旧方程；映射坐标一、二阶导数的四阶收敛；初始密度积分反演；两支 SD 守恒通量的任意光滑扰动检查；密度时间链式法则；FD/SD 相同初态和速度函数；ALE 传输项的四阶趋近。
- 208 条尝试的源码哈希全部核对；204 个完整或部分 NPZ 通过 SHA-256；已保存观测场和误差独立回读差为 0。另 4 条原细 x 失败轨道只保存错误信息，后续补测保存了失败前状态。
- 主表所有 32 条动网格轨道，每个 Euler 步的速度均非零。相对于初始节点，终点最大位移范围约 1.56e−4 至 3.18e−3；这不是只在初始时布点。
- 主表最小 J≥.50614，最小密度约为 1；没有交叉或密度失正。计算坐标求积的总质量相对漂移≤8.34e−10，等分布缺陷 max|JR/mean(JR)−1|≤2.26e−4。这是数值诊断，不是 Euler 精确保守证明。
- 主表 SD 的物理局部守恒残差≤9.64e−14；FD 的对应残差最大约 .032，符合使用共同驱动函数但不拥有同一精确守恒律的区别。
- 主表初始输出插值误差最大约 4.00e−10，逐例最多为终点误差的 1.47e−6；没有通过为 SD 换参照或不同物理初态人为制造优势。
- 误差在共同物理 x 上计算：先沿均匀 ξ 作 Fourier 加密，再对加密的物理曲线插值。主表评价点加倍使误差最多变化约 1.01%，没有改变动网格收益分类；重构分辨率加倍变化≤.00138%。直接在物理 x 使用独立七次样条重算，主表误差变化≤.0146%。
- 全部控制中评价点加倍的最大变化约 3.03%，重构加倍≤.00142%；增长配置的细小数值排序不作为稳健结论。

本轮没有比较等墙钟预算：相同节点数、时间步和算子阶下比较误差；动网格另需计算 R,Q,J，因此不能据此宣称等计算时间下同样改善。

## 7. 本轮可以采用的研究结论

可以写：“两支源于 DLW Miura 守恒结构的正密度可构造共同 x 持续动网格。在统一 Euler 与连续物理解参照下，选定的短时参数配置出现可复核的双场总误差改善。P6 的负支在所测空间/时间敏感性检查中保持改善；正支的更大主网格收益不具有相同的跨分辨率稳定性。细网格实验同时暴露了聚集与增长模态之间的限制。”

不能写：“自然密度普遍改善 DLW”“可积格式在动网格上总胜普通差分”“正密度保证长期稳定”“8 个参数构成统计显著的总体结论”。

若继续推进，应先围绕 P6 的 r− 做参数邻域确认，再讨论密度强度上限与增长控制。不能在未经验证的情况下将 β 增大来追求更小的局部间距。

## 8. 文件与复现

1. `python validate.py`：23 项实现检查，输出 `validation.json`。
2. `python run.py --phase main --workers 4`：48 条主轨道；依次以 `time_half`、`space_x`、`space_y` 重现敏感性检查。已有冻结轨道会跳过，源码变化会拒绝混写。
3. `python supplement.py --workers 4`：40 条针对观察到的增长与微小误差的补测。
4. `python summarize.py`：数据回读、哈希、指标核验，生成 `out/summary.json` 与 `out/errors.csv`。
5. `python plot.py`、`python make_report.py`：生成科学图、本报告与表格。

- [完整误差 CSV](out/errors.csv)
- [数据与指标核验](out/summary.json)
- [实现检查](validation.json)
- [密度推导来源](../dlw_mesh_densities_20260926/REPORT.md)
- [既有误差传播与增长支分析](../dlw_advantage_regions_20260926/REPORT.md)

原求解器、根目录生成 HTML 和 Lean 工程均未修改。

## 附表：较早时刻 T=.005 的主配置

@@EARLY@@
'''

replacements={'@@MAIN@@':table('main',CASES),'@@RATIOS@@':ratios(),'@@FINEX@@':table('space_x',CASES),
              '@@P6FINE@@':p6fine(),'@@FINEY@@':table('space_y',['P1','P2','P6','P10']),
              '@@SEED@@':'\n'.join(seedlines),'@@EARLY@@':table('main',CASES,.005)}
for a,b in replacements.items():text=text.replace(a,b)
(HERE/'REPORT.md').write_text(text,encoding='utf-8')
(OUT/'main_table.md').write_text(table('main',CASES)+'\n',encoding='utf-8')
print('Generated REPORT.md and out/main_table.md')
