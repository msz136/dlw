# 零通量三阶层的实际流与全格点周期主符号

2026-10-11。接续 [singular_branch_review_20261011.md](singular_branch_review_20261011.md)。本稿先在 $M=3$ 的明确实最小有理图上证明真实光滑局部流，再证明全 $M$ 在 $\kappa\ne0$ 层的变量背景约束主符号。前者是一条完整局部分支结果，不能替代全 $M$ 的一般物理场 Liouville 目标。

## 1. 三阶分母、周期规范与实际时间

沿用 $c=\Gamma=0$、$q=0$、$\chi=\kappa\ne0$、$\beta=h^2/32$，以及已证明的真实一致性闭合。令 $a_j^\pm=U_j/2\pm hs_j/8$，

\[
P=(D-a_2^-)^{-1}(D-a_2^+)(D-a_1^-)^{-1}
(D-a_1^+)(D-a_0^-)^{-1}(D-a_0^+).
\]

在三个必要异类交换差均不为零的实周期图上，用

\[
(D-a)(D-b)^{-1}
=(D-b-\vartheta)^{-1}(D-a-\vartheta),
\qquad \vartheta=D\log|a-b|
\]

将 $P$ 排成 $Q^{-1}R_0$，其中 $Q,R_0$ 是 monic 三阶微分算子。每个 $\vartheta$ 都是周期对数导数，空间平均为零。当前层 $P-I$ 的阶数恰为 $-3$、首系数

\[
a_3=3h\kappa/16=-H_0/(8L)\ne0
\]

恒定，所以

\[
\boxed{R_0-Q=a_3,\qquad P=I+a_3Q^{-1},\qquad L_3^3=Q.}
\tag{1}
\]

这不是一般第三阶 PDO 近似；在这个图上 $Q$ 是精确微分算子。

### 共同 $U$ 与二阶系数

令 $\widehat P=P(p,s)$ 表示共同 $U=0$ 的商代表，写其三阶分母

\[
\widehat Q=D^3+A D^2+B_1D+C_1.
\]

原 denominator 因子的系数之和为零；三个交换只添加周期对数导数。因此

\[
A=-\sum_{\rm swaps}\vartheta,\qquad \overline A=0.
\tag{2}
\]

实际 $U=b+p$ 给

\[
Q_b=e^\theta\widehat Qe^{-\theta},\qquad \theta_x=b/2,
\qquad A_b=A-\tfrac32 b.
\tag{3}
\]

而 $\widehat P=I+a_3\widehat Q^{-1}$ 给其下一系数 $a_4=-a_3A$。真实次约束一致性由此等价于

\[
b=\tfrac23 A+\mathsf B(t),\qquad \mathsf B(t)=\overline b.
\tag{4}
\]

规定平均共同场 $\mathsf B=0$ 时，实际 $Q_b$ 自动没有 $D^2$ 项。对任意周期三阶算子，标量共轭去掉 $A D^2$ 要取 $\zeta_x=A/3$；共轭函数周期当且仅当 $\int A=0$，否则 holonomy 为 $\exp(\int A/3)$。所以商代表可以用周期共轭去掉二阶项；实际 $Q_b$ 在任意 $\mathsf B(t)$ 下的去项规范一般是准周期，holonomy 为 $\exp(-L\mathsf B/2)$。这里保留了共同场零模，没有暗中丢掉扭转。

一般去项公式为

\[
e^\zeta(D^3+AD^2+B_1D+C_1)e^{-\zeta}
=D^3+uD+v,
\]

\[
u=B_1-A_x-A^2/3,\qquad
v=C_1-AB_1/3+2A^3/27-A_{xx}/3.
\tag{5}
\]

### 原 Hamiltonian 到 $t_2$ 的桥梁

这里直接从原场的因子微分证明实际方程。原投影式为

\[
p_t=-D(bp)-\mathcal P_0D(p^2/2+\beta s^2)-p_{xx}-Rs_{xx},
\quad s_t=s_{xx}-D(bs+ps).
\]

置商因子 $a_j^\pm=p_j/2\pm hs_j/8$，并定义周期实函数

\[
\nu_c=-\Pi(p^2/4+\beta s^2/2),\qquad
\nu_j=\nu_c+\tfrac12(Rs_x)_j-\tfrac h4s_{j,x}.
\]

$\delta_-R=M_-\mathcal P_0$ 给 $\nu_{j+1}-\nu_j=hs_{j,x}/2$。逐项代入原 PDE 得

\[
(a_j^+)_t=-(\nu_j)_x-(a_j^+)_{xx}
-D[ba_j^++(a_j^+)^2],
\]

\[
(a_j^-)_t=-(\nu_{j+1})_x-(a_j^-)_{xx}
-D[ba_j^-+(a_j^-)^2].
\]

令 $L_j=D^2+bD+\nu_j$、$\mu_j=\nu_j+b_x+2(a_j^+)_x
=\nu_{j+1}+b_x+2(a_j^-)_x$，以及 $N_j=D-a_j^-$、$B_j=D-a_j^+$。上两式等价于

\[
(B_j)_t=B_jL_j-(D^2+bD+\mu_j)B_j,\qquad
(N_j)_t=N_jL_{j+1}-(D^2+bD+\mu_j)N_j.
\]

因此 $T_j=N_j^{-1}B_j$ 满足
$T_{j,t}=T_jL_j-L_{j+1}T_j$。周期乘积逐因子消去所有中间 $L_j$，得到原场的真实微分

\[
\widehat P_t=-[D^2+bD+\nu,\widehat P]
\tag{6}
\]

其中 $\nu=\nu_0$ 是显式周期标量。这个原 PDE 因子证明适用于全 $M$ 的 $c=0$ 兼容主层，既不要求三阶最小图，也不需要 ambient 迹外延。另一方面 $\widetilde H=-8\operatorname{Tr}D^2(P-I)$ 在 $c=0,b=0$ 截面限制恰为 $H_0$，与此实际桥梁相容。

由式 (1)，$\widehat Q_t=-[D^2+bD+\nu,\widehat Q]$。三阶首一性强制 $2A_x-3b_x=0$，再得式 (4)。按式 (5) 取周期去项规范后，微分生成算子的一阶系数是空间常数 $\mathsf B(t)$。没有 $D^2$ 项又强制其零阶系数的导数为 $2u_x/3$。无关的时间标量可去掉，所以

\[
\boxed{Q=D^3+uD+v,\qquad
Q_t=-[D^2+\mathsf B(t)D+2u/3,Q].}
\tag{7}
\]

若改用实际 $P_b$，其生成算子为

\[
D^2+\nu-b_x/2-b^2/4-\theta_t;
\]

不能把商代表的 $bD$ 项原样放在实际 $P_b$ 上。通过商代表的周期去项路线，式 (7) 的系数全部周期；随时间变化的平均共同场只给平移漂移。

## 2. 实 good Boussinesq 方程与半线性 Schrödinger 表示

直接展开式 (7) 得

\[
u_t=u_{xx}-2v_x-\mathsf B u_x,
\]

\[
v_t=-v_{xx}+\tfrac23u_{xxx}+\tfrac23uu_x-\mathsf B v_x.
\tag{8}
\]

令 $z=v-u_x/2$，则

\[
u_t=-2z_x-\mathsf B u_x,\qquad
z_t=\tfrac16u_{xxx}+\tfrac23uu_x-\mathsf B z_x.
\tag{9}
\]

用时间依赖空间平移消去 $\mathsf B$ 后，

\[
u_{tt}+\tfrac13u_{xxxx}+\tfrac23(u^2)_{xx}=0.
\tag{10}
\]

其实高频主部为 good Boussinesq。常背景 $(u_*,z_*)$ 的 Fourier 特征值满足

\[
(\lambda+i\mathsf B\xi)^2
=\tfrac43u_*\xi^2-\tfrac13\xi^4.
\tag{11}
\]

高频特征值纯虚，渐近为 $\pm i\xi^2/\sqrt3$；当 $u_*<0$ 时所有非零 Fourier 模态都没有实增长指数。这里的线性判定不依赖把实型改成复物理场。

取

\[
\alpha=\frac1{2\sqrt3},\qquad
\Psi=z+i\alpha u_x,\qquad m=\overline u.
\]

实场 $(u,z)$ 与复辅助变量 $\Psi$ 一一对应，只需 $\overline{\operatorname{Im}\Psi}=0$：

\[
u=m+\alpha^{-1}D^{-1}\operatorname{Im}\Psi,\qquad
z=\operatorname{Re}\Psi.
\]

式 (9) 在零平移框架中等价于

\[
\boxed{\Psi_t=-\frac{i}{\sqrt3}\Psi_{xx}
+\frac23u u_x.}
\tag{12}
\]

非线性是 $\Psi,D^{-1}\operatorname{Im}\Psi$ 的实二次多项式，没有空间导数损失。$m$ 和 $\overline z$ 守恒；非线性平均为 $\int uu_x=0$，所以要求的零虚部均值沿流保持。

### 自足局部存在性证明

对 $r\ge0$，在空间圆上定义

\[
\mathcal B(a,b)=(D^{-1}\mathcal P_xa)b.
\]

Fourier 权满足 $\langle k\rangle^r\le C_r(\langle n\rangle^r+\langle k-n\rangle^r)$。由 $\sum_{n\ne0}|n|^{-2}<\infty$ 和 $\ell^1*\ell^2\to\ell^2$，

\[
\|\mathcal B(a,b)\|_{H^r}
\le C_r\big(\|a\|_{H^r}\|b\|_{L^2}
+\|a\|_{L^2}\|b\|_{H^r}\big).
\tag{13}
\]

特别是式 (12) 的非线性 $N$ 在每个 $H^r$ 局部 Lipschitz，且

\[
\|N(\Psi)\|_{H^r}
\le C_r(|m|+\|\Psi\|_{L^2})\|\Psi\|_{H^r}.
\tag{14}
\]

线性组 $\exp(-itD^2/\sqrt3)$ 在所有 $H^r$ 酉。Duhamel 映射在 $C([-T,T],L^2)$ 的有界球上是压缩，只要 $T$ 由 $|m|+\|\Psi_0\|_{L^2}$ 的界取得足够小。这给双向时间的唯一实际 mild 流

\[
\Psi\in C([-T,T],L^2),\quad
u\in C([-T,T],H^1),\quad z\in C([-T,T],L^2).
\]

式 (14) 和 Gronwall 保证所有较高 $H^r$ 正则性在同一 $L^2$ 时间窗内保持；无需为每个 $r$ 重取趋于零的时间窗。因此光滑初值给同一非零时间窗上的真实实光滑 $(u,z)$。式 (12) 与恢复公式直接推出式 (9)，没有把形式谱时间当作实际解存在性证明。

辅助能量也可核验：

\[
\int\left[z^2+\frac1{12}u_x^2-\frac19u^3\right]dx
\]

沿光滑零平移解守恒。在 $u_*<0$ 常背景附近、固定空间均值后，其二次部分正定。这支持实型符号判定；本稿不据此宣称大数据全局存在。

## 3. 从实际标量流重建原 $M=3$ 实场

下面给出一个明确非空的物理逆图；不借用 $c\ne0$ 的旧统一背景逆定理。

### 3.1 非共振实常背景与有限交换

取 $r_*>0$、$d=hr_*/8$、$a_*>2d$、$a_*\ne6d$，并取

\[
p_*=a_*(1,-1,0),\qquad s_*=r_*(1,1,-2).
\]

此时

\[
\kappa=\tfrac{2r_*}{3}(-a_*^2+4d^2)<0,\qquad
a_3=d(-a_*^2+4d^2)\ne0.
\]

在接续稿的非恒定族 $p=a(1,-1,0),s=r(1,1,-2)$ 上，三个交换对数分别是

\[
\vartheta_- =D\log(a/2-d),\quad
\vartheta_- =D\log(a/2-d),\quad
\vartheta_+=D\log(a/2+d),
\]

其中此处 $d(x)=hr(x)/8$。故其具体分母和分子为

\[
\widehat Q=(D-a_0^--\vartheta_--\vartheta_+)
(D-a_1^--\vartheta_-)(D-a_2^-),
\]

\[
\widehat R_0=(D-a_2^+-\vartheta_--\vartheta_+)
(D-a_1^+-\vartheta_-)(D-a_0^+).
\tag{15}
\]

交换差在所选常背景均严格不为零，故其一般场小邻域保留全部三个有限交换和逐步逆交换，不要求邻近场仍在这个特殊二幅值族中。

常背景已经去掉二阶项，且

\[
Q_*=(D-a_*/2+d)(D+a_*/2+d)(D-2d)
=D^3+u_*D+v_*,
\]

\[
u_*=-a_*^2/4-3d^2<0,\qquad v_*=-a_3/2.
\tag{16}
\]

分母的三个 Floquet 指数为

\[
a_*/2-d,\quad -a_*/2-d,\quad 2d;
\]

分子的三个指数为

\[
-2d,\quad -a_*/2+d,\quad a_*/2+d.
\]

$a_*\ne6d$ 恰排除各自唯一可能的重复指数；三者实、相异，Floquet 倍子均为正实且分离。

### 3.2 标号 Floquet 旗标给出真实静态逆

给定接近 $(Q_*,Q_*+a_3)$ 的实光滑周期 $Q=D^3+uD+v$，取 $R_0=Q+a_3$。各算子的简单正实 Floquet 倍子和特征线按初始因子顺序标号。对 $Q$，先选对应原右因子的特征线，再添加中因子特征线，再取全空间；对 $R_0$ 使用原 numerator 的相应顺序。

设每级实解旗标的 Wronskian 为 $W_1,W_2,W_3$。常背景所有 Wronskian 在紧空间圆上非零；ODE 连续依赖使足够小的有限 $C^k$ 邻域保持它们非零。依次得到

\[
\alpha_{\rm right}=D\log|W_1|,\quad
\alpha_{\rm middle}=D\log|W_2/W_1|,\quad
\alpha_{\rm left}=D\log|W_3/W_2|.
\tag{17}
\]

这些系数周期，因为 Wronskian 只乘各级 Floquet determinant。它们构成唯一的指定标号因子分解。

为明确一般场的逆，而非只沿式 (15) 的两幅值族：将 $Q$ 的左、中、右因子系数记为 $q_L,q_M,q_R$，$R_0$ 的相应系数记为 $r_L,r_M,r_R$，所有因子均写成 $D-\text{coefficient}$。依次取

\[
\tau_{20}=D\log|r_L-q_L|,\quad
\widetilde a_2^+=r_L-\tau_{20},\quad
\widetilde a_0^-=q_L-\tau_{20},
\]

\[
\tau_{10}=D\log|r_M-\widetilde a_0^-|,\quad
a_1^+=r_M-\tau_{10},\quad
a_0^-=\widetilde a_0^--\tau_{10},
\]

\[
\tau_{21}=D\log|\widetilde a_2^+-q_M|,\quad
a_2^+=\widetilde a_2^+-\tau_{21},\quad
a_1^-=q_M-\tau_{21},\quad
a_2^-=q_R,\quad a_0^+=r_R.
\]

每一步是已核验交换式的精确逆，三个非零差在所选常背景开图持续成立。再恢复

\[
U_j=a_j^++a_j^-,
\qquad s_j=\frac4h(a_j^+-a_j^-).
\tag{18}
\]

这是实际、局部、实光滑的物理像逆。每个步骤只需有限阶微分、有限维实 ODE、简单特征投影和非零函数除法；因子标号不能丢掉。微分与逆交换可能损失有限阶正则性，所以不将其称为同一个单一 Sobolev 空间的 Banach 微分同胚。

式 (1) 保证重建场满足 $c=0,q=0,\chi=\kappa$；$Q$ 的二阶项为零保证恢复的共同场满足规范 $\overline b=0$ 与真实形状闭合式 (4)。商场 $p,s$ 的组件均值编码在标号因子的 Floquet 指数中；所有周期对数导数逆交换保持这些均值。

若先指定每个组件的空间均值，则应将标量初值限制到相应标号 Floquet 指数的子集，不能把该子集称为整个 $Q$ 系数空间中的普通开集。下面的真实流保持这个子集。这里的明确常背景具有非零组件均值；因此本图不自动覆盖每个组件空间均值都为零的严格 Casimir 叶。

### 3.3 沿实际标量流保持物理图

对式 (7) 的光滑解，$Q$ 和 $R_0=Q+a_3$ 都满足同一个真实 periodic Lax 方程。其空间 ODE 是三维一阶系统；时间输运只在这三维解空间上作有限维 ODE，不需要求任意函数的后向热初值问题。

例如 $Qf=0$，令 $Y=(f,f_x,f_{xx})^T$。空间矩阵与零平移时间矩阵为

\[
B_Q=\begin{pmatrix}0&1&0\\0&0&1\\-v&-u&0\end{pmatrix},
\]

\[
C_Q=\begin{pmatrix}
-2u/3&0&-1\\
v-2u_x/3&u/3&0\\
v_x-2u_{xx}/3&v-u_x/3&u/3
\end{pmatrix}.
\tag{19}
\]

式 (8) 正是 $B_{Q,t}=C_{Q,x}+[C_Q,B_Q]$；$R_0$ 的公式只把 $v$ 换成 $v+a_3$。周期性给 monodromy 的有限维相似演化，因此简单正实倍子及其标号旗标保持；初始非零 Wronskian 和逆交换差由连续性在一段非零时间内仍非零。

这些有限 ODE、简单 Floquet 投影、Wronskian 对数导数和有限逆交换，都在所述分级光滑开图上光滑依赖系数。因而物理像逆不只有集合层面的单射性：它是显式光滑左逆，微分也左消物理推前。

故式 (12) 的实际光滑标量流可以在这个时间窗通过式 (17)–(18) 回拉为原 $M=3$ 的真实光滑周期场。原约束 Hamiltonian 向量在该物理图中的推前已经由式 (6)–(7) 确认；对该等式应用上述像逆的微分，回拉向量就是原式的真实向量。

若另一条同初态、同平均共同场规范的原光滑解留在此图中，则其标量 $Q$ 满足同一个半线性 Schrödinger mild 问题；标量唯一性与标号物理逆共同给原场唯一性。对任意预先规定的光滑 $\mathsf B(t)$，令 $\tau(t)=\int_0^t\mathsf B(\sigma)d\sigma$，从零平均共同场流恢复

\[
p_{\mathsf B}(x,t)=p_0(x-\tau(t),t),\quad
s_{\mathsf B}(x,t)=s_0(x-\tau(t),t),
\]

\[
b_{\mathsf B}(x,t)=b_0(x-\tau(t),t)+\mathsf B(t),\quad
U_{\mathsf B}(x,t)=U_0(x-\tau(t),t)+\mathsf B(t).
\]

平移之外须包含这个共同 $U$ 加量。此时实际 $U$ 的组件平均整体加 $\mathsf B$，实际 $Q_b$ 的 Floquet 指数也整体加 $\mathsf B/2$；被保持的是周期去项代表的标号指数及商场组件 Casimir。

**实际流结论。** 在上述非共振实常背景附近，满足完整兼容条件的实光滑初值、合法最小三阶因子图和规定平均共同场，有一个非零时间窗上的唯一真实原 $M=3$ 流。其构造在分级光滑物理像上成立；没有声称整个单一 Sobolev 物理相空间的无损流。$\kappa$ 是由初态选定、由原约束链守恒的能量水平，冻结其轨道值不等于把它改称 Casimir 或额外进行能量商。

仍未证明谱迹独立性、无限维 Liouville 完备性或图外真实流。

## 4. 全 $M$ 常背景的约束主符号

这一节先给所有有限 $M\ge3$ 的实常背景代数证明，不借用 $M=3$ 来替代全场。非恒定背景所需的额外主约束消元在下一节独立证明。

### 4.1 规范 shear 与三次恒等式

作正则 canonical shear

\[
Y=p+\tfrac12Rs,\qquad q=\Pi(Ys),
\]

\[
H_0=hM\int[V(Y,s)+\Pi(sY_x)]dx,\qquad
V=\Pi\left[\tfrac12(Y-Rs/2)^2s+\tfrac\beta3s^3\right],
\]

\[
\chi=-2V+\Pi(Ys_x-sY_x).
\tag{20}
\]

底层括号仍是 $-\operatorname{offdiag}D$。在常背景 $Y=T,s=S$，有 $\Pi(TS)=0$、$\kappa=-2V(T,S)\ne0$。记

\[
c=V_Y,\qquad e=V_s,\qquad
\Pi(cT+eS)=-3\kappa/2.
\]

对任意零格点平均 $S$，令 $Z=RS$。定义 $Z_j^\pm=Z_j\pm hS_j/2$。由 $\delta_-Z=M_-S$，

\[
Z_j^-=Z_{j-1}^+.
\]

对立方差作周期望远镜求和立即给

\[
\boxed{\Pi[S(RS)^2]=-\frac{h^2}{12}\Pi S^3.}
\tag{21}
\]

这个全 $M$ 恒等式是约束后振荡对的关键，不能由有限周期特例代替。

### 4.2 主、次切向和秩一修正

变分 $(y,z)=(\delta Y,\delta s)$ 的主约束为

\[
\phi=\Pi(Sy+Tz)=0.
\]

次约束的常系数线性化为

\[
\psi=-2\Pi(cy+ez)+D\Pi(-Sy+Tz)=0.
\tag{22}
\]

在 $S,T$ 均非零的正则符号图上，消元后的高频切空间是

\[
\mathcal E=\{\Pi(Sy)=0,\ \Pi(Tz)=0\},
\quad \dim\mathcal E=2(M-2).
\tag{23}
\]

未闭合主部是 $\operatorname{diag}(-D^2,D^2)$，乘子项为 $-(T,S)^TDb$。原 $\rho=X_{H_0}\chi$ 的三阶项是 $D^3\phi$，在主切向上消失；保留次阶并用 $b_x=\rho/(3\kappa)$ 得

\[
L_{\rm princ}=D^2\mathcal A,\qquad
\mathcal A=\operatorname{diag}(-I,I)-(T,S)^T\ell
\quad\text{在 }\mathcal E,
\tag{24}
\]

\[
\ell_y=\frac{(4c-2V_{YY}T)^T}{3M\kappa},
\qquad
\ell_z=-\frac{2(V_{sY}T)^T}{3M\kappa}.
\tag{25}
\]

这里的投影及 $\rho$ 来自完整主、次配对，未省略退化的主约束块。Euler Hessian 恒等式给 $\ell_yT+\ell_zS=0$；式 (21) 和 $\beta=h^2/32$ 进一步给

\[
\ell_yT=-2/3,\qquad \ell_zS=2/3.
\tag{26}
\]

因此 $\operatorname{span}\{(T,0),(0,S)\}$ 上的矩阵为

\[
\begin{pmatrix}-1/3&-2/3\\2/3&1/3\end{pmatrix},
\]

其特征值是 $\pm i/\sqrt3$。另两类特征空间分别是 $\ell_y y=0,\Pi(Sy)=0$ 和 $\ell_z z=0,\Pi(Tz)=0$，各维数 $M-3$，特征值分别为 $-1,+1$。故

\[
\boxed{\operatorname{char}_{\mathcal E}(\lambda)
=(\lambda^2+1/3)(\lambda^2-1)^{M-3}.}
\tag{27}
\]

实际 Fourier 时间主指数为

\[
\pm i\xi^2/\sqrt3
\quad\text{各一个},\qquad
+\xi^2,\ -\xi^2
\quad\text{各 }M-3\text{ 个}.
\tag{28}
\]

没有额外非零频率的零主指数。空间零 Fourier 模态另由 component Casimir 和共同平移零模处理；常背景本身又有平移固定点，不能据此宣称零动量水平正则。

所以 $M=3$ 恰留下全部高频振荡的一对通道；$M>3$ 的兼容常背景冻结谱仍有前向与后向热通道。全 $M$ 的约束链并未在这一谱中消掉混合热主部。常背景在固定组件均值的 $\Gamma=0$ 动量水平上是临界点；这些冻结热模尚未被实现为正则商上的精确高频初值曲线，因而不能仅凭式 (28) 推出正则商流的 $C^1$ 不适定。

## 5. 全 $M$ 非恒定背景：完整主约束消元

现在令兼容背景 $Y=T(x),s=S(x)$ 非恒定，仍满足 $q=0$、$\chi=\kappa\ne0$。$\kappa$ 是当前状态的能量值；下面的高频主符号计算没有额外把整个相空间固定到某个能量水平。改变 $\kappa$ 的常数模及其乘子变化属于有限秩全局项，不改变微分主符号。

令 $c=V_Y,e=V_s$，所有内积用 $\Pi$。未加共同场乘子的原 Hamiltonian 向量与次约束线性化是

\[
F_0=(-Y_{xx}-D e,\ s_{xx}-D c),
\]

\[
A_\chi=(-S D-2c+S_x,\ T D-2e-T_x).
\tag{29}
\]

原一致性源为 $\rho=A_\chi F_0$。其线性化中的 $(\delta A_\chi)F_0$ 至多一阶；$A_\chi\delta F_0$ 的三阶、二阶行系数依次是

\[
(S,T)D^3,\qquad
(4c-2V_{YY}T-S_x,\ -2V_{sY}T-T_x)D^2.
\tag{30}
\]

不能把这个三阶项在变量背景上只按冻结系数删除。主切向恒等式 $\phi=\Pi(Sy+Tz)=0$ 及 $D^3\phi=0$ 给

\[
\Pi(Sy_{xxx}+Tz_{xxx})
=-3\Pi(S_xy_{xx}+T_xz_{xx})+O(D).
\]

故完整主约束消元后的二阶行系数为

\[
r_y=4c-2V_{YY}T-4S_x,\qquad
r_z=-2V_{sY}T-4T_x.
\tag{31}
\]

真实次约束闭合 $b_x=\rho/(3\kappa)$ 的线性化给

\[
\mathcal A=\operatorname{diag}(-I,I)-(T,S)^T\ell,
\qquad \ell=(r_y,r_z)^T/(3M\kappa)
\tag{32}
\]

作用在主、次配对的高频切空间 $\mathcal E$ 上。背景 $b$ 对场变分的一阶输运不影响这个二阶矩阵。空间投影、共同平移和组件 Casimir 同样不改这个局部主符号。

写 $\chi_{\rm pot}=-2V$、$\Omega=\Pi(TS_x-ST_x)$，所以 $\kappa=\chi_{\rm pot}+\Omega$。式 (21) 给

\[
\Pi[(4c-2V_{YY}T)T]=-2\chi_{\rm pot}.
\]

$q_x=0$ 又给 $2\Pi(TS_x)=\Omega$。因此

\[
\ell_yT=\frac{-2\chi_{\rm pot}-4\Pi(TS_x)}{3\kappa}
=-2/3,\qquad \ell_zS=2/3.
\tag{33}
\]

第二式也由 cubic Euler Hessian 和 $q_x=0$ 得到。这里的 $-4S_x,-4T_x$ 正好吸收 Wronskian 项；不加入它们就不能把常背景的归一化照搬过来。

还可排除主符号的逐点退化。若某点 $S=0$，则 $V=0$，且 $q_x=0$ 迫使 $\Pi(TS_x)=0$，故 $\chi=0$，矛盾。若某点 $T=0$，则

\[
V(0,S)=\Pi[S(RS)^2]/8+\beta\Pi S^3/3=0
\]

由式 (21) 成立；$q_x=0$ 又给 $\Pi(ST_x)=0$，仍矛盾。因此 $\kappa\ne0$ 强迫 $T,S$ 在整个空间圆上均非零。因 $q=0$，两者又实正交。

于是 $\mathcal E$ 是维数恒定 $2(M-2)$ 的光滑实束；式 (33) 使振荡二维子束及两个热型子束处处成立。式 (27)–(28) 原封不动推广到所有这些非恒定背景，热型子束的秩分别为 $M-3$，振荡子束秩为二；没有额外零主指数。特征值彼此分离，紧空间圆上给光滑有界的主符号谱投影。

对一般非恒定的平移自由或局部自由状态，这个结论也适用于完整非零模 Dirac 后、再除共同平移的正则商主符号。它解决了常背景动量临界点的范围缺口，但依然只证明真实闭合方程的约束微分主部；尚未构造商上的精确高频曲线，亦未证明全 $M>3$ 的 $C^1$ 流不适定或任何一般实际局部流。

## 证据与范围

新增标量证书：[singular_m3_flow_principal_certificates.py](../../Workspaces/dlw_recovery_20261011/singular_m3_flow_principal_certificates.py) 与[结果 JSON](../../Workspaces/dlw_recovery_20261011/singular_m3_flow_principal_certificates.json)。42 项 exact 检查全部通过，涵盖去 $D^2$、负 $t_2$、实变量与 Schrödinger 变换、能量通量、九项零曲率、交换恒等式、原 PDE 的三项势差与六项 Riccati 微分、四项通用一阶因子 intertwiner、常背景归一化和 Fourier 色散；没有重跑既有 33 项检查。脚本 SHA256：7a46e468bafbd2b1a169da2637f81aecf25c407508ccf78f0b8eee77f646c50e。

全 $M$ 式 (21)、(24)–(28) 的独立推导与范围审稿见 [singular_branch_independent_audit.md](../../Workspaces/dlw_recovery_20261011/singular_branch_independent_audit.md) §8。独立 [singular_principal_independent_certificates.py](../../Workspaces/dlw_recovery_20261011/singular_principal_independent_certificates.py) 与[其 JSON](../../Workspaces/dlw_recovery_20261011/singular_principal_independent_certificates.json) 在 $M=3,\ldots,10$ 的 exact rational 矩阵上通过 56 项断言。本稿全 $M$ 证明使用望远镜恒等式及秩一分解，有限周期证书是核验。

实际 $M=3$ 桥梁、一般六系数互逆和平均共同场恢复还见独立 [singular_m3_flow_independent_audit.md](../../Workspaces/dlw_recovery_20261011/singular_m3_flow_independent_audit.md)。其 [因子证书](../../Workspaces/dlw_recovery_20261011/singular_m3_factor_independent_certificates.py) 另有 15 项新精确断言，未重跑旧检查。

变量背景的新 [singular_variable_principal_certificates.py](../../Workspaces/dlw_recovery_20261011/singular_variable_principal_certificates.py) 与[JSON](../../Workspaces/dlw_recovery_20261011/singular_variable_principal_certificates.json) 在 $M=3,\ldots,8$ 的 $q=q_x=0$、$\Omega\ne0$、$\kappa\ne0$ first jets 上完成 66 项 exact rational 检查：直接提取 $A_\chi\delta F_0$ 的三阶、二阶系数，完整消去 $D^3\phi$，核验 $\pm2/3$、切向不变性和完整特征多项式。脚本 SHA256：3c1250c0bb3265981824d14a2bad3c1a77fdb9023622af29ca4bfe2a3587403f。它没有构造周期物理曲线，也未重跑任何旧证书。式 (29)–(33) 同时已获独立手推复核，见上述独立审稿 §9。

真实标量存在性由式 (13)–(14) 的自足 Duhamel 证明给出；真实物理回拉由分离正实 Floquet 旗标、非零 Wronskian、显式一般逆交换、光滑左逆和实际零曲率给出。全 $M$ 的变量背景约束主符号已证明，但一般实际局部流、精确高频物理曲线、谱独立性与 Liouville 完备性仍未完成。
