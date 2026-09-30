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

保留辅助势 $M_j=\beta_{j,x}$，由式（4）、（5）得

$$\omega_j=M_{j+1}-M_j,\qquad
Z_j=u_j+2(M_j+M_{j+1}).\tag{10}$$

代入式（6），得

$$\begin{aligned}
0={}&u_{j,t}+\partial_x\!\left[
u_{j,x}+\frac{u_j^2}{2}+2au_j
+2(M_j+M_{j+1})_x+\frac{\omega_j^2}{2}-h\omega_j\right],\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x[(u_j+2a)\omega_j-hu_j],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{11}$$

固定对数分支，定义中心比值

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{12}$$

其中 $Q_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。由此有

$$u_{j,t}=2\partial_x\!\left(\frac{Q_{j,t}}{Q_j}\right),\qquad
u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{13}$$

式（11）的第一条化为

$$\partial_x\!\left[
\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}
+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j
\right]=0.\tag{14}$$

由式（12），括号内为 $(A_j+C_j)/2=0$，故

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{\omega_j^2}{4}-\frac h2\omega_j\right]Q_j,\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x\!\left[2a\omega_j
+2\frac{Q_{j,x}}{Q_j}(\omega_j-h)\right],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{15}$$

### 1.3　势差的乘积分解

令

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad
\omega_j=h(1-Q_jR_j),\qquad
\frac{M_{j+1}-M_j}{h}+Q_jR_j=1.\tag{16}$$

在 $Q_j\ne0$ 时，$(Q_{j,x}/Q_j)(\omega_j-h)=-hQ_{j,x}R_j$，且

$$\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{17}$$

代入式（15），得

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
0={}&(Q_jR_j)_t-(Q_jR_j)_{xx}
+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x.
\end{aligned}\tag{18}$$

利用恒等式

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx}.
\tag{19}$$

第二条可写为

$$R_j(Q_{j,t}+Q_{j,xx}+2aQ_{j,x})
+Q_j(R_{j,t}-R_{j,xx}+2aR_{j,x})=0.\tag{20}$$

再由式（18）的第一条，得到

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{21}$$

物理场由下式恢复：

$$\boxed{\begin{aligned}
u_j&=2\frac{Q_{j,x}}{Q_j},\qquad
\omega_j=h(1-Q_jR_j)=M_{j+1}-M_j,\\
v_j&=4(1-Q_jR_j)+\frac{u_{j+1}-u_{j-1}}{2h}.
\end{aligned}}\tag{22}$$

## 2　2HS 单孤子与二孤子的数值比较

### 2.1　单孤子

考虑 $c=1$ 的 2HS 系统

$$u_{tx}-uu_{xx}-\frac12u_x^2-4u-\frac12(\rho^2-1)=0,\qquad \rho_t=(u\rho)_x.\tag{23}$$

取原文图 1、图 3 的参数 $p=5$、$q=1.25$、$\xi_0=\eta_0=0$，相应的连续单孤子解为

$$\theta=\frac{15}{4}X-\frac35t,\qquad
x=X-\frac12+\frac3{10}\tanh\frac\theta2,\qquad
u=\frac9{100}\operatorname{sech}^2\frac\theta2,\qquad
\rho=\frac{16}{25-9\tanh^2(\theta/2)}.\tag{24}$$

其中 $\rho$ 的远场值为 $1$。比较可积半离散格式（Integrable）与固定网格中心差分（FD）。取辅助节点 $X_k=-4+ka$，$a=0.005$、$k=0,\ldots,N$、$N=1600$；由式（24）给出初始物理节点与场值。FD 在相同的初始物理端点间均匀布点，物理步长记为 $\Delta x$。

**Integrable。** 令 $d_k=x_{k+1}-x_k$、$b_k=u_{k+1}-u_k$，采用原文式（100）的等价形式

$$\begin{aligned}
\dot d_k&=-b_k,\qquad \dot x_0=-u_0(t),\\
\dot b_k&=2d_k(u_{k+1}+u_k)
+\frac{[d_k^2-a(a-1)]^2-b_k^2}{2d_k}-\frac{d_k}{2}.
\end{aligned}\tag{25}$$

左端 $u_0(t)$ 取解析值；各节点及胞元密度由下式递推恢复：

$$u_{k+1}=u_k+b_k,\qquad x_{k+1}=x_k+d_k,\qquad
\rho_{k+1/2}=\frac{a}{d_k}.\tag{26}$$

**FD。** 对式（23）的第一式作 $x$ 微分，令 $m=u_{xx}+2$。在固定网格上定义

$$ (D_1f)_i=\frac{f_{i+1}-f_{i-1}}{2\Delta x},\qquad
(D_2f)_i=\frac{f_{i+1}-2f_i+f_{i-1}}{\Delta x^2},\tag{27}$$

并计算

$$\begin{aligned}
\dot m_i&=u_i(D_1m)_i+2m_i(D_1u)_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=u_i(D_1\rho)_i+\rho_i(D_1u)_i,\\
u_{i+1}-2u_i+u_{i-1}&=\Delta x^2(m_i-2).
\end{aligned}\tag{28}$$

初始取 $m_i^0=(D_2u^0)_i+2$、$\rho_i^0=\rho(x_i,0)$。两端 $u,\rho,m$ 取解析值，每个时间级由最后一式联立求出内部 $u_i$。

两种系统均用 RK4 更新。记上述演化方程为 $\dot z=\mathcal F(t,z)$，则

$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),&
K_2&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_1\right),\\
K_3&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_2\right),&
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta tK_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}\tag{29}$$

每一级均按式（26）或（28）恢复物理场。取 $\Delta t=0.003125$，从 $t=0$ 计算至 $t=0.5$。

在 $x\in[-1,1]$ 的 32001 个等距点组成的集合 $\mathcal G$ 上，经线性插值后计算相对连续解的最大绝对误差：

$$E_u(t)=\max_{x\in\mathcal G}|u_h(x,t)-u(x,t)|,\qquad
E_\rho(t)=\max_{x\in\mathcal G}|\rho_h(x,t)-\rho(x,t)|.\tag{30}$$

<div class="caption">表 1　单孤子在 t=0.5 时的最大绝对误差。</div>

<!-- POINT_TABLE -->

<!-- POINT_COMPARISON -->

<!-- POINT_FIGURE -->

<!-- ONE_WAVEFORM -->

### 2.2　二孤子

取原文图 4 的参数 $p_1=1.1$、$p_2=1.25$、$q_1=11$、$q_2=5$、$c=1$、$a=0.005$。按原文的相位与坐标平移，连续二孤子的 $\tau$ 函数可写为

$$\begin{aligned}
f&=1+e^{\theta_1}+e^{\theta_2}+A_{12}e^{\theta_1+\theta_2},\qquad
A_{12}=\frac{12}{507},\\
\theta_i&=(p_i-q_i)X+\left(\frac1{p_i}-\frac1{q_i}\right)t+\log6.5,
\end{aligned}\tag{31}$$

物理场与坐标为

$$u=\partial_t^2\log f,\qquad
x=X-\partial_t\log f-\frac1{q_1}-\frac1{q_2},\qquad
\rho=\frac1{1-\partial_X\partial_t\log f}.\tag{32}$$

取 $X_k=-4+ka$、$k=0,\ldots,N$、$N=1600$，由式（32）在 $t=0$ 的值确定初始节点 $x_k^0$ 与场值 $u_k^0$。二孤子采用相同的演化方程，初值和边界均由式（32）给出。

**Integrable。** 初始取 $d_k^0=x_{k+1}^0-x_k^0$、$b_k^0=u_{k+1}^0-u_k^0$，计算

$$\begin{aligned}
\dot d_k&=-b_k,\qquad \dot x_0=-u_0(t),\\
\dot b_k&=2d_k(u_{k+1}+u_k)
+\frac{[d_k^2-a(a-1)]^2-b_k^2}{2d_k}-\frac{d_k}{2},\\
u_{k+1}&=u_k+b_k,\qquad x_{k+1}=x_k+d_k,\qquad
\rho_{k+1/2}=\frac{a}{d_k}.
\end{aligned}\tag{33}$$

左端取 $u_0(t)=\partial_t^2\log f(-4,t)$。

**FD。** 在 $[x_0^0,x_N^0]$ 上均匀取点，令 $u_i^0=u(x_i,0)$、$\rho_i^0=\rho(x_i,0)$、$m_i^0=(D_2u^0)_i+2$，计算

$$\begin{aligned}
\dot m_i&=u_i(D_1m)_i+2m_i(D_1u)_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=u_i(D_1\rho)_i+\rho_i(D_1u)_i,\\
u_{i+1}-2u_i+u_{i-1}&=\Delta x^2(m_i-2).
\end{aligned}\tag{34}$$

其中 $D_1,D_2$ 同式（27）；两端取二孤子解析值 $u,\rho,m=u_{xx}+2$，每个时间级联立恢复内部 $u_i$。两种方案均按式（29）作 RK4 更新，取 $\Delta t=0.003125$，从 $t=0$ 计算至 $t=0.5$；误差仍在 $x\in[-1,1]$ 上按式（30）计算。

<div class="caption">表 2　二孤子在 t=0.5 时的最大绝对误差。</div>

<!-- TWO_SOLITON_TABLE -->

<!-- TWO_SOLITON_COMPARISON -->

<!-- TWO_SOLITON_FIGURE -->

<!-- TWO_WAVEFORM -->

