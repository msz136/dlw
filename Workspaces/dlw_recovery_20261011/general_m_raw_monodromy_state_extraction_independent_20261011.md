# 一般 M 完整 framed 单值矩阵的实际低阶状态恢复：独立审计

2026-10-11。由已证 periodic coefficient state inverse 继续推进实际谱 **状态**恢复。全部 ODE、极限和采样均为实际对象。未执行脚本。原物理 parameters/Casimir 均值按 chart 保留；没有把 Γ(t) 冻结。

依赖：[periodic physical state audit](general_m_periodic_gauge_state_inverse_independent_20261011.md) §§3–7、11；[独立 Volterra Fourier 核](general_m_framed_monodromy_fourier_kernel_20261011.md) §§1–6（完整实际读取、逐式核验）。后者的 odd fiber estimate 与 ambient IFT 下文重新说明。

新结论分两层：任意 M、S≠0 的该物理低阶图上，原 full framed monodromy 能从正实谱极限恢复 d(0)，进而准确校准到 Cauchy-periodic constant-H frame。再在足够小的向量势图内，actual offdiagonal samples 加有限 slow block 具有 L²/ℓ² 的真实局部解析逆，因此原完整 monodromy 函数局部决定原一般物理场。这里保留 full frame；conjugacy classes/谱迹不提供同样资料。

## 1. 相空间与必须保留的数据

令 m=M−1、S=Mδ≠0、period L。物理状态为
\[
(q-q_*,d_{\rm first}-\delta\mathbf1)
\in (L^2_0)^m\times(H^1_0)^m
\]
的一个已有 nonlinear open chart。mean-normalized periodic G 给 r∈L²、V∈L²、G∈H¹。定义 Cauchy-periodic frame
\[
G^f=G G(0)^{-1},\qquad G^f(0)=G^f(L)=I,
\]
\[
a^f=qG^f,\quad b^f=(G^f)^{-1}r,\quad
H^f=G(0)H G(0)^{-1}.
\tag{1}
\]
以下省 f，实际 connection 为
\[
A_\lambda=
\begin{pmatrix}\lambda&a\\b&H\end{pmatrix},
\qquad Y_\lambda(0)=I,\quad T_A(\lambda)=Y_\lambda(L).
\tag{2}
\]
其 full framed monodromy 与原 state-adapted split 的 monodromy准确相同，因为 (1) 的 endpoint gauge 是 I。原 χ-frame 与它的关系只剩
\[
T_\chi(\lambda)=T_d(0)T_A(\lambda)T_d(0)^{-1},
\quad T_d=[d/S,Z],\quad T_d^{-1}=[\mathbf1^T;E-d_{\rm first}\mathbf1^T/S].
\tag{3}
\]
原 scalar determinant normalization在这些相似变换下相同。

## 2. 大正实 λ 的实际 periodic Riccati 与 fast 投影

对任意固定 bounded L² 的 a,b 和有限 H，在 sufficiently large real λ>0，求周期列 η：
\[
\eta_x=b+H\eta-\lambda\eta-\eta(a\eta).
\tag{4}
\]
周期 inverse Rλ=(D+λ)⁻¹ 具有
\[
\|R_\lambda\|_{L^2\to L^2}\le\lambda^{-1},
\qquad
\|R_\lambda\|_{L^2\to L^\infty}\le C_L\lambda^{-1/2}
\tag{5}
\]
（λ≥1）。第二界由周期 exponential convolution kernel 的 L² 范数直接得到。用 L∞ 球、L² 右侧作 contraction：线性 Hη 的 Lipschitz contribution O(λ⁻¹/²)，quadratic term的 contribution O(λ⁻¹)；b 的 forcing 为 O(λ⁻¹/²)。因此唯一小 η 是实际 periodic 解，且
\[
\|\eta\|_\infty=O(\lambda^{-1/2}),\qquad
\|\eta\|_2=O(\lambda^{-1}).
\tag{6}
\]
后一界用第一条 resolvent bound 和先得的 L∞ 小性闭合。η∈H¹，因为 (4) 右侧 L²；所以 η(0) 有定义。这里没有除任何 q/a 分量。

periodic triangular gauge
\[
T_\eta=\begin{pmatrix}1&0\\\eta&I\end{pmatrix}
\]
给实际 upper-triangular connection
\[
T_\eta^{-1}A_\lambda T_\eta-T_\eta^{-1}(T_\eta)_x
=\begin{pmatrix}\lambda+a\eta&a\\0&H-\eta a\end{pmatrix}.
\tag{7}
\]
令 h=H−ηa、Y_s 为 slow fundamental matrix。由 \(\|\eta a\|_1=O(\lambda^{-1/2})\)，Gronwall 给 Y_s 与 Y_s⁻¹ 在整个 interval 一致有界（亦可用 (6) 的 L² bound 得该 L¹ 误差 O(λ⁻¹)）。triangular monodromy为
\[
\widetilde T_\lambda=
\begin{pmatrix}\mu_\lambda&J_\lambda\\0&E_\lambda\end{pmatrix},
\qquad
\mu_\lambda=e^{\lambda L+\int_0^La\eta},
\quad E_\lambda=Y_s(L),
\tag{8}
\]
\[
\frac{J_\lambda}{\mu_\lambda}
=\int_0^L
e^{-\lambda t-\int_0^t a\eta}\,a(t)Y_s(t)\,dt
=O(\lambda^{-1/2}).
\tag{9}
\]
最后一步是实际 L² Cauchy–Schwarz，\(\|e^{-\lambda t}\|_2=O(\lambda^{-1/2})\)。μ exponential 增长，E有界，故 fast eigenvalue与slow谱实际分离。

triangular fast spectral projector准确是
\[
\widetilde\Pi_\lambda=
\begin{pmatrix}1&J_\lambda(\mu_\lambda I-E_\lambda)^{-1}\\0&0\end{pmatrix}.
\tag{10}
\]
由 (6)、(9)，共轭回 Tη(0) 得 \(\Pi_{A,\lambda}\to e_0e_0^T\)。同时
\[
\frac{T_A(\lambda)}{\operatorname{tr}T_A(\lambda)}
\longrightarrow e_0e_0^T.
\tag{11}
\]
可直接从 (8) 除以 μ 验证 (11)，所以无需额外输入 eigenvector 或 projector。

## 3. 原始 endpoint 的实际恢复

由 (3)、(11)，
\[
\boxed{\quad
\lim_{\lambda\to+\infty}
\frac{T_\chi(\lambda)}{\operatorname{tr}T_\chi(\lambda)}
=T_d(0)e_0e_0^TT_d(0)^{-1}
=\frac{d(0)\mathbf1^T}{S}.
\quad}
\tag{12}
\]
因此原 original wave frame 中的任何一列都恢复 d(0)/S，S已是给定 physical parameter。dH¹保证该 endpoint 有意义。每个单独 d_j 可为零，T_d 仍处处可逆。

式 (12) 对 determinant-normalized full matrix
\[
N_\chi(\lambda)=(\det T_\chi(\lambda))^{-1/M}T_\chi(\lambda)
\]
仍成立，因为相同非零 scalar factor在 ratio 中消去。选定整个函数的 scalar root须按原 normalization保留；极限本身不依赖该 scalar选择。于是原 full normalized framed Nχ也恢复 T_d(0)，并准确计算
\[
N_A(\lambda)=T_d(0)^{-1}N_\chi(\lambda)T_d(0).
\tag{13}
\]
由于 Cauchy-periodic gauge 的两端都是 I，不再需要先知道 mean-normalized G(0)。这解除的是 full original framed 数据的有限 calibration 输入，不是 conjugacy class 数据的 frame。

## 4. 实际 ℓ² 数据：fiber 预算和归一化

对 (2) 的 monodromy，只有 2r+1 个 offdiagonal insertions的 Dyson path贡献两组 offdiagonal blocks。chronological times \(0<t_1<\cdots<t_{2r+1}<L\) 的相位是
\[
\tau=t_1-t_2+\cdots+t_{2r+1}\in[0,L].
\]
上方相位 \(e^{\lambda(L-\tau)}\)，下方相位 \(e^{\lambda\tau}\)。固定 τ 的实际 Lebesgue fiber 体积为
\[
\frac{\tau^r(L-\tau)^r}{(r!)^2}
\le\frac{(L/2)^{2r}}{(r!)^2}.
\tag{14}
\]
由 gaps 换元的 Jacobian=1、fiber Cauchy–Schwarz 和全 simplex上的 product L² 积分界，任意 distinct alternating 多线性输入有
\[
\|K_{2r+1}\|_{L^2_\tau}
\le e^{L\|H\|}\frac{(L/2)^r}{r!}
\prod_{j=1}^{2r+1}\|f_j\|_2.
\tag{15}
\]
这条 bound 已逐步独核；它不是仅给每个谱参数单独的 O(δ) 界。因 1/r!，整个 kernel series在所有 bounded potential balls一致 L² 收敛且 joint analytic。实际 Dyson series的逐点收敛与 kernel Fourier 积分一致。故 λ_n=ik₀n、n∈Z 的两组 offdiagonal samples是整解析 ℓ² 数据。

对 determinant-normalized matrix，准确为
\[
N_A(\lambda)
=e^{-\lambda L/M-L\operatorname{tr}H/M}T_A(\lambda).
\tag{16}
\]
定义 samples
\[
\mathfrak s_n^\pm
=L^{-1/2}e^{ik_0nL/M}(N_A(ik_0n))_{0s,s0}.
\tag{17}
\]
它们就是 raw Fourier samples乘同一个有限解析 scalar \(e^{-L\operatorname{tr}H/M}\)，仍 joint analytic 到 ℓ²。必须保留 (17) 的已知 λ phase；直接把 normalized samples看成同一个 Fourier系数会漏该 phase。

## 5. 未知 H 的实际 finite datum 与 Banach inverse

取 finite matrix datum
\[
\mathfrak C=(N_A(0))_{ss}.
\tag{18}
\]
在向量 vacuum a=b=0 时，
\[
\mathfrak C=e^{L(H-\operatorname{tr}H\,I_m/M)}.
\tag{19}
\]
H的线性变换 \(\mathscr T H=H-(\operatorname{tr}H)I_m/M\) 可逆，因为 m=M−1，
\[
\mathscr T^{-1}K=K+(\operatorname{tr}K)I_m.
\tag{20}
\]
在 a=b=H=0，完整实际 map
\[
(a,b,H)\longmapsto
\big((\mathfrak s_n^+,\mathfrak s_n^-)_{n\in\mathbb Z},\mathfrak C-I_m\big)
\tag{21}
\]
的微分是两组 Fourier isometry 与 L\(\mathscr T\) 的 direct sum。这是 bounded Banach 同构。joint analytic IFT给真空的一个实际低阶开域上局部解析双逆；故足够小的非零 uniform物理背景也在同域，并可缩取其背景邻域。附加的小半径是该 actual inverse 的条件，不能仅由旧 strong δ 阈值未经估计地宣称满足。

在 vector vacuum a=b=0、任意给定 H₀，首次 Fourier kernels是 a(t)e^{H₀t}与e^{H₀(L−t)}b(t)，仍 bounded可逆的 L²乘法；finite derivative dexp 仅在 ad H₀ 有非零 Fourier alias时退化。因此还可在这些 nonalias H₀ 向量真空旁建立 ambient IFT。本文只需 near-zero 版本，不以它自动覆盖任意幅度物理 a,b。

## 6. 原一般物理场回拉与 B

输入原 **完整 normalized framed monodromy 函数** Nχ(λ)，先按 (12) 恢复 d(0)，再按 (13) 得 NA，最后由 (17)–(21) 的实际 inverse得 a^f,b^f,H^f。已有 Cauchy physical state map \((P_0a^f,P_0b^f)\) 的真实低阶 inverse再给 q,d及全部原物理分量。它作用在一般周期函数开域；未施加 finite Fourier 截断或 special-family ansatz。

任意共同 spatial B 可在任意 reference B₀ 附近保留：对 raw Tχ先取固定 chart shift \(\lambda_{\rm orig}=\lambda+B_0\) 与 known scalar factor e^{−B₀L}，connection的 slow matrix变为 H^f_c+(B−B₀)I，而 q,r不变；这落在同一 ambient map中。若采用 normalized Nχ，则上述共同 scalar已经消去，只需固定谱参数shift，内部 trace normalization按 (16)重新保留。恢复 q,d后，用 finite H trace减去恢复状态的 centered trace，除 m 得 B−B₀。因此这一 state chart可以同时保留 B参数，不导出 B_t=0。

## 7. 准确范围和剩余缺口

通过：actual periodic Riccati 的 L²→L∞预算；fast projector/normalized-matrix极限；从原 full framed Nχ自身恢复 endpoint d(0)；Cauchy-periodic gauge免除额外 G(0)输入；odd Volterra L²核和 actual normalized ℓ²采样；未知 holonomy H的 finite datum；small-potential Banach状态双逆；既有一般M物理 state inverse的回拉。

不通过的升级：从 conjugacy classes/eigenvalues单独恢复 state，标准 weighted h^N正则谱坐标，physical Poisson canonical化或 action-gradient闭包/最大性，以及原时间的 action-angle Liouville theorem。raw samples有1/n或1/n²尾，即使源C∞也不能直接放进全部h^N。这里得到 actual full framed谱 **状态**逆；高阶目标须另作端点/asymptotic renormalization。

此外，式 (12) 的 raw endpoint 提取使用整个正实谱方向的实际函数。本文证明的是原 full framed monodromy 在上述实际物理像上的局部唯一恢复，以及校准后的明确 Banach 数据双逆；没有给 original raw entire-function 空间指定一套自然 Banach 范数、证明其中任意邻近函数都 onto 物理态，或将仅一个未校准 raw 采样子集当作同样的自由坐标。

## 8. kernel 子审末审记录

已实际读回 [general_m_framed_monodromy_fourier_kernel_20261011.md](general_m_framed_monodromy_fourier_kernel_20261011.md) 全文，包括新增 §10 式 (28)–(39)。该文件 SHA256 为 D16B79492F24D3532839A09662B5D4898DA8B373FBA3B9BBE3D692705DA29A7B。

通过：任意 distinct alternating 输入的 fiber L² bound；kernel sum 与实际 Dyson monodromy一致；\(L^{-1/2}\) Fourier归一化；全 n∈Z 的 ℓ²整解析；fixed-H IFT；raw full slow finite datum；normalized相位 \(e^{ik_nL/M}\)；normalized有限矩阵 derivative \(L\mathsf P\) 与 inverse \((\dot C+\operatorname{tr}\dot C\,I_m)/L\)。非零 H₀ 的公式
\[
DC_{H_0}\dot H
=e^{LK_0}\varphi(L\operatorname{ad}H_0)L\mathsf P\dot H,
\quad
\varphi(z)=(1-e^{-z})/z
\]
也通过：\(\operatorname{ad}K_0=\operatorname{ad}H_0\)，dexp 的整个函数在谱上无零才可逆；Jordan非对角化不另制造障碍。

子审 §7 与 §10.4 的 n≠0 subset theorem 明确只在 finite graph 一阶导数全零的假设下成立。它适用于 mean-normalized coefficient graph，不可未经重新估计地套用 Cauchy graph，后者有式 (25) 的非零 finite derivatives。本文使用所有 n 的 augmented ambient theorem再回拉物理 Cauchy图，因此不需冒用这个 subset假设。

raw smooth 势的两个 weighted 反例亦已直接核对：b=0,a常数,H=h 时样点 \(a(e^{hL}-1)/(h-\lambda_n)\) 为1/n；H=0,a/b非零常数时准确常矩阵 exponential 给 \(2La^2b/\lambda_n^2+O(n^{-4})\)。因此这里只认证L²/ℓ²状态逆。没有新 machine certificates；没有重跑旧证书。
