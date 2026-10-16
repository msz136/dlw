# 全 M 实际谱约束与 Hamilton gauge residue：根复核

2026-10-11。独立手核 [物理谱约束主稿](general_m_physical_gauge_fredholm_and_spectral_constraints_20261011.md) 和 [全谱 Hamilton gauge 主稿](all_m_rational_physical_gauge_hamilton_bridge_20261011.md) §§1–9。所有结论保留两稿指定的非零 uniform fixed-mean、nonalias 局部状态图。未运行机器检查。

## 1. 两个真实谱点的约束与完整物理像

原 normalized connection 在 λ=±S 分别 upper/lowertriangular，diagonal 是 Δi−格点平均Δ±(di−S/M)。uniform mean 叶上的空间积分全零，故 actual N±S unipotent，tr N±S^r=M，r=1,…,m=M−1。物理 trace Hamilton 场在这些固定参数为零，但这不意味着 ambient vector-potential 中的约束微分为零。

独核 ambient 约束的满秩。背景 normalized A±S 是 regular nilpotent J±；其 actual monodromy 为 exp(LJ±)。对于 traceless δJ，
\[
\delta\operatorname{tr}e^{rLJ}
=\sum_{k=1}^{m}\frac{(rL)^{k+1}}{k!}\operatorname{tr}(J^k\delta J).
\]
系数矩阵 r=1,…,m 是对 Vandermonde 矩阵乘非零行列因子，故与全部 characteristic coefficient 首变分等价。每个 background adjoint 为常矩阵，因此只检验输入的空间平均及 δH。

置 Q(z)=det(z−H)、R(z)=a adj(z−H)b、t=tr δH。实际 trace normalization 给
\[
\delta[(z\mp S)Q(z)-R(z)]=-t(z\mp\delta)^m.
\]
相减后 δQ 的最高系数同时为 −t 与 −tm/M，强制 t=0、δQ=δR=0。H 的 simple eigenvalues 及每个非零 realization residue 保证这一 finite kernel 恰为 m² 维 constant GLm tangent，无 stabilizer。故 2m 个实际 class constraints 独立。

mean-normalized physical graph 的 finite derivative 在背景为零，其 infinite mean-zero derivative是已证 Banach 同构；加 constant GLm orbit 与一个 2m 维 finite complement，形成完整 ambient Banach direct sum。解析 IFT 后，vector Hadamard identity 的 transverse 2m×2m 矩阵可逆。因此局部确有
\[
\{\operatorname{tr}N_{\pm S}^r=M\}_{r=1}^{m}
=\text{physical coefficient graph 的 constant-GLm saturation},
\]
并有唯一小 gauge 截面。证明在 L² coefficient domain 上成立，是实际物理像的纯谱有限约束刻画；不是 action-angle、Poisson reduction 或完整 Liouville theorem。

## 2. 周期块方程与 index

直接乘法验证 raw δA=g′−[A,g] 的四块：α′=aγ−βb、δa=(D−λ)β+βH+αa−aZ、δb=(D+λ)γ−Hγ+Zb−bα、δH=(D−adH)Z−bβ+γa。

非零模的 D⁻¹ 与 (D−adH)⁻¹ gain one，constant fast equation 仍须保留平均(aγ−βb)=0。physical graph 的 2m 个均值和 m² 个 H residual 不能省去。主稿的一阶 augmented operator 从 H^{s+1} 两主块到 H^s 零均值块，加完整 finite variables/equations，base kernel 与 cokernel 都有 2m+1+m² 维，故 index 0。其余项是 compact 或 finite rank。cyclic monodromy 时 homogeneous adjoints 的 M 维 kernel 含 identity；此计数没有强行混入 slM trace 条件。通过。

全 normalized class kernel 的 δtrH=0 另由 actual simple fast root 与 C¹ O(λ⁻¹) quasimomentum remainder 得到，不从形式留数推断。

## 3. 实际 r-matrix 到全谱 rational gauge

已证 C±=R±B/2 恒等式与 periodic Wμr 收缩，准确给
\[
g_{\lambda;\mu,r}=-\frac1{16}\operatorname{tr}_2[C^+(I\otimes W_{\mu,r})],
\qquad \delta_{X_{F_{\mu,r}}}L=g'-[L,g].
\]
独核 partial-trace 的 commutator 符号：第一项为 −[L,tr₂ C+W]，第二项为 tr₂ C−W′，从而 g′−[L,g]=−tr₂ BW′/16，与原 Poisson variation 一致。

ρ=−μ/S+(S²−μ²)/(S(λ−μ))，故 residue 为 −(S²−μ²)Wμr⁰/(16S)。λ∞ 常数部分有界。μ=±S 时 upper/lowertriangular W 的 strict 与 diagonal 部分逐项抵消，整个 g=0；一阶 μ derivative 则有 residue ±W±S,r⁰/8，仍 bounded rational。

## 4. Finite rational 核的 Hamilton 生成

λ-independent physical gauge 需先用 detG⁻¹ᐟᴹ 的 normalized moving frame。其 transformed coefficient 是 λ(E00−I/M) 加常项。λ 方程强制 gauge blockdiagonal，top diagonal 的周期性强制 δtrH=0；nonalias 强制 slow K constant。剩下恰是 constant GLm tangent，与 physical graph 的切向零交，故 physical variation 为零。

任一 bounded-at-infinity finite rational periodic gauge 的最高 pole residue 是对应 μ 的 homogeneous adjoint。cyclic actual Nμ 的全部 m trace powers 提供完整 adjoint basis。普通 pole 的 k 阶项由 ∂μ^{k−1}gμr 消去；±S pole 用 ∂μ^k gμr，其最高系数分别 (k−1)!αW 或 k! (±1/8)W。递归后剩 λ-independent 部分，由上述零交排除。

因此这种有限 rational 物理核方向确在有限 parameter-derivative Hamilton span，并属于实际 trace Hamilton 场的 C∞ 闭包。每个有限差商都在同一物理切拓扑收敛；没有推到无限 pole 截断。

## 5. 全局 gauge 存在与未闭合部分

固定 cyclic vector v 的 Krylov P=[v,Nv,…,N^{M−1}v] 与 D=detP 给 global meromorphic G=δP P⁻¹−tr(δP P⁻¹)I/M。实际 characteristic derivatives 恒等零时 companion derivative 为零，所以 δN=[G,N]。g=δY Y⁻¹+YGY⁻¹ 的周期 endpoint 由该等式准确闭合。actual ODE 给 D 与 Dg 的指数增长上界，不能给 D 的全谱下界。

因此尚缺 infinite pole/residue tails、非cyclic通道和 unbounded entire 部分的物理控制。polynomial gauge 的最高 slow coefficient 满足 K′=[H,K]，nonalias 时 K 是 H 的 constant centralizer；simple H 给 m 维可能通道，不能只数 fast quasimomentum 一支。主稿保留这些限制，通过。

这里新增的全 M 连接不能替代 M=2 真实 regular fiber、切空间与实际 Hamilton 轨道的核心任务。它们提供实际约束和 Hamilton 生成的有限有理子类，一般场完整目标仍开放。
