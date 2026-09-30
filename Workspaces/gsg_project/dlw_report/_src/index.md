# DLW 孤子数值解的误差比较

<p class="abstract"><strong>摘要</strong>　在原文单孤子与二孤子参数下，比较三种空间离散方案、Euler 与 RK4 时间算法以及固定与自适应动网格。采用共同物理评价点上的双场最大绝对误差，每项对照固定其余数值条件。空间方案的相对精度依赖算例，SD 与 SD2 的误差排名可随时间算法改变。两种时间算法在单孤子 A 中的总误差接近，在单孤子 B 与二孤子 C 中则为 RK4 双场较小。动网格的收益依赖算例、离散化及物理场。时间自收敛结果支持 Euler 的一阶行为。</p>

## 1　实验设计

比较两场结构半离散方案 SD、以 $Q,R$ 为演化变量的结构半离散方案 SD2，以及直接差分方案 FD。时间算法取显式 Euler 与经典 RK4。网格取均匀固定网格（fixed）与初始自适应布点、随后持续移动的网格（moving）。SD 与 SD2 表示同一半离散结构的不同变量形式。

采用 Sheng–Yu 原文的三组参数，见表 1。均取 $a=2$、$c_i=1$，初相位为零。每个算例均比较三种离散化、两种时间算法与两种网格，共 12 个组合。同一网格策略下，各方案采用相同的初始节点和离散 $u,v$，以共同连续解析解作为误差参照。

<div class="caption">表 1　算例参数与比较范围。</div>

| 算例 | 原文图号 | 谱参数 | 比较范围 |
|---|---|---|---|
| 单孤子 A | 图 1(a) | $(p,q)=(1,2)$ | 三离散化 × 两时间法 × 两网格 |
| 单孤子 B | 图 1(b) | $(p,q)=(4,-3)$ | 三离散化 × 两时间法 × 两网格 |
| 二孤子 C | 图 3 | $(p_1,q_1)=(6,-5)$；$(p_2,q_2)=(4,-3)$ | 三离散化 × 两时间法 × 两网格 |

计算区间取 $x\in[-20,20)$，$N_x=256$；$y\in[-1.5,1.5]$，格距 $h_y=1/8$，共 24 个中点层。$x$ 方向采用四阶中心差分。主时间步长为 $\Delta t=1.25\times10^{-4}$，从 $t=0$ 推进至 $T=0.01$。

在 $x\in[-10,10]$ 的 4001 个等距点及全部 $y$ 层上，经三次样条重构，计算最大绝对误差

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_h(x,y,T)-f_*(x,y,T)|,\qquad f\in\{u,v\}.\tag{1}$$

其中 $f_*$ 为连续精确解。所有结果均为总误差，包含初始表示误差。对照设计见表 2；同一行只改变“比较因素”一项。跨算例比较方法的相对表现，不将不同波形的绝对误差差异归因于孤子数量。

<div class="caption">表 2　三项配对对照。各组均取相同评价时刻与误差指标。</div>

| 对照 | 比较因素 | 固定条件 |
|---|---|---|
| 空间离散化 | SD / SD2 / FD | 各自算例、RK4、fixed、空间格距、时间步长 |
| 时间算法 | Euler / RK4 | 各自算例与离散化、fixed、空间格距、时间步长 |
| 网格策略 | fixed / moving | 各自算例与离散化、RK4、节点数、时间步长 |

## 2　演化方程与数值递推

记 $h=h_y$，在 $y$ 方向定义

$$\begin{aligned}
\delta_-f_j&=\frac{f_j-f_{j-1}}h,&
\delta_0f_j&=\frac{f_{j+1}-f_{j-1}}{2h},\\
M_-f_j&=\frac{f_j+f_{j-1}}2,&
\Delta_hf_j&=\frac{f_{j+1}-2f_j+f_{j-1}}{h^2}.
\end{aligned}\tag{2}$$

在固定 $x$ 网格上采用四阶中心差分

$$
(D_1f)_{j,i}=\frac{f_{j,i-2}-8f_{j,i-1}+8f_{j,i+1}-f_{j,i+2}}{12\Delta x},
\qquad D_2f=D_1(D_1f).
\tag{3}$$

### 2.1　SD

令 $P_j=\delta_-u_j$、$W_j=v_j-\delta_0u_j$，并记

$$H_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{4}$$

非线性半离散方程写为

$$\begin{aligned}
P_{j,t}&=-\delta_-\partial_xH_j
-\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_hP_j\right),\\
W_{j,t}&=-\partial_x[(u_j+2a)W_j-4u_j]+\partial_x^2W_j.
\end{aligned}\tag{5}$$

初始取 $P_j^0=\delta_-u_j^0$、$W_j^0=v_j^0-\delta_0u_j^0$。每个时间级按下式恢复物理场并计算演化右端：

$$\begin{aligned}
u_{j,i}&=u_{j-1,i}+hP_{j,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i},\\
\mathcal F_{P,j}&=-\delta_-D_1H_j
-D_2\left(M_-v_j-\frac{h^2}{4}\Delta_hP_j\right),\\
\mathcal F_{W,j}&=-D_1[(u_j+2a)W_j-4u_j]+D_2W_j.
\end{aligned}\tag{6}$$

### 2.2　SD2

以 $Q_j,R_j$ 为演化变量，半离散方程为

$$\begin{aligned}
Q_{j,t}&=-Q_{j,xx}-2aQ_{j,x}
-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
R_{j,t}&=R_{j,xx}-2aR_{j,x}
+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\
M_{j+1}-M_j&=h(1-Q_jR_j).
\end{aligned}\tag{7}$$

由共同初始物理场求出 $Q_j^0,R_j^0$：

$$
D_1Q_j^0=\frac12u_j^0Q_j^0,\qquad Q_{j,0}^0=1,\qquad
R_j^0=\frac{1-(v_j^0-\delta_0u_j^0)/4}{Q_j^0}.
\tag{8}$$

令 $S_j=Q_jR_j$、$m_j=M_{j,x}$。每个时间级先计算

$$\begin{aligned}
G_j&=\frac{h^2}{4}(S_j^2-1),\\
m_0&=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{G_0}{2}+\frac h2D_1S_0,\\
m_{j+1}&=m_j-hD_1S_j,\qquad A_j=m_j+m_{j+1}.
\end{aligned}\tag{9}$$

其中第零层的 $Q_0$ 由 $D_1Q_0=u_0Q_0/2$、$Q_{0,0}=1$ 求出，$Q_{0,t}$ 由该式对时间求导得到。随后计算

$$\begin{aligned}
\mathcal F_{Q,j}&=-D_2Q_j-2aD_1Q_j-(A_j+G_j)Q_j,\\
\mathcal F_{R,j}&=D_2R_j-2aD_1R_j+(A_j+G_j)R_j,\\
u_{j,i}&=2\frac{(D_1Q)_{j,i}}{Q_{j,i}},\qquad
v_{j,i}=4(1-Q_{j,i}R_{j,i})+(\delta_0u)_{j,i}.
\end{aligned}\tag{10}$$

### 2.3　FD

连续 DLW 方程为

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}\tag{11}$$

取 $P_j=\delta_-u_j$，初始取 $P_j^0=\delta_-u_j^0$ 和 $v_j^0$。对连续方程作交错中心差分，得到

$$\begin{aligned}
u_{j,i}&=u_{j-1,i}+hP_{j,i},\\
\mathcal F_{P,j}&=-\delta_-D_1\left(\frac{u_j^2}{2}+2au_j\right)-D_2M_-v_j,\\
\mathcal F_{v,j}&=-D_1[(u_j+2a)v_j-4u_j]-D_2\delta_0u_j.
\end{aligned}\tag{12}$$

### 2.4　时间更新与节点运动

分别取 $z=(P,W)$、$z=(Q,R)$ 和 $z=(P,v)$，将上述右端记为 $\mathcal F(t,z)$。Euler 更新为

$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n).\tag{13}$$

RK4 更新为

$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),&
K_2&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_1\right),\\
K_3&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_2\right),&
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta tK_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}\tag{14}$$

每一级均按式（6）、（9）—（10）或（12）恢复场值并计算右端。

动网格取 $x_i=\xi_i+s_i$、$J_i=1+(D_\xi s)_i$，其中 $D_\xi$ 为式（3）在均匀 $\xi$ 节点上的四阶中心算子；此时 $D_1=J^{-1}D_\xi$、$D_2=D_1(D_1)$。令 $N_y$ 为 $y$ 层数，节点及演化变量按下式更新：

$$\begin{aligned}
\rho_j&=1-\frac{v_j-\delta_0u_j}{4},\\
\bar\rho_i&=\frac1{N_y}\sum_j\rho_{j,i},\qquad
\bar q_i=\frac1{N_y}\sum_j\bigl[(u_j+2a)\rho_j-D_1\rho_j-2a\bigr]_i,\\
V_i&=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\qquad
\dot x_i=V_i,\qquad \dot z=\mathcal F(t,z)+VD_1z.
\end{aligned}\tag{15}$$

固定网格取 $V_i=0$；两种网格均采用式（13）或（14）的时间更新。

## 3　空间离散化的比较

固定 RK4 与均匀网格，以 FD 为基准，定义 $R_f^{S/FD}=E_f^S/E_f^{FD}$。表 3 中小于 1 表示误差低于 FD。

<div class="caption">表 3　不同空间方案相对于 FD 的误差比，$T=0.01$。</div>

| 算例 | SD：$u$ | SD：$v$ | SD2：$u$ | SD2：$v$ |
|---|---:|---:|---:|---:|
| 单孤子 A | 0.703 | 0.841 | 3.044† | 1.441† |
| 单孤子 B | 1.746 | 1.906 | 1.901 | 2.373 |
| 二孤子 C | 1.156 | 1.775 | 1.535 | 3.021 |

<p class="table-note">† 单孤子 A 的 SD2 固定网格在 $T=0.01$ 未通过空间加密对照，相关数值仅描述主配置；表 4、5 使用相同标记。</p>

单孤子 A 中，SD 的 $u,v$ 误差分别低于 FD 约 30% 和 16%。单孤子 B 与二孤子 C 中，两个场的误差均按 FD、SD、SD2 的次序增大。因此，结构半离散方案相对于直接差分的精度优势依赖具体算例，不能由其结构来源直接推断。

单孤子 B 与二孤子 C 均包含谱对 $(4,-3)$，两者在当前配置下均为 FD 优于 SD。这说明该相对表现可以在单孤子与二孤子算例中同时出现，但不构成仅由孤子数量决定的误差规律。

## 4　时间算法的比较

对每个算例固定均匀网格和空间离散，比较相同步长下的 Euler 与 RK4。表 4 给出 $R_f^{E/R}=E_f^{\mathrm{Euler}}/E_f^{\mathrm{RK4}}$；大于 1 表示 RK4 误差较小。

<div class="caption">表 4　Euler 相对于 RK4 的总误差比，fixed，$T=0.01$。</div>

| 算例 | 空间方案 | $R_u^{E/R}$ | $R_v^{E/R}$ |
|---|---|---:|---:|
| 单孤子 A | SD | 1.002 | 0.996 |
| 单孤子 A | SD2† | 0.996 | 0.996 |
| 单孤子 A | FD | 0.990 | 0.996 |
| 单孤子 B | SD | 1.603 | 2.582 |
| 单孤子 B | SD2 | 1.084 | 5.944 |
| 单孤子 B | FD | 1.604 | 4.681 |
| 二孤子 C | SD | 2.036 | 4.112 |
| 二孤子 C | SD2 | 1.189 | 11.345 |
| 二孤子 C | FD | 1.473 | 7.205 |

单孤子 A 中，两种时间算法的总误差相差约 1% 以内，部分指标为 Euler 略小。单孤子 B 与二孤子 C 中，三种空间方案均为 RK4 双场误差较小，其中 SD2 的 $v$ 误差比分别为 5.944 和 11.345。较高时间阶并不保证每个算例的总误差都更小；这里比较的是相同步长的精度，而非相同计算成本。

单孤子 B 与二孤子 C 还表现出相同的排名变化：对 $u$ 而言，RK4 下 SD 优于 SD2，Euler 下则为 SD2 优于 SD；对 $v$ 而言，两种时间算法均为 SD 优于 SD2。因此，空间方案的排名需要同时指定时间算法与物理量。

为区分时间收敛与总误差，在固定空间配置下取 $\Delta t$、$\Delta t/2$、$\Delta t/4$，以数值场之间的差计算观测阶

$$p_f=\log_2\frac{\|f_{\Delta t}-f_{\Delta t/2}\|_{\infty,\mathcal G}}{\|f_{\Delta t/2}-f_{\Delta t/4}\|_{\infty,\mathcal G}},\qquad f\in\{u,v\}.\tag{16}$$

单孤子试验在三种空间方案、两种网格及所测时刻的观测阶为 0.9874–1.0025；SD2 在原文图 3–5 二孤子中的相应结果为 0.9903–1.0001，均支持 Euler 的一阶时间行为。该观测阶与表 4 的总误差比含义不同：前者衡量时间离散的收敛行为，后者同时包含空间、时间及场表示误差。

## 5　网格策略的比较

对每个算例固定 RK4、空间方案和节点数，定义 $R_f^{M/F}=E_f^{\mathrm{moving}}/E_f^{\mathrm{fixed}}$，结果见表 5。

<div class="caption">表 5　自适应动网格相对于均匀固定网格的误差比，$T=0.01$。</div>

| 算例 | 空间方案 | $R_u^{M/F}$ | $R_v^{M/F}$ |
|---|---|---:|---:|
| 单孤子 A | SD | 0.611 | 0.601 |
| 单孤子 A | SD2† | 0.243 | 0.464 |
| 单孤子 A | FD | 0.686 | 0.671 |
| 单孤子 B | SD | 1.075 | 1.064 |
| 单孤子 B | SD2 | 1.008 | 0.947 |
| 单孤子 B | FD | 0.798 | 1.102 |
| 二孤子 C | SD | 0.980 | 1.071 |
| 二孤子 C | SD2 | 0.828 | 0.761 |
| 二孤子 C | FD | 0.676 | 1.101 |

单孤子 A 中，SD 与 FD 的两个场均得到改善，误差降低约 31%–40%。单孤子 B 中，SD 的两个场误差均略增，FD 的 $u$ 改善约 20%，$v$ 却增加约 10%。二孤子 C 中，SD2 双场改善约 17% 和 24%，FD 仍表现为 $u$ 改善、$v$ 略差。动网格收益因而同时依赖算例、空间方案与物理场。单孤子 A 的 SD2 比值涉及空间敏感的固定网格结果，不据此估计稳定收益。

这里的网格因素包含初始节点分布与后续节点运动：fixed 使用均匀节点，moving 使用自适应初始节点并持续移动。不同离散化采用相同的监测规则，节点由各自数值场驱动。表 5 衡量两套网格策略的总体效果，不单独分离初始布点与后续移动的贡献。

## 6　结论

在原文参数与共同评价条件下，SD 与 FD 的相对精度依赖算例。两种时间算法在单孤子 A 中的总误差接近，在单孤子 B 与二孤子 C 中则为 RK4 双场较小；后两个算例中，SD 与 SD2 的 $u$ 排名均随时间算法改变。自适应动网格既可能改善双场，也可能使一个或两个场的误差增大，其收益需要结合算例、离散化与物理量评价。

这些结果支持对时间算法、空间离散与网格进行配对研究，而不支持脱离其余条件给出单一最优方案。当前结论限于所列参数、分辨率与短时间区间；时间自收敛支持 Euler 一阶行为，空间误差常数及网格一致的收敛范围仍需单独估计。进一步比较空间精度时，应固定算例、时间算法与网格策略，分别考察 $h_y$ 与 $\Delta x$ 的变化。

## 参考资料

<div class="references">
<p>[1] H.-H. Sheng and G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. <em>Physica D</em>, 432 (2022), 133140.</p>
<p>[2] <a href="Workspaces/dlw_single_aligned_20260929/HANDOFF.md">DLW 原文单孤子三方案的误差结果</a>。</p>
<p>[3] <a href="Workspaces/dlw_sd2_uv_init_20260929/HANDOFF.md">DLW 原文二孤子三方案的误差结果</a>。</p>
</div>
