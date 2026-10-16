# M=2 条件性非线性 Hamilton 完备结构：完整定理陈述

2026-10-11。这是父会话所要求的自足陈述。结论是一般函数域上的条件性 M=2 弱辛 diffeological Hamilton 结构与闭包最大性；**不是标准 Banach/Fréchet 正则积分叶意义的完整 Liouville 定理，也不是一般 M 结论**。与本文对应的用户阅读版见 [HTML](../../report/dlw_m2_conditional_theorem_20261011.html)。

## 1. 原物理条件、平均叶与小背景

固定 h>0、空间周期 L>0、格点数 M=2。Π 是两个格点的平均，P_lat=I−Π 是格点零和投影，D=∂x，〈f〉=L⁻¹∫f。原方程兼容要求 c=Πw 为时空常数、Π(Uw)=Γ(t) 为空间常数。本定理取 c≠0 的一个叶标签，S=hc/4、δ=S/2=hc/8，并采用包含均匀态的组件空间均值叶。

独立真实物理变量 u,v 是任意周期平均零函数，原场准确恢复为

\[
w=(c+8v/h,c-8v/h),\qquad
U=(\Gamma/c-2uv/S+u,\ \Gamma/c-2uv/S-u).
\tag{1}
\]

因此 Πw=c、Π(Uw)=Γ(t) 逐点成立。固定的是〈p_j〉=0（p=P_latU）、〈w_j〉=c 的 Hamilton/Poisson 均值叶；**没有另固定共同 U 均值**，它是 Γ/c−2〈uv〉/S。c 可在不同初值叶之间改变；其沿单条原轨道恒定来自原兼容。Γ(t) 可为任意给定光滑函数，不要求常数或守恒；中心化使用 B(t)=Γ(t)/(2c)。

为真实同一 strong 图的独立性见证，要求

\[
0<|\delta|<\pi/L\quad\text{即 }0<|S|<2\pi/L.
\tag{2}
\]

另有更强、非数值的谱图条件：period-one AKNS 背景 φ*=(iLδ,iLδ) 必须位于 KLTZ Proposition 2.9 的一般复近零邻域 W，且源像可置于后述 action-factorization 所用、连到零势的目标球内。某个充分小的非零 L|δ| 满足这些条件，**(2) 单独不足以保证它们**；原定理未给明确数值半径。局部范围另需中央两个谱根简单、I₀≠0；背景 I₀*=−L²S²/4，故一次缩域可保证。

## 2. 一般函数状态开域、strong 相域和非空性

记 E_N=Hᴺ_per,0(ℂ)×Hᴺ⁺¹_per,0(ℂ)，E∞=(C∞_per,0(ℂ))²，真实子空间取普通场共轭不动点。存在背景附近的**一份低阶开域** O_red⊂E₀=L²₀×H¹₀，其全部高阶交集与一份低阶序列开域满足

\[
\mathcal R:\mathcal O_{\rm red}\cap E_N
\longleftrightarrow
\mathcal U_{\rm red}\cap
\bigl(h^N(\mathbb Z\setminus\{0\})\bigr)^2,
\quad N\ge0,
\tag{3}
\]

双向复解析；所有 N 是同一低域的限制。hᴺ 的权重为〈n〉ᴺ。这是无限函数自由度的完整非中央 Cartesian 状态图，不是有限模截断。坐标为 (w_n,z_n)、I_n=w_nz_n。物理真实源对应由物理共轭经非线性图诱导的反全纯对合，未识别成标准 focusing/defocusing 实型，也未假设该对合在谱坐标全局线性。图 (3) 不宣称原 Poisson canonical。

原物理到 AKNS 的精确过程是 q=u−S、V=−2uv/S、r=[(S²/4−v²)(1+u/S)−v_x]/S，η=〈V〉、θ=D₀⁻¹(V−η)，a=e^θq、b=e^−θr。period-one 势为 φ₁=−iLa/2、φ₂=2iLb，谱变量 z=iL(λ_original−B−η)/2。原 framed 单值矩阵须保留周期 split/gauge 的端点共轭。

完整 AKNS 势的复化物理像复 codim2；原 F(±S)=2 给中央宽约束 χ=(z_+−z_−)²+L²S²=0、中央 center=−iLη/2。完整 discriminant 只依赖 ℓ¹ actions，χ=χ̂(I)，在均匀背景 I* 有 ∂I₀χ̂(I*)=4≠0，故缩域后 I₀=ρ((I_n)_{n≠0})；常数 diagonal gauge 用唯一中央角截面消除。于是 (3) 的非中央 Cartesian 坐标没有额外约束。

真正共同流所在相域 S∞⊂E∞ᴿ 定义如下。枚举全部 C₁,C₂,…，取实际有限层 mixed 中心图 E₀:U₀→E∞ᴿ、E_j:U_j→U_{j−1}，并有 b_{j−1}=E_jb_j。这些实图是其复化局部 Banach holomorphic 图的实限制；新增复轨道留在旧复源域，所有旧时间坐标的正复内窗口一旦确定便一直保留。S∞ 是这些相容链的全部中心值 E₀b₀。有限维 plot p:O⊂ℝᵈ→S∞ 要求局部存在同一链及 smooth ψ_j:O→U_j，ψ_{j−1}=E_jψ_j、p=E₀ψ₀。相域取该 diffeology 及 D 拓扑；ambient 子空间拓扑包含于 D 拓扑，两者相等未证。

存在一份固定 H=ℓ²(ℝ) 开参数球 B_R 及 F:B_R→S∞∩O_red 的光滑/复化 holomorphic 参数映射，其所有有限维 smooth 预复合是上述合法 plots；DF(0) 的像包含每个有限 Fourier 方向。它不是已证明的 S∞ 普通 Hilbert 坐标图或 onto map。精确 action Hessian

\[
I_{-n}^{[2]}=\frac{Lk_n^2}{16S}Q_nP_n,\quad k_n=2\pi n/L,
\quad I_{-n}=\overline{I_n}\text{ 在实源上},
\tag{4}
\]

及同球的解析 Jacobian minors，给 B_R 内 dense residual 非空集 R_I，使 x=F(a)、a∈R_I 满足全部 n≠0 的 I_n(x)≠0，所有有限 real action 块在真实内部方向独立。可与原 P,C₁,… 的各有限块独立条件同时实现。无限自由度由 (3) 的开域与任意大有限 rank 的真实 strong 参数方向给出。

O_red 在自然 mixed Banach 空间中开放，其 smooth 交集为 E∞ 开域。**S∞ 是否相对 E∞ 开放未证；all I_n≠0 的 regular 集只证在这份参数球中 residual，未证它相对 E∞ 或 D 拓扑开放/泛型。** 任一有限 action 块独立是相应参数球的开条件。

## 3. 原真实时间与不变性

Γ=0 的原物理时间准确为

\[
u_t=-u_{xx}-2Sv_x+(2/S)D(u^2v),\qquad
v_t=v_{xx}-(S/2)u_x+(2/S)D(uv^2).
\tag{5}
\]

普通 ∫dx 梯度的 J=−offdiag(D)/16 给 K=∫(16vu_x+4Su²+16Sv²−16u²v²/S)=−16SC₁+4LS³。强 mixed 中心构造给每个 x∈S∞ 的原时间局部真实光滑解以及全部 C_n 的相容逐坐标局部真实流；任一有限支持时间列表有实际共同 germ、交换与局部群律。偶层级的虚时间只用于 mixed 构造，通过反射回到真实原 Hamilton 时间。

这里原 centered 标量算子 ℒ=D−q(D−V)⁻¹r，C_n=n⁻¹∫₀ᴸres ℒⁿdx，res 是 formal D⁻¹ 系数。每个 C_n 本身是实际光滑场的有限 differential-polynomial 积分；C₁=−∫qr，(5) 的 Hamilton 身份是实际变分身份，而非形式解代替真实解。

每个旧时间坐标保持自己的正宽；不定义无限多个同时非零时间，也不宣称任意 E∞ 或 Sobolev Cauchy 初态有流。谱 trace/action 的每个固定实部/虚部还有真实 Banach order-zero 辅助流；这些流与原 C_n 交换，并由保持旧窗口的重新 mixed 参数化接入**同一 S∞**。原时间和这些有限谱流保持 actions、S∞ 和固定均值叶；在所需局部谱图中工作到离开该图前，all I_n≠0 由守恒保持。任一固定有限独立块及其测试 plots 在共同局部时间 germ 内由可逆流保持；不额外声称全 S∞ 的 D-open 初值域上有统一原时间窗。

任意规定 Γ(t) 经 a′(t)=Γ(t)/c、uΓ(t,x)=u₀(t,x−a(t))、vΓ(t,x)=v₀(t,x−a(t))，再代入 (1)，恢复真实原 DLW 流。谱迹须用 λ_original−B(t) 及相应 multiplier 中心化。没有人工固定 Γ。

## 4. 原辛结构、实际积分与准确完备性等式

在 E∞ᴿ 上，D₀⁻¹=K₀ 的原连续弱辛形式是

\[
\Omega(V,W)=\int(J^{-1}V)\cdot W
=-16\int[(K_0V_u)W_v+(K_0V_v)W_u].
\tag{6}
\]

内部切空间 T_intS∞ 取 pointed plot germs 的**代数余极限**。环境求值 j:T_intS∞→E∞ᴿ 已证单射且在同一基点像稠密；ω=j*Ω 代表无关、plot-wise 闭、弱非退化。真实内部 Hamilton 场满足 ι_Xω=dH 并唯一。

积分族可以取实际 original centered normalized trace F_λ、η 及原局部 C_n；它们彼此对合，沿原真实时间守恒。作为 countable 完备谱族，取 A_n=Re I_{−n}、B_n=Im I_{−n}，n≥1，I_n=π⁻¹∮zΔ_z/√(Δ²−4)dz 是实际单值 discriminant 的轮廓作用量。其物理 η-shift 变分由零绕数消除；真实物理 action 场与全部 F_λ,C_n 对合。每个有限 {A_n,B_n} 块在 R_I 的同一状态上独立；不是只给不同有限块的不同见证，也不将 actions 与有关系的 C_n 合并计为独立。

在 x∈O_red∩E∞ᴿ、全部 n≠0 的 I_n(x)≠0，定义

\[
K_x=\bigcap_{n\ge1}\ker dA_n(x)\cap\ker dB_n(x)
\subset E_\infty^{\mathbb R}.
\]

则原物理 Hamilton 场满足

\[
\overline{\operatorname{span}_{\mathbb R}\{X_{A_n},X_{B_n}:n\ge1\}}
^{E_\infty}
=\overline{\operatorname{span}_{\mathbb R}\{X_{\Re F_\lambda},X_{\Im F_\lambda}:\lambda\in\mathbb C\}}
^{E_\infty}
=K_x,
\qquad K_x^{\perp_\Omega}=K_x.
\tag{7}
\]

闭包拓扑是全部空间 Sobolev 半范数的 ambient C∞ Fréchet 拓扑，**不是未经定义的 internal tangent 拓扑或 D 拓扑闭包**。证明用精确谱场身份：mod 常数 gauge，physical X_Fλ 是 (S²−λ²)/(16S) 倍辅助 J₀_ab=[[0,1],[−1,0]]、普通 ∫dx 梯度的 canonical trace 场；KLTZ 标准场拉回 (a,b) 是其 i/L 倍，故相应物理权重为 (L/i)(S²−λ²)/(16S)。full action contour 先生成单角方向再投影；固定 contour 避开 λ=±S；有限 Riemann 和与 rapid Cartesian 截断在全部半范数收敛。实际 action span 的相同闭包还用 DB* 的标准 canonical 转置正则性、真实 Λ* 和原 J 的连续性；未将整个物理张量换成 NLS 张量。

若再有 x∈S∞，内部共同微分核 A_x=j⁻¹K_x 满足 A_x^{⊥ω}=A_x。真实共同水平集 Y_x={y∈S∞∩O_red:I_n(y)=I_n(x),n≠0} 取 subset diffeology。其内部速度的环境像 V_x 满足

\[
V_x\subset K_x,\qquad
\overline{V_x}^{E_\infty}=K_x,\qquad
V_x^{\perp_\Omega}=K_x.
\tag{8}
\]

**没有证明** T_intY_x→T_intS∞ 单射、V_x=K_x 的未闭等号、Y_x 为 regular Banach/Fréchet 流形、完整 torus 或标准 action-angle 积分叶。因此 A_x 的最大各向同性不能改名为未证的真实 fiber tangent 最大各向同性。闭隙 critical 点不受 (7) 覆盖；在均匀态，谱场全为零而共同微分核是全空间。

## 5. 借用定理、分析复核与定位

关键外部来源是 Kappeler–Lohrmann–Topalov–Zung, *Birkhoff Coordinates for the Focusing NLS Equation*, Communications in Mathematical Physics 285 (2009), 1087–1107，[DOI](https://doi.org/10.1007/s00220-008-0543-0)，**§2.5 Proposition 2.9，p.1098**。已在 published 全文核对相关 §2.3–2.5 及其一般复 L²² 近零邻域命题；只取其双解析 Cartesian 谱逆、同一低域所有 Hᴺ/hᴺ 阶、标准谱 action 与 auxiliary canonicity。一般真实 DLW 的 a,b 不满足标准 NLS 实型，故借一般复命题而非 focusing/defocusing 主定理。势缩放及 η 谱移已经准确匹配；外部定理不是物理 Liouville 结论。Yang–Yurko 两边界谱唯一性不是 (3) 加权 onto 逆的来源；一阶 smoothing 备用文献也不是 (7) 的必要依赖。

三条独立复核线均覆盖分析依赖而非仅有限代数：mixed 审查强 mixed 解与保旧窗口、真正 internal tangent/Ω、同图 Baire；zero 审查同低域高阶逆、KLTZ 适用/实型、action-factorization、轮廓/转置 Fréchet 收敛及 scope；fresh closure-chain 审查中央截面微分、full-vs-reduced gradient、实际 action 截断、realification、内部核与 fiber 区分。它们核验的是明确局部条件和推导，不提供外部定理未公布的数值半径或无限参数流。15/16 项机器证书只认证有限谱场代数身份，未代替这些分析证明。

定位：

* [完整物理状态与谱逆](akns_physical_state_inverse_bridge_20261011.md) §§2.2、4、4.3–4.5（B1–B14、C1–D7）；[状态独审](akns_physical_state_inverse_independent_audit_20261011.md) §§10–14。
* [同一 strong 图非空性与 action 独立](akns_actions_same_strong_chart_genericity_20261011.md) §§1–6；[强域原构造](../../刘维尔可积性/research/mixed_independent_review_20261011.md) §§11–13、16–17。
* [真实 action/strong 流独审](akns_actions_strong_domain_independent_audit.md) §§3–5；[实际谱 strong 输送](spectral_m2_strong_domain_flow_bridge.md) §§4–5。
* [精确物理场及闭包定理](m2_physical_trace_poisson_closure_proof_20261011.md) §§2–8，特别(15)、(17)、(24)、(27)–(30)、(35)–(38)。
* [mixed 独审](m2_physical_trace_bridge_independent_review.md) §§6–10；[zero 独审](m2_physical_trace_bridge_independent_audit_20261011.md) §§1–8；[fresh 链独审](m2_physical_trace_closure_chain_independent_review_20261011.md) §§1–7；[根复核](root_m2_nonlinear_closure_audit_20261011.md) §§1–4。

一般 M 的 nonlinear norming 逆与 Hamilton 闭包仍在继续；原用户一般场 Liouville 目标保持 OPEN。
