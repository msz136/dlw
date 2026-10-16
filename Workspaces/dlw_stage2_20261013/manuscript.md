# DLW：合法约化、辛保持与误差 Lax 缺陷

2026年10月13日

本轮得到原周期 DLW 系统的一个非退化二维行波不变流形，在其上建立一自由度 Liouville 可积性；完成真实 Hamilton 网格流的数值辛保持检验；并将物理方程残差、辅助势重构误差和空间差分代数缺陷接入 Darboux–Lax 表示。三个结果共同说明：守恒量、辛结构和波形误差分别约束不同对象，需要通过相位与残差方程联系起来。

[2A 合法约化](#reduction) · [2B 数值辛保持](#symplectic) · [2C 误差 Lax 表示](#error-lax) · [误差机制](#synthesis) · [完整材料](#materials)

<section id="reduction"></section>

## 2A　固定切片的障碍与原结构的行波约化

固定 $y_0$ 只得到场的限制，通常不能决定该切片的时间导数。连续 DLW 仍含横向导数；半离散方程仍通过相邻格点耦合。完整证明给出同一切片数据而时间导数不同的反例，包括正则 $c\ne0$ 的周期半离散见证。因此，单独的“固定 $y_0$”不能直接承载 Liouville 定理。

一个合法替代是取两个周期 $y$ 格点，再限制到原方程的固定周期行波族。这里 $x$ 仍连续，有限维来自不变解族，而不是有限差分截断。

**定理（原辛结构下的一自由度 Liouville 约化）。** 取 $M=2$、$h>0$、$c\ne0$、$\gamma=0$，并固定各自由场分量的 $x$ 均值为零。设

\[
\beta=h^2/32,\qquad q_* = |hc|/4,\qquad k_0=2\pi/L,
\qquad 0<k_0<q_*.
\]

对每个传播方向和充分小的正椭圆参数 $m$，存在固定 $x$ 周期 $L$ 的光滑行波。其振幅与平移相位组成二维不变流形，原场辛形式在该流形上的限制非退化。以原平移动量 $P$ 和相位 $\phi\in\mathbb R/L\mathbb Z$ 为坐标，

\[
\omega_{\mathrm{red}}=d\phi\wedge dP,\qquad
K_{\mathrm{red}}=K_{\mathrm{red}}(P),\qquad
\dot P=0,\quad\dot\phi=\nu(P).
\]

这里 $\nu$ 是行波速度。因而 $P$ 是一个独立第一积分，约化系统 Liouville 可积；所有平移不变谱量的限制都是 $P$ 的函数，故两两对合。

**显式构造。** 记 $\mathbf K(m)$ 为第一类完全椭圆积分，取

\[
b=\frac{4\mathbf K(m)}{L},\quad A=\sqrt m\,b,\quad
\nu=\pm\frac{\sqrt{(q_*^2-A^2)(q_*^2-b^2)}}{q_*}.
\]

对 $\xi=x-\phi$，令

\[
p=A\operatorname{sn}(b\xi\mid m),\qquad
s=\frac{c(p'-\nu p)}{p^2-q_*^2}.
\]

两格点场为

\[
U_{0,1}=-ps/c\pm p,\qquad w_{0,1}=c\pm s,
\qquad u=U-2a,\quad v=w+4.
\]

直接代入可验证原场方程。半周期反对称性使 $p,s$ 的均值自动为零；小振幅保证分母及 $w_{0,1}$ 不退化。原动量

\[
P=2h\int_0^Lps\,dx,\qquad
\lim_{m\downarrow0}\frac{dP}{dm}
=\frac{hcL\nu_0k_0^2}{q_*^2}\ne0,
\quad \nu_0=\pm\sqrt{q_*^2-k_0^2},
\]

给出原辛形式非退化的关键条件。用 $I=P/k_0$、$\theta=k_0\phi$ 便得到 $2\pi$ 周期角坐标。

这是一个独立积分的一自由度定理，不是高自由度守恒族独立性定理。它使用 $M=2$ 交替横向模态；固定 $c,L$ 令 $h\to0$ 时，存在条件会失效，不能据此推出一般连续二维场的有限维约化。

REDUCTION_PROOF

<section id="symplectic"></section>

## 2B　离散时间演化是否保辛

固定空间网格时，$x$ 是场的标签，$\delta x=0$；$du\wedge dx$ 因而不能作为场相空间的非退化辛检验。这里使用上一阶段的原 Poisson 空间离散，固定全部 Casimir 后，在辛叶上检验

\[
\Omega_h=-B_{\mathrm{leaf}}^{-1},\qquad
\mathcal E_\omega=
\frac{\|(D\Phi)^T\Omega_hD\Phi-\Omega_h\|_F}{\|\Omega_h\|_F}.
\]

采用 $i_{X_H}\omega=dH$ 的符号约定。$D\Phi$ 是实际数值程序的切映射；它同时推进全部变分方向，未用能量漂移替代辛缺陷。

实验沿用上一阶段的非线性初值，取 $M=3,h=4,c=2,\gamma=4,L_x=2\pi,N_x=15$，辛叶维数为 $56$。以下在相同 $T=0.02,\Delta t=0.0025$ 下比较；物理场末态误差以高精度状态及变分积分为参考，取两场最大范数的较大值。

SYMPLECTIC_TABLE

SYMPLECTIC_FIGURE

精确求解的隐式中点法保持这个常辛形式，显式 Euler 和经典 RK4 一般不保持。此次短时试验中 RK4 的状态精度高于中点法，而中点法的辛缺陷更小。二者并不矛盾：精度与结构保持需要分别衡量。

**非线性求解容差会改变实际结论。** 在 $\Delta t=0.02$、容差 $10^{-8}$ 时，中点程序只做一次 Newton 校正，方程残差为 $1.37\times10^{-9}$，实际辛缺陷为 $1.79\times10^{-8}$。若直接套用理想隐式方程的切映射公式，则会得到约 $4.74\times10^{-16}$，掩盖未解准的影响。本实验对实际有限 Newton 迭代求导，并用独立复步长方向微分核对。

默认细化中，$\Delta t=0.00125$ 时提前停在一次 Newton 校正，累计辛缺陷约为 $2.73\times10^{-13}$；至少进行两次校正后降至 $1.51\times10^{-15}$。这解释了曲线的小幅反升。低于统一拟合阈值的数据不用于估阶，RK4 的观测阶也不被写成一个普适的高阶保辛定理。

TOLERANCE_FIGURE

SYMPLECTIC_PROOF

<section id="error-lax"></section>

## 2C　从误差场到带源 Lax 表示

使用原半离散 DLW 的 Darboux 因子

\[
\alpha_j=U_j/2+hw_j/8,\quad\eta_j=U_j/2-hw_j/8,
\quad A_j=\partial_x-\alpha_j,\quad B_j=\partial_x-\eta_j,
\quad T_j=B_j^{-1}A_j,\quad Q_j=-\partial_x^2-V_j.
\]

对于不必精确满足方程的场，定义势差缺陷
$\kappa_j=V_{j+1}-V_j-(h/2)w_{j,x}$，以及两个 Riccati 残差

\[
E_j^\alpha=\alpha_{j,t}+\alpha_{j,xx}+2\alpha_j\alpha_{j,x}+V_{j,x},
\quad
E_j^\eta=\eta_{j,t}+\eta_{j,xx}+2\eta_j\eta_{j,x}+V_{j+1,x}.
\]

**精确缺陷恒等式**为

\[
\boxed{B_j\mathcal Z_j=-E_j^\alpha+E_j^\eta T_j+\kappa_jA_j,\qquad
\mathcal Z_j=T_{j,t}-Q_{j+1}T_j+T_jQ_j.}
\]

它把场方程的残差与线性问题的不相容量联系起来。对两个状态取差，误差的 Lax 变量同时受背景、算子变分及残差源驱动；误差场并不自动构成独立的等谱系统。

在具有循环迹的 Lax 表示 $L_t=[Q,L]+R$ 中，两状态的谱量误差满足

\[
\frac{d}{dt}\left[\operatorname{Tr}\widehat L^n-
\operatorname{Tr}L^n\right]
=n\operatorname{Tr}\left(\widehat L^{n-1}\widehat R-L^{n-1}R\right).
\]

这里的迹必须有定义并允许循环换位；相应积分界另需算子范数控制。形式伪微分迹、有限矩阵迹与上一阶段的固定密度求积不能未经证明就互换。

**空间差分产生额外代数源。** 令 $M_f$ 为格点乘法矩阵，

\[
C_1(f)=[D,M_f]-M_{Df},\qquad
C_2(f)=[D^2,M_f]-2M_{Df}D-M_{D^2f}.
\]

这两项衡量连续乘积法则在网格上的失败。系数层还需保留 $D(Uw)-U\,Dw-w\,DU$ 等链式缺陷。精确有理见证表明：即使网格方程残差及势重构残差均为零，直接把 $\partial_x$ 换成 $D$ 后的矩阵 Lax 缺陷仍可非零。因此，物理方程求解准确与谱传递准确之间，还隔着可明确计算的空间代数缺陷。

ERROR_LAX_PROOF

<section id="synthesis"></section>

## 三项结果之间的联系

2A 的原 action–angle 约化提供了一个可精确回答误差问题的试验场。两条族内精确轨道满足

\[
\delta I(t)=\delta I(0),\qquad
\delta\theta(t)=\delta\theta(0)+t[\Omega(I+\delta I)-\Omega(I)].
\]

该族的 twist 非零。因此 action 差虽保持不变，提升角误差仍可线性累积。相位对齐后，紧正则子环域上的轨道误差则有统一界 $C|\delta I|$。相应变分流是严格保辛的剪切，说明保辛本身不控制距离增长。

若约化 action 方程受到缺陷源 $r_I$ 驱动，该源会以 $\int_0^t(t-s)r_I(s)\,ds$ 的形式进入角误差界。由此可把研究重心进一步落到三个可区分的量：action 或谱量漂移、相位误差，以及偏离不变解族的误差。将这一约化估计推广到一般数值场，还需要控制流形外的偏离。

SYNTHESIS_PROOF

<section id="materials"></section>

## 完整材料

- [复现说明](README.md)：各专题的证明、数值脚本、数据及检查入口。
- [2A 定理与证明](reduction/report.md)、[椭圆约化验证](reduction/verify_reduction.py)、[检查记录](reduction/verification.json)、[椭圆波数值表](reduction/elliptic_family_checks.csv)。
- [2B 数值脚本](symplectic/symplectic_experiment.py)、[固定时间数据](symplectic/fixed_time.csv)、[单步数据](symplectic/single_step.csv)、[中点容差扫描](symplectic/midpoint_tolerance.csv)。两张数值图均有同名 PDF。
- [2C 完整推导](error_lax/REPORT.md)、[精确代数验证](error_lax/verify_error_lax.py)、[Lax 缺陷有理见证](error_lax/exact_checks.json)。
- [误差机制的证明](synthesis.md)、[独立代数核验](verify_synthesis.py)。
- [上一阶段报告](../../report/dlw_three_tracks_20261013.html)：守恒量漂移、孤子误差频谱及原物理 Poisson 括号。
