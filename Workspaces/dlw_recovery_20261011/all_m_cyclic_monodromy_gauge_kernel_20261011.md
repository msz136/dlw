# 全 M 的 cyclic 单值矩阵谱微分核：包含 Jordan 碰撞

2026-10-11，root 独立推导。接续 [simple-monodromy 周期规范引理](all_m_spectral_infinitesimal_conjugacy_lemma_20261011.md)，本稿把其固定谱点与局部解析结论扩大到 **cyclic（minimal polynomial 阶 M）** 单值矩阵，允许非半单 Jordan 碰撞。仍不声称全 M Hamilton 闭包或完整谱逆。

## 1. 精确定理

设 smooth 周期 trace-free connection A(x,λ) 的 fundamental matrix 满足 Y_x=AY、Y(0)=I，N=Y(L)∈SL_M(ℂ)。固定 λ，假设 N cyclic。给任一 smooth 周期 trace-free variation δA 与其实际 ODE variation δN，则

\[
\delta\operatorname{tr}N^r=0\quad(1\le r\le M-1)
\quad\Longleftrightarrow\quad
\delta A=g_x-[A,g]
\text{ 有 smooth periodic }g\in\mathfrak{sl}_M.
\tag{1}
\]

没有要求 N 的 eigenvalues 不同，也不要求 diagonalization。det N=1 的变分自动为零；若研究未归一 connection，须另外保留 scalar holonomy 变分。

## 2. 有限矩阵证明：cyclic centralizer 及 trace pairing

cyclic N 存在 v 使 (v,Nv,…,N^{M−1}v) 成基。任一与 N 交换的 C 由 Cv 唯一确定：Cv=p(N)v，其中 p 唯一、deg p≤M−1；交换使 CN^jv=N^jp(N)v，故 C=p(N)。因此

\[
\ker\operatorname{ad}_N
=\operatorname{span}\{I,N,\ldots,N^{M-1}\},
\quad\dim\ker\operatorname{ad}_N=M.
\tag{2}
\]

N 可逆，左乘 N 把 span{N⁻¹,I,…,N^{M−2}} 映成 (2) 的基。因此这些 M 个矩阵本身亦为 centralizer 的基。

迹导数与固定 determinant 恰给

\[
\operatorname{tr}(N^{r-1}\delta N)=0\ (1\le r\le M-1),
\qquad \operatorname{tr}(N^{-1}\delta N)=0.
\tag{3}
\]

故 δN 对整个 centralizer 的普通非退化双线性 trace pairing 正交。对任意 G,C，tr([G,N]C)=tr(G[N,C])，于是 im(G↦[G,N]) 包含于 centralizer 的正交补；两者维数均为 M²−M，准确相等。式(3) 因此等价于存在 G 使 δN=[G,N]。以 G−tr(G)I/M 代替 G，可取 trace zero。Newton identities 给 (3) 与全部 normalized characteristic coefficients 零变分等价。

这一证明不用中央特征值的 Vandermonde 分离；即使 N 是单 Jordan 块，也成立。相反 N=αI、M>1 不 cyclic，只有迹变分约束绝不能给全部 δN 为 commutator，故不能去掉 cyclic 条件。

## 3. 周期 g、非唯一性与局部全纯依赖

实际 ODE variation 的 Z=δY Y⁻¹ 满足 Z_x=δA+[A,Z]、Z(0)=0、Z(L)=δN N⁻¹。对上节的 G 定义

\[
g=Z+YGY^{-1}.
\tag{4}
\]

则 g_x=δA+[A,g]，且 g(L)=δN N⁻¹+NGN⁻¹=G=g(0)。方程的周期系数使全部 endpoint jets 相等，故 g 光滑周期。trace Z=0 且 trace G=0，所以 g∈sl_M。反向直接由周期 g 得 δN=[g(0),N]。

周期 homogeneous adjoints 为 h=YCY⁻¹，其中 C∈centralizer(N)、tr C=0；由 (2)，全部这些解由实际 trace powers r=1,…,M−1 的 trace-free adjoints 精确生成。其维数恒为 M−1，也在 cyclic Jordan 碰撞处成立。

cyclic 是开条件。若 A、δA 对 λ 全纯，且全部 trace derivatives 在一个 cyclic λ₀ 的小邻域内**恒等为零**，则每个 λ 都有 δN(λ)∈im ad_N(λ)，矩阵 G↦[G,N(λ)] 的秩恒为 M²−M。选 λ₀ 处一个非零最大阶 minor，其逆给 image 上的局部全纯 right inverse（可先在 gl_M 取解再减 trace）。因此 (4) 可局部全纯依赖 λ。只在单点 λ₀ 灭去 trace derivatives 不能推出邻域内存在 g；全谱共同微分核的应用满足这里要求的恒等零。此证明不依赖选择特征向量或 Jordan 基随参数解析，避免碰撞处的假设。

没有据此断言跨全部 λ 的单个 entire g、谱增长界或统一全频估计。全 M actual 共同谱核仍需证明这些 gauge variations 属于真实物理 Hamilton span 的 C∞ 闭包。

## 4. 对一般物理 DLW 的意义与后续任务

将 [全 M 实际 affine connection](../../刘维尔可积性/research/spectral_independent_review_20261011.md) §16 的物理 variation 代入，即得每个 cyclic 谱点上 normalized class differential kernel 的准确描述。其所有 M−1 条周期 adjoint 通道都已由已审实际 trace powers 提供；对于 M>2 仅一个 fundamental trace 一般不够。

本结果只改进真实谱点上的局部核刻画，不补 nonlinear norming state 逆、不证明 all-M Hamilton 密度、不证明 common fiber regularity。新的 general-M block gauge 状态图可与此引理共同作为下一步 vector spectral inverse 的入口。
