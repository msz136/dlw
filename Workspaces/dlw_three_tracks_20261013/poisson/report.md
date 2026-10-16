# 1C：半离散 DLW 的物理 Poisson 括号及其保结构空间离散

2026-10-13。本文从项目已有的周期场 Hamilton 约化出发，写出物理变量的全部点括号；给出任意网格的 Jacobi 证明，并以 SymPy 对小网格作全变量精确核验。另给出一个精确反例：保 Poisson、保 Hamiltonian 的空间离散仍可破坏原平移动量。

## 1. 变量、周期与归一化

令 $j,k\in\mathbb Z/M\mathbb Z$ 为半离散 $y$ 格点，格距 $h>0$；$i,\ell\in\mathbb Z/N\mathbb Z$ 为新增的周期 $x$ 网格，格距 $\Delta x>0$。本文 $u_{j,i},v_{j,i}$ 始终是论文中的**物理变量**。记

\[
\Pi f=\frac1M\sum_jf_j,\qquad P=I-\Pi,\qquad
C_0=\frac{E-E^{-1}}{2h},\qquad
U=u+2a,\quad w=v-C_0u-4.
\]

其中 $(Ef)_j=f_{j+1}$，$\Pi f$ 必要时理解为各格点相同的向量。采用原周期约化的正则扇区

\[
\Pi w=c\ne0,\qquad \Pi(Uw)=\gamma,
\tag{1}
\]

$c,\gamma$ 固定。原 $x$ 连续方程通过取格点平均推出这些条件；在本文的 $x$ 离散中，直接选取同一均值约束流形。对于偶数中心差分，$D^2$ 有额外零模，因此不能再由离散隐式方程的平均式推出只有这些闭合；本文不将所选闭合误称为所有离散隐式解。

令

\[
q=Pu,\quad r=Pv,\quad \rho=-\frac1c,\quad
b_0=\frac\gamma c-2a,\quad
S_i=\frac1M\sum_aq_{a,i}r_{a,i}.
\]

物理图为

\[
\boxed{u_{j,i}=q_{j,i}+b_0+\rho S_i,
\qquad v_{j,i}=r_{j,i}+c+4,\qquad \Pi q=\Pi r=0.}
\tag{2}
\]

因为 $C_0^T=-C_0$，在每个固定 $i$ 有 $\Pi(qC_0q)=0$。故 $p=PU=q, s=w-c=r-C_0q$，$\Pi(ps)=\Pi(qr)$。式 (2) 与原 $(p,s)$ 约化完全相同，不是另造孤子参数括号。特别地，$C_0$ 仅作用在 $y$ 方向；这个物理坐标图**不含 $x$ 差分**。

物理约束可等价写成

\[
\Pi v=c+4,\qquad
\Pi[u(v-4)]=\gamma-2ac.
\tag{3}
\]

令 $D\in\mathbb R^{N\times N}$ 固定且满足 $D^T=-D, D\mathbf1=0$。主要实例是

\[
D_{i\ell}=\frac{\delta_{\ell,i+1}-\delta_{\ell,i-1}}{2\Delta x}.
\tag{4}
\]

求和配对为 $\langle f,g\rangle_h=\omega\sum_{j,i}f_{j,i}g_{j,i}$，其中 $\omega=h\Delta x$。若 $\delta_hF=\omega^{-1}\nabla F$，则

\[
\dot z=J_h\delta_h H=B_h\nabla H,\qquad B_h=J_h/\omega.
\tag{5}
\]

因此函数梯度算子与坐标点括号相差 $h\Delta x$。下文全部点括号均采用普通坐标归一化 $B_h$；中心差分本身另含 $1/(2\Delta x)$，不得遗漏或重复这个尺度。

## 2. 自由坐标的常 Poisson 括号

记 $P_{jk}=\delta_{jk}-1/M$。原连续约化括号用 $D$ 作空间离散后给出

\[
\{q_{j,i},q_{k,\ell}\}_h=0,\qquad
\{r_{j,i},r_{k,\ell}\}_h=0,\qquad
\boxed{\{q_{j,i},r_{k,\ell}\}_h
=-\frac{P_{jk}D_{i\ell}}{\omega}.}
\tag{6}
\]

其矩阵为

\[
B_0=-\frac1\omega
\begin{pmatrix}0&P\otimes D\\P\otimes D&0\end{pmatrix}.
\tag{7}
\]

这是常斜对称矩阵，故 Jacobi 恒等式成立。由 $r=s+C_0p$ 从原 $(p,s)$ 括号转来时，新增的 $rr$ 块为零：$C_0$ 与 $P,D$ 对易且 $C_0^T=-C_0$。该论证只用矩阵代数，不用空间差分的乘积法则。

保留 $x$ 连续时，相应分布括号是

\[
\{q_j(x),r_k(x')\}=-\frac{P_{jk}}h\partial_x\delta(x-x').
\]

这说明新增 $\Delta x$ 离散与原半离散场括号的对应关系。这里 $h$ 是 $y$ 格距，不能将其与新增 $\Delta x$ 混用。

## 3. 物理 $u,v$ 的完整点括号

直接将式 (2) 代入式 (6)，得到用户要求的 $uu$ 块：

\[
\boxed{
\begin{aligned}
\{u_{j,i},u_{k,\ell}\}_h
=-\frac{D_{i\ell}}{\omega}\left[
\frac\rho M(q_{j,\ell}+q_{k,i})
+\frac{\rho^2}{M^2}\sum_{a=0}^{M-1}
\bigl(r_{a,i}q_{a,\ell}+q_{a,i}r_{a,\ell}\bigr)
\right].
\end{aligned}}
\tag{8}
\]

其余三块为

\[
\boxed{
\begin{aligned}
\{u_{j,i},v_{k,\ell}\}_h
&=-\frac{D_{i\ell}}{\omega}
\left(P_{jk}+\frac\rho M r_{k,i}\right),\\
\{v_{j,i},u_{k,\ell}\}_h
&=-\frac{D_{i\ell}}{\omega}
\left(P_{jk}+\frac\rho M r_{j,\ell}\right),\\
\{v_{j,i},v_{k,\ell}\}_h&=0.
\end{aligned}}
\tag{9}
\]

右侧的 $q=Pu,r=Pv$ 均可由当前物理场直接计算，式 (8)–(9) 是完全指定的矩阵元素公式。中心差分使它们仅耦合相邻 $x$ 节点；$y$ 方向的平均约束产生全格点耦合。

推导中的三个基本计算为

\[
\{q_{j,i},S_\ell\}=-\frac{D_{i\ell}}{\omega M}q_{j,\ell},\qquad
\{S_i,q_{k,\ell}\}=-\frac{D_{i\ell}}{\omega M}q_{k,i},
\]
\[
\{S_i,S_\ell\}=-\frac{D_{i\ell}}{\omega M^2}
\sum_a(r_{a,i}q_{a,\ell}+q_{a,i}r_{a,\ell}).
\tag{10}
\]

这也表明只写 $\{u,u\}=0$ 会丢失物理均值的场依赖。自由坐标 $q$ 的自括号为零，物理 $u$ 的自括号一般不为零。

## 4. 任意 $M,N$ 的 Jacobi 证明

对每个 $i$ 再引入两个中心坐标 $b_i,d_i$，令它们与所有变量的括号为零。在 $\Pi q=\Pi r=0$ 的线性空间上取式 (6)，定义

\[
u_{j,i}=q_{j,i}+b_i+\rho S_i,\qquad
v_{j,i}=r_{j,i}+d_i.
\tag{11}
\]

这是整个有限维空间的全局多项式坐标变换，逆为

\[
q=Pu,\quad r=Pv,\quad
d_i=\Pi v_i,\quad b_i=\Pi u_i-\rho\Pi(q_ir_i).
\tag{12}
\]

因此式 (8)–(9) 是一个常 Poisson 矩阵在可逆坐标图下的推前。若 $T$ 表示式 (11)，则任意光滑 $F,G,H$ 满足

\[
\{\{F,G\}_h,H\}_h\circ T+\mathrm{cyc}
=\{\{F\circ T,G\circ T\}_0,H\circ T\}_0+\mathrm{cyc}=0.
\tag{13}
\]

固定中心坐标为 $b_i=b_0,d_i=c+4$，得到式 (3) 的物理约束流形。于是 Jacobi 对任意 $M\ge2,N\ge3$ 成立；更一般地，对任意固定斜对称 $D$ 成立。这是一般证明，小网格符号计算仅作独立核验。

此处使用的是有限维函数对坐标的普通链式法则，严格成立；没有使用错误的离散恒等式 $D(fg)=fDg+gDf$。后一个恒等式一般不成立，因而“先在 PDE 中用乘积法则化简，再把 $\partial_x$ 换成 $D$”不构成通用保结构构造。

## 5. Casimir、秩与真正的辛叶

环境空间中每个 $b_i,d_i$ 都是 Casimir。在固定式 (3) 的物理流形上，若 $\chi\in\ker D$，则

\[
C^q_{j,\chi}=\Delta x\sum_i\chi_iq_{j,i},\qquad
C^r_{j,\chi}=\Delta x\sum_i\chi_ir_{j,i}
\tag{14}
\]

也是 Casimir；每类仅有 $M-1$ 个 $y$ 分量独立。对中心周期 $D$，

\[
\kappa=\dim\ker D=
\begin{cases}1,&N\text{ 奇},\\2,&N\text{ 偶},\end{cases}\qquad
\operatorname{rank}B_h=2(M-1)(N-\kappa).
\tag{15}
\]

奇数网格只有常数零模；偶数网格还含 $\chi_i=(-1)^i$ 的 Nyquist 零模。物理均值约束流形的维数为 $2(M-1)N$，尚不是辛叶；还需固定式 (14) 的独立 Casimir。环境空间的 Casimir 个数为 $2N+2(M-1)\kappa$。这些计数对寻找有限维刘维尔约化不可省略。

| $M$ | $N$ | 均值约束后维数 | Poisson 秩 | $\dim\ker D$ |
|---:|---:|---:|---:|---:|
| 2 | 3 | 6 | 4 | 1 |
| 3 | 3 | 12 | 8 | 1 |
| 3 | 4 | 16 | 8 | 2 |
| 4 | 5 | 30 | 24 | 1 |
| 4 | 6 | 36 | 24 | 2 |

## 6. 与实际 Hamilton 空间离散的接合

在 $(p,s)$ 坐标写

\[
U=p+\frac{\gamma-\Pi(ps)}c,\qquad w=c+s,
\qquad \beta=\frac{h^2}{32}.
\]

格点逆算子为

\[
R=h\sum_{m=1}^{M-1}\left(\frac mM-\frac12\right)E^m,
\qquad R^T=-R.
\]

定义有限维 Hamiltonian

\[
K_h=\omega\sum_{j,i}\left[
\frac12U^2w+\frac\beta3w^3+wDU+\frac12wRDw-\gamma U
\right]_{j,i}.
\tag{16}
\]

因为 $R,D$ 分别作用在两个方向，它们对易且 $RD$ 对称。令

\[
f=Uw-Dw-\gamma,\qquad
k=\frac12U^2+\beta w^2+DU+RDw.
\tag{17}
\]

在式 (1) 的约束上 $\Pi f=0$。普通有限维变分直接给出

\[
\delta_h K_h/\delta p=Pf,\qquad
\delta_h K_h/\delta s=Pk,
\]
\[
\boxed{p_t=-PDk,\qquad s_t=-PDf.}
\tag{18}
\]

这里仍未使用任何离散乘积法则。故式 (18) **确实**是由原约化 Hamiltonian 建立的空间离散，也是本轮 1A 采用的周期实验流；物理流由式 (2) 重构。应使用复合 $D^2=D\,D$，如果另换独立三点二阶模板，就不再由上述 $K_h,B_h$ 自动生成。

该有限维 ODE 精确保 $K_h$ 与所有 Casimir。普通时间积分可能产生时间离散误差；本结果本身不宣称 RK 算法精确保能、保 Poisson，也不证明已有 PE/PF 算法具有这些性质。式 (18) 是可明确复现的保结构基线。

## 7. 保 Poisson 并不保证原守恒层级：精确反例

连续平移动量的离散求积为

\[
P_h=\omega\sum_{j,i}p_{j,i}s_{j,i}.
\]

它在常括号下仍生成 $(-Dp,-Ds)$。然而有限网格上的 $D$ 不是点乘代数的导子，$K_h$ 不一定对这个一参数流不变。因此

\[
\boxed{\frac{dP_h}{dt}=\{P_h,K_h\}
=\omega\sum_{j,i}\bigl[f_{j,i}(Dp)_{j,i}+k_{j,i}(Ds)_{j,i}\bigr],}
\tag{19}
\]

右侧一般不为零。$x$ 连续时它由乘积法则和周期积分消失；离散后消失的依据不再成立。二次导数项仍可用斜对称性抵消，缺陷来自局部非线性部分的离散链式法则。

一个完全有理的见证取

\[
M=2,\quad N=3,\quad h=2/3,\quad\Delta x=3/5,\quad
c=-4,\quad\gamma=-3/2,
\]
可取 $a=5/7$；$a$ 不进入约化的 $K_h,P_h$。本例 $R=0,\ \beta=1/72$，且

\[
D=\frac56\begin{pmatrix}0&1&-1\\-1&0&1\\1&-1&0\end{pmatrix}.
\]
\[
p=\begin{pmatrix}1/7&-2/7&1/2\\-1/7&2/7&-1/2\end{pmatrix},\qquad
s=\begin{pmatrix}-1/2&9/22&-9/22\\1/2&-9/22&9/22\end{pmatrix}.
\]

代入式 (18) 精确得到

\[
\boxed{\frac{dK_h}{dt}=0,\qquad
\frac{dP_h}{dt}=\frac{169}{12936}\approx0.01306431664\ne0.}
\tag{20}
\]

这不是时间步长、舍入或边界误差。它已经存在于连续时间的 Hamilton 空间离散中。因而“已证 Jacobi”不能替代“已证有限维可积”，也不能推出 1A 的全部谱积分在新增 $x$ 网格后仍严格守恒。这个反例为分离 Poisson 结构收益与完整可积层级收益提供了具体试验依据。

## 8. 本次精确验证

运行脚本：[verify_poisson.py](verify_poisson.py)。完整结果：[exact_checks.json](exact_checks.json)。Python 3.13、SymPy 1.13.3，最终完整运行约 17 秒。

| 核验 | 范围 | 结果 |
|---|---|---|
| 物理 $uu,uv,vu,vv$ 矩阵斜对称 | 三个网格，全符号 $u,v,\rho$ | 精确成立 |
| 显式点括号与坐标导数推前独立比对 | 三个网格，全符号状态 | 完全一致 |
| Jacobi 的全部不同指标三元组 | $(M,N)=(2,3),(3,3),(2,4)$，共 $220+816+560=1596$ 组 | 多项式全部恒零 |
| 均值 Casimir 的完整梯度 | 每个网格、每个 $x$ 节点 | $B_h\nabla C=0$ |
| Poisson 秩 | 上表五个网格、精确有理状态 | 全部符合式 (15) |
| $R,D,RD$ 伴随性质 | 五个网格 | 精确成立 |
| $K_h$ 有限维梯度 | $M=2,N=3$，全符号 $p,s$ | 与式 (17) 一致 |
| 连续时间能量导数、动量缺陷公式 | 五个网格、精确有理状态 | 能量为零，缺陷公式成立 |

总计 66 项记录全部通过。Jacobi 检查保留全部物理状态符号及 $\rho=-1/c$ 参数，不是随机点数值抽检；$h,\Delta x$ 取有理正数作尺度核验。对任意参数和网格的结论来自第 4 节的一般证明。

## 9. 结果来源与后续理论问题

原场结构来源于项目的 [Hamilton 历史报告](../../../dlw_hamilton.html)、[周期约化推导](../../dlw_hamilton_20261004/phase_space/periodic_reduction.md) 和 [刘维尔可积性研究第 13 节](../../../dlw_liouville_integrability.md)。本次新增的是完全指定的 $x$ 网格物理点括号、全状态 Jacobi 符号证书、奇偶网格 Casimir 计数，以及原动量不守恒的精确见证。

接下来若要升级为可积的全空间离散，必须额外构造与这些括号相容的离散谱积分并证明独立对合，或改造 $x$ 离散以承载 Lax/层级。当前有限维 Hamilton 基线适合用于检验：守住一个 Hamiltonian 与 Casimir，究竟能减少哪些误差；额外守住谱层级又能获得多少改善。
