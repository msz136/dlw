# DLW：从初始方程到误差估计

<p class="subtitle">连续系统 · 结构半离散 · 差分缺陷 · 参数响应</p>

<p class="abstract"><strong>摘要</strong>　从连续双线性方程及交错半离散方程出发，推导 DLW 的物理场形式、SD 两场形式、SDR 比值形式及直接差分 FD。将同一连续解代入三种方案，逐项得到纵向二阶截断误差，进而建立谱参数、波形结构、空间与时间离散到物理误差的映射。SD 与 SDR 在精确微分和相容重构下具有相同的纵向残差；两者的全离散差异来自差分乘积缺陷、时间推进和重构。单孤子给出显式系数与统一上界；一般解的误差系数由受迫线性化方程决定。</p>

## 1　连续方程：物理场、势与双线性形式

本文固定连续 DLW 系统为

$$
\begin{aligned}
u_{yt}+v_{xx}+\partial_x[(u+2a)u_y]&=0,\\
v_t+u_{xxy}+\partial_x[(u+2a)v-4u]&=0.
\end{aligned}
$$

其中 $a$ 是系统参数。记

$$
b=u+2a,\qquad A(u)=\frac{u^2}{2}+2au,\qquad
w=v-u_y,\qquad B(w)=\frac{w^2}{32}-\frac w4.
$$

第一式于是写成 $u_{yt}+v_{xx}+A(u)_{xy}=0$。这一步把非线性项写成通量导数，后面的交错差分正是作用在该通量上。

文献中的另一种势形式为

$$
U_{ty}+(\eta_{xy}+2UU_y)_x=0,\qquad
\eta_{ty}+(U_{xy}+2U\eta_y)_x=0.
$$

代入 $U=a+u/2$、$\eta_y=(v-4)/2$，两式乘以 $2$，即恢复上述 DLW。第二式的常背景 $-4$ 产生 $-4u_x$，因此它必须保留。

### 1.1　连续双线性起点

令 $D_x,D_y,D_t$ 为 Hirota 双线性算子，例如 $D_xf\cdot g=f_xg-fg_x$。定义

$$
B_a=D_x^2+D_t+2aD_x,\qquad
B_af\cdot g=0,\qquad (D_yB_a-4D_x)f\cdot g=0.
$$

在 $f,g$ 非零的区域，取

$$
\rho=\log(f/g),\qquad \theta=\log(fg),\qquad
u=2\rho_x,\qquad v=2\theta_{xy}.
$$

将第一条双线性方程除以 $fg$，得到

$$
E:=\frac{B_af\cdot g}{fg}
=\theta_{xx}+\rho_x^2+\rho_t+2a\rho_x=0.
$$

对它作 $2\partial_{xy}$：

$$
2E_{xy}
=v_{xx}+u_{yt}+\partial_x[(u+2a)u_y]=0.
$$

第二条所需的恒等式是

$$
\frac{(D_yB_a-4D_x)f\cdot g}{fg}
=\rho_yE+\rho_{xxy}+\theta_{yt}
+2(\rho_x+a)\theta_{xy}-4\rho_x.
$$

利用 $E=0$，再作 $2\partial_x$，便得到第二条 DLW。这里给出了双线性方程到物理场方程的直接推导；反向恢复双线性方程还需固定积分常数。

## 2　交错双线性方程如何产生 SD

纵向格距记为 $h=\Delta y$。项目中的结构半离散从两条相邻的双线性方程开始：

$$
B_{a-h/2}F_j\cdot G_j=0,\qquad
B_{a+h/2}F_j\cdot G_{j+1}=0.
$$

$F_j$ 位于 $y=(j+\tfrac12)h$，$G_j$ 位于 $y=jh$；$x,t$ 仍是连续变量。令 $\ell_j=\log F_j$、$m_j=\log G_j$。对任意参数 $s$，有恒等式

$$
\frac{B_sf\cdot g}{fg}
=(\log f+\log g)_{xx}+(\log f-\log g)_x^2
+(\log f-\log g)_t+2s(\log f-\log g)_x.
$$

因此两条归一化方程是

$$
\begin{aligned}
0={}&(\ell_j+m_j)_{xx}+(\ell_j-m_j)_x^2
+(\ell_j-m_j)_t+(2a-h)(\ell_j-m_j)_x,\\
0={}&(\ell_j+m_{j+1})_{xx}+(\ell_j-m_{j+1})_x^2
+(\ell_j-m_{j+1})_t+(2a+h)(\ell_j-m_{j+1})_x.
\end{aligned}
$$

定义对称场与跳量

$$
u_j=(2\ell_j-m_j-m_{j+1})_x,\qquad
\omega_j=(m_{j+1}-m_j)_x,\qquad
Z_j=(2\ell_j+m_j+m_{j+1})_x.
$$

两壁的对数差导数分别为 $(u_j+\omega_j)/2$ 和 $(u_j-\omega_j)/2$。因此，平方项的和为 $(u_j^2+\omega_j^2)/2$，差为 $u_j\omega_j$；线性项的和为 $2au_j-h\omega_j$，差为 $2a\omega_j-hu_j$。两方程相加、相减并对 $x$ 求导，得到

$$
\begin{aligned}
u_{j,t}+\partial_x\!\left[A(u_j)+\frac{\omega_j^2}{2}-h\omega_j\right]
+Z_{j,xx}&=0,\\
\omega_{j,t}+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}&=0.
\end{aligned}
$$

### 2.1　消去辅助势

引入差分算子

$$
\begin{aligned}
\delta_-f_j&=\frac{f_j-f_{j-1}}h,&
M_-f_j&=\frac{f_j+f_{j-1}}2,\\
\delta_0f_j&=\frac{f_{j+1}-f_{j-1}}{2h},&
\Delta_hf_j&=\frac{f_{j+1}-2f_j+f_{j-1}}{h^2}.
\end{aligned}
$$

由 $Z_j-u_j=2(m_j+m_{j+1})_x$，直接相减可得

$$
\delta_-Z_j=\delta_-u_j+\frac4hM_-\omega_j.
$$

将第一条演化方程施以 $\delta_-$，便得到 Report 中的 SD 两场形式：

$$
\boxed{\begin{aligned}
0={}&\delta_-u_t+\partial_x\delta_-
\left[A(u)+\frac{\omega^2}{2}-h\omega\right]
+\partial_x^2\left(\delta_-u+\frac4hM_-\omega\right),\\
0={}&\omega_t+\partial_x[(u+2a)\omega-hu]-\omega_{xx}.
\end{aligned}}
$$

### 2.2　恢复共同物理场

误差比较使用 $u,v$。取

$$
v=\frac4h\omega+\delta_0u,\qquad
W_h=v-\delta_0u=\frac4h\omega,\qquad
H=A(u)+h^2B(W_h).
$$

这一步决定误差的归一化：$\omega=O(h)$，其方程中的某一阶不能直接当成 $v$ 的误差阶。利用两个有限格距恒等式

$$
M_-\delta_0=\delta_-+\frac{h^2}{4}\Delta_h\delta_-,
\qquad
\delta_0^2=\Delta_h+\frac{h^2}{4}\Delta_h^2,
$$

第一条方程直接改写；第二条则由 $v_t=(W_h)_t+\delta_0u_t$ 得到。最终为

$$
\boxed{\begin{aligned}
\mathcal R^{SD}_{1,h}={}&\delta_-u_t+\partial_x\delta_-H
+\partial_x^2\left(M_-v-\frac{h^2}{4}\Delta_h\delta_-u\right)=0,\\
\mathcal R^{SD}_{2,h}={}&v_t
+\partial_x[\delta_0H+bW_h-4u]\\
&+\partial_x^2\left(\delta_0u+\frac{h^2}{4}\Delta_hW_h\right)=0.
\end{aligned}}
$$

以上转换对有限 $h$ 精确成立，尚未使用 Taylor 展开。

## 3　SDR：同一结构的比值变量形式

保留势 $M_j=(\log G_j)_x$，则 $\omega_j=M_{j+1}-M_j$、$Z_j=u_j+2(M_j+M_{j+1})$。引入

$$
Q_j=\frac{F_j}{\sqrt{G_jG_{j+1}}},\qquad
R_j=\frac{1-\omega_j/h}{Q_j},\qquad
u_j=2\frac{Q_{j,x}}{Q_j},\qquad \omega_j=h(1-Q_jR_j).
$$

由

$$
u_t=2\partial_x(Q_t/Q),\qquad
u_x+\frac{u^2}{2}=2\frac{Q_{xx}}Q,\qquad
\frac{\omega^2}{4}-\frac h2\omega=\frac{h^2}{4}[(QR)^2-1],
$$

原 $u$ 方程在双线性规范下化为 $Q$ 方程。再令 $S=QR$，$\omega$ 方程等价于

$$
S_t-S_{xx}+2aS_x+2(Q_xR)_x=0.
$$

因为 $-S_{xx}+2(Q_xR)_x=Q_{xx}R-QR_{xx}$，用 $Q$ 方程消去 $Q_t$，即可得到 $R$ 方程：

$$
\boxed{\begin{aligned}
Q_t&=-Q_{xx}-2aQ_x-\mathcal H Q,\\
R_t&= R_{xx}-2aR_x+\mathcal H R,\\
\mathcal H_j&=(M_j+M_{j+1})_x+\frac{h^2}{4}[(Q_jR_j)^2-1],\\
M_{j+1}-M_j&=h(1-Q_jR_j).
\end{aligned}}
$$

物理场为

$$
u=2Q_x/Q,\qquad v=4(1-QR)+\delta_0u.
$$

这就是 SDR，数值报告记作 SD2。在 $Q\ne0$、规范和初边值相容时，它恢复上一节的同一有限 $h$ 物理方程。因此，保留精确的 $x,t$ 微分时，两者的物理残差完全相同。后续用差分代替微分、用时间算法代替精确流，才会破坏这项代数等价。

## 4　FD 与三种实际演化状态

当前 FD 对连续通量作交错差分：

$$
\boxed{\begin{aligned}
\mathcal R^{FD}_{1,h}
&=\delta_-(u_t+A_x)+M_-v_{xx}=0,\\
\mathcal R^{FD}_{2,h}
&=v_t+\partial_x[bv-4u]+\partial_x^2\delta_0u=0.
\end{aligned}}
$$

令 $P=\delta_-u$。实际推进的状态分别为 SD 的 $(P,W_h)$、SDR 的 $(Q,R)$ 和 FD 的 $(P,v)$。固定 $x$ 网格上，项目采用

$$
(Df)_i=\frac{f_{i-2}-8f_{i-1}+8f_{i+1}-f_{i+2}}{12k},
\qquad k=\Delta x,\qquad D_2=D^2.
$$

SD 与 FD 的原生右端因而分别是

$$
\begin{aligned}
P_t^{SD}&=-\delta_-DH-D^2\left(M_-v-\frac{h^2}{4}\Delta_hP\right),\\
(W_h)_t^{SD}&=-D[bW_h-4u]+D^2W_h,\\
P_t^{FD}&=-\delta_-DA-D^2M_-v,\\
v_t^{FD}&=-D[bv-4u]-D^2\delta_0u.
\end{aligned}
$$

SDR 则将其 $Q,R$ 方程中的 $\partial_x,\partial_x^2$ 替换为 $D,D^2$，并用 $u=2DQ/Q$ 恢复物理场。这个数值 $D$ 与 Hirota 双线性算子含义不同。

## 5　逐项推导纵向二阶残差

现在将同一连续精确解 $u,v$ 代入离散方程。以方程左端定义残差，并写

$$
\mathcal R_h^S[u,v]=h^2\tau_y^S[u,v]+O(h^4).
$$

$\tau_y^S$ 是随位置、时间和背景解变化的双分量函数。第一分量应在交错中点展开，第二分量在 $u_j,v_j$ 节点展开。

### 5.1　交错展开决定了二阶系数

在两个相邻节点的中点，

$$
\delta_-f=f_y+\frac{h^2}{24}f_{yyy}+O(h^4),\qquad
M_-f=f+\frac{h^2}{8}f_{yy}+O(h^4).
$$

在物理场节点，

$$
\delta_0f=f_y+\frac{h^2}{6}f_{yyy}+O(h^4),\qquad
\Delta_hf=f_{yy}+\frac{h^2}{12}f_{yyyy}+O(h^4),
$$

因此

$$
W_h=w-\frac{h^2}{6}u_{yyy}+O(h^4),\qquad
H=A(u)+h^2B(w)+O(h^4).
$$

虽然 $\delta_-$ 写成后向差商，它在交错中点逼近导数是二阶的。展开位置必须与所比较的连续方程一致。

### 5.2　FD 的两个分量

第一分量代入 Taylor 展开：

$$
\begin{aligned}
\mathcal R^{FD}_{1,h}
={}&(u_t+A_x)_y+v_{xx}\\
&+h^2\left[\frac1{24}(u_t+A_x)_{yyy}
+\frac18v_{xxyy}\right]+O(h^4).
\end{aligned}
$$

连续方程给出 $(u_t+A_x)_y=-v_{xx}$，故零阶项消失，二阶项合并为 $(-1/24+1/8)v_{xxyy}$。第二分量只有 $\delta_0u$ 带来纵向差分误差。于是

$$
\boxed{\tau_y^{FD}
=\begin{pmatrix}
v_{xxyy}/12\\[2pt]u_{xxyyy}/6
\end{pmatrix}.}
$$

### 5.3　SD 的第一分量

与 FD 相比，SD 第一式多出 $h^2\delta_-B(W_h)_x$ 和 $-h^2\Delta_h\delta_-u_{xx}/4$。取其零阶连续极限，即得

$$
\boxed{\tau_{y,1}^{SD}
=\frac1{12}v_{xxyy}-\frac14u_{xxyyy}+B(w)_{xy}.}
$$

### 5.4　SD 的第二分量

非线性通量需要多一步整理。因为 $A$ 是二次函数，存在精确恒等式

$$
\delta_0A(u)-b\delta_0u
=\frac{(u_{j+1}-u_j)^2-(u_{j-1}-u_j)^2}{4h}
=\frac{h^2}{2}(\Delta_hu)(\delta_0u).
$$

因此

$$
\delta_0H+bW_h-4u
=bv-4u+h^2\left[\frac12u_yu_{yy}+B(w)_y\right]+O(h^4).
$$

色散部分则有

$$
\begin{aligned}
\delta_0u+\frac{h^2}{4}\Delta_hW_h
&=u_y+h^2\left(\frac16u_{yyy}+\frac14w_{yy}\right)+O(h^4)\\
&=u_y+h^2\left(\frac14v_{yy}-\frac1{12}u_{yyy}\right)+O(h^4).
\end{aligned}
$$

代回第二式，利用连续方程消去零阶项：

$$
\boxed{\tau_y^{SD}=\tau_y^{SDR}
=\begin{pmatrix}
\dfrac1{12}v_{xxyy}-\dfrac14u_{xxyyy}+B(w)_{xy}\\[4pt]
\dfrac14v_{xxyy}-\dfrac1{12}u_{xxyyy}
+B(w)_{xy}+\dfrac12(u_yu_{yy})_x
\end{pmatrix}.}
$$

其中

$$
B(w)_{xy}=\frac{(w-4)w_{xy}+w_xw_y}{16}.
$$

三个方案均具有二阶纵向一致性，但主系数不同。结构方案中的额外项可以与 FD 项抵消，也可以增强它；只凭“二阶”或“保持结构”无法判断误差大小。

## 6　从系数公式得到可控上界

所有范数先取在所研究的时空区域及差分所需邻域。令

$$
\begin{aligned}
C_v&=\|v_{xxyy}\|_\infty,\qquad C_u=\|u_{xxyyy}\|_\infty,\\
C_B&=\frac{\|w-4\|_\infty\|w_{xy}\|_\infty
+\|w_x\|_\infty\|w_y\|_\infty}{16},\\
C_N&=\frac{\|u_{xy}\|_\infty\|u_{yy}\|_\infty
+\|u_y\|_\infty\|u_{xyy}\|_\infty}{2}.
\end{aligned}
$$

逐项取范数即可得到

$$
\begin{aligned}
\|\tau_{y,1}^{FD}\|_\infty&\le C_v/12,&
\|\tau_{y,2}^{FD}\|_\infty&\le C_u/6,\\
\|\tau_{y,1}^{SD}\|_\infty&\le C_v/12+C_u/4+C_B,&
\|\tau_{y,2}^{SD}\|_\infty&\le C_v/4+C_u/12+C_B+C_N.
\end{aligned}
$$

这些常数全部来自解的导数，因而可以进一步映射到系统参数。三角不等式丢弃了抵消信息，所以上界之间的大小不能作为方案排名。

### 6.1　FD 的有限格距余量

第一式还能给出一个精确积分表示。令 $y_c$ 为交错中点，$g(s)=v_{xx}(x,y_c+s,t)$。利用连续方程积分，

$$
\mathcal R^{FD}_{1,h}
=\frac{g(h/2)+g(-h/2)}2-\frac1h\int_{-h/2}^{h/2}g(s)\,ds
=\int_{-h/2}^{h/2}K_h(s)g''(s)\,ds,
$$

其中 $K_h(s)=((h/2)^2-s^2)/(2h)\ge0$。其偶对称性与矩给出

$$
\int K_h(s)\,ds=\frac{h^2}{12},\qquad
\frac12\int s^2K_h(s)\,ds=\frac{h^4}{480}.
$$

对 $g''(s)$ 在 $s=0$ 展开，奇项积分为零，得到

$$
\left|\mathcal R^{FD}_{1,h}-\frac{h^2}{12}v_{xxyy}(x,y_c,t)\right|
\le\frac{h^4}{480}\sup_{|s|\le h/2}|v_{xxyyyy}(x,y_c+s,t)|.
$$

同理，对中心一阶差分的积分表示展开，

$$
\left|\mathcal R^{FD}_{2,h}-\frac{h^2}{6}u_{xxyyy}(x,y_j,t)\right|
\le\frac{h^4}{120}\sup_{|s|\le h}|u_{xxyyyyy}(x,y_j+s,t)|.
$$

这说明“二阶主项”与“有限格距的实际残差”之间的偏差也可以由导数界控制。SD 可对其额外通量和复合差分作同样处理。

## 7　单孤子：谱参数直接进入系数

令

$$
K=p+q>0,\qquad P_s=p-a,\qquad Q_s=q+a,\qquad
\Gamma=-P_s/Q_s>0,
$$

并定义

$$
\ell=\frac1{P_s}+\frac1{Q_s}=\frac K{P_sQ_s},\qquad
\Omega=q^2-p^2,\qquad
z=Kx+\ell y+\Omega t+\varphi.
$$

连续单孤子的两个 $\tau$ 函数可取 $g=1+e^z$、$f=1+\Gamma e^z$。记

$$
s(z)=\frac1{1+e^{-z}},\quad
f_1(z)=s(z+\log\Gamma),\quad d=f_1-s,\quad c=f_1+s.
$$

由第 1 节的物理重构，

$$
u=2Kd,\qquad v=2K\ell c',\qquad w=4K\ell s',
\qquad
\partial_x=K\partial_z,\quad\partial_y=\ell\partial_z.
$$

这里的 $f_1$ 是 sigmoid 剖面，与双线性 $\tau$ 函数 $f$ 区分。设 $\zeta=K\ell=K^2/(P_sQ_s)$，各高阶导数自动产生 $K,\ell$ 的幂。例如

$$
v_{xxyy}=2\zeta^3c^{(5)},\qquad
u_{xxyyy}=2\zeta^3d^{(5)},\qquad
B(w)_{xy}=\frac{\zeta^3}{2}[(s')^2]''-\zeta^2s'''.
$$

逐项代入便有

$$
\tau_{y,1}^{FD}=\frac{\zeta^3}{6}(f_1^{(5)}+s^{(5)}),\qquad
\tau_{y,2}^{FD}=\frac{\zeta^3}{3}(f_1^{(5)}-s^{(5)}),
$$

$$
\begin{aligned}
\tau_{y,1}^{SD}
&=\zeta^3\left[\frac{2s^{(5)}-f_1^{(5)}}3
+\frac12[(s')^2]''\right]-\zeta^2s''',\\
\tau_{y,2}^{SD}
&=\zeta^3\left[\frac{f_1^{(5)}+2s^{(5)}}3
+\frac12[(s')^2]''+2(d'd'')'\right]-\zeta^2s'''.
\end{aligned}
$$

由此可见，参数同时改变系数尺度 $\zeta$、两过渡的相对位置 $\log\Gamma$ 和时空相位 $z$。SD 还含 $\zeta^2$ 项，不能用一个统一的三次缩放描述。

### 7.1　全波形统一上界

令 $S_m=\sup_z|s^{(m)}(z)|$。取 $\vartheta=s(1-s)\in[0,1/4]$，则

$$
(s'')^2=\vartheta^2(1-4\vartheta),\qquad
s'''=\vartheta(1-6\vartheta),\qquad
s^{(5)}=\vartheta(1-30\vartheta+120\vartheta^2).
$$

对这些多项式求极值得

$$
S_1=\frac14,\quad S_2^2=\frac1{108},\quad
S_3=\frac18,\quad S_5=\frac14,\qquad
S_2^2+S_1S_3=\frac{35}{864}.
$$

$f_1$ 只是 $s$ 的平移，具有相同范数，且 $\|d^{(m)}\|_\infty\le2S_m$。特别地，

$$
\frac12\|[(s')^2]''\|_\infty\le S_2^2+S_1S_3,\qquad
2\|(d'd'')'\|_\infty\le8(S_2^2+S_1S_3).
$$

从而

$$
\boxed{\begin{aligned}
\|\tau_{y,1}^{FD}\|_\infty&\le\frac{|\zeta|^3}{12},\\
\|\tau_{y,2}^{FD}\|_\infty&\le\frac{|\zeta|^3}{6},\\
\|\tau_{y,1}^{SD}\|_\infty&\le\frac{251}{864}|\zeta|^3+\frac{\zeta^2}{8},\\
\|\tau_{y,2}^{SD}\|_\infty&\le\frac{59}{96}|\zeta|^3+\frac{\zeta^2}{8}.
\end{aligned}}
$$

这是从方程得到的统一残差界。谱极点 $P_sQ_s=0$ 附近，界按 $|\zeta|^2,|\zeta|^3$ 恶化；对于具体参数，更紧的估计应保留前述有符号剖面。

### 7.2　参数敏感度

直接微分 $\zeta=K^2/(P_sQ_s)$ 与 $\Gamma=-P_s/Q_s$：

| 参数 $\theta$ | $\partial_\theta\log|\zeta|$ | $\partial_\theta\log\Gamma$ | $\partial_\theta\Omega$ |
|---|---|---|---|
| $a$ | $1/P_s-1/Q_s$ | $-1/P_s-1/Q_s$ | $0$ |
| $p$ | $2/K-1/P_s$ | $1/P_s$ | $-2p$ |
| $q$ | $2/K-1/Q_s$ | $-1/Q_s$ | $2q$ |

对 $\tau=\zeta^3R_3(z,\Gamma)+\zeta^2R_2(z)$ 应用链式法则，即得到任一参数对残差场的精确响应。分辨率相应由 $kK$、$h|\ell|$、$\delta|\Omega|$ 衡量，其中 $\delta=\Delta t$。

这里须区分两种改变 $a$ 的方式：固定物理初态时，$2a$ 在连续方程中给出统一的 $x$ 平移；固定谱参数 $p,q$ 时，改变 $a$ 还会改变 $\ell,\Gamma$，即同时改变初始波形。

## 8　为何 SD 与 SDR 的实际误差不同

### 8.1　横向差分破坏连续乘积法则

由四阶模板的矩条件，

$$
D=\partial_x-\frac{k^4}{30}\partial_x^5+O(k^6),\qquad
D^2=\partial_x^2-\frac{k^4}{15}\partial_x^6+O(k^6).
$$

于是 SD、FD 在 $h\to0$ 时的共同横向残差首项为

$$
\chi_x=
\begin{pmatrix}
-\partial_x^5(bu_y)/30-\partial_x^6v/15\\
-\partial_x^5(bv-4u)/30-\partial_x^6u_y/15
\end{pmatrix}.
$$

有限 $h$ 还含 $h^2k^4$ 等混合项。这里二阶导数使用 $D^2$，其系数由复合模板确定。

SDR 的连续等价推导反复使用乘积法则，而数值算子具有缺陷

$$
\begin{aligned}
\mathcal C_D(f,g)&:=D(fg)-fDg-gDf\\
&=-\frac{k^4}{30}\sum_{r=1}^4\binom5r
f^{(r)}g^{(5-r)}+O(k^6).
\end{aligned}
$$

例如令 $r=DQ/Q$、$\sigma=F_Q/Q$，由 $Q_t=F_Q=Q\sigma$，

$$
\dot u=2\left[\frac{D(Q\sigma)}Q-\frac{DQ}{Q}\sigma\right]
=2D\sigma+\frac{2\mathcal C_D(Q,\sigma)}Q.
$$

同时 $D^2Q/Q=Dr+r^2+\mathcal C_D(Q,r)/Q$。整理 $u$ 方程，即得到相对于 SD 的额外右端

$$
d_u=\frac{2\mathcal C_D(Q,\sigma)}Q
-2D\left[\frac{\mathcal C_D(Q,r)}Q\right].
$$

对 $W_h=4(1-QR)$ 同样展开乘积，可得

$$
d_W=4\left[\mathcal C_D(Q,DR)-\mathcal C_D(R,DQ)
+D\mathcal C_D(Q,R)-2a\mathcal C_D(Q,R)\right].
$$

因此在共同物理状态 $(P,v)$ 下，

$$
\Delta_x=
\begin{pmatrix}\delta_-d_u\\d_W+\delta_0d_u\end{pmatrix}.
$$

这给出了可以由方程直接计算的 SD–SDR 差异。对于光滑非零分支，它从 $k^4$ 进入；其系数依赖 $Q,R$ 及背景导数，而非仅依赖纵向残差 $\tau_y$。

### 8.2　时间推进对非线性变量变换的响应

设原生状态满足 $Y_t=F(t,Y)$。Euler 一步与精确流之差为

$$
Y+\delta F-Y(t+\delta)
=-\frac{\delta^2}{2}(F_t+F_YF)+O(\delta^3).
$$

对非线性物理重构 $z=\mathcal T(Y)$，在固定网格且重构不显含时间时，

$$
\mathcal T(Y+\delta F)-\mathcal T(Y)-\delta\mathcal T_YF
=\frac{\delta^2}{2}\mathcal T_{YY}[F,F]+O(\delta^3).
$$

SDR 的重构曲率可以显式写出。令 $Q^+=Q+\delta F_Q$、$R^+=R+\delta F_R$，直接通分与展开乘积得到

$$
u^+-u=\frac{\delta\dot u}{1+\delta F_Q/Q},\qquad
W_h^+-W_h=\delta\dot W_h-4\delta^2F_QF_R.
$$

所以即便空间向量场精确对应，同为 Euler 仍可产生不同的一阶全局时间系数。RK4 在光滑精确共轭下将这种差异推迟到五阶局部项、四阶全局项。

在线性模态 $Y_t=\lambda Y$ 上，时间系数更直观：

$$
\lambda_{E,\mathrm{eff}}=\lambda-\frac{\delta\lambda^2}{2}+O(\delta^2\lambda^3),
\qquad
\lambda_{RK4,\mathrm{eff}}=\lambda-\frac{\delta^4\lambda^5}{120}
+O(\delta^5\lambda^6).
$$

因此时间误差系数也依赖所激发的频率和演化增长率。提高时间阶并不能消除既有空间误差。

## 9　从方程残差到物理解误差

残差系数与最终场误差系数之间还隔着演化传播。先只考虑纵向半离散，假设存在受控展开

$$
u_h=u+h^2e+O(h^4),\qquad v_h=v+h^2f+O(h^4).
$$

代回离散方程，零阶项是连续 DLW；收集 $h^2$ 项，得到

$$
\boxed{\begin{aligned}
e_{yt}+f_{xx}+\partial_x[be_y+u_ye]&=-\tau_{y,1},\\
f_t+e_{xxy}+\partial_x[bf+(v-4)e]&=-\tau_{y,2}.
\end{aligned}}
$$

右端负号来自本文使用“方程左端残差”的定义。这组受迫线性化方程才决定物理误差的二阶系数。

### 9.1　传播映射与初始增长

取状态 $\pi=u_y$，在相同左基值下用 $\mathcal Jg=\int_{y_0}^y g(x,\eta)\,d\eta$ 恢复 $u$，且 $\|\mathcal J\|_\infty\le L_y$。令 $E=(e_y,f)$，上式写为

$$
\dot E=\mathcal A E-\tau_y,\qquad
\mathcal A\binom{\epsilon_\pi}{\epsilon_v}
=\binom{-\epsilon_{v,xx}-\partial_x[b\epsilon_\pi+\pi\mathcal J\epsilon_\pi]}
{-\epsilon_{\pi,xx}-\partial_x[b\epsilon_v+(v-4)\mathcal J\epsilon_\pi]}.
$$

令物理输出算子为 $\mathcal C(\epsilon_\pi,\epsilon_v)=(\mathcal J\epsilon_\pi,\epsilon_v)$。若 $\Phi(t,s)$ 是该线性化方程在所选空间中的传播算子，共同物理初值给出 $E(0)=0$，从而

$$
\boxed{
a_y^S(T)=-\mathcal C\int_0^T\Phi(T,s)\tau_y^S(s)\,ds.
}
$$

$a_y^S=(e,f)$ 是有符号误差场。对共同初值，初始速度尤其简单：

$$
e_t(x,y,0)=-\int_{y_0}^y\tau_{y,1}(x,\eta,0)\,d\eta,\qquad
f_t(x,y,0)=-\tau_{y,2}(x,y,0).
$$

若 $\|\Phi(T,s)\|\le e^{L(T-s)}$、$\|\tau_y(s)\|\le C_\tau$，则

$$
\|a_y(T)\|\le C_{\mathrm{out}}C_\tau
\begin{cases}(e^{LT}-1)/L,&L>0,\\T,&L=0,\end{cases}
\qquad C_{\mathrm{out}}\le\max\{L_y,1\}.
$$

这将“局部导数界”转化为“演化误差界”，但新增的传播常数 $L$ 同样必须被控制。

### 9.2　有限维精确恒等式与上下界

对固定的实际空间离散，以 $Y_*(t)$ 表示连续解的相容离散表示，定义

$$
r=F(t,Y_*)-\dot Y_*,\qquad A=F_Y(t,Y_*),\qquad
\epsilon=Y-Y_*.
$$

不作渐近截断便有

$$
\dot\epsilon=A\epsilon+r+N(\epsilon),\qquad
N(\epsilon)=F(t,Y_*+\epsilon)-F(t,Y_*)-A\epsilon,
$$

$$
\epsilon(T)=\Phi(T,0)\epsilon(0)
+\int_0^T\Phi(T,s)[r(s)+N(\epsilon(s))]\,ds.
$$

若 $\|\Phi(t,s)\|\le e^{L(t-s)}$、$\|N(\epsilon)\|\le C\|\epsilon\|^2$，取标量上解 $B'=LB+CB^2+\|r\|$、$B(0)\ge\|\epsilon(0)\|$，便可在其存在且余项界有效的区间控制误差。使用首项残差代替完整 $r$ 时，还需计入高阶残差的传播。

总物理误差由此组织为

$$
e_{u,v}(T)=e_{\mathrm{init}}(T)+h^2a_y^S(T)+k^4a_x^S(T)
+\delta^{\,p_t}a_t^S(T)+e_{\mathrm{boundary}}(T)
+e_{\mathrm{evaluation}}(T)+\mathcal R(T),
$$

其中 Euler 的 $p_t=1$，RK4 的 $p_t=4$。各项是误差场，先有符号相加，再取所需范数。若主项预测为 $\widehat e_f$，并已证明剩余量不超过 $\eta_f$，则

$$
\boxed{
\max\{0,\|\widehat e_f\|_\infty-\eta_f\}
\le \|e_f\|_\infty
\le\|\widehat e_f\|_\infty+\eta_f.
}
$$

这给出了上下界的共同形式。没有余量包围时，主项只能作为渐近预测；当前尚不能据此给出所有算例在指定有限时刻的认证精度。

## 10　其他因素如何进入同一映射

### 10.1　频率与传播

在零背景、非零纵向波数 $\eta$ 上，代入模态 $e^{i(\xi x+\eta y)}$，由连续方程得到

$$
\frac{d}{dt}\binom{\widehat u}{\widehat v}
=M_0\binom{\widehat u}{\widehat v},\qquad
M_0=\begin{pmatrix}
-2ia\xi&-i\xi^2/\eta\\
i(\xi^2\eta+4\xi)&-2ia\xi
\end{pmatrix},
$$

$$
\lambda_\pm=-2ia\xi\pm\sqrt{\xi^4+4\xi^3/\eta}.
$$

固定 $\eta\ne0$ 时，高 $|\xi|$ 存在约按 $\xi^2$ 增长的分支。因此，一致性二阶本身不推出任意光滑数据下的网格一致收敛；传播估计需在有限频率、固定离散维数或另一个可控解空间中建立。

实际 $x$ 差分的频率是

$$
\widetilde\xi=\frac{8\sin(\xi k)-\sin(2\xi k)}{6k},
$$

应以它和实际边界计算离散传播。尤其 $\xi k=\pi$ 时 $\widetilde\xi=0$，连续最高波数的增长率不能直接套到差分系统。

### 10.2　多孤子与相互作用

在正系数分支上，每个 $\tau$ 函数可写为

$$
\tau=\sum_{S\subset\{1,\ldots,N\}}C_S
e^{K_Sx+L_Sy+\Omega_St},\qquad C_S>0.
$$

相互作用系数
$A_{ij}=(p_i-p_j)(q_i-q_j)/[(p_i+q_j)(p_j+q_i)]$
进入 $C_S$。将每一项除以总和得到概率权重 $\pi_S$，则 $\log\tau$ 的混合导数就是斜率 $K_S,L_S$ 的混合累积量：

$$
\partial_x^r\partial_y^s\log\tau
=\operatorname{cum}(\underbrace{K_S,\ldots,K_S}_{r},
\underbrace{L_S,\ldots,L_S}_{s}).
$$

令 $K_\Sigma=\sum_i|K_i|$、$L_\Sigma=\sum_i|\ell_i|$，由累积量的分割公式，

$$
|\partial_x^r\partial_y^s\log\tau|
\le c_{r+s}K_\Sigma^rL_\Sigma^s,\qquad
c_m=\sum_{j=1}^m
\left\{\begin{matrix}m\\j\end{matrix}\right\}(j-1)!.
$$

故谱尺度控制导数上界，相互作用和初相位改变局部权重、峰形及抵消。孤子数量本身不决定误差大小；若 $\tau$ 系数有正有负，还需额外控制 $\tau$ 远离零的程度。

### 10.3　网格、初值与评价

动网格 $x=X(\xi,t)$ 满足 $\partial_x=J^{-1}\partial_\xi$、$J=X_\xi$。对实际采用的 $J_h=1+D_\xi(X-\xi)$，令计算格距为 $\varepsilon$，则

$$
D_x^hf=f_x+\varepsilon^4E_Xf+O(\varepsilon^6),\qquad
E_Xf=-\frac{\partial_\xi^5\widetilde f}{30J}
+\frac{X_{\xi^5}}{30J}f_x.
$$

其二阶导数复合算子的首项为 $\partial_xE_X+E_X\partial_x$。网格加密降低局部物理格距，但网格高阶导数和 $J^{-1}$ 同时进入系数，因此节点更密并不自动给出更小总误差。

初值偏差由 $\Phi(T,0)$ 传播；边界近似作为附加源进入同一积分；插值和采样改变末端输出。以下表概括各因素的主要作用。

| 因素 | 进入的位置 | 理论上可确定的影响 |
|---|---|---|
| $a,p_i,q_i$ | 背景导数、残差与传播 | 改变谱尺度、波形和误差放大 |
| 孤子相互作用、初相位 | $\tau$ 权重、局部重叠和位置 | 改变峰形、抵消及与边界的距离 |
| SD / SDR / FD | $\tau_y,\chi_x$ 与重构 | SD/FD 的纵向源不同；SDR 另有乘积缺陷 |
| $h,k,\delta$ | 源的幂次与可表示频率 | 主项为 $h^2,k^4,\delta^{p_t}$，仍需控制传播 |
| 时间算法与终止时刻 $T$ | 局部缺陷及累计传播 | 时间阶、频率系数和放大时长共同作用 |
| 网格几何 | $J^{-1}$、高阶导数、节点演化 | 同时改变空间缺陷和状态耦合 |
| 初始表示、边界、规范 | 初始误差、持续源、重构 | 相同物理初值才消去独有的初始场偏差 |
| 插值、采样及误差范数 | 末端评价算子 | 绝对误差、相对误差和相位误差可有不同排序 |

对连续因素 $\theta$，线性误差预测 $\dot\epsilon_L=A\epsilon_L+r$ 的敏感度满足

$$
\dot S_\theta=AS_\theta+(\partial_\theta A)\epsilon_L
+\partial_\theta r,\qquad S_\theta=\partial_\theta\epsilon_L.
$$

它把参数影响明确分为“改变误差源”和“改变传播”；物理输出还需加上重构算子随参数的变化。

## 11　加入 $h^2,h^3$ 参数能抵消哪些误差

保持物理参数 $a$ 和网格 $h$ 不变，将两壁参数改为

$$
s_\pm=a+\alpha h^2\pm\frac{h+\beta h^3}{2}.
$$

该族保留已有的 Gram 双线性和孤子结构。仍采用 $v=4\omega/h+\delta_0u$，两壁和差给出的通量变为

$$
H^{\alpha,\beta}
=A(u)+h^2B(W_h)+2\alpha h^2u-\frac{\beta h^4}{4}W_h,
$$

$$
(W_h)_t
=-\partial_x\!\left[bW_h-4u+h^2(2\alpha W_h-4\beta u)\right]
+(W_h)_{xx}.
$$

所以第一残差的二阶变化为 $2\alpha u_{xy}$；第二残差中 $\delta_0(2\alpha u)+2\alpha W_h$ 合为 $2\alpha v$，得到

$$
\boxed{
\tau_y^{\alpha,\beta}
=\tau_y^{SD}
+\alpha\begin{pmatrix}2u_{xy}\\2v_x\end{pmatrix}
+\beta\begin{pmatrix}0\\-4u_x\end{pmatrix}.
}
$$

经过同一传播映射，

$$
a_y^{\alpha,\beta}(T)=a_0(T)+\alpha a_\alpha(T)+\beta a_\beta(T).
$$

这就是可调参数到误差系数的映射。对指定解、时刻及加权内积，最小化该场的平方范数可得

$$
\begin{pmatrix}\alpha\\\beta\end{pmatrix}_{\!*}
=-G^{-1}b,\qquad
G_{ij}=\langle a_i,a_j\rangle,\quad b_i=\langle a_i,a_0\rangle,
\quad i,j\in\{\alpha,\beta\},
$$

前提是 $G$ 可逆。它用理论误差响应选择参数；若目标是最大范数，则对应一个极小极大问题。

两个常数只提供两个可调方向，不能普遍消去全部二阶残差。以零背景附近 $u=0$、$v$ 为小扰动为例，第一分量的线性主项为

$$
\tau_{y,1}^{SD,\mathrm{lin}}
=\frac1{12}v_{xxyy}-\frac14v_{xy}.
$$

此时两个可调方向的第一分量均为零，而上式对一般模态非零。因此该参数族可以降低选定解类的二阶系数，却不能使所有解普遍升级为四阶。

## 12　得到的理论结论与验证对象

完整推导建立了以下关系：

$$
\boxed{
\text{方程与参数}
\longrightarrow\text{背景解及导数}
\longrightarrow\text{有符号残差}
\longrightarrow\text{受迫误差场}
\longrightarrow\text{误差范数}.
}
$$

SD、SDR、FD 的纵向误差均从二阶进入；SD 与 SDR 的理想半离散残差相同，FD 的系数不同。谱参数通过 $\zeta,\Gamma,z$ 或多孤子的混合累积量进入残差，随后又通过线性化背景影响传播。可调双线性参数改变两个明确的源方向，可以针对指定目标优化系数。

最后的数值验证应逐层检验这些已确定的理论量：有限 $h$ 残差除以 $h^2$ 后是否趋于所推系数；SD–SDR 的右端差是否由乘积缺陷解释；共同初值下的短时场误差是否吻合受迫方程；独立改变空间、时间分辨率和系统参数后，误差场是否服从预测。最终再比较误差范数，以保留各来源之间的抵消信息。

<div class="references" markdown="1">

### 资料

[1] [DLW 非线性化原始推导](../../gsg_project/dlw_report/_src/Report.md)：交错双线性方程、两场形式与比值形式。  
[2] [当前数值方法](../../gsg_project/dlw_report/_src/index.md)：SD、SDR、FD 的实际递推与差分模板。  
[3] [系统参数与离散结构的误差映射](../REPORT.md)：参数响应、传播模型和系数界。  
[4] [固定网格二阶系数及上下界](../../dlw_h2_bounds_20260930/REPORT.md)：具体孤子参数下的解析包围。  
[5] [可调双线性参数族](../../dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md)：有限格距参数族及物理重构。

</div>
