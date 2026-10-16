# M2 完整条件定理陈述：独立 scope 审查

2026-10-11。实际逐段读取 [定理陈述](m2_conditional_theorem_statement_20261011.md)，并对照 mixed 独审 §16–17、exact AKNS 状态图 B1–D7、direct closure §§1–8 及既有 actual spectral/action strong flow 独审。本次只核数学陈述和分析适用范围，没有重跑任何证书，没有修改共享定理稿、报告或 STATE。

初读定理源 SHA256：37E86AD05F10BB42506B958F0638F77BE4B1D306655AFE0B15CF3E6E8BD135B7。
审查结论为 PASS，附下面一处必须明确的背景导数定位和一处局部时间措辞建议；没有发现七项核心结论的新增数学缺口。

## 1. 应精确修正的导数定位

§2 写“χ=χ̂(I) 且 ∂I₀χ=4”。已证明的精确量是
\[
\partial_{I_0}\widehat\chi(I^*)=4
\]
在均匀背景 \(I^*=(I_0^*,0,\ldots)\)，并由连续性在小域内非零。
它足以给 scalar analytic IFT 和 \(I_0=\rho(J)\)；没有证明整个 action domain 上该偏导恒等于四。请补上背景标记，避免将 IFT 校准写成全域恒等式。该修正不改变结论或域。

§3 的“有限块独立由守恒和局部可逆流保持”可进一步明确为：任给一个固定有限 action 块和它的有限测试 plots，在其共同局部时间 germ 上由实际时间换窗与反向时间保持独立。每个 fixed finite list 的实际谱 Banach 流已有共同小时间；全部 \(C_n\) 的存在陈述则是逐坐标和 plot-wise 的局部 germs，没有证明整个 \(\mathfrak S_\infty\) 的一个 D-open 初值域具有统一普通 Cauchy 流时间。现稿前后已经保留这一区别，此建议使该句不被孤立误读。

## 2. 原物理条件及任意 Γ 的恢复

手核原重构式
\[
w_\pm=c\pm8v/h,\qquad
U_\pm=\Gamma/c-2uv/S\pm u,\qquad S=hc/4
\]
给
\[
\Pi w=c,\qquad
\Pi(Uw)=c(\Gamma/c-2uv/S)+8uv/h=\Gamma.
\]
因此约束不是额外限制 \(u,v\) 的函数自由度。所固定的 leaf 是
\(\langle p_\pm\rangle=0,\langle w_\pm\rangle=c\)，共同 \(U\) 均值仍为
\(\Gamma/c-2\langle uv\rangle/S\)，没有误将它再固定。
\(c\) 沿一条原轨道恒定来自兼容；不同 leaf 可取不同非零 \(c\)。

Γ(t) 的原非自主贡献是速度 \(\Gamma(t)/c\) 的空间平移。令
\(a'(t)=\Gamma/c\)，则 \(u_\Gamma(t,x)=u_0(t,x-a(t))\) 给
\(u_{\Gamma,t}=u_{0,t}-(\Gamma/c)u_{\Gamma,x}\)，\(v\) 同理，再代入重构恢复原流。必须同时用
\(\lambda_{\rm original}-B(t)\)、\(B=\Gamma/(2c)\) 和已记录 scalar multiplier 中心化；定理正确保留。没有另要求 Γ 常数、守恒或零。

## 3. 状态开图与 strong 相域确实不同

一份 \(\mathcal O_{\rm red}\subset L^2_0\times H^1_0\) low open domain 的全部
\(H^N_0\times H^{N+1}_0\) restrictions 给 full noncentral Cartesian state inverse。这不是逐高阶缩小彼此不同的 source radius；exact potential inverse、full KLTZ weighted inverse 和中央有限 scalar choices 提供 same-domain bootstrap。
complex physical potential image codim two；\(\chi=0\) 是 gauge saturation 的单一谱约束，unique constant gauge section 再消去一个方向，所以完整非中央 Cartesian 图没有隐含 extra sequence constraint。没有声称该图原物理 canonical。

strong 相域的 chain、共用冻结旧复内窗口、角点 coherent 源族、center 值识别和 finite-dimensional plots，与 mixed §16.1 定义一致。每个 plot 局部共用一条实际链；不是只要求其每个点各自拥有一份不能比较的 real-time 解。
各 \(E_j\) 来源于 odd real mixed 或 even imaginary-time mixed 的 actual construction；even 时间经 reflection 回到原 real Hamilton 方程。

ambient smooth topology 的 relative open sets 是 D-open，故
\(\tau_{\rm ambient}\subset\tau_D\)；相等未知。internal tangent 是 pointed plot germs 的代数 colimit，未被赋予未经证明的 Fréchet topology。定理在 (7)–(8) 明确只用 ambient \(C^\infty\) closure，正确。

## 4. 同一个 strong 参数球的非空无限函数自由度

mixed §17 的 holomorphic \(\mathcal P:B_R(H_\mathbb C)\to E_\infty^\mathbb C\) 固定一份参数球及全部旧正窗口，derivative range 包含所有 finite physical Fourier directions。它的 finite-dimensional smooth precompositions 都是 actual strong plots；未当作 onto 相空间 chart。

actual contour residue 给
\[
I_{-n}^{[2]}=\kappa_nQ_nP_n,\qquad
\kappa_n=Lk_n^2/(16S)\ne0.
\]
原 real source 的 reflection 给 \(I_{-n}=\overline{I_n}\)，不需要 Cartesian coordinates 属 standard NLS reality。每个 finite action minor 由同球内的 actual Hilbert preimage directions 给非零 analytic witness；因背景 \(DI_n=0\)，复合 Hessian 无 \(DI_nD^2\mathcal P\) correction。
所有 actions 的 analyticity 来自一个共同 KLTZ low source ball；只缩一次 \(R\)，不随 action 索引另缩球。Baire 可数交因此在同一实 Hilbert 参数球得到 residual、dense、非空集，给同一个真实 strong 状态所有 finite action 块内部独立和所有 noncentral actions 非零。

full state 开图 (3) 具有无限函数自由度；strong 参数图在背景有任意高 finite rank，在 regular residual 点也因全部 finite minors 非零有无限 rank。它们不证明 strong 集在 ambient \(E_\infty\) 中开放，也不证明 residual 的参数像在 phase 的 D topology 泛型。定理对此区分充分。

## 5. 原 Hamilton 时间、有限共同流与原弱形式

直接变分
\[
K=\int(16vu_x+4Su^2+16Sv^2-16u^2v^2/S)
\]
给
\[
K_v=16u_x+32Sv-32u^2v/S,\qquad
K_u=-16v_x+8Su-32uv^2/S.
\]
原 \(J=-\mathrm{offdiag}\,D/16\) 因而给定理 (5)，符号及系数正确。
由 \(C_1=-\int qr\) 和周期分部积分得
\(K=-16SC_1+4LS^3\)，没有重复把 \(K,C_1\) 算作独立积分。

定理保持每个旧轴自己的正窗口，实际 finite supported time lists 有 joint germs、交换及反向换窗群律；没有定义 infinitely many simultaneously nonzero times。
normalized fixed spectral traces 与 actions 的 realified 场是 actual order-zero Banach analytic 场，它们和全部 \(C_n\) 对合；strong transport 一次固定旧复轴窗口，按 old complex corners 重新 mixed 参数化，保证仍在同一 \(\mathfrak S_\infty\)。没有由 auxiliary Fréchet tangent identity 直接推不存在依据的 ODE 解。

手核
\[
J^{-1}=-16\begin{pmatrix}0&D_0^{-1}\\D_0^{-1}&0\end{pmatrix}
\]
得到定理 (6)，且 \(\Omega(X_H,W)=dH(W)\)。\(D_0^{-1}\) 在 zero-mean smooth 空间连续和 skew，故该形式连续、闭、弱非退化。
mixed §16.4 的相对坐标轴/抛物线延拓证明 phase evaluation \(j\) 单射；§16.5 在同一基点给其像稠密。定理没有再次把仅单个 center map 的注入冒充 internal injectivity。由两事实和 \(\Omega\) 连续得到 \(\omega=j^*\Omega\) 的真实内部弱非退化、唯一 Hamilton 速度，正确。

## 6. 谱完备性、内部共同核及实际 fiber

实际读回 direct closure。精确 \(DR X_{F_\lambda}=\omega_\lambda\Pi Y_{\lambda-\eta}\) 的
\(\omega_\lambda=(S^2-\lambda^2)/(16S)\) 及 gauge section derivative 均已手核。full standard action contour 先产生单角方向后投影，绕开 full versus reduced coefficient 的区别；固定 compact contour 避开两点 \(\lambda=\pm S\)，Riemann sums 在每个空间半范数收敛。随后截断已经 rapidly decreasing 的速度，无需 action/gap inverse 的全频下界。

actual action span 等于 trace span 的 closure 需要另一真实步骤：\(DB^*\) 由 standard canonical identity 及 common high inverse 同阶连续；physical \(\Lambda^*\) 加原 \(J\) 至多固定两阶损失；reduced action coefficient \(\beta\in\ell^\infty\) 给 smooth covector
\((\beta z,\beta w)\)，有限截断严格推至 actual \(X_F=\lim\sum\beta_nX_{I_n}\)。
反向 action contour 的 \(\eta\)-variation coefficient 由 canonical root 的 zero-connected winding 精确为零。
定理明确列了转置步骤，也没有将整个 physical Poisson tensor 替换为 NLS tensor。

actual involution 和原 \(\Omega\) 连续给 ambient \(K_x\) isotropic；Hamilton identity 与 common trace/action differential kernel identity 给 \(K_x^{\perp_\Omega}=K_x\)。
同一 strong phase 内部共同微分核 \(\mathcal A_x=j^{-1}K_x\) 含全部 actual internal trace directions，故
\(\mathcal A_x^{\perp_\omega}=\mathcal A_x\)。这是真正 nonlinear 点态最大共同微分核，不是线性 Hessian pointer。

实际 fiber \(Y_x\) 的内部速度图像 \(V_x\) 被夹在 actual finite Hamilton span 与 \(K_x\) 之间，所以
\(\overline{V_x}=K_x\) 及 \(V_x^{\perp_\Omega}=K_x\)。
**未证明**未闭包 \(V_x=K_x\)、fiber inclusion tangent 单射或 regular fiber。phase \(j\) 已单射和 fiber map 的未知 ghost 是不同问题。定理将两者区分，且未称 \(Y_x\) 为已证 Lagrangian regular leaf，正确。

## 7. 外部分析假设及范围

定理借 KLTZ2009 Proposition 2.9 的 general-complex 近零 \(L^2\times L^2\) Cartesian analytic inverse、same low domain 的 weighted regularity 以及 auxiliary standard canonicity。物理 \(a,b\) 一般不在 focusing/defocusing real slice，正确使用 complex proposition。

必须共同保留：

* \(S\ne0\)、指定零组件均值物理叶；早期 explicit \(|\delta|<\pi/L\) 用于 actual Hessian/Fourier witnesses。
* 背景 \(\varphi^*=(iL\delta,iL\delta)\) 位于 KLTZ near-zero \(W\)，且进一步位于 action-factorization 的 zero-connected 目标球；这些未知数值半径不能由前一个 explicit bound 自动替代。
* 共同 low state 图、所有 contour 的 matching canonical branches、中央两 simple roots 和中央 \(I_0\ne0\) 的 angle/log branch；同一个 source/domain 缩小使这些同时成立。
* 只在该图内和实际 finite flow germs 的存在域工作；不宣称 global action-angle、uniform whole-phase Cauchy 流或全 \(M\) nonlinear inverse/closure。

一阶 smoothing 备用路线与 Yang–Yurko framed two-spectra injectivity 不承担本定理 weighted onto 逆或 closure 的必要依赖。有限机器 checks 只验证 exact field algebra，不代替 mild convergence、common-domain high inverse、compact contour/transpose 收敛或 Baire。

修后读回确认：背景导数已写为 \(\partial_{I_0}\widehat\chi(I^*)=4\)，finite-block 独立性也已明确限定在固定有限测试 plots 的共同局部 germ；所有列出的修正均已解决。修后还明确 physical reality 是经 nonlinear 图诱导的反全纯对合，不假定全局反线性；实 strong 图是复化 Banach holomorphic 图的实限制；\(C_n=n^{-1}\int\mathrm{res}\,\mathcal L^n\) 是实际 smooth 场上的有限 differential-polynomial 积分。这些措辞正确。

修后实际读取源 SHA256：FF7F48C84644A4DFBAE56CFD9752A239AA96AABD51407071C2D39629DEB00C1D。当前结论 PASS，完整条件陈述适合交付。原用户全 M 一般场完整 Liouville 目标仍未完成；当前已证 M2 的指定一般函数域 weak diffeological Hamilton 结构、actual finite flows、同图可数独立性和 nonlinear closed-kernel maximality。
