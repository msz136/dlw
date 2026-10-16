# c=0、非零平均通量的全周期分支审查

2026-10-11。Γ 在相空间中保留为状态量，本报告不预先把它固定成一个外部时间常数。

前置材料：[原周期物理约束](../../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md)、[已有全周期谱与解析范围](../../Workspaces/dlw_general_field_20261006/RESEARCH_NOTES.md)。

## 物理兼容、χ 的符号及强制守恒

令 x 的周期为 L，格点周期 M≥2，D=∂x，β=h²/32，R 为原稿的有限格点反对称矩阵。取

$$
\Pi p=\Pi s=0,\qquad U=b+p,\quad w=s,
\qquad q=\Pi(ps).
$$

原方程的平均兼容在 c=Πw=0 上强制 qₓ=0，所以 q(x,t)=Γ(t)。投影物理方程恰为

$$
p_t=-D(bp)-P_0D(p^2/2+\beta s^2)-p_{xx}-Rs_{xx},
$$

$$
s_t=-D(bs+ps)+s_{xx}. \tag{1}
$$

逐项计算 Π(pₜs+psₜ)：b 项为 −bqₓ−2qbₓ；p 非线性项为 −DΠ(p²s)；s 非线性项为 −(2β/3)DΠs³；相反扩散项为 DΠ(psₓ−spₓ)；R 项为 −DΠ(sRsₓ)，因为 Π(sₓRsₓ)=0。故

$$
q_t=-bq_x-2qb_x+D\chi,
$$

$$
\chi=-\Pi(p^2s)-\frac{2\beta}{3}\Pi s^3
+\Pi(ps_x-sp_x)-\Pi(sRs_x). \tag{2}
$$

在 q=Γ(t) 上，

$$
\Gamma'(t)=D[-2\Gamma b+\chi].
$$

对 x 积分给 **Γ′=0**。这是原周期物理方程推出的守恒，不是闭合假设。非零通量扇区因此满足

$$
b=\chi/(2\Gamma)+B(t),\qquad \Gamma\ne0. \tag{3}
$$

初值的 Γ 可以在非零开扇区内变化。B(t) 是空间积分自由度，保留为任意平移规范。Γ=0 时 (3) 不能使用，需另行处理 χₓ=0 的兼容；本文不涵盖该扇区。

## 真正的约束相空间与 Dirac 张量

用 hΣⱼ∫ 的梯度配对，原投影张量为

$$
J=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix},
$$

$$
H_0=h\sum_j\int
\left[\tfrac12p_j^2s_j+\frac\beta3s_j^3+s_jp_{j,x}
+\tfrac12s_j(Rs_x)_j\right]dx. \tag{4}
$$

它生成 (1) 的 b=0 项；s 方程中的 P₀ 与原式在 qₓ=0 上相同。

令 $\mathcal P_x f=f-L^{-1}\int f$，只施加约束

$$
\mathcal P_x q=0,
$$

而不固定 $\Gamma=L^{-1}\int q$。约束生成元

$$
F_f=hM\int f q=h\sum_j\int f p_js_j
$$

满足

$$
X_{F_f}(p,s)=(-D(fp),-D(fs)),
\qquad X_{F_f}q=-2qf_x-fq_x. \tag{5}
$$

所以在实际约束面上的非零 x 模态约束矩阵为

$$
C=-2\Gamma D,
\qquad C^{-1}=-\frac1{2\Gamma}D^{-1}, \tag{6}
$$

其中 D⁻¹ 仅作用在零空间均值的周期函数上。Γ≠0 恰是这里的非退化条件。不可把周期 D⁻¹ 误作全空间双边逆。

设 A 为 q 的微分，$A(\dot p,\dot s)=\Pi(s\dot p+p\dot s)$，$A_0=\mathcal P_xA$。相空间

$$
\mathcal S_0=\{(p,s)\in C^\infty_{\rm per}:
\Pi p=\Pi s=0,\ \mathcal P_x\Pi(ps)=0,\ \Gamma\ne0\}
$$

上的 Dirac 张量为

$$
J_D=J-JA_0^*C^{-1}A_0J. \tag{7}
$$

式 (6) 使非零模态约束有正则的弱 Dirac 约化。作为周期光滑泛函的 Poisson 约化，Jacobi 可由 Dirac 恒等式验证/继承；这不等于在一个 Sobolev 开邻域构造了实际时间流。局部函数空间证明可使用 C∞ 的弱辛/分级图，或分别记录 D 与 D⁻¹ 的 Sobolev 阶数；不要隐去其导数阶数而声称普通有界 Hamilton 向量场。

q=Γ≠0 还保证 p,s 不会同时零向量，从而 q 的点态约束微分非零。对固定原分量空间均值的叶，(6) 给零均值目标的右逆：$A_0JA_0^*C^{-1}=I$。因此约束不是仅形式地“选一条解”；它是原场变量上的正则非零模态约束。

动量

$$
\mathcal P=hM\int q=hML\Gamma
$$

满足 $X_{\mathcal P}=-D(p,s)$。Γ 在 (7) 下不是 Casimir。可选地固定动量并商去平移；主分支不需要该额外步骤，Γ 可随初值变化。

## b 的零模规范：必须区分两种 B

由 (2),(4) 分部积分，

$$
\int\chi=-2H_0/(hM),\qquad
\overline\chi/(2\Gamma)=-H_0/\mathcal P. \tag{8}
$$

Dirac 约化用零均值约束乘子。因此 $J_D\delta H_0$ 在原式中对应

$$
b_0=(\chi-\overline\chi)/(2\Gamma)
=\chi/(2\Gamma)+H_0/\mathcal P,
\qquad \overline b_0=0. \tag{9}
$$

加入任意规定的**平均速度** $\widetilde B(t)\mathcal P$ 后，b=b₀+\widetilde B(t)。这覆盖 (3) 的空间积分自由度，而且 H₀、𝒫 沿这些流均守恒，所以 (3) 中的 B=H₀/𝒫+\widetilde B(t) 仅多一个由初值决定的时间常数。

若外部另外规定了 (3) 的同一个 B(t)，在整个 Γ 可变相空间上的向量则为

$$
X_{H_0}^D-(H_0/\mathcal P)X_{\mathcal P}^D+B(t)X_{\mathcal P}^D.
$$

不能直接称它在同一个 J_D 下由 H₀+B(t)𝒫 生成：对应的一形式
$dH_0-(H_0/\mathcal P)d\mathcal P$ 一般不闭。可通过规定平均 b 的规范，或平移商，避免这项混淆。本任务没有外部指定 B(t)，所以 (9) 是合法的物理平移规范，不是人为固定 Γ。

## c=0 的谱平方根：定义与明确的阶数限制

取原 transfer 因子

$$
T_j=(D-U_j/2+hw_j/8)^{-1}(D-U_j/2-hw_j/8),
\qquad P=T_{M-1}\cdots T_0.
$$

它在 c=0 上仍有意义。旧归一化用 G=hMc/4，因此不能在此直接除 G。此时

$$
P=I+a_2D^{-2}+a_3D^{-3}+\cdots,
\qquad
a_2=-hM\Gamma/8\ne0. \tag{10}
$$

可定义

$$
N=a_2(P-I)^{-1},\qquad
L_0=N^{1/2}=D+u_0+u_1D^{-1}+\cdots. \tag{11}
$$

N 首项为 D²，故 monic 平方根唯一，其每个固定阶系数是有限 jets 除 a₂ 的有限幂；无须全 PDO 级数实际收敛。a₂ 可正可负，N 的首系数仍为一，实分支系数仍实。

u₀一般不为零，具体 $u_0=-a_3/(2a_2)$。把它移去需要 scalar gauge，通常有非零 holonomy；不能偷称周期 gauge。也不能未经证明把这个约束场张量等同标准 `u0=0` KP 张量。

另一个重要限定：order-one 的 (11) 定义在 `a1=0,a2≠0` 谱层。一般 ambient 方向有 a₁≠0 时 (P−I) 的阶数改变，平方根成为半整数阶，因此 Fn=Tr L₀ⁿ 不是直接由同一式给出的一般 ambient 光滑函数。其 Poisson 证明应使用以下显式扩展与切向代表，不能略过这个问题。

修复方法是令 $\widetilde P=P-a_1D^{-1}$，在 a₂(x) 与常数归一化参数同号非零的邻域，定义 $\operatorname{Tr}[a_2(\widetilde P-I)^{-1}]^{n/2}$。离开约束面时首系数允许为 $\sqrt{a_2/a_2(x)}$，不强求 monic；它仍是实 order-one 根，每个固定阶系数是光滑的有限-jet 泛函。在约束面它恢复 (11)。其导数与下面的 commuting 代表只差 a₁ 的 conormal；因为公共 U 规范不变性使选定 Hamilton 场切向 a₁=0，first-class Poisson 约化保证结果不依这个 conormal 选择。实际 a₂=−hMΓ/8 的全局状态依赖另按 (13) 处理。

## 谱泛函的切向性与正式对合：可以实算的部分

首先证明两个关键的规范/约束切向性，而不沿用 c≠0 的结论。

1. 在未投影的 U,w 常系数物理括号下，F_f=hΣ∫fUw 生成 Uₜ=−D(fU)、wₜ=−D(fw)。令 Aⱼ=D−Uⱼ/2−hwⱼ/8，Bⱼ=D−Uⱼ/2+hwⱼ/8，直接计算

$$
(A_j)_t=-[fD,A_j]-f_xA_j,
\quad (B_j)_t=-[fD,B_j]-f_xB_j,
$$

$$
(T_j)_t=-[fD,T_j],\qquad P_t=-[fD,P]. \tag{12}
$$

因此任何以常数 a₂ 作归一化的 trace $\operatorname{Tr}\Phi(P)$ 与所有 F_f 对合。这里 q 的点态约束不是猜测的“谱流应该保持”，而是 (12) 给出的直接证书。

2. 任意公共 U 变换 Uⱼ→Uⱼ+a(x)，使各因子及 P 由 e^σ 共轭，σₓ=a/2。σ 可准周期。形式 residue 在这种标量共轭下点态不变，所以 (11) 的 trace 完全不依 b(x)，包括其常数零模。这使 trace 在平均 w=0 的 first-class 规范约化下合法；投影后的 −offdiag P₀D 括号与此类规范不变泛函的 ambient 括号一致。

固定 a₂ 时，令 Fn=Tr L₀ⁿ。由平方根变分及 trace 循环性得到精确代表

$$
\delta F_n=\operatorname{Tr}(X_n\delta P),\qquad
X_n=-\frac n{2a_2}L_0^{n+2},\qquad [X_n,P]=0. \tag{13}
$$

实际 a₂ 随 Γ 变化时，另加

$$
\frac{nF_n}{2a_2}\,\delta a_2.
$$

在约束面上这项的 Hamilton 场只是负空间平移的常数倍，因此不破坏 q=Γ、平均 w=0，且对任意 translation-invariant trace 的括号贡献为零。故不能把 Γ 错当 Casimir，但其规范化导数有可控的真实含义。

用 [Mas–Ramos 的乘法/求逆 Adler 规则](https://arxiv.org/html/q-alg/9501009v2)，原一阶 U,w 因子对应 u=U/2+hw/8、v=U/2−hw/8 的相反自由场括号。以无权 integral 记号，P 的诱导 tensor 为标准 Adler map 的 1/8 倍（整体符号须和原 J 一致）。对满足 (13) 的代表，Adler 场为常数倍

$$
[(PX_n)_+,P].
$$

任何两个 Fn,Fm 的形式 trace 括号因此为零。这里需完整保留以下逻辑顺序：一阶因子诱导 Adler；(12) 证明 q-constraint 切向；公共 U gauge 证明平均 w=0 约化合法；最后 Dirac 修正项为零。只写“平方根 KP 已知可积”并不足够。

**正式对合结论。** 在上述正式泛函/弱 Poisson 约化范围，显式扩展、公共 U 规范不变性、(12) 的 q 切向性与 (13) 的 commuting 代表共同给 Fn 的原物理 Dirac 对合；a₂(Γ) 的额外导数仅给平移。它尚不是 actual Sobolev hierarchy flow、谱独立/完备性或作用角定理。该结论依赖实际做出的约化证明，而不是从 c≠0 分支直接延续。

## H₀ 守恒的系数检验与 common-b 项

在平均 w=0 谱层，有全 M 系数恒等式

$$
H_{\rm full}=-8\operatorname{Tr}D^2(P-I),
\qquad
H_{\rm full}=H_0+hM\int bq. \tag{14}
$$

这个等式与 common-U 共轭完全一致：P_b=e^σP₀e⁻σ、σₓ=b/2 时 a₃,b=a₃,0+a₂b，而 −8a₂b=hMqb。**Tr D²(P−I) 不像 Tr Φ(P) 那样 gauge 不变**，因为外面的 D²没有一起共轭。

这个恒等式可直接证明。令 $d_j=hw_j/8,b_j=U_j/2,v_j=b_j-d_j$。单因子展开为

$$
T_j=1+A_jD^{-1}+B_jD^{-2}+C_jD^{-3}+\cdots,
$$

$$
A_j=-2d_j,\quad B_j=-2v_jd_j+2d_{j,x},
\quad C_j=-2d_j(v_j^2-v_{j,x})+4v_jd_{j,x}-2d_{j,xx}.
$$

乘积的 a₃ 为单因子 C 和双、三因子交叉项。分部积分后，

$$
\operatorname{Tr}D^2(P-I)=\int\left[
\sum_j(-2d_jv_j^2+2v_jd_{j,x})
+\sum_{i>j}\{4d_id_j(v_i+v_j)-4d_id_{j,x}\}
-8\sum_{i>j>k}d_id_jd_k\right].
$$

用 Σd=0、v=b−d 与 Newton 恒等式
$\sum_{i>j>k}d_id_jd_k=\frac13\sum_jd_j^3$，化为

$$
\int\left[-2\sum_jd_jb_j^2-\frac23\sum_jd_j^3
+2\sum_jb_jd_{j,x}-4\sum_{i>j}d_id_{j,x}\right]. \tag{15}
$$

设 H 是 strict lower triangular 的全一矩阵。格点差分直接给
$R=hP_0(H+I/2)P_0$。于是周期积分下
$\int\sum_jw_j(Rw_x)_j=h\int\sum_{i>j}w_iw_{j,x}$。将此式及 b=U/2、d=hw/8 代入 (15)，恰得 (14) 的 −Hfull/8；所有系数、符号与原 β=h²/32 一致。这个推导适用于每个有限 M 和任意光滑周期函数。

在 b=0 截面 Hfull=H₀。a₁=0 给

$$
(PD^2)_+=(D^2P)_+=D^2+a_2.
$$

因此 (14) 的 Adler 场是 −[D²+a₂,P]，与 (13) 的 commuting 代表 trace 对合。a₂ 的 normalization 导数同样因 {Γ,H₀}=0 不贡献。加上 q 的 Dirac 修正及任意平移规范仍与 Fn 对合，所以 (14)–(15) 给 Fn 沿足够正则的实际物理 Hamilton 解的守恒证书。该证书没有构造这些解的实际存在时间。

这里 −[D²+a₂,P] 是该 ambient/截面代表的 Lax 场；任意物理 b 的 Dirac、公共-U 规范会再加一阶或零阶 commutator。不得未经核对把该截面式直接标作所有 b 闭合的 Pₜ。trace 守恒不受这些已证明的 commutator 修正影响。

## 有理平方根背后的二阶 pencil

一阶因子交换仍可把 P 写成 $Q^{-1}R$，Q,R monic order M。现在 a₁=0、a₂≠0 使 R−Q 的阶数恰为 M−2。设

$$
C=(R-Q)/a_2,\qquad N=C^{-1}Q=L_0^2.
$$

C 是 monic 的 M−2 阶微分算子。于是 c=0 分支的 scalar 问题准确是

$$
(Q-zC)\psi=0,\qquad z=\lambda^2,
\qquad \mu=1+a_2/z.
$$

两个因子标记为 z=0（Q）和 z=−a₂（R）。它是 (2,M−2) 型有理约束 KP pencil；M=2 时 C=I，所以 N 本身就是二阶微分算子。选择平均 U 的零模规范后，其 D 项均值为零，可用周期 scalar gauge 移去，得到实 Hill 算子。这提供一个确切的 KdV/Hill 逆谱桥梁，而不是仅把平方根命名为 KP。

此前 c≠0 的有限 Padé、Floquet 旗标与逆交换算法有望在 c=0 的泛型常参考场附近复用：要求所有交换 gap 非零、最小 Q,R 存在并保持、monodromy cyclic；固定物理分量均值仍只固定有序倍子比。这里还必须加入 q=Γ 的约束、公共 U gauge 和零模计数；本报告未完成该延拓的完整局部逆定理，更没有借此得到谱极大性。

## M=2 特殊退化与未闭合任务

M=2 时 p=(p,−p)、s=(s,−s)、R=0、ps=Γ≠0。由 (2)

$$
\chi=ps_x-sp_x=-2\Gamma p_x/p,
\quad b=-p_x/p+B(t).
$$

直接代回 (1) 得

$$
p_t=-B(t)p_x,\qquad s_t=-B(t)s_x.
$$

而 H₀=2hΓ∫Dlog|p|=0。该分支允许任意无零周期轮廓，但物理运动只是平移；不能用它替代一般的全场 Liouville 目标。M≥3 的 c=0,q=Γ≠0 相容场保留更多任意函数，是另一个可继续推进的真实约束分支。

M=2 的非零 Γ 图必有 p 无零且固定符号，所以不能同时要求其标量 x 均值为零；该图不在所有原分量均值均为零的叶中。使用这个分支时应选择实际非空的固定均值叶，不能从 c≠0 的零均值背景直接搬过来。

已严格核对：物理平均强制 Γ′=0、χ 的每项符号、Γ 非 Casimir、约束矩阵 (6)、Dirac 零模规范 (8)–(9)、advection intertwiner (12)、平方根变分 (13)、common-b 对 (14) 的符号影响，以及 M=2 的纯平移退化。

待完成/必须另行记录：非平凡独立作用量的计数；c=0 平方根有理谱的非线性逆、divisor/连接数据与极大性；同一实际时间及辅助流相空间。完整归档应保留上面的显式扩展和 conormal 切向证明，不能把它缩写成未经约化的 ambient 平方根定理。c=0 与 c≠0 两个非零扇区均不能覆盖 c=Γ=0 的兼容问题。本文不宣布一般物理场 Liouville 可积性已经完成。
