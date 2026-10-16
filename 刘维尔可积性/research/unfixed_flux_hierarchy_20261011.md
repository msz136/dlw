# 不固定平均通量的全周期守恒层级

2026-10-11。独立接续推导；有限格点周期 M≥2、连续空间周期 L、h>0，真实光滑实场。覆盖 c=Πw≠0 的整个正则分支，c 是原方程强制的时间常数，但不预先指定其数值；平均通量 Γ(t)=Π(Uw) 不设为时间常数。本结果将既有固定通量层级扩展到原方程允许的任意时间通量；尚不是完整 Liouville 定理。

## 原方程与唯一自由时间模

令 P₀=I−Π、β=h²/32、R=(δ₋|im P₀)⁻¹M₋P₀，R* =−R。周期原方程为

$$
\delta_-[U_t+D(U^2/2+\beta w^2)]+D^2(\delta_-U+M_-w)=0,
\qquad w_t=-D(Uw)+D^2w.
$$

对第一式取格点平均，D²Πw=0；对第二式再作空间平均，得到 c_t=0 与 DΠ(Uw)=0。令 p=P₀U、s=w−c、z=Π(ps)，则

$$
U=p+b,\quad w=c+s,\quad b=\frac{\Gamma(t)-z}{c}.
\tag{1}
$$

没有 Γ_t=0 的结论。投影方程完全等价于原方程：投影第一式恢复非平均格点分量，平均第一式是 D²c=0；第二式的平均是 DΓ=0。给定 Γ(t) 时，(1) 不需要对 p,s 添加函数形状假设。

## 精确 Hamilton 分解与实际解之间的对应

配对取 hΣⱼ∫，固定各分量空间平均作为 Casimir。用 J=−offdiag(P₀D) 和平移动量

$$
P=hM\int_0^L z\,dx,\qquad X_P=-D(p,s).
$$

将 Hfull−hM∫Γb 代入 (1)，去掉空间全导数及只依赖 c 的常数，得到

$$
K_\Gamma=hM\int_0^L\left[
\frac12\Pi((c+s)p^2)-\frac{(\Gamma-z)^2}{2c}
 +\beta c\Pi s^2+\frac\beta3\Pi s^3
 +\Pi(sp_x)+\frac12\Pi(sRs_x)\right]dx.
\tag{2}
$$

特别地，准确恒等式为

$$
K_\Gamma=K_0+\frac\Gamma c P-\frac{hML}{2c}\Gamma^2,
\qquad
z_{\rm field,t}=X_{K_0}+\frac{\Gamma(t)}c X_P.
\tag{3}
$$

这里 zfield=(p,s)，区别于标量 z=Π(ps)。平移不变性给 {K₀,P}=0，所以每条真实光滑原轨道上 K₀、P 均守恒；KΓ 本身在 Γ 可变时一般不是守恒量。

更强的实际轨道对应无需 Cauchy 适定性假设。若 (p₀,s₀)(x,t) 是 Γ=0 的任意真实解，取任意光滑 Γ(t) 和 a′=Γ/c，则

$$
(p,s)(x,t)=(p_0,s_0)(x-a(t),t),
\quad U(x,t)=U_0(x-a(t),t)+a'(t),
\quad w(x,t)=w_0(x-a(t),t)
\tag{4}
$$

是该 Γ(t) 的原方程解。反向平移给逆映射。(4) 只转换已经存在的实际解；它不宣称任意 Sobolev 初值存在。原物理均值的缺少演化方程在此明确体现为任意 a(t)；需指定规范或在这种时间依赖平移下取轨道等价类，才能讨论唯一的自治解流。

## 正确的中心化谱迹

设 G=hMc/4，f(t)=Γ(t)/(2c)，

$$
T_j=(D-U_j/2+hw_j/8)^{-1}(D-U_j/2-hw_j/8),
\quad \mathcal M_\Gamma=T_{M-1}\cdots T_0,
\quad \mathcal L_\Gamma=-G(\mathcal M_\Gamma-I)^{-1}+f-G/2.
$$

在同一 (p,s,c) 状态上，用 U⁰=p−z/c 定义 M₀、L₀。UΓ=U⁰+2f；因 f 为空间常数，k=e^{fx} 给形式算子精确恒等式

$$
\mathcal M_\Gamma=k\mathcal M_0k^{-1},
\qquad \mathcal L_\Gamma-f=k\mathcal L_0k^{-1}.
\tag{5}
$$

k 可准周期；两侧算子系数仍周期。对任意标量 PDO A，res(kAk⁻¹)=res A 点态成立：微分部分仍为微分，负阶只有原 D⁻¹ 项能贡献 D⁻¹。故不使用不合法的非周期 x 迹循环性。

严格地说，(5) 是周期形式 PDO 的自同构 D↦D−f，不是同一个周期函数定义域上已证明的有界相似。实际空间 Floquet 波函数满足 ψΓ=e^{fx}ψ₀，因而 λΓ=λ₀+f、ρΓ=e^{fL}ρ₀。接续完整 Floquet 逆谱时须同时中心化 λ 和空间 Floquet 倍子 e⁻ᶠᴸρΓ；形式留数守恒不自动给固定周期边界下的实际等谱。

若 Cᵞₙ=(1/n)Tr LΓⁿ，则真正的通量无关泛函是

$$
\widehat C_n=\frac1n\operatorname{Tr}(\mathcal L_\Gamma-f)^n
=\sum_{r=1}^n\binom{n-1}{r-1}(-f)^{n-r}C_r^\Gamma
=C_n^0.
\tag{6}
$$

Tr I=0；有限二项式计算中的系数是 (r/n)binom(n,r)=binom(n−1,r−1)。每一固定 n 都只涉及有限 jets，式 (6) 无需整个 PDO 级数收敛。Ĉₙ 可从即时原物理场计算，因为 c=Πw、Γ=Π(Uw)，并未借助外部预设 Γ 数值。

旧固定 Γ=0 的因子 Adler 证明给 Ĉₙ 彼此对合，并与 P、K₀ 对合。式 (3) 直接推出任意 Γ(t) 的实际轨道守恒。三角变换对每个固定瞬时 Γ 的对角系数全为 1，故原已核验的任意有限块独立性保留在每个 c≠0 的固定 Casimir 叶；此处仍依赖旧全阶对合、独立性的原证明，不能把新的有限符号检查当成其替代。

反而原始未中心化谱迹满足

$$
\frac d{dt} C_1^\Gamma=0,\qquad
\frac d{dt}C_n^\Gamma=(n-1)f'(t)C_{n-1}^\Gamma\quad(n\ge2).
\tag{7}
$$

证明只须反演 (6) 为 Cᵞₙ=Σ binom(n−1,r−1)fⁿ⁻ʳĈᵣ，再微分。不可以把所有 Cᵞₙ 直接标为任意 Γ(t) 的守恒量。

## 进一步的非自治 Lax 身份

对实际解，L₀,t=[−(L₀²)₊−2fD,L₀]。微分 (5)，k_tk⁻¹=f′x；用 kDk⁻¹=D−f 和 LΓ,+=D 得

$$
\mathcal L_{\Gamma,t}
=[-(\mathcal L_\Gamma^2)_+,\mathcal L_\Gamma]
 +f'([x,\mathcal L_\Gamma]+I).
\tag{8}
$$

尽管 x 非周期，最后一项实际是周期负阶算子：若 LΓ=D+ΣℓᵣD⁻ʳ，则 [x,LΓ]+I=ΣrℓᵣD⁻ʳ⁻¹。式 (8) 明确记录原 Γdot 自由度造成的谱漂移；守恒仍由 (6) 推出，避免将含 x 的交换子错误当作周期迹零项。

## 覆盖范围与后续精确任务

该层级覆盖全 M、任意一般周期涨落函数、任意允许的 c≠0 和任意 Γ(t)，不依赖 M=2、m=Ax 或有限 Fourier/孤子族。每个具体自治辛叶仍固定由原方程守恒的 c 与组件空间均值；跨叶参数没有被混入独立积分计数。

原周期解的规范商可统一到 Γ=0；因此完整 Liouville 问题的正则周期分支可在 K₀、P、Ĉ₃、Ĉ₅,… 上推进，而不需要把 Γ 常数误当成原方程定理。仍须在同一真实弱辛域证明辅助实际流及谱极大各向同性。c=0 需要独立约束约化，非周期 m=A(t)x+B(t) 也不由这里覆盖。

## 依赖与核验

原方程、R 反对称及原 Hamilton 结构：[periodic_reduction.md](../../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md)。原全阶因子证明：[MONODROMY_POISSON_PROOF.md](../../Workspaces/dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md)，恢复独立审计见 [periodic_structure_audit.md](periodic_structure_audit.md) §3。

新精确检查脚本与记录：`../../Workspaces/dlw_recovery_20261011/verify_unfixed_flux.py`、`unfixed_flux_checks.json`。检查 Hamilton 密度的全 M 平均恒等式、n≤9 的二项式互逆/通量漂移、一般形式系数的低阶准周期共轭 residue；有限检查辅助上面的全 M / 全阶代数证明。

第二位独立复核见 [unfixed_flux_independent_audit.md](../../Workspaces/dlw_recovery_20261011/unfixed_flux_independent_audit.md)，确认式 (1)–(8)，并直接用 [x,A] 的 residue 点态为零重证 (7)。两位复核同时保留上述实际 Floquet 扭转限制。
