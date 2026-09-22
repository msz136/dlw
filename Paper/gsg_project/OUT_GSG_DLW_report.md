# 将 GSG 半离散化方法移植到 DLW 双线性系统 (6)(7)

> ### ⚠ 修订说明（后加，请先读）
>
> 本文件已被 `../dlw_semidiscrete/REPORT.md` **修订并补全**。以下三处结论有误，
> 请以新报告为准：
>
> 1. **§3.3(c)「对称二点恒等式」$B_af_{j+1}\cdot g_j+B_af_j\cdot g_{j+1}=0$ 不成立**
>    （除 $N=1$ 外）。旧的 `code/obstruction.py`、`code/verify_nullvec.py` 只在
>    `DLW(1, …)`（即 $N=1$）上搜索与验证，而 $N=1$ 的 $\tau$ 只有两项，其零空间
>    高度退化，会产生大量伪恒等式。正确的一般性版本是
>    $B_af_{j+1}\cdot g_j+B_af_j\cdot g_{j+1}-2B_af\cdot g=0$（连续情形）。
> 2. **`code/mshift.py` 的「格点单孤子剖面 = 连续剖面在 $a\to a-h/2$」为误**。
>    正确结论是 **速率重正化**：连续指数中的
>    $y(1/P+1/Q)$ 被替换为 $j\ln\lambda$，即
>    $1/P\mapsto\Lambda_h(P)=(1/h)\ln\lambda(P)$。代入 $a\to a-h/2$ 会使分母
>    $QS-Pe$ 变成 $(Q-d)S-(P+d)e$，与格点结果不符。
> 3. 新报告补充了旧报告 §8.3 的第 1 项（半离散非线性 DLW 系统）、
>    唯一性/no-go 定理、格点色散关系与二阶精度的完整验证。
>
> 旧的交错对结论（§4.2/4.3）、$(\dagger)$ 结构恒等式、二点形式均**成立**，
> 已在 `../dlw_semidiscrete/` 中用**独立重写**的引擎复核。

**任务**：以 Feng–Sheng–Yu 对广义 sine-Gordon 方程 (GSG) 的半离散化方法为蓝本，对
Sheng–Yu 的 (2+1) 维色散长波 (DLW) 系统（*Physica D* **432** (2022) 133140）的双线性方程 (6)(7)
做离散化；给出离散化后双线性方程的形式，并分析格点上的孤立子结构。

所有结论均由 `gsg_project/code/` 下的精确符号–数值引擎独立验证（对称不变量已经在
连续情形 `N = 1,…,6`、格点情形 `N = 1,…,5` 上验证）。文中标注 **[精确]** 者为代数恒等式，
**[精确验证]** 者为在有限个一般有理点上的精确零检验（对有理函数而言这已充分）。

---

## 0. 记号

$$
B_s \;=\; D_x^2 + D_t + 2s\,D_x ,\qquad
D_x^mD_y^nD_t^p\,f\cdot g
=(\partial_x-\partial_{x'})^m(\partial_y-\partial_{y'})(\partial_t-\partial_{t'})^{p}
\,f(x,y,t)g(x',y',t')\big|_{\ast}
$$

DLW 双线性系统（原文 (5)–(7)，取 $\lambda=-2$）：

$$
\text{(6)}:\quad \big[D_y\big(D_x^2+D_t+2aD_x\big)+2\lambda D_x\big]f\cdot g=0 ,
\qquad
\text{(7)}:\quad \big(D_x^2+D_t+2aD_x\big)f\cdot g=0 ,
$$

$$
u=2\big(\ln\tfrac fg\big)_x,\qquad v=2(\ln fg)_{xy},
\qquad f=\tau_{n+1},\ g=\tau_n .
$$

Gram 型 $\tau$ 函数（原文 (13)–(15)）：

$$
m^{(n)}_{ik}=c_k\delta_{ik}+\frac1{p_i+q_k}
\Big(-\frac{p_i-a}{q_k+a}\Big)^{n}e^{\xi_i+\eta_k},
$$
$$
\xi_i=p_ix-p_i^2t+\frac{y}{p_i-a}+\xi_{i0},\qquad
\eta_k=q_kx+q_k^2t+\frac{y}{q_k+a}+\eta_{k0}.
$$

以下恒记

$$
P_i:=p_i-a,\qquad Q_k:=q_k+a,\qquad d:=\tfrac h2 .
$$

---

## 1. GSG 方法的内核（从原文 §2–§4 提炼）

GSG 对广义 sine-Gordon 的半离散化由三件工具构成：

| 编号 | 工具 | 数学形式 |
|---|---|---|
| **K1** | **双线性方程的 Bäcklund 变换**：把连续的 $D_\tau D_y f\cdot f=\tfrac12(f^2-\bar f^2)$ 写成位势变量 $f,g$（或 $\tau_n,\tau_{n+1}$）的 Bäcklund 对 | (3.3): $(2D_\tau-1)f_k\cdot g_k+\bar f_k\bar g_k=0$ |
| **K2** | **"离散指数"**：连续平面波 $e^{p_ix_1}$ 换成格点指数 | (Prop. 2) $\varphi^{(i)}_n(k)=p_i^{\,n}(1-ap_i)^{-k}e^{\xi_i}$ |
| **K3** | **离散 hodograph / 自适应网格**：由 $\tau$ 函数定义网格步长 | (3.28) $\delta_k=2a\cos\frac{\varphi_{k+1}+\varphi_k}{2},\ x=\sum_k\delta_k$ |

其要害是 **K2 的实质不是一个"离散指数函数"，而是"格点平移 $\equiv$ 谱参数平移"**：
$\varphi_n^{(i)}(k+1)=(1-ap_i)^{-1}\varphi^{(i)}_n(k)$，正是这一恒等式使
$k\to k+1$ 与 $p_i\to$ 谱参数平移等价，从而半离散方程能保持可积性（(3.8)–(3.13)）。

**关键观察**：DLW 的 $\tau$ 是 **Gram 行列式**，格点上可以做的自然操作正是"把格点平移写成行–列秩一乘子"。因此 **K2 对 DLW 有直接对应物**（见 §4 的恒等式 (4.1)），而 **(7) 天然是"格点逐点方程"，(6) 天然是"两点/格点差分方程"**，与 GSG 中 (3.12)（逐点）与 (3.8)（格点）的分工完全同构。**K3 则没有对应物**（见 §7）。

---

## 2. 连续基线（回归基准）**[精确验证]**

对 Gram $\tau$ 直接计算，取 $f=\tau_{n+1}$、$g=\tau_n$：

```
N = 1,…,6 :  (7)  B_a f·g = 0                                -> 恒为零
             (6)  @λ=-2   D_yB_a f·g − 4 D_x f·g = 0         -> 恒为零
             (6)  @一般 λ : D_yB_a f·g + 2λ D_x f·g ≠ 0       -> 非零（λ=−2 才成立）
```

并用到两条恒等式 **[精确]**：

$$
D_yB\,f\cdot g = B\,f_y\cdot g - B\,f\cdot g_y ,
\qquad
\text{(6)}\big|_{\lambda=-2}\ \Longleftrightarrow\ B\,f\cdot g_y+2D_xf\cdot g=0
\ \ \text{（在 (7) 成立时）}.
$$

---

## 3. 直接移植（K2 字面搬用）及其**精确障碍**

### 3.1 字面搬用

把 $y$ 方向离散：取格点 $j$，$y\mapsto jh$，并把 $e^{y/P_i}$ 换成 GSG 式离散指数

$$
\boxed{\ \frac1{P_i}\ \longrightarrow\ \Lambda_h(P_i):=\frac1h\ln\frac{P_i+\frac h2}{P_i-\frac h2},
\qquad
e^{y/P_i}\ \longrightarrow\ \Big(\frac{P_i+\frac h2}{P_i-\frac h2}\Big)^{j}\ }
\tag{3.1}
$$

显然 $\Lambda_h(z)=\dfrac1z+\dfrac{h^2}{12z^3}+\dfrac{h^4}{80z^5}+O(h^6)$。相应地格点乘子为

$$
\chi_{ik}=\lambda_i\mu_k,\qquad
\lambda_i=\frac{P_i+\frac h2}{P_i-\frac h2},\quad
\mu_k=\frac{Q_k+\frac h2}{Q_k-\frac h2}
\qquad(\text{秩一！})
\tag{3.2}
$$

（另两种自然取法：GSG 原样的 $\lambda_i=\big(1-\frac h{P_i}\big)^{-1}$（"exp"型），
以及 $\lambda_i=\frac{P_i+h}{P_i}$（"expneg"型）。下面三者一并检验。）

### 3.2 结果一：**(7) 在格点上是精确的** **[精确验证，N = 1,2,3；三种乘子]**

$$
B_a\,f_j\cdot g_j\equiv 0\qquad \forall j .
\tag{3.3}
$$

**原因**（也是本问题最重要的结构事实）：$\chi_{ik}=\lambda_i\mu_k$ 是**秩一**乘子，故
$\tau(j)$ 的第 $i$ 行只被 $\lambda_i^{\,j}$ 整体缩放、第 $k$ 列只被 $\mu_k^{\,j}$ 整体缩放。
对 $N=1$，若 $f_j=c+A_1E\chi^j,\ g_j=c+A_0E\chi^j$，则

$$
B_af_j\cdot g_j=2c(p+q)E\chi^j\big(A_0P+A_1Q\big)=0
\quad\text{因}\quad A_0=\frac1{p+q},\ A_1=-\frac{P}{Q(p+q)} ,
$$

即 (7) 的成立**完全不依赖 $y$ 的具体形式**——这正是 (7) 与 $y$ 的相位无关的原因。

### 3.3 结果二：**(6) 无法以两点格点方程精确闭合**

> **⚠ 本节 (c) 的"对称二点恒等式"结论已作废**（仅为 $N=1$ 假象），
> 且"模板穷举"只覆盖了特定的 6 类组合。
> 完整、正确的搜索见 `../dlw_semidiscrete/nosearch.py` 与
> `../dlw_semidiscrete/REPORT.md` §6：在 24 维二点模板中，交错对 $(\star)$ 恰为**全部**
> 精确解空间，而均匀类中除 (7) 之外**不存在**任何精确格点恒等式。
> 本节 (a)(b) 的 $O(h)$ 相容性结论仍然正确。

**(a) $N=1$ 的封闭形式** **[精确]**。取 $\chi=\lambda\mu$，

$$
\frac1h\big[B_af_{j+1}\cdot g_j-B_af_j\cdot g_{j+1}\big]-4D_xf_j\cdot g_j
=4c\,\chi^{j}E\;\Delta,\qquad
\Delta=P\,\frac{1-\chi}{h}+\frac{p+q}{Q}.
\tag{3.4}
$$

$$
\Delta=
\begin{cases}
-\dfrac{h\big(p^2+pq+q^2+a^2-ap+aq-h(p+q)\big)}{Q\,(P-h)(Q-h)}, &\chi=\big(1-\tfrac hP\big)^{-1}\big(1-\tfrac hQ\big)^{-1}\\[3mm]
-\dfrac{h(p+q)\big(2p+2q-h\big)}{Q\,(2P-h)(2Q-h)}, &\chi=\Big(\dfrac{P+\frac h2}{P-\frac h2}\Big)\Big(\dfrac{Q+\frac h2}{Q-\frac h2}\Big)
\end{cases}
$$

$\Delta$ 恒为 $h\times$(非零有理函数)，即**只是 $O(h)$ 相容**，而不是精确格点恒等式。
（物理原因：两点差分 $(1-\chi)/h=-\big(\tfrac1P+\tfrac1Q\big)+O(h)$，而精确的格点导数
$\ln\chi/h$ 才有 $O(h^2)$ 精度；两者相差 $O(h)$。）

**(b) 模板穷举** **[精确验证]**。对如下 6 类模板

| # | 模板 |
|---|---|
| 1 | $\frac1h\big[Bf_{j+1}\cdot g_j-Bf_j\cdot g_{j+1}\big]-4D_xf_j\cdot g_j$ |
| 2 | 后向差分 $\frac1h\big[Bf_j\cdot g_{j-1}-Bf_{j-1}\cdot g_j\big]-4D_xf_j\cdot g_j$ |
| 3 | 中心三点 $\frac1{2h}\big[Bf_{j+1}\cdot g_{j-1}-Bf_{j-1}\cdot g_{j+1}\big]-4D_xf_j\cdot g_j$ |
| 4 | $\frac1{2h}\big[Bf_{j+1}\cdot g_j-Bf_{j-1}\cdot g_j\big]-4D_xf_j\cdot g_j$ |
| 5 | $\frac1{2h}\big[Bf_{j+1}\cdot g_j-Bf_j\cdot g_{j+1}+Bf_j\cdot g_{j-1}-Bf_{j-1}\cdot g_j\big]-4D_xf_j\cdot g_j$ |
| 6 | 交错参数 $\frac1h\big[B_{a+\frac h2}f_j\cdot g_{j+1}-B_{a-\frac h2}f_j\cdot g_j\big]-4D_xf_j\cdot g_j$ |

在 $\chi\in\{\text{exp},\text{expneg},\text{sym}\}$、$N=1,2$ 上 **全部非零**。

**(c) 系数未知的广义线性搜索** **[⚠ 本小节结论已作废，见下]**

> **⚠ 作废**：本小节的自变量向量 $\{Bf_{j+1}\cdot g_j,\ Bf_j\cdot g_{j+1},\ \dots\}$
> 中，$f=\tau_1$、$g=\tau_0$ 都取**同一个系数参数**（即未做交错），且搜索与"新点复核"
> 只在 $N=1$（旧 `code/obstruction.py`、`code/verify_nullvec.py` 中的 `DLW(1,…)`）上进行。
> $N=1$ 的 $\tau$ 只有两项，其零空间高度退化，因此这里列出的两个"恒成立的零向量"
> **都不是一般 $N$ 的恒等式**：$Bf_{j+1}\cdot g_j+Bf_j\cdot g_{j+1}$ 在 $N\ge2$ 时非零
> （`../dlw_semidiscrete/certify.py` §H，$N=2$：no）。
> 正确的陈述见 `../dlw_semidiscrete/nosearch.py`（24 维模板、$N=1..5$ 求交）
> 与 `../dlw_semidiscrete/REPORT.md` §6。以下内容仅作历史记录保留。

Ansatz

$$
\alpha\,Bf_{j+1}\cdot g_j+\beta\,Bf_j\cdot g_{j+1}+\gamma\,Bf_j\cdot g_j
+\delta\,D_xf_j\cdot g_j+\varepsilon\,D_xf_{j+1}\cdot g_j+\zeta\,D_xf_j\cdot g_{j+1}
+\eta\,D_xf_{j+1}\cdot g_{j+1}+\theta\,D_x^2f_{j+1}\cdot g_{j+1}=0,
$$

其中系数只允许依赖 $a,h$（**不得依赖 $p_i,q_k$**）。经新点复核后真正恒成立的零向量只有两类：

$$
(\alpha,\beta,\gamma,\dots)=(1,1,0,\dots)\quad\text{与}\quad(0,0,1,0,\dots),
$$

即

$$
\boxed{\ Bf_{j+1}\cdot g_j+Bf_j\cdot g_{j+1}=0\ }\quad\text{（对称两点恒等式）}
\qquad\text{和}\qquad
Bf_j\cdot g_j=0 .
$$

- 第一个（对称两点恒等式）的连续极限是 $2Bf\cdot g+O(h^2)$，即 **(7) 的冗余格点副本**，
  而不是离散 (6)；
- $Bf_j\cdot g_j=0$ 就是**(7) 本身**；
- **反对称方向 $\alpha=-\beta\ne0$（即"离散 $D_y$"方向）不在零空间中**。

（搜索中出现的其余"零向量"经 12 个新随机点复核全部为有限取样造成的伪解，已剔除。）

> **结论（精确障碍）**：**(6) 不存在形如两点差分、且系数不依赖谱参数的精确格点类比。**
> 这不是某个模板的缺陷，而是结构性的：由 (3.4) 的 $\Delta\equiv O(h)$ 可看出，
> 任何两点差分都只能给出 $O(h)$ 相容的离散 (6)。

---

## 4. GSG 意义上的**正确**移植：谱参数平移格点

### 4.1 关键恒等式（DLW 版的"离散指数"）**[精确，N = 1,2,3,4]**

定义格点乘子 $\lambda_{ik}=\dfrac{(P_i+\frac h2)(Q_k+\frac h2)}{(P_i-\frac h2)(Q_k-\frac h2)}$
（**注意用基参数 $a$ 的 $P_i,Q_k$**），并令

$$
G_j=\det\Big[\delta_{ik}+\frac{e^{\xi_i+\eta_k}}{p_i+q_k}\,\lambda_{ik}^{\,j}\Big],
\qquad
F_j=\det\Big[\delta_{ik}-\frac{P_i+\frac h2}{Q_k-\frac h2}\,
\frac{e^{\xi_i+\eta_k}}{p_i+q_k}\,\lambda_{ik}^{\,j}\Big].
\tag{4.1}
$$

把"$\tau_1$ 取 Bäcklund 参数 $s$、格点 $j$"记作 $T_s(j)$，则

$$
\boxed{\;
T_{a+\frac h2}(j+1)\;=\;T_{a-\frac h2}(j)\;=\;F_j
\;}
\qquad\text{（逐元素恒等，故行列式恒等）}
\tag{4.2}
$$

**证明（逐元素）**：

$$
-\frac{P_i-\tfrac h2}{Q_k+\tfrac h2}\lambda_{ik}
=-\frac{P_i-\tfrac h2}{Q_k+\tfrac h2}\cdot
\frac{(P_i+\tfrac h2)(Q_k+\tfrac h2)}{(P_i-\tfrac h2)(Q_k-\tfrac h2)}
=-\frac{P_i+\tfrac h2}{Q_k-\tfrac h2}.
$$

这正是 GSG 中 $\varphi^{(i)}_n(k+1)=(1-ap_i)^{-1}\varphi^{(i)}_n(k)$ 的 DLW 对应物：
**"格点平移一格 $\iff$ 谱参数平移 $h$"**。

### 4.2 离散化后的双线性方程（最终形式）

由 (4.2)，取 $B_s=D_x^2+D_t+2sD_x$，

$$
\boxed{
\begin{aligned}
\textbf{(7)}_h:\quad & \Big(D_x^2+D_t+2\big(a-\tfrac h2\big)D_x\Big)F_j\cdot G_j=0,\\[2mm]
\textbf{(6)}_h:\quad & \Big(D_x^2+D_t+2\big(a+\tfrac h2\big)D_x\Big)F_j\cdot G_{j+1}=0 .
\end{aligned}}
\tag{4.3}
$$

等价写法（全部在一个格点 $j$ 上，用 (4.2) 把 $G_{j+1}$ 换成 $T_{a+\frac h2}(j+1)$）：

$$
T_{a-\frac h2}(j)\ \text{满足参数 }a-\tfrac h2\text{ 的 (7)},\qquad
T_{a+\frac h2}(j)\ \text{满足参数 }a+\tfrac h2\text{ 的 (7)} .
$$

或写成差分形式（便于与连续 (6) 对照）：

$$
\underbrace{\tfrac12\big[\textbf{(6)}_h+\textbf{(7)}_h\big]=0}_{\textstyle \longrightarrow\ \text{(7)}},
\qquad
\underbrace{\tfrac1h\big[\textbf{(6)}_h-\textbf{(7)}_h\big]=0}_{\textstyle \longrightarrow\ \text{(6)}\big|_{\lambda=-2}} .
\tag{4.4}
$$

**验证** **[精确验证]**：

```
N = 1,2,3,4,5 :  (7)_h = 0  -> 恒成立
                 (6)_h = 0  -> 恒成立
```

**解读**：$F_j$ 位于 $y=(j+\tfrac12)h$，$G_j$ 位于 $y=jh$，$G_{j+1}$ 位于 $y=(j+1)h$（半整数交错格）。
两条方程分别是"某个格点上的 (7)"与"相邻格点上的 (7)"；由于 (4.2) 使二者的 $n=1$ 位势是**同一个** $F_j$，
它们恰好构成一对 Bäcklund 相容的格点方程。(6) 不作为独立格点方程出现，而是这对格点方程在连续极限下的
**反对称组合**——这与 GSG 原文中 (3.8)（格点）+(3.12)（逐点）给出连续物理方程的方式完全同构。

### 4.3 连续极限：**精确 $O(h^2)$** **[精确，借助 jet Taylor 展开]**

设 $F=f(x,Y,t)$、$G=g(x,Y,t)$ 为一般光滑函数，$Y=(j+\tfrac12)h$，则
$G_j=g(Y-\tfrac h2)$、$G_{j+1}=g(Y+\tfrac h2)$。令

$$
M_0:=B_af\cdot g,\qquad M_1:=B_af\cdot g_Y+2D_xf\cdot g ,
$$

则

$$
\boxed{
\begin{aligned}
\tfrac12\big[\textbf{(6)}_h+\textbf{(7)}_h\big]
&=M_0+\frac{h^2}{8}\Big[B_af\cdot g_{YY}+4D_xf\cdot g_Y\Big]+O(h^4),\\[2mm]
\tfrac1h\big[\textbf{(6)}_h-\textbf{(7)}_h\big]
&=M_1+\frac{h^2}{24}\Big[B_af\cdot g_{YYY}+6D_xf\cdot g_{YY}\Big]+O(h^4).
\end{aligned}}
\tag{4.5}
$$

由 §2 的等价性 $M_1=0\iff\text{(6)}|_{\lambda=-2}$（当 $M_0=0$），
故 **(4.3) 是 (7) 与 (6)$|_{\lambda=-2}$ 的二阶精确半离散化**。
（(4.5) 中 $h^0,h^1$ 项已符号验证为零；两式的 $h^2$ 系数亦已符号给出。）

---

## 5. 格点上的孤立子结构

### 5.1 格点色散关系与相位

由 (4.1)，行列式展开后第 $i$ 个孤立子的相位为

$$
\theta_i(j)=(p_i+q_i)x+(q_i^2-p_i^2)t+j\ln\lambda_i+\text{const},
\qquad
\lambda_i=\Big(\tfrac{P_i+\frac h2}{P_i-\frac h2}\Big)\Big(\tfrac{Q_i+\frac h2}{Q_i-\frac h2}\Big),
$$

$$
\boxed{\ \frac{\ln\lambda_i}{h}=\Lambda_h(P_i)+\Lambda_h(Q_i)
=\Big(\frac1{P_i}+\frac1{Q_i}\Big)+\frac{h^2}{12}\Big(\frac1{P_i^3}+\frac1{Q_i^3}\Big)+O(h^4)\ }
\tag{5.1}
$$

即：**离散化只把连续色散 $\frac1{P_i}+\frac1{Q_i}$ 换成格点色散 $\Lambda_h(P_i)+\Lambda_h(Q_i)$**，
误差 $O(h^2)$，孤子的 $x$–$t$ 色散（$p_i+q_i$ 与 $q_i^2-p_i^2$）**完全不变**。

### 5.2 单孤立子

$N=1$ 时

$$
G_j=1+E_j,\qquad F_j=1+rE_j,\qquad
r=-\frac{P+\frac h2}{Q-\frac h2},\qquad
E_j=\frac{e^{\theta_j}}{p+q},
$$

$$
\boxed{\ u_j=2\,\partial_x\ln\frac{F_j}{G_j}
=-\frac{2\,(p+q)^2E_j}{\big(1+E_j\big)\Big[\big(Q-\frac h2\big)-\big(P+\frac h2\big)E_j\Big]}\ }
\tag{5.2}
$$

- **正则性条件**：$\big(P+\frac h2\big)\big(Q-\frac h2\big)<0$，即
  $r>0$。这是原文 (27) 条件 $(a-p_1)(a+q_1)>0$ 的格点推广（$h\to0$ 时二者一致）。
- **振幅**：$\dfrac{d u_j}{dE_j}=0\iff E_j^2=-\dfrac{Q-\frac h2}{P+\frac h2}$，故
  $E_{j,\rm cr}=\sqrt{-\big(Q-\frac h2\big)/\big(P+\frac h2\big)}$，且 $|u_j|$ 在该处取极大。
  在 $h=0$ 时 $E_{j,\rm cr}=\sqrt{-Q/P}$，恰与原文 (27) 的 $\cosh$ 极点一致。

#### 5.2.1 一个精确的"参数重整化"恒等式 **[精确]**

$$
\boxed{\;
u_j^{\rm latt}(E;\,p,q,a,h)\;=\;u^{\rm cont}(E;\,p,q,a-\tfrac h2)\;}
\tag{5.2a}
$$

即 **格点单孤子的"剖面"精确等于把 Bäcklund 参数 $a$ 换成 $a-\frac h2$ 后的连续单孤子剖面**
（符号验证：两者之差恒为 $0$）。唯一真正离散效应出现在 $y$ 相位上：

$$
\underbrace{\frac{\ln\lambda_i}{h}=\Lambda_h(P_i)+\Lambda_h(Q_i)}_{\text{格点}}
\qquad\text{vs}\qquad
\underbrace{\frac1{P_i}+\frac1{Q_i}}_{\text{连续}},
\qquad
\text{相差}\ \frac{h^2}{12}\Big(\frac1{P_i^3}+\frac1{Q_i^3}\Big)+O(h^4).
\tag{5.2b}
$$

因此格点孤子是"**剖面用 $a-\frac h2$、相位用 $a$**"的混合体；(4.5) 与 (5.2b) 表明其中
相位是 $O(h^2)$ 精确的，而剖面的 $O(h)$ 偏移是**参数重整化**（可精确预报），不是数值误差。

**数值例**（$p=1,\ q=2,\ a=3$，此时 $a-p=2>0,\ a+q=5>0$，正则）：

| $h$ | 格点 $E_{\rm cr}$ | 格点 $u_{\max}$ | 未重整的连续 $u_{\max}$（$a=3$） | 偏差 | 重整后 $u_{\max}$（$a-\frac h2$） |
|---|---|---|---|---|---|
| $0$ | 1.5811388 | $-1.3508894$ | $-1.3508894$ | — | $-1.3508894$ |
| $1/4$ | 1.6124516 | $-1.4066134$ | — | $4.13\%$ | $-1.4066134$ |
| $1/2$ | 1.6475089 | $-1.4674374$ | — | $8.63\%$ | $-1.4674374$ |
| $1$ | 1.7320508 | $-1.6076952$ | — | $19.01\%$ | $-1.6076952$ |

（"重整后"一列由 (5.2a) 精确给出，与"格点"一列逐位相同。）

> **关于原文 (27) 的一处注记。** 把 $N=1$ 的 (13)–(15) 直接代入 (5) 得到的连续 $u$ 就是
> (5.2) 取 $h=0$ 的形式，即
> $u=-2E(p+q)^2/[(1+E)((q+a)-(p-a)E)]$，$E=e^{\xi+\eta}/(p+q)$。
> 它与原文 (27) 印刷式一般**不相等**（例：$p_1=1,q_1=2,a=3$，$E=1$ 时本文为 $-1.28571$，
> (27) 为 $-0.79462$；两者作为 $E$ 的函数形状也不同：(27) 分母是"单个 $\cosh$ + 常数"，
> 而直接计算给的是 $(1+E)\big((Q-\frac h2)-(P+\frac h2)E\big)$ 型因子）。
> 本文所有推导一律以 (11)–(15) 的 Gram 行列式直接计算为准，
> 并已独立验证该 $\tau$ 满足 (6)(7)（§2）。

### 5.3 双孤立子与相移：**相移被格点精确保留**

$N=2$ 的行列式展开给出

$$
G_j=1+E_{1,j}+E_{2,j}+\Gamma_{12}E_{1,j}E_{2,j},
\qquad
\boxed{\ \Gamma_{12}=\frac{(p_1-p_2)(q_1-q_2)}{(p_1+q_2)(p_2+q_1)}\ }
\tag{5.3}
$$

**[精确验证]**：引擎给出的 $E_1E_2$ 系数与 $E_1,E_2$ 系数之比**精确等于** (5.3)。

**这是本构造最重要的定性结论**：由于格点乘子 $\lambda_{ik}=\lambda_i\mu_k$ 是**秩一**的，
两孤子的相互作用因子 $\Gamma_{12}$ 与格点指标 $j$、步长 $h$ **完全无关**（是 Cauchy 行列式的普适因子）。
因此

> **格点离散化不改变两孤子相移**，只改变每个孤子的 $y$ 相位速度（(5.1)）。
> 这与 GSG 中"离散化保持相移"的可积性质一致，且在本问题中是**精确**的，而非近似。

### 5.4 $v$ 分量与高阶孤子

定义对角积 $H_j:=\ln(F_jG_j)$，则 $v$ 的自然半离散写法为

$$
v_j=2\,\partial_x\frac{H_j-H_{j-1}}{h}\ \xrightarrow[h\to0]{}\ 2(\ln fg)_{xy},
$$

$N$ 孤子解由 Gram 行列式 (4.1) 给出，其子集展开系数为 Cauchy 行列式的余子式，
$h$ 只出现在 $\lambda_{ik}^{\,j}$ 中（秩一），故**所有阶的相移因子都与 $h$ 无关**。

---

## 6. 与连续解的一致性

- **(7)**：格点上逐点精确成立 $\Rightarrow$ $u_j$ 自动满足半离散版的 (7) 约束。
- **(6)**：由 (4.4)/(4.5)，格点对 (4.3) 的反对称组合在 $h\to0$ 时给出 (6)$|_{\lambda=-2}$，误差 $O(h^2)$。
- **相位**：由 (5.1)/(5.2b)，格点孤子的 $y$ 速度 $\Lambda_h(P)+\Lambda_h(Q)$ 与连续值相差 $O(h^2)$；
  $x$–$t$ 色散 $p+q$、$q^2-p^2$ **完全不变**。
- **剖面/振幅**：由 (5.2a)，格点孤子剖面**精确**等于参数重整化 $a\mapsto a-\frac h2$ 的连续孤子；
  相对未重整的连续解其 $O(h)$ 偏移是可精确预报的参数效应，而非数值误差。
- **相移**：由 (5.3)，**精确相等**。

因此该半离散化在"两孤子相移"与"孤子剖面（在重整化参数下）"这两项上是**精确**的，
在"$y$ 相位速度"上是**二阶精确**的；$O(h)$ 的出现只源于 Bäcklund 参数的整体平移 $h/2$，
可通过把连续解的参数取为 $a-\frac h2$ 而完全消除。

---

## 7. 关于 GSG 第三件工具（离散 hodograph / 自适应网格）

GSG 的 K3 建立在该方程的 **hodograph 对称性** 上：原方程（sG/CH/SP 型）允许
$dy=r\,dx-r\cos u\,dt$ 这类变量替换，从而 $x$ 可视为 $y$ 的因变量；离散化后
$\delta_k=2a\cos\frac{\varphi_{k+1}+\varphi_k}{2}$ 定义了自适应网格 $x=\sum_k\delta_k$，
使得格点方程**精确**等价于原方程（SAMM）。

**对 DLW 系统的检验结果**：

1. DLW（原文 (1)–(2)）**不具备 hodograph 对称性**：$u=2(\ln f/g)_x$ 不是"斜率"变量，
   方程中不存在 $\partial x/\partial y=\cos\varphi$ 型结构。因此 GSG 的
   $\delta_k=2a\cos\frac{\varphi_{k+1}+\varphi_k}{2}$ **没有 DLW 对应物**，
   SAMM 不能字面搬运。
2. 本构造中确实存在一个**替代品**，即 §4.1 的**谱参数 hodograph**：
   $T_{a+\frac h2}(j+1)=T_{a-\frac h2}(j)$，即
   **格点指标 $j$ 与 Bäcklund 参数 $a$ 互为共轭**。这正是 GSG 中
   "格点平移 $\equiv$ 谱参数平移"在 DLW 上的形式，它承担了使半离散系统可积的全部作用。
3. 其代价是：$y$ 方向只能是**均匀网格**。若强行引入解依赖的网格函数 $\delta_j$，
   则 (4.2) 的逐元素恒等式被破坏，(7)$_h$ 不再精确，可积性丧失。
   （可补偿的只是 (5.1) 中的 $O(h^2)$ 相位误差，而由于该误差依赖每个孤子的 $P_i,Q_i$，
   对多孤子解不存在统一的网格重标度 $y\mapsto y/(1+c\,h^2)$ 能同时消除所有孤子的误差。）

**结论**：GSG 方法的三件工具中，**K1（Bäcklund 对）与 K2（谱参数平移 $\equiv$ 格点平移）成功移植**，
并给出 (4.3)；**K3（离散 hodograph / SAMM）在本问题中没有对应物**，DLW 的半离散化只能是均匀网格。

---

## 8. 结论

### 8.1 离散化后的双线性方程（最终答案）

以 $d=h/2,\ P_i=p_i-a,\ Q_k=q_k+a$，$\xi_i=p_ix-p_i^2t+\xi_{i0}$，$\eta_k=q_kx+q_k^2t+\eta_{k0}$：

$$
G_j=\det\Big[\delta_{ik}+\frac{e^{\xi_i+\eta_k}}{p_i+q_k}\lambda_{ik}^{\,j}\Big],\qquad
F_j=\det\Big[\delta_{ik}-\frac{P_i+d}{Q_k-d}\,\frac{e^{\xi_i+\eta_k}}{p_i+q_k}\,\lambda_{ik}^{\,j}\Big],
$$
$$
\lambda_{ik}=\frac{(P_i+d)(Q_k+d)}{(P_i-d)(Q_k-d)}\quad(\text{秩一}),
$$

$$
\boxed{
\begin{aligned}
\textbf{(7)}_h:\quad & \big(D_x^2+D_t+2(a-d)D_x\big)F_j\cdot G_j=0,\\[1.5mm]
\textbf{(6)}_h:\quad & \big(D_x^2+D_t+2(a+d)D_x\big)F_j\cdot G_{j+1}=0,
\end{aligned}}
\qquad d=\frac h2,
$$

且

$$
\tfrac12\big[\textbf{(6)}_h+\textbf{(7)}_h\big]\xrightarrow[h\to0]{}\text{(7)},\qquad
\tfrac1h\big[\textbf{(6)}_h-\textbf{(7)}_h\big]\xrightarrow[h\to0]{}\text{(6)}\big|_{\lambda=-2},
\qquad\text{均为 }O(h^2).
$$

### 8.2 已严格建立的事实清单

| # | 事实 | 状态 |
|---|---|---|
| 1 | 连续 (7)、(6)$|_{\lambda=-2}$ 对 Gram $\tau$ 成立 | **[精确验证 $N\le6$]** |
| 2 | (7) 在任何秩一格点乘子下**逐点精确**成立 | **[精确验证 $N\le3$，3 种乘子]** |
| 3 | 字面离散指数下，两点差分 (6) 的残差为 $4c\chi^jE\Delta$，$\Delta\equiv h\times$非零 | **[精确，$N=1$ 封闭式]** |
| 4 | 6 类模板 $\times$ 3 种乘子 $\times N=1,2$ 全部不闭合 | **[精确验证]** |
| 5 | 广义线性搜索：零空间仅含 $Bf_{j+1}g_j+Bf_jg_{j+1}=0$ 与 $Bf_jg_j=0$；反对称方向不在其中 | **[精确验证 + 独立复核]** |
| 6 | 恒等式 $T_{a+\frac h2}(j+1)=T_{a-\frac h2}(j)$ | **[精确，$N\le4$]** |
| 7 | 格点对 (4.3) 精确成立 | **[精确验证 $N\le5$]** |
| 8 | 连续极限 (4.5)，$h^0,h^1$ 项为零，$h^2$ 系数显式 | **[精确，jet 展开]** |
| 9 | 格点色散 $\Lambda_h$ 的 $h^2$/$h^4$ 系数 $=1/(12z^3),1/(80z^5)$ | **[精确]** |
| 10 | 两孤子相移 $\Gamma_{12}$ 与 $h,j$ 无关 | **[精确验证 $N=2$]** |
| 11 | 单孤子 (5.2) 正则条件与振幅极值点 | **[精确]** |
| 12 | $u^{\rm latt}_j(E;p,q,a,h)=u^{\rm cont}(E;p,q,a-\tfrac h2)$ | **[精确]** |
| 13 | DLW 无 hodograph 对称性，SAMM 不适用 | **论证 + 结构分析** |

### 8.3 待进一步研究

1. **半离散非线性 DLW 系统**：由 (4.3) 经 $u_j=2\partial_x\ln(F_j/G_j)$ 消去 $\tau$ 得到
   $u_j,v_j$ 的显式格点方程（GSG 原文 (3.31)–(3.33) 的对应物）。本文给出的是其双线性层。
2. **等谱/非等谱问题的严格证明**：(4.3) 的可积性（Lax 对、守恒量）需要进一步构造。
3. **数值实验**：以 (4.3) 为模板的直接离散格式（二阶相容但非精确可积）与精确格点格式
   在长时间演化上的保结构对比。

---

## 附：复现命令

```powershell
cd C:\Users\msz\学术内容\Paper\gsg_project\code
python -u main_checks.py        # A–F：连续基线、精确障碍、恒等式、格点对、连续极限
python -u soliton_analysis.py   # 格点色散、单孤子、两孤子相移
python -u obstruction.py        # 广义线性零空间搜索
python -u verify_nullvec.py     # 零向量在新鲜点上的独立复核
python -u onesoliton_check.py   # 单孤子与原文 (27) 的数值对照
```

核心引擎 `engine.py`：以"行/列重数" $(\mathbf n,\mathbf m)$ 为指数单体的键
（关键：$E_{00}E_{11}=E_{01}E_{10}$，故不能用配对作键），
在一般有理点上做精确有理运算，从而把双线性恒等式检验化为字典是否为空。
