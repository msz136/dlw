# 全 M 实际 full-framed monodromy 的端点与 slow holonomy：独立审查

2026-10-11。本次只作手算推导，不运行旧或新增 machine checks。审查对象是原 balanced 物理状态经真实 periodic gauge 后的 constant-slow 系统。证明以实际周期 Riccati 解、实际 ODE、实际谱投影和实际正参数极限进行；没有用 formal resolvent 系数替代这些对象。

## 1. 精确定理与所用低阶空间

设 m=M−1≥1，周期 L>0，

\[
\mathcal A_\lambda(x)=
\begin{pmatrix}\lambda&a(x)\\b(x)&H\end{pmatrix},
\qquad a\in L^2(S^1;\mathbb C^{1\times m}),\quad
b\in L^2(S^1;\mathbb C^{m\times1}),\quad H\in\operatorname{Mat}_m(\mathbb C).
\tag{C1}
\]

令 T_𝒜(λ) 为 Y′=𝒜_λY、Y(0)=I 的实际 monodromy。固定任意有界 L²×L²×Mat_m coefficient ball。存在依赖该球的 Λ，使每个实 λ≥Λ 有唯一 simple fast multiplier μ_f，位于以 e^{λL} 为中心、半径 e^{λL}/2 的圆内；其实际 spectral projector Π_𝒜 满足

\[
\Pi_{\mathcal A}(\lambda)\longrightarrow E_{11},
\qquad
\bigl[(I-\Pi_{\mathcal A})T_{\mathcal A}\bigr]_{22}
\longrightarrow e^{LH}.
\tag{C2}
\]

第一极限的 matrix norm 误差 O(λ⁻¹ᐟ²)，第二极限 O(λ⁻¹)，均在该 ball 上一致。下标 22 表示 m×m slow block，不是一个单独元素。这两个结论不需要 holonomy NR；NR 只用于从 e^{LH} 恢复指定局部分支的 H。

在原物理 balanced source q∈L²、d_first∈H¹、S≠0 上，state-adapted splitting T_z 和 periodic gauge G 都在 H¹，点值 d(0)、G(0) 有准确意义。原 full-framed χ monodromy 的 fast projector 极限恢复 d(0)；随后实际正参数 slow 极限恢复 framed H^fr。这个 lemma 保留 full matrix frame，不能由 characteristic class data 独自代入。

## 2. 真正的周期 Riccati 解：L² 到 L∞ 的预算

对 λ>0，周期 R_λ=(D+λ)⁻¹ 的实际 convolution kernel 给

\[
(R_\lambda f)(x)=\frac1{1-e^{-\lambda L}}
\int_0^Le^{-\lambda t}f(x-t)\,dt.
\]

因此

\[
\|R_\lambda\|_{L^2\to L^2}\le\lambda^{-1},\quad
\|R_\lambda\|_{L^\infty\to L^\infty}\le\lambda^{-1},\quad
\|R_\lambda\|_{L^2\to L^\infty}
\le\left\{\frac{\coth(\lambda L/2)}{2\lambda}\right\}^{1/2}.
\tag{C3}
\]

取真正的 fixed-point 方程

\[
\beta=R_\lambda\{b+H\beta-\beta(a\beta)\}.
\tag{C4}
\]

β 是 m-column，aβ 为 scalar。该映射在 L∞ ball ||β||∞≤Cλ⁻¹ᐟ² 上闭合，contraction 常数可估为

\[
\|H\|/\lambda+
C\lambda^{-1/2}\|a\|_2(\|\beta\|_\infty+\|\gamma\|_\infty)
=O(\lambda^{-1}).
\]

这里 Hβ 项使用 R_λ:L∞→L∞，β(aβ) 使用 L²→L∞。选择统一 Λ 后得到唯一小实际周期解，并对固定 λ 源复解析。由 (C4) 的右端属于 L²，β∈H¹，有连续周期代表。再用 L² resolvent bound，

\[
\|\beta\|_2\le\lambda^{-1}
\{\|b\|_2+\|H\|\|\beta\|_2
+\|a\|_2\|\beta\|_\infty^2\},
\]

得一致的

\[
\boxed{\|\beta\|_\infty=O(\lambda^{-1/2}),\qquad
\|\beta\|_2=O(\lambda^{-1}).}
\tag{C5}
\]

由 differential 方程 β′=b+Hβ−λβ−β(aβ) 还得 ||β′||₂=O(1)。因此 endpoint β₀=β(0) 有意义并满足 ||β₀||=O(λ⁻¹ᐟ²)。没有对原 L² b 取 b(0)，也没有使用 β₀≈b(0)/λ 的无定义式。

## 3. Actual triangularization 与 slow monodromy 极限

实际 H¹ periodic gauge

\[
T_\beta=\begin{pmatrix}1&0\\\beta&I_m\end{pmatrix}
\]

给几乎处处精确等式

\[
T_\beta^{-1}\mathcal A_\lambda T_\beta-T_\beta^{-1}T_\beta'
=\begin{pmatrix}\lambda+a\beta&a\\0&H-\beta a\end{pmatrix}.
\tag{C6}
\]

下左 block 为零正是 (C4) 的 differential equation。设 Z_s′=(H−βa)Z_s、Z_s(0)=I，N_s=Z_s(L)。Cauchy–Schwarz 与 (C5) 给

\[
\|\beta a\|_{L^1},\ \|a\beta\|_{L^1}=O(\lambda^{-1}).
\tag{C7}
\]

故 Z_s 及其 inverse 在 [0,L] 上一致有界。实际 Duhamel 公式为

\[
N_s=e^{LH}-\int_0^Le^{(L-t)H}\beta(t)a(t)Z_s(t)\,dt,
\]

所以

\[
\boxed{N_s=e^{LH}+O(\lambda^{-1}).}
\tag{C8}
\]

这适用于 complex H，不要求它 normal，也不要求 slow eigenvalues 彼此简单。Fast scalar solution 是

\[
f(x)=\exp\{\lambda x+\kappa(x)\},\qquad
\kappa(x)=\int_0^xa(t)\beta(t)dt,
\qquad \|\kappa\|_\infty=O(\lambda^{-1}).
\]

其乘子 μ_f=f(L)=exp{λL+O(λ⁻¹)}。三角系统的实际 monodromy 为

\[
U_\lambda=\begin{pmatrix}\mu_f&B_\lambda\\0&N_s\end{pmatrix},
\qquad B_\lambda=\mu_f J_\lambda,
\]

\[
J_\lambda=\int_0^L e^{-\lambda t-\kappa(t)}a(t)Z_s(t)dt.
\tag{C9}
\]

Ns 的谱在一个固定圆内，μ_f 则指数增长，所以 μ_f 是 simple actual characteristic root，且全 coefficient ball 上可统一选择其圆盘。该选择与实际 ODE/Floquet root 相符，不是 formal high-frequency root。

## 4. Fast spectral projector 的边界项和精确 slow block

由 actual weighted integral (C9)，

\[
\|J_\lambda\|\le C\int_0^Le^{-\lambda t}|a(t)|dt
\le C\|a\|_2(2\lambda)^{-1/2}.
\tag{C10}
\]

定义 row

\[
c_\lambda=B_\lambda(\mu_f I_m-N_s)^{-1}
=J_\lambda(I_m-\mu_f^{-1}N_s)^{-1}.
\tag{C11}
\]

右侧 resolvent 的 norm 一致有界，故 c=O(λ⁻¹ᐟ²)。这里 (C11) 只涉及实际有限矩阵，乘法顺序不能改成将 inverse 放在 B 左侧。

U 的 fast projector 准确为

\[
\Pi_U=\begin{pmatrix}1&c\\0&0\end{pmatrix}.
\tag{C12}
\]

确证：Π_U²=Π_U，UΠ_U=μ_fΠ_U，Π_UU=μ_fΠ_U 的右上式是 B+cN_s=μ_fc，即 (C11)。由 simple fast root，它就是实际 Riesz spectral projector。

令 β₀=β(0)，因 T_β 周期，T_𝒜=T_β(0)U T_β(0)⁻¹。于是

\[
\boxed{\Pi_{\mathcal A}=
\begin{pmatrix}
1-c\beta_0&c\\
\beta_0(1-c\beta_0)&\beta_0c
\end{pmatrix}.}
\tag{C13}
\]

由 (C5)、(C10) 它确实趋于 E₁₁，offdiagonal errors 为 O(λ⁻¹ᐟ²)，diagonal errors 为 O(λ⁻¹)。进一步，

\[
(I-\Pi_U)U=\begin{pmatrix}0&-cN_s\\0&N_s\end{pmatrix},
\]

所以原 constant-slow frame 中移除 fast branch 后的完整矩阵为

\[
\boxed{R_{\mathcal A}:=(I-\Pi_{\mathcal A})T_{\mathcal A}
=\begin{pmatrix}
cN_s\beta_0&-cN_s\\
(\beta_0c-I_m)N_s\beta_0&(I_m-\beta_0c)N_s
\end{pmatrix}.}
\tag{C14}
\]

尤其右下块是 (I−β₀c)Ns，**不能直接写成 Ns**。因为 β₀c=O(λ⁻¹)，(C8) 给

\[
(R_{\mathcal A})_{22}=e^{LH}+O(\lambda^{-1}),\qquad
R_{\mathcal A}\to\operatorname{diag}(0,e^{LH}).
\tag{C15}
\]

完整 matrix 极限的误差只保证 O(λ⁻¹ᐟ²)，与右下块的更好误差相区别。

## 5. 原 χ frame：直接恢复 d(0) 及 framed monodromy

取原 balanced 物理状态 q∈L²、d_first∈H¹，S≠0，并采用已有 NR 周期 holonomy 规范。原准确 periodic frame 为

\[
\mathcal E(x)=T_z(x)\operatorname{diag}(1,G(x)),
\qquad T_z=[d/S,Z],\quad
T_z^{-1}=[1^T;E-(d_{\rm first}/S)1^T].
\tag{C16}
\]

这些矩阵均为 H¹，点点可逆；q,r,V∈L² 的实际 ODE gauge 等式在几乎处处和 integral-equation 意义成立。基点 full monodromy 满足

\[
T_\chi(\lambda)=\mathcal E(0)T_{\mathcal A}(\lambda)\mathcal E(0)^{-1}.
\tag{C17}
\]

Actual fast projector 按相同相似变换转换。因为 diag(1,G(0)) 与 E₁₁ 交换，由 (C13) 得

\[
\boxed{\lim_{\lambda\to+\infty}\Pi_\chi(\lambda)
=T_z(0)E_{11}T_z(0)^{-1}
=d(0)1^T/S.}
\tag{C18}
\]

Known full-framed Tχ 在每个大正 λ 的实际 simple fast root 与 finite spectral projector 已决定左侧，故可恢复 d(0)：对任意标准 χ basis vector e_j，d(0)=S(Πχ)_∞e_j。这里 S、格点标签与 χ basis 已知；若只知道 monodromy 共轭类，则这个 matrix limit 不能直接赋值。H¹ d 的连续代表保障 endpoint 的含义；不需要任何单独 d_j≠0，也未取 q(0)。

因此已知 d(0) 后得到完整 T_z(0)。从数据计算

\[
T^{\rm fr}(\lambda)=T_z(0)^{-1}T_\chi(\lambda)T_z(0)
=\operatorname{diag}(1,G_0)T_{\mathcal A}(\lambda)
\operatorname{diag}(1,G_0)^{-1},\quad G_0=G(0).
\tag{C19}
\]

它准确是 based gauge G^fr=G G₀⁻¹、G^fr(0)=G^fr(L)=I 的 actual full monodromy。相应系数为 a^fr=aG₀⁻¹、b^fr=G₀b、H^fr=G₀HG₀⁻¹。即使 G₀尚未单独恢复，(C19) 左侧已经从实际数据可计算；无需猜测 mean-normalized gauge 的基点值。

## 6. NR exponential local inverse 恢复 framed H

T^fr 的 fast projector 同样由实际矩阵决定，记为 Π^fr。由 (C15)、(C19)，

\[
\boxed{\lim_{\lambda\to+\infty}
\bigl[(I-\Pi^{\rm fr}(\lambda))T^{\rm fr}(\lambda)\bigr]_{22}
=G_0e^{LH}G_0^{-1}=e^{LH^{\rm fr}}.}
\tag{C20}
\]

在 uniform 参考 H₀=V₀，其 eigenvalues ζ_ℓ=−iδcot(πℓ/M) 简单。指数映射的实际有限矩阵导数为

\[
e^{-LH_0}D(e^{LH})[H_0](h)
=\int_0^Le^{-x\operatorname{ad}H_0}h\,dx.
\tag{C21}
\]

在 eigenbasis 的 (ℓ,j) component，该 operator 的乘数为 L（ζ_ℓ=ζ_j）或 (1−e^{-L(ζ_ℓ−ζ_j)})/(ζ_ℓ−ζ_j)。故它可逆当且仅当所有差 ζ_ℓ−ζ_j 不属于 ik₀ℤ\{0}，恰是 NR。真实 finite-dimensional analytic IFT 给 e^{LH} 在指定 H₀ 邻域的唯一局部 inverse。因此 (C20) 准确恢复 H^fr，可能需要背景指定的 matrix-log branch；不能在较大 δ 任取 principal logarithm 后声称等于 H^fr。

任意外给 static B 时 raw slow H_B=H+B I_m，raw fast diagonal是 λ_original，所有上述 actual positive-parameter 证明逐字适用。恢复的矩阵为 H_B^fr=H^fr+B I_m，known B 再给 centered H^fr；差谱 NR 不变。若使用 scalar-normalized monodromy，不能把未缩放 slow block的消失极限误当作 e^{LH}；§8 给无需预先恢复 scalar factor 的准确 scaled limit。

## 7. 审查判断与边界

Endpoint/holonomy lemma 通过。关键 signs 与 order 为：slow connection H−βa；row c=B(μI−Ns)⁻¹；原 frame projector (C13)；fast-removed slow block (I−β₀c)Ns；based constant holonomy H^fr=G₀HG₀⁻¹。所有 rate 由真实 L² convolution、Cauchy–Schwarz 和 ODE Duhamel 给出，在 bounded coefficient balls 上统一，未使用 formal residue substitute。

由原 actual full-framed positive-λ monodromy 已恢复 d(0)、T_z(0)、based full monodromy T^fr(λ) 及 H^fr。该 lemma 尚未从 full spectral/norming data 恢复全 x 上的 a,b 函数，未提供 all-M weighted nonlinear norming inverse，也未证明 class-gradient 闭包或 Liouville 最大性。

## 8. 已保存主稿式 (1)–(16) 的 normalized 增强：PASS

另已逐式读取 `all_m_actual_framed_endpoint_recovery_20261011.md` 的保存稿。其 (2)–(11) 与本审查 (C3)–(C15) 完全匹配；主稿使用 η 表示本稿的 β。下面补证其 actual matrix ratio、normalized slow limit 与全 H 恢复。

由 (C14)，R_𝒜 在 λ≥Λ 时一致有界，且 T_𝒜=μ_fΠ_𝒜+R_𝒜、trT_𝒜=μ_f+trN_s。μ_f 的绝对值指数增大，trN_s 一致有界，故 trT_𝒜不为零，并准确有

\[
\frac{T_{\mathcal A}}{\operatorname{tr}T_{\mathcal A}}
=\frac{\mu_f}{\mu_f+\operatorname{tr}N_s}\Pi_{\mathcal A}
+\frac{R_{\mathcal A}}{\mu_f+\operatorname{tr}N_s}
=E_{11}+O(\lambda^{-1/2}).
\tag{C22}
\]

连接 (C1) 的 trace 恒为 λ+trH。因此 normalized det-one monodromy 是

\[
N_{\mathcal A}=e^{-\lambda L/M-\tau}T_{\mathcal A},\qquad
\tau=\frac LM\operatorname{tr}H,\quad M=m+1.
\tag{C23}
\]

Scalar normalization 不改变 fast projector，也精确取消于 N/trN。因此 (C22) 同时适用于 N_𝒜。另一方面，(C15) 给实际一致 scaled limit

\[
\boxed{\lim_{\lambda\to+\infty}e^{\lambda L/M}
[(I-\Pi_{\mathcal A})N_{\mathcal A}]_{22}
=e^{-\tau}e^{LH}=e^{LK},\qquad
K=H-\frac{\operatorname{tr}H}{M}I_m.}
\tag{C24}
\]

其有限 λ 误差为 O(λ⁻¹)，因为 e^{−τ} 在固定 bounded H ball 上有界。关键是 scalar-fast 维数为一，即 slow block 是 m=M−1 阶，因此

\[
\operatorname{tr}K=\operatorname{tr}H/M,\qquad
\boxed{H=K+\operatorname{tr}K\,I_m.}
\tag{C25}
\]

这确实恢复全部 central holonomy，不丢 trace。K 的差谱与 H 相同，NR 保证 K↦e^{LK} 的实际 finite-matrix derivative 可逆，证明与 (C21) 相同。故先从 actual (C24) 取背景指定的局部 exponential inverse，再用 (C25)，即可从 normalized full monodromy 恢复 H，**无需先独立知道 τ**。

原 physical frame 中 Nχ=𝓔(0)N_𝒜𝓔(0)⁻¹，(C22) 给

\[
\boxed{\lim_{\lambda\to+\infty}
N_\chi/\operatorname{tr}N_\chi=d(0)1^T/S.}
\tag{C26}
\]

因此可直接从原 fixed-frame normalized matrix ratio 恢复 d(0)、T_z(0)，甚至不必先显式计算 fast root 或 projector。随后

\[
N^{\rm fr}(\lambda)=T_z(0)^{-1}N_\chi(\lambda)T_z(0)
=N_{\mathcal A^{\rm fr}}(\lambda)
\tag{C27}
\]

为 G^fr(0)=I 的 actual full normalized monodromy；对它按 (C24)–(C25) 恢复 H^fr。Finite datum N^fr(0) 的右下 block 也是准确 actual matrix datum，但有限参数下它一般不是 e^{LH^fr}；主稿只把它保留为另一个 norming datum，没有犯这一误认。

任意外给 B 在 centered 参数上与上述 normalized 恢复相容；若保留 raw 参数，则 (C24) 恢复 raw K_B，(C25) 给 H_B，最后减去 known BI_m。局部 log branch 与 NR 差谱仍按实际 uniform 背景指定。

对保存主稿的数学判断为 PASS。唯一发现的是式 (7) integrand 中指数项后的逗号可改为乘法空白，以免排版歧义；不影响证明。主稿的 full-data 限定、L² endpoint 预算、periodic gauge、slow block 顺序及 normalized trace 恢复均成立。没有新增 machine check，也没有推进 class-only Liouville 最大性。
