# 根复核：matched H¹ 谱状态图与全线正谱特殊分支

2026-10-11。两项证明互相独立；本稿不把特殊全线分支接成周期一般场定理。主证明和独审已经实际读取，未运行旧 checks。

## 1. 一般 vector AKNS 的 matched H¹ 逆

已读 [主证明](vector_akns_twisted_h1_state_inverse_recovery_proof_20261011.md) 和 [独审](vector_akns_twisted_h1_state_inverse_independent_audit_20261011.md)。结论在每个固定有限 matrix size、一般复杂 matrix H 上成立：actual odd-Dyson 核经过右、左 matrix twist 后，首项分别是 a(L−τ) 与 b(τ)，非线性高路径的 endpoint 值为零。

我逐项核对 affine duration 的输入导数、r≥2 的 fiber Jacobian 商、r=1 两重积分的两端除法估计。r=1 不能引用 r≥2 的平方 fiber bound；使用一个 H¹→L∞ 因子和其余 L² Cauchy 配对，得到相同 R²Z₁ 预算。矩阵 exponential 保留乘法顺序，不假定 H 可交换或正规。

于是 higher-kernel H¹ 范数有 CR²exp(CR²)Z₁ 的 tame bound。低域迭代收敛、H¹ 迭代一致有界与弱紧性识别唯一低逆，给同一低 L² 半径上的 periodic H¹/h¹ 双解析限制。高逆解析性通过局部高范数界及稠密低测试泛函的复线极限成立。

原 raw 样点仍有真实 1/n endpoint 尾，不能直接宣称 raw h¹。matched 数据确实解决这一层。一般 H 的第一导数跳含 e^{LH}Q_H e^{-LH} 的非交换共轭，Bernoulli B₂ 校正只供应 C² 源的 forward h²；因为 a(0)、b(0) 不是低 L² 连续泛函，当前不证明同低域 H² 逆或全阶 weighted 谱图。

**PASS：实际 framed matched H¹/h¹ state 逆。** 它仍不提供 invariant class/action/norming 的逆或原 Hamilton 完备性。

## 2. 全线 s=m=Ax 候选

已读 [来源规范重录](other_chat_s_ax_positive_spectral_candidate_20261011.md) 和 [完整独审](other_chat_s_ax_positive_spectral_candidate_independent_audit_20261011.md)。原缩放 d=h/8 确实给强制项 4(h²/32)A²x=2(2dA)²x；U₀=0、U₁=−2p、w₀=2Ax、w₁=0 回拉原方程为 p_t=2pp_x−p_xx−2c²x，c=2dA。这里 c 不是周期平均通量。

核积分 Iν(T) 的分部积分身份 Iν''=νIν+TIν' 严格给 φ''=(c²x²+k²)φ；正性与归一化来自积分本身。与 [NIST 12.5.E1](https://dlmf.nist.gov/12.5#E1) 和 [12.2.E2](https://dlmf.nist.gov/12.2#E2) 的 U 函数积分、微分方程吻合；负谱值属于单侧增长解，不是 L² oscillator eigenvalue。

归一 Ψ 的 D Aⁿ 算子顺序和紧 k² 区间多项式稠密性给双密度唯一；对有符号密度使用同一论证给实际场微分单射。密度对数公式消去整体标量后唯一恢复 Q、P、β。H¹ 中的 exponent/log 估计保证 current-density topology；反例 Q_N=(a/N)sin(2πN(k−1)) 证该拓扑的逆并非普通 C∞loc 连续逆。

全实时间 Q_t=7/3−k²、P_t=0 对应 Ψ_coord=e^{7t/3}Ψ_heat；这个整体规范必须保留。Compact k 区间和正密度给双向全局时间。uniform ν Laplace/Gamma 渐近给两端 p=−cx+O(1/|x|)；方差严格正证明动态非静态。

新定义 H¹ canonical strong Ω、完整 cosine H¹ 基和 H*=⟨7/3−k²,P⟩ 的频率公式均核对通过。共同 level V×{P*} 的实际 Hilbert 切空间 L 满足 L^Ω=L；任意 Hilbert coefficient charge 的全局 Q 平移覆盖该水平集。

**PASS：固定此特殊分支、新 current-density Hilbert 拓扑及新强辛结构下的无限维完全可积分系统。** 原 Poisson 继承未证；s 场被冻结，Γ=0 由此分支方程强制，增长渐近也不同于周期或 Schwartz 开域。不能以它替代一般耦合物理场的完整 Liouville 目标。
