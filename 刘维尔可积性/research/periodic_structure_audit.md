# 原半离散 DLW 周期场结构独立审计

2026-10-11。数学范围：有限格点周期 $M\ge2$、连续周期 $x\in\mathbb R/(\ell\mathbb Z)$、$h>0$、实光滑场、$c\ne0$ 正则分支及 $c=0,\Gamma\ne0$ 正则约束分支。结论依赖逐节所列假设。有限符号检查仅作核验；实际解流、局部谱像逆与无限维 Liouville 完备性分别说明。

## 1. 依赖定位与总判断

已读指定的 `RESEARCH_NOTES.md`、`CONSERVATION_FAMILY_VERDICT.md`、`GENERAL_PERIOD_FREE_FIELD_POISSON.md`、`GENERAL_PERIOD_MATRIX_LAX.md`、`dlw_field_liouville_20261006/THEORY.md`，以及实际依赖：

- `Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md`；
- `Workspaces/dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md`；
- `Workspaces/dlw_field_liouville_20261006/INDEPENDENCE.md`；
- `general_period_free_fields_certificate.py`、`general_period_matrix_certificate.py`、`periodic_monodromy_check.py`、`poisson_pushforward_certificate.py`、`verify_monodromy_hierarchy.py`、`verify_independence_filtration.py`；
- `Workspaces/dlw_mean_modes_20261008/verify_dlw.py`、`TWO_SITE_POISSON_PENCIL.md`，及总报告 §13.4。

THEORY.md 将 MONODROMY_POISSON_PROOF.md 写成同目录依赖，实际文件位于上述 conservation workspace 的 lax/ 下，故此处存在引用路径断链。实际证明第 3–5 节包含因子乘积/逆算法、迹梯度、平均约束切向性、共同 $U$ 规范不变量的链式法则；以下独立重算与其吻合。

**结论：未发现 $c\ne0$ 正则周期分支上“全部谱迹在同一个 $J_{\rm red}$ 下对合”的实质性错误。** 这一结论依赖冻结外延常量、正确的 Poisson 商解释及原方程/全 intertwiner 对应。一般矩阵坐标证明本身并不能代替谱对合证明。固定 $\gamma$ 是额外闭合或时间移动坐标规范，原方程不推出 $\gamma_t=0$。全场 Liouville 完备性仍未由独立对合族推出。

## 2. 原方程与平均自由模

令 $D=\partial_x$、$d=(1-E^{-1})/h$、$M_-=(1+E^{-1})/2$、$\beta=h^2/32$。实际方程为

$$
d\{U_t+D(U^2/2+\beta w^2)\}+D^2(dU+M_-w)=0,
\qquad w_t=-D(Uw)+D^2w.
$$

连续周期边界先给 $D^2\Pi w=0$，所以 $\Pi w=c(t)$ 空间恒定；第二式给 $c_t=0$ 和 $D\Pi(Uw)=0$。因此

$$
\Pi w=c,\qquad\Pi(Uw)=q(t)
$$

中的 (q$t$) 是任意时间自由模。写 $p=P_0U,s=w-c,z=\Pi(ps)$，则

$$
U=p+\frac{q(t)-z}{c},\qquad w=c+s.
$$

原 `periodic_reduction.md` 已明确指出这一点，并给出

$$
\widetilde U(x,t)=U(x-A(t),t)+A'(t),\quad
\widetilde w(x,t)=w(x-A(t),t),\quad \widetilde q=q+cA'.
$$

这保留任意 $p,s$ 函数自由度。固定 $q=\gamma$ 可视为时间坐标规范；不能把它宣称为原物理方程自动满足的守恒定理。更强且不必固定 $q$ 的表达式为：$K_q=K_0+(q/c)P_{\rm mom}-hM\ell q^2/(2c)$，$X_{P_{\rm mom}}=-D(p,s)$。平移不变的 $K_0$ 守恒族可保留于任意 (q$t$) 的实际场分支。

## 3. 原场括号与谱对合的独立全阶证明

### 3.1 因子括号：归一化和符号

采用普通不带权的变分导数时，未约束辅助场的常括号为

$$
J_{\rm amb}=-\frac1h\begin{pmatrix}0&D\\D&0\end{pmatrix}.
$$

这与 $h\sum_j\int$ 配对下的 `J0=-offdiag$D$` 相同。设

$$
b_j=U_j/2,\quad d_j=hw_j/8,\quad a_j^+=b_j+d_j,\quad a_j^-=b_j-d_j.
$$

直接线性变换给

$$
\{b_i,d_j\}=-\tfrac1{16}\delta_{ij}D,\quad
J_{a^+a^+}=-\tfrac18D,\quad J_{a^-a^-}=+\tfrac18D,\quad J_{a^+a^-}=0.
$$

Adler 映射记作

$$
\mathcal A_K(X)=(KX)_+K-K(XK)_+.
$$

第一阶因子 $K=D+v$ 的系数括号为 $-D$：取 $X=D^{-1}\phi$，直接得 $\mathcal A_K(X)=-\phi_x$。因此 $D-a^+$ 带 $+\frac18\mathcal A$，而 $D-a^-$ 带 $-\frac18\mathcal A$。求逆使 Adler 括号变号。两个独立因子满足

$$
\mathcal A_{KH}(X)=\mathcal A_K(HX)H+K\mathcal A_H(XK),
$$

由展开加号投影即可验证。故

$$
T_j=(D-a_j^-)^{-1}(D-a_j^+),\qquad
P=T_{M-1}\cdots T_0
$$

继承 **$\frac18\mathcal A_P$**。这一符号和 $1/h$ 不能混用两格点的 $K/(2h)$ 归一化。

相关一手文献是 [Mas–Ramos, The Constrained KP Hierarchy and the Generalised Miura Transformation, Theorems I/II](https://arxiv.org/html/q-alg/9501009v2)。本文使用其乘积/求逆框架，同时上面给出本 DLW 因子的实际系数计算。该文也明确区分去掉首系数的约束与未经约化的 Adler 括号，不能用其定理名跳过这里的规范约化。

### 3.2 冻结外延常量后的全部迹对合

设

$$
G=hMc/4\ne0,\quad B=\gamma/(2c),\quad \nu=B-G/2,
\quad L=\nu-G(P-I)^{-1},\quad C_n=\frac1n\operatorname{Tr}L^n.
$$

在求未约束变分时，**$G,B$ 必须作为数值常量冻结**。这不是把离开约束面后的实际 $\Pi w$、$\Pi Uw$ 代回它们；后者会随 $x$ 变，破坏下面的对易和因子论证。

若 $A=(P-I)^{-1}$，则

$$
\delta L=G A\delta P A,\quad
X_n=\nabla_PC_n=G A L^{n-1}A,\quad [X_n,P]=0.
$$

于是

$$
\{C_m,C_n\}_{\rm amb}
=\tfrac18\operatorname{Tr}X_m[(PX_n)_+,P]=0.
$$

迹循环性是周期系数的有限阶 residue 恒等式，不要求整个形式 PDO 级数收敛。每个固定阶的 $C_n$ 都是实际有限微分函数。

### 3.3 保持平均约束与时间流对应

代数恒等式给

$$
PX_n=\frac1G\big[L^{n+1}-2B L^n+(B^2-G^2/4)L^{n-1}\big].
$$

定义右端的微分部分为 $Q_n$。则

$$
X_{C_n}L=\tfrac18[Q_n,L].
$$

也可直接用 $[PX_n,P]=0$ 写

$$
X_{C_n}P=-\tfrac18[(PX_n)_-,P-I].
$$

两个右端因子均为标量负阶，其领先系数对易，故交换子阶数至多 $-3$。因此 $P$ 的 $D^{-1},D^{-2}$ 系数点态不变，恰好保持 $\sum g_j=G$ 和 $\sum U_jg_j=2BG$，其中 $g_j=2d_j=hw_j/4$。这是全阶约束切向性的独立证明。

利用已核对的密度恒等式

$$
K=-8G C_1+2B P_{\rm mom}+\text{constant},\qquad
P_{\rm mom}=h\sum_j\int p_js_j,
$$

以及目标物理括号下 $X_{P_{\rm mom}}L=-[D,L]$，得到

$$
L_t=-[(L^2)_+,L].
$$

此计算与实际 `MONODROMY_POISSON_PROOF.md` 中全 intertwiner 的 $-D^2-V_0$ Lax 流吻合；其零阶项还给 $D V_0=2D\ell_1$。

### 3.4 真正的 Poisson 商，而非任意 observable 的简单限制

任意共同周期函数平移 $U_j\mapsto U_j+2f(x)$ 使所有因子、$P,L$ 由同一乘法函数 $k$ 共轭，其中 $k_x/k=f$。$k$ 自身可准周期。对任何标量 PDO $H$，

$$
\operatorname{res}(kHk^{-1})=\operatorname{res}H
$$

**点态成立**：微分部分保持微分，负阶只有原 $D^{-1}$ 项可贡献新 $D^{-1}$ 项。故

$$
\sum_j\frac{\delta C_n}{\delta U_j}=0.
$$

对约束重构 $U=p+(\gamma-\Pi ps)/c,w=c+s$ 求链式法则，便有

$$
(C_n)_p=(C_n)_U,\qquad (C_n)_s=P_0(C_n)_w.
$$

带 $P_0$ 的物理常括号与 ambient 常括号对这些泛函给完全相同的结果，故全部 $C_n$ 在

$$
J_{\rm red}=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix}
$$

的 $h\sum\int$ 配对下确实对合。

更准确的几何解释：先取 ambient 共同 $U$ 平移作用的 Poisson 不变量代数。它由 $p=P_0U,w$ 描述，$\Pi w$ 在该代数中为 Casimir；取 $\Pi w=c$ 后得到 $p,s,J_{\rm red}$。条件 $\Pi Uw=\gamma$ 给这个商选取全局截面。这样无需错误地求周期 $D$ 的双侧逆。

不能将任意 ambient 泛函直接限制到截面，并声称限制映射都是 Poisson。明确反例是

$$
F=h\sum_j\int U_j\quad\text{在 ambient 括号下为 Casimir},
$$

但截面上

$$
F=hM\ell\gamma/c-P_{\rm mom}/c,
\qquad X_{F|\mathrm{section}}=D(p,s)/c,
$$

通常不为零。$F$ 对共同 $U$ 平移并不不变。这不是谱迹对合的反例，而是“所有物理量都是 ambient Dirac 简单限制”的反例，尤其指出其零模问题。

## 4. 矩阵自由场坐标核对

令 $m=M-1$，$Z=(e_j-e_m)_{j<m}$，$E$ 取前 $m$ 个分量。自由场 $q_j,d_j$ 的 Frechet 矩阵为

$$
F_* = \begin{pmatrix}Z^T/2&hK_d/8\\0&hE/8\end{pmatrix},
\quad (K_d)_{jk}=-\delta_{jk}-2\mathbf1_{k>j}+\delta_{km}.
$$

对于 $j,k<m$，

$$
(K_dZ)_{jk}=1-\delta_{jk}-2\mathbf1_{k>j},
$$

为严格反对称矩阵；同时 $Z^TP_0E^T=I$。故全 $M$ 直接推出

$$
F_*J_{\rm red}F_*^T=-\frac h{16}
\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix}.
$$

用不带权导数即 $\{q_i,d_j\}=-\delta_{ij}D/16$。逆重构只除以 $S=G/2$，不需要个别 $d_j\ne0$。指定文件这一部分正确。

本次独立 SymPy 1.13.3 检查 $M=2,\ldots,20$ 的矩阵等式全部通过；证明依据是上面的全 $M$ 三个矩阵恒等式，而不是 19 个测试。

矩阵内部联络 $V$ 及其 holonomy 必须保留。任意内部规范

$$
q\mapsto qH^{-1},\quad r\mapsto Hr,\quad
V\mapsto HVH^{-1}+H_xH^{-1}
$$

保持标量 $q(DI-V)^{-1}r$ 不变。因此“全矩阵系数能重构物理场”不能直接推出“谱特征值能重构物理场”。下面给出进一步缩小此缺口的正向结果。

## 5. 新的全周期观测性证明

### 5.1 明确的循环向量图

一般场定义行

$$
Q_0=q,\quad Q_{k+1}=DQ_k+Q_kV,\quad
\mathcal O=\begin{pmatrix}Q_0\\\vdots\\Q_{m-1}\end{pmatrix}.
$$

在 $\det\mathcal O\ne0$ 的图上，以 $\zeta=\mathcal O\xi$ 代换内部系统，得到 companion 联络

$$
W=(D\mathcal O+\mathcal O V)\mathcal O^{-1},\quad
\widetilde q=(1,0,\ldots,0),\quad \widetilde r=\mathcal O r.
$$

这是一条具体的局部有理微分变换，保留一般函数场；不需要把内部 holonomy 设置为零。

统一背景取 $b_j=B,d_j=\delta\ne0$，所以 $S=M\delta$、$G=2M\delta$。则

$$
q_j=-2\delta(m-j),\quad
V=(B-\delta)I-2\delta H-\frac1M\mathbf1 q,
$$

其中 $H_{ij}=\mathbf1_{j<i}$。行 $qV^k$ 与 $q[(B-\delta)I-2\delta H]^k$ 仅相差较低阶行的线性组合，最高阶系数为 1；再移除标量对角项，求行列式只需 $qH^k$。Hockey-stick 恒等式给

$$
(qH^k)_j=-2\delta\binom{m-j}{k+1}.
$$

逆序 Pascal 矩阵行列式为 $(-1)^{m(m-1)/2}$，行缩放积为 $(-2\delta)^{m(m+1)/2}$。所以

$$
\boxed{\det\mathcal O=(-1)^m(2\delta)^{m(m+1)/2}\ne0.}
$$

这是任意 $M$ 的证明。在统一背景附近的周期 $C^r$ 开图上，此行列式仍逐点非零。有限检查 $M=2,\ldots,10$、$\delta=1$ 的值依次为 $-2,8,-64,1024,-32768,2097152,-268435456,68719476736,-35184372088832$，与公式一致。

背景标量谱函数为

$$
P(z)=\left(\frac{z-B-\delta}{z-B+\delta}\right)^M,
\qquad L(z)=B-M\delta-2M\delta(P(z)-1)^{-1}.
$$

其约简分母为

$$
(z-B-\delta)^M-(z-B+\delta)^M,
$$

阶数 $M-1$，与分子互素：分母根处 $z-B+\delta\ne0$，分子项 $-2M\delta(z-B+\delta)^M\ne0$。根也互异，由非平凡 $M$ 次单位根的 Möbius 参数化可见。因此附近有最小阶 $M/(M-1)$ 的有理 PDO 图，统一背景不是一个少于 $m$ 个内部模式的退化 realization。

### 5.2 固定平均叶上的标量谱微分无核

在上述背景取非零 Fourier 参数 $\kappa=2\pi i k/\ell$，$t=z-B$，

$$
S(t)=\frac{t-\delta}{t+\delta},\quad
R(t)=\frac{S(t+\kappa)}{S(t)}.
$$

设场变分为 $e^{\kappa x}(\dot b_j,\dot d_j)$。有

$$
\dot T_j(z)=\frac{(S(t)-1)\dot b_j-(S(t)+1)\dot d_j}{t+\kappa+\delta}.
$$

按实际有序乘积插入，令

$$
A(R)=\sum_{j=0}^{M-1}\dot b_jR^{M-1-j},\quad
C(R)=\sum_{j=0}^{M-1}\dot d_jR^{M-1-j},
$$

得到

$$
\dot P(z)=-\frac{2S(t)^{M-1}}{(t+\delta)(t+\kappa+\delta)}
\big[\delta A(R(t))+tC(R(t))\big].
$$

关键是 $R(-\kappa-t)=R(t)$。若 $\dot P\equiv0$，同时代入 $t$ 和 $-\kappa-t$，相减给

$$
(2t+\kappa)C(R(t))=0.
$$

因为 $\kappa\delta\ne0$，$R(t)$ 非恒定，所以 $C$ 是零多项式，再得 $A$ 是零多项式。所有格点变分均为零。Möbius 归一化的导数可逆，故 $\dot L=0$ 同样推出 $\dot p=\dot s=0$。零 Fourier 参数恰是固定分量平均值所排除的方向。

这证明物理场到**完整标量算子**的 Frechet 微分在统一背景的固定均值叶上无核。它不是迹积分的微分无核：统一背景处这些积分的一阶变分通常仍消失，不能混淆算子信息与积分信息。独立有理函数 rank 检查 $M=2,\ldots,7$、$\delta=1,\kappa=i$ 得 $2,4,6,8,10,12$，全阶证明是前面的两支代入论证。

## 6. 对 nonlinear 局部像逆的独立复核

此部分独立审查非线性局部谱像逆构造，给出因子反交换、分母恢复与周期旗标的实际论证。

### 6.1 交换、反交换与平均值

对实周期 $a,b$ 且 $a-b$ 不为零，令 $\theta=D\log|a-b|$。则

$$
(D-a)(D-b)^{-1}=(D-b-\theta)^{-1}(D-a-\theta).
$$

将左右乘回微分因子，零阶差为

$$
-a_x+b_x+\theta(a-b)=0,
$$

一阶、二阶系数也一致。更新后的两个场为 $a+\theta,b+\theta$，差仍是 $a-b$，故同式重算 $\theta$ 可唯一反交换。周期非零差使 $\int\theta=0$，所以每个有序 factor 的平均值保持。统一背景所有异类交换差为 $2\delta\ne0$；有限 bubble sorting 及其反序在充分小的周期 $C^r$ 邻域内都有效。

于是原交错乘积可变成 $P=Q^{-1}R$，其中 $Q,R$ 为首一 $M$ 阶微分算子，统一背景分别为 $(D-B+\delta)^M,(D-B-\delta)^M$。factor label 顺序必须保持，不能任意重排。

### 6.2 从同一个标量 $P$ 唯一恢复 $Q,R$

令 $Q=D^M+\sum_{i=0}^{M-1}q_iD^i$。方程 $QP$ 的前 $M$ 个负阶系数消失，给 $q_i$ 的点态线性方程，未知量本身不被求导。经过常数谱平移使背景 $B-\delta=0$，有

$$
P_*(D)=(1-2\delta D^{-1})^M,
\quad (A_*)_{r,i}=p_{r+i},\ 1\le r\le M, 0\le i<M.
$$

该矩阵反三角，反对角 $p_M=(-2\delta)^M$，所以

$$
\det A_* =\pm(-2\delta)^{M^2}\ne0.
$$

附近以有限 $P$ 系数和其导数恢复唯一 $Q$，再 $R=(QP)_+$。对于原物理像，bubble construction 保证剩余全部负阶也消失。此直接唯一性已经足够；无需另导入非交换 Bezout 的存在定理。adjoint Sylvester/Bezout 论证也可作为该邻域中的另一证明，但不是此处的必要依赖。

### 6.3 Floquet 旗标及周期 Wronskian

固定物理 $p,s$ 分量均值只固定因子平均值的差。**共同平均值不固定**：

$$
\chi=\operatorname{avg}_x\Pi(U/2)
=\frac\gamma{2c}-\frac{P_{\rm mom}}{2hM\ell c}.
$$

在零分量均值叶，各 $a_j^+$ 的平均为 $\chi+\delta$，各 $a_j^-$ 为 $\chi-\delta$。因此 $Q,R$ 的唯一重复 Floquet 倍子分别为

$$
\mu_Q=e^{(\chi-\delta)\ell},\qquad
\mu_R=e^{(\chi+\delta)\ell}.
$$

它们随动量变化；只有比值固定。若额外固定动量才能把它们当整叶常数，这并非原 Casimir。比对 same $P$ 时，same $Q,R$ 决定其首系数积分，继而决定 same $\chi$，再结合原分量均值差，决定 same 有序 factor 平均值。上述比较只要求同一谱像，不额外固定 $\chi$。

在统一背景，$Q$ 或 $R$ 的 Floquet 矩阵是一个正实特征值乘单 Jordan block 的指数。cyclic 性为开条件；在实际物理像中重复谱保持，所以邻近仍为单 Jordan block。唯一全不变旗标为

$$
E_k=\ker(T-\mu I)^k,
$$

其秩恰为 $k$。在固定秩 minor 图上，这些空间随 ODE 系数光滑变化；共同特征值用实际 $(\det T)^{1/M}$ 的正实分支恢复，不能预设背景值。

旗标的 monic annihilator 从周期解 Wronskian 得到。统一背景 $E_k$ 由 $e^{ax},xe^{ax},\ldots,x^{k-1}e^{ax}$ 张成，Wronskian 为非零常数乘 $e^{ka x}$。紧致 $x$ 圆上 ODE 连续依赖保证充分近邻每个 Wronskian 持续非零。它们虽可准周期，但

$$
W_k(x+\ell)=\det(T|E_k)W_k(x),\qquad
v_k=D\log|W_{k+1}/W_k|
$$

给出的因子系数周期。依次恢复有序 $Q,R$ 因子，再反交换，恢复原 $a^+,a^-$，于是恢复全部一般物理场。

**独立认可范围：** 统一背景附近、固定物理分量均值的 $C^\infty$ 图中，完整标量 $P$/$L$ 对物理场有局部非线性像逆。前向和逆构造包含有限但可能较高阶的微分以及有限阶周期 ODE，故可说 smooth/tame 的像逆；必须给足有限 $C^r$ 近邻控制 gap、linear recovery minor、cyclic minor、Wronskian。不能据此宣称固定单一 Sobolev 空间中的 Banach onto 局部微分同胚，也不能据此宣称谱迹或谱特征值完整。

## 7. 任意 scalar gradient 的 Möbius Poisson 张量

这补足“先有全张量，后对迹梯度取特例”的一步，但仍须与 physical 规范约化分开。

对一般梯度 $Y=\nabla_LF$，不假设 $[Y,P]=0$。设 $K=L-\nu$，则

$$
\delta L=G^{-1}K\delta P K,\qquad
X=\nabla_PF=G^{-1}K Y K.
$$

由 $P=1-GK^{-1}$ 精确推得

$$
\boxed{J_L^{\rm amb}(Y)=\frac1{8G^2}\left[
K\big((K-G)YK\big)_+(K-G)
-(K-G)\big(KY(K-G)\big)_+K\right].}
$$

它是任意标量泛函的 ambient 推前，不使用迹对易。定义

$$
\begin{aligned}
T_{1,L}(Y)&=[Y_+,L]+[L,Y]_+,\\
T_{2,L}(Y)&=(LY)_+L-L(YL)_+,\\
T_{3,L}(Y)&=[(LYL)_+,L]+L[L,Y]_+L,
\end{aligned}
$$

设 $H=L-B,a=G/2$，展开上述矩阵外的纯标量投影运算给

$$
J_L^{\rm amb}=\frac1{8G}
\left[T_{3,L}-2BT_{2,L}+(B^2-G^2/4)T_{1,L}\right].
$$

证明只需展开 $(H-a)Y(H+a)=HYH+a(HY-YH)-a^2Y$ 以及对换式，再用 $T_{3,L-B}=T_{3,L}-2BT_{2,L}+B^2T_{1,L}$。因此三项多项式并非只在 commuting trace gradients 上成立。

**尚不可跳过的一步：** 这是未约束 Möbius ambient 张量。一般 $Y$ 会改变 $L$ 的领先系数或零阶项；物理场固定 $\Pi w=c$、$\Pi Uw=\gamma$ 对应 $L=D+O(D^{-1})$。必须先采用共同 $U$ 共轭不变量的泛函外延，再投影/规范固定。确切有

$$
\operatorname{coeff}_{D^{-1}}J_P(X)=\operatorname{res}[L,Y].
$$

故 $\operatorname{res}[L,Y]=0$ 控制固定领先系数，**不能仅凭它忽略共同零模**。一个普适的实际 Poisson 张量始终是物理 Frechet 推前 $F_*J_{\rm red}F_*^*$；要把它写成上述三项的约化版本，需明确 monic/零阶规范投影及周期均值项。当前没有完成这些定义域和零模步骤，不能把该 ambient 公式直接宣称为已完成的全 $M$ physical 三张量匹配。

## 8. 可直接推进的成果与尚缺依赖

1. 全部谱迹与真正 $J_{\rm red}$ 的对合已由独立全阶计算复核；无个别 $w_j\ne0$ 假设，无有限维场截断，也不需要丢掉 holonomy。
2. 同一个谱结构包含实际 Hamiltonian 和平移动量；一般 $q(t)$ 可通过时间平移规范及规范归一化谱族保留，而无需强制固定平均通量。
3. 全 $M$ 观测性行列式给一般函数场的显式开放 companion 图；标量谱微分在统一背景固定平均叶上无核。
4. 非线性局部像逆的交换/分母恢复/旗标/Wronskian/反交换链条已独立核对。它保留完整函数自由度，且明确排除了将动量依赖共同平均值误作 Casimir。
5. 任意 scalar gradient 的全 $M$ ambient Möbius 张量已明确导出；它为下一步 scalar physical 规范约化提供具体算式。

尚缺：scalar 规范约化的完整三张量表示及零模项；物理谱数据对应的逆 Floquet/谱变换定理；相应 symplectic form 的全场拉回；在指定拓扑中由 commuting Hamiltonian directions 的闭包等于其 symplectic orthogonal（最大各向同性），或等价的谱完备性证明；可承载物理时间与整个层级的实际解空间。既有线性高频增长 $e^{tk^2}$ 仍阻碍通常 Sobolev/ $C^\infty$ 正时间开放解流，但不取消以上代数、局部像逆和 commuting hierarchy 的正向结果。

以上有限检查只作一致性支持；全 $M$ 断言均在对应节给出恒等式或完整论证。独立性原稿的 filtration、局部 patch 与 Baire 方法与本审计未发生矛盾，但它仍只证明任意有限族独立，不能代替最后的 Liouville 完备性依赖。

## 9. 继续推进：零平均 $w$、非零 $\Gamma$ 的谱迹层级

此节讨论进一步的正则约束分支。它不在旧 $G\ne0$ 定理的假设内，但以下计算不除以 $c$。

### 9.1 真正的约束面及物理闭合

设

$$
\Pi w=0,\quad U=p+b\mathbf1,\quad w=s,\quad
\Pi p=\Pi s=0,\quad q(x)=\Pi(ps).
$$

原平均兼容要求 $Dq=0$。保留 $\Gamma=\operatorname{avg}_xq$ 为状态变量，施加约束 $q(x)-\Gamma=0$，不把平移动量固定掉。取正则子分支 $\Gamma\ne0$。投影方程直接给

$$
q_t=D[-2\Gamma b+\chi],
$$

其中

$$
\chi=-\Pi(p^2s)-\frac{2\beta}{3}\Pi s^3
+\Pi(p s_x-s p_x)-\Pi(sRs_x).
$$

周期边界强制 $\Gamma_t=0$，并确定

$$
b=\frac{\chi}{2\Gamma}+B(t).
$$

因此非零 $\Gamma$ 是实际原方程的守恒模，这与 $c\ne0$ 时任意 $q(t)$ 不同。$B(t)$ 仍为任意时间平移速度。

在 $p,s$ 的常括号 $J_{\rm red}$ 下定义

$$
F_f=h\sum_j\int f(x)p_js_j=hM\int f q.
$$

其流为 $p_t=-D(fp),s_t=-D(fs)$，所以

$$
q_t=-f q_x-2f_xq.
$$

在约束面 $q=\Gamma$ 上，非恒定约束的配对算子正是 $-2\Gamma D$（若使用普通不带权 $f,g$ 配对，整体为 $hM$ 倍）。它在零 $x$ 均值模式上可逆。零模式必须保留：

$$
P_{\rm mom}=F_1=hM\ell\Gamma
$$

生成平移，而非 Casimir。Dirac 约化只处理 $q-\Gamma$ 的非恒定模式，不应把 $\Gamma$ 固定/再商掉作为整个主相空间。

### 9.2 任意约束测试流的严格因子协变

在 ambient $U,w$ 常括号中暂写 $F_f=h\sum\int fUw$。其流为

$$
U_t=-D(fU),\qquad w_t=-D(fw).
$$

于是 $a_j^\pm{}_t=-D(fa_j^\pm)$。对任一微分因子 $A=D-a$，精确有

$$
A_t=-[fD,A]-f_xA.
$$

对 $T=B^{-1}A$，两因子上的 $f_x$ 项消去：

$$
T_t=-[fD,T],\qquad P_t=-[fD,P].
$$

这已独立展开核对，未用 $c\ne0$。所以任何冻结标量归一化参数后的周期谱迹，若作为 $P$ 的共轭协变函数定义，都对全部 $F_f$ 对合；它的 Hamiltonian 流保持 $q(x)$ 点态不变。

### 9.3 二阶逆单值算子的形式平方根

在此分支

$$
P=1+aD^{-2}+p_3D^{-3}+\cdots,\qquad
a=p_2=-hM\Gamma/8\ne0.
$$

定义

$$
\mathcal L=\big[a(P-I)^{-1}\big]^{1/2},\qquad
\mathcal L=D+u_0+\ell_1D^{-1}+\cdots,
\quad \mathcal C_n=\frac1n\operatorname{Tr}\mathcal L^n.
$$

取领先系数 $+1$ 的唯一形式根；每个固定 $n$ 的密度只涉及有限阶 $P$ 系数和导数。负 $a$ 也不成问题，因为 $a/p_2=1$。在 $p_1=0$ 子面的附近，允许 $p_2(x)$ 同符号非零且冻结数值 $a$，则领先系数为 $+\sqrt{a/p_2(x)}$，根仍局部光滑。

**不可错误外延：** $p_1\ne0$ 时 $(P-I)^{-1}$ 改为一阶，平方根为半阶，而不是附近的一阶 PDO。因此上述定义不能直接称为一般 ambient 邻域的一阶算子函数。正确方法是在 $p_1=0$ 子面求切向梯度，并选其有限 conormal 外延。

固定 $a$，对切向变分 $\delta p_1=0$ 有

$$
\delta(\mathcal L^2)=-a(P-I)^{-1}\delta P(P-I)^{-1}.
$$

迹循环性给

$$
\delta\mathcal C_n
=\tfrac12\operatorname{Tr}\mathcal L^{n-2}\delta(\mathcal L^2)
=\operatorname{Tr}X_n\delta P,
\qquad \boxed{X_n=-\frac1{2a}\mathcal L^{n+2}.}
$$

此代表与 $P$ 对易。$P$ 为零阶，其负阶梯度尾既不参与变分配对也不参与 Adler 映射，故仅有限 $X_{n,+}$ 就足够。具体可先把有限密度以 $p_2,p_3,\ldots$ 外延到 ambient coefficient space，再补 $\int p_1\eta_n$，使它在 $p_1=0$ 的正常梯度等于所选 $X_n$。两者切向导数相同，所差恰为 $p_1$ 的 conormal；$\eta_n$ 涉及有限阶系数与导数。这是可审计的局部有限泛函外延，不假定不存在的一阶根外延。

于是相同的 factor Adler 恒等式在该子面给

$$
\{\mathcal C_m,\mathcal C_n\}_{\rm amb}
=\tfrac18\operatorname{Tr}X_m[(PX_n)_+,P]=0.
$$

共同 $U$ 平移又使 $\mathcal L$ 标量共轭，故 $\sum_j(\mathcal C_n)_{U_j}=0$。这些迹可传到 mean-$w$ 零的 $p,s$ Poisson 商。

对 $F_f$ 的流，$p_1=0$ 子面本身保持；虽然 $p_2$ 可随 $x$ 变化，冻结 $a$ 的根仍存在并满足 $\mathcal L_t=-[fD,\mathcal L]$。因此 $\{\mathcal C_n,F_f\}=0$ 严格成立。每个 trace Hamiltonian 场都保持 $q(x)$，所以 $q-\Gamma$ 非恒定约束的 **Dirac 修正项对全部这些迹恒为零**。

### 9.4 采用实际 $\Gamma$ 时的归一化零模

主相空间应取 $a=-hM\Gamma/8$ 的实际状态值，而不是固定 $\Gamma$。链式法则增加

$$
\frac{\partial\mathcal C_n}{\partial a}\,da
=\frac{n\mathcal C_n}{2\Gamma}\,d\Gamma.
$$

这里 $\partial_a\mathcal C_n=n\mathcal C_n/(2a)$，因为冻结场系数时 $\mathcal L$ 按 $\sqrt a$ 缩放。该修正为常数泛函倍数的平移方向。谱迹平移不变，且冻结迹已经对 $F_1$ 对合，所以加入实际归一化后，全部迹对合保持。其 $q(x)$ 约束导数新增项正比于 $q_x$，在 $q=\Gamma$ 上仍为零。不能把这一步含糊称为“冻结实际 $\Gamma$ 后完成”，否则会漏掉原物理动量。

### 9.5 守恒性与两种闭合的 Hamiltonian 区别

不含 $b$ 的基础物理 Hamiltonian 为

$$
H_* =h\sum_j\int\left[\frac12p_j^2s_j+\frac\beta3s_j^3
+s_jp_{j,x}+\frac12s_j(Rs_x)_j\right].
$$

积分分部给

$$
\overline\chi=-\frac{2H_*}{hM\ell},\qquad
P_{\rm mom}=hM\ell\Gamma.
$$

Dirac 约束是 $q-\Gamma=0$ 的非恒定空间模，故约束乘子取零空间平均。基础 $H_*$ 的 Dirac 流选择

$$
b_D=\frac{\chi-\overline\chi}{2\Gamma}
=\frac{\chi}{2\Gamma}+\frac{H_*}{P_{\rm mom}},
\qquad \overline b_D=0.
$$

必须区分以下两种闭合。

若预先规定平均物理场 $\overline U=\beta_0(t)$，则 $b=b_D+\beta_0(t)$，实际流是同一 Dirac Poisson 张量下的时间依赖 Hamiltonian 流，

$$
X=X_{H_*}^{D}+\beta_0(t)X_{P_{\rm mom}}^{D}
=X_{H_*+\beta_0(t)P_{\rm mom}}^{D}.
$$

若预先固定原积分式中的 $B(t)$，即对整个相空间采用同一
$b=\chi/(2\Gamma)+B(t)$，则

$$
X=X_{H_*}^{D}
+\left(B(t)-\frac{H_*}{P_{\rm mom}}\right)X_{P_{\rm mom}}^{D}.
$$

其自然一形式为

$$
\alpha=dH_*+
\left(B(t)-\frac{H_*}{P_{\rm mom}}\right)dP_{\rm mom},
\qquad
d\alpha=-\frac1{P_{\rm mom}}dH_*\wedge dP_{\rm mom}.
$$

在一般正则叶上，这个二形式不为零。因此不能把固定 raw $B(t)$ 的闭合直接称为同一个 Dirac 张量的 Hamiltonian 系统。若再限制 $dH_*\wedge dP_{\rm mom}=0$，或引入另一个 Poisson/时间结构，才可能另作 Hamiltonian 解释。以下谱迹守恒性对两种闭合均成立，但同一张量下的 Liouville Hamiltonian 结论应采用规定 $\overline U$ 的闭合。

现有一般 $p_3$ 密度恒等式在 $G=0$、$q=\Gamma$ 分支给

$$
H_{\rm full}=-8\operatorname{Tr}D^2(P-I),
$$

其中等号指积分 modulo total $D$，$H_{\rm full}$ 是 $U,w$ 变量的原 cubic Hamiltonian。为避免假定它在 off-surface 仍有同一公式，使用明确 auxiliary 外延

$$
\widetilde H=-8\operatorname{Tr}D^2(P-I),\qquad
\nabla_P\widetilde H=-8D^2.
$$

在 $p_1=0,p_2=a$ 常数时

$$
(PD^2)_+=(D^2P)_+=D^2+a,\qquad
X_{\widetilde H}P=-[D^2+a,P]=-[D^2,P].
$$

这里 $1/8$ 与 $-8$ 恰好抵消。由于 $X_n$ 与 $P$ 对易，
$\{\mathcal C_n,\widetilde H\}=0$。在共同 $U$ 截面 $b=0$，
$\widetilde H$ 限制恰为 $H_*$。共同 $U$ 平移使
$p_3\mapsto p_3+2af$，所以
$\sum_j\widetilde H_{U_j}=-8a=hM\Gamma$ 为空间常数；投影到 $p,s$ 括号所差只含它乘一个周期全导数，积分为零。进一步，$q$ 的 Dirac conormal 修正已对谱迹消失。因此

$$
\boxed{\{\mathcal C_n,H_*\}_{D}=0,\qquad
\{\mathcal C_n,P_{\rm mom}\}_{D}=0.}
$$

实际 $a(\Gamma)$ 归一化增加的平移梯度也不改变这一结论，因 $H_*$ 平移不变且 $\Gamma$ 守恒。固定 raw $B(t)$ 的额外系数 $-H_*/P_{\rm mom}$ 同样只乘 $X_{P_{\rm mom}}$，故不破坏谱迹守恒。

于是得到一个不除以 $c$、适用于有限 $M\ge2$、$\Pi w=0,\Gamma\ne0$ 正则约束分支的 **一般场谱迹守恒/对合层级**。这一结论不要求个别 $s_j\ne0$，但约束本身可能产生较低维或不同的物理分支；例如 $M=2$ 会有 $ps=\Gamma$、$b=B-p_x/p$ 的 travelling-profile 特性。

此节没有证明该新层级在每个 Dirac 叶上的全阶独立性、谱像逆或最大各向同性，也没有覆盖 $c=\Gamma=0$ 的进一步退化层。形式根与守恒定理本身不解决原 Sobolev 解流问题。

## 10. 混合解中心单射的 Carleman 独立核验

本节核验 full_m_mixed_flow.md §5 的实际论证，而非仅引用中心唯一性结论。核验范围是有限格点维数、空间圆周上的图空间

$$
z\in H^1_tL^2_x\cap L^2_tH^2_x,\qquad
P_*z=Bz_x+C_0z,\qquad
A=\operatorname{diag}(-D^2,D^2),\quad P_*=\partial_t-A,
$$

其中 $B,C_0$ 在所用紧时间区间有界。**在这些假设下，中心 Cauchy 唯一性证明可以成立为自足论证。** 下述核验补足图范数密度、权重一阶项与端点处理的细节。

### 10.1 延零与图范数密度

图空间包含 $H^1_tL^2_x$，因此有连续 $L^2_x$ 时间迹。若 $z(0)=0$，把 $z$ 在 $t<0$ 延零时，分布时间导数没有端点 Dirac 项；空间 $H^2$ 的时间平方可积性也保留。故延拓仍在该图空间。时间截断后函数有紧时间支撑。

先取有限空间 Fourier 截断，再作紧支撑时间卷积，得到光滑紧支撑函数，并在

$$
\|f\|_{L^2_{t,x}}+\|f_t\|_{L^2_{t,x}}+\|Af\|_{L^2_{t,x}}
$$

中强逼近。截断和卷积与时间独立的 $A$ 交换。对任意固定有限 $\lambda$，光滑权重 $e^{\lambda\phi}$ 及其时间导数在截断支撑上有界，所以加权函数仍可按该图范数逼近。无需让逼近对 $\lambda\to\infty$ 一致，也无需对 $B,C_0$ 求时间导数。

### 10.2 精确恒等式及相反扩散符号

取 $\phi=e^{-Kt}$ 和 $Q_\lambda=\partial_t-A-\lambda\phi'$。光滑紧支撑函数满足

$$
\|Q_\lambda f\|^2
=\|f_t\|^2+\|(A+\lambda\phi')f\|^2
+\lambda\int\phi''(t)\|f(t)\|_{L^2_x}^2\,dt.
$$

混合项 $-2\operatorname{Re}\int\langle f_t,Af\rangle$ 由自伴、时间独立的 $A$ 和紧支撑消失；另一混合项
$-2\lambda\operatorname{Re}\int\phi'\langle f_t,f\rangle$
分部积分给正的 $+\lambda\phi''$ 项。上述密度将恒等式传到图空间。

虽然 $A$ 有正、负两个扩散符号，仍有

$$
|A|=-D^2I,\qquad \||A|f\|_{L^2_x}=\|Af\|_{L^2_x}.
$$

因此点时刻有
$\|f_x\|^2\le\|(A+\lambda\phi')f\|\|f\|
+\lambda|\phi'|\|f\|^2$。积分并用 Cauchy–Schwarz 得正确的整体版本

$$
\|f_x\|_{L^2_{t,x}}^2
\le S\|f\|_{L^2_{t,x}}
+\lambda\int|\phi'(t)|\,\|f(t)\|_{L^2_x}^2dt,
\qquad
S=\|(A+\lambda\phi')f\|_{L^2_{t,x}}.
$$

源文式 $8$ 已注明点时刻；将其用于整体估计时应采用上面的时间积分，不能把变化的 $|\phi'|$ 写成单个全局标量。

### 10.3 一阶扰动的吸收与权重间隙

令 $f=e^{\lambda\phi}\chi z$，则

$$
Q_\lambda f=Bf_x+C_0f+d,\qquad d=e^{\lambda\phi}\chi' z.
$$

以 $b=\|B\|_\infty$、$a_0=\|C_0\|_\infty$，平方估计给

$$
\|Q_\lambda f\|^2
\le4b^2\|f_x\|^2+4a_0^2\|f\|^2+2\|d\|^2.
$$

Young 不等式
$4b^2S\|f\|\le S^2/2+8b^4\|f\|^2$
吸收半个 $S^2$。选择 $K\ge8b^2+1$，利用
$\phi''=K|\phi'|$ 吸收 $4b^2\lambda\int|\phi'|\|f(t)\|^2dt$。在固定紧时间支撑上 $\min\phi''>0$，再取 $\lambda$ 足够大即可吸收 $(8b^4+4a_0^2)\|f\|^2$。于是

$$
\lambda\int\phi''\|f(t)\|^2dt\le C\|d\|^2,
$$

其中 $C$ 与足够大的 $\lambda$ 无关。

设 $\chi=1$ 于 $[0,t_1]$，非零解上的 $\chi'$ 支撑于
$[t_1,t_2]$。对 $0<t_*<t_1$，$\phi(t_*)>\phi(t_1)$，故

$$
\lambda c_* e^{2\lambda\phi(t_*)}
\|z\|_{L^2([0,t_*]\times\mathbb T)}^2
\le C_\chi e^{2\lambda\phi(t_1)}
\|z\|_{L^2([t_1,t_2]\times\mathbb T)}^2.
$$

令 $\lambda\to\infty$ 得前一范数为零。目标内点可任意选取，并再选较晚的 $t_1,t_2$，因此覆盖整段较晚的内区间。反向时间将 $A$ 换为 $-A$；它仍自伴，且 $|-A|=|A|$，扰动符号变化不影响有界系数估计，故同样覆盖较早一侧。

延零仅发生在已知零中心迹处，不要求混合端点有 $H^2$ 迹。证明得到全部内点相同后，再用 mild 解的端点 $H^r$ 连续性得到混合端点相同。

### 10.4 对真实 DLW 混合解与微分的适用条件

固定同一 $q(t)$ 和同一混合时间窗口，两条真实 mild 解 $y,\widetilde y$ 的差满足

$$
P_*z=D\!\left(N(y,t)-N(\widetilde y,t)\right)
=Bz_x+B_xz,\qquad
B=\int_0^1DN(\widetilde y+\theta z,t)\,d\theta.
$$

有限格点算子与局部多项式非线性不增加时间正则要求。若已建立内点空间平滑，且 $q(t)$ 有界，则紧内区间上 $B,B_x$ 有界；空间平滑和方程进一步给 $z_t\in L^2_tL^2_x$、$z\in L^2_tH^2_x$。所以图空间引理适用，中心状态相同推出整条轨道及混合数据相同。

微分单射还依赖参数映射的解析固定点构造和线性化内点提升。线性化方程
$P_*z=D(DN(y,t)z)$ 在已知光滑背景上具有相同形式，系数及其空间导数在紧内区间有界。若线性 Duhamel 提升已将其送入同一图空间，则中心变分为零推出整条线性化轨道及端点变分为零。这是原文内点提升论证的真实依赖，不能单凭非线性中心单射推导微分单射。

核验结论是：源文 §5 的中心单射及微分单射路线，在其已声明的 mild 构造、内点提升和图空间假设下成立；Carleman 部分没有遗留相反扩散符号或一阶吸收漏洞。该结论不提供中心微分的有界下界、闭像、Banach 逆或完整 Sobolev 初值流，也不单独证明谱完备性或 Liouville 可积性。
