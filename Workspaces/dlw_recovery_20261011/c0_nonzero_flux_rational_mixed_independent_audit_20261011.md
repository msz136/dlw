# c=0、Γ非零全 M 有理 mixed 路线独立复核

2026-10-11。独立复核 root 的新候选扩展；从已独核的原 q 约束链、因子 PDE Lax 和全 M 有理代数出发，给出指定合法实图的完整 mixed 证明依赖。此稿不固定一个外加 Γ：Γ 是初态参数，Γt=0 由原方程周期一致性强制；不将 Γ 或能量称为 Casimir。不重跑旧证书。

## 1. 原兼容链和精确二阶有理算子

在 c=0 格点平均零 p,s 中，q=Π(ps)，原 PDE 已直接给

\[
q_t=-bq_x-2qb_x+D\chi.
\]

原兼容 q=Γ(t) 使周期积分强制 Γt=0，并给

\[
b=\frac{\chi-\operatorname{avg}\chi}{2\Gamma}+B(t),
\qquad\Gamma\ne0.
\tag{1}
\]

原 Γ 守恒不是额外闭合。完整 finite bubble 图 P=Q−1R 的 Q,R 为 monic M 阶，P−I 阶 −2、首系数

\[
a=a_2=-hM\Gamma/8\ne0.
\]

置 n=M−2、K=(R−Q)/a，则 K monic n 阶，精确有

\[
\boxed{W=a(P-I)^{-1}=K^{-1}Q.}
\]

finite-rank negative part 的全阶证明与 reciprocal twists 完全沿用 [singular_all_m_rational_independent_audit.md](singular_all_m_rational_independent_audit.md) §§2–3：若 φ 是 K 的 fundamental basis，w=(F−1)lastcolumn，则 ψ=Q*w，W−=ΣφD−1ψ；反向任何 φ 的 full Wronskian 非零并匹配 dual ψ 即使 KW differential。

在 actual depressed 物理图中写

\[
W=D^2+u+\sum_{i=1}^n\phi_iD^{-1}\psi_i,
\quad Q=KW,\quad R=Q+aK.
\tag{2}
\]

P−I=aQ−1K 自动给 c=0、q=Γ=−8a/(hM)，没有额外 image 约束。φ/Wronskian、Q/R partial flagged Wronskians 和 inversebubble 差都需在合法实图内保持。

## 2. 实平均共同场与原时间桥

原 common U=0 商代表的 W 写 D²+w1D+…；由 a3=hMχ/16（q_x=0,b=0 截面）、a2=−hMΓ/8，得

\[
\widehat w_1=-a_3/a_2=\chi/(2\Gamma).
\]

实际 U=b+p 的 scalar 共轭 θx=b/2 使 actual w1=hat w1−b。故 (1) 恰给 actual w1 为 x 常数；选 canonical 平均

\[
\boxed{B_*:=\operatorname{avg}\widehat w_1
=\operatorname{avg}\chi/(2\Gamma)}
\]

使 actual w1=0。它通常非零，不应默设为 0。原能量关系 χ=−2e+qx 给

\[
H_0=-\frac{hM}{2}\int\chi\,dx,
\quad P_{\rm mom}=hML\Gamma,
\quad\boxed{B_*=-H_0/P_{\rm mom}.}
\]

Γ、H0 沿原闭合轨道守恒，所以 B* 为该轨道的常平均。它是状态依赖的 canonical 坐标规范；若用户已规定其他 B(t)，必须按 §6 的物理式恢复，不能当成所有状态共同预设的参数。

与 φ twists 的直接关系也正确：Q=KW 的次首系数 AQ=AK=k1，有限 bubble 的 log 导数平均零给

\[
B_*=-2\operatorname{avg}A_Q/M
=-2\operatorname{avg}A_K/M
=\frac2M\sum_i\mu_i.
\tag{3}
\]

其中 φi(x+L)=exp(μiL)φi(x)，ψ 的指数 −μi。从 common U=0 的平均 m1=avg hat w1 完全去项时，常 scalar shift 为 f=m1/2；K 根整体平移后 Σμ=M m1/2，故 (3) 仍给 B*=m1。

原 p,s PDE 的直接逐因子 intertwiner 已独证 P_hat,t=−[D²+bD+ν0,P_hat]。实际 P 经共同场共轭后，生成元只有 D²+V。B* 恒定时 V 可取周期。原 shape 先给 actual w1,x=0，而

\[
w_{1,t}=-2u_x+2V_x
\quad\text{当 }w_{1,x}=0.
\]

积分使 avg w1 守恒；初始 w1=0，所以 pointwise w1 始终零，Vx=ux。时间标量不参与交换子，故

\[
\boxed{W_t=-[K_0,W],\qquad K_0=D^2+u.}
\tag{4}
\]

没有从形式谱 Hamiltonian 代替原物理时间：式 (4) 用的是原 PDE 因子 Lax、原 shape closure 和 actual mean 恢复。

## 3. 精确 mixed 系统与不含遗漏项的中心方程

W+=D²+u 恰等于 K0，所以 [K0,W+]=0。又

\[
[D^2,\phi D^{-1}\psi]_+=2D(\phi\psi).
\]

因此 positive/negative 部分精确为

\[
\boxed{u_t=-2D\sum_i\phi_i\psi_i,\quad
\phi_{i,t}=-(D^2+u)\phi_i,\quad
\psi_{i,t}=(D^2+u)\psi_i.}
\tag{5}
\]

没有额外 ux x、非线性 uu_x 或 Schr 块。φ 的末端、ψ 的始端与 u 的 Cauchy 数据是 mixed 输入；avg u 守恒。

写 φ=e^{μx}f、ψ=e^{−μx}g，则周期实变量满足

\[
u_t=-2D\sum_i f_i g_i,\quad
f_{i,t}=-(D+\mu_i)^2f_i-u f_i,\quad
g_{i,t}=(D-\mu_i)^2g_i+u g_i.
\]

两种 twist 在 fg 中消去，但 heat 算子的常 drift 必须保留。

## 4. 真实 mixed 收缩与同一光滑时间窗

对 s>1/2，使用

\[
X_T^s=C_tH^s\times(C_tH^s\cap L^2_tH^{s+1})^{2n},
\]

首因子 u，输入 u(0)、f(T)、g(0)、μ 与 a。扭转 heat 反转对应末端时间后均有稳定最高符号 −k²，低阶增长 μ² 有界，给 uniformly T≤1 的 maximal energy bound。

\[
\|D(fg)\|_{L^1_tH^s}\le C_s\sqrt T
(\|f\|_{L^2_tH^{s+1}}\|g\|_{C_tH^s}
+\|f\|_{C_tH^s}\|g\|_{L^2_tH^{s+1}}),
\]

\[
\|u f\|_{L^2_tH^{s-1}}
\le C_s\sqrt T\|u\|_{C_tH^s}\|f\|_{C_tH^s}.
\]

故 u 的 integration Duhamel 与 heat endpoints 的 Duhamel 映射以 C_R√T 收缩，得到唯一实际 mixed mild 轨道。所有非线性是相应实 Banach 空间中的连续双线性图，低阶解映射实解析；周期变量方程和 endpoint operators 与空间平移交换。与 κ 图一样，analytic 数据解映射的 translation orbit 判据给所有空间阶仍在同一个 X_T^s，同一 T；再由方程得到 C∞t,x。选一个足够大的有限 s0 并缩短一次 T，即可保持 full Wronskian、partial flags、Sylvester 与 inversebubble 的开条件。

## 5. Q/R 的实际微分桥及物理回拉

φt=−K0φ 给 Kt=KK0−AK；阶数比较得到

\[
A=D^2+u-2k_{1,x},\quad
Q_t=QK_0-AQ,\quad R_t=RK_0-AR.
\]

所以 Q/R 核均在 ft=−K0f 的有限维 periodic zero-curvature 下输运，monodromy 和既定标号 flags 保持。

原物理向量到完整 Q/R pair 的桥不能只用 Pdot 的集合单射性。指定常背景 Q/R 互素，adjoint left Sylvester jet matrix 非零 resultant，并在高有限 Ck 邻域处处可逆；求其 periodic algebraic inverse 后取 adjoint，得实际右 Bezout QCb+RDb=1。式 (4) 给

\[
C=(Q_t-QK_0)Q^{-1}=(R_t-RK_0)R^{-1}.
\]

右 Bezout 使 C differential；首一性与 AQ=AK 迫使 −C 恰为上面的 A。因而 original vector 和 mixed 构造在 full ambient Q/R pair 中的推前相同，再由一般标号因子逆及 finite inversebubble 的可微互逆给实际物理向量相同。

这里不假定 raw φ/ψ 无 GLn 基底冗余。simple-labelled Q/R 图及 Sylvester 开条件足以给所需的实际 derivative bridge；共振旗标扩展另需处理。

## 6. 任意规定平均场、M=2 与非空背景

给任意规定 B(t)，Δ=B−B*、τ=∫Δ，完整恢复为

\[
p_B=p_*(x-\tau,t),\quad s_B=s_*(x-\tau,t),
\quad\boxed{U_B=U_*(x-\tau,t)+\Delta(t).}
\]

这保留 p/s 的组件空间 Casimir，实际 U 均值如规定变化。

M=2 时 n=0、K=1，(5) 给 ut=0、canonical P/Q/R 静态。在合法 simple-labelled 图内，标号物理逆因此给 p/s 静态；任意规定 B(t) 只剩上述平移和共同 U 加量。这是原物理轨道结论，不把二格点图当作全 M 目标的替代。

全 M 非空性与 root 的 κ 背景证明平行但 degree 为 M−2。取 Q*=∏(z−αj)，Σα=0；取 monic n 阶 K*，根实简单并避开 α；令 R*=Q*+aK*，0<|a|足够小保持 M 个实简单根 ξ。前一系数相同给 Σξ=Σα，Newton 第二阶给

\[
\sum(\xi^2-\alpha^2)=-2a,
\quad c=0,\quad
\boxed{\Gamma=\frac4{hM}\sum(\xi^2-\alpha^2)=-\frac{8a}{hM}\ne0.}
\]

Q/K、Q/R、R/K 全互素，ξj−αl 全非零。常值 W 的一阶项 m=Σγ；共同 constant gauge f=m/2 去项，所有 Q/R/K 根增加 f，实际共同均值为 B*=m，而 p/s 与 Γ 不变。因此每个有限 M≥2、两种 Γ 符号均有非空 canonical 实物理图，并允许一般函数邻域，不锁定有限背景族。

## 7. 认证范围

本次独立推导认证指定简单正实、最小有理、非零 full/partial Wronskian 与交换差/Sylvester 图内的全 M 真实光滑 mixed 轨道。a/Γ、μ/Floquet 和能量可随初态参数变化；沿单条轨道使用守恒值不是擅自固定它们为全相空间的常量。结果尚未覆盖每个预定 component-mean leaf、严格零均值共振图、任意物理 Cauchy 初态或高阶共同 Hamiltonian 时间，也没有补足 Liouville 独立性与完备性。

此稿只有新的代数和函数空间推导，没有重复任何旧脚本；本代理此前 assert 总数仍为 145。
