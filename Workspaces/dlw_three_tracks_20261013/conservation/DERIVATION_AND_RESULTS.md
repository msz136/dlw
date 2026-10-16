# 1A：周期 DLW 谱守恒量的离散值与漂移

日期：2026-10-13。此处交付实际运行的 Python 实验、原始及相对漂移曲线、逐时数据、收敛表和核验记录。

## 1. 量的定义与实验适用域

本实验严格使用既有周期逆单值化定义

\[
 I_n=\int_0^{L_x}\operatorname{res}_D\mathscr L^n\,dx,\qquad n=1,2,3.
\]

它不是质量、动量、能量的随意编号，也不是 \(I_n/n\)。它与非周期线孤子的透射系数展开 \(\log\mathcal T(z)=\sum C_nz^{-n}\) 中的 \(C_n\) 不同。论文斜线孤子的单站 \(C_n\) 可以有限，但横向无限求和通常发散；有限窗口也存在边界通量。因此本实验另取周期平均约束流形，不能把数值结论直接归于论文 A/C 的开放窗口。

横向周期格点数 \(M=3\)，横向格距 \(h_y=4\)，\(x\in[0,2\pi)\) 周期，\(c=2,\gamma=4\)。这里 \(h_y=4\) 沿用已有精确 Fourier 独立性见证的规范，**不是论文算例的横向格距**。时间窗 \(0\le t\le0.02\)。这是保留连续 \(x\) 时的原平均约束流形的数值近似；有限 \(x\) 网格是数值截断，不宣称其为有限维可积约化。

依据：[周期单值化证明](../../dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md)、[精确 Fourier 见证](../../dlw_conservation_hierarchy_20261004/lax/fixed_leaf_independence_checks.json)。

## 2. 可直接执行的前三密度

记 \(g_j=h_yw_j/4\)，\(A_j=(U_j+g_j)/2\)，\(B_j=(U_j-g_j)/2\)，

\[
 S_j=(D-B_j)^{-1}(D-A_j),\qquad
 \mathscr P=S_{M-1}\cdots S_0
 =1+aD^{-1}+bD^{-2}+p_3D^{-3}+\cdots .
\]

平均约束使 \(G=\sum_jg_j\ne0\)、\(T=\sum_jU_jg_j\) 为常数，

\[
 a=-G,\quad b=(G^2-T)/2,\quad
 \mathscr L=a(\mathscr P-1)^{-1}+b/a.
\]

本例 \(G=6,T=12,a=-6,b=12\)。单因子及乘积递推为

\[
 s_{j,1}=-g_j,\qquad s_{j,n+1}=B_js_{j,n}-Ds_{j,n},
\]
\[
 (a_iD^i)(b_jD^j)=\sum_{r\ge0}{i\choose r}a_iD^r(b_j)D^{i+j-r}.
\]

前三个积分采用以下连续密度代表元；后两式只需模全 \(x\) 导数成立：

\[
\begin{aligned}
 \rho_1&=b^2/a^2-p_3/a,\\
 \rho_2&\equiv-2p_4/a+4bp_3/a^2-2b^3/a^3,\\
 \rho_3&\equiv-3p_5/a+6bp_4/a^2+6p_3^2/a^2
              -15b^2p_3/a^3+6b^4/a^4.
\end{aligned}
\]

代码计算上述 \(p_3,p_4,p_5\) 后用周期矩形求积

\[
 I_{n,\Delta x}=\Delta x\sum_{\ell=0}^{N_x-1}
 \rho_n[U,w;D_{\Delta x}](x_\ell).
\]

**含义须精确：**这是已证明连续谱量的指定密度代表元的离散评估。把 \(D\) 换成有限矩阵后，通常不满足 Leibniz 恒等式，所以上述乘法程序不是一个已证明的离散伪微分算子代数，\(I_{n,\Delta x}\) 也不自动是完全离散系统的严格积分。不同模导数等价的连续表达，在离散时可能有不同截断误差。此处固定表达，不在不同网格间更换。

## 3. 与 1C 同一括号的 Hamilton 数值流

令 \(\Pi\) 为横向平均，\(P_0=1-\Pi\)。采用

\[
 p=P_0U,\quad s=w-c,\quad
 U=p+\frac{\gamma-\Pi(ps)}{c},\qquad w=c+s,
\]
\[
 R=(d|_{\ker\Pi})^{-1}M_-P_0,\quad
 d=(1-E^{-1})/h_y,\quad M_-=(1+E^{-1})/2,\quad \beta=h_y^2/32.
\]

本例
\[
 R=\frac23\begin{pmatrix}0&-1&1\\1&0&-1\\-1&1&0\end{pmatrix}.
\]

以 \(\omega=h_y\Delta x\) 为配对权重，离散 Hamilton 函数为

\[
 K_{\Delta x}=\omega\sum_{j,\ell}
 \left[\frac{U^2w}{2}+\frac\beta3w^3+wD_{\Delta x}U
 +\frac12wR D_{\Delta x}w-\gamma U\right]_{j\ell}.
\]

由 \(D_{\Delta x}^*=-D_{\Delta x}\)、\(R^*=-R\) 且二者作用于不同方向，\(RD_{\Delta x}\) 自伴。先对 \(U,w\) 求导，得到

\[
 f=Uw-D_{\Delta x}w-\gamma,
 \qquad k=U^2/2+\beta w^2+D_{\Delta x}U+RD_{\Delta x}w.
\]

\(\Pi f=0\) 在平均约束流形上点态成立；故复合映射的平均剪切项消失，约化梯度为 \((P_0f,P_0k)\)。实际求解

\[
 \dot p=-P_0D_{\Delta x}k,\qquad
 \dot s=-P_0D_{\Delta x}f.
\]

此推导不需要离散 Leibniz 公式。它确实是
\(J_{\Delta x}=-\left(\begin{smallmatrix}0&P_0D_{\Delta x}\\P_0D_{\Delta x}&0\end{smallmatrix}\right)\)
生成的 Hamilton ODE，而不是将任意已展开的连续方程逐项替换导数。普通坐标偏导所对应的矩阵括号为 \(J_{\Delta x}/\omega\)，与 1C 的规范一致。

实验比较中心一阶差分与实反对称 Fourier 一阶导数矩阵；二阶导数总取 \(D_{\Delta x}^2\)。中心差分不是另外选择的三点 Laplacian。Fourier 偶数网格的 Nyquist 一阶导数取零。两者均满足常 Poisson 结构，但这不足以使所有 \(I_n\) 守恒。

连续时间 ODE 精确满足 \(dK_{\Delta x}/dt=0\)。时间离散采用经典 RK4，RK4 不严格保持 \(K_{\Delta x}\)。本实验的小漂移是实测精度，不是算法恒等式。

初值取已有见证：

\[
 p=(-3,0,3)+(1/5,-2/5,1/5)\cos x,
\]
\[
 g=(1,2,3)+(1/6,1/7,-1/6-1/7)\cos x,\qquad w=4g/h_y.
\]

对应连续 \(I_n/L_x\) 的精确值为

\[
 4-\frac{466031}{3528\cdot48},\qquad
 \frac{724400267}{296352000},\qquad
 \frac{98646175112939}{11948912640000}.
\]

未减去基态常数；三个初值均非零。图中相对漂移分母严格使用每次运行自己的 \(|I_{n,\Delta x}(0)|\)，绝对漂移为 \(I_{n,\Delta x}(t)-I_{n,\Delta x}(0)\)。

## 4. 实际误差演化与机制

对任何指定离散泛函 \(I_{n,\Delta x}\)，连续时间数值流 \(\dot z=F_{\Delta x}(z)\) 精确满足

\[
 \frac{d}{dt}I_{n,\Delta x}(z(t))
 =D I_{n,\Delta x}(z(t))[F_{\Delta x}(z(t))]
 =:\mathcal D_{n,\Delta x}(z(t)).
\]

代码通过复步长方向微分计算 \(\mathcal D_{n,\Delta x}\)，不是相邻时刻相减；在存储轨迹上用 Simpson 积分核验
\(\Delta I_n\simeq\int_0^t\mathcal D_{n,\Delta x}\,dt\)。差值还包含 RK4 与诊断求积误差。这给出了实际离散守恒缺陷，避免把曲线形状单独当作机理。

最简单的一条机制是原有 \(I_1\) 的退重复恒等式。设
\(P_{\mathrm{mom},\Delta x}=\omega\sum ps\)，本例有

\[
 I_{1,\Delta x}=-\frac{K_{\Delta x}}{48}
 +\frac{P_{\mathrm{mom},\Delta x}}{24}+2L_x,
\]
\[
 \boxed{\Delta I_1=-\Delta K_{\Delta x}/48
                  +\Delta P_{\mathrm{mom},\Delta x}/24.}
\]

该离散关系只需周期分部求和，已在整条轨迹上独立核验，最大残差小于 \(7\times10^{-15}\)。常 Poisson 结构保护 \(K\) 的连续时间守恒，但 \(D_{\Delta x}\) 通常不是点乘代数的导子，因此不保证 \(P_{\mathrm{mom}}\) 守恒。其精确缺陷为

\[
 \frac{dP_{\mathrm{mom},\Delta x}}{dt}
 =\omega\sum\left[fD_{\Delta x}p+kD_{\Delta x}s\right].
\]

1C 另给出这项非零的有理数反例。于是本实验的 \(I_1\) 漂移可以追到平移对称的离散缺陷，即使 \(K\) 的数值漂移已经很小。

## 5. 数值结果

共同 \(\Delta t=2.5\times10^{-4}\)，81 个输出时刻。下表为 \([0,0.02]\) 内最大绝对漂移；中心差分三项在此窗内均于终点取最大值。

| x 算子 | \(N_x\) | \(\max|\Delta I_1|\) | \(\max|\Delta I_2|\) | \(\max|\Delta I_3|\) |
|---|---:|---:|---:|---:|
| 中心差分 | 24 | 7.55509e−8 | 1.50117e−5 | 1.26773e−4 |
| 中心差分 | 48 | 1.98071e−8 | 3.90472e−6 | 3.31944e−5 |
| 中心差分 | 96 | 5.01057e−9 | 9.85825e−7 | 8.39430e−6 |
| Fourier | 24 | 5.32907e−15 | 8.17124e−14 | 9.80549e−13 |
| Fourier | 48 | 5.32907e−15 | 1.86517e−13 | 5.67013e−12 |

中心差分 \(I_3\) 的相对最大漂移为 \(2.4439\times10^{-6}\)、\(6.3992\times10^{-7}\)、\(1.6183\times10^{-7}\)。三量的空间观测阶依次为

| 精化 | \(I_1\) | \(I_2\) | \(I_3\) |
|---|---:|---:|---:|
| 24→48 | 1.9314 | 1.9428 | 1.9332 |
| 48→96 | 1.9830 | 1.9858 | 1.9835 |

这验证的是指定短时初值族下谱量漂移的二阶空间尺度，不是对一般解的误差定理。各运行 \(K\) 最大漂移不超过 \(2.3\times10^{-13}\)，约束残差不超过 \(4.9\times10^{-15}\)。\(N_x=24\) 中心差分的 \(I_2,I_3\) 初始缺陷率分别为 \(-8.31076\times10^{-4}\)、\(6.71737\times10^{-3}\)，而 \(I_1\) 初始缺陷率因初值对称性近零，之后出现近二次漂移。缺陷积分与中心差分实测漂移的最大差值小于 \(7.5\times10^{-13}\)。

固定 \(N_x=24\) 另以 1024 步轨迹为时间参考，分别用 1、2、4、8 步。中心差分场时间误差为 \(1.45\times10^{-8},9.28\times10^{-10},5.86\times10^{-11},3.68\times10^{-12}\)，显示约四阶；Fourier 得到相同趋势。\(I_n\) 的时间误差也下降，但很快进入 \(10^{-13}\) 左右的舍入区间，不对这些末端点拟合阶。时间精化不能替代空间精化。

Fourier 两网格在公共采样点的终点场差约 \(3.1\times10^{-12}\)。这一窗内所有谱量漂移已经接近计算误差；更细网格反而使高次密度的微分舍入误差稍大。没有用过滤器抑制高频，也没有给出长期稳定性结论。DLW 实时间高频增长使延长时间窗需要独立研究；不能把本次近守恒解释为全离散可积或一般长期有界。

## 6. 核验与文件

- `conservation_experiment.py`：方程、初值、PDO 系数递推、演化、全部表和图一键重生成。
- `invariant_drift_absolute.png/.pdf`：用户要求的三项 \(\Delta I(t)\) 曲线。
- `invariant_drift.png/.pdf`：相对漂移，便于比较量级。
- `error_separation.png/.pdf`：时间场误差与空间谱量漂移分别精化。
- `invariant_timeseries.csv`：81 时刻×5 运行；含 \(I_n,\Delta I_n\)、相对漂移、瞬时缺陷率、\(K,P\) 与约束残差。
- `invariant_summary.csv`、`space_refinement.csv`、`time_refinement.csv`：数值表。
- `validation.json`：初值精确见证对照、梯度方向微分、反对称性、约束、全部运行及缺陷积分误差。
- 五个 `centered_n*.npz` / `spectral_n*.npz`：实际 \((p,s)\) 状态轨迹；其余 `time_*.npz` 是时间精化端点轨迹。

执行：在工作区运行 `python Workspaces/dlw_three_tracks_20261013/conservation/conservation_experiment.py`。仅用已安装的 NumPy、Matplotlib，无外部数据或安装步骤。

脚本用既有有理 Fourier 证书核对初始谱量，最大密度均值误差 \(2.8\times10^{-11}\)；新数值核验并不替代原符号证明。Hamilton 梯度以独立有限差分方向检查，绝对差约 \(7.4\times10^{-9}\)，连续时间 \(\nabla K\cdot F\) 约 \(8.7\times10^{-13}\)。这些浮点核验不是 Jacobi 的证明，Jacobi 理论和精确符号证书由 1C 交付。

绘图采用 `plot-is-all-you-need` 快速路径，取图库 `oa-geo-bg-21-3305-2024-f02` 的三联时间轴、简洁轴线和底部共享图例结构；不用该参考图的观测区间色带。用户数据未收入图库。候选布局包括三联时序、四联趋势和相轨迹；当前三个守恒量共同时间轴适合首选。成图已打开目视复核，并对轴量级与 CSV 核对。
