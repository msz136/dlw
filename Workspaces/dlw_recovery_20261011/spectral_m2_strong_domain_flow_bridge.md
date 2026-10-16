# M=2 实际 Floquet Hamilton 流与 strong 可数共同域的接合

2026-10-11。独立推导，接续 `spectral_independent_review_20261011.md` §13–14 与 `mixed_independent_review_20261011.md` §16。先逐式审查 §14 的真实 \(C^1\) 渐近桥，再证明新谱时间在同一个 strong coherent 相域内。没有修改两份已同步主稿。

## 1. 实际 \(C^1\) 系数提取的独核与平均叶范围

固定 \(N\ge1\)，源为一个有界 \(H^{N+2}\) 复球，低 \(H^1\) 幅度先保证 \(q=-S+u\ne0\)。Riccati 方程

\[
b_\lambda=(D+\lambda)^{-1}(r+Vb_\lambda-qb_\lambda^2),
\quad \lambda\to+\infty,
\]

在 \(H^1\) 的 \(O(\lambda^{-1})\) 球内收缩。局部系数递推使 \(\beta_j\in H^{N+2-j}\)，特别 \(\beta_N\in H^2\)，故截断 differential residual 的末项 \(D\beta_N\) 在 \(H^1\) 中。残差为 \(O(\lambda^{-N})\)，resolvent 的 \(H^1\to H^1\) norm 为 \(\lambda^{-1}\)，收缩逆有统一界，给 \(O(\lambda^{-N-1})\) 误差。较大复源球上一致的解析误差通过 Cauchy 在较小球给同阶源 \(C^1\) 误差。

实际 periodic Riccati 解给 monodromy 特征线，fast 与 slow 乘子是

\[
\mu_f=e^{\lambda L+\mathcal K_\lambda},
\quad \mu_s=e^{A-\mathcal K_\lambda},
\quad \mathcal K_\lambda=\int qb_\lambda.
\]

大正 \(\lambda\) 的分离保证 normalized trace 的 arcosh 分支可在共同源球统一解析选择；故 \(\mathcal K_\lambda\) 确为实际 \(\mathcal F_\lambda,A\) 的函数。§13 的真实对合给 \(\{\mathcal K_\lambda,\mathcal F_\mu\}=0\)。

形式 factorization

\[
1-\mathscr L/\lambda
=(1+(D-W)^{-1}qb^f)(1-D/\lambda+qb^f/\lambda)
\]

也逐项成立；使用 Riccati 关系后交叉项恰消去。第二因子 log 的每个系数为微分算子，第一因子的平方及更高幂为 \(D\) 阶至多 \(-2\)，周期 Adler trace 的 BCH 交换子项为零，故该形式计算准确识别系数 \(\int q\beta_n=-C_n\)。这里只识别有限代数系数。上面的实际 \(C^1\) 余项才证明

\[
\mathcal K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(H^{N+2};\mathbb C)}(\lambda^{-N-1}).
\tag{B1}
\]

固定 \(\mu\) 时 §2 下述 \(X_{\mathcal F_\mu}\) 为同一 \(H^{N+2}\) 源切向量，将它代入 (B1) 后逐次取系数，严格得到 \(\{\mathcal F_\mu,C_n\}=0\)。并未把实际 Bloch resolvent 与形式 residue 梯度相等作为依据。

以上估计与代数步骤不使用 \(\int u=\int v=0\)。可以在 full \(H^{N+2}\) 中低幅度球上重作同一证明。固定 \(S\ne0\) 后，\(C_n=-\int q\beta_n\) 是全 source 的有限 differential polynomial，\(\mathcal F_\mu\) 及其下述 Hamilton 场为全 \(H^{N+2}\) 上局部复解析映射；因此括号 \(dC_n[X_{\mathcal F_\mu}]\) 是 connected full complex \(H^{N+2}\) 空间上的解析 scalar 函数。它在上述非空开球为零，沿复直线的解析恒等定理使其处处为零。由此实际 commutation 扩展到任意 \(M=2,c\ne0\) 周期平均叶，允许 \(q\) 出现零点。这里没有将仅在一片固定均值叶上的零恒等式跨叶延拓：使用的是本节明确补写的 full-source 同一小球证明。若 charge 规范增加均值 Casimir，也不改变括号。

固定的 actual center/gap 仍只在 §12 的实际无轮廓零点小球中定义；其均值叶和背景条件不由此扩大。

## 2. 固定参数谱场的 order-zero Banach 流

记 \(W_\mu=Y_\mu N_\mu Y_\mu^{-1}\)，则 \(W'=[L,W]\)。实际周期梯度给

\[
X_{\mathcal F_\mu}
=-\frac1{16}\bigl(
\operatorname{tr}W_\mu[K_\mu,L_\mu],
\operatorname{tr}W_\mu[H/2,L_\mu]\bigr).
\tag{B2}
\]

没有 source 空间导数出现在 (B2) 右端。固定 \(\mu\) 时，周期 ODE、Sobolev 乘法及 \(W'=[L,W]\) 使 \(W\in H^{s+1}\) 并源解析，\(s\ge1\)。所以 (B2) 是 \(H^s\to H^s\) 局部解析场。在 \(H^1\) 的有界数据球上，原 affine connection 的 Volterra 界及乘法界统一控制场及其局部 Lipschitz 常数。Banach Picard 收缩给一个统一正复时间圆盘的解析流 \(\Phi_\sigma\)，定义于稍小的数据球；若场仅在一个 open 谱坐标域定义，紧中心族由有限局部球覆盖后取得同样正时间。

对真实实场，使用 \(\Re\mathcal F_\mu\) 或 \(\Im\mathcal F_\mu\)。其 holomorphic 复化应分别写为 \((\mathcal F_\mu+\mathcal F_{\bar\mu})/2\) 与 \((\mathcal F_\mu-\mathcal F_{\bar\mu})/(2i)\)，不是在复 source 中作复共轭运算。它们保实，且 \(X\) 为周期梯度的 \(D\) 像，保持全部 source 组件均值。

monodromy trace 在空间基点平移下不变；constant \(J\) 与平移交换，所以 \(X\) 和 \(\Phi_\sigma\) 平移等变。低 \(H^1\) 流的全部数据微分有界，沿 smooth 输入的空间平移轨道反复微分，给

\[
D_x^q\Phi_\sigma(z)
=\sum_{\sum i_\nu=q}c_{\mathbf i}
D_z^k\Phi_\sigma(z)[D_x^{i_1}z,\ldots,D_x^{i_k}z].
\]

因此 smooth 数据在首次固定的同一 \(\sigma\) 时间盘内保持全部空间正则，形成 Fréchet smooth 流；不随空间阶反复缩时间盘。紧参数 smooth 族亦同窗成立。

固定一个 actual \(a_k\) 或 \(g_k\) 的梯度，由紧谱轮廓积分的 (A6) 型梯度组合得到。其 scalar 权重不依赖 \(x\)，故用 \(D\) 后仍只有 \(W'=[L,W]\) 的 order-zero 项。在固定无轮廓零点的 open 域内，它们的实、虚部有相同 Banach flow 结论，及与全部 \(C_n\) 的严格 commutation。

## 3. 真实 \(C_n\) 方程的输送不需要其 Cauchy 开集

设 \(X\) 为上一节任一谱场。常数物理 \(J\) 与真实 \(\{H,C_n\}=0\) 给 smooth 场上的

\[
[X,X_{C_n}]=0.
\]

于是对于 smooth \(z\)，

\[
D\Phi_\sigma(z)X_{C_n}(z)
=X_{C_n}(\Phi_\sigma z).
\tag{B3}
\]

证明可在一个足够高但有限的 Sobolev 层进行：两边之差随 \(\sigma\) 满足 \(X\) 的 order-zero 线性 variational 方程，初值零，Banach 唯一性使它恒零。\(X_{C_n}\) 的有限导数损失只决定使用的层；上一节保证 \(\Phi\) 的全部高层保持同一低阶时间盘。因而任一已存在的真实有限 joint 解 \(Z_N(t_0,\ldots,t_N)\) 被逐点输送为 \(\Phi_\sigma Z_N\)，仍逐坐标满足全部旧方程。这没有假定 \(C_n\) 在普通 Sobolev 开集有 Cauchy 流。

物理 \(K\) 是 \(C_1\) 与动量、规范常数的已知组合。谱 trace 和 center/gap 的空间平移不变性给与动量对合，因此 (B3) 也包括真实物理 \(K\)。

## 4. 所有旧坐标共用一个正谱时间盘

固定一个已有 strong coherent plot，限制到紧参数盒 \(K\)。其各有限 joint 解 \(Z_N\) 相容；强 presentation 提供以后不变的逐坐标复内域。先选紧物理根复小窗，始终严格位于共同内域中。取包含中心族的一个 \(H^1\) 有界球；若新谱场只在 open 域 \(O\) 中定义，先取中心紧像的有限球覆盖，使一个统一正 \(H^1\) 管状 margin 留在 \(O\) 中。

归纳选每个新增坐标的紧复小窗 \(D_j\)，一旦选定便冻结。在旧 compact box \(K\times D_0\times\cdots\times D_{j-1}\) 上，已有真实 \(Z_j\) 在新时间零截面恰为 \(Z_{j-1}\)。其内部时间连续性及 compactness 允许取正 \(D_j\) 使

\[
\sup\|Z_j(a,t_0,\ldots,t_j)-Z_{j-1}(a,t_0,\ldots,t_{j-1})\|_{H^1}
<\rho 2^{-j-3}.
\tag{B4}
\]

偶坐标在旋转菱形内选择；强条件保证新增更长前缀仍包含已冻结的旧 complex boxes。(B4) 的 telescoping sum 将**全部**有限前缀的物理图像置于同一个 \(H^1\) 有界球或上述 fixed open 管内。它不是只对每个前缀给一个可能趋零的谱时间。

§2 的低阶 Banach 流因此对所有这些图像给同一个正 \(T_H\)。于是

\[
\widetilde Z_N(a,\sigma,t)=\Phi_\sigma(Z_N(a,t)),
\quad |\sigma|<T_H,
\tag{B5}
\]

有共同正谱时间盘，并形成全部前缀相容的实际 joint 解；旧轴窗口都已冻结。各固定有限前缀在所有空间层及 compact 参数上 smooth，complex 时间 holomorphic。

## 5. 返回同一 strong 相域与其内部 Hamilton 速度

(B5) 的物理中心必须再识别为 §16 的 strong plots，不能仅以在 ambient \(E\) 中取值为据。将谱时间限制到一个 compact 内子盘，对 \(a,\sigma\) 作有限维参数。逐坐标重新混合参数化：先围绕该参数族选择一个共同物理小 mixed 窗，继而每个新 \(C_n\) 轴选一次更小正窗，旧轴不再变。

每步的实际端点角点数据为 Fréchet 紧参数族；mixed 收缩可在包住它的有限 Banach 源球上统一成立。新增轴可更小，以使旧角点轨道留在已冻结的源域。已有实际 joint 方程及逐层 mixed 唯一性精确识别新中心与原 (B5)，如主稿 \(16.3\)。原 (B5) 已有所有坐标的共同复内域，故新虚角点可在任意较长前缀中使用。整个过程不缩 \(\sigma\) 参数盒，只逐次缩新旧层级轴。因此 (B5) 的中心是同一 \(\mathfrak S_\infty\) 的 strong plot。

对点态使用常数旧 plot，得到 \(\Phi_\sigma z\in\mathfrak S_\infty\)；对任意旧 plot，得到统一小谱时间上的 plotwise smooth 映射。反向谱时间给局部逆。谱速度因而是该相域真正内部 tangent；物理 Hamilton 身份沿每个 plot 拉回，结合已证 internal weak nondegeneracy，给唯一内部 Hamilton 场。

所有固定参数 trace、实际固定 center/gap 的实、虚部，与全部逐层 \(C_n\) 时间 germs 以及彼此对易。在此仅断言有限组选定谱场及有限支持旧时间坐标上的局部共同 germs；没有定义无限多个非零谱/层级时间同时取值的流。

## 6. Translation 成分和尚未获得的 Liouville 结论


\(A=-P_{\rm mom}/(8S)\) 的速度为 \((u_x,v_x)/(8S)\)，在 \(H^s\) 上有一阶损失，不能并入 order-zero Picard 结论。真实空间平移在 smooth 相域有已知群，并因 source 平移等变而保持全部 strong presentations。它无需被当作任意 smooth 场上的复空间平移。

例如 \(a_k-A/L\) 的真实时间是 order-zero \(a_k\) 时间与已知实空间平移的交换复合。原未归一化 trace 同样含 translation 成分；其 scalar 系数由相互对合的 \(A,\mathcal F_\lambda\) 组成，沿自身时间保持常数，可按固定谱流与实平移组合处理。这里不把这些组合宣称为 \(H^s\to H^s\) 向量场。

新的接合证明只给合法 strong 相域内的实际谱 Hamilton 运动及对合。charge 水平集取 inherited diffeology；其内部切映射单射、核等式和正规积分叶结构仍未证明，更不自动弱辛。完整 norming/divisor 逆、全频 nonlinear 括号闭包、最大各向同性和合法角变量仍是独立后续问题。
