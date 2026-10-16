# 一般 M 固定实际谱隙的 balanced 低域 Hamilton 流

2026-10-11。本稿补足 [实际 gap/trace Poisson 桥](general_m_actual_gap_trace_poisson_bridge_20261011.md) 未声称的低正则结论。它使用已审 [实际 trace/vector-AKNS 桥 §5.1](all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md)，受审版本 SHA256 `3780B13A597139691CA7660BF4CC5E817A5B08C588FA52441B7F81689992B1C0`，及 [实际高频 Riesz 引理](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md)，冻结 SHA256 `88652AEFD148F0DC803732AAE7A2038891B159B49C896F424978475209DA9C46`。全部是实际 ODE、原物理 J 与源图的分析；未运行检查脚本，未改上述来源或共享记录。

## 1. 适用域与结论

令 m=M−1、S=Mδ≠0。固定均匀背景满足已审 nonalias 条件

\[
p_j-p_\ell\notin(2\pi i/L)\mathbb Z\setminus\{0\},
\qquad p_\ell=-i\delta\cot(\pi\ell/M).
\tag{1}
\]

在固定 free component means 的物理叶，使用

\[
X_0=(L^2_0)^m_q\times(H^1_0)^m_d,
\qquad
J=-\frac1{16}\begin{pmatrix}0&D I_m\\D I_m&0\end{pmatrix}.
\tag{2}
\]

所有坐标表示扰动；背景常数不计入下标 0。取 actual coefficient inverse、完整 finite physical graph minor 和所选固定谱窗口共同存在的一个充分小 X₀ 邻域 U。B=Γ/(2c) 是保留的当前 spatial-constant 外给参数；谱标号为 centered λ=λ_original−B，不添加 B_t=0。

对任意固定高频标签 α，实际 absolute centered branch center aα 与 squared half-gap gα 均在 U 上 analytic；其原物理 Hamilton 场是 analytic U→X₀。每个真实 Re/Im 函数给真实局部 Banach Hamilton 流。固定有限组场有共同局部窗口、彼此交换并保持全部 actual trace classes；smooth 源在同一 X₀ 窗口保持 smooth，并守恒每个原 centered C_j。

此处没有断言 n-uniform 场界、无限组内部 strong plots 或一般 M 非线性谱完备性。

## 2. 轮廓组合直接给真正的 X₀ 场

采用原 determinant-normalized actual monodromy Nλ∈SL_M 与

\[
F_r(\lambda)=r^{-1}\operatorname{tr}N_\lambda^r,
\quad1\le r\le M-1.
\]

在固定 λ-circle Γα 与 fixed multiplier-circle 上，令 Dα 是 rank-two actual characteristic discriminant。前桥准确证明

\[
da_\alpha=-\frac1{4\pi i}\oint_{\Gamma_\alpha}
\frac{dD_\alpha}{D_\alpha}\,d\lambda,
\qquad
dg_\alpha=\frac1{2\pi i}\oint_{\Gamma_\alpha}
(a_\alpha-\lambda)\frac{dD_\alpha}{D_\alpha}\,d\lambda,
\]
\[
dD_\alpha=\sum_{r=1}^{M-1}d_{\alpha,r}(\lambda,x)\,dF_r(\lambda).
\tag{3}
\]

这里 x 表示整条物理源，不是 spatial variable；每个 dα,r 和 aα 是 spatial-constant scalar。Dα 在 Γα 上 nonzero，所有 coefficients jointly analytic in x,λ，并在该固定紧轮廓 locally bounded。actual trace 桥 §5.1 给 X_{F_r(λ)}:U→X₀ jointly analytic，固定 compact λ-set 上 locally uniform。

因此以下是 X₀-valued Bochner integrals：

\[
\widehat X_{a_\alpha}
=-\sum_{r=1}^{M-1}\frac1{4\pi i}
\oint_{\Gamma_\alpha}\frac{d_{\alpha,r}}{D_\alpha}
X_{F_r(\lambda)}\,d\lambda,
\]
\[
\widehat X_{g_\alpha}
=\sum_{r=1}^{M-1}\frac1{2\pi i}
\oint_{\Gamma_\alpha}(a_\alpha-\lambda)
\frac{d_{\alpha,r}}{D_\alpha}X_{F_r(\lambda)}\,d\lambda.
\tag{4}
\]

它们是 analytic U→X₀。式 (4) 使用已经证明的 low trace fields，不是从 H^s 场界推断 mixed 正则性。

## 3. 原 J-gradient 的低域识别

原 free Δ,d connection 在 L² 源上 affine，actual adjoint

\[
W_{\lambda,r}=Y_\lambda N_\lambda^rY_\lambda^{-1},
\qquad W'=[\mathsf L_\lambda,W],\quad W(L)=W(0)
\]

属于 H¹，analytic in source。对 fixed λ contour，ordinary-integral Duhamel gradients ∇F_r 是 W 与 fixed coefficient matrices 的收缩，故属于 H¹ 且有 locally uniform bounds。到 q,d 的常数仿射变换保原 J。式 (3) 因而给 actual ∇aα,∇gα∈(H¹)^{2m}，其 original J-gradients 是 analytic U→(L²₀)^{2m}。

在 smooth dense physical states，准确 trace identity 和 chain rule 已证明 J∇aα、J∇gα 等于 (4)。两侧都连续到较大的 (L²₀)^{2m}，所以相等延拓到全部 U。由于 (4) 属于 X₀，原 d velocity 实际属于 H¹。这个额外导数来自已经核验的 full finite graph cancellation；没有预先假设 rough frame derivative 沿任意方向保持 X₀。

故

\[
\boxed{X_{a_\alpha}=J\nabla a_\alpha=\widehat X_{a_\alpha},
\qquad X_{g_\alpha}=J\nabla g_\alpha=\widehat X_{g_\alpha}
\quad\text{in }X_0.}
\tag{5}
\]

## 4. 原弱辛结构、真实流和光滑保持

在 fixed-mean X₀ 上，原弱辛形式是

\[
\Omega(X,Y)=-16\int_0^L
\bigl[(D^{-1}X_q)\cdot Y_d+(D^{-1}X_d)\cdot Y_q\bigr]dx.
\tag{6}
\]

D⁻¹ 是 zero-mean 周期 primitive。式 (6) 连续、skew、weakly nondegenerate；其 inverse identification 是 (2)。由 (5)，Ω(X_a,Y)=da[Y]、Ω(X_g,Y)=dg[Y]，包括全部 rough Y∈X₀。实形式取 actual conjugate windows 的 Re/Im；不是把 complex 正频率 gap 默认为实数。

Analytic Banach ODE 定理给每个场的局部 flow。原实际 trace tensor identity 和 (3) 给 a/g/trace 的所有 pairwise Poisson brackets 为零；连续到 low U 后，固定有限场的真实 flows 交换、保持 actual trace classes。

这些 class functions 对 spatial translations invariant，原 J translation-equivariant，故场及唯一 flow 与 translations 交换。若 x∈C∞，ξ↦Tξx 是 C∞ 的 X₀-valued map；同一 low-window analytic flow 合成它仍 C∞，并等于 ξ↦TξΦ_t(x)。这给全部 spatial derivatives 在同一 X₀ 时间窗存在，即 smooth persistence，不因高阶 norm 重新缩时间。在 smooth 轨迹上，已经审过的 actual trace/C_j bridge 与 (3) 给 dC_j/dt=0，对每个固定 j 成立。

这仍是 ordinary balanced-low Hamilton flow。若要称它为先前 all-hierarchy coherent strong domain 的内部 plot，还需对该 presentation 证明真正的 mixed 重参数化；本稿不省略这一步。relative correction aα−K_n−hℓ(H) 的场也未由本证自动得到。
