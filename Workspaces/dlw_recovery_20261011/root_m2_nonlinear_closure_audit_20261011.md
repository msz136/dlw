# 原物理 M=2 非线性谱闭包与最大性：根复核

2026-10-11。独立读 [精确场与闭包稿](m2_physical_trace_poisson_closure_proof_20261011.md) §§1–8、[完整谱状态图](akns_physical_state_inverse_bridge_20261011.md) C1–D7、[同一 strong 图的 action 独立性](akns_actions_same_strong_chart_genericity_20261011.md)，并重新计算下列关键连接。仅适用指定 M=2 小非零均匀背景、零组件均值叶和已说明的同一谱图域；不扩成全 M 定理。没有重跑既存证书。

## 1. 物理谱场与规范项

从原 J=−offdiag(D)/16、固定原 centered λ 的实际变分，直接得 g_u=F+AE+2vh/S、g_v=(λ−2v)E/S+2h，其中 W=[[h,E],[F,−h]] 满足真实 adjoint ODE。为完整核对展示式，u_t 的导数展开必须为

\[
u_t=-qF/8+\left[A(S+u)/8-(\lambda-2v)(\lambda-V)/(16S)\right]E
+(\lambda-2v)qh/(8S).
\]

v_t=(λ+2v)F/16−A(λ−2v)E/16−SAh/4。初读源稿的 u_t 展示曾缺上式中的 λ² 项；两个新脚本都从 −Dg_v/16 出发，不依赖该排印式。纠正展示式后，令 R₀=SF+(λv/S−v²/S−S/4)E+(2v−λ)h，逐系数给 V_t=DR₀/(8S)，θ_t=(R₀−平均R₀)/(8S)。进而

\[
D(a,b)X_{F_\lambda}
=\frac{S^2-\lambda^2}{16S}(e^\theta E,-e^{-\theta}F)
-\frac{\langle R_0\rangle}{8S}(a,-b).
\]

后项准确是常数 diagonal gauge。辅助普通 ∫dx canonical tensor 的谱场为 (e,−f)；KLTZ period-one tensor 拉回 (a,b) 后多 i/L，因此与其标准场的系数应是 −iL(S²−λ²)/(16S)。这是具体谱场身份，不是整个物理张量等于 NLS 张量。

物理代表 p 到固定中央角代表 s=g_{γ(p)}p 的微分有额外 dγ·G。由 dϑ₀(G)=i 和 dϑ₀(Ds v)=0，恰得 Ds(v)=Π_s g_*v，Π_s v=v−dϑ₀(v)G/i。谱场 gauge 等变，Π 消去后项，故闭包稿式(15)真正成立；没有忽略状态依赖规范的微分。

## 2. 闭包证明的真正全频步骤

在完整非中央谱图中 I_n=w_nz_n。若每个 I_n≠0，共同微分核的每个坐标对为 c_n(−w_n,z_n)。其有限投影在所有 h^N 中趋于原快速下降速度，无需 c_n 或 I_n^{-1} 的统一界。

标准完整 action 场由固定 contour 的实际 trace gradient 积分得到。对 n≠0，它不改变中央角，所以投影 Π 后仍是单一非中央角方向。用上面的物理谱场身份，在该固定 contour 上除以 (S²−λ²)/(16S)；只需避开 λ=±S 两点，不需全 n 的统一非零界。实际 ODE 对参数在全部光滑半范数中连续，固定 contour 的 Riemann 和遂在同一 Fréchet topology 收敛，每个单角方向属于原物理 trace Hamilton span 的闭包。

有限坐标投影与同低域全部 Sobolev 阶状态逆组合，严格给

\[
\overline{\operatorname{span}_{\mathbb C}\{X_{F_\lambda}(x)\}}
^{C^\infty}
=K_x:=\bigcap_{n\ne0}\ker dI_n(x).
\]

反向包含由原实际 trace/action 对合与每个 dI_n 的连续性。原场共轭将 X_{Fλ} 送到 X_{F\bar λ}；取有限复近似的实部，得到真实 Re/Im trace 场的同一闭包，不要求谱 Cartesian 图属于标准 NLS 实型。

这里不能把 d(I₀=ρ(J),J) 的 reduced 梯度冒充完整标准梯度。投影 trace 场的非中央系数是 d_n−d₀，而 reduced differential 是 d_n+ρ_n d₀；二者一般不同。证明先取完整标准 I_n 的 contour 场，再投影，其 d₀=0，故正确避开了这一潜在漏洞。

### 2.1 实际 action 场的闭包也已证成

另外核对最终稿 §4.4。完整辅助 KLTZ 图的 canonical 恒等式给 DB*=J_pot⁻¹(DB)⁻¹J_seq；同低域高阶逆的微分在每阶 hᴺ→Hᴺ 有界，因此 DB* 对快速下降协向量连续。这里只用辅助图的 canonicity 证明转置正则性。之后仍要组合真正物理 Λ*=(M*−cᵀKjᵀ)E_θ 与原 J_uv；两者至多合损两阶，在全部光滑半范数的 Fréchet 拓扑下连续。

真正 reduced functional 为 F_λ=t(λ−η̃(J),ρ(J),J)，其 β_n=t_n+ρ_n t₀−t_ζ η̃_n 是 ℓ¹ 连续线性泛函的坐标，故 β∈ℓ∞。Cartesian 协向量 (β_n z_n,β_n w_n) 快速下降，有限投影在每阶趋于它。经过连续 J_uv DR*，严格得到 X_Fλ=lim_k Σ_{0<|n|≤k}β_n X_In^physical。反向包含由原 action 变分的实际 contour 积分，其 η 项由绕数消除。故实际 action Hamilton span 与 trace Hamilton span 的闭包相同，均为 K_x；实化后仍成立。没有假设 reduced 图物理 canonical 或用投影标准梯度替代 β。

## 3. 原 Ω 与真正 strong 切向

实际 action 的 η 变分项已由绕数精确消去，故 dI_n=−π⁻¹∮R⁻¹dF_{η−2iz/L}dz。共同 trace 微分核包含在 action 核；反向由完整 discriminant、η 和 I₀ 的纯 action 表达成立。因而两核相同。

真实 trace 场在原 J 上彼此对合，原 Ω 连续，故闭包 K_x 各向同性。若 V 与 K_x Ω 正交，则与所有 trace 场正交，dFλ(V)=0，进而 dI_n(V)=0。所以 K_x^{⊥Ω}=K_x。这是原物理非线性共同微分核的最大各向同性，不是线性 Hessian 的推论。

若 x 位于既有同一 strong 相域 S∞，所有有限 realified trace 流都是合法内部流，保持所有 actions。共同水平集 Y 的内部速度环境像因此包含全部 finite trace span，且包含于 K_x；其 ambient C∞ 闭包恰为 K_x。内部共同微分核 A=j_*^{-1}K_x 也满足 A^{⊥ω}=A。S∞ 的 j_* 单射已由 mixed §16 证明；本项没有重新假设它。尚未解决的是 Y→S∞ 的内部切映射单射与未闭包像等号。

## 4. 适用点确实在同一个 strong 图中存在

同一 strong Hilbert 参数图的背景 action Hessian可直接核算。旧 λ_n=iω_n 对应 KLTZ −n；R₀′=−2i(−1)^nγ_n，真实 trace 二阶项为 (−1)^n c_+\overline{c_-}。轮廓留数得 I_{−n}^{[2]}=c_+\overline{c_-}/γ_n=Lk_n²Q_nP_n/(16S)。因此每个非中央 action 及每个有限 real action Jacobian minor 在同一参数球不恒零。

一次缩小该共同球使全图在谱 state inverse 域，随后 Baire 可数交给同一实际 strong 状态：全部 I_n≠0，每个有限 action 块在真实内部切向独立。其 residual 性仅属于这个 Hilbert 参数球。中央 I₀≠0 由一次连续性缩域保证。

尚未证明普通共同 fiber 为 regular Fréchet manifold、fiber 内部速度未闭包等于 K_x、无限同时 Hamilton 时间、全局 action-angle 或所有 M 的对应非线性逆。无取闭包的 tangent 等号确有 [无限 product-level 例](infinite_product_level_tangent_caution_20261011.md) 所示障碍，必须分别研究。当前一般场全 M Liouville 目标仍 OPEN。
