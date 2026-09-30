# 2-HS 的 GSG 式数值研究：精确解、时间推进、动网格与直接差分

2026-09-24 · 对应代码与机器数据在本目录 `out/` · 本报告的所有“数值结果”均已实际运行。主要文献是 Feng–Sheng–Yu, *Numerical Algorithms* 94 (2023), 351–370, `Paper/sources/Numerical_Algorithms_gsg (1).pdf`，及 Hori–Tanaka–Maruno–Ohta, *An integrable semi-discretization of the two-component Hunter–Saxton equation*, `Paper/sources/2 Huner Saxton.pdf`。下文称前者 **GSG 原文**，后者 **2-HS 原文**。

## 摘要

GSG 原文先构造广义 sine-Gordon 方程的两种可积、另一种非可积半离散系统，再用双线性/行列式得到孤子和连续极限；数值部分列出两种结构动网格、两种普通动网格及一个固定网格 C–N 格式，对正则、非正则和回环 kink 给出解析曲线、数值点、绝对误差及网格表现。本文将**这种比较逻辑**应用到 2-HS 原文已经给出的可积半离散系统。我们的对象有两个物理场 $u,\rho$，必须同时验收两场和物理网格位置。

已实现一阶 Euler、二阶 Heun/显式中点/隐式梯形、四阶 RK4、八阶 DOP853 主公式（固定步长）；还实现普通动网格与连续 2-HS 的直接固定网格差分。结论随参照对象而变：若从**有限 $a$ 精确孤子**起步，原半离散 ODE 的短时求解误差很小，连续总误差却由约一阶的有限格距模型差主导；若从**共同连续初态**起步，普通动网格在所测单孤子窗口内比原半离散系统更贴近连续解。2-HS 的自然动网格在光滑波峰**扩张**；进一步实验表明，先按双场曲率自适应布点、再按普通动网格方程推进，在一个已采样的局部参数区域能同时降低 $u,\rho$ 的实际总误差。两格距 Richardson 后处理还能消去模型误差的主阶。八阶方法降低短时截断误差，但没有解决双孤子长窗增长；完整碰撞后散射仍未通过验收。

## 1. GSG 原文完成了什么，以及我们的对应工作

| 层次 | GSG 原文 | 本 2-HS 工作 |
|---|---|---|
| 方程 | 广义 sine-Gordon，$u_{xt}=(1+\nu\partial_x^2)\sin u$，重点 $\nu=-1$ | 2-HS 的归一化 $c>0$、负 $\mu$ 分支，两个场 $u,\rho$ |
| 结构空间离散 | 用双线性方程的 Bäcklund 变换及离散 hodograph，构造两种可积半离散和一种非可积半离散 | **直接采用 2-HS 原文已证明的** Casoratian/离散 hodograph 半离散系统；另设普通动网格作对照 |
| 解析基准 | 行列式 $N$ 孤子、连续极限；数值图主要用一孤子 | 正规化 $N=1,2$ 精确有限 $a$ tau，连续物理坐标参照，校验双场与网格 |
| 时间方法 | 四种动网格格式及固定网格 C–N；Scheme 1/2 称 integrable SAMM | 在**同一个**半离散右端上分离比较 Euler、三种二阶、RK4、RK8；时间格式的完全可积性不由空间 Lax 对自动推出 |
| 数值呈现 | 图 1–8：解析与数值、绝对误差、不同格式、固定网格比较 | 图 1–13：双场解析与数值、三层误差、时间阶、直接差分、网格分布、局部优化及碰撞失败边界 |

GSG 的 loop 解可以用其移动坐标表示；2-HS 原文 Remark 1 指出其回环分支会令 $\rho$ 发散。因此本报告主实验选择**双场均光滑**的孤子；不能把 GSG 对 loop 的数值优势原样移植到 2-HS 双场问题。

## 2. 被推进的系统及理论时间演化

连续的积分形式和密度守恒式是

$$
u_{tx}-u u_{xx}-\tfrac12u_x^2-4u-\tfrac{c^2}{2}(\rho^2-1)=0,
\qquad \rho_t=(\rho u)_x.
$$

设随动导数 $D_T=\partial_t-u\partial_x$，$w=u_x$。则**精确连续动力学**为

$$
D_Tw=\tfrac12w^2+4u+\tfrac{c^2}{2}(\rho^2-1),
\qquad D_T\rho=\rho w,
\qquad \dot x=-u.
\tag{1}
$$

在计算网格 $k$ 上取 $v_k=u_k-u_{k-1}$、$d_k=x_k-x_{k-1}=a/\rho_k$、$\alpha=a(a-c)$。2-HS 原文式 (81)/(100) 与下面的闭合系统严格等价：

$$
\dot v_k=2d_k(u_k+u_{k-1})+
\frac{(d_k^2-\alpha)^2-v_k^2}{2d_k}-\frac{c^2d_k}{2},
\qquad \dot d_k=-v_k.
\tag{2}
$$

左端给 $u_0=b(T)$、$\dot x_0=-b(T)$ 后，$u_k=b+\sum_{j=1}^kv_j$、$x_k=x_0+\sum_{j=1}^kd_j$、$\rho_k=a/d_k$。这解释数值上“系统怎么演化”：每一级时间推进先由当前差值重构节点 $u$，再计算 $\dot v,\dot d,\dot x_0$；网格速度自动满足 $\dot x_k=-u_k$，密度跟随 $d_k$ 变化。不能冻结网格或冻结 $\rho$ 再更新 $u$。

将 $w_k=v_k/d_k$ 代入 (2)，得到原半离散的斜率形式

$$
\dot w_k=\tfrac12w_k^2+2(u_k+u_{k-1})+
\tfrac12\left[\frac a{\rho_k}+(c-a)\rho_k\right]^2-\tfrac12c^2,
\qquad \dot\rho_k=\rho_kw_k.
\tag{3}
$$

直接对连续式 (1) 在格边用 $w_k=v_k/d_k$、$4u\mapsto2(u_k+u_{k-1})$，则普通动网格右端是

$$
\dot w_k=\tfrac12w_k^2+2(u_k+u_{k-1})+
\tfrac{c^2}{2}(\rho_k^2-1),\qquad \dot d_k=-d_kw_k.
\tag{4}
$$

两者的**同状态右端差**可以不依赖数值拟合地算出：

$$
F_{\rm SD}^{(w)}-F_{\rm ordinary}^{(w)}
=ac(1-\rho_k^2)+\tfrac12a^2(\rho_k^{-1}-\rho_k)^2.
\tag{5}
$$

因此在一般非平凡密度上，原结构系统相对普通格边近似具有 $O(a)$ 修正。这与下面实测的一阶模型差相符；式 (5) 本身不是全时窗误差上界。

## 3. 精确参照、物理坐标及误差定义

取 $c=1,p=5,q=1.25$ 的光滑单孤子，$\omega=1/p-1/q$，$\sigma=\log[(1-aq)/(1-ap)]$，$s_k=(1+e^{-k\sigma-\omega T-\theta_0})^{-1}$。半离散精确场可取一致的平移规范

$$
u_k^*=\omega^2s_k(1-s_k),\quad
x_k^*=ka-\omega s_k+C,\quad
d_k^*=x_k^*-x_{k-1}^*,\quad \rho_k^*=a/d_k^*.
\tag{6}
$$

双孤子使用 2-HS 原文的正常数四项 tau $f_k=1+E_{1,k}+E_{2,k}+A_{12}E_{1,k}E_{2,k}$，以对数和指数权重稳定求导；参数 $p_1=1.1,p_2=1.25,c=1$。一/双孤子的实际 RHS 已分别作解析导数与高精度差分核对，另有 18 组 Fraction 精确代数验证。

需要分清求解、模型和总误差，且移动坐标比较必须额外记坐标项。对 $u$，令 $C[x]$ 表示连续精确解在节点 $x$ 的值；对 $\rho$，令 $C[x]$ 表示对应格边区间的连续密度平均。各项在同一节点或格边编号上逐点定义为

$$
e_{\rm solve}=z_{a,\Delta T}-z_a^*,\qquad
e_{\rm model}=z_a^*-C[x_a^*],\qquad
e_{\rm coordinate}=C[x_a^*]-C[x_{a,\Delta T}],
\quad e_{\rm total}=z_{a,\Delta T}-C[x_{a,\Delta T}]
=e_{\rm solve}+e_{\rm model}+e_{\rm coordinate}.
\tag{7}
$$

$z_a^*$ 是**有限 $a$ 精确解**，不是连续真值。物理坐标下连续真值须在数值 $x_k$ 处反求参数 $X$；$\rho$ 与离散格边比较时采用该物理边区间内连续密度的**单元平均**。式 (7) 是逐点有符号恒等式；各项的最大范数不能直接相加。

代表例 $a=.02,T=.5,\Delta T=.002$ 的实际最大误差为：

| 场 | 求解误差 | 模型误差 | 总误差 |
|---|---:|---:|---:|
| 节点 $u$ | $1.43\times10^{-12}$ | $3.484742\times10^{-3}$ | $3.484742\times10^{-3}$ |
| 格边平均 $\rho$ | $2.31\times10^{-13}$ | $1.520865\times10^{-2}$ | $1.520865\times10^{-2}$ |

坐标差的 $u$ 项小于 $9\times10^{-16}$，格边密度项小于 $4.5\times10^{-14}$。其逐点可加核对见 `out/error_budget.json`。下图显示**半离散精确解**为实线，实际 RK4 推进值为点：曲线重合可证明求解器追踪了有限 $a$ 轨道，不能因此声称已达到连续模型精度。

![图 1：单/双孤子的有限格距精确线与实际数值点](out/figures/fig9_exact_numeric.png)

## 4. 同一半离散方程上的一阶、二阶、四阶、八阶时间格式

将 (2) 连同 $x_0$ 写成 $\dot z=H_a(T,z)$。给定 $H_n=H_a(T_n,z_n)$，我们实现：

| 方法 | 一步公式 | 光滑稳定有限维情形的全局阶 |
|---|---|---:|
| Euler | $z_{n+1}=z_n+\Delta T H_n$ | 1 |
| Heun（显式梯形） | $\widehat z=z_n+\Delta T H_n$；$z_{n+1}=z_n+\frac{\Delta T}{2}[H_n+H(T_{n+1},\widehat z)]$ | 2 |
| 显式中点 | $z_{n+1}=z_n+\Delta T H(T_n+\Delta T/2,z_n+\Delta T H_n/2)$ | 2 |
| 隐式梯形/C–N | $z_{n+1}=z_n+\frac{\Delta T}{2}[H_n+H(T_{n+1},z_{n+1})]$；逐步求解非线性方程 | 2 |
| 经典 RK4 | 四级 $K_1,K_2,K_3,K_4$，权重 $(1,2,2,1)/6$ | 4 |
| 固定步长 RK8 | 12 级 DOP853 八阶主公式：$K_i=H(T_n+c_i\Delta T,z_n+\Delta T\sum_{j\lt i}a_{ij}K_j)$，$z_{n+1}=z_n+\Delta T\sum_i b_iK_i$ | 8 |

八阶系数来自本机 SciPy DOP853 的 12 级表，`hs_solver.py` 对每步**固定** $\Delta T$ 使用八阶主权重；没有混入容差自适应步长。各法每个级都重构新的 $u,\rho,x$ 和阶段时刻左边界。形式局部误差阶分别为 $O(\Delta T^{p+1})$；在增长模态、边界敏感性和浮点舍入存在时，长时观测阶不必等于 $p$。

共同参数 $a=.02,p=5,X\in[-4,4],T=1$，比较对同一**半离散精确** $u$ 的最大误差：

| 方法 | $\Delta T=.1$ | 更细步长及误差 |
|---|---:|---|
| Euler | $1.162\times10^{-2}$ | $.0125\mapsto3.956\times10^{-3}$，粗步长尚未清楚进入一阶渐近区 |
| Heun | $7.062\times10^{-3}$ | $.0125\mapsto1.462\times10^{-4}$ |
| 显式中点 | $3.452\times10^{-3}$ | $.0125\mapsto7.112\times10^{-5}$ |
| 隐式梯形 | $1.495\times10^{-4}$ | $.0125\mapsto2.185\times10^{-6}$ |
| RK4 | $6.461\times10^{-5}$ | $.0125\mapsto1.854\times10^{-8}$ |
| RK8 | $2.81\times10^{-12}$ | $.5\mapsto4.360\times10^{-7}$，$.0625\mapsto9.10\times10^{-14}$，最细已接近舍入地板 |

两个二阶显式格式的误差常数不同；“同阶”不表示同一次实验误差相同。RK8 的 $.5,.25,.125$ 依次约以 144、200 倍减小，呈高阶趋势；最细端受舍入与误差传播影响，不把比值等同于严格八阶证明。两场的完整数值、时间成本及隐式残差见 `out/extended_methods.json`。

![图 2：六种时间方法对有限格距单孤子的 u 与 rho 误差](out/figures/fig5_time_orders.png)

## 5. 从半离散精确轨道到连续解：空间模型的误差地板

保持 $p=5,c=1,X\in[-4,4],T=.5$，RK4 $\Delta T=.002$，用半离散精确初态积分。此时求解误差对 $u$ 约 $1.4\times10^{-12}$，但连续真值的模型误差为：

| $a$ | $u$ 最大模型误差 | $\rho$ 边平均最大模型误差 |
|---:|---:|---:|
| .04 | $7.2273\times10^{-3}$ | $3.1986\times10^{-2}$ |
| .02 | $3.4847\times10^{-3}$ | $1.5209\times10^{-2}$ |
| .01 | $1.7128\times10^{-3}$ | $7.4190\times10^{-3}$ |
| .005 | $8.4918\times10^{-4}$ | $3.6648\times10^{-3}$ |

减半比趋近 2，符合 (5) 的一阶修正。提高时间阶**不会消除有限 $a$ 模型差**。下图左边画实际场随时间演化及其半离散误差，右边画时间方法和连续极限；连续解析解的虚线与有限 $a$ 实线之间的差是模型差。

![图 3：单孤子双场传播、求解误差和网格间距](out/figures/fig1_single.png)

![图 4：时间误差与有限格距连续极限](out/figures/fig2_convergence.png)

## 6. 自适应移动网格到底带来了什么

2-HS 自然移动网格由 $d_k=a/\rho_k$ 和 $\dot x_k=-u_k$ 精确驱动；这就是与 GSG 相对应的**结构性自适应网格**，不是事后为了好看重新摆点。本单孤子峰处 $\rho\approx.64$，所以当 $a=.02$ 时峰处 $d\approx.032$，背景 $d=.02$：波峰处网格**更疏**。实际节点位移及间距见图 5。

![图 5：节点移动轨迹和峰区网格扩张](out/figures/fig10_grid_motion.png)

为只测“同样节点数的几何表示效果”，在同一物理两端和 401 节点上，把连续精确 $u,\rho$ 分别采样于自然网格、均匀物理网格、$u$ 曲率监视器网格、$u/\rho$ 双场曲率监视器网格；再作分段线性插值，在密集公共物理网格上算误差。监视器由精确参照预先计算，属于**空间表示实验**，尚不是新的可积时间演化格式。$T=.5$ 的结果：

| 网格 | 波峰邻域平均间距 | $u$ 最大插值误差 | $\rho$ 最大插值误差 |
|---|---:|---:|---:|
| 2-HS 自然移动网格 | .02819 | $3.1595\times10^{-5}$ | $8.0954\times10^{-5}$ |
| 均匀物理网格 | .02150 | $1.4975\times10^{-5}$ | $3.8340\times10^{-5}$ |
| 仅 $u$ 曲率监视器 | .00872 | $2.7738\times10^{-6}$ | $7.9509\times10^{-5}$ |
| 双场曲率监视器 | .00915 | $6.4044\times10^{-6}$ | $1.5262\times10^{-5}$ |

本波形下，自然网格的插值误差反而大于均匀网格；只盯 $u$ 的监视器显著改善 $u$，但不能保证 $\rho$；双场监视器对两个场都有改善。它**不能**证明把这些节点在每个时间步重布后，仍求解同一个可积半离散系统。重布会改变空间方程、引入插值误差；若要做真正动态监视器算法，必须另定 ALE/重映射方程并单独验证。

![图 6：等节点数网格分布与双场插值误差](out/figures/fig7_mesh_sampling.png)

## 7. 直接有限差分：空间怎么离散，时间怎么推进

对连续 2-HS 取 $m=u_{xx}+2$，微分形式变成

$$
m_t=u m_x+2u_xm+c^2\rho\rho_x,\qquad
\rho_t=(u\rho)_x,\qquad
u_{xx}=m-2.
\tag{8}
$$

固定物理网格 $x_j=x_L+j\Delta x$，用中心差分

$$
D_0f_j=\frac{f_{j+1}-f_{j-1}}{2\Delta x},\quad
D_2f_j=\frac{f_{j+1}-2f_j+f_{j-1}}{\Delta x^2}.
$$

每个时间级先解三对角离散 Poisson 方程 $D_2u_j=m_j-2$，再计算 $\dot m_j=u_jD_0m_j+2(D_0u_j)m_j+c^2\rho_jD_0\rho_j$ 与 $\dot\rho_j=D_0(u\rho)_j$。该**空间**离散光滑情形形式上二阶；时间再独立选择 §4 的任何方法。光滑孤子实验使用两端连续精确边界数据，因而与只有左端解析驱动的移动开链在边界信息上不完全相同；图表应注明这一点。

$c=1,p=5,T=.25$，固定网格 RK8 取 $\Delta T=.005$ 使时间误差不主导，实际空间结果为：

| $\Delta x$ | $u$ 对连续精确解最大误差 | $\rho$ 最大误差 |
|---:|---:|---:|
| .08 | $1.0074\times10^{-5}$ | $9.2098\times10^{-5}$ |
| .04 | $2.5309\times10^{-6}$ | $2.3128\times10^{-5}$ |
| .02 | $6.3349\times10^{-7}$ | $5.7884\times10^{-6}$ |
| .01 | $1.5842\times10^{-7}$ | $1.4483\times10^{-6}$ |

两个场减半比都约 4，清楚支持所测短时二阶空间收敛。另固定 $\Delta x=.04$，用极细步 RK8 作为**同一个固定空间 ODE** 的时间参照。$\Delta T=.005$ 时，状态最大时间误差：Euler $3.14\times10^{-5}$、Heun $3.42\times10^{-8}$、中点 $3.27\times10^{-8}$、梯形 $1.87\times10^{-8}$、RK4 $4.22\times10^{-14}$、RK8 约 $8\times10^{-15}$。但直接对连续解的 $u$ 总误差仍约 $2.53\times10^{-6}$：此时**空间误差是地板**。这展示了“先有限差分、再时间推进”的演化链，以及必须分别测两类误差的原因。

![图 7：直接有限差分的空间二阶收敛与固定网格时间误差](out/figures/fig6_direct_fd.png)

## 8. 共同连续初态下的三种空间路线

自然结构半离散 (2)、普通动网格 (4) 在同一 $X$ 标签上采样**同一个连续初始 $u,x,d$**，均用 RK4；直接固定差分 (8) 在物理区间采样同一连续解，用 C–N。401 节点、$a=.02$、$\Delta T=.001$、$T=.5$ 时：

| 路线 | 连续物理坐标 $u$ 最大误差 | 本机耗时 |
|---|---:|---:|
| 结构半离散 + RK4 | $2.0741\times10^{-1}$ | .65 s |
| 普通动网格 + RK4 | $2.4466\times10^{-4}$ | .66 s |
| 固定物理网格 + C–N | $1.7036\times10^{-6}$ | 5.32 s |

固定网格拥有两端解析边界；移动网格只给左端，所以不能由表格宣布普遍的算法优劣。针对较少受远端影响的 $x\in[-2,2]$，在 $T=.25$ 将 $a=.04,.02,.01$ 加密，结构半离散 $u$ 误差为 $.02311,.01147,.005717$（约一阶），普通动网格为 $6.02,1.51,.377\times10^{-5}$（约二阶）。$\Delta T=.001$ 减半在 $T=.5$ 几乎不改结构格式的核心误差，说明这组差异主要不由当前 RK4 步长决定。整组边界/域宽审计见 `out/audit.json`。

这与 §5 的“结构格式求解误差 $10^{-12}$”并不矛盾：§5 的初值是**有限 $a$ 精确孤子**，这里的初值是**连续精确解**；所问的误差对象不同。

![图 8：共同连续初值的三路数值场与误差成本](out/figures/fig4_methods.png)

## 9. 双孤子、八阶推进和长时失败

从 $T=-3$ 的有限 $a$ 双孤子精确初态真正推进至 $T=3$。RK4 $\Delta T=.001,.0005$ 的终点 $u$ 误差分别为 $6.53\times10^{-4},7.07\times10^{-4}$；RK8 $\Delta T=.05,.025,.0125$ 分别为 $7.55,6.84,6.69\times10^{-4}$。提高时间阶或继续减步都未恢复终点预期阶数。图 9 同时显示精确曲线与数值点：整体形状仍近似，但误差表明不能只凭视觉判定精度。

![图 9：双孤子相互作用五个时刻的实际数值双场](out/figures/fig3_collision.png)

![图 10：RK4/RK8 的双孤子误差增长与长窗停止](out/figures/fig8_collision_error.png)

延长至目标 $T=9$ 时，RK4 两档步长分别于 $T\approx6.177,6.136$ 停止；RK8 $\Delta T=.0125$ 也于 $T\approx6.155$ 因网格边趋零停止。此时 $T=6$ 的场误差已很大。报告保留所有失败时间和最后状态，不将失败曲线放进“成功散射”图。该现象与背景线性化的增长相容，但有限开链的误差放大、边界、浮点和非线性贡献尚未严格分解。

## 10. 理论解释、结论与证据边界

背景 $u=0,\rho=1,d=a$ 的半离散线性化含 $\dot{\tilde d}=-\tilde v$、$\dot{\tilde v}=2a(\tilde u_k+\tilde u_{k-1})+c(2a-c)\tilde d$。无限/周期格的形式 Fourier 符号为 $\lambda^2+2ia\cot(\theta/2)\lambda-c(c-2a)=0$。$c=1,a=.02,\theta=\pi$ 给实增长率约 $.980$。因此场方程**非线性**，其背景也不具全波数线性稳定性。空间半离散的 tau/Lax 可积结构，与某个 Euler、RK4、RK8 全离散格式是否仍可积，是不同命题。

对光滑单孤子，已核验：一阶/二阶/四阶/八阶方法在短时各有预期精度趋势；原半离散系统的有限格距模型差约一阶，直接物理有限差分在本初边值设置下约二阶；2-HS 自然动网格在峰区变疏，等节点数插值表示没有从几何上获益。§6 的双场监视器先改善纯表示误差；§11 进一步检验其布点后的真实时间推进。更高时间阶不能消除模型误差、空间误差或增长模态。双孤子的**完整碰撞后散射、长时稳定精度以及每步动态监视器重布格式**仍是明确的未验收任务。

## 11. 进一步得到的局部“确实更好”结论

为检验自适应网格对**实际推进误差**的作用，新增同一普通动网格 ODE 的非均匀计算质量版本：在连续精确初态上按 $u,\rho$ 双场曲率等分监视器，之后由 $\dot x_k=-u_k$ 自然移动，不在内部重置精确值。对 $p=5,N=201,T=.25,\Delta T=.001$，相同节点数、端点、左边界和 RK4 下，均匀/自适应的全域 $u$ 节点误差为 $1.54087\times10^{-4}/1.78577\times10^{-5}$，$\rho$ 格边平均误差为 $6.91903\times10^{-6}/1.45216\times10^{-6}$，分别改善 8.63、4.76 倍。将两组数值场重建到同一物理区间的 2001 个点，$u$ 误差仍由 $1.40248\times10^{-4}$ 降至 $3.91199\times10^{-5}$，$\rho$ 由 $4.24440\times10^{-4}$ 降至 $1.57656\times10^{-4}$。中心附近 27 组参数配对在两种误差定义下均双场改善；误差对光滑参数的连续依赖说明，中心严格优势对应一个开放的局部优势邻域。27 组是采样盒证据，没有给整个盒的区间认证或开放邻域的认证半径。这个算法是**自适应初始布点加真实动网格推进**，并非每一步重新等分的 ALE 算法，也未证明保留原可积性。

![图 11：自适应初始布点后的实际动网格推进误差](out/figures/fig11_adaptive_dynamic.png)

格距模型差的精确右端公式见 (5)；单孤子相位还有 $\sigma(a)/a=(p-q)+a(p^2-q^2)/2+O(a^2)$。因此格距 $a$、谱参数 $p$、参数 $c$、时间窗口和密度偏离背景的程度都会影响模型误差常数。$p=5,T=.5$ 时，$a=.04,.02,.01,.005$ 的 $u$ 模型误差依次为 $.007227,.003485,.001713,.000849$；固定 $a=.02,T=.5$，$p=4.5,5,5.5$ 则为 $.002837,.003485,.004111$。固定 $p=5,a=.02,T=.5$，$c=.9,1,1.1$ 对应的 $u$ 模型误差为 $.002532,.003485,.004564$。

![图 12：格距与波形参数对模型误差的影响](out/figures/fig12_model_factors.png)

在同一物理坐标对两次**实际数值推进**作 $2z_{a/2}-z_a$，可消去平滑的一阶格距主项。$p=5,T=.5$，细格距 $a/2=.01$ 时，单次计算对连续解的 $u/\rho$ 误差为 $.001712/.007406$，组合后为 $.0000841/.000436$；27 个已测参数组合中两个场均改善。这是降低连续解总误差的明确途径，但组合场是后处理，不是原半离散方程的新精确解。时间方法方面，八阶对有限 $a$ 精确解的求解误差在邻域扫描中严格优于 RK4；连续总误差是否随之降低则取决于时间误差是否已低于模型误差地板。详细参数盒、逐场数据、局部连续性论证和复现见 [局部优势专题报告](LOCAL_ADVANTAGE_REPORT.md)。

![图 13：两格距后处理消去主阶模型误差](out/figures/fig13_richardson.png)

## 12. 把自适应布点提升为守恒坐标

2-HS 原文本身已有 $dX=\rho\,dx+u\rho\,dt$，来自 $\rho_t=(u\rho)_x$；固定 $X$ 标签的节点满足 $\dot x=-u$，等距 $X$ 均分每个移动单元的 $\rho$-质量。它是本系统与 GSG 守恒弧长坐标对应的**内禀 hodograph 结构**，只是本波形的 $\rho$ 在峰处较低，天然等质量布点未必为双场误差最优。

§11 的曲率权重还可以严格写成一个**新的守恒重参数坐标**。把初态选出的正权重 $\mu(X)$ 固定为质量标签 $X$ 的函数，定义 $Y=\int^X\mu(s)ds$、$R=\rho\mu(X(x,t))$。由于 $X$ 随速度 $-u$ 输运，可逐项得到

$$
R_t-(uR)_x=0,\qquad dY=R\,dx+uR\,dt,
\qquad x_Y=R^{-1},\quad \dot x\big|_Y=-u.
\tag{9}
$$

因此我们在初态等分 $\int\mu dX$，等价于选固定且等距的 $Y$ 标签；每个移动物理单元的 $\int Rdx$ 随时间守恒。这说明现有“初始曲率布点 + 自然移动”的实验并非只有采样直觉，而有精确的连续守恒解释。$\mu=1$ 即原文坐标。权重是由初态设计并随流携带的；若改为每步按**当前**曲率重新设 $\mu$，式 (9) 不再自动成立。

也不能直接令 GSG 的弧长密度 $\sqrt{1+u_x^2}$ 代替 $\rho$：在本 2-HS 方程中它一般不满足同速度的守恒律。限定在只依赖 $u_x,\rho$、且节点仍以 $-u$ 运动的局部密度类，要求对任意光滑解守恒会迫使密度只能是常数倍 $\rho$。加权坐标借助额外的被动标签权重绕过了这一限制。完整推导、限定范围及机器核验见 [守恒监视器坐标说明](CONSERVATIVE_HODOGRAPH.md)。该坐标支持普通动网格的理论解释；原文常 $a$ 的可积半离散 τ/Lax 结构并未因此自动推广到变 $a_k$。

### 复现入口

在工作区根目录：

```powershell
python Workspaces/hs_numerics_plan/verify_formulas.py
python Workspaces/hs_numerics_plan/validate.py
python Workspaces/hs_numerics_plan/run_study.py
python Workspaces/hs_numerics_plan/run_extended_methods.py
python Workspaces/hs_numerics_plan/adaptive_mesh_study.py
python Workspaces/hs_numerics_plan/audit_conclusions.py
python Workspaces/hs_numerics_plan/error_budget.py
python Workspaces/hs_numerics_plan/local_advantage_study.py
python Workspaces/hs_numerics_plan/local_neighborhood_probe.py
python Workspaces/hs_numerics_plan/local_time_comparison.py
python Workspaces/hs_numerics_plan/coarse_time_advantage.py
python Workspaces/hs_numerics_plan/model_factor_study.py
python Workspaces/hs_numerics_plan/richardson_model.py
python Workspaces/hs_numerics_plan/make_figures.py
python Workspaces/hs_numerics_plan/make_extended_figures.py
python Workspaces/hs_numerics_plan/make_local_advantage_figures.py
python Workspaces/hs_numerics_plan/validate_local_advantage.py
python Workspaces/hs_numerics_plan/verify_conservative_hodograph.py
python Workspaces/hs_numerics_plan/build_extended_report.py
node Workspaces/hs_numerics_plan/validate_extended_report.js
```

原始数值表：`out/results.json`、`out/extended_methods.json`、`out/mesh_representation.json`、`out/audit.json`、`out/error_budget.json`，以及 §11 对应的 `local_advantage.json`、`local_neighborhood.json`、`local_time_comparison.json`、`coarse_time_advantage.json`、`model_factor.json`、`richardson_model.json`；快照 `out/snapshots.npz`。完整的运行参数、计时、源文件哈希和失败记录随数据保存。图只从这些实测结果生成，不以精确解替代数值终态。
