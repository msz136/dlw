"""Build a concise, executable companion to the actual periodic DLW proof.

The mathematical library is read-only. The notebook calls its completed
theorems, and checks short displayed definitions by definitional equality.
Execution and publication of the draft are separate operations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from textwrap import dedent

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROOFS = ROOT / "Workspaces" / "dlw_integrability_lean_20261006"
DESTINATION = HERE / "DLW刘维尔可积性report.ipynb"


def markdown(cell_id: str, source: str):
    return nbformat.v4.new_markdown_cell(dedent(source).strip(), id=cell_id)


def lean(cell_id: str, source: str):
    return nbformat.v4.new_code_cell(
        "%%lean " + cell_id + "\n" + dedent(source).strip() + "\n",
        id="lean-" + cell_id,
        metadata={"integrability_lean_cell": cell_id},
    )


def scoped(cell_id: str, source: str):
    name = "NotebookDLW" + cell_id.title().replace("-", "")
    return lean(cell_id,
        "import FinalEndpoint\n\nnamespace " + name + "\n"
        "noncomputable section\nopen DLWLean\n"
        "open scoped BigOperators ContDiff DLWFieldTopology\n\n"
        + dedent(source).strip() + "\n\nend\nend " + name)


def build() -> dict:
    cells = [markdown("intro", r"""
        # 一般周期 DLW 的刘维尔可积性

        从光滑周期场和 DLW 方程出发，构造全阶谱族，依次证明守恒性、对易性与有限前缀的泛型独立性。
    """)]

    cells += [markdown("load-text", """
        载入本地 Lean 环境，复用已有编译器、Mathlib 与证明库。
    """), nbformat.v4.new_code_cell(dedent("""
        from pathlib import Path
        import sys

        root = next(p for p in (Path.cwd(), *Path.cwd().parents, Path("C:/Users/msz/aca"))
                    if (p / "_lean_shared" / "runtime.json").is_file())
        sys.path.insert(0, str(root / "Workspaces" / "integrability_notebook_20261007"))
        from integrability_runtime import load_lean
        load_lean()
    """).strip(), id="python-load"), lean("library", """
        import FinalEndpoint

        #check DLWLean.StartPoint
        #check DLWLean.GlobalPDO.constructedCharge
    """)]

    cells += [markdown("conditions-text", r"""
        ## 1. 周期格点与物理场

        固定

        $$M\ge2,\qquad h>0,\qquad L_x>0,\qquad c\ne0,\qquad\gamma\in\mathbb R.$$

        格点 $j\in\mathbb Z/M\mathbb Z$ 用 `Fin par.M` 表示；空间变量 $x\in\mathbb T_{L_x}$ 用满足 $f_j(x+L_x)=f_j(x)$ 的实函数表示。时间 $t\in\mathbb R$。所有场取实值，关于空间无限光滑。

        | 符号 | 含义 |
        | --- | --- |
        | $j,x,t$ | 周期格点、空间坐标、时间 |
        | $E$ | 格点移位，$Ef_j=f_{j+1}$ |
        | $D$ | 形式 PDO 的空间微分符号 |
        | $T_j$ | 第 $j$ 个格点的一阶比值因子 |
        | $X,Y$ | Adler 接口中的形式 PDO 元素 |
        | $p,s$ | 由闭合物理场提取的全局独立坐标 |

        记格点平均与零均值投影为

        $$\Pi f=\frac1M\sum_{j=0}^{M-1}f_j,\qquad P_0f=f-\Pi f.$$

        物理场逐点满足两个闭合条件：

        $$\Pi w=c,\qquad\Pi(Uw)=\gamma.\tag{1}$$

        以下代码显示参数、周期场与闭合物理场的定义，并给出式（1）中的闭合条件。`mean_w` 与 `mean_Uw` 是物理起点的条件；`smooth` 与 `periodic` 分别表达光滑性和空间周期性。
    """), scoped("conditions", """
        #print DLWLean.FieldParameters
        #print DLWLean.SmoothPeriodicField
        #print DLWLean.PeriodicPhysicalState

        theorem fixedMeans (par : FieldParameters)
            (f : PeriodicPhysicalState par) (x : ℝ) :
            latticeMean (fun j => f.w.value j x) = par.c ∧
            latticeMean (fun j => f.U.value j x * f.w.value j x) = par.gamma :=
          ⟨f.mean_w x, f.mean_Uw x⟩

        #check fixedMeans
    """)]

    cells += [markdown("coordinates-text", r"""
        ## 2. 全局独立坐标

        取

        $$p=P_0U,\qquad s=w-c,\qquad\Pi p=\Pi s=0.$$

        闭合条件决定共同模式，因而可以从 $(p,s)$ 恢复物理场：

        $$U_j=p_j+\frac{\gamma-\Pi(ps)}c,\qquad w_j=c+s_j.\tag{2}$$

        `FieldCoordinates` 保存这两个坐标；`ClosedPeriodicPair` 是由这类零均值场对组成的线性空间，用于方向微分和括号。`U`、`w` 对应式（2），`reconstruction` 给出物理场的坐标重构。
    """), scoped("coordinates", """
        #print DLWLean.FieldCoordinates

        def U {par : FieldParameters} (z : FieldCoordinates par)
            (j : Fin par.M) (x : ℝ) : ℝ :=
          z.p.value j x +
            (par.gamma - latticeMean (fun i => z.p.value i x * z.s.value i x)) / par.c

        def w {par : FieldParameters} (z : FieldCoordinates par)
            (j : Fin par.M) (x : ℝ) : ℝ :=
          par.c + z.s.value j x

        example {par : FieldParameters} (z : FieldCoordinates par)
            (j : Fin par.M) (x : ℝ) : U z j x = z.U j x := rfl

        example {par : FieldParameters} (z : FieldCoordinates par)
            (j : Fin par.M) (x : ℝ) : w z j x = z.w j x := rfl

        theorem reconstruction {par : FieldParameters}
            (f : PeriodicPhysicalState par) (j : Fin par.M) (x : ℝ) :
            f.toCoordinates.U j x = f.U.value j x ∧
            f.toCoordinates.w j x = f.w.value j x :=
          ⟨f.reconstruct_U j x, f.reconstruct_w j x⟩

        #check reconstruction
    """)]

    cells += [markdown("start-text", r"""
        ## 3. 原方程与演化起点

        记 $E^{-1}f_j=f_{j-1}$，下标按 $M$ 循环，并定义

        $$\delta_-=\frac{I-E^{-1}}h,\qquad M_-=\frac{I+E^{-1}}2.$$

        原物理方程是

        $$\delta_-\!\left[U_t+\partial_x\!\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
        +\partial_x^2(\delta_-U+M_-w)=0,$$

        $$w_t+\partial_x(Uw)-w_{xx}=0.\tag{3}$$

        下方 `physicalDLW` 逐项对应式（3）。`deriv (fun τ => ...) t` 是时间导数；`deriv (fun y => ...) x` 是空间导数；嵌套 `deriv` 是二阶导数。`previousSite` 实现周期下标。

        `StartPoint` 给定一条满足原方程的轨迹，并要求 $p,s$ 关于 $(t,x)$ 联合无限光滑。守恒证明沿这样的给定轨迹进行。
    """), scoped("start", """
        #print DLWLean.previousSite

        def physicalDLW (par : FieldParameters)
            (z : ℝ → FieldCoordinates par) : Prop :=
          ∀ t x j,
            deltaMinus par (fun i =>
              deriv (fun τ => (z τ).U i x) t +
                deriv (fun y => ((z t).U i y) ^ 2 / 2 +
                  (par.h ^ 2 / 32) * ((z t).w i y) ^ 2) x) j +
              deriv (deriv (fun y =>
                deltaMinus par (fun i => (z t).U i y) j +
                  averageMinus par (fun i => (z t).w i y) j)) x = 0 ∧
            deriv (fun τ => (z τ).w j x) t +
              deriv (fun y => (z t).U j y * (z t).w j y) x -
                deriv (deriv ((z t).w j)) x = 0

        example (par : FieldParameters) (z : ℝ → FieldCoordinates par) :
            physicalDLW par z = PhysicalDLW par z := rfl

        #print DLWLean.StartPoint

        theorem originalEquations {par : FieldParameters} (start : StartPoint par) :
            physicalDLW par start.trajectory := start.physical_equations

        #check originalEquations
    """)]

    cells += [markdown("foundation-text", r"""
        ## 4. 形式 PDO 基础

        用 $D$ 表示形式空间微分符号，正规形式为 $X=\sum_{q\le q_0}a_qD^q$。留数取 $D^{-1}$ 的系数，迹取其周期积分：

        $$\operatorname{res}_D X=a_{-1},\qquad
        \operatorname{Tr}X=\int_0^{L_x}a_{-1}(x)\,dx,\qquad
        \operatorname{Tr}(XY)=\operatorname{Tr}(YX).\tag{4}$$

        形式 PDO 的基础结构包括：每个闭合场的兼容表示、所需逆元、循环留数迹、场的方向导数的系数源表示，以及自由一阶因子的标准 Adler 乘积／求逆规则。

        $$\mathrm{Foundation}(par)\;\Longleftrightarrow\;
        \forall z\in\mathscr F_{c,\gamma},\ \exists\text{兼容的因子谱表示}.\tag{5}$$

        `NormalPDOModel` 对应正规乘法与空间导数；`base` 汇集逆元、迹与系数源；`adlerFoundation` 对应自由因子传输；`wardFoundation` 提供共同 $U$ 方向的源表示。

        以下代码展示基础接口，`foundation.toActual` 将其转换为后续定理使用的场接口。
    """), scoped("foundation", """
        def foundation (par : FieldParameters) : Prop :=
          ∀ z : ClosedPeriodicPair par,
            Nonempty (PhysicalFactorSpectrumRepresentation par z)

        example (par : FieldParameters) :
            foundation par = FactorSpectralFoundation par := rfl

        #print DLWLean.PhysicalFactorSpectrumRepresentation
        #print DLWLean.FactorAdlerFoundation
        #check DLWLean.FactorSpectralFoundation.toActual
    """)]

    cells += [markdown("charges-text", r"""
        ## 5. 全阶守恒量的定义

        从每个格点的一阶因子构造有序乘积

        $$T_j=\left(D-\frac{U_j}{2}+\frac{hw_j}{8}\right)^{-1}
        \left(D-\frac{U_j}{2}-\frac{hw_j}{8}\right),\qquad
        \mathcal M=T_{M-1}\cdots T_0.$$

        定义归一化常数与算子

        $$G=\frac{hMc}{4}\ne0,\qquad B=\frac\gamma{2c},\qquad
        L=-G(\mathcal M-I)^{-1}+(B-G/2)I.\tag{6}$$

        第 $n$ 个谱量为

        $$\mathcal C_n(z)=\frac1n\operatorname{Tr}L(z)^n
        =\int_0^{L_x}\rho_n(z)\,dx,\qquad n\ge1.\tag{7}$$

        `periodicDensityPolynomial par n` 是通过有限系数递推得到的 $\rho_n$；每个固定 $n$ 只使用有限个空间导数。以下 `C` 给出场上的多项式积分定义，`spectralL` 对应式（6）。`traceIdentification` 给出式（7）：同一个 `rep` 同时适用于全部阶数。
    """), scoped("charges", """
        def C (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) : ℝ :=
          fieldPolynomialIntegral par (GlobalPDO.periodicDensityPolynomial par n) z

        def spectralL {par : FieldParameters} {z : ClosedPeriodicPair par}
            (rep : PhysicalSpectrumRepresentation par z) : rep.A :=
          (-par.G) • (↑rep.base.physicalNormalized.difference⁻¹ : rep.A) +
            (par.B - par.G / 2) • (1 : rep.A)

        example (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) :
            C par n z = GlobalPDO.constructedCharge par n z := rfl

        example {par : FieldParameters} {z : ClosedPeriodicPair par}
            (rep : PhysicalSpectrumRepresentation par z) : spectralL rep = rep.L := rfl

        theorem traceIdentification {par : FieldParameters} {z : ClosedPeriodicPair par}
            (rep : PhysicalSpectrumRepresentation par z) (n : ℕ) :
            C par n z = (n : ℝ)⁻¹ * rep.base.tr.toLinearMap (spectralL rep ^ n) :=
          actualCharge_eq_trace rep n

        #check traceIdentification
        #print axioms traceIdentification
    """)]

    cells += [markdown("energy-text", r"""
        ## 6. Hamiltonian 与最终族

        格点算子由有限矩阵直接构造：

        $$Q_{\mathrm{lat}}f_j=h\!\left(\sum_{i<j}f_i+\tfrac12f_j\right),\qquad
        R=P_0Q_{\mathrm{lat}}P_0.$$

        定义物理能量、时间生成元与空间平移动量：

        $$\mathcal H_0=h\sum_j\int_0^{L_x}
        \left(\frac12U_j^2w_j+\frac{h^2}{96}w_j^3+w_jU_{j,x}
        +\frac12w_j(Rw_x)_j\right)dx,$$

        $$\mathcal K=\mathcal H_0-\gamma h\sum_j\int_0^{L_x}U_jdx,
        \qquad\mathcal P=h\sum_j\int_0^{L_x}p_js_jdx.\tag{8}$$

        第一留数的系数计算给出

        $$\mathcal K=-8G\mathcal C_1+\frac\gamma c\mathcal P+\kappa,\qquad
        \kappa=8G\!\left(\frac{G^2}{12}+B^2\right)L_x-
        \frac{\gamma^2hML_x}{c}.\tag{9}$$

        最终排列为 $F_0=\mathcal K$、$F_1=\mathcal P$、$F_{n+2}=\mathcal C_{2n+3}$。`H0` 展开式（8）的密度，`F` 写出这个排列；`energyIdentity` 对应式（9）。

        $\mathcal H_0$ 与第一谱量 $\mathcal C_1$ 仿射相关；约化演化由 $\mathcal K$ 生成。独立族采用上面的排列。
    """), scoped("energy", """
        def H0 (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
          let q := closedPairCoordinates par z
          par.h * ∑ j, ∫ x in (0 : ℝ)..par.Lx,
            (q.U j x) ^ 2 * q.w j x / 2 + beta par * (q.w j x) ^ 3 / 3 +
              q.w j x * deriv (q.U j) x +
                q.w j x * latticeResolvent par (fun i => deriv (q.w i) x) j / 2

        def K (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
          H0 par z - par.gamma * (closedPairCoordinates par z).physicalUIntegral

        def P (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
          coefficientPairing par z.1 z.2

        def F (par : FieldParameters) : ℕ → ClosedPeriodicPair par → ℝ
          | 0 => actualPhysicalK par
          | 1 => coefficientMomentum par
          | n + 2 => GlobalPDO.constructedCharge par (2 * n + 3)

        example (par : FieldParameters) (z : ClosedPeriodicPair par) :
            K par z = actualPhysicalK par z := rfl

        example (par : FieldParameters) (z : ClosedPeriodicPair par) :
            P par z = coefficientMomentum par z := rfl

        example (par : FieldParameters) : F par = actualPhysicalFamily par := rfl

        theorem energyIdentity (par : FieldParameters) (z : ClosedPeriodicPair par) :
            actualPhysicalK par z = -8 * par.G * GlobalPDO.constructedCharge par 1 z +
              (par.gamma / par.c) * coefficientMomentum par z + energyConstant par :=
          actualPhysicalK_eq_first_charge par z

        #check energyIdentity
        #print axioms energyIdentity
    """)]

    cells += [markdown("bracket-text", r"""
        ## 7. 微分与约化括号

        使用变分配对

        $$\langle g,v\rangle=h\sum_j\int_0^{L_x}
        (g_{p,j}v_{p,j}+g_{s,j}v_{s,j})\,dx.$$

        约化算子和括号为

        $$J_{\mathrm{red}}=-\begin{pmatrix}0&P_0\partial_x\\P_0\partial_x&0\end{pmatrix},
        \qquad\{F,H\}_{\mathrm{red}}=\langle dF,J_{\mathrm{red}}dH\rangle.\tag{10}$$

        在零均值场上 $P_0\partial_x=\partial_x$。`J` 的两个负号和分量交换对应式（10）；`bracket` 是 `reducedBracketValue` 的原始积分配对。

        `chargeDifferential` 给出 Euler 梯度所表示的场积分方向导数：

        $$\left.\frac d{da}\mathcal C_n(z+av)\right|_{a=0}=d\mathcal C_n(z)[v].\tag{11}$$

        这里 `gradientCovector` 是泛函微分的线性形式，后续 Jacobian 使用相同对象。
    """), scoped("bracket", """
        def J (par : FieldParameters) (g : ClosedPeriodicPair par) : ClosedPeriodicPair par :=
          (-(closedSpatialDerivative par g.2), -(closedSpatialDerivative par g.1))

        def bracket (par : FieldParameters) (gF gH : ClosedPeriodicPair par) : ℝ :=
          coefficientGradientPairing par gF (J par gH)

        example (par : FieldParameters) (gF gH : ClosedPeriodicPair par) :
            bracket par gF gH = reducedBracketValue par gF gH := rfl

        theorem chargeDifferential (par : FieldParameters) (n : ℕ)
            (z v : ClosedPeriodicPair par) :
            HasDerivAt (fun a : ℝ => GlobalPDO.constructedCharge par n (z + a • v))
              (gradientCovector par (GlobalPDO.constructedChargeGradient par n z) v) 0 :=
          GlobalPDO.constructedChargeGradient_hasDerivAt par n z v

        #check chargeDifferential
    """)]

    cells += [markdown("conservation-text", r"""
        ## 8. 普通时间守恒

        原方程给出 $z_t=J_{\mathrm{red}}d\mathcal K$。时空链式法则、混合导数交换与周期积分微分于是得到

        $$\frac d{dt}\mathcal C_n(z(t))=
        \langle d\mathcal C_n(z(t)),z_t\rangle=
        \{\mathcal C_n,\mathcal K\}_{\mathrm{red}}=0,\qquad n\ge1.\tag{12}$$

        最终族同样满足

        $$\frac d{dt}F_n(z(t))=0,\qquad n\ge0.\tag{13}$$

        下方 `HasDerivAt ... 0 t` 明确表达时刻 $t$ 的普通导数为零。`familyConserved` 同时包括 $\mathcal K,\mathcal P,\mathcal C_3,\ldots$。证明库封装了式（12）中的积分微分与括号计算。
    """), scoped("conservation", """
        theorem chargeConserved (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (start : StartPoint par) (n : ℕ) (hn : 0 < n) (t : ℝ) :
            HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ)) 0 t :=
          start.actualConstructedCharge_conserved foundation.toActual n hn t

        theorem familyConserved (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (start : StartPoint par) (n : ℕ) (t : ℝ) :
            HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) 0 t :=
          start.actualPhysicalFamily_conserved foundation.toActual n t

        theorem hamiltonianConserved (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (start : StartPoint par) (t : ℝ) :
            HasDerivAt (fun τ => actualPhysicalK par (start.closedCurve τ)) 0 t :=
          start.actualPhysicalFamily_conserved foundation.toActual 0 t

        theorem momentumConserved (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (start : StartPoint par) (t : ℝ) :
            HasDerivAt (fun τ => coefficientMomentum par (start.closedCurve τ)) 0 t :=
          start.actualPhysicalFamily_conserved foundation.toActual 1 t

        #check chargeConserved
        #check familyConserved
        #check hamiltonianConserved
        #check momentumConserved
        #print axioms chargeConserved
        #print axioms familyConserved
    """)]

    cells += [markdown("involution-text", r"""
        ## 9. 两两对易

        循环迹消去 Adler 括号项，因子坐标和投影变换将其传到约化括号：

        $$\{\mathcal C_m,\mathcal C_n\}_{\mathrm{red}}=0,\qquad m,n\ge1.$$

        空间平移不变性给出 $\{\mathcal C_n,\mathcal P\}_{\mathrm{red}}=0$。结合式（9），得到

        $$\{F_m,F_n\}_{\mathrm{red}}=0,\qquad m,n\ge0.\tag{14}$$

        `spectralCommutes` 与 `familyCommutes` 分别给出两个零括号结论；`withMomentum` 显示动量这一步。所有括号都由上一节的同一个 `reducedBracketValue` 计算。
    """), scoped("involution", """
        theorem spectralCommutes (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (m n : ℕ) (z : ClosedPeriodicPair par) (hm : 0 < m) (hn : 0 < n) :
            reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
              (GlobalPDO.constructedChargeGradient par n z) = 0 :=
          actualSpectralBracket_zero par foundation.toActual m n z hm hn

        theorem withMomentum (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) :
            reducedBracketValue par (GlobalPDO.constructedChargeGradient par n z)
              (momentumGradient z) = 0 :=
          GlobalPDO.constructedCharge_bracket_momentum_zero par n z

        theorem familyCommutes (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (m n : ℕ) (z : ClosedPeriodicPair par) :
            reducedBracketValue par (actualPhysicalFamilyGradient par m z)
              (actualPhysicalFamilyGradient par n z) = 0 :=
          actualPhysicalFamily_commutes par foundation.toActual m n z

        #check spectralCommutes
        #check withMomentum
        #check familyCommutes
        #print axioms familyCommutes
    """)]

    cells += [markdown("frequency-text", r"""
        ## 10. 独立性：Fourier 最高系数

        为构造见证，在两个不同格点取平衡扰动 $p_+=2g$、$p_-=-2g$、$s=0$，其余格点的 $p$ 为零，其中

        $$g(x)=\varepsilon\sum_{j=0}^{N-1}a_j\cos(\omega_jx),\qquad
        \omega_j=\frac{2\pi\ell_j}{L_x},\qquad \ell_j>0.$$

        不同正模式的二次幅度系数写成

        $$[\varepsilon^2]\mathcal C_{2k+1}(z_{\varepsilon})
        =\sum_j a_j^2F_k(\omega_j^2),$$

        $$\deg F_k\le k,\qquad[\xi^k]F_k(\xi)
        =\frac{L_x}{M}(-1)^{k+1}\ne0.\tag{15}$$

        `actualOddFrequencyPolynomial` 是这里的 $F_k$，与最终守恒族 $F_n$ 的编号含义不同。`topCoefficient` 给出式（15）的最高系数，由正规乘法和求逆的二阶 jet 推导。
    """), scoped("frequency", """
        theorem degreeBound (par : FieldParameters) (k : ℕ) :
            (actualOddFrequencyPolynomial par k).natDegree ≤ k :=
          actualOddFrequencyPolynomial_degree par k

        theorem topCoefficient (par : FieldParameters)
            (foundation : FactorSpectralFoundation par) (k : ℕ) :
            (actualOddFrequencyPolynomial par k).coeff k =
              (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) :=
          actualOddFrequencyPolynomial_top par foundation.toActual k

        theorem topCoefficientNonzero (par : FieldParameters)
            (foundation : FactorSpectralFoundation par) (k : ℕ) :
            (actualOddFrequencyPolynomial par k).coeff k ≠ 0 :=
          actualOddFrequencyPolynomial_leading_ne_zero par foundation.toActual k

        #check degreeBound
        #check topCoefficient
        #check topCoefficientNonzero
        #print axioms topCoefficient
    """)]

    cells += [markdown("jacobian-text", r"""
        ## 11. 独立性：Jacobian 非零子式

        取 $N$ 个不同模式 $\ell_j=j+1$ 和 $a_j=1$。沿相应纯 $p$ 方向 $v_j$，定义泛函微分矩阵

        $$J_{ij}(\varepsilon)=d\mathcal C_{2i+1}(z_\varepsilon)[v_j],
        \qquad 0\le i,j<N.$$

        每个矩阵元是 $\varepsilon$ 的有限多项式，常数项为零、一次项为

        $$[\varepsilon]J_{ij}=2a_jF_i(\omega_j^2).$$

        式（15）和不同频率给出广义 Vandermonde 行列式非零；行列式的首个可能系数为

        $$[\varepsilon^N]\det J(\varepsilon)
        =\det\bigl(2a_jF_i(\omega_j^2)\bigr)\ne0.$$

        因而任意 $r>0$ 内都有见证：

        $$\exists\,0<\varepsilon<r:\quad \det J(\varepsilon)\ne0.\tag{16}$$

        这里是 $N$ 维 Fourier 切片上的 Jacobian 子式。`covectorMinor` 的 $(i,j)$ 项就是 $d\mathcal C_{2i+1}[v_j]$；非零行列式证明该子式满秩，进而证明泛函微分独立。`nonzeroJacobian` 对应式（16）。
    """), scoped("jacobian", """
        #print DLWLean.covectorMinor

        theorem nonzeroJacobian (par : FieldParameters)
            (foundation : FactorSpectralFoundation par)
            (N : ℕ) (radius : ℝ) (hradius : 0 < radius) :
            ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
              (covectorMinor (fun i : Fin N => gradientCovector par
                (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
                  (balancedMomentumState par
                    (eps • periodicCosineSumCoefficient par
                      (canonicalWitnessMode (N := N)) (fun _ => 1)))))
                (balancedFourierDirection par (canonicalWitnessMode (N := N)))).det ≠ 0 := by
          exact actualOdd_small_Fourier_minor par foundation.toActual
            canonicalWitnessMode canonicalWitnessMode_pos
            (canonicalWitnessMode_injective N) (fun _ => 1)
            (fun _ => by norm_num) radius hradius

        #check nonzeroJacobian
        #print axioms nonzeroJacobian
    """)]

    cells += [markdown("generic-text", r"""
        ## 12. 开稠密集上的微分独立

        非零见证子式是连续微分多项式。沿任意场点到见证的仿射直线，它仍是非零实多项式，因此非零集合开且稠密。在由全部空间 jet 的均匀范数给出的 $C^\infty$ 场拓扑中，

        $$\forall N\in\mathbb N\ \exists S_N\subset\mathscr F_{c,\gamma}:\quad
        S_N\text{ 开且稠密},\qquad
        d\mathcal C_1(z),d\mathcal C_3(z),\ldots,d\mathcal C_{2N-1}(z)
        \text{ 线性独立}\quad(z\in S_N).\tag{17}$$

        纯 $p$ Fourier 方向被 $d\mathcal P$ 消去。再加入 $s$ 方向 $\delta s_+=g$、$\delta s_-=-g$，则

        $$d\mathcal P[\delta s]=4h\int_0^{L_x}g^2dx\ne0.$$

        于是可以加入 $\mathcal P$，再用式（9）及 $-8G\ne0$ 将 $\mathcal C_1$ 替换为 $\mathcal K$。最终族任意有限前缀满足

        $$\forall N\ \exists S_N\text{ 开且稠密}:\quad
        dF_0(z),\ldots,dF_{N-1}(z)\text{ 线性独立}\quad(z\in S_N).\tag{18}$$

        `IsOpen`、`Dense`、`LinearIndependent ℝ` 分别对应开、稠密和实线性独立；`Fin N` 给出有限前缀。`oddGeneric` 与 `familyGeneric` 分别对应式（17）和式（18）。
    """), scoped("generic", """
        theorem oddGeneric (par : FieldParameters)
            (foundation : FactorSpectralFoundation par) (N : ℕ) :
            ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
              ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N => gradientCovector par
                (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)) :=
          actualOdd_generically_independent par foundation.toActual N

        theorem familyGeneric (par : FieldParameters)
            (foundation : FactorSpectralFoundation par) (N : ℕ) :
            ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
              ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
                gradientCovector par (actualPhysicalFamilyGradient par i.val z)) :=
          actualPhysicalFamily_generically_independent par foundation.toActual N

        #check oddGeneric
        #check familyGeneric
        #print axioms oddGeneric
        #print axioms familyGeneric
    """)]

    cells += [markdown("endpoint-text", r"""
        ## 13. 周期场可积性结论

        在显式形式 PDO／循环留数迹／自由因子 Adler 基础成立时，对任意固定 $M\ge2$，

        $$\boxed{\mathcal C_n=\frac1n\operatorname{Tr}L^n,\qquad
        \frac d{dt}\mathcal C_n=0,\qquad
        \{\mathcal C_m,\mathcal C_n\}_{\mathrm{red}}=0\quad(m,n\ge1).}$$

        包含物理 Hamiltonian 的最终族

        $$\boxed{\mathcal K,\ \mathcal P,\ \mathcal C_3,\ \mathcal C_5,\ldots}$$

        两两对易并沿原物理方程守恒；该族与奇数谱族的每个有限前缀分别在开稠密集上微分独立。以上结论一并组成 `PeriodicIntegrabilityConclusion`，`periodicIntegrability` 给出主定理：

        $$\mathrm{FactorSpectralFoundation}(par)\Longrightarrow
        \mathrm{PeriodicIntegrabilityConclusion}(par).\tag{19}$$
    """), scoped("endpoint", """
        #print DLWLean.PeriodicIntegrabilityConclusion

        theorem periodicIntegrability (par : FieldParameters)
            (foundation : FactorSpectralFoundation par) :
            PeriodicIntegrabilityConclusion par :=
          general_periodic_dlw_integrability par foundation

        #check periodicIntegrability
        #print axioms periodicIntegrability
    """), markdown("references", r"""
        数学与源码：[证明报告](../Workspaces/dlw_integrability_lean_20261006/LEAN_PROOF_REPORT.md) · [最终 Lean 入口](../Workspaces/dlw_integrability_lean_20261006/FinalEndpoint.lean)。
    """)]

    notebook = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
        "colab": {"name": DESTINATION.name},
        "integrability_report": {
            "source_report": str(PROOFS / "LEAN_PROOF_REPORT.md"),
            "source_entry": str(PROOFS / "FinalEndpoint.lean"),
            "foundation": "DLWLean.FactorSpectralFoundation",
            "result": "DLWLean.PeriodicIntegrabilityConclusion",
            "lean_magic": "integrability_runtime",
        },
    })
    nbformat.validate(notebook)
    HERE.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, DESTINATION)
    provenance = {}
    for name in ("LEAN_PROOF_REPORT.md", "FinalEndpoint.lean", "FieldCoordinates.lean", "StartPoint.lean",
                 "FactorAdlerFoundation.lean", "GlobalCoefficientRecurrence.lean", "ActualPhysicalFamily.lean",
                 "ActualHamiltonianConservation.lean", "ActualGenericIndependence.lean",
                 "ActualFrequencyLeading.lean", "PhysicalEnergyEndpoint.lean", "PhysicalBracket.lean"):
        path = PROOFS / name
        provenance[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = {
        "draft_path": str(DESTINATION),
        "code_cells": sum(c.cell_type == "code" for c in cells),
        "lean_cells": [c.metadata.integrability_lean_cell for c in cells if "integrability_lean_cell" in c.metadata],
        "markdown_cells": sum(c.cell_type == "markdown" for c in cells),
        "draft_sha256": hashlib.sha256(DESTINATION.read_bytes()).hexdigest(),
        "source_sha256": provenance,
        "executed": False,
    }
    (HERE / "build_integrability_validation.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
