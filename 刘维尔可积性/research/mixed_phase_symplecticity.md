# 混合参数相空间的弱辛性与守恒族微分切向性

2026-10-11。真实光滑混合解族的弱辛形式与辅助守恒场切向性证明。

本文件接续 full_m_mixed_flow.md，但不修改该已交付文件。其先前“中心拉回二形式非退化未知”及“辅助切向性未知”的两项判断，由下列证明分别推进到**弱非退化成立**与**已验证对易族的微分切向性成立**。辅助非线性流存在、正则状态逆和 Liouville 完备性仍未证明。

## 1. 精确适用域与依赖

固定任意有限格点周期 $M\ge2$、空间圆周 $\mathbb T_L$、$c\ne0$、固定常数平均通量 $q$，在旧稿的约化物理分支与固定各组件空间均值叶上工作。记 $v=p+Rs/2$，真实方程为

$$
y_t=X_K(y),\quad y=(v,s),\qquad
v_t=-D^2v+D N_v(v,s),\quad s_t=D^2s+D N_s(v,s),
$$

其中 $N_v,N_s$ 是已核实的至多三次多项式。真实混合输入是 $s(-T)$ 与 $v(T)$。取足够小 $T$ 与一个开放混合数据球，使旧热核构造的收缩常数 $\kappa<1$。

第一部分弱辛性只依赖：

1. 该实际混合解与其端点解析/光滑依赖；
2. 原物理 Hamiltonian 和准确剪切 Poisson 结构；
3. 端点作用量变分身份；
4. 自足 Carleman 的完整状态端点唯一性。

第二部分守恒族切向性额外依赖所用具体 $I_n$ 的**精确场身份**
$[X_{I_n},X_K]=0$，而非沿一条数值轨道的近似守恒。旧全 M 层级通过 $\{I_n,K\}=0$ 与常数 Poisson Jacobi 身份提供这一前提；本文独立核查的是该前提如何推出实际微分切向性，不重新证明所有阶层级代数。

## 2. 参数、均值与配对：不使用全 Banach 对偶识别

令

$$
\mathscr E=\left\{f\in C^\infty(\mathbb T_L;\mathbb R^M):
\Pi f=0,\quad\int_{\mathbb T_L}f_jdx=0\ \text{对每个 }j\right\}.
$$

采用正定配对 $\langle f,g\rangle=h\sum_j\int f_jg_jdx$。
$D:\mathscr E\to\mathscr E$ 是连续 Fréchet 同构，$D^{-1}$ 为零空间均值逆导数。固定背景组件均值 $\bar v,\bar s$，定义

$$
Q=s-\bar s,\qquad P=D^{-1}(v-\bar v).
$$

因此 $P,Q\in\mathscr E$，并且在同一均值叶上
$Q_t=K_P,\ P_t=-K_Q$。混合参数为

$$
a=Q(-T),\qquad b=P(T).
$$

原来的 $g_v=v(T)$ 与 $b$ 关系是 $g_v=\bar v+Db$，故在 Sobolev 实现中
$a\in H^r,\ b\in H^{r+1}$，不能把两者都直接当原 $H^r$ 输入。Fréchet 平滑空间中 $D^{-1}$ 连续同构，参数是 $\mathscr E\times\mathscr E$ 的开集 $\mathcal U_T$。

$\mathcal U_T$ 可以定义为低阶 $H^r\times H^{r+1}$ 开球与平滑空间的交，$r\ge2$。该球在 Fréchet 拓扑确实开放。固定均值的仿射部分已由 $\bar v,\bar s$ 消去，所有参数变分及 $P,Q$ 输出变分都在 $\mathscr E$。

我们只使用平滑函数之间的积分配对和其非退化性。**不把 $\mathscr E$ 等同于完整拓扑对偶，也不把下文转置认作一个在全 Banach 对偶上可逆的算子。** 若 $f\in\mathscr E$ 与所有 $\mathscr E$ 测试配对为零，则取测试 $f$ 本身就得 $f=0$。格点平均与组件空间均值约束排除了潜在常数/均值 annihilator。

平滑端点的真实解空间与时间都平滑到闭区间：全区间热核正则提升可反复增加任意小的空间阶数 $0<\alpha<1$，光滑规定端点的热项无边界损失；随后自治方程给全部时间导数。其端点微分也平滑到两端。这个闭区间事实是下面端点 Carleman 的必要条件，不能仅用“内点平滑”替代。

光滑依赖可以在已有 Banach 解析依赖上逐阶提升：每个端点导数先在 $C_tH^r$ 中由收缩微分存在，满足线性化 mild 方程；系数是平滑背景的有限阶乘积，高阶导数的额外源项是较低端点导数的有限乘积。热核提升给每个固定空间/时间半范数的连续估计。逐导数阶与半范数归纳得 Bastiani $C^\infty$ Fréchet 解映射，不使用一个无条件的 Fréchet 逆函数定理。

## 3. 作用量 Hessian 与拉回形式

令 $G(a,b)$ 为该真实解，
$$
P_-(a,b)=P(-T),\qquad Q_+(a,b)=Q(T).
$$

旧 type-II 作用量是

$$
S_T(a,b)=\langle b,Q_+\rangle
-\int_{-T}^{T}\bigl(\langle P,Q_t\rangle-K(P,Q)\bigr)dt .
$$

对本节闭区间平滑解，时间分部积分严格给

$$
dS_T=\langle P_-,da\rangle+\langle Q_+,db\rangle . \tag{1}
$$

令

$$
H=D_aP_-,\qquad \mathcal K=D_bP_-,\qquad
\mathcal L=D_aQ_+ .
$$

标量函数的二阶微分对称性给

$$
\langle Ha_1,a_2\rangle=\langle Ha_2,a_1\rangle,\qquad
\langle a_1,\mathcal Kb_1\rangle
=\langle\mathcal La_1,b_1\rangle . \tag{2}
$$

后一式是两块 Hessian 的**实际配对身份**。可以把 $\mathcal L$ 记成 $\mathcal K^\top$，但无需引入完整对偶空间上的 adjoint 或其满射性。

取环境形式

$$
\Omega((\delta Q,\delta P),(\eta Q,\eta P))
=\langle\delta Q,\eta P\rangle-\langle\eta Q,\delta P\rangle,
\quad \Omega=dQ\wedge dP .
$$

这个符号与 $\iota_{X_K}\Omega=dK$ 一致。真实解族保持形式，故中心与两端拉回相等：

$$
\omega_T=E_0^*\Omega=E_-^*\Omega=E_+^*\Omega.
$$

在初始端 $Q_-=a$，$dP_-=H\,da+\mathcal K\,db$。用 (2) 消掉 $H$ 对称块，得到完全明确的式子

$$
\omega_T((u,v),(a_1,b_1))
=\langle u,\mathcal Kb_1\rangle
-\langle a_1,\mathcal Kv\rangle . \tag{3}
$$

因此 $\omega_T$ 是光滑闭二形式。式 (3) 的符号已按 $\Omega=dQ\wedge dP$ 核对。

## 4. 新增定理：弱非退化不需要中心微分像稠密

假设 $(u,v)\in\ker\omega_T$。

先测试 $(a_1,0)$，(3) 给
$\langle a_1,\mathcal Kv\rangle=0$ 对所有 $a_1\in\mathscr E$。
$\mathcal Kv\in\mathscr E$，所以 $\mathcal Kv=0$。

考虑混合端点方向 $(0,v)$ 的真实线性化轨道。其初始变分是

$$
\delta Q(-T)=0,\qquad \delta P(-T)=\mathcal Kv=0 .
$$

换回物理变量，$\delta s(-T)=0,\ \delta v(-T)=D\delta P(-T)=0$，是**完整初始状态为零**，不是只有一半混合输入为零。线性化轨道闭区间光滑，满足
$(\partial_t-A)z=Bz_x+Cz$，$A=\operatorname{diag}(-D^2,D^2)$，$B,C$ 有界。端点 Carleman 唯一性给整轨道为零，故规定的末端变分 $\delta P(T)=v$ 为零。

剩下 $(u,0)$。测试 $(0,b_1)$，由 (2)–(3)
$\langle\mathcal Lu,b_1\rangle=0$ 对所有 $b_1\in\mathscr E$，故 $\mathcal Lu=0$。

对应方向 $(u,0)$ 的真实线性化轨道满足

$$
\delta P(T)=0,\qquad\delta Q(T)=\mathcal Lu=0 ,
$$

因此完整终止物理状态为零。反向时间 Carleman（将 $A$ 换成 $-A$）给整轨道为零，故 $u=\delta Q(-T)=0$。

于是

$$
\boxed{\ker\omega_T=0.} \tag{4}
$$

**定理。** 平滑混合参数开集 $\mathcal U_T$ 带有由原物理环境形式拉回的弱辛形式 $\omega_T$。这个证明不用中心微分像稠密、不用 $\mathcal K$ 满射、不用其有界逆。

端点 Carleman 的合法性与内点版相同：零端点时间迹使向外延零不产生 Dirac 项，平滑闭区间轨道属于 $H^1_tL^2\cap L^2_tH^2$，空间谱截断和时间卷积在图范数中稠密；指数时间权重恒等式再吸收有界一阶项。所有这些条件在本节轨道与变分上满足。

“弱”必须保留：$\omega_T^\flat$ 注入拓扑对偶，但未证明它满射、有连续逆或等价于强辛 Banach 结构。热型 Hessian 块可以单射而逆无界，(4) 与高频初值不适定没有冲突。

中心取值此前已证明为单射，故参数点可唯一标识真实物理状态。但这里给该像的是混合参数传递的拓扑；没有证明它等同于物理场继承的 $H^r$ 或 $C^\infty$ 子空间拓扑。应称“混合条件参数相空间/其单射物理像”，不能说已经得到任意一般物理初值的开放 Sobolev 相空间。

## 5. 新增切向性引理：精确对易推出实际微分切向

设某个已验证泛函 $I$ 的物理向量场 $X_I=J\,dI$ 是有限阶平滑场表达式，保持格点与组件空间均值，并满足精确身份

$$
[X_I,X_K]=0. \tag{5}
$$

对任一平滑闭区间真实混合解 $y_g(t)$，设

$$
Y_I(t)=X_I(y_g(t)).
$$

链式法则与 (5) 给

$$
\partial_tY_I=DX_I(y_g)X_K(y_g)
=DX_K(y_g)X_I(y_g)
=DX_K(y_g)Y_I. \tag{6}
$$

所以 $Y_I$ 是真实物理方程的线性化解，而非只在中心定义的形式方向。它平滑直到两端，并由 $J$ 的 $P_0D$ 结构保持全部均值。

在原混合 $s_-,v_+$ 坐标中，规定方向是
$(Y_{I,s}(-T),Y_{I,v}(T))$。在本文件 $a=Q_-,b=P_+$ 坐标中必须改成

$$
\eta_I(g)=\bigl(Y_{I,s}(-T),\ D^{-1}Y_{I,v}(T)\bigr)
\in\mathscr E\times\mathscr E . \tag{7}
$$

这个 $D^{-1}$ 不能省略。平滑开放球允许每个固定方向的小参数扰动。

收缩方程的微分 $DG(g)[\eta_I]$ 满足同一线性化 mixed mild 问题及同一端点。其线性算子范数不超过原来的 $\kappa<1$，故在 $C_tH^r$ 中唯一。$Y_I$ 本身满足该 mild 方程，因此

$$
DG(g)[\eta_I](t)=Y_I(t),\qquad
DE_0(g)[\eta_I]=X_I(E_0(g)). \tag{8}
$$

这证明 **真实中心像的微分切向性**，而不仅是环境固定均值叶的形式切向性。

## 6. 拉回 Hamiltonian 族、对合与仍缺的流

令 $\widehat I=I\circ E_0$，$\widehat X_I=\eta_I$。由 (8) 与环境 Hamilton 身份，

$$
\omega_T(\widehat X_I,\zeta)
=\Omega(X_I,DE_0\zeta)
=dI[DE_0\zeta]
=d\widehat I[\zeta]. \tag{9}
$$

因此每个满足第 5 节前提的成员都在**同一弱辛参数相空间**有实际的光滑微分 Hamiltonian 向量场。弱非退化保证这个向量场唯一。其参数表达式可能损失越来越高阶导数，但对每个固定阶在 Fréchet 平滑域仍有意义。

若既有精确身份 $\{I_m,I_n\}=0$ 适用，则

$$
\{\widehat I_m,\widehat I_n\}_{\omega_T}
=\{I_m,I_n\}\circ E_0=0. \tag{10}
$$

同理，相关向量场的 Lie 括号由 $DE_0$ 推到环境括号；$DE_0$ 单射使已对易环境场的拉回场亦微分对易。链式法则的二阶 $E_0$ 项因 Hessian 对称抵消，毋须中心像已是环境 Banach 子流形。

物理 $K$ 也可用此引理：$Y_K=y_t$ 满足线性化方程，方向
$(s_t(-T),D^{-1}v_t(T))$ 是 $\widehat K=K\circ E_0$ 的 Hamiltonian 向量场。来自较长窗口的真实轨道可按时间平移给较短窗口上的实际积分曲线，保持 $\omega_T$，具有先前证明的按尺度 germ 复合性质。

**这些身份没有建立所有辅助非线性流。** 即使 $\widehat X_{I_n}$ 在 $C^\infty$ 中是光滑映射，Fréchet ODE 仍不自动有局部解；阶数上升的导数损失尤其不能由 Banach Picard 直接处理。本次关掉的是旧“辅助切向性”缺口的微分部分，留下辅助流实际存在和保持条件域的部分。

## 7. 可准确使用的结论

- 全有限 $M$、周期空间、$c\ne0$、固定 $q$、平滑混合输入的小开集上，原物理形式拉回是**弱非退化闭二形式**。
- 中心取值与其微分单射；按混合参数识别的条件物理像承载这一弱辛结构。
- 每个已严格验证与 $K$ 对易、保持均值的有限阶层级成员，其物理 Hamiltonian 场在中心像上**实际微分切向**；拉回泛函有唯一 Hamiltonian 向量场，已验证的对合身份在同一相空间保持。
- 物理时间运动由较长真实窗口向较短窗口给实际弱 Hamiltonian germ；这不要求反向 Sobolev 初值半群。

仍未证明强/正则状态逆、传递拓扑的内在物理刻画、全部辅助非线性流、全非线性逆谱、最大对合族或无限维 Liouville 完备性。本文件的正面结构结论不等于完整可积性定理。
