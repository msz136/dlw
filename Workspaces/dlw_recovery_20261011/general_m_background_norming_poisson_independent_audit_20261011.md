# 一般 M actual background norming Poisson pairing：独立审查

2026-10-11。完整逐式读 [正式 Poisson recovery proof](general_m_background_norming_original_poisson_pairing_recovery_proof_20261011.md) §§1–6、(1)–(17)，包括最终新增的real Re/Im gap fields。只写独有audit；未改主稿或共享logs，未运行 checks。

读取正式稿 SHA256：

`D833ABE8DF63DB2BD1A9DFC8ADAEB0C097C5204C1ABB3597B14516E0A7E16DF1`。

审结：**PASS**。以下核清 arbitraryperiodicadjoint 的实际原物理covector、有限frame correction、cross-channel orthogonality、全部bracket signs与n² obstruction。

## 1. Actual Born covectors与原J的合法收缩

原 convention为 {F,G}=dF(JdG)=X_G F。背景collision label i=(ℓ,n)对应 exact μ_i、y_f−y_ℓ=iκ_n。Actual dual normalization给
\[
C_i^+=e_{\ell i}\ell_{fi},\quad
C_i^-=e_{fi}\ell_{\ell i},\qquad
W_i^+=e^{-i\kappa_nx}C_i^+,\quad
W_i^-=e^{i\kappa_nx}C_i^-.
\]
Crossed dualpairings为零，故tr C_i^±=0；其phase直接给 W'=[A_0(μ_i),W]。Trace normalization的scalar项不影响该equation。

实际线性Borncovectors是 Γ_i^±=(1/L)∫tr(W_i^± δA)。Originalsourceframe中 δL转为 δA+U'−[A,U] 加一个scalar variation。Scalar与tracefree W配对为零；其余frame项满足
\[
\int_0^L\operatorname{tr}\{W(U'-[A,U])\}dx=0
\]
由periodic integrationby parts和adjoint equation直接推出。故Γ确为originalaffineconnection的真实linear covector，不能将此步替换成抽象auxiliarycanonical pairing。

原R-tensor gauge derivation只使用periodic W'=[L_μ,W]，并未使用W为tracepower。因而对每个W_i^±仍合法；(1/L)covector normalization给gauge residue −(ω_i/L)W_i^±，其中 ω_i=(S²−μ_i²)/(16S)。Moving-frame derivation给
\[
\delta A_{X_{\Gamma_i^\pm}}
=\frac{\omega_i}{L}[E_{00},W_i^\pm]+
(a_0X,-Xb_0,[H_0,X]).
\]
Originalgradient和原J-field只有一个非零Fouriermode；实际D\Pi_0是Fouriermultiplier，且DH_0=0。因此actualcoefficientvariation与第一项均无means/Hvariation，余constantorbit必须满足a_0X=0、Xb_0=0、[H_0,X]=0。Uniformsimple H_0和observability迫使X=0。正式稿(5)的actualfield式准确。

## 2. Pencilorthogonality、同collision与准确normalization

对C_i=e_{pi}ℓ_{qi}、d_i=y_{pi}−y_{qi}，原bracket收缩是
\[
\{\Gamma_i,\Gamma_j\}
=\frac{\omega_j}{L^2}\int_0^L
e^{(d_i+d_j)x}\operatorname{tr}\{C_i[E_{00},C_j]\}dx.
\]
Fourierintegration使它在d_i+d_j≠0时为零。μ_i≠μ_j时，准确affinepencil关系
\[
(y_{qi}-y_{pj})\ell_{qi}e_{pj}
=(\mu_i-\mu_j)\ell_{qi}E_{00}e_{pj}
\]
使用两次给
\[
\operatorname{tr}\{C_i[E_{00},C_j]\}
=-\frac{d_i+d_j}{\mu_i-\mu_j}
(\ell_{qi}e_{pj})(\ell_{qj}e_{pi}).
\]
符号为负；Fourierphases可能配对时它也为零，准确排除不同highlabels，包括reflectedopposite-frequency的same-signpairing。

同collision的oppositesigns给
\[
\operatorname{tr}\{C_i^+[E_{00},C_i^-]\}
=\ell_{fi}E_{00}e_{fi}-\ell_{\ell i}E_{00}e_{\ell i}
=\gamma_i.
\]
Spatialintegral提供L，因此
\[
\{\Gamma_i^+,\Gamma_j^-\}_0
=\delta_{ij}\omega_i\gamma_i/L,
\qquad\{\Gamma^+,\Gamma^+\}_0=
\{\Gamma^-,\Gamma^-\}_0=0.
\]
ActualDν(0)=LΓ再给
\[
\{\nu_i^+,\nu_j^-\}_0
=\delta_{ij}L\omega_i\gamma_i.
\]
没有遗漏L、r、归一化monodromy或额外scalar因子；本处Γ是已校准norming的一阶covector，不是unnormalizedtracepower。

## 3. Realpositivechart与弱Poisson量级

Realreflection为R(ℓ,n)=(M−ℓ,−n)。对n>0设α_i=ν_i^+、β_i=barν_i^-。Atbackground
\[
\{\alpha_i,\bar\beta_j\}_0=\delta_{ij}C_i,
\quad C_i=L\omega_i\gamma_i\in\mathbb R\setminus\{0\},
\]
\[
\{\alpha_i,\beta_j\}_0=
\{\alpha_i,\bar\alpha_j\}_0=
\{\beta_i,\bar\beta_j\}_0=0.
\]
C_i实性来自μ_i纯虚、ω_i实以及actualχ anti-Hermitianbackground的Hermitianprojector parameterderivative。γ_i=1+O(n^{-2})>0，故|C_i|\asymp n²，在有限channels中一致；C_i的符号取决于S。

写α=x+iy、β=u+iv，准确实brackets为
\[
\{x_i,u_j\}_0=\{y_i,v_j\}_0=\delta_{ij}C_i/2,
\qquad\{x_i,v_j\}_0=\{y_i,u_j\}_0=0.
\]
因此它是nondegeneratebackground pairing，但不是整个ℓ²dual上有界的canonicalPoissontensor。正式稿保持弱形式的正确范围。

## 4. Gaplinearization的complex/real符号

Actualquadraticgap为
\[
g_i^{[2]}=-\frac4{L^2\gamma_i^2}\nu_i^+\nu_i^-
=-\frac4{L^2\gamma_i^2}\alpha_i\bar\beta_i.
\]
dg_i(0)=0，所以线性化不含Poissontensor的一阶变化。在{F,H}=X_H F convention下，complexgap场给
\[
\dot\nu_i^+=-\frac{4\omega_i}{L\gamma_i}\nu_i^+,
\qquad
\dot\nu_i^-=\frac{4\omega_i}{L\gamma_i}\nu_i^-.
\]
这里是complexHamiltonian的linearization；不能对complexfield径直将ν_i^-的evolution取conjugate，作为realpositiveβ的evolution。

正式稿新增realcharges正确处理这一点：
\[
X_{\operatorname{Re}g_i}:\quad
\dot\alpha_i=-\frac{2\omega_i}{L\gamma_i}\alpha_i,
\quad\dot\beta_i=\frac{2\omega_i}{L\gamma_i}\beta_i;
\]
\[
X_{\operatorname{Im}g_i}:\quad
\dot\alpha_i=\frac{2i\omega_i}{L\gamma_i}\alpha_i,
\quad\dot\beta_i=\frac{2i\omega_i}{L\gamma_i}\beta_i.
\]
它们分别是realdilation和realrotationblocks，均有n²operatornorm。其他highlabels的linearterms由pencilorthogonality为零；finitelowFouriercoordinates由非零highFouriersupport为零。

## 5. Uniformboundsobstruction与scope

已完整读新增依赖 [fixed-gap balanced Hamilton flow theorem](general_m_fixed_gap_balanced_hamilton_flow_20261011.md) §§1–4。它在固定轮廓上把actuala/g differential写成1≤r≤M−1的实际trace differential的scalarcontour组合，利用已审trace/vectorbridge §5.1的X_0值场作Bochnerintegral，再在L²×L²中以density识别actualoriginalJgradient。该定理确实构造每个固定gap的analyticX_0值场，并没有假定所有gap的uniformbounds。

Augmentedstatechart的DΨ_0及inverse有界，故上述真实finiteFourierlinearizeddirections在balancedsource中的operatornorm也至少为常数乘n²。这里相应gapfields已经由该fixed-gap定理定义，不再需要条件式。因此它们不可能具有uniformC¹或uniformlocalLipschitz预算。

若一族complexholomorphicfields在同一个complexlowball中统一C⁰有界，BanachCauchyestimate会给uniformderivativebound，从而同样被上述n²预算排除。Bareuniformreal-domainC⁰界加realanalyticity并不推出uniformderivativebound；正式稿明确没有作这一不成立推论。

除以fixednonzero背景ω_i可消除本次linearization的n²growth；这只证明backgroundrates有界，未证明uniformnonlinearfield、共同flowwindow、nonlinearDarbouxchart或squared-eigenfunctioncompleteness。

正式稿最终只增加上述fixed-gap依赖并移除“whenever represented”条件式；已读回该新增句及所引定理全文，数学结论保持准确。读取finalhash为本文件开头的D833ABE8…16DF1。

**最终PASS，无剩余修正。** 本证明是actualbackgroundoriginalPoisson入口和exactfrequencybudget，未越界为一般M的action/divisorcanonicalcoordinates或Liouvilletheorem。
