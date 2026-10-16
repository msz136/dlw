# 半离散 DLW 一般周期场的 Lean 形式化

日期：2026-10-06。依据主文档第 13–17 节及其前序单值算子证明。本文仅记录实际源码与校验范围，随证明推进更新。

**当前状态：证明进行中。** 已核验实际闭合场坐标、任意周期格点算子 R、原隐式 PDE 到共同时间模态与周期热势、实际时空导数、完整因子交织，以及实际 Hamiltonian 的沿线普通导数和生成原方程的性质。从原 PDE 出发的普通时间守恒终点保留显式形式 PDO 表示接口。所有阶实际算子留数已与一般闭合场上的有限微分多项式积分连接；这一步通过 21 个本地模块统一检查。实际 Euler 变分梯度、约化括号识别、与动量的对易和实际光滑场拓扑也已构造。完整谱对易与非零物理 Fourier 子式仍在连接，不能将其称为全任务已经完成。

用户已明确允许将周期伪微分算子留数迹的循环性和 Adler 乘积／求逆理论列为外部理论前提。其他尚未验证的桥接会单独列出，不并入这项授权。

## 1. 物理起点

固定

\[
M\ge2,\qquad h>0,\qquad L_x>0,\qquad c\ne0,\qquad \gamma\in\mathbb R.
\]

\(\Pi\) 是逐点格点平均。物理场实值、光滑、\(x\) 周期，且

\[
\Pi w=c,\qquad \Pi(Uw)=\gamma.
\]

独立坐标与重构为

\[
\Pi p=\Pi s=0,\qquad
U_j=p_j+\frac{\gamma-\Pi(ps)}c,\qquad w_j=c+s_j.
\]

`FieldCoordinates.lean` 证明重构满足平均闭合，并证明任意满足闭合条件的物理场都可以提取坐标并精确恢复。它没有把孤子参数空间代替一般周期场。

真实源码中的物理场起点：

```lean
structure PeriodicPhysicalState (par : FieldParameters) where
  U : SmoothPeriodicField par.M par.Lx
  w : SmoothPeriodicField par.M par.Lx
  mean_w : ∀ x, latticeMean (fun j => w.value j x) = par.c
  mean_Uw : ∀ x,
    latticeMean (fun j => U.value j x * w.value j x) = par.gamma
```

`StartPoint.lean` 进一步直接定义原物理方程：

\[
\delta_-\left[U_t+\partial_x\left(\frac{U^2}2+\frac{h^2}{32}w^2\right)\right]
+\partial_x^2(\delta_-U+M_-w)=0,
\qquad w_t+\partial_x(Uw)-w_{xx}=0.
\]

轨迹的 \((t,x)\) 联合光滑性明确作为正则性条件。守恒应沿实际存在的足够光滑解表述，不包含任意光滑初值上的适定性结论。

Lean 中普通无限光滑性统一使用 `ContDiff ℝ ∞`。Mathlib 的 `⊤` 不用来代替这里的普通无限光滑阶。

## 2. 算子构造及已经核验的终点

主文档中的构造是

\[
T_j=(D-U_j/2+hw_j/8)^{-1}(D-U_j/2-hw_j/8),
\qquad\mathcal M=T_{M-1}\cdots T_0,
\]

\[
G=\frac{hMc}{4}\ne0,\qquad B=\frac\gamma{2c},
\qquad L=-G(\mathcal M-I)^{-1}+(B-G/2)I.
\]

这里的逆是形式伪微分逆，迹是 Adler 留数积分

\[
\mathcal C_n=\frac1n\int_0^{L_x}\operatorname{res}_D L^n\,dx.
\]

`LatticeResolvent.lean` 已从有限前缀矩阵构造

\[
Qf_j=h\left(\sum_{i<j}f_i+\tfrac12 f_j\right),\qquad R=P_0QP_0,
\]

并证明逆差分方程、斜对称、零平均和唯一性。`ActualPhysicalSource.lean` 从上述原方程与固定平均推出

\[
U_t=-\left(UU_x+\frac{h^2}{16}ww_x+U_{xx}+Rw_{xx}\right)
+\frac2cD\Pi e,\qquad w_t=w_{xx}-D(Uw).
\]

实际周期热势为

\[
V_j=\tfrac12(Rw_x)_j-\tfrac h4w_{j,x}-\Pi e/c+v_0,
\qquad V_{j+1}-V_j=\tfrac h2w_{j,x}.
\]

`PeriodicSpacetimeCoefficients.lean` 构造整个光滑时空函数环及真实的空间、时间导数。`ActualCoefficientSource.lean` 将原 PDE 送入系数源，`HeatIntertwiner.lean` 随后推出完整一阶因子交织。因此下式不再作为该物理源桥的前提：

\[
\dot T_j=Q_{j+1}T_j-T_jQ_j,\qquad Q_M=Q_0.
\]

Lean 推出

\[
\dot{\mathcal M}=[Q_0,\mathcal M],\qquad
\dot L=[Q_0,L],\qquad
\frac1n\operatorname{Tr}\dot{(L^n)}=0\quad(n\ge1).
\]

`SpectralVariation.lean` 从 Leibniz、循环迹和单位求逆公式证明谱变分，未将梯度公式作为假设：

\[
\delta\mathcal C_n=\operatorname{Tr}(X_n\,\delta\mathcal M),
\qquad X_n=G A L^{n-1}A,\qquad A=(\mathcal M-I)^{-1}.
\]

它随后与 `Monodromy.lean` 给出

\[
[\mathcal M,X_n]=0,
\qquad\operatorname{Tr}\bigl(X_m A_{\mathcal M}(X_n)\bigr)=0.
\]

`Endpoint.operatorStartFromPhysicalSources` 从物理系数源构造有限周期 `OperatorStart`。这里仍显式给定满足系数嵌入和交换关系的结合算子表示，以及实现各形式逆的单位；完整 PDO 环的标准实例尚未在工程中构造。

`ActualTraceDerivative.lean` 由紧时空矩形上的连续导数界证明真实区间积分可逐时求导。`ActualConservationEndpoint.lean` 新终点为

```lean
theorem physical_spectral_conservation
    (pdo : PhysicalFormalModel par start A) :
    ∀ n : ℕ, 0 < n → ∀ t : ℝ, HasDerivAt (pdo.C n) 0 t
```

这个接口只给定具体 PDO 表示、逆、留数与实际时间导数的相容性、已获许可的循环迹；不把物理 Lax 或守恒结论作为输入。它已通过 25 个本地模块的统一检查，记录为 `.lean-runs/20261006_214907_3d2c5194/result.json`。后续扩展的源文件仍需重新核对当前哈希。

## 3. 约化、物理 Hamiltonian 和独立性

`ReducedPairing.lean` 证明有限格点链式法则及约化配对恒等式：共同 \(U\) 梯度为零时，重构坐标的非线性剪切不贡献配对，零平均投影可以准确移去。这是把原因子场括号降到 \(J_{\rm red}\) 的有限代数步骤。

真实动量用区间积分定义：

\[
\mathcal P=h\sum_j\int_0^{L_x}p_js_j\,dx.
\]

`FieldCoordinates.U_integral_identity` 已证明

\[
h\sum_j\int U_j\,dx=\frac{hML_x\gamma}{c}-\frac{\mathcal P}{c}.
\]

`FirstResidueEnergy.lean` 通过真实的有限传输乘积计算至三阶，并将有限前缀耦合换为 R。`PhysicalFirstResidue.lean` 用实际周期积分消去全导数，推出首阶身份

\[
\mathcal C_1=-\frac{\mathcal H_0}{8G}
+\left(\frac{G^2}{12}+B^2\right)L_x,
\]

随后 `physicalK_eq_computed_first_residue` 证明

\[
\mathcal K=-8G\mathcal C_1+\frac\gamma c\mathcal P+\kappa,
\qquad
\kappa=8G\left(\frac{G^2}{12}+B^2\right)L_x
-\frac{\gamma^2hML_x}{c}.
\]

首阶能量公式本身已经从计算的系数推出。`GlobalFirstResidueBridge.lean` 进一步从全局正规递推推出前三阶字面系数与物理首留数的对应，证明 `constructedCharge_one_eq_physicalComputedC1` 和 `physicalK_eq_constructed_C1`。这两个纯场定理只量化参数与真实闭合场，不要求预设首留数、能量恒等式或每个场的形式单位。完整 PDO 实现的首阶谱量也由同一计算接入。

`ActualHamiltonianDerivative.lean` 对实际重构图表的任意仿射方向证明

\[
\left.\frac d{d\varepsilon}\right|_0
\mathcal K(p+\varepsilon\dot p,s+\varepsilon\dot s)
=h\sum_j\int(K_{p,j}\dot p_j+K_{s,j}\dot s_j)dx.
\]

其中 \(U\) 的二次剪切项明确保留，R 的变分由其实际斜对称性处理。`ActualHamiltonianFlow.lean` 从原 PDE 推出真实 \((p_t,s_t)=J_{\rm red}\nabla\mathcal K\)，已通过 23 个本地模块统一检查。`GradientNondegeneracy.lean` 从实际积分平方非负及零积分的非退化性，证明代表全部真实方向导数的梯度唯一。`PhysicalEnergyEndpoint.actualPhysicalKGradient_eq_first_charge` 因而证明

\[
\nabla\mathcal K=-8G\nabla\mathcal C_1+(\gamma/c)\nabla\mathcal P.
\]

`ActualPhysicalFamily.lean` 在实际积分约化括号和真实方向协变量上完成最终族的线性替换。`PhysicalFamilyGenericity.lean`、`CovectorWitness.lean` 将任一真实独立见证送到实际场上的开稠密集；未预设最终族的泛型独立性。

独立性证明采用原文的 Fourier 切片

\[
w_j=c,\quad U_0=2B+2f,\quad U_1=2B-2f,
\quad U_j=2B\ (j\ge2),
\quad f=\varepsilon\sum_{i=1}^N a_i\cos(k_ix).
\]

文档所需的任意阶身份是

\[
\mathcal C_{2k+1}^{(2)}
=\frac2M(-1)^{k+1}\int(D^kf)^2dx
+\text{低导数阶的二次项}.
\]

`QuadraticResolvent.lean` 从相对二阶 jet 的乘积和求逆法则推出均衡切片的二次算子变分。`QuadraticSymbol.lean` 用真实整数广义二项式系数计算留数，并对实际周期函数执行任意阶分部积分。Fourier 计算涵盖余弦及有限和的光滑性、周期性、零平均、正交性和任意阶导数平方积分。`BalancedCoefficientRecurrence.lean` 已从字面正规乘法与求逆递推证明全部阶数的加权齐次性，以及最高二次微分块不依赖 \(B,\eta\)。`NormalModelResidue.lean` 将完整正规系数定义规则送入实际留数公式。剩余连接是这些多项式的二阶幅度系数与同一个算子 jet 的对应。

`Independence.lean` 已证明：不同正频率的平方节点互异；三角频率多项式的评价行列式等于 Vandermonde 行列式乘对角系数积；非零评价小行列式推出真正的协变量线性独立。Fourier 二次 Jacobian 的列因子也已保留为 \(2a_j\)，不是只有无振幅的 Vandermonde。

Vandermonde 矩阵是振幅 Jacobian 关于 \(\varepsilon\) 的领先项，不能直接替代非零振幅下的完整 Jacobian。`Genericity.lean` 已证明，只要行列式多项式具有一个非零系数，就能在任意小的正振幅处找到非零见证。`Endpoint.lean` 按这个逻辑组织条件化独立性终点，显式保留实际行列式的多项式身份和领先系数身份。

动量的补充方向为

\[
\delta s_0=f,\quad\delta s_1=-f,\quad
d\mathcal P=4h\int f^2dx\ne0.
\]

`physical_covectors_independent_from_odd_minor` 证明：奇数族小行列式非零、动量在原见证方向上为零、在补充方向上非零，则

\[
d\mathcal K,d\mathcal P,d\mathcal C_3,d\mathcal C_5,\ldots
\]

线性独立，其中 \(d\mathcal K=-8G\,d\mathcal C_1+(\gamma/c)d\mathcal P\)。`PhysicalBracket.lean` 直接从真实动量积分的仿射二次展开推出变分梯度，并构造零平均周期场上的 Jred、周期积分反对称配对和负向空间平移。`MomentumWitness.lean` 与 `FourierMomentum.lean` 将补充方向实现为实际闭合周期场并证明非零。

`GlobalCoefficientRecurrence.lean` 在固定 \(M,h,c,\gamma\) 的全部闭合场上构造真实有限微分多项式。一般 transfer 是 \(1-(D-\beta_j)^{-1}g_j\)，其中 \(g_j=hw_j/4\) 在右侧，正规乘法中包含它的所有导数。单值化的最高系数为固定非零常数 \(-G\)，其 inverse 仅除固定常数。`GlobalSpectralRealization.lean` 从统一的 `NormalPDOModel` 定义规则和字面形式逆，证明全部阶数

```lean
theorem residue_realization (n : ℕ) :
    model.coefficients (realization.L ^ n) (-1) =
      evaluation par z (residuePolynomial par n)
```

并由留数迹的积分定义证明 `constructedCharge_eq_spectralInvariant`。这里多项式性与谱量身份都是结论，没有作为输入。

`AmbientEulerVariational.lean`、`EulerVariationalGradient.lean` 由多项式偏导和全部阶实际分部积分构造梯度

\[
E_{\alpha,j}(P)=\frac1h\sum_{k\ge0}(-D)^k
\operatorname{eval}\!\left(\frac{\partial P}{\partial z_{\alpha,j,k}}\right),
\]

其中和是有限的。`AmbientChartDerivative.lean` 保留真实非线性图表的二次项，`PolynomialReductionEndpoint.lean` 将实际共同 U 变分消失送到零和 U 梯度及约化括号识别。`ConstructedChargeMomentum.lean` 从常数系数密度的空间平移变分是全导数，证明所有实际构造谱积分与动量在真实约化括号下对易。

`FieldGenericity.lean` 已在实际闭合周期场上构造全部空间导数在紧周期区间上的一致拓扑，证明其为 Hausdorff 拓扑向量空间，并证明所有实际有限微分多项式积分连续、沿仿射线为有限多项式、实际方向导数为线性协变量。一个实际非零导数子式即可推出每个有限块的开稠密独立区域。这部分已通过 9 个本地模块统一检查。

`BalancedAmplitudePolynomial.lean` 证明字面 \(\varepsilon\) 代入的每个单项式恰含 \(\varepsilon^{\text{field degree}}\)，故实际二次幅度系数就是有限二次投影。`QuadraticMonomialDecomposition.lean` 将每个二次 field 单项式精确分解为两个空间 jet。`QuadraticFrequencyPolynomial.lean` 对所有有限混合二次导数项和真正有限余弦和构造频率多项式，证明导数阶界、顶系数和全部实际积分公式。`PolynomialMatrixWitness.lean` 将完整多项式矩阵的零常数项与非零一阶系数行列式送到任意小正幅度的非零实际行列式。

`dense_residual_nonzero_family` 另证明带 Baire 条件的可数交结论。实际光滑场的 Baire 实例尚未构造；用户要求的每个有限块开稠密结论不依赖这一强化。

## 4. 原场终点和剩余工作

完整原场终点仍是

\[
\frac{d\mathcal C_n}{dt}=0,\qquad
\{\mathcal C_m,\mathcal C_n\}_{\rm red}=0,
\]

\[
\boxed{\mathcal K,\ \mathcal P,\ \mathcal C_3,\ \mathcal C_5,\ldots}
\]

任意有限前缀在泛型场上独立。这里基本结论的“泛型”指每个有限块的开稠密正则集。全部有限块同时独立的稠密剩余集还需要实际场空间的 Baire 论证；不意味着所有场处独立，也不包含全局作用量—角变量。

继续形式化的具体桥接为：

1. 周期光滑系数的实际 PDO 实现、实际因子形式逆及 \(\mathcal M-I\) 的非零首系数所给出的可逆性。
2. 已完成的实际轨迹、周期热势、完整交织、普通积分微分及全局留数多项式接入同一个表示，并统一复验。
3. Adler 因子化应用到原常场括号，实际标量规范变分送入已经构造的 Euler 梯度及约化括号。非周期规范 primitive 的处理不能借用周期循环迹；已单独证明标量交换子的留数逐点为零。
4. 已完成的首阶能量计算与完整正规系数规则的对应，以及全阶 balanced 多项式与算子二阶 jet 的对应，推出真实 Fourier 雅可比的非零领先系数。一般闭合场系数含固定 G 的倒数，不是关于全部背景参数的普通多项式。
5. 实际 Fourier 非零子式送入已构造的真实场拓扑与有限块泛型定理。Baire 可数交为额外强化。

这五项不会因为抽象定理通过编译就自动成立。

## 5. 源码与复现

源码位于本目录。入口为 `Endpoint.lean`；各模块均由共享 Lean 4.34.0 / Mathlib v4.34.0 校验。

```powershell
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\dlw_integrability_lean_20261006' `
  -File 'C:\Users\msz\aca\Workspaces\dlw_integrability_lean_20261006\Endpoint.lean' `
  -TimeoutSeconds 300
```

初次完整入口已通过 11 个本地模块，记录为 `.lean-runs/20261006_181857_92f887a3/result.json`。后续扩展独立保留新的校验记录。已通过的关键 `#print axioms` 仅含 `propext`、`Classical.choice`、`Quot.sound`，没有新增公理或占位证明。该查询检查证明依赖，**不会消除定理参数中的显式前提**。

当前成功物理源桥校验记录为 `.lean-runs/20261006_214041_a1754e46/result.json`（15 模块），实际首留数能量桥为 `.lean-runs/20261006_214301_07b37bd9/result.json`（12 模块）。这两份记录对应相应文件的当前成功源码。新的实际守恒入口、二阶 Fourier 与全阶递推扩展继续保留独立记录；最终统一校验完成后补上完整源码哈希清单。

实际普通时间导数终点已通过 `.lean-runs/20261006_214907_3d2c5194/result.json`（25 模块）。均衡二阶 jet、真实 Fourier 见证及 eta 多项式商通过 `.lean-runs/20261006_214957_42347a47/result.json`（7 模块）。

新增关键记录：`20261006_221551_87e136f5`（实际 K 演化，23 模块）、`20261006_223327_94d5fd0e`（真实约化配对，23 模块）、`20261006_224015_8a1b7c38`（实际场拓扑与微分，9 模块）、`20261006_225953_c051cb7c`（全部实际谱留数的全局多项式实现，21 模块）。新增源码仍将随最终入口统一复验。

首阶纯物理能量桥统一检查通过 `20261006_232129_e42dca72`（29 模块），实际最终族组装通过 `20261006_231406_3910e789`（40 模块），balanced 全阶谱实现通过 `20261006_233816_bc861df4`（15 模块）。`VerifiedCore.lean` 正在统一复验当前源码及全部已连接核心，并保留尚未闭合的谱独立见证与 Adler 应用范围。
