# Root audit: genuine infinite frequency-weighted gap Hamiltonian flows

2026-10-11. Read `general_m_gap_frequency_weighted_hamilton_sequence_20261011.md` §§1–9 in full, then checked its corrected adjoint block names against the actual vector bridge: the top-right block is the row \(e\), the bottom-left block the column \(f\), and the auxiliary field is \((e,-f)\). The proof concerns the original weak form and one common balanced-low physical source domain; no scripts were rerun.

## Uniform reconstruction and the essential quadratic cancellation

The fixed-principal interaction representation gives uniform fundamental-matrix and inverse bounds in a vertical spectral strip, independently of the imaginary parameter. Normalized trace-power auxiliary fields are therefore uniformly bounded in the ambient \(L^2\) coefficient pair. The full physical graph has a fixed finite frame minor, whose inverse is locally bounded and independent of the spectral parameter. Composing that finite correction with the projected actual state-chart inverse gives one bounded analytic reconstruction operator \(\mathscr B_x\). It need not send an arbitrary ambient tangent to a physical Hamiltonian field; the exact actual trace identity is the justification for its use here.

On each selected fixed spectral contour, cluster separation, normalized scalar phases, characteristic denominators and the Newton chain coefficients have common bounds. The center-minus-parameter factor is bounded, so these coefficients contain no hidden factor of \(n\).

The actual rank-two function has the same free template \(\operatorname{diag}(e^{L\zeta},1)\), plus the previously proved strongly analytic correction sequence \(Q\in\ell^2(\mathcal A_r)\). Its gap contour functional has derivative zero at the free template: the linear discriminant term is \(2(e^{L\zeta}-1)(Q_{11}-Q_{22})\), and the extra root-moment factor cancels its possible pole. Hence \(\|D\mathcal G(Q)\|\le C\|Q\|\). With the full \(H\) held fixed only during this auxiliary differentiation, the actual ODE/Riesz derivative into \(\mathcal A_r\) is uniformly bounded. This proves \(\|Y_{g_\alpha}\|\le C\|Q_\alpha\|\). The original field still includes the full graph/frame correction; \(H\) was not frozen in the physical dynamics.

## Exact original weight and sequence analyticity

Use the fixed exact background collision \(\lambda^\alpha\), with \(\omega_\alpha=(S^2-(\lambda^\alpha)^2)/(16S)\ne0\). On its fixed-radius contour,

\[
\frac{\omega(\lambda)}{\omega_\alpha}-1
=-\frac{(\lambda-\lambda^\alpha)(2\lambda^\alpha+\lambda-\lambda^\alpha)}{S^2-(\lambda^\alpha)^2}
=O(1/|n|).
\]

The exact trace contour identity and the same \(\lambda\)-independent reconstruction operator give

\[
\left\|\frac{X_{g_\alpha}}{\omega_\alpha}\right\|_{X_0}
\le C\bigl(\|Q_\alpha\|_{\mathcal A_r}+1/|n|\bigr).
\]

Thus the entire normalized field sequence is locally bounded in \(\ell^2(X_0)\). Coordinate holomorphy and locally uniform dual-tail approximation yield weak, then strong Banach holomorphy. The two separate reconstructed terms need not individually be Hamiltonian; their sum is exactly the original \(X_g/\omega_\alpha\).

## Infinite profiles are actual Hamiltonians and actual flows

For a profile \(\theta\in\ell^2\), distinct from the original mean label \(c\), \(\mathcal H_\theta=\sum\theta_\alpha g_\alpha/\omega_\alpha\) is scalar analytic, and \(X_\theta=\sum\theta_\alpha X_{g_\alpha}/\omega_\alpha\) converges absolutely in \(X_0\) by Cauchy–Schwarz, locally uniformly on a smaller complex source ball. Its source derivatives converge by Cauchy estimates. Finite truncations satisfy the original Hamilton identity, and continuity of the original weak form gives

\[
d\mathcal H_\theta[Y]=\Omega(X_\theta,Y),\qquad Y\in X_0.
\]

The unique mean-zero ordinary gradient representative is \(-16(D^{-1}(X_\theta)_d,D^{-1}(X_\theta)_q)\in H^2\times H^1\); applying the original \(J\) gives \(X_\theta\). This supplies the original Hamilton identity without an unproved infinite raw-adjoint estimate or a replacement symplectic structure.

Reflected conjugate coefficients give real Hamiltonians. Analytic Banach ODE theory provides genuine local flows, uniformly for bounded \(\ell^2\) profile sets. Translation equivariance gives all smooth orders in the same low time window. Uniform analytic convergence of the finite-profile flows and their source derivatives, composed with the smooth translation orbit, gives convergence in every fixed Sobolev order; actual trace and every defined \(C_j\) are therefore conserved. The original weak Hamilton identities and constant closed weak form transfer finite commutation to these infinite profiles.

**PASS:** genuine infinite \(\ell^2\) frequency-weighted gap Hamiltonians and their original balanced-low flows are established for general fixed finite \(M\). Bounded profiles also work after the explicitly additional factor \((1+|n|)^{-1}\). This proves neither all \(\ell^\infty\) profiles with only \(\omega^{-1}\), old strong-domain internal plots, nonlinear canonical norming, invariant action inverses, regular common fibers nor Hamiltonian maximality. The all-M Liouville goal remains open.
