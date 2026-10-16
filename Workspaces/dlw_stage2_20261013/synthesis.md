# 约化轨道上的误差：守恒、辛保持与相位漂移

本节使用 2A 的原结构二维行波流形，不对一般 DLW 场或流形外的数值轨道作稳定性断言。

## 1. 两条精确轨道

在 2A 的正则小振幅环域上，写物理场为

\[
Z(x;I,\theta)=Z(x-\theta/k_0;I,0),\qquad
\omega=d\theta\wedge dI,\qquad
\dot I=0,\quad\dot\theta=\Omega(I).
\]

角变量取实数提升；实际场只依赖模 $2\pi$ 的角。固定一个不含零振幅端点的紧 action 区间 $J$。在 $C^r$ 或 $H^r$ 周期场范数中，$Z$ 对参数光滑，故

\[
C_I=\sup_{J\times\mathbb S^1}\|\partial_I Z\|<\infty,
\quad C_\theta=\sup_{J\times\mathbb S^1}\|\partial_\theta Z\|<\infty,
\quad L_\Omega=\sup_J|\Omega'(I)|<\infty.
\]

**命题 1（轨道误差与相位误差的分离）。** 对同一环域内两条精确轨道，令初始参数差为 $\delta I,\delta\theta_0$。则

\[
\delta I(t)=\delta I,
\qquad
\delta\theta(t)=\delta\theta_0+t[\Omega(I+\delta I)-\Omega(I)].
\tag{S1}
\]

其相位对齐后的轨道距离满足对所有时间一致的界

\[
\inf_{\alpha\in\mathbb S^1}
\|Z(I+\delta I,\theta_2(t))-Z(I,\theta_1(t)+\alpha)\|
\le C_I|\delta I|.
\tag{S2}
\]

未作相位对齐时有

\[
\|Z(I+\delta I,\theta_2(t))-Z(I,\theta_1(t))\|
\le C_I|\delta I|+C_\theta
\min\{\pi,|\delta\theta_0|+|t|L_\Omega|\delta I|\}.
\tag{S3}
\]

**证明。** 直接积分两个 action–angle 方程得到 (S1)。在 (S2) 中选择 $\alpha=\theta_2-\theta_1$，再沿 action 线段应用微积分基本定理。对 (S3)，先改变 action、再沿圆周的最短角弧改变相位，分别使用 $C_I,C_\theta$；最后应用频率的 Lipschitz 界。□

2A 给出的非零 twist 表明，除特殊相同 action 情形外，提升角误差一般有非零线性增长率。场误差仍受周期相位空间的直径限制；不能把角的无限增长写成场范数的无限增长。

## 2. 辛保持与剪切可以同时发生

线性化 (S1) 得到变分映射

\[
\binom{\delta\theta(t)}{\delta I(t)}=
M(t)\binom{\delta\theta(0)}{\delta I(0)},\qquad
M(t)=\begin{pmatrix}1&t\Omega'(I)\\0&1\end{pmatrix}.
\]

令 $W=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$，则

\[
M(t)^TWM(t)=W.
\tag{S4}
\]

当 $\Omega'(I)\ne0$ 时，矩阵的欧氏算子范数随 $|t|$ 增长。因而保辛衡量的是双线性面积形式的保持，不是距离收缩，也不是相位误差不增长。这是原 DLW 不变流形内的实际机制，而非另选的示例振子。

## 3. 条件性的强迫误差界

若近似轨道也已证明位于该环域，或其有效约化方程已另行建立，并满足

\[
\dot I_h=r_I(t),\qquad
\dot\theta_h=\Omega(I_h)+r_\theta(t),
\]

则对 $t\ge0$、且两 action 始终处于 $J$ 的时间段，

\[
|\delta I(t)|\le|\delta I(0)|+\int_0^t|r_I(s)|\,ds,
\]
\[
|\delta\theta(t)|\le|\delta\theta(0)|+
L_\Omega\left(t|\delta I(0)|+\int_0^t(t-s)|r_I(s)|\,ds\right)
+\int_0^t|r_\theta(s)|\,ds.
\tag{S5}
\]

**证明。** 积分 action 方程，把所得界代入角方程，再交换三角积分次序。□

初始 action 偏差以一次时间积分进入角误差，持续 action 缺陷以二次积分进入角误差。这给出守恒缺陷与相位精度之间可检验的联系。当前 2B 的网格轨道没有被证明严格留在该行波流形，因此 (S5) 不能直接作为 2B 的误差估计；仍需控制投影残差和横向偏离。
