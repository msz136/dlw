# M2 variable-action phase 与原物理辛形式的独审

2026-10-11。实际读取并独审 `m2_regular_variable_action_original_symplectic_phase_20261011.md` §§1–7（初读版本 16286 bytes，来源所报 SHA256 `42C0DF907CAB0FA5DD486135A8C0DC5ACD1B3C63E5188D7683B90B3E2DF678EC`）。同时实际读取 cross-operator 稿、mixed-low field/real-form 稿和 strong relative-fiber 稿。不复跑旧检查，不改共享记录。

结论：主稿的普通 Banach 相空间、真实共同等值集、微分无 ghost、原形式的弱非退化性和实际 level 的最大各向同性证明通过。在已证 cross inverse 下，旧 Hc 的完整等值集轨迹也通过，但其论证仅为固定 level 轨迹；不能升级成全邻域 Hamilton 自同构。本文另独立给出 reciprocal charge 的统一 ℓ¹ 解析求和引理。随后实际读取主稿 §§8–9 和 `m2_reciprocal_spectral_actions_and_dlw_frequencies_20261011.md` 全文及新增 (3a)：共同低阶域的输入已由实际 contour/log 证明补齐，因此有界角平移的全邻域 Hamilton 流和完整局部 level orbit 现为具体通过的结论。

## 1. 精确输入与实形式

使用已有实际 reduced chart

\[
\mathcal R:X_0=L^2_0(u)\times H^1_0(v)\longleftrightarrow
E_0=\ell^2\times\ell^2,
\quad W=(w,z),\quad J_n=w_nz_n,\quad n\ne0,
\]

以及其同一低阶域上的全 Sobolev restrictions。原物理张量与形式为

\[
\mathbb J=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix},
\quad
\Omega(U,V)=-16\int_0^L[(KU_u)V_v+(KU_v)V_u],
\quad K=D_0^{-1}.
\tag{1}
\]

K skew-adjoint，故 Ω skew。代入 XH=−offdiag(D)gradH/16，分部积分精确得到 Ω(XH,V)=dH(V)，符号与 16 的缩放一致。

真实相空间使用已建立的谱规范实结构
\(w_{-n}=-\bar w_n,\ z_{-n}=-\bar z_n\)。相应 J−n=barJn，但不能仅用 action 的共轭关系代替完整实结构。本文使用 mixed-low 稿 §§7–8 的归一化谱规范；主稿的原-real 结论仍以该实际等变身份为输入，不以真空 Fourier 导数代替它。

第二输入是原 centered DLW Hamiltonian K0 的精确频率式

\[
\dot w_n=\omega_n(J)w_n,\quad\dot z_n=-\omega_n(J)z_n,
\quad \omega_n=-k_n^2-2i\eta(J)k_n+r_n(J),
\quad r:\mathcal J\to\ell^\infty\text{ analytic},
\quad k_n=2\pi n/L. \tag{2}
\]

主稿明确将此频率式、其物理时间归一和所需 small-S action 范围单列为额外输入。本文独审其后的几何结论，不把一个外部 NLS 频率定理自动视作 (2) 的物理系数证明。原空间平移频率 ikn 亦保留其既有 normalization。

## 2. Banach state map、Gaussian margin 与精确周期排除

令 B 为 bounded sequence 的实际实形式，即 a−n=baran。固定原-real 强态 W*，所有 J*n≠0，并有
\((|w_n^*|+|z_n^*|)e^{\gamma k_n^2}\in s\)。这条 margin 确由 (2) 和已存在的双向小 K0 germ 推出：在真实背景 η 为实数，Reωn=−kn²+O(1)，在 ±T 两个实际解点分别控制 w 与 z 的增长即可。不必为此作虚构的无穷联合时间演化。

考虑普通真实 Banach 参数

\[
(a,q,t,s)\in B\times B\times\mathbb R^2,
\]

\[
w_n=w_n^*e^{a_n/2+q_n-tk_n^2+isk_n},\quad
z_n=z_n^*e^{a_n/2-q_n+tk_n^2-isk_n}. \tag{3}
\]

所有 bounded-sequence 导数是 bounded multipliers，t/s 导数只引入 kn 的有限次幂；在 |t|<γ/4 的严格 margin 下，它们均为到任意 hN 的有界解析导数。状态 map 复合实际 inverse chart 给原-real C∞ fields。赋予像从参数箱搬运的 Banach 拓扑，不能称它为 ambient smooth-field 子空间拓扑。

周期检验精确如下。两个状态相等先给 e^{a−ã}=1；若各 a 半径 <π/4，则差的绝对值 <π/2，故 a=ã。然后

\[
\Delta q_n-\Delta t\,k_n^2+i\Delta s\,k_n=2\pi i\ell_n,
\qquad\ell_n\in\mathbb Z. \tag{4}
\]

实部与 bounded Δq 强制 Δt=0。positive n 上二阶差分的右侧大小至多 8ε（每个 q 的半径 ε<π/16），故整数 Δ²ℓn=0。于是 ℓn=An+B，A,B∈Z。bounded Δq 再强制 Δs=LA；各 |s|<L/8 给 |Δs|<L/4，故 A=0。最后 ∥Δq∥∞<2ε<π 给 B=0。反射关系决定负指标，故 map 单射。其 differential 为零时，先有 δa=0，再有 δq−δt k²+iδs k=0；同样依次强制 δt=δs=δq=0。这里真实 t/s 的有限维模型是关键，未把一个不离散周期格的 growing complex ℓ∞ ball 搬来使用。

## 3. 实际 ordinary level 与 ghost-free tangent

Jn=J*n e^{an}。在选定统一 logarithm branch 上
\(\mathscr A_n=\log(J_n/J_n^*)=a_n\)，故 relative-action map 恰为 Banach 参数投影。它是 split submersion，其实际 common levels 是 a=a0，切空间恰为 δa=0。

这不是只从全部 coordinatewise differentials 为零猜出可积切空间：每个 δa=0 方向都由参数直线实际积分，finite sum 仍属于相同普通切空间。状态 differential 已单射，所以 ordinary Banach/internal tangent 到物理 evaluation 的 kernel 均为零。声明仅针对这个拓扑相空间；不推出完整 inherited S∞ fiber 的 ordinary regularity。

实际 action sequence 的目标可以等价描述为 weighted relative norm \(\sup_n|\delta J_n/J_n^*|\)，而不是普通 ℓ¹ action 范数。原 J*n 可任意快速趋零；它的非零性足够，不要求一个不可能的统一正下界。

## 4. 原形式：连续、闭、弱非退化与真实 Lagrangian levels

(1) 本身已在 X0 连续：K:L²0→H¹0 连续，K:H¹0→H²0 连续，各积分由 L² pairing 控制。它是常系数闭形式。inverse reduced chart 将其搬到 E0，得到 analytic、局部 operator-bounded two-form Ω̃。复合 (3) 得 Banach phase 的连续闭原形式；它不是另设的 Hilbert canonical form。

若 phase tangent U 与全部 phase tangent Ω-正交，特别与全部 genuine realified action fields 正交，则 dReIn(U)=dImIn(U)=0。Jn≠0 强制 δa=0。剩余是实际垂直速度

\[
(\theta_nw_n,-\theta_nz_n),\qquad
\theta=\delta q-\delta t k^2+i\delta s k\in\mathcal V_2. \tag{5}
\]

这里 \(\mathcal V_2=\{v:\sup|v_n|/\langle n\rangle^2<\infty\}\)。已证 B(J):ℓ∞→V2 bounded iso，且 physical torque 是 iB(J)c。因此正确系数是 c=B(J)−1(−iθ)，不是漏掉 −i 的 inverse。真实 U 的 conjugation 配合该 inverse 唯一性强制 c−n=barcn。

在这个点，genuine ambient Hc=ΣcnIn 的实际 field 就是 U。对有限支持真实 horizontal test b，有

\[
\Omega(U,U_b)=dH_c(U_b)=\sum_{n\ne0}c_nJ_nb_n. \tag{6}
\]

每对 positive/negative 项等于 2Re(cnJn bn)。bn 可任取两个真实方向，Jn≠0，因此 cn=0，继而 θ=0，状态 differential 单射给 U=0。故 phase 上原 Ω 弱非退化。这个点对 Hc 的使用不需要、也不提供 Hc 在附近 phase 内的 flow。

common-level tangent TY 是已证 ambient common action kernel 的子空间，因此 isotropic。反向若一个 phase tangent 与 TY 正交，TY 包含全部 realified action fields，便再次检测出 δa=0。故精确有

\[
(T_xY)^{\perp_\Omega}=T_xY. \tag{7}
\]

这是该 ordinary Banach level 的实际 maximal isotropy，而非有限块 Hessian 结论或 Hamilton 线性闭包。未证明 Ωflat onto 整个 Banach dual，因此仍只称 weak symplectic。

## 5. genuine flows 与原 Hc 的边界

由 (2)，原 K0 field 在完整 phase 箱内恰为

\[
\dot a=0,\quad\dot t=1,\quad
\dot s=-2\eta(J),\quad\dot q=r(J). \tag{8}
\]

translation 为 sdot=1。每个固定真实 trace/action field 的 bounded analytic torque 属于 B，故它也给完整箱内的 ordinary local analytic flow。均取 J 常值，实际解公式可直接微分核验。任意预给 Γ(t) 由既有 centered gauge/translation 重构；此处没有额外冻结 Γ。

主稿 compact balanced-test argument 的数学内容正确，但“image compact”应理解为“image 的 closure 在 h0 中 compact，且 closure 留在低阶域内”。bounded a 的无限盒有 uniform rapid tail，有限头 bounded，给该 compact closure；a 的开盒本身未必 compact。以更大的 complex a 盒统一测试、再作 Cauchy，得到各固定 charge 的 ℓ∞-valued analytic torque，且不除原态 tiny coordinate。

旧 Hc=ΣcnIn 若按一个固定 J 的 B−1 选择，可以给该等值集上的精确直线插值实际轨迹。对另一 J′，B(J′)c 可能仅在 V2，不能保证属于 B+Rk²+iRk。因此其全 phase field/flow 断言尚不能由 B inverse 得出。主稿 §§5–6 明确守住这一点，审查通过。

## 6. reciprocal actions 的统一 ℓ¹ 引理

以下是新独立证明，供新 reciprocal 稿使用。它只需同一个 star-shaped low E0 ball 的 exact identities，不需要 uniform-in-n Volterra 渐近。

**引理。** 设每个 n≠0 的 A_n 在共同复 low ball holomorphic，A_n(0)=0，其原 physical field 在 reduced coordinates 精确为

\[
X_{A_n}(W)=-L(w_ne_n,-z_ne_n). \tag{9}
\]

则 A=(A_n):E0→ℓ¹ holomorphic、局部有 \(\|A(W)\|_{\ell^1}\le ML\|W\|_{E_0}^2/2\)。对任意 d∈ℓ∞，H_d=ΣdnAn 是实际 holomorphic Hamiltonian，并有完整 low field

\[
X_{H_d}(W)=-L(d_nw_n,-d_nz_n). \tag{10}
\]

**证明。** 在小 ball 上 ∥Ω̃W∥≤M。finite-support d 的实际 Hamilton identity 与从 0 到 W 的 radial integral 给

\[
\sum_n d_n A_n(W)
=\int_0^1\widetilde\Omega_{\tau W}
[-L(d_n\tau w_n,-d_n\tau z_n),W],d\tau,
\]

\[
\left|\sum_n d_n A_n(W)\right|
\le\frac{ML}{2}\|d\|_\infty\|W\|_{E_0}^2. \tag{11}
\]

在任意 finite block 选 dn 为 An 的复相位，使每个 dnAn=|An|，即得全 ℓ¹ bound。这个使用不假定 phase 的每个复方向为真实方向：此引理在既有 low complexification 上作 holomorphic proof，然后限制实际实结构。

强解析性亦可严格证明，而非从逐坐标解析性直接跳步。固定 W0 的一个复 ball；所有 finite-coordinate projections 的 ℓ¹ norm 有统一 bound。对它们作 Cauchy Taylor 展开，每个 kth homogeneous coefficient 的所有 finite ℓ¹ block 有一致 \(M_0(\|h\|/\rho)^k\) bound。兼容坐标因此组成一个 ℓ¹ coefficient；polarization 使其为连续 homogeneous polynomial。Taylor 级数在 ∥h∥<ρ 的 ℓ¹ 中绝对收敛，其每个坐标等于 An(W0+h)。所以 A 是 Banach-valued holomorphic。

从而 H_d analytic，且其 derivative 的 ℓ¹ pairing 实际收敛。有限截断的 field 在固定 W 的 E0 norm 中趋于 (10)。Ω̃ 的连续性与 dA 的 ℓ¹ 收敛给
\(dH_d(U)=\widetilde\Omega(X_{H_d},U)\) 对全部 low tangent U 成立。其 source inverse 是原物理 field；不是任意向量场被重新命名为 Hamiltonian。显式 local flow
\(w_n(\tau)=e^{-Ld_n\tau}w_n(0),\ z_n(\tau)=e^{Ld_n\tau}z_n(0)\)
是 low Banach flow，并保留每个 higher Sobolev scale。证毕。

若 An 在 real source 满足 A−n=barAn，则 d−n=bardn 的 Hd 为真实。此 reality 可从 (9)、原 Ω 的 reality 和背景常数 An0=0 推出，不需要假装 log 的任意局部分支自动给它。

## 7. reciprocal 身份的精确检查与依赖

候选局部 primitive 使用 λ=η−2iz/L、ωλ=(S²−λ²)/(16S)：

\[
P_n(z,\eta)=4iL\log\frac{S+\lambda}{S-\lambda},
\quad P_z=\omega_\lambda^{-1},
\quad P_\eta=\frac{iL}{2\omega_\lambda}. \tag{12}
\]

直接求导核对通过。每个 noncentral contour tube 必须避开 λ=±S，并选一个单值 log branch。定义

\[
A_n=\frac1\pi\oint_{\Gamma_n}P_n\frac{\Delta_z}{R}\,dz,
\quad R^2=\Delta^2-4. \tag{13}
\]

variation 中使用 \(\delta(\Delta_z/R)=D_z(\delta\Delta/R)\)，分部积分得

\[
\delta A_n=-\frac1\pi\oint\frac{\delta\Delta}{\omega R}
+\frac1\pi\oint\frac{iL\Delta_z}{2\omega R}\,\delta\eta.
\]

固定 original λ 的 chain rule 是
\(\delta\Delta=\delta F_\lambda+(iL/2)\Delta_z\delta\eta\)，故两项精确相消：

\[
dA_n=-\frac1\pi\oint_{\Gamma_n}
\frac{dF_{\eta-2iz/L}}{\omega_{\eta-2iz/L}R}\,dz. \tag{14}
\]

这里不能把 fixed shifted z 当作 fixed original λ。actual trace field identity 再给
\(D\mathcal R X_{A_n}=\Pi Y_{I_n}\)，其原 L/i normalization 恰为 (9)，即 −L unit logarithmic torque。原 integral at collapsed noncentral gap 的 Δz/R 奇点可去，P_n holomorphic，故 An0=0。

本文已独推 (12)–(14) 和 sign。随后实读 reciprocal 主稿新增 (3a)，上述共同域条件现已实际核实：使用共同 KLTZ 低阶球的圆周 Γn=∂B(nπ,π/4)，log 在 B(nπ,π/3) 上定义；附加 L|S|<π/4，缩一次低阶球使 L|η|<π/4，则对所有 n≠0，

\[
|\lambda|\ge(2/L)(\pi|n|-\pi/3)-|\eta|
>13\pi/(12L)>|S|.
\]

每个 z disc 与 η disc 的乘积 simply connected，ratio (S+λ)/(S−λ) 无零极点，故联合 holomorphic log 存在。同一 KLTZ ball 供应所有 canonical R 分支和固定 spectral contours；没有作 n-dependent radius 的无穷交集。沿每个固定 contour 的 trace field 是已证明 mixed-low order-zero analytic field；分母 ωR 无零。高阶 dense intersections 的 Hamilton identity 通过连续低阶 Ω 和 analytic field 延至 low ball。故 §6 的全部 concrete 输入通过，新增 reciprocal 定理可以正式使用。

## 8. 共同 reciprocal 输入已成立：完整 phase Hamilton orbit 的闭合

根据 §7 实际复核的共同 low chart，§6 将任意真实 bounded d 变为 (10) 的 genuine field。它在整个 core phase 内恰为 qdot=−Ld，其他参数不变；因此不再遇到旧 Hc 邻近 J′ 的 Eg 障碍。

给定任一 phase tangent (δa=0,Q,T,S0)，在该点令

\[
\alpha=T,\quad\beta=S_0+2\eta(J)T,\quad
d=-[Q-Tr(J)]/L. \tag{15}
\]

固定这些 coefficients，实际 Hamiltonian
\(\alpha K_0+\beta P_{\rm translation}+H_d\)
不仅在该点产生指定 tangent，在所有邻近 J′ 上仍属于 phase 模型：tdot=α、sdot=β−2αη(J′)、qdot=αr(J′)−Ld。所有 coefficients analytic 且 J′ 保持常数。这给全部 level tangent 的精确 genuine Hamilton generation，不取 closure。

对同 level 的两近点，用相应参数差替换 (15)，所得 fixed Hamiltonian 的 time-one curve就是直线参数插值；取足够近的点或统一小时间，轨迹留在箱内。它是定义在整个 phase 邻域的 local Hamilton flow，而不只是 point-level ambient solution。所有这些 vertical fields 与原 K0、translation、固定 action/trace fields 在 phase 上对合；由 (7) 的 isotropy，其 Poisson pairing 为零。这使实际 common levels 成为 genuine local Hamilton orbit，仍无需宣称紧环面。

## 9. 全部严格范围

ordinary regular variable-action phase、原 weak Ω、actual Lagrangian levels 和 primitive/reciprocal 的实际共同低域链均已通过独审。全-neighborhood bounded-angle Hamilton completion 是已补齐输入的具体结论。原-real 输入由谱规范实结构独稿供应；原时间 frequency 已在以下 §10 另作独立 coefficient 和 primary theorem 核对。定理仍保留明确 small-background 和 BKM action 范围，不将其称作无条件全部 smooth data 定理。

变量 a 的整个箱是否属于此前所有 Cj 的同一 strong S∞ 尚未证。Gaussian margin 保证原 order-two DLW，不自动容纳任意高阶 hierarchy axis。固定 a=0 component 的既有 strong 入域与 variable-a 全部入域是不同命题。

该相空间仍是给定 stronger topology 的薄相域，有两组完整 bounded-function sequence 自由度；没有把 physical fields 固定为有限维 ansatz。它不等于自然开放的任意 C∞ 原物理场叶，也不解决一般 M 的 invariant-action/norming inverse。上面的最大性与 regularity 均清楚限定为这一个真实 M2 Banach phase。

## 10. 原时间系数与 primary complex frequency 输入二审

实际读取 reciprocal 稿 §3 和 `root_m2_original_frequency_normalization_audit_20261011.md` 后另独立重算：Riccati βx=b−ζβ−aβ² 的前三系数为 b、−bx、bxx−ab²；所以 c1=∫ab、c2=−∫abx、c3=∫(abxx−a²b²)。φ1=−iLa/2、φ2=2iLb、单位周期 y=x/L 给 NLS energy E=−L³c3。

\(\Pi Yc_1=0\)、\(Yc_2=\partial_x\)、\(X_\eta=\partial_x/(8SL)\)。实际 Kλ expansion 右侧的常数项 \(-\partial_x/(16S)+(L/2)X_\eta\) 精确消去；λ−1 系数给

\[
D\mathcal R X_{C_1}=(\Pi Yc_3+2\eta\,\partial_x)/(16S),
\quad D\mathcal R X_{H_{\rm DLW}}
=-i\Pi X_E^{\rm std}/L^2-2\eta\,\partial_x,
\]

其中原 H_DLW=−16SC1+constant、Y=(L/i)Xstd。standard X_E 对本地 w 的 torque 是 −iωNLS；central projection 减去 ω0。因此原 Cartesian frequency 精确为

\[
\omega_{{\rm DLW},n}
=-[\omega_n^{\rm NLS}(I)-\omega_0^{\rm NLS}(I)]/L^2
-2i\eta k_n. \tag{16}
\]

其 leading −kn²、linear −2iηkn 的符号和时间系数全部通过，无任意 NLS 时间重标。

另外实际浏览 [Berti–Kappeler–Montalto primary PDF](https://arxiv.org/pdf/1603.09252)，Theorem 3.2(i)、正文页22（PDF 索引页22）。定理确给包含 0 的 complex ℓ^{1,2} 邻域 V，以及 (ωNLS_n−4π²n²)n 的 bounded analytic ℓ∞ 映射；其证明在 complex balls 作 Cauchy derivative bounds。这支持 (2) 的 analytic bounded remainder。原 negative central I0*=−L²S²/4 必须显式满足 |I0*|<r_BKM/2，并将 noncentral weighted action 与 central variation 之和压在剩余半径内。此额外半径并无来源提供的数值，也不能由旧 KLTZ neighborhood 自动替代。全文只使用该 theorem 的频率输入，没有引入其 defocusing real form 或 KAM 结论。

## 11. 更直接的弱非退化与 isotropy 引理

weak-nondeg 可独立于旧 B inverse 核对。在任一 Jn≠0 点，每个 finite-support Cartesian tangent (δw,δz) 都由 finite-support 参数

\[
\delta a_n=\delta w_n/w_n+\delta z_n/z_n,
\qquad\delta q_n=\tfrac12(\delta w_n/w_n-\delta z_n/z_n),
\quad\delta t=\delta s=0
\]

产生；actual reflection 恰使这些参数属于真实 B。这些 finite-support real tangents dense 于整个真实 E0。Ω̃ 连续 weak-nondeg：原 X0 中，先与 (φ,0) 配对使 Kv=0，再与 (0,ψ) 配对使 Ku=0；zero means 得 u=v=0。low chart 的 derivative 是 Banach iso，保持该性质。因此一个 phase tangent 若与全部 phase tangents Ω-正交，便与 dense finite-support Cartesian tests 正交，继而是 0。此 proof 不需额外 ℓ1_4 cross-operator smallness；主稿保留该旧充分假设亦无害。

在 reciprocal identity 已成立后，§8 的每个真实 level tangent 都是某个 \(\alpha X_{K_0}+\beta X_P+X_{H_d}\) 的实际值。各 Hamiltonian 的实际 spectral brackets 已为零；无限 Hd 用 §6 的 ℓ¹ differential 与固定实际 high tangent passing-to-limit。故 TY 本身 isotropic 可直接由这些 genuine whole-phase fields 得出，不必先引用旧 ambient common-kernel closure。反向 orthogonal⇒δa=0 仍由 genuine fixed action fields 检测。因此新的 ordinary regular-level maximality 不以旧 inherited-fiber regularity 为隐藏依赖。

最终实际读取 mixed 主稿 §§8–9 的完整 proof 与 theorem 后，两者的 reciprocal completion、原 weak Liouville 精确适用域和 variable-a 尚未全部进入旧 S∞ 的限制均通过。未运行任何新的数值或 symbolic 检查。
