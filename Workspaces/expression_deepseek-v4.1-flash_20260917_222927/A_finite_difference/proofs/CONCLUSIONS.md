# CONCLUSIONS — Direction A (finite differences / constrained discretisation)

每个结论按规范 §6 的九项记录。仅 `y` 被离散化；`x, t` 连续。

---

## 结论 1 — 约束先离散：中心差分的核恰为 2-周期序列（多出一个纯离散方向）

1. **数学陈述.** 设整数格点上的中心差分 $`(\mathcal{D}f)_j = f_{j+1} - f_{j-1}`$。则
   $`\ker \mathcal{D} = \{f : \mathbb{Z}\to K \mid f_{j+1} = f_{j-1}\ \forall j\}`$，即恰为
   2-周期序列。连续算子 $`\partial_y`$ 在圆周上的核只有常值函数（1 维），故
   $`\ker\mathcal{D}`$ 比连续核多出由棋盘模式 $`\alpha_j = (-1)^j`$ 张成的一维。
   等价地：全等值函数与 $`\alpha`$ 同时被打掉。
2. **对象与适用范围.** 周期网格上的中心差分算子；任意特征 $`K`$（Lean 中为 `Field K`）。
3. **假设与边界条件.** 周期边界（序列定义在 $`\mathbb{Z}`$ 上，周期 2 用于刻画核）。
   不需要光滑性假设。
4. **Lean 定理名称.** `DLW.DirA.ctrL_kernel_iff`，配合
   `DLW.DirA.ctrL_eq_zero_of_twoPeriodic`、
   `DLW.DirA.twoPeriodic_of_ctrL_eq_zero`、`DLW.DirA.ctrL`、
   `DLW.DirA.TwoPeriodic`、`DLW.DirA.TwoAntiPeriodic`、
   `DLW.DirA.twoPeriodic_of_twoAntiPeriodic`。
   棋盘模式本身的代数性质：`DLW.DirA.altTwo`、
   `DLW.DirA.altTwo_period_two`、`DLW.DirA.altTwo_shift_one`（2-反周期，即"移位改变符号"）、
   `DLW.DirA.altTwo_eq_of_mod_two_eq`、`DLW.DirA.altTwo_two_mul`、
   `DLW.DirA.altTwo_two_mul_add_one`。
5. **文件位置.** `proofs/DirA_Periodic.lean`
6. **验证命令.**
   `& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' -Root '...\A_finite_difference\proofs' -File '...\A_finite_difference\proofs\DirA_Periodic.lean' -TimeoutSeconds 600`
7. **构建结果.** 退出码 `0`，输出 `PASSED: 1 local module(s).`（无 `sorry`/`admit`/新 `axiom`）。
8. **未形式化的桥接步骤.** 本结论在整数格点上给出；把它写成 `Fin N`（$`N`$ 偶）上的有限维
   "核维度恰为 2"的推论需要 `Fin N` 索引算术（$`j+2`$ 的模运算保奇偶性）。该桥接已在
   Python 中以数值方式复核（`exp3_constraint.py`，$`N=12`$，秩 = 10，$`\dim\ker = 2`$），
   但未在 Lean 中完成。
9. **外部依赖.** Mathlib v4.34.0（`Polynomial`、`omega`、`interval_cases`）。无新公理。
10. **证据等级.** `Lean 结构验证`（核的刻划与棋盘模式代数性质为完整证明）；
    有限维维度陈述部分为 `实验验证`。

---

## 结论 2 — 中心差分的系数代数：一阶系数恰为 1，三阶亏损恰为 1/6

1. **数学陈述.** 令 $`X`$ 为移位算子、$`s = X-1`$ 为前向差分。则
   $`\tfrac{X - X^{-1}}{2} = s + \tfrac{s^3}{6} + O(s^4)`$，即残差
   $`\tfrac{X-X^{-1}}{2} - s - \tfrac{s^3}{6} \in (s^4)`$。经由 $`X = e^{h\partial_y}`$，
   这等价于 $`D_0 u = u_y + \tfrac{h^2}{6}u_{yyy} + O(h^4)`$，即一阶相容、$`h^2`$ 阶亏损 $`+1/6`$。
   此外窄三点二阶差分满足 $`X^2 - 2X + 1 = (X-1)^2`$，故"宽模板 = 一阶差分算子之平方"
   与窄三点 Laplacian 的主符号不同。
2. **对象与适用范围.** $`\mathbb{Q}[X]`$ 上的多项式恒等式；仅系数代数。
3. **假设与边界条件.** 无（纯代数）。$`X \neq 0`$ 用于清分母。
4. **Lean 定理名称.** `DLW.DirA.narrow_second_difference`
   （以及 `DLW.DirA.ctr_eq_shift_mul_fwd`，见结论 3）。
5. **文件位置.** `proofs/DirA_Periodic.lean`
6. **验证命令.** 同结论 1。
7. **构建结果.** 退出码 `0`，`PASSED: 1 local module(s).`
8. **未形式化的桥接步骤.** 清分母后的残差整除性（$`(s^4) \mid`$ 残差）与其余项
   $`+1/120`$、$`-1/180`$ 等更高阶系数，未形式化；`exp1_symbols.py` 与 `exp2_symbols.py`
   给出完整 Taylor 系数表。
9. **外部依赖.** Mathlib `Polynomial`、`ring`。
10. **证据等级.** `Lean 代数验证`（已形式化部分）/ `实验验证`（完整系数表）。

---

## 结论 3 — 半离散色散关系：V6 中的 $`\ell`$ 被格点符号 $`f=\sin(\xi)/h`$ 替换

1. **数学陈述.** 对原方程（Sheng–Yu (1)–(2)）在 $`y`$ 方向用中心差分离散、$`x,t`$ 连续，
   在常背景 $`(u_0,v_0)`$ 附近线性化，格点模 $`e^{\sigma t + ikx + i\xi j}`$ 满足

   $$`\big[\sigma + i(u_0+2a)k\big]^2 = k^4 - (v_0+2\lambda)\,\frac{k^3}{f},\qquad f=\frac{\sin\xi}{h}.`$$

   连续极限 $`\xi\to0`$（$`f\to\ell=\xi/h`$）**精确回到**共享规范中的 V6
   $`[\sigma+i(u_0+2a)k]^2 = k^4 - (v_0+2\lambda)k^3/\ell`$。故离散关系就是 V6 把
   $`\ell`$ 换成格点符号 $`f`$；交错格式则 $`f=2\sin(\xi/2)/h`$。
2. **对象与适用范围.** 半离散（仅 $`y`$ 离散）线性化问题；常背景；周期网格。
3. **假设与边界条件.** 周期边界；只做线性化（不动点邻域）。
4. **Lean 定理名称.** 未形式化（见第 8 项）。
5. **文件位置.** `experiments/exp6_mechanical.py`（权威推导）。
6. **验证命令.** `python -u exp6_mechanical.py`
7. **构建结果.** 退出码 `0`；输出 `[6] ... difference : 0` 表明连续极限与 V6 逐项相减为 0。
8. **未形式化的桥接步骤.** 从 PDE 到符号方程组、消元得色散关系这一串代数未在 Lean 中
   完成（需要把 PDE 线性化形式化，超出本轮预算）。Python 中为符号精确（SymPy），
   并对 $`s=\sin\xi/h`$ 做了显式代入。
9. **外部依赖.** SymPy 1.13.3（符号推导）。
10. **证据等级.** `实验验证`（符号精确，非浮点）。

---

## 结论 4 — 病态性不可由 $`y`$ 离散化消除：$`|\operatorname{Re}\sigma| \sim k^2`$

1. **数学陈述.** 上述关系的 $`k`$ 主导项系数恒为 $`1`$：
   $`[\sigma+i(u_0+2a)k]^2 = k^4 + O(k^3)`$，故 $`|\operatorname{Re}\sigma| = k^2(1+o(1))`$。
   因此 $`\exp(k^2 t)`$ 型增长在任何固定 $`h`$ 下都存在，半离散格式与连续问题同样
   Hadamard 病态。唯一有界的表述是限带条件：$`|k|\le K \Rightarrow`$
   $`|\operatorname{Re}\sigma| \le K^2 + |v_0+2\lambda|K^3h/(2|\sin\xi|)`$。
   该结论对中心与交错两种符号（分别 $`f=\sin\xi/h`$ 与 $`2\sin(\xi/2)/h`$）都成立，
   因为两者的 $`k^4`$ 系数都是 $`1`$。
2. **对象与适用范围.** 本节线性化色散关系的一切一致性符号。
3. **假设与边界条件.** 常背景；$`k`$ 为实数波数；$`\xi\ne0`$（$`\xi=0`$ 时 $`f=0`$ 需另论）。
4. **Lean 定理名称.** 未形式化。
5. **文件位置.** `experiments/exp4_lattice.py`（数值增长阶）、`experiments/exp6_mechanical.py`
   （符号系数）。
6. **验证命令.** `python -u exp4_lattice.py`；`python -u exp6_mechanical.py`
7. **构建结果.** 两者退出码均为 `0`；`exp4` 输出比值 $`|\operatorname{Re}\sigma|/k^2 \to 1`$
   （$`k=10^4`$ 时为 `1.00001362`）；`exp6` 输出
   `leading term in k is k^4 times the coefficient: 1`。
8. **未形式化的桥接步骤.** 与结论 3 相同。
9. **外部依赖.** NumPy / SymPy。
10. **证据等级.** `实验验证`。

---

## 结论 5 — 约束的可解性条件比连续情形严格（多一个反对称求和条件）

1. **数学陈述.** 约束 $`w = \mathcal{D}u`$ 有解 $`\iff`$ $`w`$ 同时正交于 $`\mathbf{1}`$ 与
   $`\alpha_j=(-1)^j`$：即 $`\sum_j w_j = 0`$ **且** $`\sum_j (-1)^j w_j = 0`$。
   连续情形只要求零均值。棋盘模式 $`\alpha`$ 本身是见证：$`\sum_j\alpha_j = 0`$ 但
   $`\sum_j \alpha_j^2 = N \ne 0`$，故 $`\alpha \notin \operatorname{ran}\mathcal{D}`$。
   `exp3` 还确认（数值）$`\operatorname{ran}\mathcal{D}`$ 的余维数为 2，且
   $`\alpha`$ 作为精确对称性只在 $`u|_{\text{odd}} = v|_{\text{odd}} = 0`$ 上成立 ——
   这一"额外对称性"猜测被**否定**（见结论 6）。
2. **对象与适用范围.** $`N`$ 为偶数的周期网格；中心差分约束。
3. **假设与边界条件.** 周期边界。
4. **Lean 定理名称.** 部分：`DLW.DirA.altTwo_shift_one`（$`\alpha`$ 的 2-反周期性，
   是"反对称权重打掉 $`\operatorname{ran}\mathcal{D}`$"的代数内核）；
   `DLW.DirA.twoPeriodic_of_twoAntiPeriodic`。完整的"同时正交"刻划未形式化。
5. **文件位置.** `experiments/exp3_constraint.py`；`proofs/DirA_Periodic.lean`
6. **验证命令.** `python -u exp3_constraint.py`
7. **构建结果.** 退出码 `0`；输出 `ran D = { w : sum_j w_j = 0 and sum_j alpha_j w_j = 0 }, codimension 2`
   与 `|w - D lstsq(D,w)| = 1.0000 != 0 -> w not in ran D`。
8. **未形式化的桥接步骤.** "正交条件充分"（余维数 2）在 Lean 中未证明；Python 用
   `lstsq` 残差验证。有限维上的秩-零化度论证未形式化。
9. **外部依赖.** NumPy。
10. **证据等级.** `Lean 代数验证`（$`\alpha`$ 的性质）+ `实验验证`（可解性条件与余维数）。

---

## 结论 6 — 被否定的猜测：棋盘模式不构成半离散演化系统的额外零模

1. **数学陈述.** 尽管 $`\alpha \in \ker\mathcal{D}`$，把 $`u \mapsto u + c\alpha`$（$`w=\mathcal{D}u`$
   随之不变）代入半离散通量并不保持残差：精确地
   $`\Delta r_1 = c\,\alpha\cdot w`$，$`\Delta r_2 = c(\alpha\cdot v + 2\lambda\alpha)`$。
   两式同时对一切 $`c`$ 消失要求 $`w`$ 与 $`v`$ 在奇位点为零，而 $`\alpha\cdot w = 0`$
   在周期网格上又迫使 $`u`$ 为常值 —— 即只剩连续核。故棋盘方向**不是**额外对称性，
   也不是演化方程的额外零模；真正的离散缺陷只在**约束**中。
2. **对象与适用范围.** 周期网格 $`N`$ 偶；半离散通量（舍去 $`x`$ 导数，因线性且与 $`y`$ 离散化交换）。
3. **假设与边界条件.** 周期边界；$`w=\mathcal{D}u`$ 保持。
4. **Lean 定理名称.** 未形式化（负数结果，纯代数但涉及具体格式）。
5. **文件位置.** `experiments/exp3_constraint.py`（§[c]）。
6. **验证命令.** `python -u exp3_constraint.py`
7. **构建结果.** 退出码 `0`；输出 `|dr1 - c*alpha*w| = 1.07e-13`、
   `|dr2 - c*(alpha*v + 2*lam*alpha)| = 1.69e-14`，以及
   `the only state killing both increments is u = const`。
8. **未形式化的桥接步骤.** 上述两个闭式未在 Lean 中证明（`Fin N` 索引算术是主要障碍）。
9. **外部依赖.** NumPy。
10. **证据等级.** `实验验证`（数值精确到机器精度，且两个闭式已推导）。

---

## 结论 7 — 奈奎斯特模式的额外伪核（中心差分在 $`\xi=\pi`$ 处符号为零）

1. **数学陈述.** 中心差分符号 $`f=\sin\xi/h`$ 在 $`\xi=\pi`$ 处**恰为零**，对应棋盘模式
   $`j\mapsto(-1)^j`$，在连续问题中没有原像（$`\ell=\pi/h`$ 不是连续波数）。
   在此模态色散关系退化为 $`[\sigma+i(u_0+2a)k]^2 = k^4 + O(k^3)`$，即
   $`|\operatorname{Re}\sigma| = k^2`$ 对一切 $`k`$ 成立，且 $`k^3/f`$ 项奇异。
   交错格式在 $`\xi=\pi`$ 处 $`f = 2/h \ne 0`$，全频带无零点，故无此退化。
   （注：方向 C 已 Lean 验证 P1 一致质量 FEM 符号在 $`\ell h=\pi`$ 同样为零。）
2. **对象与适用范围.** $`y`$ 离散化的两种候选符号（中心 / 交错）。
3. **假设与边界条件.** 周期网格；$`0<\xi\le\pi`$。
4. **Lean 定理名称.** 未形式化（三角恒等式在 `exp2_symbols.py` / `exp4_lattice.py` 中验证）。
5. **文件位置.** `experiments/exp2_symbols.py` §[4]；`experiments/exp4_lattice.py` §[T4]。
6. **验证命令.** `python -u exp2_symbols.py`；`python -u exp4_lattice.py`
7. **构建结果.** 均退出码 `0`；输出 `Nyquist xi = pi : f_ctr = 0    f_sg = 2/h`。
   处理方式：交错格式据此被选为唯一在整个频带上无伪核的候选；中心格式必须在
   限带 $`|\xi| \le \pi - \delta`$ 下使用，并额外剔除棋盘分量。
8. **未形式化的桥接步骤.** `f` 的三角定义在 Lean 中未引入（Mathlib 三角函数可用，但
   与本轮预算冲突）。
9. **外部依赖.** SymPy / NumPy。
10. **证据等级.** `实验验证`。

---

## 结论 8 — 一步算子恒等式（SBP 骨架）

1. **数学陈述.** 对任意 $`f:\mathbb{Z}\to K'`$、$`j\in\mathbb{Z}`$：
   $`(f_{j+1}-f_j) + (f_{j+2}-f_{j+1}) = f_{j+2}-f_j`$。这是 $`2D_0 = (I+P)D_+`$ 的去分母形式。
2. **对象与适用范围.** 任意环 $`K'`$。
3. **假设与边界条件.** 无。
4. **Lean 定理名称.** `DLW.DirA.ctr_eq_shift_mul_fwd`、`DLW.DirA.alt_anticommutes`。
5. **文件位置.** `proofs/DirA_Periodic.lean`
6. **验证命令.** 同结论 1。
7. **构建结果.** 退出码 `0`，`PASSED: 1 local module(s).`
8. **未形式化的桥接步骤.** 完整的离散 SBP（$`\sum f\,\mathcal{D}g = -\sum \mathcal{D}f\,g`$
   在周期网格上）未形式化；共享模块 `proofs/Common/Operators.lean` 已在 `Int → K`
   上提供 `sbp_fwd`、`telescoping`、`sum_range_ctr` 等，本轮未复用。
9. **外部依赖.** Mathlib。
10. **证据等级.** `Lean 代数验证`。

---

## 路线状态与证明覆盖度（诚实标注）

- **路线状态**：`已建立候选构造（离散化方案）`，但核心病态性为**不可消除的障碍**
  （不是工具阻塞）。中心差分方案存在 $`\xi=\pi`$ 的额外伪核，交错方案在整个频带上无伪核，
  但两者都保留 $`k^4`$ 主导项，故 `|\operatorname{Re}\sigma|\sim k^2` 无法消除。
- **证明覆盖度**：`Lean 结构验证` 用于"中心差分核 = 2-周期序列"与棋盘模式代数性质、
  `Lean 代数验证` 用于一步算子恒等式与窄二阶差分恒等式；其余（色散关系、可解性条件、
  奈奎斯特退化、病态性、棋盘非对称性）为 `实验验证`。
  **尚无任何结论达到 `Lean 分析验证` 或 `数学证明，尚未完整形式化`。**

## 最有价值的下一步（单一）

在 Lean 中完成"约束可解性条件"的**充分性**：证明
$`\operatorname{ran}\mathcal{D} = \{w \mid \sum_j w_j = 0 \wedge \sum_j (-1)^j w_j = 0\}`$
（$`N`$ 偶，`Fin N`），或将结论 1 从整数格点搬到 `Fin N` 并给出 $`\dim\ker\mathcal{D}=2`$。
这需要突破 `Fin N` 的索引算术（$`j+2`$ 模 $`N`$ 保奇偶性），是当前唯一的 Lean 瓶颈。
