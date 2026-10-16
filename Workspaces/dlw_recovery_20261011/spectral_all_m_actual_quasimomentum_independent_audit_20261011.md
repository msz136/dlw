# 全 M actual fast Floquet、vector Riccati 与原 C_n 系数桥独立审稿

2026-10-11。实际读取 [谱稿新 §17.1–3，式 (115)–(127)](../../刘维尔可积性/research/spectral_independent_review_20261011.md)、其 §16 的实际 gradient/flow 与 trace normalization、原 [GENERAL_PERIOD_MATRIX_LAX.md §§1–3](../dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md)。以下是重新计算的全维证明，不从有限 M 脚本外推。没有执行或重复任何旧脚本。

## 1. 精确原谱问题与系数正则性

固定任意有限 M≥2，m=M−1，S=hMc/8≠0。在 centered B=0 截面，原转移差变量 χ 的 periodic splitting 是 T=[d/S,Z]、T⁻¹=[1ᵀ;K]，K=E−d_first1ᵀ/S。1ᵀd=S 使 T 与 T⁻¹ 互逆，detT 是非零常数；不要求任一单独 d_j 非零。共同 U 的物理重建只含固定 S 的除法，因此源 free fields 的有界 H^{N+2} 球上有

\[
q,V\in H^{N+2},\qquad r\in H^{N+1},
\qquad q\text{ row},\ r\text{ column},\ V\text{ square}.
\]

只有 r=K(Cd−d_x)/S 的 d_x 消耗一阶；这里 C 是原 zero-order χ coefficient。矩阵系统与原 scalar operator 精确为

\[
\partial_x\binom{\phi}{\xi}=
\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}\binom{\phi}{\xi},
\qquad\mathscr L=D-q(DI_m-V)^{-1}r,
\qquad C_n=\frac1n\operatorname{Tr}\mathscr L^n.
\]

首变量 φ=1ᵀχ 是原差变量之和，而 λ 是原 period-product 经同一 Möbius 变换得到的参数；没有另选 scalar L 或其 normalization。上式 inverse 是 formal PDO；下节 actual periodic b 不要求这一 matrix differential operator 有 actual bounded inverse。

## 2. Vector Riccati 的实际解及每个有限阶 C¹ 余项

取足够大正实 λ。周期 Fourier multiplier R_λ=(D+λI_m)⁻¹ 满足 ||R_λ||_{H¹→H¹}≤λ⁻¹。H¹ 为一维乘法代数，故

\[
b=R_\lambda\{r+Vb-b(qb)\}
\]

在 ||b||_{H¹}≤A/λ 内将球映入自己，且其 b-导数 norm≤C/λ。所有常数对一个选定有界 complex H^{N+2} 源球一致，只可依赖该球、M、S、N。于是唯一 small periodic actual b_λ 存在、源复解析，||b_λ||_{H¹}=O(λ⁻¹)。矩阵有限维常数不会改变这个证明，任意场幅度只改变所需 Λ。

重算系数递推：β₁=r，

\[
\beta_{j+1}=V\beta_j-D\beta_j
-\sum_{a+b=j}\beta_a(q\beta_b).
\]

按源预算 β_j∈H^{N+2−j}，1≤j≤N+1；尤其 β_N∈H²、β_{N+1}∈H¹。令 b_N=Σ_{j=1}^Nβ_jλ⁻ʲ，则 differential residual 精确有

\[
E_N=(D+\lambda)b_N-r-Vb_N+b_N(qb_N)
=-\beta_{N+1}\lambda^{-N}+O_{H^1}(\lambda^{-N-1}).
\]

尾部只有有限个 β_a(qβ_b)，在 H¹ 中均有界。差 e=b_λ−b_N 的 nonlinear 差可写为

\[
e=R_\lambda\{Ve-e(qb_\lambda)-b_N(qe)-E_N\}.
\]

右端关于 e 的 norm≤C/λ。将其移到左侧后 inverse 一致有界，R_λ 再给一阶 λ⁻¹，故 ||e||_{H¹}≤C_Nλ⁻ᴺ⁻¹。

先在稍大的 bounded complex 源球上取得这个同阶 bound；actual contraction 解与 b_N 都解析。内层球的一维 complex Cauchy estimate 对全部单位源方向一致，遂给 H^{N+2}→H¹ Fréchet derivative 的同阶余项。不能省略这份扩大 complex 球的距离，也不能只由 pointwise O-估计直接称 C¹。源稿明确执行了该步骤，预算 H^{N+2} 足够。

## 3. 实际周期 upper triangularization 与 simple fast root

直接乘 T_b=[[1,0],[b_λ,I_m]] 并减去 T_b⁻¹T_b′，得到

\[
T_b^{-1}\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}T_b-T_b^{-1}T_b'
=\begin{pmatrix}\lambda+qb_\lambda&q\\0&V-b_\lambda q\end{pmatrix}.
\]

下左 block 为 r+Vb−bλ−b(qb)−Db，严格等于零。T_b periodic，因此两个实际 monodromy 相似。这就产生一条实际 fast multiplier

\[
\mu_f=\exp(\lambda L+\mathcal K_\lambda),
\qquad\mathcal K_\lambda=\int_0^Lqb_\lambda\,dx=O(\lambda^{-1}).
\]

其余 roots 是 V−b_λq 的 actual monodromy roots；该 coefficient 的 L¹ norm 在源球统一有界，Grönwall 使全部 slow roots 落在一个固定有界圆内。对充分大正 λ，fast root 位于 |μ−e^{λL}|<e^{λL}/2，slow roots 全在外，故 fast root 的 algebraic multiplicity 恰为一。这无需 slow roots 互相分离。

实际 characteristic coefficients 对源解析，简单根 IFT 给 μ_f 的局部解析复合；已有显式 μ_f 与统一圆选择使各局部支一致。μ_f/e^{λL} 靠近一，其唯一近零 log 恰是 K_λ。

原 normalized N=e^{−λL/M−τ}T_χ，τ=M⁻¹∫Σb_i。§16 已给全部 actual normalized class functions 与 τ 对合；Newton identities 给其 characteristic coefficients。因此 K_λ 在原物理括号下与每个 fixed F_{μ,r}=r⁻¹trN_μ^r 对合，亦与另一 K_ν 对合。这里依赖的是 §16 的实际 Poisson 定理，其全 M tensor 身份由另一个独审核验；本节没有用 formal residue gradient 去代替 actual characteristic gradient。

## 4. 不除 q 的 scalar factorization：逐 λ 系数合法

这一步独立于任何 actual inverse。记 𝒞=DI_m−V，b^f=Σβ_jλ⁻ʲ 是列乘法算子。算子合成必须保留 D 作用于 b 的项：

\[
\mathcal C\circ b^f=b^fD+Db^f-Vb^f.
\]

递推方程于是精确等价于

\[
r=(\mathcal C+b^fq)\circ b^f-b^f(D-\lambda).
\]

代入原 scalar L，逐项给

\[
\begin{aligned}
\mathscr L-\lambda
&=D-\lambda-qb^f-q\mathcal C^{-1}b^f(qb^f)
+q\mathcal C^{-1}b^f(D-\lambda)\\
&=(1+q\mathcal C^{-1}b^f)(D-\lambda-qb^f).
\end{aligned}
\]

故 1−L/λ 的两个 factors 恰为 (1+q𝒞⁻¹b^f) 与 (1−D/λ+qb^f/λ)。完全没有除以 q_j、d_j 或向量分量，也没有局部 scalar gauge。

两个 factors 都为 I+O(λ⁻¹)。取每个固定 λ⁻ⁿ 系数时，log 与 BCH 只含有限次乘法和有限个 nested commutators；相应 scalar PDO 的最高 D 阶有限，Adler residue 只需每个乘积有限深的系数。所以不存在用无限个未控项交换 formal trace 的问题。周期系数使每个 commutator 的积分 residue 为零。

第二 factor 的每个 log 系数是 differential operator，res_D 为零。第一 factor X=q𝒞⁻¹b^f 的 D 阶至多 −1，X^k 的阶≤−k，因此 k≥2 不贡献 D⁻¹。𝒞⁻¹ 的首项为 I_mD⁻¹，故 res_DX=qb^f。最终得到原 normalization 的严格有限系数身份

\[
\int_0^Lqb^f\,dx
=\operatorname{Tr}\log(1-\mathscr L/\lambda)
=-\sum_{n\ge1}\frac1n\operatorname{Tr}\mathscr L^n\,\lambda^{-n}
=-\sum_{n\ge1}C_n\lambda^{-n}.
\]

这一新 factor 甚至移除了 M=2 老证明的 q≠0 识别条件；全 M 与任意场幅度直接成立，不必另作 polynomial continuation。

## 5. Actual C¹ 系数提取与真实 Hamilton 场

实际估计与 formal identity 合并给

\[
\mathcal K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(H^{N+2};\mathbb C)}(\lambda^{-N-1})
\]

在所选内层有界球上一致。每个 fixed n 只用足够高的一层，不声称全部 C_n 同时在 H¹ 开集有定义。

独核 §16 的 actual order-zero 机制：原 traceless connection L_μ 对 free fields 仿射、无源导数；periodic W=Y N^rY⁻¹ 满足 W′=[L_μ,W]。Duhamel gradient 是 tr(W H_j)、tr(W[K_j−K_m])。普通积分物理张量 −(1/16)offdiag D 作用后，Dgradient 变成 tr(W[constant matrix,L_μ])。这没有源 x 导数，固定参数时给 H^s→H^s 的解析场，s≥1；W∈H^{s+1}。因此 X_F 实际属于同一 H^{N+2} 源空间。

将这个真实切向量代入 C¹ expansion，{K_λ,F_{μ,r}}=0 可逐阶乘 λ 取正实无限极限，严格得全部 {C_n,F_{μ,r}}=0。μ 不要求大或实；§16 的 entire actual parameter dependence 已给任意复 μ，或从已有开域按 identity theorem 延拓。τ 的场是 (Δ_x,d_x)/(16S)，Cn 为周期 jet 积分，所以 {τ,Cn}=0。于是 raw actual traces 与 characteristic coefficients 亦和 centered Cn 对合。

对每个 fixed Cn 在 smooth 场上，其 actual variational vector field只耗有限阶导数。用 CnF=0、Cnτ=0 得 CnK_ν=0，再在足够高的共同 Sobolev 层代入第二份有限 C¹ expansion，可重新提取 {Cn,Cj}=0。这个实际系数桥与原 formal local hierarchy 对合一致，而非将二者混为一条未证断言。

固定 finite family 的 normalized actual Hamilton 场有 Banach Picard 流。空间平移等变性与解析 low H¹ flow map 给平滑初态的 shift curve 在同一 low 时间窗 C∞；closed translation generator 逐阶使所有空间 derivatives 持久，随后方程给时间平滑性。因此无需逐高阶缩短 T。该结论是 auxiliary ambient Hamilton 流的实际存在，不自动是原 DLW 的 unrestricted Cauchy well-posedness。

## 6. 中心、共同相域与认证范围

静态任意 B 时，原 A_{χ,B}(λ_original)=BI+A_{χ,0}(λ_original−B)。centered actual data 为 λ_original−B，原 centered local traces须以此参数展开。raw parameter 的 coefficients 是相应 binomial drift。任意指定 B(t)=Γ(t)/(2c) 逐时允许；原 c≠0 PDE 不强制 Γ 守恒，本审没有擅自添加 Γ 常数闭合。scalar τ 产生的平移速度有一阶 Sobolev 损失，不称 order-zero 场。

新 §§17.1–3 通过，认证适用任意固定有限 M≥2、S≠0、任意 component means 与 bounded finite amplitude：actual periodic vector Riccati、simple fast characteristic branch、正确 original Cn coefficients、source C¹ remainder、actual class/Cn 对合与 finite family 的真实辅助流均成立。

§17.4 的 strong mixed-coherent 内部 plot 接合仍使用现有全 M strong presentations、真实 variational transport、mixed uniqueness 与新时间轴重参数化；这项须由对应共同域独审认证，本稿不以 ordinary Hs 取值替代这些条件。全 M gap/divisor 标号、weighted state inverse、完整 action-gradient 闭包和 nonlinear 最大各向同性依然另需证明；全 M actual 对合本身不是一般物理 Liouville 完备性。

全篇为本次源稿阅读与独立手算，未新增 machine checks；已完成的独立证书累计仍为 145 个断言。
