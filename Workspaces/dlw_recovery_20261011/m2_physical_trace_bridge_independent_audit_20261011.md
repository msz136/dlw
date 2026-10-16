# M=2 原物理 trace 场、规范截面与 weighted phase kernel 独立审稿

2026-10-11。独立读取 [direct 稿 §§1–3](m2_physical_trace_poisson_closure_proof_20261011.md)、[AKNS actual 状态图 §§4.3–4.5](akns_physical_state_inverse_bridge_20261011.md)，并从原 physical tensor、actual Duhamel gradient 和三条 adjoint 方程手算全部字段。没有运行或重复其 15/16-check 脚本。这里的闭包定理是 M=2 的完整一般函数局部状态图上的 ambient 切向定理；不代替全 M 目标或原 strong 内部 tangent 的认证。

## 1. Fixed-λ gradient 与发现的印出公式遗漏

约定 S=2δ≠0，q=u−S，V=−2uv/S，t=δ²−v²，A=t/S²，Bv=−2v(1+u/S)/S，r=t(S+u)/S²−v_x/S。原 source tensor 为 J=−offdiag(D)/16。令 actual split adjoint 的 trace-zero 部分为 W=[[α,E],[F,−α]]，其周期方程是

\[
\alpha_x=qF-rE,\qquad
E_x=(\lambda-V)E-2q\alpha,\qquad
F_x=2r\alpha-(\lambda-V)F.
\]

原 traceless connection 是 ((λ−V)/2)H+qE₁₂+rE₂₁。固定原 centered λ 的 Duhamel gradient，积分分部后恰为

\[
g_u=F+AE+2v\alpha/S,
\qquad g_v=(\lambda-2v)E/S+2\alpha.
\]

这是 fixed-original-parameter 梯度，已经包括 AKNS holonomy shift ζ=λ−η 的变分；不能把 ζ 固定后算出的梯度直接当它。

首次实际读 direct 稿时，印出的 Eq(7) 的 u_t 少了 −(λ−2v)(λ−V)E/(16S)。原正确等式必须是

\[
u_t=-qF/8+
\left[\frac{A(S+u)}8-\frac{(\lambda-2v)(\lambda-V)}{16S}\right]E
+\frac{(\lambda-2v)q\alpha}{8S}.
\]

直接将 E_x 代入 −Dg_v/16 就得到该负项；未需要新脚本。已立即向 root 和作者给出精确修正。其后 Eq(10)–(11) 的正确 Poisson bridge 不受这份排印遗漏影响；下文用原 gradients 重新证明，不能以错误 Eq(7) 作为依赖。

## 2. 两个物理分量与 nonlocal primitive 的完整手算

记

\[
\omega_\lambda=\frac{S^2-\lambda^2}{16S},\quad
J_v=\lambda v-v^2-\delta^2,
\quad
H=\frac F8-\frac{(\lambda-2v)\alpha}{8S}
+\frac{J_vE}{8S^2}.
\]

从 −Dg_v/16 收集 E、F、α 系数，严格得

\[
u_t=\omega_\lambda E-qH.
\]

另一方面，重新简化 g_u 的 derivative 得

\[
(g_u)_x=\frac{4t}{S}\alpha-(\lambda+2v)F
+\frac{t(\lambda-2v)}{S^2}E,
\]

所以

\[
16v_t=-4t\alpha/S+(\lambda+2v)F-t(\lambda-2v)E/S^2.
\]

这确实无 u 或任何 source derivatives，是另一个分量正则性的关键。

逐系数验证 H_x=V_t：把三条 adjoint 方程代入 8H_x 后，F coefficient 是 −λu/S−2v，α coefficient 是 (4δ²u−4Sv²−2λvq)/S²，E coefficient 是

\[
\frac{(\lambda-2v)t(S+u)}{S^3}
+\frac{J_v(\lambda-V)}{S^2}.
\]

由 V_t=(vg_{v,x}+ug_{u,x})/(8S)，其三个 coefficients 与以上一致。E 项差可因子成 t(S+u)S⁻³[−V−2uv/S]，恰为零。于是 H_x=V_t，η_t=⟨V_t⟩=0，且 mean-zero primitive 的真实速度为 θ_t=H−⟨H⟩。

再按 r_t=A u_t+(Bv−D/S)v_t 分别收集 α、F、E coefficients。结果是

\[
r_t=rH-\omega_\lambda F.
\]

其中 α coefficient为 −r(λ−2v)/(8S)，F coefficient为 r/8−ω_λ，E coefficient为 rJ_v/(8S²)。E coefficient 的最后抵消只用 S²=4δ²、q=u−S、V=−2uv/S；没有 q,u,r 的非零假设。

因此 actual a=e^θq、b=e^{-θ}r 满足

\[
\boxed{\quad
a_t=\omega_\lambda e^\theta E-\langle H\rangle a,
\qquad
b_t=-\omega_\lambda e^{-\theta}F+\langle H\rangle b.
\quad}
\]

direct 稿 R₀ 正是 8SH，所以它的 gauge coefficient ⟨R₀⟩/(8S)=⟨H⟩。所有符号与其 Eq(10)–(11) 一致。

## 3. Half-parameter、NLS scaling 与真正保 mixed 空间的流

本稿 ζ=λ−η 是 AKNS connection 的 full coefficient parameter；实际 connection 是 ζH/2+aE+bF。若另一稿用 ζ_half H，则 ζ_half=(λ−η)/2。period-one dimensionless NLS z=iLζ/2，不能把这三者混用。

令 T_ζ 为 fixed ζ actual AKNS trace。在 x 的普通积分下 gradients为 (e^{-θ}F,e^θE)，auxiliary J₀=[[0,1],[−1,0]] 给 Y_ζ=(e^θE,−e^{-θ}F)。原 physical push 恰为

\[
D(a,b)X_{F_\lambda}=\omega_\lambda Y_{\lambda-\eta}-\langle H\rangle Q,
\qquad Q=(a,-b).
\]

fixed balancing 与 t=x/L 给 ϕ₁=−iLa(Lt)/2、ϕ₂=2iLb(Lt)。独立计算普通 integral gradients 与 velocities，published standard NLS 场表达在 a,b 中是 (i/L)Y_ζ。所以 physical first coefficient 相对于 X_NLS T 为 (L/i)ω_λ=−iLω_λ=iL(λ²−S²)/(16S)。没有丢常数 i,L 或 λ 的二分之一。

更强的真实流预算也由上述 fields直接证明。对 E_N=H^N_0(u)×H^{N+1}_0(v)，N≥0，原 affine rank-one connection 为 H^N 系数（N=0 为 L²），actual periodic W∈H^{N+1} 且解析依源。u_t=ωE−qH 属 H^N，v_t 的三个系数仅依 v 与 W，属 H^{N+1}。N=0 用 H¹ multiplication 在 L² 上的作用。因此每个 fixed λ 的 actual trace 场在最低 mixed L²×H¹ 及所有 E_N 是 analytic E_N→E_N，源均值由原 divergence 保持。Banach Picard 给 actual local mixed flows；同一低域上的 high 持久性不只是一项 balanced Hs 结论。

## 4. Eq(15) 的 representative 与状态依赖 gauge 微分

记 Birkhoff chart 为 ℬ，G_B=(−w_n,z_n)_n 是 constant diagonal gauge 的谱速度。fixed θ₀ section 上的 projection 为 ΠV=V−dθ₀(V)G_B/i。θ₀=(2i)⁻¹log(w₀/z₀)，dθ₀(G_B)=i，所以这是每个 weighted h^N 拓扑的 continuous projection。

实际 reduced map R 并非仅将 physical potentials 的 gauge derivative 删除。它先给 a,b，再施依状态而定的 H_{τ(a,b)} constant gauge，最后取 ℬ 的非中央坐标。设 c=⟨H⟩；在选定 section representative 上，gauge equivariance使

\[
DRX_F=\omega_\lambda Y_B+(\delta\tau-c)G_B,
\]

其中 Y_B 是 ℬ_*Y_ζ 在该新 representative 的值。θ₀ 沿 R 恒定，故

\[
0=\omega_\lambda d\theta_0(Y_B)+(\delta\tau-c)i,
\quad
\delta\tau-c=-\omega_\lambda d\theta_0(Y_B)/i.
\]

代回后正是

\[
\boxed{DRX_{F_\lambda}=\omega_\lambda\Pi Y_B.}
\]

因此 direct Eq(15) 正确，但“没有 additional state-dependent gauge derivative”的准确意思是该 derivative 已由 projection 严格吸收，而非 τ 的 derivative 本身为零。右端 Y 必须解释成 KLTZ 推前并在同一 section representative 求值，不能拿旧 representative 的 raw (a,b) vector 与非中央 sequence 直接比较。

这只是完整 actual trace family 的具体向量场身份；全 physical pushed Poisson tensor仍为二阶/nonlocal，未与 canonical NLS tensor相等。

## 5. Weighted Cartesian 的 closed phase kernel：实际 ambient 证明

以下固定满足共同小图条件的 smooth 状态，所有非中央 I_n=w_nz_n≠0。对每个 N，定义 K_phase 为 weighted noncentral Cartesian tangent 中全部 dI_n 的共同 kernel。每对条件是 z_nδw_n+w_nδz_n=0，所以每对 tangent 恰为 scalar 倍 (w_n,−z_n)。在 h^N² 中 finite truncations 收敛，在所有 seminorm 下也收敛，因而 standard single-action fields X_NLS I_n 的 closed linear span正是 K_phase。

必须用 full ambient standard action field 再投影：n≠0 的 X_NLS I_n 只转第 n 对，中央 angle速度为零，所以 Π 作用后就是相同 single-coordinate vector。不能把约束 I₀=ρ(I_neq0) 的 reduced derivative 与这一 full standard field混淆。

这些 single-action vectors也在原 physical trace span中。对 fixed noncentral contour Γ_n，取 λ(z)=η−2iz/L。ω_λ 的两个零点是原 λ=±S，即中央 actual pair z_±；足够小共同域的 Γ_n 不经过它们。R(z) 也在 canonical contour 非零，因此 action gradient与上节 exact push 给

\[
\Pi X_{\rm NLS}I_n
=-\frac{i}{\pi L}\oint_{\Gamma_n}
\frac{DRX_{F_{\eta-2iz/L}}}{R(z)\omega_{\eta-2iz/L}}\,dz.
\]

这里 source 状态固定，η、R、ω 都是 fixed point coefficients。compact contour 上 actual X_F 为 EN-continuous，DR 有界；Riemann sums属于有限 complex linear combinations 的原 fixed-parameter physical trace fields，极限在每个 EN/hN 中存在。故 single-action vector确属它们的 closed span。这是切向闭包论证，不需要把 inverse weight 的依状态参数另造为全域 Hamiltonian functional。

反向，所有 physical traces与全部 actual In 对合，故 DRX_F∈K_phase。由 DR 的 analytic state inverse 与连续 derivative inverse，得到在每个 weighted level及 smooth Fréchet topology上的 exact ambient equality

\[
\overline{\operatorname{span}_{\mathbb C}\{X_{F_\lambda}:\lambda\in\mathbb C\}}
=\bigcap_{n\ne0}\ker dI_n
\]

（等式两边已回拉至原物理 source tangent）。这是 regular fixed state 的拓扑等式，不作逐频 uniform nonzero lower bound。每个 phase coefficient可以随 n 增大，finite truncations只需 tangent sequence属于相应 weighted space。

物理 real version须保留 induced anti-involution。a,b 为实，Δ(−bar z)=barΔ(z)，canonical branch给 I_n=bar I_{−n}；故共同 phase kernel对 real conjugation invariant。原 physical trace family也按 λ↔barλ closed。将 finite complex sums与其共轭平均，得到真实 Re/Im trace fields的 real closed span等于 real phase kernel。不能将非中央 coordinates的 real type替换为 focusing或defocusing标准实型。

## 6. 认证的边界

corrected gradient/fields、两 component exact push、half-parameter及NLS scaling、Eq(15) 的真实 gauge projection通过。上文已给无 canonical-Poisson shortcut 的 weighted ambient trace-span=common action phase-kernel 证明。

存在所有 noncentralactions非零的同一真实 strong 状态，须用另稿 actual action Hessian与同一 Hilbert strong parameter ball 的 Baire，而不是任意 ambient initial state猜测。由上述 ambient kernel可以进一步审查原 weak symplectic Ω 的 maximality，但 strong内部 diffeological tangents、velocity lift 和 admissible covectors仍须另外匹配。特别不将这份 ambient pointwise equality直接说成所有 strong plots形成Hilbert流形，不把无穷个 I_n趋零的 fibers自动说成有一份全序列角坐标的Banach submanifold。

本次审查发现一项印出字段遗漏并给出精确修正，没有新 machine checks；以前独立脚本 145 个断言计数未变，也未把其他代理新证书计入该数。

## 7. 修正文稿与后续 physical action-span 的末审

已再次 actual read direct 稿新 §§4–8。Eq(7) 当前已补入 −(λ−2v)(λ−V)E/(16S)，与上文从原 Dg_v 手算的正确字段相同。故这项印出遗漏已解决；本审没有改作者源文件。

源稿 §§4.1–4.3 的 ambient trace闭包与 §5 realification分别和上文独证一致，尤其 full standard action先生成再投影，避免以 reduced action derivative取代projected full Hamilton field。现加入的 §4.4 不再只从 trace-span推 actual physical action-span，而用连续 transpose 补上必要一步；该步独核通过。

在 fixed smooth state，full KLTZ derivative是 L²²→h⁰² 的有界同构，保 published标准 constant tensors。故其 canonical identity严格给

\[
(D\mathcal B)^*=J_{\rm pot}^{-1}(D\mathcal B)^{-1}J_{\rm seq}.
\]

common-domain high inverse derivative bounded h^N→H^N，两个标准 tensors零阶，所以这个 bilinear transpose也保所有 positive orders。这里只证明已知谱图的 transpose regularity；不把它代入成physicaltensoridentity。

中央 angle规范微分是 bounded diagonal scaling加 smooth gaugevector乘一个 supported-central covector，transpose亦保每个h^N。zero-central insertion保每个阶。最后 physical potential transpose精确为

\[
\Lambda^*=(M^*-c^TKj^T)E_\theta,
\qquad M^*=\begin{pmatrix}1&A\\0&Bv+D/S\end{pmatrix},
\]

因为 K*=-K。它最多损一阶，原 J另损一阶。因此 JDR* : s²→E∞ 是 continuous。ordinary balanced H^N source seminorm 可由 input h^{N+2}控制；若使用本审 §3 的 mixed EN=HN×HN+1 seminorm，保守 input h^{N+3}足够。固定有限 derivative loss不妨碍smooth Fréchet continuity，但不应将这一 transpose结论说成在任意 fixed low Hs 无损。

actual fixed-original-λ trace在 reduced coordinates 是

\[
F_\lambda=t(\lambda-\widetilde\eta(J),\rho(J),J),
\qquad J=(I_n)_{n\ne0}.
\]

其 ℓ¹ action derivative coefficients

\[
\beta_n=t_{I_n}+\rho_{J_n}t_{I_0}-t_\zeta\widetilde\eta_{J_n}
\]

确为 ℓ∞，因为 t、ρ、ηtilde对ℓ¹ analytic；中央constraint和movingcenter两项均有保留。Cartesian covector c=(β_nz_n,β_nw_n)属s²，其finite truncations在所有hN收敛。连续 JDR*把这个真正 covector convergence变成

\[
X_{F_\lambda}=\lim_k\sum_{0<|n|\le k}\beta_nX_{I_n}^{\rm physical}
\]

的 smooth velocity convergence。反向 physical action contour公式由零winding已消η项，Riemannsums给 XphysIn处于closed trace-span。因此 source新 (35)–(38) 的 actualphysicalaction-span、actualtrace-span与共同phasekernel相等。此推理完全保留原 J与Λ*，没有把 reducedcoordinates宣为canonical。

## 8. 原形式的最大各向同性与内部切向的准确范围

source新 §6 ambient maximality亦通过。原均值零空间上的 continuous form可取 J⁻¹=−16offdiag(K)，其对smooth topology continuous。actual trace对合给closed trace-span K的isotropy。all dF=0⇒all dIn=0由正确 physical action轮廓gradient；反向用 full discriminant action factorization、I₀=ρ(J)和η=ηtilde(J)，all dJn=0意味着ℓ¹ differential dJ=0，因此all dF=0。故 K^{perpΩ}=K，确是原物理形式下的ambient maximalisotropy。

对同一 strong域的actualfiber Y（subsetdiffeology），内部velocityimage V_Y⊂K，已认证的finite trace真实流给trace-finite-span⊂V_Y。因此closure_ambient V_Y=K，且V_Y^{perpΩ}=K。不能把closure等式降为unclosed V_Y=K，更不能以pointwise product constraints给每一个rapidangularvelocity擅自积分一条共同fiber曲线。

在整个phase内部tangent Tinternal S∞上，令 j为ambient evaluation，ω=j*Ω，A为所有real/imagactions的common differentialkernel。naturality给jA⊂K，所以A isotropic；全部已认证internaltrace directions属于A。若ξ与A ω-orthogonal，则它与这些trace directions配对为零，得all dF(jξ)=0，进而all dIn(ξ)=0，故A^{perpω}=A。这个严格代数结论无需j injective，也不把A替换成TinternalY。

须区分三件事：phaseevaluation j的injectivity、pullbackform ω的nondegeneracy、fiberinclusion tangent map的injectivity。第一项单独不蕴含第二或第三。源稿把已有phaseevaluation证明与尚未完成fiber-map问题分开；ω的弱辛非退化若另有需要，应引用原phase构造的独立论证。上面的A-maximality不额外需要非退化，因为其radical自然包含于A。

以上是新 actual Poisson bridge之后的完整 ambient closure与 carefully defined internal common-differential-kernel最大性。实际fiberregularity/unclosedtangent、完整global actionangle、全M spectralstateinverse与closure仍不随之成立。共同小背景谱图和allnoncentralactions非零条件由 [同一strong图actiongenericity](akns_actions_same_strong_chart_genericity_20261011.md) 提供非空真实参数residual见证，仍不外推整个S∞generic。

本轮新源稿 readback和独立手算完成，无新增或重复machinechecks；独立脚本累计仍为145个断言。
