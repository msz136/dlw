# 一般 M 的周期 holonomy 规范、平衡 Sobolev 物理状态逆与有限图约束

2026-10-11。接续 [谱主稿 §§16–17](../../刘维尔可积性/research/spectral_independent_review_20261011.md)，从原 DLW 的精确 rank-one splitting 构造一般 M 的实际物理像。新增的是平衡 Sobolev Banach 状态逆、有限 holonomy/零模约束与局部常数 gauge 刚性。这里未构造从 Floquet divisor/norming 谱数据到向量势的逆，未证明一般 M 的 squared-eigenfunction 闭包或 Liouville 最大性。

式 (1)–(26) 已经 [本支独立审查](all_m_holonomy_image_independent_audit_20261011.md)、[第二份一般 M 独审](general_m_periodic_gauge_state_inverse_independent_20261011.md) 及 [根任务复核](root_general_m_periodic_state_inverse_audit_20261011.md) 核验。后两者另证明 balanced low-domain 版本与高阶 bootstrap；未重跑任何旧证书。

## 1. 原 free fields、uniform 背景及保留 B 的精确系统

令 M≥2、m=M−1、S=Mδ≠0、δ∈R，x∈R/(LZ)、k₀=2π/L。固定原物理分量均值叶；以 q_j、d_j（j<m）为准确 free fields，d_m=S−Σ_{j<m}d_j。取 uniform 叶

\[
d_j^0=\delta,\qquad q_j^0=-2\delta(m-j),\qquad
u_j=q_j-q_j^0,\quad v_j=d_j-\delta,\quad
\langle u\rangle=\langle v\rangle=0.
\tag{1}
\]

\(\langle f\rangle=L^{-1}\int_0^Lf\)。设 \(A_{j\ell}=\operatorname{sgn}(\ell-j)\)、\(\Delta_j=q_j+S+(Ad)_j\)、Δ_m=0。在 centered B=0 截面，原 b_j 的闭合是

\[
b_m=-S^{-1}\sum_{j<m}d_j\Delta_j,\qquad b_j=b_m+\Delta_j,
\qquad C_{ij}=b_i\delta_{ij}+d_i\operatorname{sgn}(j-i).
\tag{2}
\]

原 free 张量为普通积分配对下 \(J=-(1/16)\operatorname{offdiag}(I_mD)\)，本稿没有另换物理 bracket。用 Z_j=e_j−e_m、E 选择前 m 分量，原精确 splitting 为

\[
T_z=[d/S,Z],\quad T_z^{-1}=[1^T;E-(d_{\rm first}/S)1^T],
\]

\[
\binom\phi\xi'=
\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}\binom\phi\xi,
\quad
V=ECZ-d_{\rm first}q/S,\quad
r=(ECd-d_{{\rm first},x})/S.
\tag{3}
\]

prime 作用于整列。最后一个 r 公式使用原准确闭合 1ᵀCd=0，亦有 1ᵀd_x=0；不是忽略 state-adapted frame 的导数。q 在 (3) 正是 free q。V 是 q,d 的 zero-order 微分多项式，且对 q 线性；r=F(q,d)−d_first,x/S，F=ECd/S 也 zero order、对 q 线性。所有分母只有固定 S。T_z 始终可逆，允许任一单独 d_j 为零。

任意实 spatialconstant B=Γ/(2c) 只给 b_j^B=B+b_j、q^B=q、r^B=r、V^B=V+BI_m。raw top parameter是 λ_original；从整个 split connection 减 BI_M 后，参数准确变为 λ=λ_original−B、内部矩阵回到 V。本稿以下用 centered V,H；最后恢复任意 B。B(t) 可由原方程外给，不把它冻结为新守恒量。

在 (1) 背景，C₀=δ(s_ij)_{M×M}，s_ij=sgn(j−i)，且

\[
(r_0)_i=\frac\delta M(m-2i),\qquad
(V_0)_{ij}=\delta\left[-\delta_{ij}-2\mathbf1_{j<i}
+\frac{2(m-j)}M\right]
=\delta\left[\operatorname{sgn}(j-i)+\frac{m-1-2j}M\right].
\tag{4}
\]

例如 M=2 为 V₀=0、r₀=δ/2；M=3 为 V₀=δ[[1,2],[−2,−1]]/3。这些仅是标度校准，不用 M=2 推一般 M。

## 2. Uniform 内部 holonomy 与准确非共振条件

原 uniform scalar symbol 是

\[
L_0(y)=S\frac{(y+\delta)^M+(y-\delta)^M}
{(y+\delta)^M-(y-\delta)^M}
=y-q_0(yI_m-V_0)^{-1}r_0.
\tag{5}
\]

分子、分母互素，reduced denominator 的次数为 m。因右端 realization 的维数正是 m，其 characteristic denominator 准确为

\[
\det(yI_m-V_0)=\frac{(y+\delta)^M-(y-\delta)^M}{2S}.
\tag{6}
\]

所以 V₀ 有 m 个不同 eigenvalues

\[
p_\ell=-i\delta\cot(\pi\ell/M),\qquad 1\le\ell\le m.
\tag{7}
\]

这里只是将根作一种排序；取相反号是同一个无序集合。本文主要假设

\[
\boxed{\quad p_j-p_\ell\notin ik_0(\mathbb Z\setminus\{0\})
\quad\text{对全部 }j,\ell.\quad}
\tag{NR}
\]

这是内部 holonomy 无 multiplier alias，而不是原 physical trace 的所有 gap 已打开。M=2 自动满足；每个固定 M>2 排除一组离散 δ 值。一个直接、保守的充分条件是 0<|δ|<k₀/(8m)：由 (4) 的 entries bound 得 ||V₀||op≤2m|δ|、||ad V₀||≤4m|δ|<k₀/2，所以非零 Fourier resolvents (ik−ad V₀)⁻¹ 的 norm≤2/|k|。

(NR) 一般情形下，各低频 resolvents 只有有限个，全部可逆；高频用 Neumann bound。因此

已有 mixed strong 图所用的 \(|\delta|<(k_0/2)\tan(\pi/(2M))\) 自动满足 (NR)：令 t=tan(π/(2M))，由 (7)
\[
\max_{j,\ell}|p_j-p_\ell|=2|\delta|\cot(\pi/M)
<k_0(1-t^2)/2<k_0.
\]
因此把新状态图接到该已有域无需额外缩 c。小背景 Neumann 常数只是显式充分预算，不作为此接合的新前提。

\[
\mathscr R=(D-\operatorname{ad}V_0)^{-1}:
H^s_0(S^1;\operatorname{Mat}_m)\longrightarrow H^{s+1}_0
\tag{8}
\]

对每个 s≥0 有界，均值零逐 entry 定义。其 norm 可依赖背景与到 alias 的距离。不会在 alias 点假称存在这个 ambient gauge chart。

## 3. 实际 mean-normalized periodic gauge：L²→H¹ 解析图

对 V 在 V₀ 附近的 L² 复球内，解实际矩阵方程

\[
G_x=VG-GH,\qquad \langle G\rangle=I_m,
\quad G\in H^1_{\rm per},\ H\in\operatorname{Mat}_m(\mathbb C).
\tag{9}
\]

先把 G=I+g、⟨g⟩=0。映射 \(\mathcal F(g,H,V)=G_x-VG+GH\) 从 H¹₀×Mat×L² 到 L² 复解析，因为一维 H¹ 是有界乘法子；没有使用 L² 自身为乘法代数。在 (G,H,V)=(I,V₀,V₀) 的 (g,H) 微分为

\[
(g,h)\longmapsto(D-\operatorname{ad}V_0)g+h.
\tag{10}
\]

(8) 处理全部非零模，h 处理矩阵零模，故 (10) 是 Banach 同构。analytic IFT 给 V↦(G,H) 的真实局部解析解。缩低阶球使 G 处处可逆；H¹ embedding 和 matrix inverse 的 H¹ 乘法给 G⁻¹∈H¹。积分 (9) 得

\[
H=\langle VG\rangle,
\qquad DG[V_0](\dot V)=\mathscr R P_0\dot V,
\quad DH[V_0](\dot V)=\langle\dot V\rangle.
\tag{11}
\]

这里 H 是完整 m×m constant matrix，不能只保留其 trace。G periodic 使 Y_V(L)=G(0)e^{LH}G(0)⁻¹；因此实际内部 holonomy 完整保留。

定义 periodic vector potentials

\[
a=qG\quad(1\times m),\qquad b=G^{-1}r\quad(m\times1).
\tag{12}
\]

diag(1,G) 的实际 periodic gauge 将 (3) 精确化为

\[
\mathcal A_\lambda=\begin{pmatrix}\lambda&a\\b&H\end{pmatrix},
\qquad
\mathscr L=D-a(DI_m-H)^{-1}b.
\tag{13}
\]

后一个等式来自 DI−V=G(DI−H)G⁻¹；既是原 formal scalar PDO 的准确等式，也是允许相应 resolvents 时的 operator 等式，不是丢弃 holonomy 的非周期 gauge。

## 4. 完整 physical derivative 与平衡低域

用实际源

\[
X_s=H^s_0(S^1;\mathbb C^m)_u\times H^{s+1}_0(S^1;\mathbb C^m)_v,
\qquad Y_s=H^s_0\times H^s_0,
\quad s\ge0.
\tag{14}
\]

当 s=0 时 q∈L²、d∈H¹；q 与 d 的 polynomial products 都在 L²，V,r∈L²，(9) 给 G∈H¹，因而 a,b∈L²。这是一条真正 balanced vector-potential chart。source 的 d 多一个导数正是 (3) 的 d_x，不藏额外 derivative loss。

令 Π(u,v)=(P₀a,P₀b)∈Y₀，背景 Π(0)=0。原 component means 仍固定；a,b 的均值尚未给作独立目标。Π 是 X₀→Y₀ 的真实解析映射。

下面写出其准确 derivative。令

\[
\dot\Delta_i=u_i+\sum_{\ell<m}s_{i\ell}v_\ell,
\quad t_i=\dot\Delta_i-M^{-1}\sum_{\ell<m}\dot\Delta_\ell,
\quad i<m.
\]

则原 physical δC 的 diagonal 为 t_i（最后分量为 −M⁻¹ΣdotΔ），offdiagonal为 \((Zv)_is_{ij}\)。记 W=δV、Z₁=δr+d_x variation/S，准确公式为

\[
W_{ij}=\delta_{ij}(t_i-v_i)-2v_i\mathbf1_{j<i}
+\frac{2(m-j)}M v_i-\frac{u_j}M,
\]

\[
(Z_1)_i=\frac1M\left[t_i+(m-2i-1)v_i-2\sum_{j<i}v_j\right].
\tag{15}
\]

由于源 u,v 均值零，W,Z₁ 也逐 entry 均值零，DH=0。用 \(g=\mathscr RW\) 得

\[
\boxed{\quad D\Pi_0(u,v)
=(u+q_0g,\ Z_1-Dv/S-g r_0),\qquad g=\mathscr R W.\quad}
\tag{16}
\]

零模没有被“忽略”：它们在这个固定物理叶上恰为零 derivative；下节把其非线性值写成 finite graph。对每个非零 Fourier k，(15)、(16) 是一个明确的 2m×2m matrix；\(g_k=(ik-\operatorname{ad}V_0)^{-1}W_k\)。这给原 physical derivative 的 exact infinitesimal map，而不是 arbitrary matrix Darboux 示例。

## 5. 非共振全部 δ 的 balanced inverse；小 δ 的直接预算

先对一个 smooth 单非零 Fourier 方向证明 (NR) 下 DΠ₀ 无核。因为 (16) 的各输出均值零，若该方向 DΠ₀(u,v)=0，则 Da=Db=0，且 DH=0。由 (13) 得原 scalar operator 的 δL=0，特别前 2m 个完整原 scalar coefficients 的 variation 为零。已经核验的 [原全 M finite-coefficient state inverse，谱主稿 §2](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 在 uniform δ≠0 上给该 coefficient derivative 的单射，所以这个方向的 u=v=0。本步只使用既有 derivative 单射作为依赖；新的结论是 balanced Banach inverse，不把旧 finite-jet C∞ 逆重新报成新结果。复化的单射由实部、虚部分别应用同一实 derivative 得到。先逐 smooth 模态使用 PDO coefficients，再由下面的 Fourier matrix bounds 延伸到全部 low L²×H¹ 源；从未在 arbitrary rough 源上定义无限 jet coefficients。

按 Fourier 模态此为一个 2m 方阵的单射，故每个非零 k 的方阵可逆。为证明其 inverse 的 Sobolev norm 统一有界，而不是只逐模 invert，令 ζ=−ikv/S。在 (16) 中 W 与 Z₁ 为 constant coefficients 的 u,v 组合，\(g_k=O(|k|^{-1})(|u_k|+|v_k|)\)。因此在 (u,ζ) 坐标，矩阵大频极限为

\[
\begin{pmatrix}I_m&0\\(Z_1)_u&I_m\end{pmatrix}+O(|k|^{-1}).
\tag{17}
\]

它是可逆三角矩阵；不能把这个极限误写为 identity。大频 inverse 统一有界，剩余有限低频矩阵可逆给共同有限界。(u,ζ) 的 l² norm 与 X₀ 的 L²×H¹ norm 在零均值空间等价。因此 DΠ₀:X₀→Y₀ 是 bounded Banach 同构；乘同一 Fourier Sobolev 权重得 DΠ₀:X_s→Y_s 对所有 s≥0 同构。

另可不借旧单射而在显式小背景直接用 Neumann 证明。取 normalized Sobolev weights \(w_s(k)=(1+k^2/k_0^2)^{s/2}\)、X_s 的两个分量 norm 之和。由 (2) 的 δC、||Z||op=√M、||A||op≤m，有

\[
\|W\|_{H^s}\le2(M+1)\sqrt M\|(u,v)\|_{X_s},\quad
\|Z_1\|_{H^s}\le3\sqrt M\|(u,v)\|_{X_s},
\]

\[
|q_0|\le2M\sqrt M|\delta|,\quad |r_0|\le\sqrt M|\delta|,
\quad \|D_0^{-1}\|_{H^s_0\to H^{s+1}_0}\le\sqrt2/k_0.
\tag{18}
\]

把 principal inverse \((\xi,\eta)\mapsto(\xi,-SD_0^{-1}\eta)\) 左合成 (16)，记其为 I+E；在 ||adV₀||<k₀/2 的域内，\(\varepsilon=|\delta|/k_0\) 给

\[
\|E\|\le14M^3\varepsilon+9M^3\varepsilon^2<1/4
\quad\text{若 }0<|\delta|\le k_0/(128M^3).
\tag{19}
\]

此保守 threshold 自动保证前述 nonalias bound。Neumann series 直接给 exact derivative inverse；可核查它并非有限频 truncation。主要 theorem 的 (NR) 域比 (19) 大，(19) 只作独立显式充分条件。

## 6. 真正 nonlinear physical state inverse 与有限 image constraints

由 §3–5 的 actual analytic maps 与 bounded DΠ₀，Banach analytic IFT 给同一低域：存在 X₀ 中源邻域 U、Y₀ 中数据邻域 O，使

\[
\boxed{\quad \Pi:U\longrightarrow O
\text{ 是局部解析 Banach 微分同胚。}\quad}
\tag{20}
\]

这是一条一般 M 的 infinite-dimensional 状态逆；不是某个有限维解族。它作用在原固定 component means 物理叶的低正则完成上。给数据 (ã,b̃)∈O，逆 q,d 实际唯一；再按 (9)、(12) 计算完整 a,b,H。于是存在有限值解析 functions α,β,ℋ，使原 physical image 在 L²_row×L²_col×Mat_m 中准确为

\[
\boxed{\quad a=\widetilde a+\alpha(\widetilde a,\widetilde b),
\quad b=\widetilde b+\beta(\widetilde a,\widetilde b),
\quad H=\mathcal H(\widetilde a,\widetilde b).
\quad}\tag{21}
\]

α=⟨a⟩、β=⟨b⟩，ℋ 是完整 constant matrix。因此 image 有**准确 2m+m² 个复 scalar graph 约束**（实物理像是对应 real form），没有额外 functional constraint。这里 ambient 的 H 保留全部 matrix entries；从未把它当作固定 background 或额外独立物理自由度。graph 在 uniform 的 derivative 为零：Dα=Dβ=Dℋ=0，来自 (15)、(16) 和固定源均值。

一个准确 nonlinear graph 分量可直接计算。periodic G 的 near-I logdet 积分导数为零，所以

\[
\operatorname{tr}H=\langle\operatorname{tr}V\rangle
=\left\langle\sum_{i=0}^m b_i\right\rangle
=-\delta^{-1}\langle u\cdot v\rangle,
\qquad \tau=\frac LM\operatorname{tr}H.
\tag{22}
\]

最后等式展开 (2) 后，用 ⟨u⟩=⟨v⟩=0；不会把非线性 scalar holonomy 当成 Casimir。其二阶值与 §16 的 translation Hamiltonian 一致。

物理 component means 必须给定。若允许它们变化，可把这些均值作为有限参数附在 (20)；同一 IFT 给附近均值叶的参数化族。不能从 projected a,b 独自声称恢复全部 Casimir 均值，M=2 uniform 的常 d 变分已可使 first derivative 消失。

## 7. 同一低域上全部高阶正则性，不重复缩低域

在 (20) 的同一个 O 中，若 (ã,b̃)∈Y_s，则 (21) 中的 finite constants 仍是低域解析值，故 a,b∈H^s。实际低域 inverse 满足

\[
q=aG^{-1},\qquad
G_x=V(q,d)G-GH,\qquad
d_{{\rm first},x}=EC(q,d)d-SGb.
\tag{23}
\]

这些是准确 coupled first-order ODEs，V、ECd 都 zero order，对 q 线性。低域已给 d,G∈H¹。对于整数 s≥1，H¹ multiplication 先给 q∈H¹，再由 (23) 给 d,G∈H²；递推 H^j algebra 得 q∈H^j、d,G∈H^{j+1}，直到所需 s。若 s 非整数，先完成 floor(s) 阶递推，使 d,G∈H^{floor(s)+1}；该空间是 H^s 的有界 multiplier，然后将 (23) 右端置于 H^s，直接给 d,G∈H^{s+1}。0≤s<1 由已有 H¹ multiplier 同样得到。于是 source 在 X_s，无需因高阶 norm 大而缩 O。

线性化 (23) 后有同样 bootstrap，finite graph derivatives 由低域 analytic maps 控制。DΠ 的 low inverse在所有 X_s、Y_s 间仍可提升；closed graph 给各阶有界，再在任一该域高阶点应用 analytic IFT。因此 \(\Pi^{-1}:O\cap Y_s\to X_s\) 局部解析，对 smooth 数据给同一低域的 C∞ graded inverse。这里只证明 state chart 的共同低域，不将它误当成原 physical Hamilton 方程在 balanced X₀ 的 Cauchy flow；§16 的 order-zero 流另用同阶各物理分量 Hs 域。

## 8. Full frame、常数 gauge 横截性与 remaining norming gap

完整 original χ frame 没有丢弃。令

\[
\mathcal E_z(x)=T_z(x)\operatorname{diag}(1,G_z(x)).
\]

它周期；original monodromy 满足

\[
T_\chi(\lambda)=\mathcal E_z(0)\,T_{\mathcal A}(\lambda)\,\mathcal E_z(0)^{-1}.
\tag{24}
\]

由 (20) 的 physical inverse，G_z(0)、T_z(0) 均为 recovered state 的实际可计算函数；不能把 class 数据 T_𝒜 的共轭类当作已知 full framed Tχ。若改用 G^f(0)=I 的 Floquet gauge，令 G^f=G G(0)⁻¹、H^f=G(0)H G(0)⁻¹，准确保留同一 holonomy；两种 frame 的常数过渡一般具有 first derivative，不能和 (21) 的零模 graph derivative 全零混淆。

原 full background (5) 在每个 simple pole p_ℓ 的 residue 是

\[
\operatorname{Res}_{y=p_\ell}L_0(y)=\delta^2-p_\ell^2
=\delta^2\csc^2(\pi\ell/M)\ne0.
\tag{25}
\]

若 P_ℓ 为 V₀ 的 spectral projector，则 q₀P_ℓr₀=−res L₀≠0。因此 (q₀,V₀) observable、(V₀,r₀) controllable。常数 GL_m action \((a,b,H)\mapsto(aQ,Q^{-1}b,Q^{-1}HQ)\) 的 infinitesimal uniform 方向是

\[
(q_0X,-Xr_0,[V_0,X]).
\tag{26}
\]

它全为 finite constant components；(21) 的 physical graph tangent 在这些 components 为零。若 (26) 为零，V₀ simple 使 X=Σx_ℓP_ℓ，而 q₀P_ℓ≠0 强制全部 x_ℓ=0。故 m² 个常数 gauge 方向与 physical image 相切的核为零。

从 (21) 的 finite constraints 选择一个对 X 满秩的 m²-component minor，analytic finite-dimensional IFT 给 uniform 邻域内常数 gauge 横截性：若 physical data 与其一个充分接近 I 的 Q-transform 都在同一 fixed-mean physical graph 内，则 Q=I。这里仅排除了这个准确 finite gauge 冗余；没有声称完整 monodromy data 的 kernel 已全是这种 gauge，尤其没有排除 λ-dependent gauges 或证明 nonlinear spectral norming inverse。

该局部结论可去掉显式 Q 近 I 条件，只要求两端 data 都在这个足够小 uniform 邻域：observability matrix \(\mathcal O(a,H)\) 的各行为 ⟨a⟩H^j、0≤j<m，背景可逆且在邻域仍可逆；\(\mathcal O(zQ)=\mathcal O(z)Q\)。两端都靠近同一背景遂强制 Q=𝒪(z)⁻¹𝒪(zQ) 靠近 I，再应用上述唯一性。

任意 B 时 G,a,b 仍完全相同，raw H_B=H+B I_m，\(\operatorname{tr}H_B=mB-\delta^{-1}\langle uv\rangle\)。从 raw block connection 减 B I_M 给 centered λ_original−B、H；raw monodromy另乘 e^{BL}。B 是已给外部规范参数，不能由不含它的 projected a,b 独立恢复，也不能将其固定写入原 PDE。full frame (24) 与 centered actual class 数据相容。

本稿所得是一般 M 的实际 periodic coefficient/state inverse和严格 finite physical image constraints。尚缺把实际 Floquet divisor/norming data 变成 (a,b,H) 的 weighted nonlinear inverse、把原 physical J 推到这些 spectral coordinates 的完整 action/norming 配对，以及 common action-gradient kernel 的 nonlinear closed-span equality。只有这些后续步骤完成后，才可讨论一般 M 的 Liouville 最大各向同性；本稿没有声称已经完成。

## 9. 固定初值 frame 的同一 physical inverse

为接以后真正 framed spectral 数据，把 §8 的过渡直接用于状态图。令 Q_z=G_z(0)，G_z^f=G_zQ_z⁻¹、H_z^f=Q_zH_zQ_z⁻¹，a_z^f=a_zQ_z⁻¹、b_z^f=Q_zb_z。G^f periodic、G^f(0)=I，源解析依赖保持；实际 transformed block monodromy 与 state-adapted split monodromy在 x=0 的 frame **准确相同**。

固定物理均值叶上，at uniform Q₀=I，\(\dot Q=g(0)\)，所以
\[
\dot a^f=u+q_0g-q_0g(0),\qquad
\dot b^f=Z_1-Dv/S-g r_0+g(0)r_0,
\quad \dot H^f=[g(0),V_0].
\tag{27}
\]
两个 g(0) 项都是 constant；P₀ 精确杀掉它们。因此 \(\Pi^f=(P_0a^f,P_0b^f)\) 的 derivative 与 (16) 完全相同，(NR) 下同一 balanced analytic IFT 给新的 local physical inverse \(\Pi^f\)。其 full data 仍是 2m+m² 个 finite graph 约束，但与 (21) 的 mean-normalized graph 不同：例如 \(D\langle a^f\rangle=-q_0g(0)\)、\(D\langle b^f\rangle=g(0)r_0\)，H^f 的 derivative通常也非零。不得把它们写成 quadratic-only constraints。

高阶 regularity 仍由 (23) 及此 constant transition 在同一低域 bootstrap。给完整 framed periodic vector potentials (a^f,b^f,H^f)，其非零模部分通过 \(\Pi^f\) 直接恢复 physical q,d，无需猜测一个未知 constant gauge。此处的“framed”只是已经得到的 **coefficient frame**；从 original full monodromy 或 divisor/norming spectral data 恢复这些 coefficients 的实际估计仍是下一步骤，未在 (27) 中被假定完成。
