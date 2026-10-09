# DLW 方程的半离散化、τ 函数与连续极限

<div class="abstract"><span class="abstract-label">摘要</span> 从连续 DLW 方程的双线性表示出发，构造以半格点为中心的交错半离散双线性系统。通过相邻辅助层之间的秩一更新，证明任意有限阶 Gram 行列式满足该系统，并由 Cauchy 主子式展开给出相应的孤子 τ 函数。在有序正实谱参数下，τ 函数严格为正，其对数导数产生全局正则的非线性半离散解。进一步证明半离散方程及物理变量重构的二阶一致性，并建立固定谱参数的精确 Gram 解族在任意紧区域上的一致二阶连续极限。附录给出保留辅助势的 Q、R、M 表示及其物理变量映射。</div>

**关键词：** DLW 方程；半离散双线性系统；Gram 行列式；交错格点；连续极限

半离散化将一个空间方向替换为格点，同时保留其余变量的连续演化。对于具有 τ 函数表示的方程，双线性结构提供了一条连接离散方程、精确解与连续极限的途径：格点平移与谱参数变换相配合，行列式恒等式给出有限格距下的精确关系，而相位和振幅的展开决定相应解族的极限。

本文沿这一思路讨论 DLW 方程。首先将连续双线性对写成适于交错格点的形式，再构造相邻格点之间的两条双线性方程。任意有限阶 Gram 解的精确性由统一的矩阵计算得到；其正性允许通过对数导数恢复物理场。最后，分别考察方程的一致性与精确解族的连续极限，并明确两条非线性方程各自的空间评价位置。

连续变量记为 $(x,y,t)$，格点编号为 $j\in\mathbb Z$，格距为 $h>0$，参数 $a\in\mathbb R$ 固定。采用文献 [1] 中 $\lambda=-2$ 的 DLW 归一化。所用函数在各结论指定的区域内取实解析类；对数及平方根取正实分支。记号 $O_K(h^m)$ 表示在紧集 $K$ 上一致有界的 $m$ 阶余项，其常数可依赖固定的函数和谱数据。

## 1　连续 DLW 方程的双线性表示

考虑连续方程

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

对严格正的 τ 函数 $f(x,y,t),g(x,y,t)$，定义物理场

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

Hirota 算子定义为

$$D_x^rD_y^sD_t^m f\cdot g
=\left.(\partial_x-\partial_{x'})^r(\partial_y-\partial_{y'})^s
(\partial_t-\partial_{t'})^m
f(x,y,t)g(x',y',t')\right|_{(x',y',t')=(x,y,t)}.$$

记 $B_s=D_x^2+D_t+2sD_x$。连续双线性对为

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

由于

$$D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y,\qquad
\partial_y(B_af\cdot g)=B_af_y\cdot g+B_af\cdot g_y,$$

在 $B_af\cdot g=0$ 时，第二条方程可写为

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{4}$$

**命题 1.1（双线性表示与物理场）。** 设 $f,g$ 在开区域内严格为正且实解析，并满足（3）。则由（2）定义的 $u,v$ 满足（1）。

**证明。** 令 $\alpha=\log f$、$\beta=\log g$、$\phi=\alpha-\beta$、$S=\alpha+\beta$。第一条双线性方程除以 $fg$ 后为

$$S_{xx}+\phi_x^2+\phi_t+2a\phi_x=0.$$

对其施加 $2\partial_x\partial_y$，并使用 $u=2\phi_x$、$v=2S_{xy}$，得到（1）的第一条方程。

另一方面，乘积法则给出

$$\frac{B_af\cdot g_y}{fg}
=\beta_y\frac{B_af\cdot g}{fg}
+\beta_{xxy}-(u+2a)\beta_{xy}-\beta_{yt}.$$

由（4）及 $2D_xf\cdot g/(fg)=u$，有

$$\beta_{yt}-\beta_{xxy}+(u+2a)\beta_{xy}-u=0.$$

令 $b=4\beta_{xy}$，对上式施加 $4\partial_x$，得

$$b_t-b_{xx}+[(u+2a)b-4u]_x=0.$$

由（2），$b=v-u_y$。代入上式，并利用已得的第一条 DLW 方程消去 $u_{yt}$，即得（1）的第二条方程。□

## 2　交错格点双线性系统

将 $G_j$ 放在 $y=jh$，将 $F_j$ 放在 $y=(j+\tfrac12)h$。以 $F_j$ 为中心，定义半离散双线性系统

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{5}$$

两条方程分别连接半格点及其左右邻点，算子参数随平移作对称调整。固定物理位置 $y$，记

$$\mathcal B_h^- = B_{a-h/2}f(x,y,t)\cdot g(x,y-h/2,t),\qquad
\mathcal B_h^+ = B_{a+h/2}f(x,y,t)\cdot g(x,y+h/2,t).$$

**命题 2.1（双线性二阶一致性）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内实解析。对充分小的 $h>0$，有

$$\begin{aligned}
\frac{\mathcal B_h^++\mathcal B_h^-}{2}&=B_af\cdot g+O_K(h^2),\\
\frac{\mathcal B_h^+-\mathcal B_h^-}{h}&=B_af\cdot g_y+2D_xf\cdot g+O_K(h^2).
\end{aligned}\tag{6}$$

**证明。** 固定 $(x,y,t)$，令

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t)
=B_af\cdot g(y+s)+2sD_xf\cdot g(y+s).$$

在此记法中，第一因子的 $y$ 坐标固定。因而

$$\begin{aligned}
\Phi(0)&=B_af\cdot g,\\
\Phi'(0)&=B_af\cdot g_y+2D_xf\cdot g,\\
\Phi''(0)&=B_af\cdot g_{yy}+4D_xf\cdot g_y,\\
\Phi^{(3)}(0)&=B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}.
\end{aligned}$$

由 $\mathcal B_h^\pm=\Phi(\pm h/2)$ 的对称 Taylor 展开，得到

$$\begin{aligned}
\frac{\mathcal B_h^++\mathcal B_h^-}{2}
&=B_af\cdot g+\frac{h^2}{8}
\left(B_af\cdot g_{yy}+4D_xf\cdot g_y\right)+O_K(h^4),\\
\frac{\mathcal B_h^+-\mathcal B_h^-}{h}
&=B_af\cdot g_y+2D_xf\cdot g
+\frac{h^2}{24}\left(B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}\right)+O_K(h^4).
\end{aligned}$$

解析函数的各阶导数在适当的紧邻域上有界，故余项在 $K$ 上一致。保留主项即得（6）。□

## 3　Gram τ 函数与孤子展开

固定有限整数 $N\ge1$，取实谱参数 $p_i,q_i,\rho_i$。记 $d=h/2$，定义

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad
\chi_i=\lambda_h(p_i-a)\lambda_h(q_i+a),\qquad
\gamma_i=-\frac{p_i-a+d}{q_i+a-d},\tag{7}$$

$$E_i(j,x,t)=\frac{\rho_i}{p_i+q_i}\chi_i^j
 e^{(p_i+q_i)x+(q_i^2-p_i^2)t},\qquad
A_{ik}=\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)}.\tag{8}$$

假设对所有 $i,k$，有

$$p_i+q_k\ne0,\qquad p_i-a\pm d\ne0,\qquad q_k+a\pm d\ne0.$$

引入辅助层 $n$ 和参数 $s$，定义 Gram 行列式

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{9}$$

其中 $\delta_{ik}$ 为 Kronecker 符号。$N$ 表示行列式阶数，$n$ 表示辅助层编号。取

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{10}$$

$\tau_0$ 与 $s$ 无关。对于一般辅助层，要求 $q_k+s\ne0$；涉及负整数层时，还要求 $p_i-s\ne0$。

**命题 3.1（Cauchy 主子式展开）。** 式（10）的 τ 函数具有（12）所示的有限子集展开。

**证明。** 将（9）的矩阵写为 $I+K$，则

$$\det(I+K)=\sum_{I\subseteq\{1,\ldots,N\}}\det K[I,I].$$

每个主子式中的行、列因子可分别提出，余下的 Cauchy 行列式为

$$\det\left[\frac1{p_i+q_k}\right]_{i,k\in I}
=\frac{\prod_{i<k\atop i,k\in I}(p_k-p_i)(q_k-q_i)}
{\prod_{i,k\in I}(p_i+q_k)}.\tag{11}$$

从分母中提出 $\prod_{i\in I}(p_i+q_i)$，并按每对指标 $i<k$ 合并其余因子，得到

$$\det K[I,I]
=\left(\prod_{i\in I}\gamma_i(s)^nE_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\qquad
\gamma_i(s)=-\frac{p_i-s}{q_i+s}.$$

分别取 $n=0$ 和 $n=1,\ s=a-d$，即得

$$\boxed{\begin{aligned}
G_j&=\sum_{I\subseteq\{1,\ldots,N\}}
\left(\prod_{i\in I}E_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\\
F_j&=\sum_{I\subseteq\{1,\ldots,N\}}
\left(\prod_{i\in I}\gamma_iE_i\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right).
\end{aligned}}\tag{12}$$

空乘积取 $1$。□

格点平移 $G_j\mapsto G_{j+1}$ 对应于每个 $E_i\mapsto\chi_iE_i$。例如，$N=1$ 时 $G_j=1+E_1$、$F_j=1+\gamma_1E_1$；$N=2$ 时

$$G_j=1+E_1+E_2+A_{12}E_1E_2,\qquad
F_j=1+\gamma_1E_1+\gamma_2E_2+A_{12}\gamma_1\gamma_2E_1E_2.$$

一般 $N$ 的相互作用同样由成对因子 $A_{ik}$ 给出，且这些因子与 $h$ 无关。

## 4　Gram 解的双线性恒等式

相邻辅助层之间的秩一更新给出任意有限阶行列式所满足的双线性链。

**引理 4.1（相邻层恒等式）。** 固定 $j\in\mathbb Z$、$s\in\mathbb R$ 和 $n\in\mathbb Z$。设（9）中的分母、格点乘子以及 $p_i-s$ 均非零，则

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{13}$$

**证明。** 将第 $n$ 层矩阵写为 $M_{ik}=\delta_{ik}+r_ic_k/(p_i+q_k)$，其中

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{14}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义有

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{15}$$

最后一个关系来自

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.$$

在 $M$ 可逆处，记

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{16}$$

矩阵行列式引理给出最后一式，Jacobi 微分公式给出 $\kappa=\tau_{n,x}/\tau_n$。再记

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{17}$$

由 $H_x=-HM_xH$、$H_t=-HM_tH$ 及（15），逐项求导得

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{18}$$

例如，$z_x=HPr-\kappa z$，故

$$\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z),$$

即（18）的第二式。对该式再求一次 $x$ 导数，并代入其余三式，得到

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{19}$$

因此 $\psi=1-\zeta$ 满足

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{20}$$

对任意 $f=\psi g$，展开双线性算子可得

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{21}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，由（20）得到（13）。

为将恒等式延伸至奇异矩阵，将所有 $\rho_i$ 同时替换为 $\varepsilon\rho_i$。在任一固定的 $(x,t)$ 处，$\varepsilon=0$ 时 $M=I$，上述计算在 $\varepsilon=0$ 的邻域内成立。双线性残差关于 $\varepsilon$ 为多项式，故恒等于零。令 $\varepsilon=1$，即得所有 $(x,t)$ 处的结论。□

**定理 4.2（任意有限阶 Gram 精确解）。** 设 $N\ge1$ 有限，$h>0$，实谱参数满足第 3 节的非零条件。由（9）、（10）定义的 $F_j,G_j$ 对所有 $x,t\in\mathbb R$ 和 $j\in\mathbb Z$ 满足（5）。

**证明。** 在（13）中取 $n=0$、$s=a-d$，得到（5）的第一条方程。对于第二条，逐矩阵元有

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{22}$$

因而

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{23}$$

在（13）中取 $n=0$、$s=a+d$，并以 $j+1$ 代替 $j$，得到

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{24}$$

这就是（5）的第二条方程。□

## 5　正 τ 函数与非线性物理场

### 5.1　Gram τ 函数的正性

**命题 5.1（正则谱域）。** 设

$$h>0,\qquad 0<p_1<\cdots<p_N<a-h/2,\qquad
0<q_1<\cdots<q_N,\qquad \rho_i>0.$$

则由（10）定义的 $F_j,G_j$ 满足 $F_j\ge1$、$G_j\ge1$，并关于 $(x,t)$ 联合实解析。

**证明。** 上述条件蕴含 $a>h/2$、$p_i-a<-h/2$ 及 $q_i+a>h/2$。因此格点乘子均为正，且 $\gamma_i>0$、$E_i>0$。有序的 $p_i,q_i$ 又给出 $A_{ik}>0$（$i<k$）。式（12）的每一项均为正，空集项为 $1$，故 $F_j,G_j\ge1$。实解析性由有限指数和直接得到。□

### 5.2　物理变量重构与势的消去

记格点差分和平均算子为

$$\delta_-z_j=\frac{z_j-z_{j-1}}h,\qquad
\delta_0z_j=\frac{z_{j+1}-z_{j-1}}{2h},\qquad
M_-z_j=\frac{z_j+z_{j-1}}2,\qquad
\Delta_hz_j=\frac{z_{j+1}-2z_j+z_{j-1}}{h^2}.$$

对严格正的 $F_j,G_j$，定义

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
\omega_j=\partial_x\log\frac{G_{j+1}}{G_j},\qquad
v_j=\frac4h\omega_j+\delta_0u_j.$$

物理场 $u_j,v_j$ 均位于半格点 $y=(j+\tfrac12)h$。

**定理 5.2（非线性半离散 DLW 系统）。** 设 $h>0$，各 $F_j,G_j$ 关于 $(x,t)$ 联合实解析、严格为正，并满足（5）。则上述重构得到的 $u_j,v_j$ 满足（31）。特别地，命题 5.1 的谱域给出该系统的全局正则 Gram 解。

**证明。** 令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。由恒等式

$$\frac{B_sf\cdot g}{fg}
=(\log f+\log g)_{xx}+(\log f-\log g)_x^2
+(\log f-\log g)_t+2s(\log f-\log g)_x,\tag{25}$$

将（5）除以相应的 τ 函数乘积，得到

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{26}$$

由定义，

$$u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,\qquad
\omega_j=(\beta_{j+1}-\beta_j)_x.\tag{27}$$

两侧对数差的 $x$ 导数分别为 $(u_j+\omega_j)/2$ 和 $(u_j-\omega_j)/2$。再记

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{28}$$

将（26）相加、相减，并对 $x$ 求导，有

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{29}$$

式（27）、（28）给出

$$\delta_-Z_j=\delta_-u_j+\frac4hM_-\omega_j.$$

对（29）的第一条施加 $\delta_-$，即可消去 $Z_j$，得到闭合系统

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4hM_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{30}$$

令 $W_j=v_j-\delta_0u_j=(4/h)\omega_j$，并记

$$\mathcal A_j=\frac{u_j^2}{2}+2au_j
+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).$$

利用精确差分恒等式

$$\delta_- -M_-\delta_0=-\frac{h^2}{4}\Delta_h\delta_-,\qquad
M_+\delta_-=\delta_0,\qquad M_+M_-=1+\frac{h^2}{4}\Delta_h,$$

其中 $M_+z_j=(z_{j+1}+z_j)/2$，式（30）的第一条化为下式第一条。将该方程施加 $M_+$，再与乘以 $4/h$ 的 $\omega_j$ 方程相加，得到下式第二条：

$$\boxed{\begin{aligned}
0={}&\delta_-u_{j,t}
+\partial_x\delta_-\!\left[\frac{u_j^2}{2}+2au_j
+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right]\\
&+\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_h\delta_-u_j\right),\\[2pt]
0={}&v_{j,t}+\partial_x\!\left[
\delta_0\!\left(\frac{u_j^2}{2}+2au_j
+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right)
+(u_j+2a)W_j-4u_j\right]\\
&+\partial_x^2\left[\delta_0u_j+\frac{h^2}{4}\Delta_hW_j\right],
\qquad W_j=v_j-\delta_0u_j.
\end{aligned}}\tag{31}$$

同一差分恒等式也允许从（31）恢复（30）：从第二条减去第一条的 $M_+$ 平均，即得 $W_j$ 的方程。因此，在上述变量替换下，（30）与（31）等价。□

## 6　二阶一致性与精确解族的连续极限

### 6.1　非线性方程的一致性

记（1）的左端为 $\mathcal C_1[u,v]$、$\mathcal C_2[u,v]$，（31）的左端为 $\mathcal N_{1,h}[u,v]$、$\mathcal N_{2,h}[u,v]$。

**命题 6.1（非线性二阶一致性）。** 设 $u(x,y,t),v(x,y,t)$ 在紧集 $K$ 的某个开邻域内实解析。按

$$u_j=u(x,y+jh,t),\qquad v_j=v(x,y+jh,t)$$

采样。对充分小的 $h>0$，在 $j=0$ 处有

$$\begin{aligned}
\mathcal N_{1,h}[u,v](0,x,t)
&=\mathcal C_1[u,v](x,y-h/2,t)+O_K(h^2),\\
\mathcal N_{2,h}[u,v](0,x,t)
&=\mathcal C_2[u,v](x,y,t)+O_K(h^2).
\end{aligned}\tag{32}$$

在原交错网格上，第一条方程以整数格点为中心，第二条方程以半格点为中心。

**证明。** 令 $m=y-h/2$。对任一解析场 $z$，对称 Taylor 展开给出

$$\begin{aligned}
\delta_-z_0&=z_y(x,m,t)+\frac{h^2}{24}z_{yyy}(x,m,t)+O_K(h^4),\\
M_-z_0&=z(x,m,t)+\frac{h^2}{8}z_{yy}(x,m,t)+O_K(h^4),\\
\delta_0z_0&=z_y(x,y,t)+\frac{h^2}{6}z_{yyy}(x,y,t)+O_K(h^4),\\
\Delta_hz_0&=z_{yy}(x,y,t)+\frac{h^2}{12}z_{yyyy}(x,y,t)+O_K(h^4).
\end{aligned}$$

这些展开也适用于所需的 $x,t$ 导数。令 $\mathcal A_0^{(0)}=u^2/2+2au$，则

$$W_0=v-u_y+O_K(h^2),\qquad
\mathcal A_0=\mathcal A_0^{(0)}+O_K(h^2),$$

且所需的有限阶导数具有相同阶的误差。由（31）的第一条，

$$\mathcal N_{1,h}
=u_{yt}(x,m,t)+\partial_x\partial_y\left(\frac{u^2}{2}+2au\right)(x,m,t)
+v_{xx}(x,m,t)+O_K(h^2),$$

即（32）的第一式。第二条中的通量满足

$$\delta_0\mathcal A_0+(u+2a)W_0-4u
=(u+2a)u_y+(u+2a)(v-u_y)-4u+O_K(h^2)
=(u+2a)v-4u+O_K(h^2).$$

同时，$\partial_x^2\delta_0u_0=u_{xxy}+O_K(h^2)$，而含 $h^2\Delta_hW_0$ 的项为 $O_K(h^2)$。合并即得第二式。各余项由紧邻域内的导数界一致控制。□

### 6.2　物理变量重构的一致性

对于连续正 τ 函数 $f,g$，在物理位置 $y$ 定义交错重构

$$\begin{aligned}
u^{[h]}(x,y,t)
&=\partial_x\left[2\log f(x,y,t)-\log g(x,y-h/2,t)-\log g(x,y+h/2,t)\right],\\
\omega^{[h]}(x,y,t)
&=\partial_x\left[\log g(x,y+h/2,t)-\log g(x,y-h/2,t)\right],\\
v^{[h]}(x,y,t)
&=\frac4h\omega^{[h]}(x,y,t)
+\frac{u^{[h]}(x,y+h,t)-u^{[h]}(x,y-h,t)}{2h}.
\end{aligned}$$

**命题 6.2（重构的二阶精度）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内严格为正且实解析。则

$$u^{[h]}=2\left(\log\frac fg\right)_x+O_K(h^2),\qquad
v^{[h]}=2\bigl(\log(fg)\bigr)_{xy}+O_K(h^2).\tag{33}$$

**证明。** 令 $\alpha=\log f$、$\beta=\log g$、$u=2(\alpha-\beta)_x$。对 $\beta_x$ 的左右半格点值作对称展开，有

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad
\frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).$$

第一式及其 $y$ 导数的展开给出

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2).$$

故 $v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2)$，得到（33）。□

### 6.3　固定谱参数的 Gram 解族

固定 $N$ 及谱参数，设存在 $h_0>0$，使

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad
0<q_1<\cdots<q_N,\qquad \rho_i>0.$$

对于 $0<h\le h_0$，所有格点乘子均为正。将（9）中的整数幂以正实指数延伸到实数格点编号，定义

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad
f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).$$

因此，$g^{(h)}(x,jh,t)=G_j$，$f^{(h)}(x,(j+\tfrac12)h,t)=F_j$。将这对函数代入第 6.2 节的交错重构，记所得物理场为 $u^{(h)},v^{(h)}$。

定义连续 Gram τ 函数

$$\tau_n^{(0)}(x,y,t)=\det\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-a}{q_k+a}\right)^n
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t
+y((p_i-a)^{-1}+(q_k+a)^{-1})}
\right]_{1\le i,k\le N}.\tag{34}$$

令 $f^{(0)}=\tau_1^{(0)}$、$g^{(0)}=\tau_0^{(0)}$，并由（2）定义 $u^{(0)},v^{(0)}$。

**定理 6.3（精确 Gram 解族的一致二阶极限）。** 在上述固定谱参数条件下，$f^{(0)},g^{(0)}$ 严格为正并满足连续双线性对（3），从而 $u^{(0)},v^{(0)}$ 是（1）的正则解。对任意 $R>0$，存在 $C_R\ge0$ 和 $0<\varepsilon_R\le h_0$，使 $0<h<\varepsilon_R$ 时

$$\sup_{|x|,|y|,|t|\le R}
\left(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\right)
\le C_Rh^2.\tag{35}$$

**证明。** 记 $z_i=p_i-a<0$、$w_i=q_i+a>0$。由固定谱条件，$|z_i|,w_i>h_0/2$。对充分小的 $h$，

$$\frac1h\log\lambda_h(z)
=\frac1z+\frac{h^2}{12z^3}+O(h^4),$$

故第 $i$ 个指数项的 $y$ 相位系数为

$$k_i^{(h)}=\frac1h\log\chi_i
=\frac1{z_i}+\frac1{w_i}
+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_i^3}\right)+O(h^4).$$

对于 $f^{(h)}$，半格移位将（12）中的振幅 $\gamma_i$ 替换为

$$\widetilde\gamma_i^{(h)}=\gamma_i\chi_i^{-1/2}
=-\frac{z_i}{w_i}
\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_i^2)}}
=-\frac{z_i}{w_i}+O(h^2).$$

这个精确公式表明，半格移位后的振幅是 $h$ 的偶函数。于是（12）给出

$$\begin{aligned}
g^{(h)}&=\sum_I\left(\prod_{i\in I}\mathcal E_i^{(h)}\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\\
f^{(h)}&=\sum_I\left(\prod_{i\in I}\widetilde\gamma_i^{(h)}\mathcal E_i^{(h)}\right)
\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\\
\mathcal E_i^{(h)}&=\frac{\rho_i}{p_i+q_i}
 e^{(p_i+q_i)x+(q_i^2-p_i^2)t+yk_i^{(h)}}.
\end{aligned}$$

将 $k_i^{(h)}$、$\widetilde\gamma_i^{(h)}$ 分别替换为 $z_i^{-1}+w_i^{-1}$、$-z_i/w_i$，恰得（34）的 $g^{(0)},f^{(0)}$ 的主子式展开。各展开项为正，因而四个 τ 函数均不小于 $1$。

有限子集和以及上述相位、振幅展开进一步给出：对任意固定多重指标 $\nu$ 及任意紧集 $K$，

$$\partial^\nu f^{(h)}-\partial^\nu f^{(0)}=O_K(h^2),\qquad
\partial^\nu g^{(h)}-\partial^\nu g^{(0)}=O_K(h^2).$$

这里 $\partial^\nu$ 为关于 $(x,y,t)$ 的混合导数。由于 τ 函数有共同的正下界，同样的结论适用于所需的对数导数，且这些导数在适当的紧邻域内一致有界。

引理 4.1 的矩阵计算对正实指数插值同样成立，式（22）也保持不变。因此，对任意实数 $y$，有

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad
B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.$$

对这两式作命题 2.1 的对称展开。上述导数界保证展开余项对该解族一致，故令 $h\to0$ 得到

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad
B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.$$

由第 1 节的恒等式，这就是（3）；命题 1.1 随即给出连续 DLW 解。

最后，将命题 6.2 的对称展开用于 $f^{(h)},g^{(h)}$。其余项由解族的共同导数界控制，因而

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad
v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).$$

再用对数导数的一致二阶收敛，在 $K=\{(x,y,t):|x|,|y|,|t|\le R\}$ 上即得（35）。□

## 附录　Q、R、M 的势表示

设 $F_j,G_j$ 满足定理 5.2 的条件，沿用 $\alpha_j,\beta_j,u_j,\omega_j$ 的记号。保留整数格点上的辅助势 $M_j=\beta_{j,x}$，则

$$\omega_j=M_{j+1}-M_j,\qquad
Z_j=u_j+2(M_j+M_{j+1}).\tag{36}$$

代入（29），得到

$$\begin{aligned}
0={}&u_{j,t}+\partial_x\!\left[
u_{j,x}+\frac{u_j^2}{2}+2au_j
+2(M_j+M_{j+1})_x+\frac{\omega_j^2}{2}-h\omega_j\right],\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x[(u_j+2a)\omega_j-hu_j],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{37}$$

定义半格点上的中心比值

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{38}$$

于是

$$u_{j,t}=2\partial_x\!\left(\frac{Q_{j,t}}{Q_j}\right),\qquad
u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{39}$$

式（37）的第一条化为

$$\partial_x\!\left[
\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}
+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j
\right]=0.\tag{40}$$

由（26）、（38），括号内恰为 $(A_j+C_j)/2$，故其值为零。结合 $\omega_j$ 的方程，有

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j\right]Q_j,\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x\!\left[2a\omega_j
+2\frac{Q_{j,x}}{Q_j}(\omega_j-h)\right],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{41}$$

再定义

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad
\omega_j=h(1-Q_jR_j),\qquad
\frac{M_{j+1}-M_j}{h}+Q_jR_j=1.\tag{42}$$

由于 $Q_j>0$，该定义处处成立。所需的乘积关系为

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{43}$$

代入（41），得到

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
0={}&(Q_jR_j)_t-(Q_jR_j)_{xx}
+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x.
\end{aligned}\tag{44}$$

由恒等式

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{45}$$

第二条方程可写为

$$R_j(Q_{j,t}+Q_{j,xx}+2aQ_{j,x})
+Q_j(R_{j,t}-R_{j,xx}+2aR_{j,x})=0.\tag{46}$$

利用（44）的第一条，得到势表示

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{47}$$

其中 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。物理场由下式恢复：

$$\boxed{\begin{aligned}
u_j&=2\frac{Q_{j,x}}{Q_j},\qquad
\omega_j=h(1-Q_jR_j)=M_{j+1}-M_j,\\
v_j&=4(1-Q_jR_j)+\frac{u_{j+1}-u_{j-1}}{2h}.
\end{aligned}}\tag{48}$$

## 参考文献

[1] H.-H. Sheng and G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. *Physica D: Nonlinear Phenomena*, 432 (2022), 133140.
