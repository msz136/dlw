# M=2 实际准动量、全部局部谱迹和固定轮廓 Hamilton 流独立审稿

2026-10-11。独立审查 [spectral_independent_review_20261011.md](../../刘维尔可积性/research/spectral_independent_review_20261011.md) 新 §14，实际读回 §§12–13、原 [GENERAL_PERIOD_MATRIX_LAX.md](../dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md) §§1–3 及 [TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md](../dlw_general_field_20261006/TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md) §§1–4。未执行或重复旧证书。本稿给完整有限阶正则性、trace-log 和实际流证明；认证范围是 M=2、c≠0 的指定物理均值叶，不能据此称为全 M 非线性 Liouville 定理。

## 1. 原算子、物理 Poisson 常数及谱中心

令 S=hMc/8=2δ≠0，源 z=(u,v) 是原自由物理变量的常数平移，u=b0−b1、v=d0−δ，各空间均值固定为零。本节先取谱中心 B=Γ/(2c)=0 的截面；原方程在 c≠0 分支没有强制 Γ 守恒。记

\[
q=-S+u,\quad V=-2uv/S,\quad
r=\{(\delta^2-v^2)(1+u/S)-v_x\}/S.
\]

原转移式 (D−b_j+d_j)ψ_{j+1}=(D−b_j−d_j)ψ_j，以及 λ=ν−2S/(μ−1)，给原首一算子

\[
\mathscr L=\nu-2S(P-I)^{-1}
=D-q(D-V)^{-1}r.
\]

这里 split 周期换基的首变量是 φ=Σχ_j=(μ−1)ψ0；它不是另一个自选谱参数。M=2 时 r=g/2、q=2f、V=C_old，与旧两格点标量式逐项相同。q 非零时

\[
q(D-V)^{-1}=(D-V-q_x/q)^{-1}q,
\quad W=V+q_x/q,
\]

所以 §14 (89) 的 C=D−W、L=D−C^{-1}qr 是原算子的精确等式，没有额外 scalar gauge 或倍数。谱迹确为 C_n=Tr L^n/n；物理 J 中的 −1/16 或层级生成元中的 1/(8G) 不应再乘进这个泛函定义。

原无权积分张量是

\[
J=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\]

也从原 rank-one 矩阵直接恢复了 traceless connection：其对角差为 u+2λv/S、非对角项为 (δ+v)(1+λ/S)、(δ−v)(λ/S−1)，正是 §13 (74)。特别它对 u,v 仿射且不含源导数，这是 order-zero 证明的关键。

一般 B 时，L_B=B+S_B(L_0)，其中 S_B 把 D 代成 D−B。因此原 centered 迹是 Tr(L_B−B)^n/n=C_n(z)，而 normalized actual trace 满足 F_B(λ)=F_0(λ−B)。相应 actual fast 乘子的 log 是 λL+K_0(λ−B)。必须以 σ=λ−B 展开才能识别 centered C_n；以 raw λ 展开得到的是未中心化迹的 binomial 组合。没有 λ−2B，也没有把 Γ 固定为守恒量。

## 2. H^{N+2} 的实际 Riccati 构造和 C¹ 余项

固定 N≥1。取一个复开源域 U_N⊂H^{N+2}_0×H^{N+2}_0，限制高阶范数有界，同时在 H¹ 中离背景足够近，保证 inf|q|>0。只要缩到该域的内层，就有 q,V∈H^{N+2}、r∈H^{N+1} 的一致界；并非用一个低阶范数控制任意阶。

λ≥Λ>0 实数时，R_λ=(D+λ)^{-1} 的 Fourier multiplier 为 (λ+ik)^{-1}，故 ||R_λ||_{H¹→H¹}≤λ^{-1}。在 ||b||_{H¹}≤C/λ 球中，H¹ 代数界使

\[
b=R_\lambda(r+Vb-qb^2)
\]

成为一致收缩：其 b 微分 norm 不超过 C/λ。解析隐函数或解析 contraction 给实际 small periodic b_λ 对源复解析。Riccati 结构恰是 split 原方程中 ξ/φ 的方程，不是形式 Bloch resolvent 替代。

β1=r，β_{j+1}=Vβj−Dβj−qΣ_{a+b=j}βaβb。逐阶归纳给

\[
\beta_j\in H^{N+2-j},\qquad 1\le j\le N+1.
\]

尤其 βN∈H²、βN+1∈H¹。令 bN=Σ_{j=1}^Nβjλ^{-j}，其 differential residual

\[
E_N=(D+\lambda)b_N-r-Vb_N+qb_N^2
=-\beta_{N+1}\lambda^{-N}+O_{H^1}(\lambda^{-N-1})
\]

在 U_N 一致为 O_{H¹}(λ^{-N})。尾项是有限个 qβaβb，最差也在 H²，故没有隐含多一阶导数要求。真实误差 e=b_λ−bN 满足

\[
e=R_\lambda\{(V-q(b_\lambda+b_N))e-E_N\}.
\]

算子 norm 小于 1/2 后立即得到 ||e||H¹≤2λ^{-1}||EN||H¹≤C_Nλ^{-N-1}。

e 是 H^{N+2}→H¹ 的复解析映射。上述一致误差在一个较大复源域成立；对内层点及 ||h||H^{N+2}=1，沿 z+th 的小复圆作 Cauchy 导数估计，得 ||D_z e[h]||H¹≤C'_Nλ^{-N-1}。因此源 C¹ 余项确实同阶。这里的复圆半径取决于内层至外层边界的距离，不能省略内层限制。

φ_x=(λ+qb_λ)φ、ξ=b_λφ 精确满足原 split 系统。φ 是非零 exponential，b 周期，因此实际 fast 乘子为 exp(λL+Kλ)，Kλ=∫qbλ。actual determinant 精确给 slow 乘子 exp(A−Kλ)，A=∫V。大正 λ 时两乘子分离，normalized trace 为

\[
F_\lambda=2\cosh(\lambda L/2-A/2+K_\lambda).
\]

实部大的 arcosh 支在一个统一小复源域可唯一选定，sinh 不为零；因此 Kλ 是真实 Fλ、A 的解析函数。实际 eigenline、乘子和余项链均成立。

## 3. λ-adic trace-log 的每个系数合法

先对光滑周期源作纯代数推导。令 bf=Σβjλ^{-j}、zf=λ+qbf、tf=W−qbf。直接展开及 Riccati 递推给

\[
(D-t_f)(D-z_f)=D^2-(\lambda+W)D+\lambda W-qr
=C(L-\lambda).
\]

例如零阶相消项是 (Wq−qV−qx)bf−qr=−qr，恰由 W=V+qx/q 完成。左乘 C^{-1} 并除 −λ 给

\[
1-L/\lambda=(1+C^{-1}q b^f)(1-D/\lambda+qb^f/\lambda).
\]

这在周期 formal PDO 系数的 λ^{-1}-adic 完备环中成立。两个因子都是 I+O(λ^{-1})；给定 λ^{-n}，log 级数只使用至多 n 次乘积，BCH 只使用至多 n 长度的 Lie words。每个相关 PDO 都有有限最高 D 阶数；低部允许无限，但固定 residue 只依赖有限个系数。因此各 log 和 trace 逐 λ 系数明确定义，不需要把 λ^{-1} 当作 D^{-1}，也不要求整个级数收敛。

周期 Adler trace 对交换子为零，故逐系数 Trlog(UV)=TrlogU+TrlogV。第二因子的每个 log 系数是微分算子，res=0。第一因子的 X=C^{-1}qbf 为 D 阶 −1，X^k 的 D 阶≤−k；k≥2 没有 residue，而 res X=qbf。于是

\[
\int qb^f=\operatorname{Tr}\log(1-L/\lambda)
=-\sum_{n\ge1}\frac1n\operatorname{Tr}L^n\lambda^{-n}.
\]

所有系数均周期，qx/q 在此 chart 合法；不存在用准周期 exponential 循环 trace 的步骤。与光滑源相等的有限泛函 −∫qβn 对 H^{n+2} 源解析；由密度和该实际表达式延拓至上述 Sobolev 源域。因此

\[
\boxed{K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(H^{N+2};\mathbb C)}(\lambda^{-N-1}).}
\]

符号和标度可手核：C1=−∫qr，C2=−∫Wqr。均匀场 q=−S、r=δ²/S、V=0 给 Kλ=−δ²L/λ−δ⁴L/λ³−2δ⁶L/λ⁵+…，与 L0=D+δ²D^{-1} 的 C1=δ²L、C3=δ⁴L、C5=2δ⁶L 一致。

## 4. Actual Hamilton 场确实保持源空间

记 Lμ 为 §13 traceless connection，Y′=LμY、N=Y(L)、Wμ=YNY^{-1}。Wμ 周期，Wμ′=[Lμ,Wμ]。实际源梯度是

\[
\nabla F_\mu=(\operatorname{tr}W_\mu H/2,
\operatorname{tr}W_\mu K_\mu).
\]

由 cyclic trace，D tr(WμKμ)=tr(Wμ[Kμ,Lμ])，同理对 H/2。故原 J 给

\[
X_{F_\mu}=-\frac1{16}
\big(\operatorname{tr}W_\mu[K_\mu,L_\mu],
\operatorname{tr}W_\mu[H/2,L_\mu]\big).
\]

没有丢失负号，也没有留下 u_x 或 v_x。固定 μ、s≥1 时，周期 ODE 及 Hs 乘法给 Wμ∈H^{s+1}；对源的 Volterra 微分同样提升，故 Wμ 是 Hs→H^{s+1} 的解析映射。上式是 Hs→Hs 的解析向量场，且其每分量积分为零，因为它原本是周期梯度的 D。尤其在 H^{N+2} 上，它正是该源空间的允许切向量；这使 C¹ 余项提取合法。

μ 依赖是 entire：connection 仿射依赖 μ，实际 fundamental matrix 的 Volterra 系列 entire，detY=1 使 inverse 也 entire。Wμ、X_Fμ 在 μ 紧集上有统一源及高阶界。这里无需先选择 Floquet eigenline，更没有 trace 在 μ=λ 的真正 pole；§13 tensor 的 pole 仅属于该代数证明。各对合表达式都是 μ 的 entire 函数，可以在密集参数集证成后解析延拓，也可对任意固定 μ 直接作下面的提取。

## 5. 从实际对合得到 C_n 的完整桥

§13 的实际 tensor total-derivative 恒等式已给 {Fλ,Fμ}=0。该步骤使用 actual 周期 W 和原 J，而不是 formal residue 梯度；本次读回并核对其梯度、周期分部积分和取迹方向，不重跑作者 tensor 脚本。另 A=−2S^{-1}∫uv 给 XA=(u_x,v_x)/(8S)，是平移 Hamiltonian。实际 Fμ 的基点平移只是 monodromy 共轭，故 {A,Fμ}=0。

因此对 λ 大正数，arcosh 链式法则精确给 {Kλ,Fμ}=0。以实际 X_Fμ(z)∈H^{N+2} 代入上节 C¹ 余项，得到

\[
0=-\sum_{n=1}^N\lambda^{-n}dC_n(z)[X_{F_\mu}(z)]
+O(\lambda^{-N-1}).
\]

按最小幂逐次乘 λ 并取极限，证出每个 {Cn,Fμ}=0。余项常数可以依赖固定 z、N、μ；μ 紧集上一致亦成立。这是实际 Poisson 对合，不只是密度系数名义相同。

全部 Cn 相互对合也可沿同一 actual 路线推得。固定光滑 z 和 n，局部微分泛函 Cn 的 Hamilton 向量 X_Cn(z) 光滑，平移不变性给 {Cn,A}=0。刚证明的 {Cn,Fμ}=0 及 arcosh 链式法则给 {Cn,Kμ}=0。再把 X_Cn(z) 代入任意阶的 Kμ 源 C¹ 展开，令 μ→+∞ 逐系数提取，得

\[
\boxed{\{C_n,C_m\}=0\quad\text{全部有限 }n,m,
\text{在光滑源交集上。}}
\]

这里第二次提取使用的是一个固定光滑向量；没有宣称所有高阶 X_Cn 是 H¹→H¹。若要写成单对 Sobolev 命题，可取足够高的有限阶：密度 −qβn 至多使用源 n 阶 jet，其 Euler 梯度至多 2n 阶，故保守 s≥m+2n+3 已使 X_Cn∈H^{m+2}，足以沿该方向提取 Cm。这个上界不求最优。

固定轮廓链式法则也给 {Cn,a_k}={Cn,g_k}=0；不含 contour 的 A 与 Cn 对合由局部积分平移不变性直接给。如此实际 Floquet、实际 center/gap 和原全部 centered Cn 在同一光滑物理叶上相互对合。没有推断谱迹确定实际 Floquet 函数，更没有用渐近级数消除 norming 信息。

## 6. 固定轮廓 a_k、g_k 的显式 order-zero 场

令 Dλ=Fλ²−4，轮廓 γk:λ=λk+ζ、|ζ|=ρ。源小域使其分母一致非零。由 §12 实际轮廓公式的源变分，

\[
X_{a_k}=-\frac1{2\pi i}\oint_{\gamma_k}
\frac{F_\lambda}{D_\lambda}X_{F_\lambda}\,d\zeta,
\]

\[
X_{g_k}=-\frac2{2\pi i}\oint_{\gamma_k}
\zeta\frac{F_\lambda}{D_\lambda}X_{F_\lambda}\,d\zeta
-2a_kX_{a_k}.
\]

每个系数是源解析标量，在 x 上恒定；固定紧轮廓的 X_Fλ 在 Hs 一致解析。因此这两式给 Hs→Hs 的真正解析、零均值 order-zero 向量场，s≥1。取实部或虚部即可得到实物理 Hamilton 场。这里常数允许依赖 k，不声称全 k 统一的 order-zero bound 或一个无限参数共同流。

半 gap 平方 gk 的 −2ak Xak 项不可遗漏；若改成完整 gap 平方则须整体乘 4。holonomy-subtracted center ak−A/L 则额外含 −XA/L，不应也标成 order-zero Banach 向量场。

## 7. 同一非零时间窗的全部光滑持久性

选一个固定 real Hamiltonian H=Re/Im Fμ、ak 或 gk。上文在 H¹ 均值叶小域给真实解析 XH:H¹→H¹。Banach Picard 给唯一局部流 Φ_t 及对初态的实解析解映射

\[
\mathcal S:z_0\longmapsto\Phi_{\cdot}(z_0)
\in C([-T,T],H^1).
\]

T 由一份低阶初态邻域和向量场局部界确定。先缩短一次 T 保持 q 非零及固定轮廓分母非零。

Fμ 在空间平移下因实际 monodromy 共轭而不变，ak/gk 同样不变；恒定 J 与平移交换，所以 XH(T_hz)=T_hXH(z)。唯一性使 S(T_hz0)=T_hS(z0)。对光滑 z0，h↦T_hz0 是 H¹ 数据空间内的 C∞ 曲线；解析 S 给 h↦T_hΦ_.(z0) 是 C([-T,T],H¹) 内 C∞ 曲线。平移群闭生成元判据于是给

\[
\partial_x^j\Phi_.(z_0)\in C([-T,T],H^1)
\quad\text{每个 }j\ge0,
\]

全部 j 共享原低阶 T。由于 XH 在每个高阶 Hs 也解析，ODE 随后给所有时间导数，得到同一个时间窗上的 C∞(t,x) 轨道。这个证明无需逐阶重新取越来越小的时间。

对任意有限组上述 H，统一选低阶邻域和最小 T 得共同光滑窗。实际对合及 constant J 在光滑源上的 Hamilton 恒等式给 [XH,XG]=0；order-zero 场的导数在 H¹ 连续，光滑源密度把该等式延拓至 H¹ 小域，故实际局部流彼此交换。光滑轨道保留全部可定义 Cn 及 actual center/gap。这一 finite-family 结论不等于可数族的无限参数流或已证原 DLW 共同域的切向性。

## 8. 含平移的实际族也可解释，但要保留阶数区别

holonomy-subtracted center 的实流可写为 Φ^ak_t 与真实平移 T_{−t/(8SL)} 的组合，因为 A 与 ak 对合。故它有实际强连续 Hs 群及光滑点上的 C∞ 轨道；一般 Hs 点的 t 微分仍只在 H^{s−1}，不能将 XA 称为 order-zero。

原 unnormalized trace e^{(λL+A)/2}Fλ 的向量是一个 source-scalar 系数乘 X_Fλ，加上 (1/2)e^{(λL+A)/2}Fλ XA。沿其自身实 Hamilton 流，A 和 Fλ 因对合守恒，所以这些系数可冻结为初态值；实部/虚部亦由对应 order-zero 流加平移给实际轨道。该补充不改变低阶可微性界线。

## 9. 末审结论与剩余依赖

§14 的 Riccati、有限 C¹ 余项、原 centered Cn 标度、逐 λ trace-log 合法性、实际 X_F 的 order-zero 源切向和 μ 解析延拓均通过独立复核。上文另给所有 Cn 相互对合的第二次 actual 系数提取，以及固定轮廓 Hamilton 场和同 T 的 C∞ 持久性完整证明。没有找到需撤回的新 §14 定理。

前九节先认证 M=2、c≠0、明示源小域内的 actual spectral 辅助流及原 centered 局部积分的对合；下节实际读回作者新 §14.5 后去掉幅度、均值和 q 非零限制。尚未证明这些辅助流保持原 DLW strong/mixed-coherent 解域，也没有完成 nonlinear inverse spectral/norming、nonlinear 最大各向同性或 Liouville 完备性。全 M 以及任意 Γ(t) 与真实原时间共同域仍须依各自证明接合。

本次新增是纯独立推导和文件审阅，不运行旧脚本，也未增加机器证书断言；本代理先前独立脚本合计仍为 145 asserts。

## 10. 新 §14.5 的任意幅度、任意组件均值推广

实际读回作者新 §14.5 后独立复核，该推广成立。固定 S≠0，令 u,v 为任意周期源，空间均值可任意。原闭合 b1=−d0u/S、b0=b1+u 与 d0=δ+v、d1=δ−v 不要求这些均值为零；所以 traceless connection、常数 J 和 actual tensor identity 仍逐点成立。§13 的对合证明没有小幅度或 small δ 依赖。

在任意给定有界 H^{N+2} 复源球，q,V,r 有对应界；Riccati contraction 的右端没有 q^{-1}，故只需相应增大正 Λ，§2 的 actual H¹ 误差和内层 C¹ 余项原样成立。唯一待消除的 q 非零条件只在 formal 系数识别中。

使用未除 q 的原 L=D−q(D−V)^{-1}r，其固定 Cn 是有限 q,V,r jets 的多项式空间积分：formal inverse (D−V)^{-1} 的每个固定系数是 V 的 differential polynomial，固定 residue 的乘积只使用有限个系数。递推 −∫qβn 同样是有限 jet 多项式。它们再通过上述 q,V,r，成为 u,v jets 的多项式，分母只有外加非零 S 的常数幂。

给任意目标 z=(u,v)，沿 z(t)=tz。因为 q(t)=−S+tu，小 |t| 时 q 无零点，§3 的周期代数恒等式已经给 Cn(tz)=−∫q(tz)βn(tz)，且该恒等式本身不依赖零均值假设。两边是 t 的有限多项式，在一个非空开 t 域相等则处处相等；取 t=1 即跨过 q 的任意零点。对有限 Sobolev 源亦先用光滑密度，或直接采用其有限多项式表达式延拓。无需假设整个 t 路径落在 q 非零图。

因此任意有界高阶源球上都有 actual Kλ 的有限源 C¹ 展开及 Cn/Fμ 对合；其 Λ 和常数依球改变。实际 X_Fμ 是整个 Hs 源空间上的解析 order-zero 场，固定 μ 的每个源点有局部实流，§7 的 translation-equivariance 论证给光滑初態的同 T 全阶持久性。A、Cn 的平移不变性也没有均值或幅度限制，因此 §5 的全部 Cn 相互对合与实际链式提取推广到所有光滑 M=2 周期物理源。

这里“任意均值”指各指定均值叶的真实场和局部流；X_Fμ 沿每条轨道保留这些均值，并不在动力学中随意改变 Casimir。固定轮廓 center/gap 的标号、有限独立及全频源映射仍使用作者 §§12、15 的明确小均匀叶，不据此推广到任意幅度或均值。

## 11. 新 §15 的实际 gap 和 center 二次系数独核

已实际阅读 §§15.1–15.4，并读回 §7.2–7.3 的物理通道定义和 mixed 独审稿 §17 的真实 Hilbert 参数图。以下为新增手算验证，不执行任何旧/新作者脚本。

取 k=2πn/L、ω=√(k²−4δ²)、λn=iω、γ=ω/k>0、σ=(−1)^n。背景 normalized monodromy 是 σI。实际一阶矩阵在指定背景 eigenframe 中是 C=[[0,bar c−],[c+,0]]；原 actual endpoint gauge 在背景为 scalar monodromy，其一阶 conjugacy commutator 为零，故通道值无需额外 source frame 导数。反向矩阵元 bar c− 的识别仅在实源上使用，复源须用其 holomorphic 反向样本。

写 N=σ(I+εC+ε²R+…)。detN=1 给 trR=−detC=c+bar c−，因此 F=σ(2+ε²c+bar c−+…)、D=F²−4=4ε²c+bar c−+… 。这证明作者 D2(λn)=4c+bar c−，符号正确。

令 Γ(λ)=√(λ²−4δ²)，选 Γ(λn)=ik。则 Γ′=λ/Γ、Γ″=−4δ²/Γ³，所以

\[
\Gamma'(\lambda_n)=\gamma,\qquad
\Gamma''(\lambda_n)=-4i\delta^2/k^3.
\]

展开 D0=4sinh²(LΓ/2)，在 ζ=λ−λn 得

\[
D_0=L^2\gamma^2\zeta^2
+L^2\gamma\Gamma''(\lambda_n)\zeta^3+O(\zeta^4).
\]

原零均值叶使 D 的源一阶变化对所有 λ 为零，故实际轮廓 log(D/D0) 的 ε² 系数为 D2/D0。ak² 从 ε⁴ 才开始。residue 直接给

\[
g_n^{[2]}=-\frac{D_2(\lambda_n)}{L^2\gamma^2}
=-\frac{4c_+\bar c_-}{L^2\gamma^2},
\]

\[
a_n^{[2]}=-\frac12\left[
\frac{D_2'(\lambda_n)}{L^2\gamma^2}
-\frac{D_2(\lambda_n)\Gamma''(\lambda_n)}{L^2\gamma^3}
\right].
\]

两式分别是作者 (97)、(99)。§7 的真实物理 bracket 权重 K=Lk²γ/(16S)，I=QP=c+bar c−/K，因此 g_n^{[2]}=−k²I/(4SLγ)，没有漏 h、S 或 L，也没有把 half-gap 与 full-gap 平方混用。D²g(0)[η,η] 才是二次齐次系数的两倍。

原 traceless connection 对源仿射，所以作者 (98) 的有序二次 Born 积分恰是 actual F 的 ε² 系数，没有 split r 的非线性项遗漏。D2=2F0F2，F0′(λn)=0、F0(λn)=2σ 给 D2′=4σF2′。F2′ 自动包含所有 propagator 及 Kλ 的参数微分，不仅是 resonant coupling product，因此中心系数没有丢掉 off-resonant 项。§12 的 actual c0-valued 解析性使其 Taylor 二次系数仍在 c0，故 a_n^{[2]}−A^{[2]}/L∈c0 的 (100) 也成立。

有限物理见证 Q=P=1 时，I 的 δP=1、i 分别产生两条实独立 action 变化。设 b_n=−k²/(4SLγ)≠0，则 d(Re gn,Im gn)(εη) 在对应真实 ζ 测试方向上的 leading block 是 ε diag(bn,bn)，不是 2εdiag(bn,bn)。因而 (101) 的 ε^{2|E|}∏bn² 因子正确，选定 actual gap 也在 ε≠0 小时分裂。

mixed §17 明示 F 的实结构、DF(0) 对每个真实有限 Fourier 子空间满射和实有限维预复合的合法 strong plots。由于 dgn(0)=0，复合 Hessian 的 D²F 项消失；上述有限 Hessian minor 给同一 H 参数球上不恒零的解析函数。实 norm-open Hilbert 球是 Baire 空间，非零解析 minor 的集合开稠密，所以 §15.4 可数交集给同一个 actual strong 状态的每个 finite gap prefix 独立。该参数球的 residual 性不等于整个 strong 相域的 residual 性；与 charge minors 交集只保证两族分别独立，未保证其合并族独立。作者保留了这两条界线。

新增 §14.5 和 §15 关键系数均通过独立复核。一般 M=2 actual 对合及局部辅助流的幅度限制已去除；gap Hessian/有限独立与 same-strong 状态仍限定于明示小均匀平均叶。实际辅助流对 strong 域的切向、完整 norming/inverse、nonlinear 极大各向同性及 Liouville 完备性继续开放。全部工作是独立手算和源文件阅读，脚本 assert 总数仍为 145。
