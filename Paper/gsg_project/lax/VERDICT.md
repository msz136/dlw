# 定论：GSG 半离散 DLW 不是强可积

> **本“定论”已撤回（2026-09-19）**：最新复核见
> `../../dlw_semidiscrete/GRAM_INTEGRABILITY_REASSESSMENT.md` §6–9。
> 本文把固定谱参数的标量比值乘积与 Möbius 映射复合混淆，未核验周期边界，
> 并把“守恒密度必须逐点常数”作为判据；这些都不能支持全系统不可积结论。
> Lean 的指定无谱矩阵乘积恒等式仍只表达其已写明的假设，不能排除其他谱表示。
> 新工作已证明纯格点 Gram 解族、物理守恒律与 Darboux 交织关系；
> 完整谱可积性尚待建立，也不能直接沿用本文对有限 h 系统“S-可积”的宣称。
> 以下正文仅作为历史记录，标题及“最终判定”不再代表当前结论。

> ⚠️ 本文件**推翻本轮早先那个"是强可积"的结论**（它错在把"谱曲线随 `z`
> 变化"当成了"守恒量"）。被推翻的论证只在会话历史与 `REPORT_LAX.md` 里，
> 本文件是最终版。
>
> **本版新增**：§6 给出 Lean 4 机器验证（`lean/DLWLaxDegenerate.lean`，
> 无 `sorry`、无新 `axiom`），把"退化"这一步变成定理，而不是数值观察。

---

## 1. 上次错在哪

我算出的 dKP 型波函数

$$
\psi_n(z)=\frac{\tau_n(\mathbf t-[z^{-1}])}{\tau_n(\mathbf t)}\Big|_{\,x\to x-1/z,\;t\to t-1/(2z^2)}
$$

确实给出非常数的 $\operatorname{tr}T(z)$。但我当时只检查了
"$c_1,c_2,c_3\neq0$"（即在**一个点**上 `z`-非常数），
**没有**检查它在流动 `(x,y,t)` 下是否不变。补做之后（`final_test.py`，80 位）：

$$
\operatorname{tr}T(z)\Big|_{z=3}
=1.11719,\ 1.08437,\ 1.11926,\ 0.80998,\ -22.6223
$$

在五个不同 `(x,y,t)` 点上——**相对散布 1.05（100%）**。$z=10,50,500$ 同样。

$$
\boxed{\ \operatorname{tr}T(z)\ \text{依赖}\ (x,y,t)\ \Longrightarrow\ \text{它不是守恒量}\ }
$$

进一步，把 $\operatorname{tr}T(z)=I_0+I_1z^{-1}+I_2z^{-2}+I_3z^{-3}$ 的系数
在五个点上求出来（`conserved.py`）：

| | $I_0$ | $I_1$ | $I_2$ | $I_3$ |
|---|---|---|---|---|
| 最小 | 0.9060 | −12.101 | 19.055 | −6219.3 |
| 最大 | 2.5354 | 41.866 | 644.63 | 8220.2 |
| **相对散布** | **0.64** | **1.29** | **0.97** | **1.76** |

**$I_k$ 全都不是守恒量。** 上一轮"$I_k$ 给出无穷守恒密度族"的说法**作废**。

---

## 2. 那个一阶 Lax 对是真的退化（这部分原来是对的）

秩一形变 $\hat\tau_n=\det(M(n)+z^{-1}uv^{\mathsf T})$ 给出

$$
\psi_n(z)=1+\frac{Q_n}{z}
\quad\text{（60 位下 } \max|\psi_n-(1+Q_n/z)|=1.2\times10^{-53}\text{，}
a_2,a_3\equiv0\text{）}
$$

Möbius ⇒ 一阶递推 ⇒（符号验证，周期 $N$）

$$
\operatorname{tr}T(z)\Big|_{\text{一阶}}=\prod_{i=0}^{N-1}(1+Q_i)-1+O(Q^2)
\quad\text{（}z\text{-无关，恒等式）}
$$

> ⚠️ **更正（本轮）**：早先写的"$\operatorname{tr}T=q_0q_1\cdots q_{N-1}+\cdots+1$"
> 是错的。精确地说（Lean `trace_z_free`）：$\operatorname{tr}T_N$ **完全不含 $z$**，
> 这是一个 `[精确]` 恒等式（对每个固定 $N$ 与每族 $Q$）。但**它的具体闭式我没有拿到**——
> 我提出过 4 个候选闭式，全被 sympy 精确符号重算推翻。所以这里不再写闭式，
> 只写可证的那件事：$z$-无关。
>
> **关键**：$z$-无关只说明"谱问题退化"，**不**说明 $\operatorname{tr}T$ 沿流动不变；
> 后者见 §3（结论：不变是不可能的，它随 $(x,y,t)$ 变）。

**这个谱问题确实是退化的、平凡的。** 但它退化是**构造**造成的，不代表整个系统。

---

## 3. 决定性证据：连续方向的谱曲线也不是流动不变量

用 dKP 型波函数（`final_test.py`）：

| $z$ | tr T 在 5 个 $(x,y,t)$ 点上 | 相对散布 |
|---|---|---|
| 3 | 1.11719, 1.08437, 1.11926, 0.80998, −22.6223 | 1.05 |
| 10 | 0.94431, 0.90439, 0.94552, 0.67141, −74.955 | 1.01 |
| 50 | 0.89949, 0.88450, 0.89979, 0.77995, 3.71557 | 0.79 |
| 500 | 0.90484, 0.90657, 0.90474, 0.91614, 2.62179 | 0.65 |

**Lax 对的谱曲线必须沿流动不变**，否则它不给出守恒量。
这里它明确随 `(x,y,t)` 变化 ⇒ **不给出守恒量族**。

（注意：`d_x ln τ_n` 也依赖 `(x,y,t)`：在两点上分别 3.8759 与 4.3096，
所以连它也不是守恒密度。DLW 的局部守恒密度确实不容易拿到。）

---

## 4. 文献的交叉印证（子代理实测报告，`dlw_laxpair_report.md`）

这一轮的文献检索**独立印证了负面结论**：

1. **DLW 是"弱 Lax 对"（weak Lax pair）可积**，不是标准意义下的强可积。
   Boiti–Leon–Pempinelli 1987 的 Lax 对含 $\partial_x^{-1}$（非局部），
   被四次独立引用为 "weak Lax pair"：
   - `u_{yt}+h_{xx}+\tfrac12(u^2)_{xy}=0,\quad h_t+(uh+u+u_{xy})_x=0`
     — [arXiv:math/9804162](https://arxiv.org/abs/math/9804162)
   - `u_{yt}+v_{xx}+\tfrac12(u^2)_{xy}=0,\quad v_t+(uv+u+u_{xy})_x=0`
     — [Hainan Univ. J. 26 (2008) 207](https://nshu.hainanu.edu.cn/cn/article/pdf/preview/10.15886/j.cnki.hdxbzkb.2008.03.001.pdf)
   - 二阶标量形式：$\psi_t-\psi_{xx}+[\partial_x^{-1}u_t-u_x+u^2]\psi=0$，
     $\psi_{xy}+u\psi_y+\tfrac12(\eta_y+u_y)\psi=0$
     — [arXiv:solv-int/9803007](https://arxiv.org/abs/solv-int/9803007) (3.12)–(3.13)

2. **DLW 在 WTC 与 ARS 两种意义下都不通过 Painlevé 检验**。原文：
   *"It is proven that the 2DDLWE system is fails in passing the Painlevé test
   both at the WTC's … and at the ARS's … meaning"*
   — [arXiv:nlin/0107027](https://arxiv.org/abs/nlin/0107027)；
   *"Though the model equation system is Lax or IST integrable, it does not pass
   the Painlevé test"* — [CTP id=9298](https://ctp.itp.ac.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=9298)。

   → **Lax/IST 可积，但不是 Painlevé 意义下的完全可积。**
   而 "Lax 可积但非 Painlevé 完全可积" 正是 **S-可积** 的典型特征，
   与我在第 1–3 节测到的"谱曲线不守恒"完全一致。

3. **DLW 的守恒密度 $\rho_k,\sigma_k$ 在任何可及文献里都没有印出**（明确负面）。
   最接近的是 Gordoa–Joshi–Pickering 的递归算子与
   $B_1=\begin{pmatrix}0&\partial_x\\ \partial_x&0\end{pmatrix}$，
   $R=B_2B_1^{-1}$，"tri-Hamiltonian" —— 但**没印密度**。

4. **离散/半离散 DLW：文献里完全没有。** Hu & Yu 2007（离散 (2+1) sinh-Gordon）
   有 Lax 对（摘要原文提到），但付费墙 + 无预印本，具体形式未取得。

---

## 5. 最终判定

| 判据 | 结果 |
|---|---|
| 秩一形变的一阶 Lax 对 | 存在，但**谱退化**（$\operatorname{tr}T_N$ 与 $\det T_N$ 都不含 $z$，Lean 已证） |
| dKP 型二阶谱问题 | 存在，$\operatorname{tr}T(z)$ 对 $z$ 非平凡 |
| `tr T(z)` 是流动不变量？ | **否**（随 `(x,y,t)` 变化，散布 ~65–105%） |
| 由它得到守恒密度族？ | **否**（$I_0..I_3$ 都随 `(x,y,t)` 变） |
| 离散方向自身的谱结构？ | **无**（$T_N$ 完全不含谱参数 ⇒ 谱曲线平凡） |
| 文献定性 | **弱 Lax 对**；**WTC/ARS 两种 Painlevé 检验均不通过** |
| 离散 DLW 的文献 | **无** |

> 注：第 2 行与第 3 行**不是**同一条证据，也**不矛盾**：第 2 行的 dKP 型波函数
> 确实给出对 $z$ 非平凡的 $\operatorname{tr}T(z)$，但第 3 行说明它不是流动不变量，
> 所以生不出守恒量。而第 1、5 行是**离散 Lax 对自身**的退化（与 dKP 那支无关）。

### 结论

$$
\boxed{\ \text{GSG 半离散 DLW \textbf{不是强可积}；它是 S-可积（Lax/IST 可积）。}\ }
$$

具体地说：

* 它有精确的**弱 Lax 对**（含 $\partial_x^{-1}$，非局部），
  以及无穷维 Kac–Moody–Virasoro / $W_\infty$ 对称代数；
* 但它**不通过 Painlevé 检验**（WTC 与 ARS 皆然），
  且**不能**从单值矩阵的谱曲线生成一族守恒密度；
* 所以它在"强/完全可积"（Liouville / Painlevé 意义）下**不成立**，
  只在"S-可积 / Lax 可积"意义下成立。

对半离散 GSG 格式本身：交错 `a∓h/2` 是一个**一致、精确可解**的离散化
（双线性结构与 $N$-孤子解保持，相互作用系数与 `h` 无关），
但它**继承的是连续 DLW 的 S-可积性，而非强可积性**；
离散方向（`n` 与 `j`）本身不产生新的谱结构或守恒量。

---

## 6. Lean 形式化：把"退化"做成机器检查的定理（本轮新增）

文件：`gsg_project/lax/lean/DLWLaxDegenerate.lean`
环境：Lean 4.34.0 / Mathlib v4.34.0；唯一合规入口是 `_lean_shared/Check-Lean.ps1`。
状态：`PASSED: 1 local module(s).`，**无 `sorry`、无 `admit`、无新 `axiom`**。

### 编码方式

谱参数用**幂零元** $\zeta$（$\zeta^2=0$）编码，系数环取 Mathlib 的
`TrivSqZeroExt ℝ ℝ`（即 $\mathbb R[\zeta]/(\zeta^2)$）：

```lean
abbrev Sq := TrivSqZeroExt ℝ ℝ
def coef (x : Sq) : ℝ := x.snd          -- coef (a + bζ) = b
def IsZFree (x : Sq) : Prop := coef x = 0   -- "x 与 z 无关"
```

这样"$x$ 与 $z$ 无关"是一个精确的代数命题，而 $\zeta\neq0$（`Zeta_ne_zero`）
保证它不是空话。

### 已证的定理（全部 `[精确]`）

| Lean 定理 | 内容 |
|---|---|
| `zf_all` | $T_N$ 的**四个矩阵元全都**与 $z$ 无关，对一切 $N$ 成立 |
| `trace_z_free` | $\operatorname{tr}T_N$（自取迹 `tr2`）与 $z$ 无关 |
| `det_formula` | $\det T_N=\prod_{i<N}(Q_i-Q_{i+1})$ |
| `det_z_free` | $\det T_N$ 与 $z$ 无关 |
| `trace_charpoly_z_free` | $\lambda^2-\operatorname{tr}(T_N)\lambda+\det(T_N)$ 的**每个系数**都与 $z$ 无关 |
| `entry_00/01/10/11` | $T_{k+1}=T_kL_k$ 的四个矩阵元递推 |
| `Lmat_trace`, `Lmat_det`, `charpoly` | $\operatorname{tr}L_n=1+Q_n$，$\det L_n=Q_n-Q_{n+1}$，一步特征多项式 $\lambda^2-(1+v)\lambda+(v-u)$ |
| `mobius_telescopes` | 一步标量递推是精确 Möbius，一个周期内望远镜抵消 |
| `mobius_composition` | Möbius 的复合仍是 Möbius |
| `no_constant_trace` | 若 $T(s_1)\neq T(s_2)$ 则不存在 $c$ 使 $T\equiv c$ |

**"谱曲线退化"的精确含义**就是 `trace_charpoly_z_free`：
$\lambda^2-\operatorname{tr}(T_N)\lambda+\det T_N$ 的系数不含谱参数
⇒ 谱曲线不随 $z$ 移动 ⇒ 没有 Floquet 带、没有离散谱层级
⇒ 从 $n$ 方向拿不到强可积性。

> 另有一个**单步**层面的观察（`charpoly`）：$\det L_n=Q_n-Q_{n+1}$ 与
> $\operatorname{tr}L_n=1+Q_n$ 导致一步判别式 $4Q_{n+1}+(1-Q_n)^2$，
> 在 `Sq` 里一般**不是**平方 ⇒ 一步问题没有固定 Floquet 乘子，
> 也**不存在**"从单步看出塌缩"的捷径。塌缩是全局（对一切 $N$）现象，
> 所以 `zf_all` 必须用对 $N$ 的归纳，而不是从一步推出来。

### 证明方法（方法学结论，值得记下）

本文件**刻意不**经过任何 $\operatorname{tr}T_k$ 的封闭公式。理由：
我先提出过 **4 个** $\operatorname{tr}T_k$ 的候选闭式，**四个全错**，
而且每一次都是被 **sympy 的精确符号重算**推翻的，**没有一次**是被"对 $Q$ 采样"发现的
（早期几个错值的来源正是用一个 $10^{-20}$ 的有限差分代 $Q$）。
所以 `zf_all` 用对四个矩阵元递推的归纳来证，归纳不变量里同时携带每个矩阵元的
"与 $z$ 无关性"**和**它的**实递推**（`raf`/`rbf`/`rcf`/`rdf`）。
定论的证明因此不依赖任何猜测的公式。

技术上必须注意：`coef` 是**导子**（derivation），不是环同态：

```lean
theorem coeff_mul (x y : Sq) : coef (x * y) = x.fst * coef y + coef x * y.fst
```

所以不变量不能只带 `IsZFree`，必须把 `fst` 部分也带上 —— 这正是证明的全部技术内容。

> 🕳️ **一个具体的坑**（记录下来以免重犯）：递推的**种子是矩阵元本身**，
> $(T_0)_{11}=1$，所以 `rdf 0 = 1` 而**不是** `0`。我一度取 `rdf 0 = 0`，
> 于是基本情形退化成假命题 `1 = 0`（在 $\mathbb R$ 上）；而 Lean 的
> `Real.decidableEq` 走 `Classical.choice`，使 `decide` 卡住、`norm_num`
> 把它化成 `False` 却收不了尾。把种子改对（`rdf 0 = 1`）之后，
> 第四个基本情形与另外三项一样由 `rfl` 收尾。**教训：形式化里出现"证不出的假命题"时，
> 第一嫌疑是建模的种子/边界条件，而不是战术技巧。**

### 未主张的内容（诚实边界）

* τ 函数输入（$Q_n=\hat\tau_n/\tau_n-1$ 来自 GSG 交错 DLW 的 Gram 行列式）是本文件的**假设**，
  正如它也是 `TodaFormalization.DLWDiscretePair` 的假设；本文件**没有**证 τ 满足双线性方程。
* 文献事实（含 $\partial_x^{-1}$ 的弱 Lax 对、WTC/ARS Painlevé 检验不通过）**没有**形式化，
  只在 §4 作为文献证据列出。
* 本形式化说的是"**这个（秩一形变）Lax 对**退化"，与 §3 的
  "dKP 型二阶问题的 $\operatorname{tr}T(z)$ 不是流动不变量"是**两条互补证据**，不是同一条。
* `det_formula` 是恒等式；"$z$-无关"用的是 $\zeta$ 编码下的 `coef`，
  对**所有** $Q:\mathbb N\to Sq$ 成立，不限于由 τ 产生的 $Q$。

### 公理审计

```
#print axioms zf_all
#print axioms trace_z_free
#print axioms det_formula
#print axioms det_z_free
#print axioms trace_charpoly_z_free
#print axioms mobius_telescopes
#print axioms no_constant_trace
```

全部只依赖 `[propext, Classical.choice, Quot.sound]` —— **没有 `sorryAx`**。

---

## 7. 复现

```powershell
# 数值与符号
cd C:\Users\msz\学术内容\Paper\gsg_project\lax
python -u final_test.py    # 判定性：tr T(z) 是否随 (x,y,t) 变（结论：变）
python -u conserved.py     # I_0..I_3 在五个点上是否守恒（结论：不守恒）
python -u probe5.py        # 秩一形变：tr T 不含 z（退化）
python -u veto.py          # 秩一 vs dKP 的 (A,B) 对 z 的依赖
python -u link.py          # 2DTL 双线性不成立，故须用 dKP 型
python -u v4.py            # tau 实现两路交叉验证

# Lean（唯一合规入口，不要用 lake）
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Paper\gsg_project\lax\lean' `
  -File 'C:\Users\msz\学术内容\Paper\gsg_project\lax\lean\DLWLaxDegenerate.lean' `
  -TimeoutSeconds 900
# 期望输出末行：PASSED: 1 local module(s).
```

---

## 8. 一句话

$$
\boxed{\ \text{没有强的（谱意义）可积结构。}\ }
$$

GSG 交错 DLW 的离散方向只给一个**退化 Lax 对**：单值矩阵 $T_N$ 完全不含谱参数
（Lean 已证 `zf_all` / `trace_z_free` / `det_z_free` / `trace_charpoly_z_free`），
谱曲线平凡，因而**没有**离散谱层级、Floquet 带或守恒量族。
系统的可积性来自连续 DLW 的**弱 Lax 对 / S-可积性**，
**不**来自它的离散结构。
