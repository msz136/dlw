# 一般周期 DLW Notebook：只读数学核对

日期：2026-10-07。已核对 `dlw_integrability_lean_20261006` 的真实源码及当前 `LEAN_PROOF_REPORT.md`；未修改证明库或共享记录。

上述 det 非零见证、最终族开稠密独立与单独 K/P 守恒示例已保存为 `ReviewExamples.lean`，通过现有最终入口的已验证 `.olean` 离线编译（exit 0），执行证据见 `review_compile.json`。无需重建证明库。

## 起点与基础

- `FieldParameters`：`M : ℕ`、`M_ge_two : 2 ≤ M`、`Lx_pos : 0 < Lx`、`h_pos : 0 < h`、`c_ne_zero : c ≠ 0`，`gamma` 无额外条件。
- `SmoothPeriodicField`：`Fin M → ℝ → ℝ`，逐格点 `ContDiff ℝ ∞` 与周期 `Function.Periodic ... Lx`。
- `FieldCoordinates`：两个真实光滑周期场 `p,s`，逐点格点均值为零。物理场重构为 `U_j=p_j+(γ−Π(ps))/c`、`w_j=c+s_j`。任意满足 `Πw=c, Π(Uw)=γ` 的实际场可以提取坐标并重构恢复。
- `previousSite` 用模 M 实现 `j−1`；`deltaMinus=(f_j−f_(j−1))/h`；`averageMinus=(f_j+f_(j−1))/2`。这里格点移位与连续空间导数严格区分。
- `StartPoint` 的轨迹是 `ℝ → FieldCoordinates par`，两个坐标关于 `(t,x)` 联合无限光滑，并满足 `PhysicalDLW`。不是解的存在定理。
- 终点仍依赖 `FactorSpectralFoundation par`。外部接口包括形式正规 PDO 表示和形式逆元、周期留数迹循环性/实际积分身份、源代入表示，以及标准自由一阶因子的 Adler 乘积/求逆规则。目标守恒、对易、能量身份、Fourier 顶系数、独立性均已从该接口推导，不是该接口的字段。
- `StartPoint.lean` 等早期模块头注释提到能量恒等式仍需前提，这是历史中间阶段。`PhysicalEnergyEndpoint.actualPhysicalK_eq_first_charge` 已消去该目标前提，Notebook 应按最终入口解读。

## 谱族与物理量映射

`GlobalSpectralRealization.NormalizedRealization.L`：

```text
L = −G (Mmonodromy−I)^(−1) + (B−G/2) I,
G=hMc/4≠0, B=γ/(2c).
```

`GlobalPDO.constructedCharge par n z = fieldPolynomialIntegral par (periodicDensityPolynomial par n) z` 是有限微分多项式积分。`actualCharge_eq_trace rep n` 输出 `C_n=(n:ℝ)⁻¹ Tr(L^n)`。数学展示应限 `n≥1`，虽然 Lean 统一定义所有自然数阶。

`physicalEnergy par (latticeResolvent par) z` 是 H0，`actualPhysicalK` 是 K，`coefficientMomentum` 是 P。

```text
H0 = h Σ_j ∫ (U_j² w_j/2 + h² w_j³/96 + w_j U_(j,x)
                  + w_j (R w_x)_j/2) dx,
K = H0 − γ h Σ_j ∫ U_j dx,
P = h Σ_j ∫ p_j s_j dx,
K = −8G C1 + (γ/c)P + κ,
κ = 8G(G²/12+B²)Lx − γ²hMLx/c.
```

`actualPhysicalK_eq_first_charge par z` 是无能量目标假设的真实定理。低阶 H0 身份来自 `GlobalPDO.constructedCharge_one_eq_physicalComputedC1` 和 `physicalComputedC1_eq_energy`：`C1=−H0/(8G)+(G²/12+B²)Lx`。

H0 与 C1 仿射相关，不能将 H0、K、P、C1 同时列作独立族。最终物理族定义：

```lean
def actualPhysicalFamily (par : FieldParameters) : ℕ → ClosedPeriodicPair par → ℝ
  | 0 => actualPhysicalK par
  | 1 => coefficientMomentum par
  | n + 2 => GlobalPDO.constructedCharge par (2 * n + 3)
```

对应 `I0=K,I1=P,I2=C3,I3=C5,...`。

## 守恒与对易的真实终点

`StartPoint.actualConstructedCharge_conserved start foundation.toActual n hn t`：

```lean
HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ)) 0 t
```

对应实际普通时间导数 `dC_n(z(t))/dt=0`，正整数 n。`HasDerivAt` 的第二个实数参数是导数值，不是取值。

`StartPoint.actualPhysicalFamily_conserved start foundation.toActual n t`：

```lean
HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) 0 t
```

可用 `simpa only [actualPhysicalFamily]` 展示 n=0 和 n=1 的 K/P 守恒。

`actualSpectralBracket_zero par foundation.toActual m n z hm hn`：

```lean
reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
  (GlobalPDO.constructedChargeGradient par n z) = 0
```

对应 `{C_m,C_n}_red=0`。`reducedBracketValue par F G` 的两个参数是梯度场，不是泛函本身；定义为真实加权积分配对 `<F,J_red G>`，`J_red=−[[0,P0∂x],[P0∂x,0]]`。

`actualPhysicalFamily_commutes par foundation.toActual m n z` 给出 `{I_m,I_n}_red=0`。

守恒证明连接：原物理方程 → `start.actualVelocity_eq_K_vector` → 实际多项式积分时间导数等于真实 Hamiltonian 括号 → `constructedCharge_bracket_actualK_zero` → `HasDerivAt ... 0 t`。

## Jacobian 满秩、真实见证与泛型独立

应展示有限 Fourier 切片的 Jacobian 子式，而非整个无限维空间的一个行列式。`covectorMinor covectors directions i j = covectors i (directions j)` 对应 `J_ij=dC_(2i+1)(z_eps)[v_j]`。

`actualBalancedAmplitude_coeff_two`：

```text
[eps²] C_(2k+1)(z_(eps Σ a_j cos(ω_jx))) = Σ a_j² F_k(ω_j²).
```

`actualOddFrequencyPolynomial_degree par k`：`deg F_k≤k`。

`actualOddFrequencyPolynomial_top par foundation.toActual k`：

```text
[ξ^k]F_k=(Lx/M)(−1)^(k+1)≠0.
```

`actualFourierMatrix_coeff_one`：`[eps]J_ij=2a_j F_i(ω_j²)`，列幅度因子不能省略。

`actualOdd_small_Fourier_minor par foundation.toActual ...` 仅以模式正且互异、幅度非零、正半径为条件，输出任意小的正 eps 使真实非线性 Jacobian 子式非零；没有 hminor 目标假设。

可运行示例（`import FinalEndpoint`、`open DLWLean`、`open scoped DLWFieldTopology`）：

```lean
example (par : FieldParameters) (foundation : FactorSpectralFoundation par)
    (N : ℕ) (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      (covectorMinor (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
          (balancedMomentumState par
            (eps • periodicCosineSumCoefficient par (canonicalWitnessMode (N := N))
              (fun _ => 1)))))
        (balancedFourierDirection par (canonicalWitnessMode (N := N)))).det ≠ 0 := by
  exact actualOdd_small_Fourier_minor par foundation.toActual
    canonicalWitnessMode canonicalWitnessMode_pos (canonicalWitnessMode_injective N)
    (fun _ => 1) (fun _ => by norm_num) radius hradius
```

`canonicalWitnessMode j=j.val+1`，正性/单射已在实际源码中证明。该例对任意 `N`、任意正半径，不须输入 det 非零。

`actualOdd_generically_independent par foundation.toActual N` 输出每个有限奇数谱前缀 `dC1,dC3,...,dC_(2N−1)` 在一个开稠密场集线性独立。

`actualPhysicalFamily_generically_independent par foundation.toActual N` 同样输出最终物理族每个有限前缀的开稠密微分独立。两者均无 witness/minor/独立性目标假设。

物理族桥：纯 p Fourier 方向满足 dP(v_j)=0，额外真实 s 方向满足 dP(extra)=4h∫g²≠0，再由 −8G≠0 将 C1 换成 K。

## 结论和准确范围

`general_periodic_dlw_integrability par foundation` 输出 `PeriodicIntegrabilityConclusion par`：同一谱表示的全阶迹身份、物理能量身份、原物理轨迹的 Hamiltonian 坐标演化、正整数谱族对易和守恒、奇数谱族及最终物理族逐有限前缀开稠密独立。

不能表述为已构造形式 PDO 基础实例/无外部前提，或已证明所有有限块同时独立的稠密可数交、完整任意非线性泛函 Poisson 代数、全局解存在、全局作用角变量/紧环面。

`#print axioms` 只报告标准 `propext/Classical.choice/Quot.sound` 不会消除 `FactorSpectralFoundation` 这个显式定理参数。Notebook 应让假设和结论在同一 `example` 签名可见。

## 生成正文核对

已逐单元审阅 `DLW刘维尔可积性report.ipynb` 的 15 个代码单元与 16 个 Markdown 单元。关键定义、实际原方程、普通时间守恒、实际积分括号为零、Fourier 顶系数、真实 Jacobian 非零见证、开稠密微分独立和最终主定理与真实库一致。没有把目标守恒/对易/能量/独立性放入前提。正文正确保留显式形式 PDO 基础和逐有限前缀范围。

已向撰写 agent 建议并确认补入单独的 `hamiltonianConserved`、`momentumConserved`，使 K/P 导数为零的目标直接可见，而不仅通过族编号间接表达。源内容核对证据见 `mathematical_content_validation.json`；全部 Notebook 执行由主 agent 另行验证。
