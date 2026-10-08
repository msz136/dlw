# 实际首留数、正规 η 系数与最高二次块

本补充对应首留数、全阶正规系数和真实扰动多项式的 Lean 证明链。下面区分已经证明的表示连接与保留的基础表示规格。

## 首留数与物理能量

`FirstResidueEnergy.lean` 从每个 transfer 的三个真实左正规系数、有限有序乘积和总导数积分为零，推导一般有限周期的第三 monodromy 系数积分。`PhysicalFirstResidue.lean` 把系数环实例化为真实 (C^infty) 周期函数，把积分实例化为实际区间 Lebesgue 积分，并证明系数版 prefix resolvent 等于已经构造的

\[
R=hP_0\bigl(\operatorname{prefix}+\tfrac12\bigr)P_0.
\]

固定平均条件在系数环中给出

\[
m_1=-G,\qquad m_2=\frac{G^2-T}{2},\qquad
G=\frac{hMc}{4},\quad T=\frac{hM\gamma}{4}=2GB.
\]

`physicalComputedC1_eq_energy` 的结论为

\[
C_1^{\rm coeff}=-\frac{H_0}{8G}
 +\left(\frac{G^2}{12}+B^2\right)L_x.
\]

这里 (C_1^{\rm coeff}) 是由明确的 inverse-series 首系数计算出来的实际积分；能量等式是结论。`physicalK_eq_of_PDO_inverse_coefficients` 进一步只以三个逐阶乘积方程和归一化留数表示为前提，把它接到真实算子 (L) 的 (operatorname{res}L)，推出所需 (K) 恒等式。

## balanced 场上的 η 正规延拓

取 (U_j=2B+2f_j,;w_j=c,;g=hc/4=2\eta)。两项一阶算子的系数为

\[
\alpha_j=B+f_j+\eta,\qquad \beta_j=B+f_j-\eta,
\qquad T_j=1-2\eta(D-\beta_j)^{-1}.
\]

若 (Q_j=(D-\beta_j)^{-1}=\sum_{r\ge0}q_{j,r}D^{-r-1})，则左 inverse 方程确定

\[
q_{j,0}=1,\qquad q_{j,r+1}=\beta_jq_{j,r}-Dq_{j,r}.
\]

所有 (q_{j,r}) 都是在 (B,\eta,f_j^{(k)}) 中的有限微分多项式。设 (V_j=-2Q_j)，则有限有序乘积的 quotient 无需除 η：

\[
H_0^{\rm product}=0,\qquad
H_{n+1}^{\rm product}=V_n+H_n^{\rm product}
       +\eta V_nH_n^{\rm product},\qquad
\mathcal M-1=\eta H_M^{\rm product}.
\]

其 (D^{-1}) 系数恒为 (-2M)。因此

\[
L=-2M(H_M^{\rm product})^{-1}+B-M\eta
\]

的 inverse 逐阶递推只除非零实常数 (-2M)，没有 η 分母。`balancedNormalizedCoefficient_leading` 证明归一化最高系数为一。η 为零时得到的是这些系数多项式的正规求值，而不是对原奇异分式的直接代入。

## 全阶权重由递推证明

`BalancedCoefficientRecurrence.lean` 使用真正的 `MvPolynomial`，变量为 (B,\eta,f_j^{(k)})。空间导数由 `MvPolynomial.mkDerivation` 构造，参数导数为零，field jet (k) 的导数为 jet (k+1)。赋权

\[
\mathrm{wt}(B)=\mathrm{wt}(\eta)=1,\qquad
\mathrm{wt}(f_j^{(k)})=k+1.
\]

实现的 literal normal product 为

\[
(a*b)_k=\sum_{r+s+\ell=k}
  \binom{o_a-r}{\ell}\,a_rD^{\ell}b_s.
\]

空间导数升权一，所有乘积、quotient、固定 leading inverse 和幂次递推都保持对应权重。因此 `balancedResiduePolynomial_homogeneous M n` 无需输入任何目标 homogeneity 假设，直接证明 (\operatorname{res}L^n) 的系数多项式权重为 (n+1)。

对 odd 阶 (n=2k+1)，field-degree 为二且总微分阶为 (2k) 的单项式满足

\[
\underbrace{a+b}_{B,\eta\text{ 次数}}+2+2k=2k+2,
\qquad a=b=0.
\]

`balancedOddResidue_top_parameter_independent` 对真正的有限 support projection 证明：最高微分阶二次块在任何 (B,\eta) 上的求值，等于 (B=\eta=0) 上的求值。`perturbationPolynomial_eval` 则构造普通实多项式，其 ε 求值等于全部 field jets 乘 ε 后的密度求值。

## normal trace 不再假设目标 Hessian

`NormalResidueBridge.lean` 的 `PeriodicNormalResidueModel` 明确列出系数嵌入、(D) 的 formal unit、留数映射及定义性 order 规则。对于这样的 PDO 表示，由

\[
[D,a]=a_x,\quad \operatorname{res}(\text{differential})=0,
\quad\operatorname{res}(D^{-1}a)=a,
\quad\operatorname{res}(aX)=a\operatorname{res}X
\]

归纳推出

\[
\operatorname{res}(D^naD^{-1}b)=(D^na)b.
\]

接入真实周期积分后，`BalancedResolventStart.odd_spectral_second_from_normal_residue_model` 从 source factor 的 affine jet 数据得到

\[
\bigl[\varepsilon^2\bigr]C_{2k+1}
 =\frac2M(-1)^{k+1}\int(D^kf)^2dx
\quad(B=\eta=0).
\]

这个定理没有预设目标 spectral second derivative 或目标 trace 恒等式；剩余条件是明确的 PDO 表示规则。

## 同一正规表示的全阶实现

`BalancedRealization.lean` 的 `NormalPDOModel` 显式规定正规系数、有限广义二项式乘法、阶数上界和 leading-unit 逆的阶数上界。`FactorRealization.inverse_coefficient_realization` 从实际一阶算子的乘法逆方程归纳推出全部 resolvent 系数。

`BalancedSpectralRealization.lean` 随后证明真实有限 quotient、其逆、归一化算子和全部幂次的系数都等于独立构造的有限多项式递推。特别是

```lean
theorem NormalizedRealization.residue_realization
    (hM : M ≠ 0) (n : ℕ) :
  model.coefficients (realization.L ^ n) (-1) =
    e.evaluation (balancedResiduePolynomial M n)
```

此实现链已由官方检查器完整检查 15 个本地模块通过：`.lean-runs/20261006_233816_bc861df4/result.json`。

## 真实 ε 多项式的二次项，不假设算子参数 jet

`BalancedCoefficientJet.lean` 把 field jet 真正代为
\(\operatorname C(f_j^{(r)})X\)，把 \(B,\eta\) 代为零，得到普通系数多项式。其三张映射是实际系数提取

\[
J_0p=[\varepsilon^0]p,\qquad
J_1p=[\varepsilon^1]p,\qquad
J_2p=2[\varepsilon^2]p.
\]

空间相容性由 `MvPolynomial` 归纳证明。`DifferentialJetEvaluation.lean` 从有限正规乘法求和证明三张映射的 Leibniz 规则。`CoefficientJetRealization.lean` 的 inverse 定理则对系数指标强归纳：固定 leading 常数和两个字面乘法恒等式确定所有逆系数的第一、第二 jet。没有在无限 PDO 环上假设参数微分的提升或自然性。

`BalancedResolventCoefficientJet.lean` 从 \(D Q_0=1\)、\(D Q_1=fQ_0\)、\(D Q_2=2fQ_1\) 的实际正规系数证明全部 resolvent jet。`BalancedQuotientCoefficientJet.lean` 把它们按真实 quotient 递推聚合。两活跃格点 \(f,-f\) 给出

\[
J_0H=-2MD^{-1},\qquad J_1H=0,
\qquad J_2H=-8D^{-1}fD^{-1}fD^{-1}.
\]

静态 \(-2MD^{-1}\) 的逆单位由非零实常数单位和 \(D\) 显式构造。`BalancedNormalizedCoefficientJet.lean` 推出真实归一化多项式的三阶数据

\[
J_0L=D,\qquad J_1L=0,
\qquad J_2L=-\frac4M fD^{-1}f.
\]

`CoefficientJetPower.lean` 对全部幂次证明对应的有限系数 jet，并用循环迹归纳计算其 trace。最终 `BalancedActualCoefficientJet.lean` 的 `balancedOddDensity_actual_second_trace` 证明

\[
\frac12\int J_2\!\left(\frac1{2k+1}\operatorname{res}L^{2k+1}\right)dx
=-\frac2M\operatorname{Tr}(D^{2k}fD^{-1}f),
\qquad k\in\mathbb N.
\]

这里左侧来自 literal ε 系数多项式，而非预设 Hessian。`CoefficientJetPointwise.lean` 又证明周期系数点值上的 \(J_2\) 正好等于已有实多项式 `perturbationPolynomial` 的系数 2 的两倍。

这条实际 coefficient jet 与二次 trace 链的官方闭包检查覆盖 24 个本地模块，全部通过：`.lean-runs/20261007_000728_33c0cb29/result.json`。两个上述终点的 `#print axioms` 只有 `propext`、`Classical.choice`、`Quot.sound`。

## 实际物理振幅多项式与 Fourier 导数矩阵

`BalancedAmplitudeEvaluationCore.lean` 在真实周期系数环上，把 \(B,\eta\) 代为常系数，把 field jets 代为 \(\operatorname C(f_j^{(r)})X\)。普通多项式在 \(\varepsilon\) 上求值，严格等于 balanced 周期场 \(\varepsilon f\) 上的密度求值；把周期系数在 \(x\) 上求值，严格等于原实系数 `perturbationPolynomial`。证明通过两个 `MvPolynomial` algebra hom 的生成元等式完成，没有添加参数求导自然性前提。

`ActualBalancedAmplitudeBridge.lean` 由此证明，真实全局 charge 的物理振幅线多项式等于该 balanced 密度多项式的逐系数周期积分。对互异正 Fourier 模式 \(q_i\)、振幅 \(a_i\) 和 \(\omega_i=2\pi q_i/L_x\)，其实际二次系数为

\[
[\varepsilon^2]\mathcal C_{2k+1}(\varepsilon z_a)
 =\sum_i a_i^2 F_k(\omega_i^2),
\]

其中 \(F_k\) 是已定义的实际密度频率多项式 `actualOddFrequencyPolynomial par k`。

同文件没有预设导数矩阵：由 `ActualFourierEntries.lean` 已证明的普通多项式极化恒等式

\[
[\varepsilon]d\mathcal C(\varepsilon z)[v]
 =[\varepsilon^2]\mathcal C(\varepsilon(z+v))
 -[\varepsilon^2]\mathcal C(\varepsilon z)
 -[\varepsilon^2]\mathcal C(\varepsilon v)
\]

得到真实方向导数的实际一次系数

\[
[\varepsilon]d\mathcal C_{2k+1}(\varepsilon z_a)[v_j]
 =2a_jF_k(\omega_j^2).
\]

对应 Lean 终点为 `actualBalancedAmplitude_coeff_two` 与 `actualBalancedAmplitudeDifferential_coeff_one`。这两个文件已直接由 Lean 检查通过，输出写入 `.lean-runs/20261006_224015_8a1b7c38/lib/lean`；三个关键定理的 `#print axioms` 仍只有 `propext`、`Classical.choice`、`Quot.sound`。最终工程的统一闭包检查由主报告记录。

## 基础表示的准确边界

上述定理都是从明确的 `NormalPDOModel` 定义规则推出的普遍定理。整个无限正规 PDO 环的存在、乘法全局结合律及模型字段的具体全环构造，仍未在工程内从集合论定义完成。标准周期留数循环性和 Adler 理论是用户允许显式外置的基础理论；模型存在与定义性表示规格应另外如实列出，不能以没有 `sorryAx` 等同于已完成基础存在性证明。
