# M=3 零通量实际流独立复核

2026-10-11。独立复核 [singular_m3_actual_flow_20261011.md](../../刘维尔可积性/research/singular_m3_actual_flow_20261011.md) 的 §§1–3。只写本审稿与新的因子证书，不修改共享记录、不重跑先前 81 项。

结论：实标量局部流、共同光滑时间窗、周期去项、实 labelled Floquet 旗标均正确。原稿最后从静态逆的单射性推论向量场相等，省略了微分层面的论证；下文给出一般六系数 ambient 互逆图和原 PDE 的直接因子零曲率，补齐这一步。因此在指定非共振实 M=3 图内，完整兼容光滑初值确有原物理方程的唯一双向局部光滑流。这个结果不依赖初值保持在两幅值特殊族；它仍只属于 M=3 的指定物理图，不能替代全 M、所有均值叶或 Liouville 完备性。

## 1. 标量实时间流与共同光滑时间窗

零平移框架中

\[
u_t=-2z_x,\qquad z_t=u_{xxx}/6+(2/3)uu_x.
\]

取 α=1/(2√3)、Ψ=z+iαu_x、m=avg u。其非线性明确为

\[
N(\Psi)=\frac{2m}{3\alpha}\operatorname{Im}\Psi+
\frac{2}{3\alpha^2}(D^{-1}\operatorname{Im}\Psi)\operatorname{Im}\Psi.
\]

要求 ImΨ 平均零，D−1 取零平均逆。N:L²→L² 局部 Lipschitz，因为 D−1:L²₀→H¹→L∞；因此真实酉组 exp(−itD²/√3) 上的 Duhamel 收缩给双向 L² 时间窗。原稿 Fourier tame 估计也正确：在卷积中分配权重后，两项分别以 (weighted a_n/n) 的 ℓ¹ 和 a_n/n 的 ℓ¹ 控制；Σn≠0 n−2 有限给出所写的 H^r 两项估计。因而

\[
\|N(\Psi)\|_{H^r}\le C_r(|m|+\|\Psi\|_{L^2})\|\Psi\|_{H^r},\quad r\ge0.
\]

先取得 L² 流，再对每个 H^r 局部解作 Gronwall 和延拓，所有阶均保持到同一个 L² 时间窗；不是对各阶分别选趋零时间。光滑数据得到同一窗上的真实 C∞(t,x) 解。非线性平均为 ∫uu_x=0，故 ImΨ 平均零、m、avg z 全部保持。重建 u=m+α−1D−1ImΨ、z=ReΨ 后精确恢复实方程，不需要复时间旋转。

能量 ∫[z²+u_x²/12−u³/9] 的变分为 (−u_xx/6−u²/3,2z)，方程是 −offdiag(D) 的 Hamilton 流。u*<0、固定均值时二次型 ∫[η²+w_x²/12−u*w²/3] 正定。这个核对仅支持局部实型，不增加大数据全局结论。

## 2. 从原 p,s PDE 直接证明商代表的 Lax 桥梁

这里不以辅助 ambient Adler 计算代替实际原时间。用已独立复核的 c=0 原投影方程

\[
p_t=-D(bp)-P_0D(p^2/2+\beta s^2)-p_{xx}-Rs_{xx},
\qquad s_t=s_{xx}-D(bs+ps),\quad\beta=h^2/32.
\tag{A}
\]

Π 为格点平均、P0=I−Π；p、s 的格点平均为零。令

\[
a_j^\pm=p_j/2\pm hs_j/8,\quad
\nu_c=-\Pi(p^2/4+\beta s^2/2),
\]

\[
\nu_j=\nu_c+\tfrac12(Rs_x)_j-\tfrac h4s_{j,x},\quad
V_j=-D^2-bD-\nu_j.
\]

周期 skew primitive 给 νj+1−νj=hsj,x/2，νM=ν0。直接将 (A) 相加、相减得到

\[
a_{j,t}^+=-\nu_{j,x}-a_{j,xx}^+-D(ba_j^++(a_j^+)^2),
\]

\[
a_{j,t}^-=-\nu_{j+1,x}-a_{j,xx}^--D(ba_j^-+(a_j^-)^2).
\tag{B}
\]

对任意 a 与 V=−D²−bD−ν，令 W=−D²−bD−ν−b_x−2a_x。标量式 a_t=−ν_x−a_xx−D(ba+a²) 恰等价于

\[
(D-a)_t+(D-a)V=W(D-a).
\]

同格点的 ± 两个因子具有同一个 W，因为 νj+1−νj=2(a+j−a−j)_x。故 Tj=(D−a−j)−1(D−a+j) 满足

\[
T_{j,t}=V_{j+1}T_j-T_jV_j.
\]

周期相乘 P=T_{M−1}…T0 精确给

\[
\boxed{\widehat P_t=-[D^2+bD+\nu_0,\widehat P].}
\tag{C}
\]

所有系数周期。式 (C) 是原稿 (6) 的直接原 PDE 证明；P 是共同 U=0 商代表，不能把同一个 bD 生成元不加共轭搬到实际 U=b+p 的 P_b 上。

在 M=3 图内 P=I+a3Qhat−1、a3=3hκ/16≠0，原约束链给 κ_t=0。因此 (C) 推出 Qhat_t=−[D²+bD+ν0,Qhat]。令 Qhat=D³+AD²+B1D+C1。首一性给 b_x=2A_x/3，周期交换的平均零又给 avg A=0，故 b=2A/3+B(t)，其中 B=avg b。亦可直接由 P 的 a4=−a3A 和 (C) 的 a3,t=−2a4,x−3a3b_x 复核。

## 3. 周期去项、holonomy 与任意共同零模

取 ζ_x=A/3，则 expζ 为真实周期规范，且

\[
e^\zeta\widehat Qe^{-\zeta}=D^3+uD+v,
\quad u=B_1-A_x-A^2/3,
\quad v=C_1-AB_1/3+2A^3/27-A_{xx}/3.
\]

时间规范的生成元为 eζKe−ζ−ζ_t；−ζ_t 的符号不可遗漏。记 a=A/3、b=2a+B，它成为

\[
D^2+BD+[\nu_0-a_x-a^2-Ba-\zeta_t].
\]

Q 无二阶项强制方括号的 x 导数为 2u_x/3，故加时间标量后真实方程正是 Q_t=−[D²+BD+2u/3,Q]。

共同 U=0 到实际 Q_b 的规范 θ_x=a+B/2，holonomy exp(+LB/2)；实际 Q_b 去项 η_x=−B/2，holonomy exp(−LB/2)。它们相乘给周期 ζ=θ+η，时间项的 ±B′x/2 同时相消。原稿 holonomy 符号正确，没有错用准周期因子的周期 trace。

任意预先给定光滑 B(t) 的物理恢复须明确写成

\[
\tau(t)=\int_0^tB(\sigma)d\sigma,\quad
p_B(x,t)=p_0(x-\tau,t),\quad s_B(x,t)=s_0(x-\tau,t),
\]

\[
b_B(x,t)=b_0(x-\tau,t)+B(t),\quad
\boxed{U_B(x,t)=U_0(x-\tau,t)+B(t).}
\]

仅写空间平移会漏掉实际 U 的共同加量。B=0 时实际 Q_b 已 depressed；B≠0 时周期 depressed Q 的指数保持，实际 Q_b 指数整体加 B/2。

## 4. Floquet 旗标和一般六因子的 ambient 逆

背景 r*>0、d=hr*/8、a*>2d、a*≠6d 正确。分母三个指数 a*/2−d、−a*/2−d、2d 与分子三个指数 −2d、−a*/2+d、a*/2+d 均实、相异、非零。唯一可能的同一算子重根在 a*=6d；a*=2d 则 a3=0，已排除。常背景 W1 是非零指数函数，W2 含非零指数差，W3 含非零 Vandermonde，故所有指定旗标 Wronskian 非零。

实周期 ODE 的 monodromy 在有限 C^k 小邻域连续依赖；简单正实倍子不经碰撞不能变成非实或非正。用局部实特征投影选择特征线，再按指定顺序累加，得到唯一 Floquet 不变旗标。Wronskian 对 x→x+L 只乘对应倍子乘积，Dlog|Wr/Wr−1| 因而周期。有限阶连续性保持 Wronskian 与交换差非零，所有这些操作在 C∞ 分级空间是光滑的，并只损失有限阶正则性。

要严格使用“静态逆 ⇒ 实际向量相同”，需把 inversebubble 明确提升到整个六系数 ambient 图。给任意两个接近背景的 monic 三阶 Q、R（暂不要求 R=Q+a3 或 Q depressed），指定旗标给

\[
Q=(D-q_L)(D-q_M)(D-q_R),\quad
R=(D-r_L)(D-r_M)(D-r_R).
\]

下面是一般场的完整逆交换算法；三个 log 导数彼此独立，不能把特殊两幅值族中两个相等的 θ− 强加到一般场：

\[
\theta_{20}=D\log|r_L-q_L|,\quad
\widetilde a_2=r_L-\theta_{20},\quad
\widetilde b_0=q_L-\theta_{20},
\]

\[
\theta_{10}=D\log|r_M-\widetilde b_0|,\quad
a_1^+=r_M-\theta_{10},\quad a_0^-=\widetilde b_0-\theta_{10},
\]

\[
\theta_{21}=D\log|\widetilde a_2-q_M|,\quad
a_2^+=\widetilde a_2-\theta_{21},\quad a_1^-=q_M-\theta_{21},
\]

\[
a_2^-=q_R,\quad a_0^+=r_R,\quad
U_j=a_j^++a_j^-,\quad s_j=4(a_j^+-a_j^-)/h.
\tag{D}
\]

直接正向 bubble 验证 (D) 的互逆性。原 a_j± 的正向三个导数依次为 Dlog|a2+−a1−|、Dlog|a1+−a0−|、Dlog|a2++θ21−a0−−θ10|；排序后 Q 的系数是 (a0−+θ10+θ20,a1−+θ21,a2−)，R 是 (a2++θ21+θ20,a1++θ10,a0+)。(D) 恢复每个原系数。

因此 (U,s)↔(Q,R) 是全 ambient 六系数的光滑互逆局部图，未把一般场限制在两幅值族中；其微分单射来自可微互逆恒等式，而非只有集合单射性。

## 5. 物理像内约束、Casimir 和实际回拉

在 ambient 图中取 Q depressed、R=Q+a3，a3 非零常数。形式展开 P=Q−1R=I+a3Q−1 给 a1=a2=0、a3 恒定。由已全 M 独核的点态恒等式，这等价于 c=0、q=0、χ=κ=16a3/(3h)。不缺少额外像内的 primary/secondary 条件。Q 的二阶项为零和排序 log 导数平均零又使实际 U 的共同平均为零，且实际 b=2A/3，正好是原约束一致性闭合。

这里固定 a3 只是沿一条轨道使用原约束链已强制守恒的 κ/H0 值；κ 不是 Casimir。初态可在图内选择不同 κ，不能把固定能量流存在性扩大解释成已经做了能量商。

原组件均值等于各标号 a_j± 的积分组合；逆交换只加减周期 log 导数，其积分为零。Q 和 R 在同一 periodic Lax 方程下 monodromy 相似演化，所以各标号 Floquet 指数不变，原 p_j、s_j 的空间均值保持。任意 Q 的小邻域允许这些均值随初态变化；若先规定一个组件 Casimir 叶，必须限制到相应标号谱值的子集。标量流确保持这个子集，不需要声称它是普通 Banach 开集。B≠0 时实际 U_j 的均值整体加 B(t)，守恒的仍是 p_j、s_j 的组件 Casimir。

标量 Schr 流使 Q 和 R=Q+a3 满足同一个真实 periodic Lax 方程；其核时间演化是在三维解空间上的有限维 ODE。零曲率保证 monodromy 相似，实旗标保持，非零 Wronskian/交换差在进一步缩短的有限 C^k 时间窗保持。因此 (D) 给同一非零窗上的实际 C∞(t,x) 物理场。

其为原 PDE 的证明如下。用 b=2A/3 的光滑局部表达构造原 p,s 向量，再恢复 U；直接因子证明 (B)–(C) 给其完整 ambient 推前。原约束链给 c_t=q_t=κ_t=0，代入上述 a1,a2,a3 恒等式使 R_t−Q_t=0；b 的代数去项规范使 Q_t 的二阶项为零。因此原向量的 ambient (Q,R) 推前恰为真实标量 Lax 向量 (Q_t,Q_t)。回拉场的推前当然是同一对；ambient 互逆图的微分单射遂给两个物理向量相等。这一步不依赖单凭“线性化约束=实际切空间”的假设，亦不依赖固定均值常背景处的动量水平正则性。

若另一条原光滑解同初态、同 B(t) 且留在该图，直接桥梁将其送到同一标量 mild 问题；标量唯一性与 ambient 标号逆给原物理唯一性。故原稿的指定图局部真实流结论可认证，须按上述微分论证理解，并明确共同 U 恢复公式。

## 6. 范围

该图是 M=3 的一般兼容光滑场局部图，不是要求演化留在 p=a(1,−1,0)、s=r(1,1,−2) 的有限特殊族。但背景有非零组件空间均值，结果不自动覆盖严格所有组件空间均值为零的叶、图外场、其他 κ 符号或 M>3。有限阶损失的 C∞ 互逆不等于一个同阶 Sobolev Banach 无损流。全阶 commuting Hamiltonian 的实际共同时间窗、谱迹独立性及无限维 Liouville 完备性依旧未证。

标量/gauge 的独立子审由 c0_principal_symbol 完成，无文件改动、无旧脚本重跑。本审稿新增证书只核对直接原 PDE 的一阶因子 intertwiner 和一般 ambient inversebubble，不重复原稿 scalar/zero-curvature 或先前 81 项。

[singular_m3_factor_independent_certificates.py](singular_m3_factor_independent_certificates.py) 共 15 条 assert 全通过，exit code 0：一阶 intertwiner 的 4 个算子系数、投影原 p/s 方程 2 项、一般 inversebubble 的 3 个 log 参数及 6 个恢复系数。结果见 [JSON](singular_m3_factor_independent_certificates.json)，脚本 SHA-256 为 ae10f67d717a13ceb7dfb3674511378aea0e37af7e5ee3c9f6b2d9cc6062caca。

本轮另独核了非恒定 κ 层的主符号，完整变系数 primary 消元补齐后 universal 振荡/heat 谱成立；推导记在 [singular_branch_independent_audit.md](singular_branch_independent_audit.md) §9。这个线性主符号推进不会自动给 M>3 的真实初值流或混合边界流。
