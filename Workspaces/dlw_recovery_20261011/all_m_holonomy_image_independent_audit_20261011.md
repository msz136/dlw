# 全 M 周期 holonomy 规范及原物理像：独立审查

2026-10-11。只审查原 general-M split 到 periodic constant-connection 规范的实际物理像。依据 `GENERAL_PERIOD_MATRIX_LAX.md`、`GENERAL_PERIOD_FREE_FIELD_POISSON.md` 和 `spectral_independent_review_20261011.md` §§16–17，以下重新推导，不使用旧 finite-coefficient inverse 作新的逆定理，也不重跑旧证书。

## 1. 结论及准确范围

固定有限 M≥2、周期 L>0，m=M−1，k₀=2π/L。在 centered B=0 的原零分量均值叶，取均匀背景 dᵖʰʸˢ_j=δ≠0、bᵖʰʸˢ_j=0、S=Mδ。这里上标 phys 区分原物理 b_j 与下文 vector-AKNS 列 b。

对于每个 s≥1，δ 足够小且非零时，真实周期规范

\[
G'=VG-GH,\qquad \langle G\rangle=I_m
\tag{A1}
\]

有唯一邻近背景的实解析解 G∈H^{s+1}、H∈Mat_m，G 点点可逆。令 a=qG、b=G⁻¹r。原物理像在 (a,b,H) 的 H^s×H^{s−1}×Mat_m 空间中是一个有限余维解析图；其独立坐标可选为

\[
\Psi(q,d)=\left(P_0(a-q_0),-S D_0^{-1}P_0(b-r_0)\right)
\in (H^s_0)^{2m}.
\tag{A2}
\]

这里 ⟨f⟩=L⁻¹∫f、P₀f=f−⟨f⟩、D₀⁻¹ 是零均值 Fourier primitive。Ψ 在固定原分量均值的同一物理叶上有同阶 H^s 实解析局部逆。完整输出的 2m 个分量均值与 m² 个 holonomy 坐标都是该 core 的有限解析图函数；它们在 mean-normalized 规范下从二次阶开始。

一个保守的充分条件是

\[
0<|\delta|\le \frac{k_0}{148m^{5/2}}.
\tag{A3}
\]

小 δ 只用于本节原物理像的同阶逆定理。它不限制主稿 §§16–17 的全幅度实际谱对合及 C_n 桥。这里的 (a,b,H) 保留完整函数系数，并未变为谱 eigenvalues/norming data；因而没有证明谱完备性、作用角定理或最大各向同性。

## 2. 均匀 V₀ 的精确谱

按 i,j=0,…,m−1 排列，原公式直接给

\[
(q_0)_j=-2\delta(m-j),\qquad
(r_0)_i=\frac{\delta(m-2i)}{M},
\]

\[
(V_0)_{ij}=\delta\left[-\delta_{ij}-2\mathbf1_{j<i}+\frac{2(m-j)}M\right].
\tag{A4}
\]

令 Z 的列为 e_j−e_m，U=I−11ᵀ/M。全 M 背景矩阵 C₀ 的项为 δ sgn(j−i)，所以 C₀ 是 skew，V₀ 是 UC₀ 在 ker1ᵀ 上用 Z 表示的矩阵。若 z∈ker1ᵀ 是其 ζ 特征向量，则 C₀z=ζz+c1；相邻两行相减得到

\[
(\zeta+\delta)z_{j+1}=(\zeta-\delta)z_j.
\]

取 ω_ℓ=exp(2πiℓ/M)、z_j=ω_ℓ^{−j}，ℓ=1,…,m。其和为零，且对应

\[
\boxed{\zeta_\ell=\delta\frac{\omega_\ell+1}{\omega_\ell-1}
=-i\delta\cot(\pi\ell/M).}
\tag{A5}
\]

这些值彼此不同，给满 m 个 eigenvectors。等价地

\[
\det(zI_m-V_0)=\frac{(z+\delta)^M-(z-\delta)^M}{2M\delta}.
\tag{A6}
\]

这由上述全 M 特征向量证明；有限核验不承担推广。V₀ 不必在 Euclidean 坐标中 skew，但对 ZᵀZ=I+11ᵀ 的正定内积是 skew-adjoint。原物理 small-δ 背景的 slow holonomy 通常不是单位矩阵，而是 exp(LV₀)。

## 3. Mean-normalized periodic gauge 的真实解析构造

把 (A1) 写成 Banach 方程

\[
\mathcal F(V,g,H)=(I+g)'-V(I+g)+(I+g)H=0,
\qquad \langle g\rangle=0.
\]

其定义域取 H^s(V)×H^{s+1}_0(g)×Mat_m(H)，值域 H^s。s≥1 下乘法连续，故该方程复解析，并保持实子空间。背景解是 g=0,H=V₀。关于 (g,H) 的导数为

\[
(g,h)\longmapsto (D-\operatorname{ad}V_0)g+h,
\qquad \operatorname{ad}V_0(g)=[V_0,g].
\tag{A7}
\]

每个 V₀ 项绝对值≤2|δ|，所以 ||V₀||₂≤2m|δ|，||ad V₀||≤4m|δ|。若 4m|δ|≤k₀/2，则对非零 Fourier k=nk₀

\[
\|(ik-\operatorname{ad}V_0)^{-1}\|\le 2/|k|.
\tag{A8}
\]

因此 (A7) 是 H^{s+1}_0×Mat_m→H^s 的有界同构；逆先取 h=⟨f⟩，再逐非零 Fourier 求 g。Banach 解析逆函数定理给实际 (G,H)，不只是 formal Fourier 展开。H^{s+1} 嵌入连续函数，小邻域中 G 点点可逆。

空间积分 (A1) 还准确给

\[
H=\langle VG\rangle.
\tag{A9}
\]

令 Y_V'=VY_V、Y_V(0)=I。由 (A1) 得 Y_V(x)=G(x)e^{xH}G(0)⁻¹。因此真实 periodic holonomy 满足

\[
Y_V(L)=G(0)e^{LH}G(0)^{-1}.
\tag{A10}
\]

规范 ⟨G⟩=I 固定了内部常 GL_m 自由度：若 G→GC、H→C⁻¹HC，则 ⟨GC⟩=C，只有 C=I 保持归一化。不存在额外可自由选择的 m² 个常规范参数。

在任意较大 δ，若 L(ζ_ℓ−ζ_j)∈2πiℤ\{0}，则 (A7) 在对应非零频率失去可逆性，且指定 H₀=V₀ 的 ambient analytic logarithm 也出现指数映射导数退化。小 δ 条件排除这些 alias。不能在该条件之外默认同一规范 IFT；本审查未断言原受约束物理像在每个 alias 点必定失败。

## 4. 完整原物理线性化

写 q=q₀+u、d_first=δ1+v、d_m=δ−Σv_i，且 ⟨u⟩=⟨v⟩=0。设 A_{ij}=sgn(j−i)，e=uᵀ+Av。原物理 b_j−b_m 的精确差为 e_j；物理 b 的一阶变化为

\[
t_i=e_i-\frac1M\sum_{j<m}e_j\ (i<m),\qquad
t_m=-\frac1M\sum_{j<m}e_j.
\tag{A11}
\]

原 r 的唯一微分主部是 −d′/S。对 V、r 直接微分，得到

\[
W_{ij}=\delta V_{ij}
=\delta_{ij}(t_i-v_i)-2v_i\mathbf1_{j<i}
+\frac{2(m-j)}M v_i-\frac1M u_j,
\tag{A12}
\]

\[
z_i=\delta r_i
=R_i(u,v)-\frac1S v_i',\qquad
R_i(u,v)=\frac1M\left[t_i+(m-2i-1)v_i-2\sum_{j<i}v_j\right].
\tag{A13}
\]

这里 W、R 为常系数有限矩阵作用，系数只依赖 M，不含 1/δ。特别不能把 −d′/S 的 principal coefficient 漏成 −d′ 或忽略 G⁻¹ 对 r 的变化。

对真实 gauge 微分，

\[
h=\delta H=\langle W\rangle=0,\qquad
g=\delta G=(D-\operatorname{ad}V_0)^{-1}P_0W,\quad \langle g\rangle=0.
\tag{A14}
\]

所以完整 output 的一阶变化为

\[
\boxed{\delta a=u+q_0g,\qquad
\delta b=R(u,v)-v'/S-gr_0,\qquad
\delta H=0.}
\tag{A15}
\]

δa、δb 都零均值。holonomy 矩阵在固定原分量均值叶的 mean-normalized 规范中从二次阶变化；这不表示其非线性值被固定。

## 5. 同阶 source/core 逆函数定理与精确 infinitesimal inverse

由 (A15)，(A2) 的导数为

\[
D\Psi_0(u,v)=
\left(u+q_0g,
v-SD_0^{-1}\{R(u,v)-gr_0\}\right).
\tag{A16}
\]

用 Euclidean 向量、Frobenius 矩阵的 H^s norm，source/target 用两向量 norm 的和。A 的 norm≤m，(A11) 给 ||t_first||≤2(||u||+m||v||)，由 (A12)–(A13) 可取保守常数

\[
\|W\|_{H^s}\le8m\sigma,\quad
\|R\|_{H^s}\le5\sigma,\quad
\sigma=\|u\|_{H^s}+\|v\|_{H^s}.
\]

此外 ||q₀||≤2m√m|δ|，||r₀||≤√m|δ|，|S|≤2m|δ|，(A8) 给 ||g||_{H^s}≤16mσ/k₀。令 ε=|δ|/k₀≤1，则

\[
\|(D\Psi_0-I)(u,v)\|
\le\{(32m^{5/2}+10m)\varepsilon+32m^{5/2}\varepsilon^2\}\sigma
\le74m^{5/2}\varepsilon\sigma.
\tag{A17}
\]

故 (A3) 保证 ||DΨ₀−I||≤1/2。这些是常系数 Fourier 估计，常数无需随 s 增加；非线性局部邻域则可依赖 s、M、δ。精确一阶逆是收敛 Neumann series

\[
(D\Psi_0)^{-1}=\sum_{n=0}^{\infty}(I-D\Psi_0)^n.
\tag{A18}
\]

也可逐频明确写出。对每个非零 k，给定 core (α_k,y_k)，解唯一的 2m×2m 常系数系统

\[
g_k=(ik-\operatorname{ad}V_0)^{-1}W(u_k,v_k),
\]

\[
\alpha_k=u_k+q_0g_k,\qquad
y_k=v_k-\frac S{ik}\{R(u_k,v_k)-g_kr_0\}.
\tag{A19}
\]

其矩阵 ℳ(k) 满足 ||ℳ(k)−I||≤1/2，可精确取 (u_k,v_k)=ℳ(k)⁻¹(α_k,y_k)；零频 source 必为零。这是全 M 原 source→gauge coefficients 的 exact infinitesimal inverse，不经旧 Padé/flag 逆。

非线性 Ψ 确实是 H^s→H^s 实解析：q,V∈H^s；G,G⁻¹∈H^{s+1}；r∈H^{s−1}；b=G⁻¹r∈H^{s−1}；D₀⁻¹P₀ 增一阶。乘法 H^{s+1}×H^{s−1}→H^{s−1} 对 s≥1 连续。现在结合 (A18) 使用真实 Banach IFT，给同阶 Ψ⁻¹。此论证适用原独立 q,d source，没有把 constrained V 或 r 当额外独立函数。

## 6. 有限零模与 holonomy 图约束

把 ambient triples 改写成 core ξ=(α,y) 与 finite data

\[
A_* =\langle a\rangle-q_0,\quad
B_* =\langle b\rangle-r_0,\quad H_*=H-V_0.
\]

这是 H^s(a)×H^{s−1}(b)×Mat_m(H) 到 (H^s₀)^{2m}×ℝ^{2m+m²} 的有界线性坐标变化；逆为 a=q₀+α+A_*、b=r₀−Dy/S+B_*、H=V₀+H_*。定义 Ψ⁻¹ξ=(u(ξ),v(ξ))，并从真实 (A1) 计算 a,b,H。原物理像准确由

\[
A_* =\mathcal A(\xi),\quad
B_* =\mathcal B(\xi),\quad
H_* =\mathcal H(\xi)
\tag{A20}
\]

给出；三函数实解析且值与一阶导数在 ξ=0 均为零。因而余维准确为 2m+m²。约束的方程独立性来自 finite variables 的单位导数，不要求图函数彼此独立。

一个可核验的非线性 holonomy 约束为 trace identity。原 split 的 detT 为常数，所以 trV=Σ_j bᵖʰʸˢ_j；(A1) 取 trace 与周期积分给 trH=⟨trV⟩。由 Δ=e、原闭合 bᵖʰʸˢ_m=−Σ_{j<m}d_je_j/S，以及 vᵀAv=0，精确有

\[
\sum_jb_j^{\rm phys}=-\frac1\delta u v,
\qquad
\boxed{\operatorname{tr}H=-\frac1\delta\langle u v\rangle.}
\tag{A21}
\]

这里 u v=Σu_jv_j。故内部 holonomy 不是原 Casimir，也不是可任意附加的 independent constant。主稿的 τ=(1/M)∫Σbᵖʰʸˢ 精确等于 L trH/M。

## 7. Framed gauge 的准确过渡

令 F=G(0)。真实 based gauge 及其 constant connection 为

\[
G^{\rm fr}=GF^{-1},\quad H^{\rm fr}=FHF^{-1},
\quad a^{\rm fr}=aF^{-1},\quad b^{\rm fr}=Fb.
\tag{A22}
\]

于是 G^fr(0)=G^fr(L)=I，H^fr=(1/L)logY_V(L) 对应于背景 H₀=V₀ 的同一局部分支。mean-normalized 与 framed gauges 均保留完整 monodromy 信息。

一阶上 F=I+g(0)，故

\[
g^{\rm fr}=g-g(0),\quad
h^{\rm fr}=h+[g(0),V_0],
\]

\[
\delta a^{\rm fr}=u+q_0g-q_0g(0),\quad
\delta b^{\rm fr}=R-v'/S-gr_0+g(0)r_0.
\tag{A23}
\]

因此 framed finite mean/holonomy 图通常已有非零一阶项，不能照搬 mean-normalized 的 h=0 或 zero-mean output。其 zero-mean core 则满足精确变换 (α,y)→(αF⁻¹,Fy)，在背景的导数与 (A16) 完全相同，因而也有同阶局部 IFT。上述有限图仍需按 (A22) 转换后保留。

## 8. 本次有限核验及判断

进行了一次新的 inline SymPy 核验，没有保存额外 script，没有运行旧 48/332/M3 tensor 等检查。成功运行用时 0.3639 秒：M=2,…,7 的精确 characteristic polynomial (A6) 全匹配；M=3,4 对原 inverse reconstruction 直接微分，(A12)、(A13) 的 algebraic part 均逐项相等；(A21) 的 pointwise trace identity 均符号为零。此前 inline 脚本的初次启动因 SymPy Boolean 转 Python int 的写法报错，在任何核验产生之前修正；上述输出是修正后的唯一成功核验。

审查通过的新增结论是：小非零均匀背景、固定原分量均值叶上，全 M 周期 constant-connection 规范有真实解析解；其完整物理像有有限图约束和同阶 H^s 状态逆。独立手算全 M 证明为 (A5)、(A7)–(A8)、(A12)–(A18)；有限检查只辅助核验公式。这里没有完成从谱数据恢复这些 coefficient functions，也没有证明物理图受某个 ambient vector-AKNS inverse-spectral theorem 或其全套 action-angle coordinates 适配。

## 9. 增强：所有无 alias 均匀背景的 balanced 低阶状态逆

本节独核进一步增强，未运行任何新增或旧 machine checks。以下使用的旧 finite-Lax-coefficient 状态左逆来自已审 `spectral_local_inverse_audit.md` §§1–5；其 finite-jet、Padé、标记 Jordan flag、ODE 与非零 Wronskian 构造是既有依赖，不重复计为新增结论。

仍取 δ∈ℝ\{0}，不再要求 (A3)。假设准确的无 alias 条件

\[
\zeta_\ell-\zeta_j\notin i k_0\mathbb Z\setminus\{0\}
\quad(1\le\ell,j\le m).
\tag{B1}
\]

由 (A5)，这是 exp(LV₀) 的各特征值彼此不同的条件；M=2 时 m=1，条件自动成立。对于固定 M,L，排除的 δ 值是有限对差所生成的离散 alias 值。该条件只作用于指定 H₀=V₀、G₀=I 的局部规范，不是原实际 Floquet 对合定理的限制。

采用 balanced 源与 core

\[
X_s=(H^s_0)^m_q\times(H^{s+1}_0)^m_d,
\qquad
\Pi(q,d)=\bigl(P_0(a-q_0),P_0(b-r_0)\bigr)
\in(H^s_0)^{2m},\quad s\ge0.
\tag{B2}
\]

在 s=0，q∈L²、d∈H¹。原 bᵖʰʸˢ_j 的公式含 q 乘以 d 的 H¹ 系数，原 V 亦如此；原 r 含 d′∈L² 及 q 乘以 d² 的 H¹ 系数。因此 q,r,V∈L²，全部依赖为 X₀→L² 的解析多项式。这里没有使用 L²×L²→L² 的错误估计。

Gauge 方程取 V∈L²、G−I∈H¹₀、H∈Mat_m，乘法 L²×H¹→L² 连续，故 Banach 方程仍复解析。由 (B1)，每个非零 k 的 ik−adV₀ 可逆。高 |k| 时 resolvent 是 (ik)⁻¹I+O(|k|⁻²)，其余仅有限个 k；所以

\[
(D-\operatorname{ad}V_0):H^1_0\longrightarrow L^2_0
\quad\hbox{是有界同构}.
\tag{B3}
\]

把常矩阵 h 加回后，(A7) 成为 H¹₀×Mat_m→L² 的有界同构。真实解析 gauge IFT、G 的 pointwise invertibility 及 (A9)–(A10) 遂在低阶 X₀ 域成立。a=qG 与 b=G⁻¹r 都是 L²，Π 是 X₀→(L²₀)^{2m} 的解析映射；其导数仍由 (A12)–(A15) 给出。

### 9.1 每个非零频率的 kernel 严格为零

固定一个非零 k，设 smooth 单 Fourier mode source (u_k,v_k)e^{ikx} 落在 DΠ₀ 的 kernel。常系数 (A12)–(A15) 不混频；并且固定原分量均值给 δH=0、⟨δa⟩=⟨δb⟩=0。因此 projected kernel 实际满足完整

\[
\delta a=0,\qquad \delta b=0,\qquad \delta H=0.
\tag{B4}
\]

原 gauge 的精确 scalar identity 在光滑场的 formal PDO 意义下为

\[
\mathscr L=D-a(DI_m-H)^{-1}b.
\tag{B5}
\]

式 (B4) 给 δ𝓛=0，故其前 2m 个完整 ℓ coefficients 的微分为零。既有 finite-coefficient 状态恢复构造在该 fixed-mean actual source 上为解析左逆，因而

\[
D\mathcal R_{\rm coef}\circ DF=I,\qquad DF(u,v)=0\Longrightarrow(u,v)=0.
\tag{B6}
\]

此处旧逆只在 smooth 单 Fourier 方向使用，不假定低 L² 数据上可定义无限 charge 或 formal coefficient arrays。其可微左逆来自 finite jets、非零矩阵 minors、ODE 与 Wronskian 的解析表达；在 Jordan 实际像层，固定 cyclic 向量的 N^{M−i}v 基可在附近继续作解析表达，沿 actual source 仍准确恢复原场。故这里没有把单纯的连续或集合论单射错误升级成微分单射。

由 (B6)，每个非零 k 的 2m×2m Fourier symbol 都单射，也就可逆。对任意低阶 kernel 元逐 Fourier 分解，每一系数遂为零。这个步骤独立于任何小 δ Neumann 估计。

### 9.2 高频下三角主部与有界 onto 逆

令

\[
w_k=-ikv_k/S,\qquad
R_q=\frac1M\left(I_m-\frac1M11^T\right).
\tag{B7}
\]

在零均值空间，(u,v)↦(u,−Dv/S) 是 X_s 到 (H^s₀)^{2m} 的有界同构，常数可依赖 S≠0、L。由 (A12)–(A15)，g_k=(ik−adV₀)⁻¹W(u_k,v_k)，而 v_k=−S w_k/(ik)。于是

\[
\binom{\delta a_k}{\delta b_k}
=\left\{
\begin{pmatrix}I_m&0\\R_q&I_m\end{pmatrix}
+O(|k|^{-1})\right\}\binom{u_k}{w_k}
\quad(|k|\to\infty).
\tag{B8}
\]

所有常数只依赖固定 M,δ,L；余项在有限矩阵 operator norm 中一致。上右 block 实际为 O(|k|⁻²)，但不需要这一加强。**主部是下三角矩阵，不能写作 I+O(|k|⁻¹)**：r 中的 R_q u 是 order-zero 项，未因 gauge 消失。

该主部的逆为 [[I,0],[−R_q,I]]。高频由 Neumann 论证得到一致有界 symbol inverse；低频由 §9.1 的可逆性和有限个 k 给有限最大界。因此 DΠ₀ 是

\[
D\Pi_0:X_s\overset{\sim}{\longrightarrow}(H^s_0)^{2m}
\tag{B9}
\]

的有界线性同构，每个 s≥0 都成立，inverse bound 在相同 Fourier 权重下不依赖 s。现在真实 Banach IFT 在 s=0 给开域 O₀⊂X₀、V₀^core⊂(L²₀)^{2m} 及唯一双解析 Π⁻¹。δ 无需小，但 inverse radius 和常数可以随背景及其 alias distance 改变。

完整物理像在 L²(a)×L²(b)×Mat_m(H) 上仍是准确余维 2m+m² 的有限解析图，图函数为 mean a、mean b、H 随 (B2) core 的函数。其背景一阶导数为零，原因仍是 (A15)。此结论将“同阶状态逆”提升到一个实际低阶 balanced 源域，没有声称 full spectral inverse。

## 10. 同一低阶域的所有整数 Sobolev 阶 bootstrap

固定 §9 给出的一份低阶域，不为各高阶重新缩小 core 的低阶半径。给定 core ∈V₀^core∩(H^N₀)^{2m}，N 为任意非负整数，先用同一低阶 Π⁻¹ 恢复 q∈L²、d_first∈H¹、G∈H¹、H 为常矩阵。有限图函数补回的均值也是空间常数，所以完整 a,b∈H^N。

令 C 为原 χ zero-order 矩阵、E 选 first m。精确的三条恢复关系是

\[
q=aG^{-1},\qquad
G'=VG-GH,\qquad
d_{m first}'=ECd-SGb.
\tag{B10}
\]

第三式由 r=K(Cd−d′)/S 得到：原 closure 保证 1ᵀ(Cd−d′)=0，故 K 在该列上等于 E。这里 d 表示完整 M 列，末项仍由 S−Σfirstd 决定；(B10) 不引入额外微分未知数。V,C 都用原 q,d pointwise algebra 重构，不能替成 unconstrained matrix coefficients。

若 N≥1，a,b,G,d 先都在 H¹，第一式给 q∈H¹，V,C∈H¹。后两式因此给 G,d∈H²。如此逐阶递推：已知 G,d∈H^j，且 a,b∈H^N，1≤j≤N，则 q,V,C∈H^j，进而 G,d∈H^{j+1}。最后

\[
q\in H^N,\qquad d_{m first},G\in H^{N+1}.
\tag{B11}
\]

对較小低阶 inverse 域中的有界 H^N core 集，每一步高阶 norm 由低阶 norm、有限图常数和 a,b 的 H^N norm 局部控制。低阶 inverse 已复解析，各 Fourier coordinate 全纯；这些高阶局部有界估计使同一 inverse 取值于 X_N 并为 X_N-valued 全纯（可先用 finite-Fourier functionals，再以 Hilbert norm 有界作弱到强全纯提升）。Forward map 在高阶同样解析，且其规范解由低阶唯一性识别。因此

\[
\Pi:O_0\cap X_N
\longleftrightarrow
V_0^{\rm core}\cap(H^N_0)^{2m}
\tag{B12}
\]

是同一低阶开域上的双解析状态图。没有把所有原 C_n 都定义在 X₀，也没有解决原 DLW 时间方程的低正则 Cauchy 问题。

## 11. 任意外给常数 B 的准确 centered 过渡

设 bᵖʰʸˢ_j=B+bᶜ_j，原 ν=B−S。直接代入原 C 得 C_B=C_c+B(I_M−P)。因为 (I−P)d=0、1ᵀ(I−P)Z=0、K(I−P)Z=I_m，split 系数准确满足

\[
q_B=q_c,\qquad r_B=r_c,\qquad V_B=V_c+BI_m.
\tag{B13}
\]

所以同一个 G 及 a,b 工作，H_B=H_c+BI_m。Nonalias condition 只含 H 的差谱，完全不受 B 影响。原 split 的 scalar fast diagonal 是 λ_original，扣去 BI_{M} 后 centered 参数为 λ_original−B；不能同时移除 V_B 的 B 却保留原 λ。

式 (A21) 在任意固定 B 下成为

\[
\boxed{\operatorname{tr}H_B=mB-\frac1\delta\langle uv\rangle.}
\tag{B14}
\]

这里 trV_B=Σ_jbᵖʰʸˢ_j−B，故其背景是 mB；若直接把原 Σbᵖʰʸˢ 的 MB 写成内部 trace，会多计一个 B。

## 12. 常 GL_m gauge 的严格局部 section 与 rigidity

考虑 constant Q∈GL_m 的 coefficient action

\[
(a,b,H)\longmapsto(aQ,Q^{-1}b,Q^{-1}HQ).
\tag{B15}
\]

Uniform scalar operator 的符号可直接从原 uniform transfer 写为

\[
\mathscr L_0(z)=S\frac{(z+\delta)^M+(z-\delta)^M}
{(z+\delta)^M-(z-\delta)^M}.
\tag{B16}
\]

取 V₀ 的 right/left eigenvectors v_ℓ、ℓ_ℓ，归一化 ℓ_ℓv_ℓ=1。由 (B5) 的 uniform rational representation 及 (A5)，每个 pole 的 residue 满足

\[
q_0v_\ell\,\ell_\ell r_0
=-\operatorname{Res}_{z=\zeta_\ell}\mathscr L_0(z)
=\zeta_\ell^2-\delta^2
=-\delta^2\csc^2(\pi\ell/M)\ne0.
\tag{B17}
\]

验证 residue：分母导数在 pole 上是 −2Mδ(z+δ)^M/(z²−δ²)，分子为 2S(z+δ)^M，故 Res𝓛₀=δ²−ζ²。于是每个 q₀v_ℓ、ℓ_ℓr₀ 都非零。

若 [H₀,X]=0 且 q₀X=0，V₀ 的 simple spectrum 使 X 在该 eigenbasis 对角。每个对角元乘以非零 q₀v_ℓ 都为零，故 X=0。这里 H₀=V₀ 或 V₀+BI，二者 centralizer 相同；δ≠0 即足够，不需 small δ。

令 C_img 是 §9 物理 finite graph 的约束函数，按 coordinates 排列为 mean a、mean b、H 减去其 core graph 值。背景 graph 导数为零，所以 (B15) 对 Q=I+εX 的 finite-constraint 导数准确为

\[
T(X)=\bigl(q_0X,-Xr_0,[H_0,X]\bigr).
\tag{B18}
\]

上述 centralizer 论证给 T 单射。选择其一个非零 m² 阶 minor，也即有限 constraint space 上的线性投影 P 使 PT:Mat_m→ℂ^{m²} 可逆。对近旁物理 triple z，方程

\[
P C_{\rm img}(z\cdot Q)=0
\tag{B19}
\]

在 Q=I 的导数可逆；解析 finite-dimensional IFT 给唯一近旁 Q，而 Q=I 对每个物理 z 都已经是解。因此若 z 与 z·Q 同属足够小物理像且 Q 近 I，必有 Q=I。单纯 dimension counting 不足，此结论依靠 (B17) 和 (B18) 的实际 minor。

还可去掉额外的“Q 近 I”前提，只要求两个 triples 均充分近背景。定义 observability matrix

\[
\mathcal O(a,H)=
\begin{pmatrix}\langle a\rangle\\\langle a\rangle H\\\vdots\\\langle a\rangle H^{m-1}\end{pmatrix}.
\tag{B20}
\]

背景的 eigenbasis 中，该矩阵为 Vandermonde(ζ_ℓ) 乘以非零 diagonal(q₀v_ℓ)，所以可逆。附近仍可逆，且 (B15) 给 O(z·Q)=O(z)Q。因此连接两个近背景 triples 的任意 constant Q 必等于 O(z)⁻¹O(z·Q)，从而自动近 I，再由 (B19) 得 Q=I。原物理像在该局部系数域中是 constant GL_m orbit 的真实唯一 section。

本节 rigidity 只针对完整 (a,b,H) 的常 internal gauge。它不排除随 x、λ 的周期 spectral conjugacy，不证明 action fiber 维数，也未把全部 holonomy graph constraints 改写成纯 spectral invariants。增强后的新增成果仍是 all-M coefficient-state chart 与其精确有限约束。

## 13. 对已保存增强主稿式 (1)–(26) 的逐项结论

另已完整读取 `all_m_physical_holonomy_state_inverse_20261011.md` 的实际保存稿，而非只审查通信中的提纲。其 (1)–(17)、(20)–(26) 与本审查 (A4)、(A12)–(A15)、(B1)–(B20) 一致；在 NR 背景上的 balanced inverse、所有有限图约束、full framed transition 和任意外给 B 的 centered shift 均通过。

主稿 (18)–(19) 的直接 small-δ 预算也可保留，其 threshold 与本稿旧 (A3) 采用的 norm/估计不同。采用主稿 normalized weights 时，v 的 H^s norm≤其 H^{s+1} norm，D₀⁻¹:H^s₀→H^{s+1}₀ 的 norm≤√2/k₀。K₀K₀ᵀ=I_m−11ᵀ/M 给 ||K₀||≤1，||Z||=√M；δC=diag(t)+diag(Zv)s，故

\[
\|\delta C\|_F\le\|u\|+2M\|v\|,
\qquad
\delta K\,C_0Z=-v q_0/S.
\]

这给 W≤2(M+1)√M||source||。由 (A13) 与 t_first=(I−11ᵀ/M)(u+Av)，可取 Z₁≤3√M||source||。q₀≤2M√M|δ|、r₀≤√M|δ| 是保守正确上界。将 principal inverse 左合 DΠ 后，线性 correction 上界为

\[
\{8M(M+1)+3\sqrt2 M^{3/2}\}\varepsilon
\le14M^3\varepsilon,
\]

二次 correction 为 4√2 M²(M+1)ε²≤6√2 M³ε²<9M³ε²。这验证主稿 (19)；|δ|≤k₀/(128M³) 时确实 <1/4，且自动满足 gauge 的 Neumann NR bound。该小背景证明与 §9 的全部 NR 背景证明是两条准确分开的路线。

主稿 §7 的分数 Sobolev 阶也成立：令 n=floor(s)，先用 §10 到整数 n。得到 G,d∈H^{n+1}；一维 H^{n+1} 是 H^s 的有界乘法子，故 q=aG⁻¹∈H^s，V,C∈H^s，(B10) 再给 G,d∈H^{s+1}。因此同一低域的 inverse 保持每个实数 s≥0 的 balanced 级，未引入新的低域收缩。

审查未发现该增强主稿的致命缺口。需要持续保留的范围是：原分量均值给定、δ≠0 且内部 holonomy NR、完整 (a,b,H) 及真实 frame 仍保留、有限 coefficient derivative 单射作为既有依赖。新增 state chart 与有限 gauge rigidity 不应扩写为 vector inverse-spectral 或 all-M Liouville 完整性结论。
