# c=0 分支：全 M 的二、三阶有理坐标与实际混合时间流

2026-10-11。接续 [三阶实际流及变量主符号](singular_m3_actual_flow_20261011.md)。本稿在明确非空的全 $M$ 实最小有理因子图上，建立 $c=0,\Gamma\ne0$ 二阶层和 $c=\Gamma=0,\kappa\ne0$ 三阶层的短时间真实光滑混合边界轨道。先证明三阶层，再在第 6 节给更简洁的二阶层。这里的“混合”具体为热型变量的始端/末端数据加中心变量的 Cauchy 数据；它不是任意光滑物理初态的 Cauchy 流，也尚不是一般物理场的 Liouville 完备性。

## 1. 阶数三的有理坐标，不限于 M=3

固定一个合法的实最小图，令

\[
P=Q^{-1}R,\qquad n=M-3,\qquad
a=a_3=hM\kappa/16\ne0.
\]

$Q,R$ 是 monic $M$ 阶微分算子。完整原约束 $c=q=0,\chi=\kappa$ 给 $P-I$ 的阶数恰为 $-3$，首系数 $a$ 空间、时间恒定。因此

\[
K=(R-Q)/a
\]

是 monic $n$ 阶微分算子，且

\[
W=a(P-I)^{-1}=K^{-1}Q.
\tag{1}
\]

$n=0$ 时 $K=1$，回到实际三阶微分算子。$n>0$ 时分母的核正好提供此前主符号中剩余的 $M-3$ 对热型变量。

式 (1)–(4) 的逆算子和负部恒等式在标量 formal PDO 代数中使用，不假设周期 $D$ 或 $K$ 是全局可逆的有界算子。随后式 (9)–(11) 是实际有限场 PDE，mixed 存在性及原因子回拉使用真实函数、ODE 和有限微分；辅助 formal 恒等式没有替代真实时间流证明。恢复 $\Psi$ 时的 $D^{-1}$ 则是零平均周期函数上的实际有界 primitive。

写 $K=D^n+k_1D^{n-1}+\cdots$。取其一组实基本解 $\phi_1,\ldots,\phi_n$，令 companion fundamental matrix

\[
F_{ji}=D^{j-1}\phi_i,\qquad
w_i=(F^{-1})_{i,n}.
\]

这些 $w_i$ 是相应 adjoint 基本解。Variation of constants 的形式积分恒等式为

\[
K^{-1}=\sum_i\phi_iD^{-1}w_i.
\tag{2}
\]

对任意微分算子 $Q$，

\[
(\phi D^{-1}wQ)_-=\phi D^{-1}Q^*(w).
\]

所以 $\psi_i=Q^*(w_i)$ 给

\[
W=W_++\sum_i\phi_iD^{-1}\psi_i.
\tag{3}
\]

本稿选简单正实 Floquet 图，$\phi_i(x+L)=e^{\mu_iL}\phi_i(x)$、$\mu_i\in\mathbb R$ 相异。对偶 $\psi_i$ 具有相反指数 $-\mu_i$，故所有形式系数周期。恒等式 (2) 本身不要求简单 Floquet：一般基本矩阵的 matrix twist 与对偶逆转置 twist 同样消去；简单图只用于这里明确的标号坐标和物理像逆。

反方向更直接。任意 $\phi_i$ 的 Wronskian 非零时，它们定义唯一 monic $K$；若

\[
W=D^3+uD+v+\sum_i\phi_iD^{-1}\psi_i,
\tag{4}
\]

则 $(K\phi_iD^{-1}\psi_i)_-=(K\phi_i)D^{-1}\psi_i=0$，所以 $Q=KW$ 精确是 monic $M$ 阶微分算子。取 $R=Q+aK$ 即恢复 $P=Q^{-1}R$。这不是截断的 PDO 模型；它是当前图的全阶精确算子恒等式。

辅助基本解可乘常数可逆矩阵，$\psi$ 作逆转置变换，$W$ 不变。选择固定 temporal 基底规范后，下面的混合数据也固定该有限维冗余；物理 $P,Q,R$ 与回拉场不依赖常数基底缩放。

## 2. 去二阶项、共同场平均与非空实图

原共同场为 $U=b+p$、$\Pi p=\Pi s=0$。共同 $U=0$ 的 $\widehat W$ 写成 $D^3+w_2D^2+\cdots$。设 $m_2=\overline{w_2}$。原一致性闭合是

\[
b=\tfrac23(w_2-m_2)+B(t).
\tag{5}
\]

仅周期标量规范 $\zeta_x=(w_2-m_2)/3$ 会保留 $m_2D^2$；完全去项 $\zeta_x=w_2/3$ 一般准周期，其 holonomy 为 $e^{m_2L/3}$。两种规范都保持算子系数周期，但不能将准周期共轭直接称为原 $B=0$ 物理图。

本稿核心采用式 (4) 的完全去项物理图，并保留它对应的共同场平均。由 $Q=KW$ 的最高两个系数，

\[
A_Q=A_K=k_1,\qquad
\overline {k_1}=-\sum_i\mu_i.
\]

有限排序交换只加减周期对数导数，故恢复的实际共同 $U$ 平均是

\[
B_*=-\frac{2}{M}\overline {A_Q}
=\frac{2}{M}\sum_i\mu_i.
\tag{6}
\]

通常 $B_*\ne0$。从共同 $U=0$ 代表完全去项时，$\sum_i\mu_i=Mm_2/3$，式 (6) 正是 $B_*=2m_2/3$。

非空图可以直接构造。取 monic $M$ 阶实简单根多项式 $Q_*$、monic $n$ 阶实简单根多项式 $K_*$，使其根集合互不相交，并使两组根之和相等；这保证 $K_*^{-1}Q_*$ 无 $D^2$ 项。令

\[
R_*=Q_*+aK_*,\qquad 0<|a|\ll1.
\tag{7}
\]

$R_*$ 的 $M$ 个根连续地保持实、简单，且 $R_*(\alpha_j)=aK_*(\alpha_j)\ne0$，所以 $Q_*,R_*$ 互素，所有异类常因子差非零。它们的前两个非首一系数相同，因此恢复场满足 $c=q=0$；首差系数是 $a$，所以 $\kappa=16a/(hM)\ne0$。$K_*$ 的全部根给简单实 $\mu_i$。对 $n=0$，取 $K_*=1$、$Q_*$ 根和为零，并约定 $k_1=0$。

本图还保留一个明确的有限 jet 条件：$Q,R$ adjoint 的左 Sylvester 系数矩阵处处可逆。常背景由经典 polynomial resultant 非零保证；足够小的有限 $C^k$ 邻域保持一致正下界。这比只要求 Floquet 谱不相交更强，后者本身不能保证光滑周期系数的 Bezout 算子。第 5 节用此实际矩阵逆建立向量回拉。

若先取 depressed $Q_*$ 和任意 $K_*$，也可对两者作同一个常数标量共轭，使 $W$ 去项；该操作整体平移所有根，始终保留式 (7)、互素和简单实图。详见 [全 M 实背景构造](real_rational_background_20261011.md)。背景是坐标开图的中心，不将非恒定轨道限制在有限幅值族中。

## 3. 精确全 M 的闭合混合系统

原 PDE 的逐因子证明已给

\[
\widehat P_t=-[D^2+bD+\nu_0,\widehat P].
\]

实际 $P$ 经共同场标量共轭，其生成元只有 $D^2$ 和乘法项。平均共同场 $B_*$ 恒定时，这个乘法项 $V$ 周期。原 shape closure 先给实际 $W$ 的二阶系数空间恒定；其真实 Lax 演化的该系数周期积分为零，所以其平均也时间恒定。初始二阶系数为零，遂在原流中保持零；同样原约束链保持 $a$。因此 $W_t=-[D^2+V,W]$ 的 $D^2$ 系数必须为零，强制 $V_x=2u_x/3$。时间常数不参与交换子，故原时间精确为

\[
W_t=-[K_0,W],\qquad K_0=D^2+2u/3.
\tag{8}
\]

利用

\[
[D^2,\phi D^{-1}\psi]_+=2D(\phi\psi)
\]

及标准负部乘积恒等式，式 (8) 等价于

\[
u_t=u_{xx}-2v_x,
\]

\[
v_t=-v_{xx}+\tfrac23u_{xxx}+\tfrac23uu_x
-2D\sum_i\phi_i\psi_i,
\]

\[
(\phi_i)_t=-K_0\phi_i,\qquad
(\psi_i)_t=K_0^*\psi_i=K_0\psi_i.
\tag{9}
\]

给 $\phi$ 使用末端数据，给 $\psi$ 使用始端数据。两者是独立的实变量；不能额外设 $\psi=\overline\phi$，因为它们的热方向相反，该关系通常不保持。

置

\[
z=v-u_x/2,\qquad
\Psi=z+\frac{i}{2\sqrt3}u_x,\qquad
m_0=\overline u.
\]

$m_0$ 和 $\overline z$ 沿流保持；要求 $\overline{\operatorname{Im}\Psi}=0$。恢复

\[
u=m_0+2\sqrt3D^{-1}\operatorname{Im}\Psi
\]

后，系统成为

\[
\Psi_t=-\frac{i}{\sqrt3}\Psi_{xx}
+\frac23uu_x-2D\sum_i f_i g_i,
\tag{10}
\]

\[
f_{i,t}=-(D+\mu_i)^2f_i-\tfrac23u f_i,\qquad
g_{i,t}=(D-\mu_i)^2g_i+\tfrac23u g_i,
\tag{11}
\]

其中 $\phi_i=e^{\mu_i x}f_i$、$\psi_i=e^{-\mu_i x}g_i$，$f_i,g_i$ 是周期实函数。Twist 在乘积中精确消去。最高阶块现在精确为一个常系数 Schrödinger 块和 $n$ 对常系数前/后向热块；不存在未核对的变量振荡一阶 Mizohata 条件。

## 4. 自足 mixed 固定点与共同光滑时间窗

取任意 $s>1/2$，在 $0\le t\le T\le1$ 置

\[
\mathcal X_T^s=C_tH_x^s
\ \times\ (C_tH_x^s\cap L_t^2H_x^{s+1})^{2n}.
\]

第一个因子是 $\Psi$。输入是 $\Psi(0)$、$f_i(T)$、$g_i(0)$，以及实参数 $m_0,\mu_i,a$。每个扭转热算子的 Fourier 符号最高阶为 $-k^2$，低阶增长有界。前向问题和反向时间后的末端问题均有一致于 $0<T\le1$ 的能量估计

\[
\|h\|_{C_tH^s}+\|h\|_{L_t^2H^{s+1}}
\le C_\mu\left(\|h_{\rm end}\|_{H^s}
+\|F\|_{L_t^2H^{s-1}}\right).
\tag{12}
\]

Schrödinger 群在 $H^s$ 酉。其 Duhamel 项只需 $L_t^1H^s$。

一维乘积估计给

\[
\|D(fg)\|_{H^s}\le C_s(
\|f\|_{H^{s+1}}\|g\|_{H^s}
+\|f\|_{H^s}\|g\|_{H^{s+1}}).
\]

所以

\[
\|D(fg)\|_{L_t^1H^s}
\le C_s\sqrt T(
\|f\|_{L_t^2H^{s+1}}\|g\|_{C_tH^s}
+\|f\|_{C_tH^s}\|g\|_{L_t^2H^{s+1}}).
\tag{13}
\]

此外 $u\in C_tH^{s+1}$，且

\[
\|uu_x\|_{L_t^1H^s}\le
C_sT(|m_0|+\|\Psi\|_{C_tH^s})\|\Psi\|_{C_tH^s},
\]

\[
\|u f\|_{L_t^2H^{s-1}}\le
C_s\sqrt T(|m_0|+\|\Psi\|_{C_tH^s})\|f\|_{C_tH^s}.
\tag{14}
\]

差分满足同样的双线性估计。因此由式 (12)–(14) 定义的 mixed Duhamel 映射，在由低阶数据界确定的 $\mathcal X_T^s$ 球上，对充分小的 $T>0$ 具有 Lipschitz 常数 $C_R(T+\sqrt T)<1$。它给唯一的真实 mild 轨道，并实解析地依赖这些 mixed 数据。这里的 $T$ 取决于一份低阶数据界、固定 twists 及背景图距离；没有在每个高阶重新取趋于零的时间窗。

光滑持久性可自足地从空间平移证明。整个周期系统及 $D^{-1}$ 与 $T_h$ 交换，故唯一的低阶解映射 $\mathcal S$ 满足

\[
\mathcal S(T_h{\rm data})=T_h\mathcal S({\rm data}).
\]

对光滑 mixed 数据，左边是同一低阶 Banach 空间中的 $C^\infty$ 曲线，因为 $\mathcal S$ 实解析。右边的平移生成元判据给解的每个空间导数仍属于同一个 $\mathcal X_T^s$。方程随后给全部时间导数，得到同一非零窗上的真实 $C^\infty_{t,x}$ 解。

为物理图保持，可一开始选一个足够高但有限的低阶 $s_0$。具体依赖如下：Wronskian 构造 $K$ 使用 $\phi$ 的至多 $n$ 阶导数；$Q=KW$ 的最低系数使用 $u,v$ 的至多 $n$ 阶导数及 $\phi,\psi$ 的有限阶导数，所以 $K,Q,R$ 系数受 $H^{s_0-n}$ 范数控制。Companion ODE、简单特征线与 partial Wronskian 商的对数导数给标号一阶因子的同阶控制。每次逆交换只加一份对数导数，至多 $N=M(M-1)/2$ 次交换给物理 $H^{s_0-n-N}$ 控制；常数依赖 Wronskian/交换差的正下界、单 Floquet 倍子的分离距、有限 twists 以及一份低阶系数界。这些是有限损失的分级 tame 映射，未声称同阶 Banach 可逆。

Adjoint Sylvester 系统还使用 $Q,R$ 系数的至多 $2M-1$ 阶 jet，并要求其行列式的一致非零下界。保守选 $s_0>n+N+2M+10$ 已足够同时控制这些 jet 与物理系数所需的有限 $C^k$ 距离；本稿不优化该阈值。然后进一步缩短一次 $T$，保持非零 Wronskians、简单正实 Floquet 倍子、Sylvester 非退化和全部交换差。光滑持久性继续使用这同一个 $T$。

## 5. 一般实物理回拉，实际向量与平均场恢复

反向构造已给 $K,Q=KW,R=Q+aK$。若 $\phi_t=-K_0\phi$，monic right division 及 Wronskian 非零给

\[
K_t=KK_0-AK
\tag{15}
\]

其中 $A$ 是周期二阶微分算子。具体 $A=D^2+2u/3-2(k_1)_x$。结合式 (8) 得

\[
Q_t=QK_0-AQ,\qquad R_t=RK_0-AR.
\tag{16}
\]

它们不是简单的 $Q/R$ commutator；但若 $Qf=0$ 或 $Rf=0$，$f_t=-K_0f$ 正是各自核中的有限维真实时间输运。Periodic compatibility 给 monodromy 的相似演化。因此简单正实 Floquet 指数及其标号旗标保持。

对这些 $Q,R$，取按原因子排序标号的完整 Floquet 旗标，其 partial Wronskians 由初态非零并在该时间窗保持非零。Wronskian 商的对数导数给唯一的标号实周期 monic 一阶分解；逆向有限异类交换恢复全部 $M$ 个原 $(D-a_j^-)^{-1}(D-a_j^+)$，再取 $U_j=a_j^++a_j^-$、$s_j=4(a_j^+-a_j^-)/h$。每一步是在非零差图中的可微 ambient 互逆；不是只沿某个有限幅值 ansatz 的静态重建。

式 (1) 使恢复场满足 $c=q=0,\chi=\kappa=16a/(hM)$。$a$ 是轨道能量的参数；初态可取不同 $a$，没有把它改称 Casimir 或额外作能量商。$W$ 的去项及式 (6) 给真实 shape closure 与平均场 $B_*$。原 $p,s$ 组件均值由标号因子 Floquet 指数给出并沿式 (16) 保持；若预先指定一份 Casimir 叶，mixed 数据必须再限制到相应谱值子集，不能把它当作所有 mixed 数据中的普通开集。

实际向量的认证需要把裸 $P$ 方程提升到整对 $Q,R$，不能借 $\phi,\psi$ 的裸坐标单射性：这些辅助场仍有有限维 $GL_n$ 冗余。

具体地，对 $Q^\dagger,R^\dagger$ 写左组合

\[
C_LQ^\dagger+D_LR^\dagger=1,\qquad
\operatorname{ord}C_L,\operatorname{ord}D_L<M.
\]

将 $2M$ 个左系数未知数对应到 $D^0,\ldots,D^{2M-1}$ 的系数，是一个有限 jet Sylvester 线性系统；左系数不被微分。上述图内矩阵处处非奇异，实际代数逆给光滑周期 $C_L,D_L$。取 adjoint 得右 Bezout

\[
QC_b+RD_b=1,\qquad C_b=C_L^\dagger,\quad D_b=D_L^\dagger.
\tag{16a}
\]

此步骤只使用有限 jet 与一致非退化下界，避免在抽象系数域内假设没有零分母。

现在原向量的 $P_t=PK_0-K_0P$ 给

\[
\mathcal C=(Q_t-QK_0)Q^{-1}
=(R_t-RK_0)R^{-1}.
\]

式 (16a) 使
$\mathcal C=(Q_t-QK_0)C_b+(R_t-RK_0)D_b$
成为实际微分算子。置 $A=-\mathcal C$，monic $Q,R$ 的最高系数比较给 $A=D^2+2u/3-2(A_Q)_x$；$A_Q=k_1$ 正好得到式 (15)–(16)。所以原向量的整对 $(Q_t,R_t)$ 推前与构造轨道一致，而不只是 $P_t$ 一致。

最后，标号旗标与一般 ambient 因子逆是显式可微互逆；对这个整对推前恒等式应用逆的微分，式 (10)–(16) 回拉向量正是原 DLW 向量。这个证明不要求 $\phi,\psi$ 无冗余，也不把集合单射性当作微分单射性。

若要求任意规定平均共同场 $B(t)$，设 $\Delta(t)=B(t)-B_*$、$\tau(t)=\int_0^t\Delta(\sigma)d\sigma$。从上述基准轨道恢复

\[
p_B(x,t)=p_*(x-\tau(t),t),\quad
s_B(x,t)=s_*(x-\tau(t),t),
\]

\[
U_B(x,t)=U_*(x-\tau(t),t)+\Delta(t).
\tag{17}
\]

空间平移与共同 $U$ 加量都必要。它们精确把基准平均 $B_*$ 变成 $B(t)$。严格固定每个组件空间均值都为零的共振叶不属于这里的 simple-labelled 裸算子逆；若处理该叶，须保留原物理旗标并用式 (16) 的有限维输运，不能沿用本图的裸算子单射性。

**局部实际结论。** 对任意有限 $M\ge3$，上述非空实最小有理旗标图内，充分近于相应实常背景的光滑 mixed 数据产生唯一的短时间真实原 DLW 混合边界轨道，规范平均共同场可以任意预先规定。该构造允许一般非恒定场，包含全部 $2(M-2)$ 个局部函数方向；没有锁定两幅值族。

## 6. 非零 Γ 二阶层：全 M 的真实 mixed 扩展

令 $c=0$、$q=\Gamma\ne0$。原周期主约束链已强制 $\Gamma_t=0$；$\Gamma$ 与平移动量成比例，不是 Casimir。现在

\[
a=a_2=-hM\Gamma/8,\qquad n=M-2,\qquad
K=(R-Q)/a,\quad W=K^{-1}Q
\]

具有阶数二。完全去项的实际图为

\[
W=D^2+u+\sum_{i=1}^n\phi_iD^{-1}\psi_i.
\tag{18}
\]

第 1、2、5 节的 finite-rank、dual twists、Wronskian 反向构造、ambient 标号逆和有限 jet Sylvester 证明完全适用；此时 $n=M-2$。共同 $U=0$ 代表的一阶系数为 $\widehat w_1=\chi/(2\Gamma)$，故原 primary 闭合

\[
b=\widehat w_1-\overline{\widehat w_1}+B(t).
\]

周期规范只能去掉非恒定部分；完全去项可能准周期。实际去项图仍有 $A_Q=A_K$，所以必须保留

\[
B_*=\frac2M\sum_i\mu_i
=\overline{\widehat w_1}
=-\frac{H_0}{hML\Gamma}.
\tag{19}
\]

初态的 $\Gamma,H_0$ 值可以变；式 (19) 是图的规范关系及沿轨道守恒，并不是另作能量商。

原 actual $W$ 的 $D$ 系数由 primary closure 先空间恒定；恒定平均场 $B_*$ 使真实生成元 $D^2+V$ 周期，其该系数的积分演化为零。初始系数为零则保持零，交换子的 $D$ 系数强制 $V_x=u_x$。故 canonical 原时间是

\[
W_t=-[D^2+u,W].
\]

positive/negative 分部精确给

\[
u_t=-2D\sum_i\phi_i\psi_i,\qquad
(\phi_i)_t=-(D^2+u)\phi_i,\qquad
(\psi_i)_t=(D^2+u)\psi_i.
\tag{20}
\]

这里没有额外 $u_{xx}$ 项。Twisted 周期变量的两份热算子仍为 $(D\pm\mu_i)^2$，势由 $2u/3$ 改成 $u$。使用 $u(0)$、$f_i(T)$、$g_i(0)$，在

\[
C_tH^s(u)\times
(C_tH^s\cap L_t^2H^{s+1})^{2n},\qquad s>1/2
\]

中作相同 fixed point：$D(fg)$ 的中心积分由式 (13) 给 $\sqrt T$，$uf$ 的热 forcing 由 $H^s$ algebra 给 $\sqrt T$。Lipschitz 常数 $C_R\sqrt T<1$ 即闭合，低 Banach 实解析与平移等变性继续给同一非零窗的全部光滑持久性。

令 $K_t=K(D^2+u)-AK$。此时 $A=D^2+u-2(k_1)_x$，整对 $Q,R$ 的 Darboux 推前、实际 finite-dimensional flags 输运、Sylvester/ambient inverse 微分回拉完全复用第 5 节，所以得到真实原 DLW mixed 轨道，而不是仅辅助二阶层级。

非空背景也直接构造：选择实简单 $Q_*,K_*$，$K_*$ 阶数 $M-2$，两组根无交集且根和相等，$R_*=Q_*+aK_*$、$a\ne0$ 足够小。首非首一系数相同给 $c=0$；第二系数差 $a$ 给

\[
\sum_j(\beta_j^2-\alpha_j^2)=-2a,\qquad
\Gamma=\frac4{hM}\sum_j(\beta_j^2-\alpha_j^2)
=-\frac{8a}{hM}.
\]

两个 $\Gamma$ 符号都提供非空的实简单旗标/Sylvester 图。任意规定的 $B(t)$ 同样用式 (17) 恢复。

当 $M=2$，$n=0$，式 (20) 是 $u_t=0$；canonical $p,s$ 静态，恢复任意共同平均后只剩平移及共同 $U$ 加量。一般 $M>2$ 有全部 $M-2$ 对 mixed 热变量及一个中心变量，未删去一般场方向。

## 7. 证据与还缺什么

有限秩表示、dual twists、共同场平均与两阶原向量微分桥的独立审计见 [singular_all_m_rational_independent_audit.md](../../Workspaces/dlw_recovery_20261011/singular_all_m_rational_independent_audit.md)。实际 mixed 收缩、扭转热的统一能量估计和同窗光滑持久性另见 [ckp_mixed_estimate_independent_review.md](../../Workspaces/dlw_recovery_20261011/ckp_mixed_estimate_independent_review.md)。非空实图见 [real_rational_background_20261011.md](real_rational_background_20261011.md) 及其 [独立背景证书](../../Workspaces/dlw_recovery_20261011/verify_real_rational_background.py)。

三阶新增 [singular_ckp_mixed_certificates.py](../../Workspaces/dlw_recovery_20261011/singular_ckp_mixed_certificates.py) 与[JSON](../../Workspaces/dlw_recovery_20261011/singular_ckp_mixed_certificates.json) 的 20 项 exact 检查全部通过：differential 正部、五个 negative 系数、中心变量与源项、dual twists、Darboux 左右 generator、非交换 numerator 消去。SHA256：9ce936db0bfcf92cb03de60c835f9402e1e4c398b2dd123c5680d811a19885a5。

二阶新增 [singular_order2_ckp_certificates.py](../../Workspaces/dlw_recovery_20261011/singular_order2_ckp_certificates.py) 与[JSON](../../Workspaces/dlw_recovery_20261011/singular_order2_ckp_certificates.json) 的 13 项 exact 检查全部通过：正部、五个 negative 系数、$n=0$ 静态中心、Newton 差与原 $\Gamma$ 归一化。SHA256：5ba6b8d9a537e87a8119357548a8ffb71d30b5522a09ab47e2f902d135a4ef8d。未重跑此前任何 33、42、66 或其他证书。

Exact paired constraint tangent 的一阶增广逆及实际 projector 另见 [singular_paired_tangent_projector_20261011.md](../../Workspaces/dlw_recovery_20261011/singular_paired_tangent_projector_20261011.md)。它说明此前变量主符号来自真实配对约束切向；本稿的 cKP 中心方程则提供进一步的实际常系数块和端点估计，未从 principal 谱直接宣布存在。

这一结果建立的是全 $M$ 的二阶非零 $\Gamma$ 层和三阶非零 $\kappa$ 层、指定合法实图上的实际 mixed BVP 解图。它没有建立任意物理光滑初态的 Cauchy 流、图外或严格零均值共振叶的无条件流、更深零 $\Gamma$ 零 $\kappa$ 层、所有 commuting 高阶 Hamiltonian 的共同实际时间窗、谱迹独立性或无限维 Liouville 完备性。完整 Dirac 商的真实 mixed 解图与其弱辛边界几何也还需接合；不能把实际 mixed 存在直接当作 Liouville 可积性的全部证明。
