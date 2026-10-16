# 零平均、零通量周期分支：次约束正则层与正密度规范商

2026-10-11。独立复核。讨论有限周期格点 $M\ge2$、连续空间圆 $x\in\mathbb R/(L\mathbb Z)$、$h>0$ 和实光滑周期场。记 $D=\partial_x$、格点平均 $\Pi$、格点投影 $P_0=I-\Pi$、空间投影 $\mathcal P_x f=f-\overline f$、$\beta=h^2/32$。采用 $h\sum_j\int dx$ 配对，$R^*=-R$、$RP_0=P_0R=R$。以下仅覆盖 $c=\Pi w=0$、$\Gamma=\overline{\Pi(Uw)}=0$ 分支；不替代一般物理场目标。

**新结果。** 零通量分支有一个此前未列出的正则子层 $q=0,\chi=\kappa\ne0$：主、次约束的非恒定空间模组成可逆二类配对；真实一致性给出二阶有限 jet 闭合以及自动守恒的 $\kappa$。该层在 $M\ge3$ 有非恒定一般函数例子；标量 transfer 的首项为 $a_3D^{-3}$，并可在合法约束阶段证明三次根迹族的全阶形式对合与原 Hamiltonian 守恒。$M=2$ 不含这个层；其 $p>0,w\equiv0$ 精确分支允许同一完整初态的不同解析解，而固定质量后的主约束规范商只有一点。这说明应区分物理流与约束商，不能推出一般不可积。

## 1. 原方程与主、次约束

原方程是

\[
\delta_-\{U_t+D(U^2/2+\beta w^2)\}
+D^2(\delta_-U+M_-w)=0,
\qquad w_t=-D(Uw)+D^2w.
\]

连续周期边界给 $c_t=0$、$q_x=0$，其中 $q=\Pi(Uw)$。在 $c=0$ 写

\[
U=b+p,\quad w=s,\quad \Pi p=\Pi s=0,\quad q=\Pi(ps).
\]

不能由 $c=0$ 解出共同场 $b$。投影后原方程为

\[
p_t=-D(bp)-P_0D(p^2/2+\beta s^2)-p_{xx}-Rs_{xx},
\qquad
s_t=-D(bs+ps)+s_{xx}.
\tag{1}
\]

第二式与以下 projected Hamiltonian 方程在 $q_x=0$ 上一致。令

\[
J=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix},
\quad
H_0=hM\int e\,dx,
\]

\[
e=\Pi\left(\frac12p^2s+\frac\beta3s^3+s p_x+\frac12sRs_x\right),
\]

以及

\[
\chi=-\Pi(p^2s)-\frac{2\beta}{3}\Pi s^3
+\Pi(ps_x-sp_x)-\Pi(sRs_x).
\]

精确点态恒等式为

\[
\boxed{\chi=-2e+q_x},\qquad
\boxed{q_t=-bq_x-2qb_x+D\chi}.
\tag{2}
\]

在 $q=\Gamma(t)$ 上周期积分先给 $\Gamma_t=0$，再给 $D(\chi-2\Gamma b)=0$。因此 $\Gamma=0$ 是由原流保持的通量水平集，不能当作原括号的 Casimir。这个分支的主约束为 $q_x=0$、其零通量水平为 $q=0$，次约束为 $\chi_x=0$。记 $\chi=\kappa(t)$，暂不规定 $\kappa$ 的值或时间演化。

## 2. 权三变换与二类次约束层

主约束的 smeared 泛函

\[
F_f=hM\int f q\,dx
\]

生成

\[
X_{F_f}(p,s)=(-D(fp),-D(fs)),\qquad
X_{F_f}q=-fq_x-2f_xq.
\tag{3}
\]

直接对 cubic 项和两个一阶 Wronskian 项求导得到

\[
\boxed{X_{F_f}\chi=-f\chi_x-3f_x\chi.}
\tag{4}
\]

$f_{xx}$ 项分别由 $ps-sp=0$、$\Pi(sRs)=0$ 消去；这只用 $R$ 反对称，不依赖格点数。

取非恒定空间模约束

\[
\phi=\mathcal P_xq=0,\qquad \psi=\mathcal P_x\chi=0.
\]

在 $q=0,\chi=\kappa\ne0$ 上，以零空间平均函数作 smearing，约束矩阵为

\[
C=\begin{pmatrix}0&K\\K&N\end{pmatrix},
\qquad K=-3\kappa D,
\tag{5}
\]

其中 $N=C_{\psi\psi}$ 是实际局部斜伴随算子；求逆不要求先展开 $N$。周期 $D^{-1}$ 只作用于零空间平均函数，故

\[
C^{-1}=\begin{pmatrix}
-K^{-1}NK^{-1}&K^{-1}\\K^{-1}&0
\end{pmatrix},\qquad K^{-1}=-\frac1{3\kappa}D^{-1}.
\tag{6}
\]

这是**完整主、次非零模配对的 Dirac 求逆**，不是只对 $q$ 套用在 $\Gamma=0$ 已失效的 $-2\Gamma D$ 逆。若改用 $\chi_x$ 而非 $\mathcal P_x\chi$ 作次约束，相应交叉块是 $-3\kappa D^2$；二者在非零模上等价。

还有一个独立可核验的降阶。以式 (7) 的 $g_p,g_s$ 记号，

\[
A_\chi^*f=(-2f g_p+f_xs,\,-2f g_s-f_x(p+Rs)).
\]

故局部 $A_\chi J A_\chi^*$ 的三阶领先系数为 $-2q$。标量斜伴随性使其二阶系数为 $-3q_x$；在 $q=q_x=0$ 的本层，两者消失，$N$ 的局部部分至多一阶，外侧仍保留空间均值投影。式 (6) 的实际层内求逆因而无需假定一个不退化的三阶 $N$。

对具有有限 jet 的 admissible 泛函，这给出约束面上的形式/分级光滑 Dirac 张量。单一 Sobolev 空间的有界张量、邻近不同 $\Gamma$ 层的一致逆以及全局商图册还需另证，不能由式 (6) 自动推出。

### 零模与弱辛商

固定每个 $p_j,s_j$ 的空间平均值后，基础 $J$ 在零空间平均变分上有 $D^{-1}$ 弱逆。动量

\[
\mathcal P=hM\int q\,dx=hML\Gamma,
\qquad X_{\mathcal P}=-(p_x,s_x)
\]

仍生成空间平移。在主、次约束面上，它与所有非零模约束的括号为零。因此再取 $\Gamma=0$ 后，完整约束矩阵还留一个零模；若 $X_{\mathcal P}\ne0$，拉回二形式的核正是这一平移方向。

在具有自由空间平移作用的局部图上，可先取零动量水平，再除以空间平移，获得弱辛的局部约束商。也可选非零第一 Fourier 系数的相位作局部切片。常数场处 $X_{\mathcal P}=0$，零动量水平不是正则水平，需另分层。均值自由函数 (B(t)) 只给商前的时间依赖平移，不能误报成不存在的 Casimir。

## 3. 真实约束链闭合：二阶有限 jet 乘子

将 $b=0$ 的真实 $H_0$ 向量场写为

\[
g_p=P_0(ps-s_x),\qquad
g_s=P_0(p^2/2+\beta s^2+p_x+Rs_x),
\]

\[
A=-Dg_s,
\qquad S=-Dg_p.
\tag{7}
\]

这里 $A=p_t^0,S=s_t^0$，并未先代入任何约束乘子。对 $\chi$ 求真实时间微分得三阶 jet

\[
\begin{aligned}
\rho:=X_{H_0}\chi={}&-\Pi(2pAs+p^2S)-2\beta\Pi(s^2S)\\
&+\Pi(A s_x+pS_x-S p_x-sA_x)\\
&-\Pi(SRs_x+sRS_x).
\end{aligned}
\tag{8}
\]

它有二阶局部通量

\[
\boxed{\rho=D\eta},\qquad
\boxed{\eta=2\Pi(g_pg_s-sA)-\Pi(sRS)+\chi_x.}
\tag{9}
\]

一个全 $M$ 证明是逐项分部：

\[
e_t^0=D\Pi\left(sA+\frac12sRS-g_pg_s\right),
\qquad q_t^0=D\chi,
\]

再用 $\chi=-2e+q_x$。故 $\overline\rho=0$ 是恒等式，亦由 $X_{H_0}H_0=0$ 推出。

在 $q=0,\chi=\kappa\ne0$ 上，真实总微分是

\[
\chi_t=\rho-3\kappa b_x.
\]

次约束一致性与周期性遂给

\[
\boxed{\kappa_t=0,\qquad
b=\frac{\eta-\overline\eta}{3\kappa}+B(t).}
\tag{10}
\]

$\kappa$ 的守恒是约束链的结果，没有预先固定它。零空间平均乘子对应式 (5)–(6) 的 $H_0$ Dirac 流：其未约束主残差为零、次残差为 $\rho$，所以次约束乘子为零，主约束乘子恰是式 (10) 的非恒定项。规定平均共同场 $\overline b=B(t)$ 后，商前流是同一张量下的 $H_0+B(t)\mathcal P$ Hamiltonian 流。

这是约束切向的实际微分表达；其主部可能随层改变，尚未给出相应 Sobolev 真实时间流的存在、唯一性或统一高频估计。

## 4. 非恒定正则层确实非空

在 $M=3$，取

\[
p=a(x)(1,-1,0),\qquad s=r(x)(1,1,-2),\qquad r(x)>0.
\]

正交性及反对称 $R$ 使所有一阶项消失，得到

\[
q=0,\qquad \chi=\frac{2r}{3}(-a^2+2\beta r^2).
\]

任选非零常数 $\kappa$ 和足够接近正常值的周期函数 (r(x))，使

\[
a(x)=\sqrt{2\beta r(x)^2-\frac{3\kappa}{2r(x)}}
\tag{11}
\]

的根内严格为正，便有 $\chi=\kappa\ne0$。例如 $\kappa<0$ 时任意正的光滑 $r$ 都使根内为正。可取具有基本周期 $L$ 的非恒定 $r$，使空间平移作用在此图上自由。

这个族还证明约束商上存在非零 Hamiltonian 向量方向。记 $v=(1,-1,0)$、$w=(1,1,-2)$，则原式 (1) 在该族上给

\[
s_t=-(ar)_xv+[r_{xx}-D(br)]w.
\]

任意空间平移向量的 $s$ 分量只沿 $w$。对 $\kappa<0$、非恒定正 $r$，$(ar)_x$ 在某个开集非零，所以无论式 (10) 的平均平移如何选择，实际约束切向的 $H_0$ 向量都不可能只是空间平移。这个判断只用可核验的真实微分表达，没有预设解流存在。

这是原约束面的非恒定一般函数族，不是已证明存在的 DLW 解轨道；式 (10) 给其约束切向候选演化。为讨论固定均值弱辛叶，可将式 (11) 所给场的实际分量均值选为该叶的值；这并不把它宣称为已有 Sobolev 开流。

## 5. 三次根标量层与全阶形式对合

沿用原有序 transfer

\[
T_j=(D-U_j/2+hs_j/8)^{-1}(D-U_j/2-hs_j/8),
\qquad P=T_{M-1}\cdots T_0.
\]

在 $c=0$ 的点态系数为

\[
P=I+a_2D^{-2}+a_3D^{-3}+\cdots,
\quad a_2=-\frac{hM}{8}q,
\]

\[
\boxed{a_3=\frac{hM}{16}\chi+\frac{3hM}{16}q_x
-\frac{hM}{8}bq.}
\tag{12}
\]

这是点态等式，比仅有积分 $H_0=-8\int a_3$ 更强。它由各因子的 $D^{-1},D^{-2},D^{-3}$ 展开和有序乘积逐项得到；独立符号证书已核验 $M=2,\ldots,6$。在当前层上

\[
a_1=a_2=0,\quad
a_3=\frac{hM\kappa}{16}\ne0,\quad
a_3=-\frac{H_0}{8L}.
\tag{13}
\]

于是 $P-I$ 的阶数恰为 $-3$，可定义首一实形式三次根

\[
L_3=[a_3(P-I)^{-1}]^{1/3}=D+u_0+u_1D^{-1}+\cdots.
\tag{14}
\]

不先把这个根延伸成任意 ambient 首一算子。合法变分分以下阶段。

### 5.1 明确离面扩展与约束余法向类

冻结非零数值 $a_3^*$，在 $a_3(x)\ne0$ 的有限 jet 图中取

\[
\widetilde P=P-a_1D^{-1}-a_2D^{-2},\qquad
\widetilde L=[a_3^*(\widetilde P-I)^{-1}]^{1/3}.
\]

离约束面时领先系数是 $(a_3^*/a_3(x))^{1/3}$，无需首一；每个固定阶实系数仍是光滑有限 jet。对

\[
F_n^*=\operatorname{Tr}\widetilde L^n,\qquad n\ge1,
\]

迹循环性给

\[
dF_n^*=\operatorname{Tr}(X_n\,d\widetilde P),
\qquad
X_n=-\frac{n}{3a_3^*}\widetilde L^{n+3},\qquad [X_n,P]=0
\quad\text{在 }a_1=a_2=0.
\tag{15}
\]

因此在合法约束阶段，$dF_n^*$ 的类由 $\operatorname{Tr}(X_n dP)$ 表示，差只含 $da_1,da_2$。$da_1$ 属于 $c=0$ 的共同 $U$ Poisson 商余法向；$da_2$ 在该阶段属主约束 $q$ 的余法向。不能将式 (15) 写成在改变 $P-I$ 阶数的整个 ambient 上的首一三次根泛函。

共同 $U$ 平移由同一标量乘法函数共轭所有因子与 $P$。该函数允许准周期；形式 residue 在这种标量共轭下点态不变。当前 $a_1=a_2=0$ 时 $a_3$ 也不变，所以 $F_n^*$ 是共同 $U$ 规范不变量，能够进入 $p,s,c=0$ 的真实 Poisson 商。

### 5.2 全阶约束切向与对合

原因子括号推前为 $\tfrac18\mathcal A_P$，其中

\[
\mathcal A_P(X)=(PX)_+P-P(XP)_+.
\]

这是既有一阶因子乘积/求逆证明的实际归一化。对式 (15) 的 commuting 代表，

\[
X_{F_n^*}P
=\frac18[(PX_n)_+,P]
=-\frac18[(PX_n)_-,P-I].
\tag{16}
\]

右侧两项的阶数至多分别为 $-1,-3$，标量领先乘积相消，所以交换子阶数至多 $-5$。因此 $a_1,a_2,a_3,a_4$ 均逐点不变。由式 (12) 得它同时保持 $c=0$、$q=0$、$\chi=\kappa$。这正是式 (5) 完整主、次约束所需的切向性。

显式离面扩展的梯度可能含主约束余法向项，它的未约化向量场不必已经次约束切向；Dirac 会消去这类项。**“Dirac 修正为零”精确地指式 (15) 的合法余法向类代表 $X_n$**，不能混同任意离面扩展的全部梯度。

对这些切向代表，Dirac 修正不改变相互括号，迹循环性给

\[
\boxed{\{F_m^*,F_n^*\}_{D}
=\frac18\operatorname{Tr}X_m[(PX_n)_+,P]=0.}
\tag{17}
\]

它们亦对合动量，故能降到零动量空间平移商。这是所有正整数 $m,n$ 的形式证明，不是有限前缀检查。

### 5.3 原 Hamiltonian 与状态归一化

取辅助外延

\[
\widetilde H=-8\operatorname{Tr}D^2(P-I),\qquad
\nabla_P\widetilde H=-8D^2.
\]

它在 $c=0,q=0,b=0$ 截面上等于 $H_0$。在当前阶数层

\[
(PD^2)_+=(D^2P)_+=D^2,
\qquad X_{\widetilde H}P=-[D^2,P].
\]

由 $[X_n,P]=0$ 得 $\{F_n^*,\widetilde H\}=0$。共同 $U$ 商对规范不变量的括号一致；完整 Dirac 修正对切向 $F_n^*$ 消失。因此

\[
\boxed{\{F_n^*,H_0\}_D=0.}
\tag{18}
\]

这里 $\widetilde H$ 的 ambient 流通常会改变 $a_3(x)$，不能把 $-[D^2,P]$ 直接标成已经完成的物理约束流；式 (10) 的主乘子才完成其 Dirac 切向修正。

最后恢复实际 $a_3=-H_0/(8L)$ 归一化，令

\[
F_n=\operatorname{Tr}[a_3(P-I)^{-1}]^{n/3}.
\]

在任一状态冻结 $a_3^*=a_3$ 求微分，其额外项为

\[
dF_n=dF_n^*+\frac{nF_n}{3a_3}da_3
=dF_n^*-\frac{nF_n}{24La_3}dH_0.
\tag{19}
\]

它增加的是 $H_0$ 流，**不是此前非零通量层的平移流**。式 (17)–(18) 给状态归一化 $F_n$ 全阶形式对合、对 $H_0$ 与任意平均平移 $B(t)\mathcal P$ 守恒。若式 (10) 存在真实光滑解，所有这些有限 jet 迹泛函沿该解守恒。

尚未证明此族全阶独立性、物理谱像逆、最大各向同性、同一实际时间窗或真实 Liouville 完备性。

### 三阶 pencil 的条件性解释

若另处确已在这个场图建立最小阶 $M$ 有理表示 $P=Q^{-1}R_0$，且 $Q,R_0$ 均为 monic $M$ 阶算子，则

\[
C=(R_0-Q)/a_3,\quad \operatorname{ord}C=M-3,\quad
L_3^3=C^{-1}Q.
\]

谱方程为 $(Q-zC)\psi=0$、$\mu=1+a_3/z$：这是 $(3,M-3)$ pencil。$M=3$ 时 $C=I$，成为三阶微分算子。此解释依赖存在该最小有理图，不能直接借用 $c\ne0$ 统一背景的逆图；当前约束层未证明相应 Floquet 旗标或最小性。

## 6. $\kappa=0$ 是另一条约束链

当 $q=0,\chi=0$ 时，式 (4) 的主、次交叉块也为零。式 (10) 不能使用。次约束一致性给

\[
\rho_x=0,
\quad \overline\rho=0
\quad\Longrightarrow\quad \rho=0.
\]

这是三级约束；随后需要检验它的乘子矩阵与更高一致性。不能从主括号与该交叉块为零就宣布完整约束链都是第一类。以下 $M=2$ 正密度区是一个完整可解的局部子层；全 $M$ 的一般 $\kappa=0$ 分层仍未完成。

## 7. $M=2$：物理非唯一与规范商并存

在 $M=2$ 写 $p=(p,-p)$、$s=(s,-s)$，有 $R=0$、$q=ps$、$\chi=ps_x-sp_x$。若光滑 $ps\equiv0$，则 $\chi\equiv0$：在 $p\ne0$ 邻域 $s=0$，在 $s\ne0$ 邻域 $p=0$，而 $p=s=0$ 的点也使 Wronskian 为零。因此 $M=2$ 不含 $\kappa\ne0$ 次约束层。

### 7.1 正 $p$ 的精确原方程解

取 $s\equiv0$、$p(x,t)>0$。原方程仅要求

\[
p_t=-D(bp)-p_{xx}.
\tag{20}
\]

任何光滑周期 $p>0$ 路径，只要 $\int p\,dx$ 与时间无关，都给出精确解

\[
\boxed{b=\frac{B(t)-D^{-1}p_t-p_x}{p}},\quad
U_0=b+p,\quad U_1=b-p,\quad w_0=w_1=0.
\tag{21}
\]

$D^{-1}$ 的输入 $p_t$ 有零空间平均；该式没有用有限场 ansatz 去替代一般函数。它直接满足原两条 DLW 方程。

例如空间周期 $2\pi$，取 $P>0$、足够小 $|\varepsilon|T^2<P$，则

\[
p=P+\varepsilon t^2\cos x,
\qquad b=\frac{\varepsilon(t^2-2t)\sin x}{P+\varepsilon t^2\cos x}
\tag{22}
\]

与静态解 $p=P,b=0$ 在 $t=0$ 有**相同完整物理初态** $(U_0,U_1,w_0,w_1)=(P,-P,0,0)$，但在 $t\ne0$ 不同。两者解析，且式 (22) 的空间平均 $\overline b=0$，所以仅规定平均共同场也不能解决这个层的物理非唯一。

### 7.2 完整局部主约束规范商

在 $p>0$ 图上，$q=0$ 等价 $s=0$，且 $dq=p\,ds$ 正则。固定 $\overline p=P$、$\overline s=0$ 的基础弱辛叶上，$q_x=0$ 已给 $s=\Gamma/p$；$\overline s=0$ 和 $p>0$ 又迫使 $\Gamma=0$。因此这一叶的原主约束面就是 $s=0$，没有遗漏的非零通量自由模。

主约束向量为

\[
\delta p=-D(fp),\qquad \delta s=0.
\]

对每个零平均切向变分 $v=\delta p$，解

\[
f=\frac{-D^{-1}v+C}{p},\qquad
C=\frac{\overline{(D^{-1}v)/p}}{\overline{1/p}}
\]

即可使 $\overline f=0$、$-D(fp)=v$。故非恒定主约束的规范向量已覆盖这个约束面的全部切空间。拉回弱辛形式为零；固定质量后的约束商局部只有一点。

这也有有限变换解释：(p(x)dx) 是正密度。保向圆微分同胚的密度推前作用生成 $-D(fp)$，而 $y=P^{-1}\int_0^xp(\xi)d\xi$ 将任意相同质量的正密度化为常密度 $P$。此外

\[
H_0=2h\int s p_x\,dx
=2h\int q\,\frac{p_x}{p}\,dx
\]

在这个图上本身是主约束组合；$H_0+F_b$ 的演化全是规范方向，商上的 Hamiltonian 为零。式 (21) 的任意路径正体现这个第一类乘子自由度。

这里的“规范”是约束 Hamiltonian 的重参数化作用及其零动力学商。任意空间微分同胚并非无需改动 $b$ 就保持原固定 Laplacian 的坐标对称；从物理解转移到规范商是额外的物理解释，不能无说明地把这些不同 $U,w$ 视为同一观测态。该商也不提供一般场目标所需的非平凡无限维 Liouville 结构。

在此 $s=0$ 精确区，所有 $T_j=I$，所以 $P=I$。原有 scalar trace 因而对任意正密度 $p$ 完全不可见；这与商为一点相容，亦表明它不可能给原物理 $p$ 的像逆。

对偶图 $p=0,s>0$ 同理：任意固定质量正路径 $s$ 可取

\[
b=\frac{B(t)-D^{-1}s_t+s_x}{s}.
\]

其原约束商亦为一点。在含零点、变号或空间分离支撑的 $p,s$ 上，除法及上述正密度商均不能使用；本记录不声称已完成这些剩余层的分类。

## 8. 全 $M$ 的零 $w$ 区与结论范围

所有 $M$ 都有精确 $w\equiv0$ 区。特别是 $p=0$ 时所有 $U_j=b(x,t)$，共同场完全任意。这是原方程确定性需要处理的真实自由度；共同 $U$ 的 Poisson 商把它映到同一个零状态。

当全 $M$ 的 $w=0,p\ne0$ 时，原投影演化为

\[
p_t=-D(bp)-P_0D(p^2/2)-p_{xx}.
\]

$q,\chi,\rho$ 都为零，原主乘子未被这些一致性条件固定。但 $M>2$ 的 nonlinear 向量 flux 通常不沿同一个标量密度重参数化方向，不能把 $M=2$ 一点商结论照搬过去。只将 $s=0$ 当精确不变区并拉回二形式，会得到零二形式；这不是完整原约束的 Dirac 商，不能据此删除全部 $p$ 自由度。

因此本次可核验的推进包括：全 $M$ 权三交叉块、二阶一致性通量、$\kappa\ne0$ 的完整非零模 Dirac 配对及零模处理、$M=3$ 非恒定约束族、order $-3$ 标量层与全阶形式迹对合守恒、$M=2$ 正密度原解的物理非唯一及其一类规范商。尚缺一般 $\kappa=0$ 分层、实际正则时间流、谱独立/完备性和一般物理场 Liouville 结论。

## 9. 更深有限阶分层：可证的系数片段与尚待接上的 Lax 前提

**后续更新。** [singular_m3_actual_flow_20261011.md](singular_m3_actual_flow_20261011.md) §1 已从原 PDE 逐因子证明下面式 (23)，适用于全 $M$ 的 $c=0$ 兼容主层，因此这里的 Lax 前提现已接上。后续稿还给出 $M=3,\kappa\ne0$ 实最小因子图的实际局部光滑流及全 $M$ 变量背景主符号。更深 $k\ge4$ 的完整约束分类和物理时间商问题仍未由系数递推自动解决。

这里严格区分原物理 transfer 与共同 $U=0$ 商代表。令

\[
\widehat P=P(p,s),\qquad P_b=e^\theta\widehat P e^{-\theta},
\qquad \theta_x=b/2.
\]

若已在相应合法约束阶段证明商代表的真实方程为

\[
\widehat P_t=-[D^2+bD+\nu,\widehat P],
\tag{23}
\]

其中 $\nu$ 为标量规范项，那么物理 $P_b$ 的方程应是

\[
(P_b)_t=-[D^2+\nu-b_x/2-b^2/4-\theta_t,P_b].
\tag{24}
\]

不能同时把式 (23) 的 (bD) 项原样写给 $P_b$。准周期 $e^\theta$ 允许任意平均 $b$；式 (24) 的乘法规范项可以具有 affine primitive，形式 residue 的标量共轭不变性仍点态成立。

在式 (23) 的前提下，若某兼容轨道上

\[
\widehat P=I+\pi_kD^{-k}+\pi_{k+1}D^{-(k+1)}+\cdots,
\qquad k\ge2,
\]

且此前 $\pi_1,\ldots,\pi_{k-1}$ 恒零，则直接的标量 PDO 阶数计算给

\[
0=(\pi_{k-1})_t=-2D\pi_k,
\]

\[
(\pi_k)_t=-2D\pi_{k+1}-D^2\pi_k
-bD\pi_k-k\pi_k b_x.
\tag{25}
\]

因此首非零系数必须空间恒定，周期积分又给它时间恒定。若它非零，乘子是

\[
\boxed{b=-\frac{2(\pi_{k+1}-\overline{\pi_{k+1}})}{k\pi_k}+B(t).}
\tag{26}
\]

这是在式 (23) 前提下的全 $k$ 系数证明；标量 $\nu$ 的交换子从更低一阶才开始，不影响式 (25)。共同 $U$ 共轭给

\[
\pi_{k,b}=\pi_k,\qquad
\pi_{k+1,b}=\pi_{k+1}+\frac{k}{2}\pi_k b,
\]

所以式 (26) 等价于物理代表的下一系数空间恒定。对当前 $k=3$ 正则层，这与式 (10) 一致；其导数关系为

\[
\rho=-\frac{32}{hM}D\pi_4
\quad(q=0,\chi_x=0).
\]

本记录对 $k=3$ 已通过原场 Hamiltonian 和真实一致性独立建立闭合，不依赖式 (23) 来替代证明。对更深 $k$ 仍须逐阶段证明原方程的式 (23)、处理全部一次/二次约束及零模；不能只以这个系数递推宣称完整 Dirac 约化。

若在某光滑最小有理图上 $\widehat P=Q^{-1}R_0$，其中 $Q,R_0$ 为 monic $M$ 阶微分算子，且 $\widehat P\ne I$，则

\[
\operatorname{ord}(\widehat P-I)=\operatorname{ord}(R_0-Q)-M,
\qquad 2\le k\le M.
\]

所以这样的图内只需有限个首阶层；全局具有该有理图仍是前提。$\widehat P=I$ 另分层，不可借用这个界。

还必须区别形式 $k$ 次根层级与原物理时间：当 $k\ge4$ 时 $\pi_3=0$，故 $H_0=-8\int\pi_3=0$ 在该完整约束层上恒等成立。若真正完成的 Poisson/弱辛约化把原 Hamiltonian 降为零，则其商上的物理时间向量为零，剩余原场运动只能属于被商去的方向。即使另有形式 $k$ 次根 commuting 层级，也不能把原物理时间自动称为非平凡 $k$-KdV 时间。这是更深层分类必须解决的结构问题。

## 证据与复核入口

- [独立精确证书脚本](../../Workspaces/dlw_recovery_20261011/singular_zero_flux_certificates.py)：$M=2,\ldots,6$ 的 $\chi=-2e+q_x$、权三作用、$\rho=D\eta$、$a_2,a_3$ 点态公式；$M=3$ 非恒定约束族；同完整初态的两条 $M=2$ 解析解。
- [检查记录](../../Workspaces/dlw_recovery_20261011/singular_zero_flux_certificates.json)：全部精确检查通过，含脚本 SHA-256。
- 前置约束与因子括号依据：[c0_branch_audit.md](c0_branch_audit.md)、[periodic_structure_audit.md](periodic_structure_audit.md)、[原周期约化](../../Workspaces/dlw_hamilton_20261004/phase_space/periodic_reduction.md)。

有限符号检查验证局部代数及显式例子；全 $M$ 和全阶论证在正文给出。没有把这些检查当作实际解存在或 Liouville 完备性证据。
