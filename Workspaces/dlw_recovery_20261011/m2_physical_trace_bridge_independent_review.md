# M2 fixed-original-parameter 谱场及 gauge 投影独审

2026-10-11。实际读取 [direct proof §§1–8](m2_physical_trace_poisson_closure_proof_20261011.md)，两份 fresh symbolic script 的源码（未重跑），AKNS 状态 inverse、其 zero-mean 独审稿及 [同一 strong 图 action 泛型证明](akns_actions_same_strong_chart_genericity_20261011.md)。以下独立手算验证实际梯度、标准场缩放、section derivative、全频闭包与同强域适用点。完整闭包不由有限机器检查认证；本次没有执行任何旧或新 symbolic 检查。

当前结论：在明确的小非零背景、指定零均值物理叶和共同 state/action 图范围，M2 的实际谱场及实际非中央 action 场，在原物理 \(C^\infty\) 拓扑下共同稠密生成全部 action differential kernel。该 kernel 在原物理形式下与自身正交空间相等；同一已建立的 strong weak-symplectic 相空间内部共同微分核也最大各向同性。一个固定 Hilbert 参数球的 residual 非空子集同时具有全部非中央 actions 非零及任意有限 real action 块内部独立性。本稿不证明实际共同 fiber 的内部 tangent 等于该微分核、fiber inclusion 无 ghost、regular fiber/manifold 或全 M 的非线性闭包。

## 1. source-dependent spectral shift 与梯度

固定原 centered \(\lambda\)，实际谱泛函是
\(\mathcal F_\lambda=T_{\lambda-\eta}(a,b)\)。
原 periodic adjoint \(W=\left(\begin{smallmatrix}h&E\\F&-h\end{smallmatrix}\right)\)
满足
\[
E_x=(\lambda-V)E-2qh,\quad F_x=(V-\lambda)F+2rh,\quad
h_x=qF-rE.
\]
由 \(q=u-S,r=A(S+u)-v_x/S,V=-2uv/S\)，Duhamel 变分与周期 integration by parts 给
\[
g_u=F+AE+2vh/S,\qquad g_v=(\lambda-2v)E/S+2h.
\tag{1}
\]
这里 \(g_v\) 中 \(-2v(1+u/S)E/S+E_x/S+2uh/S\)
代入 adjoint 式后恰成为 (1)，不是猜测。fixed-\(\zeta\) gradient 含
\(h-\langle h\rangle\)；chain-rule 项
\(-L\langle h\rangle d\eta\) 准确补上两均值项，不能漏去。

由 \(X=(-Dg_v,-Dg_u)/16\)，准确无 source 导数形式为
\[
u_t=-qF/8+A(S+u)E/8+
(\lambda-2v)qh/(8S)
-\frac{(\lambda-2v)(\lambda-V)}{16S}E,
\tag{2}
\]
\[
v_t=(\lambda+2v)F/16-A(\lambda-2v)E/16-SA h/4.
\]
最初读到的 direct 稿展示式 (7) 漏了 (2) 最后一项，已经向作者/根报告；此漏项若不补会与其式 (10) 矛盾。两份 actual scripts 都取
\(u_t=-Dg_v/16\)，没有用漏项展示式，因此证书的核心身份不受此排印错误影响。

## 2. actual potential pushforward

定义
\[
R_0=SF+(\lambda v/S-v^2/S-S/4)E+(2v-\lambda)h.
\]
adjoint identities 与 (2) 给
\[
V_t=D R_0/(8S),\quad\eta_t=0,\quad
\theta_t=(R_0-\langle R_0\rangle)/(8S).
\]
特别 \(a_t=e^\theta(u_t+q\theta_t)\) 的 F、h 项相消；其 E coefficient 乘 \(16S\) 后准确是
\[
2SA(S+u)+2q(\lambda v/S-v^2/S-S/4)
-(\lambda-2v)(\lambda-V)=S^2-\lambda^2.
\]
同样对 \(b=e^{-\theta}r\) 用
\(r_t=A u_t-2v(1+u/S)v_t/S-Dv_t/S\) 得
\[
D(a,b)X_{\mathcal F_\lambda}
=\omega_\lambda Y_{\lambda-\eta}
-\langle R_0\rangle Q/(8S),
\quad
\omega_\lambda=(S^2-\lambda^2)/(16S),
\tag{3}
\]
其中 \(Y_\zeta=(e^\theta E,-e^{-\theta}F)\)，\(Q=(a,-b)\)。

这是 full physical 原谱参数场的精确 identity。它不是 fixed-AKNS-parameter 的无 shift 场，不是完整 physical tensor 与 standard tensor 相等。
两份 scripts 已实际读到 (3) 的 direct identities，15/16 项证书只作代数校准，未重新执行。

## 3. KLTZ 标准场的系数

KLTZ2009 的 source convention 是 \(+i\) 乘 standard skew tensor。
其 \(\varphi_1=-iLa/2,\varphi_2=2iLb,\ t=x/L\)。
若 \(dT_\zeta=\int_0^L(f\,da+e\,db)dx\)，在 ordinary \(dt\) pairing 的 gradient 转换多一个 \(L\)。设 \(A_\varphi=\operatorname{diag}(-iL/2,2iL)\)，则
\[
A_\varphi^{-1}(iJ_0)L A_\varphi^{-T}
=\frac iL J_0,\qquad J_0=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]
所以 standard KLTZ trace field 在 \((a,b)\) 中为
\((i/L)Y_\zeta\)，(3) 主项等于
\[
-iL\,\omega_\lambda\,X^{\rm std}_{T_\zeta}.
\tag{4}
\]
KST2015 使用整体相反的标准 bracket 及交换的 complex pair convention；不能把这两套 sign 混在同一个式中。本审计的 (4) 与 direct 稿所采用的 KLTZ convention 一致。闭包不依该非零 scalar，但 exact identity 依赖它。

## 4. 不同 gauge representatives 的真正 chain rule

令 full Birkhoff gauge generator
\(G=(-w_n,z_n)_n\)，\(d\vartheta_0(G)=i\)。
设 \(p\) 是 actual physical potential 代表，\(s=g_{\gamma(p)}p\) 是 fixed-central-angle 代表。
actual section map derivative 是
\[
Ds_p(v)=g_{\gamma(p)*}v+(d\gamma_p v)G_s.
\]
由 \(d\vartheta_0(Ds_p(v))=0\) 得
\[
d\gamma_p(v)=-d\vartheta_{0,s}(g_*v)/i,\qquad
Ds_p(v)=\Pi_s(g_*v),\quad
\Pi_s=I-G_s\,d\vartheta_{0,s}/i.
\tag{5}
\]
constant gauge 保 \(T_\zeta\)，且 standard canonical tensor 等变，因此
\(g_*Y_\zeta(p)=Y_\zeta(s)\)；\(g_*Q(p)=G_s\)，而 \(\Pi_sG_s=0\)。
把 (3) 代入 (5)，再读 noncentral coordinates，准确给
\[
DR\,X_{\mathcal F_\lambda}
=\omega_\lambda\Pi_sY_{\lambda-\eta}(s).
\tag{6}
\]
没有额外漏掉的 state-dependent \(\gamma\) derivative；它正是 projection 中减去的项。若不先写 (5)，把 \(\Pi_p\) 硬换为 \(\Pi_s\) 会欠一个 chain-rule 说明。当前完整推导弥补这一点。

需保留实际 state inverse 的小非零背景/zero-connected action-factorization 图，以及 \(I_0\ne0\) 的中央 angle local branch。
\(\chi=\widehat\chi(I)\) 保证 \(Y_\zeta\) tangent to \(\chi=0\)，
\(\eta=\widehat\eta(I)\) 保证它在 fixed-\(\lambda\) 过程中不会再引入未记录的 \(\eta\) 方向。没有宣布这份 gauge section 是标准 NLS symplectic reduction。

## 5. 闭包末端所需的共同微分核身份

这一部分为后续 direct closure 提供一个实际有限渐近引理。
在任何 smooth physical tangent \(v\)，若
\(d\mathcal F_\lambda(v)=0\) 对所有 centered \(\lambda\)，则由已证 actual
\[
\mathcal K_\lambda
=\operatorname{arcosh}(\mathcal F_\lambda/2)-\lambda L/2+L\eta/2
=O_{C^1(H^3)}(\lambda^{-1})
\]
得 \(d\mathcal K_\lambda(v)=Ld\eta(v)/2\)。令正 \(\lambda\to\infty\)，故
\(d\eta(v)=0\)。完整 chain rule
\(d\Delta(z)=d\mathcal F_\lambda+\mathcal F_\lambda'd\eta\)
于是给 \(d\Delta(z)(v)=0\)，轮廓得到全部 \(dI_n(v)=0\)。
反方向：full action-only \(\Delta=d(z,I)\)、\(\eta=\widehat\eta(I)\) 及
\(I_0=\rho(I_{n\ne0})\) 给
\(\mathcal F_\lambda=\widehat F_\lambda(I_{n\ne0})\)。
因此在该实际 state 图上
\[
\bigcap_\lambda\ker d\mathcal F_\lambda
=\bigcap_{n\ne0}\ker dI_n.
\tag{7}
\]
这是 actual \(C^1\) quasimomentum 引理，不是假定谱 shift 没有新自由度。

若 direct 后续证明有限 actual trace Hamilton span 的 ambient Fréchet closure 是 (7) 的共同 kernel，physical involution 和 \(\Omega\) 连续便使该 kernel isotropic；同时 Hamilton identity 给该 span 的 symplectic annihilator 正是 (7)，故这个 kernel 与自身 orthogonal 相等。
在 strong 域中只取其实际内部 tangent image 的交集，并以 ambient 相对拓扑取闭包。仍不推出 inherited fiber tangent 等于 kernel、fiber ghost 消失或 regular integral leaf。

此前 §§1–4 的 exact pushforward/normalization/projection 已通过，展示式缺项也已由作者实际补正；本稿 (7) 的 actual kernel 引理是独立第二条核验。以下补审 direct 新 §§4–8 的闭包论证，并核实其同一 strong 域非空性输入，取代此前“闭包待后续独审”的状态。

## 6. 完整 trace span 的逐频闭包

令 \(R\) 为 common low-domain reduced Cartesian state 图，实际 smooth derivative
\[
DR_x:E^\mathbb C_\infty\longrightarrow s^2
\]
是 Fréchet 连续线性同构，其中 \(s=\bigcap_Nh^N(\mathbb Z\setminus\{0\})\)。各高阶图均是同一低阶 domain 的 restrictions，不是随 \(N\) 另取 source 半径。物理图通过 unique constant-gauge 变换对应 \(\vartheta_0=\vartheta_0^*\) section；§4 的实际 chain rule 保证 (6) 正是该 representative 上的 identity。

在所有非中央 \(I_n=w_nz_n\ne0\) 的点，设
\[
K_x^\mathbb C=\bigcap_{n\ne0}\ker dI_n(x),\qquad
\mathcal H_x^\mathbb C=\operatorname{span}_{\mathbb C}\{X_{\mathcal F_\lambda}(x)\}.
\]
任意 Cartesian common-kernel 速度满足
\[
z_n\dot w_n+w_n\dot z_n=0,
\]
故每个 pair 是 \(c_n(-w_n,z_n)\)。其有限 pair 截断在每个 \(h^N\) 中收敛，因为被截断的是已经 rapidly decreasing 的速度。无需 \(c_n\) 快衰减，也无需 \(|I_n|\) 的统一下界。

full standard action 场在 KLTZ2009 convention 中是
\[
X^{\rm std}_{I_n}=iG_n,\qquad G_n=(-w_n,z_n)
\]
（只作用第 \(n\) pair）。它的中央 pair 为零，因此
\(\Pi X^{\rm std}_{I_n}=X^{\rm std}_{I_n}\)。按 §3 的 rescaling，\(Y_{I_n}=LG_n\)。
full contour identity 是
\[
Y_{I_n}=-\frac1\pi\oint_{\Gamma_n}\frac{Y_{T_{-2iz/L}}}{R(z)}\,dz.
\]
将 (6) 代入，得到一个固定基点的 tangent identity
\[
LG_n=-\frac1\pi\oint_{\Gamma_n}
\frac{DR_xX_{\mathcal F_{\eta(x)-2iz/L}}(x)}
{R(z)\omega_{\eta(x)-2iz/L}}\,dz.
\tag{8}
\]
此处 \(\eta(x)\)、\(\omega\) 与所有 scalar weights 冻结在 \(x\)。式 (8) 不把 state-dependent division 宣称为附近的 Hamiltonian 场。

每个 contour 可在其 branch-free annulus 内变形避开两个 regular points \(\lambda=\pm S\)；在指定小图中这些点对应中央两根，非中央轮廓亦可直接与它们分离。无需所有轮廓统一分离距离。该固定 contour 上 \(R\omega\) 不为零且有正的模下界；actual fundamental ODE、空间微分 ODE、gauge 和固定 \(DR_x\) 保证 integrand 在每个 smooth seminorm 连续。一次逐渐细分的有限 Riemann sums 在每个 seminorm 都收敛，故 \(G_n\in\overline{DR_x\mathcal H_x}\)。再对任意 common-kernel 速度作有限 pair 截断，利用 \(DR_x^{-1}\) 的 Fréchet 连续性，得到
\[
K_x^\mathbb C\subset\overline{\mathcal H_x^\mathbb C}.
\]
反包含由全部 actual \(\{\mathcal F_\lambda,I_n\}=0\) 及各 \(dI_n\) 连续给出。因此
\[
\boxed{\overline{\mathcal H_x^\mathbb C}^{\,E_\infty}=K_x^\mathbb C.}
\tag{9}
\]

这里 central constraint 不能略去：full action-dependent trace \(d(I)\) 经 \(\Pi\) 投影后的 angular coefficient 是
\(\partial_{I_n}d-\partial_{I_0}d\)，而 reduced restriction \(d(\rho(J),J)\) 的 differential coefficient 是
\(\partial_{I_n}d+\rho_n\partial_{I_0}d\)。两者通常不同。证明使用 full \(I_n\) 的 contour 场，再投影；它的 \(\partial_{I_0}I_n=0\)，从而准确产生单 pair \(G_n\)。这避免把实际 section 错当 standard canonical reduction。

## 7. 实际 action 场与 trace 场具有相同闭包

direct 新 §4.4 增加的转置步骤必要且正确。单有 (9) 不能自动将 trace 场替换成原物理 action 场。
full KLTZ canonical identity
\[
DB\,J_{\rm pot}(DB)^*=J_{\rm seq},\qquad
(DB)^*=J_{\rm pot}^{-1}(DB)^{-1}J_{\rm seq}
\]
只用于控制已知谱图的转置正则性。standard tensors 均为 invertible order-zero constant operators，common-domain inverse 在 smooth 点对所有阶 \(h^N\to H^N\) 有界，所以 \((DB)^*\) 同阶连续。不需要 KST 一阶 smoothing，也没有在此识别 physical tensor 与 standard tensor。

fixed-central-angle normalization 的 derivative 是 diagonal scaling 加 gauge vector 乘中央 covector；其 transpose 是 scaling 加 finite-central-rank operator，在 smooth 点对所有高阶 sequence norms 连续。非中央 projection 的 transpose 只补一个零中央 pair。physical potential derivative 与 transpose 保留实际内容：
\[
\Lambda=E_\theta(M+jKc),\qquad
\Lambda^*=(M^*-c^{\mathsf T}Kj^{\mathsf T})E_\theta,\qquad K^*=-K,
\]
\[
M=\begin{pmatrix}1&0\\A&B-D/S\end{pmatrix},\quad
M^*=\begin{pmatrix}1&A\\0&B+D/S\end{pmatrix},\quad
B=-2v(1+u/S)/S.
\]
在固定 smooth 点各系数 smooth，因而 \(DR_x^*:s^2\to E_\infty^\mathbb C\) 与
\(J_{uv}DR_x^*:s^2\to E_\infty^\mathbb C\) 都连续；后一 map 的 order \(N\) 半范数至多用 order \(N+2\) sequence 半范数控制。固定有限阶损失在 Fréchet \(C^\infty\) 拓扑中没有障碍。

由完整 actual action factorization
\[
\mathcal F_\lambda=t(\lambda-\widetilde\eta(J),\rho(J),J)
\]
在 \(\ell^1\) action domain 的 analyticity，固定 \(x,\lambda\) 后
\[
\beta_n=\partial_{I_n}t+\rho_n\partial_{I_0}t
-(\partial_\zeta t)\,\partial_{J_n}\widetilde\eta
\]
属于 \(\ell^\infty\)。准确的 reduced Cartesian covector 为
\((\beta_nz_n,\beta_nw_n)\in s^2\)。有限截断在每个 \(h^N\) 中收敛，将其经连续的 \(J_{uv}DR_x^*\) 推前，得到
\[
X_{\mathcal F_\lambda}(x)
=\lim_{k\to\infty}\sum_{0<|n|\le k}\beta_n(x,\lambda)
X^{\rm physical}_{I_n}(x)
\quad\text{于 }E_\infty^\mathbb C.
\tag{10}
\]
没有把 \(\beta\) 宣称为 projected standard angular coefficient；它包含 central constraint 及 holonomy shift 的完整 chain rule。

反向包含来自已独审的 actual action identity
\[
X^{\rm physical}_{I_n}(x)
=-\frac1\pi\oint_{\Gamma_n}\frac{
X_{\mathcal F_{\eta(x)-2iz/L}}(x)}{R(z)}\,dz.
\]
其中 source-dependent shift 的 \(d\eta\) coefficient 为
\(-iL(2\pi)^{-1}\oint d\log(\Delta+R)=0\)，正是 zero-connected root homotopy 的 winding cancellation。固定 compact contour 的 Riemann sums 再次在 \(E_\infty\) 收敛。由 (9)、(10)，
\[
\boxed{\overline{\operatorname{span}_{\mathbb C}X^{\rm physical}_{I_n}}=
\overline{\mathcal H_x^\mathbb C}=K_x^\mathbb C.}
\tag{11}
\]

## 8. 原 real structure、最大微分核与实际 fiber 的区别

在 real physical source，原 actual connection 有
\(\overline{\mathcal F_\lambda}=\mathcal F_{\bar\lambda}\) 及
\(\overline{X_{\mathcal F_\lambda}}=X_{\mathcal F_{\bar\lambda}}\)。
取复杂有限线性组合的 real parts，即得 (9)、(11) 的实际 real form；无须假定 reduced Cartesian reality 是 standard NLS real slice：
\[
\overline{\operatorname{span}_{\mathbb R}
\{X_{\Re\mathcal F_\lambda},X_{\Im\mathcal F_\lambda}\}}
=
\overline{\operatorname{span}_{\mathbb R}
\{X_{\Re I_n},X_{\Im I_n}\}}=K_x^\mathbb R.
\tag{12}
\]
\(K_x^\mathbb R\) 是全部 real/imaginary action differential 的共同 kernel。

原物理 \(\Omega\) 连续且满足
\(\Omega(X_f,v)=df(v)\)。actual involution 令 finite span isotropic，连续性令其闭包 \(K_x^\mathbb R\) isotropic。若 \(v\) 与 \(K_x^\mathbb R\) 正交，则与每个 realified trace 场正交，所以全部 \(d\mathcal F_\lambda(v)=0\)；§5 的 actual kernel identity 或 winding-cancel contour identity 给全部 \(dI_n(v)=0\)。因此
\[
\boxed{(K_x^\mathbb R)^{\perp_\Omega}=K_x^\mathbb R.}
\tag{13}
\]

同一 strong domain \(\mathfrak S_\infty\) 的 ambient evaluation
\[
j:T_x^{\rm internal}\mathfrak S_\infty\longrightarrow E_\infty^\mathbb R
\]
**已由 mixed §16.4 证明单射**，原 weak form 是 \(\omega=j^*\Omega\)。令
\[
\mathcal A_x=\bigcap_{n\ne0}\ker d(\Re I_n,\Im I_n)
\subset T_x^{\rm internal}\mathfrak S_\infty.
\]
已有真实有限 trace/action 流给内部 Hamilton directions，且全部这些 directions 属于 \(\mathcal A_x\)。由 \(j(\mathcal A_x)\subset K_x^\mathbb R\) 得 isotropy；若内部 \(\xi\) 与 \(\mathcal A_x\) 正交，则与内部 trace directions 正交，故全部 \(d\mathcal F_\lambda(j\xi)=0\)，再给 \(\xi\in\mathcal A_x\)。于是
\[
\boxed{\mathcal A_x^{\perp_\omega}=\mathcal A_x.}
\tag{14}
\]
这是已建立 weak-symplectic phase 内部的共同**微分核**最大性，不是 actual fiber tangent identity。

实际 level subset \(Y_x\subset\mathfrak S_\infty\) 取 inherited diffeology，设
\(V_x=\operatorname{im}(T_x^{\rm internal}Y_x\to E_\infty^\mathbb R)\)。
全部 plots 的 action derivatives 零，所以 \(V_x\subset K_x^\mathbb R\)；有限 actual commuting flow compositions 给 \(V_x\) 包含 (12) 中 finite span。因此
\[
\overline{V_x}^{\,E_\infty}=K_x^\mathbb R,\qquad
V_x^{\perp_\Omega}=K_x^\mathbb R.
\tag{15}
\]
尚未证明 \(V_x=K_x^\mathbb R\)、\(T^{\rm internal}Y_x\to T^{\rm internal}\mathfrak S_\infty\) 单射或 regular common-level manifold。未知的可能 ghost 属于这个 **fiber inclusion**；不能据此重新说 phase \(j\) 有 ghost。原内部 tangent 是代数 colimit，闭包陈述始终在 \(j\) 的 ambient Fréchet 图像中取，不凭空加 colimit topology。

## 9. 同一 strong 参数图中的 actual action 非零与有限独立性

实际读回 [同图 action 泛型稿 §§1–6](akns_actions_same_strong_chart_genericity_20261011.md)，以下核验精确 Hessian、原实索引与 Baire；不由 gap-open 推断 action 非零。

保留该稿列出的全部小背景/mean-leaf/factorization-domain 条件。对 \(n>0\)，
\[
k_n=2\pi n/L,\quad \omega_n=\sqrt{k_n^2-4\delta^2},\quad
\gamma_n=\omega_n/k_n>0,\quad S=2\delta.
\]
背景 \(\Delta_0(z)=2\cos w(z)\)，\(w(z)=\sqrt{z^2+L^2\delta^2}\sim z\)。
旧 physical \(\lambda_n=i\omega_n\) 对应 KLTZ index \(-n\)：
\[
z_{-n}^*=iL\lambda_n/2=-\pi n\gamma_n,\quad
w(z_{-n}^*)=-n\pi,\quad w'(z_{-n}^*)=\gamma_n.
\]
canonical root \(R_0=-2i\sin w\) 在该点 derivative 为
\(-2i(-1)^n\gamma_n\)。actual Born trace 给
\[
\Delta(z_{-n}^*;\varepsilon\xi)
=2(-1)^n+\varepsilon^2(-1)^n\mathcal B_n(\xi)+O(\varepsilon^3).
\]
全指定 zero-mean source 的 first trace variation 零；\(\eta=O(\varepsilon^2)\) 的 shift correction 乘背景 \(\mathcal F_0'(\lambda_n)=0\)，所以该点的二阶 coefficient 没有遗漏 holonomy。

由 actual contour variation，一次 residue 计算给
\[
I_{-n}(\varepsilon\xi)
=-\frac{\varepsilon^2}{\pi}\oint
\frac{\Delta_2(z;\xi)}{R_0(z)}\,dz+O(\varepsilon^3)
=\frac{\varepsilon^2}{\gamma_n}\mathcal B_n(\xi)+O(\varepsilon^3).
\]
其中 \(-2i\,(-1)^n\mathcal B_n/
[-2i(-1)^n\gamma_n]=\mathcal B_n/\gamma_n\)。
使用已核定 Fourier canonical \(Q_nP_n=\mathcal B_n/K_n\)，
\(K_n=Lk_n^2\gamma_n/(16S)\)，准确得到
\[
\boxed{I_{-n}^{[2]}(\xi)=\kappa_nQ_nP_n,\qquad
\kappa_n=Lk_n^2/(16S)\ne0.}
\tag{16}
\]
\(D^2I[\xi,\xi]\) 是该 quadratic coefficient 的两倍。不能把 (16) 升级为全 nonlinear gap/action 比例。

原 real source 的 \(\Delta(-\bar z)=\overline{\Delta(z)}\)、同 canonical branch 的
\(R(-\bar z)=\overline{R(z)}\) 给 \(I_{-n}=\overline{I_n}\)。
变元 reflection 反转轮廓 orientation，配合 \(\Delta_z\) 与 \(dz\) 两个负号，action integral 的结果为 conjugate，符号正确；未假定 Cartesian pair 的 NLS 实性。

mixed §17 已给一个固定 holomorphic \(\mathcal P:B_R(H_\mathbb C)\to E_\infty^\mathbb C\)，
\(\mathcal P(0)=0\)，\(D\mathcal P(0)\) range 包含全部 real finite Fourier directions；每个 real finite-dimensional precomposition 是同一 \(\mathfrak S_\infty\) 的 actual strong plot。
只缩一次 \(R\)，其整个像落在所有 actions 的共同 low source ball。该球来自 KLTZ 的共同 zero neighborhood，不能对每个 action 重新选择互不相容的 source radius；固定 contours 可各有不同常数。

任给 finite positive set \(E\)，选 actual real Fourier \(\xi_E\) 满足 \(Q_n=P_n=1\) 于 \(E\)，及测试 directions \(\delta Q_n=0,\delta P_n=1,i\)。各自有 fixed real Hilbert 原像。由于所有 \(DI_n(0)=0\)，复合 Hessian 不含 \(DI_nD^2\mathcal P\) 项。沿 actual strong curve \(\mathcal P(\varepsilon\widehat\xi_E)\) 的 real action differential 矩阵是
\[
\varepsilon\,\operatorname{diag}(\kappa_n,\kappa_n)_{n\in E}
+O(\varepsilon^2);
\]
其 minor leading term 是
\(\varepsilon^{2|E|}\prod_{n\in E}\kappa_n^2\ne0\)，而各 selected actions 为
\(\varepsilon^2\kappa_n+O(\varepsilon^3)\ne0\)。这里 actual curve 一般不同于有限 Fourier Cauchy 初态，未将后者擅自置入 strong domain。

每个 \(I_{-n}\circ\mathcal P\) 和各 fixed prefix minor 是同一个 real Hilbert 球上的 real-analytic nonzero function，故非零集 open dense：若在一个 open subball 恒零，连通球内解析线段 identity 延拓将违反上述小 \(\varepsilon\) 见证。real Hilbert open ball 是 Baire，countable intersection 因而 residual、dense、非空。
同一个 actual \(x=\mathcal P(a)\in\mathfrak S_\infty\) 同时拥有全部 noncentral \(I_n\ne0\) 及每个 finite real action block 在 actual internal plot directions 上独立。可以和此前 charges/gaps 各族的 residual 条件相交；没有宣称这些不同守恒量族的合并族独立。

因此 §§6–8 的 action-regular strong state 范围非空，并且在这个固定 Hilbert 参数图中有 residual 参数集。它不证明整个 \(\mathfrak S_\infty\) 的 D-topological genericity、某个 ambient open Cauchy domain 全部状态可解，或全 \(M\) nonlinear maximality。

## 10. 核验范围与下一缺口

以上把 M2 下的 exact physical field bridge、ambient trace/action closed span、同一 weak phase 内部共同微分核最大性，以及同图 actual action 非零/finite independence 完整接合。原 physical Poisson tensor 始终是 \(-\mathrm{offdiag}\,D/16\)；辅助标准 canonical 图只用于 state inverse、full angular generation 与转置正则性。

全有限 \(M\) 的 actual spectral commutativity、与 \(C_n\) 对合及同一 strong-domain finite flow 接合已在 [all-M 独审](all_m_actual_spectral_independent_audit.md) 成立。本稿的 nonlinear Cartesian state inverse 和闭包最大性仍仅 M2，不向 \(M>2\) 外推。实际 common fiber regularity、fiber 内部切映射单射/ghost 排除及 unclosed tangent equality 仍未建立。
