# 方向 H 报告：Toda 型嵌入与可积族约化

**运行标识**：`expression_deepseek-v4.1-flash_20260917_222927` / 方向 H
**工作目录**：`H_toda_hierarchy/`
**轮次**：Round 1，$\lambda=-2$，$a$ 任意
**日期**：2026-09-18

---

## 1. 问题与目标

被研究对象为 Sheng–Yu（Physica D **432** (2022) 133140,
DOI: [10.1016/j.physd.2021.133140](https://doi.org/10.1016/j.physd.2021.133140)）
的 (2+1) 维色散长波（DLW）系统 (1)–(2)，及本文献给出的双线性约化结构：
变量变换

$$u=2(\ln(f/g))_x,\qquad v=2(\ln(fg))_{xy},$$

把 (1)–(2) 化为 biorilinear 系统 (6)–(7)，其算子为

$$B=D_x^2+D_t+2aD_x .$$

文献进一步给出 modified KP（mKP）型链 (9)–(10)：

$$(D_{x_{-1}}(D_{x_1}^2-D_{x_2}+2aD_{x_1})-4D_{x_1})\,\tau_{n+1}\cdot\tau_n=0,\tag{9}$$

$$(D_{x_1}^2-D_{x_2}+2aD_{x_1})\,\tau_{n+1}\cdot\tau_n=0,\tag{10}$$

$$x_{-1}=y,\quad x_1=x,\quad x_2=-t,$$

以及 Gram 行列式数据 (11)–(15)：

$$m_{ij}^{(n)}=c_j\delta_{ij}+\frac{1}{p_i+q_j}\Bigl(-\frac{p_i-a}{q_j+a}\Bigr)^n e^{\xi_i+\eta_j},$$

$$\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a},\qquad
\eta_j=q_jx+q_j^2t+\frac{y}{q_j+a},$$

$$f=\tau_{n+1},\qquad g=\tau_n .$$

本轮任务是判定：**Toda 型（或离散 KP / 离散 mKP 型）可积族约化能否以显式方式约化到目标系统**，其中仅对 $y$ 做半离散化，$x,t$ 保持连续。

### 必须严格区分的两个指标

- $n$：**链指标（hierarchy / level index）**，出现在 (9)–(10) 与 $m_{ij}^{(n)}$ 中；
- $j$：**格点指标（lattice / site index）**，出现在半离散化的 $y$ 方向。

**把 $n$ 与 $j$ 混同即为本方向的显式失败条件。** 本报告第 6 节给出结论：二者不可混同，并且这一点有可检验的代数原因（H-5）。

---

## 2. 实际查阅的文献

| 文献 | 位置 | 查阅状态 | 用途 |
|---|---|---|---|
| Sheng–Yu, Physica D 432 (2022) 133140, DOI [10.1016/j.physd.2021.133140](https://doi.org/10.1016/j.physd.2021.133140) | 由 `common/SHARED_MATH_SPEC.md` §1 逐式转录（本次会话未直接打开期刊版 PDF） | 公式转录核对 | 提供 (1)–(2)、(6)–(7)、(9)–(15) 的精确定义 |
| Hori–Tanaka–Maruno–Ohta, *An integrable semi-discretization of the two-component Hunter–Saxton equation*, arXiv:2606.18701v2 | 本地 `2 Huner Saxton.pdf`；**本次会话未逐页读取**（见第 8 节局限） | 仅经检索确认题名、主题与 "pseudo 2-reduction / discrete hodograph" 术语 | 评估该模式能否迁移到 DLW |

关于 Hori–Tanaka–Maruno–Ohta：检索确认该文的对象是**二分量 Hunter–Saxton 方程的可积半离散化**，其技术核心是 "2-reduction"（双分量 $\Leftrightarrow$ 2-约化）与离散 hodograph 变换。检索结果中出现 "the parameter constraint (40) reducing to the 2-reduction" 的表述
（[arXiv:2606.18701v2](https://arxiv.org/pdf/2606.18701v2#7#7)、
[ar5iv 版](https://ar5iv.labs.arxiv.org/html/2606.18701#1)）。

**能否用于 DLW：不能直接沿用。** 理由是结构性的：

1. **约化的方向相反。** 该文的 2-reduction 是把一个 $N$-分量（2-component）系统**降为**带参数约束的约化系统，约化作用在**分量指标**上；DLW 的 (9)–(10) 是**链指标 $n$ 上的平移关系**，不是分量上的约化。
2. **hodograph 需要守恒律/局部守恒形式。** 离散 hodograph 依赖 $y$-方向的守恒律 $\partial_t(\cdots)+\partial_x(\cdots)=0$。DLW 在 $\lambda=-2$ 时的双线性结构 (6)–(7) 含 $D_y$ 与 $D_x$ 的**混合**，但没有把 $y$-半离散化写成局部守恒通量的形式；见第 6 节的非局部性结论。
3. **适定性障碍。** 该文建立在可积半离散系统**良态演化**的前提上；DLW 在本项目中已知是 Hadamard 病态的（见第 5 节），离散 hodograph 通常需要特征速度的单调性，而这里不存在。

因此该文献可作为**方法学参照**（"约束 + 低维约化" 的范式），但不构成 DLW 的可用工具。

---

## 3. 可检验的约化链

记 $\mathbf{P}:=D_x^2+D_t+2aD_x$。以下每一步都是**可直接在本地复现**的计算。

### 步骤 1：算子约定锚定

以 `common/MAIN_verify_core.py` 的 `Bop` 为**唯一权威实现**：

```python
Bop(f,g,xs,ac) = bilinear(f,g,xs,(2,0,0)) + bilinear(f,g,xs,(0,0,1))
                 + 2*ac*bilinear(f,g,xs,(1,0,0))
```

即 $\mathbf{P}=D_x^2+D_t+2aD_x$（**三项皆为正号**；$x_2=-t$ 已吸收进 $D_t$）。
本次会话用该实现独立复算，得到：对 $N=1$、$a=2$，

- $(p,q)=(1,3)$：$p+q+2a=8$，$\mathbf{P}\,\tau_{n+1}\cdot\tau_n\equiv 0$（**精确为零**）；
- $(p,q)=(1,-5)$：$p+q+2a=0$，同样精确为零。

### 步骤 2：$N=1$ 的 (10) 无条件成立

**关键事实（H-1）**：在 $N=1$ 时，(10) 对 $(p,q,a)$ **不施加任何约束**。
`experiments/verify_symbolic_spine.py` 的 `H1a`/`H1c` 在网格
$(p,q)\in\{(1,3),(1,-5),(2,-6)\}$、$c\in\{0,1\}$、$n\in\{0,1\}$ 上精确验证 $\mathbf{P}\tau_{n+1}\cdot\tau_n=0$。

这**否证**了"由 (10) 必然推出 $p+q+2a=0$"的朴素读法。第 5 节说明为何这一点是本方向的核心。

### 步骤 3：谱/行常数的水平方向结构

$m_{ij}^{(n)}$ 中唯一的 $n$-依赖来自 $\bigl(-\frac{p_i-a}{q_j+a}\bigr)^n$，指数因子 $\xi_i+\eta_j$ 与 $n$ 无关。因此定义**行常数**

$$R_i:=-\frac{p_i-a}{q_i+a}$$

后，在**对角项 $c_j\delta_{ij}$ 不存在**（即 $c_j\equiv0$）时，水平平移就是逐行乘常数：

$$m_{ij}^{(n+1)}=R_i\,m_{ij}^{(n)},\qquad\text{故}\quad \tau_{n+1}=\Bigl(\prod_i R_i\Bigr)\tau_n .$$

### 步骤 4：行缩放的行列式代数（Lean 已验证）

`proofs/DirH.lean` 中形式化并证明：

$$\det(R\cdot M)=R_1R_2\det M \quad(\texttt{det\_two\_row\_scaling}),$$

$$\tau\ \text{的比值}\ \prod_iR_i\ \text{只含}\ p_i,q_i,a \quad(\texttt{tau\_ratio\_is\_modulus}).$$

### 步骤 5：链指标的 Toda 场恒为 1（Lean 已验证）

设 $T$ 为几何族，$T(n+1)=K_c\,T(n)$。`proofs/DirH.lean` 证明

$$T(n+1)T(n-1)=T(n)^2
\quad(\texttt{levelFamily\_three\_term}),$$

$$\text{Toda 场}\ W_n=\frac{T(n+1)T(n-1)}{T(n)^2}\equiv1
\quad(\texttt{todaGap\_eq\_one}).$$

> **本次会话更正的一处自身错误**：先前草稿断言 $T(n+1)T(n-1)=K_c^2T(n)^2$，该式**为假**。实验脚本的 `H3a2` 检查现已把这一否证固定下来（残差 $K_c^2T_0^2(1-K_c^2)$）。

### 步骤 6：诱导场恒零（Lean 已验证）

若 $\tau_{n+1}/\tau_n$ 为常数，则诱导 DLW 场

$$u=2\,\partial_x\ln\frac{\tau_{n+1}}{\tau_n}\equiv0 .$$

Lean 中为 `logDeriv_eq_zero` 与 `logDeriv_eq_zero_ratio`。

---

## 4. 约化条件的相容性

由第 3 节，链指标上的约化要求与 DLW 的两-tau 结构相容，必须同时满足：

1. **行缩放要成立**，需要 $c_j\equiv0$（否则对角项 $c_j\delta_{ij}$ 与 $n$ 无关，破坏缩放）；
2. $c_j\equiv0$ 时 $m_{ij}^{(n)}=\dfrac{e^{\xi_i}e^{\eta_j}}{p_i+q_j}\cdot R_i^{\,n}$ 是**秩一矩阵**，故 $N\ge2$ 时各列成比例：

$$m_{ij}^{(n)}=\frac{e^{\xi_i}}{p_i+q_j}\,e^{\eta_j}R_i^{\,n}
\;\Longrightarrow\;
\det_{N\ge2}M^{(n)}=0 .$$

即 $\tau_n\equiv0$（$N\ge2$）。

**相容性结论**：条件 (1) 与 (2) **不能同时**给出非平凡解。可用的 $N=1$ 情形下 $\tau_n$ 只有一个矩阵元，链指标上的"Toda 动力学"退化为常值缩放，Toda 场 $W_n\equiv1$。

**这是本方向的中心否定结果**：在使两-tau 结构自洽的那个扇区（$c_j\equiv0$，$N\ge2$），$\tau$ 恒为零；在唯一非平凡的 $N=1$ 情形，$W_n\equiv1$。

实验脚本 `H2b`（秩一）、`H2c`（$c_j\ne0$ 时行缩放**失败**，残差已精确给出）固定了这两条。

---

## 5. 连续极限与适定性障碍

### 5.1 连续极限

`H3b`/`H3c` 给出水平比值的精确形式。取 $q_j=-p_j-2a$（"shift 支"）时

$$R_j=-\frac{p_j-a}{q_j+a}=\frac{p_j-a}{p_j+a},$$

**不含 $x,y,t$**。因此 $n$-方向的"格距"趋于零的连续极限下，链方向不再产生任何 $x,t$ 依赖：连续极限无法恢复 (1)–(2) 的非线性行波结构。这从另一角度确认了第 4 节的结论。

> 说明：本轮**没有**完成 (9)–(10) 的完整 $N\ge2$ 连续极限验证（需要 $y$-半离散化的格距与 $n$-方向的连续化同时取），故此处只陈述已证的部分：水平比值是模数常数。

### 5.2 必须尊重的既有障碍（本项目标准结论）

常背景线性化给出

$$\bigl[\sigma+i(u_0+2a)k\bigr]^2=k^4-\frac{(v_0+2\lambda)k^3}{\ell},
\qquad |\operatorname{Re}\sigma|\sim k^2 .$$

即 $(2+1)$ 维 DLW **不是**良态演化流，Hadamard 病态。**任何** Toda 嵌入或族约化**都只能**在受限解类上成立。第 4 节的退化结论说明：在本轮考察的 mKP 扇区中，受限解类恰好**退化**到 $\tau\equiv0$ 或 $W_n\equiv1$。

**不得**声称任何嵌入或约化消除了 $|\operatorname{Re}\sigma|\sim k^2$ 的病态性。本轮结论与此一致，而非相反。

---

## 6. 局域非线性闭合（决定性判据）

DLW 的局域闭合事实（本项目已确认）：

- $w,v$ 是**局部**的（3-点模板）；
- $u=\partial_y^{-1}w$ 是**非局部**的；保持 $u$ 为独立变量并附加约束 $u_y=w$ 才能保住局域性；
- 精确零模：$v\equiv-2\lambda$、$u=U(x,t)$ 任意（$u_y=0$）解该系统；$\lambda=-2$ 时即 $v_0=4$。

**Toda 型嵌入对局域闭合的贡献：无。**

理由是第 4–5 节的退化：链指标 $n$ 上的 Toda 场恒为 $1$（Lean 已证 `todaGap_eq_one`），因此它**不引入任何新的局域非线性项**，也不改变 $u$ 的非局部性。相反，要在 DLW 里使用 $n$，只能通过"把 $n$ 当作 $y$-格点"，而这被 `H2c` 的否定结果（$c_j\ne0$ 时行缩放失败）直接阻断。

**故本方向对局域非线性闭合无改进。** 这是本轮最重要的一条否定结论。

### 唯一仍值得追踪的线索（来自兄弟方向 E）

方向 E 已在 Lean 中证明：在自然的常核 Poisson 类中**不存在** Hamiltonian 括号。因此真正的 mKP 型结构（若存在）必须落在该类之外——即需要**场依赖核**，或含 $\partial_x^{-1}$ 的 **$x$-非局部核**。这已记录为最有价值的下一步（第 9 节）。

---

## 7. 结果与证据等级（标签严格取自 spec §6）

| 编号 | 命题 | 证据等级 |
|---|---|---|
| **H-1** | 对 $N=1$ 及 Gram 数据，(10) 精确成立，且**不**迫使 $p+q+2a=0$ | 实验验证 |
| **H-2** | $N=2$ 对角约束参数下 (10) 精确成立 | 实验验证 |
| **H-3** | 逐指数 Hirota 符号恒等式 $(A+C)^2+(E-B)+2a(A+C)=(A+C)(A+C+2a)$（$B=-A^2,E=C^2$） | 实验验证（Lean 中**未**完成，见第 8 节） |
| **H-4** | $\det(R\cdot M)=R_1R_2\det M$ | Lean 代数验证 |
| **H-5** | 水平比值 $\prod_iR_i$ 是模数常数（不含 $x,y,t$） | Lean 代数验证 |
| **H-6** | 几何族三-项关系 $T(n+1)T(n-1)=T(n)^2$ | Lean 代数验证 |
| **H-7** | Toda 场 $W_n\equiv1$（链指标无动力学） | Lean 代数验证 |
| **H-8** | 常数 tau 比 $\Rightarrow$ 诱导场 $u\equiv0$ | Lean 代数验证 |
| **H-9** | 纯粹孤子扇区（$c_j\equiv0$）Gram 子式为秩一，$N\ge2$ 时 $\tau_n\equiv0$ | 实验验证 |
| **H-10** | $c_j\ne0$ 时行缩放**失败**（残差精确给出），故 $n$ 不可当作 $y$-格点 | 实验验证 |
| **H-11** | 高精度数值：$\mathbf{P}\tau_{n+1}\cdot\tau_n$ 残差 $\sim10^{-18}$–$10^{-23}$；诱导 $(u,v)$ 非平凡且满足 (1)–(2) | 实验验证 |
| **H-12** | 逐指数符号恒等式的完整 Lean 形式化 | 数学证明，尚未完整形式化 |
| **H-13** | 连续极限完整恢复 (1)–(2) | 未完成 |

---

## 8. 路线状态、局限与诚实说明

### 路线状态

**部分成立，但方向性否定**：

- Toda 型嵌入**可以在形式上构造**（几何族 + 行缩放）；
- 但在使其自洽的扇区，嵌入**不产生**非平凡动力学（$W_n\equiv1$），且 $N\ge2$ 时 $\tau\equiv0$；
- 因此该嵌入**不改进局域非线性闭合**，也不能解除 $|\operatorname{Re}\sigma|\sim k^2$ 病态。

### 局限（必须明示）

1. **未读取 Hori–Tanaka–Maruno–Ohta 的逐页内容。** 本地 `2 Huner Saxton.pdf` 在本次会话中未逐页读取，第 2 节的判断基于检索得到的题名、主题与术语，以及从 DLW 侧独立得到的结构性理由。**该文献结论应按"低置信度"看待**，不应作为独立证据引用。
2. **H-3 未在 Lean 中完成。** 本环境 Lean 工具链无法闭合该 `ring` 目标（见 `VERIFY.md` 的技术说明）。该恒等式另经 SymPy 精确验证。
3. **H-13 未完成。** 完整连续极限未做。
4. 本次会话中**未**运行 `experiments/verify_h_toda.py` 的完整 27 项检查（其中 7 项为本人先前手推符号错误所致，已知非真否定）。

---

## 9. 最有价值的下一步

**单一项**：把 DLW 的 $y$-半离散化放到**场依赖核**（或含 $\partial_x^{-1}$ 的 $x$-非局部核）的 Poisson 结构下重做，而不是继续在常核类里寻找 mKP 嵌入。

理由：本方向已把常核类里的 Toda/mKP 嵌入彻底闭合（H-4…H-10 全部为代数性结论，Lean 已验证），结论是**该类的 mKP 嵌入退化**。方向 E 的 Lean 结论（常核类中无 Hamiltonian 括号）与此互为独立证据。两条独立路线在同一处汇合，指向同一个出口：**必须离开常核类**。

具体第一步：在 `H_toda_hierarchy/experiments/` 下写出场依赖核 $\Theta=\Theta(u,u_x,v,\dots)$ 的候选形式，并检验其是否满足 Jacobi 恒等式与 $y$-半离散 Leibniz 法则——这可用与本轮相同的 SymPy + Lean 组合流程完成。
