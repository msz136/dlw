## 9　数值方法与数值结果

本节基于 PE 和 PF 两种非线性形式构造数值格式，并与连续 DLW 方程的直接差分格式（FD）比较。以单孤子和二孤子解析解为参照，考察不同时间算法以及固定、动网格下的数值误差。

### 9.1　网格与迭代格式

将 $x\in[-L/2,L/2)$ 等分为 $N_x$ 个区间，取 $x_i=-L/2+i\Delta x$、$\Delta x=L/N_x$。沿 $y$ 方向采用前述交错网格：$M_j$ 位于 $y=jh$，物理场及 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$。令 $t_n=n\Delta t$，上标 $n$ 表示时间层，下标 $j,i$ 分别表示 $y$、$x$ 方向的网格编号。

对 $x$ 的一、二阶导数分别采用中心差分

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{R1}$$

$y$ 方向的 $\delta_-,\delta_0,M_-$ 仍表示第 5 节定义的差分与平均。以下先给出固定网格上的 Euler 更新；RK4 和 C–N 使用相同的空间差分，见第 9.3 节。

**PE 格式。** 取 $P=\delta_-u$、$W=v-\delta_0u$ 为演化变量。已知第 $n$ 层的 $P^n,W^n$，先由下侧边界恢复

$$u_{j,i}^n=u_{j_L,i}^n+h\sum_{k=j_L+1}^{j}P_{k,i}^n,\qquad
v_{j,i}^n=W_{j,i}^n+(\delta_0u^n)_{j,i}.\tag{R2}$$

其中 $j_L$ 为最下层编号，$u_{j_L,i}^n$ 取解析边界值。由 PE 方程计算 $P,W$ 的时间变化率

$$\begin{aligned}
F_P^n={}&-\delta_-D_1\left[\frac{(u^n)^2}{2}+2au^n
+h^2\left(\frac{(W^n)^2}{32}-\frac{W^n}{4}\right)\right]
-D_2(P^n+M_-W^n),\\
F_W^n={}&-D_1[(u^n+2a)W^n-4u^n]+D_2W^n.
\end{aligned}\tag{R3}$$

这里 $F_P^n,F_W^n$ 分别近似 $P_t,W_t$，所有乘积按节点计算。下一时间层为

$$P^{n+1}=P^n+\Delta t\,F_P^n,\qquad
W^{n+1}=W^n+\Delta t\,F_W^n.\tag{R4}$$

更新后再由（R2）恢复 $u^{n+1},v^{n+1}$。初值取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$。

**PF 格式。** 演化变量为 $Q,R$，物理场由

$$u_j^n=2\frac{D_1Q_j^n}{Q_j^n},\qquad
v_j^n=4(1-Q_j^nR_j^n)+\delta_0u_j^n\tag{R5}$$

恢复。为计算 PF 方程中的 $(M_j+M_{j+1})_x$，记 $m_j^n\simeq M_{j,x}(t_n)$、$S_j^n=Q_j^nR_j^n$。对约束 $M_{j+1}-M_j=h(1-QR)$ 作 $x$ 差分，得到

$$m_{j+1}^n=m_j^n-hD_1S_j^n.\tag{R6}$$

这一关系使 $m_j^n$ 可由下边界逐层求出。将最下层临时编号为 $0$，由该层的 $Q$ 方程确定起始值

$$m_0^n=-\frac{Q_{0,t}^n+D_2Q_0^n+2aD_1Q_0^n}{2Q_0^n}
-\frac{h^2}{8}\bigl[(S_0^n)^2-1\bigr]+\frac h2D_1S_0^n.\tag{R7}$$

其中 $Q_0(t)$ 由解析下边界确定，$Q_{0,t}^n$ 为其时间导数。由（R6）得到各层的 $m_j^n$ 后，计算

$$\begin{aligned}
F_{Q,j}^n={}&-D_2Q_j^n-2aD_1Q_j^n
-\left[m_j^n+m_{j+1}^n+\frac{h^2}{4}\bigl((Q_j^nR_j^n)^2-1\bigr)\right]Q_j^n,\\
F_{R,j}^n={}&D_2R_j^n-2aD_1R_j^n
+\left[m_j^n+m_{j+1}^n+\frac{h^2}{4}\bigl((Q_j^nR_j^n)^2-1\bigr)\right]R_j^n,\\
Q_j^{n+1}={}&Q_j^n+\Delta t\,F_{Q,j}^n,\qquad
R_j^{n+1}=R_j^n+\Delta t\,F_{R,j}^n.
\end{aligned}\tag{R8}$$

$F_Q,F_R$ 分别为 $Q,R$ 的时间变化率。$Q$ 的最下层取边界值，内部各层 $Q$ 和所有层 $R$ 按（R8）更新，再由（R5）计算物理场。

初始 $Q$ 由离散关系 $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ 及归一化 $Q_{j,0}^0=1$ 确定，再取 $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$。这样，PF 与其余格式具有相同的初始物理场。下边界的 $Q_0(t)$ 按同一关系由 $u_{*,0}(t)$ 确定。

**FD 格式。** 直接离散连续 DLW 系统，以 $P=\delta_-u$、$v$ 为演化变量。$u^n$ 仍由（R2）的第一式恢复，随后计算

$$\begin{aligned}
F_P^n&=-\delta_-D_1\left[\frac{(u^n)^2}{2}+2au^n\right]-D_2M_-v^n,\\
F_v^n&=-D_1[(u^n+2a)v^n-4u^n]-D_2\delta_0u^n,\\
P^{n+1}&=P^n+\Delta t\,F_P^n,\qquad
v^{n+1}=v^n+\Delta t\,F_v^n.
\end{aligned}\tag{R9}$$

此处 $F_P^n,F_v^n$ 分别近似 $P_t,v_t$；例如 $D_2\delta_0u$ 近似连续方程中的 $u_{xxy}$。初值为 $P^0=\delta_-u_*(0)$、$v^0=v_*(0)$。

计算域选在孤子尾部接近背景的位置。PE、FD 的 $x$ 向差分采用周期边界，PF 按 $Q,R$ 的左右端背景值处理边界。沿 $y$ 方向，下侧取解析边界，上侧对数值解与解析背景之差作二次外推。

### 9.2　自适应动网格

文献 [2] 通过离散 hodograph 变换将半离散方程与网格演化联系起来。对于本文的 DLW 系统，网格运动由 PE 方程中的守恒关系确定。令

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.
\tag{R10}$$

将 $W_j=4(1-\rho_j)$ 代入其演化方程，得到

$$\partial_t\rho_j+\partial_xq_j=0.\tag{R11}$$

在 PF 形式中，$\rho_j=Q_jR_j$。由于所有 $y$ 层共用一组 $x$ 节点，对各层取平均作为网格密度和通量：

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{R12}$$

初始网格按 $\bar\rho(x,0)$ 的累积积分等分，即令相邻节点之间的密度积分相同。密度较大的区域因此分配更多节点。令左端节点 $x_L$ 固定，并保持每个移动节点对应的累积积分不变，利用（R11）得

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.
\tag{R13}$$

因此节点速度为

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{R14}$$

计算时以 $D_1\rho$ 代替通量中的 $\partial_x\rho$，并要求 $\bar\rho>0$。FD 的动网格比较也采用（R10）、（R12）和（R14）确定节点速度。

在均匀计算坐标 $\xi_i=-L/2+i\Delta\xi$ 上写 $x_i(t)=\xi_i+s_i(t)$，令 $J_i=1+D_\xi s_i$。移动节点上的 $x$ 导数由链式法则计算：

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{R15}$$

$D_\xi,D_{\xi\xi}$ 为（R1）在均匀计算坐标上的三点差分。对随节点移动的任一演化变量 $z$，链式法则给出 $\dot z=F_z+\mathcal V D_1z$。因此，在第 9.1 节各时间变化率上加入 $\mathcal V D_1z$，并将节点方程（R14）与场变量同步推进。固定网格对应 $s=0,\mathcal V=0$。

### 9.3　时间推进

第 9.1 节的 Euler 格式以当前时间层的变化率更新场变量。为比较不同时间离散，进一步采用经典 RK4 和 Crank–Nicolson（C–N）格式。记全部演化变量为 $z$，其离散变化率为 $\mathcal F(t,z)$；在动网格计算中，$z$ 同时包含节点坐标，$\mathcal F$ 包含上述网格输运项及节点速度。

RK4 在一个时间步内计算四次变化率：

$$\begin{aligned}
k_1&=\mathcal F(t_n,z^n),\\
k_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_1/2),\\
k_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_2/2),\\
k_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t\,k_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4).
\end{aligned}\tag{R16}$$

每一级均根据该级的场变量和网格重新计算差分及边界值。

与文献 [2] 的时间平均处理相同，C–N 取相邻两个时间层变化率的平均：

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.
\tag{R17}$$

例如，FD 格式中的 $v$ 方程写为 $v^{n+1}=v^n+\Delta t(F_v^n+F_v^{n+1})/2$。由于 $F_v^{n+1}$ 依赖未知的下一层解，需与 $P$ 的更新联立求解。计算中以 Euler 结果作为初始近似，再迭代求解隐式方程，残差容差为 $10^{-12}+10^{-11}\max(1,\|z^n\|_\infty)$。

### 9.4　参数设置与误差比较

采用文献 [1] 的三组孤子参数，$a=2$、$\rho_i=1$、初相位为零。精确解由连续 Gram 行列式及变换（2）计算。

| 算例 | $p_i$ | $q_i$ | 对应解 |
|---|---|---|---|
| A | $1$ | $2$ | 单孤子，原文图 1(a) |
| B | $4$ | $-3$ | 单孤子，原文图 1(b) |
| C | $6,4$ | $-5,-3$ | 二孤子，原文图 3 |

取 $L=40$、$N_x=256$，故 $\Delta x=0.15625$；将 $y\in[-1.5,1.5]$ 等分为 24 个单元，$h=0.125$。时间步长为 $\Delta t=1.25\times10^{-4}$，计算至 $T=0.01$。三种格式采用相同的初始物理场。

在 $x\in[-10,10]$ 上取 4001 个等距点，并取全部 $y$ 层组成评价网格 $\mathcal G$。将数值场沿实际 $x$ 节点作三次样条插值，定义最大绝对误差

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,
\qquad f=u,v.\tag{R18}$$

**表 1　固定网格、RK4 下三种格式的最大绝对误差。每行最小值加粗。**

TABLE_SPACE

算例 A 中 FD 的两个场误差最小；算例 B 中 PE 的 $u$ 误差和 PF 的 $v$ 误差最小；算例 C 中 PE 的 $u$ 误差和 FD 的 $v$ 误差最小。

**表 2　固定网格上不同时间算法的最大绝对误差。每行最小值加粗。**

TABLE_TIME

在算例 A 中，Euler 的总误差略小于 RK4 和 C–N；在算例 B、C 中，RK4 和 C–N 的误差较小且彼此接近。表中比较采用相同的空间网格与时间步长。

**表 3　固定网格与动网格的最大绝对误差（RK4）。每行最小值加粗。**

TABLE_MESH

动网格降低了三个算例中各格式的两个物理场误差，动网格与固定网格的误差比约为 0.332 至 0.838。算例 A 的 PF 格式改进最明显，$u,v$ 的误差分别约为固定网格结果的 0.332 和 0.511。

### 9.5　物理场及误差分布

图 1—6 给出 PF 格式采用 RK4 在固定网格上的数值结果。为展示孤子波形及其相互作用，计算域扩大为 $x\in[-40,40)$、$y\in[-30,30)$，$\Delta x,h,\Delta t,T$ 与前述计算相同。算例 A 展示 $x\in[-3,4],y\in[-3,3]$，算例 B、C 展示 $x,y\in[-30,30]$。每个算例依次给出数值物理场与解析场的对照，以及绝对误差分布。

FIGURES
