# 独审：有界 reciprocal-action 求和的外导数与实际邻域流

2026-10-11。完整读取 [根复核稿](root_m2_reciprocal_actions_and_bounded_hamiltonians_audit_20261011.md)，独立核其 §2 的 infinite bounded-coefficient summation、闭一形式、ℓ¹ Banach 解析性及整个低邻域的实际流。本稿以 §1 的有限 charge 身份为输入；该节的实际 contour、η chain rule 及系数由另一条独审负责。未运行 checks，未改根稿、共享日志或索引。

**结论：PASS。** 强截断足以控制这里的外导数；不需要乘子截断在算子范数中收敛。下面补出严格的导数公式、径向 primitive 及共同时间窗。

## 1. 低阶二形式的 operator-valued 解析性

令 E=(ℓ²)²，取一份 reduced complex 星形球 Bᵣ(0)，其 inverse chart F=𝓡⁻¹ 映到 X₀=L²₀×H¹₀。原 Ω 在 X₀ 上是连续 constant bilinear form。因 F 是 Banach holomorphic，

\[
\widetilde\Omega_W(U,V)=\Omega(DF_WU,DF_WV)
\]

是取值于连续 bilinear forms 之 Banach 空间的 holomorphic map。因此每个 DΩ̃_W[U] 是连续 bilinear form。一次缩球可取统一界 ‖Ω̃_W‖≤C。其导数并非额外弱导数假设，而是 Banach chart 的实际 Fréchet 导数。

给 d∈ℓ∞，置有界算子

\[
M_d(w,z)=L(-d_nw_n,d_nz_n)_n,
\qquad \|M_d\|\le L\|d\|_\infty,
\]

并定义 E* 值全纯一形式

\[
\alpha_d(W)[V]=\widetilde\Omega_W(M_dW,V).
\tag{S1}
\]

这是 operator-valued holomorphy 与连续 contraction 的复合，无需先证明有限求和在导数范数中收敛。

## 2. 固定切向的强截断足够证明 closed

令 dᴺ 保留 |n|≤N，其余置零。M_{dᴺ} 的算子范数统一有界；对每个固定 Y∈E，M_{dᴺ}Y→M_dY 强收敛。实际导数公式是

\[
D\alpha_d(W)[U][V]
=D\widetilde\Omega_W[U](M_dW,V)
+\widetilde\Omega_W(M_dU,V).
\tag{S2}
\]

在每个固定 W,U,V，两项分别由 M_{dᴺ}W 和 M_{dᴺ}U 的强收敛取极限；连续 bilinear forms 控制极限。交换 U,V 后，

\[
(d\alpha_d)_W(U,V)
=\lim_N(d\alpha_{d^N})_W(U,V)=0,
\tag{S3}
\]

因为有限身份 dH_{dᴺ}=α_{dᴺ} 已经使每个 α_{dᴺ} closed。该论证没有对所有单位 U 同时取极限，也没有把 strong operator convergence 误写成 operator-norm convergence。外二形式逐固定 U,V 为零，正是所需的 closed 身份。

## 3. 径向 primitive 的实际导数

定义

\[
H_d(W)=\int_0^1\alpha_d(tW)[W]dt.
\tag{S4}
\]

星形域保证整条径向 segment 在域内。Banach holomorphy、局部 Cauchy bounds 和紧的径向 segment 允许积分与 Fréchet 导数交换。于是

\[
DH_d(W)[U]
=\int_0^1\{D\alpha_d(tW)[tU][W]+\alpha_d(tW)[U]\}dt.
\]

由 (S3)，Dα(tW)[U][W]=Dα(tW)[W][U]。被积项变为

\[
\frac d{dt}\left[t\alpha_d(tW)[U]\right].
\]

t=0 的 boundary term 为零，因此

\[
\boxed{DH_d(W)=\alpha_d(W).}
\tag{S5}
\]

这也直接证明 H_d holomorphic。统一二形式界给

\[
|H_d(W)|\le \frac{CL}{2}\|d\|_\infty\|W\|^2.
\tag{S6}
\]

finite support 时，S5 与已知有限 charge 的微分相同，二者在 W=0 都为零，所以 S4 恰等于 ∑dₙAₙ。

## 4. 绝对求和及 ℓ¹ Banach holomorphy

对任意有限 F，选择 dₙ=bar Aₙ(W)/|Aₙ(W)|（零项任取零），得到

\[
\sum_{n\in F}|A_n(W)|\le \frac{CL}{2}\|W\|^2.
\]

故 A(W)∈ℓ¹，且 ‖A(W)‖₁≤CL‖W‖²/2。这个选择是在 complexified 图中的有限独立 coefficients，合法且不受真实反射条件限制。

一般 d∈ℓ∞ 时，径向 finite truncations 有显式误差界

\[
|H_d(W)-H_{d^N}(W)|
\le \frac{CL}{2}\|d\|_\infty\|Q_NW\|\|W\|\longrightarrow0.
\tag{S7}
\]

另一方面，A(W)∈ℓ¹ 已使 finite sums 绝对收敛到 ∑dₙAₙ(W)。因此 H_d=⟨d,A(W)⟩，每个 ℓ∞ dual 配对均 holomorphic，而 A 是 ℓ¹-locally bounded。这供应 norm-valued Banach holomorphy；不要求 ℓ¹ reflexive。

可直接核其最后一步。沿任一 complex line W+ζU，取闭 disc 上的统一 ℓ¹ 界 K。对所有 ‖d‖∞≤1 的 scalar H_d 运用同一个 Cauchy remainder bound，再以 ℓ¹ dual norm 取上确界，得到

\[
\left\|\frac{A(W+hU)-A(W)}h
-\frac{A(W+kU)-A(W)}k\right\|_1
\le C'K(|h|+|k|)/r_0^2
\]

（|h|,|k|<r₀/4）。因此差商在 ℓ¹ 中 Cauchy，极限在 ℓ¹ 中存在；高阶亦由 Cauchy bounds 得到。局部有界的 line holomorphy 给 E→ℓ¹ 的 Fréchet holomorphy。这里不存在把 ℓ¹* dual 的弱导数误放到 ℓ¹** 的缺口。

结论是 A:E→ℓ¹ 解析；若另需一个以 ℓ¹ action sequence 为源的集体解析图，必须另用 action invariant factorization。根稿 §2 没有混淆这两个源空间。

## 5. 整个邻域的一致实际时间窗

坐标场 M_dW 的 explicit flow 是

\[
\Gamma_t(w,z)=(e^{-Ld_nt}w_n,e^{Ld_nt}z_n)_n,
\quad \|\Gamma_tW\|\le e^{a|t|}\|W\|,
\quad a=L\|d\|_\infty.
\tag{S8}
\]

对任意 0<δ<r，取 T<log(r/δ)/a，即在整个 Bδ 上得到同一 |t|<T 的 complex Banach flow，其像留在 Bᵣ；d=0 时是 identity。它是全邻域上的 group germ，不是在一个 action level 的一点选择系数。

源上的实际场是 X_d=DF_{𝓡(x)}M_d𝓡(x)，并满足

\[
\Omega_x(X_d,V)=d(H_d\circ\mathcal R)_x[V].
\]

故这是原 Ω 的实际 low Hamilton 场。它是 X₀-valued Banach holomorphic，局部 Lipschitz；唯一性将 FΓ_t𝓡 与实际源 Hamilton flow 识别。不存在另设 NLS Poisson tensor 的步骤。

每个 hᴺ 都有相同的乘子界 eᵃ|ᵗ|，实际状态 inverse 又是在同一低域上保持全部 high intersections，因此光滑源也得到同一低窗口中的实际光滑轨道。d₋ₙ=bar dₙ 与此前确证的 κ 实结构使 real t 流保持真实物理源；相应 H_d 在真实片上实值。

该 argument 不自动证明旧 inherited strong 相域 S∞ 的不变性，不包含 unbounded hierarchy frequencies，也不把所有共同 action fibers 证明为普通流形。根稿 §3 保留了这些边界，其 scope 正确。
