# 全 M 物理图：周期规范 Fredholm 方程与 2m 个实际谱约束

2026-10-11，mixed 独立推导，\(m=M-1\)。实际读取 vector framed L² inverse、raw endpoint 恢复、periodic physical state inverse 和 cyclic gauge 引理。新增的是物理 finite graph 上的具体规范方程及其 index、以及 graph 的 constant-GLm saturation 的纯谱约束刻画。没有重跑旧 checks，没有将 full framed state inverse 当作 action inverse或一般 M Hamilton density。

采用固定 finite \(M\)、\(S=M\delta\ne0\)、包含均匀态的固定 component-mean 叶。centered B 规范可逐空间截面使用；以下不要求 \(\Gamma_t=0\)。periodic mean-normalized constant-H frame 为
\[
A_\lambda=\begin{pmatrix}\lambda&a\\b&H\end{pmatrix},
\quad a\in L^2_{\rm row},\ b\in L^2_{\rm col},\ H\in\mathrm{Mat}_m.
\]
其 normalized monodromy
\[
N_\lambda=e^{-L(\lambda+\mathrm{tr}H)/M}T_\lambda,\qquad
\tau=(L/M)\mathrm{tr}H.
\]
物理像是已证明的 finite graph
\[
y=(P_0a,P_0b),\quad
\langle a\rangle=\mathcal A(y),\quad
\langle b\rangle=\mathcal B(y),\quad H=\mathcal H(y).
\tag{1}
\]
同一低域具有全部 higher restrictions。下面规范方程取 smooth state 与 smooth variations，finite graph derivatives 来自真实 low analytic maps。

## 1. 全 normalized class 微分核自动灭去 scalar holonomy

设 smooth physical variation 灭去所有实际 normalized characteristic coefficients，对所有 \(\lambda\) 恒等。已审 positive-real actual vector Riccati 给 isolated fast root
\[
\widetilde\mu_\lambda
=\exp\{(1-1/M)\lambda L+\mathcal K_\lambda-\tau\},
\qquad \mathcal K_\lambda=O_{C^1}(\lambda^{-1})
\]
在 sufficiently high but finite source Sobolev ball。fast root 简单且与有界 slow spectrum 分离；所有 characteristic derivatives 零使其 actual root derivative 零。因此
\[
d\mathcal K_\lambda=d\tau.
\]
令实 \(\lambda\to+\infty\)，actual \(C^1\) remainder 给
\[
\boxed{d\tau=0,\qquad \mathrm{tr}\dot H=0.}
\tag{2}
\]
于是 normalized 和 raw characteristic differential 在该 variation 上等价，可以使用 raw \(A_\lambda\) 的 periodic gauge kernel。这不是从 eigenvalue formal expansion 猜 holonomy 恒定；只用已建立实际 C¹ fast-root 估计。

## 2. Constant-H 图上的准确块规范方程

对 fixed cyclic \(\lambda\)，周期规范引理给
\[
\dot A_\lambda=g_x-[A_\lambda,g],\qquad
g=\begin{pmatrix}\alpha&\beta\\\gamma&Z\end{pmatrix}.
\]
这里 \(\beta\) 是 row、\(\gamma\) 是 column，不是原 physical free \(q,d\)。
直接 block multiplication 得
\[
\alpha_x=a\gamma-\beta b,
\]
\[
\dot a=(D-\lambda)\beta+\beta H+\alpha a-aZ,
\qquad
\dot b=(D+\lambda)\gamma-H\gamma+Zb-b\alpha,
\]
\[
\dot H=(D-\mathrm{ad}H)Z-b\beta+\gamma a.
\tag{3}
\]
\(\dot H\) 必须是 constant matrix，不能把最后一行作为额外 arbitrary slow field。

假设 \((D-\mathrm{ad}H):H^{s+1}_0\to H^s_0\) nonalias；uniform 的既有 nonalias 条件在一个 low 图内保持。置 \(K=D_0^{-1}P_0\)、\(R_H=(D-\mathrm{ad}H)^{-1}P_0\)，则
\[
\alpha=\bar\alpha+K(a\gamma-\beta b),\quad
Z=\bar Z+R_H(b\beta-\gamma a),
\]
\[
\dot H_{\rm pred}=-[H,\bar Z]-\langle b\beta-\gamma a\rangle.
\tag{4}
\]
还须保留 finite moment
\[
\langle a\gamma-\beta b\rangle=0.
\tag{5}
\]
非局部消元严格 gain one；\(\bar\alpha,\bar Z\) 是 finite constants。trace 条件由 (3)、(5) 自动一致：\(\mathrm{tr}\dot H=0\)。若只写 \(K\) 解而省去 (5)，就会错误丢掉 fast diagonal 的 constant equation。

令 (3) 的两行预测值为 \(u_a,u_b\)，\(\dot y=(P_0u_a,P_0u_b)\)。
物理 graph 切向的其余条件准确为
\[
\langle u_a\rangle=D\mathcal A(y)\dot y,\qquad
\langle u_b\rangle=D\mathcal B(y)\dot y,\qquad
\dot H_{\rm pred}=D\mathcal H(y)\dot y.
\tag{6}
\]
因此 (3)–(6) 是 physical graph 上的 explicit periodic gauge kernel equations；所有 extra equations 都是 finite scalar/matrix constraints。它们必要且充分：给 (4)–(6)，代回 (3) 即得到实际 graph variation 与 periodic gauge。固定 \(\lambda\) 的 raw full invariant-kernel equivalence仍需 cyclic monodromy；所有 \(\lambda\) 的共同核则还由 (2) 给 trace-normalization 相容。

## 3. Augmented 一阶算子的严格 Fredholm index

对固定 smooth state、\(s\ge0\)，把 (3)–(6) 写成线性 operator
\[
\mathscr G_\lambda:
(H^{s+1})^{2m}\oplus\mathbb C\oplus\mathrm{Mat}_m
\longrightarrow
(H^s_0)^{2m}\oplus
\mathbb C\oplus\mathbb C^{2m}\oplus\mathrm{Mat}_m.
\tag{7}
\]
domain 变量为 \((\beta,\gamma,\bar\alpha,\bar Z)\)。
output 第一项为 \(\dot y\)，后面的 finite residual 依次是 (5)、(6) 两均值与 H 条件。保留 glM 的 trace constant 是为了完整 index 预算；如要 slM，可另外固定 \(\bar\alpha+\mathrm{tr}\bar Z=0\)，同时应调整 identity kernel 的对应 cokernel，不在此强行改写。

base operator 取
\[
(\beta,\gamma,\bar\alpha,\bar Z)
\mapsto(D\beta,D\gamma,0_{\rm finite}).
\]
每个 \(D:H^{s+1}_{\rm per}\to H^s_{\rm per,0}\) surjective、kernel 一维。
因此 base 的 kernel 维数 \(2m+1+m^2\)，cokernel 维数同为
\(1+2m+m^2\)，index zero。
\(\mathscr G_\lambda\) 与 base 的 difference 是 compact：
两主行除 \(D\) 外均 order at most zero，Rellich
\(H^{s+1}\hookrightarrow H^s\) compact；
(4) 的 \(K,R_H\) gain one；
finite constants 与 finite graph residuals 都有限 rank。
故
\[
\boxed{\mathscr G_\lambda\text{ Fredholm，index }0.}
\tag{8}
\]
没有忽略 \(\beta H,H\gamma\) 的零阶项，也没有假定非局部 gauge derivative 零。

若 raw \(T_\lambda\) cyclic，\(\ker\mathscr G_\lambda\) 恰为 full periodic homogeneous adjoints：
output \(\dot y=0\) 与 finite residuals 零使
\(\dot a=\dot b=\dot H=0\)，故 \(g_x=[A_\lambda,g]\)；反向全部 homogeneous adjoints 满足消元和 residual。其维数 \(M\)（包括 identity），因此 cokernel 也维数 \(M\)。这给准确 finite obstruction budget，**不**把它直接识别为 spectral action coordinates或 Hamilton density。

## 4. 固定 ±S 的全部实际 unipotent 谱约束

在原 free-frame normalized affine connection 中，
\[
L_{ii}(\lambda)=\lambda(d_i/S-1/M)+\Delta_i-\overline\Delta,\quad
L_{ij}(\lambda)=d_i(\lambda/S+\mathrm{sgn}(j-i)).
\]
\(\lambda=S\) 时它上三角，\(\lambda=-S\) 时下三角。
固定 uniform mean leaf 给 \(\langle d_i\rangle=S/M\)、
\(\langle\Delta_i\rangle=0\)，所以两个三角系统每个 diagonal 的空间积分零。其实际 monodromies 上/下三角且全部 diagonal entries 一。
periodic split/constant-H gauge 只做 endpoint similarity。因此
\[
\boxed{\mathrm{tr}\,N_{S}^{\,r}
=\mathrm{tr}\,N_{-S}^{\,r}=M,\qquad r=1,\ldots,m.}
\tag{9}
\]
这不是 monodromy 等于 identity；它可以是 regular unipotent Jordan。
定义 full ambient coefficient space 的 \(2m\) 个 analytic class constraints
\[
\Phi(a,b,H)=
\bigl((\mathrm{tr}N_S^r-M)_{r=1}^m,
(\mathrm{tr}N_{-S}^r-M)_{r=1}^m\bigr).
\tag{10}
\]
physical graph 和其 constant-GLm saturation 都在 \(\Phi^{-1}(0)\) 中。

## 5. 背景的 finite derivative rank：恰好 2m

均匀背景的 original normalized \(L(S)\) 是
\(2\delta\) 乘所有严格 upper entries 一的 nilpotent matrix；
\(L(-S)\) 是 \(-2\delta\) 乘对应 lower matrix。
两者 minimal polynomial 阶 \(M\)。constant-H 背景
\[
A_{\pm S}^*=\pm\delta I_M+J_\pm
\]
与它们相似，\(J_\pm\) cyclic nilpotent，\(\mathrm{tr}H_*=0\)。
actual normalized background monodromy \(e^{LJ_\pm}\) cyclic；其 trace-free powers \(r=1,\ldots,m\) span
\(J_\pm,\ldots,J_\pm^m\)。实际 Duhamel gradients 为 constant matrices，所以
\(D\Phi\) 只依赖
\[
(\langle\dot a\rangle,\langle\dot b\rangle,\dot H)
\in\mathbb C^{2m}\oplus\mathrm{Mat}_m.
\tag{11}
\]

给这些 finite constant variations，令
\[
Q(z)=\det(zI_m-H),\quad
R(z)=a\,\mathrm{adj}(zI_m-H)b,\quad
P_\pm(z)=(z\mp S)Q(z)-R(z).
\]
normalized \(D\Phi=0\) 等价于
\(\dot A_{\pm S}-(t/M)I_M\) 是 \(A_{\pm S}^*\) 的 infinitesimal conjugacy variation，
其中 \(t=\mathrm{tr}\dot H\)。
其 raw characteristic derivative准确为
\[
\dot P_\pm(z)=-t(z\mp\delta)^m.
\tag{12}
\]
这是 source-dependent trace normalization 的必要项。
相减得
\[
\dot Q(z)=-\frac{t}{2S}
\bigl((z+\delta)^m-(z-\delta)^m\bigr).
\]
左边 \(z^{m-1}\) coefficient 是 \(-t\)，右边是
\(-tm\delta/S=-tm/M\)；故 \(t=0\)。于是
\[
D\Phi=0\quad\Longleftrightarrow\quad
\dot Q=\dot R=0
\quad\text{在 finite constants 上}.
\tag{13}
\]

已有 uniform \(H_*\) eigenvalues
\(p_j=-i\delta\cot(\pi j/M)\) 全部不同，且每个 realization residue
\(a_*P_jb_*\ne0\)。
在 eigenbasis 中 \(\dot Q=0\) 强制 \(\dot H\) 的 diagonal 零，可选
\(X\) 令 \(\dot H=[H_*,X]\)。
减去 constant gauge variation
\((a_*X,-Xb_*,[H_*,X])\) 后，\(\dot H=0\)；
\(\dot R=0\)（等价于 proper rational transfer derivative 零）逐 simple pole给
\(\dot a_j b_j+a_j\dot b_j=0\)。
因 \(a_j,b_j\ne0\)，剩余正是 diagonal \(X_j=\dot a_j/a_j\) 的 gauge direction。
因此 (13) 的 finite kernel准确是 m² 维 constant-GLm tangent。该 tangent无 stabilizer来自同一非零 residues 条件，所以
\[
\boxed{\mathrm{rank}\,D\Phi_*=2m.}
\tag{14}
\]
这里未借未证明的 action inverse或全谱 growth。

## 6. Physical image saturation 的 exact nonlinear characterization

mean-normalized physical graph (1) 在背景的 finite components derivative全零。
其 tangent的 infinite部分为任意 mean-zero \((\dot a,\dot b)\)，已有 low state inverse保证该 parameter同构。
finite constants空间的 gauge tangent m²维，选一个 \(2m\) 维 constant complement \(\mathcal T\)。由 (13)–(14)，\(D\Phi\) 在该 complement可逆。

考虑
\[
\Psi(y,X,s)=
\bigl(a(y)e^X,e^{-X}b(y),e^{-X}H(y)e^X\bigr)
+\sum_{\ell=1}^{2m}s_\ell T_\ell,\qquad T_\ell\in\mathcal T.
\tag{15}
\]
其背景 derivative：
infinite mean-zero variables、m²个 constant gauge directions 和 \(2m\) 个 constant transverse directions 构成 full ambient
\((L^2)^{2m}\oplus\mathrm{Mat}_m\) 的 bounded direct sum。
analytic Banach IFT使 \(\Psi\) 是背景附近 local chart。

由 (9) 和 constant-gauge invariance，
\(\Phi\circ\Psi(y,X,0)=0\) 恒等。
vector Hadamard identity
\[
\Phi\circ\Psi(y,X,s)
=\left[\int_0^1D_s(\Phi\circ\Psi)(y,X,ts)\,dt\right]s
\]
中的 \(2m\times2m\) matrix 在背景可逆，缩域后仍可逆。
所以在这一同一 low chart，
\[
\boxed{\Phi(a,b,H)=0
\Longleftrightarrow
(a,b,H)=(a(y)C,C^{-1}b(y),C^{-1}H(y)C)
\text{，唯一 small }(y,C).}
\tag{16}
\]
即物理 finite graph 的 constant-GLm saturation准确等于两个固定谱点的 \(2m\) 个 actual invariant constraints。
这补足的是全 M **coefficient-state image** 的纯谱刻画，analogous to M2 的 central-width saturation；仍不把其 quotient宣称为 canonical reduction或 action/norming inverse。

## 7. 与 Hamilton 闭包的下一连接及剩余缺口

已审 all-M R identity 对各 actual trace fields给 rational periodic gauge，独立详细证明由本子任务的 gauge-symbol 审查保存。周期 cohomology (3)–(8) 把任意共同谱核 variation 的形状及 finite graph conditions 明确化；(16) 表明 graph constraints 已是 pure spectral fixed-point constraints，加上一个已横截的 constant gauge section。

尚未证明任意该共同核的 \(g(x,\lambda)\) 有 bounded rational \(\lambda\) dependence，或可由 Hamilton fields的 rational gauges 逼近。cyclic 仅给 fixed-\(\lambda\)/local holomorphic gauge，full framed L² inverse 仅给 state coordinates，两者都不足以填这个缺口。也没有一般 M actual action Cartesian inverse、Hamilton closed-span equality、regular common fiber或完整 Liouville theorem。
