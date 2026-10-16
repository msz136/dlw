# 全 M 端点实际 class 约束与 constant-gauge 饱和：独立审查

2026-10-11。独立读取 `general_m_physical_gauge_fredholm_and_spectral_constraints_20261011.md` §§4–6。只审查两个特殊谱点的实际约束、背景微分满秩及非线性 saturated-image 刻画，不审查后续 Hamilton 密度闭包。本次无 machine checks。

固定 M≥2、m=M−1、L>0、S=Mδ≠0、δ实，固定包含 uniform 背景的原 component-mean 叶；使用 centered 参数与既有 nonalias physical coefficient 图。结论为 PASS，具体理由如下。

## 1. 原物理实际 monodromy 的约束确实恒等

原 normalized affine connection

\[
L_{ii}(\lambda)=\lambda(d_i/S-1/M)+\Delta_i-\bar\Delta,
\quad L_{ij}(\lambda)=d_i(\lambda/S+\operatorname{sgn}(j-i))
\]

在 λ=S 为 upper triangular，在 λ=−S 为 lower triangular。固定 uniform mean 叶给 ⟨d_i⟩=δ、⟨Δ_i⟩=0，所以每个 diagonal 的空间积分为零。真实三角 ODE 的 monodromy diagonal 因而均为 1；矩阵可以有非零 strict part，并未要求等于 I。

周期 split/gauge 仅改变 endpoint frame。因此 ambient constant-slow coefficient triple 的 normalized N_λ 在物理图上准确满足

\[
\operatorname{tr}N_{S}^{r}=\operatorname{tr}N_{-S}^{r}=M,
\quad r=1,\ldots,m.
\tag{D1}
\]

常 internal GL_m similarity 保持这些值。a,b∈L²、Hconstant 时实际 N_λ 对 coefficient triple 解析，故 (D1) 定义 2m 个真实 ambient analytic class constraints Φ。若保留外给 B，特殊点按 centered λ=λ_original−B 取值，不添加 Γ_t=0。

## 2. Regular nilpotent 处 actual exponential trace 微分没有退化

背景 normalized connections J_± 分别与 2δ 乘全 strict-upper ones、−2δ 乘全 strict-lower ones 相似。其 m 次幂非零，M 次幂零，故为 regular nilpotent。N_±=e^{LJ_±} 也 cyclic unipotent。

任意 trace-free mean variation D=⟨δJ⟩ 的 actual Duhamel 给

\[
D\operatorname{tr}N^{r}
=rL\operatorname{tr}(e^{rLJ}D)
=\sum_{k=1}^{m}\frac{(rL)^{k+1}}{k!}\operatorname{tr}(J^kD).
\tag{D2}
\]

非 constant source variation 仍只通过空间均值进入 (D2)，因为背景 adjoint e^{rLJ} 是 constant。系数矩阵 C_{rk}=(rL)^{k+1}/k!，r,k=1,…,m，因子化为非零 row diagonal (rL)²、Vandermonde (r^{k−1}) 和非零 column diagonal L^{k−1}/k!。因此 detC≠0。

对 regular nilpotent J，characteristic 的 z^{M−j} coefficient 微分是 −tr(J^{j−1}D)，j=1,…,M；trace-free 给 j=1 项零，其余 m 项正是 (D2) 的 m 个 coordinates。故 r=1,…,m 的实际 exponential trace constraints 与全部 trace-free characteristic coefficient 首变分严格等价。不能在非 regular nilpotent（例如 J=0,M>1）照搬此结论；δ≠0 正是这里保证 regularity 的条件。

## 3. Trace normalization 项与 finite kernel

实际背景 A_{±S}=±δI_M+J_±。只需审查 finite constant variations (⟨δa⟩,⟨δb⟩,δH)，因为 §2 已说明全部 DΦ 只依赖这些有限量。记

\[
Q(z)=\det(zI_m-H),\quad R(z)=a\operatorname{adj}(zI_m-H)b,
\quad P_\pm(z)=(z\mp S)Q(z)-R(z),\quad t=\operatorname{tr}\delta H.
\]

Normalized connection variation为 δA−(t/M)I_M。背景 raw P_±=(z∓δ)^M，故 normalized characteristic 首变分为

\[
\delta P_\pm(\zeta\pm\delta)+t\zeta^m.
\tag{D3}
\]

由 §2，DΦ=0 当且仅当 (D3) 为零，即

\[
\boxed{\delta P_\pm(z)=-t(z\mp\delta)^m.}
\tag{D4}
\]

这个 trace-normalization 项不能漏去。两式相减给

\[
\delta Q(z)=-\frac t{2S}\{(z+\delta)^m-(z-\delta)^m\}.
\]

左侧最高项 z^{m−1} 的 coefficient为 −t；右侧为 −tmδ/S=−tm/M。因此 t=0，继而 δQ=δR=0。反向显然成立。

H₀ 的 simple eigenvalues ζ_j=−iδcot(πj/M) 及 nonzero realization residues a₀P_jb₀=−δ²csc²(πj/M) 给 finite kernel 的精确形状。先由 δQ=0 得 δH 在 H₀ eigenbasis 的 diagonal 为零，选择 offdiagonal X 使 δH=[H₀,X]。减去 gauge variation (a₀X,−Xb₀,[H₀,X]) 后 δH=0；再由 δR=0 在每个 simple pole 得 δa_jb_j+a_jδb_j=0。a_j,b_j 均非零，故剩余方向恰为 diagonal X_j=δa_j/a_j 的 gauge variation。

因此

\[
\ker D\Phi|_{\rm finite}=\text{constant GL}_m\text{ tangent},
\quad\dim\ker=m^2,\quad \operatorname{rank}D\Phi=2m.
\tag{D5}
\]

该 gauge tangent 没有 stabilizer：若 [H₀,X]=0 与 a₀X=0，则 simple H₀ 使 X diagonal，所有非零 a₀v_j 强制 X=0。故 (D5) 不只是维数猜测。

## 4. Nonlinear zero set 等于 physical gauge saturation

已有 physical state 图参数 y=(P₀a,P₀b)，finite graph values (mean a,mean b,H) 的背景 derivative全零。其 infinite tangent 为任意零均值 row/column L² pair。Finite ambient constants 空间 dim=2m+m²；选择一个 2m-dimensional constant complement T，补足 (D5) 的 m²-dimensional gauge tangent。

物理图加 small constant gauge 和 transverse constant directions 的 map

\[
\Psi(y,X,s)=\bigl(a(y)e^X,e^{-X}b(y),e^{-X}H(y)e^X\bigr)+T s
\]

在背景的 derivative 是完整 ambient Banach space 的有界直接和同构：mean-zero 部分、gauge finite tangent、T complement。真实解析 IFT 给 local full chart；并非只凭相同 codimension 得结论。

在此 chart，ΦΨ(y,X,0)=0 准确恒等。实际 analytic Hadamard factorization 为

\[
\Phi\Psi(y,X,s)=B(y,X,s)s,
\quad B=\int_0^1D_s(\Phi\Psi)(y,X,\theta s)d\theta.
\]

背景 B 为 DΦ 在 T 上的同构，缩小同一低域后仍可逆。因此 Φ=0 当且仅当 s=0，也即该 triple属于 physical coefficient graph 的 constant-GL_m saturation，且 small (y,e^X) 唯一。此证明在 L²×L²×Mat_m 的真实 low chart 内成立。

Physical pullback 的 Φ 恒等为零、原 physical Hamilton 场为零，与 ambient DΦ 满秩完全相容：前者只作用于 graph tangent，后者的 rank来自 transverse constants。不能由 ambient满秩误称原物理系统有 2m 个新的独立 conserved quantities。

## 5. 最终判断

保存主稿 §§4–6 通过。关键链为：真实三角 monodromy约束、regular-nilpotent exponential trace Vandermonde、normalized characteristic 的 t 项、finite simple-pole gauge kernel、完整 Banach chart和 actual Hadamard matrix。所有步骤保留 fixed uniform mean leaf、δ≠0、既有 NR 状态图和完整 constant H。

得到的是物理 coefficient-image saturation 的纯实际 class constraints 刻画。未得到 all-M action Cartesian inverse、Poisson canonical reduction、Hamilton gradient closed-span equality或 Liouville 最大性。
