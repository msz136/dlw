# 混合解结构独立复核与全层级实际共同 germ 的构造

2026-10-11。独立审计与新推导；不以旧文件“已核验”的陈述代替证明。

## 0. 结论与范围

本稿的最新结论见 §11–17。§11 证明任意有限前缀的所有可缩窗口联合 germ 域为弱辛 diffeological 相域；§12 构造偶层级的真实流，因而任意有限奇、偶前缀都保留一般光滑函数源；§13 构造非平凡、在每个有限前缀生成像中稠密的可数相容共同域，具有每坐标固定正窗口及逐层真实流不变性。§14 在明确的小参数均匀平均叶上证明任意有限全 charge 块的实际独立性；§15 将光滑有限参数见证族提升到全部层级相容共同域并保留有限秩。§16 在有共同复 mixed presentation 的强子域上，通过同一基点的实际无限域切向稠密及相对轴、抛物线延拓排除内部 tangent ghost，建立合法无限弱辛结构。§17 在 §14 的背景范围内，用一份固定紧 Hilbert 参数球及 Baire 论证得到同一个实际状态上全部有限 charge 块独立。

前文 §7、§10 的未解表述保留为当时审计记录；其有限联合弱非退化、偶层级、无限一致域非平凡性及强子域无限弱辛问题分别由后续节解决。高阶固定图端点唯一性仍未证明；仅具有实时间 coherent presentation 的更大域也不自动享有 §16 的切向结论。非线性 Liouville 最大性、完整逆谱及角变量仍待解决。

本次逐式检查了 [full_m_mixed_flow.md](full_m_mixed_flow.md)、[mixed_phase_symplecticity.md](mixed_phase_symplecticity.md)，并读了本专题 GOAL、README、STATE 及其指向的原混合存在、原物理 Hamiltonian、矩阵 Lax、全阶 Poisson、独立性证明。

三项审计结论成立，适用条件必须保留：

1. 同一有界平均通量 $q(t)$ 下，真实二阶周期混合解的中心与线性化中心单射，来自合法的图空间 Carleman 估计。
2. 光滑到闭端点、固定物理平均叶的二阶混合参数开集上，原形式的拉回弱非退化；证明使用完整端点唯一性及作用量 Hessian，不用稠密像或满射逆。
3. 一个有限阶物理 Hamiltonian 场若与物理场精确对易并保持平均，确实是混合中心像的微分切向场。此结果本身没有实际辅助积分曲线。

首先从矩阵密度递推导出**所有奇阶谱 Hamiltonian 场的常系数偶阶主部**；在已有混合参数上再次做高阶混合边值收缩，可构造每个奇辅助场的真实解，并归纳构造任意指定有限前缀

\[
K,\quad P_{\rm mom},\quad C_3,C_5,\ldots,C_{2N-1}
\]

的共同多时间解。每个前缀仍以两个任意光滑周期函数为混合输入，保留全有限 $M$ 的全部格点函数自由度；不是有限维孤子或 Fourier 截断族。

这些共同解族也能实现原有限守恒块的独立性见证，见 §7.1；实际共同流的构造没有使一般场退化为有限维族。

高阶辅助中心唯一性使用**复时间菱形上的解析收缩**，不是把二阶 Carleman 误用到高阶。由此可以对每个有限前缀定义由实际共同解组成的中心 germ 域及真实换窗局部共同流。新域有兼容闭形式和沿实际共同流的 Hamilton 身份。

这些有限共同域不等于原二阶中心像的开放子集；不能将任意较短前缀中的状态自动扩成更高阶共同 germ。§13–17 另外构造并证明宽广的强可数共同域、其弱辛结构和上述指定背景范围内的同点可数独立性。高阶固定 mixed 图的辅助端点唯一性仍不能由内点解析推出，本文的无限弱辛结论使用所有可缩强 presentations 及其内部切向结构。谱完备性和 Liouville 极大性尚未证明。

## 1. 平均、物理分支与原结构

采用原隐式 DLW：

\[
\delta_-\{U_t+D(U^2/2+\beta w^2)\}
+D^2(\delta_-U+M_-w)=0,
\qquad w_t=-D(Uw)+D^2w,\qquad \beta=h^2/32.
\]

周期连续空间和周期格点先强制

\[
\Pi w=c,\qquad c_t=0,\qquad \Pi(Uw)=q(t).
\]

这里 $c$ 是物理守恒平均，而 $q(t)$ 是原方程留下的时间自由模，原方程没有推出 $q_t=0$。本报告不为原方程添加 $c$ 或 $\Gamma=q$ 的数值限制。$c\ne0$ 是被研究的正则分支，所有非零实 $c$ 都允许；固定某叶的 $c$ 是 Poisson 叶描述。零平均分支另需其约束分析。

令 $p=P_0U,s=w-c\mathbf1,z=\Pi(ps)$，则

\[
U=p+b_0\mathbf1,\qquad b_0=(q-z)/c,\qquad
R=(\delta_-|_{\operatorname{im}P_0})^{-1}M_-P_0,\qquad
R^*=-R,\qquad v=p+Rs/2.
\]

格点零均值及每个组件的空间均值均由右端的 $D$ 保持。以 $h\sum_j\int$ 配对的准确约化括号是

\[
J=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix}.
\]

在固定组件空间均值叶上取

\[
Q=s-\bar s,\qquad P=D^{-1}(v-\bar v),\qquad
\Omega((Q_1,P_1),(Q_2,P_2))
=\langle Q_1,P_2\rangle-\langle Q_2,P_1\rangle.
\]

物理 Hamiltonian 为原 $H_{\rm full}-qh\sum\int U$ 的约束重构，不是另加的端点能量。准确地

\[
K_q=K_0+(q/c)P_{\rm mom}-hMLq^2/(2c),
\qquad P_{\rm mom}=h\sum_j\int p_js_j,
\qquad X_{P_{\rm mom}}=-D(v,s).
\tag{1.1}
\]

因此 $X_{K_q}=X_{K_0}-(q/c)D(v,s)$。先构造任意常数 $q_0$ 规范的共同域，不等于先验固定物理通量；第 9 节恢复任意 $q(t)$。

原式与准确重构来源：[periodic_reduction.md](../../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md)。

## 2. 二阶 Carleman：逐项独立核验

设

\[
A=\operatorname{diag}(-D^2,D^2),\qquad |A|=-D^2I,
\qquad z_t-Az=Bz_x+Cz,
\]

其中 $B,C\in L^\infty$，且

\[
z\in H^1_tL^2_x\cap L^2_tH^2_x.
\]

在已知零 $L^2$ 时间迹处向一侧延零，不产生 Dirac 项；延拓仍属上述图空间。时间截断后，空间 Fourier 截断及时间卷积在

\[
\|f\|_2+\|f_t\|_2+\|Af\|_2
\]

中强逼近；它们与时间独立 $A$ 交换。因此下列恒等式不只是形式分部积分。

对紧时间支撑 $f$，令 $\phi=e^{-Kt}$，则

\[
\| (\partial_t-A-\lambda\phi')f\|_2^2
=\|f_t\|_2^2+\|(A+\lambda\phi')f\|_2^2
+\lambda\int\phi''\|f(t)\|_{L^2_x}^2dt.
\tag{2.1}
\]

两项交叉项分别为 $-2\int\langle f_t,Af\rangle=0$ 和

\[
-2\lambda\int\phi'\langle f_t,f\rangle
=\lambda\int\phi''\|f\|^2.
\]

符号为正。相反扩散不妨碍此恒等式，因为 $A$ 自伴，且

\[
\||A|f\|=\|Af\|.
\]

记 $S=\|(A+\lambda\phi')f\|_2$。准确的整体一阶估计是

\[
\|f_x\|_2^2
\le S\|f\|_2+\lambda\int|\phi'|\|f(t)\|^2dt.
\tag{2.2}
\]

取 $f=e^{\lambda\phi}\chi z$，$d=e^{\lambda\phi}\chi'z$，则

\[
\|Q_\lambda f\|_2^2
\le4b^2\|f_x\|_2^2+4a^2\|f\|_2^2+2\|d\|_2^2,
\quad b=\|B\|_\infty, a=\|C\|_\infty.
\]

用 $4b^2S\|f\|\le S^2/2+8b^4\|f\|^2$，选 $K\ge8b^2+1$，再在固定截断区间选足够大 $\lambda$，由 $\phi''=K|\phi'|$ 吸收所有误差，得

\[
\lambda\int\phi''\|f(t)\|^2dt\le C_\chi\|d\|_2^2.
\tag{2.3}
\]

若 $\chi=1$ 于 $[0,t_1]$、非零解上的 $\chi'$ 支撑于 $[t_1,t_2]$，则对 $0<t_*<t_1$

\[
\lambda c_*e^{2\lambda\phi(t_*)}
\|z\|_{L^2([0,t_*]\times\mathbb T)}^2
\le C_\chi e^{2\lambda\phi(t_1)}
\|z\|_{L^2([t_1,t_2]\times\mathbb T)}^2.
\]

权重间隙使 $\lambda\to\infty$ 时左侧未加权范数为零；任意较晚内区间可这样覆盖。逆时间将 $A$ 改成 $-A$，仍有同一 $ |A| $，故另一侧相同。

真实解差满足

\[
z_t-Az=D(N(y,t)-N(\widetilde y,t))=Bz_x+B_xz,
\quad B=\int_0^1DN(\widetilde y+\theta z,t)d\theta.
\]

内点空间提升及有界 $q(t)$ 给有界 $B,B_x$ 和图空间正则性，所以中心唯一性适用。线性化 mild 方程同样提升，故中心微分也单射。这一步必须检查线性化提升，不能由非线性单射直接推出。

对光滑端点，全区间热核提升用 $0<\alpha<1$、奇性 $sigma^{-(1+\alpha)/2}$ 反复迭代，给闭区间空间光滑；自治情况下时间导数也光滑。因此原弱辛证明需要的**端点版**二阶唯一性也成立。

以上确认源文 §5 的核心证明；未得到 Sobolev 连续逆、闭像或普通初值存在。

## 3. 原混合参数弱辛与微分切向性

令

\[
\mathscr E=\{f\in C^\infty(\mathbb T_L;\mathbb R^M):
\Pi f=0, \int f_jdx=0\ \forall j\},
\quad g=(a,b)=(Q(-T),P(T)).
\]

规定输入的 Sobolev 空间必须是

\[
X_r=(\mathscr E\cap H^r)\times(\mathscr E\cap H^{r+1}),
\tag{3.1}
\]

因为 $v(T)=\bar v+Db$，不是两个同阶 $H^r$ 输入。平滑参数开集是低阶开球与 $\mathscr E^2$ 的交。

对原实际解图 $\mathcal G_T(g)$，type-II 作用量给

\[
dS=\langle P_-,da\rangle+\langle Q_+,db\rangle.
\]

设 $\mathcal K=D_bP_-$、$\mathcal L=D_aQ_+$。Hessian 对称给

\[
\langle a_1,\mathcal Kb_1\rangle
=\langle\mathcal La_1,b_1\rangle,
\]

且

\[
\omega_T((u,v),(a_1,b_1))
=\langle u,\mathcal Kb_1\rangle
-\langle a_1,\mathcal Kv\rangle.
\tag{3.2}
\]

若为核方向，先得 $\mathcal Kv=0$：方向 $(0,v)$ 的完整物理初态为零，二阶端点唯一性给 $v=0$。再由 $\mathcal Lu=0$ 得方向 $(u,0)$ 的完整物理终态为零，逆时间端点唯一性给 $u=0$。这里测试只用实际光滑配对的非退化，不把 $\mathscr E$ 等同于全部拓扑对偶。故 $\omega_T$ 是弱辛形式。

若 $X_I$ 有限阶、保持均值且 $[X_I,X_K]=0$，则沿真实轨道

\[
Y(t)=X_I(y(t)),\qquad Y_t=DX_K(y)Y.
\]

取

\[
\eta_I(g)=\big(Y_s(-T),D^{-1}Y_v(T)\big),
\tag{3.3}
\]

线性化 mixed mild 问题的唯一性给

\[
D\mathcal G_T(g)[\eta_I](t)=X_I(y(t)).
\tag{3.4}
\]

于是 $\iota_{\eta_I}\omega_T=d(I\circ E_0)$。精确对合及微分对易均传递。公式中的 $D^{-1}$ 和闭端点光滑不能省略。

原全阶对合的实际依赖是 [MONODROMY_POISSON_PROOF.md](../../Workspaces/dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md) 的冻结外延、因子乘逆 Adler 计算及共同 $U$ 规范不变量商；该文给 ${C_m,C_n}_J=0$，而不是只有数值轨道守恒。

## 4. 新的全阶主部定理

本节使用 [GENERAL_PERIOD_MATRIX_LAX.md](../../Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md) 的准确物理矩阵实现；不丢弃周期 holonomy。

令 $H_{jk}=1_{k<j}$、$A_0=I+2H$，$Z=[e_j-e_{M-1}]_{j<M-1}$，$E$ 取前 $M-1$ 行。用不同字体区分原平均通量 $q(t)$ 和矩阵谱系数 $\mathsf q,\mathsf r,\mathsf V$。直接从谱分裂式有

\[
\mathsf q=\tfrac12p^TZ-\tfrac h8s^TA_0Z+\mathsf q_{\rm const},
\quad
\mathsf r=\mathsf r_{\rm alg}-\frac1{Mc}Es_x.
\tag{4.1}
\]

$\mathsf V,\mathsf r_{\rm alg}$ 都是不含空间导数的有限代数表达式；只除以 $c\ne0$。格点零均值上

\[
ZE s=s,\qquad R=\tfrac h2P_0A_0P_0.
\tag{4.2}
\]

后一式可乘 $(I-S_-)$ 检查：

\[
(I-S_-)P_0A_0P_0=(I+S_-)P_0.
\]

两侧同在零均值上，$(I-S_-)$ 可逆，故是全 $M$ 身份。

密度递推为

\[
z_1=\mathsf r,\quad
z_{n+1}=\mathsf Vz_n-Dz_n-\sum_{i+j=n}z_i(\mathsf qz_j),
\qquad C_n=\int\rho_n,\quad \rho_n=-\mathsf qz_n.
\tag{4.3}
\]

这里 $int\rho_n=(1/n)\operatorname{Tr}L^n$，等号 modulo 空间总导数。

赋每次 $D$ 总微分权重 1，所有不含导数的系数权重 0。归纳得到 $z_n$ 唯一权重 $n$ 的项

\[
z_n^{\rm top}=\frac{(-1)^n}{Mc}ED^ns,
\tag{4.4}
\]

其余每个单项权重至多 $n-1$：$\mathsf Vz_{n-1}$ 少一阶，非线性项 $z_i\mathsf qz_j$ 的 $i+j=n-1$，权重也至多 $n-1$。

代入 $\mathsf q$，再用 $p=v-Rs/2$ 及 (4.2)，$s^TA_0D^ns$ 的最高项恰抵消剪切项；常数行乘 $D^ns$ 的积分为零。故

\[
\boxed{C_n^{\rm top}
=\frac{(-1)^{n+1}}{2Mc}\int v\cdot D^ns\,dx.}
\tag{4.5}
\]

其余密度项总微分权重至多 $n-1$。Euler 导数中，对 jet 的偏微分减去其导数数目，外面的 $(-D)^j$ 再恢复；总微分权重不增加。因此余项梯度最高 jet 至多 $n-1$，经 $J$ 后至多 $n$。这是全阶界，排除了非线性项产生同阶可变最高系数。

令 $G=hMc/4\ne0$。在 $h\sum\int$ 配对及原 $J$ 下：

\[
\boxed{X_{C_n}(v,s)
=\frac1{8G}\big(D^{n+1}v,(-1)^nD^{n+1}s\big)
+\mathcal R_n(v,s),\qquad \operatorname{ord}\mathcal R_n\le n.}
\tag{4.6}
\]

例如 $C_3^{\rm top}=-(2Mc)^{-1}\int v_xs_{xx}$，

\[
X_{C_3}=\frac1{8G}(v_{xxxx},-s_{xxxx})+\mathcal R_3.
\]

这与 $K=-8GC_1+(q/c)P_{\rm mom}+\text{constant}$ 的二阶主部一致。

## 5. 新的实际辅助混合解

令 $\mathcal G_T:X_r\to C([-T,T];H^r\times H^r)$ 是足够短物理窗口的解析解图。先选 $r>n+1/2$，在此阶作原收缩，或用原低阶收缩加闭区间提升。由 (3.3)、(4.6) 得

\[
\boxed{\eta_n(a,b)
=\frac1{8G}\big((-1)^nD^{n+1}a,D^{n+1}b\big)
+\mathscr R_{n,T}(a,b),}
\tag{5.1}
\]

且

\[
\mathscr R_{n,T}:X_r\longrightarrow X_{r-n}
=H^{r-n}\times H^{r-n+1}
\tag{5.2}
\]

局部解析、局部 Lipschitz。所有空间约束隐含在这些 Sobolev 空间中。

这里不要求非规定端点的额外平滑增益：第一分量 $\mathcal R_{n,s}(y(-T))$ 的至多 $n$ 阶 jet 由闭端点 $H^r$ 给 $H^{r-n}$；第二分量 $D^{-1}\mathcal R_{n,v}(y(T))$ 由同一 $H^r$ 给 $H^{r-n+1}$。规定端点 $v(T)=\bar v+Db$ 使其主项准确变成 $D^{n+1}b$。因 $r-n>1/2$，所有剩余 jet 的有限乘积在 $H^{r-n}$ 中有界。这正好是 $X_r\to X_{r-n}$，没有暗用端点 trace 增益。

设 $n=2\ell-1$，$\Lambda_\ell=(-D^2)^\ell$，$\varepsilon_n=(-1)^\ell/(8G)$。参数主部是

\[
a_\tau=-\varepsilon_n\Lambda_\ell a+F_a(a,b),
\qquad b_\tau=\varepsilon_n\Lambda_\ell b+F_b(a,b).
\tag{5.3}
\]

若 $\varepsilon_n>0$，规定 $a(-S)=a_*,b(S)=b_*$：

\[
\begin{aligned}
a(\tau)&=e^{-\alpha(\tau+S)\Lambda_\ell}a_*
+\int_{-S}^{\tau}e^{-\alpha(\tau-\sigma)\Lambda_\ell}F_a(g(\sigma))d\sigma,\\
b(\tau)&=e^{-\alpha(S-\tau)\Lambda_\ell}b_*
-\int_{\tau}^{S}e^{-\alpha(\sigma-\tau)\Lambda_\ell}F_b(g(\sigma))d\sigma,
\end{aligned}\tag{5.4}
\]

其中 $alpha=|\varepsilon_n|$。负号情形交换两个规定端点。

Fourier 乘子直接给

\[
\|e^{-\alpha\sigma\Lambda_\ell}\|_{X_{r-n}\to X_r}
\le C(1+(\alpha\sigma)^{-n/(n+1)}).
\tag{5.5}
\]

积分常数为 $O(S+S^{1/(n+1)})$。给定有余量的小源球，足够小 $S>0$ 使 (5.4) 自映射并收缩；$g\in C_\tau X_r$ 真实存在、唯一球内、解析依赖混合输入。

由同样的核估计，若已知 $g\in C X_\rho$，则余项在 $X_{\rho-n}$，选择 $0<\alpha_0<1$ 可提升到 $X_{\rho+\alpha_0}$，因为 $(n+\alpha_0)/(n+1)<1$。平滑规定端点允许在全闭区间迭代；内点则不需要输入全阶光滑。各固定半范数的局部有界估计与低阶解析依赖一起给高阶解析依赖：有限 Fourier 测试是解析的，局部高阶有界及稠密测试将其提升为相应 Hilbert 空间值解析映射。

现在定义

\[
y(t,\tau)=\mathcal G_T(g(\tau))(t).
\]

内点光滑后 (3.4) 和链式法则给

\[
y_t=X_K(y),\qquad y_\tau=X_{C_n}(y).
\tag{5.6}
\]

这是原 Hamiltonian 场的实际共同双时间解；不是形式 Taylor 系列，也没有用辅助 Cauchy Picard。$C_n$ 沿两个时间均守恒，所有已验证对合身份仍用同一物理 $J$。

## 6. 高阶辅助中心唯一性：复时间证明

高阶 $A$ 与 $2\ell-1$ 阶扰动不能直接沿用 §2：简单时间权重可能产生 $\lambda^{(2\ell-1)/\ell}$ 误差，正项却仅为 $\lambda\phi''$。本文不声称该高阶吸收成立。

改用 (5.4) 的复解析结构。复化参数与余项，在实源球的稍大复球上保留 Lipschitz 常数。取

\[
\mathcal D_\delta={z:\ -S<\Re z<S,
\quad |\Im z|<\delta\min(\Re z+S,S-\Re z)\}.
\tag{6.1}
\]

它是凸菱形。由两个实端点到 $z$ 的直线均在闭菱形中；其倾斜满足 $|\Im\zeta|\le\delta\Re\zeta$。复稳定半群因此满足

\[
\|e^{-\alpha\zeta\Lambda_\ell}\|_{X_{r-n}\to X_r}
\le C(1+(\alpha\Re\zeta)^{-n/(n+1)}).
\tag{6.2}
\]

沿线积分的弧长与实投影之比不超过 $\sqrt{1+\delta^2}$。于是实时间的自映射、收缩估计只增加这个固定因子；再缩 $S$ 即可。

在闭菱形连续、内部 $X_r$-holomorphic 的有界函数空间中做同一个收缩。半群输入项在内部 holomorphic、在规定实端点强连续。源积分先按端点线段参数截断，再在每个紧子菱形上用 (6.2) 的一致可积奇性取极限；截断积分 holomorphic，局部一致极限仍 holomorphic。因此收缩极限 $g(z)$ 内部 holomorphic。它在实轴上由实 mixed 唯一性等于先前实际解。

还需让 Taylor 递推在全部空间导数上合法。内点 holomorphy给 $g_z\in X_r$，而方程给

\[
\Lambda_\ell g\in X_{r-n},
\]

因为余项在 $X_{r-n}$。零空间均值上常系数 $\Lambda_\ell$ 可逆，阶 $n+1$，所以 $g\in X_{r+1}$。在较小紧菱形中，Cauchy 导数估计及余项界给 $X_{r+1}$ 局部一致有界。有限 Fourier 系数仍 holomorphic；较强 Hilbert 范数局部有界与稠密测试给 $X_{r+1}$-holomorphy。重复得每个 $X_{r+m}$ 的 holomorphy。

若两条构造的实际辅助解在**内点** $\tau_0$ 的完整参数状态相同，则自治式 $g_\tau=\eta_n(g)$ 在光滑尺度中逐次确定所有时间导数；其 $X_r$ Taylor 系数全部相同。解析 identity theorem给重叠内区间轨道相同，再由端点连续性给其 mixed 数据相同。

线性化解的系数及源由上述 holomorphic背景生成，线性收缩同样复化。中心零变分递推所有 Taylor 系数为零，故线性化中心也单射。

**范围：**这是所构造辅助 mixed 类的内点唯一性；没有给任意非解析弱解唯一性，也没有给高阶辅助窗口端点 Cauchy 唯一性。不能以“平滑到闭端点”代替最后一项。

## 7. 有限前缀的实际共同多时间域

给定有限奇指标列表 $\mathcal F=(n_1,\ldots,n_N)$，每一步用前一步参数相空间的两个组件作新的混合输入，重复 §5。

归纳不变项是：前一步中心解图在每个合适 $X_r$ 上解析；每个未加入的物理场有实际微分切向 lift；lift 的主部始终是 (5.1)，余项始终 $X_r\to X_{r-n}$。原因是新 lift 只在相应规定端点评价旧场的两个组件；其最高项作用于该规定输入，余项通过已有解图评价。无需任何高阶状态逆。

精确对易使旧场沿新辅助轨道满足新方程的线性化；新 mixed 线性化收缩唯一性给切向等式。由此其 Hamiltonian 微分身份、对合与 Lie 对易逐步传递。取 $r>\max n_i+1/2$，每一步的时间窗都可选到对应收缩成立。

得到真实光滑场

\[
y(t,\tau_1,\ldots,\tau_N,x),\qquad
y_t=X_K(y),\quad y_{\tau_i}=X_{C_{n_i}}(y),
\tag{7.1}
\]

定义在一个小实多时间矩形。最终输入仍是两个 $\mathscr E$ 中的任意函数，出现在两个相反角的 $Q,P$ 分量；没有有限 Fourier 限制。

每个新辅助中心映射由 §6 内点解析性单射；复合原物理中心单射给最终中心单射及微分单射。不同窗口或不同缩小源球中的共同解若中心状态相同，可先在中心利用各辅助时间的解析 Taylor 递推识别共同 germ，再沿物理时间用 §2 唯一性识别。因此以下定义没有“同状态多轨道”的歧义：

\[
\mathfrak C_{\mathcal F}
=\{\text{由上述 finite mixed 构造得到的实际共同解之中心状态}\},
\tag{7.2}
\]

取所有足够短窗口、所有局部源球及其限制，并只将共同 germ 相同的表示识别。其条件来源是明确的多时间混合可解性，尚未给仅凭单时物理场范数的显式刻画。

对中心附近的小多时间位移，平移已有实际矩形并限制到更小矩形，仍解 (7.1)。再选够小的新窗和适合的球，mixed 唯一性把限制解识别为同一构造类。于是

\[
\Phi_{\boldsymbol\sigma}(z)
=y_z(\sigma_0,\sigma_1,\ldots,\sigma_N),
\quad
\Phi_{\boldsymbol\sigma}\Phi_{\boldsymbol\tau}
=\Phi_{\boldsymbol\sigma+\boldsymbol\tau}
\tag{7.3}
\]

在共同容纳的较小矩形中成立。这是实际局部共同流，不是原固定参数开集每点的 Cauchy 流。

可以明确给它生成 diffeology：一个有限维参数 plot 若局部能光滑 lift 到某一 mixed 输入开集，就算光滑；原解图的中心评价为生成图。换窗与 (7.3) 可局部 lift 为旧实际解在新角点的评价，因此光滑。这里给的是由实际轨道条件传递的结构，不声称与继承的 $H^r$ 或 $C^\infty$ 子空间拓扑相同。

每一生成图上拉回同一个物理 $Omega$，不同时间/不同表示兼容并闭；沿实际共同时间有

\[
\iota_{X_K}\Omega=dK,
\qquad \iota_{X_{C_{n_i}}}\Omega=dC_{n_i}
\]

的相应拉回身份。本文没有由中心微分注入直接宣称新形式弱非退化。多角 type-II 作用量确可给 Hessian 交叉公式，但核方向随后落在高阶辅助边界；§6 内点解析唯一性还不足以完成该端点步骤。需要单独修复高阶端点唯一性或找到其他非退化机制。

域的包含关系只有

\[
\mathfrak C_{\mathcal F\cup\{n\}}\subseteq\mathfrak C_{\mathcal F}
\]

及其忘记新增时间的实际限制；包含通常不应当作等号。每个有限前缀有无限维函数输入，**不自动证明**一致交集 $\bigcap_N\mathfrak C_{(3,5,\ldots,2N-1)}$ 除平衡点外非空、稠密或有同类参数开集。不能把有限前缀真实共同解升级为整个无限层级的统一相空间。

### 7.1 实际共同域上的有限积分块独立性

本小节的具体 Vandermonde 见证限于包含 \(p=s=0\) 的组件空间零均值叶；全阶主部及共同解存在证明没有这个附加均值限制。

在均匀背景，所有线性化场都是常系数，保持每个有限 Fourier 子空间。每一步 mixed 线性解的中心评价在该有限维空间上单射；输入、输出维数相同，所以可逆。复合后，任意指定有限 Fourier 物理中心方向都可由最终 mixed 输入方向实现。这个有限维可逆只用于制造测试方向，不把实际解限制为有限 Fourier 解。

原 [CONSERVATION_FAMILY_VERDICT.md](../../Workspaces/dlw_general_field_20261006/CONSERVATION_FAMILY_VERDICT.md) 的 \(s=0,p_0=2f,p_1=-2f\) 二次见证给 \(C_{2k+1}\) 的最高 Fourier 二次项

\[
\frac2M(-1)^{k+1}\int(D^kf)^2.
\]

取足够高、互异的有限频率及非零幅值，二次 Jacobian 为非零 Vandermonde 主项。每个平移不变局部谱积分在均匀态的一阶变分是空间常数，故在固定组件平均切空间上为零；实际中心解的二阶修正不会改变这个二次积分见证。上述可逆线性中心评价将见证实现为真实共同解参数方向。

在二次见证上，动量的微分对这些纯 \(p\) 幅值方向为零；另加 \(\delta s_0=f,\delta s_1=-f\) 得非零动量微分。真实中心的非线性修正只给更高幅值阶，不改变相应 Jacobian 的非零首项。因而 \(P_{\rm mom},C_1,C_3,\ldots,C_{2N-1}\) 在所构造实际共同域上有非零有限 Jacobian 见证，以 \(K=-8GC_1+(q/c)P_{\rm mom}+\text{constant}\) 替换 \(C_1\) 后仍独立。解析依赖给相应局部源球中有限块独立的开稠密条件。

这补上“实际共同解上的独立性”，仍不是对无限守恒族的谱完备性或极大各向同性证明。

## 8. 固定参数开集的精确流障碍

上述重新混合参数化是必要的。固定原窗口 $T$ 的平滑参数开集，在均匀平衡点附近仍不能承载原物理时间的普通 $C^1$ 局部流。

非零格点频率的线性物理场有

\[
\lambda_\pm(k)=-i(q/c)k\pm\sqrt{k^4-cr_\theta k^3-h^2c^2k^2/16},
\quad r_\theta=(h/2)\cot(\theta/2).
\]

混合线性解图逐 Fourier 模式是可逆有限矩阵。参数线性场与物理线性场相似，因此保留 $Re\lambda_+(k)\sim k^2$。将参数特征模式按两个参数组件的 $L^2$ 范数归一，其 $H^m\times H^{m+1}$ 范数只按 $k$ 的有限幂增长；任何正时间的线性流则按 $e^{tk^2+O(t|k|)}$ 增长。连续 $C^\infty\to C^\infty$ 线性算子对某一输出半范数必须受有限个输入半范数控制，故不可能。

同理 (5.1) 使奇辅助场在均匀态有 $Re\lambda\sim\pm\alpha k^{n+1}$。其余阶至多 $n$，不能消去这一最高实增长；固定窗口参数的普通可微辅助 Cauchy 流也被排除。这是线性可微流障碍，不是对本文实际 mixed 解的反例，不是一般不可积性证明。

## 9. 保留任意物理平均通量

本构造可先在 $q_0=0$ 的移动规范进行。给定所需 $q(t)$，令

\[
a(t)=-\int_0^t q(\sigma)/c\,d\sigma,
\qquad
U(x,t,\boldsymbol\tau)
=\widetilde U(x+a(t),t,\boldsymbol\tau)+q(t)/c,
\qquad
w(x,t,\boldsymbol\tau)
=\widetilde w(x+a(t),t,\boldsymbol\tau).
\tag{9.1}
\]

这是原准确移动坐标变换的逆；重构场满足 $\Pi(Uw)=q(t)$，$c$ 保持实际守恒值。$q\in C^1$ 时得到经典物理解，有界 $q$ 时按分布/Carathéodory 理解。$q$ 不依赖辅助时间，所以实际辅助方向由同一变换推前，共同流的混合偏导仍一致。

平移动量的实际流是 $x\mapsto x-\sigma$，与每个平移不变的层级方向共同存在。应使用零通量规范下的积分（或其移动规范推前）记录任意 $q(t)$ 的自主层级，而不是将瞬时带 $q(t)$ 参数的谱归一化误称时间常数。

这只处理 $c\ne0$ 正则周期分支。$c=0$、非周期仿射平均、无限格点需要独立相空间；不能由本文外推覆盖。

## 10. 证据与待解项

独立脚本 [verify_mixed_hierarchy_symbols.py](../../Workspaces/dlw_recovery_20261011/verify_mixed_hierarchy_symbols.py) 精确检查 $M=2,\ldots,9$ 的 $R^*=-R$、三角矩阵身份、剪切最高密度抵消、$n=1,\ldots,11$ 的 Hamiltonian 主部系数、平均通量 Hamiltonian 差及二阶谱判别式。记录：[mixed_hierarchy_symbol_checks.json](../../Workspaces/dlw_recovery_20261011/mixed_hierarchy_symbol_checks.json)。有限符号检查只作一致性支持；§2、§4、§5–7 是实际全阶推导。

没有发现被审三项证明的精确反例；发现并保留的界限是高阶端点唯一性不能由内点解析性代替，以及固定窗口参数域确实有可微 Cauchy 流障碍。

接续需要：高阶辅助端点唯一性/新联合域的弱非退化；整个无限层级一致域的非平凡性与物理场内在刻画；该域中已有独立守恒量的极大各向同性、逆谱与角变量。任意有限前缀的真实共同解已经可构造，但尚无一般物理场完整无限维 Liouville 定理。

## 11. 所有可缩窗口联合域的弱辛性：稠密切向与无 ghost

本节解决 §7、§10 留下的**有限前缀联合 germ 域**弱非退化问题。结论不依赖新增辅助轴的边界唯一性，也不声称每一个固定窗口生成图的拉回都弱非退化。原二阶固定图的弱非退化仍是 §3 已独立核验的较强结论。

### 11.1 明确域与生成 diffeology

固定一个有限前缀 \(\mathcal F\)。令 \(\mathfrak C_{\mathcal F}\) 包含其全部合法窗口、局部混合源球和源球限制所产生的共同解中心；以真实共同 germ 相同识别表示。每个生成图记为

\[
E_i:U_i\subset\mathcal E^2\longrightarrow\mathfrak C_{\mathcal F},
\qquad \mathcal E=C^\infty_{x,0}\cap\operatorname{im}P_0.
\]

这里 \(\mathcal E\) 同时实行空间零均值和格点零和；物理平均量按 Hamiltonian 平均叶处理，全部允许的非零 \(c\) 及既定 \(\Gamma\) 均可采用本构造。canonical 分量是 \((Q,P)\)，Sobolev 标度为

\[
X_r=H^r(Q)\times H^{r+1}(P).
\]

一个有限维 plot 定义为局部可 smooth lift 到某个 \(U_i\) 的映射。§6 的内部复时间解析唯一性逐层说明 \(E_i\) 和 \(DE_i\) 都单射；没有使用辅助端点唯一性。

### 11.2 有限个图有共同的更小图

设有限个图在源点 \(g_i\) 表示同一中心 \(z\)。内部唯一性使其共同解 germ 相同。选一个共同更小的多时间盒 \(J\)，其闭包严格位于各旧盒内部，并足够短，使新 mixed 收缩适用。由旧解在新指定角点的 canonical 组件定义

\[
R_i:U_i^{\rm loc}\to U_J,
\qquad R_i(g_i)=g_J.
\]

所有新角点严格位于旧解的内部。复菱形上的 holomorphy、Cauchy 公式和椭圆 bootstrap 给角点求值在任意有限 Sobolev 阶上的 smooth 参数依赖：先在原 Banach 层对参数微分和时间 Cauchy 积分，再用方程解出恒定椭圆主部，逐级提高空间正则。故 \(R_i\) 为 plot-smooth；对光滑源标度也为 Bastiani smooth。缩小旧源邻域后，其值落在同一新开源域 \(U_J\)。旧解的限制满足新 PDE 和 mixed 边值，收缩唯一性给

\[
E_J\circ R_i=E_i. \tag{11.1}
\]

若使用 §12 的偶层级图，新角点包括相应虚时间端点：先取各旧共同复 germ 的共同内多圆盘，再选位于其中的更小实/虚 mixed 菱形。各反射对称性确保新 real 源数据仍为实数；(11.1) 同样成立。有限变量的共同 holomorphy 可由逐变量 Cauchy 公式及局部有界性给出，无需把实际实轴上的解误当成端点解析解。

### 11.3 内部 diffeological tangent 没有 ghost

任意内部 tangent 是有限多个有限维 plot 速度的和。用 (11.1) 将这些 plot 全部推进同一 \(U_J\)，其物理速度成为

\[
DE_J(g_J)\,w,\qquad
w=\sum_i D(R_i\circ\psi_i)\,v_i.
\]

Fréchet 开集的内部 tangent 正是其普通速度空间。具体地，任意光滑曲线可写成

\[
\psi(t)=g_J+t w+t^2 r(t),\qquad
r(t)=\int_0^1(1-u)\psi''(ut)\,du,
\]

积分存在于完备 Fréchet 空间 \(\mathcal E^2\)，且 \(r\) 光滑。二维 plot \(H(s,u)=g_J+s w+u r(s)\) 及映射 \(t\mapsto(t,t^2)\) 说明此内部 tangent 等于直线 \(t\mapsto g_J+t w\) 的速度。有限和用有限维仿射 plot 合并。因此若物理速度为零，\(DE_Jw=0\) 的单射性给 \(w=0\)，原内部 tangent 也为零。于是

\[
T_z^{\rm internal}\mathfrak C_{\mathcal F}
\hookrightarrow\mathcal E^2 \tag{11.2}
\]

确为单射。这里没有另行定义一个人为剔除 ghost 的物理 tangent 商空间。

### 11.4 同一中心的全部缩窗切向在物理空间稠密

取 \(z\) 已有共同 germ 的一个固定内紧盒，将所有宽度 \(T,S_1,\ldots,S_N\) 缩到零。令 \(g_\varepsilon\) 是实际限制解的新混合源数据；于是

\[
E_\varepsilon(g_\varepsilon)=z.
\]

这些基准数据及全部嵌套参数轨道都是同一光滑共同解的角点限制，在每个固定高 Sobolev 阶统一有界。固定 \(r\) 足够高。物理线性混合核的范数为 \(O_r(T^{1/2})\)。第 \(i\) 个辅助主部阶 \(m_i=n_i+1\)，余项微分具有

\[
D\mathscr R_i:X_r\to X_{r-n_i},
\quad
\|K_i\|\le C_{r,i}(S_i+S_i^{1/m_i}). \tag{11.3}
\]

有界的是余项微分，不是包含 \(D^{n_i+1}\) 的全场微分。缩窗使各 \(\|K_i\|\le1/2\)，故

\[
DS_i=(I-K_i)^{-1}{\rm Free}_i,\qquad \|DS_i\|\le2.
\]

未加入方向的新余项微分只有链式项

\[
D\mathscr R_n^{(i)}
=\operatorname{ev}\bigl[D\mathscr R_n^{(i-1)}DS_i\bigr].
\]

因此所需常数由固定背景的有限 jets、端点求值和有限个范数至多 \(2\) 的逆算子控制；有限层数最多产生有限倍数，无 \(S_i^{-1}\) 项，也不需要二阶解图导数。若某一步需要更高背景阶，先在相应有限高阶应用同一归纳；不要求无限多阶同时共用一个阈值。

令 \(L_{i,\varepsilon}\) 是此级中心微分。奇辅助主部给

\[
\|L_{i,\varepsilon}\xi-e^{-|\varepsilon_i|S_i\Lambda_i}\xi\|_{X_r}
\le C_{r,i}(S_i+S_i^{1/m_i})\|\xi\|_{X_r}. \tag{11.4}
\]

物理级同样成立，取 \(m_0=2\) 和自由半群 \(e^{TD^2}\)。§12 偶级取 \(e^{-S_i|iA_i|}\)，估计相同。自由半群统一有界，并对每个固定光滑 \(\xi\) 强趋于恒等。有限乘积

\[
DE_\varepsilon=L_{0,\varepsilon}\cdots L_{N,\varepsilon}
\]

因 telescoping 及各因子统一有界而满足

\[
DE_\varepsilon(g_\varepsilon)\xi\longrightarrow\xi
\quad\hbox{于 }X_r. \tag{11.5}
\]

每个左端都是源直线 \(g_\varepsilon+t\xi\) 的真实 plot 速度，位于同一 \(z\) 的内部 tangent。每给定有限组 \(C^\infty\) 半范数，选择覆盖它们的有限 \(r\) 再缩窗即可。令 \(r_j\uparrow\infty\) 对角选窗给 Fréchet 收敛；不声称一个窗口对全部阶同时收缩。由此 (11.2) 的像在 \(\mathcal E^2\) 中稠密。

### 11.5 弱辛结论与真实 Hamiltonian 流

canonical 连续形式为

\[
\Omega(u,v)=h\int\sum_j(u_{Q,j}v_{P,j}-v_{Q,j}u_{P,j})\,dx.
\]

各生成图上的 \(E_i^*\Omega\) 由 (11.1) 兼容，定义联合域上的 smooth closed diffeological 二形式 \(\omega\)。非零内部 tangent 经 (11.2) 对应非零物理速度 \(V\)。取 \(\xi=(-V_P,V_Q)\)，则

\[
\Omega(V,\xi)=h\bigl(\|V_Q\|_{L^2}^2+\|V_P\|_{L^2}^2\bigr)>0.
\]

由 (11.5) 取同中心真实 tangent \(\xi_\varepsilon\to\xi\)，连续性使 \(\Omega(V,\xi_\varepsilon)\ne0\)。故 \(\omega_z^\flat\) 在真正内部 tangent 上单射：\(\mathfrak C_{\mathcal F}\) 是这里明确定义的**弱辛 diffeological 共同相域**。

每个选定方向的时间坐标曲线是已有实际共同 germ 的平移，并可在更小图中表示；其速度是内部 tangent。物理 Hamilton 身份给全部 plots 上的 \(\iota_{X_I}\omega=dI\)，弱非退化保证此速度唯一；共同流实际存在并对易。此结论保留一般光滑函数自由度。它不证明联合域是某个 Sobolev 开集或普通 Fréchet 流形，也不证明每个固定图的拉回弱非退化；高阶端点唯一性仍单独保留为问题。

## 12. 偶层级的虚时间 mixed 构造与真实实时间流

§5–6 的主部计算并不限于奇 \(n\)。令 \(n=2j\ge2\)、\(d=n+1=2j+1\)、\(a_0=(8G)^{-1}\)。在任何已构造有限共同图的混合源标度上，尚未加入的偶场具有

\[
\eta_n(f)=A_nf+\mathscr R_n(f),\qquad
A_n=a_0D^d I_2,
\quad \mathscr R_n:X_r\to X_{r-n}. \tag{12.1}
\]

\(\eta_n\) 为 real-analytic，可在源点附近复化。这里 \(A_n\) 对真实实时间是 skew；下面先解一个复方程，再从其解析解中提取原场的真实流。

### 12.1 稳定分裂及完整复源

令 \(B=iA_n\)。在空间 Fourier 模 \(k\ne0\) 上

\[
\lambda(k)=-a_0(-1)^j(2\pi k/L)^d,
\qquad \lambda(-k)=-\lambda(k).
\]

故 \(B\) 自伴，令 \(P_-\)、\(P_+\) 是其负、正谱投影，两投影都作用于两源分量。复共轭 \(J\) 满足 \(JB=-BJ\)，从而 \(JP_-=P_+J\)。空间零模已由平均叶分离。

完整复输入仍取 \(f\in\mathcal E_{\mathbb C}^2\)，并定义

\[
\alpha=P_-f,\qquad \beta=P_+f.
\]

这是 complex-linear 的一一源参数化，\(\alpha\)、\(\beta\) 在复源上独立；不能以 \(\beta=\overline\alpha\) 作为 holomorphic 复化定义。仅在 \(f\) 为实时，有 \(\beta=J\alpha\)。因此 real 源保留两个任意光滑实函数的全部格点自由度。

### 12.2 复菱形收缩

在 \(\mathcal D_{S,\delta}\) 上解

\[
g_z=i\eta_n(g)=Bg+i\mathscr R_n(g),\quad
P_-g(-S)=\alpha,\quad P_+g(S)=\beta. \tag{12.2}
\]

沿各端点至 \(z\) 的直线，mild 形式是

\[
\begin{split}
g(z)={}&e^{(z+S)B}\alpha+e^{(z-S)B}\beta\\
&+\int_{-S}^{z}e^{(z-\zeta)B}P_-i\mathscr R_n(g(\zeta))\,d\zeta\\
&-\int_z^{S}e^{(z-\zeta)B}P_+i\mathscr R_n(g(\zeta))\,d\zeta.
\end{split} \tag{12.3}
\]

首项只作用于负谱、次项只作用于正谱。向相应端点的正确方向均是 \(e^{-\xi|B|}\)，其中 \(\Re\xi\ge0\)、\(|\Im\xi|\le\delta\Re\xi\)。与 §6 相同，

\[
\|e^{-\xi|B|}\|_{X_{r-n}\to X_r}
\le C\bigl(1+(\Re\xi)^{-n/(n+1)}\bigr).
\]

直线弧长至多实部增量的 \(\sqrt{1+\delta^2}\) 倍，故积分核为 \(O(S+S^{1/(n+1)})\)。对固定光滑源点，整个自由路径在 \(S\to0\) 时一致趋于该点；选小源球和小 \(S\)，路径留在旧场复化域内，(12.3) 严格收缩。

得到闭菱形上连续、内部 holomorphic 的解。积分先去掉各核的短尾，截断积分 holomorphic；尾估计在紧内菱形一致趋零，故极限仍 holomorphic。由

\[
Bg=g_z-i\mathscr R_n(g)\in X_{r-n}
\]

及 \(B\) 的 \(n+1\) 阶椭圆性得 \(g\in X_{r+1}\)；Cauchy 公式、局部界和有限 Fourier 测试把 holomorphy 提升至该空间。迭代得内部任意阶光滑及 holomorphy，参数微分同样处理。完整内部值唯一及线性化内部值唯一由全部 Taylor jets 与解析恒等定理给出，不涉及边界 unique continuation。

### 12.3 反射与真实流

对 real \(f\)，令 \(\widetilde g(z)=Jg(-\overline z)\)。实系数性和反线性 \(Ji=-iJ\) 给

\[
\widetilde g_z=i\eta_n(\widetilde g).
\]

它的左负谱数据为 \(J\beta=\alpha\)，右正谱数据为 \(J\alpha=\beta\)。收缩唯一性因此给

\[
g(z)=Jg(-\overline z). \tag{12.4}
\]

取 \(z=-i\tau\)，\(|\tau|<\delta S\)。此轴满足 \(-\overline z=z\)，故 \(g(-i\tau)\) 实值，并且

\[
\frac{d}{d\tau}g(-i\tau)
=-i\,i\eta_n(g(-i\tau))
=\eta_n(g(-i\tau)). \tag{12.5}
\]

因此 (12.5) 是原偶 Hamiltonian 场的真实实时间轨道；(12.2) 的虚时间仅用于构造。其中心图 \(\Psi_{n,S}(f)=g(0)\) 是 real-analytic、中心及微分单射。线性自由中心为

\[
e^{-S|iA_n|}f,
\]

故中心通常不等于输入 \(f\)，也不能由此宣称任意先前 Cauchy 态拥有偶层级流。缩窗时它强趋于恒等，非线性误差为 \(O_r(S+S^{1/(n+1)})\)。

中心沿真实 \(\tau_0\) 平移后，\(h(z)=g(z-i\tau_0)\) 仍满足同一反射。取位于原菱形内部的更小菱形，新的实源

\[
f_{\rm new}=P_-h(-S')+P_+h(S')
\]

重新生成该实际轨道。内部解析唯一性给换窗群律；不需旧菱形端点解析性。

### 12.4 与旧共同时间及后续所有层级相容

旧解图及其精确切向身份可在源附近 complexify。解析延拓给

\[
DG_{\rm old}\,\eta_n=X_{C_n}\circ G_{\rm old}.
\]

故 (12.2) 推前为 \(Y_z=iX_{C_n}(Y)\)，(12.5) 推前为原场的真实共同解；旧实时间方程仍逐点成立，反射给新实时间上的全部物理分量实值。

对任何尚未加入的 real commuting 场 \(\eta_\ell\)，新 real 源上的 lift 为

\[
\eta_{\ell,\rm new}(f)
=P_-\eta_\ell(g(-S))+P_+\eta_\ell(g(S)). \tag{12.6}
\]

两项由 (12.4) 互为共轭，因此 lift 实值。\(P_\pm\) 与每个未来恒定主部 \(A_\ell\) 交换，指定投影端值使 (12.6) 的主部精确等于 \(A_\ell f\)；余项仍损失至多 \(\ell\) 阶。线性化混合唯一性给切向身份，中心微分单射将旧 bracket 零推进为新 bracket 零。故奇、偶构造可任意交错迭代，得到

\[
K,\ P_{\rm mom},\ C_1,C_2,\ldots,C_N
\]

任意有限前缀的真实共同 germ 域，仍以一般光滑函数参数化。§11 的共同缩窗、无 ghost、切向稠密和弱辛结论全部适用。

保留的精确区别：偶 lift 的次主部可能含 \(B_-(x)P_-D^\ell+B_+(x)P_+D^\ell\)，通常不能改写成单个 local \(B(x)D^\ell\)。所以尚未完成的高阶固定图端点 Floquet/gauge 唯一性路线不能原样跨越偶图；本节存在性及 §11 联合域弱辛性都不依赖该路线。

## 13. 可数相容共同 germ：逐步完整复合预算的对角构造

本节进一步解决 §7、§10 留下的无限一致域**非平凡性**：构造共享每一坐标正时间宽度的可数相容共同解族。它不自动给无限域的弱辛切向结构、普通开相空间或完整 Liouville 定理。

### 13.1 每一步中心映射的点态近恒等性质

以物理 mixed 图或任一既有有限前缀图作为起点

\[
E_0:U_0\subset\mathcal E^2\to\text{物理中心},
\]

并任取 \(f\in U_0\)。按一个枚举加入所有尚缺的 \(C_n\)。每次新 mixed 中心是之前源空间中的映射

\[
E_{j,S}:U_{j,S}\subset\mathcal E^2\to U_{j-1}.
\]

只要此前图已固定，对同一光滑 \(f\in U_{j-1}\)，有

\[
E_{j,S}(f)\longrightarrow f\quad(S\downarrow0)
\quad\hbox{于 }\mathcal E^2. \tag{13.1}
\]

证明逐半范数进行。给定有限阶 \(r\)，在足够高但有限的 Sobolev 层选择 \(f\) 的局部球；该球落在旧复化域内。新自由路径在闭菱形上一致趋于 \(f\)，积分余项有 \(O_r(S+S^{1/(n_j+1)})\) 界。缩窗后该层收缩解趋于常路径 \(f\)。若较低层已经定义该解，混合收缩唯一性识别两层解。奇级的自由中心是对各指定组件的热半群，偶级是 \(e^{-S|iA_{n_j}|}f\)，都强趋于恒等。因此每个给定半范数满足 (13.1)。不需要全无限阶同时收缩，也不需要中心映射满射。

上述同一旧窗口的高阶正则性可以直接从低阶图证明，避免隐含更换旧窗口。所有方程、空间零均值原函数、\(P_\pm\) 和 mixed 指定组件都与空间平移 \(T_h\) 交换；混合唯一性给固定窗口解析解图 \(\mathcal S\) 的等变性

\[
\mathcal S(T_hf)=T_h\mathcal S(f).
\]

对光滑 \(f\) 的平移轨道在固定低阶 Banach 空间微分，得到

\[
D_x^q\mathcal S(f)
=\sum_{\sum i_\nu=q}c_{\mathbf i}
D^k\mathcal S(f)[D_x^{i_1}f,\ldots,D_x^{i_k}f]. \tag{13.1a}
\]

平移轨道在 \(X_{r_0}\) 中有 \(q\) 阶导数，等价于输出在 \(X_{r_0+q}\) 中；该式也给参数微分的各高阶空间界。因而旧窗口保持不变。对新中心写 \(E_{j,S}=C_S+H_S\)。在 \(f\) 周围可以固定一个不随小 \(S\) 变化的复源球，使其自由路径及收缩解留在旧复化域中；积分核和收缩逆至多 \(2\) 给

\[
\sup\|H_S\|_{X_{r_0}}=O(S^{1/(n_j+1)}).
\]

固定复解析半径的 Cauchy 估计使每个固定 \(k\) 的 \(D^kH_S\) 也具有同一小量。\(H_S\) 同样平移等变；将 (13.1a) 应用于 \(H_S\)，其右端仅含固定 \(f\) 的有限高阶导数，故 \(H_S(f)\to0\) 于每个高阶半范数。\(C_Sf\to f\) 亦成立。这独立证明了保留全部旧窗口的 (13.1)，不需要无穷阶 tame 常数预算。

本步定下 \(S\) 后，可选择一个包含 \(f\) 的 Fréchet 开源域 \(U_j\)，使其整个新复解路径留在 \(U_{j-1}\) 的复化域内、且

\[
E_j(U_j)\subset U_{j-1},\qquad E_j=E_{j,S_j}.
\tag{13.2}
\]

先前时间窗在本步不再改变；旧解图对 \(U_{j-1}\) 中全部路径值均已定义。

### 13.2 对完整已有复合选小窗，不估计未知无限 Lipschitz 常数

取递增的 Fréchet 定义半范数 \(p_r=\|\cdot\|_{X_r}\)。每个已定源域选择有限 \(q_N\) 和 \(\rho_N>0\)，使

\[
B_N=\{u:p_{q_N}(u-f)<\rho_N\}\subset U_N.
\]

定义

\[
F_{N,J}=E_{N+1}\circ\cdots\circ E_J,
\quad F_{N,N}=\operatorname{Id},
\quad g_N^{(J)}=F_{N,J}(f).
\tag{13.3}
\]

依 (13.2)，这些有限复合合法。第 \(j\) 步之前，有限个 \(F_{N,j-1}\)、\(0\le N<j\) 都已固定并在 \(f\) 连续。由 (13.1) 可选择一个严格正的 \(S_j\)，同时满足以下有限要求：

\[
\begin{split}
p_r\bigl(F_{N,j-1}(E_jf)-F_{N,j-1}(f)\bigr)&<2^{-j},
&&0\le N<j,\ 0\le r\le j,\\
p_{q_N}\bigl(F_{N,j-1}(E_jf)-F_{N,j-1}(f)\bigr)
&<\rho_N2^{-(j-N+2)},
&&0\le N<j.
\end{split} \tag{13.4}
\]

每个复合的连续性可能要求输入有较高但有限的范数预算；本步把这些有限要求一起纳入 (13.1)，再缩 \(S_j\) 即可。这直接处理已组成外层映射的全部放大，不能以仅有 \(E_jf-f\) 的粗略小量代替。无需对无穷个图建立统一 Lipschitz 或高阶 bounded-set 估计。

选好 \(S_j\) 后取 \(U_j\)、\(q_j\)、\(\rho_j\)，继续递归。关键恒等式是

\[
g_N^{(j)}-g_N^{(j-1)}
=F_{N,j-1}(E_jf)-F_{N,j-1}(f). \tag{13.5}
\]

因此固定 \(N,r\) 后，(13.4) 对全部充分大 \(j\) 给可求和 \(2^{-j}\) 误差；\(g_N^{(J)}\) 在每个半范数 Cauchy。\(\mathcal E^2\) 完备，得到

\[
g_N=\lim_{J\to\infty}g_N^{(J)}\in\mathcal E^2.
\]

又由第二行预算及 \(g_N^{(N)}=f\)，

\[
p_{q_N}(g_N-f)
\le\sum_{j>N}\rho_N2^{-(j-N+2)}
=\rho_N/4<\rho_N.
\tag{13.6}
\]

各极限严格留在源开域内部。有限关系

\[
g_N^{(J)}=E_{N+1}(g_{N+1}^{(J)})
\]

及连续性给精确相容关系

\[
g_N=E_{N+1}(g_{N+1}). \tag{13.7}
\]

这是一条实际 inverse-limit 点，不依赖形式级数或任意旧中心的满射扩张。

### 13.3 固定的正窗口和共同中心

定义

\[
z=E_0(g_0)
=E_0E_1\cdots E_N(g_N)\quad\text{对每个 }N.
\tag{13.8}
\]

所有 \(S_j\) 只在第 \(j\) 步选一次，均严格正。每一有限前缀的真实共同解由源 \(g_N\in U_N\) 生成；其较早时间窗与前面步骤相同。奇场的实际时间宽度可取其 mixed 菱形的固定实内半宽，偶场的实际宽度可取固定 \(\delta S_j/2\)；物理窗亦取固定内半宽。新解路径留在旧源域中的要求保证旧共同图在这些固定窗口上仍定义。

由 (13.7)，第 \(N+1\) 层解在新增时间置零时，等于第 \(N\) 层的整个共同解，而不仅中心相同。因此这些解构成相容的 \(Y_N\)，共享逐坐标正窗口。也可以在只有有限个非零时间坐标的盒上定义 \(Y\)：用任一足够长前缀求值，相容性保证结果与前缀选择无关。此处没有断言对一般无限支撑时间向量的共同流。

### 13.4 非平凡性、密度及逐层真实流不变性

可先指定 \(E_0(f)\) 的任意物理 Fréchet 邻域 \(W\)，由 \(E_0\) 连续性把 \(B_0\) 选入 \(E_0^{-1}(W)\)。于是 (13.6)–(13.8) 给 \(z\in W\)。取 \(E_0(f)\) 非均匀且 \(W\) 不含均匀态，可得非平凡的可数相容中心。以任意既有有限前缀图作为 \(E_0\) 同证，因此此类中心在每个有限前缀生成像的 ambient \(C^\infty\) 拓扑中稠密。这里密度不等于其像含一个 ambient 开集，也不把新增 smoothing 图当成满射。

定义 \(\mathfrak C_\infty^{\rm coh}\) 为所有**拥有上述相容实际共同解族、并共享逐坐标正窗口**的中心。它非空且含非均匀一般函数解；包含于每个有限前缀 germ 域。它比单纯集合交 \(\bigcap_N\mathfrak C_N\) 附加了一个实质要求：某个固定时间坐标的可用宽度不能随前缀长度缩到零。

对 \(z\) 的一个相容族，固定坐标 \(i\)，在该坐标窗口的严格内区作小平移 \(\tau\)。对 \(N\ge i\) 平移 \(Y_N\)，对 \(N<i\) 使用 \(Y_i\) 并把额外坐标置零；再取逐坐标固定内子窗，仍得相容实际共同族。故中心平移后仍在 \(\mathfrak C_\infty^{\rm coh}\)。任何有限组坐标的流同样存在、彼此对易，群律由已有实际多时间解给出。各有限 germ 需要图表示时，使用 §11 的共同复内域和缩窗重新 mixed 参数化；不以辅助边界解析或边界唯一性为依据。

尚未由此推出 \(\mathfrak C_\infty^{\rm coh}\) 上的 internal tangent 稠密或无 ghost，也没有指定并证明一个无限兼容 plots 类的弱辛性。点态稠密不能代替切向稠密；§11 的有限图证明不能未经补证直接搬到无限交。仍需研究无限域的内在物理刻画、其合法辛切向结构，以及 Liouville 极大性、逆谱和角变量。

## 14. 全部奇、偶有限守恒块在实际共同域中的独立性

本节将 [spectral_independent_review_20261011.md](spectral_independent_review_20261011.md) §7.3、§8 的已推导真实 Fourier—canonical 共振坐标和 Hessian 频率，接到 §12 的实际共同解图；不是用谱代理替代非线性共同解。

### 14.1 精确背景范围

取 \(M\ge2\)、\(L>0\)、\(k_0=2\pi/L\)、\(\delta=hc/8\)，并假定

\[
0<|\delta|<\frac{k_0}{2}\tan\frac{\pi}{2M}. \tag{14.1}
\]

使用 \(B=0\) 的谱截面或既有 \(\Gamma\)-centered 层级。背景均匀物理态为 \(p=P_0U=0\)、\(w_j=c\)；源平均叶也必须包含该背景。对应 free 变量的平均是 \(\overline q_j=-2\delta(M-1-j)\)、\(\overline d_j=\delta\)。这一小 \(|\delta|\) 条件只用于本节独立性见证；§11–13 的共同流存在性没有新增此限制，也不把此见证外推到任意其他平均叶。

取若干互异的 \(C_n\)、\(n\ge1\)，可以另加入 \(P_{\rm mom}\)。\(K\) 在零通量规范与 \(C_1\) 成固定非零倍数关系，故只能用 \(K\) 替换 \(C_1\)，不能将两者同时计为独立积分。

### 14.2 全有限块的一个真实 Hessian 见证

已核验的均匀多项式为

\[
Q_n^0(D)=\frac1{8G}[\mathscr L_0^{n+1}-S^2\mathscr L_0^{n-1}]_+,
\]

次数 \(n+1\)、最高系数 \((8G)^{-1}\)；动量对应 \(-D\)。在正空间频率 \(k\) 和格点通道 \(r\) 上，令

\[
\begin{split}
\theta_r&=\pi r/M,\\
\tau_r&=\sqrt{k^2/4-\delta^2-k\delta\cot\theta_r},\\
y_+&=-ik/2+i\tau_r,\\
\Omega_n(k,r)&=Q_n^0(y_++ik)-Q_n^0(y_+).
\end{split} \tag{14.2}
\]

在 (14.1) 下真实 canonical 通道合法且全频非别名。其线性流为 \(\dot Q_e=\Omega_n(e)Q_e\)、\(\dot P_e=-\Omega_n(e)P_e\)，二次 Hamiltonian 为

\[
H_n^{(2)}=2\Re\sum_e\Omega_n(e)Q_eP_e. \tag{14.3}
\]

这些坐标到原物理 finite-Fourier 切线的逆是该谱稿公式 (30)，保留实共轭条件与原辛配对。

任何非零有限实系数组合产生非恒定实多项式 \(p\)：不同 \(C_n\) 的次数互异，加入动量的次数为一。固定任一通道 \(r\)，当 \(k\to+\infty\) 时 \(y_+\) 一致有界而 \(y_++ik=ik+O(1)\)，故

\[
p(y_++ik)-p(y_+)
\]

不可能对全部 \(k\) 为零。因此这些复频率 profiles 作为实向量空间上的函数线性独立。有限个独立 profiles 必有有限个通道的实、虚求值使矩阵满列秩：若全部有限行矩阵都不满秩，逐步扩大行集的有限维核最终稳定为非零公共核，矛盾。

在这些有限通道取 \(\eta\) 的 \(Q_e=1\)、\(P_e=0\)，其余为零。由 (14.3)，\(dH_n^{(2)}(\eta)\) 在 \(P\) 实、虚测试方向的值正是上述频率行，因而可选有限测试方向 \(\zeta_a\) 使

\[
\det\bigl[\operatorname{Hess}I_b(0)(\eta,\zeta_a)\bigr]\ne0.
\tag{14.4}
\]

这里 \(I_b\) 是所选 charge 或动量，\(\eta,\zeta_a\) 都通过真实坐标逆送回原物理有限 Fourier 切线；有限模仅用作独立性试验方向，不是非线性相空间或共同解的截断。

### 14.3 把见证实现为非线性实际共同解

令 \(E_{\mathcal F}\) 为包含所选全部方向的任一小窗口实际共同中心图，均匀源为零。其线性化在均匀背景与空间平移交换，保持任何指定有限 Fourier 子空间。§6、§12 的中心微分单射说明此有限维限制单射；输入、物理 canonical 分量的维数相同，故它在该子空间可逆。因此可选真实有限 Fourier 源方向 \(\widehat\eta,\widehat\zeta_a\)，使

\[
DE_{\mathcal F}(0)\widehat\eta=\eta,
\qquad DE_{\mathcal F}(0)\widehat\zeta_a=\zeta_a.
\]

均匀背景的一阶物理梯度空间恒定，在固定平均叶上消失；共同中心图的所有阶变分仍保持该叶。故 \(dI_b(0)D^2E_{\mathcal F}(0)\) 不产生二次修正，且

\[
d(I_b\circ E_{\mathcal F})(\varepsilon\widehat\eta)
   \widehat\zeta_a
=\varepsilon\operatorname{Hess}I_b(0)(\eta,\zeta_a)
 +O(\varepsilon^2).
\tag{14.5}
\]

由 (14.4)，对应有限 Jacobian 的行列式是 \(\varepsilon^s(\det A+O(\varepsilon))\)，小非零 \(\varepsilon\) 时不为零。于是所选任意有限奇、偶 charge 块及可选动量在真实共同域上有非线性独立见证。在包含这些源点的连通小解析源球中，非零 minor 的解析零集无内部，给相应有限块独立的开稠密集。

此证明精确补充 §7.1 的仅奇层级见证。它没有证明所有平均叶上的一般独立性，也没有将有限块独立误称为最大各向同性或非线性完整逆谱。

## 15. 光滑有限参数族的可数共同实现与有限秩保持

点态 §13 不能直接给无限域上的横向 plots：源域半径可能随层数缩小，某一条固定直线未必留在所有源域。本节证明一个严格较强但仍有限参数的结论，保留 §14 的实际独立性见证；不宣称同一基点上无限 tangent 稠密或无限弱辛。

### 15.1 紧参数族的一致近恒等 lemma

取闭参数球 \(K\subset\mathbb R^d\)，其闭包位于 \(f\) 的开参数定义域内，且 \(f:K\to\mathcal E^2\) 光滑、\(f(K)\subset U_0\)。在 \(\operatorname{int}K\) 解释最终光滑性；如需某个紧集的开邻域，先在略大的闭球执行构造。

固定已有第 \(j-1\) 层。其解图和余项在局部低 Banach 层复解析。对紧集 \(f(K)\) 用有限源球覆盖，选择统一的较小解析半径、界和小 \(S\) 阈值；不要求用一个单球覆盖全部紧像。写新中心

\[
E_{j,S}=C_S+H_S.
\]

与 §13.1 同理，每个固定 \(k\) 在这些较小球上满足一致估计

\[
\|D^kH_S\|=O(S^{1/(n_j+1)}).
\]

对混合轨道 \((a,h)\mapsto T_hf(a)\) 用链式法则，有限个源微分同时控制任意指定空间阶和参数 multiindex。固定参数导数的像在 \(\mathcal E^2\) 中紧，自由半群的强收敛在该紧像上一致。于是

\[
E_{j,S}\circ f\longrightarrow f
\quad\hbox{于 }C^\infty(K,\mathcal E^2), \tag{15.1}
\]

即对每个有限空间半范数及有限参数导数阶一致收敛。此处局部 Banach 复解析性是实际使用的条件，仅有 Fréchet 开性不足以推出 (15.1)。

### 15.2 统一窗口的 family 对角

每次 \(U_j\) 取为同一紧集 \(f(K)\) 的开邻域，且整个新复路径落在旧源域中。递增 Sobolev 半范数的共终性及紧像有限覆盖允许选择一个管状 margin

\[
f(K)+\{v:p_{q_j}(v)<\rho_j\}\subset U_j.
\]

在第 \(j\) 步，对全部已固定 \(F_{N,j-1}\)、\(N<j\)，要求

\[
\sup_{a\in K}p_r\!\left(
\partial_a^\beta\bigl[F_{N,j-1}(E_j(f(a)))
          -F_{N,j-1}(f(a))\bigr]\right)<2^{-j}
\]

对 \(r\le j\)、\(|\beta|\le j\) 成立；再对 \(\beta=0\)、\(p_{q_N}\) 加上 \(\rho_N2^{-(j-N+2)}\) 的 margin 预算。固定复合是 Bastiani smooth，其相关参数 jets 的像紧；有限覆盖和 (15.1) 使全部这些有限约束可同时满足。

尾增量仍精确等于上述差，因此 \(g_N^{(J)}(a)\) 在每个空间半范数、每个参数导数中一致 Cauchy，极限 \(g_N(a)\) 在 \(\operatorname{int}K\) 光滑。margin 尾和为 \(\rho_N/4\)，所有参数值严格留在 \(U_N\)；连续性给

\[
g_N(a)=E_{N+1}(g_{N+1}(a)).
\]

于是 \(z(a)=E_0(g_0(a))\) 的每一点都有 §13 的全部相容实际共同解，且所有窗口对整个参数族固定。它是一族真实可数共同 germ，保留所有既有时间窗。

### 15.3 任意指定有限 jet 逼近与独立性保持

若要求 \(z(a)\) 在指定空间范数和参数 \(C^L\) 范数中接近旧族 \(E_0(f(a))\)，把物理复合

\[
F_{-1,j-1}=E_0E_1\cdots E_{j-1}
\]

也加入每一步的有限约束。从第一个步骤起，对全部指定 \(r_*\)、\(|\beta|\le L\) 要求其增量小于 \(\varepsilon 2^{-j}\)。可求和误差使

\[
\sup_{a\in K}p_{r_*}
  \bigl(\partial_a^\beta[z(a)-E_0(f(a))]\bigr)<\varepsilon.
\tag{15.2}
\]

这些指定高阶指标不能仅等到 \(r,|\beta|\le j\) 才预算，否则前几步已经可能超出目标误差。

对一组有限阶守恒量，物理函数及其一阶微分在足够高但有限的空间范数中连续。若旧族在某参数点给满秩 Jacobian，先缩 \(K\) 使一个同一 minor 的绝对值有统一正下界，再取 (15.2) 的 \(L=1\) 和足够小 \(\varepsilon\)，该 minor 在新的可数共同族上仍不为零。以 §14 的实际见证族为起点，得到：在 (14.1) 和指定均匀平均叶的范围内，每个有限奇、偶 charge 块及可选动量，都在真正拥有**全部层级相容实际共同 germ**的光滑有限参数族上保持独立。

这排除了“无限一致域虽点态稠密，却完全没有可用横向光滑族”的弱点；仍未证明一个共同基点可同时容纳可数个稠密切向方向，也未排除某种尚未指定的无限 plots 类的内部 ghost。无限域合法弱辛结构是明确的下一项任务，不由本节有限参数 jet 逼近代替。

## 16. 强 mixed-coherent 无限域的合法弱辛结构

本节解决 §15 留下的问题，范围是下面明确的**强 mixed-coherent 子域**。不从点态稠密推切向稠密，不从注入的参数图直接推出内部 tangent 无 ghost，也不把只拥有实时间共同矩形的任意弱 coherent 解族自动归入本节。

### 16.1 域、强 presentation 和 plots

在任一正则 \(c\ne0\) 的 Hamiltonian 平均叶上，采用零通量自主规范，固定所有 \(C_n\) 的一个可数枚举；\(C_1\) 与物理 \(K\) 的关系按 §14 处理，平移动量的已知空间平移也共同保留。\(\Gamma\) 可取任意既定值，没有新增的场幅度或小 \(|c|\) 假设。

一个强 mixed presentation 包含实际中心图

\[
E_0:U_0\to\mathcal E^2_{\rm phys},\qquad
E_j:U_j\to U_{j-1},\quad j\ge1,
\]

以及 \(b_j\in U_j\)、\(b_{j-1}=E_jb_j\)。各 \(E_j\) 来自 §6 或 §12 的有限阶实际 mixed 构造，开源域有局部 Banach 复解析图。新增复时间轨道留在旧图的复源域内。每个较早坐标的正复菱形窗口一旦确定，不因加入新坐标而改变；有限 joint 图因而有相容的固定逐坐标复时间内域。偶坐标的实际时间域是旋转后的菱形。物理二阶根的复内菱形由同一 mild 收缩给出，损失一阶的核指数为 \(1/2\)。所有时间域都仅在各坐标严格内部使用。

令 \(\mathfrak S_\infty\) 为所有这样的物理中心 \(E_0b_0\)，按中心值识别。已有有限内部解析唯一性使共同 germ 也唯一。§13 的构造及 §15 的参数族均有这种 presentation，因此该域非平凡，并在每个有限前缀生成像中稠密。

一个有限维 plot 定义为局部存在同一强链及全部 smooth 源映射 \(\psi_j:O\to U_j\)，满足

\[
\psi_{j-1}=E_j\psi_j,
\qquad p=E_0\psi_0. \tag{16.1}
\]

常数 plot、smooth 预复合及局部拼接满足此定义，故它给一个 diffeology。每个 plot 都有共同的逐坐标正窗口；对其紧参数子域，任一固定有限前缀的所有空间、参数导数及复内时间求值均有界。这里没有要求跨所有前缀的一套统一常数。

强条件之所以必要，是为了后续新 mixed 端点可在**所有**较长前缀中使用同一批旧复角点。只给实矩形及逐前缀解析半径时，旧虚角点未必仍可使用；本文不偷换这两个条件。

### 16.2 既有强 plots 的共同缩窗与角点收敛

取有限个既有强 plots，限制到紧参数盒。选一个共同物理根小窗，严格位于各旧复内域中；以后每个新增轴只选一次更小正窗口，旧轴保持冻结。各既有 plot 的已知 joint 图可在这些角点递归求值，得到新源数据

\[
x_{j,S}(a)\longrightarrow x_{j-1}(a)
\quad(S\downarrow0)
\quad\hbox{于 }C^\infty(K,\mathcal E^2). \tag{16.2}
\]

奇轴取指定源组件在两实端点的值，偶轴取两虚端点的 \(P_\pm\) 数据。反射条件保证这些新源数据实值。(16.2) 来自已知 joint 图的内部 holomorphy、角点对 \(S\) 的趋近及紧参数上 smooth 依赖；所有旧角点保持在原强 presentation 的共同复内域中。

若几条 plot 的基点相同，其新基准角点 \(b_{j,S}\) 相同，因为有限 joint germ 唯一。给定旧新链已构造至 \(j-1\)，原 plot 的短新增时间轨道之旧角点留在旧源域：其中心角点像紧，选新 \(S\) 足够小即可。该轨道满足旧 source 中的 lifted 方程及新 mixed 条件，**逐层 mixed 唯一性**遂给

\[
E_{j,S}x_{j,S}(a)=x_{j-1}(a). \tag{16.3}
\]

这是最终无限对角极限之前的有限归纳；没有用尚未构造的相对延拓来识别原 plot，因此无循环。

### 16.3 保留约束值的相对 family 延拓 lemma

设紧有限参数盒 \(K\) 上，本步源族 \(f_{j,S}\) 满足

\[
f_{j,S}\longrightarrow f_{j-1}
\quad\hbox{于 }C^\infty(K,\mathcal E^2), \tag{16.4}
\]

其中旧 \(f_{j-1}(K)\) 位于已冻结的 \(U_{j-1}\)。依 §15 的统一近恒等 lemma，

\[
E_{j,S}\circ f_{j,S}\longrightarrow f_{j-1}
\quad\hbox{于 }C^\infty(K,\mathcal E^2).
\]

对所有已固定的有限外复合 \(F_{N,j-1}\)，选正 \(S_j\) 使实际增量

\[
\Delta_{N,j}
=F_{N,j-1}(E_jf_j)-F_{N,j-1}(f_{j-1}) \tag{16.5}
\]

在本步有限个空间/参数 jets 中可求和地小，并满足此前每个源域的 margin 预算。\(U_j\) 围绕当前紧像 \(f_j(K)\) 选择；(16.4) 使初始参数盒无需逐层缩到零。以后选 \(S_{j+1}\) 不再改变旧 \(f_j,E_j\) 或旧窗口。

尾族

\[
g_N^{(J)}=F_{N,J}(f_J)
\]

的相邻差精确为 (16.5)。与 §15 相同，全部 jets Cauchy，极限 \(g_N(a)\) smooth、严格留在 \(U_N\)，且 \(g_N=E_{N+1}g_{N+1}\)。所以 \(H(a)=E_0g_0(a)\) 是 \(\mathfrak S_\infty\) 的 plot。

此外，若在某参数约束集 \(A\subset K\) 上，各 \(f_j(a)\) 正是某个既有 strong plot 的新角点数据，则 (16.3) 给

\[
F_{N,J}f_J(a)=x_N(a)\quad(a\in A)
\]

对每个有限 \(J\) **精确成立**。极限因此精确保留该 plot 在 \(A\) 上的值。只要求约束值满足这一识别；没有对 \(A\) 作隐含 Whitney 延拓假设。下面的坐标轴、抛物线和常值直线均由显式 smooth 源族给出。

### 16.4 内部 tangent 无 ghost

任意内部 tangent 类是有限个 plot 速度的和；将参数方向限制到直线，每项可用曲线 \(p_i(t)\) 表示。设其共同基点为 \(z\)。取 §16.2 的共同小链，角点曲线为 \(\psi_{i,j}(t)\)，基准为 \(b_j\)。在小参数盒上设置

\[
f_j(t_1,\ldots,t_k)
=b_j+\sum_i(\psi_{i,j}(t_i)-b_j). \tag{16.6}
\]

初始盒足够小使 \(f_0(K)\subset U_0\)。新 \(S\to0\) 时 (16.2) 给 (16.4)。在每个坐标轴上 (16.6) 正是原 \(p_i\) 的源数据。相对延拓 lemma 给一个 strong plot \(H\)，精确满足

\[
H(0,\ldots,t_i,\ldots,0)=p_i(t_i).
\]

故原内部 tangent 的有限和等于对角曲线 \(p(t)=H(t,\ldots,t)\) 的内部速度；物理速度也正是各物理速度之和。

现在设任意 strong 曲线 \(p(t)\) 的物理速度为零。在每个有限新链上，中心微分单射给 \(\psi_j'(0)=0\)。Hadamard 积分式是

\[
\psi_j(s)=b_j+s^2r_j(s),\qquad
r_j(s)=\int_0^1(1-\theta)\psi_j''(\theta s)\,d\theta. \tag{16.7}
\]

同样对任一尚未选定的新 \(S\) 的角点曲线成立。\(\psi_{j,S}'(0)=0\) 来自该有限新链微分单射，(16.2) 的 \(C^\infty\) 收敛使积分式 \(r_{j,S}\to r_{j-1}\)；没有除以 \(s^2\) 的奇性。

取二维源族

\[
f_j(s,u)=b_j+u r_j(s). \tag{16.8}
\]

在 \(u=s^2\) 上，它精确是原曲线 \(p(s)\) 的角点数据；在 \(u=0\) 上，它精确是常值 \(z\) 的角点数据。取小矩形确保初始源族位于 \(U_0\)，相对 lemma 给 strong plot \(H(s,u)\) 满足

\[
H(s,s^2)=p(s),\qquad H(s,0)=z.
\]

内部 tangent 的参数链式关系给

\[
p_*1=H_*(1,0)=(s\mapsto H(s,0))_*1=0.
\]

结合 (16.6)，任何物理速度为零的内部 tangent 有限和都为零。因此

\[
T_z^{\rm internal}\mathfrak S_\infty
\hookrightarrow\mathcal E^2_{\rm phys} \tag{16.9}
\]

确为单射。这里单射结论来自相对坐标轴与抛物线延拓，不是从各有限 \(DE_j\) 注入跳到无限 subset 的 tangent 注入。

### 16.5 同一基点的实际无限域切向稠密

固定已有 strong presentation 的 \(z\)，给任意 smooth 物理 canonical 方向 \(\xi\)、任意指定有限输出半范数及误差。先缩物理根 \(T\)，以同一实际 germ 的新源 \(b_0^z\) 为基点。§11 的物理线性缩窗估计给

\[
DE_{0,T}(b_0^z)\xi\longrightarrow\xi.
\]

此后旧根保持冻结。逐层从该同一 germ 取得新基准角点 \(b_{j,S}^z\)，令

\[
f_{j,S}(a)=b_{j,S}^z+a\xi,
\quad a\in[-a_*,a_*]. \tag{16.10}
\]

初始 \(a_*>0\) 使源族落在 \(U_0\)；(16.2) 给 (16.4)。在 \(a=0\) 上这些输入精确相容，故相对对角得到 \(Z(a)\) 时

\[
Z(0)=z
\]

严格保持原基点。把 \(N=0\) 的指定源半范数、\(\partial_a\) 误差从第一步加入 (16.5) 的求和预算，可使

\[
g_0'(0)\quad\text{任意接近}\quad\xi.
\]

\(DE_{0,T}(b_0^z)\) 是连续线性 Fréchet 映射，针对指定输出范数只需一个有限输入范数预算。因此

\[
Z'(0)=DE_{0,T}(b_0^z)g_0'(0)
\]

任意接近原物理 \(\xi\)。所有近似都是**同一个 \(z\)** 上真正拥有全部层级相容共同 germ 的 plot 速度。逐半范数选窗，得 (16.9) 的像在物理 \(\mathcal E^2\) 中 Fréchet 稠密。

不需要把可数个方向塞进一个 Fréchet 开源域：diffeology 包含各个同基点变形，而其内部 tangent 只作有限和；§16.4 已证明这些不同 presentations 的 finite sums 没有 ghost。

### 16.6 无限弱辛相域与全部实际 Hamiltonian 时间 germs

物理 canonical 连续形式 \(\Omega\) 沿每个 plot 拉回，给 well-defined smooth closed diffeological 二形式 \(\omega\)。由 (16.9)，非零内部 tangent 对应非零 smooth 物理速度 \(V\)。取 \(\xi=(-V_P,V_Q)\)，有

\[
\Omega(V,\xi)
=h(\|V_Q\|_{L^2}^2+\|V_P\|_{L^2}^2)>0.
\]

§16.5 的同基点真实切向近似及连续性给某个内部 tangent \(w\) 使 \(\omega(V,w)\ne0\)。因此 \(\omega_z^\flat\) 对真正内部 tangent 单射：\(\mathfrak S_\infty\) 是明确定义的**无限弱辛 diffeological 相域**。

固定任一坐标 \(i\)，在一个 strong plot 的共同内时间窗作该坐标平移。原 joint 图给紧参数上的实际共同族；取各坐标固定内子窗并按 §16.2 重新 mixed 参数化，得到同一域的 strong plot。于是该方向的真实局部时间 germ 在每个 plot 上有统一小时间区间并 smooth；有限组方向的群律和对易由实际 joint 解给出。每个 \(C_n\)、物理 \(K\) 和动量的时间曲线给内部 Hamiltonian 速度，原物理身份在所有 plots 上给

\[
\iota_{X_{C_n}}\omega=dC_n,
\qquad \iota_{X_K}\omega=dK,
\qquad \iota_{X_{P_{\rm mom}}}\omega=dP_{\rm mom}.
\]

弱非退化保证这些内部速度唯一。此处只使用有限支撑时间坐标和 plot 上的局部时间 germs；没有断言无限多个非零时间坐标同时取值的流，也没有宣称 ordinary Sobolev 开集上的 Cauchy 流或一个全局共同最大时间域。

### 16.7 保留的范围与 Liouville 余项

\(\mathfrak S_\infty\subset\mathfrak C_\infty^{\rm coh}\) 是有强 mixed 复 presentation 的一般函数域。本文没有证明仅实时间 coherent 族都能取得此 presentation；该更大集合的切向结构不由本节覆盖。§14–15 的有限块实际独立见证均属于本强域，但其明确小 \(|\delta|\) 及均匀平均叶条件仍保留。

高阶固定图端点唯一性不需要本节成立；§8 的固定窗口普通 Cauchy 流障碍也未消失。新的合法结构使用所有可缩 strong presentations 的 diffeology，不能写成未经证明的 ordinary Fréchet manifold。

由此已经具有一般函数域上的全部可数 Hamiltonian 层级、真实逐层共同流、弱辛形式及所述范围内的有限块独立性。完整无限维 Liouville 定理仍须证明非线性极大各向同性、足够的完整谱梯度—局部 charge 闭包、合法逆谱及角变量；线性最大性与 raw nonlinear framed 采样不能直接替代这些步骤。

## 17. 同一状态上全部有限 charge 块独立：紧 Hilbert 参数与 Baire

本节仍保留 (14.1)、\(B=0\) 或 \(\Gamma\)-centered 层级及包含均匀态的指定平均叶。它给同一实际 \(\mathfrak S_\infty\) 状态上的可数独立性，而不仅给每个有限块各自不同的见证；不外推到其他平均叶或宣称全相域泛型。

### 17.1 一份固定的紧复参数球

取 \(\mathcal E^2\) 的实 Fourier cos/sin 基 \(e_\ell\)，包含全部格点零和、空间零均值及两 canonical 分量。令

\[
H_{\mathbb C}=\ell^2(\mathbb C),\qquad
\iota a=\sum_\ell\nu_\ell a_\ell e_\ell,
\]

其中每个 \(\nu_\ell>0\)，且对所有有限 \(r\)，

\[
\sum_\ell\nu_\ell^2\|e_\ell\|_{X_r}^2<\infty.
\tag{17.1}
\]

超快衰减正权即可。\(\iota:H_{\mathbb C}\to X_r\) 为 compact Hilbert–Schmidt 映射，range 包含全部有限 Fourier 方向；实 \(\ell^2\) 对应实物理数据。

闭 Hilbert 球 \(\overline B_R\) 弱紧，且其弱拓扑可度量。若 \(a_m\rightharpoonup a\)，每个 compact \(\iota:H\to X_r\) 使 \(\iota a_m\to\iota a\) 强收敛；故

\[
\mathcal K=\iota(\overline B_R)
\]

在 Fréchet \(\mathcal E_{\mathbb C}^2\) 中紧。选 \(R>0\) 使该复紧像位于均匀根图的复源域内。

### 17.2 Uniform 紧像预算与 holomorphic 尾极限

递归选择每个复源域 \(U_j\) 包含同一个 \(\mathcal K\)。新 \(E_{j,S}\to\operatorname{Id}\) 在 \(\mathcal K\) 上的每个空间半范数一致：自由半群的强收敛在紧像上一致，余项由有限复源球覆盖、uniform 解析半径及 §13.1 的平移公式控制。

每步用已经冻结的有限 \(F_{N,j-1}\) 对整个 \(\mathcal K\) 的连续性，要求

\[
\sup_{a\in\overline B_R}
p_r\bigl[F_{N,j-1}(E_j\iota a)-F_{N,j-1}(\iota a)\bigr]<2^{-j}
\]

对本步有限 \(N<j,r\le j\) 成立，再加入各旧源域围绕 \(\mathcal K\) 的 \(p_{q_N}\)、\(\rho_N\) margin 预算。每步只有有限约束，允许选择更小的新正 \(S_j\)；旧窗口不变。

因此

\[
g_N(a)=\lim_{J\to\infty}F_{N,J}(\iota a)
\]

在 \(\overline B_R\) 上于每个 \(X_r\) 一致收敛，严格落在 \(U_N\)，满足 \(g_N=E_{N+1}g_{N+1}\)。每个有限尾在开 \(B_R\subset H_{\mathbb C}\) 上 holomorphic。逐 \(X_r\) 的局部一致极限仍 holomorphic：在较小 H 球中，对任意单位方向用复 Cauchy 积分，uniform 函数误差控制 derivative operator 误差；高阶导数由同样 Cauchy 及极化控制。故

\[
F(a)=E_0g_0(a):B_R\longrightarrow\mathcal E_{\mathbb C}^2
\tag{17.2}
\]

holomorphic，并保持实结构。均匀 source 是零，所有 \(E_j(0)=0\)，因此 \(F(0)\) 是均匀物理态。实 H 球中的每一点给强 presentation；任意 smooth 有限维预复合都给 §16 的合法 plot。

各有限尾都经 \(\iota\) 因子化，故在闭 H 球的弱拓扑上连续到 \(\mathcal E_{\mathbb C}^2\)。上述逐半范数一致极限仍弱连续，因而每个 \(g_N(\overline B_R)\) 都是 Fréchet 紧像。可以将各 \(U_j\) 取成共轭对称，实 cos/sin 权重取正并对同频分量一致；所有有限尾及极限于是保持实结构。闭球用于紧像和 uniform 预算，holomorphic 陈述只在开 \(B_R\) 上使用。

这没有假设无限乘积在整个 H 上的算子范数收敛；导数极限由已经证明的 holomorphic 尾函数一致收敛给出。

### 17.3 原点导数 range 包含全部有限 Fourier 方向

均匀背景下每个中心线性化 \(L_j=DE_j(0)\) 与空间平移交换，保持每个有限 Fourier 子空间 \(V_k\)。有限中心微分单射及等维性给 \(L_j|_{V_k}\) 可逆。新 \(S_j\to0\) 时在该固定有限维空间 \(L_j\to I\) 为算子范数收敛。故在上述每步预算之外，还可同时要求

\[
\|(L_j-I)|_{V_k}\|<2^{-j-2}
\quad (1\le k\le j). \tag{17.3}
\]

固定 \(k\) 后，\(j\ge k\) 的误差可求和，且小于 \(1/2\)。有序矩阵乘积的 norm 由 \(\prod_j(1+\|L_j-I\|)\) 控制，其逆的尾误差也可求和，因为 \(\|L_j^{-1}-I\|\le2\|L_j-I\|\)。所以 \(L_1\cdots L_J\) 在 \(V_k\) 收敛至可逆矩阵；此前有限个因子已可逆，不影响结论。

由 §17.2 的 Cauchy derivative 收敛，\(DF(0)\) 在该模式上的值就是

\[
DE_0(0)\lim_{J\to\infty}L_1\cdots L_J\,\iota.
\]

\(DE_0(0)|_{V_k}\) 可逆、\(\iota\) 在有限模式上的正权可逆，故 \(DF(0)\) 的 range 包含每个 \(V_k\)，从而包含全部有限 Fourier 切线。只需各 fixed mode 的有限维可逆性，不把整体 smoothing derivative 当成 onto。

### 17.4 可数个 nonzero analytic minors 与同一独立状态

对第 \(N\) 个完整有限块 \(P_{\rm mom},C_1,\ldots,C_N\)，§14 给同一个有限 Fourier 方向 \(\eta\) 和有限 Fourier 测试方向 \(\zeta_\alpha\)，满足

\[
\det A_N\ne0,\qquad (A_N)_{b\alpha}=D^2I_b(0)[\eta,\zeta_\alpha].
\]

这是共同 Hessian-gradient 见证，强于只陈述各 Hessian 双线性形式线性独立。§17.3 给 H 中的有限模原像 \(\widehat\eta,\widehat\zeta_\alpha\)。在均匀平均叶上 \(dI_b(0)=0\)，所以 \(D^2F\) 不对复合 Hessian 产生项。每个 \(C_n\) 在固定 \(c,\Gamma\) 的叶上是有限 differential polynomial 的空间积分，其 Fréchet 复化 holomorphic；因而所有 \(I_b\circ F\) 都在同一个 \(B_R\) 上解析，无需随 charge 另选参数半径。定义实解析函数

\[
J_N(a)=\det\bigl[d(I_b\circ F)(a)\widehat\zeta_\alpha\bigr].
\]

沿 \(a=\varepsilon\widehat\eta\)，

\[
J_N(\varepsilon\widehat\eta)
=\varepsilon^{N+1}(\det A_N+O(\varepsilon)),
\qquad \det A_N\ne0.
\]

故 \(J_N\) 不恒零。其非零集在实 H 开球中开且稠密：任取一个开子球，沿连接其中一点与非零见证点的直线，实解析恒等定理排除整段局部恒零，得到任意近的非零点。

这里所有开集和稠密性使用实 H 的 norm topology。实 H 开球是 Baire 空间；也可在完整的闭实球 \(\overline B_{R/2}\) 上作同样的相对开稠密交集，以保证所得点严格位于原开 \(B_R\) 内。因此

\[
\mathcal R=\bigcap_{N\ge1}\{a\in B_R\cap H_{\mathbb R}:J_N(a)\ne0\}
\]

为稠密 \(G_\delta\)，特别非空。对同一个 \(a\in\mathcal R\)，\(z=F(a)\in\mathfrak S_\infty\) 同时满足所有完整有限块的独立性，因此 \(\{dP_{\rm mom},dC_1,dC_2,\ldots\}\) 在该状态的真正内部 tangent 上有限线性无关。所用 H 测试直线的有限维预复合都是合法 strong plots，故不是仅参数形式上的独立性。

这里泛型指固定 H 参数球；没有宣称其像在整个 \(\mathfrak S_\infty\) 中是 residual 或开集。可用 \(K\) 替换 \(C_1\)，不能把两者重复计数。全部坐标逐层实际流和弱辛结构来自 §16；同一状态的可数独立性仍不能替代非线性 Liouville 最大性、谱逆和角变量。
