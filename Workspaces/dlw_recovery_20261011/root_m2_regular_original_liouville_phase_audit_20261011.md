# 根复核：M=2 原物理结构上的正则局部 Liouville 相空间

2026-10-11。实际完整读取 [主定理 §§1–9](m2_regular_variable_action_original_symplectic_phase_20261011.md)、[独审](m2_regular_variable_action_phase_independent_audit_20261011.md)、[reciprocal 与原时间主桥](m2_reciprocal_spectral_actions_and_dlw_frequencies_20261011.md) 及 [实结构来源独审](m2_kltz_physical_real_involution_independent_audit_20261011.md)。根独推已分别保存 [reciprocal/无限 Hamilton 求和](root_m2_reciprocal_actions_and_bounded_hamiltonians_audit_20261011.md) 和 [原时间归一化](root_m2_original_frequency_normalization_audit_20261011.md)。没有运行旧检查。

**PASS：主定理是原 M=2 DLW 与原连续弱辛形式在一个明确强拓扑 Banach 函数相空间上的真实局部弱 Liouville 定理。** 它跨越了仅闭包最大性的缺口：该相空间中的共同水平集正则、实际切空间等于共同微分核、切评估无 ghost、水平集最大各向同性，且由整个相空间上的真实 Hamilton 流覆盖。两组完整无限序列同时自由，未固定某个物理场。

## 1. 适用域与实际状态

保留同一低阶 reduced 谱状态逆、标准 Abel/Dirichlet 实对称归一、一次共同谱 contour/log 域，以及额外 BKM 复 action 频率域。后者需负中央背景 I₀*=−L²S²/4 足够小，并非由旧 KLTZ 或 mixed 半径自动推出。

实际原实结构 w₋ₙ=−bar wₙ、z₋ₙ=−bar zₙ 已通过原规范与中央消元；根已核对 unitary 算子变换、Dirichlet sheet 的恒定符号、固定 Abel 周期及背景零 log/root 分支。任意 action-dependent rephasing 不能无条件套用这一线性公式。

从既有真实强态的原时间双向 germ 及精确频率 Ω_H,n=−kₙ²−2iηkₙ+有界项，得到 base 的 Gaussian margin。这个推论只需要真实 ±T 两个解点，未虚构无穷联合时间。非中央 actions 全部非零的 base 来自同一参数球的 Baire 构造。

实际图
\[
w_n=w_n^*e^{a_n/2+q_n-tk_n^2+isk_n},\qquad
z_n=z_n^*e^{a_n/2-q_n+tk_n^2-isk_n}
\]
令 a、q 任取 bounded 反射共轭序列，t、s 为真实小参数；Gaussian margin 保证整箱解析进入每个 hᴺ 与原 C∞ 物理场。声明的 Banach 拓扑比 ambient C∞ 强。

## 2. 真正 regular fiber 与实际切空间

两个图点相等先由 Jₙ=Jₙ*e^{aₙ} 的统一小 log 域确定 a。余下 exponent 的实部除去 t 的二次项；正指标整数周期的二阶差分，结合 uniform small q，除去 s 的线性项和全部剩余周期。微分单射则直接由二次、一次增长与 bounded δq 依次推出。

因此相对 action 映射 log(J/J*) 恰为 a 投影，是 split submersion。其 levels 是普通 Banach 流形 a=a₀；所有 δa=0 方向都有实际参数直线实现，且严格等于全部实际 action 微分的共同核。相域与水平集的切评估均单射。这些结论限定在该声明拓扑，不冒充更大的 inherited S∞ fiber 正则性。

## 3. 原形式，未另设 Poisson 张量

原 Ω=−16∫[(D₀⁻¹Vᵤ)Wᵥ+(D₀⁻¹Vᵥ)Wᵤ] 与 J=−offdiag(D)/16 的 sign/scaling 核对通过；Ω(X_H,V)=dH(V)。它已在 L²ᵤ×H¹ᵥ 连续弱非退化，实际 low inverse 搬运得到连续闭的 Ω̃。

主稿的 cross-operator 非退化证明有效。另有不需 cross inverse 的直接证明：每个 all-Jₙ≠0 点，finite-support δa、δq 给全部 finite-support Cartesian tangents，且严格保持原实结构。它们在原 low tangent 稠密。与全相域正交的向量因而与整个 low tangent 正交，原 Ω̃ 非退化使它为零。

水平集切向由真正内部 Hamilton 场 X_H、X_P、X_{H_d} 精确生成；它们彼此对合，故 level isotropic。与 level 正交的相域向量又被内部各 realified Iₙ 场检测出 δa=0。故 (TY)^⊥Ω=TY，不是只取环境闭包。

## 4. 真实完整局部 Hamilton 轨道

reciprocal Aₙ 的所有非中央 contour 在一个 low ball 内共同成立；P_z=1/ω、P_η=iL/(2ω) 的中心变分严格抵消。原实际 X_Aₙ=L(−wₙeₙ,zₙeₙ)。原 low Ω 的径向配对给 A:E₀→ℓ¹ 解析，任意 bounded d 的 H_d=ΣdₙAₙ 是真实 Hamiltonian，且 X_Hd 为有界 multiplier、实际 flow 是 exponent(∓Ldₙτ)。这一步也可以构造真实 H²×H¹ 积分梯度，并直接用原 J 得到相同 field；未将无穷级数硬穿过无界 D。

原时间在整箱给 ȧ=0、ṫ=1、ṡ=−2η(J)、q̇=r(J)；平移为 ṡ=1；H_d 为 q̇=−Ld。它们均定义在相邻所有 actions 上。相同 a 的两近点可取 τ=Δt、σ=Δs+2ητ、d=−(Δq−rτ)/L，以三个实际 flow 的有限复合精确相连。也可用固定 Hamiltonian τH+σP+H_d 的 time-one 轨道作参数直线插值。

全部 actual Iₙ 对合、任意有限实 action 块独立，joint relative action map 为 submersion；共同水平集是上述 commuting Hamilton algebra 的真正局部轨道。该结论是局部，存在窗要求轨道留在图箱内，不宣称所有参数全时间全局流。

## 5. 留在目标中的限制

这个相空间允许两个场分量的无限函数自由度，保留原 Ω、原 DLW 时间及任意预给 Γ(t) 的平移重构；小非零 S 是指定 Casimir 叶标签，可在可用背景区间内改变，未固定成一个特殊数值。

它仍不是任意普通 C∞ 初态的自然开邻域。整个 variable-action 箱进入旧全层级 S∞ 的证明、旧 inherited fiber 与新正则 level 的同一性、所有高阶 Cⱼ 在该箱内的共同流以及一般 M 的 invariant action/norming 图仍未给出。因此一般物理场上的完整目标保持 OPEN；新定理不以特殊全线 s=Ax 分支或有限维族作替代。
