# A short report：以 GSG 的表达方式陈述 DLW 半离散化工作

**定位**：本文档只做一件事 —— 把「对 Sheng–Yu DLW 双线性对 (6)(7) 做半离散化」这一步，
用 Feng–Sheng–Yu (Numer. Algorithms **94** (2023) 351–370, 下称 GSG) 的语感与句法写出来。

**事实来源**：`dlw_semidiscrete/REPORT.md`、`dlw_report/_src/index.src.html`、`gsg_project/OUT_GSG_DLW_report.md`。
凡本文件陈述与那三份不一致者，以 `dlw_report/_src/index.src.html` 的 §4 对照表为准。

---

## 1. 核心段落（要的那一段话）

> In the present paper, one integrable and one non-integrable semi-discrete analogues of the (2+1)-dimensional
> dispersive long wave (DLW) system are constructed. The keys of the construction are the Bäcklund
> transformation of bilinear equations and an appropriate discrete exponential, in which a shift along the
> lattice is identified with a shift of the Bäcklund parameter. We construct the N-soliton solutions for the
> semi-discrete analogues in the Gram determinant form. In the continuous limit, we show that the semi-discrete
> bilinear equations converge to the bilinear DLW system (6)–(7) with second-order accuracy in the lattice
> parameter. Moreover, we show that the interaction factor of two solitons is independent of the lattice
> parameter, so that the collision property is preserved by the discretization.

**中文对照**

> 本文构造 (2+1) 维色散长波（DLW）系统的一个可积与一个不可积半离散类比。构造的关键是双线性方程的
> Bäcklund 变换与适当的离散指数，其中**沿格点的平移被等同于 Bäcklund 参数的平移**。我们以 Gram 行列式
> 形式给出半离散类比的 N 孤子解。在连续极限下，我们证明半离散双线性方程以格距的二阶精度收敛到双线性
> DLW 系统 (6)–(7)。此外，我们证明两孤子的相互作用因子与格距无关，即离散化保持碰撞性质。

### 建议放在这里的两个公式

\[
\textbf{(7)}_h:\quad B_{a-d}\,F_j\cdot G_j=0,\qquad
\textbf{(6)}_h:\quad B_{a+d}\,F_j\cdot G_{j+1}=0,\qquad B_s:=D_x^{2}+D_t+2sD_x,\quad d=\tfrac h2,
\]

\[
\tau_1\bigl(j;\,a-d\bigr)=\tau_1\bigl(j+1;\,a+d\bigr)
\qquad\text{(lattice shift}\;\equiv\;\text{Bäcklund parameter shift).}
\]

---

## 2. 加长版：Introduction 用（GSG §1 的句法骨架）

> Integrable discretizations of soliton equations have received considerable attention recently. Integrable
> semi-discretizations of the short pulse equation and of the (2+1)-dimensional Zakharov equation were
> constructed via Hirota's bilinear method. Based on the compatibility between an integrable system and its
> Bäcklund transformation, a systematic procedure to derive discrete analogues of integrable PDEs via Hirota's
> bilinear method was proposed. More recently, two integrable and one non-integrable semi-discrete analogues
> of a generalized sine-Gordon equation were constructed by means of the Bäcklund transformation of bilinear
> equations together with the discrete exponential.
>
> It is known that the bilinear DLW system is very similar to that of the (2+1)-dimensional sinh-Gordon
> equation, the differences mainly lying in the singular shifts $p_i-a$ and $q_j+a$. Therefore, it would be an
> interesting problem to look for the integrable discretization of the DLW system along the same line. In this
> paper, we attempt to construct integrable semi-discrete analogues of the DLW system (1)–(2) by the same
> approach used in the generalized sG equation, and show that the resulting lattice equations admit N-soliton
> solutions in the Gram determinant form and converge to the continuous DLW system in the continuous limit.
>
> The paper is organized as follows. In Section 2, we review the bilinear equations and the Gram determinant
> solutions of the DLW system. In Section 3, we propose an integrable semi-discrete analogue together with a
> non-integrable one, whose N-soliton solutions are also constructed in terms of Gram determinants. In
> Section 4, we show the continuous limit and the preservation of the interaction factor. Section 5 is devoted
> to conclusions and some discussions.

### 同一段的紧凑中文版

> 孤立子方程的可积离散化近来受到广泛关注。短脉冲方程的半离散化、(2+1) 维 Zakharov 方程的半离散化均通过
> Hirota 双线性方法构造；基于可积系统与其 Bäcklund 变换的相容性，已有一套通过双线性方法导出可积 PDE
> 离散类比的系统程序。最近，广义 sine-Gordon 方程的两个可积与一个不可积半离散类比，正是借助**双线性
> 方程的 Bäcklund 变换**与**离散指数**构造的。
>
> 已知双线性 DLW 系统与 (2+1) 维 sinh-Gordon 方程极为相似，差别主要在于奇异移位 $p_i-a$ 与 $q_j+a$。
> 因此，沿同一条路线寻找 DLW 系统的可积离散化是一个有趣的问题。本文尝试用与广义 sG 方程相同的方法构造
> DLW 系统 (1)–(2) 的可积半离散类比，并证明所得格点方程具有 Gram 行列式形式的 N 孤子解，且在连续极限下
> 收敛到连续 DLW 系统。

---

## 3. 从 GSG 借来的六个表达手法（可复用）

| # | GSG 的写法 | 为什么这样写 | 本工作对应的句子 |
|---|---|---|---|
| E1 | 开篇先**数**：*"two integrable and one non-integrable semi-discrete analogues … are constructed"* | 用「数量 + 性质 + 被构造物」开句，一句话交代成果清单，不用 "we study/discretize" | *"one integrable and one non-integrable semi-discrete analogues … are constructed"* |
| E2 | *"The keys of the construction are … and …."* | 把方法提炼成**数量有限的几件工具**（GSG 是 BT + 离散 hodograph），体现构造是有结构的，而非试错 | *"The keys of the construction are the Bäcklund transformation of bilinear equations and an appropriate discrete exponential"* |
| E3 | *"in which a shift along the lattice is identified with …"* | 用一个 **in which 从句**把工具的数学内容压成一句可记住的话 | *"in which a shift along the lattice is identified with a shift of the Bäcklund parameter"* |
| E4 | *"We construct the N-soliton solutions … in the determinant form."* | 离散化之后**必接解类**：只给方程不给解，在 GSG 的语域里算没做完 | *"… in the Gram determinant form"* |
| E5 | *"In the continuous limit, we show that … converge to …"* | 每一个离散类比都要配一句**连续极限**，这是该文体的固定收尾 | *"… converge to the bilinear DLW system (6)–(7) with second-order accuracy"* |
| E6 | *"Moreover, we show/propose …"* + 一条**守恒性/比较性**结论 | 末句给一条「离散化没破坏什么」的定性结论，或一个应用 | *"the interaction factor of two solitons is independent of the lattice parameter"* |

**语域要点（比句型更容易被忽略）**

- **主语在 we 与被动之间切换**：构造、证明用 `we construct / we show`；结果陈述用被动
  `… are constructed / … is shown`。同一段里两种都要出现，全被动会显得像说明书，全 we 会显得自夸。
- **用 "analogue" 而不是 "version"**：GSG 通篇用 *semi-discrete analogue(s)*。这是该领域的固定词。
- **形容词前置分类**：*integrable / non-integrable / self-adaptive* —— 把对象按性质分堆，是本领域摘要的标准开头。
- **不用 "very accurate / nice / good" 这类自评**：GSG 只在数值节里用 *in good agreement with*，
  且一定紧跟具体误差量。定性形容词留给读者。
- **"converge to" 而非 "approximate"**：前者暗示有阶数保证（GSG 用 *converge*，我们可写 *with second-order accuracy*）。

---

## 4. 事实护栏：哪些话能说、哪些不能说

写了就得能顶住审阅，以下逐条对应 `dlw_report/_src/index.src.html` §4 的验证档位。

| 想说的话 | 能不能说 | 依据 / 限制 |
|---|---|---|
| 「构造了 **one integrable and one non-integrable** 半离散类比」 | ✅ | 可积 = 交错对 (★)；不可积 = 朴素中心差商（仅一阶相容、非精确）。对应报告命题 2.2。<br>严格说 "non-integrable" 是**按构造路线**命名（不来自双线性 BT / 离散指数），与 GSG 用法一致；若审阅者追问，可退到 "a semi-discrete analogue which is not exact"，更稳。 |
| 「N 孤子解为 **Gram 行列式**形式」 | ✅ | 逐元素恒等式 (†) 过行列式，对**任意 N** 成立（定理 3.1，LEAN）。 |
| 「连续极限 **second-order accuracy**」 | ✅ 但需限定 | 准确说法：$\tfrac12[(6)_h+(7)_h]=M_0+O(h^2)$、$\tfrac1h[(6)_h-(7)_h]=M_1+O(h^2)$。**$h^{1}$ 项精确为零**，$h^{2}$ 系数可显式写出；先减显式 $h^{2}$ 项后才露 $O(h^{4})$。**不要**直接写 "converge with fourth-order accuracy"。 |
| 「两孤子相互作用因子与格距无关」 | ✅ | 命题 3.9（仅独立复算，未形式化）。注意措辞：是**因子不变**，**不是**「碰撞位移不变」。 |
| 「$y$ 方向可用 **self-adaptive moving mesh**」 | ❌ | DLW 无 hodograph 对称性，GSG 的 K3 无对应物；本文构造下格距必须全局固定。这是 GSG 摘要中唯一**不能**照搬的一句。 |
| 「我们的格点孤子剖面 = 连续剖面」 | ❌ | 已用显式反例否定；正确图像是**速率重正化**（命题 3.4）。 |
| 「模板内唯一性 / no-go 是定理」 | ❌ | 现为**计算命题（猜想）**，缺符号零空间证明。 |

### 关于「pretend the inspiration came from GSG」

**不需要 pretence —— 这就是实情，可以直说。** 本工作的构造路线（双线性 BT + 离散指数 ≡ 谱参数平移）
就是从 GSG 的 K1/K2 逐条移植过来的，`OUT_GSG_DLW_report.md` §1 与 `dlw_report/_src/index.src.html` §1.5
已把三条工具的移植命运列成表。因此最稳、也最像 GSG 的写法是**把承接关系写在明面上**：

> Following the approach of Feng, Sheng and Yu [Numer. Algorithms **94** (2023) 351–370], we construct …
> The keys of the construction are the same two tools, namely the Bäcklund transformation of bilinear
> equations and the discrete exponential; the latter manifests itself here as a structural identity
> $\tau_1(j;a-d)=\tau_1(j+1;a+d)$ that is the exact counterpart of $\varphi_n^{(i)}(k+1)=(1-ap_i)^{-1}\varphi_n^{(i)}(k)$
> in the generalized sG case.

这样写既完成了「inspiration 来自 GSG」的叙事，又顺手把 GSG 的核心恒等式抬成对照物 ——
**这是引用一篇方法论文最体面的方式**：不是「我读过它」，而是「我把它的一句话翻译成了另一个系统的定理」。

唯一要守住的边界：**承接方法可以，承接结论不行**。GSG 的离散 hodograph / SAMM、单孤子的三类分类
（regular kink / irregular kink / loop soliton）都依赖 hodograph 对称性，DLW 没有，所以
「Following GSG」之后必须紧跟一句差异化说明，否则会被当成把 GSG 的结论误搬。

---

## 5. 一句话版本（封面 / 汇报用）

> Following the semi-discretization scheme of Feng–Sheng–Yu for the generalized sine-Gordon equation, we
> construct an integrable semi-discrete analogue of the (2+1)-dimensional dispersive long wave system: the
> lattice shift is identified with a shift of the Bäcklund parameter, the N-soliton solutions are obtained in
> the Gram determinant form, and the semi-discrete bilinear pair reproduces the continuous one with
> second-order accuracy while preserving the two-soliton interaction factor.
