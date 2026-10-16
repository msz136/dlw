# 全 M 标量物理像、Floquet 切线逆与完备性独立审查

2026-10-11。目标为一般物理场的原半离散 DLW 的完整 Liouville 可积性。本稿独立审查 `completeness_routes.md`、`scalar_poisson_quotient.md`、`periodic_structure_audit.md`，并接续其实际原始证明。没有完成该目标；下面给出可核验的新连接、严格条件及下一步需要证明的命题。

本稿只处理有限格点周期 M≥2、连续周期 x∈R/(LZ)、h>0、c≠0 的静态物理叶；独立物理分量 p=P_0U 与 w 的空间均值固定。共同 U 分量由闭合关系非线性恢复，其空间均值没有额外固定。连续谱参数中的 B=Γ/(2c) 先取某个时间截面的数值。原方程不强制 Γ_t=0；解释任意 Γ(t) 的守恒谱数据时必须先作相应平移与谱中心化。这里没有把 Γ 固定为原方程额外守恒量，也没有覆盖 c=0 或非周期平均分支。

## 1. 原依赖恢复与审查结论

已实际读取：本专题 `GOAL.md`、`README.md`、`STATE.md`；上述三份研究稿及 `scalar_monodromy_linearization.md`、`nonlinear_inverse_checks.md`；旧稿 `GENERAL_PERIOD_MATRIX_LAX.md`、`GENERAL_PERIOD_FREE_FIELD_POISSON.md`、`RESEARCH_NOTES.md`、`CONSERVATION_FAMILY_VERDICT.md`、`dlw_field_liouville_20261006/THEORY.md`；真正的全阶括号证明 `dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md`。旧 THEORY 的同目录引用并不是实际文件位置，不能把断链当作未读证明。

可保留的结论是：固定物理分量均值的实际有理像上，前 2M−2 个完整标量系数具有局部状态逆；源物理叶及其实际标量像具有准确的弱辛形式；全部已构造的局部谱迹在原物理括号下对合。本轮已接到已有 strong 共同域中的有限支持真实时间 germs，未证明一般 Sobolev 初值的原层级 Cauchy 流。尚未证明完整非线性 inverse Floquet/divisor 变换、非线性谱作用量括号的正则化或非线性最大各向同性。

本次新增自足结果：

1. 均匀全 M 背景上，**带固定基点和 companion 归一化的完整 Floquet 单值矩阵的微分，可从共振采样恢复每个非零空间 Fourier 模态**。这把旧的系数状态逆具体接到了 Floquet/norming 数据的切线层。
2. 同一背景上，**谱迹层级与平移动量的线性化 Hamilton 场能通过多项式插值分离任一非退化 Fourier 模态的全部 Floquet 通道**。这是二阶 Hamilton/线性层级的有限块结论，不能改称非线性最大各向同性。

3. §7–10 进一步给出原物理 Poisson 结构在完整 framed 共振通道中的精确配对、统一全频半阶辛归一化、指数衰减正则序列上的线性二次最大各向同性及共同真实线性流域。全频最大性使用**全部 C_n 与 P_mom**；只有奇数 C_n 与 P_mom 时严格缺少独立相位方向。所有这些新增结论仍限定于均匀背景的线性二次模型。

4. §11 核实固定 frame 的非线性代数尾项会破坏候选同阶 Sobolev inverse；§12–15 则构造 M=2 的 actual moving gaps、真实 Poisson/C_n 桥和精确 Hessian。在同一个实际 strong 参数图中，可同时使全部有限 actual gap 块分别独立。这些结果仍不证明 gap 最大性。

5. **§16–17 给任意有限 M、S≠0、任意分量均值及幅度的新实际谱定理**：从原 h-weighted 张量推出 free J=−offdiag(D)/16；exact affine traceless connection 的 dimension-free R 恒等式证明全部 actual Floquet characteristic 数据彼此对合。vector periodic Riccati 给真实 H^{N+2} 源 C¹ 高频展开，trace-log factorization 不除 q 并准确识别全部原 centered C_n；故 actual class 数据与每个 C_n 也对合。固定 normalized 谱参数 Hamilton 场为 order-zero 解析辅助流，并可在已有全 M strong presentations 条件下输送同一共同域。仍缺 nonlinear norming/divisor inverse 与 Hamilton 闭包=共同微分 annihilator。

独有证据：[局部逆独立核查](../../Workspaces/dlw_recovery_20261011/spectral_local_inverse_audit.md)、[共振与插值核验脚本](../../Workspaces/dlw_recovery_20261011/spectral_floquet_resonance_checks.py)、[核验结果](../../Workspaces/dlw_recovery_20261011/spectral_floquet_resonance_checks.json)。以下全 M 结论的依据是推导，有限检查只核对算式。

## 2. 局部状态逆的关键依赖可补成明确命题

沿用 b_j=U_j/2、d_j=hw_j/8、u_j=b_j+d_j、v_j=b_j−d_j，S=Σd_j=hMc/8，ν=B−S。原顺序为

\[
P=T_{M-1}\cdots T_0,\qquad T_j=(D-v_j)^{-1}(D-u_j),
\qquad \mathscr L=\nu-2S(P-I)^{-1}.
\]

非零实周期差的交换恒等式

\[
(D-a)(D-b)^{-1}=(D-b-\theta)^{-1}(D-a-\theta),
\qquad \theta=D\log|a-b|
\]

保持两个标签各自的空间均值，且可唯一反交换。有限次交换给真实左分式 P=Q^{-1}R。其 Q、R 为 monic M 阶算子；前 M 个负部方程对 Q 的低阶系数是逐点线性方程，不含这些未知系数的导数。均匀点的矩阵行列式为

\[
\det A=(-1)^{M(M-1)/2}(-2\delta)^{M^2},\qquad \delta=hc/8\ne0.
\]

因此 A 可逆；两个同阶左分母之差及任何低阶左分母都会给 At=0，故 Q 唯一且最小。**全部负部消失的存在性仍来自实际因子交换；不能只解前 M 个负部方程就在任意 ambient PDO 上宣称有理性。**

零分量均值叶的 Q/R Floquet 倍子分别只有一个值

\[
\mu_Q=e^{L(\chi-\delta)},\qquad \mu_R=e^{L(\chi+\delta)}.
\]

均匀 monodromy 是单 Jordan 块；cyclic 性是开条件。在固定实际谱重数层内，令 F 为其中一个 monodromy，N_F=F−μI；固定参考 cyclic 向量 v 后

\[
e_i=N_F^{M-i}v,\quad i=1,\ldots,M,
\qquad E_k=\operatorname{span}(e_1,\ldots,e_k)=\ker N_F^k
\]

给显式、相容、实解析的旗标基。随后线性 ODE 与非零 Wronskian 恢复有序因子。基函数是 Floquet 解，通常不是周期函数；其 Wronskian 的对数导数才是周期系数。

共同均值无需另加冻结：若 q_{M−1}、r_{M−1} 分别为 Q、R 的次首系数，则

\[
\boxed{\quad\chi=\delta-\frac1{ML}\int q_{M-1}
             =-\delta-\frac1{ML}\int r_{M-1}.\quad}
\]

同一 P 先给同一 Q/R，继而给同一 χ，再与已固定的原分量均值合成同一有序倍子列表。χ 随物理动量变化，不能写作 Casimir。

一个足够的保守导数预算是 J=3M+M(M−1)/2：前 2M−2 个 ℓ 系数的 C^{k+J} 控制可给逆出的物理场 C^k 控制。有限 jet、有限矩阵逆、固定秩核基和 ODE 连续依赖给 C∞ 实际像上的连续局部逆；这不证明同阶 Sobolev Banach onto 微分同胚。

还可以扩大参考点：任意满足原闭合的实常场，只要每个 numerator 常根 u_i^0 与每个 denominator 常根 v_j^0 都不同，Q_0/R_0 互素，有限 Padé 矩阵同样可逆。实根的不同指数没有 Floquet 别名；重复根各有单 Jordan 块，固定标记倍子模式仍给唯一旗标。所有跨根交换差非零且参考 Wronskian 非零，故同一局部状态逆成立。这扩大了静态逆的常场域，仍不是一般场的逆谱定理。

## 3. 完整 Floquet 数据的准确切线接口

定义

\[
C=(Q-R)/(2S),\quad N=Q+\nu C,\quad A_\lambda=N-\lambda C.
\]

C monic 阶 M−1，N monic 阶 M，\(\mathscr L=C^{-1}N\)。令 \(\mathsf T(\lambda)\) 是 monic 标量方程 A_λψ=0 在 x=0 的 companion jet 基 \((\psi,D\psi,\ldots,D^{M-1}\psi)\) 中的完整单值矩阵。固定基点和该归一化，不能只保留矩阵的共轭类。

若 Φ_x=𝔅_λΦ、Φ(0)=I，𝔅_λ 为 companion 矩阵，则直接微分积分方程得

\[
\delta\mathsf T=\mathsf T\int_0^L\Phi^{-1}\delta\mathcal B_\lambda\Phi\,dx. \tag{1}
\]

对一个简单 Floquet 倍子 μ_a，取左右特征向量 ℓ_a、r_a，ℓ_ar_a=1；令 v_a(x)=Φ(x)r_a、u_a(x)=ℓ_aΦ(x)^{-1}。则

\[
\boxed{\quad\delta\log\mu_a=\int_0^L
u_a(x)\,\delta\mathcal B_\lambda(x)\,v_a(x)\,dx.\quad} \tag{2}
\]

u_a、v_a 的相反 Floquet 倍子相消，积分核周期。𝔅_λ 的系数由物理场有限 jets 给出，分部积分即可得到原自由场坐标中的光滑梯度及零均值投影。因此 (2) 给一个可直接计算的 squared-eigenfunction 协向量入口；没有借用未核实的周期逆谱定理。

若对所有非碰撞 λ 知道全部 Floquet 倍子及它们在固定 companion 基中的全部项目特征线，则可由

\[
\mathsf T(\lambda)=V(\lambda)\operatorname{diag}(\mu_a(\lambda))V(\lambda)^{-1}
\]

恢复完整矩阵；列缩放不影响该式。碰撞处由解析延拓恢复。这里的“全部基点特征线”明确包含 norming/连接信息。它不能直接替换成尚未定义和验证的一个 divisor 符号；也不能只给谱曲线的特征值就使用本节的有框架逆。

### 3.1 全 M 均匀共振的精确位置

均匀 b_j=B、d_j=δ 时，写 y=z−B：

\[
Q_0(z)=(y+\delta)^M,\quad R_0(z)=(y-\delta)^M,
\quad C_0(y)=\frac{(y+\delta)^M-(y-\delta)^M}{2S},
\]

\[
\lambda(y)=B+S\frac{(y+\delta)^M+(y-\delta)^M}
{(y+\delta)^M-(y-\delta)^M}. \tag{3}
\]

给定非零空间 Fourier κ=2πin/L，Floquet 共振要求两个空间指数相差 κ，即 λ(y+κ)=λ(y)。置

\[
W=y^2+\kappa y-\delta^2,\qquad u=W-\kappa\delta,\quad v=W+\kappa\delta.
\]

在有限、非 pole 点，这等价于

\[
\boxed{\quad v^M-u^M=0.\quad} \tag{4}
\]

κδ≠0 排除单位根 1，故令 ζ_r=e^{2πir/M}、r=1,…,M−1，可得

\[
W_r=\kappa\delta\frac{\zeta_r+1}{\zeta_r-1}
=-i\kappa\delta\cot(\pi r/M),
\]

\[
y_{r,\pm}=-\kappa/2\pm
\sqrt{\kappa^2/4+\delta^2-i\kappa\delta\cot(\pi r/M)}. \tag{5}
\]

通常是 2(M−1) 个不同空间共振点。对下述简单采样图，准确条件为：(i) 各平方根内量非零；(ii) 每个点 C_0(y)≠0。第二条件排除 λ=∞ 的内部通道共振。有限共振不在两标记值 B±S：那里所有空间根分别等于 ±δ，不能相差非零 κ。又 (3) 是 Möbius∘M 次幂∘Möbius，全部空间分歧仅在这两个标记值，因此有限非标记 A_λ 的空间根都是简单的。

在中心化的波时间中，两指数的增长率差为 Ω=−κ(2y+κ)。取 κ=ik，则 (5) 给

\[
\boxed{\quad\Omega^2=k^4-4\delta\cot(\pi r/M)k^3-4\delta^2k^2.\quad} \tag{6}
\]

恢复背景对流后是 −2iBk±√右端。因为 4δ=hc/2、4δ²=h²c²/16，它逐通道等于原 DLW 的真实线性化色散。这证明本共振通道来自原物理场，而非另一个 unconstrained AKNS 系统。

### 3.2 由共振单值矩阵变分恢复原 Fourier 模态

写物理变分为 δb_j=e^{κx}α_j、δd_j=e^{κx}β_j，Σα_j=Σβ_j=0。精确有序乘积变分给

\[
\delta P=e^{\kappa x}\frac{-2\mathsf H_\kappa(y)}
{(y+\kappa+\delta)^M(y+\delta)^M},
\]

\[
\mathsf H_\kappa(y)=\sum_{j=0}^{M-1}(\delta\alpha_j+y\beta_j)
v^{M-1-j}u^j,\qquad \deg\mathsf H_\kappa\le2M-3. \tag{7}
\]

令 f_κ(y) 为 \(\delta A_{\lambda(y)}e^{zx}=e^{(z+\kappa)x}f_\kappa(y)\) 的系数。从 \(\delta\mathscr L=C_0^{-1}(\delta N-\delta C\mathscr L_0)\) 与 Möbius 变分直接相消得到

\[
\boxed{\quad f_\kappa(y)=-\frac{\mathsf H_\kappa(y)}{S C_0(y)}.\quad} \tag{8}
\]

此式在 λ(y) 有限处成立，不仅在共振处。特别是在共振 λ_*，令 a、b 两个空间根为 z_a=B+y、z_b=z_a+κ。以背景指数 jet 向量 v(z)=(1,z,…,z^{M−1}) 组成矩阵 E，得到背景 companion 的指数基。monic 多项式 A_{λ_*} 的左 eigenvector 最后分量是 1/A'_{λ_*}(z_b)，所以 (1) 给

\[
\boxed{\quad
(E^{-1}\delta\mathsf T(\lambda_*)E)_{ba}
=-\frac{L e^{z_aL}}{A'_{\lambda_*}(z_b)}f_\kappa(y).
\quad} \tag{9}
\]

一般扰动含所有 Fourier 模态时，右边仍只采样指定 κ：积分因子为 e^{(κ_l−κ)x}，其他整数 Fourier 模态积分为零。初始 jet 基固定；无需扰动特征向量在碰撞点可微这一错误前提。

由 (8)–(9)，完整有框架 Floquet 数据给 \(\mathsf H_\kappa\) 在 2m=2(M−1) 个不同点的值。次数至多 2m−1，故 Vandermonde 插值恢复该多项式。再用旧的反射恒等式（W 保持于 y↦−κ−y）恢复两组 α、β。其系数映射行列式为

\[
(-1)^{m(m-1)/2}\delta^m(2\kappa\delta)^{m(m+1)}\ne0.
\]

因此在上述简单采样条件对全部非零 Fourier 模态成立时，**物理场→完整 companion Floquet 单值矩阵函数的 Frechet 微分在均匀固定均值叶上单射，并有逐 Fourier 的明确反演。** 零 Fourier 模态由固定组件均值排除。本结论未给统一 Sobolev/tame 逆估计；微分单射也不能推出非线性局部逆谱。

若 (5) 有重根，需要 confluent 采样和 λ 导数；若 C_0=0，需要 λ=∞ 的 holonomy 数据。当前 (9) 的简单 Vandermonde 证明不覆盖这些例外，不能静默略去。它们是方法需要另补的谱图，不是一般物理不可积性的结论。

## 4. 线性化层级能分离全部非退化通道

已独立核对的原物理谱迹流为

\[
X_{C_n}\mathscr L=[Q_n,\mathscr L],\qquad
Q_n=\frac1{8G}\big[\mathscr L^{n+1}-2B\mathscr L^n
+(B^2-S^2)\mathscr L^{n-1}\big]_+,\quad G=2S.
\tag{10}
\]

平移动量给 \(X_{P_{\rm mom}}\mathscr L=-[D,\mathscr L]\)。均匀点这些物理 Hamilton 场本身全为零；但它们的线性化并不为零。

均匀 Q_n^0 是 D 的常系数多项式，次数 n+1，最高系数 1/(8G)。Q_1^0,Q_2^0,…，加 D 和常数，按次数为三角基，因此张成所有有限次多项式。线性化 (10) 在一个共振 y 上，项 [δQ_n,𝓛_0] 因 λ(y+κ)=λ(y) 消失，故

\[
\partial_{t_n}\mathsf H_\kappa(y)
=\big[Q_n^0(B+y+\kappa)-Q_n^0(B+y)\big]\mathsf H_\kappa(y). \tag{11}
\]

所有采样通道因此同时对角化。

对固定 κ，将每个共振根 y 连边到 y+κ。根不同且 κ≠0；这种有限图是若干条步长 κ 的路径，不可能有环。可沿每条路径给节点指定多项式值，使每条边差任意指定。节点数至多 4m；普通多项式插值取次数至多 4m−1 即可实现。由 (10) 的三角基，有限个 C_n 与 P_mom 的线性组合实现相同边差。

这证明：**在单个非退化非零 Fourier 模态上，复杂化的线性化 commuting hierarchy 具有全部 2m 个独立通道频率；不存在一个该图中所有层级线性化都看不到的物理 Fourier 方向。** 加共轭模态并施加相容条件得到真实场结论。对多个 κ 的有限集合，只要其共振边图无环，同样可插值；若出现更高 Floquet 碰撞形成环，边差有相容关系，不能再任意赋值。

这里用的是均匀点 Hamiltonian Hessian 的线性作用。没有证明插值系数随模态数增加的统一控制，也没有证明非线性等谱叶由这些实际 Hamilton 流充满。有限块频率分离与无限维拓扑闭包仍须区分。

### 4.1 指数权重下可以证明的全频线性闭包

上述尾部问题有一个可直接证明的条件式答案。令 k_0=2π/L，增加明确的小均匀背景条件

\[
\boxed{\qquad 0<|\delta|<\frac{k_0}{2}\tan\frac{\pi}{2M}.\qquad} \tag{15}
\]

对所有 k=nk_0，(5) 的平方根内实量满足

\[
\delta^2-k^2/4+k\delta\cot(\pi r/M)<0.
\]

这是因为最大的 cot 是 cot(π/M)，其正根界
\((\sqrt{1+\cot^2(\pi/M)}-\cot(\pi/M))/2=\tan(\pi/(2M))/2\)。因此全部共振空间点 y=iξ 都在虚轴且互异。

本条件还排除节点重叠和 λ=∞ 别名。若 λ−B 纯虚，(3) 的 M 个 t=(y−δ)/(y+δ) 根都在单位圆，其半角 θ_j 等间距 π/M，空间根为 y_j=iδcot θ_j。至多一个 θ_j 离 πZ 小于 π/(2M)；其余满足

\[
|\xi_j|\le |\delta|\cot(\pi/(2M))<k_0/2.
\]

故除了至多一个 fast 根，全部根在同一严格宽度小于 k_0 的内部区间。两内部根不可能相差非零整数 k_0；fast 根也不能同时与两个内部根共振，否则这两个内部根之差为非零整数 k_0。任何有限 Floquet 碰撞因此仅有一条 fast–inner 边。不同 λ 的边不可能共享空间点，因为 λ(y) 单值。λ=∞ 的 C_0 根也全在这个内部区间，不能出现非零 Fourier 别名。

取全部 n>0、r、± 的边 e=(iξ_a,iξ_b)，避免反向重复；这些边的全部端点互不相同。令 R_e=max(|ξ_a|,|ξ_b|)，正权重满足

\[
0<w_e\le C e^{-2\sigma R_e},\quad \sigma>0,
\qquad \mathcal H_w=\{\Omega:\ \sum_e w_e|\Omega_e|^2<\infty\}.
\]

因为 R_e≥nk_0/2，每个 n 只有 2m 条边，所有多项式边差
\(\Omega_e^p=p(i\xi_b)-p(i\xi_a)\) 属于此 Hilbert 空间。它们的复杂线性张成在 𝓗_w 中**稠密**。

证明如下。若 f∈𝓗_w 与全部多项式边差正交，令 d_e=w_e\overline{f_e}。对任意 0<ε<σ，Cauchy–Schwarz 给

\[
\sum_e |d_e|e^{\epsilon R_e}
\le \|f\|_{\mathcal H_w}
\left(\sum_e w_e e^{2\epsilon R_e}\right)^{1/2}<\infty.
\]

因此有限复杂测度
\(\mu=\sum_e d_e(\delta_{\xi_b}-\delta_{\xi_a})\)
有指数绝对矩。正交性给其全部多项式矩为零。Fourier 变换

\[
\widehat\mu(t)=\sum_e d_e(e^{it\xi_b}-e^{it\xi_a})
\]

在 |Im t|<ε 解析；所有 t=0 的导数为零，故在整条实轴为零。有限测度的 Fourier 唯一性可由与 Gaussian 卷积并令 Gaussian 宽度趋零直接证明，于是 μ=0。每个端点只属于一条边，即便内部端点有积聚，单点原子质量仍等于 ±d_e，故全部 d_e=0，进而 f=0。Hilbert 正交判据给所需稠密性。

由 (10) 的三角多项式基，同一稠密性适用于**谱迹与 P_mom 的线性化通道频率**。若权重对实型配对对称，在满足 \(\Omega_{e'}=-\overline{\Omega_e}\) 的真实子空间，可把多项式系数共轭对称化得到对应的实稠密性。

也可选 w_e 为某个非零指数衰减背景变分的通道幅度平方和。该判据会给该变分处 diagonal 线性层级方向的闭包；但是要称它为原物理 Hilbert 叶的线性最大各向同性，还需证明通道变换的有界性、反向边的辛配对常数及此权重对应的物理拓扑。**这里完成的是一个全频、明确权重的线性频率闭包，不是非线性作用量最大性。** 对不满足 (15) 的背景、仅多项式下降权重或未处理的谱碰撞图，不能援用本段的指数矩唯一性。

## 5. 物理 Poisson 商可保留；极大性的真正余项

自由場 z=(q,d) 的准确无权张量与逆为

\[
J_0=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix},\qquad
W_0=-16\begin{pmatrix}0&D^{-1}\\D^{-1}&0\end{pmatrix}
\]

（每块为 m×m，D^{-1} 是各分量零空间均值的周期逆）。旧稿从 p,s 到 q,d 的变换为可逆仿射变换；h 加权与无权配对的常数一致。对前 2m 个系数的实际像 F、逆 G，设 A=DF、B_y=DG，则 B_yA=I；像上

\[
J_\mathcal Y\alpha=A J_0(A^*\alpha),\qquad
\omega_\mathcal Y(v,w)=\langle W_0B_yv,B_yw\rangle. \tag{12}
\]

对光滑 ambient 数组代表要写 A* 后的零均值投影；核恰为实际切空间的 conormal。一般像上的允许协向量由源拉回有光滑 L² 代表定义，不能无证声称 A* 对指定的光滑 ambient 数组满射。取非零 η=B_yv、w=A W_0η，便有

\[
\omega_\mathcal Y(v,w)=\|W_0\eta\|_{L^2}^2>0.
\]

因此静态完整物理像的弱辛性证明成立。该伙伴 w 不必属于任意实际混合中心子像；不能仅凭 (12) 替代后者的辛证明。

对于已证明对合的 I_α，真正的极大性判据仍为

\[
\overline{\operatorname{span}\{J_0a_\alpha\}}
=\bigcap_\alpha\ker\langle a_\alpha,\cdot\rangle,
\qquad a_\alpha=\mathcal P_xF^*\delta I_\alpha, \tag{13}
\]

闭包须指定同一物理拓扑；P_mom 应单独纳入。谱对合只给左边包含于右边。

### 5.1 均匀点的准确奇异性

固定均值叶上，任意局部谱迹 C_n 的均匀梯度是空间常数，故其微分为零；P_mom 的微分也为零。更强地，对所有简单 Floquet 倍子，(2) 在均匀背景只积分非零 Fourier 变分，因此 δμ_a=0。特征多项式的变分在非碰撞 λ 恒为零，解析延拓使其在碰撞 λ 也为零。

所以**全部不带 norming 的 Floquet 特征值数据，在该均匀固定均值叶上一阶都不观测任何物理方向**；完整有框架矩阵的 (9) 却忠实观测这些方向。两者并不矛盾：闭合谱隙处角/norming 信息和二阶谱变化决定态恢复。

在此点，由这些作用型积分的一阶 Hamilton 场形成的 V=0，而 V^ω 是整个非零切空间。故不能宣称 (13) 在包括均匀点的所有物理场上成立。一个正确 Liouville 定理可以具有奇异集合，但必须明确其正则集、closed-gap 的 Cartesian 坐标和结论类型。第 4 节的 Hessian 分离不消除这一一阶奇异性。

### 5.2 完整谱梯度与局部谱迹的连接仍须证明

大参数标量分支有形式展开

\[
\log\mu_{\rm fast}(\lambda)=\lambda L-
\sum_{n\ge1}C_n\lambda^{-n}.
\]

它的形式系数来自真正有限微分泛函，但目前没有证明该渐近级数收敛、唯一确定全部 Floquet 分支，或使所有 (2) 的谱协向量落入 trace 协向量的可控闭包。m 个内部通道的 holonomy、连接数据和 divisor 相位不能从一个形式展开的名字中自动删除。具有同一渐近级数的函数可差指数小项，这只是逻辑提示，不能未经构造当作 DLW 物理反例。

由 (2) 拉回后的光滑协向量记 a_λ。在原物理坐标中，新 Floquet 积分是否对合可直接审计

\[
\{I_\lambda,I_\eta\}_{\rm phys}
=-\frac1{16}\int\big[(a_\lambda)_qD(a_\eta)_d
+(a_\lambda)_dD(a_\eta)_q\big]dx. \tag{14}
\]

局部形式迹的对合证明没有自动证明任意有限 λ 的非局部 Floquet 泛函满足 (14)=0；必须另证其可容许梯度、因子共轭不变性及周期零模。即使 (14) 完成，也仍要证明 (13) 的反向包含。

## 6. 后续可实行的证明任务

第一步可从 (1)–(9) 建立完整有框架 Floquet 变换的高频估计。需要证明逐 Fourier 插值逆在某个明确 Sobolev/分级尺度中有可控损失，并处理重根共振与 λ=∞ 的 confluent/holonomy 图。只有微分单射不够；非线性局部逆需要实际谱像约束、连续性估计和对应逆构造。

第二步把谱数据拆成原物理叶上的守恒谱参数和规范化角/norming 数据。应保留两个标记值 B±S 的有序均值约束、共同平均 χ 的动量依赖、内部 holonomy 和真实场实型。若用 divisor，须具体给出与基点特征线之间的重建及归一化；不能以标准 periodic AKNS 定理替代。

第三步用 (2)、(12)、(14) 推导这些数据的物理括号，再以第 4 节的全部通道分离为线性起点证明正则集上的 (13)。必须给出无限模态闭包估计和实际辅助流切向/存在性，不能只列任意有限块独立。

最后把该静态谱构造放到与原物理时间共同合法的真实相空间。原高频 e^{tk²} 障碍仍排除均匀点附近通常 Sobolev/C∞ 开集上的可微正时间流；新的 Floquet 切线逆没有改变这个事实。实际混合中心域、谱加权序列域或其他明确的解空间需要与本稿物理 Poisson 叶逐项接合。

目前结论是：局部系数状态逆的关键依赖可独立补齐，并能扩大到跨根分离的实常场；完整 Floquet/norming 数据已获得全 M 的明确忠实切线恢复与线性化层级通道分离。完整非线性逆谱、正则作用角的物理括号、最大各向同性及共同实际解流仍未证。因此本稿不宣称一般物理场的完整 Liouville 定理已完成。

## 7. 完整 framed 共振通道的原物理辛配对

本节继续采用 (15)，固定均匀背景 b_j=B、d_j=δ，S=Mδ≠0；k=nk_0>0，κ=ik，θ_r=πr/M，r=1,…,m=M−1。以下都是该实际物理叶的切空间恒等式。新结论补上 §3–6 当时留下的全频有界性与物理辛匹配，未使用任意矩阵 Darboux 定理代替计算。

### 7.1 从原 J 到共振分子配对

物理均匀背景的非零 Fourier 扰动写为

\[
\delta b_j=e^{\kappa x}\alpha_j,\qquad
\delta d_j=e^{\kappa x}\beta_j,\qquad
\sum_j\alpha_j=\sum_j\beta_j=0.
\]

此时 α=p/2、β=hs/8，其中 p=P_0δU、s=δw。原普通积分梯度下 p,s 的核为 −P_0D/h，因此

\[
\{\alpha_j(\kappa),\beta_l(-\kappa)\}
=-\frac{\kappa}{16L}(P_0)_{jl}.
\tag{16}
\]

空间 Fourier 系数的归一化为 L^{-1}∫；格点 DFT 不除以 M，定义

\[
\widehat\alpha_r=\sum_{j=0}^{M-1}\zeta_r^{-j}\alpha_j,
\quad\widehat\beta_r=\sum_j\zeta_r^{-j}\beta_j,
\quad\zeta_r=e^{2\pi ir/M}.
\]

于是

\[
\{\widehat\alpha_r(\kappa),\widehat\beta_s(-\kappa)\}
=-\frac{M\kappa}{16L}\,\mathbf1_{s=M-r}.
\tag{17}
\]

对正 k，实物理切空间上的精确原辛形式也可直接写为

\[
\omega_0=-\sum_{n>0,r}\frac{16L}{M\kappa}
\left(d\widehat\alpha_r\wedge d\overline{\widehat\beta_r}
+d\widehat\beta_r\wedge d\overline{\widehat\alpha_r}\right).
\tag{18}
\]

该式为实双线性形式，等价于 §5 的 ⟨W_0v,w⟩；所有常数使用同一普通积分约定。

记

\[
\tau_r=\sqrt{k^2/4-\delta^2-k\delta\cot\theta_r}>0,
\qquad y_{r,\pm}=-ik/2\pm i\tau_r.
\]

在 (7) 的共振点，u/v=ζ_r、Σ_jv^{m-j}u^j=0，故

\[
\mathsf H_\kappa(y_{r,\pm})
=v_{r,\pm}^{m}
\bigl(\delta\widehat\alpha_r+y_{r,\pm}\widehat\beta_r\bigr).
\tag{19}
\]

这给出每个 κ 的明确 2m×2m 块矩阵：对每个 r，样本 (H_+,H_-) 等于

\[
\begin{pmatrix}v_+^m\delta&v_+^my_+\\
v_-^m\delta&v_-^my_-\end{pmatrix}
\begin{pmatrix}\widehat\alpha_r\\\widehat\beta_r\end{pmatrix}.
\]

两行独立，因为 δ(y_-−y_+)≠0。它是先前 Vandermonde 逆的更直接 DFT 分块形式。

反向共振为 (−κ,y+κ)，其 u,v 交换。由 (16) 的几何级数求和，得到

\[
\boxed{\quad
\{\mathsf H_\kappa(y),\mathsf H_{-\kappa}(y+\kappa)\}
=-\frac{M\kappa\delta(2y+\kappa)(uv)^m}{16L}.
\quad}\tag{20}
\]

其余反向共振配对全为零。若根比不是 ζ_r^{-1}，格点求和为零；若根比相同但选另一空间根，则该根为 −y，因 y+(−y)=0 而消失。这同时证明 ±κ 配对与所有 r 的对角化，不只是对固定有限块作形式逆矩阵。

### 7.2 从 δT 直接获得精确辛权重

沿用 (9) 的固定 companion 框架，定义线性共振坐标

\[
c_\kappa(y)=e^{-(B+y)L}
(E^{-1}\delta\mathsf T(\lambda(y))E)_{ba}.
\tag{21}
\]

它是背景处 δT 的线性函数，尚不声称其非线性延拓具有下面的常数括号。背景根上有

\[
C_0(y)A'_{\lambda(y)}(B+y)=(y^2-\delta^2)^m.
\tag{22}
\]

证明：写 Λ=λ−B，A_λ=[(S−Λ)(y+δ)^M+(S+Λ)(y−δ)^M]/(2S)，使用 A_λ(y)=0 和 S=Mδ 即得 (22)。将 (22) 代入 (8)–(9)，共振根比关系进一步给出

\[
\boxed{\quad
c_{r,\pm}=\frac{L}{S}
\frac{y_{r,\pm}+\kappa+\delta}{y_{r,\pm}+\delta}
\bigl(\delta\widehat\alpha_r+y_{r,\pm}\widehat\beta_r\bigr).
\quad}\tag{23}
\]

因此 monodromy 归一化恰好消去了 H 中随 M 增大的分母幂。正反向两个比例因子的乘积为 L²/[S²(uv)^m]；与 (20) 合并得到

\[
\boxed{\quad
\{c_\kappa(y),c_{-\kappa}(y+\kappa)\}
=-\frac{L\kappa(2y+\kappa)}{16S}.
\quad}\tag{24}
\]

全部其他通道配对为零。实型满足 c_{-κ}(y_++κ)=\overline{c_κ(y_-)}；格点反向编号为 M−r。故

\[
\{c_{r,+},\overline{c_{r,-}}\}=K_r,
\qquad K_r=\frac{Lk\tau_r}{8S},
\tag{25}
\]

不同 (n,r) 的括号为零。

### 7.3 正则 Cartesian 坐标与全频半阶估计

定义

\[
Q_{nr}=\frac{k^{-1/2}c_{r,+}}{\sqrt{|K_r|}},\qquad
P_{nr}=\frac{\operatorname{sgn}(S)k^{1/2}\overline{c_{r,-}}}
{\sqrt{|K_r|}}.
\tag{26}
\]

则 {Q,P}=1、{\bar Q,\bar P}=1，其余交叉括号为零。原物理辛形式正好是

\[
\boxed{\qquad\omega_0=2\operatorname{Re}
\sum_{n>0,r}dQ_{nr}\wedge dP_{nr}.\qquad}\tag{27}
\]

取 q_1=√2ReQ、p_1=√2ReP、q_2=√2ImQ、p_2=−√2ImP，则每个 (n,r) 为两对实正则坐标。固定 κ 有 2m 个复物理维度；正 k 与实型合并为 4m 个实维度。

这里存在统一全频估计。令 R_±=(y_±+κ+δ)/(y_±+δ)、D_±=(L/S)R_±，从 (23)–(26) 得

\[
\begin{pmatrix}Q\\\bar P\end{pmatrix}
=\mathcal H_{nr}\begin{pmatrix}\widehat\alpha_r\\\widehat\beta_r\end{pmatrix},
\quad
\mathcal H_{nr}=\frac1{\sqrt{|K_r|}}
\begin{pmatrix}
k^{-1/2}D_+\delta&k^{-1/2}D_+y_+\\
\operatorname{sgn}(S)k^{1/2}D_-\delta&
\operatorname{sgn}(S)k^{1/2}D_-y_-
\end{pmatrix}.
\tag{28}
\]

严格阈值 (15) 给 τ_r≍k；y_+ 一致有界，|R_+|≍k、|R_-|≍k^{-1}。根关系给精确 R_+R_-=ζ_r^{-1}，因此

\[
\det\mathcal H_{nr}=-\frac{16iL\zeta_r^{-1}}{Mk}.
\tag{29}
\]

矩阵 √k H 的全部元素一致有界，其行列式固定非零；其逆也一致有界。于是

\[
|Q_{nr}|^2+|P_{nr}|^2\asymp
k^{-1}\bigl(|\widehat\alpha_r|^2+|\widehat\beta_r|^2\bigr).
\tag{30}
\]

常数依赖固定 M,L,δ 与阈值余量，不依赖 n,r。因此实际物理切空间 H^s 与正则序列 h^{s+1/2} 之间有有界实线性同构；指数空间权重 e^{2σk} 同样保持，并附加半阶提升。共振 fast 端点 R_e=k+O(1)，故 §4.1 的端点指数权重与 Fourier 指数权重相容。

记 t=s+1/2。t≥0 时 (27) 在 h^t 上连续；t=0 是这个**线性切空间 Hilbert 完成**的强辛形式，t>0 是弱辛形式。弱非退化由有限模态测试直接成立；t>0 时从空间到连续对偶的辛映射不是满射。指数权重与下面的 Fréchet 空间仍为弱辛。s=−1/2 的负 Sobolev 完成仅用于线性切空间，并没有定义相应非线性 Lax 图。

## 8. 线性二次作用角与全部 C_n 的全频最大性

每个通道定义复二次不变量 I_e=Q_eP_e，以及两项实作用量

\[
A_{1,e}=2\operatorname{Re}I_e,\qquad
A_{2,e}=-2\operatorname{Im}I_e.
\tag{31}
\]

全部对合。Q_e≠0 时选局部 Θ_e=logQ_e，则

\[
\omega_e=2\operatorname{Re}(d\Theta_e\wedge dI_e)
=d\log|Q_e|\wedge dA_{1,e}
+d\arg Q_e\wedge dA_{2,e}.
\tag{32}
\]

Q_e=0、P_e≠0 时用 Θ_e=−logP_e。该式是有限通道或逐通道局部作用角恒等式；没有证明全无限 log 图在某个 Hilbert 开邻域内连续，趋零的 Q_e 会使相对扰动失控。

实多项式 p 的线性流满足

\[
\dot Q_e=\Omega_e^pQ_e,\qquad
\dot P_e=-\Omega_e^pP_e,
\quad\Omega_e^p=p(B+y_++\kappa)-p(B+y_+).
\]

其准确二次 Hamiltonian 为

\[
H_p^{(2)}=2\operatorname{Re}\sum_e\Omega_e^pI_e
=\sum_e\bigl(\operatorname{Re}\Omega_e^p A_{1,e}
+\operatorname{Im}\Omega_e^p A_{2,e}\bigr).
\tag{33}
\]

原 DLW 的线性频率 Ω_K=2kτ_r−2iBk；故原 K 的二次部分为 Σ_e(2kτ_r A_{1,e}−2Bk A_{2,e})。P_mom 的频率是 −ik，其二次 Hamiltonian 为 −Σ_e kA_{2,e}。任意实 Γ(t) 仅给相应 B(t) 的旋转/平移，I_e 保持常数；非中心化谱迹本身的漂移仍须采用根任务的 Γ 中心化公式处理。

现在选实际线性序列拓扑 X_t=h^t，t≥0，及正则序列 η=(Q_e,P_e)：每个通道对不同时为零，并且系数指数衰减。其作用量共同核为

\[
\mathcal L_\eta=\bigcap_e\ker dI_e
=\{v_e=\Omega_e(Q_e,-P_e)\in X_t\}.
\tag{34}
\]

频率到向量的范数是 Σ_e w_e|Ω_e|²，其中 w_e=k^{2t}(|Q_e|²+|P_e|²)>0；指数衰减可吸收多项式权重，满足 §4.1 的条件。L_η 是闭子空间，且

\[
\mathcal L_\eta^{\omega_0}=\mathcal L_\eta.
\tag{35}
\]

证明：L_η 每个通道为复直线，因此各向同性；用仅一个通道支撑的任意复 Ω 测试其辛正交向量，强迫 P_ev_{Q,e}+Q_ev_{P,e}=0，恰好返回 (34)。

这里必须使用**全部 n=1,2,3,… 的 C_n，加 P_mom**。由 (10) 的次数三角性，它们生成所有实多项式差；§4.1 的实型指数矩唯一性则给

\[
\boxed{\quad
\overline{\operatorname{span}_{\mathbb R}
\{(DX_{C_n})_0\eta:n\ge1,\ (DX_{P_{\rm mom}})_0\eta\}}^{X_t}
=\mathcal L_\eta=\mathcal L_\eta^{\omega_0}.
\quad}\tag{36}
\]

因此全 M 小均匀背景的**线性二次 Hamiltonian 系统**已得到原物理辛匹配与全频最大各向同性。这里的 η 是线性模型中的正则点；它不是已经构造了逆谱作用量的原非线性物理场。均匀原场本身的一阶 Hamiltonian 场仍为零，与 §5.1 完全相容。高阶 Hessian 向量在指数衰减 η 处有定义，但不能据此称其在普通 Sobolev 开域上构成共同连续流。

### 8.1 任意有限 all-C 家族的真实物理独立见证

还有一个不依赖非线性逆谱的有限独立结论。范围限于含均匀 p=0、w_j=c 的那张均值叶，即 p_j 的空间均值为零，w_j 的均值为 c；等价 free 坐标均值为 q_j=−2δ(M−1−j)、d_j=δ。这里不把均匀见证移用于其他分量均值叶。

取任意有限组不同 C_n，可另加入 P_mom，B=0 或使用中心化谱迹。对应 Q_n^0 的次数为 n+1，最高系数 1/(8G)，动量为 −D。任何非零实线性组合是非恒定多项式 p。固定一个格点通道 r，沿 k→∞，plus 边的 y_+ 一致有界，而 y_++ik=ik+O(1)；所以 p(y_++ik) 无界，p(y_+) 有界，该组合的共振频率不可能恒为零。有限组频率 profiles 因此实线性独立。

由此存在有限通道集合 E_0，使这些 profiles 在 E_0 的实/虚 evaluation 矩阵满秩。在正则 Cartesian 切线中取 η_e=(Q_e,P_e)=(1,0) 于 E_0，其余为零。根据 (33)，dH_n^{(2)}(η) 在 P_e 的实、虚测试方向正好给这些频率，故有限个二次 Hamiltonian 微分独立。由 (28) 的精确逆与有限 DFT，η 和测试方向都对应真实实值 finite-Fourier 物理切线。

把 η 先送回 free q,d 坐标，取实际状态 z_ε=z_0+εη，保持上述所有独立分量均值；再用 §2 的精确闭合公式恢复 b。每个固定 n 的 residue 只用有限次形式运算与有限阶导数，形式逆的领先系数为固定 −2S≠0；因此这些局部谱迹及 P_mom 在该有限维实变化上实解析。它们在均匀固定均值叶的一阶微分为零，故在固定有限测试方向上的实际 Jacobian 满足

\[
\det\bigl(dI_i(z_\varepsilon)[v_j]\bigr)_{i,j=1}^{N}
=\varepsilon^N\bigl(\det\mathsf H+O(\varepsilon)\bigr),
\qquad\det\mathsf H\ne0.
\tag{36a}
\]

充分小非零 ε 因而给任意指定有限 all-C 家族及动量的**真实物理函数独立见证**。该结论不止是形式有限矩阵样例，但仍然仅为有限家族独立，不证明无限闭包最大性。若要将这条曲线放入某个要求共同真实时间解的非线性 germ 子域，还必须另证该曲线在该子域可容许；本节不把光滑状态函数的定义自动等同于全部辅助流的存在。

## 9. 奇数守恒族与一个动量严格缺少独立相位

本节取 B=0，或先将任意 Γ 截面的谱层级中心化。均匀背景 L_0(y) 是奇有理函数；于是奇数 n 的 Q_n^0 是偶多项式，而偶数 n 的 Q_n^0 是奇多项式。在纯虚空间节点上，前者的 Ω_e 是实数，后者的 Ω_e 是纯虚数。

奇数 C_1,C_3,… 只能生成 A_1 的 hyperbolic 方向，P_mom 只给频率 −ik 的一个全局 A_2 方向。这个缺失可以精确写成闭包。对 canonical plus 边，ξ_a=τ_r−k/2 满足 |ξ_a|<k_0/2，ξ_b=τ_r+k/2>k_0/2；所有正 fast ξ_b 互异。若实 f∈ℓ²(w) 消灭全部偶多项式差，置 d_e=w_ef_e，构造

\[
\mu=\sum_e d_e\left[
\frac{\delta_{\xi_b}+\delta_{-\xi_b}}2
-\frac{\delta_{\xi_a}+\delta_{-\xi_a}}2\right].
\tag{37}
\]

偶矩全零，奇矩因对称自动全零。指数权重仍给 ξ 变量的解析 Fourier strip，故 μ=0；每个正 fast 原子独有且与所有 inner 原子分离，所以 d_e=0。这证明奇数族稠密生成全部实频率。不能直接将节点平方后套指数矩论证，因为平方后的权重只有 e^{−σ√ρ}；(37) 保留了正确的 ξ 指数矩条件。

令 T_ηΩ=Ω_e(Q_e,−P_e)，得到准确的实闭包

\[
\boxed{\quad
\mathcal V_{\rm odd+mom}
=T_\eta\{a_e+ick_e:
a\in\ell^2(w;\mathbb R),\ c\in\mathbb R\}.
\quad}\tag{38}
\]

全局 ik 序列属于此 ℓ²(w)，其一维实线闭合；所以不能通过无限组合动量得到独立逐模态相位。

显式缺失向量可以取偶数谱迹 C_2。均匀 L_0 的 D^{-1} 系数为 (M²−1)δ²/3，因而对所有 M≥2，

\[
Q_2^0=\frac{D^3-\delta^2D}{8G},\qquad
\Omega_e^{C_2}
=\frac{ik}{8G}\bigl[-k^2+2\delta^2+3k\delta\cot\theta_r\bigr].
\tag{39}
\]

这里使用 y(y+κ)=δ²+kδcotθ_r；频率不依赖 ± 选择。它是纯虚 profile，并且随 k,r 改变，不能是一个固定实常数乘 ik。故在上述全通道正则 η 处

\[
(DX_{C_2})_0\eta\in
\mathcal L_\eta\subset\mathcal V_{\rm odd+mom}^{\omega_0},
\qquad
(DX_{C_2})_0\eta\notin\mathcal V_{\rm odd+mom}.
\tag{40}
\]

这严格证明 odd+P 在线性二次模型中不是最大各向同性，提供了保留偶数守恒方向的具体动机。该结论不证明一般非线性不可积，也没有把此前 mixed odd-prefix 的实际定义域替换为 all-C 的完整共同非线性域。

## 10. 整个线性层级的共同真实流域与非线性缺口

还可以给所有多项式线性流一个共同实际空间，而不仅逐点计算其生成元。定义实 Fréchet 序列空间

\[
\mathcal E=\bigcap_{N\ge1,\ a\in\mathbb N_{>0}}
\left\{(Q,P):
\sum_e e^{2ak_e^N}(|Q_e|^2+|P_e|^2)<\infty\right\}.
\tag{41}
\]

有限支撑序列及 Q_e,P_e≈e^{−e^{k_e}} 的全活跃序列都属于 E。若 p 是任意固定实多项式，Ω_e^p 至多多项式增长。因此

\[
\Phi_p(t)(Q_e,P_e)
=(e^{t\Omega_e^p}Q_e,e^{-t\Omega_e^p}P_e)
\tag{42}
\]

对每个有限实 t 是 E 上连续线性群，群作用 C∞。证明只需将每个目标权重 e^{ak^N} 与 e^{|tΩ|} 吸收到更强的 e^{a'k^{max(N,deg p)}} 中；任意时间导数额外的多项式因子也由更强权重控制。全部 p 的群两两交换，保持 (27)、I_e 与每个 H_p^{(2)}。H_p^{(2)} 在 E 连续；Ω 连续且弱非退化。任意时间 Γ(t) 的线性平移因子绝对值为一，在相应有限积分时间内也保持该域。

对 η∈E 且每个通道对不同时为零，(34)–(35) 仍成立，且 (36) 的闭包可以取 **E 的完整 Fréchet 拓扑**。证明使用连续泛函分离：L_η 上的任一连续实线性泛函由一个更强加权 Hilbert seminorm 控制，Hahn–Banach 与该 Hilbert 空间的 Riesz 表示给对应 ℓ²(w) 泛函，其中

\[
w_e=e^{2ak_e^N}(|Q_e|^2+|P_e|^2).
\]

η∈E 保证这个 w 仍指数衰减：取同 N、更大的 a' 即得 w_e≤Ce^{−2εk_e}。有限支撑在这些空间及 L_η 中稠密。若泛函消灭全部多项式频率，§4.1 的矩唯一性使该泛函为零，得到 Fréchet 稠密性。奇数族的对称测度证明同样适用，(38)–(40) 在 E 中依然给严格相位缺失。

这是一个共同有定义、可演化的全频**线性 Hamiltonian 层级**。E 是均匀物理切空间的强衰减完成，经 (30) 对应相应物理 Fourier 拓扑。未证明原非线性 DLW 在 E 的开邻域中有共同流，也未证明其非线性谱变换保持这种极强衰减类。

因此截至本次更新，以下依赖仍缺少证明：

1. 完整 framed Floquet / norming / divisor 数据在一般非线性实际物理像上的局部或全局逆，以及统一非线性 tame 估计；(23)–(30) 只解决明确阈值内均匀背景的切线逆与辛权重。
2. 真正非线性作用量与 norming 变量的原物理括号，及其全频坐标图、碰撞图与 holonomy 约束。线性 I_e=Q_eP_e 不能直接认作这些非线性谱作用量。
3. 在指定非线性正则集合与共同实际流域内，全 C_n 与完整非局部谱作用量之间的闭包同一性；本稿只证明线性二次模型的 (36)。只保留奇数族时，连这个背景模型的最大性都不成立。
4. 全部 Γ(t) 分支上的谱中心化、实型与真实流的兼容，以及不满足 (15) 的背景中的实根、重复共振与 λ=∞ 通道。根任务的中心化守恒解决 Γ 漂移，不自动解决后三项。

新独有核验见 [辛配对与全频归一化脚本](../../Workspaces/dlw_recovery_20261011/spectral_symplectic_checks_20261011.py) 及 [对应结果](../../Workspaces/dlw_recovery_20261011/spectral_symplectic_checks_20261011.json)。有限计算核对 (17)、(20)、(22)–(30)、(39) 的算式与高频尺度；全 M 与全频结论来自上述推导，不由有限抽样归纳。

## 11. 非线性 framed 状态逆的下一步与一个明确原始采样障碍

一个自然候选是：固定均匀背景的共振 λ_{r,k} 与 jet 框架，把完整非线性 T(λ_{r,k}) 的相应 off-diagonal 元素用 (26) 归一化，记为 S_raw(z)。它在背景处的微分由 (28)–(30) 给出 H^s→h^{s+1/2} 同构。只有在**另行证明** S_raw 进入同一序列空间且为 C¹，并有该拓扑下统一非线性余项后，才能用 Banach 逆函数定理构造局部非线性 framed 状态逆。线性同构没有自动提供这些前提。

旧原始 M×M 系统已经给出避免高 jet 的合适起点：χ_x=(λP+C)χ，P=d1^T/S、P²=P，其中 P,C 只含物理 b,d；其精确场依赖 splitting T=[d/S,Z] 将领先 P 化为 diag(1,0)，却引入 T^{-1}T_x 的一阶 d_x。该系统确实比高阶 companion 方程适合做一致谱估计，不能仅由它断言采样余项有界。小阈值内 λ_{r,k} 随 k 线性趋向虚无穷，有限 k 没有 C_0=0；Vandermonde 框架的多项式条件数与真实内部 holonomy 的非线性改变仍需处理。

### 11.1 自足 M=2 引理：原始固定框架采样有非零代数尾

取 L=2π、B=0、S=2δ，0<δ<1/2。选真实 free 坐标

\[
q(x)=-S+\varepsilon\sin x,\qquad
d_0(x)=\delta+\varepsilon\sin x,\qquad
d_1(x)=\delta-\varepsilon\sin x,
\quad0<|\varepsilon|<S.
\tag{43}
\]

该曲线保持均匀背景所在均值叶。物理 b 由精确闭合公式恢复，是真实光滑物理场，且可任意接近均匀点；q 从不为零。原精确 M=2 系统为

\[
\phi_x=\lambda\phi+q\xi,\qquad
\xi_x=r\phi+V\xi,
\]

\[
r=\frac{d_0(S-d_0)(2+q/S)-d_{0,x}}{S},
\qquad V=(S-2d_0)(1+q/S).
\tag{44}
\]

所以

\[
V=-\frac{2\varepsilon^2\sin^2x}{S},\qquad
\mu_{\rm slow}(\infty)=e^{\int_0^LVdx}
=e^{-\varepsilon^2L/S}\ne1.
\tag{45}
\]

消去 ξ，或用 q(D−V)^{-1}=(D−V−q_x/q)^{-1}q，获得同一个最简 scalar pencil

\[
\mathscr L=(D-W)^{-1}(D^2-WD-qr),\qquad
W=V+q_x/q,
\]

\[
A_\lambda=D^2-(\lambda+W)D+\lambda W-qr,
\qquad W(0)=-\varepsilon/S.
\tag{46}
\]

均匀背景 A^0_λ=D²−λD+δ²。固定正整数 k 的背景共振为

\[
\lambda_k=i\sqrt{k^2-4\delta^2},\quad
z_s=(\lambda_k-ik)/2,\quad z_f=z_s+ik,
\quad E_0=\begin{pmatrix}1&1\\z_s&z_f\end{pmatrix}.
\tag{47}
\]

对非线性 companion 单值矩阵定义同样的原始样本

\[
c_{+,k}^{\rm raw}
=e^{-z_sL}(E_0^{-1}\mathsf T(\lambda_k)E_0)_{fs}.
\]

背景该元素为零，所以减去 T_0 不改变定义。则

\[
\boxed{\quad
c_{+,k}^{\rm raw}
=\frac{W(0)(e^{\int V}-1)}{\lambda_k}+O(k^{-2}),
\qquad k\to\infty.
\quad}\tag{48}
\]

系数非零，且小 ε 时为 ε³L/S²+O(ε⁵)。

证明不需引用任何逆谱定理。对一般固定光滑周期 q,r,V、q≠0，在物理 first-order 框架手构造周期矩阵

\[
U_N=\begin{pmatrix}1&a_N\\b_N&1\end{pmatrix},
\quad b_N=\frac r\lambda+O(\lambda^{-2}),\quad
a_N=-\frac q\lambda-\frac{q_x+Vq}{\lambda^2}+O(\lambda^{-3}).
\]

取有限多项式 Laurent 级数，使 fast、slow 两列的余差达到 O(λ^{-N})。递推分别来自

\[
\lambda b=r+Vb-b_x-qb^2,\qquad
\lambda a=-q+Va+a_x+ra^2.
\tag{49}
\]

所有系数是有限阶微分表达式；固定光滑场上余差一致。U_N^{-1}AU_N−U_N^{-1}U_{N,x} 等于 diag(λ+qb_N,V+ra_N)+O(λ^{-N})，且 U_N 及逆一致有界。沿纯虚 λ，剩余对角演化的 norm 一致有界，因此 Duhamel 给单值矩阵相应 O(λ^{-N}) 误差。固定背景本征基与原物理框架之间的共轭至多放大 O(k)，故 N≥3 足以支持 (48)，也可取 N=6 同时支持下面更精确的双通道余项；这里没有将未经放大的 physical O(k^{-N}) 直接当成 companion 余项。

把两列的 φ 分量归一为 1，并用 φ_x=λφ+qξ 转回固定 companion jet。slow 列斜率为 W(0)+O(λ^{-1})，fast 列斜率为 λ+qr(0)/λ+O(λ^{-2})；对应对角传播因子分别为 e^{∫V}(1+O(λ^{-1})) 与 e^{λL}(1+O(λ^{-1}))。在 (47) 的背景 E_0 下，slow→fast 换基系数为 W(0)/λ+O(λ^{-2})。共轭对角传播矩阵因而给 off-diagonal 元素

\[
\frac{W(0)}\lambda
\bigl(e^{\int V}-e^{\lambda L}\bigr)+O(\lambda^{-2}).
\]

由于 e^{λ_kL}=1+O(k^{-1})、e^{z_sL}=1+O(k^{-1})，即得 (48)。这也表明首项来自真实 slow holonomy 与背景 resonance/frame 的失配，不是有限 λ pole。

仍用背景 (26) 的归一化，τ=√(k²/4−δ²)、|K|=Lkτ/(8S)，得到

\[
Q_k^{\rm raw}
=-i\sqrt{16S/L}\,W(0)(e^{\int V}-1)
\,k^{-5/2}+O(k^{-7/2}).
\tag{50}
\]

因此当 s≥3/2 时，Q_raw **不属于 h^{s+1/2}**：端点 s=3/2 已出现 Σk^{-1} 发散。源状态 (43) 的 free 坐标是有限 Fourier 和，物理 b 也是有限 Fourier 表达式；任意高 H^s 与 E 都包含它。由此 S_raw 在任何均匀背景 H^s 开邻域（s≥3/2）中甚至不映入拟议同阶目标空间。不能在这些空间直接使用 Banach 逆函数定理，也不能把新的线性半阶同构当作非线性映射的高正则同构。

本例在基点 0 的 q,d,b 数值全部等于背景。旧原始 rank-one 框架到 split 框架的 T(0)，以及 split 到 scalar jet 的 G(0,λ)=[[1,0],[λ,q(0)]]，因此恰为背景矩阵。令固定原始本征框架 E_χ=T_bg(0)G_bg(0,λ)^{-1}E_0，则原始 M=2 monodromy 的归一化 off-diagonal 与上述 companion 样本逐 k 完全相同。只把 ODE 换回不含高 jet 的原始固定框架，不能消除这一尾部。

该障碍不排除在 1/2<s<3/2 的较低空间证明某个真实 C¹ 采样图；也不排除用随场改变的 holonomy/frame/gap 中心、减去足够的高 λ 渐近项，重新构造正确的谱序列图。这里未证明这些修正方案已实现。

独有 [原始框架尾部核验脚本](../../Workspaces/dlw_recovery_20261011/spectral_fixed_frame_tail_checks_20261011.py) 与 [结果](../../Workspaces/dlw_recovery_20261011/spectral_fixed_frame_tail_checks_20261011.json) 直接积分实际物理 2×2 单值矩阵，再通过固定 scalar jet E_0 计算 (48)；有限积分只核验系数与尺度，证明由 (49) 的有限阶构造给出。

### 11.2 可继续推进的具体路线

先在原 M×M rank-one 系统中构造实际 slow holonomy 与 fast 分支的统一高频渐近，明确状态依赖基点框架产生的边界项。对固定 λ_{r,k} 的原始采样，必须给出真实渐近减项及其物理可恢复参数；(48) 已证明只沿用线性 normalizer 不够。另一选择是在低 Sobolev 域中先证明原采样图真正进入 h^{s+1/2}，具有统一 C¹ 余项，再通过可验证的状态依赖渐近提高正则性。

完成这些步骤后才可用 Banach 逆函数定理获得局部非线性**完整 framed 状态逆**。随后还需要在实际 double-Floquet 共振处作 Lyapunov–Schmidt 消元，构造真实 gap 与 norming 的正则 Cartesian 变量，并计算其原物理 Poisson 括号。完整状态逆只保证谱数据忠实，尚不能把 raw off-diagonal 样本认作对合非线性作用量。

最后应把新的谱变量放入承载共同原 DLW 与辅助流的真实域，证明 all-C 的无限闭包及正则最大性。§8.1 的真实有限独立见证、§8–10 的线性最大性与 (48) 的原始采样障碍分别给出可靠起点、应达到的线性检验和必须解决的非线性边界项，三者不能相互替代。

### 11.3 一步真实非线性重整化：去掉首个边界尾并保持背景二阶信息

对 M=2、同一背景及同一均值叶，令 q=−S+u、d_0=δ+v，u,v 均值零，在足够小的 C^R 周期 Banach 球上取 R≥10。q 保持非零。以下是在这个**开 C^R 物理状态域**上的非线性映射引理，并非只对 (43) 的有限参数族观察。

设 m_∞=exp∫V，其中精确

\[
V=-2uv/S,\quad
W=-2uv/S+u_x/(-S+u),
\]

\[
qr+\delta^2=v^2+(\delta^2-v^2)u^2/S^2
+(1-u/S)v_x.
\tag{51}
\]

记 λ_{+,k}=λ_k、λ_{-,k}=−λ_k。正向 c_+ 仍是 (48) 的 slow→fast 样本；c_- 是在 λ_- 的 fast→slow 样本，对应 §7 的 y_-→y_-+ik。有限 normal form 在该 C^R 小球内一致，给

\[
c_{+,k}^{\rm raw}=\frac{W(0)(m_\infty-1)}{\lambda_{+,k}}+O(k^{-2}),
\]

\[
c_{-,k}^{\rm raw}=\frac{(qr(0)+\delta^2)(m_\infty-1)}
{\lambda_{-,k}^2}+O(k^{-3}).
\tag{52}
\]

第二式的符号可直接核查：fixed background 下 slow←fast 的换基系数为 −(qr(0)+δ²)/λ²+O(λ^{-3})，乘 μ_fast−μ_slow 即返回 (52)。R≥10 容许取有限 N=6，控制全部系数及放大后的余项，一致常数只依赖该小球。

分别减去 (52) 两个首项，得到 c_±^{ren}；再用同一个背景 (26) 得到 Q^{ren},P^{ren}。于是统一地

\[
(Q^{\rm raw}_k,P^{\rm raw}_k)=O(k^{-5/2}),\qquad
(Q^{\rm ren}_k,P^{\rm ren}_k)=O(k^{-7/2}).
\tag{53}
\]

这里确实获得非线性序列图的解析性：raw 图是 C^R→h^t 的真实实解析映射，t<2；ren 图是 C^R→h^t 的真实实解析映射，t<3。证明是每个固定参数的 first-order ODE 及固定 jet 变换对 C^R 系数解析，(53) 在一个复 C^R 小球内给一致可求和的序列尾。有限坐标投影因此在相应 h^t 中局部一致收敛，向量值 Cauchy 公式给解析极限。

复化时须使用正反向矩阵元的 holomorphic 延拓，不能直接对复输入写 \bar c_-。例如实场上 \bar c_- 正好等于 λ_+ 的反向上三角元 e^{-z_sL}(E_0^{-1}T(λ_+)E_0)_{sf}，用后者定义 P 的复化；共轭 Q、P 同样用 λ_- 的相应元。四个矩阵元分别 holomorphic，实型限制给所述真实实解析映射。

由 (51)，m_∞−1 从二阶开始，W(0) 与 qr(0)+δ² 从一阶开始；两个渐近减项都从三阶开始。因此 ren 图保留背景 first 与 second jet，保持 §7 的线性辛同构及 §8 的二次层级检验。它去掉了一个真实非线性边界尾，使序列正则性提高一阶。

这个引理尚未给 H^s→h^{s+1/2} 的同阶解析图。这里源是 C^R，微分的像具有远高于 t 的 Fourier 正则性，不能在无限维低阶 h^t 目标上满射；Banach 逆函数定理仍不适用。下一步必须用 Sobolev Fourier/Volterra 估计降低余项所需源导数，或构造完整移动 holonomy/gap/frame 图。本稿已经证明首项重整化与开放物理状态域上的真实解析序列映射，尚未证明完整非线性 inverse Floquet、作用角或 Liouville 完备性。

### 11.4 未校准原始 rank-one 固定框架有更强的低正则障碍

原始 M=2 χ 系统自身只含 b,d：

\[
\chi_x=(\lambda P+C)\chi,
\quad P=S^{-1}\begin{pmatrix}d_0&d_0\\d_1&d_1\end{pmatrix},
\quad C=\begin{pmatrix}b_0&d_0\\-d_1&b_1\end{pmatrix}.
\tag{54}
\]

固定背景原始框架 E_χ=T_bgG_bg^{-1}E_0；实际 split、companion 基点矩阵分别为 T_actual=[d/S,Z]、G_actual=[[1,0],[λ,q(0)]]。写 u_0=u(0)、v_0=v(0)、q_0=−S+u_0，它们与固定背景框架之间的精确 endpoint 共轭为

\[
\mathcal B=G_{\rm bg}T_{\rm bg}^{-1}T_{\rm actual}G_{\rm actual}^{-1}
=\begin{pmatrix}1&0\\
\lambda u_0/q_0-v_0&-S/q_0\end{pmatrix}.
\tag{55}
\]

因此 actual slow 列在固定原始背景本征基中的 fast 混合系数不再是 O(λ^{-1})，而是 u_0/q_0+O(λ^{-1})；相应 slow 分量与换基行列式都以 −S/q_0 为首项。对角传播的共轭直接给

\[
\boxed{\quad
c_{+,k}^{\rm original,raw}
=-\frac{u_0}{S}(m_\infty-1)+O(k^{-1}).
\quad}\tag{56}
\]

取同一真实均值叶的 u=v=εcosx，m_∞=e^{−ε²L/S}，首项非零。背景线性辛归一化于是给

\[
Q_k^{\rm original,raw}
=\sqrt{16S/L}\left[-\frac\varepsilon S(m_\infty-1)\right]
\,k^{-3/2}+O(k^{-5/2}).
\tag{57}
\]

此时任何 s≥1/2 都有 Q_raw∉h^{s+1/2}；端点 s=1/2 的加权平方尾为 Σk^{-1}。源仍是有限 Fourier 的实际物理场。因而在通常使用连续物理系数的低正则 s>1/2 上，也不能对**未校准 endpoint 的原始固定框架**直接使用同阶 Banach 逆函数定理。

实际 T(0)、G(0,λ) 的 endpoint 校准准确恢复 companion 图，消掉 (56) 这个更坏尾；之后仍需处理 §11.1 的 holonomy/frame 尾及 §11.3 的重整化。对 (43) 的 sin 例 u_0=v_0=0，B=I，原始固定框架与 companion 样本完全相同，故不存在这两项障碍相互矛盾的问题。本文未排除 s<1/2 的其他弱空间，也未证明校准后的 1/2<s<3/2 同阶 H^s 图已解析。

独有 [原始 b,d 系统核验脚本](../../Workspaces/dlw_recovery_20261011/spectral_original_frame_tail_checks_20261011.py) 与 [结果](../../Workspaces/dlw_recovery_20261011/spectral_original_frame_tail_checks_20261011.json) 直接积分 (54)，不引入 d_x 或高阶 jet，独立核对 (56) 的常数尾。

本节与 §11.1–11.3 已另行独立审查，见 [fixed-frame 独立审查证书](../../Workspaces/dlw_recovery_20261011/spectral_fixed_frame_tail_independent_audit.md)。

## 12. 实际 M=2 Floquet 双分支点：统一 Sobolev 解析提取与移动 holonomy 中心

本节绕过固定 framed 样本的边界尾，直接提取实际 monodromy 的共轭不变量。得到全频统一的 H^s→c₀ 解析估计、实际双根计数及移动中心，尚未给同阶 H^s→h^{s+1/2} 的完整状态图。独立审查见 [M=2 moving-gap 审查证书](../../Workspaces/dlw_recovery_20261011/spectral_m2_moving_gap_independent_audit.md)。

### 12.1 真正的 Sobolev 物理状态域及统一 Volterra 界

令 k₀=2π/L、0<|δ|<k₀/2、S=2δ，取 B=0（一般 B 先采用 centered 参数）。使用 §11 的同一实际 free 源均值叶

\[
X_s=\{(u,v)\in H^s_{\rm per}(\mathbb C)^2:\int u=\int v=0\},\qquad s\ge1.
\tag{58}
\]

实型限制为原物理实场。q=−S+u、d₀=δ+v、d₁=δ−v，闭合给 b₁=−d₀u/S、b₀=b₁+u。split 系统精确为

\[
Y_x=A_\lambda(z)Y,\quad Y(0)=I,\quad
A_\lambda=\begin{pmatrix}\lambda&q\\r&V\end{pmatrix},
\quad V=-2uv/S,
\quad r=\frac{(\delta^2-v^2)(1+u/S)-v_x}{S}.
\tag{59}
\]

H^s 是乘法代数，v_x∈L²⊂L¹；因此 z↦(q,r,V) 是 X_s→(L¹)^3 的复解析多项式，源球内各阶微分一致有界。原 rank-one 系统到 split 的周期变换由 d 构成、行列式恒定非零；H¹ 函数的绝对连续代表足以使变换及 (59) 在几乎处处意义成立。因此 T(λ,z)=Y(L) 是原物理 monodromy 的基点共轭。这里不必除以 q，也不必先要求 q 无零点。

对任意固定竖条 |Re λ|≤R_λ，去掉 diag(λ,0) 的传播子。Volterra 系列的 n 阶项由 C^n/n! 控制，C 只依赖源球、L、R_λ，与 Im λ 无关。于是 T 的源解析性不是仅逐频成立：在该竖条的有界矩阵函数 Banach 空间中，T 是复解析映射，并在较小源球上满足

\[
\sup_\lambda\|T(\lambda,z)\|\le C,\quad
\sup_\lambda\|D_zT(\lambda,z)h\|\le C\|h\|_{H^s},
\]

\[
\sup_\lambda\|T(\lambda,z+h)-T(\lambda,z)-D_zT(\lambda,z)h\|
\le C\|h\|_{H^s}^2.
\tag{60}
\]

这是实际 Sobolev 输入上的统一非线性估计。证明只用 L¹ 系数、乘法界及可求和 Dyson 项，没有使用 C^R 高 jet 或高频本征框架。

### 12.2 同一圆盘中的实际双根与准确半 gap 平方

记 A(z)=∫₀ᴸV。L¹ Liouville 公式给 detT=e^{λL+A}，故实际判别式

\[
\mathscr D(\lambda,z)=\frac{(\operatorname{tr}T(\lambda,z))^2}{\det T(\lambda,z)}-4
=e^{-\lambda L-A(z)}(\operatorname{tr}T)^2-4
\tag{61}
\]

对周期 gauge 共轭不变，其零点正好表示实际两个 Floquet 乘子相等。背景为

\[
\mathscr D_0(\lambda)=4\sinh^2\!\left(\frac L2\sqrt{\lambda^2-4\delta^2}\right).
\tag{62}
\]

这是 λ 的整函数，平方根表达不要求全局选支。令 k_n=nk₀、ω_n=√(k_n²−4δ²)、λ_n=iω_n。λ_n 与 −λ_n 是二重零点；另有 ±2δ 的简单零点。可取

\[
0<\rho<\min(k_0/4,\omega_1/2).
\tag{63}
\]

正侧相邻中心间距大于 k₀，反侧最近距离为 2ω₁，λ_n 到 ±2δ 的距离等于 k_n，故每个 |λ−λ_n|<ρ 圆盘仅含其背景二重零点。且一致地

\[
\mathscr D_0(\lambda_n+\zeta)\longrightarrow4\sinh^2(L\zeta/2)
\quad (|\zeta|=\rho),
\qquad \inf_{n,|\zeta|=\rho}|\mathscr D_0|=\gamma>0.
\tag{64}
\]

背景的一阶源变化对全部 λ 为零。确实 δq=h_u、δr=δ²h_u/S²−(h_v)_x/S、δV=0，全部均值为零；常系数背景及 cyclic trace 给

\[
\delta\operatorname{tr}T_0
=\operatorname{tr}\!\left(e^{A_0L}\int_0^L\delta A\,dx\right)=0,
\qquad D_z\mathscr D(\lambda,0)=0.
\tag{65}
\]

由 (60)，一个与 n 无关的小复源球可使 |𝒟−𝒟₀|≤C||z||²<γ/2；Rouché 定理在每个圆盘内给恰好两个实际零点，按重数计。记其移位为 ζ_{n,1},ζ_{n,2}，定义

\[
a_n=\frac{\zeta_{n,1}+\zeta_{n,2}}2,
\qquad g_n=\frac{(\zeta_{n,1}-\zeta_{n,2})^2}{4}.
\tag{66}
\]

实际中心为 λ_n+a_n；g_n 是 **半 gap 的平方**，完整 gap 平方为 4g_n。有序根未必解析，(66) 的对称组合解析。

圆周上令 R_n(ζ,z)=𝒟(λ_n+ζ,z)/𝒟₀(λ_n+ζ)，统一取接近 1 的 log 分支。argument principle 与分部积分给无任何 λ_n 大幂的精确公式

\[
a_n=-\frac12\frac1{2\pi i}\oint_{|\zeta|=\rho}\log R_n\,d\zeta,
\qquad
g_n=-\frac1{2\pi i}\oint_{|\zeta|=\rho}\zeta\log R_n\,d\zeta-a_n^2.
\tag{67}
\]

统一 Volterra 解析界与 log 的一致收敛级数使 z↦(a,g) 成为 X_s→ℓ∞×ℓ∞ 的真正 Banach 复解析映射。在较小源球上

\[
\|(a,g)(z)\|_\infty\le C\|z\|_{H^s}^2,\qquad
\|D_z(a,g)(z)h\|_\infty\le C\|z\|_{H^s}\|h\|_{H^s},
\tag{68}
\]

并有任意点统一 C||h||² 的二阶余项。这里只得到真实不变量提取；把它称为完整 Lyapunov–Schmidt 坐标图还需要核、余核与消元等价证明。

### 12.3 实际 slow holonomy 决定全频移动中心

固定一个 (58) 的源，不增加光滑性。令 F(x)=∫₀ˣV、G_λ=diag(e^{λx},e^{F(x)})、Y=G_λU。则

\[
U_x=\begin{pmatrix}0&q e^{F-\lambda x}\\r e^{-F+\lambda x}&0\end{pmatrix}U.
\tag{69}
\]

每个非零 Dyson transition 项是有序 simplex 上的 L¹ 多重积分，含相位 exp(iω_nΣ_jσ_jx_j)，σ_j=±1 交替；一旦至少发生一次 transition，这个线性相位就不恒定。L¹ 多维 Riemann–Lebesgue 引理使该项趋于零。ζ 在紧集上时，振幅形成 L¹ 紧集，有限网给 ζ 一致性；共同 C^N/N! 界允许求和后取极限。因此

\[
T(\lambda_n+\zeta,z)\longrightarrow
\operatorname{diag}(e^{L\zeta},e^{A(z)}),
\quad
\mathscr D(\lambda_n+\zeta,z)\longrightarrow
4\sinh^2\!\left(\frac{L\zeta-A(z)}2\right)
\tag{70}
\]

在 ζ 紧集上一致。这里 e^{λ_nL}→1；未经平方的 SL₂ normalized trace 带交替符号，不能误称其本身有同一极限。

缩小源球使 |A/L|<ρ/2，(70) 的极限在圆盘内仅有 ζ=A/L 的双根。轮廓矩遂给

\[
a_n(z)\longrightarrow A(z)/L,\qquad g_n(z)\longrightarrow0.
\tag{71}
\]

这只是每个固定源的高频极限，未声称整个 H^s 有界球上统一的 RL 衰减率。仍可严格强化 (68)：因为 c₀×c₀ 是 ℓ∞×ℓ∞ 的闭子空间，而映射值逐点由 (71) 落入其中，Fréchet 差商及解析 Taylor 系列也留在该闭子空间。因此

\[
\boxed{\quad
z\longmapsto\left(a_n(z)-\frac1L\int_0^LV(z),\ g_n(z)\right)
\ :\ B_\epsilon(X_s)\longrightarrow c_0\times c_0
\quad\text{复解析。}\quad}
\tag{72}
\]

它继承 (68) 与统一 C¹ 二阶余项估计。这是实际 slow holonomy 的精确中心重整化，并得到真正 Sobolev 源上的全频非线性序列图。尚无加权 ℓ² 衰减、norming 数据或 Poisson 对应；(65) 又说明其背景微分全为零，不能作为状态逆的 Banach 微分同构。因此本节没有完成原场 Liouville 完备性，也不把共轭不变量与完整 framed 状态信息混为一谈。

## 13. M=2 实际 Floquet 不变量的原物理 Poisson 对合

本节补上 §12 当时未证的一个依赖：实际有限 λ monodromy trace、判别式及双分支点对称组合，在原物理 J 上对合。证明直接计算 actual monodromy 梯度，不使用形式 residue/resolvent 梯度替代，也不援引未经核实的 AKNS Poisson 定理。尚未证明 M>2、作用角或原场最大各向同性。

actual 梯度、周期分部积分、正确 Γ 中心以及 §15 的 Hessian/strong 泛型结论已通过 [独立物理 Poisson 审计](../../Workspaces/dlw_recovery_20261011/spectral_m2_actual_poisson_independent_audit.md)。

### 13.1 准确物理括号与无需场导数的 traceless connection

M=2 时已有 free q₀=b₀−b₁−d₀−d₁=b₀−b₁−S。故本稿 u=q₀+S=b₀−b₁、v=d₀−δ 与原 free q₀,d₀ 仅差常数，普通积分梯度下准确张量仍是

\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix},
\qquad
\{F,G\}=-\frac1{16}\int_0^L
\left(F_uD G_v+F_vD G_u\right)dx.
\tag{73}
\]

固定均值投影不会改变 D。利用 (54) 及 b₁=−d₀u/S、b₀=b₁+u，原 rank-one connection 的迹为 λ−2uv/S=λ+V。去掉这个 scalar trace 得到实际 traceless connection

\[
\mathsf L_\lambda=
\begin{pmatrix}
u/2+\lambda v/S&(\delta+v)(1+\lambda/S)\\
(\delta-v)(\lambda/S-1)&-u/2-\lambda v/S
\end{pmatrix}.
\tag{74}
\]

记 H=diag(1,−1)、E=[[0,1],[0,0]]、F=[[0,0],[1,0]]，并定义

\[
K_\lambda=\frac\lambda S H+(1+\lambda/S)E+(1-\lambda/S)F,
\quad L^0_\lambda=\frac S2(E-F)+\frac\lambda2(E+F).
\]

则 𝕃_λ=L⁰_λ+uH/2+vK_λ，依赖 u,v 仿射且不含任何场导数。这使下面的梯度与周期分部积分直接合法。此段计算使用原物理矩阵，而不是 companion 的场依赖框架。

### 13.2 Actual monodromy 的周期 adjoint 梯度

令 𝕐_λ′=𝕃_λ𝕐_λ、𝕐_λ(0)=I，𝓝_λ=𝕐_λ(L)，𝓕_λ=tr𝓝_λ。精确地

\[
\mathcal N_\lambda=e^{-(\lambda L+A(z))/2}\mathsf T_{\chi}(\lambda,z),
\quad\det\mathcal N_\lambda=1,
\quad\mathscr D(\lambda,z)=\mathcal F_\lambda^2-4.
\tag{75}
\]

定义 𝕎_λ(x)=𝕐_λ(x)𝓝_λ𝕐_λ(x)^{-1}。周期系数使 𝕎_λ(L)=𝕎_λ(0)，并有 𝕎_λ′=[𝕃_λ,𝕎_λ]。初值问题的实际 Duhamel 变分给

\[
\delta\mathcal F_\lambda
=\int_0^L\operatorname{tr}(\mathcal W_\lambda\,\delta\mathsf L_\lambda)dx,
\qquad
(\mathcal F_{\lambda,u},\mathcal F_{\lambda,v})
=\left(\operatorname{tr}(\mathcal W_\lambda H/2),
\operatorname{tr}(\mathcal W_\lambda K_\lambda)\right).
\tag{76}
\]

对于光滑周期场这些梯度光滑且周期。s=1 的实际 H¹ 物理场也足够：𝕃∈H¹，𝕎 先由 ODE 属于 H¹，再由 H¹ 乘法代数及 𝕎′=[𝕃,𝕎] 得 𝕎∈H²；故梯度∈H²、J 梯度∈H¹ 且均值为零。更高正则度按同一乘法引导提升。以下对合因此在真实 H¹ 小球上可容许，不是只有形式符号运算。

### 13.3 常数双谱参数 tensor 给精确周期 total derivative

取 λ≠μ，令

\[
\mathsf B_{\lambda\mu}=H/2\otimes K_\mu+K_\lambda\otimes H/2.
\]

在 H,E,F⊗H,E,F 基上定义常数 tensor

\[
\begin{aligned}
\mathsf R_{\lambda\mu}={}&
\frac{2S^2-\lambda^2-\mu^2}{4S(\lambda-\mu)}H\otimes H
+\frac{S+\mu}{4S}H\otimes E+\frac{S-\mu}{4S}H\otimes F\\
&-\frac{S+\lambda}{4S}E\otimes H
+\frac{(S+\lambda)(S-\mu)}{S(\lambda-\mu)}E\otimes F\\
&+\frac{\lambda-S}{4S}F\otimes H
+\frac{(S-\lambda)(S+\mu)}{S(\lambda-\mu)}F\otimes E.
\end{aligned}
\tag{77}
\]

直接使用 [H,E]=2E、[H,F]=−2F、[E,F]=H 展开，得到对任意 u,v 的恒等式

\[
\boxed{\quad
[\mathsf R_{\lambda\mu},\mathsf L_\lambda\otimes I+I\otimes\mathsf L_\mu]
=\frac12[\mathsf B_{\lambda\mu},I\otimes\mathsf L_\mu-\mathsf L_\lambda\otimes I].
\quad}\tag{78}
\]

它只需分别比较 1,u,v 三个系数。独有 [exact tensor 脚本](../../Workspaces/dlw_recovery_20261011/spectral_m2_actual_poisson_tensor_checks_20261011.py) 与 [结果证书](../../Workspaces/dlw_recovery_20261011/spectral_m2_actual_poisson_tensor_checks_20261011.json) 用 48 个 scalar 方程解出 9 个 tensor 系数，逐项约分验证 (78)；同时独立核对 (74)、原矩阵 trace 及 R_{λμ}=−flip(R_{μλ})。最终成功脚本 SHA256 为 `966318bf7023887ff857efab6db1b9498dcd1ebf1f28b4aa9f9cb6dd5962b7f8`，证书内含同一 hash。

由 (76)，(73) 的括号被积项等于 tr₁₂(B_{λμ}W_λ⊗W_μ′)。周期分部积分及 cyclic trace 给

\[
\begin{aligned}
\int\operatorname{tr}_{12}(B\,W_\lambda\otimes W_\mu')dx
&=\frac12\int\operatorname{tr}_{12}
([B,I\otimes L_\mu-L_\lambda\otimes I]\,W_\lambda\otimes W_\mu)dx\\
&=\int_0^L\frac d{dx}\operatorname{tr}_{12}
(R\,W_\lambda\otimes W_\mu)dx=0.
\end{aligned}
\tag{79}
\]

第一行是**积分后**的恒等式，不误称未分部积分的原被积项逐点相等。第二行正是 (78) 与 adjoint 方程。故

\[
\boxed{\quad\{\mathcal F_\lambda,\mathcal F_\mu\}_{\rm physical}=0
\quad\text{对全部 }\lambda,\mu\in\mathbb C.\quad}
\tag{80}
\]

λ=μ 从实际泛函与梯度对谱参数的解析性取极限；R 的 pole 是证明 tensor 的 pole，不是 actual F 的 pole。实场上 F_{\bar λ}=\overline{F_λ}，因此各实部、虚部同样相互对合。

### 13.4 实际移动 center/gap 族对合及 holonomy

(75)、(80) 给 {𝒟(λ),𝒟(μ)}=0。§12 的每个固定频率轮廓都紧致且分母不为零，可以在真实 Sobolev 微分中交换轮廓积分与源变分。由 (67) 的链式法则，所有实际 a_n、g_n（含实部及虚部）的梯度均可容许，且任意两个坐标的物理括号为零。

归一化中 A=∫V=−2S^{-1}∫uv 也不是未知 Casimir。由原 J 直接计算

\[
J\,\delta A=\frac1{8S}(u_x,v_x).
\tag{81}
\]

它产生真实空间平移；周期 monodromy 在基点平移下共轭，所以 {F_λ,A}=0。于是原未归一化 trT_χ=e^{(λL+A)/2}F_λ、detT_χ=e^{λL+A} 也彼此对合，且 (72) 的 holonomy 重整化 center 与半 gap 平方仍全部对合。

本节完成的是 M=2 **实际**全谱 trace/判别式/分支点族的物理对合，不再只依赖形式 C_n。它不补上 norming/divisor 的恢复，不证明这些梯度的 Hamilton 场在原非线性相空间中闭包为最大各向同性，也未建立实际共同层级解流。§8 的全频线性二次最大性与本节 nonlinear 对合之间仍缺少 nonlinear 完备性桥梁。

非零 B 的参数必须准确中心化。原 ν=B−S 使 C_Γ=C_{B=0}(b)−BP；物理闭合 b_j=B+b_j⁰，故

\[
A_{\chi,\Gamma}(\lambda)=B I+A_{\chi,0}(\lambda-B),
\qquad \mathcal F_{\Gamma}(\lambda)=\mathcal F_0(\lambda-B).
\tag{82}
\]

这里 centered 参数是 λ−B，与原 L−B 相同。原矩阵中 −BP 项不能遗漏；遗漏会错误地得到 λ−2B。B 对 x 恒定，故 normalized monodromy 的 scalar 因子恰抵消 e^{BL}，(82) 在每个固定时间精确成立。任意 B(t) 的实际时间守恒仍按已有周期 centered gauge 处理。

## 14. 实际 quasimomentum 的局部 C_n 展开与真实 order-zero Hamilton 流

本节把 §13 的 actual Floquet 族接到原 centered 局部 C_n。formal trace 只用于**识别有限渐近系数**；实际周期 Riccati 解及 Sobolev C¹ 余项另行证明，后者使系数提取能用于真实 Poisson 括号。没有把 actual Bloch resolvent 当作形式 residue 梯度。

本节实际 Riccati、C¹ 余项、原 charge 标度及 order-zero 流另经 [quasimomentum 独立审计](../../Workspaces/dlw_recovery_20261011/spectral_actual_quasimomentum_independent_audit.md) 核验；其中补证固定轮廓向量场、同一个低阶时间窗的 C∞ 持久性与有限选定谱流交换。

### 14.1 大正参数的实际周期 Riccati 解和有限 Sobolev C¹ 余项

令 N≥1 为任意固定整数。在 (58) 的一个有界 H^{N+2} 复源球内，另缩小 H¹ 幅度使 q=−S+u 无零点。q,V∈H^{N+2}、r∈H^{N+1}。对真实 λ≥Λ>0，周期 Fourier resolvent

\[
R_\lambda=(D+\lambda)^{-1},\qquad
\|R_\lambda\|_{H^1\to H^1}\le\lambda^{-1}
\tag{83}
\]

给 Riccati 固定点方程

\[
b_\lambda=R_\lambda(r+Vb_\lambda-qb_\lambda^2).
\tag{84}
\]

H¹ 乘法代数使右端在 ||b||_{H¹}≤C/λ 球内为 contraction，常数对源球一致；其微分 norm 为 O(λ^{-1})。因此存在唯一 small periodic H¹ 解，且 b_λ 对实际源复解析。无需估计虚频振荡或使用固定 companion 条件数。

递推定义真正局部微分多项式

\[
\beta_1=r,\qquad
\beta_{j+1}=V\beta_j-D\beta_j
-q\!\sum_{a+b=j,\ a,b\ge1}\beta_a\beta_b.
\tag{85}
\]

β_j∈H^{N+2−j}，j≤N+1；故 b^{[N]}=Σ_{j=1}^Nβ_jλ^{-j} 在 (84) 中的 differential residual 为 H¹ 中 O(λ^{-N})，在上述源球上及其源微分一致。再用 (83) 与 contraction 逆给

\[
\left\|b_\lambda-\sum_{j=1}^N\beta_j\lambda^{-j}\right\|_{H^1}
\le C_N\lambda^{-N-1}.
\tag{86}
\]

该误差在较大复源球上一致，且本身源解析；Cauchy 差商估计在较小球上给同阶 Fréchet C¹ 余项。因此 (86) 是 H^{N+2}→H¹ 的有限阶 **C¹** 展开，非仅逐场形式 WKB。常数可以依赖 N 与该高阶源球，不声称任意阶只用一个低阶 H¹ norm 控制。

实际 fast 解取 φ_x=(λ+q b_λ)φ、ξ=b_λφ。由 (84) 它精确满足 (59)，b_λ 周期使 (1,b_λ(0)) 成为实际 monodromy 特征线。因此

\[
\mu_{\rm fast}(\lambda,z)=\exp\{\lambda L+\mathcal K_\lambda(z)\},
\quad \mu_{\rm slow}=\exp\{A(z)-\mathcal K_\lambda(z)\},
\quad \mathcal K_\lambda=\int_0^Lq b_\lambda dx.
\tag{87}
\]

第二式由 actual detT 精确获得。λ≥Λ 时两乘子分离，且

\[
\mathcal F_\lambda=2\cosh\left(\lambda L/2-A/2+\mathcal K_\lambda\right),
\quad
\mathcal K_\lambda=\operatorname{arcosh}(\mathcal F_\lambda/2)
-\lambda L/2+A/2.
\tag{88}
\]

arcosh 分支由 λ→+∞、K_λ=O(λ^{-1}) 唯一选定；源球与 Λ 可统一选到 sinh 不为零。因此 K_λ 是 actual F_λ,A 的解析函数，§13 已严格给 {K_λ,F_μ}=0，而非从一个形式展开猜测对合。

### 14.2 有限渐近系数准确等于原 centered C_n

本节 q≠0，令 W=V+q_x/q、C=D−W。原 M=2 centered scalar Lax 算子就是

\[
\mathscr L=C^{-1}(D^2-WD-qr)=D-C^{-1}qr,
\quad C_n=\frac1n\operatorname{Tr}\mathscr L^n,
\quad\operatorname{Tr}=\int_0^L\operatorname{res}_D.
\tag{89}
\]

该算子与原 ordered-product centered L 的等式来自 [原全周期矩阵稿 §1–2](../../Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md)：φ=Σχ=(μ−1)ψ₀，精确 splitting 给 L=D−q(D−V)^{-1}r；q≠0 时再用 q(D−V)^{-1}=(D−V−q_x/q)^{-1}q 得到 (89)，没有另换一个相似但不同的 charge 层级。

只在此小节作 λ^{-1}-adic formal 运算。令 b^f=Σ_{j≥1}β_jλ^{-j}、z_f=λ+qb^f、t_f=W−qb^f。(85) 直接给

\[
(D-t_f)(D-z_f)=D^2-(\lambda+W)D+\lambda W-qr
=C(\mathscr L-\lambda).
\]

于是得到两个都为 I+O(λ^{-1}) 的准确乘积分解

\[
1-\mathscr L/\lambda
=\left(1+C^{-1}q b^f\right)
\left(1-D/\lambda+q b^f/\lambda\right).
\tag{90}
\]

周期 Adler trace 对交换子为零；λ-adic log 的乘法公式因各 BCH 项都是交换子，给 Trlog(UV)=TrlogU+TrlogV。这里每个 λ^{-n} 系数是有限阶 PDO，所有 trace 均逐系数定义。第二因子的每个 log 系数都是微分算子，res 为零。第一因子中的 C^{-1}qb^f 是 D 阶 −1，平方及更高次阶≤−2，故其 log residue 准确等于 qb^f。因此

\[
\int_0^Lq b^f dx
=\operatorname{Tr}\log(1-\mathscr L/\lambda)
=-\sum_{n\ge1}C_n\lambda^{-n}.
\tag{91}
\]

这只是一个 algebraic 系数识别；由 actual (86)、(87) 才获得

\[
\boxed{\quad
\mathcal K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(B(H^{N+2});\mathbb C)}(\lambda^{-N-1}).
\quad}\tag{92}
\]

例如 K 的第一系数 ∫qr=−C₁，第二系数 ∫q(Vr−r_x)=∫Wqr=−C₂；背景 K=−δ²L/λ−δ⁴L/λ³+… 与 L₀=D+δ²D^{-1} 的 C_n 也吻合。不能省略 (86) 后直接把 (91) 当成真实 source-gradient 渐近式。

### 14.3 Actual F_μ 与全部局部 C_n 的严格对合桥

固定 μ∈ℂ。(76) 的周期 adjoint 方程把实际 Hamilton 场写成不含 source x 导数的精确表达式

\[
X_{\mathcal F_\mu}
=-\frac1{16}\left(
\operatorname{tr}(\mathcal W_\mu[K_\mu,\mathsf L_\mu]),
\operatorname{tr}(\mathcal W_\mu[H/2,\mathsf L_\mu])\right).
\tag{93}
\]

固定 μ 时，Hs 的周期 ODE 与乘法引导给 W_μ∈H^{s+1}、源解析依赖；(93) 因而为 H^s→H^s 的解析映射，s≥1，均值为零。对 z∈H^{N+2}，它确实是同一高阶 Sobolev 源切向量。以此向量代入 (92) 的真实 C¹ 余项，并用 {K_λ,F_μ}=0，得到

\[
0=-\sum_{n=1}^N\lambda^{-n}\{C_n,\mathcal F_\mu\}
+O(\lambda^{-N-1}).
\]

逐次乘 λ 并令 λ→+∞ 给

\[
\boxed{\quad\{\mathcal F_\mu,C_n\}_{\rm physical}=0
\quad\text{对每个 }n\ge1,\ \mu\in\mathbb C.\quad}
\tag{94}
\]

任意有限 n 在相应 H^{n+2} 小球上严格成立，所有 n 则在其光滑交集上成立。这没有断言存在一个固定低阶 Sobolev 开集支持全部 C_n。轮廓链式法则同样把 (94) 接到 §12 全部实际 a_k、g_k；A 与 C_n 的对合另由这些局部周期积分的平移不变性直接获得。

### 14.4 真实局部 order-zero 辅助流与余下困难

对实际实场，取 H=ReF_μ 或 ImF_μ；(93) 的实型组合仍为 H^s→H^s 解析 Hamilton 场，固定 μ、s≥1。Banach Picard contraction 因而给真实局部 H^s 解流，保持 source 各均值、保持全部可定义的 C_n，也保持 §12 每个 actual center/gap。每个固定 a_k、g_k 的实部/虚部由紧轮廓积分得到同样 order-zero 解析场与局部辅助流。

A、原未归一化 trace 及 holonomy-subtracted center 还含 (81) 的 translation 项；它在 H^s→H^{s-1}，不能把这项也称为 order-zero Banach 向量场。它们的 §13 对合在光滑叶及相应 H¹ 积分括号中有效，平移本身有实际群；这里不额外声称该群在每个 H^s 点可微。

新增的 auxiliary actual Floquet 流不解决原 DLW 的 e^{tk²} 正时间不适定性。与已经存在的 strong presentations 的实际共同域接合另见 [strong 谱时间桥](../../Workspaces/dlw_recovery_20261011/spectral_m2_strong_domain_flow_bridge.md)：order-zero 低阶流统一覆盖全部旧有限 joint 图，Cn 对合给真实方程输送，随后重新 mixed 参数化识别为同一 𝔖∞ 的 strong plots；其 Hamilton 速度因此为同一弱辛域的内部切向。这个接合保留已有强域条件，并不把全部 Hs 初值都变成原 DLW 的合法 Cauchy 初值。仍缺完整 norming/divisor 坐标、加权全频 nonlinear inverse 和 nonlinear 最大各向同性。

### 14.5 M=2 actual trace/C_n 对合可推广到任意均值叶与有限幅度

§13 的 affine connection、actual gradient 与 tensor 恒等式从未使用 ∫u=∫v=0，也未使用 small δ 或 small source；这些限制只服务 §12 的统一高频双根标号。对任意固定 S≠0、任何周期 u,v，物理闭合 (74)、常数 J 及 normalized F 的对合均仍精确成立。F_μ 与 (93) 在整个 H^s 复源空间为解析映射，固定 μ、s≥1，每个点都有真实局部实型 auxiliary 流。

Riccati contraction (84) 也不除以 q：在任意给定有界 H^{N+2} 源球内，只需相应更大的正 Λ，即有 (86) 的真实 C¹ 余项。因此只剩 (91) 的 q≠0 系数识别须延拓。未除以 q 的原 scalar 算子为

\[
\mathscr L=D-q(D-V)^{-1}r.
\tag{94a}
\]

它的每个固定 C_n 及 −∫qβ_n 都是 q,r,V 有限 jets 的微分多项式积分，进而是 u,v 有限 jets 的多项式积分。给任意目标状态 (u,v)，沿 z(t)=t(u,v)；小 t 时 q=−S+tu 无零点，(91) 已证明 C_n(z(t))=−∫q(z(t))β_n(z(t))。两侧均为 t 的有限多项式，故恒等式对 t=1 也成立，包括 q 有零点的情形。

于是 (92)、(94) 在每个任意幅度有界 H^{N+2} 源球上仍成立，均值可任意；常数与正 Λ 随该球改变。该推广不需要全谱 inverse 或 q≠0 的 coefficient chart。它完成的是任意 M=2 周期物理状态上的 actual F_μ/C_n 对合及 fixed-parameter auxiliary 流，并不把 §12、§15 的均匀叶 gap 标号、有限独立或 strong 泛型结论推广到别的均值叶。

## 15. Actual moving gaps 的精确 Hessian、中心二阶项及同一 strong 参数域上的有限独立

本节严格采用 M=2、(58)、0<|δ|<k₀/2 和包含均匀态的指定分量均值叶。对每个正 k_n，令

\[
\gamma_n=\omega_n/k_n>0,\qquad d_n=L\gamma_n/2,
\qquad K_n=Lk_n^2\gamma_n/(16S),\qquad \sigma_n=(-1)^n.
\tag{95}
\]

K_n 正是 §7 的物理 bracket 权重，S<0 时它也带符号；canonical Q,P 的定义已含该符号。

### 15.1 实际二重 Floquet 点的 gap Hessian

固定真实物理切向量 η=(η_u,η_v)∈X_s。在 λ_n 处，normalized 背景 monodromy 为 σ_nI。按 §7 的固定背景 eigenframe 共轭后，零均值 first Born 给对角项为零，非对角项为

\[
\mathcal N(\lambda_n,\varepsilon\eta)
=\sigma_n\left[I+\varepsilon
\begin{pmatrix}0&\overline{c_{-,n}(\eta)}\\c_{+,n}(\eta)&0\end{pmatrix}
+\varepsilon^2R_n+O(\varepsilon^3)\right].
\tag{96}
\]

这里 reverse 样本的共轭恰是同一个 λ_n 的反向矩阵元；不是对复源随意加共轭。§11 的实际 endpoint gauge 在背景为标量 monodromy，故 first variation 的 gauge commutator 为零，(96) 可由 original χ、split 或 companion 的背景固定框架等价计算。

detN=1 给 trR_n=c_{+,n}\overline{c_{-,n}}，因此真实判别式的 ε² 系数为 4c_{+,n}\overline{c_{-,n}}。另一方面，(62) 在 ζ=λ−λ_n 处为 4d_n²ζ²+O(ζ³)。实际 center 与 gap 坐标在背景的一阶全为零，所以 (66) 或 (67) 精确给

\[
\boxed{\quad
g_n(\varepsilon\eta)
=-\frac{\varepsilon^2}{d_n^2}
c_{+,n}(\eta)\overline{c_{-,n}(\eta)}+O(\varepsilon^3)
=-\frac{k_n^2}{4SL\gamma_n}\varepsilon^2I_n(\eta)
+O(\varepsilon^3).
\quad}\tag{97}
\]

最后一步用 §7–8 的 **原物理** canonical I_n=Q_nP_n=c_{+,n}\overline{c_{-,n}}/K_n。此式给二次齐次项；若写 D²g_n(0)[η,η]，右端二次系数须乘 2。对固定有界 η 集，余项在 ℓ∞ 中一致来自 §12 的真实解析 Taylor 估计。

因此 actual Re g_n、Im g_n 的 Hessian 分别探测 Re I_n、Im I_n，两条实 action 方向都存在。它们与 odd-only 层级缺失的 phase 方向一致，但没有把这些二次 action 自动当作非线性 canonical action。

### 15.2 中心二阶项：精确 Born 表达与 holonomy/phase 分解

为避免只给形式 shift，令

\[
\mathsf H_\lambda(x)=\eta_u(x)H/2+\eta_v(x)K_\lambda,
\quad F_0(\lambda)=2\cosh\!\left(\frac L2\sqrt{\lambda^2-4\delta^2}\right),
\]

\[
F_2(\lambda;\eta)=\int_{0<y<x<L}\operatorname{tr}
\left[e^{L^0_\lambda(L-x)}H_\lambda(x)
e^{L^0_\lambda(x-y)}H_\lambda(y)e^{L^0_\lambda y}\right]dx\,dy,
\quad D_2=2F_0F_2.
\tag{98}
\]

原 traceless connection 对源仿射，故这是 actual F(λ,εη) 的 ε² 系数；不是少掉二阶场系数的近似。全部 first-order trace 变化为零，所以 D₂ 正是 actual 𝒟 的 ε² 系数。写 Γ(λ)=√(λ²−4δ²) 的局部支，Γ(λ_n)=ik_n，有 Γ′(λ_n)=γ_n、Γ″(λ_n)=−4iδ²/k_n³。背景 𝒟₀ 的 ζ²、ζ³ 系数分别为 L²γ_n²、L²γ_nΓ″(λ_n)。(67) 的 residue 遂给精确中心二次项

\[
a_n(\varepsilon\eta)=\varepsilon^2a_n^{[2]}(\eta)+O(\varepsilon^3),
\quad
a_n^{[2]}=-\frac12\left[
\frac{D_2'(\lambda_n)}{L^2\gamma_n^2}
-\frac{D_2(\lambda_n)\Gamma''(\lambda_n)}{L^2\gamma_n^3}
\right].
\tag{99}
\]

F₀′(λ_n)=0、F₀(λ_n)=2σ_n，使 D₂′(λ_n)=4σ_n F₂′(λ_n)；故 (98)、(99) 可直接计算每个方向的 shift，含所有 off-resonant Born 耦合，并非只取 gap coupling product。

A(εη)=ε²A^{[2]}，A^{[2]}=−2S^{-1}∫η_uη_v。更强的 holonomy 结论来自 (72) 在 c₀ 中的源 Taylor 系数：

\[
a_n^{[2]}(\eta)=\frac{A^{[2]}(\eta)}L+\Phi_n^{[2]}(\eta),
\qquad (\Phi_n^{[2]}(\eta))_n\in c_0.
\tag{100}
\]

其中 Φ^{[2]} 用 (98)、(99) 减去 A^{[2]}/L 精确给出；它是剩余二阶 phase shift，未被误计为额外 Casimir 或已构造 norming 角变量。未声称该 c₀ 余项具有某个加权 ℓ² 衰减率。

### 15.3 真正物理场上的任意有限 actual gap 块独立

取有限正频率集合 E。由 §7 的明确物理 Fourier 同构，存在真实有限 Fourier 方向 η，使每个 n∈E 的 Q_n(η)=P_n(η)=1，其余块为零。每个 n 再取真实测试方向 ζ_{n,R},ζ_{n,I}，分别使 δP_n=1、i，所有其他 δQ,δP 为零。这些方向都属于同一均值叶。

记 b_n=−k_n²/(4SLγ_n)≠0。由 (97)，在 actual 源状态 z_ε=εη 上，2|E| 个真实泛函 {Re g_n,Im g_n:n∈E} 的微分在上述测试方向的矩阵为 ε diag(b_n,b_n)_{n∈E}+O(ε²)，故

\[
\det\mathsf J_E(z_\varepsilon)
=\varepsilon^{2|E|}\left(\prod_{n\in E}b_n^2+O(\varepsilon)\right)\ne0
\tag{101}
\]

对充分小非零 ε 成立。同时 selected g_n=ε²b_n+O(ε³)≠0，所以这些实际双根已经分裂。这是 full actual monodromy gap 泛函的有限独立，非只对代理线性矩阵作独立性检验。所有泛函在 §13 已证明实际物理对合，其固定参数 Hamilton 场在 §14 为真实 order-zero 辅助场。

(101) 本身不把有限 Fourier 初值误归入某个原非线性全层级共同域。该接合使用下面已经构造的 strong 参数图。

### 15.4 同一无限 strong 参数图中可数 actual gap 块独立

使用 [mixed 独审稿 §17](mixed_independent_review_20261011.md) 已证明的同一 holomorphic Hilbert 参数图 F:B_R(H_C)→𝓔_C²：F(0) 是均匀物理态，DF(0) 的 range 包含全部有限 Fourier 切向量，实有限维预复合全是 𝔖_∞ 的实际合法 strong plots。限制同一图到更小 H 球，使 F 的像进入 §12 的共同 H¹ 物理小球，故全部 actual g_n 同时解析，轮廓无需随 n 另选参数域。

对每个 E={1,…,N}，取 (101) 的 η、ζ 在 DF(0) 下的 H 原像。由于 Dg_n(0)=0，D²F 对复合 g_n∘F 的 Hessian 不产生额外项。于是同一参数球上对应的 real-analytic Jacobian minor J_N^gap 满足沿该原像直线

\[
J_N^{\rm gap}(\varepsilon\widehat\eta)
=\varepsilon^{2N}\left(\prod_{n=1}^Nb_n^2+O(\varepsilon)\right),
\tag{102}
\]

不恒零。其非零集在实 H 球中开且稠密：任意开子球若恒零，沿连接其内点与见证点的实解析线段会迫使全段恒零，矛盾。Baire 的可数交集给同一个实际 z=F(a)∈𝔖_∞，使所有 actual gap finite prefixes 的微分在真正内部 plot 切向量上独立。还可同时加入每个 g_n≠0 的开稠密条件，得到所有这些 actual 双分支点都分裂的同一状态。

同样可与 mixed §17 的全部 charge minor 非零集相交，使 **每个族分别**具有所有有限块独立的同一个状态。没有宣称 {C_n} 与 {g_n} 的合并族代数独立；它们之间已有 (92) 的真实谱关系。这里的 residual 性仅指固定 H 参数球，不外推为整个 𝔖_∞ 的泛型或所有均值叶。

由此消除了“每个 finite gap 只有不同见证状态”这一弱点，但没有给 nonlinear Hamilton 闭包=共同微分 annihilator。§12 的一阶全零、§15 的 Hessian 与有限独立都不能推出该反向包含；仍须 actual norming/inverse 或可核验的完整 squared-eigenfunction 闭包定理，并与 𝔖_∞ 的同一弱辛内部切向结构匹配。

## 16. 全 M 实际 monodromy 的物理对合与固定谱参数 Hamilton 流

本节重新从原物理张量计算跨分量 free bracket，再证明全 M 的实际 affine traceless connection 与通用 tensor 恒等式。结论适用任意有限 M≥2、S≠0 的周期物理场，任意分量均值及有限幅度；不要求 small δ。M=3 的搜索只用于发现公式，全 M 定理由下面的 dimension-free matrix-unit 证明给出。

本节公式及 §17 的同一 strong 相域接合已通过 [全 M 实际谱独立审计](../../Workspaces/dlw_recovery_20261011/all_m_actual_spectral_independent_audit.md)；另有 [根任务独立代数复核](../../Workspaces/dlw_recovery_20261011/root_all_m_actual_spectral_audit_20261011.md)。两者均没有重跑既存证书，特别区分 (114) 的周期积分式与含 R+B/2 的逐点式。

### 16.1 原 h 加权配对到普通积分：完整跨分量核验

原 [periodic reduction §3](../../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md) 使用 hΣ_j∫ 配对，源 (p=P₀U,s=w−c) 的张量为 −offdiag(P₀D)。令 m=M−1，Z_j=e_j−e_m，E 取前 m 分量，

\[
q_j=b_j-b_m-d_j-2\sum_{k=j+1}^m d_k+d_m,
\quad d_j=hw_j/8,
\quad (K_d)_{jk}=-\delta_{jk}-2\mathbf1_{k>j}+\delta_{km}.
\]

共同 U 的非线性 mean reconstruction 在 b_j−b_m 中精确抵消，故实际 source Frechet 矩阵恒为

\[
\mathsf F_*=
\begin{pmatrix}Z^T/2&hK_d/8\\0&hE/8\end{pmatrix}.
\]

P₀Z=Z、ZᵀEᵀ=I_m，且

\[
(K_dZ)_{j\ell}=1-\delta_{j\ell}-2\mathbf1_{\ell>j}
=\begin{cases}1&\ell<j,\\0&\ell=j,\\-1&\ell>j,\end{cases}
\]

是 skew 矩阵。因而 pushforward 的 qq block 是 −h(K_dZ+(K_dZ)^T)D/16=0，dd block 也为零，qd 与 dq block 准确为 −hI_mD/16。目标普通积分梯度等于 h 倍 h-weighted 梯度，故同一括号的普通积分张量为

\[
\boxed{\quad J_{qd}=-\frac1{16}\begin{pmatrix}0&I_mD\\I_mD&0\end{pmatrix}.\quad}
\tag{103}
\]

没有把跨分量 identity 当作假设；它由原 P₀、Z、E 完整计算。S 固定为原 Casimir 参数，B 的外部时间规范不进入这些 free 坐标。

再令 Δ_j=b_j−b_m，j<m，Δ_m=0。准确关系为

\[
\Delta_j=q_j+S+\sum_{\ell<m}\operatorname{sgn}(\ell-j)d_\ell.
\tag{104}
\]

混合矩阵 A_{jℓ}=sgn(ℓ−j) skew，所以 (q,d)↦(Δ,d) 的 qq correction 为 A+Aᵀ=0。因此 (Δ_first,d_first) 同样具有 (103)。它们只作可逆仿射变换，固定分量均值的同一物理叶不变。

### 16.2 Actual traceless connection 仿射于全部 free fields

以 centered λ=λ_original−B 工作，先取 B=0。原矩阵 A_χ=λP+C，P=d1ᵀ/S，C=diag(b−d)−2diagdH+d1ᵀ。物理闭合 b_m=−Σ_{j<m}d_jΔ_j/S。令 Δ̄=M^{-1}Σ_iΔ_i。减去 scalar trace 得

\[
(\mathsf L_\lambda)_{ii}=\lambda(d_i/S-1/M)+\Delta_i-\bar\Delta,
\qquad
(\mathsf L_\lambda)_{ij}=d_i\bigl(\lambda/S+\operatorname{sgn}(j-i)\bigr),\ i\ne j.
\tag{105}
\]

闭合中 b_m 的 quadratic field 项准确被 trace normalization 消掉，因此这是全部 free fields 的真实 affine connection。它不是把独立 matrix coefficients 当成 unconstrained 物理场。记

\[
H_i=E_{ii}-I/M,\quad s_{ij}=\operatorname{sgn}(j-i),\quad s_{ii}=0,
\quad K_i(a)=\sum_j(a+s_{ij})E_{ij},\quad a=\lambda/S.
\]

则 L_λ=Σ_iΔ_iH_i−λI/M+Σ_id_iK_i(a)，d_m=S−Σ_{j<m}d_j。

令 Y_λ′=L_λY_λ、Y_λ(0)=I，N_λ=Y_λ(L)∈SL_M。对 r≥1 取 actual class functional F_{λ,r}=r^{-1}trN_λ^r。Duhamel 的 actual gradient 为

\[
W_{\lambda,r}=Y_\lambda N_\lambda^rY_\lambda^{-1},\quad
W'= [L_\lambda,W],\quad W(L)=W(0),
\]

\[
F_{\Delta_j}=\operatorname{tr}(WH_j),\qquad
F_{d_j}=\operatorname{tr}\bigl(W[K_j(a)-K_m(a)]\bigr),\quad j<m.
\tag{106}
\]

因此固定 λ,r 的实际 Hamilton 场为

\[
X_{F_{\lambda,r}}
=-\frac1{16}\left(
\operatorname{tr}W[K_j(a)-K_m(a),L_\lambda],
\operatorname{tr}W[H_j,L_\lambda]\right)_{j<m}.
\tag{107}
\]

右端没有 source x 导数。与 §14 相同的 Sobolev ODE/乘法证明使 W∈H^{s+1}、源解析，s≥1；故 (107) 是全 H^s 源空间上的局部解析 H^s→H^s 向量场，均值为零。实部/虚部通过 F_{\bar λ,r} 的 holomorphic 组合保实，Banach Picard 给真实局部 auxiliary Hamilton 流；空间平移等变性使光滑初态的全部正则共享首次低阶时间窗。此流结论不需要先证明下面的 R 恒等式。

### 16.3 从 M=3 exact search 到通用 R

两参数 a=λ/S、b=μ/S，a≠b，设

\[
C_H=\sum_iH_i\otimes H_i,\quad
\Pi_0=\sum_{ij}E_{ij}\otimes E_{ji}-I\otimes I/M,
\quad T_s=\sum_{i\ne j}s_{ij}E_{ij}\otimes E_{ji},
\quad \rho=\frac{1-ab}{a-b}.
\]

原物理 bracket 的 gradient tensor 在 (Δ,d) 坐标下精确为

\[
\mathsf B_{ab}=\sum_i\left[H_i\otimes K_i(b)+K_i(a)\otimes H_i\right].
\tag{108}
\]

这是 (106) 中 j<m 的 K_j−K_m 求和后，利用 Σ_iH_i=0 扩展成全 i 的结果。定义

\[
\boxed{\quad
R_{ab}=\left(\rho-\frac{a-b}{2}\right)C_H+T_s
+\frac12\sum_{i\ne j}
\left[(b+s_{ij})H_i\otimes E_{ij}-(a+s_{ij})E_{ij}\otimes H_i\right]
+\rho\sum_{i\ne j}E_{ij}\otimes E_{ji}.
\quad}\tag{109}
\]

等价地，首项与最后项合为 ρΠ₀−(a−b)C_H/2。独有 [M=3 有界 exact 搜索](../../Workspaces/dlw_recovery_20261011/spectral_m3_actual_poisson_tensor_search_20261011.py) 解 405 方程、64 未知量，得到唯一有理 tensor 并逐式核验；搜索自身用时 1.05 秒，设置 55 秒硬预算。其 [证书](../../Workspaces/dlw_recovery_20261011/spectral_m3_actual_poisson_tensor_search_20261011.json) 含源 hash。另一个 [新通用公式检查](../../Workspaces/dlw_recovery_20261011/spectral_all_m_tensor_pattern_checks_20261011.py) 在 M=4,5 验证全部 Cartan 与 row 系数，共 18 块，2.66 秒；[结果](../../Workspaces/dlw_recovery_20261011/spectral_all_m_tensor_pattern_checks_20261011.json) 全通过。没有重跑旧证书。

下面给全 M 的独立证明，有限检查本身不作全 M 推断。

### 16.4 Dimension-free matrix-unit 恒等式

从 (108)、(109) 得

\[
R+B/2=\rho\Pi_0+T_s+\sum_iH_i\otimes K_i(b),\qquad
R-B/2=\rho\Pi_0+T_s-\sum_iK_i(a)\otimes H_i.
\tag{110}
\]

目标是

\[
[R,L_\lambda\otimes I+I\otimes L_\mu]
=\tfrac12[B,I\otimes L_\mu-L_\lambda\otimes I],
\tag{111}
\]

等价于 [R+B/2,L_λ⊗I]+[R−B/2,I⊗L_μ]=0；这里 plus tensor 配**第一** connection，minus 配第二，不能颠倒。

对共同 Cartan D_Δ=ΣΔ_iH_i，matrix-unit 的 root weights 直接证明此式；off-diagonal pair E_ij⊗E_ji 的总 root weight 为零。central −λI/M 不贡献交换子。仅需证明每个单独 row K_i(a),K_i(b) 的贡献为零。

为给可核验的全 M 证据，令 p,q 为输出 tensor 行索引、r,s 为输入列索引（此处 q,s 只是索引）。利用 (110)，两 tensor 的 matrix 元分别为

\[
(R+B/2)_{pq,rs}=
\rho(\delta_{ps}\delta_{qr}-\delta_{pr}\delta_{qs}/M)
+s_{pq}\delta_{ps}\delta_{qr}
+\delta_{pr}(b+s_{qs})(\delta_{pq}-1/M),
\]

\[
(R-B/2)_{pq,rs}=
\rho(\delta_{ps}\delta_{qr}-\delta_{pr}\delta_{qs}/M)
+s_{pq}\delta_{ps}\delta_{qr}
-\delta_{qs}(a+s_{pr})(\delta_{pq}-1/M).
\tag{112}
\]

K_i(a)_{pr}=δ_{pi}(a+s_{ir})。代入有限 matrix multiplication 后，内部求和只含 Kronecker δ，所有 1/M 项抵消；用 ρ(a−b)=1−ab，row 交换子残差精确压成

\[
\delta_{ps}\delta_{qi}\,\Theta(i,p,r)
-\delta_{pi}\delta_{qr}\,\Theta(i,q,s),
\quad
\Theta(i,j,k)=1-s_{ij}s_{ik}-s_{ik}s_{jk}+s_{jk}s_{ij}.
\tag{113}
\]

任意整数索引都有 Θ(i,j,k)=δ_{ij}δ_{jk}：三者互异按六种顺序给 0，两者相同用 s²=1 给 0，三者相同则给 1。于是 (113) 的两项均为 p=q=r=s=i 的同一个 δ，准确抵消。这证明 (111) 对**每个有限 M**、任意物理 free fields 成立，与 M=4,5 的有限核验无逻辑依赖。

### 16.5 全部 actual Floquet class functions 在原物理 J 上对合

将 (106) 的周期 W_{λ,r},W_{μ,s} 代入 (103)，与 §13 相同的周期分部积分给

\[
\{F_{\lambda,r},F_{\mu,s}\}
=-\frac1{16}\int_0^L
\frac d{dx}\operatorname{tr}_{12}
\left(R_{ab}W_{\lambda,r}\otimes W_{\mu,s}\right)dx=0.
\tag{114}
\]

λ=μ 用 actual ODE 与 gradient 对参数解析性取极限。因而所有 λ、r 的真实 trace 泛函及其真实实部/虚部对合。normalized characteristic coefficients 是 traces 的 Newton 多项式、detN=1，故全部实际 Floquet characteristic 数据也对合。这里没有把 formal C_n gradient 当作实际 monodromy gradient。

原 scalar trace normalization 也可恢复。令

\[
\tau=\frac1M\int\sum_i b_i dx
=\int\left[-\frac1S\sum_{j<m}d_j\Delta_j
+\frac1M\sum_{j<m}\Delta_j\right]dx.
\]

则 N_λ=e^{−λL/M−τ}T_χ。直接计算 Jδτ=(Δ_x,d_x)/(16S)，它是空间平移，故与全部 F_{λ,r} 对合。于是原未归一化 trT_χ^r、detT_χ=e^{λL+Mτ} 及全部实际 characteristic coefficients 同样彼此对合。τ 含 translation 速度的一阶损失，不能额外称作 order-zero Hs 向量场。

对任意静态 B，原 A_{χ,Γ}(λ_original)=BI+A_{χ,0}(λ_original−B)，normalized N 精确变为 N₀(λ_original−B)。任意 B(t) 的实际谱守恒使用已核验 centered 周期规范；本节是其同一原物理 Poisson 结构上的 static involution 定理。它仍不证明完整 norming/inverse 或最大各向同性。

## 17. 全 M 实际 fast Floquet 支的 Sobolev C¹ 展开、原 C_n 系数与共同域桥

本节把 §16 的全 M actual class family 接到原 centered 局部 C_n。证明只用原矩阵的精确 periodic splitting、vector Riccati contraction、actual characteristic root 和有限阶 trace-log 代数；不除以任何 q_j 或 d_j。适用任意固定有限 M≥2、S≠0、任意组件均值及有限幅度。谱完备性与 nonlinear action-angle 结论仍未由此得到。

§17.1–3 的全幅度 Sobolev 预算、actual simple root、原 charge 标度及 C¹ 系数桥另经 [全 M quasimomentum 独立二审](../../Workspaces/dlw_recovery_20261011/spectral_all_m_actual_quasimomentum_independent_audit_20261011.md) 逐项核验；§17.4 的内部 plot 接合由上面的全 M 实际谱审计 §7 核验，保留其 strong-domain 条件。

### 17.1 原精确 split 及全幅度 Sobolev Riccati 估计

采用 [原全周期矩阵稿 §2](../../Workspaces/dlw_general_field_20261006/GENERAL_PERIOD_MATRIX_LAX.md) 的 T=[d/S,Z]、K=E−(d_first/S)1ᵀ、T⁻¹=[1ᵀ;K]。其 determinant 是非零常数，T 及 T⁻¹ 周期，允许任意单独 d_j 为零。在 centered B=0 截面，原 χ 系统精确变为

\[
\binom{\phi}{\xi}'=
\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}
\binom{\phi}{\xi},\qquad
q=1^TCZ,\quad r=K(Cd-d_x)/S,\quad V=KCZ.
\tag{115}
\]

其中本式 C 是原 χ 矩阵的 zero-order 系数，不是下节的 differential matrix。q 是 1×m row，r 是 m×1 column，V 是 m×m matrix。唯一源导数在 r 的 d_x 中；各系数是 physical free fields 的局部多项式、只除固定 S。精确 scalar elimination 给原 centered scalar operator

\[
\mathscr L=D-q(DI_m-V)^{-1}r,\qquad C_n=n^{-1}\operatorname{Tr}\mathscr L^n.
\tag{116}
\]

固定 N≥1，取任意有界 H^{N+2} 复源球；q,V∈H^{N+2}、r∈H^{N+1}，界随该球与 M,S 改变。对 λ≥Λ>0，周期 Fourier multiplier R_λ=(D+λI_m)⁻¹ 的 H¹→H¹ norm≤λ⁻¹。vector 方程

\[
b_\lambda=R_\lambda\{r+Vb_\lambda-b_\lambda(qb_\lambda)\}
\tag{117}
\]

在 ||b||_{H¹}≤C/λ 球上有 contraction；H¹ 是乘法代数，固定有限矩阵维数只改变常数。选择依赖源球的 Λ 后，得到唯一小周期 H¹ 解，源复解析，不要求低幅度或任一 q_j 无零点。

定义列系数

\[
\beta_1=r,\qquad
\beta_{j+1}=V\beta_j-D\beta_j
-\sum_{a+b=j\atop a,b\ge1}\beta_a(q\beta_b).
\tag{118}
\]

β_j∈H^{N+2−j}，j≤N+1。截断 b^{[N]}=Σ_{j=1}^Nβ_jλ⁻ʲ 的 differential residual 在 H¹ 中一致为 O(λ⁻ᴺ)：最后 Dβ_N∈H¹，其余有限乘积都在同一代数中。R_λ 再给一个 λ⁻¹，contraction inverse 统一有界，故

\[
\left\|b_\lambda-\sum_{j=1}^N\beta_j\lambda^{-j}\right\|_{H^1}
\le C_N\lambda^{-N-1}.
\tag{119}
\]

在一个稍大的有界复源球上先作同一证明。误差源解析，Cauchy 差商估计在较小球给同阶 H^{N+2}→H¹ Fréchet C¹ 余项。常数可依赖 N 及高阶球；未声称所有阶只用一个低 H¹ norm 控制。

### 17.2 实际 periodic triangularization 与 simple fast characteristic root

实际周期 gauge T_b=[[1,0],[b_λ,I_m]] 精确给

\[
T_b^{-1}\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}T_b
-T_b^{-1}T_b'
=\begin{pmatrix}\lambda+qb_\lambda&q\\0&V-b_\lambda q\end{pmatrix}.
\tag{120}
\]

下左 block 为零正是 (117) 的 differential 方程。由于 T_b 周期，这是一条实际 monodromy 相似变换，不只是 formal diagonalization。actual fast multiplier 为

\[
\mu_f=\exp\{\lambda L+\mathcal K_\lambda\},\qquad
\mathcal K_\lambda=\int_0^Lqb_\lambda dx=O(\lambda^{-1}).
\tag{121}
\]

其余 m 个实际乘子是 V−b_λq 的 monodromy 特征值。源球上该系数的 L¹ norm 一致有界，Grönwall 因而统一控制这些 slow multipliers；无需 slow roots 彼此简单。大正 λ 时 fast multiplier 指数增大，且唯一落在以 e^{λL} 为中心、半径 e^{λL}/2 的圆内，其余 roots 在固定有界圆内。因此它是 simple actual characteristic root，源球与 Λ 可统一选定。由 root 的简单性和唯一选择，μ_f 是原 actual characteristic coefficients 的解析函数。选择 μ_f/e^{λL} 靠近 1 的 log 分支，准确恢复 (121) 的 K_λ。

原 χ 与 (115) monodromy 相似，而 §16 的 N=e^{−λL/M−τ}T_χ。故 K_λ 是 normalized actual class coefficients 与 τ 的局部解析复合；(121) 本身给在整个该源球的一致选择。§16 已证明这些真实函数彼此对合，因而

\[
\{\mathcal K_\lambda,F_{\mu,r}\}=0,\qquad
\{\mathcal K_\lambda,\mathcal K_\nu\}=0
\tag{122}
\]

在相应正参数的共同源球上成立，且 μ∈ℂ、r≥1 任意。这里没有把实际 resolvent 梯度认作 formal residue 梯度。

### 17.3 不除 q 的全 M trace-log factorization 与 actual C_n 对合

以下只作 λ⁻¹-adic 运算。令 \(\mathcal C=DI_m-V\)、\(b^f=\sum_{j\ge1}\beta_j\lambda^{-j}\)。由 (118) 得准确 operator identity

\[
r=(\mathcal C+b^fq)\circ b^f-b^f(D-\lambda).
\tag{123}
\]

这里 b^f 是列乘法算子，\(\mathcal C\circ b^f=b^fD+Db^f-Vb^f\)，所以右端等于 Db^f−Vb^f+b^f(qb^f)+λb^f，恰为 r。代入 (116) 立即给

\[
\mathscr L-\lambda
=(1+q\mathcal C^{-1}b^f)(D-\lambda-qb^f),
\]

\[
1-\mathscr L/\lambda
=(1+q\mathcal C^{-1}b^f)(1-D/\lambda+qb^f/\lambda).
\tag{124}
\]

两 scalar factors 都是 I+O(λ⁻¹)。周期 Adler trace 的 λ-adic BCH commutator 项逐系数为零。第二因子的每个 log 系数都是 differential operator，res 为零。第一因子 X=q𝒞⁻¹b^f 的 D 阶为 −1；X² 及更高幂阶≤−2，且 res_D X=qb^f。因此

\[
\int_0^Lqb^f dx
=\operatorname{Tr}\log(1-\mathscr L/\lambda)
=-\sum_{n\ge1}C_n\lambda^{-n}.
\tag{125}
\]

本式在全 M 原 scalar operator 上准确成立，既未除 q，也无需跨叶解析延拓。它只识别有限代数系数。结合 actual (119) 的真实 C¹ 余项，才得到

\[
\boxed{\quad
\mathcal K_\lambda=-\sum_{n=1}^NC_n\lambda^{-n}
+O_{C^1(B(H^{N+2});\mathbb C)}(\lambda^{-N-1}).
\quad}\tag{126}
\]

固定 μ,r，§16 的 X_{F_{μ,r}} 是同一 H^{N+2} 源切向量。以它代入 (126)，再用 (122)，逐次乘 λ 取极限，给

\[
\boxed{\quad\{F_{\mu,r},C_n\}_{\rm original\ physical}=0
\quad(M\ge2,\ S\ne0,\ n,r\ge1,\ \mu\in\mathbb C).\quad}
\tag{127}
\]

每个固定 n 使用相应 H^{n+2} 层，全部 n 则在 smooth 物理场上成立；不是一个固定低阶 Sobolev 开集上的无限 charge 定义。τ 与 C_n 的对合来自周期局部积分的平移不变性。于是原未归一化 actual trace 及 actual characteristic coefficients 也与全部原 centered C_n 对合。取 (122) 中 K_ν 的第二次有限 C¹ 展开还可重新得到每个 {C_n,C_j}=0，但此处没有用它替代原局部层级证明。

### 17.4 对同一 strong 域的适用范围与剩余缺口

对固定有限个 normalized actual class Hamiltonians，§16 的 order-zero 场、空间平移等变性和 (127) 是 [M=2 strong 谱时间桥](../../Workspaces/dlw_recovery_20261011/spectral_m2_strong_domain_flow_bridge.md) 的全部方程分析输入。其 Banach 球界、同一低阶时间窗内 C∞ 持久性、真实旧 C_n 方程的 variational 输送、全部前缀的 H¹ telescoping 控制都逐字适用于 2m 个源分量；仅有限维常数随 M 改变。必须保留原 all-M strong presentations 及其 mixed 唯一性条件，才可用同一重新 mixed 参数化识别新图为该 \(\mathfrak S_\infty\) 的内部 plot，不能只凭 ambient Hs 取值作此识别。

具体而言，在一个已有 strong coherent plot 的紧参数盒上，逐坐标固定旧复时间窗，使相邻真实有限 joint 图的 H¹ 差小于 ρ2⁻ʲ⁻³。全部图像遂落在同一低阶有界球内；固定 actual flow Φ_σ 给一个对全部前缀共同的正谱时间盘。constant J 与 (127) 使 DΦ_σ X_{C_n}=X_{C_n}∘Φ_σ，所以 Φ_σZ_N 仍为原全部旧方程的相容实际 joint 解。随后沿全 M 已有 mixed 机制重参数化、每次只缩新层级轴而不缩 σ 参数盒；mixed 唯一性识别其中心。此时谱速度才是同一弱辛域的内部 Hamilton 切向。结论只含有限组选定谱参数及有限支持旧时间 germs。

若仅有普通 Hs 源而没有该 strong presentation，本节只给实际 auxiliary Banach flow 及其有限可定义 charge 守恒；不解决原 DLW 正时间高频 Cauchy 不适定。raw trace 中 τ 的 translation 项另按已知真实空间平移处理，不称 order-zero Hs 场。M=2 的 actual gaps 仍有 §12、§15 的专属标号域；全 M 并未构造统一多分支 gap/norming 坐标。

新增全 M actual 对合、C_n 桥和合法辅助谱流均不证明 nonlinear Hamilton 闭包等于共同微分 annihilator，不构造完整 divisor/norming inverse，也不推出最大各向同性。特别不能由有限 M=3 tensor search、无限有限块独立或 uniform-point Hessian 代替这些非线性缺口。
