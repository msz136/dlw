# 全 M 实际谱对合与 vector Riccati 的根复核

2026-10-11。对谱主稿 §16 作独立代数复核，并记录新 vector Riccati 桥的直接推导。这里只认证实际泛函对合和有限阶渐近识别，不认证非线性 Liouville 最大性；未重跑任何既存检查。

## 1. 原场到完整 free bracket

原配对为 hΣ∫，故普通积分梯度的原张量是 −offdiag(P₀D)/h。令 Z_j=e_j−e_m，E 取前 m=M−1 个分量。q 的 p 微分为 Zᵀ/2，d 的 s 微分为 hE/8；q 的 s 微分为 hK_d/8。于是普通积分推前 qd 块为 −ZᵀP₀EᵀD/16=−I_mD/16。qq 块是 −h(K_dZ+(K_dZ)ᵀ)D/16。逐项有 (K_dZ)_{jℓ}=1−δ_{jℓ}−2·1_{ℓ>j}，确为反对称矩阵；dd 块为零。因此全 free 张量准确为 −offdiag(I_mD)/16，不能预先忽略跨分量项。

Δ=q+S+A d 的 A_{jℓ}=sgn(ℓ−j) 也反对称，所以转换到 (Δ,d) 不改变张量。M=2 时 Δ=u、d₀=δ+v，立刻还原已审 Juv；这只作常数校准，全 M 证明依赖上面的矩阵计算。

## 2. 实际 connection、梯度及通用 tensor

原 b_m=−Σd_jΔ_j/S 的非线性项是共同 diagonal scalar；减去 trace 后确实留下主稿 (105) 的 affine traceless connection。d_m=S−Σd_j，Δ_m=0，故 actual gradients 分别是 tr(WH_j)、tr(W(K_j−K_m))，不是所有 M 个 d 的独立梯度。ΣH_i=0 才允许 gradient tensor 写为全 i 的 B。

独核 (109) 先与 B/2 相加减，可准确重组为

\[
R+B/2=\rho\Pi_0+T_s+\sum_iH_i\otimes K_i(b),\qquad
R-B/2=\rho\Pi_0+T_s-\sum_iK_i(a)\otimes H_i.
\]

共同 Cartan 的两个交换子中，H_i 项各自在其非 root 一侧交换，exchange tensor 的两个 root weights 抵消。单 row K_i 的矩阵乘法只含 Kronecker δ；代入 ρ(a−b)=1−ab 后，残差为主稿 (113) 的两项。Θ(i,j,k)=1−s_ij s_ik−s_ik s_jk+s_jk s_ij 在六个互异次序都为零，两重索引用 s²=1 也为零，三者相同为一。因此 Θ=δ_ijδ_jk；剩余两项都是全索引相同的同一 δ，准确相消。这是对任意有限 M 的证明，不使用有限 M 检查作归纳。

括号的积分常数也核过。令 I₁=tr₁₂[B(Wλ⊗Wμ′)]、I₂=tr₁₂[B(Wλ′⊗Wμ)]，则

\[
D\operatorname{tr}_{12}(R Wλ\otimes Wμ)=(I₁-I₂)/2,
\quad D\operatorname{tr}_{12}(B Wλ\otimes Wμ)=I₁+I₂.
\]

真正逐点 identity 是 I₁=D tr₁₂[(R+B/2)Wλ⊗Wμ]。周期分部积分才给 ∫I₁=∫D tr₁₂[R Wλ⊗Wμ]，所以主稿 (114) 的积分式成立。不能把后一式误作逐点式。W 周期，故全部实际 normalized trace powers 及 Newton characteristic coefficients 对合。λ=μ 可由实际 ODE/梯度解析性取极限。

scalar holonomy τ 的直接梯度给 Xτ=(Δ_x,d_x)/(16S)，确为平移；未归一化特征数据也对合。τ 的场有一阶损失，未计为 order zero。固定 λ,r 的 X_F 消去梯度上的 D 后为 tr W[常数矩阵,L]，故 Hˢ→Hˢ order zero，s≥1；其同一 C∞ 时间窗来自空间平移等变性，而不是逐个高阶存在时间的交集。

## 3. 无 q 除法的 vector Riccati 与 scalar 留数系数

对实际 split connection A=[[λ,q],[r,V]]，q 是行向量、r 是列向量。periodic b 满足

\[
b_x+\lambda b=r+Vb-b(qb),\qquad
b=(D+\lambda)^{-1}\{r+Vb-b(qb)\}.
\]

λ>0 大时周期 resolvent 的每个 Hˢ 范数不超过 1/λ；H¹ 是一维乘法代数。对有界 H¹ coefficients，右侧在 O(1/λ) 的 b 球上收缩；参数和源依赖解析。β₁=r、β_{j+1}=Vβ_j−Dβ_j−Σ_{a+b=j}β_a(qβ_b) 的 finite truncation，其 residual 在 H¹ 为 O(λ^{-N})，resolvent 再给一阶 λ^{-1}。在有界 H^{N+2} source 上，线性化同样收缩，故 source C¹ remainder 为 O(λ^{-N−1})。有限矩阵大小只改变常数。

T=[[1,0],[b,I]] 的实际 periodic gauge 给 upper triangular connection [[λ+qb,q],[0,V−bq]]。因此 fast multiplier μfast=exp(λL+Kλ)，Kλ=∫qb；slow monodromy 在 λ 大时保持有界。fast root 与其余根分离，所以 Kλ 是 normalized characteristic coefficients 和 scalar holonomy 的局部解析函数。它由全 M 对合定理与 τ 平移得到实际物理对合。

形式 scalar L=D−q C^{-1}r，C=DI−V。注意 multiplication by b 的 operator 不能与 D 混淆。Riccati 的准确 operator identity 是

\[
r=(C+bq)b-b(D-\lambda),\qquad
L-\lambda=(1+qC^{-1}b)(D-\lambda-qb).
\]

第二式由第一式直接左乘 qC^{-1}，无需 q 非零或除以 q。于是

\[
1-L/\lambda=(1+qC^{-1}b)(1-D/\lambda+qb/\lambda).
\]

形式 Trlog 的 BCH 交换子留数为零。第二因子的每个 λ^{-1} coefficient 是 differential operator，留数为零；第一因子的 log 只有一次项可能含 D^{-1}，留数正是 qb，所有高次项 order≤−2。故实际 Kλ 的渐近 coefficient 是 −C_n，其中 C_n=Tr(L^n)/n。此处形式计算仅识别系数；实际 C¹ remainder 才允许沿真实 fixed-spectrum order-zero Hamilton 场提取 {F,C_n}=0。再次提取两份 actual K 渐近也给各原 C_n 的实际对合。

## 4. 适用范围

上述 affine Poisson/tensor 与 actual C¹ coefficient bridge 允许所有有限 M≥2、S≠0、任意固定组件均值叶和有限幅度。gaps 标号与同点独立另有小背景范围；全频 norming inverse、完整 Hamilton 闭包、共同水平集正则性与最大各向同性仍需独立证明。M=2 的 AKNS weighted inverse 不能直接填补全 M 缺口。
