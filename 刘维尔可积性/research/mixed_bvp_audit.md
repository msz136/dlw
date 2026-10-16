# 全线混合边值候选的独立审计与补证

审计日期：2026-10-11。范围为 [候选报告](../sources/2026-10-11_mixed_bvp_candidate.md) 的 (19)、(25)–(28)、(29)–(32)；以下仅报告所列依赖的推导，不升级报告其余主张。

## 0. 结论与证据等级

**没有找到所审式子的数学反例。** 固定 $c=2dA>0,T>0$，(19) 的变换、方向和衰减系数正确；(25) 的非齐次边界项可吸收；(26)–(27) 的端点时间导数正则性足够；(28) 的输运零化块估计成立。三次映射 (31)–(32) 在现有 $\mathcal Z_k\to\mathcal Y_k,\ k\ge6$ 上成立，不需要另加空间矩。

原稿的主要问题是**省略了证明步骤**：非齐次入流不能当普通有界 Hilbert 空间源项；负移位逆须明确高频选择与低频拼接；(25) 的非齐次边界项需要具体迹估计；(27) 的逼近须保留由方程决定的输入导数。本文补齐这些缺项，不以有限数值检查充当分析证明。

本结论只得到固定有限物理时间窗的全线小数据混合边值定理。没有审定后续矩归纳、中心非线性单射、初值重启、Hamilton 辅助流切向性、逆谱或 Liouville 完备性；不能升级为一般物理场的无限维 Liouville 定理。

## 1. 修正版线性定理

记 $D=\partial_x$、$I=[-T,T]$、$q=(1+x^2)^{-1}$，

$$
R=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
C=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\quad
L_\nu=R\partial_t+CD^2+cD(x\cdot)+\nu .
$$

采用原稿空间

$$
Y_k=L^2H^k\cap H^1H^{k-2},\quad
D_k=\{g\in H^k:qg\in H^{k+1},\ xg_x\in H^{k-2}\},
$$

$$
\begin{aligned}
\|w\|_{E_k}={}&\|w\|_{L^2H^k}+\|w(-T)\|_{H^k}+\|w(T)\|_{H^k}\\
&+\|qw\|_{L^2H^{k+2}}+\|qw_t\|_{L^2H^k}
+\|\sqrt q\,w_x\|_{L^2H^k},\\
\|w\|_{Z_k}={}&\|w\|_{E_k}+\|w_t\|_{E_{k-2}}.
\end{aligned}
$$

**定理 A。** 对整数 $k\ge2$，$F\in Y_k$、$g_\pm\in D_k$，问题

$$
L_0w=F,\quad u(-T)=g_+,\quad v(T)=g_-
$$

有唯一 $Z_k$ 解，并有

$$
\|w\|_{Z_k}\le C_{k,c,T}
(\|F\|_{Y_k}+\|g_+\|_{D_k}+\|g_-\|_{D_k}). \tag{A1}
$$

方程按分布理解，端点由图空间迹理解。不要求已有物理时间 Cauchy 半群。

**定理 B（负移位）。** 对正整数 $j$，若 $k\ge j+2$，将 $L_0$ 换为 $L_{-jc}$ 后仍有 (A1)，常数允许依赖 $j$。较低正则版本是：整数 $r\ge j$、$F\in L^2H^r$、输入在 $H^r$ 且 $qg_\pm\in H^{r+1}$，有唯一 $E_r$ 解和 (25) 型估计。唯一性在 $L^2H^j$ 类中成立。**不声称整个无附加正则的 $L^2$ 类中有同一唯一逆。**

## 2. 实际逆算子：补齐 (19) 的非齐次构造

Fourier 变换使 $D(xw)$ 变成 $-\xi\partial_\xi\widehat w$，没有额外常数项。正负频率分别设

$$
\theta=-\log|\xi|,\qquad
W(\theta,t)=e^{-\theta/2}\widehat w(\pm e^{-\theta},t).
$$

这是 $L^2_\xi\to L^2_\theta$ 的酉变换。方程变成

$$
\partial_\theta W+\frac1cR\partial_tW
-\frac{e^{-2\theta}}cCW+\left(\frac12+\frac\nu c\right)W
=\frac1c\widetilde F. \tag{A2}
$$

在 $\mathcal H=L^2((-T,T);\mathbb C^2)$ 中，无势输运半群为

$$
(S(s)f)_+(t)=f_+(t-s/c)\mathbf1_{t-s/c>-T},\quad
(S(s)f)_-(t)=f_-(t+s/c)\mathbf1_{t+s/c<T}.
$$

所以它收缩且 $S(2cT)=0$，核验了入流端点方向。势 $-e^{-2\theta}C/c$ 在任意有限辅助区间有界、反 Hermitian。有限区间上沿特征线的积分方程以短区间 Picard 迭代构造实际演化，串接后覆盖任意有限区间。齐次入流的能量给

$$
\|U_\nu(\theta,\sigma)\|\le
e^{-(1/2+\nu/c)(\theta-\sigma)}. \tag{A3}
$$

$\nu=0$、零输入时，(19) 是实际 Bochner 积分：

$$
W(\theta)=\frac1c\int_{-\infty}^{\theta}
U_0(\theta,\sigma)\widetilde F(\sigma)\,d\sigma,\qquad
\|W\|_{L^2_\theta\mathcal H}\le\frac2c\|\widetilde F\|_{L^2_\theta\mathcal H}. \tag{A4}
$$

非齐次输入为 $h_\pm(\theta)=e^{-\theta/2}\widehat g_\pm(\pm e^{-\theta})$。不能把它直接塞进 (A4) 的普通源项。先取辅助变量中光滑紧支撑的 $F,h_\pm$，在支撑左侧 $\theta=a$ 置零状态，用同一特征线积分方程解条带。输入在角点附近为零，没有角点兼容问题。精确能量是

$$
\begin{aligned}
\frac12\frac d{d\theta}\|W\|_\mathcal H^2
&+\frac1{2c}(|W_+(\theta,T)|^2+|W_-(\theta,-T)|^2)
+\left(\frac12+\frac\nu c\right)\|W\|_\mathcal H^2\\
&=\frac1c\operatorname{Re}\langle\widetilde F,W\rangle
+\frac1{2c}(|h_+|^2+|h_-|^2). \tag{A5}
\end{aligned}
$$

$\nu=0$ 时积分与 Young 不等式统一控制全线状态 $L^2$、任一辅助时刻的状态范数及出流边界 $L^2_\theta$，常数独立于左截断点。对一般 $L^2$ 数据取光滑紧支撑逼近，差也满足 (A5)，故状态与出流迹强收敛；有限条带上的弱特征线方程识别极限方程与入流。

唯一性：零数据 $L^2_\theta\mathcal H$ 解有一列 $\theta_n\to-\infty$ 使 $\|W(\theta_n)\|\to0$。从 $\theta_n$ 积分到任意 $\Theta$，再取极限，得 $W=0$。弱图空间解用有限条带正则化得到同一不等式。返回物理变量就是 (20)。

这完成原稿对非齐次输入仅用一句话省略的实际存在性，且没有假定物理时间双向流。

## 3. 加权最大正则性：补齐 (25)

### 3.1 基础高阶能量

$$
D^\ell D(xw)=D(xD^\ell w)+\ell D^\ell w,\quad
L_{c\ell}D^\ell w=D^\ell F .
$$

也可在 (A4) 及边界特征线表示中乘 $|\xi|^\ell=e^{-\ell\theta}$：演化核增加 $e^{-\ell(\theta-\sigma)}$，辅助阻尼为 $1/2+\ell$。这使交换在构造过程中严密成立。求和得

$$
\|w\|_{L^2H^k}+\|w(-T)\|_{H^k}+\|w(T)\|_{H^k}
\le C(\|F\|_{L^2H^k}+\|g_+\|_{H^k}+\|g_-\|_{H^k}). \tag{A6}
$$

### 3.2 非齐次边界项

令 $P=R\partial_t+CD^2$。分部积分给

$$
\|Py\|_2^2=\|y_t\|_2^2+\|y_{xx}\|_2^2
-2\operatorname{Re}\left[\int u_x\overline{v_x}\,dx\right]_{-T}^{T}. \tag{A7}
$$

齐次混合边界使交叉项为零，故 (23) 正确。若 $u(-T)=h_+$、$v(T)=h_-$，Hilbert 空间迹估计给

$$
\|y(\pm T)\|_{H^1}\le C_T
(\|y_t\|_{L^2L^2}+\|y_{xx}\|_{L^2L^2}+\|y\|_{L^2L^2}). \tag{A8}
$$

其证明可对 $\|y(t)\|_{H^1}^2$ 求导，用 $H^2$-$L^2$ 对偶配对，选一个由时间平均控制的时刻，再用 Cauchy–Schwarz。设 $Q^2=\|y_t\|_2^2+\|y_{xx}\|_2^2$，边界交叉项满足

$$
2|B|\le\varepsilon Q^2+C_{\varepsilon,T}
(\|h_+\|_{H^1}^2+\|h_-\|_{H^1}^2+\|y\|_2^2).
$$

所以

$$
Q\le C_T(\|Py\|_2+\|y\|_2+\|h_+\|_{H^1}+\|h_-\|_{H^1}). \tag{A9}
$$

### 3.3 权重吸收

分部积分给

$$
\|\sqrt q f_x\|_2^2\le\|qf_{xx}\|_2\|f\|_2
+\|q'/\sqrt q\|_\infty\|\sqrt q f_x\|_2\|f\|_2 ,
$$

从而

$$
\|\sqrt q f_x\|_2\le\varepsilon\|qf_{xx}\|_2+C_\varepsilon\|f\|_2. \tag{A10}
$$

即 (24)。取 $f=D^\ell w$、$y=qf$，有

$$
Py=qD^\ell F-cqx f_x-(c+c\ell+\nu)qf
+C(2q'f_x+q''f). \tag{A11}
$$

$|qx|\le\sqrt q$、$|q'|\le C\sqrt q$ 及 $y_{xx}=qf_{xx}+2q'f_x+q''f$ 给

$$
\|\sqrt q f_x\|_2\le\delta\|y_{xx}\|_2+C_\delta\|f\|_2 .
$$

代入 (A9)–(A11)，选小 $\delta$ 同时吸收漂移与权重交换项。输入满足

$$
\|qD^\ell g\|_{H^1}\le C_k(\|qg\|_{H^{k+1}}+\|g\|_{H^k}),\quad\ell\le k .
$$

求和并用 (A6)，得到 (25) 的全部项。同时

$$
\|qw\|_{CH^{k+1}}\le C
(\|qw\|_{L^2H^{k+2}}+\|qw_t\|_{L^2H^k}). \tag{A12}
$$

### 3.4 避免先假定正则性的循环

只有 (A6) 的弱解时，先对 $f$ 用 Fourier 平滑截断 $J_\epsilon$。$[J_\epsilon,D(x\cdot)]$ 的符号为有界 $\xi\partial_\xi J_\epsilon$，交换误差由 $\|f\|_2$ 统一控制。$y_\epsilon=qJ_\epsilon f$ 的方程已给 $y_{\epsilon,t}\in L^2L^2$，空间平滑给 $y_{\epsilon,xx}\in L^2L^2$，故可以使用 (A9)。

输入的统一 $H^1$ 界来自 $\|[q,J_\epsilon]f\|_{H^1}\le C\|f\|_2$：卷积核证明只用 $|q(x)-q(x-z)|\le C|z|$ 与 $\int |z||J'_\epsilon(z)|dz\le C$。统一估计后取弱极限即得加权正则性。

## 4. 时间导数与 (26)–(27)

第一层正则性给两端 $w\in H^k$、$qw\in H^{k+1}$；$Y_k\hookrightarrow CH^{k-1}$。一般移位下，方程决定的导数输入是

$$
\begin{aligned}
h_+&=F_1(-T)-v_{xx}(-T)-cD(xg_+)-\nu g_+,\\
h_-&=-F_2(T)-u_{xx}(T)+cD(xg_-)+\nu g_- . \tag{A13}
\end{aligned}
$$

$\nu=0$ 就是 (26)，两个符号都正确。应用 $E_{k-2}$ 只要求输入 $H^{k-2}$ 且乘 $q$ 后 $H^{k-1}$，不要求完整 $D_{k-2}$。具体有

$$
\begin{aligned}
\|w_{xx}(\pm T)\|_{H^{k-2}}&\le C\|w(\pm T)\|_{H^k},\\
\|qw_{xx}(\pm T)\|_{H^{k-1}}&\le C(\|qw(\pm T)\|_{H^{k+1}}+\|w(\pm T)\|_{H^k}),\\
\|D(xg)\|_{H^{k-2}}&\le C(\|g\|_{H^k}+\|xg_x\|_{H^{k-2}}),\\
\|qD(xg)\|_{H^{k-1}}&\le C\|g\|_{H^k}. \tag{A14}
\end{aligned}
$$

最后一行只用 $qx$ 是有界光滑乘子，不需要额外的 $xg_x\in H^{k-1}$。因此

$$
\|h_\pm\|_{H^{k-2}}+\|qh_\pm\|_{H^{k-1}}
\le C(\|F\|_{Y_k}+\|g_+\|_{D_k}+\|g_-\|_{D_k}). \tag{A15}
$$

严密逼近：选 $F_n,g_n$ 光滑，Fourier 数据用环带截断避开零频与无穷频。有限辅助条带的特征线构造给经典解，辅助初始状态为零、入流在角点附近为零。对经典解，$w_{n,t}$ 的强迫为 $F_{n,t}$，输入恰为 (A13)。先在有限辅助区间积分它的能量，(A15) 控制输入，再把辅助右端取无穷，这无需先假定 $w_{n,t}$ 全局 $L^2$；然后用 $k-2$ 版 (25)。

环带截断在 $D_k$ 中强收敛：漂移交换为 $\xi J'_n\widehat g$，支撑于消失的高/低频尾，且 $|\xi J'_n|\le C$；加权多一阶由上节交换子估计与密度控制。时间平滑在 $Y_k$ 中强收敛。两项之差先由 $E_k$ 估计控制输出迹，再由 (A13)–(A15) 控制导数输入差，故 $w_{n,t}$ 在 $E_{k-2}$ 中 Cauchy。极限是分布导数，证明 (27)。

$w\in L^2H^k,w_t\in L^2H^{k-2}$ 还给 $w\in CH^{k-1}$，与 (A12) 一起证明 (16)。

## 5. 负移位：补齐 (28) 的全频逆

$\nu=-jc$ 时辅助阻尼为 $1/2-j$。设 $L=2cT$、$\alpha=j-1/2$。低频尾 $\theta\ge\theta_0$ 上选 $\|B(\theta)\|=\|e^{-2\theta}C/c\|\le\epsilon$。无势演化为 $e^{\alpha s}S(s)$，在 $s=L$ 为零。Duhamel 与 $\|U(\sigma,\theta)\|\le e^{(\alpha+\epsilon)(\sigma-\theta)}$ 给

$$
\|U(\theta+L,\theta)\|\le\epsilon L e^{(\alpha+\epsilon)L}. \tag{A16}
$$

这就是 (28)，势符号不影响范数界。取 $\epsilon$ 使其 $\rho<1/2$。

**高频选择。** 对整数 $r\ge j$，先构造 $V=|\xi|^rW=e^{-r\theta}W$。它的阻尼为 $1/2+r-j\ge1/2$，源与输入分别乘 $|\xi|^r$。第 2 节给全线实际 $V$，故 $W=e^{r\theta}V$ 是每个有限辅助区间上的实际解。高频 $\theta\le\theta_0$ 的 $H^r$ 界成立，且 (A5) 的有限上限积分控制状态 $W(\theta_0)\in\mathcal H$。

**低频拼接。** 将低频尾分成长度 $L$ 的块。含源与入流时，块终点满足

$$
z_{n+1}\le\rho z_n+d_n,\quad
d_n^2\le C\int_{\text{第 }n\text{ 块}}
(\|\widetilde F\|_\mathcal H^2+|h_+|^2+|h_-|^2)d\theta .
$$

块内能量将状态与出流平方积分控制在 $C(z_n^2+d_n^2)$。几何核属于 $\ell^1$，离散卷积给 $\sum z_n^2\le C(z_0^2+\sum d_n^2)$。这补齐低频 $L^2$ 与出流估计，得到

$$
\|w\|_{L^2H^r}+\|w(-T)\|_{H^r}+\|w(T)\|_{H^r}
\le C_{j,r,c,T}(\|F\|_{L^2H^r}+\|g_+\|_{H^r}+\|g_-\|_{H^r}). \tag{A17}
$$

若两解之差在 $L^2H^j$，则 $D^jw$ 满足 $L_0D^jw=0$、零混合输入，故 $D^jw=0$。$L^2$ 中不存在非零多项式，所以唯一。

以 (A17) 替代 (A6)，第 3 节加权证明原样成立；$\nu$ 只增加有界零阶项。时间导数步骤要求 $k-2\ge j$，正是原稿条件。定理 B 得证。

**应保留的限制：** 常数可依赖 $j$，没有证明 $j\to\infty$ 的统一界。指定有限 $m$ 的矩归纳可容许这种依赖；无限阶 Schwartz 控制、解析矩控制仍需新的统一估计。本文没有检查矩归纳本身。

## 6. 三次非线性映射的完整证明

这部分独立于线性逆。用槽位 $a,b,z\in Z_k$，避免与固定常数 $c$ 混淆，定义

$$
\mathcal Bf=(f(0)-f(x))/x,\qquad
\mathcal T(a,b,z)=D[\mathcal B(ab)z].
$$

### 6.1 除法与局部图空间嵌入

对 $J=(-R,R)$，Minkowski 与变量替换给

$$
D^\ell\mathcal Bf=-\int_0^1\theta^\ell f^{(\ell+1)}(\theta x)d\theta,\quad
\|D^\ell\mathcal Bf\|_{L^2(J)}
\le\frac1{\ell+1/2}\|f^{(\ell+1)}\|_{L^2(J)}. \tag{A18}
$$

故 $\|\mathcal Bf\|_{H^s(J)}\le2\|f\|_{H^{s+1}(J)}$，证明 (29)。图范数给

$$
\begin{aligned}
&\|w\|_{CH^{k-1}}+\|qw\|_{CH^{k+1}}
+\|w\|_{L^2H^k}+\|\sqrt q\,w_x\|_{L^2H^k}\le C\|w\|_{Z_k},\\
&\|w_t\|_{L^2H^{k-2}}+\|\sqrt q\,w_{tx}\|_{L^2H^{k-2}}
+\|qw_t\|_{L^2H^k}\le C\|w\|_{Z_k}. \tag{A19}
\end{aligned}
$$

有限 $J$ 上 $q^{-1}$ 光滑有界，所以

$$
\|w\|_{CH^{k+1}(J)}+\|w\|_{L^2H^{k+2}(J)}
+\|w_t\|_{L^2H^k(J)}\le C_J\|w\|_{Z_k}. \tag{A20}
$$

特别是 $w(0,\cdot)\in L^\infty_t,w_t(0,\cdot)\in L^2_t$，点迹的时间导数由光滑逼近与 (A20) 识别。

### 6.2 零点附近的两种阶数

取 $\chi\in C_c^\infty(J)$ 在零点附近为 1，$\mathcal T_0=D[\chi\mathcal B(ab)z]$。一维 tame 乘积及 (A18) 给

$$
\|\mathcal T_0(a,b,z)\|_{H^k}\le C\|z\|_{H^{k+1}(J)}
(\|a\|_{H^{k+2}(J)}\|b\|_{H^{k+1}(J)}
+\|b\|_{H^{k+2}(J)}\|a\|_{H^{k+1}(J)}). \tag{A21}
$$

时间导数落于第一槽时，

$$
\|\mathcal T_0(a_t,b,z)\|_{H^{k-2}}
\le C\|a_t\|_{H^k(J)}\|b\|_{H^{k+1}(J)}\|z\|_{H^{k+1}(J)}. \tag{A22}
$$

第二、第三槽同理。配合 (A20) 与时间 Hölder 给局部三线性 $Y_k$ 界，亦证明 (30)。

### 6.3 远场最高导数与点迹导数

令 $h=(1-\chi)/x$。它光滑，$h/\sqrt q$ 的各阶导数有界，故

$$
\|hf_x\|_{H^s}\le C_s\|\sqrt q\,f_x\|_{H^s}. \tag{A23}
$$

远场 $\mathcal T_\infty=D\{h[a(0)b(0)-ab]z\}$。展开普通乘积：

$$
D(habz)=h'abz+h(a_xbz+ab_xz+abz_x).
$$

对整数 $s\ge1$，

$$
\|f_1f_2f_3\|_{H^s}\le C_s
\sum_i\|f_i\|_{H^s}\prod_{\ell\ne i}\|f_\ell\|_{H^1}. \tag{A24}
$$

此式可由 Fourier 卷积 $L^2*L^1*L^1\to L^2$、$\|\widehat f\|_1\le C\|f\|_{H^1}$ 直接证明。最高 $a_x$ 项由 (A23) 和加权 $L^2H^k$ 控制；最高导数落在其他槽时，用该槽无权 $L^2H^k$，而 $ha_x\in CH^1$ 由 $a\in CH^{k-1}$ 控制。故

$$
\|D(habz)\|_{L^2H^k}\le C\|a\|_{Z_k}\|b\|_{Z_k}\|z\|_{Z_k}. \tag{A25}
$$

点迹项 $a(0)b(0)D(hz)$ 用 $L^\infty_t$ 点迹乘 $\|z\|_{L^2H^k}+\|\sqrt q\,z_x\|_{L^2H^k}$。

令 $s=k-2$。时间导数槽位的界为

$$
\|D(ha_tbz)\|_{H^s}\le C
(\|a_t\|_{H^s}+\|\sqrt q\,a_{tx}\|_{H^s})
\|b\|_{H^{s+1}}\|z\|_{H^{s+1}}. \tag{A26}
$$

逐项是 $h'a_tbz,ha_{tx}bz,ha_tb_xz,ha_tbz_x$，用 $H^s$ 代数、(A23) 即可。所有时间槽位由 (A19) 控制。点迹时间导数需明确写出：

$$
\partial_t[a(0)b(0)D(hz)]
=[a_t(0)b(0)+a(0)b_t(0)]D(hz)+a(0)b(0)D(hz_t).
$$

方括号在 $L^2_t$，$D(hz)\in L^\infty H^{k-2}$；最后项用 $\|z_t\|_{L^2H^{k-2}}+\|\sqrt q z_{tx}\|_{L^2H^{k-2}}$。所以时间部分也闭合。

### 6.4 拼接及 Lipschitz

精确恒等式 $\mathcal T=\mathcal T_0+\mathcal T_\infty$ 已包含截断导数，没有遗漏交换项。得到

$$
\|\mathcal T(a,b,z)\|_{Y_k}\le C\|a\|_{Z_k}\|b\|_{Z_k}\|z\|_{Z_k}. \tag{A27}
$$

原非线性 $r(w)=(u^2-v^2)/(8d)$、$b[w]=\mathcal B(r(w))/A$、$\mathcal N(w)=-R D(b[w]w)$ 是这些三线性项的有限和。因此 (31) 成立。对每项使用

$$
T(w,w,w)-T(\widetilde w,\widetilde w,\widetilde w)
=T(w-\widetilde w,w,w)+T(\widetilde w,w-\widetilde w,w)
+T(\widetilde w,\widetilde w,w-\widetilde w)
$$

得到 (32)。光滑图空间的完备化与 (A20) 延伸估计并识别极限零点值。独立子核查也得同一结果；这里已写完整证明，不依赖另一个文件。

## 7. 可以宣布的非线性定理及边界

**小数据混合边值定理。** 固定 $A,d,T>0,k\ge6$，存在 $\delta>0$，使 $\|g_+\|_{D_k}+\|g_-\|_{D_k}<\delta$ 时，原稿 (7)–(11) 有唯一的小 $Z_k$ 解，且实解析依赖输入。唯一性限于一个预先选定的充分小 $Z_k$ 球。

证明：第 2–4 节给连续 $G_0:Y_k\times D_k^2\to Z_k$，第 6 节给连续三次 $\mathcal N$。取 $R=2C_L\|g\|_{D_k^2}$，若 $C_LC_NR^2\le1/8$，映射 $w\mapsto G_0(\mathcal N(w);g_+,g_-)$ 保持半径 $R$ 球，Lipschitz 常数至多 $1/2$。收缩给唯一解。$I-G_0D\mathcal N(w)$ 由 Neumann 级数可逆，解析隐函数论给实解析依赖。

这是两个任意物理空间端点函数的小邻域，没有固定 Fourier 截断。但它只给混合输入参数化的解族。中心值的非线性单射、取值像上的正则重启、后续 Hamilton / Poisson 与逆谱步骤，均不由本定理推出。

## 8. 审计清单

| 候选式 | 结论 | 本文件补证 |
|---|---|---|
| (19) | 正确；非齐次构造原稿过短 | (A2)–(A5)，特征线、入流能量与强极限 |
| (25) | 成立；输入需加权额外一阶 | (A7)–(A12)，边界交叉项吸收、正则化 |
| (26) | 两个符号正确 | (A13) 的一般移位形式 |
| (27) | 成立；$D_k$ 的 $xg_x$ 正则够用 | (A14)–(A15)，导数输入与 Cauchy 逼近 |
| (28) | 块界正确；块界本身尚不足全频逆 | (A16)–(A17)，高频选择与低频拼接 |
| (31)–(32) | 现有 $k\ge6$ 空间成立 | (A18)–(A27)，除法、远场 tame 项、点迹时间导数、极化 |

没有发现这些步骤的确切数学漏洞；补齐的是实际证明缺项。所得定理仍限于该 $M=2,m=Ax,A>0$ 分支、固定有限 $T$，没有关于矩移位阶数的统一常数结论。
