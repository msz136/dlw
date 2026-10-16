# 全 M 原物理谱对合、vector Riccati 及 strong 域独审

2026-10-11。独立读取谱主稿 §§16–17、原 GENERAL_PERIOD_MATRIX_LAX.md §§1–3、根复核稿，以及 periodic reduction 的 h 加权约定。以下是重新推导，不以既存有限检查代替证明，也未重跑旧检查。范围为任意固定有限 \(M\ge2,\ S=hMc/8\ne0\)，任意固定组件均值叶和有限幅度。gap 标号、独立性和 AKNS 逆的专属小背景条件不自动推广。

## 1. 原配对及跨分量 bracket

记 \(m=M-1,\ Z_j=e_j-e_m\)，\(E\) 取前 \(m\) 分量。源物理 pairing 为 \(h\sum_j\int\)，原 tensor 为 \(-\operatorname{offdiag}(P_0D)\)。普通 target 积分下应将此源 tensor 除以 \(h\)，并使用实际 derivative
\[
F_*=\begin{pmatrix}Z^T/2&hK_d/8\\0&hE/8\end{pmatrix},
\quad (K_d)_{jk}=-\delta_{jk}-2{\bf1}_{k>j}+\delta_{km}.
\]
这里
\[
q_j=b_j-b_m-d_j-2\sum_{k>j}d_k+d_m,\quad d_j=hw_j/8.
\]
共同 \(U\) 的 mean reconstruction 完全从 \(b_j-b_m\) 抵消，没有遗漏 nonlinear mean derivative。
\(P_0Z=Z,\ Z^TE^T=I_m\)，且
\[
(K_dZ)_{j\ell}=1-\delta_{j\ell}-2{\bf1}_{\ell>j}
\]
为 skew 矩阵。因此普通积分 tensor 的 qq block 为
\(-[K_dZ+(K_dZ)^T]D/16=0\)，qd、dq blocks 为 \(-I_mD/16\)，dd 为零：
\[
J=-\frac1{16}\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix}.
\tag{1}
\]
令 \(\Delta_j=b_j-b_m=q_j+S+\sum_{\ell<m}s_{j\ell}d_\ell\)，
\(s_{j\ell}=\operatorname{sgn}(\ell-j)\)。这个 skew 仿射混合也保留 (1)。\(S\) 是原 Casimir 标签，外部 \(B(t)\) 未进入 free 坐标。

## 2. centered affine connection 与实际 gradients

原一般通量矩阵包含 \(-(B-S)P\)，因此准确 static identity 是
\[
A_{\chi,\Gamma}(\lambda_{\rm orig})
=BI+A_{\chi,0}(\lambda_{\rm orig}-B).
\tag{2}
\]
不能遗漏 \(-BP\) 后误取 \(\lambda_{\rm orig}-2B\)。
以后 \(\lambda=\lambda_{\rm orig}-B\)。\(B=0\) 的 raw connection 有 diagonal
\(\lambda d_i/S+b_i\)、off diagonal \(d_i(\lambda/S+s_{ij})\)，而闭合
\(b_m=-\sum_{j<m}d_j\Delta_j/S\) 是共同 scalar 项。减 trace 精确得
\[
L_{ii}=\lambda(d_i/S-1/M)+\Delta_i-\overline\Delta,\quad
L_{ij}=d_i(\lambda/S+s_{ij})\quad(i\ne j).
\tag{3}
\]
它是原 constrained 物理 source 的真实 affine \(sl_M\) connection。

记 \(H_i=E_{ii}-I/M,\ K_i(a)=\sum_j(a+s_{ij})E_{ij}\)，\(a=\lambda/S\)。
因 \(d_m=S-\sum_{j<m}d_j,\ \Delta_m=0\)，独立 source gradients 是
\[
F_{\Delta_j}=\operatorname{tr}(WH_j),\qquad
F_{d_j}=\operatorname{tr}[W(K_j(a)-K_m(a))].
\tag{4}
\]
对 \(F_{\lambda,r}=r^{-1}\operatorname{tr}N_\lambda^r\)，
\(W=Y_\lambda N_\lambda^rY_\lambda^{-1}\) 满足 \(W'=[L,W]\) 且周期。
这是实际 Duhamel 变分，允许 generic mean leaf；没有换用 formal residue 梯度。

## 3. 通用 R 的独立逐指标证明

设 \(b=\mu/S,\ \rho=(1-ab)/(a-b)\)，
\[
\Pi_0=\sum_{ij}E_{ij}\otimes E_{ji}-I\otimes I/M,\quad
T=\sum_{i\ne j}s_{ij}E_{ij}\otimes E_{ji},\quad C_H=\sum_iH_i\otimes H_i,
\]
\[
B_{ab}=\sum_i(H_i\otimes K_i(b)+K_i(a)\otimes H_i).
\]
原 source 的 (4) 确给此 \(B\)：只需利用 \(\sum_iH_i=0\) 将 \(K_j-K_m\) 扩成全 \(i\) 求和。定义
\[
R=\rho\Pi_0-\frac{a-b}{2}C_H+T+
\frac12\sum_{i\ne j}[(b+s_{ij})H_i\otimes E_{ij}
-(a+s_{ij})E_{ij}\otimes H_i].
\]
直接相加减得
\[
C_+=R+B/2=\rho\Pi_0+T+\sum_iH_i\otimes K_i(b),\quad
C_-=R-B/2=\rho\Pi_0+T-\sum_iK_i(a)\otimes H_i.
\tag{5}
\]
目标等价于
\([C_+,L_\lambda\otimes I]+[C_-,I\otimes L_\mu]=0\)。
共同 Cartan 部分：flip 和 \(T\) 的两总 root weights 抵消；其余 terms 在相应 Cartan factor 直接交换。central scalar 部分不贡献。

每个 row \(K_i\) 可以逐分量验证。以下 tensor matrix 的 row 是 \((p,r)\)、column 是 \((q,s)\)。flip contribution 是
\[
(1-ab)(\delta_{ps}\delta_{ri}-\delta_{rq}\delta_{pi}).
\]
\(T\) contribution 与两个 mixed terms 合并后，完整残差准确是
\[
\delta_{ps}\delta_{ri}\Theta(i,p,q)
-\delta_{pi}\delta_{rq}\Theta(i,r,s),\qquad
\Theta(i,j,k)=1-s_{ij}s_{ik}-s_{ik}s_{jk}+s_{jk}s_{ij}.
\tag{6}
\]
这份 index convention 与主稿 (113) 是同一式的重命名。三索引互異的六种顺序各给零；仅两者相同用 \(s^2=1\) 给零；全部相同为一。因此
\(\Theta(i,j,k)=\delta_{ij}\delta_{ik}\)，(6) 的两项都只在 \(p=q=r=s=i\) 非零，精确抵消。这是任意有限 \(M\) 的证明。
\[
[R,L_\lambda\otimes I+I\otimes L_\mu]
=\tfrac12[B,I\otimes L_\mu-L_\lambda\otimes I].
\tag{7}
\]

设 \(I_1=\operatorname{tr}_{12}[B(W_\lambda\otimes W_\mu')]\)，
\(I_2=\operatorname{tr}_{12}[B(W_\lambda'\otimes W_\mu)]\)。
实际逐点 identities 是
\[
D\operatorname{tr}(R W_\lambda\otimes W_\mu)=(I_1-I_2)/2,\quad
D\operatorname{tr}(B W_\lambda\otimes W_\mu)=I_1+I_2.
\]
故 \(I_1=D\operatorname{tr}[(R+B/2)W_\lambda\otimes W_\mu]\)；
周期积分后才可只写 \(R\)。与 (1) 合并给全部 actual trace powers 彼此对合。等参数用 ODE/source-gradient 的实际解析性取极限。Newton identities 给所有实际 characteristic coefficients 对合。

## 4. scalar holonomy 的缩放

采用主稿的归一
\[
\tau=\frac1M\int\sum_i b_i
=\int[-S^{-1}\sum_{j<m}d_j\Delta_j+M^{-1}\sum_{j<m}\Delta_j],
\quad N_\lambda=e^{-\lambda L/M-\tau}T_\chi.
\]
由 (1) 得
\[
X_\tau=(\Delta_x,d_x)/(16S).
\tag{8}
\]
所以 \(\tau\) 是实际空间平移，和全部 periodic class functions 对合。若使用未除 \(M\) 的 full trace \(\tau_{\rm full}=M\tau\)，速度相应乘 \(M\)；两记号不可混用。raw characteristic data 对合也由此成立，但 raw trace 场另含 loss-one translation 部分。

## 5. vector Riccati 的 actual C¹ 估计

已实际读原全周期 splitting。\(T=[d/S,Z]\) 的 determinant 非零常数；
\(T^{-1}=[1^T;E-(d_{\rm first}/S)1^T]\)，允许任何单独 \(d_j=0\)。
centered raw 系统精确为
\[
\binom\phi\xi'=\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}\binom\phi\xi,
\quad q=1^TCZ,\quad r=K(Cd-d_x)/S,\quad V=KCZ.
\tag{9}
\]
这里 prime 作用整列；\(C\) 为 raw zero-order matrix，\(K\) 为上述矩阵选择，不是微分 inverse。
所有源分母仅是固定 \(S\)；\(q,V\) 是无导数多项式，\(r\) 含一阶 \(d_x\)。有界 \(H^{N+2}\) 源球给
\(q,V\in H^{N+2},r\in H^{N+1}\) 的共同有限界。

周期 \(R_\lambda=(D+\lambda)^{-1}\) 在每个 Sobolev norm 有界 \(\le\lambda^{-1}\)。
\[
b=R_\lambda(r+Vb-b(qb))
\tag{10}
\]
在 \(H^1\) 的 \(O(\lambda^{-1})\) 球内收缩，\(\lambda\ge\Lambda>0\) 随给定源球选定。源复解析。递推
\[
\beta_1=r,\quad
\beta_{j+1}=V\beta_j-D\beta_j-\sum_{a+b=j}\beta_a(q\beta_b)
\]
给 \(\beta_j\in H^{N+2-j}\)。截断至 \(N\) 的 differential residual 为
\(O_{H^1}(\lambda^{-N})\)：最后 \(D\beta_N\in H^1\)，其余为有限 \(H^1\) 乘积。
resolvent 增一个 \(\lambda^{-1}\)，收缩 inverse 有界，所以
\[
b_\lambda=\sum_{j=1}^N\beta_j\lambda^{-j}
+O_{H^1}(\lambda^{-N-1}).
\tag{11}
\]
先在稍大复源球证明同界，holomorphic Cauchy 估计给较小球的真实
\(H^{N+2}\to H^1\) Fréchet \(C^1\) 余项，同阶 \(\lambda^{-N-1}\)。
有限矩阵大小只改变常数。没有把这当成只依 low norm 的全无限阶估计。

## 6. simple actual fast root 与 trace-log

实际 periodic triangular gauge \(\xi=b_\lambda\phi+\zeta\) 给
\[
\phi'=(\lambda+qb_\lambda)\phi+q\zeta,\qquad
\zeta'=(V-b_\lambda q)\zeta.
\tag{12}
\]
fast multiplier 为 \(e^{\lambda L+\mathcal K_\lambda}\)，
\(\mathcal K_\lambda=\int qb_\lambda=O(\lambda^{-1})\)；slow monodromy 由统一
\(L^1\) 系数界控制。大正 \(\lambda\) 下 fast root 简单、指数分离，源球上 log branch 一致。normalized fast root 是
\[
\widehat\mu_f=\exp((1-1/M)\lambda L+\mathcal K_\lambda-\tau).
\]
故 \(\mathcal K_\lambda\) 是全部 characteristic coefficients 与 \(\tau\) 的 actual 解析函数。对 \(M>2\)，不能声称只由一个 fundamental trace 反演所有根。§3、(8) 给其和全部 fixed-spectrum classes 对合。

形式留数识别独立如下。令 \(\mathcal C=DI_m-V\)，将 \(b^f\) 视为列乘法算子；Riccati 直接给
\[
r=(\mathcal C+b^fq)\circ b^f-b^f(D-\lambda).
\]
因此原 scalar \(\mathscr L=D-q\mathcal C^{-1}r\) 准确满足
\[
\mathscr L-\lambda=(1+q\mathcal C^{-1}b^f)(D-\lambda-qb^f).
\tag{13}
\]
没有除以 \(q\)。两 scalar factors 为 \(I+O(\lambda^{-1})\)；
lambda-adic BCH 周期 trace 的 commutators 消失。第二因子的 log coefficients 为 differential operators，residue 零；第一因子 \(A=q\mathcal C^{-1}b^f\) 阶 \(-1\)，
\(\operatorname{res}A=qb^f\)，\(A^j,j\ge2\) 阶 \(\le-2\)。所以
\[
\int qb^f=\operatorname{Tr}\log(1-\mathscr L/\lambda)
=-\sum_{n\ge1}C_n\lambda^{-n}.
\]
形式计算只识别 coefficients；与 (11) 的 actual \(C^1\) 余项合并才得到
\[
\mathcal K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(H^{N+2})}(\lambda^{-N-1}).
\tag{14}
\]
固定 \(\mu,r\) 的 class Hamilton 场从 actual \(W'=[L,W]\) 把 gradient 上的 \(D\) 化为 \(\operatorname{tr}W[\text{constant matrix},L]\)，为同一
\(H^{N+2}\to H^{N+2}\) 的真实切向。代入 (14)，逐次提取正 \(\lambda\) 系数得
\[
\{F_{\mu,r},C_n\}_{\rm original}=0
\tag{15}
\]
对全部有限 \(M,n,r\) 成立。每个 \(n\) 用适当高 Sobolev 层，全部层级用 smooth 交集；不宣布一个 low Sobolev 开域支持全部 \(C_n\)。

## 7. 同一 all-M strong 相域里的实际谱流

固定有限 \(M\) 和一个 normalized class Hamiltonian 的真实实部/虚部。
§2 的 actual ODE gradients 与 (15) 正是既有
[strong flow bridge §§3–5](spectral_m2_strong_domain_flow_bridge.md) 的全部分析输入：
局部解析 order-zero low \(H^1\) 场、translation equivariance、与全部原 \(C_n\) 及平移的实际 commutation。
其中有限源分量从二个增加到 \(2(M-1)\) 只改变常数，不改变任何核指数或参数重构机制。

在已有 all-M strong plot 的 compact 参数盒上，逐坐标一次固定旧 complex windows，用可求和 low \(H^1\) 增量保持全部 finite prefixes 的物理像在同一个低阶 ball 内。actual Banach 谱流给对所有前缀共同的一个正谱时间盘。constant physical \(J\) 和 (15) 给
\[
D\Phi_\sigma X_{C_n}=X_{C_n}\circ\Phi_\sigma.
\]
于是被输送的所有旧 joint germs 仍为原方程的相容 actual 解。取其 mixed source corners，通过全 M 已证 finite mixed contraction/中心唯一性重参数化；每层仅缩新层级轴，谱参数盒不缩。中心与 plot 因真实 uniqueness 精确识别，逆 \(-\sigma\) 给局部逆。谱速度因此是同一 \(\mathfrak S_\infty\) 的内部 Hamilton 场，而不只是取值在 ambient smooth 场空间。

此结论保留原 strong presentations 和 mixed 唯一性假设。任意 ordinary \(H^s\) 源只有 auxiliary Banach flow；不自动有原 DLW 的全部 Cauchy 时间。仅有限个非零谱时间和有限支持旧时间 germs 被定义。raw trace 中的 \(\tau\) 项另由真实空间平移处理，不称 order zero。全 M 的 uniform gap/norming 标号、nonlinear state inverse、Hamilton 闭包最大性和共同 fiber 正则性仍未由这些证明得到。

结论：谱主稿 §§16–17 的全 M 对合、actual \(C^1\) 桥及同 strong 域接合已独立通过；(7)、(13) 和 (14) 是核心新证明，有限证书未代替它们。
