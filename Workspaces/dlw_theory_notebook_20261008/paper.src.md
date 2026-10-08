# DLW 方程的半离散化、τ 函数与连续极限

<div class="abstract"><span class="abstract-label">摘要</span> 对 DLW 方程构造交错格点双线性离散，给出任意有限阶的 Gram 行列式解。由秩一更新证明该解满足两条半离散双线性方程，并导出正则非线性解。在固定正实谱参数下，半离散物理场在任意紧区域上以二阶精度趋于连续 DLW 孤子解。</div>

连续变量记为 $(x,y,t)$，离散格点为 $j\in\mathbb Z$，格距为 $h>0$。参数 $a$ 固定，采用 $\lambda=-2$ 的 DLW 归一化。函数均取实解析类；涉及实对数时，τ 函数取正值。

## 1　连续 DLW 与双线性表示

考虑连续 DLW 方程

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{1}$$

引入正的 τ 函数 $f(x,y,t),g(x,y,t)$，令

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{2}$$

记 $B_a=D_x^2+D_t+2aD_x$，对应的连续双线性对为

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{3}$$

Hirota 算子采用 $D_xf\cdot g=f_xg-fg_x$，$D_x^2f\cdot g=f_{xx}g-2f_xg_x+fg_{xx}$。由乘积法则，

$$D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y,$$
$$\partial_y(B_af\cdot g)=B_af_y\cdot g+B_af\cdot g_y.$$

因此，在第一条双线性方程成立时，第二条等价于

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{4}$$

将（2）代入并求导，由（3）得到连续 DLW 方程（1）。

## 2　交错格点与半离散双线性方程

将 $G_j$ 放在 $y=jh$，将 $F_j$ 放在 $y=(j+\tfrac12)h$，构造

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{5}$$

固定物理位置 $y$，记

$$\mathcal B_h^- = B_{a-h/2}f(x,y,t)\cdot g(x,y-h/2,t),$$
$$\mathcal B_h^+ = B_{a+h/2}f(x,y,t)\cdot g(x,y+h/2,t).$$

二阶展开为： 对实解析 $f,g$，在固定 $(x,y,t)$ 处有

$$\frac{\mathcal B_h^++\mathcal B_h^-}{2}=B_af\cdot g+O(h^2),$$
$$\frac{\mathcal B_h^+-\mathcal B_h^-}{h}=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{6}$$

证明。固定 $(x,y,t)$，令

$$\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t)
=B_af\cdot g(y+s)+2sD_xf\cdot g(y+s).$$

这里 $f$ 的 $y$ 坐标保持不变，$s$ 只作用于第二个因子的平移和算子参数。对 $s$ 求导，在 $s=0$ 处得到

$$\begin{aligned}
\Phi(0)&=B_af\cdot g,\\
\Phi'(0)&=B_af\cdot g_y+2D_xf\cdot g,\\
\Phi''(0)&=B_af\cdot g_{yy}+4D_xf\cdot g_y,\\
\Phi^{(3)}(0)&=B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}.
\end{aligned}$$

由于 $\mathcal B_h^{\pm}=\Phi(\pm h/2)$，Taylor 展开给出

$$\mathcal B_h^{\pm}=\Phi(0)\pm\frac h2\Phi'(0)
+\frac{h^2}{8}\Phi''(0)\pm\frac{h^3}{48}\Phi^{(3)}(0)
+\frac{h^4}{384}\Phi^{(4)}(0)+O(h^5).$$

两式相加后除以 $2$，奇次项相消：

$$\begin{aligned}
\frac{\mathcal B_h^++\mathcal B_h^-}{2}
&=\Phi(0)+\frac{h^2}{8}\Phi''(0)+O(h^4)\\
&=B_af\cdot g+\frac{h^2}{8}
\left(B_af\cdot g_{yy}+4D_xf\cdot g_y\right)+O(h^4).
\end{aligned}$$

两式相减后除以 $h$，偶次项相消：

$$\begin{aligned}
\frac{\mathcal B_h^+-\mathcal B_h^-}{h}
&=\Phi'(0)+\frac{h^2}{24}\Phi^{(3)}(0)+O(h^4)\\
&=B_af\cdot g_y+2D_xf\cdot g
+\frac{h^2}{24}\left(B_af\cdot g_{yyy}+6D_xf\cdot g_{yy}\right)+O(h^4).
\end{aligned}$$

舍去显式的二阶项即得（6）。

## 3　孤子解与 Gram 行列式

记 $d=h/2$，定义

$$\lambda_h(z)=\frac{z+d}{z-d},\qquad \chi_i=\lambda_h(p_i-a)\lambda_h(q_i+a),\qquad \gamma_i=-\frac{p_i-a+d}{q_i+a-d}, \tag{7}$$

$$E_i(j,x,t)=\frac{\rho_i}{p_i+q_i}\chi_i^j e^{(p_i+q_i)x+(q_i^2-p_i^2)t},\qquad A_{ik}=\frac{(p_i-p_k)(q_i-q_k)}{(p_i+q_k)(p_k+q_i)}. \tag{8}$$

一般 $N$ 孤子的 τ 函数为

$$\boxed{\begin{aligned}G_j&=\sum_{I\subseteq\{1,\ldots,N\}}\left(\prod_{i\in I}E_i\right)\left(\prod_{i<k\atop i,k\in I}A_{ik}\right),\\F_j&=\sum_{I\subseteq\{1,\ldots,N\}}\left(\prod_{i\in I}\gamma_iE_i\right)\left(\prod_{i<k\atop i,k\in I}A_{ik}\right).\end{aligned}} \tag{9}$$

空乘积取 $1$，$G_{j+1}$ 由 $E_i\mapsto\chi_iE_i$ 得到。以下用等价的 Gram 行列式证明这对函数满足半离散方程。

$$\tau_n(j;s)=\det_{1\le i,k\le N}\!\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\left(-\frac{p_i-s}{q_k+s}\right)^n\bigl(\lambda_h(p_i-a)\lambda_h(q_k+a)\bigr)^j e^{(p_i+q_k)x+(q_k^2-p_i^2)t}\right]. \tag{10}$$

$$F_j=\tau_1(j;a-d),\qquad G_j=\tau_0(j). \tag{11}$$

这里 $N$ 是行列式阶数，$n$ 是辅助层编号；$\tau_0$ 与 $s$ 无关。所有分母和格点乘子均取非零值；当使用负整数层 $n$ 时，还要求 $p_i-s\ne0$。

由主子式展开和 Cauchy 行列式公式

$$\det\left[\frac1{p_i+q_k}\right]_{i,k\in I}=\frac{\prod_{i<k\atop i,k\in I}(p_k-p_i)(q_k-q_i)}{\prod_{i,k\in I}(p_i+q_k)} \tag{12}$$

提出每个主子式的行、列指数因子，即得到（9）。其中 $A_{ik}$ 是归一化相互作用系数，与格距 $h$ 无关。

## 4　Gram 解的双线性恒等式

**主定理（Gram 解）。** 在第 3 节的谱参数条件下，由（10）和（11）定义的 $F_j,G_j$ 满足（5）。

先证明固定 $s$ 的双线性链：

$$\boxed{B_s\tau_{n+1}(j;s)\cdot\tau_n(j;s)=0.} \tag{13}$$

证明。固定 $j,s,n$，将矩阵写成 $M_{ik}=\delta_{ik}+r_ic_k/(p_i+q_k)$，其中

$$r_i=\rho_i[-(p_i-s)]^n\lambda_h(p_i-a)^j e^{p_ix-p_i^2t},\qquad c_k=(q_k+s)^{-n}\lambda_h(q_k+a)^j e^{q_kx+q_k^2t}. \tag{14}$$

令 $P=\operatorname{diag}(p_i)$、$Q=\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义得

$$\begin{gathered}r_x=Pr,\quad r_t=-P^2r,\quad c_x=Qc,\quad c_t=Q^2c,\quad b_x=c-sb,\\M_x=rc^{\mathsf T},\quad M_t=-Pr c^{\mathsf T}+rc^{\mathsf T}Q,\quad M_{n+1}=M-rb^{\mathsf T}.\end{gathered} \tag{15}$$

最后一式由 $-(p_i-s)/(q_k+s)-1=-(p_i+q_k)/(q_k+s)$ 得到。在 $M$ 可逆处记

$$H=M^{-1},\quad z=Hr,\quad\kappa=c^{\mathsf T}z,\quad\zeta=b^{\mathsf T}z,\quad\psi=\frac{\tau_{n+1}}{\tau_n}=1-\zeta. \tag{16}$$

矩阵行列式引理给出 $\psi=1-\zeta$。由 Jacobi 微分公式，$\kappa=\tau_{n,x}/\tau_n$。再记

$$\mu=c^{\mathsf T}Qz,\quad\nu=c^{\mathsf T}HPr,\quad\eta_1=b^{\mathsf T}HPr,\quad\eta_2=b^{\mathsf T}HP^2r. \tag{17}$$

利用 $H_x=-HM_xH$ 和 $H_t=-HM_tH$ 求导，得

$$\begin{aligned}\kappa_x&=\mu+\nu-\kappa^2,\\\zeta_x&=\kappa(1-\zeta)-s\zeta+\eta_1,\\(\eta_1)_x&=\nu(1-\zeta)-s\eta_1+\eta_2,\\\zeta_t&=\mu(1-\zeta)-s\kappa+s^2\zeta-\eta_2+\eta_1\kappa.\end{aligned} \tag{18}$$

其中 $z_x=HPr-\kappa z$，故 $\zeta_x=(c-sb)^{\mathsf T}z+b^{\mathsf T}(HPr-\kappa z)$。对第二式再求一次导数，代入其余三式：

$$\begin{aligned}\zeta_{xx}+\zeta_t+2s\zeta_x&=(\kappa_x+\mu+\nu)(1-\zeta)+(s-\kappa)\zeta_x-s\eta_1-s\kappa+s^2\zeta+\kappa\eta_1\\&=(\kappa_x+\mu+\nu-\kappa^2)(1-\zeta)\\&=2\kappa_x(1-\zeta).\end{aligned} \tag{19}$$

代入 $\psi=1-\zeta$，得

$$\psi_{xx}+\psi_t+2s\psi_x+2\kappa_x\psi=0. \tag{20}$$

对任意 $f=\psi g$，双线性算子的展开给出

$$\frac{B_sf\cdot g}{g^2}=\psi_{xx}+\psi_t+2s\psi_x+2\left(\frac{g_x}{g}\right)_x\psi. \tag{21}$$

取 $g=\tau_n$、$f=\tau_{n+1}$，由（20）得（13）。将全部 $\rho_i$ 替换为 $\varepsilon\rho_i$，则 $\varepsilon=0$ 时 $M=I$，上述恒等式在零点邻域成立。双线性残差是 $\varepsilon$ 的多项式，因而恒为零。取 $\varepsilon=1$，结论也适用于 $M$ 不可逆的点。

在（13）中取 $n=0$、$s=a-d$，得到（5）的第一条方程。又有逐矩阵元恒等式

$$-\frac{p_i-a-d}{q_k+a+d}\lambda_h(p_i-a)\lambda_h(q_k+a)=-\frac{p_i-a+d}{q_k+a-d}. \tag{22}$$

故

$$\tau_1(j;a-d)=\tau_1(j+1;a+d)=F_j. \tag{23}$$

在（13）中取 $n=0$、$s=a+d$，并将 $j$ 换为 $j+1$，得

$$B_{a+d}F_j\cdot G_{j+1}=B_{a+d}\tau_1(j+1;a+d)\cdot\tau_0(j+1)=0. \tag{24}$$

两条方程对任意有限 $N$、实数 $x,t$ 及整数 $j$ 成立。□

## 5　正则性与非线性化

 假设

$$h>0,\qquad0<p_1<\cdots<p_N<a-h/2,\qquad0<q_1<\cdots<q_N,\qquad\rho_i>0.$$

则子集展开的每一项均为正，常数项为 1，所以 $F_j,G_j>0$。对数导数无奇点，定义

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.$$

由下述消元，它们满足（31）。

### 5.1　辅助势的消去

证明。令 $\alpha_j=\log F_j$、$\beta_j=\log G_j$。利用恒等式

$$\frac{B_sf\cdot g}{fg}=(\log f+\log g)_{xx}+(\log f-\log g)_x^2
+(\log f-\log g)_t+2s(\log f-\log g)_x,\tag{25}$$

将（5）除以相应的 τ 函数乘积，得

$$\begin{aligned}
A_j={}&(\alpha_j+\beta_j)_{xx}+(\alpha_j-\beta_j)_x^2+(\alpha_j-\beta_j)_t+(2a-h)(\alpha_j-\beta_j)_x=0,\\
C_j={}&(\alpha_j+\beta_{j+1})_{xx}+(\alpha_j-\beta_{j+1})_x^2+(\alpha_j-\beta_{j+1})_t+(2a+h)(\alpha_j-\beta_{j+1})_x=0.
\end{aligned}\tag{26}$$

取两侧对数差导数的和与差

$$u_j=(2\alpha_j-\beta_j-\beta_{j+1})_x,\qquad
\omega_j=(\beta_{j+1}-\beta_j)_x.\tag{27}$$

于是两侧对数差的导数分别为 $(u_j+\omega_j)/2$ 和 $(u_j-\omega_j)/2$。将式（26）相加、相减并对 $x$ 求导，记

$$Z_j=(2\alpha_j+\beta_j+\beta_{j+1})_x.\tag{28}$$

可得

$$\begin{aligned}
u_{j,t}+\partial_x\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]+Z_{j,xx}&=0,\\
\omega_{j,t}+[(u_j+2a)\omega_j-hu_j]_x-\omega_{j,xx}&=0.
\end{aligned}\tag{29}$$

定义 $\delta_-f_j=(f_j-f_{j-1})/h$、$M_-f_j=(f_j+f_{j-1})/2$。由式（27）有 $\delta_-Z_j=\delta_-u_j+(4/h)M_-\omega_j$，从而消去 $Z_j$，得到闭合的非线性半离散系统

$$\boxed{\begin{aligned}
\delta_-u_{j,t}+\partial_x\delta_-\!\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4hM_-\omega_j\right)&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}}\tag{30}$$

为恢复连续 DLW 的物理变量，令 $v_j=(4/h)\omega_j+\delta_0u_j$，其中 $\delta_0f_j=(f_{j+1}-f_{j-1})/(2h)$。写 $W_j=v_j-\delta_0u_j$、$\Delta_hf_j=(f_{j+1}-2f_j+f_{j-1})/h^2$，式（30）等价地表示为

$$\begin{aligned}
0={}&\delta_-u_{j,t}
+\partial_x\delta_-\!\left[\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right]\\
&+\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_h\delta_-u_j\right),\\
0={}&v_{j,t}+\partial_x\!\left[\delta_0\!\left(\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right)\right)
+(u_j+2a)W_j-4u_j\right]\\
&+\partial_x^2\left[\delta_0u_j+\frac{h^2}{4}\Delta_hW_j\right],
\end{aligned}\tag{31}$$

消元对每个有限 $h>0$ 成立。□

## 6　半离散方程的连续极限

二阶非线性一致性如下。 对固定实解析场 $u(x,y,t),v(x,y,t)$，令 $u_j=u(x,y+jh,t)$、$v_j=v(x,y+jh,t)$。以 $\mathcal N_{1,h},\mathcal N_{2,h}$ 表示（31）的两条残差，以 $\mathcal C_1,\mathcal C_2$ 表示（1）的残差，则

$$\mathcal N_{1,h}(0,x,t)=\mathcal C_1(x,y-h/2,t)+O(h^2),$$
$$\mathcal N_{2,h}(0,x,t)=\mathcal C_2(x,y,t)+O(h^2).\tag{32}$$

证明。第一式的后向差分与相邻平均以 $y-h/2$ 为中心，第二式以 $y$ 为中心。分别在这些位置作 Taylor 展开，奇次余项相消，得到（32）。

同时，将连续 τ 函数按 F、G 的交错位置采样，物理变量的重构满足

$$u^{[h]}=2(\log(f/g))_x+O(h^2),\qquad v^{[h]}=2(\log(fg))_{xy}+O(h^2).\tag{33}$$

对 $g(y-h/2)$ 和 $g(y+h/2)$ 作对称展开，并使用中心差商的二阶精度，得（33）。□

### 6.1　Gram 解族的极限

对上述正实谱参数，连续 τ 函数为

$$\tau_n^{(0)}(x,y,t)=\det\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-a}{q_k+a}\right)^n
e^{(p_i+q_k)x+(q_k^2-p_i^2)t+y((p_i-a)^{-1}+(q_k+a)^{-1})}\right].\tag{34}$$

令 $f^{(0)}=\tau_1^{(0)}$、$g^{(0)}=\tau_0^{(0)}$，并由（2）定义 $u^{(0)},v^{(0)}$。有限 $h$ 的 $F_j,G_j$ 分别以 $j=y/h-1/2$ 和 $j=y/h$ 作正实指数插值，再按（27）及 $v=(4/h)\omega+\delta_0u$ 重构 $u^{(h)},v^{(h)}$。

固定任意有限 $N$，若谱参数在某个 $h_0>0$ 处满足第 5 节的正性条件，则对任意 $R>0$，存在 $C_R\ge0$、$\varepsilon_R>0$，使 $0<h<\varepsilon_R$ 时

$$\sup_{|x|,|y|,|t|\le R}\left(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\right)\le C_Rh^2.\tag{35}$$

这里取极限的是随 $h$ 变化的精确 Gram 解。其相位满足 $h^{-1}\log\lambda_h(z)=z^{-1}+O(h^2)$，F 的半格移位与振幅的一阶项相消；对数导数在紧区域上保持正则，因而得到上述二阶界。

## 附录　保留势的非线性表示

保留辅助势 $M_j=\beta_{j,x}$，由式（27）、（28）得

$$\omega_j=M_{j+1}-M_j,\qquad
Z_j=u_j+2(M_j+M_{j+1}).\tag{36}$$

代入式（29），得

$$\begin{aligned}
0={}&u_{j,t}+\partial_x\!\left[
u_{j,x}+\frac{u_j^2}{2}+2au_j
+2(M_j+M_{j+1})_x+\frac{\omega_j^2}{2}-h\omega_j\right],\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x[(u_j+2a)\omega_j-hu_j],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{37}$$

定义中心比值

$$Q_j=\exp\!\left(\alpha_j-\frac{\beta_j+\beta_{j+1}}2\right)
=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
u_j=2\frac{Q_{j,x}}{Q_j}.\tag{38}$$

其中 $Q_j$ 位于 $y=(j+\tfrac12)h$，$M_j$ 位于 $y=jh$。由此有

$$u_{j,t}=2\partial_x\!\left(\frac{Q_{j,t}}{Q_j}\right),\qquad
u_{j,x}+\frac{u_j^2}{2}=2\frac{Q_{j,xx}}{Q_j}.\tag{39}$$

式（37）的第一条化为

$$\partial_x\!\left[
\frac{Q_{j,t}+Q_{j,xx}+2aQ_{j,x}}{Q_j}
+(M_j+M_{j+1})_x+\frac{\omega_j^2}{4}-\frac h2\omega_j
\right]=0.\tag{40}$$

由式（38），括号内为 $(A_j+C_j)/2=0$，故

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{\omega_j^2}{4}-\frac h2\omega_j\right]Q_j,\\
0={}&\omega_{j,t}-\omega_{j,xx}
+\partial_x\!\left[2a\omega_j
+2\frac{Q_{j,x}}{Q_j}(\omega_j-h)\right],\\
\omega_j={}&M_{j+1}-M_j.
\end{aligned}\tag{41}$$

### 势差的乘积分解

令

$$R_j=\frac{1-\omega_j/h}{Q_j},\qquad
\omega_j=h(1-Q_jR_j),\qquad
\frac{M_{j+1}-M_j}{h}+Q_jR_j=1.\tag{42}$$

在 $Q_j\ne0$ 时，$(Q_{j,x}/Q_j)(\omega_j-h)=-hQ_{j,x}R_j$，且

$$\frac{\omega_j^2}{4}-\frac h2\omega_j
=\frac{h^2}{4}(Q_j^2R_j^2-1).\tag{43}$$

代入式（41），得

$$\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
0={}&(Q_jR_j)_t-(Q_jR_j)_{xx}
+2a(Q_jR_j)_x+2(Q_{j,x}R_j)_x.
\end{aligned}\tag{44}$$

利用恒等式

$$-(Q_jR_j)_{xx}+2(Q_{j,x}R_j)_x
=Q_{j,xx}R_j-Q_jR_{j,xx}.
\tag{45}$$

第二条可写为

$$R_j(Q_{j,t}+Q_{j,xx}+2aQ_{j,x})
+Q_j(R_{j,t}-R_{j,xx}+2aR_{j,x})=0.\tag{46}$$

再由式（44）的第一条，得到

$$\boxed{\begin{aligned}
0={}&Q_{j,t}+Q_{j,xx}+2aQ_{j,x}\\
&+\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\[2pt]
0={}&R_{j,t}-R_{j,xx}+2aR_{j,x}\\
&-\left[(M_j+M_{j+1})_x
+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\[2pt]
1={}&\frac{M_{j+1}-M_j}{h}+Q_jR_j.
\end{aligned}}\tag{47}$$

物理场由下式恢复：

$$\boxed{\begin{aligned}
u_j&=2\frac{Q_{j,x}}{Q_j},\qquad
\omega_j=h(1-Q_jR_j)=M_{j+1}-M_j,\\
v_j&=4(1-Q_jR_j)+\frac{u_{j+1}-u_{j-1}}{2h}.
\end{aligned}}\tag{48}$$