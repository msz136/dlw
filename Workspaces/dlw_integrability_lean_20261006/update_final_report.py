"""Write the Markdown report only from a passed, unchanged final closure."""
from pathlib import Path
import datetime
import hashlib
import json

project = Path(__file__).resolve().parent
candidates = []
for path in (project / '.lean-runs').glob('*/result.json'):
    result = json.loads(path.read_text(encoding='utf-8-sig'))
    if result.get('status') == 'PASSED' and Path(result['target']).name == 'FinalEndpoint.lean':
        candidates.append((result['run_id'], path, result))
if not candidates:
    raise SystemExit('No passed FinalEndpoint closure; report was not changed.')
run_id, record, result = max(candidates)
for entry in result['files']:
    source = Path(entry['file'])
    if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
        raise SystemExit(f'Source changed since final check: {source.name}; report was not changed.')

def source_block(name, begin, end):
    text = (project / name).read_text(encoding='utf-8-sig')
    return text[text.index(begin):text.index(end, text.index(begin))].strip()

starting_state = source_block('FieldCoordinates.lean',
    'structure PeriodicPhysicalState', 'def PeriodicPhysicalState.toCoordinates')
starting_curve = source_block('StartPoint.lean',
    'structure StartPoint', 'theorem StartPoint.mean_closure')
ending_structure = source_block('FinalEndpoint.lean',
    'structure PeriodicIntegrabilityConclusion', 'theorem periodic_integrability_of_actual_foundation')
ending_theorem = source_block('FinalEndpoint.lean',
    'theorem general_periodic_dlw_integrability', '#print axioms actualCharge_eq_trace')
factor_theorem = source_block('FactorAdlerFoundation.lean',
    'structure FactorAdlerFoundation', 'theorem FactorAdlerFoundation.actual_covector_eq_projected')

report = r'''# 一般周期 DLW：Lean 证明起点、终点与基础前提

更新：@@DATE@@。数学来源为 [dlw_liouville_integrability.md](../../dlw_liouville_integrability.md) 第 13–17 节；该文档作为论证来源使用。交付为 Markdown 与 Lean 源码，没有生成 HTML。

**已完成并统一校验的是带显式形式 PDO 基础前提的定理。** 最终入口 [FinalEndpoint.lean](FinalEndpoint.lean) 的全部 @@COUNT@@ 个本地依赖模块已经由 Lean 4.34.0 / Mathlib 4.34.0 重新编译通过。实际守恒量、Euler 微分、约化括号、能量身份、Fourier 独立性见证及每个有限前缀的开稠密结论均在 Lean 中推导；没有把这些目标结论写成外部假设。

用户已允许把周期留数迹循环性和标准 Adler 乘积／求逆理论列为外部前提。**具体正规形式 PDO 环、所需形式逆元及系数源代入表示的存在，目前也仍由结构参数显式提供；这项额外基础范围的询问尚未得到答复。** 因此本报告不把当前结果称为已经从集合／级数定义构造了整个 PDO 基础的无条件证明。下面给出准确的起点、外部接口和终点。

## 1. 实际物理起点

固定

\[
M\ge2,\quad h>0,\quad L_x>0,\quad c\ne0,\quad\gamma\in\mathbb R.
\]

取实值光滑周期场，\(j\in\mathbb Z/M\mathbb Z\)、\(x\in\mathbb T_{L_x}\)，固定逐点格点平均闭合

\[
\Pi w=c,\qquad\Pi(Uw)=\gamma.
\]

Lean 中的真实场起点是：

```lean
@@STARTSTATE@@
```

用全局独立坐标

\[
p=P_0U,\quad s=w-c,\quad \Pi p=\Pi s=0,\qquad
U_j=p_j+\frac{\gamma-\Pi(ps)}c,\quad w_j=c+s_j.
\]

[FieldCoordinates.lean](FieldCoordinates.lean) 已证明从任意上述物理场提取坐标并重构后，\(U,w\) 逐点恢复。后续 `ClosedPeriodicPair par` 正是这两个零格点均值的真实光滑周期场的线性空间。

守恒性从原物理方程出发：

\[
\delta_-\!\left[U_t+\partial_x\!\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)=0,
\qquad w_t+\partial_x(Uw)-w_{xx}=0,
\]

其中 \(\delta_-=(I-E^{-1})/h\)、\(M_-=(I+E^{-1})/2\)。[StartPoint.lean](StartPoint.lean) 的 `PhysicalDLW` 逐项使用 Mathlib 的 `deriv` 表达这两条方程。给定解的正则性和方程条件为：

```lean
@@STARTCURVE@@
```

这里 `ContDiff ℝ ∞` 表示普通无限光滑。当前 `StartPoint` 使用全 \(\mathbb R\) 上的给定光滑轨迹；没有证明这类解的全局存在。

## 2. 构造同一个全阶谱族

设 \(D\) 为形式 PDO 的空间微分符号，定义

\[
T_j=\left(D-\frac{U_j}{2}+\frac{hw_j}{8}\right)^{-1}
\left(D-\frac{U_j}{2}-\frac{hw_j}{8}\right),\qquad
\mathcal M=T_{M-1}\cdots T_0,
\]

\[
G=\frac{hMc}{4}\ne0,\quad B=\frac\gamma{2c},\qquad
L=-G(\mathcal M-I)^{-1}+(B-G/2)I.
\]

正规形式 \(\mathcal M-I\) 的最高阶为 \(-1\)，其首系数为 \(-G\)。这由平均闭合与有限乘积递推证明；不要求逐点 \(w_j\ne0\)。所用逆元是形式 PDO 逆元，\(D^{-1}\) 没有被当成周期函数空间上的实际积分逆算子。

[GlobalCoefficientRecurrence.lean](GlobalCoefficientRecurrence.lean) 从有限阶正规乘法公式递推每个所需系数，直接定义真实场上的微分多项式积分：

```lean
def constructedCharge (par : FieldParameters) (n : ℕ)
    (z : ClosedPeriodicPair par) : ℝ :=
  fieldPolynomialIntegral par (periodicDensityPolynomial par n) z
```

每个固定 \(n\) 只涉及有限个空间 jet。[GlobalSpectralRealization.lean](GlobalSpectralRealization.lean) 证明该有限递推与表示中真实 \(L^n\) 的系数一致。最终 `actualCharge_eq_trace` 给出

\[
\mathcal C_n(z)=\frac1n\operatorname{Tr}(L(z)^n),\qquad
\operatorname{Tr}X=\int_0^{L_x}\operatorname{res}_D X\,dx,
\quad n\ge1.
\]

终点对每个场取一个表示，该表示同时实现全部阶数；不是对不同 \(n\) 分别假设不同的谱量身份。

## 3. 全部外部基础接口

最终主定理的唯一额外参数是 `FactorSpectralFoundation par`。它对每个实际闭合场要求存在 `PhysicalFactorSpectrumRepresentation`，其数据依次为：

1. 一个实代数上的 `NormalPDOModel`：系数嵌入、形式 \(D\)、有上界的整数阶系数、系数外延性、正规乘法公式及已有单位逆元的阶界。空间导数固定为实际 `periodicSpatialEvolution`，不是可任意指定的场导数。
2. 一阶分母和 \(\mathcal M-I\) 的形式逆元、循环迹及“迹等于实际周期留数积分”的身份。
3. 每个实际仿射系数方向的形式 PDO 源表示，以及在扰动参数零点的系数逐项代入同态；源的空间／参数导数均固定为真实导数。
4. 每个共同 \(U\) 方向的光滑形式 PDO 源表示。`ActualSpectralWardFoundation` 只要求这种表示存在；共同规范变分的零留数与 Ward 恒等式由源码推导。
5. 标准自由一阶因子的 Adler 乘积／求逆传输规则和正阶投影。

第 5 项的精确接口是：

```lean
@@FACTORINTERFACE@@
```

这里 `staticMonodromyVariation` 由独立因子 \((\delta\alpha,\delta\beta)\) 的有限乘积变分定义；`standardFactorBracket` 是自由因子的标准异号常括号。该接口没有假设实际 DLW 约化括号等于 Adler 括号，没有输入谱量对易、能量身份、守恒、最高 Fourier 系数或独立性结论。

DLW 对应在项目内证明：

\[
\alpha=U/2+hw/8,\quad\beta=U/2-hw/8,
\qquad F_\alpha=hF_U+4F_w,\quad F_\beta=hF_U-4F_w.
\]

实际源中的 \(\delta w=P_0v_w\) 对应因子投影

\[
Q(f_\alpha,f_\beta)=
\left(f_\alpha-\frac12\Pi(f_\alpha-f_\beta),
      f_\beta+\frac12\Pi(f_\alpha-f_\beta)\right).
\]

[StaticFactorVariation.lean](StaticFactorVariation.lean) 把实际源变分接到该静态自由变分；[StaticFactorTraceCotangent.lean](StaticFactorTraceCotangent.lean) 从循环迹构造真实因子余向量；[AdlerFactorCoordinates.lean](AdlerFactorCoordinates.lean) 与 [FactorProjectionAlgebra.lean](FactorProjectionAlgebra.lean) 证明配对变换、\(1/8\) 归一化、\(Q\) 自伴性和 Ward 条件下的括号修正抵消。最后 [FactorAdlerFoundation.lean](FactorAdlerFoundation.lean) 将它们组成实际 DLW 传输接口。

`ActualSpectralFoundation` 是中间接口，最终主定理使用更明确的 `FactorSpectralFoundation`。不能把旧中间接口自身当成裸标准 Adler 定理。

## 4. 实际 Hamiltonian 与实际括号

源码采用真实变分配对 \(h\sum_j\int dx\)，约化算子为

\[
J_{\mathrm{red}}=-\begin{pmatrix}0&P_0\partial_x\\P_0\partial_x&0\end{pmatrix},\qquad
\{F,H\}_{\mathrm{red}}=\langle dF,J_{\mathrm{red}}dH\rangle.
\]

[EulerVariationalGradient.lean](EulerVariationalGradient.lean) 通过周期分部积分证明实际 Euler 梯度确实表示仿射方向的普通导数。`gradientCovector` 因而是真实微分，而非为独立性任意指定的一组向量。

有限格点矩阵

\[
Q_{\rm lat}f_j=h\left(\sum_{i<j}f_i+\tfrac12f_j\right),\qquad
R=P_0Q_{\rm lat}P_0
\]

由 [LatticeResolvent.lean](LatticeResolvent.lean) 直接构造，证明所需逆差分与斜对称性质。物理泛函定义为

\[
\mathcal H_0=h\sum_j\int_0^{L_x}
\left(\frac12U_j^2w_j+\frac{h^2}{96}w_j^3+w_jU_{j,x}
+\frac12w_j(Rw_x)_j\right)dx,
\]

\[
\mathcal K=\mathcal H_0-\gamma h\sum_j\int_0^{L_x}U_jdx,
\qquad\mathcal P=h\sum_j\int_0^{L_x}p_js_jdx.
\]

第一留数通过真实低阶系数计算识别，得到无能量／留数身份前提的定理 `actualPhysicalK_eq_first_charge`：

\[
\mathcal K=-8G\mathcal C_1+\frac\gamma c\mathcal P+\kappa,
\qquad
\kappa=8G\left(\frac{G^2}{12}+B^2\right)L_x
-\frac{\gamma^2hML_x}{c}.
\]

真实时间生成元的变分与原方程连接也已证明。具体的谱量／最终族括号值均使用上述 `reducedBracketValue`。本项目没有另行构造一个涵盖任意非线性泛函类别的完整 Poisson 代数；本次结论的对易断言是这些实际泛函的明确括号等式。

## 5. 所有正整数阶的对易与普通时间守恒

正规 PDO 源的实际链式法则给出 \(d\mathcal C_n\) 与单值算子余切的对应；共同 \(U\) 规范变分给出 Ward 恒等式，随后以上已证明的 DLW 因子坐标／投影变换把标准 Adler 理论接到约化括号。

共同规范方向使用的原函数可以不周期；相应留数消去通过 `NormalScalarResidue` 的逐点标量交换子恒等式证明，没有把周期循环迹施加到该非周期原函数。

由于归一化谱余切与 \(\mathcal M\) 对易，循环迹直接消去 Adler 括号项，得到

\[
\{\mathcal C_m,\mathcal C_n\}_{\mathrm{red}}=0
\quad(m,n\ge1).
\]

空间平移不变性通过微分多项式的总导数积分证明，给出 \(\{\mathcal C_n,\mathcal P\}_{\mathrm{red}}=0\)。它没有作为外部前提。

时间守恒使用同一个实际场积分定义。真实联合光滑性给出时空混合导数交换，有限多项式 Leibniz 法则与紧周期区间积分微分给出

\[
\frac d{dt}\mathcal C_n(z(t))
=\langle d\mathcal C_n(z(t)),z_t\rangle
=\{\mathcal C_n,\mathcal K\}_{\mathrm{red}}=0.
\]

[ActualPolynomialCurveDerivative.lean](ActualPolynomialCurveDerivative.lean) 与 [ActualHamiltonianConservation.lean](ActualHamiltonianConservation.lean) 的终点是 Mathlib 的 `HasDerivAt ... 0 t`。因此最终守恒断言是普通时间导数，不只是抽象算子上的形式零留数，也没有额外的时间 PDO 表示前提。

## 6. 任意有限前缀的泛型独立性

只为构造见证，取 \(p_+=2\varepsilon f\)、\(p_-=-2\varepsilon f\)、\(s=0\)，其余格点为背景；等价地，\(U/2\) 在两格点的扰动为 \(\varepsilon f,-\varepsilon f\)。真实全阶二次系数从正规乘法／求逆的有限二阶 jet 推出，在最高微分阶块中为

\[
\bigl([\varepsilon^2]\mathcal C_{2k+1}\bigr)_{\mathrm{top}}
=\frac2M(-1)^{k+1}\int_0^{L_x}(\partial_x^kf)^2dx.
\]

该最高块独立于背景参数；有限背景下的完整二次项由真实频率多项式 \(F_k\) 表达。对不同正 Fourier 模式 \(\ell_j\) 和非零幅度 \(a_j\)，源码证明

\[
[\varepsilon^2]\mathcal C_{2k+1}
\left(z_{\varepsilon\sum_j a_j\cos(\omega_jx)}\right)
=\sum_j a_j^2F_k(\omega_j^2),\qquad
\omega_j=\frac{2\pi\ell_j}{L_x},
\]

\[
\deg F_k\le k,\qquad [\xi^k]F_k(\xi)=\frac{L_x}{M}(-1)^{k+1}\ne0.
\]

这些是 [ActualFrequencyLeading.lean](ActualFrequencyLeading.lean) 与 [ActualBalancedAmplitudeBridge.lean](ActualBalancedAmplitudeBridge.lean) 的推导结论。微分矩阵的线性幅度项为 \(2\varepsilon a_jF_i(\omega_j^2)\)，广义 Vandermonde 行列式非零。随后真实有限多项式行列式的首项给出任意小正幅度的非零见证。

在实际见证中记 \(g=\varepsilon\sum_j a_j\cos(\omega_jx)\)，故 \(p_+=2g\)、\(p_-=-2g\)、\(s=0\)。取额外的真实 \(s\) 方向 \(\delta s_+=g\)、\(\delta s_-=-g\)，则

\[
d\mathcal P(\delta s)=4h\int_0^{L_x}g^2dx\ne0,
\]

而纯 \(p\) Fourier 见证方向被 \(d\mathcal P\) 消去。因此 \(\mathcal P\) 与每个有限奇数块联合独立；再由 \(-8G\ne0\) 以 \(\mathcal K\) 替换 \(\mathcal C_1\)。

[FieldGenericity.lean](FieldGenericity.lean) 使用全体空间 jet 在 \([0,L_x]\) 上的均匀范数诱导普通 \(C^\infty\) 拓扑，源码中通过 `open scoped DLWFieldTopology` 启用。非零见证子式是连续微分多项式；沿任意场点到见证的仿射直线，它是非零实多项式，因而非零集合开且稠密。[ActualGenericIndependence.lean](ActualGenericIndependence.lean) 消去了所有 witness、minor 和目标系数假设，得到

\[
\forall N\in\mathbb N\ \exists S_N\subset\mathscr F_{c,\gamma}:
\quad S_N\text{ 开且稠密},\quad
\forall z\in S_N,
\ d\mathcal C_1(z),d\mathcal C_3(z),\ldots,d\mathcal C_{2N-1}(z)
\text{ 线性独立}.
\]

最终族的每个有限前缀亦有这样的开稠密集。此处场拓扑通过全局 \((p,s)\) 坐标给出；没有另外形式化原 \((U,w)\) 表示的拓扑同胚定理。没有证明 Baire 完备性或所有有限块同时独立的稠密可数交，这不影响本次逐有限块结论。

## 7. 真实 Lean 终点

最终结论结构的完整源码如下；其各个字段都是主定理的输出：

```lean
@@ENDSTRUCTURE@@
```

主定理：

```lean
@@ENDTHEOREM@@
```

它准确表达以下数学蕴含：在以上显式形式 PDO／循环迹／自由因子 Adler 基础成立时，对任意固定 \(M\ge2\)，

\[
\boxed{
\mathcal C_n=\frac1n\operatorname{Tr}L^n,
\quad\dot{\mathcal C}_n=0,
\quad\{\mathcal C_m,\mathcal C_n\}_{\mathrm{red}}=0
\quad(m,n\ge1).
}
\]

\[
\mathcal K=-8G\mathcal C_1+\frac\gamma c\mathcal P+\kappa,
\qquad
\boxed{\mathcal K,\ \mathcal P,\ \mathcal C_3,\ \mathcal C_5,\ldots}
\]

是包含实际物理 Hamiltonian 的两两对易守恒族；该族以及奇数谱子族的任意有限前缀分别在开稠密集上微分独立。

## 8. 可复核记录

- 最终入口：`FinalEndpoint.lean`。
- 编译器：`leanprover/lean4:v4.34.0`。
- Mathlib commit：`5ed2965256430c3649e86755f9576b54eca72435`。
- 完整本地 import closure：**@@COUNT@@ 个模块，全部 PASSED**。
- 本次记录：[result.json](.lean-runs/@@RUN@@/result.json)；逐模块诊断：[build.log](.lean-runs/@@RUN@@/build.log)。记录保存每个输入源码的 SHA-256 和对应 `.olean`。
- 检查器拒绝验证闭包中的 `sorry`、`admit`、新 `axiom`。本次入口与关键定理的 `#print axioms` 仅报告 Mathlib/Lean 的 `propext`、`Classical.choice`、`Quot.sound`。

`#print axioms` 没有自建公理不等于没有数学假设；`FactorSpectralFoundation par` 是明确的定理参数，仍须按第 3 节审阅。

复现命令：

```powershell
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\dlw_integrability_lean_20261006' `
  -File 'C:\Users\msz\aca\Workspaces\dlw_integrability_lean_20261006\FinalEndpoint.lean' `
  -TimeoutSeconds 300
```

当前定理没有包含形式 PDO 基础实例的从定义存在性证明、给定初值的全局适定性、所有有限块同时独立的 Baire 强化，或全局作用量—角变量／紧不变环面构造。后者保持为用户提出的进一步研究方向。
'''
replacements = {
    '@@DATE@@': datetime.date.today().isoformat(),
    '@@COUNT@@': str(len(result['files'])), '@@RUN@@': run_id,
    '@@STARTSTATE@@': starting_state, '@@STARTCURVE@@': starting_curve,
    '@@ENDSTRUCTURE@@': ending_structure, '@@ENDTHEOREM@@': ending_theorem,
    '@@FACTORINTERFACE@@': factor_theorem,
}
for key, value in replacements.items():
    report = report.replace(key, value)
target = project / 'LEAN_PROOF_REPORT.md'
backup = project / 'registration_before' / run_id
backup.mkdir(parents=True, exist_ok=True)
if target.exists() and not (backup / target.name).exists():
    (backup / target.name).write_bytes(target.read_bytes())
target.write_text(report, encoding='utf-8')
print(f'Wrote {target}; verified {len(result["files"])} unchanged Lean sources from {record}.')
