# T01：固定 Γ 的有限 h 相位限制——独立推导

2026-10-01。范围：固定物理 a、正格距 h、精确 x/t 微分，同一连续单孤子谱族。只用已有常数 α、β；两常数在整个预先指定谱区间及 h→0 的比较中共用。本文不含新 PDE 实验或参数扫描。

## 1. 假设、谱分支与精确相位

令 Γ>0、Γ≠1，I=[A₋,A₊] 为长度非零、完全位于一条非零半轴的紧区间。设

\[
x=P^{-1}=\frac{A}{1+\Gamma},\qquad
y=Q^{-1}=-\frac{\Gamma A}{1+\Gamma},\qquad
L=x+y=\lambda_\Gamma A,\quad
\lambda_\Gamma=\frac{1-\Gamma}{1+\Gamma}.
\]

因此 P=(1+Γ)/A、Q=−(1+Γ)/(ΓA)。若还要求单孤子的 K=P+Q>0，则

\[
K=\frac{\Gamma^2-1}{\Gamma A}>0
\quad\Longleftrightarrow\quad \operatorname{sign}A=\operatorname{sign}(\Gamma-1).
\]

若不要求 K>0，正实 τ 分支还须另行检查权重/交叉 Gram 分母。下文相位代数只需所给半轴及正实乘子分支；并不替代多孤子的所有正则条件。

特别地，不能将一个连续固定 Γ 区间无条件声明成“任意谱组合的全局正则实多孤子族”。固定 Γ 给出 \(q_i-q_k=-(p_i-p_k)/\Gamma\)，故不同近邻谱点、正交叉分母下相互作用系数 A\_{ik}<0。若 K\_i,K\_k>0 且 E\_i,E\_k 权重为正，则二孤子 \(g=1+E_i+E_k+A_{ik}E_iE_k\) 随 x 从 1 变到负值，必有零点。相位定理安全适用于 N=1 的整段族，或在已明确证明 τ 无零的有限物理域上逐谱应用。要求所有交叉分母为正还会给出 R\_I<max(Γ,1/Γ)，但该条件并不是 τ 正则性的充分条件。

该反例可严格落实于任何非退化 I：任选其内部谱点 A₀，由 K(A₀)>0 及连续性，选取两个足够近且不同的 A₁,A₂，使全部 \(p_i+q_k\) 仍为正。相互作用分子恰为 \(-(p_1-p_2)^2/\Gamma<0\)，所以 A₁₂<0。固定任意 y,t，正权重指数 Eᵢ=cᵢexp(Kᵢx+⋯) 满足 Eᵢ→0（x→−∞），而 E₁E₂ 的增长严格快于每个 Eᵢ（x→+∞）；故 g→1 与 g→−∞，由介值定理 g 至少有一个实零点。连续 τ₁ 为 \(f=1+\Gamma(E_1+E_2)+\Gamma^2A_{12}E_1E_2\)。在 g=0 处，

\[
f=f-\Gamma^2g=(1-\Gamma)[1+\Gamma+\Gamma(E_1+E_2)]\ne0.
\]

因此该零点不能通过 f/g 的共同零点消去，连续物理 u=2∂ₓlog(f/g) 必奇异。这仅排除“任意组合的全局实正则族”；不排除特定分离谱、有限无零域、复谱或其他 Gram 正则构造。

记 μ=αh²、r=1+βh²、H=hr。原结构给出

\[
\chi_h(A)=\frac{P-\mu+H/2}{P-\mu-H/2}
\frac{Q+\mu+H/2}{Q+\mu-H/2},\qquad
\kappa_h=\frac{\log\chi_h}{h}.
\tag{1}
\]

这里取从 h=0 连续延拓的实对数分支，并要求 H>0。设

\[
\widetilde x=\frac{x}{1-\mu x},\qquad
\widetilde y=\frac{y}{1+\mu y}.
\]

在 1−μx>|Hx|/2、1+μy>|Hy|/2 下，两个格点因子都为正，且

\[
\kappa_h=\frac2h\left[
\operatorname{artanh}\frac{H\widetilde x}{2}
+\operatorname{artanh}\frac{H\widetilde y}{2}\right].
\tag{2}
\]

Γ≠1、A≠0 保证归一化分母 L≠0。

### 整个谱区间的精确可行条件

设 σ=sign A、M=max\_{A∈I}|A|、cΓ=max(1,Γ)/(1+Γ)。由于 x、y 在同一半轴区间上线性依赖 A，上述正则条件在整个 I 上**等价于**

\[
r>0,\qquad
c_\Gamma M\left[\sigma\alpha h^2+\frac{h(1+\beta h^2)}2\right]<1.
\tag{3}
\]

若括号≤0，第二条件自动成立。式 (3) 保证 P−μ±H/2、Q+μ±H/2 不过零，并保持各自的连续符号。因此 γ(s₋)、γ(s₊) 也保持正。若要求所有 0<h≤h₀ 都正则，需要 (3) 对全部这些 h 成立；不能仅凭 h₀ 端点代替，除非先证对应三次多项式单调。

## 2. 归一化的精确积分式

设 JΓ=Γ/(1+Γ)²，

\[
D=(1-\mu x)(1+\mu y)
=1-\alpha h^2 A+\alpha^2h^4J_\Gamma A^2.
\]

直接通分得 \(\widetilde x+\widetilde y=L/D\)。正则分支上 \(\widetilde x\) 和 \(-\widetilde y\) 同号。将 artanh 的差商写成积分，得到

\[
\boxed{\frac{\kappa_h}{L}
=\frac rD\int_0^1
\frac{d\theta}{1-(H/2)^2z_\theta^2},
\qquad z_\theta=\theta\widetilde x-(1-\theta)\widetilde y.}
\tag{4}
\]

这是精确公式，不是 Taylor 模型。证明使用

\[
\frac{\operatorname{artanh}a-\operatorname{artanh}b}{a-b}
=\int_0^1\frac{d\theta}{1-[\theta a+(1-\theta)b]^2}.
\]

式 (4) 避免用 \((|x|^m+|y|^m)/|L|\) 进行粗估所引入的人为 1/|Γ−1| 因子。Γ=1 的原归一化仍未定义；只有 Γ→1 的形式极限是平滑的。

## 3. 首项与显式统一四阶余项

由 (4) 展开

\[
\frac{\kappa_h-L}{L}
=h^2q_{\alpha,\beta}(A)+R_h(A;\alpha,\beta),
\quad q_{\alpha,\beta}=\beta+\alpha A+C_\Gamma A^2,
\tag{5}
\]

其中

\[
C_\Gamma=\frac{1+\Gamma+\Gamma^2}{12(1+\Gamma)^2}>0.
\]

下面给一个可直接检查的统一常数。预先限定 |α|≤a₀、|β|≤b₀、0<h≤h₀。记 ε₀=h₀²、s=cΓM、

\[
\rho=a_0\varepsilon_0s<1,\quad
R=1+b_0\varepsilon_0,\quad
\delta=(1-\rho)^2,\quad
q=\frac{h_0Rs}{2(1-\rho)}<1,
\quad b_0\varepsilon_0<1.
\tag{6}
\]

这些是充分条件，使整个参数盒在全部 h∈(0,h₀] 上正则，且 r>0。再记

\[
E_0=C_\Gamma M^2,\quad J=J_\Gamma M^2,\quad
B_r=b_0(3+3b_0\varepsilon_0+b_0^2\varepsilon_0^2),
\quad
T_\Gamma=\frac{1+\Gamma+\Gamma^2+\Gamma^3+\Gamma^4}
{80(1+\Gamma)^4}.
\]

一个显式余项界为

\[
\sup_{A\in I}|R_h|\le h^4B,
\tag{7}
\]

\[
\begin{aligned}
B={}&\frac{a_0b_0M+12a_0^2E_0
+\varepsilon_0a_0^2J(b_0+a_0M)}{\delta}\\
&+\frac{E_0(B_r+a_0M+\varepsilon_0a_0^2J)}{\delta^2}
+\frac{a_0s^3}{2\delta}
+\frac{R^5T_\Gamma M^4}{\delta^3(1-q^2)}.
\end{aligned}
\tag{8}
\]

这个常数以可核查为主，并非最紧常数。

### 余项证明

令 ε=h²、\(K_2=(\widetilde x^2-\widetilde x\widetilde y+\widetilde y^2)/12\)。在 (4) 的几何级数中保留前两项，得

\[
\frac{\kappa_h}{L}=\frac rD+\varepsilon\frac{r^3}D K_2
+\varepsilon^2\frac{r^5}{16D}
\int_0^1\frac{z_\theta^4}{1-(H/2)^2z_\theta^2}\,d\theta.
\tag{9}
\]

第一项减去 1+ε(β+αA) 后，精确为

\[
\varepsilon^2\frac{\alpha\beta A
+\alpha^2(A^2-J_\Gamma A^2)
-\varepsilon\alpha^2J_\Gamma A^2(\beta+\alpha A)}D.
\]

因 A²−JΓA²=12CΓA²、D≥δ，其界正好是 (8) 第一行。

第二项使用

\[
K_2\le E_0/\delta,
\quad \left|\frac{r^3/D-1}{\varepsilon}\right|
\le(B_r+a_0M+\varepsilon_0a_0^2J)/\delta.
\]

以 \((u^2-uv+v^2)/12\) 的梯度界及
\(|\widetilde x-x|,|\widetilde y-y|\le a_0\varepsilon s^2/(1-\rho)\)，得到

\[
|K_2-C_\Gamma A^2|/\varepsilon\le a_0s^3/(2\delta).
\]

最后，\(|z_\theta|\le [\theta|x|+(1-\theta)|y|]/(1-\rho)\)。将四次方积分并用最大几何比 q² 包围分母，得到

\[
\int_0^1[\theta|x|+(1-\theta)|y|]^4d\theta
\le 16T_\Gamma M^4.
\]

因此 (9) 最后一项被 (8) 最后一项乘 h⁴ 所控制，证明 (7)。全部估计覆盖完整连续谱区间及参数盒，未使用有限样本。

## 4. 原结构的有限 h 基准可以精确确定

对 α=β=0，(4) 变成正项级数：

\[
\frac{\kappa_h-L}{L}
=\sum_{n\ge1}\frac{h^{2n}A^{2n}}{4^n(2n+1)}
\frac{\sum_{j=0}^{2n}\Gamma^j}{(1+\Gamma)^{2n}}.
\tag{10}
\]

所有系数严格为正，因而相位指标

\[
E_h^0:=\sup_{A\in I}|(\kappa_h-L)/L|
\]

恰在 |A|=M 取到，可由 (2) 或 (10) 精确求出。若 q₀=h₀cΓM/2<1，则

\[
h^2E_0\le E_h^0\le h^2E_0+h^4B_0,
\quad B_0=\frac{T_\Gamma M^4}{1-q_0^2}.
\tag{11}
\]

右端从 (9) 的四阶积分直接得到，比只用绝对值分离 x/y 更紧。

## 5. 最佳一致逼近：完整证明与可行性

记 m=(A₋+A₊)/2、d=(A₊−A₋)/2>0。对任意常数 α、β，二阶差分消去仿射项：

\[
q(m-d)+q(m+d)-2q(m)=2C_\Gamma d^2.
\]

若 \(\|q\|_{L^\infty(I)}\le E\)，则左边≤4E，故

\[
\boxed{E\ge E_*:=C_\Gamma d^2/2
=C_\Gamma(A_+-A_-)^2/8.}
\tag{12}
\]

令

\[
\alpha_*=-2C_\Gamma m,\qquad
\beta_*=C_\Gamma m^2-C_\Gamma d^2/2.
\tag{13}
\]

则 \(q_*=C_\Gamma[(A-m)^2-d^2/2]\)，端点为 E*，中点为 −E*，区间内绝对值≤E*。下界因此达到。

最优点唯一：若 E=E*，二阶差分不等式必须逐项等号，强迫两个端点值 E*、中点值 −E*；这三式唯一确定 (13)。它也说明首项不可能在非退化区间全部消失。首项最多可在两个不同谱尺度上同时为零；这句话不自动约束有限 h 精确误差的零点数。

在有界且保留预定正则余量的闭紧可行集中，(12) 仍是下界，等号达到当且仅当 (13) 属于该集。若只取 (3) 定义的开可行集，边界点可能只被逼近；此时 inf 可以等于 E* 而不被达到，不能混淆“等号达到”与“下确界相等”。

因为 I 在同一非零半轴，|m|>d，故 β*>0；α* 向谱半轴的反方向移动参数中心。它有利于避开中心移位的极点，但增大的 H 仍须按 (3) 检查。(13) 只由 Γ、I 决定，不依赖 h，符合冻结常数要求。

## 6. 十倍范围阈值与有限 h 定量判据

这里冻结的指标是**归一化纵向相位** \(E_h(\alpha,\beta)=\sup_I|(\kappa_h-L)/L|\)。它不是物理 u/v 的误差指标。

首项基准为 E₀=CΓM²，故最佳比值

\[
\frac{E_*}{E_0}=\frac{(A_+-A_-)^2}{8M^2}.
\tag{14}
\]

设 m₀=min\_I|A|>0、谱尺度比 R\_I=M/m₀。由于同半轴，A₊−A₋=M−m₀。因此首项十倍改善的必要且无约束可实现条件为

\[
\frac{E_*}{E_0}\le\frac1{10}
\quad\Longleftrightarrow\quad
R_I\le 5+2\sqrt5\simeq9.472135955.
\tag{15}
\]

等号没有有限 h 的严格余量。若可行参数盒满足 (6)，由 (7) 得所有可行常数上的有限 h 下界

\[
\inf E_h\ge h^2E_*-h^4B.
\tag{16}
\]

这不允许把 α、β 无界放大后继续沿用同一个 B。

若 Chebyshev 常数 (13) 可行，以包含该点的冻结参数盒求 B*，则

\[
E_h(\alpha_*,\beta_*)\le h^2E_*+h^4B_*.
\tag{17}
\]

所以：

- 若 \(E_*+h^2B_*\le E_0/10\)，(11)、(17) 认证所选固定常数至少十倍改善归一化相位。
- 若 \(E_*-h^2B>(E_0+h^2B_0)/10\)，(11)、(16) 排除整个冻结可行集内的十倍相位改善。
- 落在两项余量之间时，本界不决定结果；可以从精确公式作解析加强，不应据少量样本重划范围。

因此 R\_I<5+2√5 且最优点可行时，充分小 h 留有十倍相位改善的理论可能；R\_I>5+2√5 时，对任何冻结有界可行集，充分小 h 都不能实现十倍归一化相位改善。阈值与 Γ 无关是所选归一化指标的结果；未归一化的 |κ−L| 或固定 y 条带的相位误差含 |L(A)| 权重，不能沿用 (15)。

## 7. 固定有限 h 也不能在整段谱范围完全匹配

这不是仅由二阶展开推出的结论。对任意固定 h>0 及有限 α、β，式 (1) 在固定 Γ 下是 A 的有理函数，分子和分母次数至多 2。假设在非退化开区间上相位完全匹配，则

\[
\chi_h(A)=\exp(h\lambda_\Gamma A).
\]

写 χ=N/D（约去公因子），对数导数满足

\[
N'/N-D'/D=h\lambda_\Gamma\ne0.
\]

区间上的相等给出有理恒等式；然而任何非零多项式 N、D 的对数导数差在 A→∞ 时为 O(1/A)，不可能恒等于非零常数，矛盾。该论证包括多项式降阶、分子分母约消和 H=0 的情形；后者 χ=1 同样不可能匹配 L≠0。

于是两个结构常数在任何固定正 h 上都不能让整段正则谱区间的相位缺陷为零。它不提供无界参数集上的数值下确界；定量有限 h 下界仍按 (16) 的有界集假设给出。

## 8. 结论不能直接提升到共同初值 u/v 演化

相位差只给自然 Gram 解族的一项偏移。F 的中心系数、交错物理重构和初始提升也各有 h² 修正。譬如令 γ\_±=γ(s\_±)，中心放置的 F 系数为 \(\sqrt{\gamma_-\gamma_+}\)，其相对连续 Γ 的对数满足

\[
\frac12\log\frac{\gamma_-\gamma_+}{\Gamma^2}
=-h^2L(\alpha+A/8)+O(h^4).
\]

因此把 (16) 乘一个 u/v 导数并不构成整场下界。更关键的是，同物理初值下，精确离散族的静态偏移 B(t) 必须减去其初态偏移的传播 \(\Phi(t,0)B(0)\)；在 t=0 两者严格抵消。边界不相容时还需边界纠正。有限 h 相位限制只界定“两个常数能校准多少谱曲率”，没有证明物理传播映射在该余量方向上具有统一正下界。

要升级为十倍 u/v 演化不可能性，至少还需：固定物理初边值、冻结双场范数；推导包含全部重构/提升修正的源；证明从不可消去相位/源方向到指定时间物理输出的统一非退化界；包围传播、非线性及高阶余量。没有这条桥梁时，应止于相位定理。

## 9. 已有事实与本次增量

- 已有事实：两壁参数族、精确 Möbius 乘子及首项相位来自 `dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md` §2；物理源方向与共同初值传播来自 `dlw_factor_model_20260930/REPORT.md` §6、10。
- 已有种子：修订3的 `ideas.json`、`theory_seed_checks.json` 已核对二次归一化与 Chebyshev 值；该核对不能代替正则分支与余项证明。
- 本次完整证明/加强：区间的精确可行条件 (3)、归一化有限 h 积分式 (4)、显式统一余项 (7)–(8)、原结构的正项基准 (10)–(11)、唯一 minimax 点及可行性区分、十倍尺度比阈值与有限 h 认证/排除式 (15)–(17)、固定有限 h 整区间完全匹配的有理函数障碍。
- 未解：相位障碍经全部物理重构及共同初值纠正后的统一场误差下界；外部文献原创性。本笔记没有数值扫描，也不声称物理优化成功。
