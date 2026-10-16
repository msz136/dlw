# M=2 移动双根与 holonomy 极限：独立 Sobolev 审查

2026-10-11。审查范围为 small-δ、B=0、固定 free 分量均值叶上的实际 monodromy 不变量。以下给出 uniform Sobolev analyticity、双根计数及高频极限；不证明逆谱、作用角坐标、Poisson 对应或 Liouville 完备性。本次未重新运行旧证书。

结论：所提 lemma 成立，须把 g 明确定义为 half-gap squared，并在统一圆盘选择中包括背景 λ=±2δ 的简单零点。轮廓矩可以改写为边界 log 公式，直接获得 uniform ℓ∞ 解析性及二阶估计。高频极限还给出严格的 H^s→c₀×c₀ holonomy-renormalized 不变量映射；无需声称在源球上一致的 Riemann–Lebesgue 衰减。

## 1. 真正 Sobolev 输入与 L¹ ODE

令 k₀=2π/L，0<δ<k₀/2，S=2δ。源空间为

\[
X_s=\{(u,v)\in H^s_{\rm per}(\mathbb C)^2:
\int u=\int v=0\},\qquad s\ge1.
\]

实物理场为其实型子空间。取

\[
q=-S+u,\quad d_0=\delta+v,\quad d_1=\delta-v,
\]

\[
V=-2uv/S,\qquad
r=\frac{(\delta^2-v^2)(1+u/S)-v_x}{S}.\tag{B1}
\]

原物理闭合给 b₁=−d₀u/S、b₀=b₁+u；所以这是同一源 Poisson 均值叶内的实际场。H^s⊂L∞、v_x∈L²⊂L¹，故 (q,r,V)∈(L¹)^3，且 (B1) 给出 X_s→(L¹)^3 的复解析多项式映射，其各阶导数在有界源球上一致有界。此处不需要 q 无零点，因为直接使用 split 系统，不消去 ξ。

定义

\[
Y_x=A_\lambda Y,\quad Y(0)=I,
\qquad
A_\lambda=\begin{pmatrix}\lambda&q\\r&V\end{pmatrix},
\quad T(\lambda,z)=Y(L).
\]

这是具有 L¹ 系数的实际初值问题。对 |Re λ|≤R_λ，先去掉 diag(λ,0)，再应用 Volterra/Picard 展开。其 n 阶项以 C^n/n! 控制，C 只依赖 R_λ、L 和源球的 L¹ 界，与 Im λ 无关。由此 T、其源 Fréchet 导数和二阶余项在该竖条上一致有界；λ 导数也一致有界。参数依赖是复解析的。这避免了固定 companion 本征基的高频条件数。

## 2. 行列式归一化及背景零点

Liouville 公式在 L¹ 系数下仍给出

\[
\det T=\exp\{\lambda L+a(z)\},\qquad
a(z)=\int_0^L V(x)\,dx.
\]

于是

\[
N=e^{-(\lambda L+a)/2}T\in SL_2(\mathbb C),\qquad
D=(\operatorname{tr}N)^2-4.\tag{B2}
\]

D 也是 (tr T)²/det T−4，其零点等价于实际两个 Floquet 乘子重合。它对周期 gauge 的 monodromy 共轭不变，不依赖 companion frame。

背景 z=0 时，q₀=−S、r₀=δ²/S、V₀=0，故

\[
D_0(\lambda)=4\sinh^2\left(\frac L2
\sqrt{\lambda^2-4\delta^2}\right).\tag{B3}
\]

右边关于 λ 是整函数，不需要选择全局平方根。令

\[
k_n=nk_0,\quad\omega_n=\sqrt{k_n^2-4\delta^2},\quad
\lambda_n=i\omega_n,\qquad n\ge1.
\]

每个 λ_n 是恰好二重零点。背景另有 −λ_n 二重零点及 λ=±2δ 简单零点。δ<k₀/2 确保 λ₁≠0，排除了两侧双根在零点合并的情形。

可以取

\[
0<\rho<\min(k_0/4,\omega_1/2).\tag{B4}
\]

此时每个圆盘 |λ−λ_n|<ρ 只含其中心的背景双根。正侧相邻频率间距大于 k₀；反侧最近距离至少 2ω₁；λ_n 到 ±2δ 的距离恰为 k_n。

固定 |η|=ρ 时，(B3) 有一致极限

\[
D_0(\lambda_n+\eta)\longrightarrow
4\sinh^2(L\eta/2),\qquad n\to\infty.
\]

极限在该圆周无零点；有限首段各圆周也无零点。因此存在 γ>0，使所有 n、|η|=ρ 上 |D₀(λ_n+η)|≥γ。

## 3. 固定均值使全部一阶判别式变化为零

任取 h=(h_u,h_v)∈X_s，在背景

\[
\delta q=h_u,\quad
\delta r=\delta^2h_u/S^2-(h_v)_x/S,\quad
\delta V=0.
\]

故 ∫δA=0。背景 A₀ 是常矩阵，第一 Born 变分满足

\[
\delta\operatorname{tr}T_0
=\int_0^L\operatorname{tr}
\left(e^{A_0(L-x)}\delta A(x)e^{A_0x}\right)dx
=\operatorname{tr}\left(e^{A_0L}\int_0^L\delta A\,dx\right)=0.
\]

同时 δa=0。因此

\[
D_z(\lambda,0)=0\quad\text{对全部 }\lambda.\tag{B5}
\]

这里使用的是 cyclic trace 和背景常系数；不要求 δA 与 A₀ 对易。统一二阶 ODE 估计遂给出

\[
\sup_{n,\ |\eta|=\rho}
|D(\lambda_n+\eta,z)-D_0(\lambda_n+\eta)|
\le C\|z\|_{H^s}^2.
\]

缩小一个与 n 无关的复源球，使右边小于 γ/2。Rouché 定理则在每个圆盘内恰给两个零点，按重数计，不要求两个零点已分裂。

## 4. 无 λ_n 幂增长的实际 center 与 half-gap squared

若两个零点为 λ_n+η_{n,1}、λ_n+η_{n,2}，定义

\[
\widetilde c_n=\frac{\eta_{n,1}+\eta_{n,2}}2,
\qquad
g_n=\frac{(\eta_{n,1}-\eta_{n,2})^2}{4}.\tag{B6}
\]

因此 c_n=λ_n+\widetilde c_n 是 actual center，g_n 是 half-gap squared；完整 gap squared 为 4g_n。两个有序根本身不必解析，但其对称组合解析。

轮廓矩公式为

\[
\widetilde c_n=\frac12\frac1{2\pi i}
\oint_{|\eta|=\rho}\eta\frac{D'}D\,d\eta,
\]

\[
g_n=\frac12\frac1{2\pi i}
\oint_{|\eta|=\rho}\eta^2\frac{D'}D\,d\eta
-\widetilde c_n^2.\tag{B7}
\]

更直接的解析估计来自

\[
R_n(\eta,z)=\frac{D(\lambda_n+\eta,z)}{D_0(\lambda_n+\eta)}.
\]

圆周上 R_n 一致接近 1，所以 log R_n 可统一取其近 1 的解析分支。轮廓分部积分给出精确公式

\[
\widetilde c_n=-\frac12\frac1{2\pi i}
\oint\log R_n\,d\eta,
\]

\[
g_n=-\frac1{2\pi i}\oint\eta\log R_n\,d\eta
-\widetilde c_n^2.\tag{B8}
\]

这里背景 shifted moments 全为零。这些公式避免使用 λ_n 的大幂，也不需要额外证明 D′ 的高频尾估计。

uniform Volterra/Cauchy 界及 log 的一致收敛级数，使

\[
z\longmapsto(\widetilde c,g):X_s\supset B_\epsilon\to
\ell^\infty\times\ell^\infty
\]

成为真正的 Banach 空间复解析映射。逐坐标解析性之外，统一 Cauchy 估计保证源 Taylor 级数在目标 sup norm 中收敛。由 (B5)、(B8)，在更小源球上

\[
\|(\widetilde c,g)\|_{\ell^\infty}
\le C\|z\|_{H^s}^2,\qquad
\|D_z(\widetilde c,g)\|\le C\|z\|_{H^s}.
\tag{B9}
\]

各点的二阶 Fréchet 余项也以 C||h||² 一致控制。

## 5. 高频 holonomy 极限的 L¹ Dyson/RL 证明

固定一个上述源 z，不要求它光滑。令 F(x)=∫₀ˣV、a=F(L)，写

\[
Y(x)=G_\lambda(x)U(x),\qquad
G_\lambda=\operatorname{diag}(e^{\lambda x},e^{F(x)}).
\]

则 U_x=B_λU，其中

\[
B_\lambda(x)=\begin{pmatrix}
0&q(x)e^{F(x)-\lambda x}\\
r(x)e^{-F(x)+\lambda x}&0
\end{pmatrix}.
\]

对 λ=λ_n+η，|η|≤R 固定，Dyson 系列每个非零 n 阶 transition term 是有序 simplex 上的 L¹ 多重积分。其 λ_n=iω_n 相位是

\[
\exp\left(i\omega_n\sum_{j=1}^{n}\sigma_jx_j\right),
\qquad \sigma_j\in\{1,-1\},
\]

符号随 transition 交替；n≥1 时该线性相位不恒定。将 L¹ 振幅以零延拓到 ℝⁿ，多维 Riemann–Lebesgue 引理使每个固定 transition term 趋于零。

对 η 的统一性也成立：η 在紧集上使这些振幅形成 L¹ 紧集，取有限网后使用逐振幅 RL 引理即可。全部项有共同的 C_R^n/n! 绝对界，因此可交换极限与 Dyson 和，得到 U(L)→I，uniform in η compact。

ω_n−k_n→0、e^{ik_nL}=1，因此

\[
T(\lambda_n+\eta,z)\longrightarrow
\operatorname{diag}(e^{\eta L},e^a),
\tag{B10}
\]

并有

\[
D(\lambda_n+\eta,z)\longrightarrow
4\sinh^2\left(\frac{L\eta-a}{2}\right).
\tag{B11}
\]

N 本身的归一化含 e^{−λ_nL/2} 的交替符号；(B11) 使用平方消除了该符号，不应把 N 本身误写成单一有极限的矩阵。

再缩源球使 |a/L|<ρ/2。由 (B4)，(B11) 的极限函数在圆盘内只有 η=a/L 的双根，并在圆周无零点。uniform compact 收敛也保证 λ 导数在该圆周收敛；于是轮廓矩给出

\[
\widetilde c_n(z)\longrightarrow a(z)/L,
\qquad g_n(z)\longrightarrow0.\tag{B12}
\]

本证明只声称每个固定源的高频极限，不声称在整个有界 H^s 源球上一致 RL 衰减。

## 6. 可强化为 c₀ 的实际 holonomy-renormalized 映射

(B12) 表明对每个源，

\[
\left(\widetilde c_n-a/L,\ g_n\right)\in c_0\times c_0.
\]

这个映射已经在 ℓ∞×ℓ∞ 中复解析，而 c₀×c₀ 是闭子空间、具有相同范数。源差商、Fréchet 导数与 Taylor 极限均留在该闭子空间，因此它实际是

\[
\boxed{\quad
X_s\supset B_\epsilon\longrightarrow c_0\times c_0
\quad\text{的复解析映射。}\quad}\tag{B13}
\]

a(z) 是二次多项式泛函，所以 (B9) 的二阶与导数估计仍成立。这个结论无需增加 uniform-source RL 假设；闭子空间论证即足够。但它不含任何指定的加权衰减率，不能升级为 ℓ²、Sobolev 序列或指数序列估计。

## 7. 结论范围

已获得的是实际 Sobolev 源上的、全频统一的、共轭不变的 center/half-gap extraction，及明确可减去的 holonomy 极限。它对原始 monodromy 仍成立，因为周期 gauge 只作基点共轭。

这些不变量在均匀背景的一阶导数全为零，且没有 norming 信息；它们不能作为完整场坐标。若称作 Lyapunov–Schmidt chart，还需要另行指定核/余核、证明所消元方程与实际 monodromy 双根等价，并控制相关分支或 Cartesian norming 数据。本 lemma 本身尚未完成这些工作，也没有给出 nonlinear inverse、Poisson/action-angle 对应或原场 maximality。

补充验证：独立 SymPy 检查 half-gap moment 恒等式与归一化 discriminant 的代数形式，均通过，退出码 0。核心全频结论来自上面的 uniform L¹ ODE、Rouché、轮廓 log 与 RL 证明，而非有限数值抽样。
