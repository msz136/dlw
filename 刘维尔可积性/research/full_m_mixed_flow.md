# 全 M 周期混合解旧稿复核与新的中心单射定理

2026-10-11。周期空间、任意固定有限 M 的实际混合解与中心唯一性推导。

## 1. 先区分旧结果与本次新增

旧稿 [MIXED_TIME_EXISTENCE.md](../../Workspaces/dlw_general_field_20261006/MIXED_TIME_EXISTENCE.md) 已经给出任意固定有限 M≥2 的剪切、热核混合边值收缩、解析依赖、内点平滑、端点作用量与有限守恒块的真实轨道实现。本次先复核这些已有结果。

本次复核确认其混合解构造成立，补清内点平滑、端点作用量的共同配对域，以及有界 $q(t)$ 下的正则区别。本次真正新增的是第 5 节：**周期混合解的中心取值为单射，线性化中心取值也为单射。** 证明是自足的时间 Carleman 估计；没有假设 Sobolev 初值半群或逆谱坐标。

新增单射只解决实际解之间的 Cauchy 唯一性，不解决任意初值的存在性、连续逆、Banach 相空间流或无限维 Liouville 完备性。

## 2. 精确剪切、非线性与旧混合定理

固定空间圆周 $\mathbb T_L$、有限 $M\ge2$、$h>0,c\ne0,\beta=h^2/32$。令 $\Pi$ 为格点平均、$P_0=I-\Pi$，

$$
R=(\delta_-|_{\operatorname{im}P_0})^{-1}M_-P_0,\qquad R^*=-R,\quad RP_0=R .
$$

$R$ 是有限实矩阵，和 $D=\partial_x$ 交换。取 $\Pi p=\Pi s=0$，

$$
w=c\mathbf1+s,\quad
b=(q(t)-\Pi(ps))/c,\quad U=b\mathbf1+p .
$$

这是原方程在 $c\ne0$ 分支的准确平均闭合，不额外指定 $b$。设

$$
v=p+\tfrac12Rs,\quad p=v-\tfrac12Rs .
$$

直接代入得

$$
v_t=-D^2v+D N_v(v,s;t),\qquad
s_t=D^2s+D N_s(v,s;t), \tag{1}
$$

$$
\begin{aligned}
N_s&=-P_0(Uw)=-cp-bs-P_0(ps),\\
N_v&=-P_0(U^2/2+\beta w^2)-\tfrac12R P_0(Uw)\\
&=-bv-\tfrac c2Rp-2\beta cs-\tfrac12P_0(p^2)
-\beta P_0(s^2)-\tfrac12R P_0(ps). \tag{2}
\end{aligned}
$$

第二阶交叉项确实完全抵消。$b^2$ 在 $P_0(U^2)$ 中消失，故 $N_v,N_s$ 至多三次，不是四次；$q(t)$ 只作为有界标量系数进入。

对 $r>1/2$，$H^r(\mathbb T_L;\mathbb R^M)$ 是 Banach 代数。固定格点平均零及各组件空间平均；这些均由 $D$ 型右端保持。规定

$$
s(-T)=g_s,\qquad v(T)=g_v .
$$

旧稿的 mild 方程在 $[-T,T]$ 上为

$$
\begin{aligned}
v(t)&=e^{(T-t)D^2}g_v-\int_t^T e^{(\tau-t)D^2}D N_v(y(\tau);\tau)d\tau,\\
s(t)&=e^{(t+T)D^2}g_s+\int_{-T}^t e^{(t-\tau)D^2}D N_s(y(\tau);\tau)d\tau .
\end{aligned} \tag{3}
$$

$\|D e^{\sigma D^2}\|_{H^r\to H^r}\le(2e\sigma)^{-1/2}$。在固定球上 $N$ 的 Lipschitz 常数为
$C_{M,h,c,r}(1+\|q\|_\infty+R+R^2)$，所以积分常数为 $O(\sqrt T)$。取 $T$ 足够小，得到唯一球内 $C_tH^r_x$ 解，解析依赖混合端点。固定任意组件均值时可围绕相应常数场取球，结论相同。

这些解重构后满足原隐式 DLW 方程及 $\Pi w=c,\Pi(Uw)=q(t)$。$q$ 有界可测时按分布/Carathéodory 理解；常数 $q$ 下是旧稿的自治方程。

## 3. 旧稿内点平滑的严格补充

在稍大的闭内区间 $J'\Subset(-T,T)$ 已知 $y\in L^\infty H^\rho$，则 $N(y,t)\in L^\infty H^\rho$。对较小 $J\Subset J'$，把 (3) 的积分拆成靠近 $t$ 的部分与离 $t$ 有固定距离的尾部。尾部及两个规定端点的热半群任意平滑；近部使用

$$
\|D e^{\sigma D^2}\|_{H^\rho\to H^{\rho+\alpha}}
\le C_\alpha \sigma^{-(1+\alpha)/2},\qquad 0<\alpha<1 .
$$

奇性可积，得 $y\in CH^{\rho+\alpha}(J)$。用有限个嵌套区间重复，任意固定空间阶均得到控制，因此同一内点区间上 $y$ 空间 $C^\infty$。有界可测时间源也产生连续空间 Sobolev 轨迹，因上述算子值时间核属于 $L^1$，其平移在 $L^1$ 中连续。

若两个混合输入均空间光滑，可直接在整个闭区间重复这个提升：规定端点的热项在所有 $H^\rho$ 中有界，不必缩短既有 $T$。故该解空间光滑直到两端。

必须区分时间正则性：

- $q\in L^\infty$：内点 $y\in W^{1,\infty}(J;H^m)$ 对任意固定 $m$（先提升两阶再用 (1)）；通常不能声称时间 $C^\infty$。
- $q$ 连续：约化 $y$ 内点 $C^1$ 时间；重构 $U$ 的格点均值只继承 $q$ 的时间正则性。
- $q\in C^1$：重构 $U,w$ 是通常意义的经典物理解；$q$ 光滑时内点时间、空间均光滑。旧稿固定 $q$ 属于此情形。

上述平滑本身没有依赖有限 Fourier 数值检验。

## 4. 端点作用量与无限层级的共同域

剪切保持约化常数 Poisson 算子

$$
J=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix}.
$$

在固定组件空间均值叶上，令 $Q=s-\bar s$、$P=D^{-1}(v-\bar v)$。$D^{-1}$ 取空间零均值逆导数；则
$Q_t=K_P,\ P_t=-K_Q$，$K$ 是旧 Hamiltonian 在剪切后的同一泛函。这里没有用端点能量替换物理 Hamiltonian。

对足够光滑解及端点变分，

$$
S(Q_-,P_+)=\langle P_+,Q(T)\rangle
-\int_{-T}^T(\langle P,Q_t\rangle-K(P,Q))dt
$$

满足

$$
dS=\langle P(-T),dQ_-\rangle+\langle Q(T),dP_+\rangle . \tag{4}
$$

证明只有时间分部积分：Hamilton 方程使内部变分抵消；混合端点给 (4)。在 $r>1/2$ 也可用弱配对解释：
$P\in H^{r+1},Q_t\in H^{r-2}$，$P_t\in H^{r-1},\delta Q\in H^r$。配对成立分别因为 $r+1\ge2-r$、$r\ge1-r$。Hamiltonian 中 $\int s p_x,\int sRs_x$ 亦用该双对偶配对；其余多项式由 $H^r$ 代数控制。光滑端点逼近、(3) 的解析依赖与方程的 $H^{r-2}$ 连续性延伸 (4)。

以 $\Omega=dQ\wedge dP$ 的符号约定，(4) 给

$$
E_t^*\Omega=E_a^*\Omega,\qquad a,t\in[-T,T]. \tag{5}
$$

这是实际轨道族的闭二形式等式；它不自动证明中心参数空间上的形式非退化。

无限层级的共同**定义域**可取固定平均叶的
$\mathcal P_\infty=C^\infty(\mathbb T_L;\mathbb R^{2M})\cap\{\Pi p=\Pi s=0\}$。
每个固定阶 PDO 留数是有限阶局部表达式，所以每个 $I_n$、其光滑变分梯度与形式向量场 $J\,dI_n$ 同时在这个 Fréchet 域有意义。同一真实混合解内点也在此共同域，不要求完整 PDO 级数收敛。

但“所有泛函都定义”不等于“所有辅助 Hamiltonian 流都实际存在并保持中心取值像”。后者仍未知。本文没有独立重证旧稿的所有阶 Lax、对合与有限块独立性代数；共同域讨论说明这些已验证身份应在哪个域使用，不把阅读旧稿当作代数证明。

有界 $q(t)$ 的推广亦非新的自治闭合：旧 periodic_reduction.md 已给移动坐标 $U'=U(x-A(t),t)+A'(t),w'=w(x-A(t),t)$，令 $A'=-q/c$ 可归到零 $q$。有界 $q$ 下 $A$ 绝对连续，按弱链式法则实现该规范。对自主守恒层级及时间平移，下文固定 $q$。

## 5. 新增：自足的中心 Cauchy 唯一性

### 5.1 有界一阶扰动的唯一性引理

在空间圆周上令

$$
A=\operatorname{diag}(-D^2,D^2),\qquad |A|=-D^2I,\qquad P_*= \partial_t-A.
$$

格点维数任意有限。设实际解差 $z$ 在紧时间区间满足
$z\in H^1_tL^2_x\cap L^2_tH^2_x$，

$$
P_*z=B(x,t)z_x+C_0(x,t)z,\qquad
\|B\|_\infty\le b,\quad\|C_0\|_\infty\le a . \tag{6}
$$

若 $z(t_0)=0$（$L^2$ 迹），则整个该区间 $z=0$。

先證 $t\ge t_0$，平移 $t_0=0$。在 $t<0$ 延零；零时间迹使分布时间导数没有 Dirac 项，延拓仍属所需图空间。取时间截断 $\chi=1$ 于 $[0,t_1]$，在 $t_2>t_1$ 前降到零；负时间端也截断但那里 $z=0$。令

$$
\phi(t)=e^{-Kt},\quad f=e^{\lambda\phi}\chi z,\quad
Q_\lambda=e^{\lambda\phi}P_*e^{-\lambda\phi}
=\partial_t-A-\lambda\phi' .
$$

对紧时间支撑的图空间函数有精确恒等式

$$
\|Q_\lambda f\|_2^2
=\|f_t\|_2^2+\|(A+\lambda\phi')f\|_2^2
+\lambda\int\phi''\|f(t)\|_2^2dt . \tag{7}
$$

关键符号是正的 $+\lambda\phi''$：交叉项
$-2\lambda\int\phi'\langle f_t,f\rangle$
分部积分后就是这一项。$A$ 自伴，且时间独立。

恒等式的合法性：先做空间谱截断与时间卷积，得到光滑紧支撑函数；在 $H^1_tL^2\cap L^2_tH^2$ 图范数中强逼近，有限固定 $\lambda$ 下各项连续，故 (7) 成立。无需对 $B,C_0$ 求时间导数。

记 $S=\|(A+\lambda\phi')f\|_2$。由 $|A|=-D^2I$ 和 $\||A|f\|=\|Af\|$，点时刻有

$$
\|f_x\|_2^2=\langle|A|f,f\rangle
\le\|(A+\lambda\phi')f\|_2\|f\|_2
+\lambda|\phi'|\|f\|_2^2 . \tag{8}
$$

而 (6) 给

$$
Q_\lambda f=Bf_x+C_0f+d,\qquad d=e^{\lambda\phi}\chi' z .
$$

平方后不等式为

$$
\|Q_\lambda f\|_2^2
\le4b^2\|f_x\|_2^2+4a^2\|f\|_2^2+2\|d\|_2^2.
$$

用 (8) 及 Young 吸收半个 $S^2$，误差至多
$(8b^4+4a^2)\|f\|_2^2+4b^2\lambda\int|\phi'|\|f\|_2^2$。
选 $K\ge8b^2+1$，则 $\phi''=K|\phi'|$ 吸收后一项。再选 $\lambda$ 足够大吸收零阶项，得到

$$
\lambda\int\phi''|f|^2\le C\|d\|_2^2 . \tag{9}
$$

$\chi'$ 的非零解支撑在 $[t_1,t_2]$。任取 $0<t_*<t_1$，$\phi(t_*)>\phi(t_1)$，于是 (9) 给

$$
\lambda c_*e^{2\lambda\phi(t_*)}\|z\|_{L^2([0,t_*]\times\mathbb T)}^2
\le C_\chi e^{2\lambda\phi(t_1)}
\|z\|_{L^2([t_1,t_2]\times\mathbb T)}^2.
$$

$\lambda\to\infty$ 得左侧未加权范数为零。$t_*,t_1,t_2$ 可覆盖任意较晚紧内区间。反向时间把 $A$ 换为 $-A$，仍自伴且同一 $|A|$，证明较早一侧。引理得证。

### 5.2 用于真实非线性混合解

两条 (1) 的真实解 $y,\widetilde y$ 有差

$$
P_*z=D(N(y,t)-N(\widetilde y,t))
=Bz_x+B_xz,\quad
B=\int_0^1DN(\widetilde y+\theta z,t)d\theta . \tag{10}
$$

内点空间平滑和有界 $q$ 使 $B,B_x$ 在任意紧内区间有界；方程给所需 $H^1_tL^2\cap L^2_tH^2$。因此相同内点状态推出两条轨道全部相同，再由端点连续性推出混合数据相同。

**中心单射定理。** 固定同一 $q(t)$ 及同一混合窗口与数据球，$E_{t_0}:g\mapsto(v(t_0),s(t_0))$ 对任何内点 $t_0$ 都是单射。此结论对原来的 $r>1/2$ mild 类成立，因为内点提升给了引理正则性。

解析线性化 $z=DE_{t_0}(g)\eta$ 满足 $P_*z=D(DN(y,t)z)$。同一估计给：若中心变分为零，则整条线性化轨道及端点变分为零。因此 **$DE_{t_0}(g)$ 也是单射**。

严谨术语是“实解析单射且微分单射”。Banach immersion 通常还要求分裂/有界下界，本文未得到这种性质。

### 5.3 为什么仍没有 Sobolev Banach 流

在常数平衡点，各非零空间 Fourier 模式的线性生成元为
$\operatorname{diag}(k^2,-k^2)+ik B_0$。固定任意非零格点模态，有稳定特征值
$-k^2+O(|k|)$、非零稳定 $s$ 分量。把相应真实线性轨道的混合输入 $H^r$ 范数归一到 1，则中心 $H^r$ 范数是
$O(e^{-Tk^2+O(T|k|)})$。

所以中心微分不具有有界下界，在线性化中心像上的逆无界。不能据单射调用 Banach 逆函数论，不能宣称 $C^1$ Banach embedding 或开放 Sobolev 初值流。这个线性结论本身也没有证明非线性集合逆必定不连续。

## 6. 尺度中心像与真正的部分轨道重启

固定常数 $q$，令 $C_T$ 为 $[-T,T]$ 的一个小混合数据球之中心取值像。由于第 5 节，同一物理状态对应唯一实际轨道。若状态来自较长窗口 $C_{2T}$，则对 $|\tau|<T$ 可由该真实轨道定义

$$
\Phi_\tau:C_{2T}\longrightarrow C_T,\qquad
\Phi_\tau(z)=y_z(\tau). \tag{11}
$$

目标球需按限制端点选择，必要时缩小源球；不能未经检查自动使用同一半径。具体端点限制是
$g^\tau=(s_z(-T+\tau),v_z(T+\tau))$，它仍保持全部平均。固定 $\tau$ 下该限制在端点参数中解析，(3) 的唯一性识别限制轨道；中心单射消除了“通过同一状态有不同轨道”的歧义。

当足够长的窗口同时容纳所有平移且球条件满足时，
$\Phi_\sigma\Phi_\tau=\Phi_{\sigma+\tau}$、$\Phi_0=\mathrm{id}$；这是按尺度解释的真实轨道 germ 性质。还没有在继承的 Sobolev 拓扑中证明这些图的逆连续或可微，也没有建立由物理场自身正则性给出的内在相空间。

在端点参数中 $\omega_T=E_0^*\Omega$ 是闭二形式，(5) 给不同时间的相同拉回。长窗口轨道的时间平移给短窗口端点的可微曲线，故在这些点有实际时间方向 $V$，并有

$$
\omega_T(V,\eta)=d(K\circ E_0)[\eta]. \tag{12}
$$

这是沿真实 germ 的 Hamilton 身份，使用 $\iota_{X_K}\Omega=dK$ 的符号。**尚未证明 $\omega_T$ 弱非退化**；需另外证明中心微分像的足够稠密性/可控性或其他非退化机制。不能因此称 $C_T$ 已经是辛相空间。

辅助 $I_n$ 向量场是否位于中心微分像、其真实辅助轨道是否保持这组中心像，仍未解决。第 5 节的物理 Cauchy 唯一性也没有证明逆谱完备性、最大对合族或作用角坐标。

## 7. 本次可交付结论

旧全 M 混合存在定理经独立复核可使用；内点平滑和高正则端点作用量可严密化。新增的中心与线性化中心单射来自 (7)–(10) 的完整估计。真实轨道给按窗口尺度解释的部分重启，且有闭二形式与实际 Hamilton 身份。

仍缺连续/正则状态逆、内在相空间拓扑、中心拉回形式非退化、全部辅助流切向性与存在性、非线性逆谱及无限维完备性。因此这些进展仍不是一般物理场完整 Liouville 定理。
