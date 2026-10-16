# 全 M 有界有理周期 gauge 核与实际 Hamilton 场：精确 residue 桥

2026-10-11。由已审全 M R tensor 和新物理 coefficient图继续推进共同谱微分核。本稿只写一个严格可证明的子类：对谱参数有界有理、有限简单极点的周期 gauge directions。没有把一般 local-holomorphic gauge 自动提升为这个子类，亦未证明完整 Hamilton closure。未运行机器检查，未重跑证书。

依赖：[谱主稿 §16](../../刘维尔可积性/research/spectral_independent_review_20261011.md) (103)–(114)，[一般 M physical coefficient图](all_m_physical_holonomy_state_inverse_20261011.md) §§3、6、8，以及 [cyclic actual monodromy 核引理](all_m_cyclic_monodromy_gauge_kernel_20261011.md)。

## 1. 原物理 actual trace 场的全谱 gauge generator

固定 S≠0、component means，以及一个当前 spatialconstant B 截面。以下 λ=λ_original−B 是 centered 参数；这不添加 B_t=0 条件。用原准确 free坐标 Δ_first,d_first，原普通积分 Poisson张量是
\[
J=-\frac1{16}\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix},\qquad m=M-1.
\tag{1}
\]
原 traceless actual connection 为
\[
L_\lambda=\sum_i\Delta_iH_i-\lambda I/M+\sum_id_iK_i(\lambda/S),
\quad H_i=E_{ii}-I/M,
\quad K_i(a)=\sum_j(a+s_{ij})E_{ij},
\tag{2}
\]
s_ij=sgn(j−i)，d_m=S−Σ_{j<m}d_j、Δ_m=0。

实际 F_{μ,r}=r⁻¹trN_μ^r 的 periodic adjoint是
\[
W_{\mu,r}=Y_\mu N_\mu^rY_\mu^{-1},\qquad
W'=[L_\mu,W],\quad W(L)=W(0).
\tag{3}
\]
令 a=λ/S、b=μ/S，并使用已证明的 tensors
\[
B_{ab}=\sum_i[H_i\otimes K_i(b)+K_i(a)\otimes H_i],
\quad C^+_{ab}=R_{ab}+B_{ab}/2,
\quad C^-_{ab}=R_{ab}-B_{ab}/2.
\]
原 R 恒等式准确为
\[
[C^+,L_\lambda\otimes I]+[C^-,I\otimes L_\mu]=0.
\tag{4}
\]
定义 partial trace 的实际 periodic矩阵
\[
\boxed{\quad
g_{\lambda;\mu,r}
=-\frac1{16}\operatorname{tr}_2
\big[C^+_{ab}(I\otimes W_{\mu,r})\big].\quad}
\tag{5}
\]
它 trace-free。将 (4) 与 W收缩给
\[
[L_\lambda,G]=\operatorname{tr}_2[C^-(I\otimes W')],
\quad G=\operatorname{tr}_2[C^+(I\otimes W)].
\]
因 C±独立于 x，G'−[Lλ,G]=tr₂[B(I⊗W')]。而由原 J 和实际 gradient，物理 connection variation准确为
\[
\delta_{X_{F_{\mu,r}}}L_\lambda
=-\frac1{16}\operatorname{tr}_2[B_{ab}(I\otimes W')].
\]
故
\[
\boxed{\quad
\delta_{X_{F_{\mu,r}}}L_\lambda
=(g_{\lambda;\mu,r})'-[L_\lambda,g_{\lambda;\mu,r}].\quad}
\tag{6}
\]
这是 actual finite-μ Hamilton方向在全部 λ上的周期 gauge表示。没有用 formal residue gradient。

## 2. 有界 rational 形式与准确 residue

令 W⁰=W−trW I/M、T_s(W)=Σ_{i≠j}s_ijW_ijE_ij。由原 C+的准确公式，
\[
g_{\lambda;\mu,r}=-\frac1{16}
\left[
\rho W^0+T_s(W)+\sum_iH_i\operatorname{tr}(K_i(b)W)
\right],
\quad \rho=\frac{1-ab}{a-b}
=-b+\frac{1-b^2}{a-b}.
\tag{7}
\]
所以 g对 λ是 bounded-at-infinity rational函数，只有 λ=μ 的至多简单极点，并有
\[
\boxed{\quad
\operatorname{Res}_{\lambda=\mu}g_{\lambda;\mu,r}
=-\frac{S^2-\mu^2}{16S}W_{\mu,r}^0.\quad}
\tag{8}
\]
尽管 g有pole，(6) 的 variation是原 affine λ函数。pole residue本来就是 μ处的 homogeneous periodic adjoint，因此 gauge方程的pole项消去。

## 3. λ=±S：三角约束与一阶谱参数导数

由 (2)，L_S严格 upper-offdiagonal，L_{−S}严格 lower-offdiagonal，其 diagonal分别是
\[
\Delta_i-\bar\Delta\pm(d_i-S/M).
\tag{9}
\]
因此其 monodromy、W_{±S,r} 也分别 upper/lowertriangular。对 upper W，tr(K_i(1)W)=W_ii；对 lower W，tr(K_i(−1)W)=−W_ii。(7) 中的三项由 stricttriangular部分与 diagonal部分精确抵消，得到
\[
\boxed{\quad g_{\lambda;S,r}=g_{\lambda;-S,r}=0
\quad\text{对所有 }\lambda\ne\pm S.\quad}
\tag{10}
\]
两端 classfunction由固定 component means确定。uniform均值叶上全部 monodromy diagonal为1，故 F_{±S,r}=M/r；一般均值叶上用 (9) 的积分给 diagonal eigenvalues。它们在每个固定均值叶上恒定，X_{F±S,r}=0，与 (10) 一致。这不是全部 physical image条件。

但对应一阶谱参数导数
\[
G_{\varepsilon,r}
=\left.\partial_\mu F_{\mu,r}\right|_{\mu=\varepsilon S},
\qquad \varepsilon\in\{1,-1\},
\tag{11}
\]
一般不是常数。实际参数解析性和 (6)给 periodic generator
h_{λ;ε,r}=∂_μg_{λ;μ,r}|_{μ=εS}。由于 (8) 的prefactor有简单零，该 generator仍只有一个简单pole，准确为
\[
\boxed{\quad
\operatorname{Res}_{\lambda=\varepsilon S}h_{\lambda;\varepsilon,r}
=\frac\varepsilon8W_{\varepsilon S,r}^0.\quad}
\tag{12}
\]
没有 doublepole：其系数是 (8) 的prefactor在 μ=εS 的值0。微分 (7) 的 λ∞常数部分仍有界。X_G是 actual X_F的参数导数；对固定 smooth物理态它属于 all actual trace Hamilton场的 C∞闭包，差商直接实现。其向量场仍是每阶 H^s上的解析 order-zero场，不需要源的额外x导数。

## 4. λ-independent periodic gauge 与物理 tangent 的零交

下面的引理作用在 [physical state图](all_m_physical_holonomy_state_inverse_20261011.md) 的足够小 uniform邻域，即该uniform均值叶或已由参数IFT构造的附近均值叶。只需该 coefficient图的 (NR)，不另要求 ambient谱状态inverse的小向量势半径。固定均值与 B，内部 H接近 nonalias V₀。结论：若一个真实 physical variation δz满足
\[
\delta L_\lambda=g_0'-[L_\lambda,g_0]
\quad\text{对全部 }\lambda,
\qquad g_0(x)\in\mathfrak{sl}_M\text{ smooth periodic、独立于 }\lambda,
\tag{13}
\]
则 δz=0。

证明需保留 pointwise trace normalization。令 E=T_z diag(1,G)，G是已证 mean-normalized periodic内部 gauge，det T_z是 state-independent常数。取近I logdetG，定义
\[
\bar E=(\det G)^{-1/M}E.
\tag{14}
\]
其 determinant是该固定常数，且它将原 Lλ准确变为
\[
\bar A_\lambda=
\begin{pmatrix}\lambda&a\\b&H\end{pmatrix}
-\frac{\lambda+\operatorname{tr}H}{M}I_M.
\tag{15}
\]
原因是 (logdetG)'=trV−trH=Σ_ib_i−trH。不能直接用未归一 blockconnection遗漏这个 scalar项。

g转为 \(\bar g=\bar E^{-1}g_0\bar E-\bar E^{-1}\delta\bar E\)，仍trace-free、periodic、独立于 λ。由于 (15) 的 λ coefficient J_*=E₀₀−I/M是 state-independent，(13) 的 λ项强制 [J_*,ḡ]=0，即 ḡ=diag(t,K)。topdiagonal方程给
\[
t'=-\delta\operatorname{tr}H/M.
\tag{16}
\]
右侧是常数；周期性强制 δtrH=0、tconstant。其余方程是
\[
\delta a=t a-aK,\qquad
\delta b=Kb-bt,\qquad
\delta H=K'-[H,K].
\tag{17}
\]
Hconstant，δH亦constant；在每个非零 Fourier模 (ik−adH)K_k=0。nonalias条件给 K_k=0，因此Kconstant。

于是 (17) 恰是常数 GL_m action
(aQ,Q⁻¹b,Q⁻¹HQ) 的 tangent，X=tI−K。新 physical finite graph在uniform处与这个m²维action相交的核为0：H simple、aP_jb≠0，使 (aX,−Xb,[H,X])=0只能X0；完整 finite constraints的对应minor满秩。满秩是开条件，故缩同一物理邻域后这种零交在每点保持。physical variation因此为0；state chart的 derivative同构保证原δz=0。tracefree进一步给 t=K=0。引理不依赖 spectralclass inverse，也未仅在 uniform切空间使用此结论。

## 5. 有限简单 pole 的 exact Hamilton span theorem

取上述邻域内一个 smooth物理态，令 δz为 smooth、固定均值的 physical variation。假设它存在全谱 rational periodic gauge
\[
g(x,\lambda)=g_\infty(x)+\sum_{j=1}^J\frac{R_j(x)}{\lambda-\mu_j},
\qquad
\delta L_\lambda=g'-[L_\lambda,g],
\tag{18}
\]
g∞,R_j trace-free smooth periodic，pole μ_j互异。假设每个 actual N_{μ_j} cyclic；允许 cyclic Jordan碰撞。

δLλ是 affine且无pole，所以每个 residue满足
\[
R_j'=[L_{\mu_j},R_j].
\tag{19}
\]
cyclic引理给完整 actual periodic adjoint basis
\[
R_j=\sum_{r=1}^{M-1}c_{jr}W_{\mu_j,r}^0,
\tag{20}
\]
c_jr是 x-independent scalars。全部 M−1 tracepowers都需要；M>2仅 fundamental trace不够。

若 μ_j≠±S，(8) 用系数 −16S c_jr/(S²−μ_j²) 的 actual X_Fμjr匹配该 residue。若 μ_j=εS，(12) 用 8ε c_jr 的 X_Gεr匹配。减去有限个这些 Hamilton方向及其 generators，(18) 的 gauge没有pole，仍bounded∞，因而剩一个 λ-independent periodic矩阵。剩 physical variation由 §4强制为0。所以
\[
\boxed{\quad
\delta z\in\operatorname{span}_{\mathbb C}
\{X_{F_{\mu_j,r}}:\mu_j\ne\pm S\}
+\operatorname{span}_{\mathbb C}
\{X_{G_{\varepsilon,r}}:\varepsilon S\text{ 是pole}\}.
\quad}
\tag{21}
\]
若没有特殊pole，已是 finite actualtrace Hamiltonspan；有特殊pole时仍属于 all actualtrace Hamilton场的 C∞闭包。对实δz取 conjugate-real平均，或直接使用对应 real/imag Hamilton场，不增加实方向。

## 6. 仍缺的全谱步骤

cyclic class-kernel引理给每个 cyclic谱邻域的 local holomorphic周期 gλ。它未提供 (18) 的单个 global rational、有界∞的表示。一般共同谱核可能还需 infinitely many spectralpoles与无界entire部分；这些不能由局部minor逆、framed L²状态inverse或有限维rational插值自动排除。

本稿证明有界rational简单pole这一子类无额外物理 missingdirections，并给 ±S约束与第一谱导数的准确补偿。要将 (21)扩为 nonlinear fullclosure，须证明任意共同核方向能由具有 (18)物理兼容性的方向在同一 physical C∞ tangent topology内逼近，或给等价的完整 squared-eigenfunction定理。仅在λ紧集上近似任意g，并不能控制由g产生的 physical variation、谱尾部与finiteconstraints。

因此本稿不是一般 M Liouville完备性证明。它把下一缺口收紧为全谱周期 gauge的统一表示/逼近，而不再是每个cyclic pole处 periodicadjoint通道数或 λ-independent物理gauge冗余。下一节另给共同核的一个全局 meromorphic表示；它不补这些pole与tail的控制。

## 7. 共同 class 微分核的单个 global meromorphic gauge

对任一 smooth periodic physical源，Lλ是 affine λ，实际 fundamental Yλ(x)、Nλ都是 entire λ。设 δz灭去全部 normalized characteristic coefficients对每个 λ的微分，并有一个 cyclic谱点 λ₀。选固定 cyclic vector v，使
\[
P(\lambda)=[v,N_\lambda v,\ldots,N_\lambda^{M-1}v],
\qquad D(\lambda)=\det P(\lambda),\quad D(\lambda_0)\ne0.
\tag{22}
\]
P、D entire，D的零点离散。无需让 v随 λ变化。

在 D≠0处，P⁻¹NP是准确 companion矩阵：前 M−1列给 shift，最后列由 N的 characteristic polynomial给出。因这些实际 characteristic variations全为零，该 companion矩阵的 δ值为0。微分 NP=PC立即给
\[
\delta N_\lambda=[G_\lambda,N_\lambda],\quad
G_\lambda=\delta P\,P^{-1}
-\frac1M\operatorname{tr}(\delta P\,P^{-1})I.
\tag{23}
\]
其中 δP的第 j列是 δ(N^j)v，首列0；只微分源，v保持固定。

令 Zλ=δYλYλ⁻¹，则 Z'=δL+[L,Z]、Z(0)=0，定义
\[
\boxed{\quad
g_\lambda(x)=Z_\lambda(x)+Y_\lambda(x)G_\lambda Y_\lambda(x)^{-1}.
\quad}
\tag{24}
\]
它 trace-free，满足 δLλ=gλ'−[Lλ,gλ]，而 (23)使 g(L)=g(0)。因此给一个**单个 global meromorphic** smooth-periodic gauge；pole只在 D的离散零点，阶数有限。周期性在 D≠0成立，以 meromorphic恒等式延续；每个principal-part coefficient同样periodic。未要求 N在D零点cyclic，亦未把这些pole全称为actual谱branchpoints。

这里解决的是 localgauge patching的存在，不解决 boundedrational表示。可从实际ODE给显式 growth预算：固定smooth源与variation，对每阶xjet p，存在 C,C_p、有限整数d_p，使
\[
|D(\lambda)|\le C e^{C|\lambda|},
\qquad
\|D(\lambda)g_\lambda\|_{C^p_x}
\le C_p(1+|\lambda|)^{d_p}e^{C_p|\lambda|}.
\tag{25}
\]
证明：Gronwall给 Y、Y⁻¹及N的exp(C|λ|)界；δY的Duhamel公式额外至多一个1+|λ|因子；反复x微分给有限多项式因子。P、adjP及δP是N、δN的有限矩阵多项式，用 P⁻¹=adjP/D即可。(25)不依赖整个函数分解定理。

没有D在全谱的下界，不能从 (25)控制pole距离、residue大小或Hamilton尾。若D零点仍cyclic，其pole可能只是所选Krylov frame的退化，可用局部另一个cyclic vector重新规范；当前globalg的principal parts仍是要控制的homogeneous通道。非cyclic点还可能有超出tracepowers的periodic adjoints。

在本文uniform fixed-mean物理邻域，λ=±S的三角monodromy有一个Jordan链，adjacent entries为非零±2δL；所以uniform N±S cyclic，缩邻域后仍cyclic，(22)的起始点实际存在。这个globalmeromorphic引理也适用于任何另有cyclic起始点的源，并不限于uniform邻域。

§5只处理有限简单pole且bounded∞的g。下一节将其扩大到有限任意阶cyclic poles。将 (24)这一实际全局表示送进同一物理C∞ Hamiltonclosure，仍缺：无限principal parts的受控截断、非cyclic点的完整处理，以及截断后残余entire部分的物理兼容性。没有用整个函数紧集近似冒充这些步骤。

## 8. 任意有限 pole 阶数：实际谱参数 derivatives 逐阶消去

将 (18)扩大为任意 finite rational、bounded∞的 periodic tracefree g，pole μ_j有有限阶 k_j，每个 Nμ_j仍cyclic。令
\[
\alpha(\mu)=-\frac{S^2-\mu^2}{16S},\qquad
g_{\lambda;\mu,r}=\frac{\alpha(\mu)W_{\mu,r}^0}{\lambda-\mu}
+B_{\mu,r}(x),
\tag{26}
\]
Bμr独立于 λ。所有对 μ的 derivatives仍是实际 Hamilton场 ∂_μ^jX_Fμr的 periodic gauge generators，bounded∞。对于 μ≠±S，∂_μ^{k−1}g 的最高 pole为
\[
\frac{(k-1)!\alpha(\mu)W_{\mu,r}^0}{(\lambda-\mu)^k}.
\tag{27}
\]
在 μ=εS，α=0、α'=ε/8，故 ∂_μ^k g的最高 pole为
\[
\frac{k!\varepsilon W_{\varepsilon S,r}^0/8}
{(\lambda-\varepsilon S)^k}.
\tag{28}
\]
这两式直接由 Leibniz rule与 ∂_μ^j(λ−μ)⁻¹=j!(λ−μ)⁻ʲ⁻¹得出；特殊点的表面(k+1)阶pole系数为α=0。

任意阶k pole的最高 Laurent coefficient R_k，由 affineδL无pole强制 R_k'=[Lμ,R_k]。cyclic adjoint basis使它可写为Σc_rWμr⁰。按 (27)或(28)用有限个 actualparameter-derivative Hamilton场消去该最高pole；差仍产生一个真实物理variation，剩pole阶降低。有限递归消去全部principal parts后，剩λ-independentgauge由 §4排除。

因此 **全部 bounded-at-infinity finite rational周期 gauge物理核方向，只要各pole actual monodromy cyclic，都在实际trace Hamilton场的 C∞闭包中**。更精确地，它们在有限集合的 parameter-derivative Hamiltonspan中：普通pole可用 j=0,…,k_j−1，μ=±S的pole可用 j=1,…,k_j。

每个固定阶parameter derivative在C∞中是有限差商极限；这不提供极点数或阶数趋于无穷时的统一bound。本节只消去 finite higherpole作为单独障碍。全谱仍缺 infinite-pole convergence、非cyclic通道，以及 unbounded entire residual的物理控制。

## 9. 无界 polynomial 部分的最高通道：不能只数 fast 一支

如果共同核的 global gauge是非恒定 polynomial，§4的bounded∞引理不适用。对任一 degree N≥1 的 polynomial periodic tracefree gλ，把它通过 (14)变换并减去Ē⁻¹δĒ；所得 ḡλ仍degreeN，因为movingframe独立于λ。令最高 coefficient为ḡ_N。source变分δĀ没有λ项，而Āλ=λJ_*+Q，故最高λ^{N+1} coefficient要求 [J_*,ḡ_N]=0，即
\[
\bar g_N=\operatorname{diag}(t_N,K_N).
\tag{29}
\]
接下来的λ^N equation取diagonal blocks，得到
\[
t_N'=0,\qquad K_N'=[H,K_N].
\tag{30}
\]
这里 [J_*,ḡ_{N−1}]仅有offdiag blocks，不能贡献 (30)。周期性、internal nonalias条件强制 K_N是constant且与H交换；tracefree要求t_N+trK_N=0。

在H simple的当前uniform邻域，这个必要的最高channel空间有复维数m=M−1：K_N属于H的m维centralizer，t_N由其trace给定。它不是只含fast projector的一维空间。此为必要条件；本稿没有声称每个channel均能完成lower-order recursions并落在原finitephysicalgraph tangent，也未构造它们的Hamiltoncharges。

所以即使先完成所有finitepole消去，还必须控制entire/polynomial部分的slow通道。仅将fast quasimomentum WKB系数等同于原C_n，不自动完成这m维最高channel的物理匹配。完整actual class family保留全部M−1 traceadjoints，是继续处理该部分的正确数据入口。

统一scope校验：在均匀背景，所有actual trace gradients在源free坐标中都是spatialconstant，所以全部meanzero物理变分都灭去其微分，而J使全部trace Hamilton场为0。这是closed-gap临界点，不能从framed状态inverse或§5/8推出那里共同微分核最大性；非零核方向的globalgauge必须违反finiteboundedrational cyclic-pole假设之一。上述finite-rational定理没有把整个uniform邻域的所有共同核方向都假定成这种形式。
