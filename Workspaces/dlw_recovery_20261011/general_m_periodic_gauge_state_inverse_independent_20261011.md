# 一般 M 周期规范与真实物理状态逆：独立审计

2026-10-11。本稿只审物理状态映射及其有限约束，不把矩阵谱迹的对合升级为逆谱完备性。未运行旧脚本，未修改共享记录。

依赖原构造 [GENERAL_PERIOD_MATRIX_LAX.md](../dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md) §§1–2；本轮独立闭式计算见 [general_m_inverse_linearization_independent.md](general_m_inverse_linearization_independent.md) §§5–7。既有 scalar factor inverse 的适用域见 [nonlinear_inverse_checks.md](../../刘维尔可积性/research/nonlinear_inverse_checks.md) §§1、4–6；那部分不是本轮新证明。

结论：对每个有限 M≥2，固定原 free 分量空间均值的周期叶，在均匀非零背景及下述无 Fourier alias 条件下，原物理场有一张真正的、解析的 framed covariant-AKNS 状态图

\[
(q-q_*,d_{\rm first}-\delta\mathbf1)\in
(L^2_0)^m\times(H^1_0)^m
\quad\longleftrightarrow\quad
(P_0a,P_0b)\in(L^2_0)^{2m},\qquad m=M-1.
\tag{1}
\]

它在同一个低阶邻域上保留全部高阶 Sobolev 正则性。任意实的空间常数 B 可作为参数保留，不能把这项状态定理解释为强制 Γ 守恒。完整 framed 数据 (a,b,H) 的物理像是有限余维图。该结果补足一般 M 的低阶非线性 **状态逆**，尚未给谱 divisor/norming 逆或一般 M 的 Liouville 最大性。

## 1. 物理坐标、B 参数和准确背景

令站点 j=0,…,m，
\[
S=\sum_jd_j=hMc/8\ne0,\quad \delta=S/M,
\quad B=S^{-1}\sum_j b_jd_j=\Gamma/(2c),
\quad \Delta_j=b_j-b_m\ (j<m).
\]
这里物理 b_j=U_j/2；下文没有下标的 b 是规范后的列向量，二者不同。原均匀背景为 d_j=δ、b_j=B。固定 free 分量均值的零平均叶满足
\[
\langle d_j\rangle=\delta,\qquad \langle\Delta_j\rangle=0.
\]
q 与 d_first 是等价的 free 坐标：
\[
\Delta_j=q_j+S+\sum_{\ell<m}\operatorname{sgn}(\ell-j)d_\ell,
\quad d_m=S-\sum_{j<m}d_j,
\quad b_m=B-S^{-1}\sum_{j<m}d_j\Delta_j.
\tag{2}
\]
因此 \(q-q_*\) 与 \(d_{\rm first}-\delta\mathbf1\) 分别零平均。式 (2) 是原场坐标变换，不施加函数 ansatz。

原 split 给
\[
\mathscr L=D-q(DI_m-V)^{-1}r,
\quad q=\mathbf1^TCZ,
\quad r=\mathsf K(Cd-d_x)/S,
\quad V=\mathsf KCZ,
\quad \mathsf K=E-d_{\rm first}\mathbf1^T/S.
\tag{3}
\]
背景独立计算如下。记 \(A_{ij}=\operatorname{sgn}(j-i)\)，i,j=0,…,m，则
\[
C_*=\delta A+B(I-\mathbf1\mathbf1^T/M),
\]
\[
q_{*,j}=-2\delta(m-j),\qquad
r_{*,i}=\delta(m-2i)/M,
\]
\[
(V_*-BI)_{ij}
=\delta\left[\operatorname{sgn}(j-i)
+\frac{m-1-2j}{M}\right],\qquad i,j<m.
\tag{4}
\]
M=2 时 V_*−BI=0、q_*=−S、r_*=δ/2。M=3 时
\[
V_*-BI=\frac\delta3
\begin{pmatrix}1&2\\-2&-1\end{pmatrix}.
\]

更强的是全场恒等式：改变共同 B 时，q、r 完全不变，V 增加 B I。原 C 的 B 部分是 \(B(I-d\mathbf1^T/S)\)；它消去 d/S 且在 Z 列上为 BZ，所以可直接验证。下面的 G、a、b 不依赖 B，而 H 增加 B I。Π=(P_0a,P_0b) 单独不恢复 B；须把 B 留作参数，或保留 H 的有限数据。

## 2. 无 alias 的准确条件

写 \(V_0=V_*-BI\)。其特征值是
\[
p_k=-i\delta\cot(\pi k/M),\qquad k=1,\ldots,m.
\tag{5}
\]
证明可由背景最小 realization 得到：
\[
\mathscr L_*(p)=
S\frac{(p+\delta)^M+(p-\delta)^M}
{(p+\delta)^M-(p-\delta)^M},
\quad
K_*(p)=\frac{(p+\delta)^M-(p-\delta)^M}{2S}.
\]
分子与分母互素，m 维 realization 的特征多项式因而就是 monic K_*。K_* 根由非平凡 M 次单位根解出 (5)，全部互异。

设周期为 L，k_0=2π/L。所需条件是
\[
ik_0n\notin\operatorname{spec}(\operatorname{ad}V_0)
\qquad(n\in\mathbb Z\setminus\{0\}),
\tag{6}
\]
即
\[
\delta\{\cot(\pi j/M)-\cot(\pi k/M)\}
\ne k_0n
\quad(j,k=1,\ldots,m;\ n\ne0).
\tag{7}
\]
对固定 M,L，它只排除可数的 δ 值。一个简单充分条件是 \(\|\operatorname{ad}V_0\|<k_0\)，因此足够小的非零 |δ| 总符合。M=2 没有这种非零 Fourier alias，任意 δ≠0 均符合。

式 (6) 是此规范坐标的条件。碰到 alias 只说明这张 \(\langle G\rangle=I\) 坐标的线性方程可能失去唯一性，不能据此断言原物理状态逆或可积性失败。原完整 scalar differential 的所有非零 Fourier 模式仍没有 kernel。

## 3. 周期 mean-normalized gauge 的低阶解析存在

要求
\[
G_x=VG-GH,\qquad \langle G\rangle=I,
\qquad H\text{ 为常矩阵}.
\tag{8}
\]
置 G=I+g、\(\langle g\rangle=0\)。平均式强制
\[
H=\langle V(I+g)\rangle.
\]
因此只须解
\[
\mathcal F(g,V)
=Dg-P_0[V(I+g)]+g\langle V(I+g)\rangle=0.
\tag{9}
\]
这是 \((H^1_0)^{m\times m}\times(L^2)^{m\times m}\to(L^2_0)^{m\times m}\) 的解析映射：H¹ 在一维是 L² 的乘子，式中没有 L²×L² 乘法。

在 g=0,V=V_*，
\[
D_g\mathcal F=D-\operatorname{ad}V_0,
\qquad
\dot g=(D-\operatorname{ad}V_0)^{-1}P_0\dot V,
\quad \dot H=\langle\dot V\rangle.
\tag{10}
\]
式 (6) 给 H¹_0→L²_0 有界同构。大频率下其 resolvent 是 O(|n|⁻¹)，有限个低频由 (6) 排除奇点。Banach 解析逆函数定理给同一个 L² 的 V 邻域上的 G∈H¹、H∈Mat_m；G 充分近 I 所以处处可逆。实 V 得实 G,H。该结论不是先取非周期 fundamental matrix 后丢弃 holonomy。

令
\[
a=qG,\qquad b=G^{-1}r.
\tag{11}
\]
则 a,b 都周期，而且
\[
DI-V=G(DI-H)G^{-1},\qquad
\mathscr L=D-a(DI-H)^{-1}b.
\tag{12}
\]
扩大的 block gauge diag(1,G) 是周期的，因此原 block connection 与 \(\begin{psmallmatrix}\lambda&a\\b&H\end{psmallmatrix}\) 的 monodromy 通过同一初始值作相似变换；任何谱迹都保留。H 是保留的内部 holonomy 资料：内部方程的 monodromy 与 e^{LH} 共轭。

## 4. 物理映射的低阶预算

由 (2)–(3)，在 S≠0 的图内
\[
V=BI+\widetilde V(q,d),\qquad
r=-d_{{\rm first},x}/S+F(q,d),
\tag{13}
\]
其中 \(\widetilde V,F\) 都是零阶多项式，只含固定 S 的分母；对 q 至多线性，d 次数有限。导数项准确来自 \(\mathsf Kd_x=d_{{\rm first},x}\)，因为 \(\mathbf1^Td_x=0\)。

故在
\[
X_0=(L^2_0)^m\times(H^1_0)^m
\]
上，V,r∈L²，G∈H¹，a,b∈L²，且所有映射解析。这里 qL²、dH¹ 的不同阶数是实际预算；不把 b 当作同阶 q,dL² 的普通乘法表达。

令 u=δq、v=δd_first。在背景处 \(\dot V=W(u,v)\) 与 F 的变分 Z(u,v) 都是常系数零阶线性表达，而
\[
\dot a=u+q_*g,
\qquad
\dot b=Z(u,v)-Dv/S-g r_*.
\tag{14}
\]
固定 free 均值给 \(\langle W\rangle=0\)，所以 \(\dot H=0\)；g、\(\dot a\)、\(\dot b\) 也零平均。谱参数 B 的共同平移不改变任何一项。

## 5. 不靠 δ 小性的全非共振背景微分逆

设 Π(q,d)=(P_0a,P_0b)。背景微分平移不变，按各非零 Fourier 模式分解，源/目标每模都是 2m 维。

若某非零 Fourier 模式满足 DΠ(u,v)=0，则 (14) 给 \(\dot a=\dot b=0\)，并且 \(\dot H=0\)。由实际全阶算子恒等式 (12)，\(\dot{\mathscr L}=0\)。而原物理场到完整 scalar operator 的独立 symbol 证明给
\[
\dot{\mathscr L}
=e^{zx}\frac{-4S P_z(p)}{\mathcal R_M(p+z)\mathcal R_M(p)},
\quad z=ik_0n\ne0,
\]
\[
P_z(p)=\sum_{j=0}^{m}(\delta h_j+pk_j)
(w+z\delta)^{m-j}(w-z\delta)^j,
\quad w=p^2+zp-\delta^2,
\quad \sum h_j=\sum k_j=0.
\tag{15}
\]
在约束空间，\(P_z=\delta H_1(w)+pK_1(w)\)。反射 p↦−z−p 令 w 不变，故 P_z=0 先强制 K_1=0，再 H_1=0；因 Bernstein 基 \((w+z\delta)^{m-j}(w-z\delta)^j\) 独立，全部 h,k 为零。物理 h,k 与 u,v 的背景坐标变换是可逆的，因此 u=v=0。每个 Fourier block 因维数相等而可逆。

这也给统一 Sobolev 有界性。令 f=Dv，以 (u,f) 标记源。对 |n|→∞，
\[
g=O(|n|^{-1})u+O(|n|^{-2})f,
\]
\[
D\Pi(n)=
\begin{pmatrix}I&0\\ Z_u&-I/S\end{pmatrix}
+O(|n|^{-1})
\quad\text{在 }(u,f)\text{ 坐标中}.
\tag{16}
\]
主矩阵是可逆下三角矩阵。它不是默认的单位阵；Z_u 的零阶交叉项必须保留。所有充分大频率统一有界可逆，有限个低频由上一段单射性给有限常数。于是
\[
D\Pi_*:(L^2_0)^m\times(H^1_0)^m
\longrightarrow(L^2_0)^{2m}
\tag{17}
\]
是有界同构。同一 Fourier 论证对任意 H^N×H^{N+1} 成立。

Banach 解析逆函数定理现在给式 (1) 的真实非线性局部双逆。这里 scalar symbol 被用来排除这张规范的低频 kernel；没有把 scalar trace differential 当成 state differential。所有实际 Floquet class functions 在均匀背景的零均值切向上仍可一阶为零。

## 6. 同一个低阶域上的高阶逆

低阶逆给 qL²、dH¹、GH¹。给定规范 a,b∈H^N，利用 (11)、(13)、(8) 可直接写成
\[
q=aG^{-1},\qquad
G_x=(BI+\widetilde V(q,d))G-GH,
\]
\[
d_{{\rm first},x}=S F(q,d)-S G b.
\tag{18}
\]
若 N≥1，由 G,dH¹ 以及 H¹ 乘法代数得 qH¹，右侧均 H¹，故 G,dH²。再依次：若 a,bH^n 且 G,dH^n，式 (18) 给 qH^n 与 G,dH^{n+1}。由归纳得到
\[
a,b\in H^N
\Longrightarrow q\in H^N,\quad d,G\in H^{N+1}
\qquad(N\ge0).
\tag{19}
\]
只在同一低阶域中要求输入的高阶正则性，未为每个 N 重新缩小 δ 或另选一张解域。式 (18) 的线性化给相同的高阶 bootstrap；低阶逆的唯一性、闭图定理给每个高阶线性逆有界。因此在共同低阶域与 H^N 的交上，逆在各高阶 Banach 拓扑局部解析。全部 C∞ 输入在同一低阶域恢复 C∞ 物理场。

## 7. 完整数据的约束数与 B 恢复

对固定 S、fixed free component means、给定 B，低阶物理像可用 y=(P_0a,P_0b) 参数化。其余
\[
\langle a\rangle=\mathcal A(y),\quad
\langle b\rangle=\mathcal B(y),\quad
H=BI+\mathcal H(y)
\tag{20}
\]
是解析有限维函数。它在完整目标 \((L^2)^{2m}\times\mathrm{Mat}_m\) 中是 2m+m² 个有限约束的 graph；这些不是 m² 个随 x 的自由 AKNS 场约束。图包含一般周期函数的开放低阶域，不能缩成有限模或特殊解族。

如果 B 也作为 free 外部参数加入源，只剩 2m+m²−1 个有限 graph 约束。B 可从同一 y 与 H 恢复，例如
\[
B=m^{-1}\operatorname{tr}\{H-\mathcal H(y)\}.
\tag{21}
\]
任意 B(t) 时按每个时刻使用该参数族；本稿没有推导 B_t=0。S 及其他组件 Casimir 均值也可作为有限参数在本图附近保留；固定它们描述一张 Poisson 叶，并非将一般物理场变成函数 ansatz。

若只保留完整 scalar \(\mathscr L\)，它对内部常数 GL_m 的变化
\[
(a,b,H)\mapsto(aC,C^{-1}b,C^{-1}HC)
\]
不变。这些有限 frame 数据不可擅自视作另一组独立物理场。原 \(\langle G\rangle=I\) 规范与 (20) 标记了实际物理截面。

## 8. 与 2m 个 scalar rational 系数的对应

令原 period product \(P=Q^{-1}R\)，Q,R monic M 阶，\(\nu=B-S\)。
\[
K=(Q-R)/(2S),\qquad H_{\rm diff}=Q+\nu K,
\qquad \mathscr L=K^{-1}H_{\rm diff}.
\tag{22}
\]
K 是 monic m 阶，H_diff 是 monic M 阶。原 \(\mathscr L\) 的 D⁰ 项为零，等价于两者的次首系数相等。因此 m+M−1=2m 个函数，恰与物理 free 场一致；背景是
\[
K_*={((D+\delta)^M-(D-\delta)^M)}/{(2S)},
\quad H_{{\rm diff},*}=\tfrac12[(D+\delta)^M+(D-\delta)^M]
\]
（B=0）。这与子审中的 monic denominator Q 和 numerator N 完全一致。

原 finite jet denominator recovery、cyclic repeated-Floquet flags、非零 Wronskians、heterogeneous inverse bubble 在已证明的实际 rational image 上可从完整 \(\mathscr L\) 恢复原物理场，带有限 derivative budget。zero component means 不把共同 factor mean冻结：两个 repeated multipliers 只固定比值 \(e^{2\delta L}\)，共同 multiplier 仍随状态变化。

此段 scalar 非线性 inverse 是既存 factor theorem 的准确接合，不是由本稿 (1) 自动得到的同阶 scalar coefficient Banach IFT。一般 finite coefficients 的开放域还须满足完整 rational/factor/Floquet image 条件；只解有限个 negative equations 不会保证无限尾部全消失。

## 9. 审结与剩余工作

本轮新增证成：mean-normalized 周期规范在低 L² 域解析存在；一般 M 物理到 framed periodic a,b 的低阶非线性状态双逆；任意无 alias 非零均匀背景的有界微分逆；同一低阶域的全部高阶正则 bootstrap；准确的有限约束及 B 参数保留。独立子审还给 full scalar symbol 的闭式 determinant 和可变均值的常量 kernel/精确 permutation 反例。

仍开放：general M 的谱 divisor/norming 数据重建这些 state coordinates，谱 actions 对原物理 Poisson 的闭包/极大性，以及与所有实际原时间流接合后的完整 Liouville 定理。矩阵 gauge 和 state inverse 无法单独填补这些谱完备性步骤。

## 10. 新主稿与 strong 背景接合的独立末审

已实际读回 [all_m_physical_holonomy_state_inverse_20261011.md](all_m_physical_holonomy_state_inverse_20261011.md) §§1–8 与 [root_general_m_periodic_state_inverse_audit_20261011.md](root_general_m_periodic_state_inverse_audit_20261011.md) 全文。除本稿式 (19) 的一个排版缺失反斜线外，分析链通过；该排版已修复。

主稿式 (15) 的两个原物理零阶微分可直接重新求出。若 \(\xi_i=u_i+\sum_{\ell<m}\operatorname{sgn}(\ell-i)v_\ell\)、\(t_i=\xi_i-M^{-1}\sum_{\ell<m}\xi_\ell\)，则
\[
\dot V_{ij}
=\delta_{ij}(t_i-v_i)-2v_i\mathbf1_{j<i}
+2(m-j)v_i/M-u_j/M,
\]
\[
\dot F_i=M^{-1}\left[t_i+(m-2i-1)v_i-2\sum_{j<i}v_j\right].
\tag{23}
\]
第二式来自
\(\delta(Cd)=\delta C\,\delta\mathbf1+\delta A\,Zv\)，后一项的第 i 行是
\(\delta[-v_i-2\sum_{j<i}v_j]\)，因而没有漏掉最后一个格点的变分或原 state frame 的 derivative。

主稿的 constant GL_m 横截性也通过：背景 \(V_0\) simple，proper scalar part 在每个极点的 residue 为
\[
\delta^2-p_\ell^2=\delta^2\csc^2(\pi\ell/M)\ne0.
\]
故 \(q_*P_\ell r_*\ne0\)。若 \((q_*X,-Xr_*,[V_0,X])=0\)，X 与 \(V_0\) 对易，所以 \(X=\sum x_\ell P_\ell\)；由 \(q_*P_\ell\ne0\) 得全部 \(x_\ell=0\)。这些 infinitesimal gauge 方向只在有限常数资料中，而物理 graph 的有限分量在背景微分为零。选择一个 m² 阶非零 minor，有限维 IFT 便排除近 I 的 constant gauge 在该物理 image 内的非唯一性。这没有排除 λ-dependent gauge，也没有证明 class 数据的完整 kernel。

既有 mixed/strong 小背景条件
\[
|\delta|<(k_0/2)\tan(\pi/(2M))
\]
已经保证式 (6)。M>2 时，令 \(\alpha=\pi/(2M)\)，
\[
\max_{j,k}|p_j-p_k|
=2|\delta|\cot(\pi/M)
<k_0\tan\alpha\cot(2\alpha)
=\frac{k_0}{2}(1-\tan^2\alpha)<k_0.
\tag{24}
\]
M=2 时 ad \(V_0=0\)，自动合法。因此这张状态逆在既有 strong 背景附近不另要求更小的 c。取域的交须保持为一个低阶开邻域；不能由此声称其中每一点已经具有所有作用量非零或最大性。

## 11. Cauchy 周期 frame 与常数 gauge 的补审

实际读取新主稿 §9 式 (27)。置 \(Q_0=G(0)\)、\(G^f=GQ_0^{-1}\)、\(H^f=Q_0HQ_0^{-1}\)、\(a^f=aQ_0^{-1}\)、\(b^f=Q_0b\)。G^f 周期且 G^f(0)=G^f(L)=I，因此 split monodromy 与 constant-H^f 系统的 full framed monodromy准确相同。uniform 的微分为
\[
\dot a^f=u+q_*g-q_*g(0),\qquad
\dot b^f=Z-Dv/S-g r_*+g(0)r_*,
\quad \dot H^f=[g(0),V_0].
\tag{25}
\]
P₀ 正好消去两个 constant 项，所以 \((P_0a^f,P_0b^f)\) 的微分仍是式 (14)，同一个物理低阶 IFT 成立。这张 finite graph 的均值和 H^f 一阶导数一般非零，不能沿用 mean-normalized graph 的 quadratic-only 性质。

新主稿 §8 去掉 explicit constant Q 近 I 的限制也通过：对于同一 uniform 邻域的两端 data，矩阵 \(\mathcal O(a,H)\) 的各行为 \(\langle a\rangle H^j\)，j=0,…,m−1；背景由 simple pole 非零 residues 得可逆。\(\mathcal O(zQ)=\mathcal O(z)Q\)，故 Q=\(\mathcal O(z)^{-1}\mathcal O(zQ)\) 本来就近 I。再用 §10 的 finite minor IFT 得 Q=I。

上述 coefficient-frame 定理本身不允许从 original class 数据猜测 Q₀。不过从原 **完整有标定 monodromy 函数**恢复 physical endpoint 的独立极限、以及 actual Fourier kernel inverse，可以另外解除这一有限 endpoint 输入；见 [独立 raw monodromy 审稿](general_m_raw_monodromy_state_extraction_independent_20261011.md)。这个新步骤只给低阶 framed state inverse，仍不将 raw samples称为加权 action coordinates。
