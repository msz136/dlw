# AKNS 谱作用量、strong 域真实流及零号谱约束独审

2026-10-11，mixed 独审 agent。只核查原物理 Poisson，不调用标准 AKNS bracket 代替它。来源为 [精确状态桥](akns_physical_state_inverse_bridge_20261011.md)、[actual 谱独审](spectral_m2_actual_poisson_independent_audit.md)、[strong 输送引理](spectral_m2_strong_domain_flow_bridge.md)，及 KLTZ2009 published §2.3 (2.15)、Propositions 2.7、2.9 的全文。原文：[DOI](https://doi.org/10.1007/s00220-008-0543-0)，[PDF](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf)。

## 1. 已核 normalization 与范围

取 \(M=2,\ S=2\delta\ne0\)，固定 \(\int u=\int v=0\) 的物理叶。普通积分梯度的原 tensor 是
\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\]
取 mean-zero \(K=D^{-1}_0P_0\)，
\[
q=-S+u,\quad V=-2uv/S,\quad
r=((\delta^2-v^2)(1+u/S)-v_x)/S,\quad
\theta=KV,\quad\eta=\operatorname{avg}V,
\quad a=e^\theta q,\ b=e^{-\theta}r.
\]
split traceless 系统经周期 diagonal gauge 化为
\[
w_x=((\lambda-\eta)H/2+aE+bF)w.
\]
fixed balancing \(\operatorname{diag}(\sqrt2,1/\sqrt2)\) 与 \(t=x/L\) 后，KLTZ 势为
\(\varphi_1=-iLa/2,\ \varphi_2=2iLb\)，谱参数
\[
z=\frac{iL}{2}(\lambda_{\rm orig}-B-\eta),\qquad
\Delta(z)=\mathcal F_{\eta-2iz/L}.
\tag{1}
\]
此处 \(\mathcal F\) 已是 centered normalized trace；原参数的中心位移是 \(B=\Gamma/(2c)\)，不是 \(2B\)。周期 gauge 与 fixed balancing 仅 conjugate monodromy，不产生遗漏的 scalar trace factor。

KLTZ Proposition 2.9 只给一般复势的零邻域双解析谱图；必须将背景 \((iL\delta,iL\delta)\) 和物理像放进适当小零邻域。没有可从文献取出的明确数值半径。使用下节 winding 证明时再缩为一个含零势的 complex ball，并在这整个 ball 上保持 fixed contours 与根分支。单独“背景属于某个连通分支”不足以取 winding 为零。

## 2. source-dependent shift 的完整变分

固定 \(z\)，实际 chain rule 是
\[
d\Delta(z)=d\mathcal F_\lambda+
(\partial_\lambda\mathcal F_\lambda)d\eta,\qquad
\lambda=\eta-2iz/L.
\tag{2}
\]
既有 actual 物理证明给 \(\{\mathcal F_\lambda,\mathcal F_\mu\}=0\)，
\(\{\mathcal F_\lambda,\eta\}=0\)，以及全部有定义的
\(\{\mathcal F_\lambda,C_m\}=\{\eta,C_m\}=0\)。
逐项代入 (2)，严格得到
\[
\{\Delta(z),\Delta(w)\}=\{\Delta(z),\eta\}
=\{\Delta(z),C_m\}=0.
\tag{3}
\]
所以 source shift 没有被略去；本证明也不需要 KLTZ tensor 的 canonical 性。

## 3. holonomy 变分为何准确消失

KLTZ (2.15) 的 normalization 是
\[
I_n=\frac1\pi\oint_{\Gamma_n}
z\,\frac{\Delta_z}{R}\,dz,\qquad R^2=\Delta^2-4.
\tag{4}
\]
每个 fixed counterclockwise contour 包围对应两根，\(R\) 在轮廓 annulus 上单值且不为零。该 local branch 条件已经足够作以下变分；不假定全局 arcosh 单值。
由 \(dR=\Delta\,d\Delta/R\)，
\[
d(\Delta_z/R)=\partial_z(d\Delta/R).
\]
对单值 annulus function 积分 \(\partial_z(z\,d\Delta/R)\)，得
\[
dI_n=-\frac1\pi\oint_{\Gamma_n}\frac{d\Delta}{R}\,dz.
\tag{5}
\]
又因 \(\Delta_z=(-2i/L)\partial_\lambda\mathcal F_\lambda\)，
\[
\oint\frac{\partial_\lambda\mathcal F_\lambda}{R}\,dz
=\frac{iL}{2}\oint\frac{\Delta_z}{R}\,dz
=\frac{iL}{2}\oint d\log(\Delta+R).
\tag{6}
\]
最后一步使用 \((\Delta+R)(\Delta-R)=4\)，故 \(\Delta+R\) 无零点，且
\((\Delta+R)'/(\Delta+R)=\Delta_z/R\)。
这个 integral 是 \(2\pi i\) 乘 winding。固定 contour/root 沿含零势小 ball 的同伦中连续，该整数不变。零势
\(\Delta=2\cos z,\ R=-2i\sin z\) 给 \(\Delta+R=2e^{-iz}\)，winding 为零；反号 root 给 \(2e^{iz}\)，也为零。因而 (6) 确为零。

若没有这条同伦条件，(5) 中的 \(\eta\) coefficient 一般等于 \(L\) 乘该 winding，而不能自行删去。当前小零邻域内没有这个问题。

于是精确原物理 Hamilton 场为
\[
\boxed{X_{I_n}=-\frac1\pi\oint_{\Gamma_n}
\frac{X_{\mathcal F_\lambda}}{R}\,dz,\quad
\lambda=\eta-2iz/L.}
\tag{7}
\]
每个固定 \(n\) 的 contour 与 centered parameter path 紧。既有 actual adjoint ODE 把 \(X_{\mathcal F_\lambda}\) 写成无 source 导数的 \(H^s\to H^s\) 解析映射，\(s\ge1\)，且 compact parameter 集上局部界一致。\(R\) 的 source-dependent weight 也是解析的。因此 (7) 是 actual order-zero Banach field，而不是 holonomy 平移 loss-one 场。

(3)、(5) 给全部 \(\{I_n,I_j\}=\{I_n,\eta\}=\{I_n,\mathcal F_\mu\}=\{I_n,C_m\}=0\)。复势上是双线性 holomorphic 身份；实际实叶取 Re/Im 的 real-type combinations。没有要求这些 action 非负或落在 NLS reality slice。源均值由 \(J=-\operatorname{offdiag}D/16\) 保持。

## 4. 在同一 strong 相域里的合法真实时间

令 \(\mathcal O\) 是上述物理 low \(H^1\) 开域，包含给定 strong presentation 的中心；固定 action contour 分支在 \(\mathcal O\) 内成立。对任一 fixed \(I_n\) 的实部或虚部，(7) 在较小 low ball 内给共同 Banach 时间 \(T_I>0\)。translation equivariance 及低阶解析流的参数微分给同一时间内所有空间光滑阶持久性。

既有 [strong flow bridge §§3–5](spectral_m2_strong_domain_flow_bridge.md) 的假设在此逐项成立：

1. \(X_{I_n}\) low order-zero 解析，且保持 \(C_m\) 和平移动量；所以 actual commutator 身份将每个旧有限 joint germ 输送为同一 \(C_m\) 方程的解。
2. 逐坐标缩旧 complex windows，一次冻结每个正宽；新增轴的 low-norm 变动用可求和预算控制。所有有限 joint images 因而处于同一个 \(\mathcal O\) 内。此步骤不要求一个含全部高阶局部 charges 的固定 Sobolev 开域。
3. \(T_I\) 对全部前缀一致。将输送后的 joint germs 取 mixed source corners，在必要时缩新的 \(C_m\) 坐标，以实际 finite mixed 唯一性识别中心。旧 \(I\)-parameter compact interval 保留，不随前缀趋零。
4. 参数 smoothness 对 compact parameter families 同样成立；反向 \(-t\) 给局部逆。因此它是同一 strong diffeology 的实际局部 flow，内部速度合法，并满足 \(\iota_{X_I}\omega=dI\)。

因此 KLTZ 的谱 actions 已得到原物理对合、实际 order-zero 时间和同一 weak symplectic \(\mathfrak S_\infty\) 接合。仍只允许任意有限个非零时间坐标。没有得到标准 AKNS angles 的物理 canonical 性、共同 fiber 正则性或 maximality。

## 5. 零号谱对宽度及真正 gauge 截面

这是新的独立局部结构结果，不借标准 AKNS bracket。原 traceless connection 在 \(\lambda=\pm S\) 为
\[
L_S=(u/2+v)H+2(\delta+v)E,\qquad
L_{-S}=(u/2-v)H-2(\delta-v)F.
\tag{8}
\]
它们为三角系统。\(\int u=\int v=0\) 使两 diagonal multipliers 均为 1，故对任意该均值叶物理场
\[
\mathcal F(S)=\mathcal F(-S)=2.
\tag{9}
\]
在 (1) 的 AKNS 参数中，对应两根为
\[
z_\pm=\frac{iL}{2}(\pm S-\eta),\quad
z_+-z_-=iLS,\quad (z_++z_-)/2=-iL\eta/2.
\tag{10}
\]

接下来在 full complex potentials \((a,b)\) 的 \(H^s\times H^s\) 背景
\((a^0,b^0)=(-S,S/4)\) 附近工作，整数 \(s\ge0\)。该域的 spectral equation 为
\(w_x=(-izH/L+aE+bF)w\)。
背景 \(\Delta_0(z)=2\cosh(L\sqrt{a^0b^0-z^2/L^2})\)，
在 \(z_\pm^0=\pm iLS/2\) 有
\(\partial_z(\Delta_0-2)=-2z_\pm^0=\mp iLS\ne0\)。
所以两根 \(z_\pm(a,b)\) 是局部 holomorphic simple-root functions，定义
\[
\mathcal W(a,b)=z_+(a,b)-z_-(a,b)-iLS.
\tag{11}
\]
背景 monodromy 变分的 cyclic integral 只取 source means；或直接对常数势公式变分，得到对任意 \((f,g)\)
\[
D\mathcal W_0(f,g)
=2iL\bigl(\operatorname{avg}g-\operatorname{avg}f/4\bigr).
\tag{12}
\]
因此 \(\{\mathcal W=0\}\) 是合法 holomorphic codimension-one Banach hypersurface。

令 \(a(u,v),b(u,v)\) 是精确状态桥的势，定义
\[
\Psi(u,v,\gamma)=(e^\gamma a(u,v),e^{-\gamma}b(u,v)).
\tag{13}
\]
constant diagonal conjugation 保持 discriminant，所以 (9)–(10) 给 \(\Psi\) 的像在 \(\{\mathcal W=0\}\)。在背景
\[
D\Psi_0(h,k,\gamma)
=(h-S\gamma,\ h/4-Dk/S-S\gamma/4).
\tag{14}
\]
它是
\(H^s_0\times H^{s+1}_0\times\mathbb C
\to\ker D\mathcal W_0\)
的有界同构。若目标为 \((f,g)\) 且
\(\operatorname{avg}g=\operatorname{avg}f/4\)，准确逆为
\[
\gamma=-\operatorname{avg}f/S,\quad h=P_0f,\quad
k=S K(f/4-g).
\tag{15}
\]
故 Banach IFT 在 hypersurface 图上给 (13) 的局部双解析逆。这个结论对 \(s=0\) 也合法：\(u\in L^2,v\in H^1\)，exact potential map 的乘法与 ODE analytic 已由状态桥证明。

物理 codimension-two potential image 因而准确等于 fixed-width hypersurface \(\mathcal W=0\) 上的 unique \(\gamma=0\) 截面；每个附近 fixed-width full potential 都唯一表示为 constant-diagonal gauge 乘一个原物理势。归一条件是原 map 的 mean-zero \(\theta\) 与这份 \(\Psi\) 逆所确定的 \(\gamma=0\)，不是任意加入的线性 mean gauge。KLTZ 双解析谱图可把这份 hypersurface/section 搬到其 Cartesian target，但其 physical Poisson operator 仍需独立计算。

尤其 \(n=0\) gap 并非额外自由谱 action，其 width 被固定；center 编码 \(\eta\)。这个结构把约束与 gauge 的一维来源准确分开，但尚未识别全部 nonlinear action level tangent，也未证明 cross-operator 的 Fredholm 性或最大各向同性。
