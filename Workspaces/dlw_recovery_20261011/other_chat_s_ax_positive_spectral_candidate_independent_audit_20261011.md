# 全线 s=m=Ax 正谱密度候选的独立审查

日期：2026-10-11。审查对象：`other_chat_s_ax_positive_spectral_candidate_20261011.md` 的 S1–S15 规范重录；该来源注明不是用户全文的逐字副本。本文不改共享研究记录，也不复跑既有证书。

**结论：在下述固定参数、新设 Hilbert 拓扑和新设强辛结构内，候选给出一条成立的特殊无限维完全可积分定理。** 它确实回拉为原半离散 DLW 的全线光滑解，并有全实时间流、单射谱状态坐标和 Hilbert Lagrangian 等值集。这里的辛结构由谱密度坐标新定义；本文没有证明它是原物理 Poisson 张量的约化或回拉。一般物理场、一般 M、原物理辛叶上的完整 Liouville 可积性仍未由该候选解决。

## 1. 原方程回拉与参数核对

沿用原项目 `刘维尔可积性/README.md` 的方程及缩放：

\[
\delta_-[U_t+D(U^2/2+\beta_{\rm DLW}w^2)]
+D^2(\delta_-U+M_-w)=0,
\qquad w_t+D(Uw)-D^2w=0,
\]

\[
\delta_-f_j=(f_j-f_{j-1})/h,\qquad
M_-f_j=(f_j+f_{j-1})/2,\qquad
\beta_{\rm DLW}=h^2/32,\qquad d=h/8.
\]

取 M=2、全线 x∈R、固定 A>0，并令

\[
U_0=0,\quad U_1=-2p,\quad w_0=2Ax,\quad w_1=0,
\qquad c=2dA=hA/4>0. \tag{1}
\]

这里 c 是谐振子势的参数，不是此前周期常通量分支里的平均 w 参数。候选中的常数谱对数比 β 也不同于 \(\beta_{\rm DLW}\)。

第二条原方程逐分量成立：w0 与 w1 均不随 t 变，w0,xx=0，且 U0w0=U1w1=0。第一条方程的 j=0 分量乘 h/2 恰为

\[
p_t-2pp_x+p_{xx}+4\beta_{\rm DLW}A^2x=0.
\]

因为 \(4\beta_{\rm DLW}A^2=2c^2\)，原方程等价于

\[
p_t=2pp_x-p_{xx}-2c^2x. \tag{2}
\]

j=1 分量只是其相反数。平均量 m=(w0+w1)/2=Ax、q=(U0w0+U1w1)/2=0，故该分支满足 Γ=0。若先只固定 w0=2Ax、w1=0，则第二方程给 D(xU0)=0；要求 U0 在 x=0 光滑，就强制 U0=0。因此 Γ=0 在此光滑特殊分支内来自方程，而不能推广为一般原 DLW 的外加冻结条件。

令 \(\mathcal A=-D^2+c^2x^2\)、\(p=-D\log\Psi\)。只要 Ψ>0 且

\[
\Psi_t=\mathcal A\Psi+a(t)\Psi, \tag{3}
\]

直接求导就得到 (2)，因为
\(\Psi_{xx}/\Psi=p^2-p_x\)，而 x 无关的 a(t) 被 D 消去。后文的坐标规范采用 a=7/3；去除此整体标量规范后就是 a=0 的精确线性方程。

## 2. 积分核、负特征值与规范常数

设 K=[1,2]，

\[
\nu(k)=\frac12+\frac{k^2}{2c},\quad
I_\nu(t)=\int_0^\infty z^{\nu-1}e^{-z^2/2+tz}\,dz,\quad
N_\nu=I_\nu(0)=2^{\nu/2-1}\Gamma(\nu/2),
\]

\[
\phi_\pm(k,x)=\frac{e^{-cx^2/2}}{N_{\nu(k)}}
 I_{\nu(k)}(\pm\sqrt{2c}\,x). \tag{4}
\]

ν 的取值在一个严格正的紧区间。积分在所有复 x 的紧集上一致收敛，可逐次微分；对实 x 严格为正。分部积分给

\[
I_\nu''(t)=\nu I_\nu(t)+tI_\nu'(t).
\]

代入 (4) 得到精确恒等式

\[
\phi_\pm''=(c^2x^2+2c\nu-c)\phi_\pm
=(c^2x^2+k^2)\phi_\pm,
\qquad \mathcal A\phi_\pm=-k^2\phi_\pm. \tag{5}
\]

并且

\[
\phi_\pm(k,0)=1,\qquad
\phi_\pm'(k,0)=\pm\chi(k),\qquad
\chi(k)=2\sqrt c\,
\frac{\Gamma((\nu(k)+1)/2)}{\Gamma(\nu(k)/2)}>0. \tag{6}
\]

χ 在 K 上光滑且有正的上下界。上述核不是全线 L² 特征函数；它们在一侧增长，所以 (5) 的负特征值不与 L² 谐振子正谱冲突。

主来源公式亦核对一致：令 a=k²/(2c)，则
\(\phi_\pm=U(a,\mp\sqrt{2c}x)/U(a,0)\)、
\(N_\nu=\Gamma(\nu)U(a,0)\)。这由 [NIST DLMF 12.5.E1 的积分表示](https://dlmf.nist.gov/12.5.E1) 和 [12.2.E2 的微分方程](https://dlmf.nist.gov/12.2.E2) 直接得到。本文的 (5) 另外作了完整积分核求导核验，不依赖引用替代证明。

## 3. 谱状态映射及精确单射

记

\[
V=\{f\in H^1(K;\mathbb R):\int_Kf=0\},\qquad
\langle f,g\rangle_1=\int_K(fg+f'g').
\]

固定 β∈R，取任意 (Q,P)∈V×V，定义

\[
\mu_\pm=e^{Q\pm(P+\beta)},\quad
\Psi(x)=\int_K[\mu_+\phi_+(k,x)+\mu_-\phi_-(k,x)]\,dk,
\quad \Phi_\beta(Q,P)=-D\log\Psi. \tag{7}
\]

H¹(K) 嵌入 C(K)，是乘法代数。故 μ± 是严格正的 H¹ 密度；每个有界坐标球内有一致正下界和一致 H¹ 上界。Ψ 对所有实 x 严格正，因此 p=Φβ(Q,P) 在全线光滑且实解析。对任意 x 的紧区间，Φβ 是 H¹×H¹ 到 C^r 的实解析映射，r 可任取。

令

\[
Z=\Psi(0)=\int_K(\mu_++\mu_-),\qquad
\rho_\pm=\mu_\pm/Z,\qquad
\widehat\Psi(x)=\Psi(x)/Z
=\exp\!\left(-\int_0^x p(y)\,dy\right).
\]

从 p 可以精确算出全部归一矩：

\[
(-1)^n\mathcal A^n\widehat\Psi(0)
=\int_K k^{2n}(\rho_++\rho_-)\,dk, \tag{8}
\]

\[
(-1)^nD\mathcal A^n\widehat\Psi(0)
=\int_K k^{2n}\chi(k)(\rho_+-\rho_-)\,dk. \tag{9}
\]

这里算子严格按 \(D\mathcal A^n\) 的次序施加，不把 D 与势项交换。每个左侧只需 p 在 0 的有限阶 jet。

由于 k↦k² 是 K 到 [1,4] 的同胚，k² 的多项式在 C(K) 中一致稠密。若两组归一密度的 (8)–(9) 全相同，则其和与 χ 乘差分别与所有连续测试函数配对为零；它们属于 H¹⊂L²，因而几乎处处为零。χ 无零点，故两组 ρ± 完全相同。反演可具体写作

\[
E(y)=\frac{\rho_+(\sqrt y)+\rho_-(\sqrt y)}{2\sqrt y},
\quad O(y)=\frac{\chi(\sqrt y)[\rho_+(\sqrt y)-\rho_-(\sqrt y)]}{2\sqrt y}.
\]

(8)–(9) 是 E,O 在 [1,4] 的普通多项式矩；例如 Legendre 完备性恢复唯一 L² 函数，然后

\[
\rho_\pm(k)=k\left[E(k^2)\pm\frac{O(k^2)}{\chi(k)}\right]. \tag{10}
\]

这里证明唯一 L² 恢复；并未另行声称某一矩反演算法或 Legendre 截断在 H¹ 中稳定收敛。

最后设

\[
r_Q=\tfrac12(\log\rho_++\log\rho_-),\quad
r_T=\tfrac12\log(\rho_+/\rho_-).
\]

实际像上的逆为

\[
Q=r_Q-\int_Kr_Q,\qquad
\beta=\int_Kr_T,\qquad P=r_T-\beta. \tag{11}
\]

K 长度为 1。Q 的零均值恰好消去整体 Ψ 标量；\(\log Z=-\int_Kr_Q\)。固定 β 的两点产生同一 p 时，(8)–(11) 强制两点相同。因此 Φβ 全局单射。

微分也单射：若 δp=0，则 \(D(\delta\Psi/\Psi)=0\)，即 δΨ=CΨ。对有符号 H¹ 密度 δμ±−Cμ± 应用同一矩唯一性，得 δμ±=Cμ±，从而 δQ±δP=C。零均值强制 C=0、δQ=δP=0。这是实际场映射的微分单射，不是只在均匀点的形式线性化结论。

## 4. 必须保留的新拓扑

令 \(\mathcal M_\beta=\Phi_\beta(V\times V)\)，以唯一坐标 (Q,P) 把它赋予 V×V 的 Hilbert 拓扑；距离记作

\[
d_*^2=\|Q_1-Q_2\|_{H^1}^2+\|P_1-P_2\|_{H^1}^2. \tag{12}
\]

在有界坐标球内，(Q,P) 与严格正归一密度对 (ρ+,ρ−) 的 H¹ 距离互相控制。正方向由指数的 H¹ 乘法估计和 Z 的正下界得到；逆方向由 (11)、对数的 H¹ 链式法则及正下界得到。因此该拓扑确实是当前密度拓扑的等价表达。

它严格强于通常的 C∞loc 场拓扑。显式取固定非零 a 和

\[
Q_N(k)=\frac aN\sin(2\pi N(k-1)),\qquad P_N=0. \tag{13}
\]

则 QN 零均值且一致趋于 0，但
\(\|Q_N\|_{H^1}^2=a^2/(2N^2)+2\pi^2a^2\not\to0\)。相反 μ±,N 一致趋于基点密度；(7) 的紧 x 集逐次微分给 pN→p0 于 C∞loc。故通常场拓扑中的连续逆不存在。来源中的 C¹ 轨道唯一性应明确指 (12) 的 Hilbert chart；仅假定 p(t) 是 C∞loc 中的 C¹ 曲线不足以调用坐标微分单射。

## 5. 全实时间流与标量规范

写 \(\kappa(k)=k^2\)、\(f(k)=7/3-k^2\in V\)。精确线性解是

\[
\Psi_{\rm heat}(t,x)=\int_K e^{-k^2t}
[\mu_{+,0}\phi_++\mu_{-,0}\phi_-],dk. \tag{14}
\]

K 有界，故所有实 t 都定义良好，严格正且可任意逐次求导；\(\Psi_{{\rm heat},t}=\mathcal A\Psi_{\rm heat}\)。由 (3) 得原 DLW 的全实时间解。

零均值坐标流是

\[
Q(t)=Q_0+tf,\qquad P(t)=P_0,\qquad\beta(t)=\beta. \tag{15}
\]

将 (15) 代回 (7) 得 \(\Psi_{\rm coord}=e^{7t/3}\Psi_{\rm heat}\)，所以坐标选取的 Ψ 满足 \(\Psi_{{\rm coord},t}=(\mathcal A+7/3)\Psi_{\rm coord}\)。该整体正标量不影响 p。不能同时把零均值 Q 的 Ψcoord 写成无标量项的线性方程；p 的方程与时间参数无需更改。

(15) 是整个 V×V 上的全局平移流，也保持 d*。在 C¹ Hilbert chart 曲线中，若 p(t) 解 (2)，链式法则与微分单射给 \(D\Phi_\beta(z)\dot z=D\Phi_\beta(z)(f,0)\)，从而 \(\dot z=(f,0)\)。因此此相空间内解唯一。本文不从这条特殊正谱分支推出整个全线反向热方程或整个原 DLW 函数空间的适定性。

## 6. 增长渐近与非静态性

令 T=√(2c)x→+∞。对紧的 ν 区间，Laplace 展开一致给

\[
I_\nu(T)=\sqrt{2\pi}\,e^{T^2/2}T^{\nu-1}
[1+O(T^{-2})],\qquad
\frac{I_{\nu+1}(T)}{I_\nu(T)}
=T+\frac{\nu-1}{T}+O(T^{-3}), \tag{16}
\]

\[
I_\nu(-T)=\Gamma(\nu)T^{-\nu}[1+O(T^{-2})],\qquad
\frac{I_{\nu+1}(-T)}{I_\nu(-T)}
=\frac\nu T+O(T^{-3}). \tag{17}
\]

证明预算如下：在 (16) 中平移 z=T+u，核心 |u|≤T/2 的高斯积分作四阶一致 Taylor 展开；奇项积分为零，尾部为指数小量。ν 的正下界控制 z=0 的可能幂奇性。比值使用相邻 ν 的展开，其 T^-2 系数差为 ν−1。在 (17) 中作 z=u/T，展开 e^-u²/(2T²)，余项由 Gamma 矩统一控制。由此

\[
\phi_+(k,x)\sim C_+(k)e^{cx^2/2}x^{\nu(k)-1},\quad
\phi_-(k,x)\sim C_-(k)e^{-cx^2/2}x^{-\nu(k)},
\]

\[
C_+=\sqrt{2\pi}(\sqrt{2c})^{\nu-1}/N_\nu,
\quad C_-=\Gamma(\nu)(\sqrt{2c})^{-\nu}/N_\nu,
\]

\[
\frac{\phi_+'}{\phi_+}=cx+\frac{\nu-1}{x}+O(x^{-3}),\qquad
\frac{\phi_-'}{\phi_-}=-cx-\frac\nu x+O(x^{-3}). \tag{18}
\]

对正权积分，衰减侧相对增长侧是指数小量；增长侧的对数导数是 (18) 的正加权平均。负 x 用 \(\phi_-(k,x)=\phi_+(k,-x)\)。所以两端都有

\[
p(t,x)=-cx+O(|x|^{-1}),\qquad
b(t,x)=-p(t,x)=cx+O(|x|^{-1}). \tag{19}
\]

余项在有界 H¹ 坐标球和有界时间区间上一致。这里的物理场增长、w0 在 0 穿零，w1 恒零；它不属于此前周期常通量 S≠0 的状态图，也不能自动放进全线 Schwartz 扰动或原哈密顿积分收敛的函数域。

此族并非静态或刚性空间平移。归一密度演化满足
\(\partial_t\rho_\pm=(\mathbb E\kappa-\kappa)\rho_\pm\)，且

\[
(p^2-p_x)(t,0)=\mathbb E_t\kappa,
\qquad \partial_t\mathbb E_t\kappa
=-\operatorname{Var}_t(\kappa)<0. \tag{20}
\]

严格性来自密度在整个 K 上正且 κ 非常数。若 p(t,x)=p0(x−vt)，其两端渐近含常数 cvt，而 (19) 没有该项，故 v=0；(20) 又排除静态。固定的 w0=2Ax 本身也选定了空间原点。

## 7. 新设强辛结构与实际 DLW 时间

在 V×V 定义

\[
\Omega_*((q_1,p_1),(q_2,p_2))
=\langle q_1,p_2\rangle_1-\langle q_2,p_1\rangle_1. \tag{21}
\]

通过 Φβ 将其搬到 \(\mathcal M_\beta\)。这是闭的常系数强辛形式：其 flat 映射借 Hilbert Riesz 同构是有界可逆的。采用 \(\iota_{X_H}\Omega_*=dH\)，对应 Hilbert 梯度公式

\[
X_H=(\nabla_P H,-\nabla_Q H),\qquad
H_* =\langle f,P\rangle_1
=\int_K[(7/3-k^2)P-2kP']. \tag{22}
\]

因此 \(X_{H_*}=(f,0)\)，恰好是 (15)，其物理回拉就是原方程 (2)，没有重标原时间。P 无端点边界条件；若将 (22) 分部积分，必须保留边界项，不能把它误作没有边界项的 L² 梯度。

本文没有计算原物理 J 在这个增长特殊分支上的限制，也没有证明 (21) 与原 J 相等。让 β 也变化时，可以人为把 β 设为 Casimir，但相应 Poisson 结构有核；(21) 的强辛断言只适用于固定 β 叶。

## 8. 完整 Hilbert Lagrangian 积分族

令

\[
e_n(k)=\frac{\sqrt2\cos(n\pi(k-1))}{\sqrt{1+n^2\pi^2}},\qquad n\ge1. \tag{23}
\]

它们是 V 的 H¹ 正交归一完备基。完备性适用于全部零均值 H¹，不要求 Neumann 边界条件：将任意 H¹ 函数偶延拓到 [-1,1] 并作周期 H¹ Fourier 展开，即得到加权 cosine Parseval 恒等式；零均值除去常数模。

设 Qn=〈Q,en〉1、Pn=〈P,en〉1，则

\[
\Omega_*=\sum_{n\ge1}dQ_n\wedge dP_n,\qquad
H_* =\sum_{n\ge1}\omega_nP_n,
\]

\[
\omega_n=\langle f,e_n\rangle_1
=\frac{2\sqrt2\sqrt{1+n^2\pi^2}}{n^2\pi^2}
[1-2(-1)^n]. \tag{24}
\]

两级数由 Cauchy–Schwarz 在 Hilbert 意义下收敛；ω∈ℓ²，且每个 ωn 非零。额外核对 \(\|f\|_{H^1}^2=454/45\)。定义 In=Pn，则全部 In 两两对合并沿实际 DLW 时间守恒。积分映射

\[
\mathcal I:V\times V\to\ell^2,\qquad (Q,P)\mapsto(P_n)_{n\ge1}
\]

是连续满射线性次浸没，任意有限子族微分独立。对任意固定 P*，其等值集正是 V×{P*}；切空间 L=V×{0} 满足 \(L^{\Omega_*}=L\)。所以这是实际强 Hilbert Lagrangian 等值集，而不只是无限个独立对合函数。

每个 In 的流是 Q→Q+ten。有限个流的组合在任意 Q 方向中稠密；若要严格得到任意 g∈V 的一次平移，使用连续 Hamiltonian \(H_g=\langle g,P\rangle_1\)，其流是 Q→Q+tg。这是收敛的 Hilbert 线性组合，不把有限组合的稠密性误称为有限组合已达到每一点。物理辅助流亦实际定义：

\[
\dot p=-D\left\{
\frac{\int_K g(k)[\mu_+\phi_++\mu_-\phi_-],dk}{\Psi(x)}
\right\}.
\]

所有实辅助时间的密度保持正，故仍在同一全线增长相空间。Q 是非周期 Hilbert 位置坐标；这些等值集不是紧环面，定理不声称准周期轨道。

## 9. 审查边界与最终判断

在固定 c>0、A=c/(2d)、β 的特殊全线分支，采用 (12) 的 current-density Hilbert 拓扑和 (21) 的新设辛结构，(7)、(15)、(21)–(24) 构成一条完整、实际、非线性的 Hilbert Lagrangian 可积分系统，并精确回拉原半离散 DLW 时间。它的两组函数自由度并非有限维特殊解族；谱状态单射、微分单射、全实时间、增长渐近和完整等值集均已独立核实。

两项修辞必须保持精确：零均值 Q 的 Ψ 使用 (3) 的整体标量规范；逆谱坐标和 C¹ 轨道唯一性使用新 H¹ 密度拓扑。通常 C∞loc 拓扑的稳定逆已被 (13) 明确排除。

该特殊定理不推出一般物理场原半离散 DLW 的完整 Liouville 可积性，也不认证任何一般 M 原物理 Poisson 辛叶的最大各向同性。把候选记为「特殊增长分支 + 新设强辛结构的完整定理」是准确结论；把它记为此前一般物理目标已完成则证据不足。

审查证据：本文全部公式作了独立手推；`all_m_holonomy_image_audit` 子审再次独立核实了 (16)–(19) 的 uniform Laplace 渐近、(14)–(15) 的原时间标量规范和新密度拓扑内的唯一性，结论一致。未运行数值或 symbolic 检查，也未复跑任何旧证书。
