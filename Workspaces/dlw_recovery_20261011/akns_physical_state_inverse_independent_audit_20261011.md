# M=2 AKNS 状态逆、复 Birkhoff 转移及原物理 action 对合独审

2026-10-11。独立复核 [akns_physical_state_inverse_bridge_20261011.md](akns_physical_state_inverse_bridge_20261011.md) §§1–5，实际读回其新 §4.2，并直接阅读 Kappeler–Lohrmann–Topalov–Zung 2009 原文 §2.3–2.5、Prop.2.9 及 Yang–Yurko 原文 §§1–2、Theorem 2。没有执行或重跑既存证书。结论是指定图上的完整状态逆与原物理 invariant-action 对合成立；不把 NLS canonical 性转成原物理 canonical 性。

## 1. 实际 periodic gauge 和 holonomy 核对

沿用 S=2δ≠0、q=−S+u、V=−2uv/S、r=[(δ²−v²)(1+u/S)−vx]/S。原 centered split connection 为 [[λ,q],[r,V]]；normalized traceless connection 为 (λ−V)H/2+qE+rF。取

\[
\eta=\operatorname{avg}V,\quad
\theta=D_0^{-1}(V-\eta),\quad
G=\operatorname{diag}(e^{-\theta/2},e^{\theta/2}),
\quad a=q e^\theta,\quad b=r e^{-\theta}.
\]

令 split traceless ψ=G w，直接计算 G^{-1}AG−G^{-1}Gx 得

\[
w_x=\{(\lambda-\eta)H/2+aE+bF\}w.
\]

θ 取周期平均零 primitive，G 周期；所以 actual normalized trace 完全相同，而 full monodromy 需基点共轭。原 rank-one 到 split 的 T=[[d0/S,1],[d1/S,−1]]，detT=−(d0+d1)/S=−1。full framed 数据的 calibration 因此正是 G(0)^{-1}T(0)^{-1}NχT(0)G(0)，不能只保留原 trace 后声称恢复此完整矩阵。

若恢复外部 B=Γ/(2c)，原 rank-one connection 是 B I 加 centered connection(λorig−B)。所以 raw determinant 是 exp[(λorig+B+η)L]，normalized AKNS 参数是 λorig−B−η；作者两式一致。η 是源状态函数，不是新 Casimir；Γ(t) 不被固定为原方程守恒量。

## 2. Φ 的 Sobolev IFT：最低合法层和 derivative budget

对混合源 E_s=H^s_0(u)×H^{s+1}_0(v)，整数 s≥0，a,b∈H^s、θ∈H^{s+1}。s=0 时也成立：H¹(v)⊂L∞，uv∈L²，θ∈H¹，exp(±θ)∈H¹⊂L∞；v² 是 H¹ multiplier，所以 r∈L²。各映射是真正复解析的连续多项式与 exponential/Nemytskii 组合，不需要 q 非零。

背景 u=v=0 给 a*=−S、b*=S/4、θ*=η*=0。因为 V 二次，

\[
D\Phi_0(h,k)=\left(h,\frac h4-\frac{Dk}{S}\right),
\quad \Phi=(P_0a,P_0b).
\]

其精确逆 (f,g)↦(f,S D_0^{-1}(f/4−g)) 是 E_s 与 H^s_0×H^s_0 之间的有界同构，故 IFT 已在最低 E0=L²_0×H¹_0 上给源邻域 U0、目标邻域 V0 和双解析逆。低阶图具有两个势均值的 graph；η 再是该 graph 上的解析标量，不能当独立自由数据。

对 balanced 源 H^s_0×H^s_0、s≥1，a∈H^s、b∈H^{s−1}，同一线性式则给到 H^s_0×H^{s−1}_0 的 IFT。这是不同的源/目标预算，不能声称 balanced Hs² 同阶进入两个 Hs 势，更不能由它直接取得早先 Hs→h^{s+1/2} 图。

## 3. 所有高阶使用同一个低阶 IFT 域

下面补充作者稿每固定 s IFT 之外的同域正则性，不需交无穷个可能趋零的高阶半径。给 (f,g)∈V0∩(HN_0)²，先取低阶逆 u∈L²、v∈H¹。完整势 a=f+α(f,g)、b=g+β(f,g) 已属于 HN，因为 α、β 是标量均值。η=γ(f,g) 同样是标量。由原式重写

\[
u=S+a e^{-\theta},\quad
\theta_x=-2uv/S-\eta,
\quad v_x=(\delta^2-v^2)(1+u/S)-Sbe^\theta.
\]

低阶 θ,v∈H¹。N≥1 时 a,b∈HN⊂H¹，第一式使 u∈H¹；后两式的右端都是 H¹，于是 θ,v∈H²。若已知 θ,v∈H^{k+1}，第一式给 u∈H^{min(N,k+1)}；另两式则给 θ,v∈H^{min(N,k+1)+1}。有限次归纳达到

\[
u\in H^N,\qquad v,\theta\in H^{N+1}.
\]

因此同一个低阶 V0 的所有 HN 目标都有 EN 的源逆，且 Φ(U0∩EN)=V0∩(HN_0)²。各步乘法和一次 D^{-1} 都连续；对两份数据取差作同样归纳，给高阶拓扑连续性。

高阶逆也解析。DΦ 在 U0 的每个点作为 E0→Y0 算子可逆。给 HN 的目标变分，低阶逆变分先在 L²×H¹；线性化上述三式，利用背景已有 HN/HN+1 系数，逐阶提升至 EN。low inverse 的界及有限递推给高阶有界逆。于是高阶 DΦ:EN→YN 是同构，高阶解析 IFT 的局部逆由低阶唯一性等于同一逆；故高阶限制双解析。相同论证给 C∞ 源/目标的分级连续可微逆，没有每阶新缩窗或隐含状态 jet 丢失。

balanced 高阶预算也可在同一低阶图上恢复：若 a∈Hs、b∈H^{s−1}，上述递推先达到 θ,v∈Hs、u∈Hs，再由 θx=−2uv/S−η 得 θ∈H^{s+1}。这里恢复 u,v 各 Hs，仍没有把 b 升成 Hs。

## 4. KLTZ 原文确实是一般复状态逆

已经实际阅读 [published PDF §2.5, Prop.2.9, p.1098](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf)。其零邻域 W 是一般复 L²×L² 的开集，U 是一般复 ℓ²×ℓ² 的开集；映射双解析且双射。相同 W/U 的 HN 与 hN 限制具有逆，N≥0。它不是仅 focusing 实型的 Theorem 1.1；正文在 §2.3–2.4 还给判别式 action 与 Dirichlet-divisor/angle 的复化构造。这里以该已发表定理作为外部输入，不声称独立重证其无限维 inverse theorem。

本稿只转用完整状态逆和加权正则性；该定理所保的括号是 NLS 括号。相关原论文也可由 [DOI](https://doi.org/10.1007/s00220-008-0543-0) 定位。

作者 convention 核对如下：固定 diagonal balancing R=diag(√2,1/√2) 后，a→a/2、b→2b。令 t=x/L，period-one ZS 势为

\[
\varphi_1(t)=-iLa(Lt)/2,\qquad
\varphi_2(t)=2iLb(Lt),
\quad z=\frac{iL}{2}(\lambda_{\rm orig}-B-\eta).
\]

由 iH∂tϕ-wave+offdiag(ϕ1,ϕ2) 的 eigenvalue equation，Dx matrix 的 diagonal 为 −iz/L=(λorig−B−η)/2、offdiag 恰为 a/2、2b，符号正确。背景势是 (iLδ,iLδ)，pair L² norm=√2L|δ|。它落在 focusing 实型，但一般实物理 u,v 给两个独立 imaginary 势，不保持该 focusing 条件；general complex Prop.2.9 正是这里合法的输入。

必须额外要求该背景在论文 W 内，并缩物理图使其势像保持在 W。论文未给数值半径，旧 |δ|<π/L 的 Fourier 阈值不能替代这一假设。因为 W 含零，存在充分小但未量化的 L|δ|>0 满足它；此小非零 S 下原 IFT 半径可依 S 改变。

在这个明示低阶图上，KLTZ 与 §3 的同域 Φ 逆合成，给 EN=HN_0×HN+1_0 到其 Birkhoff hN² **实际像**的完整状态双解析逆。该像是 ambient 复目标中的 codimension-two graph 的 diffeomorphic 像，包含两个势均值约束。η 是其上的状态函数，不额外增加一个独立谱坐标。实际实场则取该复像中的诱导实结构，不能识别为标准 focusing/defocusing 序列实型，也不能向整个 unconstrained hN² 宣称 onto。

## 5. 原物理 Poisson 不等于标准 NLS

独立微分 a,b：δθ=K(c1δu+c2δv)，c1=−2v/S、c2=−2u/S，δr=Aδu+(B−D/S)δv，A=(δ²−v²)/S²、B=−2v(1+u/S)/S。所以

\[
\Lambda=\operatorname{diag}(e^\theta,e^{-\theta})
\left\{\begin{pmatrix}1&0\\A&B-D/S\end{pmatrix}
+\binom q{-r}K(c_1,c_2)\right\}.
\]

这正是作者 (12)。以周期双线性 adjoint、K*=-K、D*=-D 得 J_ab=Λ J_uv Λ*；projected map 在两端加 P0。其局部 M J M* 的四块与作者 (14) 全一致，nonlocal K 项保留。背景 A=1/4、B=0、c=0，直接乘法给

\[
J_{ab,*}=\begin{pmatrix}
0&-D^2/(16S)\\D^2/(16S)&0
\end{pmatrix}.
\]

这是二阶物理张量，标准 NLS 是零阶。因此 KLTZ coordinates 的 canonical 性不能作物理 canonical 性、角括号或最大各向同性的证据。η 的原场恰为 (u_x,v_x)/(8SL)，故其对 a,b 的括号是相同系数的平移；η 不是 Casimir。

## 6. Invariant actions 的 actual 物理对合与 η 项精确消除

实际 readback 新 §4.2 后，式 (A1)–(A8) 独核通过。记 Fλ 是原 centered normalized actual trace，KLTZ discriminant 精确为

\[
\Delta(z;u,v)=F_{\eta(u,v)-2iz/L}(u,v).
\]

这个状态依赖的谱 shift 在变分中给 δΔ=δsourceFλ+F′λ δη，不能预先丢弃。已证明 {Fλ,Fμ}=0、{Fλ,η}=0，以及它们与每个局部 Cm 对合，因此全部 Δ(z) 在原物理括号下彼此对合。

论文 §2.3 的 action 定义为 I_n=π^{-1}∮ z Δz/R dz，R²=Δ²−4，轮廓固定在 period-one z 平面。R 的 canonical branch 在轮廓 annulus 单值且非零。因为

\[
\delta(\Delta_z/R)=\partial_z(\delta\Delta/R),
\]

真正的闭轮廓积分给

\[
\delta I_n=-\frac1\pi\oint\frac{\delta\Delta}{R}\,dz.
\]

无需 arcosh 全局单值，只需 δΔ/R 在 annulus 单值。由 λ=η−2iz/L，F′λ=(iL/2)Δz。η 的变分系数因而是 −iL/(2π)∮Δz/R dz。又

\[
\frac{\Delta_z}{R}=\partial_z\log(\Delta+R),
\quad(\Delta+R)(\Delta-R)=4.
\]

该非零函数的 winding 在连接零势的小 W 上为不变整数；零势时 Δ+R=2exp(±iz)，其 winding 为零。所以 η 系数 **确实精确为零**，不是忽略 η。可把 W 缩为连接零势的小复球，并保持论文 canonical branch 的 source 延拓及所有固定 contour 的非零性；该 integer argument 对每个 n 合法。

所以原物理 Hamilton 场恰为

\[
X_{I_n}=-\frac1\pi\oint_{\Gamma_n}
R(z)^{-1}X_{F_{\eta-2iz/L}}\,dz.
\]

每个固定 contour 的参数路径虽依源，但保持在一个紧谱集合；X_F 对源及参数联合解析。于是 X_In 是 balanced Hs²→Hs² 的解析 order-zero 场，s≥1。这里的流空间是 balanced 源；没有未经证明地宣称其保持最低混合 L²×H¹ inverse-chart 空间。

源梯度的上述轮廓式与 actual F 全族对合给所有 {In,Ij}={In,Fμ}={In,η}={In,Cm}=0，含实际实场上的 Re/Im 成员。这个证明来自原物理 actual trace，不使用 standard NLS canonical bracket。沿各自真实局部流 Fλ 和 η 守恒，故 scalar weights、spectral path 亦可沿轨道冻结；§7 的固定 order-zero flow 及平移等变性方法给同 T 的全部 C∞ 持久性。

这里只对 invariant actions 认证，不对所有 Birkhoff Cartesian coordinates 或 angles 宣称物理对合/正则。固定 n 的 bounds 可以依 n，尚无无限参数流、action-gradient 最大闭包或 strong mixed 域切向结论。

## 7. Yang–Yurko 两边界谱输入另行核实

已实际读取 [Yang–Yurko 原文 §1–2, Theorem 2](https://arxiv.org/html/1503.01748v1)。其系数允许两独立复、绝对连续函数；Theorem 2 给一份固定左条件、两份右端分量条件的双谱唯一性，而非 Banach onto 或加权逆。作者选择 U1=y1(0)、V1=y1(L)、V2=y2(L) 确属其范围，不需 selfadjoint 或 focusing 实性。

独立算 C=[[1,1],[i,−i]] 后 J_D C=C iH；相应 Ω=−C iH(aE+bF)C^{-1}=½[[i(b−a),a+b],[a+b,i(a−b)]]，正是论文的 trace-zero symmetric Dirac 形。两 characteristic functions 是 full normalized matrix 的 X12、X22；detX=1 使其不能有共同零。必须给它们含重数的完整零多集，并使用已定的 AKNS/Dirac frame 与谱参数；只给原 Floquet 特征值不具备这些数据。

所以指定局部物理 inverse-chart 内，两份 calibrated boundary spectra 加 η 的相等确使 a,b 相等，随后 Φ 逆给 u,v 相等。这个输入不要求 KLTZ 的近零 AKNS 半径，但只得 injectivity；不增加 weighted analytic inverse、原物理 action-angle 或全 M 完备性。

## 8. 最终认证范围

原 periodic gauge、Φ 的精确状态逆、codimension-two 势均值 graph、η graph、general complex KLTZ 转移及实际谱 action 的原物理对合全部通过。上文补了同一个低阶 IFT 图上的全部高阶正则性与解析逆，避免逐阶邻域交集为空的缺口。KLTZ 额外背景邻域条件、balanced/mixed budget、实际 image 约束和不同 Poisson 张量均已明确保留。

还缺这些 action 的原物理 norming/angle brackets、nonlinear 最大各向同性与完整 action-gradient 闭包、对真实 strong/mixed-coherent 相域的切向/流不变性、全 M 推广以及一般物理 Liouville 完备性。这是无限维一般函数局部图的实质推进，不能把 M=2 图替代全 M 目标。

本次全部为独立手算、源稿阅读和两份 primary 原文核对；没有运行旧脚本或新增 machine checks，累计独立脚本断言仍为 145。

## 9. 新 §4.3 的 exact 谱 hypersurface 与 gauge section 二审

已实际读取源稿新 (B1)–(B14)，并从原 affine connection、背景 monodromy 与扩展状态图逐项独立计算。结论通过：这是原 codimension-two 势 graph 的确切局部谱描述，允许一个常数对角 gauge 后成为一条中央谱宽 hypersurface；不需要先借 KLTZ 定理。

在原 centered 参数 λ=±S，(B1) 分别成为上、下三角矩阵，对角系数是 u/2±v。指定物理平均叶的两项积分均为零，故两个 diagonal Floquet multipliers 均为一，精确有 F_S=F_{−S}=2。一般非零 off-diagonal monodromy 留下 Jordan 块，因此不能把这两个 monodromy 说成 identity。此前的状态图完全保留了这一点。

背景 full AKNS trace 是 Δ₀(z)=2cos√(z²+L²δ²)。用整个幂级数解释根号处的解析性，在 z=±iLδ 有 Δ₀=2 和 Δ₀′=∓2iLδ≠0。取这两个背景点周围互不相交的固定小圆盘，并按圆盘标号 z₊、z₋；δ 的正负不改变这份标号规则。实际 L²×L² monodromy 对源解析，简单根 IFT 给两根在同一个低阶邻域内解析，随后

\[
\chi(A,B)=(z_+-z_-)^2+L^2S^2
\]

是纯 actual discriminant 的解析函数。原物理谱参数关系 z=iL(λ−η)/2 与 F_{±S}=2 给 z_±=iL(±S−η)/2，因而 χ=0，且 η=(2i/L)(z₊+z₋)/2。后一个身份把物理 holonomy 从中央谱对恢复出来；不能在全 ambient potential 空间预设它与独立物理 η 有这种关系。

独核横截导数不只依赖常数势扰动。在未 rescale 的 AKNS 变量 ζ=z/(iL) 下，背景根处 M²=0。任意 L² 势扰动 δQ=[[0,A₁],[B₁,0]] 的 Duhamel trace 因 cyclicity 精确压成

\[
\delta\Delta(z_\pm)=\int_0^L\operatorname{tr}(e^{LM}\delta Q(x))\,dx
=L^2\bigl(b_0\langle A_1\rangle+a_0\langle B_1\rangle\bigr).
\]

非零 Fourier 模不贡献一阶 trace；没有把一般函数扰动替换为常数势。根微分与平方宽微分继而给

\[
D\chi_0(A_1,B_1)=4L^2\bigl(b_0\langle A_1\rangle+a_0\langle B_1\rangle\bigr)
=-4SL^2(\langle B_1\rangle-\langle A_1\rangle/4).
\]

扩展图 Ψ(u,v,τ,σ)=(e^τa,e^{−τ}b+σ) 的背景微分为 (h−Sτ,h/4−Dk/S−Sτ/4+σ)。其 full L²² 逆确为 τ=−⟨A₁⟩/S、σ=⟨B₁⟩−⟨A₁⟩/4、h=P₀A₁、k=SK(h/4−P₀B₁)。所以低阶 Banach IFT 给实际 onto 的 ambient 状态图，而不是只做维数计数。

在 σ=0 时，常数 reciprocal scaling 是 AKNS 的 exact diagonal conjugation，χ∘Ψ 恒为零。令 H=χ∘Ψ；其严格解析因子可以取

\[
g(u,v,τ,σ)=\int_0^1\partial_\sigma H(u,v,τ,t\sigma)\,dt,
\qquad H=\sigma g,\qquad g(0)=-4SL^2\ne0.
\]

缩小 IFT box 后 g 处处不为零，故 χ=0 当且仅当 σ=0；Ψ 的唯一性再给唯一 small (u,v,τ)。物理像 τ=σ=0 是这条 hypersurface 的确定 gauge section。它在同一个低阶域的全部 H^N² intersections 成立：先取低阶 Ψ 逆与标量 τ，撤销常数 gauge，再使用 §3 的实际物理 bootstrap，得到 u∈H^N、v∈H^{N+1}；不必逐阶缩小半径。

此定理对每个固定 S≠0 有效。只有进一步称中央两根为 KLTZ n=0 pair、搬入其 weighted full Cartesian 图时，才需额外的 published W 邻域条件。它确实推进了物理像描述与 holonomy 的纯谱恢复；尚未证明 χ 是全部 actions 的函数、中央 action 可消元、所有角方向在该物理 section 上自由，更未证明原物理辛商或最大各向同性。上述结论均不能单从 exact gauge section 推出。

本节仅做新源稿阅读与独立手算，无新 machine checks；累计独立脚本断言仍为 145。

## 10. 全 complex discriminant 的 action factorization 独核

已实际读取新 §4.4 的 (C1)–(C9)。本节的 NLS canonical 运算只描述已知谱图，不改变原物理 J。

在 period-one AKNS equation 中 U_z=−izH+iH[[0,ϕ₁],[ϕ₂,0]]。周期 M_z=X_zX_z(1)X_z⁻¹ 满足 M_z′=[U_z,M_z]。actual Duhamel gradients 是 Δ_{ϕ₁}=iM_{z,21}、Δ_{ϕ₂}=−iM_{z,12}。重新计算得到

\[
\partial_t\operatorname{tr}(M_zM_w)
=-2i(z-w)(M_{z,12}M_{w,21}-M_{z,21}M_{w,12}),
\]

而标准 NLS bracket 为 −i 倍最后括号，恰等于上述 derivative 除以 2(z−w)。周期积分为零，同参数按 actual parameter continuity 补齐。L² potentials 下 X、M∈H¹，交换子与积分身份仍实际成立。action 的严格轮廓 gradient 因而给 {Δ(z),I_n}_NLS=0。

KLTZ canonical Cartesian 图中的 I_n=(x_n²+y_n²)/2 产生有限坐标平面旋转。因此每个 holomorphic Δ(z) 对各有限 rotations invariant。必须把这个逐坐标结论提升到真正无限序列；源稿所给 invariant 引理足够，独核如下。

取零点附近一份复 ℓ²² 球，使 F holomorphic 且在较大半径 r 球有统一 bound M。Taylor 齐次项 p_k 的 norm≤Mr⁻ᵏ。每个 finite-support restriction 的旋转 invariant polynomial ring 由 I_n 生成：在 w_n=(x_n+iy_n)/√2、z_n=(x_n−iy_n)/√2 中，旋转权强制每个 monomial 对 w_n,z_n 次数相同。所以 odd p_k=0，p_{2m}=q_m(I)。这些有限支持 q_m 对 restriction 兼容。

给有限 I，选择 x_n=√(2I_n)、y_n=0，不需把平方根当成一个解析 map，只使用它作为 polynomial bound 的见证。由 ||(x,y)||²=2||I||_{ℓ¹}，有

\[
|q_m(I)|\le M(2/r^2)^m\|I\|_{\ell^1}^{m}.
\]

复 polarization 给统一 m-linear bound，至多追加 m^m/m!，与支持数无关；由 ℓ¹ 有限序列稠密性唯一延拓到连续 m-homogeneous polynomial。延拓后的 diagonal bound 保留上式。于是 Σq_m 在 2||I||₁<r² 内正常收敛，给真正 ℓ¹-holomorphic Fhat，且 F=Fhat(I)。finite-support Cartesian identity 再由 ℓ²→ℓ¹ quadratic action map 的连续性延拓到全部序列。compact z 集的 uniform Volterra/analytic inverse bounds 给联合 z,I analyticity。

这证明 Δ(z)=d(z,I)。源稿没有把背景简单根在 zero action 点硬拆开：先构造 entire-in-z 的 d，随后在 nonzero 常背景 I* 附近对 d(z,I)=2 用两个 separate simple roots IFT。由唯一性，它们与 §9 的实际 z_± 相同，χ=χhat(I)，物理 η 亦是其中央根中心的函数。这份域连接正确。

## 11. 中央 action 约束的精确 normalization

对足够小常势 (A,B)，c=L²AB，Δ=2cos√(z²−c)。canonical R=−2i sin√(z²−c)，中央 pair 外取 √(z²−c)∼z。action integrand 给

\[
I_0=-\frac i\pi\oint\frac{z^2}{\sqrt{z^2-c}}\,dz=c.
\]

因为 z²/√(z²−c)=z+c/(2z)+O(z⁻³)，轮廓的 Laurent coefficient 与 orientation 恰给 c。非中央 double gap 的 integrand 在其局部 disk 内解析，故 I_n=0，n≠0。

在物理常背景 A=−S、B=S/4，I₀*=−L²S²/4≠0，且 χhat(I₀,0)=4I₀+L²S²。所以 ∂_{I₀}χhat(I*)=4，ℓ¹ 上 scalar analytic IFT 确使 χ=0 等价于 I₀=ρ((I_n)_{n≠0})。这不是擅自令 I₀ 全叶常数；一般其他 actions 改变时，ρ 也会改变。

这里比仅要求背景落在 published W 多一份小域条件：常背景必须位于上述 invariant-factorization target ball，使其 I* 落在正常收敛 action 球内。对充分小非零 Lδ 可以同时满足，但旧 |δ|<π/L 或未经量化的原 W membership 单独不能自动给这份进一步缩域。源稿明确保留了额外小图条件。

## 12. Canonical mass、constant gauge 与中央 angle 截面

已重新核实 [published KLTZ Proposition 2.9(iii)、式 (2.21)](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf) 的 complex Fourier differential：设 a_n=hatϕ₁(−n)、b_n=hatϕ₂(n)，它的 quadratic action 恰为 a_nb_n。因此 Parseval 的双线性配对给 M^{[2]}=∫ϕ₁ϕ₂=ΣI_n，符号没有相反。

标准 NLS M 的场是 (iϕ₁,−iϕ₂)，real time 2π flow 为 identity 且保持 potential L² norm。constant diagonal conjugacy 保全部 Δ 和 actions，故同一 invariant 引理给 M=m(I) 的 ℓ¹-holomorphic factor。

为严格用 time 2π，先取一份 potential ε-ball，其整个像落入 factorization target ball；forward KLTZ 在零点连续即可做到。再缩小 initial Cartesian representative，使其 potential 落入 ε-ball。real mass circle 保 norm，故整圈保留在此图。canonical {w_n,z_j}=−iδ_nj 给 w_n(t)=exp(−i m_{I_n}t)w_n、z_n(t)=exp(i m_{I_n}t)z_n。对任意 finite-support small actions、I_n≠0 的 balanced representative，两坐标均非零，真实 time 2π identity 强制 m_{I_n}∈Z。

这份导数在 finite-dimensional connected action ball 是 continuous/analytic，故为常整数，零 action 处由连续性补齐；quadratic Fourier identity 给该整数为一。所有 finite supports 兼容，ℓ¹ density 与 derivative continuity 给每个偏导在 full action ball 仍为一，最后沿 tI 积分得 m(I)=ΣI_n。这证明 source (D3)，无需额外导入 trace identity。

complex gauge τ 对应 mass time −iτ，因此原 (A,B)↦(e^τA,e^{−τ}B) 在 Birkhoff 图中恰为 (w_n,z_n)↦(e^{−τ}w_n,e^τz_n)。先由 real-time identity 得到，再以 τ 的 local holomorphic identity theorem 延拓。中央 I₀*≠0 保证 w₀,z₀ 非零，θ₀=(2i)⁻¹log(w₀/z₀) 可选一支，且 θ₀↦θ₀+iτ。故 θ₀=θ₀* 是 χ=0 上合法 local gauge section。

这里只得到真实 analytic gauge section。χ 的 characteristic NLS Hamilton 场不一定就是 mass/gauge 场；不能因此把该状态 quotient 称成已经匹配的 NLS symplectic reduction，更不能移植为物理 (13) 的 reduction。

## 13. 全部非中央 Cartesian 坐标的完整 mixed 状态逆

需要说明背景 noncentral Cartesian pairs 确为零：单在一般 complex 图有 I_n=0，并不强制 w_n=z_n=0。可用 published real defocusing 图的常势 ϕ₁=ϕ₂=t（real small t）。其 n≠0 actions 为零，real x_n,y_n 的平方和为零，故两坐标均零。Φ 的常势 restriction 对 complex t holomorphic，identity theorem 将这一身份延拓到 t=iLδ。于是指定物理常背景确有全部非中央 Cartesian pairs 零。已将这一必要补论证反馈源稿作者。

取任意足够小的非中央 ℓ²² pair (w,z)，quadratic products 给 ℓ¹ actions。ρ 补 I₀，固定 θ₀* 与 I₀≠0 通过两维 analytic IFT 唯一补中央 w₀,z₀。这个填充 map 对 ℓ²² holomorphic，且 derivative 在背景对非中央坐标为 identity；其像精确是 χ=0、θ₀=θ₀* 的 local section。

KLTZ inverse 给实际 AKNS 势。§9 的 ambient chart Ψ 与 χ=0⇔σ=0 给唯一 (u,v,τ)；撤销其 τ gauge 后正是实际 physical graph。反向则从实际物理势选唯一小 gauge 使 θ₀=θ₀*，再读全部非中央 coordinates。这两个 maps 由各段唯一性互逆，没有另设像内约束或自由 holonomy。

所有中央填充、finite scalar gauges 都有界且无导数损失。KLTZ 同低域高阶逆与 §3 的 physical bootstrap 因而给一份 low-domain 的每个 high intersection 上

\[
H^N_0\times H^{N+1}_0\longleftrightarrow
h^N(\mathbb Z\setminus\{0\})\times h^N(\mathbb Z\setminus\{0\}),\qquad N\ge0,
\]

的双解析完整状态图。Cartesian 图允许任意 noncentral closed gaps；不必要求所有 I_n 非零。原实源则取经该图诱导的 reality，不能用 standard NLS focusing/defocusing real sequence 空间代替。

这是 M=2 一般函数局部 mixed chart 的完整 weighted spectral inverse，并有精确 action fiber 描述；源稿新 (C1)–(D6) 核心通过。它仍需要明确保留进一步的小背景/共同 zero-connected target ball 条件，不扩展到全 M，也不证明 nonlinear physical maximal isotropy、physical angle brackets 或无限 action-gradient closure。以上仍要匹配原 order-two pushed Poisson 与真实 strong-coherent 内部相域。

本轮新增审计全部为 actual 文件阅读、primary Fourier normalization 复核与手算；没有新 machine checks，累计独立脚本断言仍为 145。

## 14. 最后 source readback 与同一 strong 图的 actual action regularity

已再次实际读 source 的背景补论证和新 (D7)：作者使用 published defocusing closed-gap Cartesian 定义，在小常势 real-type plane ϕ₂=barϕ₁ 上各非中央 pair为零，随后在两维 constant complex potential 中沿最大 totally-real plane作 holomorphic identity continuation。这确实比 §13 给的单参数常势 continuation更强，并合法；没有从一般 complex product I_n=0推 Cartesian两项零。real mass整圈的 targetball选择也已明确。D7 正确把 all-high restrictions 写为同一低域的 intersections，原 real image定义为整图搬来的 anti-involution fixed set。

同时实际完整读取 [akns_actions_same_strong_chart_genericity_20261011.md §§1–6](akns_actions_same_strong_chart_genericity_20261011.md)。下列 Hessian、索引、real-type 与 Baire 结论独核通过。

旧 physical λ_n=iω_n 对应 dimensionless z_{−n}*=iLλ_n/2=−πnγ_n，故是 KLTZ负索引 −n。背景 w(z)=√(z²+L²δ²)∼z，在该点 w=−πn、w′=γ_n，因此 canonical R₀′=−2iσ_nγ_n。原 actual determinant/Born 算法给 Δ₂(z_{−n}*)=σ_n c_{+,n}bar c_{−,n}。物理 η=O(ε²) 所乘的背景 F₀′(λ_n)=0，故并未漏掉 spectral shift二次项。

由实际 dI=−π⁻¹∮dΔ/R，严格 residue计算给

\[
I_{-n}(\varepsilon\xi)
=\varepsilon^2\frac{c_{+,n}(\xi)\overline{c_{-,n}(\xi)}}{\gamma_n}
+O(\varepsilon^3)
=\varepsilon^2\frac{Lk_n^2}{16S}Q_n(\xi)P_n(\xi)+O(\varepsilon^3).
\]

二次 Hessian 是此 coefficient的两倍。与旧 actual g_n 的比例只对 quadratic terms成立：I_{−n}^{[2]}=−L²γ_n g_n^{[2]}/4；源稿没有把这一系数关系外推为完整 nonlinear gap-action equality，也没在一般 complex势上用 gap-open⇒action-nonzero。

物理 real a,b使 Δ(−bar z)=barΔ(z)。canonical R在freebackground满足相同 antipodal conjugation，保持一份共同 zero-connected branch后仍成立。换变量 z=−bar w的 dz负号与 contourorientation翻转抵消，精确得 I_n=bar I_{−n}，中央 I₀实。这是原物理 induced reality，并非 focusing/defocusing Cartesian real type。

所有 actions先定义于同一个 balanced H¹ source球：实际 a∈H¹、b∈L²，KLTZ图与 invariant-factorization球接受它们。已经构造的同一 holomorphic strong Hilbert parameter map P:B_R(H_C)→E_C² 在 H¹中连续；一次缩 R把整张图送入该共同action域。此处只用 strong图的真实finite real precompositions与 DP(0)覆盖所有finite Fourier directions，不假定finite Fourier初值本身是实际 strong状态。

令 κ_n=Lk_n²/(16S)≠0。取同一组finite Fourier见证 Q=P=1和测试δP=1,i，其 DP(0) 的真实 Hilbert原像给 actual曲线P(εξhat)。所有 DI_{±n}(0)=0，故 D²P不贡献复合 Hessian；actionreal微分矩阵 leadingterm为 εdiag(κ_n,κ_n)，finite minor为 ε^{2N}(∏κ_n²+Oε)，不恒零。各 selectedactions亦有 ε²κ_n+Oε³的非零见证。

每个 action-nonzero集与各finite-prefix minor-nonzero集都在同一个 real Hilbert球开稠密，连通real-analytic identity theorem排除在任意子球恒零。Baire countableintersection给同一实际 strong状态，全部非中央actions非零、所有finite real/complexaction块在actual内部plot方向独立。I₀*非零可由一次连续缩球保全；它是已约束的中央action，不是另一个独立freeaction。

该 residual结论仅在这一固定Hilbert参数球成立。可与已核 charge/gap族的residual集相交，使各族分别有限独立；不宣布它们合并后独立，也不宣布整个 strong相域generic或已有正则Hilbert fiber。

本节实际阅读与手算通过，无新machinechecks。原physical exacttrace-push、同weighted Cartesian phasekernel的闭包审计另见 [m2_physical_trace_bridge_independent_audit_20261011.md](m2_physical_trace_bridge_independent_audit_20261011.md)。累计独立脚本断言仍为145。
