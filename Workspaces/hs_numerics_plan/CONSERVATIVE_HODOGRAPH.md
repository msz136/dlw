# 2-HS 的守恒监视器坐标：从原 hodograph 到双场自适应网格

2026-09-24。本文回答“能否像 GSG 那样由守恒律建立自适应坐标，而非仅在初态上随意采样”。结论分两层：**2-HS 原文已经有内禀守恒坐标 (X)**；曲率加权可以进一步严格构造一个**守恒的重参数坐标 (Y)**，解释现有普通动网格算法的自适应布点。但 (Y) 的权重由初态选择，不是由 2-HS 方程唯一指定；将它代入原文常格距可积半离散式并保持 Lax/τ 结构，尚未证明。

## 1. 原文给出的内禀守恒坐标

对本文归一化的 2-HS 分支，连续方程有

\[
\rho_t=(u\rho)_x,\qquad \rho>0.
\tag{1}
\]

因此原文式 (17)/(43) 的 reciprocal/hodograph 坐标是

\[
dX=\rho\,dx+u\rho\,dt,\qquad dT=dt.
\tag{2}
\]

这不是经验选择：\(X_x=\rho, X_t=u\rho\) 的交叉导数相等恰是 (1)。固定 \(X\) 时 \(0=dX/dt=\rho(\dot x+u)\)，所以

\[
\dot x\big|_X=-u,\qquad x_X=\rho^{-1}.
\tag{3}
\]

在 \(X\) 上取等距 \(X_k=ka\)，对应每条移动物理边上的 \(\rho\)-质量

\[
\int_{x_{k-1}(t)}^{x_k(t)}\rho(x,t)\,dx=X_k-X_{k-1}=a.
\tag{4}
\]

原文离散 hodograph 恰为 \(d_k=x_k-x_{k-1}=a/\rho_k\)，以及 \(\dot d_k=-(u_k-u_{k-1})\)。所以 2-HS **早已有与 GSG 守恒弧长坐标同等级别的结构来源**；它均分的是 \(\rho\)-质量，不是曲线弧长。由于本实验光滑波峰处 \(\rho<1\)，(4) 在该处给出较大的物理边长，这解释原自然网格为什么在那里变疏。

## 2. 把双场曲率权重变成真正守恒的坐标

在初态给一个正的计算坐标权重 \(\mu(X)>0\)，例如现有数值实验的

\[
\mu(X)=1+\frac{\gamma}{2}\left(
\frac{|u_{xx}(x(X,0),0)|}{\max|u_{xx}|}+
\frac{|\rho_{xx}(x(X,0),0)|}{\max|\rho_{xx}|}\right).
\tag{5}
\]

这里 \(\gamma=2\)，两个最大值只在选定初始区间上取；若某场曲率恒为零，应把该项置零而不能除以零。**权重以后作为 \(X\) 标签的函数固定**，不在每个时间重新根据当前曲率计算。定义

\[
Y=\Phi(X),\qquad \Phi'(X)=\mu(X),\qquad R(x,t)=\rho(x,t)\mu(X(x,t)).
\tag{6}
\]

由 (2) 立即得到一个 GSG 式的新 reciprocal 坐标：

\[
dY=R\,dx+uR\,dt,\qquad Y_x=R,\quad Y_t=uR,
\qquad \dot x\big|_Y=-u,\quad x_Y=R^{-1}.
\tag{7}
\]

其守恒律也可直接验算。令物理权重 \(\widetilde\mu(x,t)=\mu(X(x,t))\)，则 \(\widetilde\mu_t-u\widetilde\mu_x=0\)；利用 (1)，

\[
R_t-(uR)_x
=\rho(\widetilde\mu_t-u\widetilde\mu_x)=0.
\tag{8}
\]

在 \(Y\) 上取等距 \(Y_k=Y_0+k\Delta Y\)，每条移动物理边满足

\[
\int_{x_{k-1}(t)}^{x_k(t)}R(x,t)\,dx=\Delta Y.
\tag{9}
\]

这就是“均分监视器质量”的精确含义。它与程序中的初始等分 \(\int\mu(X)dX\) 完全对应：\(X_k=\Phi^{-1}(Y_k)\)，所以原 \(X\) 单元质量 \(a_k=X_k-X_{k-1}\) 不等；经过初态变换后的物理节点按 (3) 移动。离散上 \(\rho_k=a_k/d_k\) 且令边平均权重 \(\mu_k=\Delta Y/a_k\)，便有 \(R_k=\rho_k\mu_k=\Delta Y/d_k\)。因此在当前普通动网格推进中，每条边的 \(R_kd_k=\Delta Y\) 是精确的重构恒等式，而不仅是初态上一张漂亮的采样图。

但 (5) 是**初态驱动的设计权重**。若希望每一时刻都按当前曲率重新均分，\(\mu\) 将不再满足 \(\widetilde\mu_t-u\widetilde\mu_x=0\)；要重新推 ALE/重映射方程和误差、守恒校验。

## 3. 为什么不能直接照搬 GSG 的弧长密度

GSG 有特殊恒等式 \(r=\sqrt{1+u_x^2}\) 且 \(r_t+(r\cos u)_x=0\)。对这里的 2-HS，令 \(w=u_x\)、\(D=\partial_t-u\partial_x\)，则

\[
Dw=\tfrac12w^2+4u+\tfrac{c^2}{2}(\rho^2-1),
\qquad D\rho=\rho w.
\tag{10}
\]

若强行取弧长密度 \(r=\sqrt{1+w^2}\)，要让它与速度 \(-u\) 一起守恒必须满足 \(Dr=rw\)，但实际差为

\[
Dr-rw=\frac{w}{\sqrt{1+w^2}}
\left(4u-1-\tfrac12w^2+\tfrac{c^2}{2}(\rho^2-1)\right),
\tag{11}
\]

一般不为零。因此这里**没有同一个简单的弧长守恒律**。

还有一个限定范围内的唯一性判断：假设另找一个只依赖当前 \(w,\rho\) 的局部密度 \(F(w,\rho)\)，并要求它在**相同节点速度 \(-u\)** 下对任意光滑解守恒。由 (10) 和 \(DF=Fw\)，比较独立的 \(u\) 项，必有 \(F_w=0\)；其余条件给 \(\rho F_\rho=F\)，所以 \(F=C\rho\)。这只排除该类无额外变量、同速度的局部斜率密度；它不排除含 \(u\)、导数、非局部量、其他速度或额外被动标签的守恒构造。式 (6) 正是通过**额外的被动标签权重**获得新的正密度。

## 4. 已核验什么、下一层工作是什么

`verify_conservative_hodograph.py` 用符号代数核对 (8)，并在 \(c=1,p=5,N=201,\gamma=2\) 的实际监视器布点上检查 200 个单元的初始 \(\int\mu dX\) 等分；同一数值积分规则下最大相对偏差约 \(1.8\times10^{-14}\)，\(\rho_kd_k=a_k\) 的最大初始残差约 \(3.5\times10^{-18}\)。这些是坐标与守恒身份核对，不代替全时窗误差证明。其实际动网格误差改善已在 [局部优势报告](LOCAL_ADVANTAGE_REPORT.md)记录。

因此本项目可以明确采用两条研究线：**原文 \(X\) 坐标**保持其已知可积半离散结构；**加权 \(Y\) 坐标**给普通动网格一个真正守恒的自适应解释和已测误差优势。若要宣称加权网格仍是新的可积半离散系统，下一步必须重新构造非均匀格距下的双线性/τ 恒等式或 Lax 对，而不能仅把原公式中的常数 \(a\) 换成 \(a_k\)。

原文依据：`Paper/sources/2 Huner Saxton.pdf` 式 (11)、(17)、(51)–(54)、(84)–(85)、(93)–(105)。数值入口：`local_advantage_study.py`；验证命令：`python Workspaces/hs_numerics_plan/verify_conservative_hodograph.py`；机器记录：`out/conservative_hodograph.json`。
