# 将（广义）sine-Gordon 半离散化方法移植到 DLW 双线性系统 (6)(7)

> **最新复核（2026-09-19）**：下面的整体验证作废声明需要限定范围。
> 纯 x,t,j 的 Gram 构造现已获得任意 N 的独立证明；额外连续 y 相位随参数 s 变化的混合构造不成立。
> 当前精确公式、正则性、相移与可积性证据见 `GRAM_INTEGRABILITY_REASSESSMENT.md`，
> 正确闭合非线性形式见 `NONLINEAR_CLOSURE.md`。这不恢复本文其他未经复核的唯一性、物理公式及可积性结论。
## —— 离散双线性方程的形式与孤立子结构分析

> ## ⚠ 作废声明（见 `AUDIT.md`）
>
> **本报告中关于 §2 起的离散（格点）结果的"精确验证"是无效的。**
> 审计发现两个缺陷：
>
> 1. `jet3.py` 的系数是 `mpmath.mpf`（60–90 位浮点），所以残差 `1e-89` 是**浮点噪声**，不是零；
> 2. 更严重：所有判零都在**单个基点** `(x,t,y)=(1/5, 2/7, 0)` 上求值，而该点恰好落在使
>    残差为零的曲面上（`(7)_h` 的残差精确地正比于 `e^{433y/385} − 1`），
>    于是**非恒等式被误判为恒等式**。
>
> **`(7)_h`、`(6)_h` 并不恒成立**：残差在一般点上的量级为 `O(0.02–2833)`，且随 `h→0`
> 按 **`O(h)`** 衰减——它们是离散化误差，不是有限 `h` 下的恒等式。由它们导出的
> `(★)`、`(★')`、`(†)`、"非线性层" `(A)_h`/`(B)_h`/`(A')`、以及连续极限那张表**全部作废**。
>
> **存活的结论**：
> - `(H1)` 商恒等式 `D_x²F·G/(FG)=(lnF)_xx+(lnG)_xx+[(lnF)_x−(lnG)_x]²`（交叉项系数 +1）——
>   这是**真正**的精确代数恒等式，由 `idcheck3.py` 在任意符号 `F,G` 上 sympy 证明，
>   且用 `Fraction` 可得到字面 0；
> - 连续层 `(7) B_a f·g = 0`——精确为零（N=1、N=2 均确认）；
> - 论文形态的 `(6)` 与我实现的 τ **不相容**（`audit_gauge.py`：残差与相位常数无关，对
>   相位常数无解）；此问题**尚未解决**。
>
> 下文正文保留原文以便对照，但**§2 起的一切"精确验证"字样请勿采信**，以 `AUDIT.md` 为准。
>
> ---

> 本文件是 `gsg_project/OUT_GSG_DLW_report.md` 的**修订与补全版**。
> 记号约定（**已修正**）：`[精确]` = 代数恒等式（对任意参数成立，可用精确有理数得到字面 0）；
> `[精确验证]` = 在有限个一般位置有理点上精确测试为零（对有理函数即充分）——**但必须多点，
> 单点测试不足以判零**；`[数值]` = 高精度数值验证。

---

## 0. 摘要：最终交付的离散双线性方程

设 y 方向格距为 $h>0$，记

$$d=\tfrac h2,\qquad \lambda(z)=\frac{z+d}{z-d}\;\bigl(\;\approx e^{h/z}\;\bigr).$$

在第 $j\in\mathbb Z$ 个格点上取

$$\boxed{\;F_j:=\tau_1\bigl(j;\,s=a-d\bigr),\qquad G_j:=\tau_0(j)\;}$$

其中 $\tau_n(j;s)$ 是 DLW 的 Gram 型行列式（元素见 §1.2）。则**离散化后的双线性方程组**为

$$
\boxed{\;
\begin{aligned}
\textbf{(7)}_h:\quad & \Bigl[D_x^{2}+D_t+2(a-d)D_x\Bigr]F_j\cdot G_j=0,\\[2mm]
\textbf{(6)}_h:\quad & \Bigl[D_x^{2}+D_t+2(a+d)D_x\Bigr]F_j\cdot G_{j+1}=0 .
\end{aligned}}
\tag{$\star$}
$$

与 $\;(\star)\;$ **完全等价**、且连续极限直接给出论文中 (6) 的二点形式是

$$
\boxed{\;
\frac1h\Bigl[D_x^{2}+D_t+2(a-d)D_x\Bigr]F_j\cdot\bigl(G_{j+1}-G_j\bigr)
+2D_xF_j\cdot G_{j+1}=0
\;}
\tag{$\star'$}
$$

支撑整个构造的**结构恒等式**是 $F_j$ 的"格点位移 = 谱参数位移"：

$$
\boxed{\;\tau_1\bigl(j;\,a-d\bigr)=\tau_1\bigl(j+1;\,a+d\bigr)\quad\text{逐元素相等}\;}
\tag{$\dagger$}
$$

**主要结论一览**

| 编号 | 结论 | 状态 |
|---|---|---|
| A | $(\star)$ 的两个方程对全部 $N$-孤子解精确成立（$N\le5$，格点 $j=0,\dots,3$） | [精确验证] |
| B | $(\star)\Leftrightarrow(\star')$（用 $(\dagger)$） | [精确] |
| C | $(\star')$ 的连续极限恰为 $(6)\vert_{\lambda=-2}$：$B_af\cdot g_y+2D_xf\cdot g=0$，且为**二阶精度** | [数值] |
| D | 在 24 维二点模板 $\{D_x^2,D_t,D_x,\mathrm{id}\}\times\{(0,0),(\pm1,0),(0,\pm1),(1,1)\}$ 中，$(\star)$ **恰好张成全部**精确解空间（dim 4），且对 $h$ 稳健（5 个 $h$ 值） | [精确验证] |
| E | 若不用交错（$s$ 与算子参数同为 $a$），则模板中**不存在**任何首阶给出 (6) 的格点方程；表面的跨位点解是固定 $h$ 的伪向量 | [精确验证 + 显式反例] |
| F | 格点 $\tau$ = 连续 $\tau$ 在替换 $\frac1{p_i-s}\mapsto\Lambda_h(p_i-s)$、$\frac1{q_k+s}\mapsto\Lambda_h(q_k+s)$ 之下 | [精确] |
| G | 格点色散：$\Lambda_h(z)=\frac1z+\frac{h^{2}}{12z^{3}}+\frac{h^{4}}{80z^{5}}+\cdots$（二阶） | [精确] |
| H | 双孤子相互作用系数 $\kappa$ 与 $h$ **严格无关** ⟹ 相移与连续情形完全相同 | [精确] |
| I | 旧报告中"对称二点恒等式"只在 $N=1$ 成立；旧 `mshift.py` 的"$a\to a-h/2$"结论有误 | 更正，见 §9 |
| J | **非线性层**：$(\star)$ 除以 $F_jG_j$ 后化为纯势函数方程 $(\mathrm{A})_h$：$\Psi_{j,xx}+\theta_{j,x}^2+\theta_{j,t}+2(a-d)\theta_{j,x}=0$ | [精确验证] |
| K | 物理形式 $u_{j,t}+w_{j,x}+\tfrac12u_j^2+2(a-d)u_j=0$，其中 $u_j=2\theta_{j,x}$、$w_j=2\Psi_{j,x}$ | [精确验证] |
| L | $(\mathrm{A})_h$ 的连续极限 $h\to0$ 恢复连续非线性方程 $\Psi_{xx}+\theta_x^2+\theta_t+2a\theta_x=0$；误差 $O(h)$（比值 0.5） | [数值] |
| M | 关键 Hirota 商恒等式：$D_x^2F\cdot G/(FG)=(\ln F)_{xx}+(\ln G)_{xx}+[(\ln F)_x-(\ln G)_x]^2$（交叉项系数 **+1**，由 sympy 唯一确定） | [精确] |

---

## 1. 出发点

### 1.1 论文中的 DLW 系统与双线性对

`PhysD-published.pdf`（Sheng–Yu, *Physica D* **432** (2022) 133140）的 (2+1) 维色散长波系统为

$$u_{yt}+v_{xx}+uu_{xy}+u_xu_y+2a\,u_{xy}=0, \tag{1}$$
$$v_t+(uv)_x+u_{xxy}+2a\,v_x+2\lambda\,u_x=0, \tag{2}$$

其双线性对为

$$(D_x^{2}+D_t+2aD_x)f\cdot g=0, \tag{7}$$
$$\bigl[D_y(D_x^{2}+D_t+2aD_x)+2\lambda D_x\bigr]f\cdot g=0 . \tag{6}$$

记 $B_s:=D_x^{2}+D_t+2sD_x$。由 $D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y$ 与
$\partial_y[(7)]\Rightarrow B_af_y\cdot g=-B_af\cdot g_y$，得

$$\lambda=-2\ \text{时}\quad (6)\iff B_af\cdot g_y+2D_xf\cdot g=0\quad(\text{在 (7) 成立的前提下}). \tag{6'}$$

变量变换为

$$u=2(\ln f/g)_x,\qquad v=2(\ln fg)_{xy}.$$

### 1.2 Gram $\tau$ 函数

论文 (13)–(15)：

$$m^{(n)}_{ik}=c_k\delta_{ik}+\frac1{p_i+q_k}\Bigl(-\frac{p_i-a}{q_k+a}\Bigr)^{n}
e^{\xi_i+\eta_k},\qquad
\xi_i=p_ix-p_i^{2}t+\frac{y}{p_i-a},\quad \eta_k=q_kx+q_k^{2}t+\frac{y}{q_k+a}.$$

以 $f=\tau_{n+1}$，$g=\tau_n$ 代入即得 (6)(7)。

---

## 2. 方法：GSG 半离散化的三个部件及其移植

`gsg_project/gsg.txt`（Feng–Sheng–Yu, *Numer. Algorithms* **94** (2023) 351–370）
的广义 sine-Gordon 半离散化由三个部件组成：

**K1　双线性 Bäcklund 变换。**
在 GSG 中，(7) 型方程本身即由 Bäcklund 变换给出；在 DLW 中对应的事实是
$B_s$ 的**参数 $s$ 必须与 $\tau_1$ 的系数参数 $s_f$ 一致**，且偏差是精确可算的：

$$\boxed{\;B_s\,\tau_1(j;s_f)\cdot\tau_0(j)=2(s-s_f)\,D_x\tau_1(j;s_f)\cdot\tau_0(j)\;}$$

（连续、格点、$N=1,2$、$j=0,1$ 均已精确验证为空）。
特别地 $s=s_f$ 时 $B_s\tau_1\cdot\tau_0=0$，这就是 (7)。
这把"算子参数"与"$\tau$ 参数"锁在一起，是后面交错构造的根源。

**K2　离散指数（"格点位移 $\equiv$ 谱参数位移"）。**
GSG 的核心是把连续指数 $e^{\xi_i}$ 换成 $\lambda_i^{n}$。在 DLW 中，

$$\frac{y}{p_i-a}\ \longrightarrow\ j\ln\lambda(p_i-a),\qquad
\frac{y}{q_k+a}\ \longrightarrow\ j\ln\lambda(q_k+a),$$

即每个矩阵元乘上**秩一因子**

$$\chi_{ik}=\lambda(p_i-a)\,\lambda(q_k+a),\qquad m^{(n)}_{ik}(j)=m^{(n)}_{ik}\big|_{\text{连续}}\cdot\chi_{ik}^{\,j}.$$

$\chi_{ik}$ 的秩一性是全部精确结论的来源（见 §8.1）。

**K3　离散 hodograph / 自适应移动网格（SAMD）。**
GSG 用 $\delta_k=2a\cos\frac{\varphi_{k+1}+\varphi_k}{2}$ 把格点位置变成动力学变量。
DLW 系统**没有** hodograph 对称性（(1)(2) 中 $x,t$ 的地位不可互换），
因此 K3 **没有** DLW 对应物。本工作只移植 K1+K2，得到的是**固定格距**的半离散化。
这是必须诚实指出的局限。

---

## 3. 结果 A：格点上的 (7) 是逐点精确恒等式

**命题 1**　对任意 $N$、任意格点 $j$、任意 $s$，只要 $\tau_1$ 的系数参数等于 $s$，

$$B_s\,\tau_1(j;s)\cdot\tau_0(j)=0 .$$

*验证*：`certify.py` §B（$N\le4$，$j=0,\dots,3$，全套 OK）。

但对**同一个** $s$，跨位点组合 $B_s\,f_{j+p}\cdot g_{j+q}\ (p\ne q)$ 一般不为零。
$N=1$ 时可得精确闭式（`certify.py` §C）：

$$B_a\,\tau_1^{(p)}\cdot\tau_0^{(q)}=2c\,P\,E\,\bigl(\chi^{q}-\chi^{p}\bigr),
\qquad P=p_1-a,\ \ \chi=\lambda(P)\lambda(Q).$$

它关于 $(p,q)$ **反对称**，故当且仅当 $p=q$ 时为零。这说明：
**仅靠 (7) 无法产生任何格点信息——(7) 是纯逐点等式。**

---

## 4. 结果 B：离散化后的双线性方程（核心交付）

要让"跨位点"组合为零，必须让**算子参数与 $\tau$ 参数不一致**。取

$$F_j=\tau_1\bigl(j;\,s=a-d\bigr),\qquad G_j=\tau_0(j),\qquad d=\frac h2,$$

并利用 $(\dagger)$：$\tau_1(j;a-d)=\tau_1(j+1;a+d)$。于是

$$
\boxed{\;
\begin{aligned}
\textbf{(7)}_h:\quad & B_{a-d}\,F_j\cdot G_j=0,\\[1mm]
\textbf{(6)}_h:\quad & B_{a+d}\,F_j\cdot G_{j+1}=0 .
\end{aligned}}
$$

**命题 2**　$(\star)$ 对全部 $N$-孤子解精确成立。

*验证*：`certify.py` §F，$N=1,\dots,5$，格点 $j=0,1,2,3$，全部 OK（4×5=20 组全过）。
另有独立代码路径 `soliton_lattice.py` §1/2，用**显式 determinant + sympy 求导 + 机器精度求值**
复核：$N=1,2,3$ 时 $\max|(7)_h|=\max|(6)_h|=0.00\text{e}+00$。

**$(\dagger)$ 为什么成立（一行证明）** 在格点上，$\tau_1$ 的矩阵元除指数因子外只有一个系数
$-\frac{p-s}{q+s}\cdot\frac1{p+q}$，乘上 $\chi_{ik}^{j}$。取 $s=a-d,\ j$ 与 $s=a+d,\ j+1$：

$$-\frac{P-d}{Q+d}\cdot\chi_{ik}
=-\frac{P-d}{Q+d}\cdot\frac{P+d}{P-d}\cdot\frac{Q+d}{Q-d}
=-\frac{P+d}{Q-d},$$

右端正是 $s=a+d$ 的系数。$\square$

（`certify.py` §E，$N\le4$ 逐元素相等，全部 OK。）

---

## 5. 结果 C：等价二点形式与连续极限

### 5.1 等价二点形式

由 $B_{a+d}=B_{a-d}+2hD_x$ 与 $(7)_h$，

$$
(\star')\quad
\frac1h B_{a-d}F_j\cdot(G_{j+1}-G_j)+2D_xF_j\cdot G_{j+1}=0
\;\Longleftrightarrow\;
\frac1h(6)_h=0 .
$$

*验证*：`certify.py` §G，$N\le4$，$j=0,1,2$ 全部 OK。

### 5.2 连续极限（必须用二点形式）

若把 $F_j,G_j$ 看成光滑函数在 $y_0=(j+\tfrac12)h$（$F$）与 $y_0\pm\tfrac h2$（$G$）处的取值：

* $B_{a-d}F_j\cdot G_j$ 的首项恒为 $B_af\cdot g$，故 $(7)_h$ 的极限就是 **(7)**；
* $(\star')$ 中差分与算子参数偏移各贡献一阶项，求和后首项不再抵消：

$$\frac1h B_{a-d}F_j\cdot(G_{j+1}-G_j)+2D_xF_j\cdot G_{j+1}
\;\xrightarrow[h\to0]{}\;
B_af\cdot g_y+2D_xf\cdot g=0,$$

正是 $(6)\vert_{\lambda=-2}$。

> **一个必须讲清楚的细节**：单独看 $(6)_h=0$，它的 $O(h^0)$ 项与 $(7)_h$ 相同（都退化为 (7)）；
> 真正携带 (6) 的信息的，是 $[(6)_h-(7)_h]/h$，而它**恰好就是** $(\star')$。
> 因此半离散系统应写成 $\{(7)_h,\;(\star')\}$（或等价地 $\{(7)_h,(6)_h\}$ 并做线性重组），
> 否则在 $h\to0$ 时会看到"两个方程退化成同一个"的假象。

*验证*：`soliton_lattice.py` §7，把两个格点算子作用在**连续精确解** $\tau$ 上，
$|E_1|$ 与 $|E_2|$ 均以 $h^{2}$ 衰减。实测：

| $h$ | $\vert E_1\vert$ | 比值 | $\vert E_2\vert$ | 比值 |
|---|---|---|---|---|
| 1/4 | 2.273e−01 | — | 5.453e−01 | — |
| 1/8 | 6.363e−02 | 3.57 | 1.872e−01 | 2.91 |
| 1/16 | 1.688e−02 | 3.77 | 5.532e−02 | 3.38 |
| 1/32 | 4.350e−03 | **3.88** | 1.507e−02 | **3.67** |

比值趋于 4，即二阶精度。

### 5.3 朴素方案为什么不行

最自然的写法是中心差商：

$$\frac1h\Bigl[B_af_{j+1}\cdot g_j-B_af_j\cdot g_{j+1}\Bigr]-4D_xf_j\cdot g_j .$$

$N=1$ 时（`certify.py` §D）此残差有闭式

$$\text{res}=\frac{h\,c\,E\,\chi^{j}(p+q)(h-2p-2q)}{Q\,(P-d)(Q-d)},$$

即**恒为 $O(h)$，对 $h>0$ 永不为零**；$N\le3$ 数值验证残差不恒为零。
所以朴素中心差商只有**一阶**精度且非精确可积——这正是必须使用交错构造的原因。

---

## 6. 结果 D/E：唯一性与 no-go —— $(\star)$ 是二点模板中的唯一可能

**搜索空间。** 全部 24 个双线性组合

$$\bigl\{D_x^{2},\,D_t,\,D_x,\,\mathrm{id}\bigr\}\times\bigl\{(0,0),(1,0),(0,1),(1,1),(-1,0),(0,-1)\bigr\},$$

系数限定在 $\mathbb Q(a,h)$ 中（**不得依赖谱参数 $p_i,q_k$**）。
判定方法：把 $N=1,2,3,4,5$ 的线性约束叠在一起求交（`nosearch.py`）。

> **方法学警告（本工作发现的一个陷阱）.** 求交矩阵是在**固定**的 $(a,h)$ 上组装的。
> 因此零空间里可能混入"**只在该 $h$ 处为零**"的伪向量。这一点已被显式证实（见下）。
> 另外，**必须求交，不能只检验 $N=1$ 零空间的一组基向量**——$N=1$ 的 $\tau$ 只有两项，
> 其零空间高度退化，混有大量伪解（旧报告 §3.3(c) 的错误正源于此）。

### 6.1 交错类：唯一且对 $h$ 稳健

在 $h\in\{1/2,\;3/7,\;1/3,\;1/5,\;1/10\}$ 五个值上分别做 $N\le5$ 的交集，**每次**都得到
$\dim=4$，而且零空间基**恰好**是下面四个向量（以 $h=1/2$ 的规范化为例，
$D_x^2,D_t$ 系数 $2/9$ 表示算子 $B_{a-d}$，$a-d=9/4$）：

| 位点 | $D_x^{2}$ | $D_t$ | $D_x$ | $\mathrm{id}$ | 含义 |
|---|---|---|---|---|---|
| $(0,0)$ | $2/9$ | $2/9$ | $1$ | — | $(7)_h$ 在格点 $j$：$B_{a-d}F_j\cdot G_j$ |
| $(1,1)$ | $2/9$ | $2/9$ | $1$ | — | $(7)_h$ 在格点 $j+1$ |
| $(0,1)$ | $2/11$ | $2/11$ | $1$ | — | $(6)_h$ 在 $(j,j+1)$：$B_{a+d}F_j\cdot G_{j+1}$ |
| $(-1,0)$ | $2/11$ | $2/11$ | $1$ | — | $(6)_h$ 在 $(j-1,j)$ |

（$2/11$ 对应 $2(a+d)=11/2$，$a+d=11/4$。）
即：**该模板中全部精确格点恒等式，就是 $(\star)$ 在两个相邻位点上的取值。**
换言之，$\{(7)_h,(6)_h\}$ 是此模板内**唯一**的精确可积半离散系统，且该结论对 $h$ 稳健。

### 6.2 均匀类：固定 $h$ 会造出伪向量

均匀类（$f=\tau_1$ 携带系数参数 $a$）在**固定** $h=1/3$、$N\le7$（8748 行）时维数也是 4，
多出两个跨位点向量。它们的系数**按 $h^{-2}$ 发散**，结构可以完全定出来。
$a=5/2$、$h=1/2,1/3,1/5,1/10,1/20$ 的规范化基给出

| 位点 | $D_x^{2}=D_t$ | $D_x$ | $\mathrm{id}$ |
|---|---|---|---|
| $(1,0)$ | $-1/h^{2}$ | $-(2a-2h)/h^{2}$ | $-1$ |
| $(0,1)$ | $+1/h^{2}$ | $+(2a+2h)/h^{2}$ | $+1$ |

乘以 $-h^{2}$ 后即

$$\boxed{\;X:=B_{a-h}F_{j+1}\cdot G_j-B_{a+h}F_j\cdot G_{j+1}
+h^{2}\bigl(F_{j+1}G_j-F_jG_{j+1}\bigr)=0\;}\tag{$\ddagger$}$$

**$(\ddagger)$ 是否精确？** `uni_identity.py` 直接检验（$N\le4$，位点 $j=0,1,2$）：

| $h$ | $N=1$ | $N=2$ | $N=3$ | $N=4$ |
|---|---|---|---|---|
| $1/2$ | 3/3 | 3/3 | **0/3** | **0/3** |
| $1/3$ | 3/3 | 3/3 | 3/3 | 3/3 |
| $1/4$ | 3/3 | 3/3 | 3/3 | 3/3 |

即 $(\ddagger)$ 在 $h=1/3,1/4$ 处为零，却在 $h=1/2$ 处**不为零**。
所以 $(\ddagger)$ **不是恒等式**，它只是在某些 $h$ 值上恰好为零——
**固定 $h$ 的零空间搜索确实会造出伪向量。**

**为什么是伪向量（结构论证）.** 让 $h\to0$（保持物理 $y=jh$ 固定），全部位点合并为一点，
故任何 $\mathbb Q(a,h)$ 系数的均匀类恒等式的极限算子是**单点**双线性算子，它必须
湮灭连续 $\tau$；而单点恒等式空间一维（§3 的反对称闭式），故极限 $\propto B_a$。
也就是说：

> **均匀类恒等式的 $h^{0}$ 阶内容永远只能是 $(7)$，不可能在首阶给出 (6)。**
> 而 $(6)$ 含 $\partial_y$，只能出现在 $O(h)$ 阶；这时 $(\ddagger)$ 的首阶为

$$X=h\,D_yB_af\cdot g-4h\,D_xf\cdot g+O(h^{2})=O(h^{2})\quad(\text{用了 }(6)),$$

即首阶**恒等于零**——这正是 $(\ddagger)$ 看起来"很像恒等式"的原因，也是它为什么
只在特殊 $h$ 处才真正为零。

**结论（no-go + uniqueness）。**

> 若要求算子参数与 $\tau$ 参数一致（"均匀"），则 y 格点模板中**不存在** (6) 的精确格点对应物
> （只能得到 $(7)$ 及其退化变形）；正是 $(\dagger)$ 所允许的"参数—位点"交错，
> 才使 (6) 获得精确格点形式，并且该形式在此模板内**唯一**（§6.1，对 $h$ 稳健）。

---

## 7. 结果 E：非线性形式

令

$$\theta_j=\ln\frac{F_j}{G_j},\quad \Psi_j=\ln(F_jG_j),\quad
\Theta_j=\ln\frac{F_j}{G_{j+1}},\quad \Phi_j=\ln(F_jG_{j+1}).$$

利用 $D_x^{2}F\cdot G=FG\bigl[(\ln FG)_{xx}+((\ln F/G)_x)^{2}\bigr]$、$D_xF\cdot G=FG(\ln F/G)_x$、
$D_tF\cdot G=FG(\ln F/G)_t$，$(7)_h$ 与 $(6)_h$ 分别化为

$$
\textbf{(N1)}\quad \Psi_{j,xx}+\theta_{j,x}^{2}+\theta_{j,t}+2(a-d)\theta_{j,x}=0,
$$
$$
\textbf{(N2)}\quad \Phi_{j,xx}+\Theta_{j,x}^{2}+\Theta_{j,t}+2(a+d)\Theta_{j,x}=0 .
$$

两者由**纯代数**关系联系：

$$\Theta_j=\tfrac12(\Psi_j-\Psi_{j+1})+\tfrac12(\theta_j+\theta_{j+1}),\qquad
\Phi_j=\tfrac12(\Psi_j+\Psi_{j+1})+\tfrac12(\theta_j-\theta_{j+1}).$$

再引入场量 $u_j:=2\theta_{j,x}$（对应 $u=2(\ln f/g)_x$）、
$w_j:=2\partial_x\ln(G_{j+1}/G_j)$，对 (N1)(N2) 各求一次 $\partial_x$ 后相减，得到**闭合的二点系统**

$$
\textbf{(L1)}\quad u_{j,t}+u_ju_{j,x}+2(a-d)u_{j,x}+2\Psi_{j,xxx}=0,
$$
$$
\textbf{(L2)}\quad w_{j,t}+(u_jw_j)_x-\tfrac12(w_j^{2})_x
+2a\,w_{j,x}-2h\,u_{j,x}+h\,w_{j,x}-w_{j,xx}=0 .
$$

其中 $w_j\simeq 2h(\ln g)_{xy}$，故 $w_j/h$ 才对应论文的 $v=2(\ln fg)_{xy}$。
**这里要明确指出**：论文的 $v=2(\ln fg)_{xy}$ 涉及 $f$ 与 $g$ 的**乘积**，而交错构造中
$G_{j+1}/G_j$ 只含 $g$；要得到完整的 $v$ 必须同时使用对角量与交叉量
（$\Psi_j,\Phi_j$），这正是 (N1)(N2) 与代数关系的作用。因此
**(N1)+(N2)+代数关系** 是半离散非线性 DLW 系统的正确、无冗余形式；
把它压成两个 $(u,v)$ 方程需要额外的规范选择，且不同选择给出形式上不同的系统。

---

## 8. 结果 F–H：孤立子结构分析

### 8.1 结构定理（本工作最有力的结果）

$$m^{(n)}_{ik}(j)=c_k\delta_{ik}+\frac1{p_i+q_k}
\Bigl(-\frac{p_i-s}{q_k+s}\Bigr)^{n}\chi_{ik}^{\,j}e^{\xi_i+\eta_k},\qquad
\chi_{ik}=\lambda(p_i-s')\,\lambda(q_k+s'),$$

其中 $\chi_{ik}$ 对 $(i,k)$ **秩一**。行列式展开时，每一个单项都是
$\prod_i\chi_{i,\sigma(i)}^{\,j}$，而

$$\prod_i\chi_{i,\sigma(i)}
=\prod_i\lambda(p_i-s')\cdot\prod_k\lambda(q_k+s'),$$

只依赖**行/列重数**，与指数部分 $\prod_i e^{\xi_i+\eta_k}$ 的乘法结构完全一致。于是

> **定理（离散指数定理）.** 格点 $\tau$ 等于连续 $\tau$ 在如下替换之下：
> $$\frac1{p_i-s}\ \longmapsto\ \Lambda_h(p_i-s),\qquad
> \frac1{q_k+s}\ \longmapsto\ \Lambda_h(q_k+s),$$
> $$\Lambda_h(z):=\frac1h\ln\lambda(z)=\frac2h\operatorname{artanh}\frac{h}{2z}.$$

**推论 1**　行列式展开中一切**相互作用（碰撞）系数保持不变**，与 $h$ 无关。
特别地，$2\times2$ 行列式的相互作用系数

$$\kappa=A_{11}A_{22}-A_{12}A_{21}
=\frac{(p_1-a)(p_2-a)(p_1-p_2)(q_1-q_2)}
{(a+q_1)(a+q_2)(p_1+q_1)(p_1+q_2)(p_2+q_1)(p_2+q_2)}$$

**不含 $h$**。故

> **双孤子相移与连续 DLW 完全相同，格点化不改变相移。**

*验证*：`soliton_lattice.py` §3 与 §6(b)；§6(a) 进一步在**物理场** $u_j=2\partial_x\ln(F_j/G_j)$
上验证（$N=2$，$j=1$）：
$\max|u_{\text{格点}}-u_{\text{连续(速率重正化)}}|=1.4\times10^{-10}$（$h=1/4$）、
$8.6\times10^{-11}$（$h=1/8$），即机器精度一致。

### 8.2 格点色散关系

$$\Lambda_h(z)=\frac1z+\frac{h^{2}}{12z^{3}}+\frac{h^{4}}{80z^{5}}+\frac{h^{6}}{448z^{7}}+\cdots$$

单孤子的 y 相位：格点为 $j\ln\!\bigl(\lambda(P)\lambda(Q)\bigr)=jh\bigl[\Lambda_h(P)+\Lambda_h(Q)\bigr]$，
连续为 $y\bigl(\tfrac1P+\tfrac1Q\bigr)$。误差

$$\Delta=\frac{h^{2}}{12}\Bigl(\frac1{P^{3}}+\frac1{Q^{3}}\Bigr)+O(h^{4}),$$

**二阶**，且系数明确。

### 8.3 单孤子精确解

取 $c=1$，$S=p+q$，$P=p-a$，$Q=q+a$，$E=e^{Sx+(q^{2}-p^{2})t}$：

$$F_j=1-\frac{P}{QS}e_j,\qquad G_j=1+\frac{e_j}{S},\qquad e_j=E\,\lambda(P)^{j}\lambda(Q)^{j},$$

$$\boxed{\;u_j=2\partial_x\ln\frac{F_j}{G_j}
=\frac{-2S^{3}e_j}{(S+e_j)\bigl(QS-Pe_j\bigr)}\;}$$

这与连续单孤子**函数形式完全相同**，只是把
$e^{y(1/P+1/Q)}$ 换成 $\lambda^{j}$——即 8.1 的结构定理在 $N=1$ 的显式体现。
剖面是"线孤子"型扭结；格点化只改变它在 $y$ 方向的**速率**（$O(h^{2})$），不改变形状。

### 8.4 双孤子与相移

* 精确 $2\times2$ Gram 行列式（$N\le5$ 已用机器精度复核满足 $(\star)$）；
* 由推论 1，相互作用系数 $\kappa$ 不含 $h$，故**相移 $h$-无关**；
* 数值上，格点 $u$ 场与"速率重正化后的连续 $u$ 场"在 $N=2$ 时逐点相符到 $10^{-10}$。

**物理图像**：格点上的 $N$-孤子解与连续 $N$-孤子解逐项一一对应，唯一的差别是每个
$(i,k)$ 通道的 $y$-速率被 $\Lambda_h$ 重正化；孤子之间的相对相位、碰撞位移、
渐近振幅均与连续情形**完全一致**。这就是"离散指数"机制的净效果。

### 8.5 连续极限与精度汇总

| 量 | 连续极限 | 误差阶 | 实测比值（$h\to h/2$） |
|---|---|---|---|
| $(7)_h$ 作用于连续解 | $(7)$ | $O(h^{2})$ | 3.57 → 3.77 → **3.88** |
| $(\star')$（二点形式）作用于连续解 | $(6)\vert_{\lambda=-2}$ | $O(h^{2})$ | 2.91 → 3.38 → **3.67** |
| 色散 $\Lambda_h$ vs $1/z$ | — | $h^{2}/(12z^{3})$ | $h=0.1$ 时 $1.6395\times10^{-4}$，公式值 $1.6445\times10^{-4}$ |
| 固定物理 $y=1$ 的场误差 | — | $O(h^{2})$ | 5.31 → 4.27 → **4.06** |
| 固定格点 $j=1$ 的场误差 | — | $O(h^{3})$ | 11.5 → 8.57 → **8.13** |

> 固定 $j$ 与固定物理 $y$ 的阶数差异是自然的：相位误差为
> $j\cdot h\cdot\bigl[(h^{2}/12)(P^{-3}+Q^{-3})+\cdots\bigr]$。

**图** `soliton_lattice.png` 三个面板：
(a) 单孤子剖面 $u_j(x)$（$j=1$）在 $h=0,0.4,0.8$ 下的对比；
(b) 格点色散误差与 $\propto h^{2}$ 参考线的双对数图；
(c) 两条组成孤子的剖面（$j=1,\ h=0.4$）。

---

## 8b. 非线性层：从双线性 $(\star)$ 回到真正的非线性微分-差分系统

本节把第 4–5 节的 $\tau$-函数层面的结果**回代**为非线性方程。全部结论由
`nlfinal.py`（逐点精确复核，机器精度 $\sim10^{-89}$）、`idcheck2.py`/`idcheck3.py`
（sympy 符号判定）与 `nlcont.py`（连续极限与收敛阶）给出。

### 8b.1 关键 Hirota 商恒等式

设 $\alpha=\ln F$、$\beta=\ln G$，记
$A=\alpha_x=F_x/F$、$B=\beta_x=G_x/G$。则对**任意**非退化 $F,G$：

$$
\boxed{\;
\frac{D_x^2F\cdot G}{FG}
=(\ln F)_{xx}+(\ln G)_{xx}+\bigl[(\ln F)_x-(\ln G)_x\bigr]^2
\;}
\tag{H1}
$$

$$
\frac{D_tF\cdot G}{FG}=(\ln F)_t-(\ln G)_t,\qquad
\frac{D_xF\cdot G}{FG}=(\ln F)_x-(\ln G)_x
\tag{H2}
$$

其中 $(\ln F)_{xx}=F_{xx}/F-(F_x/F)^2$（**不是** $F_{xx}/F$）。

> **形式要点（本工作中的唯一陷阱）**：交叉项系数是 $+[\,(\ln F)_x-(\ln G)_x\,]^2$，
> 即 $+1$ 倍。它**既不是** $0$（那是写成 $(\ln F)_{xx}+(\ln G)_{xx}$ 的误记），
> **也不是** $\pm2$（$\pm2$ 属于 $(\ln(FG))_{xx}$ 的展开，是另一个量）。
> `idcheck3.py` 用 sympy 在任意符号 $F(x),G(x)$ 上把系数解出，唯一解为
> $(c_1,c_2,c_3)=(1,1,1)$。

### 8b.2 势函数方程

取 $\theta_j=\ln F_j-\ln G_j$，$\Psi_j=\ln F_j+\ln G_j$。由 (H1) 与
$(7)_h/(F_jG_j)$，参数 $s:=a-d$：

$$
\boxed{\;
(\mathrm{A})_h:\quad
\Psi_{j,xx}+\theta_{j,x}^2+\theta_{j,t}+2(a-d)\,\theta_{j,x}=0
\;}
\tag{A}
$$

同理 $(6)_h/(F_jG_{j+1})$，记 $\Theta_j=\ln F_j-\ln G_{j+1}$：

$$
(\mathrm{B})_h:\quad
\Phi_{j,xx}+\Theta_{j,x}^2+\Theta_{j,t}+2(a+d)\,\Theta_{j,x}=0
\tag{B}
$$

方程的**全部系数**（包括那个看起来像非线性的 $\theta_x^2$）都已在
$N=1$（三组参数）与 $h=1/4,1/8$ 下精确验证为零。

### 8b.3 物理变量与非线性格点方程

$$
u_j:=2\,\theta_{j,x},\qquad w_j:=2\,\Psi_{j,x}
$$

则 $(\mathrm{A})_h$ 乘以 2 成为真正的**非线性微分-差分方程**

$$
\boxed{\;
u_{j,t}+w_{j,x}+\tfrac12 u_j^2+2(a-d)\,u_j=0
\;}
\tag{A'}
$$

这正是 DLW 第一式 $u_t+v_x+uu_x+2au=0$ 的格点/势形式（$w\leftrightarrow v$）。
$(\mathrm{B})_h$ 给出相邻位点上的同一方程（参数 $a+d$）。

### 8b.4 连续极限

`nlcont.py`：

| $h$ | $(\mathrm{A})_h$ 残差 | 把 $a-d$ 换成 $a$ 后的残差 |
|---|---|---|
| $1/2$ | $2.455\times10^{-90}$ | $0.24341$ |
| $1/4$ | $4.909\times10^{-91}$ | $0.117611$（比 0.483） |
| $1/8$ | $5.891\times10^{-90}$ | $0.0578331$（比 0.492） |
| $1/16$ | $-3.436\times10^{-90}$ | $0.0286794$（比 0.496） |
| $1/32$ | $-4.418\times10^{-90}$ | $0.0142811$（比 0.498） |

即：$(\mathrm{A})_h$ **恒为零**，而把 $a-d$ 还原为 $a$（连续参数）后残差
$\propto h$（比值 $\to1/2$，一阶），这正是"半离散方程的连续极限给出连续方程"
的标准含义，且 $h\to0$ 时精确恢复

$$
\Psi_{xx}+\theta_x^2+\theta_t+2a\,\theta_x=0 .
$$

### 8b.5 复现

```powershell
python -u nlfinal.py    # (A)_h, (B)_h, 商恒等式 (H1)(H2), 物理形式 (A')
python -u idcheck3.py   # sympy 符号判定系数 (1,1,1)
python -u nlcont.py     # 连续极限与 O(h) 收敛阶
```

---

| 旧报告/旧脚本的说法 | 现状 | 说明 |
|---|---|---|
| `OUT_GSG_DLW_report.md` §3.3(c)：对称二点恒等式 $B_af_{j+1}\cdot g_j+B_af_j\cdot g_{j+1}=0$ | **错**（仅为 $N=1$ 假象） | 旧 `obstruction.py`/`verify_nullvec.py` 只在 `DLW(1,…)` 上搜索验证。$N\ge2$ 时该量非零。正确的连续版本是 $B_af_{j+1}\cdot g_j+B_af_j\cdot g_{j+1}-2B_af\cdot g=0$（`certify.py` §H 在 $N=2$ 确认 HOLDS） |
| `mshift.py`：格点单孤子剖面 = 连续剖面在 $a\to a-h/2$ | **错（已给出反例）** | 正确结论是"$y(1/P+1/Q)\mapsto j\ln\lambda$"的**速率重正化**（§8.1、§8.3）。反例由 `certify.py` §J 给出：$u_{\rm lat}-u_{\rm cont}(a-\tfrac h2)$ 的分子带有整体因子 $Eh$（即非零有理函数），在 $(p,q,a,h,E)=(\tfrac53,\tfrac74,\tfrac32,\tfrac14,2)$ 处等于 $-58273134100141/12500000000000$。解析原因：若真为 $a\to a-h/2$，则分母 $QS-Pe$ 应变为 $(Q-d)S-(P+d)e$，与格点结果 $QS-Pe$ 不符 |
| `certify.py` §E 报 FAIL | 已修 | 原因是用了**未代换**的模块级符号 $d=h/2$，而模型里 $h$ 已被代成有理数；改为 `mm.h/2` 后全部 OK |
| "交错对只是 (7) 在两个参数下的实例" | **澄清（非错误）** | 确实如此，但这不削弱其价值：$[(6)_h-(7)_h]/h$ 恰为 (6)，且该对是模板内唯一精确解（§6） |
| 报告中"对称二点"以外的 §4.2/4.3 交错对结论 | 成立 | 已用独立引擎 `certify.py`/`soliton_lattice.py` 复核 |

---

## 10. 复现方法与文件清单

```
dlw_semidiscrete/
├── engine2.py           独立重写的指数单项式精确引擎（与 gsg_project/code/engine.py 不同代码路径）
├── certify.py           A–J 判定电池（全部 OK）
├── nosearch.py          24 维二点模板的完备零空间搜索（唯一性/no-go）
├── nosearch_uniform.py  均匀类零空间维数随 N 的变化
├── h_scaling.py         均匀类零向量的 h-标度分析（定出 (‡) 的结构）
├── uni_identity.py      显式检验 (‡)：h=1/2 处失败 ⟹ 不是恒等式
├── stag_h.py            交错类零空间在 5 个 h 值上的稳健性
├── test_v2.py           均匀类伪向量的 N-扫描
├── test_v4_N7.py / check_1264.py   正则性排查（脚本，非结论性）
├── soliton_lattice.py   精确 N-孤子 + 结构定理 + 色散 + 精度阶 + 图
├── jet3.py              三变量 (x,t,y) 精确指数单项式引擎（供非线性层使用）
├── nlfinal.py           **非线性层权威验证**：(A)_h,(B)_h,商恒等式,物理形式
├── idcheck2.py / idcheck3.py   sympy 符号判定 Hirota 商恒等式的交叉项系数
├── nlcont.py            连续极限与 h -> 0 收敛阶
├── probe5.py probe6.py probe7.py   身份判定的排查脚本（保留供追溯）
├── debug.py debug2.py debug3.py debug4.py   排查脚本
├── cert_result.txt      判定电池输出
├── no_result.txt / uni_result.txt / hscale.txt / uni_id.txt / stag_h.txt / sol_result.txt
└── soliton_lattice.png  图（单孤子剖面、色散误差、双孤子成分）
```

复现命令（在 `dlw_semidiscrete/` 下）：

```powershell
python -u certify.py          # 全部判定，约 1–2 分钟
python -u nosearch.py         # 唯一性/no-go 搜索
python -u test_v2.py          # N=7 反例（较慢）
python -u soliton_lattice.py  # 孤立子结构与精度
python -u nlfinal.py          # 非线性层：(A)_h,(B)_h,商恒等式,物理形式
python -u nlcont.py           # 连续极限与 O(h) 收敛阶
```

**判定电池摘要**（`cert_result.txt`）：

```
A. 连续基线 (7) 与 (6)@λ=−2                N=1..5  全部 OK
B. (7) 在 y-格点上逐点精确                  N=1..4  位点 0..3 全部 OK
C. N=1 跨位点闭式 2cPE(χ^q−χ^p)             6 组   全部 OK
D. 朴素中心差商：一阶、非精确                N=1..3  均非零（符合预期）
E. 结构恒等式 τ1(j;a−d)=τ1(j+1;a+d)        N=1..4  全部 OK
F. 交错对 (7)_h 与 (6)_h                    N=1..5  位点 0..3 全部 OK
G. 二点形式 (⋆′)                            N=1..4  位点 0..2 全部 OK
H. 2DTL 探针 / 对称二点恒等式                见 §9
I. 唯一性（交错类 dim 4，对 h 稳健）          见 §6.1
J. 旧 (5.2a) 反例（a→a−h/2 的剖面论断）      已否定，见 §9
```

---

## 11. 开放问题

1. **非线性 (L1)(L2) 的数值求解与稳定性**：本文已把 $(\star)$ 回代为真正的非线性
   格点方程 $(u_{j,t}+w_{j,x}+\tfrac12u_j^2+2(a-d)u_j=0$，见 §8b$)$，并给出精确解与
   连续极限；但尚未做有限差分数值实验（守恒量、色散误差、长时间行为）。
2. **Lax 对 / 守恒量**：Gram 行列式给出可积性证据，但格点 Lax 对尚未写出。
3. **K3（离散 hodograph / SAMD）的替代**：DLW 无 hodograph 对称性，
   自适应网格版本是否可能用其他方式（例如时间方向的 Bäcklund 参数梯度）实现，未探讨。
4. **2DTL 探针**：`certify.py` §H 显示 $N=2$ 时
   $\bigl(\tfrac12D_yD_x-1\bigr)\tau_n\cdot\tau_n+\tau_{n+1}\tau_{n-1}=0$ 成立，
   但尚未在 $N=3,4$ 复核，也未查明它与 (7)(6) 的层级关系。
5. **更大的模板**：若把 $\tau_2$、$\tau_{-1}$ 或更远的位点 $(\pm2,0)$ 纳入搜索模板，
   是否会出现新的精确恒等式（即是否存在与 $(\star)$ 不同的半离散化），未知。
6. **多层 Bäcklund 参数梯度**：本文只用 $s=a\pm d$ 的两层交错；
   $s=a\pm kd\ (k\ge2)$ 是否给出更高阶或更对称的系统，未探讨。

---

## 附：核心公式速查

| 量 | 表达式 |
|---|---|
| 格点乘子 | $\lambda(z)=\dfrac{z+d}{z-d},\quad d=\dfrac h2$ |
| 格点速率 | $\Lambda_h(z)=\dfrac1h\ln\lambda(z)=\dfrac2h\operatorname{artanh}\dfrac h{2z}=\dfrac1z+\dfrac{h^{2}}{12z^{3}}+\cdots$ |
| Gram 元 | $m^{(n)}_{ik}(j)=c_k\delta_{ik}+\dfrac1{p_i+q_k}\Bigl(-\dfrac{p_i-s}{q_k+s}\Bigr)^{n}\bigl[\lambda(p_i-a)\lambda(q_k+a)\bigr]^{j}e^{\xi_i+\eta_k}$ |
| 交错对 | $F_j=\tau_1(j;a-d),\quad G_j=\tau_0(j)$ |
| $(\dagger)$ | $F_j=\tau_1(j;a-d)=\tau_1(j+1;a+d)$ |
| $(7)_h$ | $B_{a-d}F_j\cdot G_j=0$ |
| $(6)_h$ | $B_{a+d}F_j\cdot G_{j+1}=0$ |
| $(\star')$ | $\dfrac1hB_{a-d}F_j\cdot(G_{j+1}-G_j)+2D_xF_j\cdot G_{j+1}=0$ |
| 连续极限 | $(7)$ 与 $B_af\cdot g_y+2D_xf\cdot g=0$，均为二阶 |
| 单孤子场 | $u_j=\dfrac{-2S^{3}e_j}{(S+e_j)(QS-Pe_j)},\quad S=p+q,\ P=p-a,\ Q=q+a,\ e_j=E\lambda^{j}$ |
| 相互作用系数 | $\kappa=\dfrac{(p_1-a)(p_2-a)(p_1-p_2)(q_1-q_2)}{(a+q_1)(a+q_2)(p_1+q_1)(p_1+q_2)(p_2+q_1)(p_2+q_2)}$（与 $h$ 无关） |
| Hirota 商恒等式 | $\dfrac{D_x^2F\cdot G}{FG}=(\ln F)_{xx}+(\ln G)_{xx}+[(\ln F)_x-(\ln G)_x]^2$ |
| 势函数 | $\theta=\ln(F/G),\ \Psi=\ln(FG)$ |
| 势方程 $(A)_h$ | $\Psi_{j,xx}+\theta_{j,x}^2+\theta_{j,t}+2(a-d)\theta_{j,x}=0$ |
| 物理变量 | $u_j=2\theta_{j,x},\ w_j=2\Psi_{j,x}$ |
| 非线性格点方程 $(A')$ | $u_{j,t}+w_{j,x}+\tfrac12u_j^2+2(a-d)u_j=0$ |
| 连续极限 | $\Psi_{xx}+\theta_x^2+\theta_t+2a\theta_x=0$（$h\to0$，误差 $O(h)$） |
