# 同一 strong Hilbert 参数图中的全部非中央 AKNS actions：非零与有限独立

2026-10-11。只证明指定 \(M=2\)、\(S=2\delta\ne0\)、包含均匀态的零均值物理叶、小背景及共同谱图范围。结论为**同一已有 strong Hilbert 参数球**中的 residual 集；不外推为整个 \(\mathfrak S_\infty\) 泛型，也不替代全 \(M\) 问题。

依赖：[精确 AKNS 状态桥 §§1–4.5](akns_physical_state_inverse_bridge_20261011.md)，[actual spectral 独审 §§12、15](../../刘维尔可积性/research/spectral_independent_review_20261011.md)，[mixed strong Hilbert 图 §17](../../刘维尔可积性/research/mixed_independent_review_20261011.md)。action normalization 已实际读 [KLTZ published §2.3, (2.15), Proposition 2.7](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf)。该文 Proposition 2.3 讲 Dirichlet 谱，不能把它误引为 action/gap 归一化。本稿直接计算 actual action Hessian，不假定一般复势上“gap 非零必然 action 非零”。

全部 §§1–6 已由 [独立状态/谱审计 §14](akns_physical_state_inverse_independent_audit_20261011.md) 实际读回并逐项手核通过。本次没有运行新或旧脚本；residue 与 Hilbert 图泛型证明为精确数学论证。

## 1. 所有 actions 的共同源域及 strong 参数图

取 \(k_n=2\pi n/L\)、\(\omega_n=\sqrt{k_n^2-4\delta^2}\)、\(\gamma_n=\omega_n/k_n>0\)，\(n\ge1\)。保留旧 \(|\delta|<\pi/L\) 条件和 mixed §17 继承的全部背景、平均叶、centered 层级假设，并进一步将非零 \(L\delta\) 取到精确状态桥的 KLTZ/invariant-factorization 小域；后者没有已知数值半径，不能由前一个不等式自动替代。这里只缩已有图，不改变任意既定 \(B(t)=\Gamma(t)/(2c)\) 的 centered 参数规约。

对 balanced physical source \(X_1=(H^1_0)^2\)，实际
\[
q=-S+u,\quad V=-2uv/S,\quad
r=((\delta^2-v^2)(1+u/S)-v_x)/S,
\]
\[
\eta=\langle V\rangle,\quad \theta=D^{-1}_0P_0V,\quad
a=e^\theta q,\quad b=e^{-\theta}r
\tag{1}
\]
给 analytic \(X_1\to H^1\times L^2\subset L^2\times L^2\) map。fixed balancing 和 period-one rescaling 后
\(\varphi_1=-iLa/2,\ \varphi_2=2iLb\)。选**一个**物理 \(H^1\) 小球，使整个像留在 KLTZ 的共同零邻域和所需 factorization ball，且固定所有 action contours 的 canonical branches。所有 \(I_m\)、\(m\in\mathbb Z\) 因而在这个同一源球上 holomorphic；每个 contour 的界可依 \(m\)，本稿不需全频统一导数界。

精确 actual discriminant 与 actions 为
\[
\Delta(z;u,v)=\mathcal F_{\eta(u,v)-2iz/L}(u,v),\qquad
I_m=\frac1\pi\oint_{\Gamma_m}z\frac{\Delta_z}{R}\,dz,\quad
R=\sqrt[c]{\Delta^2-4}.
\tag{2}
\]

采用 mixed 独审 §17 已经构造的**同一张** holomorphic map
\[
\mathcal P:B_R(H_{\mathbb C})\longrightarrow\mathcal E_{\mathbb C}^2,
\quad H_{\mathbb C}=\ell^2(\mathbb C),\qquad
\mathcal P(0)=(u,v)=(0,0)
\tag{3}
\]
（将原 free variables按既有实际重构换成 \(u,v\)）。其每个有限实参数预复合均为同一 \(\mathfrak S_\infty\) 的合法 strong plot；\(D\mathcal P(0)\) 的 range 包含所有真实有限 Fourier 切向量。通过该 map 在 \(H^1\) 中的连续性，只缩一次 \(R\)，使**整个**图像留在上述共同 source ball。原 compact-tail construction 及每个旧层级的正窗口保留，不重新换图，也不要求 finite Fourier 初态自身属于 strong 域。

以下所有 scalar actions、Jacobian minors 都定义于这个同一连通复 Hilbert 球；实参数球记 \(B_R^{\mathbb R}\)。

## 2. 原实物理源的 action reality 与索引

对真实 \(S,u,v\)，势 \(a,b,\eta\) 均为实。unit AKNS connection 的对角部分为 \(-izH\)，off-diagonal 为实（fixed balancing 保此性质），所以
\[
\overline{U_z}=U_{-\bar z},\qquad
\Delta(-\bar z)=\overline{\Delta(z)}.
\tag{4}
\]
canonical root 在零势满足
\(R_0(-\bar z)=\overline{R_0(z)}\)，因为 \(R_0(z)=-2i\sin z\)。在含零势的小 complex ball 上用同一个 contour/branch 连续延拓，得到
\[
R(-\bar z)=\overline{R(z)},\qquad
\Delta_z(-\bar z)=-\overline{\Delta_z(z)}.
\tag{5}
\]
可取 \(\Gamma_{-m}\) 为 \(-\bar\Gamma_m\) 后反向，保持 counterclockwise orientation。变元 \(z\mapsto-\bar z\) 的 \(dz\) 负号与方向翻转负号抵消；(2) 遂给
\[
\boxed{I_{-m}=\overline{I_m},\qquad I_0\in\mathbb R
\quad\text{on the original real source}.}
\tag{6}
\]
这里没有使用 focusing/defocusing real Cartesian slice。可用
\(\{\operatorname{Re}I_{-n},\operatorname{Im}I_{-n}:n\ge1\}\)
作为实际 real action family。

旧 actual physical double point 为 \(\lambda_n=i\omega_n\)、\(n>0\)。背景 \(\eta=0\)，故它对应 (2) 的
\[
z_{-n}^*=\frac{iL\lambda_n}{2}
=-\pi n\gamma_n.
\tag{7}
\]
因此旧正 physical frequency 记号对应 KLTZ **负**谱索引 \(-n\)；另一 physical point \(-\lambda_n\) 对应 \(+n\)。不能混用这两个索引。

## 3. 实际 action 的精确背景 Hessian

背景
\[
\Delta_0(z)=2\cos w(z),\qquad
w(z)=\sqrt{z^2+L^2\delta^2},\quad w(z)\sim z.
\tag{8}
\]
在 \(z_{-n}^*\) 的局部支取
\(w(z_{-n}^*)=-n\pi,\ w'(z_{-n}^*)=\gamma_n\)。
令 \(\sigma_n=(-1)^n\)，canonical root 局部是
\[
R_0(z)=-2i\sin w(z),\qquad
R_0'(z_{-n}^*)=-2i\sigma_n\gamma_n\ne0.
\tag{9}
\]

对一个实际零均值物理方向 \(\xi=(\xi_u,\xi_v)\)，既有 actual Born Hessian 计算给
\[
\mathcal N(\lambda_n,\varepsilon\xi)
=\sigma_n\left[
1+\varepsilon
\begin{pmatrix}0&\overline{c_{-,n}(\xi)}\\c_{+,n}(\xi)&0\end{pmatrix}
+\varepsilon^2\mathcal R_n+O(\varepsilon^3)\right],
\]
\[
\operatorname{tr}\mathcal R_n
=\mathcal B_n(\xi):=c_{+,n}(\xi)\overline{c_{-,n}(\xi)}.
\tag{10}
\]
determinant 身份真实给出 trace 二阶项 \(\sigma_n\mathcal B_n\)。全零均值 source 的 first trace variation 为零，且 \(D\eta(0)=0\)。因此
\[
\Delta(z;\varepsilon\xi)=
\Delta_0(z)+\varepsilon^2\Delta_2(z;\xi)+O(\varepsilon^3),
\quad
\Delta_2(z_{-n}^*;\xi)=\sigma_n\mathcal B_n.
\tag{11}
\]
没有漏掉 source-dependent shift：\(\eta=O(\varepsilon^2)\) 乘的
\(\mathcal F_0'(\lambda_n)\) 恰为零。

精确 contour variation（状态桥 A5）为
\[
dI_m=-\frac1\pi\oint_{\Gamma_m}\frac{d\Delta}{R}\,dz.
\tag{12}
\]
对 fixed \(n\) 用 (11) 展开，在其背景 contour 上 \(R_0\) 仅于 \(z_{-n}^*\) 有一个 simple zero，故
\[
I_{-n}(\varepsilon\xi)
=-\frac{\varepsilon^2}{\pi}
\oint_{\Gamma_{-n}}\frac{\Delta_2(z;\xi)}{R_0(z)}\,dz
+O(\varepsilon^3)
=\varepsilon^2\frac{\mathcal B_n}{\gamma_n}
+O(\varepsilon^3).
\tag{13}
\]
residue 的系数准确是
\(-2i\cdot(\sigma_n\mathcal B_n)/(-2i\sigma_n\gamma_n)
=\mathcal B_n/\gamma_n\)。

旧原物理 Fourier canonical variables 满足
\[
Q_nP_n=\mathcal B_n/K_n,\qquad
K_n=\frac{Lk_n^2\gamma_n}{16S}.
\tag{14}
\]
于是得到真实 action Hessian，而非代理 action：
\[
\boxed{\
I_{-n}(\varepsilon\xi)
=\varepsilon^2\kappa_n Q_n(\xi)P_n(\xi)
+O(\varepsilon^3),\qquad
\kappa_n=\frac{Lk_n^2}{16S}\ne0.\
}
\tag{15}
\]
若写 \(D^2I_{-n}(0)[\xi,\xi]\)，须将这个二次系数乘二。所有一阶 action derivatives 在背景为零。

与旧 physical half-gap-square \(g_n\) 的关系，仅对 quadratic terms 是
\[
I_{-n}^{[2]}=-\frac{L^2\gamma_n}{4}\,g_n^{[2]},
\qquad
g_n^{[2]}=-\frac{k_n^2}{4SL\gamma_n}Q_nP_n.
\tag{16}
\]
本稿没有把 (16) 宣称为全非线性 action/gap 等式，也未借 gap-open 推断 action 非零。精确 (13)–(15) 已足以给全部所需 analytic witnesses。

## 4. 同一 strong 图中的所有 finite real action blocks 独立

取任意有限 positive frequency 集 \(E\)。旧 Fourier 同构给一个真实有限 Fourier 方向 \(\xi_E\)，使
\[
Q_n(\xi_E)=P_n(\xi_E)=1\ (n\in E),
\]
其余块为零。对每个 \(n\in E\)，再选真实 finite Fourier 测试方向
\(\zeta_{n,R},\zeta_{n,I}\)，分别使 \(\delta P_n=1,i\)、\(\delta Q_n=0\)，其他块全零。取它们在 \(D\mathcal P(0)\) 下的真实 Hilbert 原像
\(\widehat\xi_E,\widehat\zeta_{n,R},\widehat\zeta_{n,I}\)。

因为 \(DI_{\pm n}(0)=0\)，复合 Hessian 中
\(DI_{\pm n}(0)\,D^2\mathcal P(0)\) 项为零。因此 actual strong curve
\(\mathcal P(\varepsilon\widehat\xi_E)\) 上，real action derivatives 在这些 actual internal plot directions 的矩阵为
\[
\varepsilon\,\operatorname{diag}(\kappa_n,\kappa_n)_{n\in E}
+O(\varepsilon^2).
\tag{17}
\]
由 (15)，selected actions 也为
\(\varepsilon^2\kappa_n+O(\varepsilon^3)\ne0\)。
该 finite Jacobian minor 满足
\[
J_E^I(\varepsilon\widehat\xi_E)
=\varepsilon^{2|E|}
\left(\prod_{n\in E}\kappa_n^2+O(\varepsilon)\right)\ne0
\tag{18}
\]
对充分小非零 real \(\varepsilon\) 成立。它是真正原物理 \(I_{\pm n}\) 在同一 strong 参数图内的有限独立性；没有把有限 Fourier 初态自身当作合法 strong 状态。

由于 (6)，也可使用 holomorphic combinations
\[
A_n=(I_{-n}+I_n)/2,\qquad
B_n=(I_{-n}-I_n)/(2i).
\tag{19}
\]
它们在实图上恰是 \(\operatorname{Re}I_{-n},\operatorname{Im}I_{-n}\)。
(18) 同时说明在 complexified internal tangent 上，每个有限 noncentral \(I_{\pm n}\) family 的复线性独立；(19) 与它们是可逆有限线性变换。

## 5. 一个 residual 参数集同时满足全部条件

对每个 \(n\ge1\)，(15) 给 \(I_{-n}\circ\mathcal P\) 在同一 real \(H\) 球内的非零 analytic witness，因此
\[
\mathcal O_n=\{a\in B_R^{\mathbb R}:
I_{-n}(\mathcal P(a))\ne0\}
\]
是开稠密集。证明稠密不需要复 action 的正性：若它在某个 real open 子球全零，real-analytic identity theorem（或连接子球内点与见证点的解析线段）将迫使它在整个连通球恒零，与见证矛盾。

取 \(E_N=\{1,\ldots,N\}\)，固定 (18) 所用的 Hilbert 测试原像，得到 real-analytic minor \(J_N^I\)。每个
\[
\mathcal V_N=\{a\in B_R^{\mathbb R}:J_N^I(a)\ne0\}
\]
同样开稠密。更小的同一 Hilbert 球不破坏见证：只需选更小 \(\varepsilon\)。

实 Hilbert 开球是 Baire 空间，故
\[
\boxed{\
\mathcal R_I=
\bigcap_{n\ge1}\mathcal O_n
\cap\bigcap_{N\ge1}\mathcal V_N
\quad\text{is residual, dense and nonempty in }B_R^{\mathbb R}.\
}
\tag{20}
\]
对每个 \(a\in\mathcal R_I\)，同一真实状态
\[
z=\mathcal P(a)\in\mathfrak S_\infty
\tag{21}
\]
满足所有 \(I_m(z)\ne0\)、\(m\ne0\)，且每个 finite noncentral real action block 在实际内部 strong plot directions 上独立。任意有限 index 集包含于某个 prefix，故不只 prefix 独立。

若需要 \(m=0\) 也非零，只再缩一次共同球：背景
\(I_0^*=-L^2S^2/4\ne0\)，连续性使整个缩小图有 \(I_0\ne0\)；不添加新的可数条件，也不把中央 action 作为额外自由 independent action。

还可以在同一参数球与既有全部 gap-minor、charge-minor residual 集相交，得到各族分别所有 finite blocks 独立的同一个 strong 状态。没有宣称 local charges 与 actions 的合并族独立；它们本来存在真实谱关系。

## 6. 对新的物理 Hamilton 闭包证明所提供的准确输入

(20)–(21) 消除了“ambient action-regular 点可能根本不属于既有 strong 域”的问题。这里的 nonzero 条件直接来自 actual action Hessian；索引、source-dependent holonomy 和原实 action reality 均已核定。它提供新 physical trace-push 与 reduced Cartesian chart 所需的一个非空、同图 residual action-regular strong 子集。

本稿只提供这个必要输入。Hamilton closure=maximal action kernel 的证明须另使用实际 physical trace-push 恒等式、相关拓扑下的有限截断逼近及原弱辛形式连续性；regular fibers 或 Hilbert/Fréchet manifold 也不能由 Baire 或 finite minors 自动推出。
