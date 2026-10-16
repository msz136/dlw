# M=2 原物理场到一般 AKNS 的精确状态逆桥

2026-10-11。范围：(M=2,c\ne0)，固定一个已有 Hamiltonian 平均叶，采用 centered 谱参数；(S=2\delta\ne0)。本稿没有固定原时间自由参数 (c\Gamma)，没有以特殊解族替代一般函数。新增结果是物理场—AKNS 势的局部双解析图、物理像的精确中央谱约束及 gauge 截面，并在明确小邻域条件下得到全部非中央 Cartesian 谱坐标的完整状态逆。谱 actions 已在原物理 bracket 中严格对合，有限 action 流保持同一 strong 相域；原物理 angle brackets 与共同 fibers 的最大性仍须另证。

本稿 §§2–4.5 已经 [独立状态逆审计 §§3、6、9–13](akns_physical_state_inverse_independent_audit_20261011.md) 实际读回并手核；有限 action 的 strong 域接合另由 [strong 独审 §4](akns_actions_strong_domain_independent_audit.md) 核定。[全新符号核验脚本](verify_akns_physical_bridge_20261011.py) 的 [12 项结果](akns_physical_bridge_symbolic_checks_20261011.json) 全部通过，仅检查有限代数 identities，不代替 Banach/谱逆/无限维论证。原文来源与本地下载状态记录于 [Paper reference metadata](../../Paper/refs/akns_transfer_20261011/reference_access_20261011.md)。

后续 [同一 strong Hilbert 图中的 action 泛型证明](akns_actions_same_strong_chart_genericity_20261011.md) 已直接用实际 contour Hessian 给非空 residual 参数集：全部非中央 \(I_n\ne0\) 且每个有限 action 块在真正内部 plot 切向量上独立。其精确二次归一化为 \(I_{-n}^{[2]}=(Lk_n^2/(16S))Q_nP_n\)（旧 physical 正频率对应 KLTZ 负索引），原实源满足 \(I_{-n}=\overline{I_n}\)。该 residual 性只指同一固定 Hilbert 参数球，不推广为整个 strong 相域泛型。

## 1. 周期 gauge、实际 holonomy 与谱参数

令 (D=\partial_x)、

\[
\langle f\rangle=L^{-1}\int_0^Lf,\qquad P_0f=f-\langle f\rangle,
\qquad K=D_0^{-1}P_0.
\]

(Kf) 是唯一平均零的周期 primitive，(DK=KD=P_0)，在普通积分的双线性配对下 (K^*=-K)。始终使用这一 normalization，因而 (K) 与空间平移交换。

实际 free 物理场为平均零的 (u,v)，

\[
q=-S+u,\quad V=-2uv/S,\quad
r=\frac{(\delta^2-v^2)(1+u/S)-v_x}{S}.
\tag{1}
\]

split connection 是 (A_\lambda=\bigl(\begin{smallmatrix}\lambda&q\\r&V\end{smallmatrix}\bigr))。这里的 (\lambda) 已 centered；原参数为 (\lambda_{\rm orig})、(B=\Gamma/(2c)) 时取 (\lambda=\lambda_{\rm orig}-B)。先去 scalar trace，得到

\[
\mathcal A_\lambda=\frac{\lambda-V}{2}H+qE+rF.
\]

定义

\[
\eta=\langle V\rangle,\quad \theta=KV,\quad
G=\operatorname{diag}(e^{-\theta/2},e^{\theta/2}),\quad
a=e^\theta q,\quad b=e^{-\theta}r.
\tag{2}
\]

由于 (\theta_x=V-\eta)，令 trace-free split 解 (\psi=G w)，精确得到

\[
w_x=\left(\frac{\lambda-\eta}{2}H+aE+bF\right)w.
\tag{3}
\]

这是 constant-principal、两独立势的一般 AKNS。(G(L)=G(0))，故 AKNS monodromy 是 trace-free split monodromy 的基点共轭，normalized trace 完全相等。不能丢弃 (\eta)：原 centered determinant 是 (e^{(\lambda+\eta)L})，实际 slow holonomy 是 (e^{\eta L})，对应全频移动中心 (\lambda\mapsto\lambda-\eta)。若恢复 (B)，raw 原矩阵 determinant 是 (e^{(\lambda_{\rm orig}+B+\eta)L})，而 normalized trace 对应 (3) 的 (\lambda_{\rm orig}-B-\eta)。任意既定 (B(t)) 逐时均适用，未要求其守恒。

原 rank-one 到 split 的周期基变换为

\[
T(u,v)=\begin{pmatrix}(\delta+v)/S&1\\(\delta-v)/S&-1\end{pmatrix},
\qquad\det T=-1.
\tag{4}
\]

若 (N_\chi) 是原 trace-free normalized monodromy，则 AKNS full monodromy 为 (G(0)^{-1}T(0)^{-1}N_\chi T(0)G(0))。因此对完整 framed 数据，必须保留实际 endpoint calibration；只给 conjugacy-invariant trace 无法提供这一矩阵。规约不除以 (u,v,q)，因而不存在 (u=0) 的奇性。

## 2. 函数空间与非线性局部逆

记 (H^s_0=P_0H^s_{\rm per}(\mathbb C))。有两种精确、不同的 Sobolev 预算。

* balanced 源：(X_s=H^s_0\times H^s_0\)，(s\ge1)。由 (1)–(2)，(a\in H^s,b\in H^{s-1},\theta\in H^{s+1})，映射解析。
* mixed 源：(\widetilde X_s=H^s_0\times H^{s+1}_0\)，整数 (s\ge0)。此时 (a,b\in H^s,\theta\in H^{s+1})，映射解析。端点 (s=0) 也合法：(v\in H^1\hookrightarrow L^\infty)，所以 (uv\in L^2)、(\theta\in H^1)，(e^{\pm\theta}\in H^1\hookrightarrow L^\infty)，(1) 中全部项属于 (L^2)。更高阶使用一维乘法估计。

定义 projected potential map

\[
\Phi(u,v)=(P_0a,P_0b).
\tag{5}
\]

背景 (u=v=0) 给 (a_0=-S,b_0=S/4,\eta_0=\theta_0=0)。(V\) 为二次表达式，故背景一阶变分为

\[
D\eta_0=D\theta_0=0,\qquad
D\Phi_0(h,k)=\left(h,\frac h4-\frac{Dk}{S}\right).
\tag{6}
\]

其精确逆为

\[
(f,g)\longmapsto\left(f,S K(f/4-g)\right).
\tag{7}
\]

在 balanced 源上 (6) 是 (H^s_0\times H^s_0\to H^s_0\times H^{s-1}_0) 的有界复线性同构；在 mixed 源上是 (H^s_0\times H^{s+1}_0\to H^s_0\times H^s_0) 的有界复线性同构。解析 Banach 逆函数定理因此给每个上述固定 (s) 的开源邻域、开 projected-potential 邻域及唯一双解析逆。对实输入，所有 operations 保持共轭，唯一逆亦保持实型。这是完整一般函数状态逆，不是 finite-Fourier 截断或仅微分单射。

### 2.1 完整势的两个均值约束和 holonomy graph

设 ((u,v)=\Phi^{-1}(f,g))，定义解析标量

\[
\alpha(f,g)=\langle a\rangle,\quad
\beta(f,g)=\langle b\rangle,\quad
\gamma(f,g)=-\frac2S\langle uv\rangle.
\tag{8}
\]

完整势和 holonomy 的实际像精确为

\[
(a,b,\eta)=\left(f+\alpha(f,g),\ g+\beta(f,g),\ \gamma(f,g)\right).
\tag{9}
\]

其中 ((\alpha,\beta,\gamma)(0,0)=(-S,S/4,0))，其三个一阶微分均为零。对复化的物理源，完整 ((a,b)) 的像是相应复 product Sobolev 空间中 complex codimension-two 解析 graph；加上 (\eta) 后是 complex codimension-three graph。原实物理源的像另满足诱导的 reality 条件，不能说它在 full complex target 中仅有 real codimension two。任意独立 ((a,b)) 并不都来自该指定平均叶，任意独立 (\eta) 也不允许。给定完整势只需先投影再用 (7) 的非线性 IFT 逆；其均值是否满足 (8) 是必要且局部充分的 compatibility 检验。

也可把 compatibility 写成不除以 (u) 的精确 periodic ODE：

\[
u=S+a e^{-\theta},\quad
\theta_x=-2uv/S-\eta,\quad
v_x=(\delta^2-v^2)(2+a e^{-\theta}/S)-S e^\theta b,
\tag{10}
\]

并要求 (\langle u\rangle=\langle v\rangle=\langle\theta\rangle=0)。它是 (1)–(2) 的重写；(5)–(9) 已严格给其局部唯一实际解及 graph，不需假定 ODE 周期边值问题另有任意数据解。

### 2.2 同一个低阶 mixed 开域上的全部整数 Sobolev 阶

可以只在 (\widetilde X_0=L^2_0\times H^1_0) 使用一次 IFT，固定其物理开域 (\mathcal O_0) 与 projected-potential 开域 (\mathcal V_0\subset L^2_0\times L^2_0)。令 (f,g\in\mathcal V_0\cap(H^N_0)^2)，先用这份低阶唯一逆，获得 (u\in L^2,v\in H^1,\theta\in H^1)。由 (8) 补回 constants 后 (a,b\in H^N)。

对于 (N\ge1)，(10) 的第一式及 (H^1) 乘法代数先给 (u\in H^1)；随后第二、第三式给 (\theta,v\in H^2)。若已知 (u\in H^j,\theta,v\in H^{j+1})，且 (j<N)，第一式给 (u\in H^{j+1})，再由另两式给 (\theta,v\in H^{j+2})。有限归纳得

\[
u\in H^N,\qquad v,\theta\in H^{N+1}.
\tag{10b}
\]

反向包含来自 (1)–(2)。因此同一低阶 map 满足

\[
\Phi\bigl(\mathcal O_0\cap\widetilde X_N\bigr)
=\mathcal V_0\cap(H^N_0)^2
\quad\text{对全部整数 }N\ge0.
\tag{10c}
\]

所有 high-norm estimates 在较小低阶逆域和 bounded (H^N) data 上局部有界：初始 (u_{L^2},v_{H^1},\theta_{H^1}) 由低阶逆控制，每一步只用有限阶乘法与 (e^{\pm\theta}) 的 Sobolev 复解析估计。低阶 inverse 已 holomorphic，(10b) 与这些 locally bounded high norms 给其 (H^N)-valued holomorphic 性；等价地可微分 (10)，对低阶 inverse derivative 作同样 first-order bootstrap，然后逐高阶 IFT 与低阶唯一逆识别。因此 (10c) 是同一低阶开域各 Sobolev intersections 上的双解析逆，不要求逐 (N) 缩半径。

这只对 mixed 空间作了一份共同低阶状态图，未声称全部局部 (C_m) 同时在 (L^2\times H^1) 上定义。

## 3. 原物理 Poisson 的精确推前

原普通积分梯度的 Poisson tensor 是

\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\tag{11}
\]

以下 formal adjoint 均为双线性积分配对；实场上即通常 real adjoint。定义 multiplication operators

\[
A=(\delta^2-v^2)/S^2,\quad B=-2v(1+u/S)/S,\quad
c_1=-2v/S,\quad c_2=-2u/S,
\]

\[
M=\begin{pmatrix}1&0\\A&B-D/S\end{pmatrix},\quad
j=\binom q{-r},\quad c=(c_1,c_2),\quad
E_\theta=\operatorname{diag}(e^\theta,e^{-\theta}).
\]

直接微分 (2) 给完整势的精确 Fréchet derivative

\[
\Lambda=D_{(u,v)}(a,b)=E_\theta\left(M+jKc\right).
\tag{12}
\]

故对有可容许 smooth 梯度的函数，实际推前 bracket 为

\[
\boxed{J_{ab}=\Lambda J_{uv}\Lambda^*,\qquad
J_{fg}=\mathsf P\Lambda J_{uv}\Lambda^*\mathsf P,
\quad\mathsf P=\operatorname{diag}(P_0,P_0).}
\tag{13}
\]

这是完全指定、可逐项计算的局部与 nonlocal operator，而不是把未经匹配的 canonical AKNS bracket 放入物理场。若希望展开，其局部部分由

\[
MJ_{uv}M^*=-\frac1{16}
\begin{pmatrix}
0&D(B+D/S)\\
(B-D/S)D&(B-D/S)DA+AD(B+D/S)
\end{pmatrix}
\tag{14}
\]

给出；(12) 的 (jKc) 产生其余确定的 nonlocal terms。

背景尤其清楚：

\[
\Lambda_0=\begin{pmatrix}1&0\\1/4&-D/S\end{pmatrix},\quad
\boxed{J_{ab,0}=\begin{pmatrix}0&-D^2/(16S)\\D^2/(16S)&0\end{pmatrix}.}
\tag{15}
\]

其 order 为二；标准 NLS bracket 的 order 为零。因此由 AKNS/Birkhoff chart 的 canonical 性，不能直接推出物理 action-angle 性或原叶最大各向同性。

holonomy 的精确 Hamilton 场为

\[
X_\eta=\frac1{8SL}(u_x,v_x),\qquad
\{a(x),\eta\}=\frac{a_x(x)}{8SL},\quad
\{b(x),\eta\}=\frac{b_x(x)}{8SL}.
\tag{16}
\]

后两式依赖已选定的 translation-equivariant mean-zero (K)。这再次表明 (\eta) 不是新 Casimir；实际谱中心的场依赖不能在 Poisson 变分中略去。上述 smooth 张量身份并不自动说明 order-two tensor 对任意低阶 Sobolev dual 的无损延拓。

## 4. 可用的一般复 Birkhoff 原文及精确适用范围

[Kappeler–Lohrmann–Topalov–Zung 2009](https://doi.org/10.1007/s00220-008-0543-0) 的 published full text 已核对，重点是 **§2.5, Proposition 2.9, p.1098**，而不是 abstract 或仅 focusing 实型的 Theorem 1.1。[原文 PDF 镜像](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf) 的 PDF 第13页即纸本1098页；镜像额外第1页为封面。该命题给一般 (L^2(\mathbb T,\mathbb C)^2) 的零邻域 (W) 到一般复序列邻域 (U) 的双解析 Birkhoff 逆，保 standard NLS bracket；每个 (N\ge0) 有 (H^N\times H^N\leftrightarrow h^N\times h^N) 同阶逆。actions 是谱判别式 contour expressions，并用于 regular Cartesian coordinates；复杂 potentials 不必满足 focusing/defocusing reality。此处只借其谱图与状态逆，不借其 canonical 性当作物理 canonical 性。

为了准确匹配该文 operator convention，先作 fixed diagonal balancing：

\[
R=\operatorname{diag}(\sqrt2,1/\sqrt2),\quad
\widetilde a=a/2,\quad \widetilde b=2b.
\]

取 (t=x/L\)、(\zeta=(\lambda-\eta)/2\)，(3) 的 operator 等价于 period-one ZS operator

\[
\mathcal L_{\rm KLTZ}=iH\partial_t+
\begin{pmatrix}0&\varphi_1\\\varphi_2&0\end{pmatrix},\quad
\varphi_1(t)=-iL\widetilde a(Lt),\quad
\varphi_2(t)=iL\widetilde b(Lt),
\]

\[
z= iL\zeta=\frac{iL}{2}(\lambda_{\rm orig}-B-\eta).
\tag{17}
\]

Its discriminant is exactly the original normalized monodromy trace with this affine, state-dependent parameter correspondence. Background is (\varphi^0=(iL\delta,iL\delta)), with (L^2) pair norm (\sqrt2L|\delta|). It belongs to the focusing real slice, but a general real (u,v) gives two independent imaginary components and leaves that slice.

The precise transfer statement is conditional on (\varphi^0\in W): since (W) is open, shrink one lowest mixed-source inverse domain so its image stays in (W). Proposition 2.9 and §2.2 then apply on this same low domain at all integer Sobolev levels. The composite KLTZ map embeds the **complexified** physical (H^N_0\times H^{N+1}_0) source onto a complex codimension-two analytic submanifold of (h^N\times h^N), with unique analytic inverse obtained by KLTZ inverse, fixed balancing/rescaling inverse, projection (P_0(a,b)), and (5). The original real physical image additionally obeys the transported reality condition. These are full Cartesian spectral state coordinates on the actual image. Some sufficiently small (L|\delta|>0) satisfies the condition; the paper supplies no numerical radius, so (0<|\delta|<\pi/L) alone does **not** establish (\varphi^0\in W).

On the original balanced (H^s\times H^s) source, the potential orders differ. Applying KLTZ at order (s-1) alone loses one order on (u); it does not prove the earlier desired same-order (H^s\to h^{s+1/2}) chart. The weighted mixed-space transfer above is a new legitimate inverse bridge with its stated domain, not a replacement for that stronger assertion.

### 4.1 Reality checks for the two RHP papers

[Biondini–Zhang, arXiv:2311.18127v3](https://arxiv.org/html/2311.18127v3), §1 (1.3), assumes lower potential (q^*); [Biondini et al. Physica D 483 (2025), 134970](https://math.buffalo.edu/~biondini/papers/physd2025v483p134970.pdf), §1 (1.3), assumes lower potential (-q^*). Both use (C^2) potentials in their main formalism. Thus neither RHP theorem directly treats our generic independent (a,b). In contrast, KLTZ Proposition 2.9 explicitly complexifies both potentials and does apply under its neighborhood condition. Failure of an NLS real slice is not a valid reason to discard that complex theorem.

### 4.2 原物理 action family 的严格对合和 order-zero Hamilton 场

以下另用已经严格证明的原物理 identities：全部固定参数 (\mathcal F_\lambda\) 彼此对合、与 (\eta\) 对合、与每个有定义的局部 (C_m\) 对合；(\eta\) 与局部 (C_m\) 的对合来自平移不变性。**不使用** KLTZ canonical bracket。

以 (z\) 表示 (17) 的 dimensionless period-one spectral parameter，写

\[
\Delta(z;u,v)=\mathcal F_{\lambda(z;u,v)}(u,v),\qquad
\lambda(z;u,v)=\eta(u,v)-2iz/L.
\tag{A1}
\]

若写原 noncentered parameter，右边即 (\mathcal F_{\Gamma,B+\eta-2iz/L}\)。固定 (B\) 在当前物理叶上作参数；任意既定时间 (B(t)\) 仍按既有 centered 规范。

谱参数对源的 chain rule 为

\[
d\Delta(z)=d\mathcal F_\lambda+\partial_\lambda\mathcal F_\lambda\,d\eta.
\tag{A2}
\]

对任意两个 (z,w\)，逐项使用上述物理对合恒等式，得到

\[
\{\Delta(z),\Delta(w)\}_{uv}=0,\quad
\{\Delta(z),\eta\}_{uv}=0,\quad
\{\Delta(z),C_m\}_{uv}=0.
\tag{A3}
\]

This calculation includes the source-dependent shift; differentiating at fixed (\lambda\) alone would omit the second term of (A2).

采用 KLTZ §2.3 formula (2.15) 的标准 branch (R(z)=\sqrt[c]{\Delta(z)^2-4}\) 及 counterclockwise contour (\Gamma_n\)，其 action normalization 是

\[
I_n=\frac1\pi\oint_{\Gamma_n}
z\frac{\partial_z\Delta(z)}{R(z)}\,dz.
\tag{A4}
\]

缩到一个连接零势的小 complex ball (W\)；每个固定 (\Gamma_n\) 避开该 ball 上的两 branch points，包围该 pair，(R\) 在轮廓的 annulus 上单值且非零。源解析性允许轮廓与 Fréchet 变分交换。周期分部积分给

\[
dI_n=-\frac1\pi\oint_{\Gamma_n}\frac{d\Delta(z)}{R(z)}\,dz.
\tag{A5}
\]

Indeed (d[\Delta_z/R]=\partial_z[d\Delta/R]\)，且 (\oint\partial_z(z\,d\Delta/R)dz=0\)。(d\Delta/R\) 在该 annulus 上单值即可，不要求 arcosh 全局单值。

这里 (A2) 中的 holonomy variation term **精确消失**。因为

\[
\oint_{\Gamma_n}\frac{\partial_\lambda\mathcal F_\lambda}{R}\,dz
=\frac{iL}{2}\oint_{\Gamma_n}\frac{\Delta_z}{R}\,dz
=\frac{iL}{2}\oint_{\Gamma_n}d\log(\Delta+R)=0.
\tag{A6}
\]

最后一个 integral 的 (2\pi i\) 倍数为 nonzero function (\Delta+R\) 的 winding number；它从不为零，因为 ((\Delta+R)(\Delta-R)=4\)。在连接零势的小 (W\) 上该整数不变。零势时 (\Delta=2\cos z,R=-2i\sin z\)，故 (\Delta+R=2e^{-iz}\)，winding number 为零。相反 root convention 也给 (2e^{iz}\)，仍为零。This argument is uniform as a statement for each fixed action contour, without imposing all-frequency operator estimates.

所以实际物理 Hamilton 场的 exact formula 是

\[
\boxed{X_{I_n}=-\frac1\pi\oint_{\Gamma_n}
\frac{X_{\mathcal F_\lambda}}{R(z)}\,dz,
\qquad\lambda=\eta-2iz/L.}
\tag{A7}
\]

每个 fixed (n\) 上 (X_{\mathcal F_\lambda}\) 对 compact 参数集为 (H^s\to H^s\) 的解析 order-zero 场，(s\ge1\)，因此 (A7) 亦为同一 balanced (H^s\) 源上的解析 order-zero 场。小球需使实际势落入 (W\)、(R\) 在该 fixed contour 上远离零；不需在任何一个低阶源 norm 上控制全部高阶局部 charges。

(A3)、(A5) 精确给

\[
\{I_n,I_j\}_{uv}=\{I_n,\eta\}_{uv}
=\{I_n,\mathcal F_\mu\}_{uv}
=\{I_n,C_m\}_{uv}=0.
\tag{A8}
\]

在真实实场上取 (\operatorname{Re}I_n,\operatorname{Im}I_n\) 及相应实型 Hamilton 场，仍相互对合。它们有真实局部 (H^s\) Banach Picard 流，保持各源均值、全部可定义的 (C_m\) 和 actual Floquet family。沿这些流 (\eta) 与全部 (\mathcal F_\lambda) 恒定，因此 (A7) 的 centered spectral path 与 scalar weights 可沿轨道冻结。

[strong 域 action 独审 §4](akns_actions_strong_domain_independent_audit.md) 已逐项核定既有 strong flow bridge 的输入：低阶 order-zero 解析、translation equivariance、全部 \(C_m\) 的严格对合和实际 finite mixed uniqueness。一次冻结旧轴窗口，在同一 low ball 上取新谱时间；该时间不随旧层级前缀缩小。输送后的 joint germs 通过 mixed corner 重参数和实际唯一性识别，反向时间给局部逆。因此每个固定 action 的实型流以及任意有限组已选 action 时间均保持**同一** weak-symplectic \(\mathfrak S_\infty\) strong diffeology，并有内部 Hamilton 场。这里没有无限个同时非零谱时间，也未将该 diffeology 宣称为 Hilbert/Fréchet manifold。

这补上了 weighted inverse chart 的 **原物理谱 Hamiltonian family**；actions 的数值未要求 NLS 实性或非负。原物理 angles、maximality 和 action-gradient completeness 仍未由 (A8) 得到。

### 4.3 物理像的纯谱 hypersurface 与常数对角 gauge 截面

这里给 (9) 的两个均值 graph 一个更具体的、完全非线性的谱解释。全部陈述先在 complexified mixed 源与 full complex AKNS 势空间中成立；原实物理源再取相应 real restriction。本节不把标准 NLS Poisson reduction 当作原物理 reduction。

原 trace-free rank-one connection 的准确公式是既有 spectral 独审 (74)：

\[
\mathsf L_\lambda=
\begin{pmatrix}
u/2+\lambda v/S&(\delta+v)(1+\lambda/S)\\
(\delta-v)(\lambda/S-1)&-u/2-\lambda v/S
\end{pmatrix}.
\tag{B1}
\]

因而

\[
\mathsf L_S=(u/2+v)H+2(\delta+v)E,\qquad
\mathsf L_{-S}=(u/2-v)H-2(\delta-v)F.
\tag{B2}
\]

两矩阵分别上、下三角，且物理平均叶满足 \(\int u=\int v=0\)。monodromy 的两个对角 entry 均为一，故对所有该叶物理场有精确身份

\[
\boxed{\mathcal F_S=\mathcal F_{-S}=2.}
\tag{B3}
\]

这里 Floquet multiplier 一可以是 Jordan，不能从 trace 二推出 monodromy 为 identity。

在完整 AKNS 势 \((A,B)\) 的背景 \((a_0,b_0)=(-S,S/4)\) 附近，令 \(z_\pm(A,B)\) 为 \(\Delta_{A,B}(z)=2\) 中分别位于 \(\pm iL\delta\) 两个不相交小 disc 内的根。这里是固定 disc 标签，\(\delta<0\) 时也不改作 lexicographic 排序。背景

\[
\Delta_0(z)=2\cos\sqrt{z^2+L^2\delta^2},\qquad
\partial_z\Delta_0(\pm iL\delta)=\mp2iL\delta\ne0.
\tag{B4}
\]

故它们在 full \(L^2\times L^2\) 的足够小邻域上各自解析；这只用简单根 IFT。定义纯 discriminant 函数

\[
\chi(A,B)=\bigl(z_+(A,B)-z_-(A,B)\bigr)^2+L^2S^2.
\tag{B5}
\]

若 \(\varphi^0\in W\) 且背景及源邻域足够小，它们正是 KLTZ 的 \(n=0\) periodic pair。否则本节仍在这两个标定根的局部邻域成立，不依赖 KLTZ 定理。

对实际物理势，(B3)、参数恒等式 (17) 与简单根唯一性给

\[
z_\pm(a,b)=\frac{iL}{2}(\pm S-\eta),\quad
z_+-z_-=iLS,\quad
\frac{z_++z_-}{2}=-\frac{iL\eta}{2}.
\tag{B6}
\]

因此 \(\chi(a,b)=0\)，并且在物理像上 holonomy 由中央谱对唯一恢复：

\[
\eta=\frac{2i}{L}\frac{z_++z_-}{2}.
\tag{B7}
\]

下面证明 \(\chi=0\) 的局部充分性，允许一个常数 diagonal gauge。定义

\[
\Psi(u,v,\tau,\sigma)=
\bigl(e^\tau a(u,v),\ e^{-\tau}b(u,v)+\sigma\bigr),
\quad
(u,v,\tau,\sigma)\in L^2_0\times H^1_0\times\mathbb C^2.
\tag{B8}
\]

其背景微分及精确线性逆为

\[
D\Psi_0(h,k,t,s)=
\left(h-St,\frac h4-\frac{Dk}{S}-\frac{St}{4}+s\right),
\tag{B9}
\]

\[
t=-\frac{\langle A_1\rangle}{S},\quad
s=\langle B_1\rangle-\frac{\langle A_1\rangle}{4},\quad
h=P_0A_1,\quad
k=SK\bigl(h/4-P_0B_1\bigr).
\tag{B10}
\]

这是 onto full \(L^2\times L^2\) 的有界复线性同构。解析 Banach IFT 给唯一 local chart \(\Psi\)。在该 chart 中，\(\tau=\sigma=0\) 正是原物理势像；\(\sigma=0\) 正是其常数 gauge saturation。常数 diagonal conjugation 不改变 discriminant，所以 \(\chi\circ\Psi(u,v,\tau,0)=0\) 恒等。

为排除另一支 hypersurface，准确计算其 transverse derivative。对任意 AKNS 势扰动 \((A_1,B_1)\)，在背景根处 nilpotent constant matrix 的 Duhamel 公式给

\[
d\Delta_0(z_\pm)=L^2
\bigl(b_0\langle A_1\rangle+a_0\langle B_1\rangle\bigr).
\tag{B11}
\]

事实上 unscaled spectral variable \(\zeta=z/(iL)\) 下 \(M_\pm^2=0\)，
\(e^{LM_\pm}=1+LM_\pm\)；variation trace 是
\(L\,\mathrm{tr}(M_\pm\int\delta Q)=L^2(b_0\langle A_1\rangle+a_0\langle B_1\rangle)\)。
由 (B4) 隐函数微分得

\[
d\chi_0(A_1,B_1)
=4L^2\bigl(b_0\langle A_1\rangle+a_0\langle B_1\rangle\bigr)
=-4SL^2\left(\langle B_1\rangle-\frac{\langle A_1\rangle}{4}\right).
\tag{B12}
\]

结合 (B9)，\(\partial_\sigma(\chi\circ\Psi)(0)=-4SL^2\ne0\)。
在小 chart 内的解析 Hadamard factorization 因而为

\[
\chi\circ\Psi=\sigma g(u,v,\tau,\sigma),\quad
g=\int_0^1\partial_\sigma(\chi\circ\Psi)(u,v,\tau,t\sigma)\,dt,\quad
g(0)=-4SL^2,\quad g\ne0.
\tag{B13}
\]

于是得到 exact local image 定理：

\[
\boxed{\ \chi(A,B)=0
\quad\Longleftrightarrow\quad
(A,B)=(e^\tau a(u,v),e^{-\tau}b(u,v))
\text{ for a unique small }(u,v,\tau).\ }
\tag{B14}
\]

原物理像是该纯中央 gap-width hypersurface 的 local gauge section \(\tau=0\)；其选择由 mean-zero primitive 及实际状态图确定。证明用了显式 transverse derivative 和解析因子，未用仅维数计数。对于高阶 data，在 \(\sigma=0\) 先由低阶 chart 得标量 \(\tau\)，还原实际 \(a,b\)，再用 §2.2 bootstrap，故同一低阶 chart 的 hypersurface 与 section 在每个 \(H^N\times H^N\) intersection 上仍成立。

应用 KLTZ 双解析谱图，可以将这个纯谱 hypersurface 和 gauge section 原样搬到 full Cartesian Birkhoff 坐标。它明确了原物理像的形状，也使 holonomy 本身成为像上的谱函数。以下再严格证明其 action 形式和一份完整 reduced Cartesian 状态图；原物理 Poisson quotient 最大性仍不由这些坐标证明。

### 4.4 全复 discriminant 的 action factorization 与中央 action 约束

本节的 canonical 计算**只用于描述 AKNS 谱图**，全部带下标 NLS；它不改变 (11)–(15) 的原物理张量。KLTZ Proposition 2.9 直接保证谱图双解析及 canonical，但其 item (ii) 只显式说 NLS Hamiltonian 依赖 actions，不能把它误读成现成的全 discriminant 声明。下面给后一声明的自足证明。

period-one 变量下令

\[
U_z=-izH+iH\begin{pmatrix}0&\varphi_1\\\varphi_2&0\end{pmatrix},
\quad M_z(t)=X_z(t)X_z(1)X_z(t)^{-1}.
\tag{C1}
\]

于是 \(M_z'=[U_z,M_z]\)，\(M_z(1)=M_z(0)\)，
\(\partial_{\varphi_1}\Delta_z=i(M_z)_{21}\)，
\(\partial_{\varphi_2}\Delta_z=-i(M_z)_{12}\)。
对论文 (1.2) 的标准括号
\(\{F,G\}_{\rm NLS}=i\int(F_1G_2-F_2G_1)\,dt\)，直接算

\[
\partial_t\operatorname{tr}(M_zM_w)
=-2i(z-w)\bigl((M_z)_{12}(M_w)_{21}
-(M_z)_{21}(M_w)_{12}\bigr),
\]
\[
\{\Delta_z,\Delta_w\}_{\rm NLS}
=\frac1{2(z-w)}\int_0^1
\partial_t\operatorname{tr}(M_zM_w)\,dt=0.
\tag{C2}
\]

同参数由连续性得到。该计算在 \(L^2\) 势上也成立：fundamental matrix 属 \(H^1\)，乘积 identities 属 \(W^{1,1}\)，可作周期积分。结合 action variation (A5)，
\(\{\Delta_z,I_n\}_{\rm NLS}=0\) 对所有 \(n\) 成立。
因此在 KLTZ 的 Cartesian 图 \((x_n,y_n)\) 上，每个 analytic \(\Delta_z\) 对每一个有限坐标平面的实旋转均不变。

这里保留一个无限维 analytic invariant 引理，避免把“每个有限子系统成立”当作全序列结论。令 analytic \(F\) 定义于 \(\ell^2\times\ell^2\) 的零球，且对各坐标平面旋转不变。取较小半径 \(r\)，在该球有界 \(M\)，Taylor homogeneous polynomials 满足
\(\lVert p_k\rVert\le Mr^{-k}\)。在任意 finite-support 子空间，旋转 invariant ring 由

\[
I_n=(x_n^2+y_n^2)/2
\tag{C3}
\]

生成，所以奇次 \(p_k\) 为零，\(p_{2m}=q_m(I)\)，其中 \(q_m\) 在有限支撑 actions 上为兼容的 \(m\) 次齐次多项式。任取 \((I_n)\) 有限支撑，选择 \(x_n=\sqrt{2I_n},y_n=0\)，有

\[
|q_m(I)|\le M\left(\frac2{r^2}\right)^m
\lVert I\rVert_{\ell^1}^{m}.
\tag{C4}
\]

复 polarization 将这个 diagonal bound 转为统一的 \(m\)-linear bound，额外常数至多 \(m^m/m!\)，与 support 大小无关。由有限序列在 \(\ell^1\) 中稠密，polarized forms 唯一延拓；其 diagonal \(q_m\) 仍满足 (C4)。故
\(\widehat F(I)=\sum_mq_m(I)\) 在 \(2\lVert I\rVert_{\ell^1}<r^2\) 的球内正常收敛，给 \(\ell^1\)-holomorphic 函数，且

\[
F(x,y)=\widehat F\bigl((I_n)\bigr).
\tag{C5}
\]

等式先在 finite-support coordinates 上成立，再用 \(\ell^2\to\ell^1\) 的 quadratic map 连续性及稠密性。对 compact spectral \(z\) 集，Volterra bounds 与 KLTZ inverse bounds 给一致的 \(M\)，所以 \(\Delta(z)\) 的这个 factorization 对 \(z\) 联合解析。它是本稿证明，不是借用未经核实的“全 hierarchy theorem”。

取 \(B_r(0)\) 于 KLTZ target 并再要求实际常背景在这个小图中。由 (C2)–(C5) 有

\[
\Delta(z)=d(z,I),\quad
\chi=\widehat\chi(I),\quad
\eta\big|_{\rm physical}
=\frac{2i}{L}\frac{z_+(I)+z_-(I)}2.
\tag{C6}
\]

后两个式子由中央简单根 IFT 得到，仅在 \(I\) 靠近常背景 \(I^*\) 时使用；**未在零 action 点把两个简单根硬拆开**。

精确 normalization 可由恒势 contour 直接求出。置 \(c=L^2AB\)，则
\(\Delta=2\cos\sqrt{z^2-c}\)，
\(R=-2i\sin\sqrt{z^2-c}\)，中央 pair 外取 \(\sqrt{z^2-c}\sim z\)。因此

\[
I_0=-\frac i\pi\oint
\frac{z^2}{\sqrt{z^2-c}}\,dz=c,\qquad
I_n=0\ (n\ne0).
\tag{C7}
\]

中央 integral 的 \(1/z\) 系数为 \(c/2\)；非中央闭隙 contour 的 integrand 在盘内解析。这个计算沿小恒势 family 合法，并给

\[
I_0^*=-L^2S^2/4\ne0,\qquad
\widehat\chi(I_0,0)=4I_0+L^2S^2,\qquad
\partial_{I_0}\widehat\chi(I^*)=4.
\tag{C8}
\]

还要辨认 Cartesian 背景，不能从复 product \(I_n=0\) 单独推出 \(w_n=z_n=0\)。KLTZ §2.5 对 defocusing 实型明确将闭隙处的 \((x_n,y_n)\) 定义为 \((0,0)\)。对小的恒势实型 \(\varphi_2=\overline{\varphi_1}\)，每个非中央隙闭合，所以全部 \(n\ne0\) Cartesian 坐标为零。对固定 \(n\)，这些坐标限制在恒势参数 \((\varphi_1,\varphi_2)\in\mathbb C^2\) 后是 holomorphic；上述 real-type plane 是最大 totally real plane。由其 analytic identity theorem，这个零值延拓到全部小复恒势。因此我们的 focusing 常背景也有 \(w_n^*=z_n^*=0\) 对全部 \(n\ne0\)。这里使用了具体闭隙 Cartesian 定义及 holomorphic extension，没有作 product-zero 推断。

所以 \(\ell^1\) 上的 scalar analytic IFT 给唯一函数

\[
\chi=0\quad\Longleftrightarrow\quad
I_0=\rho\bigl((I_n)_{n\ne0}\bigr),\qquad
\rho(0)=-L^2S^2/4.
\tag{C9}
\]

这是原物理像的中央 action 约束，含完整其他 action 序列；未固定原 \(c\Gamma\) 或人为删除 holonomy。

### 4.5 gauge 的精确 Birkhoff 作用与 reduced Cartesian 状态逆

标准 NLS mass

\[
\mathcal M=\int_0^1\varphi_1\varphi_2\,dt=L^2\langle AB\rangle
\tag{D1}
\]

的 canonical Hamilton 场（约定 \(X_F(q)=\{q,F\}_{\rm NLS}\)）是
\((i\varphi_1,-i\varphi_2)\)。它的 real time \(2\pi\) 流为 identity，并保持 \(L^2\) norm。这个流在势上就是 constant diagonal gauge。它保持 \(\Delta\) 与每个 contour action，故在 KLTZ 图中 \(\mathcal M=m(I)\)，由与 (C5) 相同的 invariant 引理可取 \(\ell^1\)-analytic \(m\)。

这里也可以自足核定通常的 trace identity，而不把它作为额外文献假设。定义

\[
w_n=(x_n+iy_n)/\sqrt2,\quad
z_n=(x_n-iy_n)/\sqrt2,\quad I_n=w_nz_n.
\tag{D2}
\]

有 \(\{w_n,z_j\}_{\rm NLS}=-i\delta_{nj}\)。因此 mass 流给
\(w_n(t)=e^{-i(\partial_{I_n}m)t}w_n(0)\)，
\(z_n(t)=e^{i(\partial_{I_n}m)t}z_n(0)\)。
由 KLTZ 图在零点的连续性，先选 potential \(L^2\) 的 \(\varepsilon\) 球，使**整个球**映入 (C4)–(C5) 使用的 target factorization 球。再取更小的 action 球，保证 balanced Cartesian representative 的 KLTZ inverse 在这个 \(\varepsilon\) 球内。mass 保 potential norm，故其整条 real \(0\le t\le2\pi\) orbit 均位于同一 factorization 球。对有限支撑 small actions 且 \(I_n\ne0\) 的代表，time \(2\pi\) identity 强制 \(\partial_{I_n}m\in\mathbb Z\)。该 analytic 函数在连通 small action 域中恒定，含 \(I_n=0\) 时由连续性补齐。论文 Proposition 2.9(iii) 的准确 Fourier derivative (2.21) 给零点二次项
\(\mathcal M^{[2]}=\sum_n I_n\)，所以每个整数恰为一。由 finite-support actions 稠密与 \(\ell^1\) 连续性得

\[
\boxed{\mathcal M=\sum_{n\in\mathbb Z}I_n.}
\tag{D3}
\]

这也核定了 mass normalization。complex gauge parameter \(\tau\) 对应 canonical mass time \(t=-i\tau\)，故全部谱坐标上

\[
(A,B)\mapsto(e^\tau A,e^{-\tau}B)
\quad\Longleftrightarrow\quad
(w_n,z_n)\mapsto(e^{-\tau}w_n,e^\tau z_n).
\tag{D4}
\]

此式先由 real mass 流得到，再以 holomorphic identity 延拓到 small complex \(\tau\)。

因为 \(I_0^*\ne0\)，在常背景附近 \(w_0,z_0\ne0\)，可固定一支

\[
\vartheta_0=\frac1{2i}\log(w_0/z_0).
\tag{D5}
\]

它在 gauge 下精确改变为 \(\vartheta_0+i\tau\)。因此
\(\chi=0,\vartheta_0=\vartheta_0^*\) 是该 hypersurface 的另一份 local gauge section，和 (B14) 的实际物理 section 通过唯一 small gauge 双解析对应。

现在任意给足够小的全部非中央 Cartesian 序列
\((w_n,z_n)_{n\ne0}\in h^N\times h^N\)。其 products 是 \(\ell^1\) actions；用 (C9) 补回 \(I_0\)，再用 (D5) 的固定角及 \(w_0z_0=I_0\) 唯一补回中央 pair。KLTZ inverse 给一份 \(\chi=0\) AKNS 势，(B14) 唯一去除常数 gauge 给实际物理势，§2 给唯一 \((u,v)\)。反向由实际物理势先调到固定中央角，再读出非中央序列。由 §2.2、KLTZ 同低域高阶逆及 constant gauge 的有界性，得到同一 low-domain 各整数阶上的精确状态图：

\[
\boxed{\ 
(u,v)\in H^N_0\times H^{N+1}_0
\quad\longleftrightarrow\quad
(w_n,z_n)_{n\ne0}\in h^N\times h^N
\text{ in corresponding local open sets.}\ }
\tag{D6}
\]

该图对 complexified source 是双解析，覆盖一般函数邻域；原 real source 另取诱导 reality。它不要求任何非中央 action 非零：Cartesian 坐标同时覆盖闭隙。若只在全部所选 \(I_n\ne0\) 的局部区域讨论，才可以逐坐标再选 action/angle。

准确的共同域意思是：先在 \(h^0\times h^0\) 的非中央序列上完成上述有限 scalar IFT、固定 log/root 分支和唯一 gauge 选择，得开域 \(\mathcal U_{\rm red}\)，再以实际低阶状态逆定义对应 \(\mathcal O_{\rm red}\subset L^2_0\times H^1_0\)。这些 scalar choices 只依赖 low norm，与 \(N\) 无关。前向的 high potential map、KLTZ 图和 constant gauge 都保持 \(H^N/h^N\)；反向的 KLTZ inverse、constant gauge 和 §2.2 bootstrap 同样保持各高阶。因此
\[
\mathcal O_{\rm red}\cap(H^N_0\times H^{N+1}_0)
\ \longleftrightarrow\
\mathcal U_{\rm red}\cap(h^N\times h^N)
\quad(N\ge0)
\tag{D7}
\]
为同一 low 图的双解析 restrictions。不能把原 real image 当作标准 NLS 实型：其 reality 是将 \((u,v)\mapsto(\bar u,\bar v)\) 通过这份整图搬来的 analytic anti-involution；取其 fixed set 才恢复实际 real state inverse。

完整 discriminant 由非中央 actions 和 (C9) 决定，所以这些是实际 reduced 图上的谱 fiber 描述；\(\vartheta_n\) 是谱图中的角变量名称。式 (D3)–(D6) **没有声称**这些角对原物理 (13) canonical、Hamilton 场具有标准 NLS 速度、common action-gradient 闭包已占满 fiber tangent，或任一真实 strong-coherent 层已成为 Hilbert/Fréchet manifold。后面的物理 Poisson 与 nonlinear maximality 问题仍须单独完成。

## 5. A second usable inverse result without a near-zero AKNS condition

[Yang–Yurko, Recovering Dirac Operator with Nonlocal Boundary Conditions, arXiv:1503.01748](https://arxiv.org/html/1503.01748v1), §1 and **Theorem 2** allow two independent complex, absolutely continuous Dirac coefficients. The theorem is inverse uniqueness from two fixed boundary spectra; it does not assert a weighted Banach analytic inverse.

For the unbalanced (a,b) in (3), set

\[
C=\begin{pmatrix}1&1\\i&-i\end{pmatrix},\quad
J_D=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\quad y=Cw.
\]

Then (J_DC=CiH), and the exact equivalent finite-interval Dirac equation is

\[
J_Dy_x+\Omega y=z_Dy,\quad z_D=i(\lambda-\eta)/2,
\quad\Omega=-CiH\begin{pmatrix}0&a\\b&0\end{pmatrix}C^{-1}
=\frac12\begin{pmatrix}i(b-a)&a+b\\a+b&i(a-b)\end{pmatrix}.
\tag{18}
\]

For its normalized full monodromy (X_D\), take fixed left boundary (y_1(0)=0) and the two right boundaries (y_1(L)=0), (y_2(L)=0). The two spectra are the zero multisets of ((X_D)_{12}) and ((X_D)_{22}). Their characteristic functions cannot have a common zero, since \(\det X_D=1\). These are precisely a specialization of the theorem's (U_1,V_1,V_2\), requiring no selfadjoint/skewselfadjoint reality. Absolute continuity follows for smooth physical fields, or for mixed (H^N\times H^{N+1}\) with (N\ge1\).

Consequently, on the local state domain of §2, equality of **calibrated two-boundary spectra plus \(\eta\)** implies equality of (a,b\) by Theorem 2, and hence equality of original (u,v\) by (5). This is a non-small-\(\delta\) framed inverse injectivity statement. It is not uniqueness from Floquet branch points alone, and no claim of norming-coordinate continuity, weighted surjectivity or action-angle normal form is obtained from it.

## 6. What has and has not been obtained

The exact local potential state inverse (5)–(10c) and pure spectral hypersurface plus constant-gauge section (B14) hold for every fixed (S\ne0); no small-(c) assumption is used. After the explicit further small-background and invariant-factorization ball conditions, (C9) removes the central action and (D6)–(D7) gives full noncentral weighted Cartesian spectral state coordinates on one common low domain. Equations (A1)–(A8) supply their actions as an actual commuting order-zero physical Hamiltonian family. Yang–Yurko supplies a separate general-complex framed two-spectra injectivity route without that small-background test.

Still unproved: the physical action/norming Poisson matrix for (13); regularity and maximal isotropy of actual common fibers on the original physical leaf; whether the full spectral state chart describes the strong mixed-coherent subset as a regular fiber/manifold; extension of these (M=2) bridges to all (M). Actual fixed finite action flows themselves now preserve the same strong diffeology by the separate flow audit. The local state chart (D6) and this flow result do not close the remaining physical completeness dependencies.
