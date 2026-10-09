## 9　非线性半离散系统的数值实现

半离散系统保留 $x,t$ 连续，仅将 $y$ 替换为格点。本节进一步离散 $x$ 并作时间积分，以检验两种非线性表示的计算表现。SD、SD2 分别指第 5 节的物理变量形式和第 7 节的势变量形式；FD 为直接离散连续 DLW 方程的对照方法。有限 $x$ 网格上的差分不满足连续乘积法则，因此 SD 与 SD2 的数值结果可以不同，尽管其半离散物理场精确对应。

### 9.1　计算域、初值与精确参照

采用文献 [1] 的三组参数，$a=2$、$\rho_i=1$、初相位为零。

| 算例 | $p_i$ | $q_i$ | 对应解 |
|---|---|---|---|
| A | $1$ | $2$ | 单孤子，原文图 1(a) |
| B | $4$ | $-3$ | 单孤子，原文图 1(b) |
| C | $6,4$ | $-5,-3$ | 二孤子，原文图 3 |

精确参照取（34）的连续 τ 函数，并用（2）的解析对数导数计算 $u_*,v_*$。A、B 的振幅比为 $1/4,2$；C 的振幅比为 $4/3,2$，交叉项系数为 $4/3$。三组均有正系数展开。B、C 不属于命题 5.1 所选的有序正实谱子域，但其各子集系数、振幅比与小格距格点乘子均为正，故正性及固定谱参数的偶次展开论证仍适用；这里使用的是该论证的直接推广。

主误差表取 $x\in[-20,20)$，$N_x=256$，$\Delta x=0.15625$；$y\in[-1.5,1.5]$ 划分 24 个单元，$h=0.125$，物理场位于单元中点。时间步长为 $\Delta t=1.25\times10^{-4}$，终点为 $T=0.01$。所有方案从相同的连续物理初值出发，因而表中误差同时包含半离散模型、$x$ 差分、时间积分及场值重构的影响。该试验与定理 6.3 的精确半离散 Gram 解族比较是两个不同层次的问题。

### 9.2　连续方向 $x$ 的差分

对任意一层的离散函数 $z_{j,i}\simeq z_j(x_i,t)$，固定网格 $x_i=-20+i\Delta x$ 上取

$$D_1z_{j,i}=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x},\qquad
D_2z_{j,i}=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}.\tag{N1}$$

离散右端中的 $\partial_x$、$\partial_{xx}$ 分别替换为 $D_1,D_2$。特别地，$D_2$ 直接采用三点二阶导数算子，不以复合算子 $D_1D_1$ 代替。对光滑函数，二者截断误差依次为 $\Delta x^2z_{xxx}/6$ 和 $\Delta x^2z_{xxxx}/12$。$h$ 控制 $y$ 向半离散误差，$\Delta x$ 控制另一个空间方向的数值误差。

动网格在均匀计算坐标 $\xi_i=-20+i\Delta\xi$ 上写为 $x_i(t)=\xi_i+s_i(t)$。由 $\partial_x=J^{-1}\partial_\xi$ 得

$$\begin{aligned}
J_i&=1+D_\xi s_i,\\
D_1z_i&=J_i^{-1}D_\xi z_i,\\
D_2z_i&=J_i^{-2}D_{\xi\xi}z_i-J_i^{-3}(D_\xi J)_i(D_\xi z)_i.
\end{aligned}\tag{N2}$$

$D_\xi,D_{\xi\xi}$ 是（N1）在均匀计算坐标上的算子，$\Delta\xi=40/256$。这一定义在 $s=0$ 时退化为固定网格公式；在光滑、$J$ 有正下界的映射上具有二阶局部截断精度。

SD、FD 沿 $x$ 作周期延拓。SD2 的 $Q,R$ 两端通常趋于不同常数，采用加性跳量延拓：若 $z(x+L)=z(x)+b$，则虚点为 $z_{-1}=z_{N_x-1}-b$、$z_{N_x}=z_0+b$，随后仍使用（N1）或（N2）。该处理用于孤子尾部已接近常数背景的计算域。

沿 $y$ 的最下层物理场每级取解析边界，最上层虚点取解析背景加扰动外推。若 $e_j=u_j-u_{*,j}$，则 $e_{J+1}=3e_J-3e_{J-1}+e_{J-2}$。下侧边界固定了从 $\delta_-u$ 恢复 $u$ 时的积分自由度。这些边界条件构成本文孤子基准的闭合方式。

### 9.3　SD、SD2 与 FD 的离散右端

**SD。** 以 $P_j=\delta_-u_j$、$W_j=4\omega_j/h$ 为演化变量，定义

$$H_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).$$

每个时间级先由 $u_j=u_{j_L}+h\sum_{k=j_L+1}^jP_k$ 恢复 $u$，再计算

$$\begin{aligned}
F_P&=-\delta_-D_1H-D_2(P+M_-W),\\
F_W&=-D_1[(u+2a)W-4u]+D_2W,\qquad v=W+\delta_0u.
\end{aligned}\tag{N3}$$

初值为 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$。

**SD2。** 置 $S_j=Q_jR_j$、$\Gamma_j=h^2(S_j^2-1)/4$、$m_j=M_{j,x}$。以下为简洁将最下层重新编号为 $0$。由下边界的 $Q_0,Q_{0,t}$ 计算

$$\begin{aligned}
m_0&=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}-\frac{\Gamma_0}{2}+\frac h2D_1S_0,\\
m_{j+1}&=m_j-hD_1S_j,\qquad A_j=m_j+m_{j+1},\\
F_Q&=-D_2Q-2aD_1Q-(A+\Gamma)Q,\\
F_R&=D_2R-2aD_1R+(A+\Gamma)R,\\
u&=2(D_1Q)/Q,\qquad v=4(1-QR)+\delta_0u.
\end{aligned}\tag{N4}$$

为使三个方案的初始物理场一致，各层解线性提升问题 $D_1Q_j^0=u_j^0Q_j^0/2$、$Q_{j,0}^0=1$，同时求端点跳量；然后取 $R_j^0=[1-(v_j^0-\delta_0u_j^0)/4]/Q_j^0$。下边界每个时间级采用同一提升，其时间导数由提升方程微分求得。内部 $Q$ 和全部 $R$ 按（N4）演化。动网格下先求物质时间导数，再扣除网格输运以获得式中的 $Q_{0,t}$。

**FD。** 直接对连续方程离散，以 $P=\delta_-u$ 与 $v$ 演化：

$$\begin{aligned}
F_P&=-\delta_-D_1(u^2/2+2au)-D_2M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u.
\end{aligned}\tag{N5}$$

其 $u$ 的恢复及边界与 SD 相同。

### 9.4　网格运动与时间积分

取 $\rho_j=1-W_j/4$；在 SD2 中它等于 $Q_jR_j$。对全部物理层平均，定义

$$\begin{aligned}
\bar\rho&=\frac1{24}\sum_j\rho_j,\\
\bar q&=\frac1{24}\sum_j[(u_j+2a)\rho_j-D_1\rho_j-2a],\\
\mathcal V_i&=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\qquad \dot x_i=\mathcal V_i.
\end{aligned}\tag{N6}$$

初始节点按 $\bar\rho$ 的累积积分等分。移动节点上的场变量满足 $\dot z=\mathcal F(t,z)+\mathcal V D_1z$；节点与场在同一时间级更新，每级重新计算 $J$、边界和离散右端。固定网格取 $s=0,\mathcal V=0$。计算要求 $J>0$、节点有序，动网格另要求 $\bar\rho>0$。

时间比较采用显式 Euler、经典四级 RK4 和隐式梯形 C–N。把节点并入状态后，三者均应用于同一常微分方程右端。Euler 为 $z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n)$；RK4 为

$$\begin{aligned}
k_1&=\mathcal F(t_n,z^n),\\
k_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_1/2),\\
k_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_2/2),\\
k_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t\,k_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4).
\end{aligned}\tag{N7}$$

C–N 解

$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].\tag{N8}$$

主表沿用残差阈值 $10^{-12}+10^{-11}\max(1,\|z^n\|_\infty)$，以 Euler 预测、固定点修正，最多 80 次迭代。本文的全离散计算用于比较误差，其可积结构结论针对前述保持 $x,t$ 连续的半离散方程。

### 9.5　误差定义与数值结果

在 $[-10,10]$ 上取 4001 个等距评价点，结合全部 $y$ 层形成 $\mathcal G$。将数值场沿实际 $x$ 节点作三次样条插值，定义

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_{\rm num}(x,y,T)-f_*(x,y,T)|,\qquad f=u,v.\tag{N9}$$

这是固定采样集上的最大误差。主试验包含三个算例、三个空间方案、固定网格的三种时间算法以及动网格 RK4，共 36 组，均到达共同终点。初始物理场的最大节点差小于 $2.0\times10^{-13}$。

**表 1　固定网格、RK4 下的空间方案比较。**

TABLE_SPACE

算例 A 中 FD 的两个场误差最小；B 中 SD 的 $u$ 误差和 SD2 的 $v$ 误差最小；C 中 SD 的 $u$ 误差和 FD 的 $v$ 误差最小。两种半离散表示的精确等价不意味着它们在额外差分后具有相同误差，也不意味着对每个场都优于 FD。

**表 2　固定网格上的时间算法比较。**

TABLE_TIME

固定空间网格时，减小时间误差后可能由空间误差主导。因此表 2 用于比较给定步长下的总误差，不能单独用于判定时间收敛阶。

**表 3　Euler 的时间自收敛。** 记 $d_f(\Delta t)=\|f_{\Delta t}-f_{\Delta t/2}\|_{\infty,\mathcal G}$，观测阶为 $p_f=\log_2[d_f(\Delta t)/d_f(\Delta t/2)]$，其中初始 $\Delta t=1.25\times10^{-4}$。

TABLE_ORDER

表 3 的 SD、SD2 均呈现接近一阶的时间自收敛。C–N 的公式为二阶，但固定迭代容差可干扰细化检验：现有算例 C 的独立配对复核中，仅将容差缩紧至 $10^{-15}+10^{-14}\max(1,\|z^n\|_\infty)$，SD、SD2、FD 六个场的观测阶恢复至 $1.9986$—$2.0001$。该容差检验与表 2 沿用的原容差数据分开报告。

**表 4　相同节点数和时间步长下的固定、动网格比较（RK4）。**

TABLE_MESH

网格移动对不同场的作用并不一致，结论应逐算例、逐物理场读取。这里不将网格聚集本身等同于误差降低。

### 9.6　物理场及误差分布

图 1—6 保留已有数值报告中的 SD2、RK4、固定网格结果。场图采用独立宽域 $x\in[-40,40)$、$y\in[-30,30)$，$\Delta x,h,\Delta t,T$ 与主表相同。A 展示 $x\in[-3,4],y\in[-3,3]$；B、C 展示 $x,y\in[-30,30]$。每个算例先给出数值曲面及数值、解析等高线对照，再给出绝对误差分布。宽域图与表 1—4 的计算域和评价集不同。

FIGURES

### 9.7　短时试验的解释

上述结果验证了给定光滑孤子、计算域和短时间窗口内的数值表现。端点尾部复核在 $T=0.01$ 给出 B、C 两端物理场之差不超过 $1.1\times10^{-8}$，小于当前主表误差。

空间一致性本身不提供长时间稳定性。以 SD 的零背景为例，$x$ 棋盘格扰动 $P_{j,i}=(-1)^i$、$W=0$ 满足 $D_1P=0$，而 $-D_2P=4P/\Delta x^2$，存在正增长高频分支。因此本文不从短时孤子结果推出对一般扰动的网格一致稳定性。定理 6.3 给出精确解族的 $h^2$ 极限；全离散算法的联合空间收敛仍需独立控制 $h,\Delta x,\Delta t$ 和边界误差。

## 10　结论

从连续 DLW 方程出发，本文构造了交错半离散双线性系统，并通过秩一更新证明任意有限阶 Gram τ 函数的精确性。对称格点构造给出双线性和非线性方程的二阶一致性，固定谱数据的正则解族在紧区域上以 $O(h^2)$ 逼近连续物理场。SD 与 SD2 通过势变量精确关联；相应 Darboux–Lax 表示在明确的势差和非退化条件下恢复原半离散方程。

数值部分将保留连续的 $x$ 方向补充离散，统一比较 SD、SD2、FD，以及时间推进和网格策略。实验显示，各方案的误差优势随算例和物理场变化。进一步研究将集中于控制高频增长的计算策略，以及独立的空间细化检验。

## 参考文献

[1] H.-H. Sheng, G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. *Physica D*, **432** (2022), 133140. [原文](../Paper/sources/PhysD-published.pdf).

[2] B.-F. Feng, H.-H. Sheng, G.-F. Yu. Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation. *Numerical Algorithms*, **94** (2023), 351–370. DOI: [10.1007/s11075-023-01504-1](https://doi.org/10.1007/s11075-023-01504-1).

[3] W. Fu. Direct linearisation of the discrete-time two-dimensional Toda lattices. arXiv:[1802.06452](https://arxiv.org/abs/1802.06452), version 3 (2018).

[4] Y.-B. Tian, Y. Cheng, N. Shao. Construction of recursion formulas for Lax pairs of (2+1)-dimensional equation: Modified generalized dispersive long wave equation. *Communications in Theoretical Physics*, **41** (2004), 807–812. [原文](../Paper/refs/ctp8805.pdf).
