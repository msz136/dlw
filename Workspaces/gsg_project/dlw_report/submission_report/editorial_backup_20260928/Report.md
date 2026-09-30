# DLW 半离散系统的非线性化与 2HS 数值比较

## 1　DLW 半离散系统的非线性化

### 1.1　消去辅助势的两场形式

考虑交错格点上的双线性方程

$$B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0,\qquad B_s=D_x^2+D_t+2sD_x.\tag{1}$$

其中 $D$ 为 Hirota 双线性算子，$F_j$ 与 $G_j$ 分别位于 $y=(j+\tfrac12)h$ 和 $y=jh$，$h\ne0$。在 $F_j,G_j$ 非零的区域内，令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。利用恒等式

$$\frac{B_sf\cdot g}{fg}=(\log f+\log g)_{xx}+(\log f-\log g)_x^2
+(\log f-\log g)_t+2s(\log f-\log g)_x,\tag{2}$$

将式（1）除以相应的 $\tau$ 函数乘积，得到

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{3}$$

取两侧对数差导数的和与差

$$u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,\qquad
\omega_j=(\beta_{j+1}-\beta_j)_x.\tag{4}$$

于是两侧对数差的导数分别为 $(u_j+\omega_j)/2$ 和 $(u_j-\omega_j)/2$。将式（3）相加、相减并对 $x$ 求导，记

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{5}$$

可得

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{6}$$

定义 $\delta_-f_j=(f_j-f_{j-1})/h$、$M_-f_j=(f_j+f_{j-1})/2$。由式（4）有 $\delta_-Z_j=\delta_-u_j+(4/h)M_-\omega_j$，从而消去 $Z_j$，得到闭合的非线性半离散系统

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4hM_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{7}$$

为恢复连续 DLW 的物理变量，令 $v_j=(4/h)\omega_j+\delta_0u_j$，其中 $\delta_0f_j=(f_{j+1}-f_{j-1})/(2h)$。写 $W_j=v_j-\delta_0u_j$、$\Delta_hf_j=(f_{j+1}-2f_j+f_{j-1})/h^2$，式（7）等价地表示为

$$\begin{aligned}
0={}&\delta_-u_{j,t}
+\partial_x\delta_-\!\left[\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right]\\
&+\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_h\delta_-u_j\right),\\
0={}&v_{j,t}+\partial_x\!\left[\delta_0\!\left(\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right)
+(u_j+2a)W_j-4u_j\right]\\
&+\partial_x^2\left[\delta_0u_j+\frac{h^2}{4}\Delta_hW_j\right],
\end{aligned}\tag{8}$$

上述消元在有限 $h$ 下成立；在光滑连续极限中，式（8）趋于

$$u_{yt}+v_{xx}+[(u+2a)u_y]_x=0,\qquad
v_t+u_{xxy}+[(u+2a)v-4u]_x=0.\tag{9}$$

### 1.2　保留势的比值形式

另一条路线从式（6）出发，保留辅助势，不再对第一条作格点差分。以下始终使用式（4）的 $u_j,\omega_j$，物理场仍为 $v_j=4\omega_j/h+\delta_0u_j$。

首先令 $M_j=\beta_{j,x}$。由式（4）、（5）直接得到

$$\omega_j=M_{j+1}-M_j,\qquad
Z_j=u_j+2(M_j+M_{j+1}).\tag{9a}$$

代回式（6），当前方程为

$$\begin{aligned}
0={}&u_{j,t}+\partial_x\!\left[
u_{j,x}+\frac{u_j^2}{2}+2au_j
+2(M_j+M_{j+1})_x+\frac{\omega_j^2}{2}-h\omega_j\right],\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x[(u_j+2a)\omega_j-hu_j],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{9b}$$

这一步只将 $Z_j$ 写成 $u_j$ 与 $M_j$ 的组合。相应的物理场为 $u_j$ 和 $v_j=4(M_{j+1}-M_j)/h+\delta_0u_j$。

第一条中的 $u_{j,x}+u_j^2/2$ 可以由对数导数合并。固定对数分支，取中心比值

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{9c}$$

这里 $Q_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。式（9c）保持原来的 $u_j$，并给出

$$u_{j,t}=2\partial_x\!\left(\frac{Q_{j,t}}{Q_j}\right),\qquad
u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{9d}$$

因此，式（9b）的第一条成为

$$\partial_x\!\left[
\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}
+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j
\right]=0.\tag{9e}$$

仅由式（9e）积分，括号等于一个 $c_j(t)$；采用式（9c）的 tau 比值时，括号恰为 $(A_j+C_j)/2$，故由原双线性方程可知它为零。于是得到

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{\omega_j^2}{4}-\frac h2\omega_j\right]Q_j,\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x\!\left[2a\omega_j
+2\frac{Q_{j,x}}{Q_j}(\omega_j-h)\right],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{9f}$$

此时的未知量为 $Q_j,\omega_j,M_j$；物理场由 $u_j=2Q_{j,x}/Q_j$、$v_j=4\omega_j/h+\delta_0u_j$ 恢复。第一条的导数平方项已经合并，第二条仍含分母 $Q_j$。

### 1.3　势差的乘积分解

式（9f）的分式乘着 $\omega_j-h$，因此取

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad
\omega_j=h(1-Q_jR_j),\qquad
\frac{M_{j+1}-M_j}{h}+Q_jR_j=1.\tag{9g}$$

这一变换只需 $Q_j\ne0$，不要求 $R_j$ 非零。它使 $(Q_{j,x}/Q_j)(\omega_j-h)=-hQ_{j,x}R_j$，同时有

$$\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{9h}$$

代入式（9f），第二条中的常数通量 $2ah$ 求导后消失。当前两条演化式为

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
0={}&(Q_jR_j)_t-(Q_jR_j)_{xx}
+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x.
\end{aligned}\tag{9i}$$

势约束仍为式（9g）。第二条展开后，混合导数项抵消：

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx}.
\tag{9j}$$

故乘积方程可写成

$$R_j(Q_{j,t}+Q_{j,xx}+2aQ_{j,x})
+Q_j(R_{j,t}-R_{j,xx}+2aR_{j,x})=0.\tag{9k}$$

利用式（9i）的第一条并除以 $Q_j$，得到最终的耦合系统

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{9l}$$

两条演化式的二阶导数项和势项分别反号，来自式（9j）的乘积恒等式。原来的变量及物理场为

$$\boxed{\begin{aligned}
u_j&=2\frac{Q_{j,x}}{Q_j},\qquad
\omega_j=h(1-Q_jR_j)=M_{j+1}-M_j,\\
v_j&=4(1-Q_jR_j)+\frac{u_{j+1}-u_{j-1}}{2h}.
\end{aligned}}\tag{9m}$$

## 2　2HS 原文单孤子参数下的数值比较

### 2.1　原文单孤子参数

考虑 $c=1$ 的 2HS 系统

$$u_{tx}-uu_{xx}-\frac12u_x^2-4u-\frac12(\rho^2-1)=0,\qquad \rho_t=(u\rho)_x.\tag{10}$$

取原文图 1、图 3 的单孤子参数 $p=5$、$q=1.25$、$\xi_0=\eta_0=0$，保留原文坐标平移。其连续解可写为

$$\theta=\frac{15}{4}X-\frac35t,\qquad
x=X-\frac12+\frac3{10}\tanh\frac\theta2,\qquad
u=\frac9{100}\operatorname{sech}^2\frac\theta2,\qquad
\rho=\frac{16}{25-9\tanh^2(\theta/2)}.\tag{11}$$

其中 $\rho$ 为第二个物理场，远场值为 $1$。采用以下三种空间方案，并统一使用经典四阶 Runge–Kutta 方法，取 $\Delta t=0.003125$，计算至 $t=0.5$。

可积半离散方案取原生步长 $a=0.005$、$N=1600$。令 $d_k=x_{k+1}-x_k$、$b_k=u_{k+1}-u_k$，推进

$$\dot d_k=-b_k,\qquad
\dot b_k=2d_k(u_{k+1}+u_k)+\frac{[d_k^2-a(a-1)]^2-b_k^2}{2d_k}-\frac{d_k}{2},\qquad
\rho_k=\frac a{d_k}.\tag{12}$$

由左端解析 $u$ 累加 $b_k$ 恢复速度场，节点按 $\dot x_k=-u_k$ 运动。固定网格直接差分和动网格直接差分共用变量 $m=u_{xx}+2$ 及以下空间方程：

$$\begin{aligned}
\dot m_i&=(u_i+V_i)(D_1m)_i+2(D_1u)_i m_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=(u_i+V_i)(D_1\rho)_i+\rho_i(D_1u)_i,\qquad D_2u=m-2,\qquad \dot x_i=V_i.
\end{aligned}\tag{13}$$

$D_1,D_2$ 为当前节点上的三点非均匀中心差分，每个时间级用两端解析值反演 $u$。固定网格取 $V_i=0$；动网格取与可积方案相同的初始节点，取 $V_i=-u_i$。直接差分将 $\rho_i$ 作为节点场按式（13）演化，可积方案则由胞元宽度计算 $\rho_k=a/d_k$。

三种方案均以式（11）的连续解为初始目标。可积方案的密度位于胞元，直接差分的密度位于节点；将两者线性重构到 $[-1,1]$ 上的 32001 个共同物理点，计算

$$E_u=\max_{x\in\mathcal G}|u_h(x,0.5)-u(x,0.5)|,\qquad
E_\rho=\max_{x\in\mathcal G}|\rho_h(x,0.5)-\rho(x,0.5)|.\tag{14}$$

<div class="caption">表 1　原文单孤子参数下三种方法在 x∈[−1,1] 上的物理场最大绝对误差。</div>

<!-- POINT_TABLE -->

<!-- POINT_COMPARISON -->

<!-- POINT_FIGURE -->

这里比较的是相对连续解的总误差，包含空间离散、时间推进与重构误差。原文图 3 展示的是半离散精确孤子；表 1 则是采用原文参数、从连续初态推进得到的数值比较。可积方案与直接差分的边界闭合不同，因此上述差异反映完整方案在这一参数点的表现。

### 2.2　原文二孤子参数

原文图 4 的参数为 $p_1=1.1$、$p_2=1.25$、$q_1=11$、$q_2=5$、$c=1$、$a=0.005$。保留原文的相位与物理坐标规范；将精确解写为实正形式时，令

$$\begin{aligned}
f&=1+e^{\theta_1}+e^{\theta_2}+A_{12}e^{\theta_1+\theta_2},\qquad
A_{12}=\frac{12}{507},\\
\theta_i&=(p_i-q_i)X+\left(\frac1{p_i}-\frac1{q_i}\right)t+\log6.5,
\end{aligned}\tag{15}$$

于是连续二孤子的物理场和坐标为

$$u=\partial_t^2\log f,\qquad
x=X-\partial_t\log f-\frac1{q_1}-\frac1{q_2},\qquad
\rho=\frac1{1-\partial_X\partial_t\log f}.\tag{16}$$

从该连续解在 $t=-3$ 的同一初值出发，沿用上节的三种空间方案，取 $N=1600$、$X\in[-4,4]$、RK4 与 $\Delta t=0.003125$，推进至 $t=3$。表 2 和图 2 统一在物理区间 $x\in[-1,1]$ 上与式（16）比较；每个时刻把双场线性重构到 32001 个共同位置，列出最大绝对误差。

<div class="caption">表 2　原文二孤子参数下三种方法在 x∈[−1,1] 上的最大绝对误差。</div>

<!-- TWO_SOLITON_TABLE -->

<!-- TWO_SOLITON_FIGURE -->

在 $t=-2.5$，原可积方案的 $u/\rho$ 误差为 $4.484\times10^{-2}/3.913\times10^{-3}$，明显高于两种直接差分。它在约 $t=-1.684$ 出现非正网格边而停止，故表中的空格表示未到达该时刻。直接差分的两条轨道都到达 $t=3$；在表中三个时刻，固定网格的双场误差均小于论文动网格。特别在 $t=3$，固定网格与动网格的 $\rho$ 误差分别为 $3.556\times10^{-5}$ 和 $6.010\times10^{-5}$。

原文图 4 给的是精确半离散二孤子在 $t=-50,-20,20,50$ 的剖面。本节给出的是在同一原文参数下、较短时间窗中从连续初值出发的数值推进；它不能代替原文长时间精确解图，也不提供原可积方案在停止后的误差。三种方案的边界闭合与密度存储位置不同，以上误差反映完整数值方案的表现。
