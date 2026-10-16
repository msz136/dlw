# M=2 actual mixed-low trace/action fields and bounded angular torques

2026-10-11. This note works on the actual mean-zero physical leaf with S=2δ≠0 and under the existing small-background/common-domain assumptions of [the reduced Cartesian state bridge, D6–D7](akns_physical_state_inverse_bridge_20261011.md). Its low source is **L²₀(u)×H¹₀(v)**. All source and coordinate maps below are holomorphic on the complexification; S is real when the original physical real structure is considered. No checks were run, and no shared log or index was edited.

The exact algebraic identities used here are the already audited (4), (6), and (7) of [the physical trace proof](m2_physical_trace_poisson_closure_proof_20261011.md). This note supplies their mixed-low analytic interpretation and an all-coordinate boundedness lemma for each fixed trace/action charge. Sections 1–6 passed the [independent low-field/torque audit](m2_actual_mixed_low_bounded_torques_independent_audit_20261011.md). The explicit real structure in §§7–8 uses the [independent primary-source involution proof](m2_kltz_physical_real_involution_independent_audit_20261011.md). It does not identify the reduced physical tensor with the standard NLS tensor.

## 1. Mixed-low coefficients and the actual adjoint

Put X₀=L²₀×H¹₀, with the product norm. For (u,v)∈X₀, define

\[
q=u-S,\quad V=-2uv/S,\quad A=1/4-v^2/S^2,
\quad r=A(S+u)-v_x/S.
\tag{1}
\]

Since H¹per↪L∞ and is a multiplication algebra, q,V,r belong to L² and A belongs to H¹. These maps are holomorphic X₀→L² or H¹ with bounds on every bounded X₀ set. For λ in a fixed compact subset of C, the trace-free split coefficient

\[
\mathcal A_\lambda=((\lambda-V)/2)\operatorname{diag}(1,-1)
+qE_{12}+rE_{21}
\tag{2}
\]

is bounded in L² on those sets.

The actual fundamental matrix solves X′=𝒜λX, X(0)=I. Its Volterra series converges in C⁰; the exponential bound depends on ‖𝒜λ‖L¹≤√L‖𝒜λ‖L². Then X′=𝒜λX∈L², so X∈H¹. The inverse matrix satisfies the corresponding inverse ODE and also belongs to H¹. The Volterra expansion and the identity X′=𝒜λX give holomorphic dependence into H¹, with bounds uniform over compact λ sets and bounded coefficient sets. This is an actual ODE statement, not a formal adjoint series.

Let N=X(L). The trace-gradient adjoint is XNX⁻¹ with its scalar part omitted:

\[
W=\begin{pmatrix}h&E\\F&-h\end{pmatrix}\in H^1,
\quad W'=\mathcal A_\lambda W-W\mathcal A_\lambda.
\tag{3}
\]

It is periodic, since W(L)=W(0). Consequently W:X₀→(H¹)³ is holomorphic and locally bounded, uniformly for λ in a compact set. Its three derivative identities are exactly those of the previously audited physical trace proof and hold as L² identities.

## 2. The fixed-original-λ trace field maps X₀ to X₀

For the ordinary ∫dx gradient convention, Juv=−offdiag(D)/16. The actual fixed-λ gradients and derivative-free field are

\[
g_u=F+AE+2vh/S,\qquad
g_v=(\lambda-2v)E/S+2h,
\tag{4}
\]

\[
u_t=-qF/8+A(S+u)E/8+(\lambda-2v)qh/(8S)
-(\lambda-2v)(\lambda-V)E/(16S),
\]
\[
v_t=(\lambda+2v)F/16-A(\lambda-2v)E/16-SA h/4.
\tag{5}
\]

Every uₜ term is an L² factor multiplied by H¹ factors (or is itself H¹), so uₜ∈L². Crucially, vₜ uses only v,A(v) and the H¹ entries of W: every factor is H¹. Hence vₜ∈H¹. The formulas are finite continuous multilinear/polynomial combinations of holomorphic maps and therefore establish

\[
\boxed{X_{F_\lambda}:X_0\supset\mathcal O\longrightarrow X_0
\text{ is holomorphic and locally bounded.}}
\tag{6}
\]

The means vanish. Indeed (4) belongs to H¹, and the weak adjoint identities give uₜ=−Dgᵥ/16, vₜ=−Dgᵤ/16 distributionally. Formula (5) improves the second derivative expression to H¹; it does not change its integral, which is zero. Thus (6) takes values in the specified mean-zero space.

The compact-λ bounds from §1 give one locally uniform X₀ bound on any fixed compact spectral parameter set. This is a genuine low order-zero statement for **mixed L²×H¹**, not for a balanced L²×L² source. The cancellation in vₜ is necessary; estimating Juv applied to a general low-gradient covector would not prove (6).

The fixed-ζ pullback contains an additional (∂λFλ)Xη. Here Xη=(uₓ,vₓ)/(8SL) does not in general map X₀ to X₀. Therefore the present lemma is for fixed original centered λ. It cannot be extended to fixed ζ by silently dropping the spectral-shift chain rule.

## 3. Each fixed actual action contour has the same mixed-low property

Fix an action index j and a fixed contour Γⱼ on a smaller common source neighborhood where its root R(z)=√(Δ(z)²−4) is single-valued and nonzero. Retain the already proved zero-winding branch condition. The actual action variation has the exact physical field identity

\[
X_{I_j}(x)=-\frac1\pi\oint_{\Gamma_j}
\frac{X_{F_{\eta(x)-2iz/L}}(x)}{R(z;x)}\,dz.
\tag{7}
\]

The dη term has vanished only because its contour coefficient is zero. Formula (7) is not obtained by treating η(x) as a fixed parameter in the original action Hamiltonian.

On a smaller low neighborhood, η is bounded and holomorphic, the varying parameters η−2iz/L remain in one compact set, and R⁻¹ is bounded and holomorphic along this fixed contour. Equation (6) therefore makes (7) a holomorphic X₀-valued Banach contour integral. It follows that each fixed actual XIj maps X₀ analytically to X₀. The bound may depend on the fixed charge j and its contour; no uniform estimate in the charge label is asserted. Finite constant combinations of trace/action fields inherit the result.

The actual commutation with every action extends to the low domain by continuity from smooth sources: dIk is a continuous low differential, each field above is a continuous low map, and smooth sources are dense in the open low domain. Thus all actions remain constant along each such low Banach flow.

## 4. The reduced actual fields have order zero on h⁰

Write R:𝒪red⊂X₀↔𝒰red⊂E₀ for the actual low reduced Cartesian state chart, where E₀=ℓ²(Z∖{0})×ℓ²(Z∖{0}) and Jₙ=wₙzₙ. Both R and its inverse are holomorphic. Their derivatives form holomorphic locally bounded operator families. For any one of the fixed fields H above, define

\[
\mathcal V_H(y)=DR_{R^{-1}y}X_H(R^{-1}y).
\tag{8}
\]

Equations (6)–(7) imply that 𝒱H is holomorphic 𝒰red→E₀. This is the desired **actual reduced h⁰→h⁰ order-zero field**. It does not follow from applying the full order-two physical pushed tensor to arbitrary h⁰ covectors.

The exact bridge gives pure-action torques. With Gₙ=(−wₙ,zₙ) on pair n, the fixed trace field is

\[
\mathcal V_{F_\lambda,n}=c_{\lambda,n}(J)G_n,
\qquad
c_{\lambda,n}(J)=L\omega_\lambda
\left(\partial_{I_n}t-\partial_{I_0}t\right)
\bigl(\lambda-\widetilde\eta(J),I(J)\bigr),
\tag{9}
\]

where ωλ=(S²−λ²)/(16S), I(J)=(ρ(J),J), Tζ=t(ζ,I), and η̃(J)=η̂(I(J)). The L factor corresponds to the x-normalized auxiliary field; the KLTZ field itself has the already specified i/L normalization. Equation (9) comes from the exact physical field projection, not from the reduced functional gradient. In particular ∂In t−∂I0 t is not replaced by ∂In t+ρₙ∂I0 t−tζ∂Jₙη̃.

Applying (7) after (8) proves that each fixed actual action field also has pure-action torques:

\[
\mathcal V_{I_j,n}=c_{j,n}(J)G_n,
\quad
c_{j,n}(J)=-\frac1\pi\oint_{\Gamma_j}
\frac{c_{\eta(J)-2iz/L,n}(J)}{R(z;I(J))}\,dz.
\tag{10}
\]

All factors here depend only on the common action sequence. Nothing is divided by Jₙ.

## 5. A uniform bound in the angular coordinate index

The following elementary lemma is useful independently of the explicit coefficients (9)–(10).

Suppose 𝒱 is a locally bounded map on a zero-neighborhood in E₀, and its pair components satisfy 𝒱ₙ=cₙ(J)(−wₙ,zₙ) with coefficients depending only on all the products J. Choose r>0 such that Bᵣ⊂domain and ‖𝒱(y)‖E₀≤M on Bᵣ. This is possible for the holomorphic fixed fields of §4 by continuity at the background y=0. Put δ=ε=r/4.

For any y∈Bδ and any n≠0, replace only pair n by

\[
w_n^{[n]}=\varepsilon,\qquad
z_n^{[n]}=J_n/\varepsilon,
\tag{11}
\]

and leave all other pairs unchanged. This preserves the **entire** action sequence J, including the filled central action ρ(J). Since |Jₙ|≤‖y‖E₀²/2≤δ²/2,

\[
\|y^{[n]}\|_{E_0}^2
\le\delta^2+\varepsilon^2+\frac{\delta^4}{4\varepsilon^2}
=\frac94\delta^2<r^2.
\tag{12}
\]

At this same-action state, the upper component of the field is −cₙ(J)ε. Hence

\[
\boxed{\sup_{n\ne0}|c_n(J)|\le M/\varepsilon,
\qquad y\in B_\delta.}
\tag{13}
\]

This test uses a fixed nonzero ε independent of n. It never divides by the small action or the small coordinate at the original state. It works even at Jₙ=0 when the torque coefficient is defined there. The bound is uniform in the coordinate index n for each fixed trace/action charge; its constant can depend on that charge, its contour, and the chosen low chart.

The bound also applies on a genuine small ℓ¹ action ball: for 2‖J‖ℓ¹<δ², choose a square root of each Jₙ and set wₙ=zₙ=√Jₙ. This balanced representative has ‖y‖E₀²=2‖J‖ℓ¹<δ². Only existence of these representatives is used; there is no claim that these square-root choices form a holomorphic inverse at closed gaps.

For a compact set of fixed λ parameters, §2 permits common r,M and therefore a locally uniform ℓ∞ bound over that compact set. Any fixed finite constant combination of trace/action charges has a bounded torque sequence as well. The finite-action field bound is not a claim that the whole matrix (cⱼ,ₙ) is uniformly bounded in both indices.

The existing ℓ¹-analytic full action factorization gives more regularity where it is defined: the derivative DI t is a holomorphic function with values in (ℓ¹)*=ℓ∞. The scalar central entry, the compositions with ρ and η̃, and the fixed-contour Banach integral preserve that holomorphy. Thus cλ and each fixed cⱼ are locally holomorphic ℓ¹-action functions into ℓ∞. This supplementary observation uses the already proved action-factorization domain; the direct same-action test above obtains the uniform bound from actual low fields without requiring a separate small-gap estimate.

## 6. Consequences for bounded relative angle profiles

At a fixed common action level J, (13) gives cH(J)∈ℓ∞. The actual low flow is consequently the explicit coordinate flow

\[
w_n(s)=e^{-s c_{H,n}(J)}w_n(0),\qquad
z_n(s)=e^{s c_{H,n}(J)}z_n(0),
\tag{14}
\]

for small s for which its image remains in the low chart. Boundedness of c makes this an analytic E₀ curve and preserves every Jₙ exactly. Differentiating (14) gives (8)–(10); low Banach uniqueness identifies it with the actual physical flow. On smooth data the same diagonal multiplier is bounded on every hᴺ, so the curve is smooth in the ordinary ambient C∞ topology.

For a regular sequence Jₙ≠0 and a chosen point (w*,z*) on its level, bounded relative logarithmic angles have the map

\[
\Theta(\alpha)_n=(e^{-\alpha_n}w_n^*,e^{\alpha_n}z_n^*),
\qquad \alpha\in\ell^\infty\text{ near }0.
\tag{15}
\]

Every fixed trace/action time translates α by s cH(J), hence lies in this bounded relative profile and gives genuine actual finite-charge time directions there. This proves neither that every common-level E∞ velocity has bounded relative coefficient nor that a local hierarchy Hamiltonian such as the original K has bounded angular frequency. η and higher local hierarchy fields can have derivative losses or growing frequencies; they require the separate strong-domain/hierarchy argument.

For an initial point in the already constructed strong phase domain, its previously audited finite trace/action strong flows agree with these low flows by uniqueness and therefore retain their proved strong-domain membership. This alone does not establish membership of every arbitrary Θ(α), α∈ℓ∞, in that strong domain; that is the separate admissibility step for a proposed regular-level profile.

The actual physical real slice is discussed separately below. One must not declare all complex profiles (15), or all ℓ∞ angle directions, real without proving its precise involution.

## 7. The actual spectral-normalized Cartesian real structure

For real S and physical real (u,v), the unbalanced a,b are real. Thus the KLTZ variables φ₁=−iLa/2 and φ₂=2iLb satisfy the anti-holomorphic involution

\[
\sigma_\varphi(\varphi_1,\varphi_2)
=(-\overline{\varphi_1},-\overline{\varphi_2}).
\tag{16}
\]

This is componentwise negative conjugation. It differs from the standard focusing involution (−barφ₂,−barφ₁). The existing D7 inverse always supplies the genuine reduced anti-holomorphic involution

\[
\sigma_{\rm red}=R\circ\operatorname{conj}_{u,v}\circ R^{-1};
\tag{17}
\]

its fixed set is exactly the original real physical image. We now identify it linearly for the **spectral-normalized KLTZ map actually defined by its Abel angles**, on a symmetric common near-zero domain containing the actual small background. An arbitrary action-dependent rephasing of a Birkhoff map is not being substituted.

The necessary primary-source symmetry is [Grébert–Kappeler 2002, Theorem 1.2 and Proposition 3.3(ii)](https://www.numdam.org/item/10.24033/bsmf.2432.pdf): in its defocusing potential notation, ψ↦barψ sends Iₙ to I₋ₙ and θₙ to −θ₋ₙ modulo 2π. This is matched to [KLTZ §§2.4–2.5](https://scispace.com/pdf/birkhoff-coordinates-for-the-focusing-nls-equation-3fe747h6fb.pdf), rather than treating the two papers' coordinate maps as unspecified interchangeable maps. The exact boundary/divisor matching is:

* T=[[1,i],[1,−i]]/√2 takes the real AKNS operator with the paper's auxiliary ψ=−qGK+ipGK to the KLTZ ZS operator, preserving Δ and its periodic roots.
* Its Z=0 Dirichlet boundary is exactly KLTZ's F₁=F₂ boundary. The Dirichlet roots agree, while M₁₂+M₂₁=Y₁−Z₂=−δGK flips the divisor sheet.
* The normalized Abel differentials have the same 2π periods and canonical sheet. Sheet involution fixes the same branch-point basepoints and reverses the differential, so the Abel angles differ by an overall sign modulo 2π. A fixed π Cartesian sign, if present, also preserves θ(Pφ)=−θ₋ₙ(φ). No action-dependent angle offset occurs. KLTZ (2.21) fixes the remaining Fourier sign.

Consequently the actual KLTZ map B satisfies BPφ=(x₋ₙ,−y₋ₙ). It holds first on the defocusing maximal totally real plane, extends through closed gaps by Cartesian continuity, and extends holomorphically to the common complex domain. KLTZ's focusing theorem gives BCf=(−barx,−bary), with Cfφ=(−barφ₂,−barφ₁), by the same analytic identity argument on its focusing maximal totally real plane. Because σφ=P Cf, these two actual identities yield

\[
B\sigma_\varphi=\kappa B,
\qquad
\kappa(w,z)_n=(-\overline{w_{-n}},-\overline{z_{-n}}),
\tag{18}
\]

Indeed σ sends (xₙ,yₙ) to (−barx₋ₙ,+bary₋ₙ), which gives (18) for w=(x+iy)/√2 and z=(x−iy)/√2. This is an exact equivariance identity, not a deduction from only the vacuum Fourier derivative. The full source/convention argument is recorded in the independent involution proof cited above.

The central action and gauge section preserve (18). Put (𝔯J)ₙ=barJ₋ₙ. The actual simple-root discs around ±iLδ are each invariant under z↦−barz, hence χ∘σ=barχ. The unique scalar IFT branch gives ρ(𝔯J)=barρ(J). The constant background φ*=(iLδ,iLδ) is KLTZ-even and focusing; its central y₀*=0 and x₀* is purely imaginary. Thus w₀*=z₀*≠0 and their ratio is 1. Take the zero logarithm branch near this ratio. Then

\[
\vartheta_0\circ\kappa=-\overline{\vartheta_0},\qquad
\vartheta_0=\frac1{2i}\log(w_0/z_0),
\tag{19}
\]

so the chosen central section ϑ₀=0 is invariant. The root s(I₀)²=I₀ with s(I₀*)=w₀* obeys s(barI₀)=−bar s(I₀) by branch uniqueness. Filling w₀=z₀=s(ρ(J)) therefore preserves κ exactly.

The constant gauge gτ(a,b)=(eτa,e⁻τb) acts as Gτ(w,z)=(e⁻τw,eτz), and κGτ=Gbarτκ. A real physical potential has ϑ₀ purely imaginary, so its adjustment to ϑ₀=0 uses τ=iϑ₀ real. Conversely κ-fixed filled data give real a,b after B⁻¹ and the fixed balancing inverse. The already proved full physical/gauge chart Ψ has real coefficients and a unique low inverse, so its inverse yields real u,v and a real gauge parameter. Removing that gauge gives the actual real physical potential.

It follows that one may choose the D7 common low chart, once and at every Sobolev restriction, so that

\[
\boxed{R(\bar u,\bar v)=\kappa_{\rm red}R(u,v),
\quad \kappa_{\rm red}(w,z)_n=(-\bar w_{-n},-\bar z_{-n}),\ n\ne0.}
\tag{20}
\]

The fixed set is precisely w₋ₙ=−barwₙ and z₋ₙ=−barzₙ. The two positive-index sequences remain independent; this is neither the standard focusing nor the standard defocusing Cartesian slice. It implies the actual action reality J₋ₙ=barJₙ but contains more state information than that action identity alone.

For comparison, if a different chart rephases wₙ to eᶠⁿ⁽ᴵ⁾wₙ and zₙ to e⁻ᶠⁿ⁽ᴵ⁾zₙ, its conjugated involution acquires the multiplier exp(fₙ(𝔯I)−barf₋ₙ(I)). It retains exactly the linear formula (18) if fₙ(𝔯I)=barf₋ₙ(I) on the chosen zero log branch (or the corresponding exponent equality). Without that normalization, the transported formula (17) remains valid while a linear index-reflection claim would require proof.

## 8. Real bounded angle profiles and actual real finite-charge flows

Fix a real regular state (w*,z*) with Jₙ≠0. On a uniformly small logarithmic branch, (15) is real if and only if

\[
\alpha_{-n}=\overline{\alpha_n},\qquad n\ne0.
\tag{21}
\]

Necessity follows from comparing e⁻α₋ₙw₋ₙ* with −overline(e⁻αₙwₙ*); the nonzero coordinates permit cancellation, and the uniform branch removes the 2πi ambiguity. Sufficiency follows directly for both w and z. Thus the real bounded profile has the explicit closed real model ℓ∞𝔯={α∈ℓ∞:α₋ₙ=barαₙ}, with an arbitrary complex angle at each positive index.

An actual real trace/action charge respects source conjugation, and its real-time low flow preserves the real physical source by uniqueness. From (20), its reduced torque at a real regular state must satisfy

\[
c_{H,-n}(J)=\overline{c_{H,n}(J)}.
\tag{22}
\]

Equations (13), (14), and (22) show that the genuine real finite-charge trajectory translates the real angle profile by s cH(J)∈ℓ∞𝔯. Real trace charges are holomorphic extensions (Fλ+Fbarλ)/2 and (Fλ−Fbarλ)/(2i); real action charges are (Ij+I₋ⱼ)/2 and (Ij−I₋ⱼ)/(2i), using the actual action reality. Any fixed finite combination retains the boundedness and reflection conditions.

If a separate argument supplies an actual real hierarchy field with an unbounded angular frequency sequence, the same exact real structure forces the reflection identity (22), without a boundedness conclusion. This identifies their real conjugation rule; their existence windows and strong-domain regularity remain the separate actual-flow theorem. This note does not turn all C∞ action levels into ordinary submanifolds and does not prove the original K flow or general-M Liouville completeness.

