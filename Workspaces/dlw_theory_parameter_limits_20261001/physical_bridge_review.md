# T01：相位障碍的物理见证与共同初值纠正

2026-10-01。独立理论审查；未运行 PDE 演化、扫描或重调参数。本文的“新增”仅指相对项目既有材料的新证明，不主张外部文献原创性。

## 1. 来源、固定对象与谱尺度

核对来源：`dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md` §2、5；`dlw_semidiscrete/NONLINEAR_CLOSURE.md` §1–5；`dlw_factor_model_20260930/REPORT.md` §4、6、10；`dlw_h2_bounds_20260930/REPORT.md` §1、4。已有材料给出精确重构、二阶方程残差、共同初值的受迫线性化和初始增长率；以下质量见证、跨切片下界和尺度区间初始速度障碍尚未见于这些来源。有限维投影或已有数字不是本证明的输入。

固定物理 \(a,h\)、精确 \(x,t\)、正则单孤子，\(K=p+q>0\)，

\[
P=p-a,\quad Q=q+a,\quad \Gamma=-P/Q>0,\quad \Gamma\ne1,
\quad A=P^{-1}-Q^{-1},\quad L=P^{-1}+Q^{-1}.
\]

令 \(g=\log\Gamma\)、\(s(z)=(1+e^{-z})^{-1}\)、\(f(z)=s(z+g)\)、\(d=f-s\)。连续场为

\[
z=Kx+Ly+\Omega t+\varphi,\qquad
u=2K d(z),\qquad v=2KL(f'+s'),\qquad \Omega=q^2-p^2.
\]

固定 \(\Gamma\) 时

\[
K=\frac{\kappa_\Gamma}{A},\quad L=\lambda_\Gamma A,
\quad \kappa_\Gamma=\frac{\Gamma^2-1}{\Gamma},\quad
\lambda_\Gamma=\frac{1-\Gamma}{1+\Gamma},\quad
\zeta=KL=-\frac{(\Gamma-1)^2}{\Gamma}<0.                 \tag{1}
\]

因 \(K>0\)，\(A\) 与 \(\Gamma-1\) 同号；\(L<0\)。取同一半轴上的闭区间 \(I\)，\(0<a_{\min}:=\min_I|A|\le a_{\max}:=\max_I|A|<\infty\)。所有结论要求有限 \(h\) 的谱因子非零且实正、远离极点。两个常数 \(\alpha,\beta\) 整段共用。

## 2. 精确单孤子的中点物理重构

设 \(s_\pm=a+\alpha h^2\pm(h+\beta h^3)/2\)，

\[
\gamma_\pm=-\frac{p-s_\pm}{q+s_\pm}>0,
\qquad \chi=\gamma_-/\gamma_+>0,\qquad k_h=\frac{\log\chi}{h},
\]

并定义

\[
c_h=\tfrac12\log(\gamma_-\gamma_+),\qquad
b_h=c_h-g,\qquad d_h=\tfrac12hk_h,
\qquad z_h=Kx+k_h y+\Omega t+\varphi.
\]

自然解析插值在 \(y=(j+1/2)h\) 与 Gram 格点场严格一致：

\[
u_h(x,y,t)=K[2s(z_h+c_h)-s(z_h-d_h)-s(z_h+d_h)],               \tag{2}
\]
\[
W_h=\frac{4K}{h}[s(z_h+d_h)-s(z_h-d_h)],\qquad
v_h=W_h+\frac{u_h(y+h)-u_h(y-h)}{2h}.                       \tag{3}
\]

这里 \(c_h\) 是 F 与 G 的对称相对相位；不要混淆 \(c_h\) 与仅表示二阶偏移的 \(b_h\)。直接展开给出

\[
k_h=L+h^2Le(A)+O(h^4),\quad
b_h=-h^2L(\alpha+A/8)+O(h^4),\quad
e(A)=\beta+\alpha A+C_\Gamma A^2,                         \tag{4}
\]

\(C_\Gamma=(\Gamma^2+\Gamma+1)/[12(\Gamma+1)^2]\)。式 \(2\) 同时含纵向相位、F/G 的相对相位和物理差分重构，故单独的 \(k_h-L\) 不是全部物理误差。

## 3. 新证明：静态 \(v\) 质量精确读出相位，但共同初值使该见证恒为零

恒等式

\[
\int_{\mathbb R}[s(z+a)-s(z+b)]\,dz=a-b
\]

由对 \(a,b\) 求导及同参数时取零直接证明。利用 \(K>0\)、\(dx=dz_h/K\)，\(2\)–\(3\) 给出

\[
\int u_h\,dx=2c_h,\qquad
\int W_h\,dx=4k_h,\qquad
\int\delta_0u_h\,dx=0,\qquad
\boxed{\int v_h\,dx=4k_h}.                                \tag{5}
\]

连续场的对应质量为 \(\int u\,dx=2g\)、\(\int v\,dx=4L\)。因此对同谱**精确孤子族的静态比较**，预先定义的物理有符号质量指标严格满足

\[
\frac{\int(v_h-v)\,dx}{4L}=\frac{k_h-L}{L}=:D_h(A),\qquad
\frac{\|v_h-v\|_{L^1_x}}{4|L|}\ge |D_h(A)|.              \tag{6}
\]

所以相位障碍能够提升为这个静态质量指标的精确定量限制，也能给归一化静态 \(v\) 的 \(L^1\) 下界；它还没有成为静态 \(v\) 最大范数的相同比例下界。任何十倍比较须用相同物理指标的原参数基线，不能拿相位基线作任意 \(u/v\) 范数的分母。

**共同初值的反例桥梁。** 有限 \(h\) 第二物理方程的右侧全部是 \(\partial_x\) 或 \(\partial_x^2\) 通量。若每层的场和通量在 \(x\to\pm\infty\) 衰减足以积分，且解存在，则

\[
\frac d{dt}\int v_h\,dx=0,
\qquad \frac d{dt}\int v\,dx=0.
\]

共同物理初值意味着 \(\int(v_h-v)(0)dx=0\)，于是这个有符号质量误差在所有存在时刻都等于零。式 \(6\) 的静态相位质量见证经初值纠正**完全取消**。这不是“可能有抵消”的模糊警告，而是精确守恒反例；不能据 \(6\) 宣称共同初值动态 \(L^1\) 误差的下界。一般动态 \(L^1\) 误差仍可非零，质量只是不再提供下界。

## 4. 新证明：自然插值的静态 \(u\) 跨 \(y\) 切片的最大范数障碍

固定 \(Y>0\)，评价域为 \(x\in\mathbb R,y\in[-Y,Y]\)，精确场采用 \(2\) 的自然解析插值。令 \(U(z)=2Kd(z)\)。对每个连续相位 \(z\)，以

\[
x_y(z)=\frac{z-Ly-\Omega t-\varphi}{K}
\]

表示同一相位切片；这只是对全线最大范数的解析换元，未改变物理采样指标。由 \(2\)–\(4\)

\[
u_h(x_y(z),y,t)-u(x_y(z),y,t)=h^2B_u(z,y)+\mathcal R_u,
\]

\[
B_u(z,y)=yLe(A)U'(z)+S_u(z),\quad
S_u=-2KL(\alpha+A/8)f'-\frac{KL^2}{4}s''.                \tag{7}
\]

两端切片之差严格消去全部与 \(y\) 无关的重构形变：

\[
B_u(z,Y)-B_u(z,-Y)=2YLe(A)U'(z).
\]

由三角不等式

\[
\boxed{\|B_u\|_{L^\infty(\mathbb R\times[-Y,Y])}
\ge Y|Le(A)|\|U'\|_\infty
=Ym_\Gamma|e(A)|},\qquad
m_\Gamma=\frac{2(\Gamma-1)^2}{\Gamma}\|d'\|_\infty>0.    \tag{8}
\]

若在整个 \(I\)、某个固定可行系数紧集及 \(0<h\le h_0\) 上已有 \(\|\mathcal R_u\|_\infty\le M_uh^4\)，则

\[
\sup_{A\in I}\|u_h-u\|_\infty
\ge h^2Ym_\Gamma\frac{C_\Gamma(a_{\max}-a_{\min})^2}{8}
-M_uh^4.                                                \tag{9}
\]

这里用的是相位 minimax 下界；受限可行集仍成立，未声称其最优点一定可行。

**余项条件的精确说明。** 固定 \(\Gamma\ne1\)、紧谱区间、\(|y|\le Y\)、有界 \(\alpha,\beta\) 与统一极点/零点距离，\(2\) 可在 \(|h|\le h_0\) 延拓为偶的 \(C^4\) 函数。\(c_h,k_h\) 为偶函数，\(d_h\) 为奇函数；分母距零的紧性及 sigmoid 全阶导数有界使第四 \(h\) 导数在全实 \(z\) 上一致受控。因此可以取

\[
M_u=\frac1{24}\sup_{|\eta|\le h_0,A\in I,(\alpha,\beta)\in\mathcal F,
\,z\in\mathbb R,|y|\le Y}|\partial_\eta^4u_\eta(x_y(z),y,t)|<\infty. \tag{10}
\]

这给出严谨但未数值计算的余项常数定义；可以从谱因子的对数导数界和 sigmoid 导数界直接上估。无限 \(y\) 域上该展开不一致：非零 \(k_h-L\) 与任意大 \(y\) 相乘，不能把式 \(9\) 的 \(Y\) 任意送到无穷而保留同一 \(M_u\)。若只评价离散 \(y\) 层，须选实际两层，其间距替代 \(2Y\)；仅一个 \(y\) 层不能使用这个见证。

式 \(9\) 是静态同谱精确族的物理 \(u\) 下界，尚不比较其与原参数 \(u\) 基线的比例。原参数领先上界可写成

\[
\sup_A\|B_u^{0,0}\|_\infty\le
Ym_\Gamma C_\Gamma a_{\max}^2+S_\Gamma a_{\max},
\]

\[
S_\Gamma=\frac{|\zeta|}{4}
\|f'+\lambda_\Gamma s''\|_\infty.
\]

只有把 \(9\) 同这个物理基线上界、两侧余项放在一起，才得到静态物理十倍不可能性的充分条件。相位比值本身不能替代这一步。

## 5. 可选的精确 \(u\) 质心见证

当 \(c_h\ne0\) 时，质量非零且全线一阶矩存在。sigmoid 的反射对称性给出

\[
\int z[s(z+a)-s(z+b)]dz=-\tfrac12(a^2-b^2).
\]

故 \(u_h\) 的有符号质心为

\[
\bar x_h(y,t)=\frac{-c_h/2+d_h^2/(2c_h)-k_h y-\Omega t-\varphi}{K}.
\]

于是 \(\partial_y\bar x_h=-k_h/K\)，连续质心斜率为 \(-L/K\)。对两条不同层，预先冻结的归一化质心倾斜误差严格等于 \(D_h\)。\(\Gamma\ne1\) 与足够小 \(h\) 保证 \(c_h\) 远离零。它是物理矩指标，不是通常 \(u\) 最大范数；初值纠正后的解通常不再具有 \(2\) 的形状，因此不能直接沿用这条斜率公式。

## 6. 新证明：共同初值领先 \(u\) 初始速度的尺度区间障碍

下面研究另一个预先声明的物理指标。采用全 \(x\) 线和 \(y_0=-\infty\) 的零基值；由于 \(L<0\)，此端对应 \(z\to+\infty\)，所有剖面导数衰减。对于领先受迫误差系统，令

\[
b_u^{\alpha,\beta}(A,z)=\partial_t a_u^{\alpha,\beta}(A,z,0),\qquad
a_u(0)=a_v(0)=0.
\]

这个量由首项方程定义；将其认定为实际轨道的 \(h^{-2}\partial_te_u(0)\) 极限，需要存在且可对时间求导的共同初值误差展开。以下代数结论自身不假定有限正时间收敛。

既有来源给出

\[
H_\Gamma(z)=\zeta^3\left[\frac{2s^{(4)}-f^{(4)}}3+\frac12((s')^2)'\right]-\zeta^2s'',
\qquad R_1=H_\Gamma'(z),\qquad \partial_y(H_\Gamma/L)=R_1,
\]

且可调首项源为 \(\Psi_{\alpha,1}=2u_{xy}\)、\(\Psi_{\beta,1}=0\)。因此

\[
b_u^{\alpha,\beta}=-H_\Gamma/L-2\alpha u_x
=\frac{F_\Gamma(z)}{A}+\frac{\alpha G_\Gamma(z)}{A^2},    \tag{11}
\]

\[
F_\Gamma=-H_\Gamma/\lambda_\Gamma,\qquad
G_\Gamma=-4\kappa_\Gamma^2d'.
\]

式 \(11\) 的关键是 \(\beta\) 在 \(u\) 初始速度中完全缺席，\(\alpha\) 与原缺陷的尺度次数不同。定义冻结指标

\[
B(\alpha,\beta)=\sup_{A\in I}\|b_u^{\alpha,\beta}(A,\cdot)\|_{L^\infty_x},
\qquad B_0=B(0,0)=\|F_\Gamma\|_\infty/a_{\min}.
\]

全 \(x\) 范数可等价换为全 \(z\) 范数。两端 \(A_-,A_+\) 位于同一半轴，故 \(|A_+-A_-|=a_{\max}-a_{\min}\)。从 \(11\) 相减可消去 \(\alpha G_\Gamma\)：

\[
A_+^2b_u(A_+,z)-A_-^2b_u(A_-,z)=(A_+-A_-)F_\Gamma(z).
\]

因此对于所有 \(\alpha,\beta\)，不需要假设最优点可行，

\[
\boxed{B(\alpha,\beta)\ge
\frac{a_{\max}-a_{\min}}{a_{\max}^2+a_{\min}^2}\|F_\Gamma\|_\infty,\qquad
\frac{B(\alpha,\beta)}{B_0}\ge\frac{r(1-r)}{1+r^2}},\quad
r=a_{\min}/a_{\max}.                                   \tag{12}
\]

这是真正的共同初值领先物理 \(u\) 初始速度下界，不是将相位下界更名。十倍改善不可能的充分范围为

\[
\frac{5-\sqrt{14}}{11}<r<\frac{5+\sqrt{14}}{11},
\quad\text{约 }0.1144<r<0.7947.                           \tag{13}
\]

等价地，以尺度跨度 \(R=a_{\max}/a_{\min}\) 表示，该充分范围为 \(5-\sqrt{14}<R<5+\sqrt{14}\)，约 \(1.2583<R<8.7417\)。例如冻结尺度跨度 \(a_{\max}/a_{\min}=2\)，式 \(12\) 给出 \(B/B_0\ge1/5\)：不可能改善十倍。相同跨度的无约束领先相位 minimax 比却为 \(1/32\)。这精确展示“相位允许数量级改善”仍不能推出“共同初值物理误差允许数量级改善”。常数界的约束只会增强 \(12\)；有限左端基值或有限 \(x\) 窗口则改变这个指标与函数关系，需要重新推导。

## 7. \(F_\Gamma\ne0\) 的完整复极点证明

设 \(z_*=-g+i\pi\)。因 \(g\in\mathbb R\setminus\{0\}\)，\(f(z)=s(z+g)\) 在 \(z_*\) 有简单极点，而 \(s(z)\) 在该点解析。写 \(w=z-z_*\)，则

\[
1+e^{-(z+g)}=1-e^{-w}=w+O(w^2),\qquad
f(z)=w^{-1}+O(1),\qquad f^{(4)}(z)=24w^{-5}+O(1).
\]

\(H_\Gamma\) 中其余各项均只由 \(s\) 与其导数组成，在 \(z_*\) 解析。因此

\[
H_\Gamma(z)=-8\zeta^3w^{-5}+\text{在 }z_*\text{ 解析的项},
\qquad
F_\Gamma(z)=\frac{8\zeta^3}{\lambda_\Gamma}w^{-5}+\text{解析项}. \tag{14}
\]

\(\Gamma\ne1\) 给出 \(\zeta\ne0\)、\(\lambda_\Gamma\ne0\)，五阶主部非零。若 \(F_\Gamma\) 在实线上恒零，由解析恒等定理，其在去除孤立极点的连通域中恒零，矛盾。因此 \(F_\Gamma\) 不恒为零；实线上各 sigmoid 导数有界且衰减，故

\[
0<\|F_\Gamma\|_{L^\infty(\mathbb R)}<\infty.
\]

此外，\(G_\Gamma\) 在 \(z_*\) 至多有二阶极点，故任何常数倍 \(G_\Gamma\) 都不能消去 \(F_\Gamma\) 的五阶主部。即使仅固定一个尺度，也不能把完整 \(u\) 初始速度剖面精确消掉。有限维直线在 \(C_0(\mathbb R)\) 中闭，因而其到 \(F_\Gamma\) 的距离为正；这个陈述没有提供单尺度“至少 0.1”的量化比例。

## 8. 尚缺的有限时间桥梁

设相容边界与可控解空间中已有同谱静态展开 \(U_h^*(t)=U_0^*(t)+h^2B(t)+O(h^4)\)。共同初值误差首项为

\[
a(t)=B(t)-\Phi_0(t,0)B(0),                               \tag{15}
\]

其中 \(\Phi_0\) 是同一连续物理线性化的传播。若精确孤子族不满足实际边界，还须加边界源响应。\(15\) 与质量反例说明，只控制 \(B(t)\) 无法给出 \(a(t)\) 的正下界。

若进一步有冻结指标下的统一包围

\[
\|a_u^{\alpha,\beta}(T)-Tb_u^{\alpha,\beta}\|\le C_*T^2,
\qquad \|a_u^{0,0}(T)-Tb_u^{0,0}\|\le C_0T^2,
\]

则由 \(12\) 得

\[
\frac{\sup_A\|a_u^{\alpha,\beta}(T)\|}{\sup_A\|a_u^{0,0}(T)\|}
\ge\frac{T\,r(1-r)B_0/(1+r^2)-C_*T^2}{TB_0+C_0T^2}.     \tag{16}
\]

有认证的 \(h^4\) 实际解误差余项时还要在分子减去、分母加上相应余量。对 \(r=1/2\)，\(16\) 在满足 \(T(C_*+0.1C_0)<0.1B_0\) 且实际余项受控的短时间内排除十倍 \(u\) 演化误差改善。当前未认证这些 \(C_*,C_0\) 或网格一致传播，也未建立给定有限 \(T\) 的双场下界；DLW 已知高频增长不能忽略。

已证明的物理结论为静态质量/切片限制与共同初值领先初始速度尺度限制。有限正时间 \(u/v\) 演化误差、当前有限边界、一般初态及多孤子仍需各自桥梁。
