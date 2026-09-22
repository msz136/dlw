# 方向 H 结论编号记录（CONCLUSIONS）

运行：`expression_deepseek-v4.1-flash_20260917_222927` / 方向 H
模块：`proofs/DirH.lean`（+ `proofs/Common/Operators.lean`，只读共享）
审计：`proofs/AuditH.lean`
证据等级标签**严格取自** `common/SHARED_MATH_SPEC.md` §6：
`实验验证` / `Lean 代数验证` / `Lean 结构验证` / `Lean 分析验证` / `数学证明，尚未完整形式化`。

---

## H-1 — (10) 对 $N=1$ 无条件成立

- **数学陈述**：对 Sheng–Yu Gram 数据 (11)–(15) 在 $N=1$ 的取值，
  $\mathbf{P}\,\tau_{n+1}\cdot\tau_n\equiv0$ 对任意 $(p,q,a)$（$p\ne a,\ q\ne -a,\ p+q\ne0$）成立；
  特别地 (10) **不**迫使 $p+q+2a=0$。
- **对象与适用范围**：$N=1$，$c\in\{0,1\}$，$\lambda=-2$，$a=2$（数值），$(p,q)$ 见下。
- **假设与边界条件**：$p\ne a$（否则 $\xi_i$ 奇异）、$q\ne-a$、$p+q\ne0$（否则矩阵元奇异）。
- **外部依赖**：SymPy 1.13.3。
- **验证命令**：见 `VERIFY.md` 第 3 节 `verify_symbolic_spine.py`（检查 `H1a`、`H1c`）。
- **构建结果**：`PASSED: all Direction H symbolic checks.`，exit 0。
- **未形式化的桥接步骤**：由数值/符号多点验证推广到"任意 $(p,q,a)$"未在 Lean 中形式化；
  网格为 $(p,q)\in\{(1,3),(1,-5),(2,-6)\}\times c\in\{0,1\}\times n\in\{0,1\}$。
- **证据等级**：`实验验证`

## H-2 — (10) 对 $N=2$ 对角约束参数成立

- **数学陈述**：$N=2$、$q_j=-p_j-2a$、$c_j=1$ 时 $\mathbf{P}\,\tau_{n+1}\cdot\tau_n\equiv0$ 精确成立。
- **对象与适用范围**：$N=2$，$(p_1,p_2)=(1,3)$，$(q_1,q_2)=(-5,-7)$ 及 $(2,-6)$ 对，$a=2$，$n\in\{0,1\}$。
- **假设与边界条件**：对角约束 $p_i+q_i+2a=0$；$c_j=1$。
- **外部依赖**：SymPy 1.13.3。
- **验证命令**：`verify_symbolic_spine.py`（检查 `H1b`）。
- **构建结果**：`PASSED`，exit 0。
- **未形式化的桥接步骤**：一般 $(p_i,q_i,c_i)$ 的 $N\ge2$ 情形未验证。
- **证据等级**：`实验验证`

## H-3 — 逐指数 Hirota 符号恒等式

- **数学陈述**：$\mathbf{P}$ 作用于 $e^{Ax+Bt}\cdot e^{Cx+Et}$ 得该乘积乘
  $(A+C)^2+(E-B)+2a(A+C)$；在色散数据 $B=-A^2,\ E=C^2$ 下等于 $(A+C)(A+C+2a)$。
- **对象与适用范围**：单个指数对；算子约定 = `common/MAIN_verify_core.py` 的 `Bop`。
- **假设与边界条件**：算子固定为 $D_x^2+D_t+2aD_x$（三项正号）。
- **外部依赖**：SymPy 1.13.3；权威实现 `Bop`。
- **验证命令**：见 `report.md` 第 3 节步骤 1 的复算记录；完整形式见 `verify_symbolic_spine.py` 的 `bilinear`/`Bop`。
- **构建结果**：精确恒等（差为零）。
- **未形式化的桥接步骤**：**Lean 形式化未完成**。本环境 Lean 工具链无法闭合对应的 `ring` 目标
  （目标 `(A+C)^2 + (C^2 - -A^2) + 2a(A+C) = (A+C)(A+C+2a)` 中 `ring`/`ring_nf` 均失败，
  `linear_combination`/`nlinarith` 未导入）。因此该恒等式已从 `DirH.lean` **撤出**，以免留下失败构建。
- **证据等级**：`数学证明，尚未完整形式化`

## H-4 — 行缩放的行列式代数

- **数学陈述**：$\det(R\cdot M)=R_1R_2\det M$，其中 $R$ 为对角行缩放。
- **对象与适用范围**：任意交换环 $K$ 上的 $2\times2$ 矩阵。
- **假设与边界条件**：无（域公理即可）。
- **Lean 定理名称**：`DLW.DirH.det_two_scaling`（含列缩放的一般式）、`DLW.DirH.det_two_row_scaling`
- **文件位置**：`proofs/DirH.lean`
- **验证命令**：见 `VERIFY.md` 第 2 节。
- **构建结果**：exit 0，`PASSED: 2 local module(s).`
- **未形式化的桥接步骤**：无。
- **证据等级**：`Lean 代数验证`
- **公理审计**：`[propext, Quot.sound]`

## H-5 — 水平比值是模数常数

- **数学陈述**：$\tau$ 的水平比值 $\prod_i R_i=\prod_i\bigl(-\frac{p_i-a}{q_i+a}\bigr)$ 只含参数，不含 $x,y,t$。
- **对象与适用范围**：Gram 数据的行常数定义；$2\times2$ 情形显式记录。
- **假设与边界条件**：$q_i+a\ne0$。
- **Lean 定理名称**：`DLW.DirH.tau_ratio_is_modulus`；定义 `DLW.DirH.rowConst`
- **文件位置**：`proofs/DirH.lean`
- **构建结果**：exit 0。
- **未形式化的桥接步骤**：一般 $N$ 的 $\prod_{i=1}^N$ 形式未形式化（仅 $N=2$）。
- **证据等级**：`Lean 代数验证`
- **公理审计**：`[propext, Quot.sound]`

## H-6 — 几何族三-项关系

- **数学陈述**：若 $T(n+1)=K_cT(n)\ \forall n\in\mathbb Z$，则 $T(n+1)T(n-1)=T(n)^2$。
- **对象与适用范围**：任意域 $K$，$\mathbb Z$-指标族。
- **假设与边界条件**：几何族假设（`LevelFamily`）。
- **Lean 定理名称**：`DLW.DirH.levelFamily_three_term`；结构 `DLW.DirH.LevelFamily`
- **文件位置**：`proofs/DirH.lean`
- **构建结果**：exit 0。
- **未形式化的桥接步骤**：无。
- **证据等级**：`Lean 代数验证`
- **公理审计**：`[propext, Quot.sound]`
- **备注**：本次会话**更正**了先前的错误陈述 $T(n+1)T(n-1)=K_c^2T(n)^2$（该式为假）；
  否证已由 `verify_symbolic_spine.py` 的 `H3a2` 固定（残差 $K_c^2T_0^2(1-K_c^2)$）。

## H-7 — 链指标 Toda 场恒为 1

- **数学陈述**：$W_n=\dfrac{T(n+1)T(n-1)}{T(n)^2}\equiv1$（$T(n)\ne0$）。
- **对象与适用范围**：几何族；涵义是链指标上无非线性动力学。
- **假设与边界条件**：$T(n)\ne0$。
- **Lean 定理名称**：`DLW.DirH.todaGap_eq_one`；定义 `DLW.DirH.todaGap`
- **文件位置**：`proofs/DirH.lean`
- **构建结果**：exit 0。
- **未形式化的桥接步骤**：无。
- **证据等级**：`Lean 代数验证`
- **公理审计**：`[propext, Classical.choice, Quot.sound]`（`Classical.choice` 来自 `div_self` 路径，
  仍属标准三公理，无用户公理）

## H-8 — 常数 tau 比使诱导场恒零

- **数学陈述**：若 $\tau_{n+1}=K_c\tau_n$ 且一阶 jet 满足 $D_1=K_cD_0$，则
  $D_1V_0-V_1D_0=0$；除法形式 $\dfrac{D_1V_0-V_1D_0}{V_0V_1}=0$。
- **对象与适用范围**：任意域；DLW 中 $u=2\partial_x\ln(\tau_{n+1}/\tau_n)$。
- **假设与边界条件**：$V_0\ne0,\ V_1\ne0$（除法形式）。
- **Lean 定理名称**：`DLW.DirH.logDeriv_eq_zero`、`DLW.DirH.logDeriv_eq_zero_ratio`
- **文件位置**：`proofs/DirH.lean`
- **构建结果**：exit 0。
- **未形式化的桥接步骤**：从 jet 恒等式到"$u\equiv0$ 在 $x,y,t$ 全空间"需要把 jet 论证
  逐点粘贴，未形式化（属标准微积分桥接）。
- **证据等级**：`Lean 代数验证`
- **公理审计**：`[propext, Quot.sound]`

## H-9 — 纯粹孤子扇区秩一退化

- **数学陈述**：$c_j\equiv0$ 时 $m_{ij}^{(n)}=e^{\xi_i}e^{\eta_j}R_i^{\,n}/(p_i+q_j)$ 为秩一，
  故 $N\ge2$ 时 $\tau_n\equiv0$。
- **对象与适用范围**：Gram 数据 (11)–(15)，$c_j=0$。
- **假设与边界条件**：$p_i+q_j\ne0$。
- **外部依赖**：SymPy 1.13.3。
- **验证命令**：`verify_symbolic_spine.py`（检查 `H2b`）。
- **构建结果**：`PASSED`，exit 0。
- **未形式化的桥接步骤**：一般 $N$ 的秩一性未形式化（Lean 中仅有 $2\times2$ 的行列式代数）。
- **证据等级**：`实验验证`

## H-10 — $c_j\ne0$ 时行缩放失败（$n$ 不可当作 $y$-格点）

- **数学陈述**：含对角项 $c_j\delta_{ij}$ 的 $2\times2$ Gram 子式**不**满足
  $\det M^{(n+1)}=R_1R_2\det M^{(n)}$，除非 $R_1R_2=1$。精确残差：

  $$-R_1R_2c_1c_2-R_1R_2c_1r_2s_2-R_1R_2c_2r_1s_1+R_1c_2r_1s_1+R_2c_1r_2s_2+c_1c_2 .$$
- **对象与适用范围**：Gram 数据；结论是"把链指标 $n$ 读作 Toda 格点指标"的**显式失败条件**。
- **假设与边界条件**：$c_j\ne0$。
- **外部依赖**：SymPy 1.13.3。
- **验证命令**：`verify_symbolic_spine.py`（检查 `H2c`，断言残差非零）。
- **构建结果**：`PASSED`，exit 0。
- **未形式化的桥接步骤**：一般 $N$ 的残差形式未给出。
- **证据等级**：`实验验证`

## H-11 — 高精度数值证据

- **数学陈述**：$\mathbf{P}\tau_{n+1}\cdot\tau_n$ 的残差在 60 位精度下为 $\sim10^{-18}$–$10^{-23}$；
  诱导 $(u,v)$ 非平凡且满足 (1)–(2)。
- **对象与适用范围**：$N=1,2$；$a=2$；generic 与 constrained 参数。
- **假设与边界条件**：$p_i\ne a$。
- **外部依赖**：mpmath（`mp.dps=60`）。
- **验证命令**：`experiments/num_mkp_check.py`（见 `VERIFY.md` 第 3 节）。
- **构建结果**：exit 0。
- **未形式化的桥接步骤**：数值 → 精确陈述的推广。
- **证据等级**：`实验验证`
- **备注**：本次会话由此**否证**了本人早先的假设"约束 $p_i+q_i+2a=0$ 迫使 $u\equiv0$"：
  在 $N=1$ 约束情形下 $u=-7.2678\ldots\ne0$。

## H-12 — 逐指数符号恒等式的 Lean 形式化

- **数学陈述**：同 H-3。
- **状态**：**未完成**。
- **原因**：本环境 Lean 工具链不能闭合该 `ring` 目标（详见 `VERIFY.md` 第 4 节技术说明）。
  该恒等式已从 `proofs/DirH.lean` 撤出，以保证构建通过。
- **证据等级**：`数学证明，尚未完整形式化`

## H-13 — 完整连续极限恢复 (1)–(2)

- **数学陈述**：$y$-半离散格距与 $n$-连续化同时取极限时恢复 (1)–(2)。
- **状态**：**未完成**。本轮只完成水平比值是模数常数这一部分（H-5）。
- **证据等级**：`数学证明，尚未完整形式化`

---

## 总览

| 等级 | 条目 |
|---|---|
| `Lean 代数验证` | H-4, H-5, H-6, H-7, H-8 |
| `实验验证` | H-1, H-2, H-9, H-10, H-11 |
| `数学证明，尚未完整形式化` | H-3, H-12, H-13 |
| `Lean 结构验证` | —（本轮无） |
| `Lean 分析验证` | —（本轮无；分析性结论已按项目标准结论引用，非本轮所证） |
