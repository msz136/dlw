# 报告 scope 独审与 nonlinear cross-map 备用证明

2026-10-11。只写独立新稿，未改共享 report/STATE。实际读取 build_current_report.py、mixed 主独审 §§16–17、actual 谱稿 §§16–17、AKNS 状态桥及 KST primary 全文。下文区分已经核过的输入、条件式定理和仍待合成核验的具体算子。

## 1. 当前 report 源码的范围通过

读取版本已明确：全部原局部层级的 strong 弱辛域属于 \(c\ne0\) 正则分支；同一状态有限块独立属于指定小非零均匀背景均值叶/Hilbert 参数图。没有泛化为任意物理 Cauchy、普通 manifold、全相域 generic 或 regular integral leaf。

内部切空间使用 algebraic pointed-plot colimit，D topology 与 ambient Fréchet subspace topology 区分准确。内部速度的 weak pairing 是 ambient \(\Omega\) 的明确 cross pairing；相域 ghost 排除不被移植成共同 fiber ghost 排除。fiber \(Y\) 只知
\(\operatorname{im}(T_{\rm int}Y\to T_{\rm int}\mathfrak S_\infty)
\subset\bigcap\ker dI\)，甚至此 fiber tangent map 的单射未证。当前源码准确保留此限制。

fixed-spectrum flow 桥准确要求已有 strong presentation；真实 low Banach auxiliary 流没有被升级为任意原 DLW Cauchy 流。normalized trace 和未扣 holonomy 的 \(a_n,g_n\) 为 order zero；扣 holonomy 另含实际 translation。零平均全 M 部分只称指定非空 real flag/Sylvester 一般函数 mixed 图上的原时间，未扩大为零平均所有高阶共同时间或严格全零组件均值共振叶。

后续全 M actual normalized class 对合、\(C_n\) 桥和同 strong 域谱流已由
[新的独审](all_m_actual_spectral_independent_audit.md) 严格完成；报告可以对应扩大这些条目。M=2 的 gap/norming 标号和 AKNS state inverse 不能随之扩大到全 M。

## 2. 一份可直接使用的 primary complex one-smoothing 输入

[Kappeler–Schaad–Topalov, arXiv:1505.04455v1](https://arxiv.org/html/1505.04455v1)
Theorem 1.1 的标题陈述以 defocusing real slice 为主，但 §3 的证明明确在
\(W\cap H_c^N,\ N\ge1\) 给 nonlinear Fourier map 减 Fourier 的一阶增益及局部一致界，并证明解析性。这里使用的是其 proof 中的一般 complex 结论，未把 real-slice theorem 自行外推。与 KLTZ2009 Proposition 2.9 的 near-zero map 在共同零邻域上相同：两者是同一 defocusing Birkhoff map 的 analytic extension，零点附近 uniqueness 给一致。

记 \(\mathcal B=\mathcal F+\mathcal S\)。在该共同 complex 域和每个整数 \(r\ge1\)，
\[
\mathcal S:H^r\longrightarrow h^{r+1}
\]
locally holomorphic。Cauchy 估计给 \(D\mathcal S\) 同阶 gain。inverse 的 gain 来自准确 identity
\[
\mathcal B^{-1}-\mathcal F^{-1}
=-\mathcal F^{-1}(\mathcal B-\mathcal F)\mathcal B^{-1}.
\tag{1}
\]
standard NLS canonical identity 只在下面用于控制 adjoint：
\[
D\mathcal B\,J_0\,D\mathcal B^*=J_0
\ \Longrightarrow\
D\mathcal B^*=J_0^{-1}D\mathcal B^{-1}J_0.
\tag{2}
\]
所以 adjoint 减 Fourier adjoint 也在 positive Sobolev scales 有一阶 gain。这个技术使用不把 physical tensor 宣布为 standard \(J_0\)。

## 3. exact physical principal part 在一般光滑状态也常数

状态桥给
\[
\Lambda=E_\theta(M+jKc),\quad
M=\begin{pmatrix}1&0\\A&B-D/S\end{pmatrix},\quad
J_{ab}=\Lambda J_{uv}\Lambda^*.
\]
\(K=D^{-1}_0P_0\) 阶 \(-1\)，故含 \(jKc\) 的交叉项阶至多一。
局部部分 rr block 中 \(-D^2A/S+AD^2/S\) 的二阶项相消；
off-diagonal 的 \(e^\theta D^2e^{-\theta}\) leading coefficient 是一。
因此在每个固定 smooth state，
\[
J_{ab}=
\begin{pmatrix}0&-D_x^2/(16S)\\D_x^2/(16S)&0\end{pmatrix}
+R_1,\qquad R_1:H^{r+2}\to H^{r+1}.
\tag{3}
\]
该 claim 是实际 operator pushforward 的 principal identity，不限背景。
source-dependent smooth coefficients、mean projection/constant terms 及 finite-rank terms 不影响 order-two principal symbol。

ordinary target pairing 需在 \(t=x/L\) 时除 \(L\)。对
\(\varphi_1=-iLa/2,\varphi_2=2iLb\)，其 principal tensor 是
\[
\begin{pmatrix}0&-D_t^2/(16SL)\\D_t^2/(16SL)&0\end{pmatrix}.
\tag{4}
\]
KST (1)–(2) 的 gain 把一般 Birkhoff pushforward 写为
Fourier 变换后的 (4) 加一个 \(h^{r+2}\to h^{r+1}\) 的余项。这里需要固定一份真实 physical Cartesian state chart；不能仅把 full AKNS potentials 视为 unconstrained 物理状态。

## 4. 条件式 nonlinear maximality 定理

这是自足的 operator theorem。具体 AKNS 应用的条件须逐条核验；本节自身不宣布它们已经全部合成认证。

假设给定实际 smooth physical state 的同一源叶有 Cartesian state coordinates
\(\xi_n=(z_n,w_n),n\ne0\)，与各 Sobolev scales 对应；原物理 actions 为
\(I_n=z_nw_n\)，且它们的真实 Hamilton 场属于同一
\(\mathfrak S_\infty\)。假设这些 actions 已物理对合，且每个 pair \(\xi_n\ne0\)。
把 exact physical tensor 在此 chart 写为
\[
\mathcal J=c_*\operatorname{diag}(n^2)
\begin{pmatrix}0&1\\-1&0\end{pmatrix}
+\mathcal R_1,\quad
c_*\ne0,\quad
\mathcal R_1:h^{r+2}\to h^{r+1}
\tag{5}
\]
在每个整数 \(r\ge1\) 成立。还要求 smooth cotangent 上 \(\mathcal J\) 的 kernel 为零，这由真实 source inverse 与原 leaf 的 \(D\) 非退化可核验。

在固定 state 令
\[
\nu_n=(|z_n|^2+|w_n|^2)^{1/2},\quad
g_n=(w_n,z_n)/\nu_n,\quad
t_n=(z_n,-w_n)/\nu_n.
\]
它们定义 scalar \(h^r\) 到双序列 \(h^r\) 的 unit frames \(U_g,U_t\)。
每个 norm 的 frame bound 恰为一，不需要 uniform lower gap bound。
双线性 action differential 的共同 kernel 是 closed subspace
\[
\mathcal K^r=U_t h^r
=\{v:w_nv_{z_n}+z_nv_{w_n}=0\ \forall n\}.
\tag{6}
\]
physical involution 首先对 finitely supported coefficients 给
\(\mathcal J U_g a\in\mathcal K^r\)，再由 boundedness 和 closedness 延拓到所有 \(a\in h^{r+2}\)。
定义实际 cross-map
\[
\mathcal M=U_t^{-1}\mathcal J U_g:h^{r+2}\to h^r.
\]
因 standard skew matrix 把 \(g_n\) 准确送到 \(t_n\)，
\[
\mathcal M=c_*\operatorname{diag}(n^2)+\text{compact }(h^{r+2}\to h^r).
\tag{7}
\]
非零 index \(n\) 上第一项是有界同构；一阶余项经 compact embedding 成为 compact。因此 \(\mathcal M\) Fredholm index zero。

若 \(\mathcal Ma=0\)，(7) 用 gain-one 余项 bootstrap \(a\in h^{r+2}\) 到所有更高阶；\(U_ga\) 也是 smooth。smooth physical tensor 无核给 \(U_ga=0\)，所以 \(a=0\)。index zero 便给所有 \(r\) 的 onto，逆在这些 scales 中一致；同一解的 elliptic bootstrap 保全部高阶。

对任意 \(v\in\mathcal K^\infty\)，解 \(\mathcal Ma=U_t^{-1}v\) 得 \(a\in h^\infty\)。截断 \(a\) 到有限频率，
\[
\mathcal J U_g a^{(N)}
=\sum_{0<|n|\le N}\frac{a_n}{\nu_n}X_{I_n}
\longrightarrow v
\quad\text{在每个 }h^r.
\tag{8}
\]
每个有限 coefficient 可以很大，不需要无穷时间向量或对 \(\nu_n^{-1}\) 的 uniform bound。这里接近的是固定 state 的 tangent vectors。

令 \(\mathcal A\) 为 finite actual Hamilton span，ambient Fréchet closure 由 (8) 等于 \(\mathcal K^\infty\)。\(\mathcal A\) 物理对合，所以 isotropic；ambient \(\Omega\) 连续给 \(\mathcal K^\infty\) isotropic。对任意合法 strong internal tangent \(v\)，
\[
v\in\mathcal A^\omega\iff dI_n(v)=0\ \forall n.
\]
于是 common differential kernel 内部的向量与 ambient \(\mathcal K^\infty\) 配对为零，其 weak symplectic orthogonal 也等于自身：这就是同一 strong weak phase 的 nonlinear pointwise maximal isotropy。

闭包的拓扑必须明确为内部注入 \(j_*\) 后的 ambient Fréchet 相对拓扑；内部 algebraic colimit 没有预设 Banach/Fréchet topology。没有推出 inherited fiber 的内部 tangent 单射、fiber tangent 等于 differential kernel、regular leaf 或全频普通 action-angle chart。

## 5. 具体应用尚需合成审定的条件

KST gain 输入与 (3) 已有严格来源/推导，但 (5) 用于 physical 非中央 Cartesian chart 时必须把所有投影、state-dependent central constraints 和 gauge slice 的 finite-rank corrections 完整带入。near-zero 小 \(S\) 下可尝试
\(\Xi=\pi_{n\ne0}\mathcal B(\varphi(u,v))\) 的 low Banach IFT：
physical mean graph 在背景的 derivative 是 mean-zero potential inclusion，而
\(D\mathcal B_{\varphi^0}\) 随 sufficiently small \(S\) 接近 Fourier，非中央 projection 可逆。
需要证明同一 low chart 的全部 higher intersections 和 exact adjoint tensor formula；仅逐高阶 IFT 不能给一套共同源域。

real physical coordinates 的 induced reality 不能当成 standard NLS real slice。可从 actual normalized trace 的
\(\overline{\Delta(z)}=\Delta(-\bar z)\) 及 matching square-root branch 推
\(\overline{I_n}=I_{-n}\)，再将复 (8) 的 truncations 与共轭配对实化；这一步必须按同一 contour labels 验证，不能默认。

这些是可具体核验的新条件。另一条更直接的路线是原 physical fixed-\(\lambda\) 谱场模 constant diagonal gauge 的 exact pushforward 为 weighted canonical discriminant 场；若其 direct closure 能严格证明 (8)，即可替代本节 Fredholm 技术而保留同一 maximality 结论的范围。

## 6. 两个条件的进一步直接证明：同一 state 图与 induced reality

### 6.1 非中央 Cartesian 图的共同 Sobolev 逆

这一引理只取 sufficiently small nonzero \(S\)，其半径依文献零邻域，未指定数值。令 \(f=P_0a,g=P_0b\) 是已证真实 low state 图；full potential image 是
\((a,b)=(f+\alpha(f,g),g+\beta(f,g))\)。
背景 \((a^0,b^0)=(-S,S/4)\)，\(D\alpha_0=D\beta_0=0\)，所以 tangent inclusion 恰为 mean-zero potential inclusion。固定 balancing 和 \(t=x/L\) 不改变同构性。

设 \(\pi_\ne\) 删除 Birkhoff 两个 \(n=0\) 分量。定义
\[
\Xi(f,g)=\pi_\ne\mathcal B(\varphi(f,g)).
\tag{9}
\]
当 \(S\to0\)，background potential \(\varphi^0\to0\)，low operator
\(D\mathcal B_{\varphi^0}\to D\mathcal B_0=\mathcal F\)；
\(\pi_\ne\mathcal F\) 在 mean-zero potentials 上正是 onto
\((h^0(\mathbb Z\setminus\{0\}))^2\) 的 Fourier 同构。
因此 sufficiently small \(0<|S|\) 的 (9) 由一次 low Banach IFT 给一份共同双解析 state 图。

这份 low inverse 自行保所有 higher intersections，不需逐阶缩半径：
给定 low target 中 \(\xi_\ne\in(h^r)^2\)，low inverse 已确定两个 central scalar
\(\xi_0\)。补上这两个数得到 full \(\xi\in(h^r)^2\)；
KLTZ Proposition 2.9 的同一 low 图逆给 full potentials \(H^r\times H^r\)。
投影 mean-zero 及原状态桥的 low inverse bootstrap 便给
\(u\in H^r_0,v\in H^{r+1}_0\)。反向包含由 direct map 得到。
各 finite high norms 在 high bounded sets 上 locally bounded，故同一 low holomorphic inverse 的 higher-valued 解析性由 Cauchy/ODE bootstrap 得到。这样建立实际 nonlinear state coordinates，且 background 附近 higher domains 正是同一 low domain 的 intersections。

其 tensor 不需另对 central constraints 做未经证明的 reduction：准确直接推前就是
\[
\mathcal J_\Xi=\pi_\ne D\mathcal B\,
J_{\varphi,\rm physical}\,
D\mathcal B^*\pi_\ne^*.
\tag{10}
\]
所有 actual mean/gauge reconstruction 都已经包含于
\(J_{\varphi,\rm physical}\)。noncentral source 正是原 leaf 的真实 local state chart。
由 §§2–3，在固定 smooth state 上 (10) 的 order-two principal part 是 noncentral Fourier diagonal；余项 \(h^{r+2}\to h^{r+1}\)。
KST 使用
\(J_0=\left(\begin{smallmatrix}0&-i\\i&0\end{smallmatrix}\right)\)，
Fourier canonical 校准给
\[
\mathcal J_\Xi=
\frac{\pi^2}{4SL}\operatorname{diag}(n^2)
\begin{pmatrix}0&1\\-1&0\end{pmatrix}
+\mathcal R_1,\qquad n\ne0.
\tag{11}
\]
即 §4 的 \(c_*=\pi^2/(4SL)\ne0\)。归一校准经过 ordinary \(dt\) pairing 的 \(1/L\)，不能漏掉该因子。

smooth kernel 无核也可直接证明。若 \(\mathcal J_\Xi \ell=0\)，
真实 state chart derivative 是 smooth tangent 同构；所以原 \(J_{uv}\) 作用于 pulled-back smooth gradient 为零。它在 fixed zero-mean leaf 的 kernel 只是 constant gradient、即零 leaf functional。state chart 的 onto 性于是迫使 \(\ell=0\)。因此 §4 的 Fredholm 条件在这一具体 low state 图中有完整来源，但仍建议由另一 agent 对 (10)–(11) 全部 scaling 独立复核后再升级报告。

### 6.2 真实谱反射及复闭包的实化

对 real physical \(u,v\)，\(\eta\) 实，actual normalized trace 满足
\(\overline{\mathcal F_\lambda}=\mathcal F_{\bar\lambda}\)。由
\(\lambda=\eta-2iz/L\) 得
\[
\overline{\Delta(z)}=\Delta(-\bar z).
\tag{12}
\]
zero-connected contour family 取
\(\Gamma_{-n}=-\overline{\Gamma_n}\)；canonical root 从零势
\(-2i\sin z\) 延拓，故
\(\overline{R(z)}=R(-\bar z)\)。
对 action contour 作复共轭，再令 \(w=-\bar z\)：共轭反转 contour orientation，而
\(\overline{\Delta_z(z)}=-\Delta_w(w)\)。
三个负号（\(z\)、导数、\(d\bar z\)）与 orientation 反转抵消，准确给
\[
\overline{I_n}=I_{-n}.
\tag{13}
\]
这来自 actual physical spectrum，未假定 Birkhoff Cartesian coordinates 的 reality 是 standard NLS reality。root 与 labels 必须取这份匹配约定。

因此 finite complex action-Hamilton spans 在 real state 由
\(X_{\operatorname{Re}I_n},X_{\operatorname{Im}I_n}\) 的 complexification 生成。
若 complex finite sums \(v_N\to v\)，其中 \(v\) 为 real physical tangent，则取 real parts 仍为 finite actual real Hamilton sums，且在 ambient Fréchet 收敛到 \(v\)。
complex §4 closure 可据此严格实化。这个过程没有把 real strong phase 的 internal tangent 全部等同于 ambient tangent；只使用实际 action flow 已是 internal，以及 \(j_*\) 的真实单射。

### 6.3 当前认证状态

以上引理补齐具体 near-zero state 图的 higher inverse 与 induced reality；§4 Fredholm 证明可与 (10)–(11) 组合成一个 narrow-domain nonlinear pointwise maximality 候选定理。它的全部推导已明确写出，正在等待独立复核，当前共享报告尚未将它视为已证最大性。direct weighted-discriminant 路线可能更短；无论采用哪条路线，regular fiber、fiber ghost 与 ordinary action-angle geometry 都没有随 pointwise closure 自动解决。

## 7. 最终采用 direct proof；备用 cross-map 不承担已证最大性

本节更新前面各节的历史状态。已实际独读 [direct physical trace closure §§1–8](m2_physical_trace_poisson_closure_proof_20261011.md)、[同一 strong 图 action 泛型 §§1–6](akns_actions_same_strong_chart_genericity_20261011.md) 及 [根审计 §§1–4](root_m2_nonlinear_closure_audit_20261011.md)，完整独立核验保存于 [场与闭包独审 §§6–10](m2_physical_trace_bridge_independent_review.md)。本次没有运行任何旧或新证书。

已证连接使用原物理 fixed-\(\lambda\) trace 场的精确 pushforward：
\[
DR\,X_{F_\lambda}
=\frac{S^2-\lambda^2}{16S}\Pi Y_{\lambda-\eta}.
\]
不同 gauge representative 的 \(d\gamma\) 项准确包含在 \(\Pi\)，period-one KLTZ 场的 scalar normalization 是
\(-iL(S^2-\lambda^2)/(16S)\)。full standard noncentral action 场不改变中央 angle，所以其固定 contour 的 projected integral 给单一 Cartesian angular direction。在各自 contour 上避开 \(\lambda=\pm S\) 后，ordinary Riemann sums 在每个 smooth seminorm 收敛；随后截断已 smooth 的实际速度。因此全部 angular kernel 在 original physical trace-field span 的 ambient \(C^\infty\) 闭包中，无需全频 gap 下界、无限个同时非零谱时间或椭圆 cross-map。

actual action-field span 的闭包也相同，另需 direct §4.4 已补证的 transpose continuity：
\[
(DB)^*=J_{\rm pot}^{-1}(DB)^{-1}J_{\rm seq}
\]
由 full standard canonical chart 及共同低阶 domain 的全部 high inverse 给同阶连续；再与 physical \(\Lambda^*\)（至多一阶）和原 \(J_{uv}\)（一阶）组合得 \(J_{uv}DR^*:s^2\to E_\infty\) Fréchet 连续。
action factorization 的 reduced coefficients \(\beta\in\ell^\infty\)，所以
\((\beta_nz_n,\beta_nw_n)\in s^2\)，其有限截断严格给
\[
X_{F_\lambda}
=\lim_N\sum_{0<|n|\le N}\beta_nX^{\rm physical}_{I_n}.
\]
反向 actual action contour identity 的 holonomy coefficient 精确由 winding 零消去。这只使用已知标准 canonical 图控制 transpose；physical tensor 没有被替换成标准张量。

在全部 noncentral \(I_n\ne0\) 的指定图内，
\[
\overline{\operatorname{span}_{\mathbb R}
\{X_{\Re F_\lambda},X_{\Im F_\lambda}\}}
=
\overline{\operatorname{span}_{\mathbb R}
\{X_{\Re I_n},X_{\Im I_n}\}}
=K_x,\qquad K_x^{\perp_\Omega}=K_x.
\]
realification 来自 actual physical connection 的 complex conjugation，不预设 standard NLS real slice。
同一已经建立 weak-symplectic \(\mathfrak S_\infty\) 的内部 action differential kernel
\(\mathcal A_x=j^{-1}K_x\) 满足 \(\mathcal A_x^{\perp_\omega}=\mathcal A_x\)。
phase evaluation \(j\) 的单射已由 mixed §16.4 证明；这里未知的 ghost 只可能出现在
\(T^{\rm internal}Y_x\to T^{\rm internal}\mathfrak S_\infty\) 这个不同的 fiber map。
实际 common-level inherited tangent 的 ambient 图像 \(V_x\) 满足
\(\overline{V_x}^{C^\infty}=K_x\)，但 \(V_x=K_x\)、fiber map 单射和 regular fiber 未证明。

这些点在同一 strong 图中确实存在：actual action residue 给
\[
I_{-n}^{[2]}=\frac{Lk_n^2}{16S}Q_nP_n,\qquad
I_{-n}=\overline{I_n}.
\]
mixed §17 的固定 holomorphic Hilbert 参数图在背景的 derivative range 包含全部 real finite Fourier directions。所有 one-action 非零函数与 fixed finite minors 因而在同一个 real Hilbert 参数球有非零 analytic witness；一次共同缩域后 Baire 给 residual、dense、非空参数集，同一个实际 strong 状态同时满足全部 action 非零和任意 finite real action 块内部独立。参数 residual 不能写成整个 \(\mathfrak S_\infty\) 的 D-topological genericity。

准确范围仍是 \(M=2\)、指定小非零均匀背景、包含该态的零组件均值叶及同一 KLTZ/invariant-factorization low 图。小背景半径依文献零邻域，不能用早期显式 spectral 小 \(\delta\) bound 自动替代。一般 \(M>2\) 的 nonlinear state inverse/closed span、regular common fibers、ordinary global action-angle 和任意 physical Cauchy 初态仍不在结论内。全有限 \(M\) 已证的是 actual trace classes 对合、与全部 \(C_n\) 对合及每个 fixed finite spectral/action-list（actions 已建立的 M2 情形）保持同一 strong presentation。

前面 §§2–6 的 one-smoothing/Fredholm route 保留为独立备用候选。KST2015 的 general-complex gain 已有原文支持，但把其具体 Birkhoff norming map 与本次 KLTZ2009 chart 的具体 normalization 适配，不能仅由共同 Fourier derivative 或“都是 canonical”推出；需要再核同一 norming-map 或指定 analytic transition 的 gain。当前 direct 主证明完全绕过这一待审适配，不以备用 (10)–(11) 为已证最大性的依赖。

报告可准确说“原弱辛相空间的非线性共同微分核最大性及实际 Hamilton 场的闭包完备性”，不可写“实际共同水平集已是 regular Lagrangian leaf”“physical Cartesian angles 已 canonical”“全 \(M\) nonlinear maximality”或“普通全场 Cauchy 可解”。
