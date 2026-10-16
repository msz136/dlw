# 一般 M actual trace 场与 vector AKNS 有限 frame 商：独立审查

2026-10-11。只读核验原物理 gauge 桥 §§1–4 与实际 holonomy/state 图中的归一化和有限图约束；不运行 checks，不修改主证明或共享 logs。

基础文件：

- [全 M rational physical gauge 桥](all_m_rational_physical_gauge_hamilton_bridge_20261011.md)。
- [实际 holonomy 与 coefficient/state 逆](all_m_physical_holonomy_state_inverse_20261011.md)。

以下结论作用于固定 component means、满足 (NR) 的足够小 uniform 物理邻域，m=M−1。采用当前外部 B 参数对应的 centered 谱标签；所有状态方向微分均保持该外部参数不变。

## 1. Trace-normalized moving frame 与实际 monodromy 因子

原实际周期 frame 是
\[
E=T_z\operatorname{diag}(1,G),\qquad G_x=VG-GH,
\quad \langle G\rangle=I_m.
\]
这里 det T_z 是 state-independent 非零常数。近 I 的 logdet G 为周期函数，并满足
\[
(\log\det G)'=\operatorname{tr}V-\operatorname{tr}H.
\]
因此
\[
\bar E=(\det G)^{-1/M}E
\]
具有 state-independent constant determinant。它将原 traceless connection 精确变为
\[
\bar A_\lambda=A_\lambda-
\frac{\lambda+\operatorname{tr}H}{M}I_M,
\qquad
A_\lambda=\begin{pmatrix}\lambda&a\\b&H\end{pmatrix},
\quad a=qG, b=G^{-1}r.
\tag{A1}
\]
不能用未作 trace normalization 的 E 直接替换 \bar E。

令 Y_A(0)=I、N_A(\mu)=Y_A(L,\mu)。由于 \bar E 周期，原 traceless actual monodromy满足
\[
N_\chi(\mu)=\bar E(0)
\left[e^{-L(\mu+\operatorname{tr}H)/M}N_A(\mu)\right]
\bar E(0)^{-1}.
\tag{A2}
\]
从而原 trace functional 的 coefficient 表达是
\[
F^\chi_{\mu,r}=\frac1r\operatorname{tr}N_\chi(\mu)^r
=c_r(\mu,H)\frac1r\operatorname{tr}N_A(\mu)^r,
\quad
c_r=e^{-rL(\mu+\operatorname{tr}H)/M}.
\tag{A3}
\]
若
\[
W_{A,\mu,r}=Y_A(\mu)N_A(\mu)^rY_A(\mu)^{-1},
\]
则原 periodic adjoint 转入 \bar E frame 后准确为 c_r W_A；其 trace-free 部分为 c_r W_A^0。归一化因子不能省略。

## 2. Pole 方程给 canonical offdiagonal 场与 finite correction

原 gauge 桥已给
\[
\delta L_\lambda=g'-[L_\lambda,g],\qquad
g=-\frac{\omega_\mu W^0_{\chi,\mu,r}}{\lambda-\mu}
+g_\infty(x),\qquad
\omega_\mu=\frac{S^2-\mu^2}{16S}.
\]
Moving frame 的正确 generator 是
\[
\bar g=\bar E^{-1}g\bar E-\bar E^{-1}\delta\bar E.
\]
它仍是 trace-free、periodic，且
\[
\bar g=-\frac{\omega_\mu c_rW^0_{A,\mu,r}}{\lambda-\mu}
+k(x),
\tag{A4}
\]
其中 k 不依赖 \lambda。设
\[
W_A=\begin{pmatrix}h&e\\f&D\end{pmatrix},
\qquad J_*=E_{00}-I_M/M.
\]
由 W_A'=[\bar A_\mu,W_A] 和
\bar A_\lambda-\bar A_\mu=(\lambda-\mu)J_*，pole 项的完整 contribution 为
\[
\left(-\frac{\omega_\mu c_rW_A^0}{\lambda-\mu}\right)'
-\left[\bar A_\lambda,
-\frac{\omega_\mu c_rW_A^0}{\lambda-\mu}\right]
=\omega_\mu c_r[J_*,W_A]
=\omega_\mu c_r\begin{pmatrix}0&e\\-f&0\end{pmatrix}.
\tag{A5}
\]
这一符号直接由 gauge 方程决定。

\delta\bar A 不含 \lambda 项，所以 [J_*,k]=0，即
k=diag(t,K)。Top diagonal 方程为
\[
t'=-\delta\operatorname{tr}H/M.
\]
H 和 \delta H spatialconstant；周期性强制
\delta trH=0、t constant。其余 diagonal 方程给
\[
\delta H=K'-[H,K].
\]
对每个非零 Fourier 模，
(ik-ad H)K_k=0；邻域内 (NR) 保持成立，故 K 也是 constant。写
\[
X=tI_m-K.
\]
所得实际 coefficient variation 是
\[
\boxed{
\delta a=\omega_\mu c_r e+aX,\qquad
\delta b=-\omega_\mu c_r f-Xb,\qquad
\delta H=[H,X].}
\tag{A6}
\]
Trace-free 条件 t+trK=0 仅确定 t=trX/M、K=tI_m-X，不限制 X 的 m² 个自由 entries。原 matrix H 并未冻结。

## 3. Canonical Hamilton 解释及 H Casimir 的范围

在 ambient coefficient space 使用普通积分配对下的 canonical bracket
\[
P_{\rm can}(\xi_a,\xi_b,\Xi_H)=(\xi_b,-\xi_a,0),
\tag{A7}
\]
其中 row/column 按 trace contraction 识别。完整 H 的全部 entries 都是此 ambient bracket 的 Casimirs。Actual variation formula 是
\[
\delta\left(\frac1r\operatorname{tr}N_A^r\right)
=\int_0^L\operatorname{tr}(W_A\delta A)\,dx.
\]
因此它的 a,b canonical 场为 (e,−f)。对于 (A3)，c_r 的 H derivative 被 (A7) 杀掉，准确得到
\[
P_{\rm can}\,dF^\chi_{\mu,r}
=c_r(e,-f,0).
\tag{A8}
\]
(A6) 表示 original actual trace 场等于
\omega_\mu P_can dF^\chi，加一个 constant GL_m orbit tangent。

这不能改写为“原物理 H 是 J 的 Casimir”：实际 physical graph 上已有
\[
\operatorname{tr}H=-\delta^{-1}\langle u\cdot v\rangle,
\]
一般随状态变化。这里证明的是 actual trace 场保持 H 的 conjugacy class；ambient H-Casimir 是 auxiliary canonical bracket 的约定。式 (A6) 也没有给出 entire original J 在 coefficient 图中的 canonical 表达。

## 4. Finite GL_m frame quotient 的实际范围

准确群作用是
\[
(a,b,H)\longmapsto(aQ,Q^{-1}b,Q^{-1}HQ),
\qquad Q\in GL_m.
\]
其 tangent 正是 (aX,−Xb,[H,X])。在 uniform 背景，V_0 simple 且 q_0P_jr_0≠0；若这一 tangent 为零，则 X 与 V_0 对易，且 observability 强制 X=0。因此该作用在邻域内 locally free。

Physical image 由 2m+m² 个 finite graph constraints C=0 定义。在 uniform，D C 作用于上述 orbit tangent 是 injective，选定 m²-component minor 后满秩在邻域内保持。故同一 physical graph 与每个附近 constant orbit 具有唯一交点。Canonical trace 场 (A8) 与 original actual trace 场通过 (A6) 在这一 finite frame 商中对应。

准确商的对象是 physical graph 的 GL_m saturation。该 saturation 在完整 coefficient ambient 中仍有 2m 个 finite constraints；不能宣称 entire ambient AKNS/GL_m quotient 已与 original physical neighborhood 相同。这里得到的是 finite frame correction 的真实、唯一消除，未处理 \lambda-dependent gauges，也未建立 spectral class/divisor inverse 或 action/norming chart。

## 5. Current B 与原谱标签

任意外给 spatialconstant B 下，raw block 是
\[
\begin{pmatrix}\lambda_{\rm original}&a\\b&H+BI_m\end{pmatrix}
=B I_M+A_{\lambda_{\rm original}-B}.
\]
Raw monodromy因而多一个 e^{BL}，但其 raw trace normalization也包含 MB；两个 B scalar factors精确消去。因此 (A2)–(A6) 采用
\mu=\mu_original-B、\lambda=\lambda_original-B，并继续是 original normalized actual trace family。

当前 B 固定仅表示对 original free state 施加 J 时保持外部参数不变。B(t) 可以由原 PDE 外给；本论证不能推导 B_t=0，也没有把外给 B_t correction 当成这些 trace Hamilton directions。\Gamma 未被新增为守恒量。

## 6. Balanced low 场的稳妥延伸方式

Moving-frame 计算首先在 smooth physical states/variations上成立。若欲报告 balanced X_0 上的解析延伸，应使用 finite graph minor，而不要先假定 rough actual trace tangent 的 \delta\bar E 已定义。

令 O_X=(aX,−Xb,[H,X])，V_can=\omega_\mu c_r(e,−f,0)，固定上述满秩 minor。实际 fundamental matrix在 L² vector coefficients上解析，其 W_A 属于 H¹；所以 V_can 在 low coefficient ambient上解析。定义
\[
X=-\big[\operatorname{minor}(D C\,O_\bullet)\big]^{-1}
\operatorname{minor}(D C\,V_{\rm can}).
\tag{A9}
\]
Smooth 原场的 (A6) 和满秩唯一性证明其 correction 恰为 (A9)。再以 smooth physical states 的密度和所有 finite constraints 的低域解析性，得到
D C(V_can+O_X)=0 的完整约束，包含未选入 minor 的余 2m 项。于是由 physical state inverse 的 tangent inverse 拉回，可定义 balanced low 域的解析原场延伸。该论证未要求 a,b 的点迹，也没有将 fixed coefficient frame 与未标定的谱 norming 数据混同。

## 7. 新主稿逐式审结与 actual low identification

已完整读回 [actual trace/vector AKNS 主证明](all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md) §§1–7，包括最新 §5.1 的 (21)–(24)；另读 [实际 framed endpoint calibration](all_m_actual_framed_endpoint_recovery_20261011.md) (1)–(16)。主稿用 \bar W 的 normalized e,f；因此其 (18) 中写 \omega_\mu(e,−f,0)，与本审查把 c_r 单独写出的 (A6) 完全一致。

主稿 §5.1 对 rough actual Poisson field 的识别成立。核对原 [谱主稿 §16.1–16.2](../../刘维尔可积性/research/spectral_independent_review_20261011.md) (103)–(106)，有准确公式
\[
\Delta_j=q_j+S+
\sum_{\ell<m}\operatorname{sgn}(\ell-j)d_\ell.
\tag{A10}
\]
这里和式仅取前 m 个 free 分量，混合矩阵 A 是 skew；仿射变换保留原普通积分 offdiagonal J，因为 A+A^T=0。不得把 (A10) 误读为另包含消去的 d_m 的 full-M 和。

原 normalized L_\mu 是 (\Delta_first,d_first) 的严格 affine 函数，实际 Duhamel 梯度正是
\[
(F_{\mu,r})_{\Delta_j}=\operatorname{tr}(W H_j),\qquad
(F_{\mu,r})_{d_j}
=\operatorname{tr}\{W[K_j(\mu/S)-K_m(\mu/S)]\}.
\tag{A11}
\]
Low source 给 L_\mu\in L²，故原实际 W\in H¹；(A11) 的 fixed-matrix contractions 均属于 H¹，关于 balanced low source 连续解析。Constant affine gradient change 保持这一预算。施加原 J 后，actual field 先确定为连续解析的 L²×L² 值映射。

(A9) 与主稿 (22) 则构造 X_0 值解析场，其 projected coefficient push 通过 (D\Pi)^{-1} 定义。Smooth 源上它与 original field 一致；两边均连续到 L²×L²，所以 density 给全部 low 源上的实际相等。因 constructed 场的第二分量在 H¹，actual J-gradient 的第二分量由此也确实在 H¹。该结论并未预先假定 actual J-gradient 已是 X_0 值映射，因而不存在正则性循环。

Analytic X_0 值场的 Banach Picard 给真正局部流；主稿保持每个固定 finite r、compact \mu 的预算，没有宣称任意 r 一致界或 unbounded hierarchy 的共同流窗口。Finite quotient 与余 2m constraints、原完整 \chi frame、current B 及外给 \Gamma 的范围均表述准确。

最终审结：**PASS**。归一化 scalar factor、moving frame、actual trace family 的 canonical offdiagonal 比较、完整 H 的 finite similarity correction、实际 finite physical quotient及最新 balanced-low actual flow 均已核清。式 (21) 的两个单独 `\` 是 TeX 空格而不是换行，数学内容无歧义；这只是排版选择。本文件不声称一般 M action chart、Hamilton closure 或 Liouville 最大性已完成。
