# 2026-10-11 全线小解混合边值候选报告

> **外部研究草稿，尚未完整独立复核；其中声称的定理不是本仓库已认证结果。候选定理，未完整独立复核。**
>
> 本文归档所提供报告全文，仅规范 Markdown 数学排版与转义字符。正文内部“成立”“已证明”“定理”等表述是原报告的声称，不代表本次归档完成独立审定。原报告提及的符号复核脚本未在本次取得，未运行；代数脚本检查亦不能替代分析证明。优先待审项为负移位线性逆的统一界、端点时间迹、非线性 Lipschitz 估计和空间矩归纳。
>
> 记号提醒：本文 $u=p+2ds$、$v=p-2ds$ 是涨落组合；$c=2dA$ 是算子系数，均不是旧周期稿的物理 $u,v$ 或平均 $c$。本文后段 $m$ 表示空间矩阶，前段 $m=Ax$ 表示平均场；第三节起 $q=(1+x^2)^{-1}$ 是权重，范数中的 $w$ 是向量函数，分别区别于专题平均通量 $q$ 和格点场 $w_j$。专题统一记号及当前目标见 [README](../README.md) 与 [GOAL](../GOAL.md)。

---

**本轮可以把“全线小解存在性”推进到一个具体的非线性混合边值定理，但仍不能把它等同于原始物理场上的双向初值流，更不能据此宣布无限维刘维尔可积。** 这次的关键区别是：存在性不再假设 $\Phi_t$，也不依靠空间零点的时间迹参数化，而是直接对

$$
a_+(-T)=g_+,\qquad a_-(T)=g_-
$$

构造全线解，并给出数据空间、解空间和收缩估计。

继续检查中心取值后，可以证明：中心映射的线性化单射，但其逆在自然的加权索伯列夫初值范数下无界。因此，“两端数据适定”到“中心初值适定”之间确实还有一个不能跳过的数学环节。进一步，旧辛形式的非闭合缺陷在新构造的真实解族中仍然出现，并不是此前使用过大的等时空间所造成的假象。

以下先处理 $A>0$。这是与你指定的端点分配相匹配的符号。对 $A<0$，通过反转时间并交换两个涨落组件，可以证明**反向分配端点**的同类结果；本轮不把它写成原端点分配下的 $A<0$ 定理。

## 一、独立复核：哪些结论保留，哪里需要修正

### 1. 严格单调恒等式成立，而且可以降低衰减要求

令

$$
r=ps,\qquad N=p^2+4d^2s^2,\qquad mb+r=\Gamma,\qquad m=Ax.
$$

直接代入物理方程得到

$$
r_t
=D\left[-br+ps_x-sp_x-\frac m2N\right]
-b_xr-\frac A2N.
\tag{1}
$$

其中 $D=\partial_x$。

一种足以支持以下计算的正则性是：$p,s$ 及其所需空间导数连续，$p,s,xp,xs$ 属于 $L^2(\mathbb R)$，时间导数具有相应的局部时间可积性，零点商按光滑除法定义。后面构造的解满足比这些更强的条件。

由 $r=\Gamma-mb$，

$$
\int_{\mathbb R}b_xr\,dx
=\Gamma[b]_{-\infty}^{+\infty}
-\left[\frac{mb^2}{2}\right]_{-\infty}^{+\infty}
+\frac A2\int_{\mathbb R}b^2\,dx.
$$

因为

$$
b(x,t)=\frac{\Gamma(t)}{Ax}+o(|x|^{-1}),
$$

这里的两个边界项都为零。式（1）的通量也可用空间截断函数严格积分，得到

$$
\boxed{
\frac{d}{dt}\int_{\mathbb R}ps\,dx
=-\frac A2\int_{\mathbb R}
\left(p^2+4d^2s^2+b^2\right)dx.
}
\tag{2}
$$

右侧是普通绝对收敛积分，不涉及主值。

因此，上一轮严格单调结论保留。它不要求所有涨落都属于施瓦茨空间；足够的加权索伯列夫正则性已经可以支持它。

### 2. 混合边值差分估计成立，但不能用于替代中心初值唯一性

考虑同一个 $A$ 下的两解。用

$$
\delta p=p^{(1)}-p^{(2)},\qquad
\bar p=\frac{p^{(1)}+p^{(2)}}2
$$

表示差与平均；$s,b,\Gamma$ 同样记号。定义

$$
N_\delta=(\delta p)^2+4d^2(\delta s)^2.
$$

精确恒等式为

$$
\begin{aligned}
\frac d{dt}\int\delta p\,\delta s\,dx
={}&-\frac A2\int\left(N_\delta+(\delta b)^2\right)dx\\
&-\int\bar b_x\,\delta p\,\delta s\,dx
-\int\delta b\left(\bar p_x\delta s+\bar s_x\delta p\right)dx.
\end{aligned}
\tag{3}
$$

这里使用的是

$$
Ax\,\delta b+\bar p\,\delta s+\bar s\,\delta p=\delta\Gamma,
$$

没有把 $\delta\Gamma$ 设为零。

令

$$
B=\|\bar b_x\|_\infty,\qquad
G=\left\|\sqrt{\bar s_x^2+\frac{\bar p_x^2}{4d^2}}\right\|_\infty.
$$

由

$$
|\delta p\,\delta s|\le \frac{N_\delta}{4d},
\qquad
|\bar p_x\delta s+\bar s_x\delta p|\le G\sqrt{N_\delta},
$$

只要

$$
\frac{B}{2d}+G\le\frac A2,
\tag{4}
$$

就有

$$
\frac d{dt}\int\delta p\,\delta s\,dx
\le-\frac A4\int\left(N_\delta+(\delta b)^2\right)dx.
\tag{5}
$$

这确实给出小解的混合边值唯一性。但是，$\delta p(0)=\delta s(0)=0$ 并不意味着两个混合端点的数据相同。因此，式（5）**不能直接证明中心初值唯一性**。

### 3. 局部解析构造需要纠正一处公式，并降低“解流”表述

上一轮采用的系数权重

$$
\omega_{n,k}=\binom{n+2k}{n}^{-1}
$$

可以保留，但展示出来的算子权重比有一处分子、分母写反。正确的是

$$
\frac{k+1}{(n+1)(n+2)}
\frac{\omega_{n+2,k}}{\omega_{n,k+1}}
=\frac1{2(2k+1)}.
\tag{6}
$$

因此

$$
\|\mathcal I^2\partial_t u\|_{R,T}
\le \frac{R^2}{2T}\|u\|_{R,T}
$$

的结论仍然成立，原点积分方程的收缩构造也可以保留。

但它所证明的对象应准确称为：

> 由四个小解析时间迹参数化的局部解析时空解族；在联合解析解类内，同一个初始空间芽至多对应一个这样的解。

还没有证明的是：这族初始空间芽能由自然的初始场条件描述，以及从初始芽到时间迹的逆映射在自然解析拓扑中连续。**先前把时间迹参数空间中的平移直接称为物理初值空间上的双向解流，表述过强。**

下面的全线构造不使用这个解析迹空间。

## 二、把全线问题写成真正可求逆的混合算子

定义

$$
u=p+2ds,\qquad v=p-2ds,\qquad
\mathbf a=\binom uv,\qquad c=2dA>0.
$$

这里 $u,v$ 只是本节的涨落组合，不是原来的格点物理场 $U_j,w_j$。反变换为

$$
p=\frac{u+v}{2},\qquad s=\frac{u-v}{4d},
\qquad r=\frac{u^2-v^2}{8d}.
$$

记

$$
\mathsf R=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
\mathsf C=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

则原方程精确等价于

$$
\boxed{\mathcal L_0\mathbf a=\mathcal N(\mathbf a),}
\tag{7}
$$

其中

$$
\mathcal L_\nu
=\mathsf R\partial_t+\mathsf C D^2+cD(x\,\cdot)+\nu I,
\qquad
\mathcal N(\mathbf a)=-\mathsf R D(b[\mathbf a]\,\mathbf a),
\tag{8}
$$

$$
b[\mathbf a]=\frac{\Gamma[\mathbf a]-r[\mathbf a]}{Ax},
\qquad
\Gamma[\mathbf a]=\frac{u(0)^2-v(0)^2}{8d}.
\tag{9}
$$

$\nu$ 是稍后处理空间矩时使用的常数移位参数；原物理系统对应 $\nu=0$。

写成分量就是

$$
u_t=-v_{xx}-c(xu)_x-(bu)_x,\qquad
v_t=-u_{xx}+c(xv)_x-(bv)_x.
\tag{10}
$$

混合边界条件正是

$$
u(-T)=g_+,\qquad v(T)=g_-.
\tag{11}
$$

原先无界的 $Ax$ 耦合现在全部放在线性算子 $\mathcal L_0$ 中处理，而不是把它当作有界小扰动。

## 三、具体的数据空间与解空间

固定 $I=[-T,T]$，并令

$$q(x)=\frac1{1+x^2}.$$

下文 $H^k=H^k(\mathbb R)$ 是实索伯列夫空间；向量函数的范数是两个组件范数的和。所有时间积分均在 $I$ 上。

对整数 $k\ge2$，定义强迫空间

$$
\mathcal Y_k=L^2(I;H^k)\cap H^1(I;H^{k-2}),
$$

使用范数

$$
\|F\|_{\mathcal Y_k}
=\|F\|_{L^2H^k}+\|F_t\|_{L^2H^{k-2}}.
\tag{12}
$$

定义端点数据空间

$$
\mathcal D_k=\left\{g\in H^k:qg\in H^{k+1},\ xg_x\in H^{k-2}\right\},
$$

$$
\|g\|_{\mathcal D_k}
=\|g\|_{H^k}+\|qg\|_{H^{k+1}}+\|xg_x\|_{H^{k-2}}.
\tag{13}
$$

它是由物理空间函数及其导数定义的班纳赫空间，不涉及未知解历史。

为描述解的正则性，先定义

$$
\begin{aligned}
\|w\|_{\mathcal E_k}
={}&\|w\|_{L^2H^k}
+\|w(-T)\|_{H^k}+\|w(T)\|_{H^k}\\
&+\|qw\|_{L^2H^{k+2}}+\|qw_t\|_{L^2H^k}
+\|\sqrt q\,w_x\|_{L^2H^k}.
\end{aligned}
\tag{14}
$$

再令

$$
\boxed{\|w\|_{\mathcal Z_k}
=\|w\|_{\mathcal E_k}+\|w_t\|_{\mathcal E_{k-2}}.}
\tag{15}
$$

这些空间可以由光滑函数关于上述图范数完备化定义。端点迹与方程一起由下面的估计确定。

其中两个重要嵌入是

$$
w\in C(I;H^{k-1}),\qquad qw\in C(I;H^{k+1}).
\tag{16}
$$

第二个嵌入意味着：在任何有限空间区间上，实际上比全局无权正则性多控制了两阶空间导数。这正是处理零点除法需要的补偿。

## 四、线性混合边值问题的存在性：不只是一条能量估计

### 1. 对数频率变换给出实际逆算子

采用空间傅里叶变换，令

$$
\eta=\log|\xi|,\qquad
\widetilde{\mathbf a}(\eta,t)
=e^{\eta/2}\widehat{\mathbf a}(\pm e^\eta,t).
$$

正、负频率分别处理。因子 $e^{\eta/2}$ 使这一步在 $L^2$ 中为酉变换。

算子变成

$$
\widetilde{\mathcal L_\nu}
=\mathsf R\partial_t-c\partial_\eta-e^{2\eta}\mathsf C
+\left(\frac c2+\nu\right)I.
\tag{17}
$$

再令 $\theta=-\eta$，除以 $c$，得到

$$
\partial_\theta W+\frac1c\mathsf R\partial_tW
-\frac{e^{-2\theta}}c\mathsf C W
+\left(\frac12+\frac\nu c\right)W
=\frac1c\widetilde F.
\tag{18}
$$

现在把 $\theta$ 当作构造线性逆算子的辅助演化变量，而不是物理时间。算子

$$
\frac1c\mathsf R\partial_t,\qquad W_+(-T)=0,\quad W_-(T)=0,
$$

具有耗散的入流边界条件。其无势输运半群经过长度 $2cT$ 后完全离开区间，因此为零。矩阵项

$$-\frac{e^{-2\theta}}c\mathsf C$$

在每个有限 $\theta$ 区间上有界且反对称，不增加能量。

对 $\nu=0$，由分段常系数逼近或有界扰动的积分方程，得到辅助演化算子 $U(\theta,\sigma)$，满足

$$
\|U(\theta,\sigma)\|\le e^{-(\theta-\sigma)/2},\qquad \theta\ge\sigma.
$$

因此齐次混合边界下实际定义

$$
W(\theta)=\frac1c\int_{-\infty}^{\theta}
U(\theta,\sigma)\widetilde F(\sigma)\,d\sigma.
\tag{19}
$$

非齐次入流数据可先在有限辅助区间上加入，再由同一个能量估计取极限。这样得到的是实际 $L^2$ 解，而不是假设已有物理时间半群。

对应的精确估计为

$$
\begin{aligned}
&\frac12\left(\|u(T)\|_2^2+\|v(-T)\|_2^2
-\|g_+\|_2^2-\|g_-\|_2^2\right)
+\frac c2\|\mathbf a\|_{L^2(I\times\mathbb R)}^2\\
&\hspace{4cm}=\operatorname{Re}\int_{I\times\mathbb R}
F\cdot\overline{\mathbf a}\,dx\,dt.
\end{aligned}
\tag{20}
$$

齐次数据和强迫下，辅助演化的衰减及 $L^2$ 条件给出唯一性。

这一步使用的是对称耗散边界问题的构造机制，但这里已经具体写出了本系统的变换、边界方向、反对称势和逆积分。一般弗里德里希斯系统的存在性框架可以作为背景，不能替代这些核验。〔原报告引文尚未核验〕

### 2. 高阶导数不会破坏这个估计

交换关系

$$D^kD(xw)=D(xD^kw)+kD^kw$$

给出

$$
(\mathcal L_0+ck)D^k\mathbf a=D^kF.
\tag{21}
$$

所以对 $k$ 阶导数，式（20）的体积耗散系数由 $c/2$ 增加到

$$c\left(k+\frac12\right).$$

因此可以控制

$$
\|\mathbf a\|_{L^2H^k}
+\|\mathbf a(T)\|_{H^k}+\|\mathbf a(-T)\|_{H^k}.
\tag{22}
$$

### 3. 加权正则性补偿零点处的两阶损失

令

$$\mathcal P=\mathsf R\partial_t+\mathsf C D^2.$$

对齐次混合边界的光滑函数，有精确等式

$$
\boxed{\|\mathcal Pw\|_{L^2}^2
=\|w_t\|_{L^2}^2+\|w_{xx}\|_{L^2}^2.}
\tag{23}
$$

交叉项为

$$-2\left[\int u_xv_x\,dx\right]_{-T}^{T},$$

在 $u(-T)=0,\ v(T)=0$ 下消失。

非齐次数据时，这个边界项由输入数据的 $H^1$ 范数及通常的时间迹估计控制。另一方面，分部积分给出

$$
\|\sqrt q\,w_x\|_2
\le\varepsilon\|q w_{xx}\|_2+C_\varepsilon\|w\|_2.
\tag{24}
$$

把式（23）应用于 $qD^kw$，则

$$qxw_x,\qquad q'w_x$$

均可由式（24）吸收。无界系数 $x$ 没有被丢弃，而是由

$$|xq(x)|\le\sqrt{q(x)}$$

实际控制。结合式（22），得到

$$
\boxed{
\|w\|_{\mathcal E_k}\le C\left(
\|F\|_{L^2H^k}
+\|g_+\|_{H^k}+\|g_-\|_{H^k}
+\|qg_+\|_{H^{k+1}}+\|qg_-\|_{H^{k+1}}
\right).
}
\tag{25}
$$

### 4. 时间正则性所需的端点导数是由方程给出的

对光滑逼近解求时间导数。$w_t$ 满足同一个线性方程，强迫为 $F_t$。它的混合输入不是任意添加的，而是

$$
\begin{aligned}
u_t(-T)&=F_1(-T)-v_{xx}(-T)-cD(xg_+),\\
v_t(T)&=-F_2(T)-u_{xx}(T)+cD(xg_-).
\end{aligned}
\tag{26}
$$

式（25）控制输出端的 $H^k$ 迹和加权 $H^{k+1}$ 迹；而

$$F\in\mathcal Y_k\quad\Longrightarrow\quad F\in C(I;H^{k-1}).$$

因此式（26）属于应用 $\mathcal E_{k-2}$ 估计所需的数据空间。通过光滑逼近取极限，得到

$$
\boxed{
\|w\|_{\mathcal Z_k}\le C_{k,c,T}\left(
\|F\|_{\mathcal Y_k}+\|g_+\|_{\mathcal D_k}+\|g_-\|_{\mathcal D_k}
\right).
}
\tag{27}
$$

至此，线性存在性、唯一性和连续依赖均已构造，而不是由先验估计单独宣布。

### 5. 空间矩需要的负移位算子也可以处理

稍后会出现 $\mathcal L_{-jc}$，其中 $j$ 是正整数。它的零阶能量不再正定，不能直接重复式（20）。

在式（18）中，它的阻尼是 $1/2-j$。在高频端，用 $|\xi|^j$ 加权后，阻尼重新变成 $1/2$。在低频端，反对称势 $e^{-2\theta}\mathsf C/c$ 趋于零，而无势输运在长度 $2cT$ 后为零。若低频端的势范数不超过 $\varepsilon$，一个长度为 $2cT$ 的演化块满足

$$
\|U(\theta+2cT,\theta)\|
\le\varepsilon(2cT)
\exp\!\left[(j-\tfrac12+\varepsilon)2cT\right].
\tag{28}
$$

取足够低的频率使右侧小于 $1/2$，即可逐块求和。

因此，$\mathcal L_{-jc}$ 在具有至少 $j$ 阶空间正则性的混合数据类中有实际逆算子；若还要使用式（27）的时间正则性，则取 $k-2\ge j$。**这里没有声称负移位算子在无额外正则性的整个 $L^2$ 空间上有同样的逆界。**

## 五、非线性全线小解：收缩估计确实闭合

### 1. 零点商的损失被上面的局部正则性补偿

定义光滑除法算子

$$
\mathcal Bf(x)=\frac{f(0)-f(x)}x=-\int_0^1f'(\theta x)\,d\theta.
$$

在固定有限空间区间上，

$$
\|\mathcal Bf\|_{H^k}\le C_k\|f\|_{H^{k+1}}.
\tag{29}
$$

因此 $D(bw)$ 在零点附近确实可能损失两阶空间导数，不能把它当作普通的一阶半线性项。

但是，式（15）—（16）给出

$$
qw\in L^2H^{k+2}\cap C H^{k+1},\qquad qw_t\in L^2H^k.
$$

这恰好支持局部估计

$$
\begin{aligned}
\|\mathcal N(w)\|_{L^2H^k(\text{零点附近})}
&\le C\|w\|_{CH^{k+1}(\text{局部})}^2
\|w\|_{L^2H^{k+2}(\text{局部})},\\
\|\partial_t\mathcal N(w)\|_{L^2H^{k-2}(\text{零点附近})}
&\le C\|w\|_{CH^{k+1}(\text{局部})}^2
\|w_t\|_{L^2H^k(\text{局部})}.
\end{aligned}
\tag{30}
$$

$\Gamma_t$ 在这里由 $u(0),v(0),u_t(0),v_t(0)$ 计算，点值均由这些局部索伯列夫范数控制。

在远离零点的区域，

$$b=\frac{\Gamma}{Ax}-\frac r{Ax}.$$

最高的一阶导数附带 $1/x$，由

$$\|\sqrt q\,w_x\|_{L^2H^k}$$

控制；其余乘积由 $w\in C H^{k-1}$ 控制。由此，对 $k\ge6$，得到真正的班纳赫空间估计

$$
\boxed{\|\mathcal N(w)\|_{\mathcal Y_k}
\le C_N\|w\|_{\mathcal Z_k}^3,}
\tag{31}
$$

以及

$$
\boxed{
\|\mathcal N(w)-\mathcal N(\widetilde w)\|_{\mathcal Y_k}
\le C_N(\|w\|_{\mathcal Z_k}+\|\widetilde w\|_{\mathcal Z_k})^2
\|w-\widetilde w\|_{\mathcal Z_k}.
}
\tag{32}
$$

### 2. 非线性存在性定理

记式（27）定义的线性解算子为

$$\mathcal G_0(F;g_+,g_-).$$

原问题成为

$$w=\mathcal G_0(\mathcal N(w);g_+,g_-).\tag{33}$$

若输入数据范数不超过 $\varepsilon$，取半径 $R_0=2C_L\varepsilon$。当

$$C_LC_NR_0^2$$

足够小时，式（31）—（32）使右侧成为该闭球上的收缩映射。

**定理：全线小数据混合边值适定性。** 固定 $A>0,d>0,T>0$ 和整数 $k\ge6$。存在 $\varepsilon=\varepsilon(A,d,T,k)>0$，使任意实数据

$$
g_+,g_-\in\mathcal D_k,\qquad
\|g_+\|_{\mathcal D_k}+\|g_-\|_{\mathcal D_k}<\varepsilon
$$

都确定唯一的小解

$$\mathbf a\in\mathcal Z_k$$

满足式（7）、（9）、（11）。解映射对混合数据是实解析的。

这个定理保留两个任意空间函数的自由度；没有有限模态、孤子参数或空间仿射涨落限制。存在性证明没有预设 $\Phi_t$。

### 3. 加入空间矩，控制渐近与实际谱问题

为避免只得到无权解，还必须传播空间矩。精确交换关系是

$$
\begin{aligned}
(\mathcal L_0-jc)(x^jw)
={}&x^jF+2j\mathsf C D(x^{j-1}w)
-j(j-1)\mathsf C x^{j-2}w.
\end{aligned}
\tag{34}
$$

而本系统特殊的零点闭合给出

$$
\boxed{
x^j\mathcal N(w)
=-\frac{\mathsf R}{A}D\!\left[x^{j-1}(\Gamma-r)w\right]
+\frac{j\mathsf R}{A}x^{j-2}(\Gamma-r)w.
}
\tag{35}
$$

当 $j=1$ 时，最后一项就是 $\mathsf R bw$，通过光滑延拓解释，不引入新奇性。

式（35）的重要性是：第 $j$ 阶空间矩的强迫只需要第 $j-1$ 阶及以下空间矩。结合负移位逆算子，可以逐阶推进。

具体地，取整数 $m\ge1$、$k\ge2m+6$，定义

$$
\mathcal D_{k,m}
=\{g:x^jg\in\mathcal D_{k-j},\ 0\le j\le m\}.
\tag{36}
$$

若混合数据在这个空间中足够小，则上述解还满足

$$
\boxed{x^j\mathbf a\in\mathcal Z_{k-j},\qquad 0\le j\le m.}
\tag{37}
$$

这是有限但任意预先指定阶数的加权正则性定理；**没有未经证明地把它升级为一个施瓦茨开放邻域定理。**

特别地，当 $m\ge1$，

$$
p,s\in C(I;L^1\cap L^2),\qquad xp,xs\in C(I;L^2).
$$

公共场满足

$$
b(0,t)=-\frac{r_x(0,t)}A,\qquad
b(x,t)=\frac{\Gamma(t)}{Ax}+o(|x|^{-1}),
\tag{38}
$$

而原物理场由

$$
U_0=b+p,\quad U_1=b-p,\qquad w_0=Ax+s,\quad w_1=Ax-s
$$

重构，确实满足最初的半离散系统。

组件积分也实际守恒：

$$
\int p\,dx=\frac12\left(\int g_+\,dx+\int g_-\,dx\right),
$$

$$
\int s\,dx=\frac1{4d}\left(\int g_+\,dx-\int g_-\,dx\right).
\tag{39}
$$

要固定组件积分，只需在数据空间中施加这两个线性条件，不会损失函数自由度。

## 六、中心取值：已经能证明什么，仍不能证明什么

定义自然的物理初值空间

$$
\mathscr X_{k,m}
=\left\{z=(p,s):x^jz\in H^{k-j-1},\ 0\le j\le m\right\},
\tag{40}
$$

其范数由这些加权索伯列夫范数组成。这里完全没有使用解历史。

混合解给出实解析映射

$$\mathcal E_t:(g_+,g_-)\longmapsto z(t)\in\mathscr X_{k,m},$$

以及

$$
z\in C(I;\mathscr X_{k,m})\cap H^1(I;\mathscr X_{k-1,m}).
\tag{41}
$$

但要定义物理初值流，必须进一步把

$$\mathcal E_t=\Phi_t\circ\mathcal E_0\tag{42}$$

落实为单值、正则的映射分解。

### 1. 真空处的中心线性化单射

因为非线性是三次的，

$$
\mathcal E_0(g)=\mathcal E_0^{\rm lin}(g)+O(\|g\|^3).
\tag{43}
$$

线性物理方程在傅里叶空间为

$$
u_t-c\xi u_\xi=\xi^2v,\qquad
v_t+c\xi v_\xi=\xi^2u.
\tag{44}
$$

在任意有限对数频率区间上，这是系数有界的双向输运系统。若中心数据为零，局部依赖域上的能量唯一性迫使解为零；扩大区间即可覆盖所有非零频率。因此

$$\mathcal E_0^{\rm lin}\text{ 单射}.$$

其像包含由光滑紧频率初值生成的线性轨道的中心值，所以具有真正的无限函数维数。这里紧频率函数只用于验证线性映射性质，**没有把最终物理条件域限制为固定频带**。

### 2. 但自然初值范数下的可微流存在明确障碍

在高频 $R$ 附近选取非负平滑傅里叶平台，初始幅值为 $e^{-R}$。由式（44）的特征线和耦合项的正性，对任意固定 $\tau>0$，可以在一个高频子区间上得到

$$
|\widehat u(\tau,\xi)|
\ge\exp\!\left(\tau R^2e^{-2c\tau}-R\right)
\tag{45}
$$

这一类型的下界。初值的所有固定阶加权索伯列夫范数趋于零，而正时间输出范数发散。

这些线性初值都有实际的有限时紧频率轨道，因而对应合法的混合数据方向。若存在一个在真空处对 $\mathscr X_{k,m}$ 范数可微的中心演化映射，则由式（42）的链式法则，

$$
D\Phi_\tau(0)\,\mathcal E_0^{\rm lin}=\mathcal E_\tau^{\rm lin}.
$$

左边要求一个有界线性算子实现式（44）的正时间推进，与式（45）矛盾。

因此可以明确排除：

> 在真空处，以自然加权索伯列夫初值范数作为切空间拓扑，并同时实现整个上述小混合解族的可微局部流。

这不排除更强的内在函数空间、具有损失的尺度流、条件连续流，或避开真空的其他区域；本证明没有覆盖那些对象。

### 3. 非线性中心唯一性仍未完成

线性化单射不能自动升级为非线性 $\mathcal E_0$ 单射，因为它没有有界逆，不能直接使用逆函数定理。

混合解在较短时间窗上的限制当然仍满足原方程；当其新端点迹属于相应较低阶数据空间时，混合唯一性保证重新求解得到同一段轨道。但这是**用两个新端点重启**，不是证明一个中心物理场唯一决定轨道。

一般反向抛物问题的条件稳定性研究也明确区别于通常初值适定性；针对有界域耦合抛物系统的结果不能直接覆盖这里的无界 $Ax$、相反扩散方向和点值闭合。〔原报告引文尚未核验〕

所以，新定理没有借助人为历史拓扑掩盖不适定性。相反，它把这一缺口明确暴露出来了。

## 七、在这批真实全线解上检查谱与辛结构

### 1. 实际谱泛函现在可以与真实物理轨道相遇

取 $m\ge3$，并按上面要求选取足够大的 $k$。则 $p,s\in L^1$，且 $x^2p,x^2s\in L^1$。在振荡轮廓

$$(-2d,2d)\cup i\mathbb R$$

的任意紧子弧上，沃尔泰拉构造实际定义全线散射矩阵与左右半线矩阵

$$\mathcal S_\lambda,\qquad H_+(\lambda),\qquad H_-(\lambda).$$

它们对物理场在这些加权空间中解析地依赖；上述矩条件也足以处理一次谱参数微分。

原拉克斯恒等式的空间边界项现在有实际衰减控制，因此沿这些解可以得到

$$
\frac d{dt}F_\lambda=-v(\lambda)\partial_\lambda F_\lambda
\tag{46}
$$

以及相应的半线矩阵演化。于是，实带内的自主谱时钟和归一化谱形状积分，在其窗口有效时，确实成为**这些真实非线性轨道上的自主守恒泛函**，不再只是等时向量场恒等式。

这一正则谱窗口也非空：中心映射的线性像包含足够丰富的函数方向，而谱迹的二阶项在一般这样的方向上不是常数；三次非线性修正不会消去一个已经非零的有限阶验证量。

但是，泛函有定义还不等于辅助向量场切向。对于原安全紧支撑权重，利用远场伴随矩阵估计和谱分部积分，在足够的有限矩条件下至少可证明谱梯度属于 $H^1$。因此旧括号表达式

$$
-\frac1{2h}\int\left[
(\mathcal dI_\rho)_pD(\mathcal dI_\sigma)_s+
(\mathcal dI_\rho)_sD(\mathcal dI_\sigma)_p
\right]dx
\tag{47}
$$

实际收敛，并可由光滑衰减逼近延续原来的零值结论。

**尚未证明的是**

$$
J\mathcal dI_\rho\in T_z\bigl(\mathcal E_0(\text{小混合数据})\bigr).
$$

即使其属于某个较弱的环境空间，也不能据此宣称它在中心值集合上生成合法流。因此，式（47）目前仍不足以构成该中心值集合上的完整泊松代数。

### 2. 旧弱辛形式在环境空间有定义，但真实解族并没有消除其缺陷

在固定组件积分的叶上，第一空间矩控制给出

$$
\|D^{-1}f\|_2\le2\|xf\|_2\qquad\left(\int f\,dx=0\right).
$$

因此旧形式

$$
\Omega(\xi,\eta)=-2h\int\left[
(D^{-1}\xi_s)\eta_p+(D^{-1}\xi_p)\eta_s
\right]dx
\tag{48}
$$

在相应加权环境空间上连续、闭合且弱非退化。$I_b,\Gamma,K,\alpha$ 也都有实际定义，原来的恒等式仍成立：

$$
\mathcal dK=\alpha-2hI_b\,\mathcal d\Gamma,\qquad
\mathcal d\alpha=2h\,\mathcal dI_b\wedge\mathcal d\Gamma.
\tag{49}
$$

更重要的是，非闭合性没有因混合边值存在性而自动消失。

例如，在零积分施瓦茨验证场

$$p=s=f,\qquad f=(1-2x^2)e^{-x^2}$$

处，选择两个零积分变分

$$\xi=(f,0),\qquad\eta=(xe^{-x^2},0).$$

则

$$
\mathcal d\Gamma[\xi]=1,\qquad\mathcal d\Gamma[\eta]=0,
$$

$$
\mathcal dI_b[\xi]=0,\qquad
\mathcal dI_b[\eta]=-\frac{\sqrt\pi}{2\sqrt2\,A}.
\tag{50}
$$

故 $\mathcal dI_b\wedge\mathcal d\Gamma\ne0$。

用中心线性映射像中的光滑紧频率方向逼近这些验证场及变分，再使用

$$
\mathcal E_0(\varepsilon g)
=\varepsilon\mathcal E_0^{\rm lin}(g)+O(\varepsilon^3),
$$

得到：在任意小的混合数据球内，都存在实际中心场，使

$$
\boxed{
\mathcal d(\mathcal E_0^*\alpha)
=2h\,\mathcal d(I_b\circ\mathcal E_0)
\wedge\mathcal d(\Gamma\circ\mathcal E_0)\ne0.
}
\tag{51}
$$

因此，**旧结构的障碍已经出现在真实小解族内，而不只是出现在没有解流的任意等时场上。** 凡是试图在这整个小解族上保留旧形式并生成物理时间，都必须面对式（51）。

### 3. 解流拉回结构仍不能直接落地

公式

$$
\Omega_*=
\pi^*(\Omega|_\Sigma)+d\tau\wedge dH_*,\qquad
\pi(z)=\Phi_{-\tau(z)}z
$$

仍缺少由中心物理场定义的单值、正则 $\Phi_t$。

目前可以在混合数据空间中追踪一条已经构造的轨道，但不能把这件事换名为原物理相空间上的 $\Phi_t$。那样会重新引入你明确要求避免的历史参数拓扑。

即使中心流得到解决，还要重新检查受限二形式的弱非退化性、谱辅助向量场切向性及完整积分叶结构。增加 $H_*$ 不会自动解决这些问题。

## 八、完整谱重构仍缺少的，不是更多谱迹积分

在这批全线解上，左右半线矩阵已经是实际数据，而不是形式对象。真空处的完整线性反演可以保留。但它还不能升级为非线性坐标定理，原因现在可以更具体地表达。

首先，若只给所有紧谱区间上的一致收敛拓扑，逃向高谱频率的数据仍会使逆映射不连续。必须规定覆盖整条谱轮廓的加权数据范数，而不是仅说“知道所有谱参数”。

其次，当前真实小解一般允许 $p(0)s(0)\ne0$。零点处的高谱缩放模型仍是

$$
\Phi_\zeta=
\begin{pmatrix}A\zeta/2&p_0/2\\s_0&-A\zeta/2\end{pmatrix}\Phi,
$$

对应的标量方程为

$$
\phi_1''=
\left(\frac{A^2\zeta^2}{4}+\frac A2+\frac\Gamma2\right)\phi_1.
\tag{52}
$$

其抛物柱阶数依赖 $\Gamma/A$。因此，统一的非线性谱范数与重构归一化必须处理这个随物理场变化的零点连接，不能只使用真空的线性傅里叶范数。

第三，实际半线时间方程为

$$
(X+v\partial_\lambda)H_\pm
=(AW_\lambda-\Gamma V_\lambda)H_\pm-H_\pm B_0,
\tag{53}
$$

而 $B_0$ 含 $p_0,s_0,p_1,s_1$。要得到闭合谱演化，必须证明这些零点数据能从当前完整谱数据中恢复，并且左右恢复值满足光滑拼接。它们不能被任意指定为外部边界驱动。

所以，当前尚缺的是一个真正的非线性定理：

> 在上述真实解所处的某个明确加权条件域上，经过正确的零点连接归一化，完整半线矩阵数据与物理场之间存在正则的双向映射；其值域条件由式（53）的物理演化保持。

这项定理必须包含相位与连接数据，而不是要求谱迹积分单独重构场。它也不能仅由线性单射或一般逆散射框架推出。

## 九、当前结论与剩余的三个核心命题

本轮已经得到的最强结果是：

**对 $A>0$、任意固定有限 $T$，在明确的加权索伯列夫混合数据空间中，原始全线非线性系统存在唯一小解，并解析地依赖两个端点函数。零点闭合、公共场渐近、组件积分和任意预先指定有限阶空间矩均可实际控制。** 这不是有限维约化，也没有修改物理时间方程。

但完整可积性仍然缺少三个必须贯通的环节。

**第一，中心初值的恢复与正则重启。** 需要证明非线性中心映射的单射性，并找到由物理场自身定义的条件与拓扑，使中心场能够正则地恢复轨道。自然加权索伯列夫范数下，包含整个小混合解族的真空可微流已经被排除；更强的尺度空间或非真空区域仍未排除，但尚未构造。

**第二，同一个条件域上的物理哈密顿结构。** 旧形式在新真实解族中仍有式（51）的非闭合缺陷。新的非局域结构需要在第一项给出的实际相空间上验证，而不能只在混合历史参数空间上构造后再宣称已经约化到物理场。

**第三，完整非线性谱坐标与刘维尔完备性。** 除了积分的实际定义与对合表达式，还需证明完整数据的重构、相位方向和零点连接的合法性，以及所采用定义要求的

$$
\overline{\operatorname{span}\{X_I\}}
=\ker D\mathcal I
=\left(\overline{\operatorname{span}\{X_I\}}\right)^{\Omega_*}
$$

等完备性条件。这里的拓扑、切空间和辛形式必须来自前两项的同一个对象。

**因此，最终回答仍是：现在尚不能在一个已经明确建立的原物理初值条件域上宣布无限维刘维尔可积。** 不过，“全线非线性小解根本没有构造”已经不再是当前缺口；现在的主要断点是**两端适定解族能否成为正则的物理初值相空间，以及在该相空间上能否完成新的哈密顿结构和带零点连接的完整谱重构**。本轮没有把混合边值存在性包装成初值流，也没有把某种拓扑或旧结构的失败解释为系统普遍不可积。

原报告另提及符号复核脚本，但该脚本未在本次整理中取得；不得把代数脚本检查等同于分析证明已审定。
