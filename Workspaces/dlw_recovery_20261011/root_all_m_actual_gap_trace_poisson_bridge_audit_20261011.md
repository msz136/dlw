# Root audit: actual gap functionals and the original Poisson structure

2026-10-11. Read `general_m_actual_gap_trace_poisson_bridge_20261011.md` §§1–5 and its independent short audit in full, against the already audited all-M actual trace tensor and quasimomentum bridge. No scripts were rerun. This audit concerns fixed finite collections of actual spectral windows.

## Actual cluster variation, including its projector

For the original normalized monodromy \(N_\lambda\in SL_M\), Newton identities express every characteristic coefficient through \(F_r=\operatorname{tr}N_\lambda^r/r\), \(1\le r\le M-1\), and the fixed determinant. A fixed multiplier contour selecting the actual rank-two cluster gives

\[
T_k=\frac1{2\pi i}\oint\mu^k\frac{p_\mu}{p}\,d\mu,
\qquad D=2T_2-T_1^2.
\]

Differentiation of this characteristic formula includes the full variation of the Riesz projector. The resulting exact differential is \(dD=\sum_r d_r\,dF_r\), with spatially constant scalar coefficients. The two eigenvalues within the cluster may collide; no simple-eigenvalue division occurs.

With a fixed spectral contour surrounding the two actual collision roots, define the absolute center \(a=s_1/2\) and half-gap square \(g=s_2/2-a^2\). Spectral contour integration by parts gives exactly

\[
da=-\frac1{4\pi i}\oint\frac{dD}{D}\,d\lambda,
\qquad dg=\frac1{2\pi i}\oint(a-\lambda)\frac{dD}{D}\,d\lambda.
\]

The moving coefficient holonomy shifts the relative center but leaves this gap unchanged. Multiplication of the discriminant by a nonvanishing analytic scalar has zero logarithmic-derivative root residue, so the normalized and raw definitions have the same actual roots. Using normalized characteristic data avoids accidentally introducing a separate raw determinant translation field.

## Original bracket and real components

Substituting the exact differential into the original free-field gradient expresses \(\nabla g\) and \(\nabla a\) as compact scalar-weighted contour integrals of the actual trace gradients. The weights depend on the source, but they are independent of spatial \(x\); the original \(J=-\operatorname{offdiag}(D)/16\) differentiates no such weight. A Poisson bracket uses these first differentials, so no second derivative of a contour weight belongs in the bracket.

The audited identities \(\{F_r(\lambda),F_t(\mu)\}_J=0\) and \(\{F_r(\lambda),C_j\}_J=0\) therefore imply actual gap/center mutual involution and their involution with every defined original centered \(C_j\). The latter retains the bridge's common regularity domain; it does not define arbitrary high jets on a rough source.

Complex conjugation of a real source sends the actual windows to their reflected negative labels. Applying the same trace identity to both sets proves the mixed conjugate brackets vanish. Thus every real and imaginary gap component is in involution; positive-frequency gaps are not incorrectly declared real-valued.

## Genuine fixed-collection fields and the unresolved infinite sum

On original isotropic \(H^s\) sources, \(s\ge1\), the affine connection's periodic adjoint satisfies \(W'=[A,W]\). Its Duhamel gradients gain one derivative. Fixed compact spectral contours preserve these locally analytic \(H^{s+1}\) bounds, so applying the original first-order \(J\) gives actual analytic \(H^s\to H^s\) Hamiltonian fields and local Banach flows. Mean preservation, translation equivariance, and the fixed-collection commutator identities are retained. Smooth persistence in the same \(H^1\) time window follows by differentiating the analytic flow along the translation orbit.

**PASS:** fixed finite actual gap/center families are original Hamiltonians in involution, with genuine same-order flows. Their regularity and independence can be used together on their explicit common domains. The strong coherent-domain transport still requires its actual mixed reparameterization. Strong \(g\in\ell^1\) analyticity alone supplies no uniform high-frequency field bound or convergence of \(\sum d_\alpha X_{g_\alpha}\); it does not prove an infinite Hamiltonian closure or all-M Liouville completeness. A possible balanced-low extension must use the separately proved actual trace/vector field bridge, rather than infer it from the isotropic Sobolev estimate.

## The balanced-low extension is now separately proved

Read `general_m_fixed_gap_balanced_hamilton_flow_20261011.md` §§1–4 in full. **PASS.** On the actual trace/vector graph neighborhood, each normalized trace field is jointly analytic into \(X_0=(L^2_0)^m\times(H^1_0)^m\), locally uniformly on the fixed compact contour. Its scalar-weighted Bochner integral therefore belongs analytically to the same \(X_0\).

Independently, the original affine Duhamel gradients are \(H^1\), and the original \(J\)-gradient belongs to the larger \((L^2_0)^{2m}\). It agrees with the Bochner field on dense smooth sources, hence agrees everywhere by continuity. Thus the extra \(H^1\) regularity of the second velocity is proved, rather than assumed. The original continuous weak form gives \(\Omega(X_g,Y)=dg[Y]\) for all rough \(Y\in X_0\). True balanced-low Banach flows, finite commutation and actual trace preservation follow. Analyticity and translation equivariance give smooth persistence in the same low time window and conservation of every defined \(C_j\) on those smooth trajectories. No uniform-in-frequency or old strong-domain internal-plot claim has been added.
