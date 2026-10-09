# （2+1）维 DLW 方程的半离散化、Lax 表示与数值模拟

<div class="abstract"><span class="abstract-label">摘要</span> 本文研究（2+1）维色散长波（DLW）方程的半离散化及其数值计算。通过离散连续双线性方程中的一个空间变量，构造交错格点半离散系统，并给出任意有限阶的 Gram 行列式解。利用相邻辅助层之间的秩一关系，证明所构造的 τ 函数满足半离散双线性方程。对辅助势分别采用格点差分消元和势函数变换，得到差分消势形式（potential-elimination formulation，PE）与势函数形式（potential formulation，PF），并建立相应的 Darboux–Lax 表示。在正则谱参数条件下，证明半离散方程的二阶一致性及精确解族在紧集上的二阶连续极限。进一步采用三点中心差分离散其余空间导数，结合 Euler、RK4 和 Crank–Nicolson 方法进行单孤子与二孤子数值模拟。通过与解析解及直接差分方法比较，考察两种非线性形式的误差以及网格移动对计算精度的影响。</div>

**关键词：** 色散长波方程；可积半离散化；Gram 行列式；Lax 对；连续极限；数值模拟

## 引言

Hirota 双线性方法为构造非线性可积方程的行列式解及其离散形式提供了有效途径。Sheng 和 Yu [1] 利用双线性方法与 KP 层级约化，给出了（2+1）维 DLW 系统的孤子、呼吸子和有理解。其 τ 函数具有 Gram 行列式结构，相应非线性解由 τ 函数的对数导数给出。本文以该双线性表示为基础，研究 DLW 系统的半离散化。

可积半离散方程也可用于构造数值方法。Feng、Sheng 和 Yu [2] 对广义 sine–Gordon 方程构造了两种可积半离散形式，并将其用于自适应动网格计算。对于（2+1）维 DLW 系统，沿一个空间方向离散后，方程仍含另一空间方向的连续导数。因此，其数值计算还需对保留的空间导数进行离散，并考察这一步离散对不同非线性表示的影响。离散方程的线性问题及其与势变量的关系，可参见二维 Toda 的直接线性化研究 [3] 和修正色散长波方程的 Darboux 变换研究 [4]。

本文沿 $y$ 方向引入交错格点，构造两条半离散双线性方程。所构造系统具有任意有限阶的 Gram 行列式解，其双线性恒等式由秩一更新直接证明。在非线性化过程中，对同一辅助势 $Z_j$ 采用两种处理：通过格点差分消去该势，得到 PE 形式；引入势变量 $Q,R,M$ 表示该势，得到 PF 形式。两种形式由同一 τ 函数解产生相同的物理场。进一步给出相应的 Lax 表示，并在固定谱参数下证明精确半离散解族以二阶精度趋于连续 DLW 解。

本文的安排如下。第 1、2 节介绍连续双线性表示及其半离散化。第 3、4 节给出 Gram 行列式解并证明其双线性恒等式。第 5、6 节推导 PE 和 PF 两种非线性形式，第 7 节讨论连续极限，第 8 节给出 Lax 对及相容性证明。第 9 节比较两种形式与直接差分方法的数值结果，第 10 节给出结论。

连续变量记为 $(x,y,t)$，格点编号为 $j\in\mathbb Z$，格距为 $h>0$，参数 $a\in\mathbb R$ 固定。采用文献 [1] 中 $\lambda=-2$ 的 DLW 归一化。各命题所涉及的函数在指定区域内假设为实解析函数；对数及平方根取正实分支。记号 $O_K(h^m)$ 表示在紧集 $K$ 上一致有界的 $m$ 阶余项，其常数可依赖固定的函数和谱数据。

## 1　连续 DLW 方程的双线性表示

考虑（2+1）维 DLW 系统

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

引入因变量变换，其中 τ 函数 $f(x,y,t),g(x,y,t)$ 严格为正：

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

Hirota 算子定义为

$$D_x^rD_y^sD_t^m f\cdot g
=\left.(\partial_x-\partial_{x'})^r(\partial_y-\partial_{y'})^s
(\partial_t-\partial_{t'})^m
f(x,y,t)g(x',y',t')\right|_{(x',y',t')=(x,y,t)}.$$

记 $B_s=D_x^2+D_t+2sD_x$。与上述变换对应的双线性方程为

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

令 $G_j$ 和 $F_j$ 分别定义在格点 $y=jh$ 和 $y=(j+\tfrac12)h$ 上。考虑如下半离散双线性方程：

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{5}$$

为考察式（5）的连续极限，在固定坐标 $y$ 处记

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

对 $s$ 求导时保持第一因子不变，得到

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

解析函数的各阶导数在适当的紧邻域上有界，故余项在 $K$ 上一致。从而得到估计（6）。□

## 3　Gram 行列式解

设 $N\ge1$ 为整数，$p_i,q_i,\rho_i$ 为实参数。记 $d=h/2$，并定义

$$\lambda_h(z)=\frac{z+d}{z-d}.\tag{7}$$

假设对所有 $i,k$，有

$$p_i+q_k\ne0,\qquad p_i-a\pm d\ne0,\qquad q_k+a\pm d\ne0.$$

引入辅助层 $n$ 和参数 $s$，定义 Gram 行列式

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-s}{q_k+s}\right)^n
\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t}
\right].\tag{8}$$

其中 $\delta_{ik}$ 为 Kronecker 符号，$N$ 为行列式阶数，$n$ 为辅助层指标。令

$$\boxed{F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j).}\tag{9}$$

$\tau_0$ 与 $s$ 无关。对于一般辅助层，要求 $q_k+s\ne0$；涉及负整数层时，还要求 $p_i-s\ne0$。

## 4　Gram 解的双线性恒等式

本节证明式（9）满足半离散双线性方程（5）。首先建立相邻辅助层之间的双线性恒等式。

**引理 4.1（相邻层恒等式）。** 固定 $j\in\mathbb Z$、$s\in\mathbb R$ 和 $n\in\mathbb Z$。设（8）中的分母、格点乘子以及 $p_i-s$ 均非零，则

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.}\tag{10}$$

**证明。** 将第 $n$ 层矩阵写为 $M_{ik}=\delta_{ik}+r_ic_k/(p_i+q_k)$，其中

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad
c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}.\tag{11}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义有

$$\begin{gathered}
r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\
M_x=rc^{\mathsf T},\qquad
M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\qquad
M_{n+1}=M-rb^{\mathsf T}.
\end{gathered}\tag{12}$$

最后一式由下列恒等式得到：

$$-\frac{p_i-s}{q_k+s}-1=-\frac{p_i+q_k}{q_k+s}.$$

在 $M$ 可逆处，记

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad
\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta.\tag{13}$$

式（13）的最后一式由矩阵行列式引理得到。由 Jacobi 微分公式，有 $\kappa=\tau_{n,x}/\tau_n$。再令

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad
\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r.\tag{14}$$

由 $H_x=-HM_xH$、$H_t=-HM_tH$ 及（12），逐项求导得

$$\begin{aligned}
\kappa_x&=\mu+\nu-\kappa^2,\\
\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\
(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\
\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.
\end{aligned}\tag{15}$$

例如，$z_x=HPr-\kappa z$，故

$$\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z),$$

即（15）的第二式。对该式再求一次 $x$ 导数，并代入其余三式，得到

$$\begin{aligned}
\zeta_{xx}+\zeta_t+2s\zeta_x
&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x
-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\
&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\
&=2\kappa_x(1-\zeta).
\end{aligned}\tag{16}$$

因此 $\psi=1-\zeta$ 满足

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0.\tag{17}$$

对任意 $f=\psi g$，展开双线性算子可得

$$\frac{B_sf\cdot g}{g^2}
=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi.\tag{18}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，由（17）得到（10）。

为将恒等式延伸至奇异矩阵，将所有 $\rho_i$ 同时替换为 $\varepsilon\rho_i$。在任一固定的 $(x,t)$ 处，$\varepsilon=0$ 时 $M=I$，上述计算在 $\varepsilon=0$ 的邻域内成立。双线性残差关于 $\varepsilon$ 为多项式，故恒等于零。令 $\varepsilon=1$，即得所有 $(x,t)$ 处的结论。□

**定理 4.2（任意有限阶 Gram 精确解）。** 设 $N\ge1$ 有限，$h>0$，实谱参数满足第 3 节的非零条件。由（8）、（9）定义的 $F_j,G_j$ 对所有 $x,t\in\mathbb R$ 和 $j\in\mathbb Z$ 满足（5）。

**证明。** 在（10）中取 $n=0$、$s=a-d$，得到（5）的第一条方程。对于第二条，逐矩阵元有

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)
=-\frac{p_i-a+d}{q_k+a-d}.\tag{19}$$

因而

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j.\tag{20}$$

在（10）中取 $n=0$、$s=a+d$，并以 $j+1$ 代替 $j$，得到

$$B_{a+d}F_j\cdot G_{j+1}
=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0.\tag{21}$$

即得式（5）的第二式。□

## 5　正则性与 PE 形式

### 5.1　解的正则性

为使对数变换处处有定义，先给出保证 τ 函数严格为正的一组充分条件。

**命题 5.1（正则谱域）。** 设

$$h>0,\qquad 0<p_1<\cdots<p_N<a-h/2,\qquad
0<q_1<\cdots<q_N,\qquad \rho_i>0.$$

则由（9）定义的 $F_j,G_j$ 满足 $F_j\ge1$、$G_j\ge1$，并关于 $(x,t)$ 联合实解析。

**证明。** 在上述参数条件下，式（8）中 $n=0$ 和 $n=1,s=a-h/2$ 对应的矩阵均可写为 $I+D_1CD_2$，其中 $D_1,D_2$ 为正对角矩阵，$C_{ik}=1/(p_i+q_k)$。有序正参数下的 Cauchy 矩阵 $C$ 严格全正，正对角缩放保持这一性质，故 $\det(I+D_1CD_2)\ge1$。因此 $F_j,G_j\ge1$。矩阵元关于 $(x,t)$ 实解析，其行列式亦实解析。□

### 5.2　PE 形式的推导

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

**定理 5.2（非线性半离散 DLW 系统）。** 设 $h>0$，各 $F_j,G_j$ 关于 $(x,t)$ 联合实解析、严格为正，并满足（5）。则上述重构得到的 $u_j,v_j$ 满足（28）。特别地，命题 5.1 的谱域给出该系统的全局正则 Gram 解。

**证明。** 令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。由恒等式

$$\frac{B_sf\cdot g}{fg}
=(\log f+\log g)_{xx}+(\log f-\log g)_x^2
+(\log f-\log g)_t+2s(\log f-\log g)_x,\tag{22}$$

将（5）除以相应的 τ 函数乘积，得到

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2
+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2
+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{23}$$

由定义，

$$u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,\qquad
\omega_j=(\beta_{j+1}-\beta_j)_x.\tag{24}$$

两侧对数差的 $x$ 导数分别为 $(u_j+\omega_j)/2$ 和 $(u_j-\omega_j)/2$。再记

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{25}$$

将（23）相加、相减，并对 $x$ 求导，有

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{26}$$

为消去式（26）中的辅助势 $Z_j$，由式（24）、（25）可得

$$\delta_-Z_j=\delta_-u_j+\frac4hM_-\omega_j.$$

对式（26）的第一式作用差分算子 $\delta_-$，并代入上述关系，得到

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4hM_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{27}$$

令 $W_j=v_j-\delta_0u_j=(4/h)\omega_j$，并记

$$\mathcal A_j=\frac{u_j^2}{2}+2au_j
+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).$$

利用精确差分恒等式

$$\delta_- -M_-\delta_0=-\frac{h^2}{4}\Delta_h\delta_-,\qquad
M_+\delta_-=\delta_0,\qquad M_+M_-=1+\frac{h^2}{4}\Delta_h,$$

其中 $M_+z_j=(z_{j+1}+z_j)/2$，式（27）的第一条化为下式第一条。将该方程施加 $M_+$，再与乘以 $4/h$ 的 $\omega_j$ 方程相加，得到下式第二条：

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
\end{aligned}}\tag{28}$$

反之，将式（28）的第二式减去第一式的 $M_+$ 平均，即得 $W_j$ 的演化方程。因此，在上述变量变换下，系统（27）与（28）等价。□

## 6　PF 形式

本节通过引入势函数，将式（26）化为另一种非线性形式。设 $F_j,G_j$ 满足定理 5.2 的条件，并沿用上一节的记号。在整数格点上定义 $M_j=\beta_{j,x}$，则辅助势 $Z_j$ 可表示为

$$\omega_j=M_{j+1}-M_j,\qquad
Z_j=u_j+2(M_j+M_{j+1}).\tag{29}$$

将式（29）代入式（26），得到

$$\begin{aligned}
0={}&u_{j,t}+\partial_x\!\left[
u_{j,x}+\frac{u_j^2}{2}+2au_j
+2(M_j+M_{j+1})_x+\frac{\omega_j^2}{2}-h\omega_j\right],\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x[(u_j+2a)\omega_j-hu_j],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{30}$$

进一步引入因变量变换

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{31}$$

于是

$$u_{j,t}=2\partial_x\!\left(\frac{Q_{j,t}}{Q_j}\right),\qquad
u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{32}$$

式（30）的第一条化为

$$\partial_x\!\left[
\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}
+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j
\right]=0.\tag{33}$$

由（23）、（31），括号内恰为 $(A_j+C_j)/2$，故其值为零。结合 $\omega_j$ 的方程，有

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j\right]Q_j,\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x\!\left[2a\omega_j
+2\frac{Q_{j,x}}{Q_j}(\omega_j-h)\right],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{34}$$

再定义

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad
\omega_j=h(1-Q_jR_j),\qquad
\frac{M_{j+1}-M_j}{h}+Q_jR_j=1.\tag{35}$$

由 $Q_j>0$，上述变换处处有定义。利用关系

$$\frac{Q_{j,x}}{Q_j}(\omega_j-h)=-hQ_{j,x}R_j,\qquad
\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{36}$$

代入（34），得到

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
0={}&(Q_jR_j)_t-(Q_jR_j)_{xx}
+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x.
\end{aligned}\tag{37}$$

由恒等式

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx},\tag{38}$$

第二条方程可写为

$$R_j(Q_{j,t}+Q_{j,xx}+2aQ_{j,x})
+Q_j(R_{j,t}-R_{j,xx}+2aR_{j,x})=0.\tag{39}$$

代入式（37）的第一式，得到 PF 系统

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{40}$$

其中 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。物理场由下式恢复：

$$\boxed{\begin{aligned}
u_j&=2\frac{Q_{j,x}}{Q_j},\qquad
\omega_j=h(1-Q_jR_j)=M_{j+1}-M_j,\\
v_j&=4(1-Q_jR_j)+\frac{u_{j+1}-u_{j-1}}{2h}.
\end{aligned}}\tag{41}$$



**命题 6.1（两种形式的物理场）。** 由同一正 τ 函数对构造 PE 和 PF 时，两种形式恢复的 $u_j,v_j$ 在每个有限格距下完全相同。在定理 7.3 的固定谱条件下，PF 恢复的物理场也满足（45）的一致二阶估计。

**证明。** 由（31），$2Q_{j,x}/Q_j=(2\alpha_j-\beta_j-\beta_{j+1})_x=u_j$；由（35），$4(1-Q_jR_j)=4\omega_j/h$。将二者代入（41），得到 PE 的物理场重构，故两者逐点相同。（45）因而同时适用于两种表示。□


## 7　连续极限

下面分别考察非线性方程、物理变量变换及 Gram 解族的连续极限。所有估计均在固定紧集上进行。

### 7.1　非线性方程的一致性

记（1）的左端为 $\mathcal C_1[u,v]$、$\mathcal C_2[u,v]$，（28）的左端为 $\mathcal N_{1,h}[u,v]$、$\mathcal N_{2,h}[u,v]$。

**命题 7.1（非线性二阶一致性）。** 设 $u(x,y,t),v(x,y,t)$ 在紧集 $K$ 的某个开邻域内实解析。按

$$u_j=u(x,y+jh,t),\qquad v_j=v(x,y+jh,t)$$

采样。对充分小的 $h>0$，在 $j=0$ 处有

$$\begin{aligned}
\mathcal N_{1,h}[u,v](0,x,t)
&=\mathcal C_1[u,v](x,y-h/2,t)+O_K(h^2),\\
\mathcal N_{2,h}[u,v](0,x,t)
&=\mathcal C_2[u,v](x,y,t)+O_K(h^2).
\end{aligned}\tag{42}$$

式（42）的两个展开分别在整数格点和半格点处进行。

**证明。** 令 $m=y-h/2$。对任一解析场 $z$，对称 Taylor 展开给出

$$\begin{aligned}
\delta_-z_0&=z_y(x,m,t)+\frac{h^2}{24}z_{yyy}(x,m,t)+O_K(h^4),\\
M_-z_0&=z(x,m,t)+\frac{h^2}{8}z_{yy}(x,m,t)+O_K(h^4),\\
\delta_0z_0&=z_y(x,y,t)+\frac{h^2}{6}z_{yyy}(x,y,t)+O_K(h^4),\\
\Delta_hz_0&=z_{yy}(x,y,t)+\frac{h^2}{12}z_{yyyy}(x,y,t)+O_K(h^4).
\end{aligned}$$

对相应的 $x,t$ 导数作同样展开。令 $\mathcal A_0^{(0)}=u^2/2+2au$，则

$$W_0=v-u_y+O_K(h^2),\qquad
\mathcal A_0=\mathcal A_0^{(0)}+O_K(h^2),$$

且所需的有限阶导数具有相同阶的误差。由（28）的第一条，

$$\mathcal N_{1,h}
=u_{yt}(x,m,t)+\partial_x\partial_y\left(\frac{u^2}{2}+2au\right)(x,m,t)
+v_{xx}(x,m,t)+O_K(h^2),$$

即（42）的第一式。第二条中的通量满足

$$\delta_0\mathcal A_0+(u+2a)W_0-4u
=(u+2a)u_y+(u+2a)(v-u_y)-4u+O_K(h^2)
=(u+2a)v-4u+O_K(h^2).$$

同时，$\partial_x^2\delta_0u_0=u_{xxy}+O_K(h^2)$，而含 $h^2\Delta_hW_0$ 的项为 $O_K(h^2)$。合并即得第二式。各余项由紧邻域内的导数界一致控制。□

### 7.2　物理变量重构的一致性

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

**命题 7.2（重构的二阶精度）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内严格为正且实解析。则

$$u^{[h]}=2\left(\log\frac fg\right)_x+O_K(h^2),\qquad
v^{[h]}=2\bigl(\log(fg)\bigr)_{xy}+O_K(h^2).\tag{43}$$

**证明。** 令 $\alpha=\log f$、$\beta=\log g$、$u=2(\alpha-\beta)_x$。对 $\beta_x$ 的左右半格点值作对称展开，有

$$u^{[h]}=u-\frac{h^2}{4}\beta_{xyy}+O_K(h^4),\qquad
\frac4h\omega^{[h]}=4\beta_{xy}+\frac{h^2}{6}\beta_{xyyy}+O_K(h^4).$$

第一式及其 $y$ 导数的展开给出

$$\frac{u^{[h]}(y+h)-u^{[h]}(y-h)}{2h}=u_y+O_K(h^2).$$

故 $v^{[h]}=4\beta_{xy}+u_y+O_K(h^2)=2(\alpha+\beta)_{xy}+O_K(h^2)$，得到（43）。□

### 7.3　固定谱参数的 Gram 解族

固定 $N$ 及谱参数，设存在 $h_0>0$，使

$$0<p_1<\cdots<p_N<a-h_0/2,\qquad
0<q_1<\cdots<q_N,\qquad \rho_i>0.$$

对于 $0<h\le h_0$，所有格点乘子均为正。将（8）中的整数幂以正实指数延伸到实数格点编号，定义

$$g^{(h)}(x,y,t)=\tau_0(y/h),\qquad
f^{(h)}(x,y,t)=\tau_1(y/h-1/2;a-h/2).$$

因此，$g^{(h)}(x,jh,t)=G_j$，$f^{(h)}(x,(j+\tfrac12)h,t)=F_j$。将这对函数代入第 7.2 节的交错重构，记所得物理场为 $u^{(h)},v^{(h)}$。

定义连续 Gram τ 函数

$$\tau_n^{(0)}(x,y,t)=\det\!\left[
\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-a}{q_k+a}\right)^n
 e^{(p_i+q_k)x+(q_k^2-p_i^2)t
+y((p_i-a)^{-1}+(q_k+a)^{-1})}
\right]_{1\le i,k\le N}.\tag{44}$$

令 $f^{(0)}=\tau_1^{(0)}$、$g^{(0)}=\tau_0^{(0)}$，并由（2）定义 $u^{(0)},v^{(0)}$。

**定理 7.3（精确 Gram 解族的一致二阶极限）。** 在上述固定谱参数条件下，$f^{(0)},g^{(0)}$ 严格为正并满足连续双线性对（3），从而 $u^{(0)},v^{(0)}$ 是（1）的正则解。对任意 $R>0$，存在 $C_R\ge0$ 和 $0<\varepsilon_R\le h_0$，使 $0<h<\varepsilon_R$ 时

$$\sup_{|x|,|y|,|t|\le R}
\left(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\right)
\le C_Rh^2.\tag{45}$$

**证明。** 记 $z_i=p_i-a<0$、$w_k=q_k+a>0$。由固定谱参数条件，$|z_i|,w_k>h_0/2$。当 $h$ 充分小时，

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4).$$

因此，$g^{(h)}$ 的行列式中第 $(i,k)$ 个指数项的 $y$ 系数为

$$k_{ik}^{(h)}=\frac1h\log\bigl(\lambda_h(z_i)\lambda_h(w_k)\bigr)
=\frac1{z_i}+\frac1{w_k}+\frac{h^2}{12}\left(\frac1{z_i^3}+\frac1{w_k^3}\right)+O(h^4).$$

对 $f^{(h)}$，半格移位后的矩阵元振幅因子为

$$\widetilde\gamma_{ik}^{(h)}
=-\frac{z_i+h/2}{w_k-h/2}\bigl(\lambda_h(z_i)\lambda_h(w_k)\bigr)^{-1/2}
=-\frac{z_i}{w_k}\sqrt{\frac{1-h^2/(4z_i^2)}{1-h^2/(4w_k^2)}}
=-\frac{z_i}{w_k}+O(h^2).$$

将上述相位与振幅代入式（8），各矩阵元在 $h\to0$ 时趋于式（44）中的相应矩阵元，误差为 $O(h^2)$。由于行列式阶数固定，其关于矩阵元的多项式依赖给出：对任意固定多重指标 $\nu$ 及紧集 $K$，

$$\partial^\nu f^{(h)}-\partial^\nu f^{(0)}=O_K(h^2),\qquad
\partial^\nu g^{(h)}-\partial^\nu g^{(0)}=O_K(h^2).$$

这里 $\partial^\nu$ 为关于 $(x,y,t)$ 的混合导数。命题 5.1 的正对角缩放论证同样适用于实数格点插值及其连续极限，故上述四个 τ 函数均不小于 $1$。因此，相应对数导数也满足一致二阶估计，且所需导数在紧邻域内一致有界。

引理 4.1 的矩阵计算对正实指数插值同样成立，式（19）也保持不变。因此，对任意实数 $y$，有

$$B_{a-h/2}f^{(h)}(y)\cdot g^{(h)}(y-h/2)=0,\qquad
B_{a+h/2}f^{(h)}(y)\cdot g^{(h)}(y+h/2)=0.$$

对这两式作命题 2.1 的对称展开。上述导数界保证展开余项对该解族一致，故令 $h\to0$ 得到

$$B_af^{(0)}\cdot g^{(0)}=0,\qquad
B_af^{(0)}\cdot g_y^{(0)}+2D_xf^{(0)}\cdot g^{(0)}=0.$$

由第 1 节的恒等式，上述两式等价于（3）。再由命题 1.1，得到连续 DLW 系统（1）的解。

最后，将命题 7.2 的对称展开用于 $f^{(h)},g^{(h)}$。其余项由解族的共同导数界控制，因而

$$u^{(h)}=2\left(\log\frac{f^{(h)}}{g^{(h)}}\right)_x+O_K(h^2),\qquad
v^{(h)}=2\bigl(\log(f^{(h)}g^{(h)})\bigr)_{xy}+O_K(h^2).$$

再用对数导数的一致二阶收敛，在 $K=\{(x,y,t):|x|,|y|,|t|\le R\}$ 上即得（45）。□


## 8　两种非线性形式的 Lax 表示

### 8.1　变量平移与辅助势

引入变量 $U_j=u_j+2a$、$w_j=W_j-4=4\omega_j/h-4$。PE 系统可写为

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{46}$$

上述变量平移使第一式的通量相差一个与 $x$ 无关的常数。为构造线性问题，引入辅助势 $V_j$，满足

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{47}$$

对第一关系作格点差分，并对第二关系求 $x$ 导数，所得一致性条件正是（46）的第一式。因此先在一个参考格点积分，再沿格点递推，即可为每个光滑解构造 $V$，其自由度为共同的时间函数。以下在局部空间区间及格点链上讨论；$V_j$ 为辅助势，$v_j$ 为第二物理场。

### 8.2　PE 的线性问题及相容性证明

取辅助函数 $\psi_j$，定义

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{48}$$

**定理 8.1（Lax 相容性）。** PE 的每个光滑解连同（47）所确定的势都使（48）在形式算子意义下相容。反之，在 $w_j\ne0$ 的区域内，相容条件与（47）的势差关系共同推出（46）。

**证明。** 置 $\alpha_j=U_j/2+hw_j/8$、$\eta_j=U_j/2-hw_j/8$，并令

$$A_j=\partial_x-\alpha_j,\quad B_j=\partial_x-\eta_j,\quad
T_j=B_j^{-1}A_j,\quad \mathscr Q_j=-\partial_x^2-V_j.\tag{49}$$

$B_j^{-1}$ 在形式伪微分算子代数中定义。相容条件为

$$T_{j,t}=\mathscr Q_{j+1}T_j-T_j\mathscr Q_j.\tag{50}$$

定义残差

$$\begin{aligned}
\mathcal E_j^\alpha&=\alpha_{j,t}+\alpha_{j,xx}+2\alpha_j\alpha_{j,x}+V_{j,x},\\
\mathcal E_j^\eta&=\eta_{j,t}+\eta_{j,xx}+2\eta_j\eta_{j,x}+V_{j+1,x}.
\end{aligned}\tag{51}$$

利用势差关系，直接求得

$$\begin{aligned}
\mathcal E_j^\alpha-\mathcal E_j^\eta&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^\alpha+\mathcal E_j^\eta&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{52}$$

由系统（46）和关系（47），两项残差均为零。另一方面，乘积法则给出 Darboux 恒等式

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{53}$$

分别取 $r=\alpha_j,\eta_j$，共同的中间势为 $V_j+2\alpha_{j,x}=V_{j+1}+2\eta_{j,x}$。两条交织关系代入 $T_{j,t}=(B_j^{-1}A_j)_t$，中间势抵消，即得（50）。

反之，设势 $V_j$ 满足（47）的第二式，且相容条件（50）成立。由恒等式

$$B_j(T_{j,t}-\mathscr Q_{j+1}T_j+T_j\mathscr Q_j)
=-\mathcal E_j^\alpha+\mathcal E_j^\eta T_j\tag{54}$$

结合 $T_j=I-B_j^{-1}hw_j/4$，先比较 $\partial_x^0$ 系数，得 $\mathcal E_j^\alpha=\mathcal E_j^\eta$；再比较 $\partial_x^{-1}$ 系数，得 $w_j\mathcal E_j^\eta=0$。当 $w_j\ne0$ 时，两项残差为零。（52）的差给出第二场方程，其和作后向格点差分后给出第一场方程。□

对于 τ 函数解，取 $V_j=2(\log G_j)_{xx}$，则

$$\alpha_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad
\eta_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{55}$$

代入两条半离散双线性方程可知，相应的 Riccati 残差均为零。因此，τ 函数解满足上述 Darboux–Lax 相容关系。

### 8.3　PF 的 Lax 表示

在 PF 中，$U_j=2Q_{j,x}/Q_j+2a$、$w_j=-4Q_jR_j$，且可取 $V_j=2M_{j,x}$。于是（48）成为

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{56}$$

约束 $M_{j+1}-M_j=h(1-Q_jR_j)$ 的 $x$ 导数恰好给出（47）的势差关系。PF 的两条演化方程则使（51）为零，因而（56）相容。在 $Q_jR_j\ne0$ 时，反向论证恢复 PE 的物理场方程。

## 9　数值方法与数值结果

本节基于 PE 和 PF 两种非线性形式构造数值格式，并与连续 DLW 方程的直接差分格式（FD）比较。以单孤子和二孤子解析解为参照，考察不同时间算法以及固定、动网格下的数值误差。

### 9.1　网格与迭代格式

将 $x\in[-L/2,L/2)$ 等分为 $N_x$ 个区间，取 $x_i=-L/2+i\Delta x$、$\Delta x=L/N_x$。沿 $y$ 方向采用前述交错网格：$M_j$ 位于 $y=jh$，物理场及 $Q_j,R_j$ 位于 $y=(j+\tfrac12)h$。令 $t_n=n\Delta t$，上标 $n$ 表示时间层，下标 $j,i$ 分别表示 $y$、$x$ 方向的网格编号。

对 $x$ 的一、二阶导数分别采用中心差分

$$\begin{aligned}
(D_1z)_{j,i}&=\frac{z_{j,i+1}-z_{j,i-1}}{2\Delta x}\simeq\partial_xz_j(x_i,t),\\
(D_2z)_{j,i}&=\frac{z_{j,i+1}-2z_{j,i}+z_{j,i-1}}{\Delta x^2}\simeq\partial_{xx}z_j(x_i,t).
\end{aligned}\tag{57}$$

$y$ 方向的 $\delta_-,\delta_0,M_-$ 仍表示第 5 节定义的差分与平均。以下先给出固定网格上的 Euler 更新；RK4 和 C–N 使用相同的空间差分，见第 9.3 节。

**PE 格式。** 取 $P=\delta_-u$、$W=v-\delta_0u$ 为演化变量。已知第 $n$ 层的 $P^n,W^n$，先由下侧边界恢复

$$u_{j,i}^n=u_{j_L,i}^n+h\sum_{k=j_L+1}^{j}P_{k,i}^n,\qquad
v_{j,i}^n=W_{j,i}^n+(\delta_0u^n)_{j,i}.\tag{58}$$

其中 $j_L$ 为最下层编号，$u_{j_L,i}^n$ 取解析边界值。由 PE 方程计算 $P,W$ 的时间变化率

$$\begin{aligned}
F_P^n={}&-\delta_-D_1\left[\frac{(u^n)^2}{2}+2au^n
+h^2\left(\frac{(W^n)^2}{32}-\frac{W^n}{4}\right)\right]
-D_2(P^n+M_-W^n),\\
F_W^n={}&-D_1[(u^n+2a)W^n-4u^n]+D_2W^n.
\end{aligned}\tag{59}$$

这里 $F_P^n,F_W^n$ 分别近似 $P_t,W_t$，所有乘积按节点计算。下一时间层为

$$P^{n+1}=P^n+\Delta t\,F_P^n,\qquad
W^{n+1}=W^n+\Delta t\,F_W^n.\tag{60}$$

更新后再由（58）恢复 $u^{n+1},v^{n+1}$。初值取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$。

**PF 格式。** 演化变量为 $Q,R$，物理场由

$$u_j^n=2\frac{D_1Q_j^n}{Q_j^n},\qquad
v_j^n=4(1-Q_j^nR_j^n)+\delta_0u_j^n\tag{61}$$

恢复。为计算 PF 方程中的 $(M_j+M_{j+1})_x$，记 $m_j^n\simeq M_{j,x}(t_n)$、$S_j^n=Q_j^nR_j^n$。对约束 $M_{j+1}-M_j=h(1-QR)$ 作 $x$ 差分，得到

$$m_{j+1}^n=m_j^n-hD_1S_j^n.\tag{62}$$

这一关系使 $m_j^n$ 可由下边界逐层求出。将最下层临时编号为 $0$，由该层的 $Q$ 方程确定起始值

$$m_0^n=-\frac{Q_{0,t}^n+D_2Q_0^n+2aD_1Q_0^n}{2Q_0^n}
-\frac{h^2}{8}\bigl[(S_0^n)^2-1\bigr]+\frac h2D_1S_0^n.\tag{63}$$

其中 $Q_0(t)$ 由解析下边界确定，$Q_{0,t}^n$ 为其时间导数。由（62）得到各层的 $m_j^n$ 后，计算

$$\begin{aligned}
F_{Q,j}^n={}&-D_2Q_j^n-2aD_1Q_j^n
-\left[m_j^n+m_{j+1}^n+\frac{h^2}{4}\bigl((Q_j^nR_j^n)^2-1\bigr)\right]Q_j^n,\\
F_{R,j}^n={}&D_2R_j^n-2aD_1R_j^n
+\left[m_j^n+m_{j+1}^n+\frac{h^2}{4}\bigl((Q_j^nR_j^n)^2-1\bigr)\right]R_j^n,\\
Q_j^{n+1}={}&Q_j^n+\Delta t\,F_{Q,j}^n,\qquad
R_j^{n+1}=R_j^n+\Delta t\,F_{R,j}^n.
\end{aligned}\tag{64}$$

$F_Q,F_R$ 分别为 $Q,R$ 的时间变化率。$Q$ 的最下层取边界值，内部各层 $Q$ 和所有层 $R$ 按（64）更新，再由（61）计算物理场。

初始 $Q$ 由离散关系 $D_1Q_j^0=u_{*,j}(0)Q_j^0/2$ 及归一化 $Q_{j,0}^0=1$ 确定，再取 $R_j^0=[1-(v_{*,j}(0)-\delta_0u_{*,j}(0))/4]/Q_j^0$。这样，PF 与其余格式具有相同的初始物理场。下边界的 $Q_0(t)$ 按同一关系由 $u_{*,0}(t)$ 确定。

**FD 格式。** 直接离散连续 DLW 系统，以 $P=\delta_-u$、$v$ 为演化变量。$u^n$ 仍由（58）的第一式恢复，随后计算

$$\begin{aligned}
F_P^n&=-\delta_-D_1\left[\frac{(u^n)^2}{2}+2au^n\right]-D_2M_-v^n,\\
F_v^n&=-D_1[(u^n+2a)v^n-4u^n]-D_2\delta_0u^n,\\
P^{n+1}&=P^n+\Delta t\,F_P^n,\qquad
v^{n+1}=v^n+\Delta t\,F_v^n.
\end{aligned}\tag{65}$$

此处 $F_P^n,F_v^n$ 分别近似 $P_t,v_t$；例如 $D_2\delta_0u$ 近似连续方程中的 $u_{xxy}$。初值为 $P^0=\delta_-u_*(0)$、$v^0=v_*(0)$。

计算域选在孤子尾部接近背景的位置。PE、FD 的 $x$ 向差分采用周期边界，PF 按 $Q,R$ 的左右端背景值处理边界。沿 $y$ 方向，下侧取解析边界，上侧对数值解与解析背景之差作二次外推。

### 9.2　自适应动网格

文献 [2] 通过离散 hodograph 变换将半离散方程与网格演化联系起来。对于本文的 DLW 系统，网格运动由 PE 方程中的守恒关系确定。令

$$\rho_j=1-\frac{W_j}{4},\qquad
q_j=(u_j+2a)\rho_j-\partial_x\rho_j-2a.
\tag{66}$$

将 $W_j=4(1-\rho_j)$ 代入其演化方程，得到

$$\partial_t\rho_j+\partial_xq_j=0.\tag{67}$$

在 PF 形式中，$\rho_j=Q_jR_j$。由于所有 $y$ 层共用一组 $x$ 节点，对各层取平均作为网格密度和通量：

$$\bar\rho=\frac1{N_y}\sum_j\rho_j,\qquad
\bar q=\frac1{N_y}\sum_jq_j.\tag{68}$$

初始网格按 $\bar\rho(x,0)$ 的累积积分等分，即令相邻节点之间的密度积分相同。密度较大的区域因此分配更多节点。令左端节点 $x_L$ 固定，并保持每个移动节点对应的累积积分不变，利用（67）得

$$\frac{d}{dt}\int_{x_L}^{x_i(t)}\bar\rho(x,t)\,dx
=-\bar q(x_i,t)+\bar q(x_L,t)+\bar\rho(x_i,t)\dot x_i=0.
\tag{69}$$

因此节点速度为

$$\dot x_i=\mathcal V_i
=\frac{\bar q_i-\bar q_0}{\bar\rho_i}.\tag{70}$$

计算时以 $D_1\rho$ 代替通量中的 $\partial_x\rho$，并要求 $\bar\rho>0$。FD 的动网格比较也采用（66）、（68）和（70）确定节点速度。

在均匀计算坐标 $\xi_i=-L/2+i\Delta\xi$ 上写 $x_i(t)=\xi_i+s_i(t)$，令 $J_i=1+D_\xi s_i$。移动节点上的 $x$ 导数由链式法则计算：

$$D_1z_i=\frac{D_\xi z_i}{J_i},\qquad
D_2z_i=\frac{D_{\xi\xi}z_i}{J_i^2}
-\frac{(D_\xi J)_i(D_\xi z)_i}{J_i^3}.\tag{71}$$

$D_\xi,D_{\xi\xi}$ 为（57）在均匀计算坐标上的三点差分。对随节点移动的任一演化变量 $z$，链式法则给出 $\dot z=F_z+\mathcal V D_1z$。因此，在第 9.1 节各时间变化率上加入 $\mathcal V D_1z$，并将节点方程（70）与场变量同步推进。固定网格对应 $s=0,\mathcal V=0$。

### 9.3　时间推进

第 9.1 节的 Euler 格式以当前时间层的变化率更新场变量。为比较不同时间离散，进一步采用经典 RK4 和 Crank–Nicolson（C–N）格式。记全部演化变量为 $z$，其离散变化率为 $\mathcal F(t,z)$；在动网格计算中，$z$ 同时包含节点坐标，$\mathcal F$ 包含上述网格输运项及节点速度。

RK4 在一个时间步内计算四次变化率：

$$\begin{aligned}
k_1&=\mathcal F(t_n,z^n),\\
k_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_1/2),\\
k_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t\,k_2/2),\\
k_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t\,k_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4).
\end{aligned}\tag{72}$$

每一级均根据该级的场变量和网格重新计算差分及边界值。

与文献 [2] 的时间平均处理相同，C–N 取相邻两个时间层变化率的平均：

$$\frac{z^{n+1}-z^n}{\Delta t}
=\frac{\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})}{2}.
\tag{73}$$

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
\qquad f=u,v.\tag{74}$$

**表 1　固定网格、RK4 下三种格式的最大绝对误差。每行最小值加粗。**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">算例</th><th scope="col">场</th><th scope="col">PE</th><th scope="col">PF</th><th scope="col">FD</th></tr></thead>
<tbody>
<tr>
<th rowspan="2" scope="rowgroup">A</th>
<th scope="row">u</th>
<td>1.560308e-03</td>
<td>1.187746e-02</td>
<td><strong>1.161402e-03</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>3.229398e-03</td>
<td>7.254773e-03</td>
<td><strong>3.008503e-03</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">B</th>
<th scope="row">u</th>
<td><strong>6.639277e-05</strong></td>
<td>1.266358e-04</td>
<td>7.809306e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.664598e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.429802e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">C</th>
<th scope="row">u</th>
<td><strong>1.299876e-04</strong></td>
<td>2.620490e-04</td>
<td>1.442262e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.267185e-04</td>
<td>1.405303e-04</td>
<td><strong>1.242170e-04</strong></td>
</tr>
</tbody>
</table></div>

算例 A 中 FD 的两个场误差最小；算例 B 中 PE 的 $u$ 误差和 PF 的 $v$ 误差最小；算例 C 中 PE 的 $u$ 误差和 FD 的 $v$ 误差最小。

**表 2　固定网格上不同时间算法的最大绝对误差。每行最小值加粗。**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">算例</th><th scope="col">格式</th><th scope="col">场</th><th scope="col">Euler</th><th scope="col">RK4</th><th scope="col">C–N</th></tr></thead>
<tbody>
<tr>
<th rowspan="6" scope="rowgroup">A</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td><strong>1.559149e-03</strong></td>
<td>1.560308e-03</td>
<td>1.560309e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.228608e-03</strong></td>
<td>3.229398e-03</td>
<td>3.229404e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td><strong>1.186363e-02</strong></td>
<td>1.187746e-02</td>
<td>1.187746e-02</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>7.210650e-03</strong></td>
<td>7.254773e-03</td>
<td>7.254804e-03</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td><strong>1.160637e-03</strong></td>
<td>1.161402e-03</td>
<td>1.161404e-03</td>
</tr>
<tr>
<th scope="row">v</th>
<td><strong>3.008253e-03</strong></td>
<td>3.008503e-03</td>
<td>3.008508e-03</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">B</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>6.674179e-05</td>
<td><strong>6.639277e-05</strong></td>
<td>6.639418e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.968001e-05</td>
<td><strong>6.664598e-05</strong></td>
<td>6.664697e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>1.302977e-04</td>
<td>1.266358e-04</td>
<td><strong>1.266346e-04</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>8.322184e-05</td>
<td><strong>6.194167e-05</strong></td>
<td>6.194314e-05</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>7.824931e-05</td>
<td><strong>7.809306e-05</strong></td>
<td>7.809446e-05</td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.738482e-05</td>
<td><strong>6.429802e-05</strong></td>
<td>6.429896e-05</td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">C</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>1.306127e-04</td>
<td><strong>1.299876e-04</strong></td>
<td>1.299912e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.332472e-04</td>
<td><strong>1.267185e-04</strong></td>
<td>1.267211e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>2.745545e-04</td>
<td><strong>2.620490e-04</strong></td>
<td>2.620512e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.986149e-04</td>
<td><strong>1.405303e-04</strong></td>
<td>1.405323e-04</td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>1.447371e-04</td>
<td><strong>1.442262e-04</strong></td>
<td>1.442298e-04</td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.300531e-04</td>
<td><strong>1.242170e-04</strong></td>
<td>1.242195e-04</td>
</tr>
</tbody>
</table></div>

在算例 A 中，Euler 的总误差略小于 RK4 和 C–N；在算例 B、C 中，RK4 和 C–N 的误差较小且彼此接近。表中比较采用相同的空间网格与时间步长。

**表 3　固定网格与动网格的最大绝对误差（RK4）。每行最小值加粗。**

<div class="table-wrap"><table class="comparison">
<thead><tr><th scope="col">算例</th><th scope="col">格式</th><th scope="col">场</th><th scope="col">固定网格</th><th scope="col">动网格</th></tr></thead>
<tbody>
<tr>
<th rowspan="6" scope="rowgroup">A</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>1.560308e-03</td>
<td><strong>1.198143e-03</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>3.229398e-03</td>
<td><strong>2.172159e-03</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>1.187746e-02</td>
<td><strong>3.940103e-03</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>7.254773e-03</td>
<td><strong>3.703664e-03</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>1.161402e-03</td>
<td><strong>8.878667e-04</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>3.008503e-03</td>
<td><strong>1.960738e-03</strong></td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">B</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>6.639277e-05</td>
<td><strong>4.533361e-05</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.664598e-05</td>
<td><strong>5.568003e-05</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>1.266358e-04</td>
<td><strong>8.467373e-05</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.194167e-05</td>
<td><strong>4.606240e-05</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>7.809306e-05</td>
<td><strong>5.709006e-05</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>6.429802e-05</td>
<td><strong>5.387754e-05</strong></td>
</tr>
<tr>
<th rowspan="6" scope="rowgroup">C</th>
<th rowspan="2" scope="rowgroup">PE</th>
<th scope="row">u</th>
<td>1.299876e-04</td>
<td><strong>8.193645e-05</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.267185e-04</td>
<td><strong>8.860848e-05</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">PF</th>
<th scope="row">u</th>
<td>2.620490e-04</td>
<td><strong>1.626438e-04</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.405303e-04</td>
<td><strong>8.423511e-05</strong></td>
</tr>
<tr>
<th rowspan="2" scope="rowgroup">FD</th>
<th scope="row">u</th>
<td>1.442262e-04</td>
<td><strong>9.643247e-05</strong></td>
</tr>
<tr>
<th scope="row">v</th>
<td>1.242170e-04</td>
<td><strong>8.548888e-05</strong></td>
</tr>
</tbody>
</table></div>

动网格降低了三个算例中各格式的两个物理场误差，动网格与固定网格的误差比约为 0.332 至 0.838。算例 A 的 PF 格式改进最明显，$u,v$ 的误差分别约为固定网格结果的 0.332 和 0.511。

### 9.5　物理场及误差分布

图 1—6 给出 PF 格式采用 RK4 在固定网格上的数值结果。为展示孤子波形及其相互作用，计算域扩大为 $x\in[-40,40)$、$y\in[-30,30)$，$\Delta x,h,\Delta t,T$ 与前述计算相同。算例 A 展示 $x\in[-3,4],y\in[-3,3]$，算例 B、C 展示 $x,y\in[-30,30]$。每个算例依次给出数值物理场与解析场的对照，以及绝对误差分布。

<figure><img src="../Workspaces/dlw_paper_20261009/figure_1.png" alt="算例A：数值物理场与解析场对照" loading="lazy"><figcaption>图 1　算例 A 的数值物理场与解析场对照。PF，RK4，固定网格，T = 0.01。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figure_2.png" alt="算例A：绝对误差分布" loading="lazy"><figcaption>图 2　算例 A 的绝对误差分布。PF，RK4，固定网格，T = 0.01。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figure_3.png" alt="算例B：数值物理场与解析场对照" loading="lazy"><figcaption>图 3　算例 B 的数值物理场与解析场对照。PF，RK4，固定网格，T = 0.01。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figure_4.png" alt="算例B：绝对误差分布" loading="lazy"><figcaption>图 4　算例 B 的绝对误差分布。PF，RK4，固定网格，T = 0.01。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figure_5.png" alt="算例C：数值物理场与解析场对照" loading="lazy"><figcaption>图 5　算例 C 的数值物理场与解析场对照。PF，RK4，固定网格，T = 0.01。</figcaption></figure>

<figure><img src="../Workspaces/dlw_paper_20261009/figure_6.png" alt="算例C：绝对误差分布" loading="lazy"><figcaption>图 6　算例 C 的绝对误差分布。PF，RK4，固定网格，T = 0.01。</figcaption></figure>


## 10　结论

本文构造了（2+1）维 DLW 方程的交错半离散双线性系统，给出了任意有限阶的 Gram 行列式解，并利用秩一更新证明其满足双线性方程。通过对辅助势作格点差分消元和引入势函数变换，得到 PE 与 PF 两种非线性形式。两种形式由同一 τ 函数解产生相同的物理场，并具有相应的 Darboux–Lax 表示。在正则谱参数条件下，证明了半离散方程的二阶一致性，以及固定谱数据的精确解族在紧集上以 $O(h^2)$ 趋于连续 DLW 解。

基于两种非线性形式，采用三点中心差分和时间积分方法进行了单孤子与二孤子数值计算，并与直接差分格式比较。固定网格上的精度排序随算例及物理场变化；在所考察的算例中，动网格均降低了两个物理场的误差。

## 参考文献

[1] H.-H. Sheng, G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. *Physica D*, **432** (2022), 133140. [原文](../Paper/sources/PhysD-published.pdf).

[2] B.-F. Feng, H.-H. Sheng, G.-F. Yu. Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation. *Numerical Algorithms*, **94** (2023), 351–370. DOI: [10.1007/s11075-023-01504-1](https://doi.org/10.1007/s11075-023-01504-1).

[3] W. Fu. Direct linearisation of the discrete-time two-dimensional Toda lattices. arXiv:[1802.06452](https://arxiv.org/abs/1802.06452), version 3 (2018).

[4] Y.-B. Tian, Y. Cheng, N. Shao. Construction of recursion formulas for Lax pairs of (2+1)-dimensional equation: Modified generalized dispersive long wave equation. *Communications in Theoretical Physics*, **41** (2004), 807–812. [原文](../Paper/refs/ctp8805.pdf).
