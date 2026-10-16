# 一般 M 原物理场到标量有理算子的状态图：独立线性化

2026-10-11。本稿独立核验状态维数、原 split frame 的局部逆与常背景处的标量线性化。未重跑既存脚本；只写本文件，共享进度由父任务合并。

源稿：[原全周期矩阵 Lax 构造](../dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md) §§1–2；[实际谱独立审稿](../../刘维尔可积性/research/spectral_independent_review_20261011.md) §§16–17。

结论：

1. 对每个有限 \(M\ge3\)，保留原 split frame 时，\(q\) 加每行一个非对角 \(V\) 元素就有显式、零阶、逐点的物理状态逆。完整 \(q,r,V\) 并非自由的 matrix-AKNS 场。
2. 在 \(b_j=0,\ d_j=\delta=S/M\ne0\) 背景，正规标量分子/分母的 \(2(M-1)\) 个系数，对固定分量均值的全部非零 Fourier 模式具有可逆线性化。唯一退化频率是零频率。
3. 若允许分量均值变化，全部 \(2(M-1)\) 个常数切向被该背景的标量算子消去。常数场的站点置换给出精确非唯一性。
4. 非零模式 symbol 给出零均值 \(C^\infty\) 空间之间的线性拓扑同构；它本身尚不证明非线性 Banach 逆、谱/norming 逆或物理 Liouville 完备性。

## 1. 物理维数与准确 frame

记 \(m=M-1\)，站点 \(j=0,\ldots,m\)，
\[
S=\sum_jd_j\ne0,\qquad B=S^{-1}\sum_jb_jd_j,\qquad
\Delta_j=b_j-b_m\ (j<m),\quad\Delta_m=0.
\]
对给定 \(S,B\) 的叶，自由场恰为 \((\Delta_{\rm first},d_{\rm first})\)，共 \(2m\) 个函数；其余分量为
\[
d_m=S-\sum_{j<m}d_j,\quad
b_m=B-\frac1S\sum_{j<m}d_j\Delta_j,\quad b_j=b_m+\Delta_j.
\tag{1}
\]
以下用 centered \(B=0\) 表示。结论对任意给定非零 \(S\) 与外部 \(B\) 分别成立，不把 \(c,\Gamma\) 固定成全相域数值。

原稿的 \(T=[d/S,Z]\)、\(K=E-(d_{\rm first}/S)1^T\) 给
\[
\mathscr L=D-q(DI_m-V)^{-1}r.
\tag{2}
\]
\(q,r,V\) 的 frame 已由站点顺序与 \(Z_j=e_j-e_m\) 标定。内部变换
\[
\widetilde q=qG,\quad\widetilde r=G^{-1}r,\quad
\widetilde V=G^{-1}VG-G^{-1}G_x
\tag{3}
\]
保持标量算子不变，故未标定的全部矩阵元素不能视作自由物理坐标。周期 gauge 的 holonomy 以及非周期 gauge 的端点作用不能省略。

## 2. M≥3：原 frame 的零阶显式逆

centered 原 \(C\) 的对角为 \(b_i\)，非对角为
\(d_i\operatorname{sgn}(j-i)\)。直接乘 \(CZ\) 得
\[
q_j=\Delta_j-d_j-2\sum_{k=j+1}^{m-1}d_k-d_m,
\tag{4}
\]
\[
V_{ij}=\delta_{ij}(b_i-d_i)
+d_i\left(-2\mathbf1_{i>j}-q_j/S\right),\quad i,j<m.
\tag{5}
\]
等价地
\[
\Delta_j=q_j+S+\sum_{\ell<m}\operatorname{sgn}(\ell-j)d_\ell.
\tag{6}
\]

常背景满足 \(q_j^*=-2(m-j)\delta\)。在 (5) 的非对角项中，\(i<j\) 时的 \(d_i\) 系数为 \(2(m-j)/M>0\)，\(i>j\) 时为 \(-2(j+1)/M<0\)。因此 \(m\ge2\) 时，每行任选一个 \(j(i)\ne i\)，就在背景的一个共同邻域有
\[
\boxed{\quad d_i=
\frac{V_{i,j(i)}}{-2\mathbf1_{i>j(i)}-q_{j(i)}/S}.\quad}
\tag{7}
\]
可以固定选择 \(j(i)=i+1\)（\(i<m-1\)），以及 \(j(m-1)=0\)。再用 (6)、(1) 恢复全部物理场。

所以 \((q_i,V_{i,j(i)})_{i<m}\) 恰为 \(2m\) 个独立的逐点状态坐标，在乘法代数 \(H^s,\ s>1/2\) 上局部解析，且没有 derivative loss。固定 free 分量均值仍在目标中通过 (7)、(6) 施加；其余 \(V,r\) 不可自由赋值。

其余 \(V\) 由 (5) 给出代数约束，\(r=K(Cd-d_x)/S\) 给出微分约束。形式函数维数上，完整 \(q,r,V\) 的物理 image 有 \(m^2\) 个约束。若保留未中心化的完整 \(V\)，其对角也可恢复 \(b_i,B\)；选出的非对角小图使用原已标定的外部 \(B\)。

## 3. M=2 的准确例外与尺度核验

当 \(m=1\) 没有非对角 \(V\)。令
\(u=b_0-b_1,\ v=d_0-\delta,\ S=2\delta\)，
\[
q=-S+u,\quad V=-2uv/S,\quad
r=\frac{(\delta^2-v^2)(1+u/S)-v_x}{S}.
\tag{8}
\]
在 \(u=v=0\)，
\[
\dot q=\dot u,\quad \dot V=0,\quad
\dot r=\dot u/4-D\dot v/S.
\tag{9}
\]
因此 \(q,V\) 不能线性恢复 \(v\)；固定其均值后，\(q,r\) 的逆使用 \(D^{-1}_0\)。这与已审的 M=2 mixed 状态逆一致。

下文的全 M Fourier 式在 M=2 精确给出：取
\(h_0=h,h_1=-h,k_0=k,k_1=-k\)，则
\[
P_z=2z\delta(\delta h+pk),\qquad
\mathcal R_2(p)=4\delta p,\qquad
\dot{\mathscr L}
=-e^{zx}\frac{z(\delta h+pk)}{p(p+z)}.
\tag{10}
\]
直接用 (8) 得 \(\dot u=2h,\ \dot r=h/2-zk/S\)，于是
\[
\dot{\mathscr L}
=e^{zx}\left[-\frac{\delta h}{p}
+\frac{\delta h-zk}{p+z}\right],
\]
与 (10) 完全一致。原 \(-2S\) 和 monic denominator 的尺度未改变。

## 4. 具有 2m 个函数的正规标量分式

定义 row recursion
\[
q^{[0]}=q,\qquad q^{[a+1]}=Dq^{[a]}+q^{[a]}V,\qquad
\mathcal O=\begin{pmatrix}q^{[0]}\\\vdots\\q^{[m-1]}\end{pmatrix}.
\tag{11}
\]
当 \(\det\mathcal O\ne0\)，唯一的 \(c_a\) 满足
\(q^{[m]}=\sum_{a<m}c_aq^{[a]}\)。对
\(\xi_x=V\xi+r\phi,\ y=q\xi\)，逐次微分消去 \(\xi\) 得
\[
Qy=\Pi\phi,\qquad Q=D^m-\sum_{a<m}c_aD^a,\qquad
\operatorname{ord}\Pi\le m-1.
\]
准确的 formal scalar operator 为
\[
\boxed{\quad\mathscr L=D-Q^{-1}\Pi=Q^{-1}N,\qquad N=QD-\Pi.\quad}
\tag{12}
\]
因此 \(Q\) 的 \(m\) 个低阶系数与 \(\Pi\) 的 \(m\) 个系数是 \(2m\) 个正规的标量 state 数据。保持左分母约定；左右分母互换会改变系数中的导数项。

背景 transfer \(t(p)=(p-\delta)/(p+\delta)\) 给
\[
\mathscr L_*(p)=S\frac{(p+\delta)^M+(p-\delta)^M}
{(p+\delta)^M-(p-\delta)^M}.
\tag{13}
\]
写
\[
\mathcal R_M(p)=(p+\delta)^M-(p-\delta)^M,\quad
Q_*(p)=\mathcal R_M(p)/(2S),\quad
N_*(p)=\big((p+\delta)^M+(p-\delta)^M\big)/2.
\tag{14}
\]
\(Q_*\) monic、次数 \(m\)；\(N_*\) monic、次数 \(m+1\)。两者互素：若和与差都为零，则 \((p+\delta)^M=(p-\delta)^M=0\)，与 \(\delta\ne0\) 矛盾。因此 \(\Pi_*=pQ_*-N_*\) 与 \(Q_*\) 亦互素。

背景 proper 部分有最小分母次数 \(m\)。若 (11) 在背景不满秩，其 Krylov 关系将给次数小于 \(m\) 的输出分母，矛盾。故 \(\mathcal O_*\) 可逆，(12) 在一个 \(C^{m-1}\) 背景邻域成立。这是局部 differential state 图；未在此构造低 \(L^2\) 邻域上的同一非线性 Banach 逆。

## 5. 从原 transfer 直接求任意 Fourier 模式

令
\[
\dot b_j=h_je^{zx},\quad\dot d_j=k_je^{zx},\quad
z=2\pi in/L,\quad \sum_jh_j=\sum_jk_j=0.
\tag{15}
\]
最后两个约束来自 (1) 的背景点态线性化。固定各 free 分量均值时取 \(n\ne0\)。

用 \(f(D)e^{zx}=e^{zx}f(D+z)\)，单站 variation 为
\[
\dot T_j=e^{zx}\frac{-2(\delta h_j+pk_j)}
{(p+\delta)(p+z+\delta)}.
\tag{16}
\]
按原顺序 \(T_m\cdots T_0\) 求导，令
\[
w=p^2+zp-\delta^2,\quad A=w+z\delta,\quad C=w-z\delta,
\]
\[
P_z(p)=\sum_{j=0}^m(\delta h_j+pk_j)A^{m-j}C^j.
\tag{17}
\]
由于各站背景相同，
\[
\dot{\mathcal M}
=e^{zx}\frac{-2P_z(p)}{(p+\delta)^M(p+z+\delta)^M}.
\]
原 \(\mathscr L=-2S(\mathcal M-I)^{-1}-S\) 因而满足
\[
\boxed{\quad\dot{\mathscr L}
=e^{zx}\frac{-4S P_z(p)}{\mathcal R_M(p+z)\mathcal R_M(p)}
=e^{zx}\frac{-P_z(p)/S}{Q_*(p+z)Q_*(p)}.\quad}
\tag{18}
\]
这是原物理场到完整标量算子的 variation，不依赖 matrix traces 或 NLS Poisson 结构。

## 6. 可逆 symbol 与准确退化阶

定义
\[
H(w)=\sum_{j=0}^m h_j(w+z\delta)^{m-j}(w-z\delta)^j,\quad
K(w)=\sum_{j=0}^m k_j(w+z\delta)^{m-j}(w-z\delta)^j.
\]
由 (15)，\(H,K\) 次数均不超过 \(m-1\)，且
\[
P_z(p)=\delta H(w)+pK(w),\qquad \deg P_z\le2m-1.
\]

若 \(z\ne0\)，\(c=z\delta\ne0\)，则
\((w+c)^{m-j}(w-c)^j,\ j=0,\ldots,m\)
线性无关：除以 \((w+c)^m\) 后，是
\(((w-c)/(w+c))^j\) 的各次幂。受 \(\sum h_j=0\) 约束的 \(M\) 个 \(h_j\)，故与全部次数不超过 \(m-1\) 的 \(H\) 一一对应；\(k,K\) 同理。

另外 \(\mathbb C[p]=\mathbb C[w]\oplus p\mathbb C[w]\)。因为 \(w(p)=w(-z-p)\)，若 \(\delta H(w)+pK(w)=0\)，替换 \(p\mapsto-z-p\) 后相减就得 \((2p+z)K(w)=0\)，所以 \(K=H=0\)。维数均为 \(2m\)，于是满秩。

采用源坐标 \(h_0,\ldots,h_{m-1},k_0,\ldots,k_{m-1}\)，以约束消去末站；目标按 \(p^0,\ldots,p^{2m-1}\) 排列，有准确 determinant
\[
\boxed{\quad
\det[(h,k)\mapsto P_z]
=(-1)^{m(m-1)/2}\delta^m(2z\delta)^{m(m+1)}.
\quad}
\tag{19}
\]
证明：每组约束基
\((w+c)^{m-j}(w-c)^j-(w-c)^m,\ j<m\)
的 coefficient determinant 为
\((2c)^{m(m+1)/2}\)。先把完整基写在
\((w+c)^{m-\ell}\) 上，三角 diagonal 是 \((-2c)^j\)，反转行序消去其符号；减末列后最高次行成为 \((0,\ldots,0,1)\)。最后从 \(H,K\) 到 \(P_z\) 的 determinant 为
\((-1)^{m(m-1)/2}\delta^m\)：各列的最高次数按偶数、奇数排列。

所以非零 Fourier 模式具有秩 \(2m\)，不存在额外实 Fourier 共振。内部 slow eigenvalues 不引入新的退化频率。

## 7. 正规分子/分母系数的线性化等价

令
\(\dot Q=e^{zx}\alpha(p),\ \dot\Pi=e^{zx}\beta(p)\)，
\(\deg\alpha,\deg\beta<m\)。对左分式 (12) 求导给
\[
\dot{\mathscr L}
=e^{zx}\frac{\alpha(p)\Pi_*(p)-\beta(p)Q_*(p)}
{Q_*(p+z)Q_*(p)}.
\tag{20}
\]
故与物理源的准确关系为
\[
\alpha(p)\Pi_*(p)-\beta(p)Q_*(p)=-P_z(p)/S.
\tag{21}
\]
因 \(\gcd(Q_*,\Pi_*)=1\)，左侧是 \(2m\) 维同构：若为零，则 \(Q_*\mid\alpha\)，由次数限制得 \(\alpha=\beta=0\)。其 determinant 与 \(z\) 无关且非零。因此到正规 scalar coefficients 的 symbol 满足
\[
\boxed{\quad\det\mathcal A_M(z)=C_{M,\delta}z^{m(m+1)},\quad
C_{M,\delta}\ne0.\quad}
\tag{22}
\]

矩阵元素是 \(z\) 的多项式，逆矩阵是有限 Laurent 多项式。所以在固定分量均值的线性切空间，正逆向仅含有限阶 \(D,D^{-1}_0\)，给出
\[
D\mathcal F_*:(C^\infty_0)^{2m}\longrightarrow
(C^\infty_0)^{2m}
\]
的拓扑同构。正逆向可能需要不同的 Sobolev derivative budgets，不能直接称作同阶 \(H^s\) 的有界 Banach 同构。

这个结论不自动给非线性 inverse-function 或 Nash–Moser 定理。仍需邻域内 uniform tame inverse、非线性 image 的均值约束与适当尺度。尤其 nonlinear coefficient 的均值未必等于其背景值；上述目标零均值空间是背景处的线性切空间。

## 8. 零模式 kernel 与精确 permutation 反例

若 \(z=0\)，则 \(A=C=p^2-\delta^2\)，
\[
P_0(p)=(p^2-\delta^2)^m
\left(\delta\sum_jh_j+p\sum_jk_j\right)=0.
\tag{23}
\]
所以只固定 \(S,B\)、允许分量常数均值变化时，全部 \(2m\) 个常数方向都是 kernel。在均匀背景上一般的可微局部双逆不可能成立。

还有精确的非单射反例。足够小的常数场保持
\(\sum d_j=S,\ \sum b_jd_j=SB\) 时，
\[
\mathcal M(D)=\prod_{j=0}^m
\frac{D-b_j-d_j}{D-b_j+d_j}
\]
的各 transfer 彼此交换，故任意站点置换给同一完整标量算子。令 \(b_j=0,\ d_j=\delta+\varepsilon a_j\)，\(\sum a_j=0\)，交换两个不同的 \(a_j\)，就得到不同状态。二者在 \(\varepsilon\to0\) 时趋于同一个均匀背景，因此包含可变分量均值的任何背景邻域都不是 scalar state map 的单射域。

固定各原 free 分量均值排除了该常数反例与线性 kernel；此时 (22) 给正面的全 M 线性化。站点顺序与正规分式约定仍须保留，直至证明非线性逆。

## 9. Floquet class family 不能替代 state coefficients

上述恢复使用 \(x\)-依赖的正规标量 state coefficients。在常背景，原 traceless connection 是常数。对任意非零 Fourier perturbation，Duhamel 与 trace 循环性给
\[
D(r^{-1}\operatorname{tr}N_\lambda^r)_*
\cdot\dot z
=\int_0^L\operatorname{tr}
\left(N_{\lambda,*}^{\,r}\dot{\mathsf L}_\lambda(x)\right)dx=0.
\tag{24}
\]
所以全部实际 Floquet class functions 的一阶 variation 在该零均值切空间为零，而 (22) 的 scalar state coefficients 满秩。实际谱迹对合、fast 支 \(C_n\) 展开与辅助流不能替代 divisor/norming inverse。

已通过：全 M 物理维数，M≥3 framed split 的显式状态逆，常背景正规 scalar coefficients 的非零模式可逆 symbol，M2 原尺度，以及可变分量均值的具体 kernel 与精确非单射反例。

尚未通过：全 M 同一低阶邻域上的非线性 state inverse，一般 physical action-angle chart，Hamilton 闭包等于共同微分核，以及完整 Liouville 最大性。

