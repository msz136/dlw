"""Present the constant-parameter spatial residual optimization."""
from pathlib import Path
import json
ROOT=Path(__file__).parent
d=json.loads((ROOT/'optimization.json').read_text(encoding='utf-8'))
c,kappa=d['shared_optimum']

def tables(rows):
    md='\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
    html=''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)
    return md,html

shared_rows=[];floor_rows=[];individual_rows=[];transfer_rows=[]
for name,rec in d['calibration'].items():
    m=d['shared_metrics'][name]
    shared_rows.append([name,f"{m['relative_L2'][0]:.6f}",f"{m['relative_L2'][1]:.6f}",
                        f"{m['relative_Linf_sampled'][0]:.6f}",f"{m['relative_Linf_sampled'][1]:.6f}"])
    floor_rows.append([name,f"{rec['floors']['first_c_minimizer']:.8f}",
                       f"{rec['floors']['individual_equation_L2_floors'][0]:.6f}",
                       f"{100*(1-rec['floors']['individual_equation_L2_floors'][0]):.4f}%"])
    m=rec['individual_metrics'];theta=rec['individual_optimum']
    individual_rows.append([name,f'{theta[0]:.8f}',f'{theta[1]:.8f}',f"{m['relative_L2'][0]:.6f}",f"{m['relative_L2'][1]:.6f}"])
for name,rec in d['transfer_without_refit'].items():
    p=rec['parameters']
    transfer_rows.append([name,f"({p['a']:g}, {p['p']:g}, {p['q']:g})",f"{rec['relative_L2'][0]:.6f}",f"{rec['relative_L2'][1]:.6f}"])
sm,sh=tables(shared_rows);fm,fh=tables(floor_rows);im,ih=tables(individual_rows);tm,th=tables(transfer_rows)

note=r'''# 保留双线性结构的常数参数优化：只研究空间残差

2026-09-26。承接 REPORT.md。本轮使用解析连续孤子剖面和空间函数积分，没有运行 PDE 时间演化，没有引入 x 数值差分，也没有改动生产求解器。

## 1. 保持的结构与调整范围

固定物理 a,h 与原 u/v 定义，取

\[
s_\pm=a+ch^2\pm\frac{h+\kappa h^3}{2},\qquad
\chi(p,q)=\frac{(p-s_-)(q+s_+)}{(p-s_+)(q+s_-)}.
\]

c、κ 是在 x,y,t 和所有孤子谱分量之间共用的常数；选好后随格距加密保持同一数值。这保持原有的任意 N Gram 双线性恒等式与常参数 Darboux 结构。若让 c、κ 随格点、时间或不同孤子分别改变，就超出当前同一个双线性对的证明。一般初值 IST 仍未建立。

此前已得到，连续解代回新格点方程的二阶残差为

\[
R_1(c,\kappa)=R_1+2c u_{xy},\qquad
R_2(c,\kappa)=R_2+2c v_x-4\kappa u_x.
\]

R₁、R₂ 保持上一份报告的物理 N1/N2 方程组合；更换残差表示或权重会改变最优系数。优化减少的是二阶系数，阶数仍为二阶。

## 2. 先指定一个清楚的空间误差指标

令内积为完整单孤子剖面上的 x 积分。采用两条方程各自相对原残差的 L² 比例：

\[
J(c,\kappa)=\frac{\|R_1+2cu_{xy}\|_2^2}{\|R_1\|_2^2}
+\frac{\|R_2+2cv_x-4\kappa u_x\|_2^2}{\|R_2\|_2^2}.
\]

本例两条原残差都非零。分别归一化避免把不同方程的量纲、大小直接相加，并给两条方程同等的相对改善权重。原方案 J(0,0)=2。它是一个具体选择，不是独立于物理目标的唯一指标，也不等于 L∞ 误差或最终场误差。

单孤子在 y,t 上只有剖面平移，完整 x 积分的这些比值不随平移变化。因此这里的最优常数不需要逐时、逐格更新；ρ 也只改变位置。实际积分改用中心相位，dx 的常数因子在每个比值中抵消。

## 3. 最优系数由 2×2 线性方程决定

直接对 J 求偏导，得到

\[
\begin{aligned}
&c\left(\frac{4\|u_{xy}\|_2^2}{\|R_1\|_2^2}
+\frac{4\|v_x\|_2^2}{\|R_2\|_2^2}\right)
-\kappa\frac{8\langle v_x,u_x\rangle}{\|R_2\|_2^2}
=-\frac{2\langle u_{xy},R_1\rangle}{\|R_1\|_2^2}
-\frac{2\langle v_x,R_2\rangle}{\|R_2\|_2^2},\\
&-c\frac{8\langle v_x,u_x\rangle}{\|R_2\|_2^2}
+\kappa\frac{16\|u_x\|_2^2}{\|R_2\|_2^2}
=\frac{4\langle u_x,R_2\rangle}{\|R_2\|_2^2}.
\end{aligned}
\]

系数矩阵是两个可调函数方向的 Gram 矩阵。若 u_xy 和 u_x 都不是零函数，其二次型为两个平方范数之和，只在 c=κ=0 时为零，所以严格正定，存在唯一的无约束最小值。实际使用还需满足所选有限 h 的谱分母与正则性要求。

也可以先固定 c，直接消去 κ：

\[
\kappa(c)=\frac{\langle u_x,R_2+2cv_x\rangle}{4\|u_x\|_2^2}.
\]

剩下只是一元严格凸二次式。因此不需要黑箱搜索，也不需要时间模拟。多剖面共用参数时，把各剖面的 J 相加即可，仍是同样大小的线性方程组。

## 4. 每个剖面单独调，与一套方程共用参数

先分别最小化四组已有参数的 J，得到：

| 参数 | c | κ | 第一式 L² 比 | 第二式 L² 比 |
|---|---:|---:|---:|---:|
@@INDIVIDUAL@@

其中 P10 的联合最优解使第一式增加约 1.27%，同时降低第二式；联合指标最小不保证每一项都更小。不同剖面单独得到的最优系数，也不能在同一个多孤子方程里逐孤子混用。

为给出一组实际共用的候选，令 P1/B/P6/P10 的四个 J 等权相加，得到

\[
\boxed{c=@@C@@,\qquad\kappa=@@K@@.}
\]

这里 P1=(4,1,2)、B=(4,2,3)、P6=(4,1,3)、P10=(2,1.5,2)，顺序为 (a,p,q)。这组数值是指定四剖面、指定残差和权重下的候选，不是全体 DLW 解的普遍最优系数。

| 参数 | 第一式 L² 比 | 第二式 L² 比 | 第一式最大值比 | 第二式最大值比 |
|---|---:|---:|---:|---:|
@@SHARED@@

所有比值均为优化后除以优化前。四组八项归一化残差的总体 RMS 比为 0.887312，下降约 11.27%。P1/P6 的第一式改善约 62.14%/39.74%；第二式只改善约 0.43%–2.42%。P10 的第一式 L² 仅改善约 0.058%，最大值反而增加约 0.978%。不能把 L² 优化称为一致的逐点改善或最大误差界优化。

该候选在 0<h≤1/4 的所列八组谱参数上满足正则性充分条件：κ>0，c−κ/8>0，且最小 a−p 为 0.5，从而 s_−−p≥0.5−1/8=0.375，q+s_−也为正，参数间距保持正值。此处仍保留原有任意 N 结构机制；单孤子上的误差优化不代表已经优化多孤子碰撞残差。

## 5. 有些残差从根本上调不掉

第一式不含 κ，只能通过 c 调整沿 u_xy 的一个函数方向。即使完全不顾第二式，它能达到的最低相对 L² 残差也是

\[
\boxed{\min_c\frac{\|R_1+2cu_{xy}\|_2}{\|R_1\|_2}
=\sqrt{1-\frac{\langle R_1,u_{xy}\rangle^2}
{\|R_1\|_2^2\|u_{xy}\|_2^2}}.}
\]

对应 c=−⟨u_xy,R₁⟩/(2‖u_xy‖²)。这是精确的函数投影公式；下表是对其积分的数值求值。

| 参数 | 只优化第一式的 c | 最低残差比 | 最多可降低 |
|---|---:|---:|---:|
@@FLOOR@@

P10 即使单独优化第一式，仍至少保留约 99.9264% 的 L² 残差。因此当前双参数族对这个困难剖面的改善空间很小，继续扩大搜索范围也不会突破这个下限。这里讨论的是固定物理变量下的二阶残差，不是最终解误差的下界。

另一个直观限制来自对称性：中心化单孤子的 u,v 为偶函数，u_xy 为偶函数、u_x 和 v_x 为奇函数。因此 c 无法改变 R₁ 的奇部；c、κ 都无法改变 R₂ 的偶部。可调系数只能抵消与这些方向相匹配的误差形状。

## 6. 不重新调参时，能否迁移到其他波形？

固定上面的共用 c、κ，计算四组不同谱参数的解析空间残差，不用它们重新拟合：

| 参数 | (a,p,q) | 第一式 L² 比 | 第二式 L² 比 |
|---|---|---:|---:|
@@TRANSFER@@

H1/H4 第二式分别增加约 5.62%/21.66%，虽然第一式改善。说明当前系数不能保证换波形后两条残差同时减小，也不能据四组原样本声称参数区域内普遍改善。

若下一步要求一个指定波形集合内两式都不变差，可在同一个凸二次优化中加入逐剖面的约束：

\[
\|R_1+2cu_{xy}\|_2\le\|R_1\|_2,\qquad
\|R_2+2cv_x-4\kappa u_x\|_2\le\|R_2\|_2.
\]

原参数 (0,0) 始终满足这些条件，因此不会被迫接受更差的系数；但最优解也可能只能给出很小的改善。若目标是最大残差，则应另定 L∞ 指标，不能沿用本轮 L² 最优的称号。本轮未执行这两种额外优化。

## 7. 二阶分析与有限格距的关系

对冻结的共用系数，直接将同一连续剖面代入完整有限 h 空间方程，计算 h=1/4、1/8、1/16、1/32 的残差；x,t 导数仍为解析值，没有积分时间演化。在 h=1/8，四组两式的优化前后 L² 比，与二阶系数预测的差均小于 0.00014。这只确认所选参数及格距下的残差改善，不是数值解误差或长期稳定性结论。

## 8. 本轮得到的结论

常数 c、κ 可以在既有 Gram/Darboux 参数族内，有目标地降低空间二阶残差；系数由一个可解释的二次优化确定。收益依赖剖面与指标，当前共用候选对温和参数的第一式最有效，对困难剖面第一式几乎无能为力。方法仍是二阶，原生产格式未被替换。

计算入口 optimize_residuals.py，数据 optimization.json。有限区间复合积分与独立全实轴自适应积分得到的共用系数差低于 6×10⁻¹⁶；扩大相位区间并加密后，L² 比差低于 2×10⁻¹⁵，采样最大值比差低于 1.3×10⁻⁶。最大值仍为数值采样量，不宣称区间认证。
'''
note=note.replace('@@C@@',f'{c:.11f}').replace('@@K@@',f'{kappa:.11f}').replace('@@SHARED@@',sm).replace('@@FLOOR@@',fm).replace('@@INDIVIDUAL@@',im).replace('@@TRANSFER@@',tm)
(ROOT/'PARAMETER_OPTIMIZATION.md').write_text(note,encoding='utf-8')

html=r'''<!-- DLW-PARAMETER-OPTIMIZATION-START -->
<section class="part" id="parameter-optimization">
<div class="part-label">第六部分 · 保留结构，调整空间误差系数</div>
<h2>两个常数能改善多少，又有哪些误差调不掉？</h2>
<p class="lede">本节保持物理格距 $h$ 与原来的 $u,v$ 定义，只调整双线性参数的中心和间距。所有计算都针对解析空间残差，不运行时间演化，也不对 $x$ 作数值差分。目标是先弄清：这两个常数有没有用，能做到哪一步。</p>

<h3>1. 仍在同一个 Gram/Darboux 结构族中</h3>
<div class="mathblock">$$
s_\pm=a+ch^2\pm\frac{h+\kappa h^3}{2},\qquad
\chi(p,q)=\frac{(p-s_-)(q+s_+)}{(p-s_+)(q+s_-)}.\tag{65}
$$</div>
<p>参数和格点乘子配套改变后，原来的任意 $N$ Gram 恒等式与常参数 Darboux 关系继续成立。这里 $c,\kappa$ 在所有格点、时刻与孤子分量之间共用，选好后在格距加密时也保持不变。给每个孤子分别选一套系数，或者随位置、时间重新调整，都超出了当前同一个双线性对的证明。</p>
<p>对连续解，二阶残差的变化已经由式 (64) 确定：</p>
<div class="mathblock">$$
R_1(c,\kappa)=R_1+2cu_{xy},\qquad
R_2(c,\kappa)=R_2+2cv_x-4\kappa u_x.
$$</div>
<p>因此我们只能沿这些明确的函数方向调节误差，不能任意修改式 (58)–(59)。本节优化的是二阶系数，精度阶数仍为二阶。</p>

<h3>2. 先把“更小”定义清楚</h3>
<p>采用完整单孤子剖面上的 $L^2$ 范数，比较两条残差各自相对原值的大小：</p>
<div class="mathblock">$$\begin{aligned}
J(c,\kappa)={}&\frac{\|R_1+2cu_{xy}\|_2^2}{\|R_1\|_2^2}\\
&+\frac{\|R_2+2cv_x-4\kappa u_x\|_2^2}{\|R_2\|_2^2}.
\end{aligned}\tag{66}$$</div>
<p>两条原残差在本例中都非零。分别除以原范数，使两式具有同等的相对改善权重，也避免把不同量纲的数直接相加。原方案的 $J$ 为 2。这个指标衡量整体空间残差，不是最大残差，也不是最终物理场误差。</p>
<p>单孤子在 $y,t$ 上只是剖面平移，完整 $x$ 积分不受平移影响。因此这里求出的常数不需要随时刻或位置更新。多个目标剖面共用系数时，把各自的 $J$ 相加即可。</p>

<h3>3. 不用试凑：最优系数来自一个线性方程组</h3>
<p>式 (66) 是关于 $c,\kappa$ 的二次函数。令两项偏导为零，就得到一个 $2\times2$ 线性方程组。对于这里的非平凡剖面，二次型严格正定，所以指定指标下的无约束最小值唯一。</p>
<p>也可以先固定 $c$，把最佳 $\kappa$ 显式解出来：</p>
<div class="mathblock">$$
\kappa(c)=\frac{\langle u_x,R_2+2cv_x\rangle}{4\|u_x\|_2^2}.\tag{67}
$$</div>
<p>这里内积就是两个函数乘积在空间上的积分。把式 (67) 代回后，只剩一个关于 $c$ 的一元二次函数。因此整个过程是计算空间函数的积分、解线性方程，不需要时间模拟或黑箱参数搜索。</p>
<details><summary>完整的两个线性方程</summary>
<div class="mathblock">$$\begin{aligned}
&c\left(\frac{4\|u_{xy}\|_2^2}{\|R_1\|_2^2}
+\frac{4\|v_x\|_2^2}{\|R_2\|_2^2}\right)
-\kappa\frac{8\langle v_x,u_x\rangle}{\|R_2\|_2^2}\\
&\qquad=-\frac{2\langle u_{xy},R_1\rangle}{\|R_1\|_2^2}
-\frac{2\langle v_x,R_2\rangle}{\|R_2\|_2^2},\\[5pt]
&-c\frac{8\langle v_x,u_x\rangle}{\|R_2\|_2^2}
+\kappa\frac{16\|u_x\|_2^2}{\|R_2\|_2^2}
=\frac{4\langle u_x,R_2\rangle}{\|R_2\|_2^2}.
\end{aligned}$$</div>
<p>系数矩阵是可调函数方向的 Gram 矩阵。其二次型为两个平方范数之和；只要 $u_{xy}$ 与 $u_x$ 都不是零函数，它就在非零参数方向上严格为正。多个剖面时相加这些矩阵和右侧，方程组仍只有两个未知数。</p>
</details>

<h3>4. 四个目标剖面共用一组系数，得到什么？</h3>
<p>继续用上一节 P1、B、P6、P10 四组参数，让它们的 $J$ 等权相加。得到</p>
<div class="mathblock">$$
\boxed{c=@@C@@,\qquad\kappa=@@K@@.}\tag{68}
$$</div>
<p>这是一组针对指定四剖面与指定指标的共用候选。对所列谱参数，在 $0&lt;h\le1/4$ 内也满足原 Gram 正则性的充分条件。优化后的残差除以原残差，结果如下：</p>
<div class="table-wrap"><table><thead><tr><th>参数</th><th>第一式 $L^2$ 比</th><th>第二式 $L^2$ 比</th><th>第一式最大值比</th><th>第二式最大值比</th></tr></thead><tbody>@@SHARED@@</tbody></table></div>
<p>四组八项归一化残差的总体 RMS 比为 0.887312，下降约 11.27%。P1/P6 的第一式分别降低约 62.14%/39.74%，第二式的改善较小。P10 第一式的 $L^2$ 仅降低约 0.058%，最大值却增加约 0.978%。<strong>整体平方误差更小，不代表每一点的残差都更小。</strong></p>
<p>进一步直接把连续剖面代入完整有限格距方程，在 $h=1/8$，四组两式的优化前后 $L^2$ 比与二阶预测的差均小于 0.00014。这仍然只涉及空间残差，没有求解时间演化。</p>
<details><summary>如果每组参数分别优化呢？</summary>
<div class="table-wrap"><table><thead><tr><th>参数</th><th>$c$</th><th>$\kappa$</th><th>第一式 $L^2$ 比</th><th>第二式 $L^2$ 比</th></tr></thead><tbody>@@INDIVIDUAL@@</tbody></table></div>
<p>P10 单独的联合最优值使第一式增加约 1.27%，以换取第二式下降。联合目标最小并不保证每一项都改善。这些分开得到的最优值也不能在同一个多孤子方程里逐孤子混用。</p>
</details>

<h3>5. 为什么困难参数的改善这么小？可以给出下限</h3>
<p>第一式没有 $\kappa$，$c$ 只能改变与 $u_{xy}$ 同形的那一部分残差。即使完全不考虑第二式，最小相对残差也只能达到</p>
<div class="mathblock">$$\boxed{
\min_c\frac{\|R_1+2cu_{xy}\|_2}{\|R_1\|_2}
=\sqrt{1-\frac{\langle R_1,u_{xy}\rangle^2}
{\|R_1\|_2^2\|u_{xy}\|_2^2}}.
}\tag{69}$$</div>
<p>这是精确的函数投影公式。把已有剖面代入这些积分，得到：</p>
<div class="table-wrap"><table><thead><tr><th>参数</th><th>只优化第一式的 $c$</th><th>最低残差比</th><th>最多可降低</th></tr></thead><tbody>@@FLOOR@@</tbody></table></div>
<p><strong>P10 第一式即使单独调到最优，也仍保留约 99.9264% 的二阶 $L^2$ 残差。</strong>这个限制来自可调函数方向，扩大参数搜索范围也不能突破它。它是当前变量、当前两壁参数族的残差下限，不是物理解误差的下限。</p>
<p>单孤子还提供一个直观解释：把波峰居中后，$u,v$ 是偶函数，$u_{xy}$ 是偶函数，而 $u_x,v_x$ 是奇函数。因此第一残差的奇部不受 $c$ 影响，第二残差的偶部不受两个系数影响。它们都含有当前参数调不掉的部分。</p>

<h3>6. 换一组波形，还能同时改善吗？</h3>
<p>固定式 (68)，不重新拟合，再计算四组不同谱参数的解析空间残差：</p>
<div class="table-wrap"><table><thead><tr><th>参数</th><th>$(a,p,q)$</th><th>第一式 $L^2$ 比</th><th>第二式 $L^2$ 比</th></tr></thead><tbody>@@TRANSFER@@</tbody></table></div>
<p>H1/H4 的第二式分别增加约 5.62%/21.66%。所以当前系数不能保证所有波形的两式都更好；它是一个明确目标下的折中。单孤子剖面上的这些结果也没有涵盖多孤子碰撞残差。</p>
<p>如果下一步要求指定波形集合内两式都不变差，可以在同一个凸优化中加入</p>
<div class="mathblock">$$\begin{aligned}
\|R_1+2cu_{xy}\|_2&\le\|R_1\|_2,\\
\|R_2+2cv_x-4\kappa u_x\|_2&\le\|R_2\|_2.
\end{aligned}\tag{70}$$</div>
<p>原系数 $(0,0)$ 始终满足这些条件，因此不会被迫选择更差的参数；但可达到的收益也可能很小。如果目标是最大残差，应另外选择最大范数指标。本轮先完成上述 $L^2$ 分析，没有执行这两种额外优化。</p>
<div class="key"><p><strong>这一步的结论：</strong>通过常数 $c,\kappa$，可以在保留已有 Gram/Darboux 结构的参数族内，有目标地降低空间二阶残差。对于温和剖面的第一式，收益明显；对困难剖面及跨波形的双式共同改善，这两个方向的能力有限。</p><p>我们已经有了选系数的线性方程、可实现的改善幅度和调不掉的残差下限。原生产格式保持原样，尚未把候选系数当成通用替代方案。</p></div>
<p class="source"><a href="Workspaces/dlw_modified_equation_20260926/PARAMETER_OPTIMIZATION.md">完整参数优化推导</a> · <a href="Workspaces/dlw_modified_equation_20260926/optimization.json">空间残差与积分结果</a></p>
</section>
<!-- DLW-PARAMETER-OPTIMIZATION-END -->
'''
html=html.replace('@@C@@',f'{c:.11f}').replace('@@K@@',f'{kappa:.11f}').replace('@@SHARED@@',sh).replace('@@FLOOR@@',fh).replace('@@INDIVIDUAL@@',ih).replace('@@TRANSFER@@',th)
source=ROOT.parent/'gsg_project/dlw_report/_src/miura_dlw.src.html'
text=source.read_text(encoding='utf-8')
begin='<!-- DLW-PARAMETER-OPTIMIZATION-START -->';end='<!-- DLW-PARAMETER-OPTIMIZATION-END -->'
if begin in text:
    start=text.index(begin);stop=text.index(end,start)+len(end)
    text=text[:start]+html+text[stop:]
else:
    text=text.replace('<footer id="sources">',html+'\n<footer id="sources">',1)
    text=text.replace('</ol></nav>','<li><a href="#parameter-optimization">六 · 用两个常数调整残差</a><small>空间指标 → 系数选择 → 改善幅度与限制</small></li>\n</ol></nav>',1)
source.write_text(text,encoding='utf-8')
print('Generated PARAMETER_OPTIMIZATION.md and HTML source section.')
