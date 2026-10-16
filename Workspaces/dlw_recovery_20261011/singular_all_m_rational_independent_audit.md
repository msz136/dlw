# 全 M 三阶有理图、dual twists 与实际物理桥独立审计

2026-10-11。续审 singular_zero_flux 的 exact constrained-KP 路线，独立核算有限 rank 表示、像内约束、规范均值和 flagged physical 回拉的必要依赖。§8 进一步复核已保存的新实际 mixed 流稿，补齐最小分式的微分桥，并认证指定图的真实 mixed 轨道；不宣称任意初态 Cauchy 流，不重跑既有证书。

## 1. 精确有理表示

令 M≥3、n=M−3、a=a3≠0，并在完整 bubble 图中写 P=Q−1R，Q、R 为 monic M 阶微分算子。原层 c=Γ=0、χ=κ≠0 给 R−Q=aK，其中 K 为 monic n 阶微分算子，a=hMκ/16 为空间常数。因此

\[
P-I=aQ^{-1}K,\qquad
\boxed{W=a(P-I)^{-1}=K^{-1}Q.}
\]

这是精确阶三有理 PDO，不能用一般阶三算子近似替代。n=0 时 K=1，回到已经认证的 M=3 微分图。

## 2. 全阶 finite-rank negative part 与 reciprocal twists

对 n>0，取 K 的任意 fundamental solution basis φ1,…,φn，companion matrix F 的第 i 行第 j 列为 D^{i−1}φj；Wronskian det F 在全圆无零。置

\[
w_i=(F^{-1})_{i,n}.
\]

variation-of-constants 精确给 formal inverse

\[
\boxed{K^{-1}=\sum_{i=1}^n\phi_iD^{-1}w_i.}
\]

w_i 是 adjoint K* 解。formal 逆不携带 ODE 积分常数；若要解释为某个 Hilbert 空间上的实际逆，还需另说明边界/Floquet 是否有 multiplier 1，不能把 formal D−1 任意当 periodic 实际逆。

对任意微分 B，Leibniz 展开给

\[
(fD^{-1}gB)_-=fD^{-1}B^*(g),\qquad
(BfD^{-1}g)_-=B(f)D^{-1}g.
\tag{A}
\]

所以

\[
\boxed{W_-=\sum_i\phi_iD^{-1}\psi_i,\quad\psi_i=Q^*(w_i).}
\tag{B}
\]

ψ 的符号由 formal adjoint 决定。例如 B=D 时 negative part 为 −fD−1gx，正是 B*g=−gx。

若 φi(x+L)=ρiφi(x)，则 wi、ψi 的 twist 是 ρi−1；ρi 不必等于 1。故每个 φi ψi^(r) 及所有 W 的 formal coefficients 周期，Σφiψi 也周期。不得各自强改为 periodic 而丢掉真实 twist。

simple Floquet 并不是 (B) 必需条件。明确 matrix 约定：把 φ 写成 basis row，F(x+L)=F(x)C，则 φ(x+L)=φ(x)C、dual column w/ψ 在 x+L 变成 C−1w/ψ，故 φD−1ψ 保持。若改用 basis column，才是 φ→Cφ、dual→C−Tψ。两种转置约定不能混写。Jordan 或复杂共轭块可保留 matrix twists；实 W 要使用实 fundamental basis 或匹配复杂共轭数据。

## 3. 反向表示没有额外 differential 像内约束

反过来，给定 φ 的非零 full Wronskian，定义其唯一 monic annihilator K；给任意匹配 dual twists 的 ψ 与周期 u,v，令

\[
W=D^3+uD+v+\sum_i\phi_iD^{-1}\psi_i.
\]

由 (A) 和 Kφi=0，

\[
(KW)_-=\sum_i(K\phi_i)D^{-1}\psi_i=0.
\]

故 Q:=KW 恰为 monic M 阶微分算子，不需要再施加一个无穷阶 KW differential 条件。置 R=Q+aK，则 P=Q−1R=I+aQ−1K，W=a(P−I)−1。若 Q、R 保留指定物理 bubble/flag 图，P−I 的阶 −3 与首系数 a 自动给 c=q=0、χ=16a/(hM)。

Wronskian 全 rank、Q/R 的物理 partial flag Wronskians 和所有 inversebubble 异类差非零是不同的条件；不能只凭 K 的 full Wronskian 非零省略后两者。ρK=1 只影响 K 的实际 periodic inverse，不破坏上面的 formal coefficient 代数或 KW differential 恒等式。

## 4. canonical cKP 时间及 Q/R 核的真实输运

置 B0=D²+2u/3。若

\[
W_t=-[B_0,W],\quad\phi_{i,t}=-B_0\phi_i,
\quad\psi_{i,t}=B_0^*\psi_i,
\]

则 (A) 核实 negative part；positive part 精确给

\[
u_t=u_{xx}-2v_x,
\]

\[
v_t=-v_{xx}+2u_{xxx}/3+(2/3)uu_x-2D\sum_i\phi_i\psi_i.
\]

特别 [D²,φD−1ψ]+ 的零阶项为 2D(φψ)，没有漏掉 source 的符号或系数。取 z=v−u_x/2、Ψ=z+i u_x/(2√3)，中心方程为

\[
\Psi_t=-i\Psi_{xx}/\sqrt3+(2/3)uu_x-2D\sum_i\phi_i\psi_i.
\]

源项依靠 heat 的一阶空间时间 smoothing 控制，不能把它当无导数损失的 Ψ-only 多项式。

φ 的真实时间方程给 K_t−KB0 annihilate ker K，故存在 monic 二阶 A 使

\[
\boxed{K_t=KB_0-AK},\qquad A=(KB_0K^{-1})_+.
\]

因此

\[
\boxed{Q_t=-AQ+QB_0,\qquad R_t=-AR+RB_0.}
\tag{C}
\]

一般不能误写成 Q_t=−[B0,Q]；仅 n=0 时 A=B0。式 (C) 仍给 Qf=0 或 Rf=0 的真实时间输运 f_t=−B0f，以及 P_t=−[B0,P]。在 M 维空间解系统上消去高阶 x 导数后，这是有限维 periodic zero-curvature 输运，足以保持 kernel monodromy 的相似类和既定 invariant flags；没有求 arbitrary backward-heat Cauchy 问题。

## 5. 共同 U 均值必须由该图确定并恢复

一般 W 的 D² 系数为 w2=AQ−AK，其中 AQ、AK 是 Q、K 的次首系数。共同 U=0 图有 avg AQ=0，但并不保证 avg w2=0；若 m=avg w2，则周期规范 ζx=(w2−m)/3 只能留下 mD²，完全去项 ζx=w2/3 是准周期，改变 φ/ψ twists。

一种清楚的 canonical 选择是在 actual physical 图中直接要求 W=D³+uD+v+source。此时 AQ=AK。周期 bubble 的 log 导数积分为零，c=0 又给 numerator/denominator 的均值和相同，因此

\[
\boxed{\mathsf B_*:=\operatorname{avg}\Pi U
=-2\operatorname{avg}A_Q/M
=-2\operatorname{avg}A_K/M.}
\]

若 K 的 scalar Floquet 指数为 μi，这就是 B*=2Σμi/M；matrix 情形用 (1/L)log det monodromy 的真实和，不任意更改 log 分支。twists 固定则 B* 沿流恒定。B* 是这个表示图恢复的原共同零模，不能未经说明替换成零。

实际 P 的真实生成元在常平均 B* 下是 D²+V，系数周期。W 的 D² 项为零强制 Vx=2ux/3，时间 scalar 不影响交换子，遂得到 canonical B0。若先从共同 U=0 的图去项，须同时把所有 twists 与 Q/R 的实际共同场值改变；这是同一个图选择，不是丢掉原零模。

对任意预先规定的光滑原平均共同场 B(t)，令 Δ=B−B*、τ=∫Δ，精确恢复

\[
p_B=p_*(x-\tau,t),\quad s_B=s_*(x-\tau,t),
\]

\[
\boxed{U_B=U_*(x-\tau,t)+\Delta(t).}
\]

这保留所有 p/s 组件空间 Casimir 均值。a=hMκ/16 是初态选取、原约束链守恒的能量轨道值，不是额外把 κ 改成 Casimir。

## 6. 根的新实背景非空性证明复核

已读 [real_rational_background_20261011.md](../../刘维尔可积性/research/real_rational_background_20261011.md)，未重跑根证书。其 Q*=∏(z−αj)、K* 根避开 α、R*=Q*+aK* 的全 M 实简单图构造正确。

由 degree(R−Q)=M−3，Newton 给 Σξ=Σα、Σξ²=Σα²、Σ(ξ³−α³)=−3a。每一格点直接恒等式

\[
(\alpha+\xi)^2\frac4h(\xi-\alpha)
+\frac{h^2}{48}\left[\frac4h(\xi-\alpha)\right]^3
=\frac{16}{3h}(\xi^3-\alpha^3)
\]

故 κ=−16Σ(ξ³−α³)/(3hM)=16a/(hM)，与 a3=a 完全一致。Q/K 互素给 Q/R、R/K 也互素；每个 ξj−αl 非零，常系数 bubble 的全部异类交换合法。|a| 足够小时每个 Q 实简单根附近 R 仍有实简单根的 perturbation 证明完整，a 两种符号均提供非空背景。

该稿采用 Σα=0，所以原 actual B=0，而 W 的常二阶项 m=Σγi 一般不零。对所有 Q/R/K 施加 constant gauge f=m/3，所有根增加 f、W depressed、U 的均值增加 2m/3，p/s 和 κ 不变。新的 K 根 μ 满足 Σμ=M m/3，故新的 B*=2Σμ/M=2m/3，正好对应上一节 canonical 图。非空性无需修改或重跑。

该背景及其一般函数邻域保留 component means 由标号 Floquet 值选取的范围，不覆盖每个预定均值叶。尤其严格所有组件均值零时 Q/R 倍子通常重复 1，不能沿用 simple-labelled operator inverse。可保留原初态的 invariant flags 并沿 (C) 输运来尝试共振扩展，但必须证明 flagged derivative/time bridge；裸 unflagged operator 的单射性在该叶不可假设。

## 7. 实际 mixed 流的依赖与范围

finite-rank 表示、dual twists、KW differential、全 M 非空实物理图及 canonical 零模恢复已通过本独立审计。真正的 nonlinear mixed contraction 还须逐项处理 φ 给末端、ψ 给始端、Ψ 给 Cauchy 数据的 heat/Schr Banach 空间估计、共同光滑时间窗、Wronskian/physical flags/inversebubble 开条件、最小分式和 ambient 标号逆的微分；这些依赖在 §8 完成复核。

dual-twisted heat 在 periodic 坐标下有常一阶 drift，必须保留真实 quasi-periodic twist，不能把端点 φ/ψ 自动改成 periodic。DΣφψ 的中心源由 L²_tH^{s+1} heat smoothing 和 L∞_tHs 乘积控制得到 √T 因子；完整收缩核算见 §8。

mixed 边界轨道存在性也不等于任意原物理初态的 Cauchy 流，尤其 M>3 有真实 backward heat 主模。全阶共同 Hamiltonian 时间、谱迹独立性及 Liouville 完备性仍须另证。

与此独立的 exact paired tangent projector 已完整保存于 [singular_paired_tangent_projector_20261011.md](singular_paired_tangent_projector_20261011.md)，包括所有 holonomy 下的增广一阶逆，以及振荡中心块的必要 periodic Mizohata 平均条件。

## 8. 新全 M 实际 mixed 稿的最终独立核算

已读 [singular_ckp_actual_mixed_flow_20261011.md](../../刘维尔可积性/research/singular_ckp_actual_mixed_flow_20261011.md) 全文。以下是足以独立认证其指定图定理的补全证明；作者已收到全部公式修正。没有运行作者新证书或旧证书。

### 8.1 常 twist heat、源项 smoothing 与 analytic 固定点

φ=e^{μx}f、ψ=e^{−μx}g，真实 μ 固定时，周期 f 的末端问题反转时间后生成元 (D+μ)²，周期 g 的始端生成元 (D−μ)²。Fourier 符号均为 −k²±2iμk+μ²，drift skew，低阶真实增长只为 μ²。标准逐模或能量积分给与 T≤1 一致的 C_tHs∩L²_tH^{s+1} 范数，以及 forcing L²_tH^{s−1} 范数。

对 s>1/2，Hs 是乘积代数，

\[
\|D(fg)\|_{L^1_tH^s}\le C_s\sqrt T
\big(\|f\|_{L^2_tH^{s+1}}\|g\|_{C_tH^s}
+\|f\|_{C_tH^s}\|g\|_{L^2_tH^{s+1}}\big).
\]

u=m0+2√3D−1ImΨ 属于 C_tH^{s+1}；uu_x 的 Schr forcing 为 L¹_tHs，带 T 因子，u f/u g 的 heat forcing L²_tH^{s−1} 带 √T 因子。差分遵守同一双线性估计。因此 mixed Duhamel 映射在

\[
X_T^s=C_tH^s\times(C_tH^s\cap L^2_tH^{s+1})^{2n}
\]

的低阶有界球中以 C_R(T+√T) 收缩。线性 heat endpoint 轨道的 L²_tH^{s+1} 范数无需趋于零，收缩仍有源项的外部 √T，故这里没有隐藏“高阶初态导致 T 趋零”的要求。

非线性是实 Banach 空间上的连续多项式，线性 solution operators 有界，收缩或 analytic implicit function theorem 给同一低阶邻域的实解析数据解映射。ImΨ 平均零、m0 与 avg ReΨ 都保持；f/g 在真实 twist-reduced 周期坐标中保持实值。原稿 (10) 的 uu_x 前应有加号：Ψt=−iΨxx/√3+(2/3)uu_x−2DΣfg；这是排版遗漏，前后实际方程均支持该加号。

### 8.2 所有高阶保持同一个非零时间窗

周期变量方程、D−1、D±μ 和 mixed endpoint operators 全与空间平移交换。对光滑数据，h→T_h data 是低阶数据 Banach 空间内的 C∞ 曲线；analytic 解映射与平移等变性给 h→T_h solution 是 X_T^s 内的 C∞ 曲线。平移群闭生成元的判据遂给每个 ∂x^r solution∈X_T^s，全部阶共享刚取得的同一个 T。方程再依次给全部时间导数。这一方法足以严格证明 C∞(t,x) 持久性，不需要逐阶另作小时间收缩。

一开始选一个足够大的有限 s0，控制 K/Q/R 系数、monodromy/partial Wronskians 和最多 N=M(M−1)/2 次 inversebubble 所需的有限 C^k 距离。常背景的 baseline f/g 只含时间指数缩放、乘积常数，低阶连续性和一次缩短 T 保持全部开图条件；高阶持久性仍使用这个 T。

### 8.3 原 shape closure 如何保持 actual W2=0

不能仅把“原一致性保持 W 的二阶项”当成无解释的假设。原 a3/χ 一致性及 monic 商 Lax 给 actual w2,x=0。选平均实际 U 为常数 B*，共同 scalar θx=b/2 的 θt 可以取周期，因此 actual P/W 的生成元 D²+V 的 V 周期。其 W 的 D² 系数满足

\[
w_{2,t}=-2u_x+3V_x\quad\text{当 }w_{2,x}=0.
\]

积分即 avg w2,t=0。初始 actual w2=0，结合 shape closure 的空间常数性，给 w2 恒为零；于是 Vx=2ux/3，exact 原时间生成元就是 B0=D²+2u/3（mod 时间标量）。B* 的值由 §5 的实际 mean 公式确定，没有默设 B=0。

### 8.4 最小分式的微分桥：右 Bezout 的方向和 periodic 实现

仅 Pdot 相同，不应未经说明就判 Qdot/Rdot 相同；raw φ/ψ 还有常 GLn 基底冗余，也不能称作裸可微互逆。下面直接在最小 monic 分式中证明原物理与构造轨道的 (Q,R) 向量相同。

在根的新常背景图，Q/R 的根互不相交，故各自正实 Floquet 谱互不相交，并在足够小邻域保持。尤其它们没有共同 left/right 微分因子。所需右 Bezout 的方向是

\[
\boxed{Q C_B+R D_B=1.}
\]

不必假定所有光滑函数是抽象 Ore 系数域。对 Q*、R* 构造 left Sylvester 系数矩阵：求阶 ≤M−1 的 C_L,D_L，使 C_LQ*+D_LR*=1。这里乘子的系数放在最左，Leibniz 只对已知 Q*/R* 系数微分，所以是有限个点态线性方程。常背景矩阵就是 classical Sylvester/resultant 矩阵，因根分离而可逆；有限 C^k 邻域内它全圆一致可逆，所得乘子系数光滑、周期。adjoint 给 C_B=C_L*、D_B=D_L*，恰得上面的右 Bezout。

由 Pdot=P B0−B0P，直接微分 P=Q−1R 得

\[
C:=(Q_t-QB_0)Q^{-1}=(R_t-RB_0)R^{-1}.
\]

右 Bezout 使

\[
C=(CQ)C_B+(CR)D_B
\]

为实际周期微分算子。令 A=−C，最高阶是 D²；monic Qt 的 D^{M+1} 系数迫使 A 无 D 项，D^M 系数给 A0=2u/3−2(AQ)x。AQ=AK=k1，所以

\[
\boxed{A=D^2+2u/3-2k_{1,x}},\quad
Q_t=QB_0-AQ,\quad R_t=RB_0-AR.
\]

这与实际 mixed 构造的 Darboux pair 完全一致。因而原向量和构造向量在完整 ambient Q/R 图中的推前相同；simple-labelled flag inverse 和每一次 inversebubble 的可微互逆再给物理向量相同。没有使用 raw φ/ψ 坐标单射性，也没有把 bare P 的集合单射性冒充微分论证。

### 8.5 认证后的结论及未完成项

上述补全足以认证：对每个有限 M≥3，明确非空的简单正实、互素、非零旗标/交换差的有理物理图内，充分近背景的光滑 mixed 数据（Ψ 始端、φ 末端、ψ 始端，及 a/μ/m0 参数）产生同一非零窗上的唯一真实原 DLW mixed 轨道。其有限阶正则性损失的物理重建仍给完整 C∞ 时间解，并保留 κ、p/s 组件均值及任意预先给定 B(t) 的准确恢复。这个认证不把初态限在常背景族或两幅值 ansatz。

它仍不是每个物理初态的 Cauchy 解定理，也不覆盖 strictly zero-component-mean 的共振旗标图。高阶 commuting Hamiltonians 的真实共同时间、mixed 弱辛边界关系、谱迹独立性和 Liouville 完备性继续开放。本次新增审计是纯新推导与新稿逐项阅读，没有重跑任何既存证书；先前本代理独立 assert 计数仍为 145。

## 9. c=0、Γ非零的二阶真实 mixed 扩展末审

已实际阅读作者新保存的 [singular_ckp_actual_mixed_flow_20261011.md](../../刘维尔可积性/research/singular_ckp_actual_mixed_flow_20261011.md) §6，并独立从原约束链、actual 因子 Lax 和有限秩恒等式推导。完整依赖与函数空间证明保存在 [c0_nonzero_flux_rational_mixed_independent_audit_20261011.md](c0_nonzero_flux_rational_mixed_independent_audit_20261011.md)。以下公式全部通过本次独立数学复核。

原 q=Γ(t) 周期一致性强制 Γt=0，闭合为 b=(χ−avgχ)/(2Γ)+B(t)。取 a=−hMΓ/8、n=M−2，W=a(P−I)−1=K−1Q 的 actual depressed 图为 D²+u+ΣφD−1ψ。原共同场为零的商代表 hat w1=χ/(2Γ)，actual w1=hat w1−b，因此正确 canonical 平均是

\[
B_*=\frac{\operatorname{avg}\chi}{2\Gamma}
=-\frac{H_0}{hML\Gamma}
=\frac2M\sum_i\mu_i.
\]

这里 Γ、能量和 twists 可随初態参数变化，B* 沿指定原轨道守恒；均未被改成相空间的外加固定常量或 Casimir。原 shape 先使 actual w1 空间恒定，实际周期生成元 D²+V 给 w1,t=−2ux+2Vx，积分及初始去项使 w1 始终零、Vx=ux。故真实原时间恰为 Wt=−[D²+u,W]。

因为 K0=W+=D²+u，positive/negative 分部精确是

\[
u_t=-2D\sum_i\phi_i\psi_i,\qquad
\phi_{i,t}=-(D^2+u)\phi_i,\qquad
\psi_{i,t}=(D^2+u)\psi_i.
\]

特别没有漏掉 uxx 项。Reciprocal twists 化为周期 f/g 后仍须保留 D±μ 的真实 heat drift。s>1/2 的 C_tHs(u) 与两份 C_tHs∩L²_tH^{s+1} heat 空间中，中心源 D(fg) 的 L¹Hs 范数有 √T，uf 的 L²Hs−1 有 √T；差分以 C_R√T 收缩。实解析低阶解映射加平移等变性给同一个非零窗的全部光滑持久性。这证明 actual mixed 轨道，没有把 backward heat 改称任意物理 Cauchy 流。

全阶 finite-rank 表示与反向 KW differential 依旧成立。此时 Kt=KK0−AK、Qt=QK0−AQ、Rt=RK0−AR，A=D²+u−2k1,x；§8.4 的实际右 Bezout 方向、adjoint Sylvester jet 非退化和整对 ambient flag/inversebubble 微分桥逐项适用。因此原向量和重建向量确实相同，不能只以裸 Pdot 相同取代这一步。

非空图可取 Q/K 实简单且互素、R=Q+aK，|a| 小并保持所有 real roots。作者 §6 额外令 Q/K 根和相等只是直接选择 canonical depressed 常背景，不是必须的物理约束；一般不同根和用同一 constant scalar gauge 去项。Newton 第二阶差 Σ(ξ²−α²)=−2a，给 Γ=−8a/(hM)，两种 Γ 符号均有合法图。M=2 时 K=1、n=0、ut=0，simple-labelled inverse 给 canonical p/s 静态；任意规定 B(t) 都由 Δ=B−B* 的空间平移及共同 U 加量恢复。

末审结论：作者 §6 的二阶层全 M actual mixed 定理已获得独立认证，限定于明示的非空、简单实正 Floquet、full/partial Wronskian、交换差及 Sylvester 合法图；一般函数邻域不限为常背景族。该结果与三阶定理共享严格零组件均值共振图、任意 Cauchy 初态、高阶共同实际时间和 Liouville 完备性的缺口。没有执行或重复作者的 13 项新证书，也没有重跑旧证书；本代理累计独立脚本断言仍为 145。
