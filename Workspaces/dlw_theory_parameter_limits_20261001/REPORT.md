# DLW：两个结构参数的谱范围限制

2026年10月1日。理论推导与冻结预测先于定向核对。

**摘要。** 固定物理参数与同一连续单孤子谱族，两个结构常数只能对纵向相位的二次谱曲率作仿射校准。归一化相位系数的十倍改善要求谱尺度比不超过 $5+2\sqrt5$，并满足参数可行性与有限步长余量。相位缺陷确实对应一个物理量：同谱离散孤子的横向 $v$ 质量偏差。然而，共同物理初值使这项偏差由守恒律完全消去。另从物理方程推得：尺度比为 $2$ 时，共同初值下的领先 $u$ 误差初始速度至多改善五倍，尽管相位系数允许改善三十二倍。结论给出校准的范围及限制；尚未证明指定正时间的双场数量级改善。

## 1　比较对象与正则谱域

固定 $a$、物理格距 $h>0$、精确的 $x,t$ 微分及同一物理重构。仅允许原有两个常数 $\alpha,\beta$，在整段谱区间以及步长细化时共用。连续目标的谱参数、物理初值和评价指标不随校准改变。自然有限 $h$ 精确族自身的初态偏移将在§4与共同初值的演化比较分开。

记 $P=p-a$、$Q=q+a$、$\Gamma=-P/Q>0$，并固定 $\Gamma\ne1$。令 $A=P^{-1}-Q^{-1}$，谱域 $I=[A_-,A_+]$ 为同一非零半轴上的非退化紧区间。由定义直接得到

$$
P^{-1}=\frac{A}{1+\Gamma},\qquad Q^{-1}=-\frac{\Gamma A}{1+\Gamma},\qquad
L=\frac{1-\Gamma}{1+\Gamma}A,\qquad K=p+q=\frac{\Gamma^2-1}{\Gamma A}.
$$

采用 $K>0$ 的正单孤子分支，故 $\operatorname{sign}A=\operatorname{sign}(\Gamma-1)$。下文整区间的物理结论针对逐个 $N=1$ 的连续 Gram 孤子族。相位公式可逐谱用于多孤子，但多孤子的交叉分母和无零 $\tau$ 域须另行验证；固定 $\Gamma$ 不保证任意谱组合构成全局正则多孤子。

已有两壁结构为 $s_\pm=a+\alpha h^2\pm(h+\beta h^3)/2$。写 $\mu=\alpha h^2$、$r_h=1+\beta h^2$、$H=hr_h$，精确格点乘子与纵向频率为 [1]

$$
\chi_h=\frac{P-\mu+H/2}{P-\mu-H/2}\frac{Q+\mu+H/2}{Q+\mu-H/2},\qquad k_h=\frac{\log\chi_h}{h}.
$$

取从 $h=0$ 延拓的实正分支。设 $M=\max_I|A|$、$\sigma=\operatorname{sign}A$、$c_\Gamma=\max(1,\Gamma)/(1+\Gamma)$。整段区间保持该分支的精确条件为

$$
r_h>0,\qquad c_\Gamma M\left[\sigma\alpha h^2+\frac{h(1+\beta h^2)}2\right]<1.
$$

要求一段步长范围都正则时，此条件须在整个步长范围检查。参数有界本身不保证粗格距正则。

## 2　谱曲率的最佳校准及十倍门槛

冻结相位指标 $E_h(\alpha,\beta)=\sup_{A\in I}|(k_h-L)/L|$。谱参数远离极点且常数有界时，已有相位展开可统一加强为

$$
\frac{k_h-L}{L}=h^2q_{\alpha,\beta}(A)+R_h(A),\qquad
q_{\alpha,\beta}=\beta+\alpha A+C_\Gamma A^2,\qquad
C_\Gamma=\frac{\Gamma^2+\Gamma+1}{12(\Gamma+1)^2}>0.
$$

**定理1：最佳一致剩余。** 设 $m=(A_-+A_+)/2$、$d=(A_+-A_-)/2$。任意两常数都满足

$$
\|q_{\alpha,\beta}\|_{\infty,I}\ge E_*:=\frac{C_\Gamma d^2}{2}
=\frac{C_\Gamma(A_+-A_-)^2}{8}.
$$

证明只需三个谱位置：$q(m-d)+q(m+d)-2q(m)=2C_\Gamma d^2$，而若三处绝对值均不超过 $E$，左侧不超过 $4E$。取

$$
\alpha_*=-2C_\Gamma m,\qquad \beta_*=C_\Gamma(m^2-d^2/2)
$$

即有 $q_*=C_\Gamma[(A-m)^2-d^2/2]$，端点为 $E_*$，中点为 $-E_*$，整个区间绝对值不超过 $E_*$。等号迫使三个位置分别取这三个值，因此最优常数唯一。此为二次函数的经典最佳一致逼近；本题的增量在谱域、有限步长和物理纠正后的限制。

受限常数上的 $E_*$ 仍是下界。闭紧可行集中，等号达到当且仅当上述最优点可行。只用严格正则条件定义开集时，还须区分下确界与实际取到最优值。最优常数只依赖 $\Gamma,I$，不依赖 $h$。

原结构 $\alpha=\beta=0$ 的相位首项指标为 $E_0=C_\Gamma M^2$。设 $m_0=\min_I|A|>0$、$\mathcal R=M/m_0$。同半轴使区间宽度等于 $M-m_0$，从而

$$
\frac{E_*}{E_0}=\frac{(1-\mathcal R^{-1})^2}{8},\qquad
\frac{E_*}{E_0}\le\frac1{10}\ \Longleftrightarrow\ 
\mathcal R\le5+2\sqrt5\simeq9.47214.
$$

严格小于门槛、最优点可行且 $h$ 足够小时，十倍相位改善可实现；严格大于门槛时，任意冻结有界常数集在充分小 $h$ 下均不能实现。等号处首项没有余量，须另作有限 $h$ 判定。谱范围极宽时最优比值趋于 $1/8$，改善上限趋于八倍。这个门槛依赖所冻结的归一化相位指标；未归一化的相位及整场误差不能直接沿用。

**定理2：任何固定有限步长都不能整段完全拟合。** 固定 $h>0$ 后，$\chi_h(A)$ 是有理函数。若整段相位完全匹配，就有 $\chi_h(A)=\exp[h(1-\Gamma)A/(1+\Gamma)]$。对数导数将是非零常数；而任何非零有理函数的对数导数在无穷远为 $O(1/A)$。区间上的等式给出有理恒等式，因而矛盾。该证明允许分子分母约消，不依赖小步长展开。

## 3　有限步长的余项和区间认证

这里给出可检查的充分条件。预先限定 $|\alpha|\le a_0$、$|\beta|\le b_0$、$0<h\le h_0$，定义

$$
\varepsilon_0=h_0^2,\quad s=c_\Gamma M,\quad \rho=a_0\varepsilon_0s<1,\quad
R_b=1+b_0\varepsilon_0,\quad \delta_b=(1-\rho)^2,\quad
q_b=\frac{h_0R_bs}{2(1-\rho)}<1,\quad b_0\varepsilon_0<1.
$$

这些条件保证整个参数盒在全部 $0<h\le h_0$ 上正则。记 $J=\Gamma M^2/(1+\Gamma)^2$，$B_r=b_0(3+3b_0\varepsilon_0+b_0^2\varepsilon_0^2)$，以及 $T_\Gamma=(1+\Gamma+\Gamma^2+\Gamma^3+\Gamma^4)/[80(1+\Gamma)^4]$。则

$$
\sup_I|R_h|\le h^4B,
$$

$$
\begin{aligned}
B={}&\frac{a_0b_0M+12a_0^2E_0+\varepsilon_0a_0^2J(b_0+a_0M)}{\delta_b}\\
&+\frac{E_0(B_r+a_0M+\varepsilon_0a_0^2J)}{\delta_b^2}
+\frac{a_0s^3}{2\delta_b}
+\frac{R_b^5T_\Gamma M^4}{\delta_b^3(1-q_b^2)}.
\end{aligned}
$$

证明基于精确差商积分。令 $x=P^{-1}$、$y=Q^{-1}$、$\widetilde x=x/(1-\mu x)$、$\widetilde y=y/(1+\mu y)$、$D=(1-\mu x)(1+\mu y)$，直接通分得到 $\widetilde x+\widetilde y=L/D$，故

$$
\frac{k_h}{L}=\frac{r_h}{D}\int_0^1\frac{d\theta}
{1-(H/2)^2[\theta\widetilde x-(1-\theta)\widetilde y]^2}.
$$

在积分的几何级数中保留常数与二次项，余项由 $q_b^2<1$ 包围；移位逆谱的分母均由 $1-\rho$ 控制。上式避免了人为的 $1/|\Gamma-1|$ 放大。各项估计与完整证明见附带的[有限步长推导](../../Workspaces/dlw_theory_parameter_limits_20261001/finite_h_review.md)。

原结构的精确归一化相位缺陷有严格正项级数，随 $|A|$ 增大，因此其区间最大值恰在 $|A|=M$ 取到。若 $q_0=h_0c_\Gamma M/2<1$，有

$$
h^2E_0\le E_h(0,0)\le h^2E_0+h^4B_0,\qquad B_0=\frac{T_\Gamma M^4}{1-q_0^2}.
$$

于是，用包含最优点的参数盒求 $B_*$，若 $E_*+h^2B_*\le E_0/10$，即可认证固定最优常数的十倍相位改善。反之，若 $E_*-h^2B>(E_0+h^2B_0)/10$，即可排除整个参数盒内的十倍改善。

下表的两项均由完整连续区间的余项不等式及精确有理算术认证，使用 $\Gamma=2$、$|\alpha|\le1$、$|\beta|\le2$、统一 $h_0=1/50$。常数在整段谱域和全部所列步长共用。

| 谱区间 | 首项最优／原结构 | 有限步长结论 |
|---|---:|---|
| $[1,2]$ | $1/32$ | $0<h\le1/50$：固定 $\alpha_*=-7/36,\ \beta_*=119/864$ 至少十倍相位改善 |
| $[1,10]$ | $81/800>1/10$ | $0<h\le1/500$：参数盒内任何两常数均不能十倍相位改善 |

对应 $B$ 分别为 $10.46354$ 与 $401.28332$ 以下的精确值，认证不等式的严格余量分别为 $0.01363866$ 与 $0.00647749$ 以上的精确值。这些是相位认证，尚不是物理演化收益。

## 4　物理重构：静态见证与初态纠正

单孤子的原结构使用 $G_j=1+E_j$、$F_j=1+\gamma(s_-)E_j$，其中 $E_j=\exp(Kx+\Omega t+\varphi)\chi_h^j$、$\Omega=q^2-p^2$。共同物理格距下的重构为 [1,2]

$$
u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.
$$

**定理3：相位缺陷有精确的静态物理见证。** 在全横向实线，正单孤子衰减使积分存在。对上述对数导数直接取 $x\to\pm\infty$ 的端值，得到

$$
\int_{\mathbb R}u_j\,dx=2\log\gamma(s_-)-\log\chi_h,\qquad
\int_{\mathbb R}v_j\,dx=4k_h.
$$

第一项与 $j$ 无关，故 $\int\delta_0u_j\,dx=0$。连续单孤子满足 $\int v_0\,dx=4L$，因而

$$
\frac{\int(v_h-v_0)\,dx}{4L}=\frac{k_h-L}{L},\qquad
\frac{\|v_h-v_0\|_{L^1_x}}{4|L|}\ge\left|\frac{k_h-L}{L}\right|.
$$

它将相位限制传递到同谱精确解族的静态物理量。基线的完整 $L^1$ 误差还包含其他重构项，因此相位的改善比值仍不能当作完整 $L^1$ 误差改善比值。

静态 $u$ 也有见证。自然解析插值置于 $y\in[-Y,Y]$，令 $z=Kx+Ly+\Omega t+\varphi$、$u_z=\partial_z u_0$。其二阶偏移有形式 $B_u=yLq_{\alpha,\beta}u_z+S_{\alpha,A}(z)$。在 $y=\pm Y$ 选择相同连续相位 $z$，两切片相减完全消去 $S$，因此

$$
\|B_u\|_{L^\infty(\mathbb R_x\times[-Y,Y])}\ge
Y|Lq_{\alpha,\beta}|\,\|u_z\|_\infty.
$$

由于 $KL=-(\Gamma-1)^2/\Gamma$，固定 $\Gamma$ 下 $|L|\|u_z\|_\infty$ 与 $A$ 无关且严格为正，故存在整个谱族的静态 $u$ 下界。该结论使用连续 $y$ 插值；只评价有限格层时须使用实际层跨度。

**定理4：共同物理初值完全消去质量见证。** 连续 $v$ 方程及整个两参数半离散 $v$ 方程均为 $v_t+\partial_x(\cdots)=0$。在零远场、足够衰减且解存在的条件下，每个 $y$ 层的横向 $v$ 质量守恒。若初始化时 $v_h=v_0$，则

$$
\int_{\mathbb R}[v_h(x,y,t)-v_0(x,y,t)]\,dx=0
$$

对全部存在时间成立。静态相位质量下界因此属于初态族偏差，被共同初值纠正精确抵消。它并不排除其他物理误差，却明确阻断了把该见证直接升级为演化误差下界的论证。

## 5　共同初值下的另一条短时限制

直接从物理方程出发，不继承静态质量见证。共同初值且可作受控误差展开时，写 $e_{u,v}=h^2a_{u,v}+O(h^4)$、$a(0)=0$。已有残差源为 [3]

$$
\tau^{\alpha,\beta}=\tau^{SD}+
\alpha(2u_{xy},2v_x)^{\mathsf T}+\beta(0,-4u_x)^{\mathsf T}.
$$

在 $y_0=-\infty$ 的零基值下，$\partial_ta_u(0)=-\int_{-\infty}^y\tau_1\,d\eta$。令 $s(z)=(1+e^{-z})^{-1}$、$f(z)=s(z+\log\Gamma)$、$d(z)=f(z)-s(z)$，写 $\kappa_\Gamma=(\Gamma^2-1)/\Gamma$、$\lambda_\Gamma=(1-\Gamma)/(1+\Gamma)$、$\zeta=KL=-(\Gamma-1)^2/\Gamma$。由于 $K=\kappa_\Gamma/A$、$L=\lambda_\Gamma A$，显式原函数给出

$$
b_u(A,z):=\partial_ta_u(0)=\frac{F_\Gamma(z)}A+
\frac{\alpha G_\Gamma(z)}{A^2},\qquad \beta\ \text{不进入此首项},
$$

$$
\begin{aligned}
F_\Gamma&=-\frac1{\lambda_\Gamma}\left\{
\zeta^3\left[\frac{2s^{(4)}-f^{(4)}}3+\frac{((s')^2)'}2\right]-\zeta^2s''\right\},\\
G_\Gamma&=-4\kappa_\Gamma^2d'.
\end{aligned}
$$

固定 $\Gamma\ne1$ 保证 $F_\Gamma$ 非零：$f^{(4)}$ 在 $z=-\log\Gamma+(2n+1)i\pi$ 有五阶极点，而其余仅含 $s$ 的项在该点解析；该极点系数非零。若 $F$ 在实轴恒零，其亚纯延拓也将恒零，与此矛盾。$G_\Gamma$ 在该点至多有二阶极点，故即使只校准一个谱尺度，也不能完整消去领先 $u$ 初始速度剖面；此结论自身不提供十倍的量化比例。

**定理5：初始误差速度不能任意迁移。** 冻结指标 $V(\alpha,\beta)=\sup_{A\in I}\|b_u(A,\cdot)\|_\infty$，对每个谱的全物理平面取最大值。设 $A_1,A_2$ 为区间端点，则

$$
A_2^2b_u(A_2,z)-A_1^2b_u(A_1,z)=(A_2-A_1)F_\Gamma(z).
$$

端点相消已消去全部可调项。取范数及三角不等式，而原结构 $V_0=\|F_\Gamma\|_\infty/m_0$，得到对任何两常数都成立的下界

$$
\frac{V(\alpha,\beta)}{V_0}\ge
\frac{m_0(M-m_0)}{M^2+m_0^2}
=\frac{\mathcal R-1}{\mathcal R^2+1}.
$$

因此，当 $5-\sqrt{14}<\mathcal R<5+\sqrt{14}$，即约 $1.25834<\mathcal R<8.74166$ 时，十倍初始速度改善不可能。尺度比 $2$ 给出 $V/V_0\ge1/5$：即使相位允许改善三十二倍，共同初值的领先 $u$ 误差初始速度也至多改善五倍。这是两个不同的冻结指标；首项相位校准不能作为物理收益的代理。

这个定理严格限制领先误差系数的初始导数。若在指定状态空间中另有统一展开 $e_u=h^2[tb_u+O(t^2)+O(h^2t)]$，严格余量可将限制推广到充分小的正 $t,h$。目前尚未包围这条统一演化余项，故不声称已获得指定终点的 $u$ 或双场误差下界。有限边界还会引入基值、边界通量及对应源项，不能套用全空间公式。

## 6　成立范围、查重与剩余问题

| 声明 | 当前结论 |
|---|---|
| 整段归一化相位十倍改善 | 已证明范围门槛、可行性及有限 $h$ 认证；窄范围有明确可实现例，宽范围有明确排除例 |
| 同谱精确孤子族的物理偏差 | 已证明 $v$ 质量／$L^1$ 见证与自然插值静态 $u$ 下界 |
| 共同物理初值下的误差初始速度 | 已证明一个直接的谱范围下界；尺度比 $2$ 排除十倍领先 $u$ 初始速度改善 |
| 指定正时间的双场十倍改善 | 未证明可能，也未证明普遍不可能；须控制演化、边界与全部余项 |

物理首项的正确对象是受迫响应 $a=a_0+\alpha a_\alpha+\beta a_\beta$。若从静态精确族偏移 $B$ 出发，则共同初值要求减去初态传播，得到 $a(t)=B(t)-\Phi(t,0)B(0)$；有边界源时还要加入相应响应。要判定指定时间的十倍物理改善，需在预先声明的状态空间内包围该响应与高阶余项，或构造在两可调响应上为零、对剩余源具有统一下界的物理见证。一般传播上界不足以提供这样的下界。

项目已有两参数 Gram 族、相位二阶展开、物理源方向、共同初值响应和二次最佳一致逼近的代数种子。本次新增的是完整正则条件、有限 $h$ 余项与区间证书、十倍谱范围门槛、有限 $h$ 整段匹配障碍、物理质量见证的守恒取消，以及初始误差速度的谱尺度限制。已核查项目来源及原文定义；未完成外部文献原创性审查，不把经典最佳逼近论证当作原创方法。

预测与指标先保存在 [THEORY_FREEZE.json](../../Workspaces/dlw_theory_parameter_limits_20261001/THEORY_FREEZE.json)，有限 $h$ 证书的参数盒先保存在 [CERTIFICATE_CONTRACT.json](../../Workspaces/dlw_theory_parameter_limits_20261001/CERTIFICATE_CONTRACT.json)。随后完成十四项精确代数核对、两项精确有理区间认证，以及两个冻结谱域在两种步长的端点／中点定向公式核对。三点核对只检查展开，不认证区间最大值；区间结论来自证明和余项界。本轮没有 PDE 演化或参数扫描。

参考来源：

1. [两壁 Gram 参数族与共同物理格距的闭合](../../Workspaces/dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md)，§2、5。
2. [对称物理重构与非线性闭合](../../Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md)，§1、2。
3. [误差映射、单孤子残差及共同初值参数响应](../../Workspaces/dlw_factor_model_20260930/REPORT.md)，§4、6、10。
4. [二阶系数界与初始误差速度](../../Workspaces/dlw_h2_bounds_20260930/REPORT.md)，§4。
5. [理论研究问题登记](../../Workspaces/dlw_research_pipeline_20261001/ideas.json)，修订3，T01。
6. [详细证明与独立物理审查](../../Workspaces/dlw_theory_parameter_limits_20261001/physical_bridge_review.md)；[定向核对与区间证书](../../Workspaces/dlw_theory_parameter_limits_20261001/theory_validation.json)。
