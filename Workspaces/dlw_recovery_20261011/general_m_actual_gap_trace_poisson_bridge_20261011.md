# 一般 M 的实际高频谱隙：原 trace/C_j 对合与固定有限组 order-zero Hamilton 流

2026-10-11。本稿把 [实际多通道高频谱隙引理](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md) 接到原物理 J。证明使用固定 spectral windows 中 actual normalized monodromy 的 characteristic polynomial，不使用 source-dependent holonomy 作新的不变量。所有 contour 和场的范数断言只针对固定有限个谱隙；不声称 n-uniform Hamilton 场界或任意 ℓ∞ 谱隙和的真实流。

前提是已核验的 [谱主稿 §§16–17](../../刘维尔可积性/research/spectral_independent_review_20261011.md)：原 free J=−offdiag(D)/16、actual normalized affine connection、全部实际 trace 彼此对合、actual trace 与每个原 centered C_j 对合，以及固定 trace Hamilton 场 H^s→H^s 的解析性。新短链已另由 all_m_holonomy_image_audit 代理手核；未运行脚本，未改共享记录。

## 1. 固定实际窗口；不变量来自 characteristic classes

固定一个高频标签 α=(ℓ,n)，其准确背景 λ_α 来自上述实际共振引理。选固定 λ-circle Γ_α 围绕 λ_α，以及固定 multiplier-circle C_α 围绕实际 normalized collision multiplier。它们不随源移动。在一个源邻域中，对每个 λ 在整个 λ-disk 内，C_α 内准确有两个 multipliers，其余 M−2 个排除；在 Γ_α 上，两分支 discriminant 非零，disk 内准确有两个 λ roots，计重数。前引统一 Riesz 引理保证这些选择可对所有高频存在；以下函数计算仍逐个固定 α 进行。

使用 centered λ=λ_original−B。令 N_λ∈SL_M 为原实际 normalized monodromy，取

\[
F_r(\lambda)=r^{-1}\operatorname{tr}N_\lambda^r,
\quad 1\le r\le M-1,
\qquad p(\mu,\lambda)=\det(\mu I-N_\lambda).
\tag{1}
\]

detN=1，Newton 恒等式说明 p 的全部 coefficients 是有限组 rF_r 的多项式；没有遗漏最后一个 determinant coefficient。定义 actual rank-two Riesz projector 和 cluster moments

\[
P_\alpha(\lambda)=\frac1{2\pi i}\oint_{C_\alpha}
(\mu I-N_\lambda)^{-1}\,d\mu,
\]
\[
T_k(\lambda)=\operatorname{tr}(P_\alpha N_\lambda^k)
=\frac1{2\pi i}\oint_{C_\alpha}\mu^k
\frac{\partial_\mu p}{p}\,d\mu,\quad k=1,2.
\tag{2}
\]

因此实际 cluster discriminant

\[
D_\alpha(\lambda)=2T_2(\lambda)-T_1(\lambda)^2
\tag{3}
\]

是 fixed λ 处 F₁,…,F_{M−1} 的局部 holomorphic function。它准确等于 cluster 两个 multipliers 之差的平方。式 (2) 包含 δP 的全部变化；不是固定 P 后只变 N 的近似。

定义 λ-root contour moments

\[
s_j=\frac1{2\pi i}\oint_{\Gamma_\alpha}\lambda^j
\frac{\partial_\lambda D_\alpha}{D_\alpha}\,d\lambda,
\quad j=1,2,
\qquad a_\alpha=s_1/2,\quad g_\alpha=s_2/2-a_\alpha^2.
\tag{4}
\]

a 是两个实际 λ roots 的平均，g 是半根差的平方。这与高频引理通过 K_n+hℓ(H)+ζ 定义的 g 完全相同；source holonomy hℓ(H) 只定位窗口，平移不影响 g。a 这里是 centered λ 内的 absolute center，未减 source holonomy。fixed windows 的标签唯一延续，所以 a,g 是实际 characteristic-data functions，frame similarity 不改变它们。

采用 raw monodromy 时，两个 cluster multipliers 同乘非零 analytic scalar，D 乘其平方；在 (4) 中该 scalar 的 logarithmic derivative 无 contour residue，因此 a,g 不变。本稿专门使用 normalized N，避免将 raw determinant/holonomy 的 translation 场额外混入 order-zero 断言。

## 2. 准确的 chain functional 与原梯度

令 A_{k,r}=∂T_k/∂F_r。由 (2) 对源微分并在 μ-circle 上分部积分，

\[
A_{k,r}(\lambda,z)
=-\frac{k}{2\pi i}\oint_{C_\alpha}\mu^{k-1}
\frac{\partial_{F_r}p}{p}\,d\mu,
\quad
dD_\alpha=\sum_{r=1}^{M-1}d_r(\lambda,z)\,dF_r(\lambda),
\]
\[
d_r=2A_{2,r}-2T_1A_{1,r}.
\tag{5}
\]

这些 coefficients 对源 holomorphic，在 contour 上局部 bounded，且是空间 x 无关的 scalar。没有要求 λ-window 内每个单独 multiplier 都简单。

对 (4) 作源微分，再对 λ-circle 分部积分，

\[
ds_j=-\frac{j}{2\pi i}\oint_{\Gamma_\alpha}\lambda^{j-1}
\frac{dD_\alpha}{D_\alpha}\,d\lambda.
\]

准确得到

\[
da_\alpha=-\frac1{4\pi i}\oint_{\Gamma_\alpha}
\frac{dD_\alpha}{D_\alpha}\,d\lambda,
\qquad
dg_\alpha=\frac1{2\pi i}\oint_{\Gamma_\alpha}
(a_\alpha-\lambda)\frac{dD_\alpha}{D_\alpha}\,d\lambda.
\tag{6}
\]

以 ordinary integral 配对取原 free-field gradient，故

\[
\nabla g_\alpha=
\sum_{r=1}^{M-1}\frac1{2\pi i}\oint_{\Gamma_\alpha}
(a_\alpha-\lambda)\frac{d_r(\lambda,z)}{D_\alpha(\lambda,z)}
\nabla F_r(\lambda,z)\,d\lambda,
\tag{7}
\]

而 ∇a 使用 coefficient −d_r/(2D)。这是实际 functional gradient，未用 formal resolvent/residue 替代它。所有 coefficient 的 state dependence 已由一阶 chain rule 包含；它们无 x-dependence，原 J 的 D_x 不对其产生额外项。

## 3. 实际 Poisson 对合，含 Re/Im 与全部原 C_j

谱主稿的实际 tensor 定理给任意 complex λ,μ、r,t

\[
\{F_r(\lambda),F_t(\mu)\}_{J}=0.
\tag{8}
\]

对任意固定 α,β，将 (7) 及 a 的对应式代入原 constant J。紧轮廓、局部 gradient bounds 和 spatial integral 的连续性允许 Fubini。每个 double-contour integrand 含 (8)，所以

\[
\{a_\alpha,a_\beta\}_J=
\{a_\alpha,g_\beta\}_J=
\{g_\alpha,g_\beta\}_J=0,
\quad
\{a_\alpha,F_t(\mu)\}_J=
\{g_\alpha,F_t(\mu)\}_J=0.
\tag{9}
\]

谱主稿 §17 的实际 Sobolev C¹ quasimomentum/C_j 桥另外证明 {F_r(λ),C_j}_J=0。对 (7) 同样积分，得到

\[
\boxed{\qquad
\{a_\alpha,C_j\}_J=\{g_\alpha,C_j\}_J=0
\qquad\text{对每个固定 }j.
\qquad}
\tag{10}
\]

它在该 actual bridge 的共同正则域成立：可保守地取源 H^{j+2}，全部 j 同时则取 smooth 周期物理场。没有在任意低 X₀ 源上定义无限 jets。

对实源 N(barλ)=overline(N(λ))。共轭 gap 是对应负窗口 (M−ℓ,−n) 的同一 class functional；(8) 对所有 complex 参数成立，故上述证明也给 {gα,overline(gβ)}=0，以及 a 的所有混合版本。因此所有实际 Re/Im gap、center、trace 泛函与全部可定义 centered C_j 在原实物理 J 上对合。这里不把正频率 g 当实值。

## 4. 每个固定谱隙/中心给同阶真实 Hamilton 场

回到原 affine traceless connection，用 Δ_first,d_first free 坐标（到 q,d 是同一保 J 的常数仿射变换）。谱主稿准确给

\[
W_{\lambda,r}=Y_\lambda N_\lambda^rY_\lambda^{-1},\quad
W'=[\mathsf L_\lambda,W],\quad W(L)=W(0),
\]
\[
(\nabla F_r)_{\Delta_j}=\operatorname{tr}(WH_j),\qquad
(\nabla F_r)_{d_j}=\operatorname{tr}(W[K_j(\lambda/S)-K_m(\lambda/S)]).
\tag{11}
\]

因 (1) 采用 1/r normalization，(11) 没有额外 r 因子。H_j、K_j−K_m 是 x-independent tracefree coefficient matrices；identity part 的 W 不贡献。

对固定 s≥1，全部 physical free components 在 H^s。ODE 与 H^s multiplier estimates 给源解析的 W∈H^{s+1}。在固定 compact λ-contours 上这些界 locally uniform。式 (7) 因此实际给

\[
\nabla g_\alpha,\nabla a_\alpha\in H^{s+1},\qquad
X_{g_\alpha}=J\nabla g_\alpha,\quad X_{a_\alpha}=J\nabla a_\alpha\in H^s,
\tag{12}
\]

且 H^s→H^s strong analytic。等价地，X_g 是 (7) 同一 scalar-weighted contour integral 的 actual X_F；(11) 中 x-derivative 使用 W′=[L,W] 消去，不含 source x-derivative。所有 mean components 保持，因为 J 是 D_x。真实 Hamiltonians 取 Re/Im 后保原 real form，Banach Picard 给局部实际 H^s auxiliary flows。固定有限组 α 使用这些场的共同 local window；(9) 给有限流交换。

此处不把 relative correction cα=aα−K_n−hℓ(H) 的 Hamilton 场也称 order zero。hℓ(H) 的低域解析性不提供这一 Hamilton 正则性；原 holonomy/determinant translation 项需要单独处理。任意外给 B(t) 只恢复 λ_original=B+λ：g 不变、原参数下 center 为 B+a，本文没有把 B 冻结成新的不变量。

intrinsic a,g 的 translation invariance 来自 monodromy class 随 basepoint 作相似变换，constant J 也 translation equivariant。因此 X_a,X_g 与空间平移交换。H¹ 的 analytic flow 对 translated initial state 作任意有限次 differentiations，给 smooth 源在同一个初始 H¹ 时间窗中的所有 Sobolev 正则性；无需因高阶 norm 大再次缩时间。由 (10)，smooth 轨迹保持全部原 centered C_j。

若另有原全 M strong coherent presentations 及 mixed 唯一性，则既有谱主稿 §17.4 的 finite order-zero flow transport 证明适用这些固定有限组 a/g 场：共同低阶窗口、(10)、平移等变性是所需分析输入。只有完成那一原 strong 图的重新 mixed 参数化，才可称其为同一弱辛域的内部 plots；本稿不从普通 H^s auxiliary flow 自动宣称 strong-domain membership。

## 5. 本证没有补出的无限闭包

实际 g-sequence 的 ℓ¹ 解析性说明对 d∈ℓ∞，Σdαgα 是低阶源上的 scalar analytic functional。它本身不能证明其原 J-gradient 属于 H^{s+1}，也不能证明 ΣdαX_gα 在 H^s 收敛；这里没有 n-uniform contour/field bound。故本稿只闭合固定有限组 actual spectral Hamiltonians。

实际有限高频 gap families 的独立性与本稿对合可同时使用；仍未得到完整 norming/action inverse、全部物理像的有限谱约束完备描述、或无穷 Hamiltonian 闭包等于共同微分 annihilator。一般物理全 M 的完整 Liouville 目标继续 OPEN。
