# 一般 M 实际高频 gap 的频率加权 Hamilton 场序列

2026-10-11。本稿证明原物理场上的 normalized gap Hamilton 序列估计及真实 ℓ² 时间组合流。基础是已冻结 [actual high-frequency Riesz/gap 引理](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md)、[实际 gap/trace 对合桥](general_m_actual_gap_trace_poisson_bridge_20261011.md)、[fixed-gap balanced 流](general_m_fixed_gap_balanced_hamilton_flow_20261011.md) 与 [actual trace/vector-AKNS 桥 §5.1](all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md)。新估计另交 all_m_holonomy_image_audit 独审。未运行脚本，未改冻结稿、共享记录或旧证书。

## 1. 统一源域、准确标号与结论

沿用 m=M−1、S=Mδ≠0、任意固定实 nonalias 均匀背景，以及 fixed component means 叶的

\[
X_0=(L^2_0)^m_q\times(H^1_0)^m_d.
\]

取已经核验的实际 coefficient state 图、完整 finite physical graph 和全部高频 rank-two Riesz 图共同存在的一个充分小 complex X₀ 球 U；真实物理域是其实部分。索引 α=(ℓ,n)，1≤ℓ≤m、|n|≥N，λᵅ 是固定均匀背景的准确 actual collision parameter，而不是其 K_n+pℓ 近似。N 可以增大一次；所有源、全部这些 n 此后共用 U。

保留 centered λ=λ_original−B、B=Γ/(2c)，不添加 B_t=0。定义固定背景 scalar

\[
\omega(\lambda)=\frac{S^2-\lambda^2}{16S},
\qquad \omega_\alpha=\omega(\lambda^\alpha).
\tag{1}
\]

λᵅ 为纯虚且 λᵅ=2πin/L+pℓ+O(1/n)，故 ωᵅ≠0，|ωᵅ|≍n²。它不依赖当前源；对共轭标签 α*=(M−ℓ,−n)，ωᵅ*=overline(ωᵅ)。

实际 squared half-gap gα 的原物理 Hamilton 场满足

\[
\boxed{
x\longmapsto
Z(x)=\left(\frac{X_{g_\alpha}(x)}{\omega_\alpha}\right)_\alpha
\quad\text{是 strong analytic }U\longrightarrow\ell^2(X_0).
}
\tag{2}
\]

更准确地，下面证明同一源球上的局部估计

\[
\frac{\|X_{g_\alpha}(x)\|_{X_0}}{|\omega_\alpha|}
\le C\left(\|Q_\alpha(x)\|_{\mathcal A_r}+|n|^{-1}\right),
\quad (Q_\alpha)\in\ell^2(\mathcal A_r).
\tag{3}
\]

Qα 是已证明的 actual rank-two monodromy correction，A_r 是 fixed disk 上 analytic matrix functions 的 sup-norm Banach 空间。这里只估计 gap；absolute center 的 differential 在 free template 处有一阶项，不能套用同一二次抵消。

## 2. 固定 principal matrix 给 strip-uniform actual adjoint 界

在实际 vector coefficient frame 中，determinant-normalized connection 是

\[
\bar A_\lambda=\lambda J_*+Q(x),
\quad J_*=\operatorname{diag}(1,0_m)-I_M/M,
\]
\[
Q=\begin{pmatrix}0&a\\b&H\end{pmatrix}
-\frac{\operatorname{tr}H}{M}I_M.
\tag{4}
\]

J* 是固定 Hermitian matrix；a,b∈L²、H 是完整 spatial-constant matrix。对 |Reλ|≤R，用 e^{λJ*t} 作 interaction representation，actual Volterra/Gronwall 给

\[
\|Y_\lambda\|_{C^0}+\|Y_\lambda^{-1}\|_{C^0}
\le C\exp(CLR+C\sqrt L\,\|Q\|_2).
\tag{5}
\]

常数不依赖 Imλ。归一化 Nλ=Yλ(L)，Wλ,r=YλNλ^rYλ⁻¹；对有限 r=1,…,M−1，它们 C⁰ norm 也 uniform。完整 actual source endpoint frame 在 U 上 analytic、有 bounded inverse，只改变该统一常数。这里绝不使用原 raw χ 中含 λδP 的 rough perturbation 直接估计。

写 W blocks 为 [[c,e],[f,D]]，e 是 row、f 是 column。固定完整 H 时，auxiliary canonical a,b field 是

\[
Y_{F_r(\lambda)}=(e,-f,0),
\qquad
\|Y_{F_r(\lambda)}\|_{L^2_a\times L^2_b}\le C.
\tag{6}
\]

这是 actual monodromy variation 的 block gradient；1/r trace normalization 消去 r。auxiliary tensor只用于准确 field 比较，不假设它等于原物理 tensor。

## 3. 与 λ 无关的有限 graph reconstruction operator

令完整物理 coefficient graph 为 C(a,b,H)=0；其 finite constant-frame tangents 是

\[
\mathcal V_X=(aX,-Xb,[H,X]).
\]

已审 full-rank minor T_zX=P DC_z[V_X] 在 U 可逆，Π=(P₀a,P₀b) 的 actual source derivative 也可逆。对任意 ambient offdiagonal tangent y=(y_a,y_b,0)，定义

\[
\mathscr B_z y=(D\Pi_x)^{-1}P_0
\left[y+\mathcal V_{-T_z^{-1}P D\mathcal C_z[y]}\right]_{a,b},
\qquad z=\mathcal P(x).
\tag{7}
\]

这是 bounded linear L²-pair→X₀ operator，analytic in physical x，locally uniform；它与 λ 无关。任意 y 不必使完整 unused graph constraints 为零，故本稿不把 B_z y 自动称 Hamilton 场。对于 actual trace fields，已审准确身份及全部 graph constraints 则给

\[
X_{F_r(\lambda)}=\mathscr B_z
\bigl[\omega(\lambda)Y_{F_r(\lambda)}\bigr].
\tag{8}
\]

由 (5)–(8)，原 free fields 满足

\[
\|X_{F_r(\lambda)}\|_{X_0}\le C(1+|\lambda|^2).
\tag{9}
\]

有限 graph correction 已包含完整 H/frame 变化；这里没有在物理源空间另外冻结 H。

## 4. 实际 fixed contours 的常数可对全部高频统一

选 background actual λᵅ 为中心、共同足够小半径的 fixed λ-circles Γα。normalized multiplier circles 以 background collision multiplier 为中心，半径共同选一次。背景原 χ generator 在纯虚 λ 上 anti-Hermitian，因此 normalized collision multiplier modulus 1；各 n 的 circle 只由 unit-modulus phase 旋转。

nonalias 与 actual high-frequency separation 给该 rank-two cluster 对其余 multipliers 的共同正 margin。式 (5) 及 bounded endpoint frames 给 physical-source monodromy 的统一 perturbation 界；缩 U 一次即可保持全部 multiplier resolvent、characteristic p⁻¹ 及 finite Newton derivatives uniform。λ-circle 上的 two-multiplier discriminant Dα 有 uniform nonzero lower bound：背景在共同半径圆上的 eigenvalue difference近于 e^{Lζ}−1，γᵅ=1+O(n⁻²)，其 normalized scalar phase modulus 1；source perturbation 保留 margin。

gap/trace bridge 的 exact differential 可写

\[
dg_\alpha=\sum_{r=1}^{M-1}\frac1{2\pi i}
\oint_{\Gamma_\alpha}K_{\alpha,r}(\lambda,x)
\,dF_r(\lambda),
\]
\[
K_{\alpha,r}=(a_\alpha-\lambda)\frac{d_{\alpha,r}}{D_\alpha},
\qquad
\sup_{\alpha,\lambda\in\Gamma_\alpha,x\in U'}
|K_{\alpha,r}|\le C_{U'}.
\tag{10}
\]

U' 是任意较小源球；absolute center aα 仍在固定 λ-disk 内，所以 |aα−λ| bounded，不含 n。由 (9)–(10) 首先得到粗界 ||X_gα||X₀≤C(1+n²)，absolute centers 也有此粗界。下面利用 gap-specific cancellation 改进归一序列的求和性。

## 5. Free double-root 的二次结构控制 auxiliary gap field

在 complete H 的 source-adapted slow eigenbasis 与 grid λ=K_n+hℓ(H)+ζ 中，已经证明 actual rank-two compressed monodromy 可以写成

\[
B_\alpha(\zeta)=
\begin{pmatrix}e^{L\zeta}&0\\0&1\end{pmatrix}
+Q_\alpha(\zeta),
\qquad Q\in\ell^2(\mathcal A_r)
\tag{11}
\]

strong analytic，全部 n 共用源域。取更大 analytic disk 后的 fixed smaller-circle radius；N 与 U 可选使所有 Qα 在同一个 sufficiently small A_r ball 内。gap 是同一个 holomorphic contour functional G(Qα)。free double root 的准确一阶 discriminant 是

\[
D_1=2(e^{L\zeta}-1)(Q_{11}-Q_{22});
\]

root-moment contour因子给 DG(0)=0，故

\[
\|D\mathcal G(Q)\|_{\mathcal A_r^*}\le C\|Q\|_{\mathcal A_r}.
\tag{12}
\]

固定整个 H、只对 ambient a,b 微分时，grid hℓ(H)、slow basis 和 template 不变。actual ODE perturbation、uniform Riesz resolvent、compression intertwiners 和 larger-disk Cauchy estimates 给

\[
\|D_{a,b}Q_\alpha\|_{
\mathcal L(L^2_a\times L^2_b,\mathcal A_r)}\le C
\quad\text{uniform in }\alpha.
\tag{13}
\]

因此 actual auxiliary canonical gap field 满足

\[
Y_{g_\alpha}
=\sum_{r=1}^{M-1}\frac1{2\pi i}
\oint_{\Gamma_\alpha}K_{\alpha,r}Y_{F_r(\lambda)}\,d\lambda,
\qquad
\|Y_{g_\alpha}\|_{L^2_a\times L^2_b}
\le C\|Q_\alpha\|_{\mathcal A_r}.
\tag{14}
\]

λ-root gap is invariant under the hℓ(H) shift, so this auxiliary derivative agrees with the fixed-window class definition. “固定 H”只在计算 auxiliary derivative 时使用；原 physical field仍是 (8) 的完整 graph-corrected场。

## 6. 原 pole weight 的误差只有 1/n

在 λ=λᵅ+ζ∈Γα 上，准确 identity 给

\[
\frac{\omega(\lambda)}{\omega_\alpha}-1
=-\frac{\zeta(2\lambda^\alpha+\zeta)}{S^2-(\lambda^\alpha)^2}
=O(|n|^{-1}).
\tag{15}
\]

B_z 与 λ 无关，故由 (8)、(10)、(14) 得

\[
\frac{X_{g_\alpha}}{\omega_\alpha}
=\mathscr B_z\left(Y_{g_\alpha}+R_\alpha\right),
\]
\[
R_\alpha=
\sum_{r=1}^{M-1}\frac1{2\pi i}
\oint_{\Gamma_\alpha}K_{\alpha,r}
\left(\frac{\omega(\lambda)}{\omega_\alpha}-1\right)
Y_{F_r(\lambda)}\,d\lambda,
\qquad \|R_\alpha\|_2\le C/|n|.
\tag{16}
\]

这正是 (3)。有限 channel 数和 Σ|n|⁻²<∞ 给 normalized physical fields 的 locally bounded ℓ²(X₀) norm。每个 coordinate analytic；X₀ 是 Hilbert，finite-coordinate dual tests 稠密，locally bounded norm 使 weak holomorphy 延拓到全部 dual tests。Banach-valued Cauchy/Morera 因而给 (2) 的 strong analyticity，包括 source derivatives 的局部 ℓ² bounds。

B_zY_g 或 B_zR 分别不必是 Hamiltonian；式 (16) 的总和才由准确 original trace contour identity 得到 genuine X_g/ωᵅ。

## 7. 真实 ℓ² 时间组合及原 J 的识别

对固定时间 profile θ=(θα)∈ℓ² 定义；θ 与原 Casimir c 是不同参数：

\[
\mathcal H_\theta(x)=\sum_\alpha
\theta_\alpha\frac{g_\alpha(x)}{\omega_\alpha},
\qquad
X_\theta(x)=\sum_\alpha\theta_\alpha Z_\alpha(x).
\tag{17}
\]

g∈ℓ¹ strong analytic，θ∈ℓ²⊂ℓ∞、ω⁻¹ bounded，故 H_θ scalar analytic。式 (2) 和 Cauchy–Schwarz 给 field series 在 X₀ 绝对收敛，locally uniformly in x；它是 genuine analytic U→X₀ field，||X_θ||≤||θ||₂||Z||ℓ²(X₀)。联合 (x,θ) 也是 analytic。有限 truncations 的场与 source derivatives 在较小 complex source balls 上局部一致收敛。

原 weak Ω 已在 fixed-gap 稿证明。有限截断满足 dH_{θ,F}=Ω(X_{θ,F},·)。scalar analytic uniform convergence 给 differential 在 X₀* 中局部一致收敛，field convergence 和 Ω continuity 则给

\[
\boxed{d\mathcal H_\theta[Y]=\Omega(X_\theta,Y),\qquad Y\in X_0.}
\tag{18}
\]

这已是原 weak Hamilton identity。它也识别真正的原 J，而非额外选择一个新辛结构：在 fixed-mean 叶上，unique mean-zero gradient representative 是

\[
\widetilde\nabla\mathcal H_\theta
=-16(D^{-1}(X_\theta)_d,D^{-1}(X_\theta)_q)
\in(H^2_0)^m\times(H^1_0)^m,
\qquad J\widetilde\nabla\mathcal H_\theta=X_\theta.
\tag{19}
\]

它由各有限 original gradients 去掉 Casimir constants 后的 X₀ field limit得到。无需尚未证明的 infinite raw adjoint gradient estimate；均值常数对本叶与 J 均无贡献。

对 real sources，gα*=overline(gα)。取 θα*=overline(θα) 给 real H_θ 与 original real field；也可采用正频率 Re/Im basis。有限 truncations须保持共轭对。

## 8. 实际 local flow、光滑保持与守恒

Analytic Banach ODE 给 X_θ 在原 balanced X₀ 的 genuine local flow。对 bounded ℓ² coefficient balls，有共同 sufficiently small local time。profile truncations 的 analytic fields 与 derivatives 局部一致收敛，标准 ODE perturbation estimate 给有限 flows 到无限 flow 的局部一致 X₀ convergence。

每个 fixed gα 对 spatial translation invariant，原 J equivariant；无限 field sum仍 equivariant。对 smooth initial source，translation-orbit ξ↦Tξx 合成 analytic flow 与所有 ξ derivatives 都在同一个 X₀ 时间窗存在，故原轨迹 smooth。有限-flow source derivatives 的 Cauchy convergence 再沿这个 translation orbit给 finite-profile 轨迹在每个固定 Sobolev norm 的收敛。

有限 profiles保持全部 actual normalized trace classes。它们在 X₀ 连续，故无限 flows亦保持。对每个 centered C_j，smooth 轨迹的上述 Sobolev convergence 与 C_j 的有限-jet continuity给守恒；没有在 rough X₀ 上定义无限 jets。两个 ℓ² profiles θ,ϑ 的有限 Hamilton brackets为零，(18) 和 Ω continuity给 Ω(X_θ,X_ϑ)=0；constant closed Ω 与 weak nondegeneracy给 [X_θ,X_ϑ]=0，故真实局部 flows交换。

一个直接可用的有界 profile 推论是：对 d∈ℓ∞，取 θα=dα/(1+|n|)∈ℓ²，则 Σdαgα/[(1+|n|)ωᵅ] 也有 genuine X₀ Hamilton flow。这里额外 1/n 是明确权重，未被隐去。

## 9. 仍未解决的全 M 完备性

本证没有给无权 X_gα 的 n-uniform derivative bounds。原 pole factor ωᵅ≈n²，不能只由 g∈ℓ¹ 推断 ΣdαX_gα 对任意 d∈ℓ∞ 收敛。本证也未给只除 ωᵅ 后的全部 ℓ∞ profiles；ℓ²(X₀) 范数估计本身不够。更大的 profile 空间需要进一步 Riesz-basis/operator cancellation 或 action normalization。

同样，smooth persistence 不自动给旧 all-hierarchy coherent strong domain 的内部 plots；还需真正的 mixed reparameterization。此处没有 canonical norming brackets、完整 class/action inverse、普通 invariant fibers或 nonlinear maximal isotropy。一般 M 原物理场的完整 Liouville 目标继续 OPEN；本稿新增的是原 J 的真实无限 ℓ² 时间组合流。
