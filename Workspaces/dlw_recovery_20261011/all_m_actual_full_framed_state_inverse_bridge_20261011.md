# 全 M actual full framed 谱状态逆的接合：低阶 Banach 数据、端点与 B

2026-10-11。spectral_completeness 独立读回并核验以下实际证明。未运行新检查，未重跑既有证书。本稿证明一般 M 原物理状态的局部恢复，完整 matrix frame 是输入数据的一部分。

依赖：[physical coefficient state 图](all_m_physical_holonomy_state_inverse_20261011.md) §§1–9；[actual endpoint 稿](all_m_actual_framed_endpoint_recovery_20261011.md) (1)–(16) 及 [端点独审](all_m_full_framed_endpoint_holonomy_independent_audit_20261011.md)；[actual Fourier-kernel 稿](general_m_framed_monodromy_fourier_kernel_20261011.md) §§1–6、10 及 [raw extraction 独审](general_m_raw_monodromy_state_extraction_independent_20261011.md)。

## 1. 定理的严格域

固定 M≥2、m=M−1、周期 L>0、S=Mδ≠0、原物理 component means。取对应 uniform 叶的
\[
X_0=(L^2_0)^m_q\times(H^1_0)^m_d.
\tag{1}
\]
uniform free fields 为 q_j^*=−2δ(m−j)、d_j^*=δ。内部 V₀ 的 eigenvalues 是 p_j=−iδcot(πj/M)。要求 p_j−p_l 不属于 (2πi/L)(Z\{0})，随后取足够小的 X₀ 邻域，使内部 nonalias 条件保持。

另外要求 uniform constant-slow triple (q_*,r_*,V₀) 位于 §3 的 ambient spectral IFT 域。固定 M,L 时，所有足够小但非零 |δ| 都满足：q_*,r_*,V₀ 是 δ 的固定线性函数。这个新 small-vector-potential 条件不自动等同于旧 mixed strong 图的 δ 阈值；没有合并未估计的半径。这里不允许 δ=0，尽管辅助 ambient 图在 vector vacuum 上构造。

在此域内，原完整、固定 χ frame 的 determinant-normalized monodromy 函数 Nχ(λ_original) **局部唯一决定原 q,d 状态**。经该函数自身恢复端点而校准后，全部整数样点的两个 offdiag blocks 与零参数 slow block 是明确的 Banach 谱状态数据，有真实解析 L²/ℓ² inverse。物理数据在 ambient inverse 的像内满足原有限 graph 约束。

只给 characteristic coefficients、eigenvalues 或 traces 时，本定理没有提供所需端点或 offdiag 数据。

## 2. 实际 Fourier 核的独立复核

对实际 block connection
\[
A_\lambda=\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\quad a,b\in L^2,\quad H\in\operatorname{Mat}_m,
\tag{2}
\]
odd Dyson path 的 ordered times 0<t₁<⋯<t₂ᵣ₊₁<L 给相位 τ=t₁−t₂+⋯+t₂ᵣ₊₁∈[0,L]。upper scalar phase为 e^{λ(L−τ)}，lower为 e^{λτ}。gap 变量的 even 总和是 τ，odd 总和是 L−τ，Lebesgue 换元 Jacobian准确为 1。固定 τ 的 fiber 体积为
\[
v_r(\tau)=\frac{\tau^r(L-\tau)^r}{(r!)^2}.
\tag{3}
\]
任意 distinct alternating 输入 f₁,…,f₂ᵣ₊₁ 的 slow exponential 总 norm≤e^{L||H||}。fiber Cauchy–Schwarz、(3) 与整个 ordered simplex上的 product L² 积分界给
\[
\|K_r\|_{L^2_\tau}
\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\prod_{j=1}^{2r+1}\|f_j\|_2.
\tag{4}
\]
先构造同一个真实 L² kernel，再用 Parseval 控制全部样点；没有直接相加每谱点的 absolute bound。

设 A=||a||₂、B=||b||₂，upper/lower kernel series 的 L² norms分别≤e^{L||H||}A e^{LAB/2}、e^{L||H||}B e^{LAB/2}。bounded potential balls上一致整解析。每个采样值与实际 Volterra/Dyson monodromy相同。重复输入的更强 factorial bound不是本接合所必需。

## 3. normalized 实际 ambient Banach inverse

令 T_A(λ) 是 (2) 的实际 monodromy，M=m+1。准确 normalization为
\[
N_A(\lambda)=e^{-\lambda L/M-L\operatorname{tr}H/M}T_A(\lambda).
\tag{5}
\]
对 λ_n=2πin/L，定义
\[
\mathscr D(a,b,H)=
\left(
L^{-1/2}\big(e^{\lambda_nL/M}(N_A(\lambda_n))_{0s},
e^{\lambda_nL/M}(N_A(\lambda_n))_{s0}\big)_{n\in\mathbb Z},
(N_A(0))_{ss}\right).
\tag{6}
\]
两组用同一已知 positive phase。lower Fourier sign与upper相反，指标反射仍unitary。包括 n=0。finite slow block一般不等于 e^{LH}，不能替换成该公式。

(4) 给 (6) 到 ℓ²_{2m}×Mat_m 的真实整解析映射。在 a=b=H=0，中心数据是 (0,I_m)，其 derivative为
\[
D\mathscr D_0=\mathcal U\oplus L\mathsf P,
\qquad \mathsf PH=H-\frac{\operatorname{tr}H}{M}I_m,
\tag{7}
\]
𝒰 是两组准确 Fourier isometry。因为 m=M−1，
\[
\mathsf P^{-1}K=K+\operatorname{tr}K\,I_m.
\tag{8}
\]
有限 block derivative的 inverse是 (δC+trδC I_m)/L，保留 H 的 trace。Banach analytic IFT给真空邻域的实际解析双逆。

这个 ambient inverse不要求物理零模 graph的 derivative为零，因此可用于已有 Cauchy frame图。Fourier-kernel稿 §7 的 n≠0 subset theorem不能未经额外预算套在 Cauchy图上。

## 4. 原矩阵自身的端点恢复及物理回拉

已有 coefficient图给 periodic G、完整 H。取 G^f=GG(0)⁻¹、H^f=G(0)HG(0)⁻¹，a^f=qG^f、b^f=(G^f)⁻¹r。G^f(0)=G^f(L)=I，故
\[
N_\chi(\lambda)=T_d(0)N_{A^f}(\lambda)T_d(0)^{-1},
\quad T_d=[d/S,Z],\quad 1^TT_d=(1,0).
\tag{9}
\]
positive real λ 的 periodic lower Riccati解满足 η∞=O(λ⁻¹/²)、η₂=O(λ⁻¹)。actual triangular monodromy 的 fast multiplier为 e^{λL+O(λ⁻¹)}，slow block有界，upper/fast=O(λ⁻¹/²)。由此
\[
\frac{N_{A^f}(\lambda)}{\operatorname{tr}N_{A^f}(\lambda)}\longrightarrow E_{00},
\qquad
\frac{N_\chi(\lambda)}{\operatorname{tr}N_\chi(\lambda)}
\longrightarrow\frac{d(0)1^T}{S}.
\tag{10}
\]
ratio scalar normalization取消。d∈H¹ 有实际 endpoint；任意一列恢复 d(0)/S。因此 T_d(0) 从原 full matrix本身得到，(9) 的常数 conjugation准确给 N_{A^f}，不附加 G(0) metadata。

在 §1 的 small-vector chart内，(6) 逆得 a^f,b^f,H^f。coefficient theorem §9 的
\[
\Pi^f(q,d)=(P_0a^f,P_0b^f):X_0\longrightarrow(L^2_0)^{2m}
\tag{11}
\]
是真实局部解析双逆。应用它得原 q,d，再由准确 closure恢复全部原分量。

因此两近邻物理态若原 entire-λ full normalized framed Nχ相同，则端点、(6) 数据、a^f,b^f,H^f、q,d依次相同。这是原实际物理像上的局部唯一恢复。没有给 original raw entire-function空间指定自然 Banach norm或证明任意附近函数都 onto物理态；真正 open-set IFT是 (6) 的 calibrated ambient Banach定理。

## 5. B 不冻结：固定 reference parameter 的准确恢复

原静态 connection满足
\[
A_{\chi,B}(\lambda_{\rm orig})=B I_M+A_{\chi,0}(\lambda_{\rm orig}-B).
\tag{12}
\]
给定 reference B₀，取固定 λ_orig=B₀+λ，从 raw connection减 B₀I_M。exact split top-left是 λ，q,r不变，slow block准确是
\[
V_{\rm ref}=V_c+(B-B_0)I_m,
\qquad H_{\rm ref}^f=H_c^f+(B-B_0)I_m.
\tag{13}
\]
未知 B没有先行用于中心化。raw monodromy的 e^{B₀L} scalar在 determinant normalization中取消，所以 Nχ(B₀+λ) 正是 (5) 的 reference normalized matrix，直接应用 (10)、(6)。

恢复 q,d后计算该状态的 centered H_c^f，再由
\[
\boxed{\quad B-B_0=
\frac{\operatorname{tr}H_{\rm ref}^f-\operatorname{tr}H_c^f}{m}.\quad}
\tag{14}
\]
恢复局部 spatialconstant B 参数。分母是 m=M−1。centered trace为 −δ⁻¹⟨u·v⟩，reference trace额外含 m(B−B₀)。若数据已经重标为 centered λ，则 B不在该数据中；(14) 使用固定 reference λ_orig标签。静态恢复不添加 B_t=0 或 Γ_t=0，原时间守恒谱仍用正确 centered规范。

## 6. 物理 graph、真实结构与高阶界限

固定 B时，物理 triples在 ambient (a,b,H) 中有准确 2m+m² 个 finite graph约束。放开一个局部 B参数时，a,b图不变，H沿 identity增加 B−B₀，codimension变为 2m+m²−1。identity方向与 fixed-B图 tangent横截，因为 (11) 的 projected derivative是同构。

complex analytic inverse限制到实 form：实 a,b,H给 N_A(\barλ)=overline{N_A(λ)}，因此 (6) 样点有 s_{−n}=overline{s_n}，finite C实值；map与derivative都尊重该 involution。没有 finite Fourier限制。

已有 coefficient inverse使高阶 recovered系数在同一低域提升。raw samples一般有1/n或1/n²端点尾，smooth a,b也不在全部 h^N。因此这里只有 ℓ² 谱坐标，未证明 graded weighted谱双逆。

## 7. 已补与仍缺

已补：一般 M periodic物理图、full matrix端点恢复、无额外 G(0)/τ metadata的实际 normalized ℓ²+finite-block逆，以及 small-potential邻域内原 full framed谱函数的状态唯一性。

仍缺：class fibers与norming方向的完整 nonlinear描述；physical J的 canonical action/norming配对；所有 actual class Hamilton场闭包与共同微分核的全 M equality。framed状态逆给真实数据入口，Liouville完备性仍未完成。
