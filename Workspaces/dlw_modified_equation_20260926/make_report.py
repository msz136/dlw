"""Build the error-analysis note, figure, and report section from saved results."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).parent
data=json.loads((ROOT/'results.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'Microsoft YaHei','font.size':10,'svg.fonttype':'path',
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.facecolor':'#fffdf9','figure.facecolor':'#fffdf9'})
fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
colors={'P1':'#8a5a2b','B':'#426c80','P6':'#777047','P10':'#ad5444'}
for name,rec in data['cases'].items():
    rows=rec['field_scans']
    for i in (0,1):
        axs[i].loglog([r['h'] for r in rows],[r['norm'][i] for r in rows],'-o',markersize=4,color=colors[name],label=name)
for i in (0,1):
    axs[i].set_title(('u','v')[i]+'：同谱参数精确解差')
    axs[i].set_xlabel('横向格距 h');axs[i].set_ylabel('采样最大绝对误差')
    axs[i].grid(True,which='major',alpha=.18);axs[i].legend(frameon=False,fontsize=8)
rows=data['cases']['P10']['field_scans']
for i,color in enumerate(('#8a5a2b','#426c80')):
    axs[2].loglog([r['h'] for r in rows],[r['norm'][i] for r in rows],'-o',color=color,label=('u','v')[i]+' 原差值')
    axs[2].loglog([r['h'] for r in rows],[r['minus_leading_norm'][i] for r in rows],'--s',color=color,markersize=3,label=('u','v')[i]+' 减去二阶首项')
axs[2].set_title('P10：二阶首项能解释多少？')
axs[2].set_xlabel('横向格距 h');axs[2].set_ylabel('采样最大绝对值')
axs[2].grid(True,which='major',alpha=.18);axs[2].legend(frameon=False,fontsize=8)
fig.savefig(ROOT/'model_error.png',dpi=180)
fig.savefig(ROOT/'model_error.svg')
plt.close(fig)

field_rows=[];residual_rows=[];md_field=[];md_res=[]
for name,rec in data['cases'].items():
    pars=rec['parameters'];r=rec['field_scans'][1]
    label=f"{name}：({pars['a']:g}, {pars['p']:g}, {pars['q']:g})"
    vals=[label,f"{r['norm'][0]:.4g}",f"{r['norm'][1]:.4g}",f"{100*r['relative_norm'][0]:.3g}% / {100*r['relative_norm'][1]:.3g}%"]
    field_rows.append('<tr>'+''.join('<td>'+s+'</td>' for s in vals)+'</tr>')
    md_field.append('| '+' | '.join(vals)+' |')
    norms=rec['residual_h2_norm']; ratios=[norms['SD'][i]/norms['FD'][i] for i in (0,1)]
    vals=[name,f"{norms['SD'][0]:.5g}",f"{norms['FD'][0]:.5g}",f"{ratios[0]:.3f}",f"{norms['SD'][1]:.5g}",f"{norms['FD'][1]:.5g}",f"{ratios[1]:.3f}"]
    residual_rows.append('<tr>'+''.join('<td>'+s+'</td>' for s in vals)+'</tr>')
    md_res.append('| '+' | '.join(vals)+' |')

note=r'''# DLW 半离散模型的二阶误差：修正项、直接差分对照与精确解差

2026-09-26。只考察横向 y 半离散；x、t 导数保持精确。本轮不推进 PDE，不改变已有求解器，不调参。

## 1. 比较的对象

连续方程为

\[
u_{yt}+v_{xx}+[(u+2a)u_y]_x=0,\qquad
v_t+u_{xxy}+[(u+2a)v-4u]_x=0.
\]

结构格式采用现有 NONLINEAR_CLOSURE.md 的 N1、N2 和原物理 u/v 定义。直接差分采用已有 dynamics.py 的交错 FD：第一式是对 u_t+(u²/2+2au)_x 作后向差分，加相邻 v 平均的二阶 x 导数；第二式用中心差分近似 u_y。该比较与任意其他 FD 模板无关。

第一式位于相邻 u 格点的中间，第二式位于 u/v 格点；Taylor 展开分别以各自位置为中心。若强行放在同一点而不平移，会人为引入一阶项。

## 2. 原模型多出的二阶项

将一个精确连续 DLW 解代入结构半离散方程，得到残差 h² R₁、h² R₂ 加 O(h⁴)，其中

\[
\boxed{R_1=\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac1{12}v_{xxyy}-\frac14u_{xxyyy},}
\]

\[
\boxed{R_2=\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac12\partial_x(u_yu_{yy})
+\frac14v_{xxyy}-\frac1{12}u_{xxyyy}.}
\]

这对一般光滑连续解成立，不依赖孤子假设。它们是方程残差系数，不是 u/v 的演化误差。

### 第一式的推导

在两格中间，后向差商等于 ∂y+h²∂y³/24+O(h⁴)，相邻平均等于 1+h²∂y²/8+O(h⁴)。中心差分等于 ∂y+h²∂y³/6+O(h⁴)。代入 N1 后，未使用连续方程时的二阶系数为

\[
\frac1{24}\partial_y^3[u_t+(u^2/2+2au)_x]
+\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac18v_{xxyy}-\frac14u_{xxyyy}.
\]

连续第一式给出 u_t+(u²/2+2au)_x 的 y 导数等于 −v_xx，因此第一项等于 −v_xxyy/24，合并成 R₁。

若 u/v 不是连续方程的解，设连续第一式左侧为 E₁，完整展开是 E₁+h²(E₁,yy/24+R₁)+O(h⁴)。在光滑修正方程意义下，可减去原残差的 h²/24 倍二阶 y 导数，得到等价到 O(h⁴) 的 E₁+h²R₁=0；不能把这个形式处理误称为有限 h 精确换元。

### 第二式的推导

N2 的通量中心差分产生

\[
\frac16\{(u^2/2+2au)_{yyy}-(u+2a)u_{yyy}\}
=\frac12u_yu_{yy}.
\]

线性高阶项则为 v_xxyy/4+(1/6−1/4)u_xxyyy。与平方修正合并，得到 R₂。对一般光滑 u/v，第二式直接展开为 E₂+h²R₂+O(h⁴)。

## 3. 与已有直接差分比较

相同位置上的 FD 首项是

\[
R_1^{FD}=\frac1{12}v_{xxyy},\qquad
R_2^{FD}=\frac16u_{xxyyy}.
\]

所以结构格式额外多出的首项分别为

\[
R_1-R_1^{FD}=\frac1{32}\partial_{xy}(v-u_y-4)^2-\frac14u_{xxyyy},
\]

\[
R_2-R_2^{FD}=\frac1{32}\partial_{xy}(v-u_y-4)^2
+\frac12\partial_x(u_yu_{yy})+\frac14v_{xxyy}-\frac14u_{xxyyy}.
\]

它们有符号，可能增强也可能抵消已有误差。保留孤子结构没有强制这些系数更小。

下表用已有四组 N=1 参数，解析求导，在完整波形的相位区间 [−16,16] 取 8193 点。数值是 R 的采样最大绝对值；实际残差首项还须乘 h²。只在同一条方程内比较，不能把不同方程的两个数相加作为场误差。

| 参数 | SD 第一式 | FD 第一式 | 比值 | SD 第二式 | FD 第二式 | 比值 |
|---|---:|---:|---:|---:|---:|---:|
@@RESIDUAL_TABLE@@

这四例的第一式结构残差较大，第二式有大有小。该现象提供了可积格式未必更准确的具体原因，但并不直接给出时间演化后的 u/v 排名。

## 4. 同谱参数精确解的模型差

比较有限 h 的精确 Gram 物理场与同谱参数的连续精确场，均在 y=(j+1/2)h 取值。取 x∈[−10,10] 的 4001 点、y∈[−1.5,1.5] 的实际中点格点、t=0。ρ 分别为 P1=3、B=5、P6=4、P10=3.5。

| 参数 (a,p,q) | h=1/8 的 u 误差 | h=1/8 的 v 误差 | 相对连续场峰值 u / v |
|---|---:|---:|---:|
@@FIELD_TABLE@@

该表比较两个同谱参数精确解族，并非同一连续初值出发的两条演化；t=0 就已有此差异，不能称为所有半离散解不可避免的误差下限。FD 不具有此处同一个有限 h Gram 真值，所以不能捏造对应的 FD 精确解差表。

从 h=1/4 到 1/64 共五档，原差值最后一档观测阶在 1.9958–1.9997；减去本节下面推导的二阶误差首项后，余量最后一档阶数约 3.986–3.999。在 h=1/8，二阶首项对整个误差场的相对最大范数预测偏差，P1/B/P6 不超过 0.070%，P10 不超过 1.585%。这说明本轮推导解释了这些精确解族的主要差异。

![模型差及减去二阶首项后的余量](model_error.png)

### 为什么不能只用上一轮的变量提取误差？

令 α=log f、β=log g，交错位置上的平滑 tau 插值写成 α_h=α+h²α₂+O(h⁴)、β_h=β+h²β₂+O(h⁴)。则完整场误差首项为

\[
u_h=u+h^2\left[2(\alpha_2-\beta_2)_x+\frac{u_{yy}-v_y}{16}\right]+O(h^4),
\]

\[
v_h=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac{9u_{yyy}-v_{yy}}{48}\right]+O(h^4).
\]

后面的导数项是变量提取误差；前面的 α₂、β₂ 记录 tau 本身的改变。上一轮只对精确采样同一连续 tau 给出的公式，不能遗漏这一部分后拿来预测实际 Gram 模型差。

### 单孤子的 tau 改变可以显式写出

记 k=p+q、P=p−a、Q=q+a、ℓ=1/P+1/Q、γ=−P/Q，

\[
z=kx+(q^2-p^2)t+\log\frac\rho k+\ell y,\qquad
\sigma(z)=\frac1{1+e^{-z}}.
\]

定义两个明确的谱系数

\[
C=\frac1{12}(P^{-3}+Q^{-3}),\qquad
D=\frac18(Q^{-2}-P^{-2}).
\]

格点相位给出 log χ/h=ℓ+h²C+O(h⁴)，F 中点系数给出 log[γ(s_−)χ^{-1/2}]=log γ+h²D+O(h⁴)。因此

\[
\alpha_2=(yC+D)\sigma(z+\log\gamma),\qquad
\beta_2=yC\sigma(z).
\]

将它们代入完整场误差公式即可得到上面的预测，无需拟合 h 扫描数据。C 对应横向相位及其导数的改变，D 对应 F 的系数改变，剩下是变量提取误差。三者的有符号场先相加再取范数；分量范数不能当成可相加的误差百分比。

P10 的 |p−a|=0.5，而 P1 是 3。C 含三次倒数，D 含二次倒数，因而靠近谱极点时误差系数明显增大。同为 h=1/8，P10 的 u/v 差分别约为 P1 的 123/446 倍。二阶描述 h 的幂次，没有限制其前面的系数。渐近展开要求 h 相对谱极点距离足够小；正则性不等于误差常数温和。

## 5. 从方程残差到演化误差还差哪一步

若在所选初边值与光滑区域内，解可以展开为 u_h=u+h²e_u+O(h⁴)、v_h=v+h²e_v+O(h⁴)，则领先系数满足

\[
(e_u)_{yt}+(e_v)_{xx}+\partial_x[(u+2a)(e_u)_y+u_y e_u]=-R_1,
\]

\[
(e_v)_t+(e_u)_{xxy}+\partial_x[(u+2a)e_v+(v-4)e_u]=-R_2.
\]

这说明残差如何注入误差，背景线性化如何传播误差。若两个模型从同一连续物理初值开始，应使用 e_u=e_v=0 的相应初值与匹配边界；上面同谱 Gram 家族则使用其非零的首项初值。两者是不同的误差问题。

已有的固定右幽灵重构可把部分 v 误差放大到 O(1/h)，高频传播也可能增长；本轮纯模型分析未包含这些实现因素。当前结果不能单独解释所有旧求解器曲线。

## 6. 对下一步优化的含义

1. 先使用完整 R₁/R₂ 或完整物理场首项决定目标；仅优化相位不足以处理 F 系数与变量提取误差。例如 P1/P6 的 u 首项中，F 系数分量明显大于相位分量。
2. 对 s±=a+ch²±(h+κh³)/2，领先残差变为 R₁+2c u_xy、R₂+2c v_x−4κu_x。两个参数只提供这些特定修正方向，不能任意取消全部高阶导数项。
3. 如果要调参，应固定目标波形范围及要改善的物理量，再评价总的有符号误差；若直接把 R₁/R₂ 从非线性方程中减掉，则是在另造格式，原可积结构需重新证明。

本轮完成误差来源与量级分析，没有据此宣称某组最优参数，也没有改变原可积系统。

## 计算记录与来源

- derive.py：24 项任意光滑函数 Taylor/线性化恒等式，结果 symbolic.json。
- measure.py：解析导数残差、精确场差、五档 h、二阶首项预测；结果 results.json。
- 65 位独立微分验证四组单孤子误差首项满足受迫线性化方程，最大残差低于 2×10⁻⁶⁵。
- 表格采样加密后，场误差最大值相对变化不超过 0.00195%，残差系数最大值不超过 0.00065%。这些为采样精度诊断，不是区间认证的上界。
- 上游：../dlw_semidiscrete/NONLINEAR_CLOSURE.md、numerics/lib/dynamics.py、numerics/ERROR_BUDGET_REPORT.md、numerics/PARAMETRIC_THEORY.md。
'''
note=note.replace('@@FIELD_TABLE@@','\n'.join(md_field)).replace('@@RESIDUAL_TABLE@@','\n'.join(md_res))
(ROOT/'REPORT.md').write_text(note,encoding='utf-8')

html=r'''<!-- DLW-MODIFIED-ERROR-START -->
<section class="part" id="model-error">
<div class="part-label">第五部分 · 半离散模型的误差</div>
<h2>同为二阶，为什么误差可以相差很大？</h2>
<p class="lede">这一部分只让 $y$ 离散，$x,t$ 的导数保持精确。先把连续解代入两种格点方程，找出它们的二阶残差；再比较同谱参数的半离散与连续精确孤子。这样能把模型差本身与时间推进、$x$ 差分、边界重构造成的误差分开。</p>

<h3>1. 第一件事：把二阶修正项写全</h3>
<p>采用前面的原物理场 $u,v$。第一条离散方程在两个 $u$ 格点的中间展开，第二条在 $u,v$ 格点展开。将一个光滑连续 DLW 解代入原结构格式，两式左侧分别为 $h^2R_1+O(h^4)$ 与 $h^2R_2+O(h^4)$，其中</p>
<div class="mathblock">$$\boxed{
R_1=\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac1{12}v_{xxyy}-\frac14u_{xxyyy}.
}\tag{58}$$</div>
<div class="mathblock">$$\boxed{\begin{aligned}
R_2={}&\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac12\partial_x(u_yu_{yy})\\
&+\frac14v_{xxyy}-\frac1{12}u_{xxyyy}.
\end{aligned}}\tag{59}$$</div>
<p>$R_1,R_2$ 只是两条方程的误差系数，具体表达式已全部写出。它们对一般光滑连续解成立，并不依赖孤子假设。<strong>二阶说明误差含 $h^2$，误差多大还由这些导数和非线性项决定。</strong></p>
<p>第一项来自两壁平方项的有限格距修正；其余项来自差商、平均及乘积在展开时的差异。横向变化越快，高阶 $y$ 导数可能越大，所以相同的 $h$ 并不对应相同的误差大小。</p>
<details><summary>式 (58)–(59) 怎样从原方程得到？</summary>
<p>在两个格点中间，差商展开为 $\partial_y+h^2\partial_y^3/24+O(h^4)$，平均展开为 $1+h^2\partial_y^2/8+O(h^4)$；中心差分则为 $\partial_y+h^2\partial_y^3/6+O(h^4)$。第一式的二阶系数在使用连续方程之前是</p>
<div class="mathblock">$$\begin{aligned}
&\frac1{24}\partial_y^3\left[u_t+(u^2/2+2au)_x\right]\\
&+\frac1{32}\partial_x\partial_y(v-u_y-4)^2
+\frac18v_{xxyy}-\frac14u_{xxyyy}.
\end{aligned}$$</div>
<p>连续第一式把第一项化成 $-v_{xxyy}/24$，于是得到式 (58)。如果场不满足连续方程，完整展开还含连续第一式残差的 $h^2/24$ 倍二阶 $y$ 导数；在光滑修正方程意义下可以消去这一项，到 $O(h^4)$ 等价，但这不是有限 $h$ 的精确换元。</p>
<p>第二式中，通量展开用到</p>
<div class="mathblock">$$
\frac16\left[(u^2/2+2au)_{yyy}-(u+2a)u_{yyy}\right]
=\frac12u_yu_{yy}.
$$</div>
<p>线性修正则为 $v_{xxyy}/4+(1/6-1/4)u_{xxyyy}$。两者与平方项相加，就是式 (59)。因此每一个二阶项都有确定的来源。</p>
</details>

<h3>2. 与隔壁数值分析采用的直接差分比较</h3>
<p>这里采用已有数值程序中的二阶交错直接差分：第一式对 $u_t+(u^2/2+2au)_x$ 作差商，并平均相邻的 $v$；第二式用中心差分近似 $u_y$。其二阶残差系数只有</p>
<div class="mathblock">$$
R_1^{\mathrm{FD}}=\frac1{12}v_{xxyy},\qquad
R_2^{\mathrm{FD}}=\frac16u_{xxyyy}.\tag{60}
$$</div>
<p>结构格式为了保持精确格点关系，还含式 (58)–(59) 中的其他修正。它们可能增加误差，也可能相互抵消；可积结构没有要求它们的总幅度更小。</p>
<p>在已有四组单孤子参数上，用解析导数直接计算，得到下表。每个数是对应二阶系数的采样最大绝对值，实际残差首项还要乘 $h^2$。“比值”是结构格式除以直接差分；只在同一条方程内比较。</p>
<div class="table-wrap"><table><thead><tr><th>参数</th><th>结构第一式</th><th>差分第一式</th><th>比值</th><th>结构第二式</th><th>差分第二式</th><th>比值</th></tr></thead><tbody>@@RESIDUAL_TABLE@@</tbody></table></div>
<p>这四例中，结构格式第一式的二阶残差系数约大 2.9–5.2 倍；第二式在 B、P10 上反而更小。<strong>因此已有数据支持“可积格式不自动更准确”，也表明两场耦合后的效果不能用单一排序概括。</strong>残差还要经过误差传播，不能把这两个比值直接当作最终 $u,v$ 误差的比值。</p>
<p class="aside">残差在单孤子的相位区间 $[-16,16]$ 上采样，$x,t$ 导数均解析求值，没有时间推进或 $x$ 差分。这里比较的是已有交错 FD 模板，不代表所有有限差分方法。</p>

<h3>3. 模型差究竟有多大？用两个精确解直接相减</h3>
<p>固定同一组谱参数，比较有限 $h$ 的精确 Gram 场与连续精确场，均在 $y=(j+1/2)h$ 取值。取 $t=0$、$x\in[-10,10]$、$y\in[-1.5,1.5]$。下表没有求解器误差：</p>
<div class="table-wrap"><table><thead><tr><th>参数 $(a,p,q)$</th><th>$h=1/8$ 的 $u$ 差</th><th>$h=1/8$ 的 $v$ 差</th><th>相对连续峰值 $u/v$</th></tr></thead><tbody>@@FIELD_TABLE@@</tbody></table></div>
<p>这比较的是<strong>两个同谱参数精确解族</strong>，初始时刻就有表中的差异。如果两种演化从完全相同的连续物理初值出发，初始误差应为零，那是下一节的受迫误差问题。表中数值不是任何离散解都无法突破的误差下限，也不是 FD 的时间演化误差。</p>
<p>将 $h$ 从 $1/4$ 连续减半到 $1/64$，四组的最后一档观测阶为 1.9958–1.9997，确实趋于二阶。用下面推导的二阶首项从误差场中减去后，余量约为四阶。这一步表明我们已经抓住主要误差，而不仅是从曲线估计幂次。</p>
<figure style="margin:24px 0"><div role="img" aria-label="四组参数的 u、v 精确模型差随 h 呈二阶变化，P10 减去二阶首项后的余量呈近四阶变化" style="width:100%">@@FIGURE@@</div><figcaption class="aside">前两图显示模型差的参数依赖。右图只从已知误差中减去解析首项，用来说明误差展开的作用，没有修改方程或运行一个新的四阶求解器。</figcaption></figure>

<h3>4. 二阶首项包括三部分，不能只看变量定义</h3>
<p>前面式 (55) 讨论的是同一连续 tau 的采样。真正的半离散 Gram tau 自身也随 $h$ 改变。若交错位置上的平滑插值写成 $\alpha_h=\alpha+h^2\alpha_2+O(h^4)$、$\beta_h=\beta+h^2\beta_2+O(h^4)$，则完整场误差为</p>
<div class="mathblock">$$\begin{aligned}
u_h-u={}&h^2\left[2(\alpha_2-\beta_2)_x
+\frac{u_{yy}-v_y}{16}\right]+O(h^4),\\
v_h-v={}&h^2\left[2(\alpha_2+\beta_2)_{xy}
+\frac{9u_{yyy}-v_{yy}}{48}\right]+O(h^4).
\end{aligned}\tag{61}$$</div>
<p>后面的导数项来自变量提取；前面的 $\alpha_2,\beta_2$ 记录 tau 的改变。单孤子中，这又分为<strong>横向相位改变</strong>与<strong>$F$ 的系数改变</strong>，都可以直接从谱参数算出。</p>
<details><summary>单孤子完整误差首项的显式公式</summary>
<p>令 $k=p+q$、$P=p-a$、$Q=q+a$、$\ell=1/P+1/Q$、$\gamma=-P/Q$，并记</p>
<div class="mathblock">$$
z=kx+(q^2-p^2)t+\log(\rho/k)+\ell y,\qquad
\sigma(z)=\frac1{1+e^{-z}}.
$$</div>
<p>由格点乘子与中点系数展开得到</p>
<div class="mathblock">$$
C=\frac1{12}(P^{-3}+Q^{-3}),\qquad
D=\frac18(Q^{-2}-P^{-2}),
$$</div>
<div class="mathblock">$$
\alpha_2=(yC+D)\sigma(z+\log\gamma),\qquad
\beta_2=yC\sigma(z).\tag{62}
$$</div>
<p>其中 $\log\chi/h=\ell+h^2C+O(h^4)$，而 $\log[\gamma(s_-)\chi^{-1/2}]=\log\gamma+h^2D+O(h^4)$。代回式 (61)，即得到完整物理误差首项，无需拟合格距扫描数据。</p>
</details>
<p>在 $h=1/8$，这个首项对整个误差场的相对最大范数预测偏差，P1/B/P6 均低于 0.070%，P10 低于 1.585%。三部分必须先带符号相加再比较；分别取绝对值再相加，会丢掉它们之间的抵消。</p>
<p>P10 的 $|p-a|=0.5$，P1 则为 3。相位系数含三次倒数，$F$ 系数含二次倒数，靠近谱极点时会明显增大。因此同为 $h=1/8$，P10 的 $u,v$ 差约为 P1 的 123 倍和 446 倍。<strong>“二阶”没有保证误差系数小；$h$ 相对谱极点距离的大小也必须考虑。</strong></p>

<h3>5. 从残差到同初值演化误差，还需要怎样联系？</h3>
<p>若在所选光滑区域与初边值下，能够写出 $u_h=u+h^2e_u+O(h^4)$、$v_h=v+h^2e_v+O(h^4)$，则领先误差系数满足</p>
<div class="mathblock">$$\begin{aligned}
(e_u)_{yt}+(e_v)_{xx}
+\partial_x[(u+2a)(e_u)_y+u_y e_u]&=-R_1,\\
(e_v)_t+(e_u)_{xxy}
+\partial_x[(u+2a)e_v+(v-4)e_u]&=-R_2.
\end{aligned}\tag{63}$$</div>
<p>右侧是模型持续注入的误差，左侧描述背景解怎样传播它。同连续初值比较时，要取相应的零初始误差与匹配边界；同谱 Gram 比较则有式 (61) 给出的非零初始误差。即使残差小，传播或边界重构也可能放大它。</p>
<p>已有数值记录中，固定右幽灵闭合会使某些 $v$ 重构误差出现 $O(1/h)$ 的放大，高频响应也会增长。因此这里的纯模型结果解释了一个明确来源，尚不能代替完整的求解器误差分解。</p>

<h3>6. 这些结果怎样指导后续优化？</h3>
<p>首先，不应只追求横向相位更准。在 P1/P6 的 $u$ 首项中，$F$ 系数改变的分量明显大于相位分量；只消掉相位误差未必能改善主要问题。</p>
<p>其次，对前面的参数族 $s_\pm=a+ch^2\pm(h+\kappa h^3)/2$，二阶残差只能沿下面两个方向改变：</p>
<div class="mathblock">$$
R_1\longmapsto R_1+2c\,u_{xy},\qquad
R_2\longmapsto R_2+2c\,v_x-4\kappa u_x.\tag{64}
$$</div>
<p>这给出了下一步调参能做到什么的明确范围。应先确定要改善哪一类波形、哪个物理量，再比较完整的有符号误差。两个常数不能任意抵消式 (58)–(59) 中的全部高阶项。</p>
<div class="key"><p><strong>这一小步的结果：</strong>我们已经得到一般连续解上的二阶残差、与已有 FD 的逐项差异，以及四组精确孤子的完整二阶物理误差首项。原方案是二阶，但系数可以很大，且部分结构修正确实会增大局部残差。</p><p>下一步可以据这些首项研究有目标的参数匹配。若直接在非线性方程里减掉 $h^2R_1,h^2R_2$，则是在构造另一个格式，原可积结构需要重新证明。</p></div>
<p class="source"><a href="Workspaces/dlw_modified_equation_20260926/REPORT.md">完整误差推导</a> · <a href="Workspaces/dlw_modified_equation_20260926/results.json">本轮量化结果</a> · <a href="Workspaces/dlw_semidiscrete/numerics/ERROR_BUDGET_REPORT.md">已有演化误差分解</a></p>
</section>
<!-- DLW-MODIFIED-ERROR-END -->
'''
svg=(ROOT/'model_error.svg').read_text(encoding='utf-8')
svg=svg[svg.index('<svg'):]
svg=svg.replace('<svg ', '<svg style="width:100%;height:auto;display:block" ',1)
html=html.replace('@@FIELD_TABLE@@',''.join(field_rows)).replace('@@RESIDUAL_TABLE@@',''.join(residual_rows)).replace('@@FIGURE@@',svg)
source=ROOT.parent/'gsg_project/dlw_report/_src/miura_dlw.src.html'
text=source.read_text(encoding='utf-8')
begin='<!-- DLW-MODIFIED-ERROR-START -->';end='<!-- DLW-MODIFIED-ERROR-END -->'
if begin in text:
    start=text.index(begin);stop=text.index(end,start)+len(end)
    text=text[:start]+html+text[stop:]
else:
    text=text.replace('<footer id="sources">',html+'\n<footer id="sources">',1)
    text=text.replace('</ol></nav>','<li><a href="#model-error">五 · 二阶误差来自哪里</a><small>修正项 → 直接差分对照 → 精确解误差</small></li>\n</ol></nav>',1)
source.write_text(text,encoding='utf-8')
print('Generated REPORT.md, scientific figure, and HTML source section.')
