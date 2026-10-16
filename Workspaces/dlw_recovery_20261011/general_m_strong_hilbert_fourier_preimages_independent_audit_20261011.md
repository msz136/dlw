# 一般 M 旧强域 Hilbert 图：有限物理 Fourier 原像独审

2026-10-11。只读核验旧 [mixed 独审稿 §§13、15–17](../../刘维尔可积性/research/mixed_independent_review_20261011.md)，补出完整中心导数的有限 Fourier 乘子、明确原像和旧 canonical 变量到新 free fields 的接合。未运行旧检查，未改共享日志、状态或冻结稿。

## 1. 结论与范围

旧 §17 的构造确实给一份固定复 Hilbert 开球上的映射
\[
F^{\rm can}:B_R\subset H_{\mathbb C}=\ell^2(\mathbb C)
\longrightarrow \mathcal E_{\mathbb C}^2,
\]
满足 \(F^{\rm can}(0)=0\)，且对每个有限 \(r\)，作为 \(X_r=H^r_Q\times H^{r+1}_P\) 值映射 holomorphic。其全部实参数值属于旧 \(\mathfrak S_\infty\)，各层正复窗口只选择一次并冻结。原点导数的 range **包含**每个有限实物理 Fourier 块，不只是稠密。

下文原像是 Hilbert 中有限支撑向量，可能有很大的有限范数；有限个见证方向可共同缩正幅值而留在同一个球。这不要求整体 smoothing 导数 onto 或具有有界逆。保守引用旧 §17 时仍保留其固定均匀分量均值叶和旧 (14.1) 的小 \(|\delta|\) 范围；不宣称 \(\mathfrak S_\infty\) 自身为 Hilbert 流形或拥有 ambient 开像。

## 2. 同一 Hilbert 球与全高阶解析性

取全部非零空间 Fourier 模、格点零和通道及两 canonical 分量的实 cos/sin 基 \(e_\ell\)。旧 (17.1) 选严格正权重：
\[
\iota a=\sum_\ell\nu_\ell a_\ell e_\ell,\qquad
\sum_\ell\nu_\ell^2\|e_\ell\|_{X_r}^2<\infty
\quad\text{对每个有限 }r.
\tag{1}
\]
\(\iota:H\to X_r\) 为 compact Hilbert–Schmidt。闭 Hilbert 球弱紧、弱可度量，弱收敛经每个 compact \(\iota\) 成为强收敛，故
\[
\mathcal K=\iota(\overline B_R)
\tag{2}
\]
在 Fréchet \(\mathcal E_{\mathbb C}^2\) 中紧。这是统一预算的依据，普通 Fréchet 有界性不能代替它。

各层复源必须明确沿用旧 (13.2) 的复版：
\[
\mathcal K\subset U_j,\qquad E_j(U_j)\subset U_{j-1},
\tag{3}
\]
并令整条新复时间路径留在旧复源域内。仅写 \(\mathcal K\subset U_j\) 不足以保证尾复合合法。旧 §13.1、§15.2 提供选择依据：围绕紧像的正有限半范数 margin、统一自由路径近恒等、余项核小量、有限复源球覆盖。选择新 \(S_j>0,U_j\) 不改变旧窗口。

记 \(F_{N,J}=E_{N+1}\cdots E_J\)，\(g_N^{(J)}=F_{N,J}\iota\)。旧 §17.2 预算的是完整已冻结外复合的实际增量
\[
F_{N,j-1}(E_j\iota a)-F_{N,j-1}(\iota a),
\tag{4}
\]
而非只估计 \(E_j\iota a-\iota a\)。逐个有限 \(N,r\) 的误差可求和，并满足所有旧源的 margin，故在同一闭球上每个 \(X_r\) 一致收敛，极限严格留域，且
\[
g_N=E_{N+1}g_{N+1},\qquad F^{\rm can}=E_0g_0.
\tag{5}
\]
固定旧窗口的高空间正则性由旧 (13.1a) 空间平移等变公式给出；有限 Fourier 测试仍解析，高阶范数局部有界，因此每个有限尾逐 \(X_r\) holomorphic。

若有限尾差在球上 \(X_r\)-范数至多 \(\varepsilon\)，且 \(B_\eta(a)\subset B_R\)，沿所有 Hilbert 单位方向的同半径 Cauchy 积分给
\[
\|D(g_N^{(J)}-g_N^{(J')})(a)\|_{\mathcal L(H,X_r)}
\le \varepsilon/\eta.
\tag{6}
\]
高阶导数由同样估计与极化控制。故局部一致极限逐 \(X_r\) holomorphic，导数可在每个有限块取极限；无需整个 \(H\) 上的矩阵乘积范数收敛。

物理外复合 \(E_0g_0^{(J)}\) 的统一收敛也有依据：各 \(g_0^{(J)}\) 是闭球弱拓扑到 Fréchet 空间的连续映射，且逐半范数一致收敛。各尾像与极限像之并集闭包紧；源 margin 保证它在 \(U_0\) 中。\(E_0\) 在此紧集上一致连续，于是物理外复合也逐 \(X_r\) 一致收敛。等价地可把旧 §15.3 的 \(F_{-1,j-1}\) 直接纳入预算。

全部 \(E_j(0)=0\)，故 \(F^{\rm can}(0)\) 是均匀态。实结构由旧奇轴实解、偶轴完整复源及反射保持。实参数的 (5) 给旧 §16 的强 presentation；有限维 smooth 预复合为合法 strong plot。每个新步骤只有有限收缩、margin、半范数及 Fourier 预算，故可以选严格正 \(S_j\) 并冻结；不需这些正窗口有统一正下界。

## 3. 完整中心导数的 Fourier 乘子

固定非零频率 \(\kappa=2\pi k/L\)。\(V_k\) 包含该频率的全部格点零和通道和两 canonical 分量；正频率复块维数 \(2(M-1)\)，与负频率共轭合并给完整实 cos/sin 块。空间平移等变性使每个 \(DE_j(0)\) 保持该块。以下全部使用完整实际线性场，不能将自由主部半群认作准确中心导数。

### 3.1 物理根

旧剪切变量 \(v_{\rm sh}=p+Rs/2\)，canonical 变量 \(Q=s,P=D^{-1}v_{\rm sh}\)，\(\beta=h^2/32\)。由旧 [full M mixed 稿 (1)–(2)](../../刘维尔可积性/research/full_m_mixed_flow.md) 的线性项，零通量规范的准确 Fourier 矩阵是
\[
A_0(\kappa)=
\begin{pmatrix}
-\kappa^2I+ic\kappa R/2 & c\kappa^2 I\\
c(R^2/4-2\beta I)&\kappa^2I-ic\kappa R/2
\end{pmatrix}.
\tag{7}
\]
即 \(Q_t=D^2Q-cD^2P+(c/2)RDQ\)，\(P_t=-D^2P-(c/2)RDP+c(R^2/4-2\beta I)Q\)。固定常通量仅添加共同 \(-i(q_0/c)\kappa I\)。

令 \(\mathsf P_Q,\mathsf P_P\) 为两组件投影。中心 \(y_0\) 的线性轨道为 \(e^{tA_0}y_0\)，mixed 输入是
\[
f=\mathsf P_Qe^{-TA_0}y_0+\mathsf P_Pe^{TA_0}y_0
=H_0(\kappa;T)y_0.
\tag{8}
\]
因此
\[
L_0(\kappa)=DE_0(0)|_{V_k}=H_0(\kappa;T)^{-1}.
\tag{9}
\]
有限矩阵逆来自实际线性 mixed 存在唯一性，亦由中心微分单射及等维性可得。它一般不是 \(e^{-T\kappa^2}I\)，后者仅为自由中心。

### 3.2 新奇轴和偶轴

令 \(A_j^{\rm full}(\kappa)\) 是旧 source 中新增 charge 的完整线性 lift。由准确切向身份
\[
A_j^{\rm full}
=T_{j-1}^{-1}A_{C_{n_j}}^{\rm phys}T_{j-1},
\qquad T_{j-1}=L_0\cdots L_{j-1}.
\tag{10}
\]
所有低阶线性项均在 \(A_j^{\rm full}\) 中。奇轴规定组件投影按最高阶热主部的正负选择；主部系数变号时交换两规定组件。完整 endpoint operator 为
\[
H_j(\kappa;S_j)
=\mathsf P_{j,-}e^{-S_jA_j^{\rm full}}
+\mathsf P_{j,+}e^{S_jA_j^{\rm full}}.
\tag{11}
\]
偶轴投影是旧 §12 的 \(iA_{n_j}^{\rm principal}\) 的正负谱投影，作用于两组件。完整复时间流为 \(e^{ziA_j^{\rm full}}\)，故
\[
H_j(\kappa;S_j)
=\mathsf P_{j,-}e^{-iS_jA_j^{\rm full}}
+\mathsf P_{j,+}e^{iS_jA_j^{\rm full}}.
\tag{12}
\]
负频率投影与正频率投影共轭交换；反射确保完整实 Fourier 块保持实结构。两种情形均准确给
\[
L_j(\kappa)=DE_j(0)|_{V_k}=H_j(\kappa;S_j)^{-1}.
\tag{13}
\]
可逆性来自实际 linearized mixed 构造。对固定 \(j,k\)，\(H_j(\kappa;S)\to I\)，所以 \(L_j(\kappa;S)\to I\)。这直接解释旧 (17.3) 的新有限模式预算可行。

## 4. 乘积极限和准确有限支撑原像

每次选择新窗口还可同时要求
\[
\|(L_j-I)|_{V_k}\|<2^{-j-2}\quad(1\le k\le j).
\tag{14}
\]
固定 \(k\) 后尾误差可求和，且小于 \(1/2\)。由于
\[
\|L_j^{-1}-I\|\le
\frac{\|L_j-I\|}{1-\|L_j-I\|}
\le2\|L_j-I\|,
\tag{15}
\]
有序有限维乘积及其逆均收敛；前面有限个因子本来可逆。于是
\[
T_k=L_0(\kappa)\lim_{J\to\infty}L_1(\kappa)\cdots L_J(\kappa)
\tag{16}
\]
可逆。

对任意有限频率集合 \(\mathcal F\)，令 \(V_{\mathcal F}\) 是其完整块，\(\iota_{\mathcal F}\) 为严格正对角权重，\(T_{\mathcal F}=\bigoplus_{k\in\mathcal F}T_k\)。任意 \(f\in V_{\mathcal F}\) 的准确原像为
\[
a_f=\iota_{\mathcal F}^{-1}T_{\mathcal F}^{-1}f,
\qquad DF^{\rm can}(0)a_f=f.
\tag{17}
\]
它在 \(H\) 中有限支撑。等价地 \(T_k^{-1}=\lim_JH_J\cdots H_1H_0\)，故原像是实际 endpoint 算子的逆顺序极限，再除以正权。实 \(f\) 给实原像。同一有限见证及测试方向都可选有限原像；缩
\[
0<|\varepsilon|<
R/[2\max(1,\|a_f\|,\|a_{h_1}\|,\ldots)]
\]
给严格正的同球幅值预算。

## 5. canonical/free 坐标的准确接合

新 [actual gap 稿 §1](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md) 的低源是
\[
X_0^{\rm free}=(L^2_0)^m_u\times(H^1_0)^m_{v_{\rm fr}},
\quad u=q-q^0,\quad v_{\rm fr}=d_{\rm first}-\delta.
\]
它和旧图的 \((Q,P)\) 不同，须组成实际坐标转换。旧 [谱主稿 §16.1](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 给恒定真实矩阵
\[
\delta q=Z^T\delta p/2+hK_d\delta s/8,\qquad
\delta d_{\rm first}=hE\delta s/8.
\tag{18}
\]
共同 \(U\) 的非线性 mean 在 \(b_j-b_m\) 中精确消去，故这是固定叶上 affine 坐标转换的完整导数。令 \(C=hK_d/8-Z^TR/4\)，由 \(p=DP-RQ/2,s=Q\) 得
\[
\binom{\widehat u_k}{\widehat v_{{\rm fr},k}}
=\mathcal C_k\binom{\widehat Q_k}{\widehat P_k},
\qquad
\mathcal C_k=
\begin{pmatrix}C&i\kappa Z^T/2\\hE/8&0\end{pmatrix}.
\tag{19}
\]
输入 \(Q,P\in\operatorname{im}P_0\)。\(E\) 在此空间的逆为 \(Z\)，\(Z^T\) 也可逆。准确反解是
\[
Q_k=8Zv_{{\rm fr},k}/h,\qquad
p_k=Z(Z^TZ)^{-1}(2u_k-hK_dQ_k/4),\qquad
P_k=(p_k+RQ_k/2)/(i\kappa).
\tag{20}
\]
故 \(\mathcal C_k\) 在每个非零模可逆，保持实共轭及有限 Fourier 支撑。它把充分高的旧 \(X_r\) 连续映入 \(X_0^{\rm free}\)。

背景减去常值后定义 \(F^{\rm free}=\mathcal C F^{\rm can}\)。它在同一 \(B_R\) 上低源全纯，实点仍是相同旧 strong 域的原物理状态，且 \(F^{\rm free}(0)=0\)。任意有限 free Fourier 方向的准确 Hilbert 原像是
\[
a_f=\iota_{\mathcal F}^{-1}T_{\mathcal F}^{-1}
\mathcal C_{\mathcal F}^{-1}f.
\tag{21}
\]
如 actual gap 只在低源半径 \(\epsilon_0\) 上定义，利用原点连续性缩一次 \(B_{R'}\subset B_R\) 使全像落在该源域中即可；旧 strong 窗口不变。

## 6. 可用的传递与未作的外推

新 gap 稿 §8 的 finite physical Fourier Hessian witnesses 可由 (21) 准确拉回。\(Dg(0)=0\) 给
\[
D^2(g\circ F^{\rm free})(0)[a_f,a_h]
=D^2g(0)[f,h],
\]
不含 \(D^2F\) 项。在同一个 strong Hilbert 参数球中分别证明可数 finite minors 不恒零，再作参数 norm topology 的 Baire 交，得到强域图内的同一 generic 参数。不能从 ambient 低源 residual 直接推出强域 residual。

未发现本传递前提的实质缺口。引用时应显式写出复版 (3) 和 canonical/free 转换 (19)–(21)。它们分别已有旧 §13 和谱 §16.1 的证据。本审查未证明 gap flows、norming canonical、共同水平集正规或一般 M 的 Liouville 最大性，也未给任何 ambient 开集上的 residual 结论。

## 7. 新主传递稿的逐项判定

已另外实读 [同一 strong Hilbert 主传递稿](general_m_high_gap_same_strong_hilbert_transfer_20261011.md)。其 §2 (3)–(4) 的 \(\mathcal C_k\) 与逆和本稿 (19)–(20) 完全等价：主稿先解 \(Z^TP=2(u-CQ)/(i\kappa)\)，本稿先解 \(p\) 再恢复 \(P\)。两者保留所有格点零和与实共轭条件。

主稿 §3 (7)–(8) 使用完整 \(\mathcal A_j(k)\) 的 endpoint extractor，奇轴规定投影和偶轴 \(i\mathcal A_j\) 的旋转正确。每步仅有限 Fourier 导数要求，故能与紧像源 margin 一起选择严格正新窗口，旧窗口冻结；其 (11) 的固定模导数极限与本稿 (16)–(17) 相同。

主稿 §1 区分旧小 \(|\delta|\) 图与另一个满足 (NR) 的均匀叶是必要的。后者重新执行旧 §§17.1–17.3 的图构造，依赖的是对全 \(c\ne0\) 已有的 §§11–13；不需要旧 §14 的 charge Hessian 见证。只要按主稿所述重建该叶自己的强链和正窗口，就不是把旧图跨叶搬运。

主稿 §4 通过 low 全纯性一次缩参数球，§5 由 exact Hessian 重新构造每个非零 minor，然后在该同一球上作 Baire 交，逻辑成立。Re/Im 的复延拓借用准确负频共轭通道，不把所有正频 gap 当实值。finite test lines 为旧合法 strong plots，检测的是实际物理 differential；与旧 charge minors 作交只给分别独立，主稿正确保留“合并联合块独立”仍未证的限制。

判定：PASS。没有需要修改新主传递稿的公式或结论。第 2 节的复域包含与外复合统一收敛说明，可作为主稿 §3 引用旧 §17.2 时的展开证据。

