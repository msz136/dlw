# 一般 M：实际高频两分支 Riesz 谱隙的统一物理 Sobolev 引理

2026-10-11。接续已核验的一般 M 原物理 rank-one connection、周期内部 holonomy 规范和 balanced 状态图。本稿给出同一个物理低阶 Banach 邻域上全部高频的实际 rank-two Floquet reduction、中心的 ℓ² 估计、谱隙平方的 ℓ¹ 解析性，以及准确二阶 Born Hessian。这里的谱隙来自实际 monodromy 的特征多项式；没有假设一般 M 的谱曲线为 hyperelliptic。framed 非对角元素仍只是 norming 候选，不是已证 divisor/action-angle 坐标。

复用的证明分别是 [物理 holonomy/状态逆](all_m_physical_holonomy_state_inverse_20261011.md)、[实际奇数阶 Fourier 核](general_m_framed_monodromy_fourier_kernel_20261011.md) 和 [本轮独立实际均匀共振审稿](general_m_uniform_resonance_independent_audit_20261011.md)。最后一稿独立核验了本稿 §1 的实际背景。新偶数阶核和无限序列谱隙函数的证明见 §§3–5。未运行机器脚本或重跑旧证书。

## 1. 适用域、原参数及准确的均匀共振

固定 M≥2、m=M−1、L>0、δ∈R\{0}、S=Mδ。原 free fields 在一个包含均匀态的固定分量均值叶上写为

\[
q_j=q_j^0+u_j,\quad q_j^0=-2\delta(m-j),\qquad
d_j=\delta+v_j\ (j<m),\quad d_m=S-\sum_{j<m}d_j,
\]
\[
X_0=(L^2_0(0,L))^m_u\times(H^1_0(0,L))^m_v.
\tag{1}
\]

下标 0 是分量均值为零；后文采用此空间的复化证明解析性，再限制到原实场。普通积分配对下原物理张量仍是 J=−offdiag(I_mD)/16。本稿没有引入新 bracket。

保留原共同 spatialconstant 参数 B=Γ/(2c)。用 λ=λ_original−B；从全部 split connection 减 BI_M 后，精确物理连接经周期规范变成

\[
A_\lambda(x)=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\qquad a\in L^2(\mathbb C^{1\times m}),\quad
b\in L^2(\mathbb C^{m\times1}),\quad H\in\mathbb C^{m\times m}.
\tag{2}
\]

源到 (a,b,H) 在 X₀ 的某个开邻域解析。它来自 T(d)=[d/S,Z]、Z_j=e_j−e_m 和 G_x=VG−GH、⟨G⟩=I_m：

\[
a=qG,\qquad b=G^{-1}r,\qquad
r=-d_{{\rm first},x}/S+F(q,d),
\tag{3}
\]

F、V 是 zero-order 多项式且只有常数分母 S；G∈H¹。所用周期规范、状态图和同低域高阶 bootstrap 已在前引状态稿证明。均匀源 0 处 G=I、a₀=q₀、b₀=r₀、H₀=V₀，

\[
(r_0)_i=\delta(m-2i)/M,\qquad
(V_0)_{ij}=\delta[\operatorname{sgn}(j-i)+(m-1-2j)/M].
\tag{4}
\]

本稿以 unnormalized M_A=Y(L) 做 Fourier/cluster 估计；原实际 trace-normalized monodromy 的准确 frame 对应是
\[
N_\chi(\lambda_{\rm original})
=E_0\,\mathcal N_A(\lambda_{\rm original}-B)\,E_0^{-1},
\quad E_0=T(d(0))\operatorname{diag}(1,G(0)),
\]
\[
\mathcal N_A(\lambda)
=e^{-(\lambda L+L\operatorname{tr}H)/M}M_A(\lambda).
\tag{4a}
\]
periodic G 保持 integrated trace；任意 B 的共同 e^{BL} 被 trace normalization 精确消去。(4a) 的 scalar factor 非零，故不改 repeated-multiplier 的 λ roots 或 g。均匀 H₀ 的 trace 为零，normalized slow multipliers 含共同旋转因子 e^{−λℓnL/M}，不能把 raw slow 的极限 e^{Lpℓ} 当作 normalized slow 极限。

V₀ 有不同特征值

\[
p_\ell=-i\delta\cot(\pi\ell/M),\quad 1\le\ell\le m.
\]

假设内部无 multiplier alias：

\[
p_j-p_\ell\notin i(2\pi/L)\mathbb Z\quad(j\ne\ell).
\tag{NR}
\]

δ 无需在本引理再满足一个未声明的“小幅度”条件；(NR) 与既有状态图的局部邻域足够。此前 strong 图的 |δ|<(k₀/2)tan(π/(2M)) 是已证的充分条件。

实际均匀 χ generator 是 Aχ⁰(λ)=λP+C₀，P=11ᵀ/M、C₀,ij=δsign(j−i)。它的空间特征值满足准确 dispersion

\[
\lambda=\mathcal R(y)
=S\frac{(y+\delta)^M+(y-\delta)^M}{(y+\delta)^M-(y-\delta)^M}
=y+\sum_{\ell=1}^{m}\frac{r_\ell}{y-p_\ell},
\]
\[
r_\ell=\delta^2-p_\ell^2=\delta^2\csc^2(\pi\ell/M),\qquad
A=\sum_\ell r_\ell=\delta^2(M^2-1)/3.
\tag{5}
\]

这里 R 是 scalar symbol；此等式也由实际有限矩阵 characteristic polynomial 直接推出，不用 formal resolvent 替代实际 monodromy。实际 fast/slow 空间分支为

\[
y_f(\lambda)=\lambda-A/\lambda+O(\lambda^{-3}),\qquad
y_\ell(\lambda)=p_\ell+r_\ell/\lambda-r_\ell p_\ell/\lambda^2+O(\lambda^{-3}).
\]

令 K_n=iκ_n、κ_n=2πn/L。真实 fast/slow Floquet 碰撞位置准确解 y_f−y_ℓ=K_n，故

\[
\lambda_{\ell n}=K_n+p_\ell+(A+r_\ell)/K_n
-p_\ell(A+2r_\ell)/K_n^2+O(|n|^{-3}).
\tag{6}
\]

K_n+p_ℓ 只是 leading center。所有高频 λℓn 纯虚，原 χ monodromy 及其 trace-normalized 版本均 unitary；碰撞 multiplier 的代数和几何重数均为 2。由 (NR)，其余 slow multipliers 同这对的距离有与 n 无关的正下界。设

\[
\gamma_{\ell n}=\partial_\lambda(y_f-y_\ell)(\lambda_{\ell n})
=1+O(n^{-2}).
\tag{7}
\]

这给准确、非零的碰撞斜率。式 (5)–(7)、解析分支、无 triple collision、统一 rank-two Riesz circles 和 λ 链间分离由上引本轮独审逐项证明。旧谱主稿 §3.1 的 quadratic 被复用，未当作本轮新结果。

## 2. 同一 balanced 源邻域上的实际 Riesz blocks

原 χ 连接的物理源 variation 含 λδP(d)，不能直接从其 raw 系数取得独立于 n 的小扰动界。(2) 的 principal matrix E₀₀ 是固定的，这是源估计的必要步骤。

在任何固定 Reλ 有界的 strip 中，写 Aλ=λE₀₀+K(x)。去掉 unitary e^{i Imλ E₀₀x} 后，Gronwall/Volterra 给

\[
\sup_{0\le x\le L}(\|Y_\lambda(x)\|+\|Y_\lambda(x)^{-1}\|)
\le 2\exp[L|\operatorname{Re}\lambda|+\sqrt L\|K\|_2].
\tag{8}
\]

同一估计控制源 Frechet derivatives，特别对任意固定源有界球

\[
\|M_A(\lambda;z)-M_A(\lambda;0)\|\le C\|z\|_{X_0},
\tag{9}
\]

C 不依赖该 strip 内的 Imλ。实际 fundamental matrix 对 L² 源整解析；(8) 来自实际 ODE，(9) 来自 Duhamel，不是形式项逐频估计。

均匀 (2) frame 是原 unitary χ frame 的固定相似变换，其 condition number 与 n 无关。因此 §1 的同一 λ-radius 和 Riesz-resolvent bound 经 (9) 后，在一个源半径 ε>0 上对全部 |n|≥N、所有 ℓ 同时成立。每个实际 projection Pℓn(λ,z) holomorphic、rank 2，且与背景 projection uniformly close。

例如用

\[
U(P,P_*)=[PP_*+(I-P)(I-P_*)]
[I-(P-P_*)^2]^{-1/2}
\tag{10}
\]

作解析 intertwiner；平方根是接近 I 的 convergent binomial series。于是实际 M_A 在该 image 上给一个真正两维 holomorphic compression。该 construction 只用 rank-two Riesz 分离，不假定整条谱曲线的类型，也不要求其余 slow 根在 perturbed source 上全部单值化。

## 3. 新偶数阶 Volterra 核：FULL monodromy 的 ℓ² 估计

本节先在 ambient (a,b,H) 空间证明，随后复合物理图。以 diag(λ,H) 为自由传播子。奇数阶 offdiag 插入的 L² Fourier 核和 bound

\[
\|K_{2r+1}\|_2\le e^{L\|H\|}(L/2)^r(r!)^{-1}
\prod_{j=1}^{2r+1}\|f_j\|_2
\tag{11}
\]

已经由前引 Fourier 核稿证明；f_j 是按原次序 alternating row/column inputs。本节补足 diagonal blocks 的偶数阶项。

对 2r 次插入，r≥1，取 ordered times 0<t₁<⋯<t₂r<L，gaps s₀=t₁、s_j=t_{j+1}−t_j、s₂r=L−t₂r。fast→fast 路径的 total fast time 是 τ=s₀+s₂+⋯+s₂r；它包含 r+1 个 fast gaps、r 个 slow gaps。消去最后一个 fast 与最后一个 slow gap，Jacobian 绝对值 1，故 fiber Lebesgue 体积准确为

\[
v^{ff}_r(\tau)=\frac{\tau^r(L-\tau)^{r-1}}{r!(r-1)!}.
\]

slow→slow 路径的 fast time 是 odd gaps 之和，fast/slow 个数交换，所以

\[
v^{ss}_r(\tau)=\frac{\tau^{r-1}(L-\tau)^r}{(r-1)!r!}.
\tag{12}
\]

两项的实际 fast exponent 都是 e^{λτ}。slow propagators 的总时长≤L，operator norm 的乘积≤e^{L||H||}。fiber Cauchy–Schwarz 和完整 ordered simplex 的平方积分给

\[
\boxed{\quad
\|K_{2r}^{ff/ss}\|_2
\le e^{L\|H\|}\frac{L^{r-1/2}}{\sqrt{r!(r-1)!}}
\prod_{j=1}^{2r}\|f_j\|_2.
\quad}
\tag{13}
\]

使用 row/column Euclidean 和矩阵 Frobenius norm 时，非零插入的 rank-one product 仍满足这一乘积界；改用任意等价有限矩阵 norm 只增加固定 C_M。这里没有把 coarea Euclidean 面积误作 fiber Lebesgue 体积。

对重复 a,b，右侧含 (||a||₂||b||₂)^r，且 √(r!(r−1)!)=r!/√r。因此偶数 series 在任意有界 L²_a×L²_b×Mat_H 球中绝对一致收敛于 L²_τ。连同 (11)，实际 FULL 数据

\[
\mathcal E_n(a,b,H;\sigma)
=M_A(K_n+\sigma)-\operatorname{diag}(e^{(K_n+\sigma)L},e^{HL})
\tag{14}
\]

属于 ℓ²_n(Mat_M)，并对 (a,b,H,σ) joint entire analytic。σ 只给 kernel 上 e^{στ} 或 e^{σ(L−τ)} 的 bounded multiplier。Plancherel 在每个固定 σ 给 (14)；L² kernel 收敛也蕴含 L¹ 收敛，逐个 n 的 Fourier 值与实际 convergent Dyson series 完全相同。

一个以后使用的较强版本是：若 0<r<R、σ₀ 在 compact set，则

\[
\left(\sup_{|\zeta|\le r}\|\mathcal E_n(\sigma_0+\zeta)\|\right)_n\in\ell^2
\tag{15}
\]

该 sup-norm 序列有 ℓ² 的局部一致界；其含绝对值/sup，本身不称 holomorphic。证明不能只写 sup_ζ||E(ζ)||ℓ²。取 R 上的 ℓ²-valued Cauchy coefficients E_j，||E_j||ℓ²≤C_R R^{-j}；Minkowski 给 ||(sup_{|ζ|≤r}||ΣE_j,nζ^j||)_n||ℓ²≤Σr^j||E_j||ℓ²≤C_R/(1−r/R)。真正 strong analytic 的是 function-valued 映射到序列空间 ℓ²_n(A_r)，A_r 是 closed disk 上连续且内部 holomorphic 的矩阵函数空间。

这里只是未加权 ℓ² 估计。raw smooth monodromy 仍可能有 1/n、1/n² endpoint 尾；没有声称 h^s 的全阶 preservation。

## 4. 移动 slow holonomy grid 与实际两根

在 H₀ 附近，其简单 eigenvalues hℓ(H) 与 slow eigenbasis S(H) 可选为有限维 holomorphic branches；取 S(H₀) 固定。缩一次源球使 |e^{Lh_j}−e^{Lhℓ}| 的正下界保持。定义仅用于分析的 moving grid

\[
\lambda=K_n+h_\ell(H)+\zeta,
\qquad \rho_\ell(H)=e^{Lh_\ell(H)}.
\tag{16}
\]

以 diag(1,S(H)) 校准且除以 ρℓ 后，uncoupled template 是

\[
\operatorname{diag}(e^{L\zeta},e^{L(h_1-h_\ell)},\ldots,1,\ldots,e^{L(h_m-h_\ell)}).
\tag{17}
\]

固定绕 1 的 multiplier circle，包含 e^{Lζ} 与 1，排除所有其他 template multipliers。取一个固定小 ζ disk，再取较大 disk 供 (15) 用。背景 (a₀,b₀,H₀) 的 E_n 序列属于 ℓ²，故其所有高频尾的 sup norm 趋于零；(6) 也保证准确背景碰撞位于这些 disks 内。由 (14)–(15) 的解析 Lipschitz 界，增大 N、缩一个源半径 ε 后，所有 ℓ、|n|≥N 的真实 matrix 都落在同一 Riesz/Weierstrass perturbation budget 内。

用 (10) 把实际 rank-two image 送回 template 的 fast/slow-ℓ 平面。得到

\[
B_{\ell n}(\zeta,z)=
\begin{pmatrix}e^{L\zeta}&0\\0&1\end{pmatrix}
 + Q_{\ell n}(\zeta,z),
\qquad (Q_{\ell n})_{\ell,|n|\ge N}\in\ell^2(A_r).
\tag{18}
\]

这是实际 compression，两个 eigenvalues 准确等于该实际 cluster 的 multipliers。Riesz integral、intertwiner、压缩和 finite scalar normalization 都是均匀 bounded holomorphic matrix operations；在 E=0 时 correction 为零。它们的 Taylor 展开与 ℓ² 的 multiplier ideal 界给 (18) 的 strong analytic 映射。有限个 channels ℓ 不改变 ℓ² 结论。

令

\[
D_{\ell n}(\zeta,z)=(\operatorname{tr}B_{\ell n})^2-4\det B_{\ell n}.
\tag{19}
\]

选 r<2π/L 并在边界 |ζ|=r 保持 |(e^{Lζ}−1)²| 的正下界。统一 Q-smallness 后，Rouché 给 D 在 disk 内准确两个 roots，含重数，记其无序对 ζ±。不选择平方根标签，直接定义 contour moments

\[
s_j=\frac1{2\pi i}\oint_{|\zeta|=r}\zeta^j
\frac{\partial_\zeta D}{D}\,d\zeta,\qquad
c_{\ell n}=\frac{s_1}2,\qquad
g_{\ell n}=\frac{s_2}2-c_{\ell n}^2.
\tag{20}
\]

c=(ζ++ζ−)/2，g=((ζ+−ζ−)/2)²。这些是对源 holomorphic 的实际根函数，即使两根未打开也有定义。

绝对 λ-center 是 K_n+hℓ(H)+cℓn；g 与这一步平移无关。hℓ(H) 本身这里只是 calibrated holonomy 的坐标，没有宣称它是原 class invariant。统一 Q-smallness 可使两根位于 |ζ|<r/2；再缩源使 |hℓ(H)−pℓ|<r/8，取 N 使 (6) 的背景 shift<r/8。这对实际 roots 始终属于以固定 λℓn 为中心、互不重叠的同一标签窗口。两根的绝对 λ 位置和差由实际 repeated-multiplier 位置决定：在邻域中通过 (6) 的标签唯一延续，因此不受 frame similarity 或 monodromy 的非零 scalar normalization 影响。特别 (19) 是 rank-two characteristic discriminant，未以一般 M 的一个 trace 代替全部 characteristic classes。

## 5. 实际谱隙平方 ℓ¹、中心 ℓ²：同一个源域

令 B₀=diag(e^{Lζ},1)。它的 D₀=(e^{Lζ}−1)²。对任意 holomorphic matrix variation Q，其一次项准确为

\[
D_1=2(e^{L\zeta}-1)(Q_{11}-Q_{22}),\qquad
D_1/D_0=2(Q_{11}-Q_{22})/(e^{L\zeta}-1).
\tag{21}
\]

D₁/D₀ 在 ζ=0 至多是 simple pole。对 (20) integration by parts，

\[
\delta s_2=-\frac1{\pi i}\oint\zeta D_1/D_0\,d\zeta=0.
\]

因 c₀=0，得到 Dg(0)=0。均匀 bounded holomorphic contour functional 的 Taylor estimate 因而给

\[
|c(Q)|\le C\|Q\|_{A_r},\qquad
|g(Q)|\le C\|Q\|_{A_r}^2.
\tag{22}
\]

故在同一个物理 ε-ball、同一个 N 上

\[
\boxed{\quad
z\longmapsto(c_{\ell n}(z))\in\ell^2,
\qquad z\longmapsto(g_{\ell n}(z))\in\ell^1
\quad\text{均为 strong analytic。}\quad}
\tag{23}
\]

解析性不只是 coordinatewise：对 gap 的 degree k≥2 多线性 Taylor 项，用 ∑_n∏_{j=1}^k||Q_n^j||≤||Q^1||ℓ²||Q^2||ℓ²∏_{j≥3}||Q^j||ℓ∞，而 ℓ²⊂ℓ∞，结合均匀 Cauchy coefficient bound 即给在 ℓ¹ 中绝对收敛的 Taylor series。中心的 degree≥1 使用同样的 ℓ² ideal 界。这也覆盖有限 H-parameters 和所有 channels。

背景源 0 的实际 gℓn=0，其 Q(0) 一般并非 abstract Q=0，所以不能直接以 (21) 断言原源 derivative 为零。另在准确 λℓn 附近，用背景实际 generator 的解析 eigenbasis 对角化 block，记 ξ=λ−λℓn、F_n(ξ)=ν_f(λ)−νℓ(λ)。由 (7) 它在 ξ=0 有 simple zero，背景 D=F_n²。任意源一次项仍准确为 2F_n(dot B11−dot B22)，比值至多有 simple pole。把 (20) 的 moments 改用 ξ（g 对平移不变），同一分部积分给 δs₂=0；背景 ξ-center=0，故 Dgℓn(0)=0。strong ℓ¹ derivative 的全部坐标都为零，故 Dg(0)=0 在 Banach 意义成立。特别 g(z)=O(||z||²_X₀) 在 ℓ¹ 中，Taylor 的 cubic remainder 也在 ℓ¹ 中为 O(||z||³_X₀)。

这是同源 balanced Sobolev→实际 invariant gap sequence 的无失真估计；没有从 C^R 源到较低 h^t 的估计替代它。ℓ¹ 的 gap squares 比 framed 全矩阵的 ℓ² 更强，来自 double-root gap functional 的一次项消失。

## 6. 实际 first Born couplings 与准确二阶谱隙 Hessian

下面在准确背景点 λℓn 使用实际 generator A₀(λ)，不是 leading grid。选它的 fast/slow-ℓ right eigenvectors e_f,eℓ 和 dual left rows ℓ_f,ℓℓ；用 χ orthonormal frame 经固定 split 相似变换校准，所以这些 basis/dual norm 对 n 一致 bounded。设实际 common multiplier ρℓn=e^{Lyℓ(λℓn)}。Fourier convention 为

\[
\widehat F_n=L^{-1}\int_0^L F(x)e^{-i\kappa_nx}\,dx.
\]

对物理 tangent f∈X₀，在 calibrated (2) frame 中写 dot A(x)=DA(0)f。它对 λ 的 principal part为零。均匀处 D⟨a⟩=D⟨b⟩=DH=0 已由物理状态图证明，因此 ⟨dot A⟩=0。实际 monodromy variation 准确是

\[
\dot M=M_0\int_0^Le^{-A_0x}\dot A(x)e^{A_0x}\,dx.
\tag{24}
\]

定义

\[
\Gamma^+_{\ell n}(f)=\ell_f\widehat{\dot A}_{n}e_\ell,
\qquad
\Gamma^-_{\ell n}(f)=\ell_\ell\widehat{\dot A}_{-n}e_f.
\tag{25}
\]

因 y_f−yℓ=iκ_n，准确碰撞 block 的 offdiag 一阶项分别为 ρℓn LΓ+ 和 ρℓn LΓ−；diagonal 一阶项为零。moving frame 的 derivative 只产生与 scalar collision block ρI₂ 的 commutator，故在这一点消失；moving λ-center 的一阶导数同样不改变这两个 offdiag entries。

背景 (19) 在准确 λℓn 的 leading quadratic 是 ρ²L²γ²(λ−λℓn)²；源的 constant quadratic 项是 4ρ²L²Γ+Γ−。其余 off-cluster effects 已被实际 Riesz compression 包含，并不改 degree-two Weierstrass polynomial 的这一系数。因此

\[
\boxed{\quad
g_{\ell n}(\varepsilon f)
=-\frac{4\varepsilon^2}{\gamma_{\ell n}^2}
\Gamma^+_{\ell n}(f)\Gamma^-_{\ell n}(f)
 +O_{\ell^1}(\varepsilon^3\|f\|_{X_0}^3).
\quad}
\tag{26}
\]

g 定义为半根差的平方，所以符号和 factor 4 如上；D²g(0)[f,f]=−8Γ+Γ−/γ²。任意 f₁,f₂ 的双线性 Hessian 是 −4[Γ+(f₁)Γ−(f₂)+Γ+(f₂)Γ−(f₁)]/γ²。

两 Γ-sequences 从 X₀ bounded 到 ℓ² 可直接由 Parseval 证明：dot A(x) 与 λ 无关（principal variation=0、DH(0)=0），X₀→L² 的 DA 有界；实际 χ generator 在纯虚 λℓn 的 orthonormal eigenbasis 经固定 T₀ 换基后，使全部 e、dual norm 对 ℓ,n 一致有界。因此 |Γℓn±|≤C||widehat(dot A)±n||，有限 ℓ 加总后得到 ℓ²。γ 有一致非零下界，故 (26) 与 (23) 的 ℓ¹ Hessian 完全相容；不需要额外 λ-grid shift 比较。

对实物理源，C₀ 与原 coefficients 为实、λℓn 纯虚，负频率的 conjugate channel 是 (M−ℓ,−n)。basis 的 phase 可配成这个 conjugation；于是 g_{M−ℓ,−n}=overline(gℓn)，Γ 的同一 conjugate correspondence 自动成立。未把每个正 n 的全部 gℓn 擅自当成实数，也未借用 M=2 的额外实结构。

## 7. framed norming 候选与尚未解决的步骤

在 (18) 的固定 template rank-two frame 中，取实际 moving center 的非对角项

\[
\mathfrak n^+_{\ell n}=(B_{\ell n}(c_{\ell n}))_{12},\qquad
\mathfrak n^-_{\ell n}=(B_{\ell n}(c_{\ell n}))_{21}.
\tag{27}
\]

template 的 offdiag 恒零；(15)、(18) 和 |cℓn|<r/2 给 (n+,n−)∈ℓ² strong analytic。可以再用一个 uniform bounded、I+O(1/n) 的背景两维换基，使背景碰撞处 basis 与 §6 实际 generator basis 相同；其 template offdiag 修正含 O(1/n)(e^{Lc_n}−1)，仍为 ℓ²。保留 (18) 除以 template ρℓ(H) 的规范时，这个 calibration 下 first variation 准确为 χℓn LΓ±，其中 χℓn=ρℓn/ρℓ(H₀)=1+O(1/n)，而不是直接 LΓ±。若另把每个 norming 候选除以已知的背景常数 χℓn，才得到准确 LΓ±；这个 uniformly bounded scalar 改动保留 ℓ² 和解析性。source frame variation 在背景 scalar block 处消失。

(27) 是完整 frame 下的实际 norming 候选。未证明这些数据在 finite physical graph 上 locally onto、没有证明它们给全状态逆，也未证明 canonical Poisson 关系或正则谱隙族 Hamiltonian 闭包=共同 differential annihilator。所需下一步包括：一般 M 的 multichannel squared-eigenfunction completeness；norming/divisor 与 finite physical graph 的准确兼容；原弱辛结构中规范坐标及无限闭包。已完成的 framed 全状态 IFT 不能自动填补这些 invariant/action-angle 步骤。

本引理的实际进展是：一般 M、任意固定满足 (NR) 的均匀 δ、同一个 X₀ 源开邻域、全部足够高频上的 rank-two actual monodromy reduction；实际 gap squares 的 ℓ¹ 解析性、实际中心 correction 的 ℓ² 解析性和准确 first Born 二阶 Hessian。它未宣称一般物理 DLW 的完整 Liouville 可积性。

## 8. 新有限高频 actual gap 独立性：准确实维数与 Fourier 见证

### 8.1 全部 high-channel coupling 的一致线性逆

以下仍在 (1) 的固定均匀分量均值叶，不把这份结果推广到所有均值叶。前引物理状态逆准确给

\[
D\Pi(0):X_0\longrightarrow (L^2_0)^{1\times m}_a\times(L^2_0)^{m\times1}_b
\quad\text{bounded isomorphism},\qquad
D\langle a\rangle=D\langle b\rangle=DH=0.
\tag{28}
\]

该 derivative 是在常数背景的 translation-equivariant Fourier multiplier。其逐非零模矩阵可逆，所以任意 finite Fourier a,b tangent 的源原像也为 finite Fourier，且保留实 conjugation。

选择 H₀ 的 right/left slow eigenbasis sℓ,tℓ，t_j sℓ=δ_jℓ，配成 s_{M−ℓ}=overline(sℓ)、t_{M−ℓ}=overline(tℓ)。由实际 finite generator

\[
A_0(\lambda)=\begin{pmatrix}\lambda&q_0\\r_0&H_0\end{pmatrix}
\]

及其 simple branches 的有限维 perturbation，fast basis 可以规范为

\[
e_f=(1,O(n^{-1}))^T,\qquad \ell_f=(1+O(n^{-2}),O(n^{-1})),
\]
\[
e_\ell=(O(n^{-1}),s_\ell+O(n^{-1}))^T,\qquad
\ell_\ell=(O(n^{-1}),t_\ell+O(n^{-1})).
\tag{29}
\]

这里按每个准确 λℓn 取 basis，O-bounds 仍在有限 ℓ 中一致。可以直接解 fast 下方分量 (y_f−H₀)⁻¹r₀=O(1/n)，slow 的 top 分量 q₀eℓ,slow/(yℓ−λ)=O(1/n)，然后用 distinct H₀ roots 与 dual normalization 得其余式。

对一个 real source tangent 的正 n 模，任意 complex row/column A_n,B_n 都可由 (28) 实现，而且

\[
\widehat{\dot A}_{n}=\begin{pmatrix}0&A_n\\B_n&0\end{pmatrix},
\qquad\widehat{\dot A}_{-n}=\overline{\widehat{\dot A}_{n}}.
\]

于是一个准确 complex-linear 方阵是

\[
T_n:(A_n,B_n)\longmapsto
(\alpha_{\ell n},\beta_{\ell n})_{\ell=1}^m,
\quad\alpha_{\ell n}=\Gamma^+_{\ell n},\quad
\beta_{\ell n}=\overline{\Gamma^-_{\ell n}}.
\tag{30}
\]

complex linearity 采用实场的负 Fourier conjugation，把 Γ− 的整体 conjugate 后只依赖 A_n,B_n。式 (29) 准确给

\[
T_n(A_n,B_n)=
\big(A_n s_\ell,\ t_{M-\ell}B_n\big)_{\ell=1}^m
 +O(n^{-1})(|A_n|+|B_n|).
\tag{31}
\]

极限矩阵是 slow eigenbasis 与其 inverse，另含 ℓ↦M−ℓ 的 permutation，故可逆。增大 N 后 T_n 及 T_n⁻¹ 在全部 n≥N 一致 bounded。这是准确 physical Fourier channel inverse；没有假定不同分量的原 bracket 是 arbitrary identity offdiag。

### 8.2 每个有限高频 block 的实际 nonlinear 梯度独立

取任意 finite positive frequencies F⊂{n≥N}。由 (30) 的真实逆和 (28)，可选一个 real finite Fourier source tangent f，使全部选中通道 αℓn=βℓn=1，并令未选 Fourier modes 为零。同时可选 2m|F| 个 real finite Fourier test directions h_j，使选中模式 δα=0，而 δβ 分别为各 complex coordinate 的 1 与 i。

由 (26)，实际 g 在 εf 的 Jacobian leading term 等于 ε 乘 quadratic gap 的 Jacobian；每个通道是

\[
Dg^{[2]}_{\ell n}(f)h
=-4\gamma_{\ell n}^{-2}\,\overline{\delta\beta_{\ell n}},
\qquad (\delta\alpha=0).
\tag{32}
\]

它作为 complex 一维的 real map 可逆；exact Born selection 的 ±n Fourier phases 使不同 n 无交叉 block。故所选 real functions

\[
\big(\operatorname{Re}g_{\ell n},\operatorname{Im}g_{\ell n}\big)_
{1\le\ell\le m,\ n\in F}
\tag{33}
\]

在 εf 的一个 2m|F|×2m|F| Jacobian minor 等于 ε^{2m|F|} 乘非零常数加 O(ε^{2m|F|+1})。对充分小 ε≠0，它们的实际 nonlinear differentials 独立。这些 witnesses 可任意接近均匀态；未把均匀点的零梯度误报成独立。

正 n 的 m 个 g 通常是 complex。对应负通道 g_{M−ℓ,−n}=overline(gℓn)；因此 (33) 的计数是每个正频率 2m 个实函数，不额外再计负频率，也不把全部正频率 g 当实值。

每个上述 finite minor 是源球上的 real analytic function，且已有 arbitrarily near-zero 的非零 witness，所以在 connected 源球不恒零，其非零 locus 为 open dense。所有 finite positive sets 是可数族；Baire 给一个 residual 子集，在其上全部 finite high-frequency blocks (33) 同时独立。这个结论目前落在实际 X₀ 源球；不是无穷 Hamiltonian 闭包定理，也没有声称 g 与全部 formal C_n 的合并族独立。

### 8.3 精确的 strong-chart 传递前提

若另一个已证共同 strong 域以 real analytic parameter map F:O_H→X₀ 给出，F(0)=0，且 DF(0) 的 range 含本节所有 finite real physical Fourier directions，则这一 finite-gap 结论可在同一个 parameter ball 传递：Dg(0)=0 使 D²(g∘F)(0)=D²g(0)[DF(0),DF(0)]，没有 D²F 的 correction。选 f,h_j 的 H 原像后，沿 εf_H 的同一 minor leading term 非零；对可数 finite blocks 取 Baire intersection。因此强域中的 generic 参数拥有全部 finite high-gap blocks 的实际独立性。

这一段明确以 F 的上述已证解析性、共同域和 Fourier-range 为前提；不能仅凭 X₀ residual 集或 ambient smooth 密度断言它与一个较薄 strong 域相交。它也不声称全部 gap flows 在 X₀ 中存在、norming canonical、regular-level 最大各向同性，或完整一般 M Liouville theorem。
