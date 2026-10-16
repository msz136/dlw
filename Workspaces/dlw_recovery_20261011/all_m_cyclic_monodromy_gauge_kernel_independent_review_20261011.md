# 全 M cyclic monodromy 周期规范引理：独立审查

2026-10-11。实际逐段读取 [根 cyclic 引理](all_m_cyclic_monodromy_gauge_kernel_20261011.md)，独立核 fixed-\(\lambda\) 等价、全部 periodic adjoints、局部 holomorphic right inverse。没有执行机器 checks、借助谱增长/Cartan B 或宣称 Hamilton density。

固定 cyclic 谱点的 theorem PASS，包括 Jordan 碰撞。局部 holomorphic 陈述应明确 variation 在整个小邻域中属于 commutator image；下面给精确表述和反例。原实际共同全谱核的应用满足该条件，故无需降低其适用结论。

## 1. Cyclic centralizer 与 normalized characteristic differential

对 cyclic \(N\in SL_M(\mathbb C)\)，取 cyclic vector \(v\)。若 \([C,N]=0\)，
\(Cv\) 唯一写成 \(p(N)v\)，\(\deg p\le M-1\)；交换关系使
\(CN^jv=p(N)N^jv\)，故
\[
\ker\operatorname{ad}_N=\operatorname{span}\{I,N,\ldots,N^{M-1}\},
\quad\dim\ker\operatorname{ad}_N=M.
\]
各 polynomial basis 独立，不需要 diagonalization。左乘 invertible \(N\) 把
\(\{N^{-1},I,\ldots,N^{M-2}\}\) 变为上述基，因此前一组也完整。

fixed determinant 的 actual variation 为
\(\operatorname{tr}(N^{-1}\delta N)=0\)；
\(\delta\operatorname{tr}N^r=r\operatorname{tr}(N^{r-1}\delta N)\)，
\(r=1,\ldots,M-1\)。这些零条件精确说
\(\delta N\) 与全 centralizer 在 ordinary complex bilinear trace pairing 下正交。
该 pairing 在整个 \(\mathrm{Mat}_M\) 非退化；**不要求**它在 centralizer 上非退化，Jordan 情形亦无此额外假设。

由
\[
\operatorname{tr}([G,N]C)=\operatorname{tr}(G[N,C])
\]
和 rank–nullity，
\[
\operatorname{im}(G\mapsto[G,N])
=(\ker\operatorname{ad}_N)^\perp,\qquad
\dim\operatorname{im}=M^2-M.
\]
因此所有 normalized trace/characteristic differential 零等价于
\(\delta N=[G,N]\)。subtract \(\operatorname{tr}G\,I/M\) 令 \(G\in\mathfrak{sl}_M\)，不改变 commutator。Newton identities 在 fixed determinant 约束下给 normalized characteristic coefficients 的完全等价；只有 fundamental trace 对 \(M>2\) 不足。

## 2. Actual periodic variation 与全部 adjoint branches

actual fundamental ODE variation
\[
Z=\delta Y\,Y^{-1},\quad Z_x=\delta A+[A,Z],\quad
Z(0)=0,\quad Z(L)=\delta N\,N^{-1}
\]
给
\[
g=Z+YGY^{-1},\qquad \delta A=g_x-[A,g].
\]
\(\delta N=[G,N]\) 准确给 \(g(L)=G=g(0)\)；周期 coefficients 和该 first-order ODE 使所有 endpoint jets 相等。trace \(Z=0\)、trace \(G=0\)，故 \(g\) smooth periodic slM-valued。
反向同初值 uniqueness 给 \(\delta N=[g(0),N]\)。符号、端点 conjugation 和 fixed determinant 均正确。

homogeneous periodic adjoints 必为
\[
h=YCY^{-1},\qquad [C,N]=0,\quad\operatorname{tr}C=0.
\]
centralizer 的 trace-free 部分由
\[
N^r-\frac{\operatorname{tr}N^r}{M}I,\qquad 1\le r\le M-1
\]
完整生成且线性独立：若其组合为零，则给 \(\deg p\le M-1\) 的 polynomial \(p(N)=0\)，与 minimal polynomial 阶 M 矛盾。actual \(F_r=\operatorname{tr}N^r\) 的 source-gradient adjoint 是
\[
r\,YN^rY^{-1};
\]
去 scalar 后恰为上述 basis 的 \(r\) 倍。因此全部 \(M-1\) periodic adjoint branches 无漏，cyclic Jordan 点也成立。非 cyclic \(N=\alpha I\) 的 centralizer 更大，trace constraints 与 polynomial adjoints 都不完整，cyclic 条件不能删。

## 3. 局部 holomorphic 等价的准确条件和构造

cyclic 是开条件：一个 fixed cyclic vector 的 Krylov determinant 在 \(\lambda_0\) 非零，连续性使其在小邻域仍非零。因此
\[
T(\lambda):G\mapsto[G,N(\lambda)]
\]
在 cyclic 邻域秩恒为 \(\rho=M^2-M\)。

若 \(A,\delta A\) 在该邻域以 periodic smooth functions 为值 holomorphic，且 normalized characteristic variations 对**每个** \(\lambda\) 恒等为零，则
\(\delta N(\lambda)\in\operatorname{im}T(\lambda)\)。
选 \(T(\lambda_0)\) 中一个非零 \(\rho\times\rho\) minor，冻结该 row/column index 组。邻域内此 minor 可逆；所选 \(\rho\) columns 形成 image 的 basis，选中的 \(\rho\) rows 在它们的 span 上 injective。
把其 inverse 作用到 \(\delta N\) 的选中 rows，并只在选中 columns 放系数，得到 local holomorphic \(G(\lambda)\)，且完整 rows 都满足
\([G(\lambda),N(\lambda)]=\delta N(\lambda)\)，因为右侧已属于 image。
再 subtract trace 和代入 \(g=Z+YGY^{-1}\)，便得 local holomorphic periodic slM \(g\)。

反向，local holomorphic periodic \(g\) 逐 \(\lambda\) 给 commutator identity，故邻域全部 characteristic variations 恒等零。
这证明的是 kernel identity 在一整个 cyclic 邻域中的 local holomorphic 等价；不是从单个点的一阶 kernel condition 自动延拓到邻域。

## 4. 单点条件不足：精确 cyclic Jordan 反例

取任意 \(L>0\)、\(M=2\)，spatial constant coefficients
\[
A(\lambda)=
\begin{pmatrix}\lambda&1\\0&-\lambda\end{pmatrix},
\qquad
\delta A(\lambda)=\lambda
\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\]
二者 entire、trace zero、periodic。实际 monodromy 是
\[
N(\lambda)=
\begin{pmatrix}
e^{L\lambda}&\sinh(L\lambda)/\lambda\\
0&e^{-L\lambda}
\end{pmatrix},
\qquad
N(0)=\begin{pmatrix}1&L\\0&1\end{pmatrix}.
\]
\(N(0)\) 是 cyclic Jordan，附近仍 cyclic。由于 \(\delta A(0)=0\)，fixed \(\lambda_0=0\) 的全部 normalized characteristic derivatives 零，取 \(g=0\) 即解。
但 actual variation 把 \(A\) 的 diagonal parameter 改成
\((1+\varepsilon)\lambda\)，所以
\[
\delta\operatorname{tr}N(\lambda)=2L\lambda\sinh(L\lambda),
\]
不在邻域恒零。故不存在一个邻域上对所有 \(\lambda\) 解周期规范方程的 \(g\)，无论是否要求 holomorphic。

已向根报告要求 §3 明写 image condition，并已实际读回根的修正：“全部 trace derivatives 在一个 cyclic \(\lambda_0\) 的小邻域内恒等为零”，同时明确单点条件不足。我的旧 simple-monodromy 短稿同一处省略也已同步补正。实际 physical 共同全谱微分核灭去所有 \(\lambda\) 的全部 characteristic derivatives，自动满足所需条件。修后的 fixed-point、periodic-adjoint completeness 和 local holomorphic 结论全部 PASS。

## 5. 范围

此引理只刻画 actual normalized connection 在 fixed cyclic 谱点和局部 cyclic 邻域的 gauge kernel，并证明 trace-power adjoints 的 pointwise 完整性。没有 entire \(g\)、跨所有谱点统一估计、谱增长、nonlinear norming inverse 或 Hamilton span density。
原未归一 connection 须另保留 scalar holonomy variation；不能把 source-dependent normalization 的额外方向丢掉。全 M nonlinear closed-kernel maximality 仍等待这些 periodic gauge variations 被实际 finite-\((r,\lambda)\) Hamilton directions 稠密生成的独立证明。
