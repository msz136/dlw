# M2 实际谱纤维：非线性稳定图、临界反例与有限正则商

2026-10-11。仅新增独立推导，不改共享状态。采用 [实际谱稿](spectral_independent_review_20261011.md) §12–14 的真实归一化 Floquet 迹 $\mathcal F_\lambda$，不是形式 residue 的替代。以下给出三个可核验结果：一个真实无限维同谱稳定图；一个排除无正则假设完备性的反例；有限正则谱块的实际非线性纤维和弱辛商。完整开 gap 状态上的无限梯度闭包仍未证明。

## 1. 准确 M2 原时间、Hamiltonian 与范围

令 $S=hc/4=2\delta\ne0$、$k_0=2\pi/L$，先取原允许的自主平均通量规范为零。固定包含均匀态的组件空间均值叶，令 $u,v$ 都空间平均零。物理重构为

\[
p=(u,-u),\quad s=\frac8h(v,-v),\quad
b=-\frac{2uv}{S},\quad U=b\mathbf1+p,\quad w=c\mathbf1+s.
\tag{1}
\]

其逐点 $\Pi(Uw)=0$，不为原方程添加额外守恒假设。M2 的零和格点分量上 $R=0$。原 DLW 精确成为

\[
\begin{split}
u_t&=-u_{xx}-2Sv_x+\frac2S D(u^2v),\\
v_t&= v_{xx}-\frac S2u_x+\frac2S D(uv^2).
\end{split}\tag{2}
\]

普通积分梯度的张量是 $J=-\mathrm{swap}\,D/16$。式 (2) 由真实 Hamiltonian

\[
K=\int_0^L\left(16vu_x+4Su^2+16Sv^2-\frac{16}{S}u^2v^2\right)dx
\tag{3}
\]

生成。具体梯度 $K_v=16u_x+32Sv-32u^2v/S$、$K_u=-16v_x+8Su-32uv^2/S$。

实际 split 方程的
$q=-S+u$、$r=[(S^2/4-v^2)(1+u/S)-v_x]/S$
给

\[
C_1=-\int qr,\qquad K=-16SC_1+4LS^3.
\tag{4}
\]

因此已证明的 actual $\{\mathcal F_\lambda,C_1\}=0$ 足以严格给每条真实光滑式 (2) 解上的全 $\lambda$ 迹守恒。没有把形式渐近式直接当成真实梯度。

若该对合最初只在谱稿的小高阶源球内证明，其 smooth 全域使用可直接补上：对任意固定 smooth 源 $z$，$\{\mathcal F_\lambda,C_1\}(tz)$ 是复 $t$ 的整函数。原因是 traceless connection 对源仿射，真实 ODE monodromy 和梯度整解析，$C_1$ 是有限 differential polynomial；每个紧 $t$ 集上的 smooth 配对合法。小 $t$ 的恒等式经一变量解析延拓给 $t=1$。因此半线图只需低阶幅度小，不隐含全部高阶范数同时小。

## 2. 半无限真实稳定图

现在明确限制 $0<|S|<k_0$；这只为以下稳定图提供全非零 Fourier 模态的双曲性。线性化

\[
A=\begin{pmatrix}-D^2&-2SD\\-SD/2&D^2\end{pmatrix},\qquad
A_k^2=(k^4-S^2k^2)I.
\]

令 $\Lambda_k=\sqrt{k^4-S^2k^2}>0$、$\Lambda$ 为对应正 Fourier multiplier，及
$P_\pm=(I\pm A\Lambda^{-1})/2$。两投影是保持实型、均值零的零阶 multiplier。令 $E_\pm^s=\operatorname{ran}P_\pm\subset H^s_{\rm per,0}(\mathbb R)^2$；每个空间频率各有一个稳定和不稳定通道。

记 $B(z)=2(u^2v,uv^2)/S$，则 $z_t=Az+DB(z)$。固定

\[
s>1/2,\qquad 0<\gamma<\nu<\min_{k\ne0}\Lambda_k.
\]

标准逐 Fourier 估计直接给

\[
\|e^{-\Lambda t}P_\pm\|_{H^{s-1}\to H^s}
\le C\,t^{-1/2}e^{-\nu t},\qquad t>0.
\tag{5}
\]

这里 $\nu$ 严格小于最小速率，不能在长时将它改成等号。Hs 乘积代数给 $\|B(z)\|_{H^s}\le C_S\|z\|_{H^s}^3$。

对任意充分小 $a\in E_-^s$，在
$Z_\gamma^s=\{z:\sup_{t\ge0}e^{\gamma t}\|z(t)\|_{H^s}<\infty\}$
中考虑真实积分方程

\[
\begin{split}
z(t)={}&e^{-\Lambda t}a+
\int_0^t e^{-\Lambda(t-\tau)}P_-DB(z(\tau))\,d\tau\\
&-\int_t^\infty e^{-\Lambda(\tau-t)}P_+DB(z(\tau))\,d\tau .
\end{split}\tag{6}
\]

第二行的负号必要。式 (5) 与 $e^{-3\gamma\tau}$ 给两项一致的 $C R^3$ 范数界及 $C R^2$ Lipschitz 界：past 积分用
$\int_0^\infty \sigma^{-1/2}e^{-(\nu-\gamma)\sigma}d\sigma<\infty$，
future 积分用
$\int_0^\infty \sigma^{-1/2}e^{-(\nu+3\gamma)\sigma}d\sigma<\infty$。
小 $a$ 时收缩，因此有唯一小加权解，且对 $a$ 实解析。微分式 (6) 在 $H^{s-2}$ 中合法，给式 (2)；并没有声称不稳定通道任意初值的 Cauchy 适定性。

该映射与空间平移交换。若 $a$ 光滑，则 $r\mapsto a(\cdot+r)$ 在同一个低阶输入球中是 C∞ 曲线。实解析解映射及平移生成元判据给所有空间导数仍属于同一个 $Z_\gamma^s$；式 (2) 再给全部时间导数。因此整个 $t\ge0$ 半线上存在真实 C∞ 原解，且每个固定空间/时间导数都以 $e^{-\gamma t}$ 衰减。高阶输入范数无需重新缩减时间域。

其中心图是

\[
\Phi(a)=z_a(0)=a+h(a),\quad h(a)\in E_+^s,\quad
h(a)=O(\|a\|_{H^s}^3),\quad D\Phi(0)|_{E_-^s}=I.
\tag{7}
\]

特别 $P_-\Phi(a)=a$，故它确实是可微单射的无限维非线性图，不是 Fourier 截断或线性近似。光滑 $a$ 的任意有限维平滑参数族给实际 smooth ambient plots。

一个具体真实方向是任意 $k=nk_0>0$ 的
$a_k=(\cos kx,\alpha_k\sin kx)$，
$\alpha_k=(k^2+\Lambda_k)/(2Sk)$；
直接代入给 $Aa_k=-\Lambda_ka_k$。因此 $\Phi(\varepsilon a_k)=\varepsilon a_k+O(\varepsilon^3)$ 是非恒定真实物理同谱曲线，而不只是在均匀态上选一条形式切线。

## 3. 真实同谱性及无正则假设完备性的反例

固定每个 $\lambda$。实际 ODE monodromy 随 H¹ 源连续，式 (4) 的守恒及 $z_a(t)\to0$ 给

\[
\mathcal F_\lambda(\Phi(a))=\mathcal F_\lambda(0)
\quad\hbox{对全部 }\lambda\in\mathbb C.
\tag{8}
\]

同样 $A_{\rm hol}=-2S^{-1}\int uv$ 直接由式 (2) 守恒，故在图上等于零。因而未归一化的实际 trace/determinant 也精确相同。式 (8) 是完全非线性的 actual isospectral 结论；没有只从 gap 的二阶 Hessian 推断。

实际 fast quasimomentum 由 $\mathcal F_\lambda,A_{\rm hol}$ 在大正参数唯一选支；其全部有限渐近系数按谱稿 §14 精确为 $-C_n$。所以图上还满足 $C_n(\Phi(a))=C_n(0)$ 对全部 $n$，并有相同动量。这是 ambient 中的真实全 charge 同水平图，同样没有宣称它属于强 coherent 域。

均匀点的 traceless connection 是
$L_\lambda^0=S(E-F)/2+\lambda(E+F)/2$。其 adjoint 梯度为
$\operatorname{tr}(e^{L_\lambda^0L}H/2)$、
$\operatorname{tr}(e^{L_\lambda^0L}K_\lambda)$，
两者都空间常数。因此固定均值叶上

\[
d\mathcal F_\lambda(0)=0,\quad X_{\mathcal F_\lambda}(0)=0
\quad\hbox{对全部 }\lambda.
\tag{9}
\]

于是以 ambient C∞ 拓扑闭包，

\[
\overline{\operatorname{span}_{\mathbb R}
\{\Re X_{\mathcal F_\lambda}(0),\Im X_{\mathcal F_\lambda}(0)\}}
=\{0\},
\qquad
\bigcap_\lambda\ker d\mathcal F_\lambda(0)
=C^\infty_{\rm per,0}(\mathbb R)^2.
\tag{10}
\]

实际共同谱纤维本身也含式 (7) 的真非线性图，故其 inherited ambient 内部切向至少含 $E_-^\infty$。这个反例比只陈述均匀点梯度消失更强。

稳定图的光滑切向沿原 Hamilton 流衰减。原弱辛形式的守恒及衰减给该图实际拉回二形式为零；但这里不需要也不声称该图恰是整个谱纤维，或已经取得严格最大各向同性。

**范围。** 这排除没有正则或开 gap 条件的普遍梯度完备性；不否定开 gap 正则状态的 Liouville 路线。均匀态属于既有强相域，且在其内部 tangent 上式 (9) 同样使共同微分核全为零约束、Hamilton span 为零。不过式 (7) 全图属于强 $\mathfrak S_\infty$，或者这些 ambient 同谱曲线能够精确提升为其 inherited 谱纤维 plots，均尚未证明；不能移植 ambient 纤维的无 ghost 结论。

## 4. 正则有限谱块：真实非线性局部纤维和弱辛商

这是可用于开 gap 点的正面中间定理。取有限个实 actual spectral functionals $I_1,\ldots,I_N$，例如 actual 分支点对称组合的实部/虚部或有限个 $\mathcal F_\lambda$ 的实部/虚部。紧谱轮廓中的梯度积分仍给已证明的 Hs→Hs order-zero 实解析 Hamilton 场，$s\ge1$。它们真实对合。

设一个实际 smooth 点 $z_*$ 满足 $\{dI_i(z_*)\}$ 在均值叶 Hs 上线性无关。这是明确有限秩条件；只说 gap 非零还不够。已有 actual gap 独立见证提供这种点。固定均值叶的准确环境形式为

\[
\Omega(V,W)=\int (J^{-1}V)\cdot W,\qquad
J^{-1}=-16\,\mathrm{swap}\,D^{-1}.
\tag{11}
\]

它是连续弱非退化形式。因 $\iota_{X_i}\Omega=dI_i$，$X_i(z_*)$ 也独立。选连续线性 $\ell_j$ 使 $\ell_j(X_i(z_*))=\delta_{ij}$，并取 smooth 分离测试。令
$\Sigma=\{z:\ell_j(z-z_*)=0\}$。
真实 order-zero flows 的

\[
(t,y)\longmapsto
\exp(t_1X_1)\cdots\exp(t_NX_N)y,\quad y\in\Sigma
\tag{12}
\]

在基点微分为 Banach 直和同构，故实际解析逆函数定理给局部图。对合使所有 $I_i$ 与 $t$ 无关；$dI|_\Sigma$ 仍 onto $\mathbb R^N$，因为移去的 $X_i$ 方向本来均在其核。再作有限秩解析 submersion 图，得到真正局部坐标 $(t,I,w)$。

因此每个固定有限共同谱水平集是实际 Hs split submanifold，其 ordinary tangent 恰是

\[
K_z^N=\bigcap_{i=1}^N\ker dI_i(z).
\tag{13}
\]

其 smooth 子域也有兼容局部图：式 (12) 的真实流保持 smooth，逆用同一有限时间流，横截分解只作有限 smooth 方向校正。这一步没有使用无限共同谱纤维的 implicit function theorem。

此外，纯有限 codimension 的线性代数给准确 characteristic 核

\[
\ker(\Omega|_{K_z^N})=\operatorname{span}\{X_1(z),\ldots,X_N(z)\}.
\tag{14}
\]

证明：$\Omega(V,\cdot)$ 在 $K_z^N$ 上为零，故作为连续线性泛函等于有限组合 $\sum\alpha_i dI_i$；弱非退化给 $V=\sum\alpha_iX_i$。反向由对合成立。没有要求整个 Banach 对偶由 Hamilton 梯度覆盖。式 (12) 将这些 characteristic 轨道真正积分为局部 $\mathbb R^N$ 作用；有限水平集对该局部作用的商得到合法闭弱非退化二形式。

这是正则 actual spectral functionals 的非线性、真实流层面结论。它明确区分：有限谱块的 characteristic span 是水平集二形式的核，整个有限水平集仍有无限多个横向方向，并非仅由这些谱流填满。

## 5. 全部参数的 gauge kernel 与仍缺的无限步骤

独立 [gauge 审稿](../../Workspaces/dlw_recovery_20261011/m2_gauge_kernel_independent_audit.md) 证明：对固定 $\lambda$，若归一化 monodromy $\mathcal N_\lambda\in SL_2$ 非中心且满足正则共轭条件，则
$d\mathcal F_\lambda\,\delta z=0$
等价于

\[
\delta L_\lambda=(G_\lambda)_x-[L_\lambda,G_\lambda]
\]

具有 smooth 周期 sl2 解。在 $\Delta=\mathcal F_\lambda^2-4\ne0$ 时，令
$B=\mathcal N_\lambda-\mathcal F_\lambda I/2$，可取
$G_\lambda(0)=-[B,\delta\mathcal N_\lambda]/\Delta$；
再用真实 variation-of-constants 构造整个周期解。这在正则谱参数集合上给无需选择特征值分支的单值全纯 gauge。

非中心 Jordan 点也有同样的共轭切向刻画；上述特殊公式的 pole 可换局部 normalization。中心点 $\mathcal N_\lambda=\pm I$ 则不可：trace 微分恒零，但周期 gauge 必须 $\delta\mathcal N_\lambda=0$。均匀源的 $\lambda_*=i\sqrt{k^2-S^2}$ 上，$\delta u=\cos(kx),\delta v=0$ 给非零 $\delta\mathcal N_{\lambda_*}$；所有参数的 tracekernel 并不自动给全参数 holomorphic gauge。

### 5.1 所有非中心单值矩阵的全参数整 gauge 定理

固定任意 actual smooth 物理态 $z$，假设 $\Delta(\lambda)$ 不恒零，并且

\[
\mathcal N_\lambda(z)\ne\pm I\qquad\hbox{对每个 }\lambda\in\mathbb C.
\tag{15}
\]

例如 $\Delta$ 的全部零点都简单则满足第二条件：中心 SL2 矩阵处 determinant 导数强制 trace 参数导数为零，因此 $\Delta'$ 也为零。条件 (15) 是实际 monodromy 条件，不是从均匀线性梯度推断；不声称它在普通 Sobolev 拓扑中开放，也不把“某有限块 gap 打开”偷换为此全参数条件。

对固定 smooth 物理 $\delta z$，下列条件等价：

1. $d\mathcal F_\lambda(z)\delta z=0$ 对每个 $\lambda$；
2. 存在关于 $\lambda$ 整解析、关于 $x$ 光滑周期的 traceless $G_\lambda(x)$，满足 $\delta L_\lambda=G_{\lambda,x}-[L_\lambda,G_\lambda]$。

证明的困难只在如何去掉全部 $\Delta$ 零点处的 pole。设 $Z=\delta\mathcal N_\lambda$、$B=\mathcal N_\lambda-\mathcal F_\lambda I/2$。条件 1 与 determinant 变分给 $\operatorname{tr}Z=\operatorname{tr}(BZ)=0$，且条件 (15) 给 $B\ne0$。写

\[
B=\begin{pmatrix}a&b\\c&-a\end{pmatrix},\quad
Z=\begin{pmatrix}p&q\\r&-p\end{pmatrix},\quad
2ap+br+cq=0.
\]

在 $b\ne0$ 的谱邻域，可显式取

\[
G_{\rm loc}=
\begin{pmatrix}q/(2b)&0\\-p/b&-q/(2b)\end{pmatrix},
\quad [G_{\rm loc},B]=Z.
\]

当 $c\ne0$ 或 $a\ne0$ 时对称选取也给局部解析解：分别取
$(\alpha,\beta,\gamma)=(-r/(2c),p/c,0)$
或 $(0,-q/(2a),r/(2a))$，表示矩阵
$\bigl(\begin{smallmatrix}\alpha&\beta\\\gamma&-\alpha\end{smallmatrix}\bigr)$。
因此包括非中心 Jordan 点在内都有实际解析局部解。

谱零点离散。canonical
$G_{\rm can}=-[B,Z]/\Delta$
与任意上述局部解之差都与 $B$ commute；sl2 内非零 $B$ 的 centralizer 准确为 $\mathbb C B$，故在每个 pole 邻域

\[
G_{\rm can}-G_{\rm loc}=h_{\rm loc}B
\]

有标量 meromorphic $h_{\rm loc}$。取标量 Mittag–Leffler 函数 $h$，在全部离散 pole 处匹配这些主部，则
$G_0=G_{\rm can}-hB$
整解析并满足 $[G_0,\mathcal N_\lambda]=Z$。这里的存在可由显式局部一致级数证明：对趋向无穷的每个 pole 的有理主部减足够长的 Taylor 多项式，使其在逐渐扩大的不含该 pole 的圆盘内小于 $2^{-j}$，再求和。有限 pole 单独处理。因此没有隐藏有界 interpolation 假设。

最后令

\[
G_\lambda(x)=Y_\lambda(x)
\left(G_0(\lambda)+\int_0^xY_\lambda^{-1}\delta L_\lambda Y_\lambda\,dy\right)
Y_\lambda(x)^{-1}.
\tag{16}
\]

实际 ODE 的参数解析性给整 $\lambda$ 依赖及每个紧参数集上的全部 smooth x 半范数。式 $[G_0,\mathcal N]=\delta\mathcal N$ 正好使 $G(L)=G(0)$；周期方程遂给完整周期性。反向的周期 gauge 只使 monodromy 共轭，故 trace 变分为零。实型源与扰动时对 $G_\lambda$ 作 $\lambda\mapsto\bar\lambda$ 的共轭平均可保留真实对称性。

这是 arbitrary nonlinear actual state 上的精确全谱微分核刻画。它没有积分成所有共同纤维的真实物理曲线，也没有提供该 gauge 选择对状态的全频 tame 依赖。

### 5.2 此定理与 Hamiltonian 梯度闭包之间的真实缺口

Mittag–Leffler 去 pole 不控制无穷远增长，所得 $G_\lambda$ 可以远超过 admissible spectral generating functions 的增长；其整性本身不提供 constrained squared-eigenfunction 展开的系数估计。若要得到 actual Hamilton fields 的 C∞ 或明确 weighted 拓扑闭包，还需一个具有准确增长和全频余项控制的 gauge 插值／谱变换定理。各固定 $\lambda$ 的解析 ODE、上面的全参数去 pole、有限秩 submersion、所有有限 gap 块独立，都没有提供该估计。也不能由 ambient 微分核相等推 strong 共同谱纤维内部 tangent 注入或等号。

### 5.3 可证的局部增长界与全频失控依赖

上述 entrywise rightinverse 还给一个精确定量片段。在任何固定正则参数 $\lambda_*$，选择 $|a|,|b|,|c|$ 中最大的非零 entry，在使其保持至少初值一半的复邻域内使用对应解析公式，有

\[
\|G_{\rm loc}(0,\lambda)\|
\le C\frac{\|\delta\mathcal N_\lambda\|}{\|B_\lambda\|}.
\tag{17}
\]

对任何固定紧谱集，真实 ODE 变分估计再给 $\|\delta\mathcal N_\lambda\|\le C_{z,K,s}\|\delta z\|_{H^s}$，以及式 (16) 的全部 x 半范数估计。若该紧集上 noncentral margin $\inf\|B_\lambda\|>0$，只需有限 cover，即取得真实 finite-frequency tame 控制。

但是全部 gap 非零只保证每个对应点的 $\|B_\lambda\|>0$，不给随频率的统一下界；简单零点条件也不给这种下界。接近中心的高频单值矩阵使式 (17) 的常数变大，解析局部图半径也依赖这个 margin。Mittag–Leffler 所用 Taylor 阶数可随 pole 不受控增长，不能据此获得规定指数或 polynomial 的整函数增长界。这两个依赖都须在实际 weighted 谱空间中控制，或通过一个已证明的 normalized squared-eigenfunction basis 消去。当前没有从有限谱块图或逐点非中心性推出该全频估计。

本稿的有限正则商、全参数微分核和真实非线性稳定反例把下一步条件收紧，但没有宣布无限 nonlinear maximality、norming inverse 或 Liouville 完备性。

## 6. 新证据

新增 [symbol check](../../Workspaces/dlw_recovery_20261011/m2_nonlinear_kernel_checks_20261011.py) 及 [JSON](../../Workspaces/dlw_recovery_20261011/m2_nonlinear_kernel_checks_20261011.json) 的 17 项 exact assert 已全部通过，exit 0，SHA256 为 6ab78c2904f3c0659901c2e12f9703db02292daad695a8a694d8342d814e29f8。脚本只核验原 M2 物理重构、Hamiltonian、C1 归一化、动量通量、Fourier dichotomy 和共轭轨道代数；实际半线 contraction 与 finite quotient 依据上面的证明。没有重跑任何旧证书。第一次新检查曾遗漏 C1 密度比较中的全导数 $-16S v_x$，已在该项补入；积分 Hamiltonian 归一化不变。

独立 [m2_gauge_kernel_independent_audit.md](../../Workspaces/dlw_recovery_20261011/m2_gauge_kernel_independent_audit.md) 已实际读取本稿并核验：§7 半线真实稳定图及 K/C1 守恒；§8 全参数整 gauge 的 constructive patch；§9 finite regular actual flow-box、纤维切向和弱辛商。审稿 SHA256 为 1d024f7eab1be80935adabd53fa37c41f0406a3e0b31e18535d03f6e83171e95；其没有执行或重复上述 17 项新检查，也没有重跑旧检查。
