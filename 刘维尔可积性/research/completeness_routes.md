# 全周期非线性因子逆与谱完备性路线审查

日期：2026-10-11。研究证明与范围说明。

前置材料：[原谱与物理 Hamilton 结构](../../Workspaces/dlw_general_field_20261006/RESEARCH_NOTES.md)、[全周期矩阵谱](../../Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md)、[全周期自由场括号](../../Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_FREE_FIELD_POISSON.md)、[两站非线性逆](../../Workspaces/dlw_general_field_20261006/TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md)、[两站物理 pencil](../../Workspaces/dlw_general_field_20261006/TWO_SITE_POISSON_PENCIL.md)。

## 结论与范围

比固定 `M=2,m=Ax` 更有希望的是原来的**周期 x、任意有限 M、非零格点平均 c** 分支。这里仍保留 `2(M-1)` 个任意函数，不施加有限孤子、有限 Fourier、行波或仿射假设。周期边界强制 c 为时间常数；平均通量 Γ(t) 的任意时间自由度应按平移规范保留，以下先用某一固定时间的 B=Γ/(2c) 记号写谱构造。

旧稿已有全 M 的协变矩阵谱问题、物理常系数自由场括号以及完整矩阵系数的逆。它们不能计作本次新增证明。本次可增加一个实质结果：**在均匀背景附近、固定物理分量空间均值的叶上，有限个标量 Lax 系数已经可非线性地恢复全部物理场。** 证明用有限 Padé 型方程、两个标记谱点的有序 Floquet 旗标以及可逆的一阶因子交换。这个结果证明状态信息没有在标量化中丢失；尚不等于从谱不变量和角数据到状态的完整逆谱定理。

M=2 的 AKNS 路线有已证明的局部复 Birkhoff 图可借用，但只在文献保证的零附近复开集，且必须保留扭转参数、缩放商和原物理三次 Poisson pencil。下文给出一个可直接用于谱 Poisson 审计的精确加权生成式；全 M 的对应生成式尚未证明。

## 一阶因子、均值与谱标记

令 D=∂x，x 的周期为 L，

$$
b_j=U_j/2,\qquad d_j=hw_j/8,\qquad
u_j=b_j+d_j,\quad v_j=b_j-d_j,
$$

$$
S=\sum_jd_j=hMc/8\ne0,\qquad
B=\frac{\sum_jb_jd_j}{S}=\frac{\Gamma}{2c},\qquad
\nu=B-S.
$$

使用旧稿的准确因子顺序：

$$
P=T_{M-1}\cdots T_0,\qquad
T_j=(D-v_j)^{-1}(D-u_j),\qquad
\mathscr L=-2S(P-I)^{-1}+\nu I.
$$

当所有 p,s 分量空间均值为零时，设

$$
\chi=L^{-1}\int_0^L\Pi b\,dx
=B-\frac1{2cL}\int_0^L\Pi(ps)\,dx .
$$

则

$$
\int u_j=L(\chi+\delta),\qquad
\int v_j=L(\chi-\delta),\qquad \delta=hc/8.
$$

**χ 随动量而变，不能作为原物理 Casimir 固定。** 非零分量均值时，令 $P_j=\int p_j$, $W_j=\int s_j$，相应公式是

$$
\int u_j=L\chi+P_j/2+\delta L+hW_j/8,
\quad
\int v_j=L\chi+P_j/2-\delta L-hW_j/8.
$$

原 Casimirs 固定这些有序均值的差，而非共同的 Lχ。下面比较同一个 P 的两个物理前像时，Lχ 将由同一个最小分式的系数恢复，因此无需人为增加动量约束。

## 可逆交换与最小左分式

若实周期函数 a−b 无零，定义

$$
\theta=D\log|a-b|=\frac{a_x-b_x}{a-b}.
$$

有准确恒等式

$$
(D-a)(D-b)^{-1}
=(D-b-\theta)^{-1}(D-a-\theta). \tag{1}
$$

验证只须左右乘分母：

$$
(D-b-\theta)(D-a)=(D-a-\theta)(D-b).
$$

两侧 D 的系数相同，常数项差为
$-a_x+b_x+\theta(a-b)=0$。交换后的差仍是 a−b，故用同一个 θ 减回去就是唯一逆交换。因为 $\int_0^L\theta=0$，交换保持每个带标签因子的空间均值，而不是只保持总和。

对 P 作有限次这种交换，把全部逆因子移到左边，得到

$$
P=Q^{-1}R,\qquad
Q,R\text{ 为 monic 的 M 阶微分算子}. \tag{2}
$$

正因子之间、逆因子之间均不交换标签。R 的从右向左因子标签为 `u0,…,u(M−1)`；Q 的从右向左标签为 `v(M−1),…,v0`。后一处反序必须在有序 Floquet 旗标中保留。

均匀物理背景是

$$
b_j=B,\quad d_j=\delta\ne0,
\quad Q_0=(D-B+\delta)^M,
\quad R_0=(D-B-\delta)^M.
$$

所有交换所用差均为 2δ。因此在一个控制足够多个 Cᵏ 半范数的小邻域中，有限次正、逆交换均有意义；分母不会因为某个单独 d_j 为零而出现额外条件。

Q₀,R₀ 互素。附近最小 monic 左分式的存在来自上述有限交换；唯一性与阶数保持可由下面的有限矩阵直接证明，无须在光滑系数环上引入抽象微分域。

## 有限标量系数恢复 Q,R

写

$$
P=1+\sum_{n\ge1}\pi_nD^{-n},\qquad
Q=D^M+\sum_{i=0}^{M-1}q_iD^i.
$$

QP 的 $D^{-r}$ 系数，r=1,…,M，等于零。给定 P 的有限系数，这给出逐点线性系统

$$
\sum_{i=0}^{M-1}A_{ri}q_i=-b_r,
$$

$$
A_{ri}=\sum_{\ell=0}^i\binom i\ell D^\ell\pi_{r+i-\ell},
\qquad
b_r=\sum_{\ell=0}^{M}\binom M\ell D^\ell\pi_{r+M-\ell}. \tag{4}
$$

式 (4) 只使用 $\pi_1,\dots,\pi_{2M}$ 的有限 jets。QP 的微分部分随后给 R。对实际来自物理因子的 P，真实 Q 就是此系统的解；所以无须错误地把只消去 M 个负阶系数当作对任意形式 PDO 的全阶有理性证明。

均匀点可用常数指数规范移去 B−δ。此时

$$
P_0=((D-2\delta)/D)^M,
\qquad
\pi_n=\binom Mn(-2\delta)^n\ (1\le n\le M),
\quad \pi_n=0\ (n>M).
$$

于是 $A_{ri}=\pi_{r+i}$。它是反三角矩阵，反对角线全部为 $\pi_M=(-2\delta)^M$，因此

$$
\det A=(-1)^{M(M-1)/2}(-2\delta)^{M^2}\ne0. \tag{5}
$$

不作该常数规范时矩阵同样可逆：若其核非零，所得低于 M 阶的非零微分算子 Q₁ 使 Q₁P₀ 的前 M 个负阶系数为零。Q₁P₀ 是分母 (D−B+δ)ᴹ 的普通有理函数，前 M 个负阶系数消失迫使余项为零，与两个互素 M 次多项式矛盾。由连续性，附近 (4) 仍可逆。

若某个低于 M 阶的微分算子 $T=\sum_{i<M}t_iD^i$ 满足 TP 为微分算子，其前 M 个负阶系数给 At=0。A 逐点可逆，所以 T=0。两个 monic M 阶分母的差正是这种 T，故

$$
P=Q^{-1}R=Q'^{-1}R',\quad Q,Q'\text{ monic、阶 M}
\ \Longrightarrow\ Q=Q',\ R=R'. \tag{3}
$$

同一核论证还排除任何低于 M 阶的非零左分母。这样分式确为最小，且论证直接适用于实光滑周期系数。Q⁻¹在此是形式 PDO 逆，未声称 Q 在周期函数空间中无核或有有界逆；后面的 Floquet ODE 正是保留其解空间信息。

物理约束已固定

$$
\pi_1=-2S,\qquad
\pi_2=2S^2-2SB.
$$

在 $\mathscr L=D+\sum_{r\ge1}\ell_rD^{-r}$ 与 P 之间作形式逆，$\pi_{r+2}$ 由 $\ell_1,\dots,\ell_r$ 的有限 jets 决定，首个新未知系数的系数非零。因此 (4) 实际只需要

$$
\ell_1,\dots,\ell_{2M-2} . \tag{6}
$$

这与每个非零 Fourier 模态 `2(M−1)` 维线性忠实性的独立计算一致，但 (1)–(6) 已是非线性恢复算法的一部分。

## 从两个 Floquet 旗标恢复全部物理因子

考虑一个 monic 微分算子

$$
R=(D-a_{M-1})\cdots(D-a_0)
$$

以及它在 [0,L] 上的 M 维解空间。右端 k 个因子的核 Eₖ 给一个完整 Floquet 不变旗标

$$
0\subset E_1\subset\cdots\subset E_M,
\qquad \dim E_k=k.
$$

该旗标第 k 个一维商的 Floquet 倍子是
$\exp\int_0^L a_{k-1}$。若 $f_1,\dots,f_k$ 是 Eₖ 的相容基，令

$$
W_k=\operatorname{Wr}(f_1,\dots,f_k),\quad W_0=1.
$$

Abel 恒等式给出恢复公式

$$
a_{k-1}=D\log|W_k/W_{k-1}| . \tag{7}
$$

换旗标相容基只把 Wₖ 乘以非零常数，所以 (7) 不依赖该选择。又因为

$$
W_k(x+L)=\det(F_R|_{E_k})W_k(x),
$$

其对数导数是周期函数；**基函数本身不需要周期，亦不能把 Floquet 旗标误称作周期解的基。**

均匀背景 R₀=(D−a)ᴹ 的 monodromy 相似于
$e^{aL}e^{LN}$，其中 N 是一个 M 阶 nilpotent Jordan 块。由于 $e^{LN}-I=N\,[L+\cdots]$，它仍只有一个 Jordan 块，且是 cyclic。每个维数 k 的不变子空间唯一，等于 $\ker(F_R-e^{aL}I)^k$。因此**重倍子不破坏这张局部图的唯一旗标**；要求简单倍子反而会错误地排除整张零均值叶。

cyclic 性是开条件。例如选均匀点的一个 cyclic 向量 v，行列式 $\det[v,Fv,\dots,F^{M-1}v]\ne0$ 在邻域仍成立。零物理分量均值叶上，交换保持均值，R 的所有倍子确实同为 $e^{(\chi+\delta)L}$，Q 的同为 $e^{(\chi-\delta)L}$，χ 可变。结合 cyclic 性，两者的完整旗标都唯一。

均匀点的旗标可取 $e^{ax}\{1,x,\dots,x^{k-1}/(k-1)!\}$，Wₖ 是非零常数乘 $e^{kax}$。解的有限阶 ODE 对系数连续依赖，旗标在固定秩的 Jordan 谱层内连续/解析选取；故紧区间上足够小的扰动仍使所有 Wₖ 无零。可用固定的非零 minors 从 $\ker(F-\mu I)^k$ 选择相容基，避免任意归一化跳变。

若固定的非零分量均值导致不同的倍子，附近仍可用同一论证：每个特征值只允许一个 Jordan 块，按已指定的有序商倍子决定每个广义特征空间的前缀维数，其直和就是唯一旗标。此推广还要求参考常因子没有 numerator/denominator 共同根及交换差零点；它不是任意常场的无条件全局结论。

对于同一 P 的两个物理前像，(3) 已给相同 Q,R。它们 $D^{M-1}$ 系数的积分给各因子均值总和，因而给共同的 Lχ。再与固定的物理均值差合并，所有有序 quotient 倍子相同。Q,R 的唯一旗标和 (7) 给相同的一阶因子；逆向执行 (1) 给相同 uⱼ,vⱼ，最后

$$
U_j=u_j+v_j,\qquad w_j=4(u_j-v_j)/h
$$

恢复原物理场。因此局部单射已非线性证明，而不是仅由线性无核推断。

**局部像逆命题。** 对任意 M≥2、h>0、c≠0，在零分量空间均值叶的均匀背景附近，映射 $(p,s)\mapsto(\ell_1,\dots,\ell_{2M-2})$ 在其实际像上有由有限 jets、有限线性系统、线性 ODE、固定秩核与无零 Wronskian 组成的局部逆。解析选旗标的声明限于固定谱重数的实际像层，不跨越任意 ambient 碰撞层；在此层内各有限步骤解析，并至多需要有限个额外导数。对 C∞ Fréchet 图，它给连续的局部像逆。

这里未证明目标是一个无约束 Banach 开集，也未给出最优 Sobolev 导数计数。需要足够高阶 Cᵏ 控制的原因是有限次交换含对数导数，(4) 含有限 jets。该命题不需要、也不宣称物理实时间在 Sobolev 开邻域存在可微流。

## 标记谱值的准确解释

令

$$
C=(Q-R)/(2S),\qquad N=Q+\nu C.
$$

C 是 monic 的 M−1 阶微分算子，

$$
\mathscr L=C^{-1}N,
\qquad (N-\lambda C)\psi=0. \tag{8}
$$

原 transfer 特征参数满足

$$
\mu=\frac{\lambda-(B+S)}{\lambda-(B-S)}.
$$

所以

$$
N-(B-S)C=Q,\qquad N-(B+S)C=R. \tag{9}
$$

两个标记值始终是 λ₋=B−S、λ₊=B+S；M=2 时 S=2η，正好恢复旧 Riccati 逆的 B±2η。全 M 的替代对象是两个有序 M 维 Floquet 旗标，不是把两站标量 Riccati 方程逐分量复制。

式 (9) 没有完成逆谱：仅知道两个标记值处有限维 monodromy 矩阵，不能恢复两个任意函数系数微分算子。完整的谱曲线、norming/divisor/连接数据首先要重建 N,C，之后 (1)–(9) 才重建物理场。不得把标记旗标逆称为谱不变量逆。

## M=2 准周期 AKNS 可用的边界与静态逆

旧稿设

$$
f=p/2-\eta,\quad
g=-s_x/c+(1-s^2/c^2)(p/2+\eta),\quad
C_0=B-ps/c,
$$

$q=f e^\sigma,r=g e^{-\sigma},\sigma_x=C_0$，满足
$q_t=-q_{xx}+2q^2r$, $r_t=r_{xx}-2qr^2$。令

$$
\mathcal S=\int_0^LC_0\,dx,
\qquad \tau=\mathcal S/L
=B-\frac1{cL}\int ps\,dx.
$$

由 $(C_0)_t=A_x$ 得 τ 沿此流守恒，但 τ **不是物理 Casimir**。边界为

$$
q(x+L)=e^{\mathcal S}q(x),\qquad
r(x+L)=e^{-\mathcal S}r(x).
$$

令 $Q_a=e^{-\tau x}q$, $R_a=e^{\tau x}r$，则 Qₐ,Rₐ 周期，且

$$
(Q_a)_t=-(Q_a)_{xx}-2\tau(Q_a)_x-\tau^2Q_a+2Q_a^2R_a,
$$

$$
(R_a)_t=(R_a)_{xx}-2\tau(R_a)_x+\tau^2R_a-2Q_aR_a^2.
$$

对应的 determinant-one 周期 AKNS 系统是

$$
W_x=\begin{pmatrix}(\lambda-\tau)/2&Q_a\\R_a&-(\lambda-\tau)/2\end{pmatrix}W.
$$

若原周期系统的 Floquet 倍子为 μ，其倍子是
$m=\mu\exp[-(\lambda L+\mathcal S)/2]$。转换时需要这个 holonomy 校正。

若完整 AKNS 逆谱数据在合法的局部图中给出 Qₐ,Rₐ，还要保留 τ 和处理全局缩放 $(Q_a,R_a)\mapsto(kQ_a,k^{-1}R_a)$。在 Qₐ 无零图上，

$$
a=Q_aR_a,\qquad d=\tau+(Q_a)_x/Q_a
$$

恢复旧稿的两玻色子系数，然后用两标记 Riccati/Floquet 逆恢复 p,s。物理叶的两个标记判别式约束为

$$
\Delta(B-2\eta)=2\cosh\frac{\int p-(2\eta/c)\int s}{2},
$$

$$
\Delta(B+2\eta)=2\cosh\frac{-\int p-(2\eta/c)\int s}{2}.
$$

因此不能把任意 periodic AKNS 势的全空间自动当作 DLW 的像。

## 原物理 pencil 的谱加权生成式：可直接验证的修复

对旧稿两玻色子变量 a,d 的实际、非共振 Riccati 分支，设

$$
y_x=y^2+(d-\lambda)y-a,\qquad
\mathcal C(\lambda)=\int y,
\qquad g(\lambda)=\delta\mathcal C(\lambda).
$$

旧稿已给准确恒等式

$$
(J_2-\lambda J_1)g=0,
\qquad (J_3-\lambda J_2)g=T,
\qquad T=(a_x,d_x).
$$

物理张量和另一个准确恒等式为

$$
J_{\rm phys}=-\frac1{2c}
[J_3-2BJ_2+(B^2-4\eta^2)J_1],
\qquad
J_{\rm phys}\delta\!\int d=T/c.
$$

因此令

$$
\widehat{\mathcal C}(\lambda)=\mathcal C(\lambda)+\tfrac12\int d,
\qquad \mathfrak p(\lambda)=(\lambda-B)^2-4\eta^2,
$$

就得到

$$
\boxed{\quad
J_{\rm phys}\delta\widehat{\mathcal C}(\lambda)
=-\frac{\mathfrak p(\lambda)}{2c}
J_1\delta\mathcal C(\lambda).
\quad} \tag{10}
$$

这里的 $\frac12\int d$ 恰好消去此前不能删去的 translation 项。两个标记值是 $\mathfrak p$ 的根，所以它们给物理 Casimirs，和逆谱标记完全一致。

若某个实际谱轮廓 γ 避开两标记值，且分支、变分及积分合法，取

$$
I_\gamma=\oint_\gamma \mathcal C(\lambda)\,d\lambda,
\qquad
A_\gamma=\oint_\gamma
\frac{\widehat{\mathcal C}(\lambda)}{\mathfrak p(\lambda)}\,d\lambda.
$$

在 B,c,η 固定的条件下，由 (10) 得

$$
J_{\rm phys}\delta A_\gamma
=-\frac1{2c}J_1\delta I_\gamma. \tag{11}
$$

更一般的固定谱权重可同样插入。这个公式提供了具体的物理 action 构造方向；若标准 AKNS 作用量写成 Floquet 对数的轮廓积分，应先统一 λ 与其标准 ζ 参数及整体常数。

**(11) 仍不是作用角完备性证明。** 在同一物理叶上还必须处理：τ 不是 Casimir；两个标记约束与缩放商；可能围住标记值的中央谱轮廓；closed gap 的 Cartesian 坐标；物理弱辛形式中加权算子的有界可逆性；以及共轭角的恢复。J₁ 的 Casimir 叶和 Jphys 的 Casimir 叶不同，不能仅凭共同的 Hamilton 向量就断言两个叶上的极大性相同。

全 M 有两个相同的 Möbius 标记 B±S，提示可能存在类似的二次谱权重。但从此提示到全 M 的实际原物理张量生成式尚缺推导。不能把 (10) 的两站 J₁,J₂,J₃ 逐矩阵项推广。全 M 常系数 (q,d) 物理坐标只能保证其推前张量正确；它本身没有证明谱分离变量的括号。

可进一步给出一个精确的、尚未完成物理约化的全 M tensor 起点。固定 $\alpha=2S$, $\nu=B-S$，令 $A=\mathscr L-\nu$。则

$$
P=(A-\alpha)A^{-1},\quad
\delta P=\alpha A^{-1}\delta\mathscr L A^{-1},\quad
X_P=\alpha^{-1}AXA.
$$

若 P 的 ambient 自由因子张量按无权 trace 归一化为 Adler map 的 1/8 倍，冻结 α,ν 的形式推前准确为

$$
J_{\mathscr L}^{\rm amb}(X)=\frac1{8\alpha^2}
\left\{A\big[(A-\alpha)XA\big]_+(A-\alpha)
-(A-\alpha)\big[AX(A-\alpha)\big]_+A\right\}. \tag{12}
$$

这由 $J_P(Y)=(PY)_+P-P(YP)_+$ 直接代入得到，适用于全 M，不依赖内部矩阵秩。两个算子因子正是 $\mathscr L-\lambda_-$、$\mathscr L-\lambda_+$。但 (12) 的 ambient 场未必切向固定 π₁、π₂ 的物理谱层；还需原平均约束、公共 gauge 和零模的真正 Dirac 计算。它因此提供全 M 二次谱权重的具体推导入口，而没有补上全 M 作用量括号或极大性。

## 一手文献能支持到哪里

[Mas–Ramos 1995](https://arxiv.org/html/q-alg/9501009v2) 给 Adler 张量在乘法、求逆和有理分式下的代数规则。它不提供周期无限维逆谱、全局作用角或本文 (1)–(9) 的物理均值与 Jordan 旗标结论。

[Huang–Shaw–Tu 1998](https://arxiv.org/abs/solv-int/9801019) 与 [Aratyn 等 1994](https://arxiv.org/abs/hep-th/9401058) 给约束 KP 的矩阵/多玻色子 Hamilton 框架。它们没有在这里的多重内部谱通道、非平凡 holonomy 及原物理像上证明周期 Birkhoff 完备性。

[Kappeler–Lohrmann–Topalov–Zung 2009，Prop. 2.9](https://link.springer.com/article/10.1007/s00220-008-0543-0) 给复 pair 空间零附近的双解析正则 Birkhoff 图。它不要求共轭切片或简单谱，因此小的独立实 Qₐ,Rₐ 可以使用。周期重标为 1 后，均匀 AKNS 背景范数为 √2|η|L；需小到进入文献的未量化开邻域，不能声称精确阈值是 π。

[Kappeler–Schaad–Topalov 2015，Theorem 2.1](https://arxiv.org/html/1505.04455v1) 重述 defocusing 的全局正则图及其复邻域延拓。这里标准 Zakharov–Shabat 势可取 $\varphi_1=-iQ_a,\varphi_2=iR_a$：defocusing 共轭切片要求 Rₐ=Qₐ，focusing 要求 Rₐ=−Qₐ。一般独立实 pair 不在这两个切片中；复延拓的定义域不能假定为全部 pair 空间。

[Kappeler–Topalov 2020/2022](https://arxiv.org/html/2002.11638v1) 在 focusing 势的简单 periodic/antiperiodic 谱假设下给局部图。均匀点的无限 closed gaps 不满足其简单谱前提。[Kappeler–Topalov 2018](https://arxiv.org/html/1807.02455v1) 则在特定较大常 focusing 背景排除 gauge-invariant 局部 Birkhoff 图。该限定不能删去，但足以阻止对任意大背景无条件套用普通图。

[Biondini–Zhang 的无限亏格 periodic inverse theorem](https://arxiv.org/html/2311.18127v2) 使用 q,q* 的共轭势，对一般独立实 Qₐ,Rₐ 没有直接覆盖。

均匀 M=2 的判别式是

$$
\Delta(\lambda)=2\cosh\!\left(L\sqrt{(\lambda-B)^2/4-\eta^2}\right).
$$

λ=B±2η 是 Δ²−4 的简单根；该点 monodromy 的两个倍子重合而呈 Jordan，不等于 periodic operator eigenvalue 必然代数多重。一般非零编号 closed gaps 才是双根。closed gap 上作用量 Iₙ 及 dIₙ 可同时为零，故 Cartesian Birkhoff 图的完备性也不能误称为所有作用量在均匀点梯度独立。

## 实时间与最终缺口

静态逆谱坐标存在不会消除原物理时间的 $e^{k^2t}$ 高频增长。文献的复 Birkhoff 图可启发另一条实际解路线：在谱坐标中选择高斯或更快下降的任意序列，用对角频率的高频估计控制有限时间窗，再经逆图与 (7)/(两站 Riccati) 恢复真实物理场。这比直接猜物理函数的高斯 Fourier 代数更有结构。

但本文件没有把这条路线升级为定理：尚需明确文献图在所选谱加权空间的正则性、实际虚时间频率估计、物理标记约束的保存、缩放规范、重启空间，以及物理 Jphys 的谱弱辛形式。不能拿一个标准 canonical NLS 图自动完成这些步骤。

当前可用的具体新增命题是 (1)–(9) 的全 M 非线性局部像逆；(10)–(11) 是两站实际物理谱权重的精确生成式。它们分别关闭“标量化是否丢失任意函数自由度”和“标准 AKNS canonicality 与物理 bracket 不同，如何着手修复”这两个具体问题。

仍未闭合的一般 Liouville 目标包括：全 M 周期有理 pencil 的完整 inverse spectral/divisor 定理；同一物理弱辛叶上的作用量/角和极大性；以及允许原实时间及所需辅助流的共同实际相空间。这些不是无限多个独立局部守恒量可自动补上的结论。

独立复核记录：交换式、反三角系统、零物理分量均值叶上的单 Jordan 旗标和无零 Wronskian 论证已分别复核；保留的范围是实际有理像、固定谱重数层、χ 从实际 Q/R 恢复，以及有限导数损失。这里只记录数学复核，不代替完整无限维 Liouville 定理。
