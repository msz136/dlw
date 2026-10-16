# 一般 M actual full monodromy 的基点 frame 与 slow holonomy 恢复

2026-10-11。本稿证明低正则、实际 Floquet 矩阵的正参数极限，不用 formal residue gradient。它接续 [一般 M physical holonomy state 图](all_m_physical_holonomy_state_inverse_20261011.md)，式 (1)–(16) 已经 [完整端点独审](all_m_full_framed_endpoint_holonomy_independent_audit_20261011.md) 逐式核验。所用原物理 Casimir S≠0、component means 及 B 规范参数已给；完整 normalized monodromy 取原 χ 分量的固定 frame。仅有 characteristic coefficients 时不能执行此恢复。

## 1. Constant-slow block 与周期 positive-resolvent

考虑实际周期系统
\[
y_x=A_\lambda y,\qquad
A_\lambda=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\quad a\in L^2(S^1;\mathbb C^{1\times m}),\ b\in L^2(S^1;\mathbb C^{m\times1}),
\quad H\in\operatorname{Mat}_m(\mathbb C).
\tag{1}
\]
以下界在任意给定 bounded a,b,H 球上一致，λ→+∞ 为真实正参数。实际 fundamental solution 与 monodromy T_A 在 L¹ coefficients 下由 Volterra 唯一得到。

R_λ=(D+λ)⁻¹ 的实际 periodic kernel 是 \(e^{-\lambda t}/(1-e^{-\lambda L})\)、0≤t<L，故 λL≥1 时
\[
\|R_\lambda\|_{2\to2}\le\lambda^{-1},\qquad
\|R_\lambda\|_{2\to\infty}\le C_L\lambda^{-1/2},\qquad
\|R_\lambda\|_{\infty\to\infty}\le\lambda^{-1}.
\tag{2}
\]
第二界是 kernel 的 L² norm 乘 Cauchy–Schwarz；没有要求 b 的 pointwise endpoint 值。

在 L∞ 的 O(λ⁻¹ᐟ²) 球上，vector Riccati 方程
\[
\eta=R_\lambda\{b+H\eta-\eta(a\eta)\}
\tag{3}
\]
为真实 contraction：H 项的 Lipschitz norm O(λ⁻¹)，quadratic 项≤Cλ⁻¹ᐟ²||a||₂·2||η||∞=O(λ⁻¹)。因此存在 unique small periodic η，对 a,b,H 解析，且
\[
\|\eta\|_\infty=O(\lambda^{-1/2}),\qquad
\|\eta\|_2=O(\lambda^{-1}),\qquad
\|a\eta\|_1+\|\eta a\|_1=O(\lambda^{-1}).
\tag{4}
\]
L² 界从 (3) 的第一 resolvent bound 再估计：||η(aη)||₂≤||a||₂||η||∞²。方程随后给 η_x∈L²，所以 η∈H¹、实际周期 endpoint η(0)=η(L) 已定义；其 H¹ norm不被误称 O(λ⁻¹)。

## 2. Actual fast projector、trace ratio 与 slow limit

实际 periodic T_η=[[1,0],[η,I]] 给 upper triangular connection
\[
T_\eta^{-1}A_\lambda T_\eta-T_\eta^{-1}T_\eta'
=\begin{pmatrix}\lambda+a\eta&a\\0&H-\eta a\end{pmatrix}.
\tag{5}
\]
令 Z_s′=(H−ηa)Z_s、Z_s(0)=I、N_s=Z_s(L)，则
\[
N_s=e^{LH}+O(\lambda^{-1}),\qquad
\mu=e^{\lambda L+\mathcal K_\lambda},\quad
\mathcal K_\lambda=\int_0^La\eta=O(\lambda^{-1}).
\tag{6}
\]
slow Duhamel bound 使用 ||ηa||₁=O(λ⁻¹)。upper monodromy 准确为
\[
U_\lambda=\begin{pmatrix}\mu&\mu J_\lambda\\0&N_s\end{pmatrix},
\quad
J_\lambda=\int_0^L e^{-\lambda t-\int_0^t a\eta}a(t)Z_s(t)dt
=O(\lambda^{-1/2}).
\tag{7}
\]
最后界用 exp(−λt) 的 L² norm 及 a∈L²；Z_s 与指数 correction 一致有界。这一步避免假定 a(0) 存在。

大正 λ 的 μ 是 simple fast multiplier，全部 slow multipliers 有界。令
\[
c_\lambda=J_\lambda(I-N_s/\mu)^{-1}=O(\lambda^{-1/2}),
\quad P_U=\begin{pmatrix}1&c_\lambda\\0&0\end{pmatrix}.
\tag{8}
\]
P_U 是 U 的实际 fast spectral projector：c(μI−N_s)=μJ 保证两个矩阵交换，P_U²=P_U。回到 (1) 的固定 frame，
\[
P_A=T_\eta(0)P_UT_\eta(0)^{-1}=E_{11}+O(\lambda^{-1/2}).
\tag{9}
\]
trT_A=μ+trN_s，大参数不为零；(7)、(8) 也给
\[
\boxed{\quad T_A/\operatorname{tr}T_A\longrightarrow E_{11}.
\quad}\tag{10}
\]
这是 actual matrix ratio，不能从 eigenvalues 的共轭类推出其固定 frame 极限。

设 R_A=(I−P_A)T_A。其 slow 22 block 精确为
\[
(R_A)_{22}=(I_m-\eta(0)c_\lambda)N_s
=e^{LH}+O(\lambda^{-1}).
\tag{11}
\]
首式来自 T_η(0)[[0,−cN_s],[0,N_s]]T_η(0)⁻¹；不能在 finite λ 直接写成 N_s。

normalized monodromy为
\[
N_A=e^{-\lambda L/M-\tau}T_A,
\qquad M=m+1,\quad \tau=(L/M)\operatorname{tr}H.
\tag{12}
\]
scalar 因子不改变 fast projector 或 (10) 的 ratio，且
\[
\lim_{\lambda\to+\infty}e^{\lambda L/M}
[(I-P_A)N_A]_{22}
=\exp\{L(H-\operatorname{tr}H\,I_m/M)\}.
\tag{13}
\]
H↦H−trH I/M 是可逆线性 map，inverse为 K↦K+trK I_m。若 H 背景满足 ad nonalias条件，matrix exponential在该背景的 derivative亦可逆。因此 (13) 的 actual slow matrix limit在这个局部范围准确恢复完整 H；未只取 trace 或 eigenvalues。此项是可选的 full-data holonomy 恢复，后续也可使用有限参数 λ=0 的 slow block。

## 3. 原 χ full normalized monodromy 的 endpoint 校准

由上述 physical state 图，在同一 nonalias 均匀邻域有 framed periodic internal gauge G^f(0)=G^f(L)=I。原 χ 与 (1) 系统的 endpoint frame 准确为
\[
T_z(0)=[d(0)/S,Z],\qquad
N_\chi(\lambda)=T_z(0)N_{A^f}(\lambda)T_z(0)^{-1}.
\tag{14}
\]
这里 \(T_z(0)^{-1}\) 的第一行为 1ᵀ；d∈H¹ 连续，所以这个实际基点值在 balanced low domain已定义。于是 (10) 给
\[
\boxed{\quad
\lim_{\lambda\to+\infty}\frac{N_\chi(\lambda)}{\operatorname{tr}N_\chi(\lambda)}
=\frac{d(0)1^T}{S}.
\quad}\tag{15}
\]
每列都等于 d(0)/S，故完整 fixed-frame actual Nχ直接恢复 d(0)，继而恢复整个 T_z(0)。不需先知道 q(0)、G(0) 或一个未规范的 constant gauge。

取该 T_z(0) 作**一个常数** conjugation，
\[
\widetilde N(\lambda)=T_z(0)^{-1}N_\chi(\lambda)T_z(0)
=N_{A^f}(\lambda)
\tag{16}
\]
就是 G^f(0)=I 的实际 normalized full block monodromy。其 endpoint 没有额外未知 G(0)。随后 (13) 可恢复 H^f，或把 finite slow block \(\widetilde N(0)_{22}\) 作为另一个 actual norming datum。

任意 B(t) 在当前空间截面给 centered λ=λ_original−B；scalar gauge e^{BL} 在 ratio (15) 中取消。normalized原data只需按这个 centered参数取值，不把 Γ_t=0 添加为假设。固定 S/component means 已给的物理标签不会从 monodromy ratio 自动消失。

## 4. 认证范围

本稿的 (2)–(16) 是真实 positive-parameter ODE 及矩阵极限，允许 a,b 仅 L²。asymptotic 在 bounded coefficient 球上统一，并无 formal PDO 交换。在原 balanced physical low域上，恢复的 endpoint与完整 holonomy保留 source frame。

本稿本身只给 endpoint/holonomy 恢复。后续 [实际 Fourier 核](general_m_framed_monodromy_fourier_kernel_20261011.md) §10 已证明 normalized 校准后 ℓ² 数据的真实 ambient 状态 inverse；[接合审稿](all_m_actual_full_framed_state_inverse_bridge_20261011.md) 保留两者各自的域并接回原物理场。本文没有把 (15) 的 frame 恢复称为 invariant action 坐标，更没有由它证明一般 M 的 Liouville 完备性。raw fixed-frame weighted high-frequency tails 与 class-only 缺失的 norming 信息仍须分开处理。
