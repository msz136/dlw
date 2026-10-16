# Exact complex periods of the general-M reciprocal spectral flows

2026-10-13, continuation. The preceding goal turn made progress: it constructed reciprocal Floquet Hamiltonians and recorded their common-domain fields. This continuation derives their complete Cauchy gauge generator, proves the return map at complex time 2πi using the ORIGINAL physical slice, and constructs exact nonlinear eigen-coordinates for every fixed finite block. It does not claim an infinite simultaneous chart.

All statements inherit the actual common low source domain and the original field bridge listed in [RECIPROCAL_PERIODS.md](RECIPROCAL_PERIODS.md). The proofs here are analytic arguments, not conclusions inferred from symbolic tests. They have been checked within this branch but not by an independent reviewer.

## 1. Conventions and the exact projector adjoint

Let s∈S¹_L denote the spatial variable; x denotes the complete source state. The normalized vector connection is

\[
 \bar A_\lambda=\lambda J_*+Q(x;s),\qquad
 J_*=\operatorname{diag}(1,0_m)-I_M/M,
\]

with complete slow matrix H(x) independent of s. Its actual normalized monodromy is Nλ and initial fundamental solution is Yλ(s). Fix a high collision label α and two nested λ contours enclosing only that rank-two branch cluster. Their intervening annulus is free of multiplier collisions. Let Pα±(λ) be the two labeled eigenprojectors there. Define

\[
 W_\alpha(\lambda;s)
 =\frac12Y_\lambda(s)(P_\alpha^+(\lambda)-P_\alpha^-(\lambda))Y_\lambda(s)^{-1}.
 \tag{1}
\]

W is trace-free, periodic in s, and W_s=[Aλ,W]. The two-sheet projectors may be branched inside the contours, whereas their sum Πα=Pα++Pα− is holomorphic on the entire cluster disk by the original separated Riesz projection.

For κ=½log(μ+/μ−), actual Duhamel variation gives

\[
 d\kappa_\alpha[\delta\bar A]
 =\int_0^L\operatorname{tr}(W_\alpha\delta\bar A)ds.
 \tag{2}
\]

Indeed dlog μ±=tr(P±N⁻¹δN); substitute δN=N∫Y⁻¹δA Y. This calculation includes arbitrary source dependence of the actual connection. A scalar trace normalization contributes zero to (2). Expressing κ as a local function of the full characteristic classes identifies the trace-free part of the corresponding sum of trace-power adjoints with precisely W, not merely with its value at the background.

## 2. Exact Cauchy generator; the finite correction is retained

For the reciprocal Hamiltonian

\[
 \mathcal A_\alpha=\frac1{2\pi i}\oint
 \frac{\kappa_\alpha(\mu)}{\omega(\mu)}d\mu,
 \qquad\omega(\mu)=\frac{S^2-\mu^2}{16S},
\]

the original rational gauge identity and its moving-frame correction yield

\[
 \delta_{X_{\mathcal A_\alpha}}\bar A_\lambda
 =(G_\alpha)_s-[\bar A_\lambda,G_\alpha],
\]

\[
 \boxed{G_\alpha(\lambda;s)
 =\frac1{2\pi i}\oint\frac{W_\alpha(\mu;s)}{\mu-\lambda}d\mu
 +K_\alpha.}
 \tag{3}
\]

Kα is trace-free, block diagonal relative to J*, and independent of s and λ. It is the ORIGINAL physical finite-frame correction, not a discarded gauge. To see its constancy, first integrate the exact corrected trace generator; its λ-independent remainder is block diagonal. The top diagonal equation and periodicity give δtrH=0 and a constant top scalar. The slow block equation and the common nonalias condition force all nonzero Fourier modes of the slow block to vanish, exactly as in the established trace/vector bridge.

Equivalently Kα is the finite graph correction associated with the auxiliary unweighted period field. The old invertible graph minor determines it uniquely and analytically. At the uniform source it is zero: the unweighted period's first variation is zero even for arbitrary auxiliary coefficient variations (in the analytic background generator eigenbasis their diagonal first variations extend through the collision), so its auxiliary field and hence its finite graph correction vanish.

Equation (3) gives the actual framed monodromy variation

\[
 \dot N_\lambda=[G_\alpha(\lambda;0),N_\lambda].
 \tag{4}
\]

It also gives δH=[Kα,slow,H], so every eigenvalue of the complete H is constant along this flow. Absolute spectral centers are constant by (4); therefore the moving-grid centers cβ=aβ−K_n−hℓ(H) are also constant along this flow. A center-motion term must not be inserted in the norming derivative along these particular Hamiltonian flows. Frame-motion terms do remain.

## 3. The spectral jump is an exact half-projector

Let G_in use the outer contour and G_out the inner contour. G_in is holomorphic inside its contour, G_out outside its contour including infinity, and both generate the same physical connection variation. The integral defining K is unchanged under this contour deformation. On their common annulus the Cauchy formula gives

\[
 \boxed{G_{\rm in}-G_{\rm out}=W_\alpha.}
 \tag{5}
\]

This is an identity at every source in the common domain, not a Taylor expansion. Their difference is an adjoint homogeneous solution, consistent with the same δA.

Let x(t) be the actual complex Hamiltonian orbit. At fixed λ in this annulus, solve the time parallel-transport equations

\[
 \partial_t T_{\rm in/out}(t,\lambda;s)
 =G_{\rm in/out}(x(t),\lambda;s)T_{\rm in/out}(t,\lambda;s),
 \quad T_{\rm in/out}(0)=I.
 \tag{6}
\]

The connection identity gives the intertwining relation for spatial connections and the actual monodromy conjugacy. Consequently its spectral projectors, and the periodic adjoint (1), are transported by T_out:

\[
 W_\alpha(t)=T_{\rm out}(t)W_\alpha(0)T_{\rm out}(t)^{-1}.
\]

Differentiate T_out⁻¹T_in using (5). Its coefficient becomes the time-independent Wα(0), proving

\[
 \boxed{T_{\rm in}(t)=T_{\rm out}(t)\exp(tW_\alpha(0)).}
 \tag{7}
\]

On the two selected eigenlines the transition factors are e^{t/2} and e^{−t/2}; on the complementary spectral subspace the factor is 1. This explicitly describes the eigenline gluing, including the full matrix transport.

## 4. Complex time 2πi gives the identity PHYSICAL return map

The apparent sign at t*=2πi is essential:

\[
 \exp(2\pi i W_\alpha(0))=I-2\Pi_\alpha(\lambda;s),
 \quad \Pi_\alpha^2=\Pi_\alpha.
 \tag{8}
\]

The right side extends holomorphically to the entire disk, including the two branch points, because it uses the full rank-two projector. It is invertible, with its square equal to I. It need not be I, so it would be wrong simply to declare T_in=T_out at this time.

Instead put D(λ;s)=I−2Πα(λ;s) at the INITIAL source. Equation (7) lets us glue

\[
 U(\lambda;s)=
 \begin{cases}
 T_{\rm in}(t_*,\lambda;s)D(\lambda;s)^{-1},&\text{inside},\\
 T_{\rm out}(t_*,\lambda;s),&\text{outside}.
 \end{cases}
 \tag{9}
\]

This is an entire invertible matrix in λ. As λ→∞, G_out=Kα+O(λ⁻¹), so T_out tends to U∞(t*), where

\[
 \dot U_\infty=K_\alpha(x(t))U_\infty,\qquad U_\infty(0)=I.
 \tag{10}
\]

Kα is spatially constant and block diagonal; U∞ has the same properties. The Cauchy integral is O(λ⁻¹) uniformly along the finite time path, so the limit and boundedness needed here follow from the time integral equation. Matrix-entry Liouville then gives U(λ;s)=U∞(t*), independent of both λ and s.

On the exterior patch (6) intertwines the original and final spatial connections. Hence

\[
 \bar A_{\lambda}(x(t_*))
 =U_\infty(t_*)\bar A_\lambda(x(0))U_\infty(t_*)^{-1}.
 \tag{11}
\]

This identity extends to all λ since both connections are affine in λ. Write U∞=diag(u₀,U_s) and Q_f=u₀U_s⁻¹. Then (11) is exactly the finite constant-frame action

\[
 (a,b,H)\mapsto(aQ_f,Q_f^{-1}b,Q_f^{-1}HQ_f).
\]

Both sources belong to the ORIGINAL physical coefficient graph. Its previously established transverse local slice intersects each nearby constant-frame orbit once. Provided Q_f is in this slice neighborhood, (11) therefore forces x(t*)=x(0).

### 4.1 Existence for the whole loop and a uniform single-index radius

No unrestricted complex-time continuation is assumed. From the preceding common-domain ℓ²(E) field theorem, all X_Aα are uniformly analytic on one source ball and vanish at 0. The same finite-graph estimates give uniform analytic Kα with Kα(0)=0. Shrink to a common ball with

\[
 \|X_{A_\alpha}(x)\|_E+\|K_\alpha(x)\|\le C\|x\|_E
\]

for every high α. Along t=iτ, 0≤τ≤2π, Gronwall yields ||x(iτ)||≤e^{Cτ}||x(0)||. Choose one initial radius so this path stays in the common spectral/slice ball, and shrink it further so ∫||Kα|| |dt| makes U∞(t*) close enough to I. Analytic Banach ODE provides the full path for every α on this SAME initial ball. The same reasoning permits a small complex neighborhood of the path.

**Theorem.** On that common ball, every actual reciprocal spectral Hamiltonian has the exact complex return identity

\[
 \boxed{\phi_{\mathcal A_\alpha}^{\,2\pi i}(x)=x.}
 \tag{12}
\]

The proof first applies to smooth sources, where all connection identities are classical. Same-window smooth persistence, density in E and continuous dependence of the low analytic flow extend (12) to the whole ball. No invariant spectral state inverse is used in this return-map proof; the finite PHYSICAL frame slice is sufficient.

## 5. Exact finite nonlinear spectral eigen-coordinates

For a fixed finite set F of complex labels, the commuting flows (12) give a holomorphic action of the real compact torus (iR/2πiZ)^F on a sufficiently small invariant neighborhood of 0. For fixed |F|, existence of all successive loop pieces and their small extensions follows from the same bounds with the finite sum of lengths. The neighborhood may shrink with F; no uniform exhaustion is claimed.

Use the holomorphic complexification of the old genuine real-analytic augmented norming state inverse to identify a source neighborhood with a Hilbert data neighborhood and write this finite torus action as Φ_F(θ). Positive coordinates and their real conjugates are independent variables in this complexification; no physical reality constraint is imposed on a single complex Hamiltonian orbit. Its derivative at 0 is the exact diagonal representation L_F(θ): on each selected pair it multiplies the linear norming components by e^{iθ_α} and e^{−iθ_α}, and is the identity on all other high coordinates and finite low supplements. This is the established unit quadratic torque, now combined with an ACTUAL periodic group.

Define the Bochner-averaged map in these state data by

\[
 \Psi_F(z)=\int_{\mathbb T^F}L_F(\theta)^{-1}\Phi_F(\theta,z)d\theta,
 \tag{13}
\]

with normalized Haar measure. Analyticity on a common smaller source neighborhood follows from finite compact parameter integration of uniformly bounded holomorphic maps. DΨ_F(0)=I. The Banach inverse function theorem gives a genuine local analytic state chart. Haar invariance gives

\[
 \Psi_F(\Phi_F(\varphi,z))=L_F(\varphi)\Psi_F(z).
 \tag{14}
\]

Let Zα± be the corresponding selected coordinate functions. Differentiating (14) and complexifying the time direction proves the EXACT nonlinear relations

\[
 \boxed{\{Z_\beta^\pm,\mathcal A_\alpha\}
 =\pm\delta_{\alpha\beta}Z_\beta^\pm,\qquad \alpha,\beta\in F.}
 \tag{15}
\]

All residual coordinates in this chart are invariant under these selected fields. At points with both selected Zα± nonzero, any local logarithm branch gives

\[
 \Theta_\alpha=\tfrac12\log(Z_\alpha^+/Z_\alpha^-),
 \qquad\{\Theta_\beta,\mathcal A_\alpha\}=\delta_{\alpha\beta}.
 \tag{16}
\]

This is a nonlinear all-neighborhood conjugacy, not a background bracket. The chart is not asserted to be symplectic simply because it is equivariant. In particular {Θα,Θβ}=0 has not been obtained from averaging; for a finite block the earlier original-form Darboux–Carathéodory construction supplies a further canonical normalization. For an infinite block such normalization and the state inverse are still open.

### 5.1 Reality and compact versus hyperbolic directions

At real physical sources Aα*=overline(Aα). For a positive independent label, the real Hamiltonian i(Aα−Aα*)=−2 Im Aα generates the combination of times it and −it on the reflected pair; it has real period 2π wherever the joint loop is defined. The real Hamiltonian Aα+Aα*=2 Re Aα is the complementary real scaling direction and is not claimed periodic. Reflection-symmetric finite Haar averaging preserves the induced real structure. Thus these local real variables contain both circular and hyperbolic directions; no compact real Liouville torus for the original DLW time is inferred.

## 6. Why this does not yet solve the infinite problem

The single-index return radius is uniform, but a finite simultaneous action is so far controlled by the number of selected labels. Equation (13) therefore does not yet converge to a full infinite-torus average on one common general-field neighborhood. Nor does it preserve every A without proving uniform operator bounds and a nonlinear weak symplectic normalization.

The next required estimate is a bound for simultaneous finite imaginary-time profiles that depends on ||θ||ℓ∞, not on ||θ||ℓ² or |F|. The exact Cauchy jump representation (7) provides a concrete route through uniformly bounded Cauchy operators on the separated spectral circles; this requires a genuine matrix factorization and source reconstruction estimate, including the complete finite frame. It is a new task, not an available consequence of the individual period theorem.

Full action completeness, invariant low data, a single infinite state chart, and original-time action-only H remain unproved. The active goal is unchanged.

Latest continuation: the common all-label physical flow bound is now proved in [BOUNDED_PROFILE_PHYSICAL_FLOWS.md](BOUNDED_PROFILE_PHYSICAL_FLOWS.md), without RH inverse reconstruction. [INFINITE_TORUS_STATE_CHART.md](INFINITE_TORUS_STATE_CHART.md) extends the finite averaging argument to a common countable torus and a genuine analytic state inverse. The outstanding requirements are now the full weak symplectic/action normalization, low invariant completion, and original-time action-only H, not the common infinite state chart itself.
