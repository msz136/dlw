# 一般 M 高频实际谱隙：同一 Hilbert strong 参数图的独立性传递

2026-10-11。独立实读 [mixed 审稿 §§16–17](../../刘维尔可积性/research/mixed_independent_review_20261011.md)、其实际原物理坐标与 §§11–13 mixed 构造，以及 [新高频 Riesz 谱隙引理 §8](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md)。本稿只补精确的 strong 参数传递，不改冻结主稿、共享记录，也没有运行旧 checks。

**结论：旧 strong Hilbert 图满足新 §8.3 的解析、共同域、均匀原点和所有有限物理 Fourier 原像条件。每个有限 high-gap block 的非零 Jacobian 可以在同一参数球直接构造；Baire 给同一实际 strong 状态上的全部有限 high-gap block 独立性。** 不从粗 \(X_0\) residual 或点态稠密推出此结论。

## 1. 原背景、平均叶与参数范围

固定 \(M\ge2\)、\(m=M-1\)、\(h,L>0\)、\(c\ne0\)、\(\delta=hc/8\)、\(S=M\delta\)。仍是包含均匀物理态 \(p=0,\ w=c\mathbf1\) 的指定分量空间均值叶。新 gap 源坐标是
\[
q_j=q_j^0+u_j,\quad q_j^0=-2\delta(m-j),\qquad
d_j=\delta+v_j,\quad j<m,
\]
\[
X_0=(L^2_0)^m_u\times(H^1_0)^m_v.
\tag{1}
\]
新谱隙引理要求其内部无 multiplier alias 条件 (NR)，其所有高频 Riesz 窗口和解析函数在一份 \(X_0\) 球内定义。

旧 mixed §17 的文字保留了
\[
0<|\delta|<\frac{\pi}{L}\tan\frac{\pi}{2M}.
\tag{2}
\]
按旧 §14.1，这个条件只用于旧 charge 独立性见证；旧 §§11–13 的实际共同流构造没有这一限制。对已固定的旧 §17 图，首先保留 (2)，不能把同一张图偷偷搬到另一个 \(c\) 叶。(2) 是新 (NR) 的充分条件，故下面的传递直接适用于这份既存图。

若选择满足 (NR) 而不满足 (2) 的另一个均匀叶，则可在该叶**重新执行旧 §§17.1–17.3 的图构造**：这里只使用 §§11–13 的全 \(c\ne0\) mixed 图、紧像近恒等性和有限模可逆乘积，未调用旧 §14 的 charge Hessian。第 3 节给出所需的全部有限约束，所以这个重建也成立；它得到该叶自己的正窗口和参数球，不是一张对所有 \(c\) 的统一图。第 5 节新的 high-gap Hessian 在该叶供应独立性，不依赖旧 §17.4 的小参数 charge 见证。

\(c\) 沿原轨道恒定来自兼容性，\(\Gamma(t)\) 不另冻结。证明用 centered spectral variable \(\lambda=\lambda_{\rm original}-B\)、\(B=\Gamma/(2c)\)。共同 \(B\) 不进入下面的 free 坐标转换。实际非恒定 \(\Gamma\) 仍按旧 mixed §9 的空间平移重构；此谱隙传递没有改变其范围。

## 2. 旧 canonical 图到新 \(X_0\) 源的精确接合

区分新源 \(v_j=d_j-\delta\) 与旧 physical shear。旧 mixed §1 的 canonical 变量在本均匀均值叶上为
\[
Q=s=w-c\mathbf1,\qquad P=D_0^{-1}(p+RQ/2),\qquad
p=DP-RQ/2,
\]
其中 \(p,Q,P\) 格点零和且空间均值为零，
\(R=(\delta_-|_{\mathrm{im}P_{\rm lat}})^{-1}M_-P_{\rm lat}\) 是实常矩阵。

令 \(Z=[e_j-e_m]_{j<m}\)，\(E\) 取前 \(m\) 行，
\[
(K_d)_{jk}=-\delta_{jk}-2\mathbf1_{k>j}+\delta_{km}.
\]
[原谱审稿 §16.1](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 给出精确仿射 source 矩阵
\[
\mathsf F_*=
\begin{pmatrix}Z^T/2&hK_d/8\\0&hE/8\end{pmatrix}.
\]
共同 \(U\) 重构项在 \(b_j-b_m\) 中抵消，所以在均匀偏移坐标中整个转换确实是线性的：
\[
\boxed{\mathcal C(Q,P)=
\left(\frac12 Z^TDP+
\left(-\frac14Z^TR+\frac h8K_d\right)Q,\quad
\frac h8EQ\right)=(u,v).}
\tag{3}
\]
记 \(A=-Z^TR/4+hK_d/8\)。在非零空间频率 \(\kappa=2\pi k/L\) 上，其逆是
\[
Q_\kappa=\frac8h Zv_\kappa,\qquad
P_\kappa=\frac2{i\kappa}
Z(Z^TZ)^{-1}(u_\kappa-AQ_\kappa).
\tag{4}
\]
使用 \(ZEQ=Q\) 和 \(P\in\mathrm{im}Z\) 直接检验 (4)。因此 \(\mathcal C\) 是保留实共轭的有限 Fourier 块同构；有限模原像仍是有限模。这里只需要 (4) 的有限块逆，不宣称同阶全空间逆。

旧 canonical 标度为 \(\mathcal X_r=H^r(Q)\times H^{r+1}(P)\)。式 (3) 连续映射 \(\mathcal X_1\to X_0\)，因为 \(Q\in H^1\)、\(DP\in H^1\subset L^2\)。这给下面的 low holomorphy 接合预算。

## 3. 同一 Hilbert 图、固定正窗口与可逆 Fourier 导数

旧 §§17.1–17.3 选实 cos/sin basis \(e_\ell\) 包含所有格点零和、空间非零频率和两 canonical 分量，及严格正权 \(\nu_\ell\)，使
\[
\iota a=\sum_\ell\nu_\ell a_\ell e_\ell,\qquad
\sum_\ell\nu_\ell^2\|e_\ell\|_{\mathcal X_r}^2<\infty
\quad\text{对每个有限 }r.
\tag{5}
\]
对 \(H_\mathbb C=\ell^2(\mathbb C)\)，
\(\iota(\overline B_R)\) 是每个高阶空间中的共同紧像。所有正权都不为零，故有限 Fourier 向量的 \(\iota\) 原像是有限支撑 Hilbert 向量，范数有限。

选择实际根图 \(E_0\) 的一个正复内时间窗口。逐层加入旧枚举的全部 \(C_j\)，得到 \(E_j:U_j\to U_{j-1}\)。这些是旧证明的复版开域和映射；不仅中心 \(E_j(U_j)\subset U_{j-1}\)，整条新复解路径也严格留在旧复源域内。因而全部先前复角点仍可求值，不能以仅实时间中心包含关系替代强 presentation。每步选择一个严格正 mixed 宽度 \(\sigma_j\)，同时满足：
1. 旧 §17.2 的整个紧像外复合误差和源域 margin 预算；
2. 对该步有限 \(r,N\) 的 \(2^{-j}\) 空间误差预算；
3. 在空间模 \(1\le |k|\le j\) 上
\[
\|(DE_j(0)-I)|_{V_k}\|<2^{-j-2}.
\tag{6}
\]
旧 §13.1 的紧像近恒等性和 finite-mode operator convergence 保证有限要求可以同时满足。以后加入新坐标不改变任何旧 \(\sigma_j\)、根窗口或旧复内角点。旧 §13.3 的实际正时间可取：根窗口固定内半宽；奇辅助轴 \(\sigma_j/2\)；偶轴其复菱形 aperture \(\alpha_j\) 乘 \(\sigma_j/2\)。非零 Hamilton 时间归一化只乘固定正宽度因子。没有跨所有 \(j\) 的统一下界，也不需要这样的下界。

令 \(L_j(k)=DE_j(0)|_{V_k}\)。均匀背景、空间平移等变性使它不混合空间频率。在该有限维块，线性化的完整 source 场是常系数矩阵 \(\mathcal A_j(k)\)。其 mixed endpoint extractor为
\[
\mathcal B_j(k,\sigma_j)
=P_-^{(j)}(k)e^{-\sigma_j\mathcal A_j(k)}
 +P_+^{(j)}(k)e^{\sigma_j\mathcal A_j(k)}
\tag{7}
\]
（偶轴是旧 §12.2 的 rotated equation，完整矩阵换成 \(i\mathcal A_j(k)\)）。投影取该实际 mixed 构造的指定左右数据，满足 \(P_-+P_+=I\)。实际 linear mixed solution gives
\(\mathcal B_jL_j=I\)。
两端都有限同维，故
\[
L_j=\mathcal B_j^{-1},\qquad L_j(k)\to I
\quad(\sigma_j\downarrow0).
\tag{8}
\]
这也可直接从完整 center-zero 线性 ODE 唯一性和相同维数推出。矩阵是完整 lifted 场，不能只以其最高阶热符号代替；(7) 只在实际已存在 mixed 窗口内使用。实反射给正负模和 cos/sin 形式的真实同构。

由 (6)，固定 \(k\) 时尾部 \(\sum_{j\ge |k|}\|L_j(k)-I\|<\infty\)，且每项小于 \(1/2\)。其逆误差亦可求和。故有序乘积
\[
L_\infty(k)=\lim_{J\to\infty}L_1(k)\cdots L_J(k)
\tag{9}
\]
存在并可逆；有限的前缀均已可逆。它不声称在整个 Hilbert/Sobolev 空间上 onto。

旧 §17.2 的一致 holomorphic 尾极限给
\[
F_{\rm can}(a)=E_0g_0(a),\quad
g_N=\lim_{J\to\infty}E_{N+1}\cdots E_J(\iota a),
\tag{10}
\]
在开 \(B_R\) 中逐 \(\mathcal X_r\) holomorphic，实限制给合法同一强链。所有 \(E_j(0)=0\)，故 \(F_{\rm can}(0)=0\)。Cauchy derivative convergence identifies
\[
DF_{\rm can}(0)|_k
=DE_0(0)|_k\,L_\infty(k)\,\iota|_k.
\tag{11}
\]
根 finite block 也由同样 endpoint/ODE argument 可逆。所有因子均有有限维逆。

这里外层物理图 \(E_0\) 的一致收敛也有实际来源，不能仅从 \(g_0\) 点态收敛跳到参数 holomorphy。每个有限尾在闭 Hilbert 球上经 \(\iota\) 因子化，是 weak-to-Fréchet continuous，故其像紧；\(g_0\) 的逐高阶一致极限仍 weak-to-Fréchet continuous，像亦紧。所有有限尾像和极限像之并集的闭包在 Fréchet 空间紧：逐半范数的统一收敛给尾像一致逼近极限紧像，前面有限个像已紧。旧 margin 预算使此闭包严格位于 \(U_0\)。\(E_0\) 在该紧闭包上的一致连续性因此给
\[
E_0g_0^{(J)}\longrightarrow E_0g_0
\quad\text{在 }\overline B_R\text{ 上逐物理高阶半范数一致}.
\tag{11a}
\]
有限物理尾的解析性、(11a) 与较小复 Hilbert 球上的 Cauchy 公式共同给出上述 \(F_{\rm can}\) 高阶 holomorphy 和 derivative convergence。无需改变已冻结窗口或另补未知无限 Lipschitz 常数。

定义真正给新 gap 的图
\[
\boxed{F=\mathcal C\circ F_{\rm can}:B_R\to X_0.}
\tag{12}
\]
它 holomorphic，\(F(0)=0\)，保持原实场；任意所用有限 physical Fourier 向量 \(f\) 有有限支撑参数原像：先用 (4) 取 canonical 原像，然后逐模使用 (11) 的逆和正权 \(\nu_\ell^{-1}\)。因此
\[
DF(0)\widehat f=f
\tag{13}
\]
准确成立，绝非仅稠密逼近。某个高模参数原像的范数可以很大，但总是有限；后面的见证小参数可以相应更小，不改变公共图或时间窗口。

## 4. 仅一次参数球缩小，使全部 high gaps 同域

新引理给一个统一 \(X_0\) 半径 \(\varepsilon_{\rm gap}>0\) 和一个统一高频起点 \(N\)。由 (12) 的 low holomorphy，在 \(r_0<R/2\) 的复球上可取
\[
M_F=\sup_{\|a\|\le r_0}\|DF(a)\|_{H_\mathbb C\to X_0}<\infty.
\]
若需要先把 \(r_0\) 取小，局部解析的 norm continuity 保证这一界。取一次
\[
0<r<\min\left(r_0,\frac{\varepsilon_{\rm gap}}{2M_F}\right)
\tag{14}
\]
（若 \(M_F=0\) 可去掉第二项；这里 (13) 实际保证 \(M_F>0\)）。则 \(F(B_r)\) 落在所有 \(g_{\ell n}\)、\(|n|\ge N\) 的同一个 gap 源域。只是限制参数球：已选的全部原正窗口、mixed maps、链 \(g_N\) 都不变。没有对每个频率或有限 block 再缩公共球。

## 5. 在同一强参数球直接重建每个非零 analytic minor

取任意 finite positive set \(\mathcal F\subset\{n\ge N\}\)，令 \(d=2m|\mathcal F|\)。新 §8.2 在真实 physical finite Fourier space 给 \(f,h_1,\ldots,h_d\)，使
\[
A_{\mathcal F}
=\bigl(D^2G_b(0)[f,h_j]\bigr)_{b,j=1}^d,\qquad
\det A_{\mathcal F}\ne0,
\tag{15}
\]
其中 \(G_b\) 是所选正通道的 \(\operatorname{Re}g_{\ell n}\)、\(\operatorname{Im}g_{\ell n}\)。其真实 Hessian 来自 exact Born couplings，不是假设 gaps/actions 的对应。

这些 real functions 有共同复解析延拓：
\[
G_{\ell n}^{\rm Re}
=\frac{g_{\ell n}+g_{M-\ell,-n}}2,\qquad
G_{\ell n}^{\rm Im}
=\frac{g_{\ell n}-g_{M-\ell,-n}}{2i}.
\tag{16}
\]
在真实源上正是其 Re/Im；这使用新引理的精确实反射，不把正 \(n\) 的全部 gaps 误计为实函数。

由 (13) 取真实有限支撑原像 \(\widehat f,\widehat h_j\in H_\mathbb R\)。新 gap 图在均匀点满足 \(Dg(0)=0\)，故
\[
D^2(G_b\circ F)(0)[\widehat f,\widehat h_j]
=D^2G_b(0)[f,h_j].
\tag{17}
\]
没有 \(D^2F\) 修正。定义同一球内的 real analytic minor
\[
\Delta_{\mathcal F}(a)
=\det\bigl[d(G_b\circ F)(a)\widehat h_j\bigr].
\tag{18}
\]
于是
\[
\boxed{\Delta_{\mathcal F}(\epsilon\widehat f)
=\epsilon^d(\det A_{\mathcal F}+O(\epsilon)),
\qquad \det A_{\mathcal F}\ne0.}
\tag{19}
\]
对每个 block，选足够小的非零 \(\epsilon\) 使
\(\|\epsilon\widehat f\|<r\)。
它只决定一个见证点，并不改变 \(r\)、\(N\) 或旧时间宽度。

\(\Delta_{\mathcal F}\) 在 connected real Hilbert ball \(B_r\cap H_\mathbb R\) 不恒零，其非零集合开且稠密。证明在该球直接用 real analytic 直线恒等定理：若某个开子球上恒零，沿连接该子球点和 (19) 的见证点的直线继续，矛盾。所有 finite positive sets 可数，因此
\[
\boxed{\mathcal R_{\rm gap}
=\bigcap_{\mathcal F\Subset\{n\ge N\}}
\{a\in B_r\cap H_\mathbb R:
\Delta_{\mathcal F}(a)\ne0\}}
\tag{20}
\]
是 norm topology 的 dense \(G_\delta\)，特别非空。也可在完整的闭 \(\overline B_{r/2}\) 取相对开稠密交集，保持全部点严格处于原开球。

每条参数测试线 \(a+t\widehat h_j\) 的有限维预复合都是旧 §16.1 意义的合法 strong plot，且拥有原固定逐坐标正窗口。因此 (18) 的满秩确实检测原 strong 域内部切向上的物理 differentials，不只是参数形式独立。对任何一个 \(a\in\mathcal R_{\rm gap}\)，同一实际状态 \(F(a)\) 的全部 finite positive high-channel gap blocks 有 \(2m|\mathcal F|\) 个真实独立 differentials。没有假定 \(F\) 是普通 Hilbert 状态坐标或全域 immersion。

可另外要求全部单个 \(g_{\ell n}\ne0\)：新 Born 见证取两耦合均非零，给 \(g_{\ell n}\circ F\) 的非零二次项。其非零集同样开稠密，与 (20) 作可数交即可。这是追加的开隙 generic-parameter 结论，不把 gap nonzero 与 derivative independence 混为一谈。

在满足旧 (2) 的同一图中，还可与旧 §17.4 的 charge minors residual 作交，从而同一 strong 状态同时拥有全部 finite high-gap blocks 和各旧 finite charge blocks 的独立性。这个交集**不证明两类合并成一个更大联合 block 后仍独立**；两类可能有依赖，须另证联合 minors。

## 6. 判定与保留范围

新 §8.3 的两个实质前提均被旧 actual strong 图逐式供应，坐标接合、均匀原点、finite parameter 原像和一次同域缩球均已写明。因此本 strong-chart transfer 是 PASS。

泛型仅在这份固定 Hilbert 参数球上；没有声称其像在整个 strong 域或自然 \(X_0/C^\infty\) 相空间 residual、开放或 onto。所有 high gaps 的统一序列解析域来自新 Riesz 引理；旧 strong 的全层级正窗口来自原 mixed construction。这里没有新增全部 gap flows 的低阶存在、norming/action-angle canonical、regular fiber manifold、Hamilton 闭包最大性或一般 M Liouville 定理。

独立并行审查见 [旧 Fourier 原像审稿](general_m_strong_hilbert_fourier_preimages_independent_audit_20261011.md)。该稿已实际读完本传递稿，确认坐标逆、完整 mixed endpoint matrix、原正窗口、同球 Hessian minor 和 Baire 步骤通过。

