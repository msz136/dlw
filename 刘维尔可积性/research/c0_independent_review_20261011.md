# c=0、Γ≠0 分支：独立恢复审计与两项新定理

2026-10-11。有限格点周期 M≥2、连续周期 x∈T_L、h>0、实光滑场。目标仍为一般物理场 Liouville 可积性；本报告没有完成谱完备性或一般非线性共同流。未重跑历史核验脚本，所附证书只核验本报告新增计算。

本次独立阅读 GOAL.md、README.md、STATE.md、c0_branch_audit.md，以及原 periodic_reduction.md、RESEARCH_NOTES.md、MONODROMY_POISSON_PROOF.md、INDEPENDENCE.md；全 M 混合时间报告只作方法对照，未把其 c≠0 定理移用于本分支。

新增结果是：任意 M 的奇谱迹具有任意大的独立有限块，证书位于完整约束场的相对开集；任意 M≥3 的约束主符号仍有 M−2 个正二阶方向与 M−2 个负二阶方向，并多出一个中性方向。后一结果排除兼容常背景附近普通 Sobolev C¹ 初值流，同时给出正确的线性混合边值替代模型。

## 1. 原方程强制 Γ_t=0；零模规范核对

记 Π 为格点平均、P0=I−Π、D=∂x、β=h²/32，R=(δ_-|im P0)^−1 M_-P0，R*=−R。原方程平均先给 Πw=c 为时间、空间常数，且 DΠ(Uw)=0。取 c=0、U=b+p、w=s、Πp=Πs=0，便有 q=Π(ps)=Γ(t)。投影物理方程为

\[
p_t=-D(bp)-P_0D(p^2/2+\beta s^2)-p_{xx}-Rs_{xx},\qquad
s_t=-D(bs+ps)+s_{xx}.
\]

独立乘积计算给

\[
q_t=-bq_x-2qb_x+D\chi,
\quad
\chi=-\Pi(p^2s)-\frac{2\beta}{3}\Pi s^3
+\Pi(ps_x-sp_x)-\Pi(sRs_x).
\]

R 项成立是因为 Π(s_xRs_x)=0。令 q=Γ(t)，对周期 x 积分即得 Γ_t=0，再得 b=χ/(2Γ)+B(t)。因此此分支的 Γ 时间守恒由原方程推出；它仍可随初值变化。README 中“将 Γ 设为时间常数属于附加闭合”可用于 c≠0 的常规分支，不能作为 c=0、Γ≠0 的结论。

以 hΣ∫ 配对，

\[
J=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix},\quad
H_0=h\sum_j\int\left[\frac12p_j^2s_j+\frac\beta3s_j^3+s_jp_{j,x}
+\frac12s_j(Rs_x)_j\right].
\]

其 b=0 向量恰为上式；第二式只在 q_x=0 后可去掉 P0。点态能量密度 e=Π[p²s/2+βs³/3+sp_x+sRs_x/2] 满足 χ+2e=q_x，故约束面上 χ=−2e，不只积分后成立。

## 2. Dirac 结构：必须保留变化的 Γ

仅施加 C(p,s)=P_xΠ(ps)=0，P_x 为连续空间零均值投影。标量约束配对取 hM∫，与 hΣ∫ 兼容，则 A(δp,δs)=Π(sδp+pδs)、A0=P_xA。生成元 F_f=hM∫fq 满足

\[
X_{F_f}=(-D(fp),-D(fs)),\qquad
X_{F_f}q=-2qf_x-fq_x.
\]

因此 C=A0JA0*=−2ΓD，定义域和值域均为连续空间零均值函数；C^−1=−D^−1/(2Γ)。原稿的

\[
J_D=J-JA_0^*C^{-1}A_0J
\]

在光滑弱 Poisson 范围正确。右逆 A0JA0*C^−1=I 证明非零空间模约束正则。固定组件空间均值并不妨碍这个非零模右逆；额外固定 Γ 后的零模约束在常态处却可能有二阶奇性，不能混淆。

动量 P=hM∫q=hMLΓ 的 Dirac 场为 −D(p,s)，所以 Γ 不是 Casimir。χ 的空间均值为 −2H0/(hML)，从而 Dirac H0 对应的物理平均速度规范是

\[
b_0=\frac{\chi-\bar\chi}{2\Gamma}
=\frac\chi{2\Gamma}+\frac{H_0}{P},\qquad\bar b_0=0.
\]

规定平均 b 的速度 Btilde(t) 可加 Btilde(t)P。若跨初值固定的是原积分常数 B(t)，则场多出 −(H0/P)X_P；其一形式 dH0−(H0/P)dP 一般不闭。原稿对此区分正确。

## 3. 平方根谱迹的约化证明：避免 ambient 阶数跳变

T_j=(D−U_j/2+hw_j/8)^−1(D−U_j/2−hw_j/8)，P=T_{M−1}…T0。在 c=0 层 a1=0，在 q=Γ 层

\[
P=I+a_2D^{-2}+\cdots,\qquad a_2=-hM\Gamma/8\ne0,
\quad N=a_2(P-I)^{-1},\quad L_0=N^{1/2}.
\]

首一平方根唯一、实系数，不要求无穷 PDO 级数收敛。F_n=Tr L0^n 的每一固定阶都是有限 jets 的光滑泛函。

原稿指出 a1 离开零层后造成阶数改变，这一警告必要。较清楚的证明顺序是先作共同 U 规范的 Poisson 商、取 Πw=0，再作 q 的 Dirac 约化：

1. 在这个 c=0 商中，允许 q(x) 暂时不恒定；选数值常量 a2* 与 a2(x) 同号非零。定义 Lhat=[a2*(P−I)^−1]^(1/2)，其首系数 sqrt(a2*/a2(x)) 可随 x 变。这在商内是合法 order-one 根。
2. 固定 a2* 的迹变分，在 c=0 切向 PDO 变化上满足 dFhat_n=Tr(X_nδP)，X_n=−n Lhat^(n+2)/(2a2*)，且 [X_n,P]=0。把 Tr(X_nδP) 视作 ambient cotangent 代表即可；不需把同一根公式错误地定义到 a1≠0 的场。
3. 两个代表相差的 a1 conormal 生成共同 U 规范；共同 U 变换使 P、Lhat 标量共轭，res 点态不变。因此 conormal 对规范不变量的括号贡献为零。这给第一步商的可核验代表独立性。
4. 原相反自由场因子括号诱导 (1/8) Adler map。于是任意两个 commuting 代表的 ambient 配对为 Tr X_m[(PX_n)_+,P]/8=0，传到前述商仍为零。
5. 约束生成元的直接 intertwiner 为 (T_j)_t=−[fD,T_j]，P_t=−[fD,P]；因子微分由 (D−a)_t=−[fD,D−a]−f_x(D−a) 核对。因此固定归一化 Fhat_n 与全部 F_f 对合，q 的 Dirac 修正项为零。
6. 实际 a2=a2(Γ) 的归一化变化另给 nF_n da2/(2a2)。因 a2 正比平移动量，其额外场仅为常数倍平移；不破坏 q 约束，也不改变任意平移不变迹的括号。

因此原稿的全阶形式对合主张可保留。需要保留上述商与 cotangent 代表逻辑，不能只写“平方根 KP 已知对合”。本次未发现 Γ 守恒、Dirac 零模及此对合链的实质错误。

H0 的谱守恒可按原全 M 系数恒等式 Hfull=−8Tr D²(P−I)、Hfull=H0+hM∫bq 核对。在 b=0、a1=0、a2 常数截面，H0 的 Adler 代表场为 −[D²+a2,P]。这里 Hfull 本身并非共同 U 规范不变量；与投影 J 的 trace 配对差只含 DΠ(Hfull_U)=Dq=0 或 Π((F_n)_U)=0，故这个代表计算在实际 q 约束面合法。q 的 Dirac 修正和共同 U 规范只加已经证明不影响 trace 的 commutator。因此 F_n 沿足够正则的真实物理 Hamilton 解守恒；此计算仍未证明这样的非线性解普遍存在。

## 4. 新定理：任意 M 的奇谱迹具有任意大的独立有限块

### 4.1 保留任意函数的活动格点图

取任意无零正周期函数 f，非零标量 K，令

\[
p=(f,-f,0,\ldots,0),\qquad
s=(K/f,-K/f,0,\ldots,0),\quad\Gamma=2K/M.
\]

此图属于真实 q=Γ 约束面，f 有任意函数自由度。j≥2 的 transfer 因子恒为 I，故全 M monodromy 等于前两个因子。它只用于计算完整场泛函的 covector；不假设 M≥3 的物理运动保留此图。

置 α=hK/8、θ=f_x/f、t=f/2−α/f。一次精确反交换给

\[
P=Q^{-1}R_2,
\quad Q=(D-t-\theta)(D+t),
\quad R_2=(D+f/2+\alpha/f-\theta)(D-f/2-\alpha/f),
\]

\[
R_2-Q=-2\alpha=a_2,\qquad N=Q.
\]

Q 的 D 系数为 −θ，平均为零。用周期标量规范 σ_x=−θ/2，得

\[
e^\sigma Qe^{-\sigma}=D^2+v,
\quad v=a_x-a^2,
\quad a=\frac f2-\frac\alpha f+\frac{f_x}{2f}.
\]

因此 F_n 在此图精确等于 Hill 算子 D²+v 的平方根迹；这里所需规范确实周期，不借用一般 u0 的非零 holonomy 情形。

### 4.2 同一固定组件均值叶上的图

固定 avg f=f0>0、avg(K/f)=S0≠0。参数化为

\[
f=f_0+\varepsilon r,\quad\bar r=0,
\quad K(f)=S_0/\overline{f^{-1}}.
\]

这是解析的真实约束参数图。所有 p_j、s_j 的组件空间均值固定；Γ=2K(f)/M 随初值变化，没有预先外固定。并且

\[
\bar a=f_0/2-hS_0/8
\]

精确固定。选择 S0=4f0/h，则 a*=0，Γ*=8f0²/(hM)>0；线性变分为 a1=r+r_x/(2f0)。

### 4.3 全阶二次项与精确 Vandermonde

对 F1，res(D²+v)^(1/2)=v/2，故

\[
[\varepsilon^2]F_1=-\frac12\int a_1^2.
\]

对 n≥1，

\[
[\varepsilon^2]F_{2n+1}
=c_n\int(D^n a_1)^2,
\qquad c_n=\frac{(2n+1)(-1)^{n-1}}{2^{2n+1}}\ne0.\tag{I}
\]

这个公式不是有限阶猜测。取 f(A)=A^(n+1/2)、A*=D²，trace 的二次变分是 (1/2)Tr Df'(A*)[V]V。对 V=e^(κx)，

\[
Df'(D^2)[e^{\kappa x}]
=e^{\kappa x}\frac{(n+1/2)[(D+\kappa)^{2n-1}-D^{2n-1}]}{\kappa(2D+\kappa)}.
\]

把分子在 D=−κ/2 的值除以 2κ，即得 D^−1 系数 (2n+1)κ^(2n−2)/2^(2n)。再乘 1/2 并周期分部积分，给 (I)。a*=0 时 F_(2n+1) 对 v 的线性 trace 项为零，故 v 的二阶变化不贡献；v1=Da1 即得所列结果。

取 r=Σ_i A_i cos(k_i x)，k_i=2πm_i/L，m_i 为互异正整数。令 c0=−1/2，则 F_(2n+1) 的二次型为

\[
\frac L2c_n\sum_i A_i^2(k_i^2)^n
\left(1+\frac{k_i^2}{4f_0^2}\right),\qquad n=0,\ldots,N-1.
\]

其幅值微分矩阵，除去非零行列因子后，正是 [(k_i²)^n]。行列式

\[
\prod_i\left(1+\frac{k_i^2}{4f_0^2}\right)
\prod_{i<j}(k_j^2-k_i^2)\prod_n c_n
\]

非零。以实际幅值 z_i=εA_i 为坐标，在所有 A_i≠0、充分小非零 ε 的实际 f 上，完整微分矩阵的首项行列式为非零 ε^N 倍，故 dF1,dF3,…,dF_(2N−1) 在同一固定组件均值叶上线性独立。N 任意。

从活动图推到完整场的开集可在每个有限 N 上具体实现。选 r 足够大，使所选有限迹及微分在 H^r 连续。在光滑 witness 处，约束微分 A0 有有界右逆 JA0*[-D^−1/(2Γ)]：目标 g∈H^r 时乘子 f∈H^(r+1)，固定的光滑 p,s 使 −D(fp),−D(fs)∈H^r，且其组件空间均值为零。q 的乘积约束是 H^r（r>1/2）间的光滑映射，故 split implicit function theorem 给固定均值叶中的局部约束图。上述有限幅值切向量可在这个图上延拓；非零 minor 连续保持。这只构造静态状态约束图，未假设有界 Hamilton 解流。

**定理范围。** 每个有限 M≥2 和每个 N≥1，c=0、Γ>0 的完整约束场都有一个非空相对开集，其前 N 个奇谱迹独立。证书并非动力学 Fourier 截断，也不靠有限维行波/孤子族。相对开集结论由完整约束流形的正则性以及 covector minor 的连续性得到。此图的活动组件空间均值非零，故严格要求每组件空间均值全为零的叶仍未覆盖；它也不证明任意固定均值叶都有同一证书、不证明一个共同开集承载全部无限阶、不证明作用量完备性。

### 4.4 Γ<0 的覆盖

任取 S0<0、f0>0，记 α0=hf0S0/8、a*=f0/2−α0/f0、A=1/2+α0/f0²。线性 a1=Ar+r_x/(2f0)，v*=−a*²。F1 二次型最高项仍为 −∫r_x²/(8f0²)。对 n≥1，F_(2n+1) 的 Fourier Hessian 是 k² 的多项式，其次数为 n+1，最高系数

\[
\frac{(2n+1)(-1)^{n-1}}{2^{2n+3}f_0^2}\ne0.
\]

证明由上一 divided-difference 公式将 D² 换成 D²−a*²：f'(D²−a*²) 的正阶展开最高项未变；其余项及 v 的二阶变化均降低 Fourier 次数。取 k_i=K(2πi/L)，K 为充分大的整数，行列式最高 K 次项是非零 Vandermonde。因此相同有限块独立结论也有 Γ<0 的非空相对开集。没有借改变 Γ 的符号跨越退化面。

## 5. 新定理：Dirac 约束后的真实主符号及初值流障碍

在任意常背景 p,s∈E=kerΠ、Γ=Π(ps)≠0，b0=0。非零空间 Fourier 的合法切空间是

\[
W=\{(u,v)\in E\oplus E:A(u,v)=\Pi(su+pv)=0\}.
\]

从 χ 的导数部分得

\[
\ell(u,v)=\frac{\Pi(pv-su-sRv)}{2\Gamma},\quad
T(u,v)=(u+Rv+p\ell,\,-v+s\ell).
\]

物理线性化主部为 k²T。设

\[
B=\begin{pmatrix}I&R\\0&-I\end{pmatrix},\quad w=(p,s),
\quad P_c=I-\frac{wA}{2\Gamma},\quad z=Bw=(p+Rs,-s).
\]

R*=−R 给 B²=I、A(w)=2Γ、AB=−2Γℓ，所以 T=PcB。z∈W、ℓ(z)=−1、Tz=0；对 x∈W，

\[
T^2x=x+z\ell(x),\qquad T^3x=Tx.
\]

因此 T|W 实可对角化，且

\[
\begin{aligned}
W_+&=\{(u,0):\Pi(su)=0\},\quad \dim W_+=M-2,\\
W_-&=\{(-Rv/2,v):\Pi((p+Rs/2)v)=0\},\quad \dim W_-=M-2,\\
W_0&=\operatorname{span}\{(p+Rs,-s)\},\quad \dim W_0=1.
\end{aligned}
\]

这三项是全 M 证明，非有限矩阵数值猜测。空间常数的 δΓ 模不属于上述非零 Fourier 计算。若错误地把同式放到整个 E⊕E，Tw=z、Tz=0 会有长度二的 Jordan 链；被排除的横向 w 正是违反 q_x=0 的方向。中性 z 自身不是 δΓ 方向。

完整 Fourier 矩阵为 M_k=k²T+ikC，C 为实常矩阵，并保持 W。显式地

\[
K(u,v)=-\frac{\Pi(2psu+(p^2+2\beta s^2)v)}{2\Gamma},
\]

\[
C(u,v)=\bigl(-pK-P_0(pu+2\beta sv),\ -sK-P_0(su+pv)\bigr).
\]

正谱簇维数 M−2，Re λ=k²+O(|k|)。M≥3 时，选非零 u∈s^perp∩E，初值曲线 pε=p+εu cos(kx)、sε=s 精确保持 q=Γ 及所有组件空间均值，故避开了把不可积分的抽象 tangent 当作实际初值的风险。正谱簇投影趋近 W+ 的投影，线性解在该方向具有 exp[(k²−O(|k|))t] 增长。若存在这些常态附近的正时间 H^r→H^r C¹ 解映射，其导数必须是此线性解算子，矛盾。允许任意固定有限阶导数损失仍不能压住指数增长。

**限定。** 这些常态在具有相应非零组件均值的叶上。若要求每个 p_j,s_j 的空间均值全为零，Γ≠0 常态不在该叶；本报告未将常态结论冒充该严格零均值叶的流障碍。非恒定背景冻结符号同谱，但严格的变系数结论仍须高频局部化与线性演化估计。该障碍也不排除其他解析相空间或非紧 Liouville 结构。

## 6. 调整真实流路线：线性混合问题已闭合，非线性不能照搬

上节中性块是一维，完整高频谱有 λ0=ikc0+O(1)，c0 实数；± 簇为 ±k²+O(k)。这是对 M_k/k²=T+(i/k)C 的简单零特征值解析扰动结论。Riesz 投影 Q_k^±、Q_k^0 一致有界，趋近主符号投影。

因此高频线性混合问题可以规定 Q_k^-y_k(−T)、Q_k^+y_k(T)、Q_k^0y_k(0)。精确解为

\[
y_k(t)=e^{M_k(t+T)}g_k^-+e^{M_k(t-T)}g_k^+
+e^{M_kt}g_k^0.
\]

在对应谱块上，第一、二项分别有 exp[−c k²(t+T)]、exp[−c k²(T−t)] 界；第三项有 exp(C|t|) 界。低频有限块另用有限维 ODE。由 Parseval，这给任意 H^r 混合数据的真实线性 C_tH^r 解与统一界。稳定、反稳定块在内点平滑，中性块没有该热平滑。

这一步决定了下一条非线性路线：在 q 约束的正则场图中，使用两侧抛物端点与中性中心数据构造 quasilinear 混合问题；中性分量需要 transport 型能量估计，± 块需要 maximal regularity。不能直接把 c≠0 的“固定剪切、三次一阶非线性、两侧热核收缩”原样套用，因为本分支 b 含 p_x,s_x，约束后的二阶系数随场改变，且有一个零主符号分量。该非线性构造尚未完成；本报告不把线性混合解称作一般真实物理流。

M=2 时 ± 块均为空。ps=Γ≠0 直接给 b=−p_x/p+B(t)、p_t=−Bp_x、s_t=−Bs_x，且 H0=0，与全 M 主符号定理完全一致。本节线性/独立性证明没有用 M=2 的纯平移运动替代 M≥3 的一般物理场。

## 7. 可引用的新证据与状态修正

新增独立脚本：[c0_independent_certificates.py](../../Workspaces/dlw_recovery_20261011/c0_independent_certificates.py)，输出：[c0_independent_certificates.json](../../Workspaces/dlw_recovery_20261011/c0_independent_certificates.json)。检查包含两因子 Q/R 与周期 Hill 规范恒等式、M=2,…,10 的受约束主符号精确重数、n=1,…,12 的 divided-difference 留数、N=1,…,8 的精确 Vandermonde minor。这些是本报告新增全阶/全 M 证明的核验，有限测试不替代证明。

建议父任务修正 STATE 的 c=0 行：Γ 强制守恒、Dirac 张量、形式对合与实际解上的守恒继续有效；“全阶独立性未证”可改为“奇谱迹任意有限块在每个 Γ 符号扇区的非空相对开集独立，尚未得到任意均值叶上的全局泛性”；真实流项补入“约束主符号 ±1 各 M−2、0 一维，普通 Sobolev C¹ 常态流受阻；线性混合替代问题成立，非线性共同流尚缺”。

仍缺：同一内在物理相空间上的非线性真实时间流与全部辅助流、完整 Floquet/角数据的非线性逆、极大各向同性及无限维谱完备性、c=Γ=0 兼容分支。本轮新独立块定理明显超过旧稿，但不能升级为一般物理场 Liouville 可积性已完成。

## 8. 第二位独立审阅与最终核验数

2026-10-11，独立子审 c0_principal_symbol 复核第 4 节后确认：K(f) 保留组件均值且没有遗漏一阶 δK；平方根 trace 的 c_n 系数、周期 Hill 规范、全 M 活动格点嵌入、正 Γ 的 Vandermonde 和负 Γ 的最高 Fourier 次数均正确。其指出的范围限制已明确记录：所选固定组件均值叶、Γ 随状态变化、每个有限块的非空相对开集；不推广到所有固定均值叶、外固定 Γ 的叶、全域稠密性或同一点全部阶独立。其提出的完整场切向延拓要求已由第 4.3 节的 split 约束图补齐。

新脚本最终全部通过，共 31 组独立核验项：2 个因子/Hill 符号恒等式、9 个 M 的主符号矩阵、12 个二次变分留数、8 个 Vandermonde minor。对应 49 条 Python assert；行列式 assert 同时检查精确公式及非零性。脚本 SHA-256 为 e1ab4dfdf9df9b235a9803c586bb4544bf641b3b776814ac54caae7f6b101991，记录在 JSON 中。
