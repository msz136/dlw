# Root audit: all-M actual high-frequency Riesz/gap lemma

2026-10-11. The main `general_m_actual_high_frequency_riesz_gap_lemma_20261011.md` §§1–7 was read in full, including the corrected physical-background cancellation and norming multiplier factor. The complete `general_m_even_volterra_and_gap_sequence_independent_audit_20261011.md` was also read. The actual uniform dispersion was independently checked in `root_all_m_uniform_actual_resonance_audit_20261011.md`. No machine check was run.

## 1. The same physical source ball controls every high index

The actual state-adapted periodic frame gives \(A_\lambda=\lambda E_{00}+K(x)\), with a fixed principal matrix and \(K\in L^2\) depending analytically on the original balanced source \(X_0=(L^2_0)^m\times(H^1_0)^m\). In a vertical strip, removing the unitary imaginary fast propagator gives an actual Volterra bound independent of \(\operatorname{Im}\lambda\). Duhamel then bounds the full monodromy perturbation by \(C\|z\|_{X_0}\), uniformly in the high index. The earlier uniform semisimple rank-two background blocks therefore persist on a single source ball.

This step does not perturb the raw physical variable-principal \(\lambda P(d)\) and so does not overlook its unbounded \(\lambda\delta P\) variation. Complete matrix holonomy and the actual physical source chart remain present.

## 2. Even Volterra fibers give the missing full-matrix estimate

For \(2r\) alternating insertions, the fast-fast path has \(r+1\) fast intervals and \(r\) slow intervals. Its duration density is
\[
v_r^{ff}(\tau)=\frac{\tau^r(L-\tau)^{r-1}}{r!(r-1)!},
\quad
v_r^{ss}(\tau)=\frac{\tau^{r-1}(L-\tau)^r}{(r-1)!r!}.
\]
The disintegration uses coordinate Lebesgue measure, with Jacobian one. As a consistency check, each density integrates to the full ordered-simplex volume \(L^{2r}/(2r)!\). Fiber Cauchy–Schwarz and enlarging the squared-input integral to the product cube give
\[
\|K_{2r}\|_2\le e^{L\|H\|}
\frac{L^{r-1/2}}{\sqrt{r!(r-1)!}}\prod_{j=1}^{2r}\|f_j\|_2.
\]
Thus diagonal and offdiagonal kernel series converge locally uniformly in \(L^2\). The zero-insertion endpoint atoms are kept separately. The actual full matrix remainder, sampled at \(2\pi in/L+\sigma\), is a jointly entire \(\ell^2\) map. Larger-disk Cauchy estimates promote it to \(\ell^2(A_r)\), where \(A_r\) is the holomorphic disk-function Banach space. The sequence of sup norms supplies a bound, not a holomorphic map by itself; this wording has been corrected.

## 3. Actual two-root extraction and strong sequence analyticity

Diagonalize the finite simple slow holonomy locally and shift the grid by its eigenvalue. Uniform Riesz compression gives actual two-dimensional matrices
\[
B_n(\zeta)=\operatorname{diag}(e^{L\zeta},1)+Q_n(\zeta),
\quad Q\in\ell^2(A_r).
\]
For the characteristic discriminant \(D=(\operatorname{tr}B)^2-4\det B\), uniform Rouché gives exactly two roots. Logarithmic contour moments define their center \(c\) and half-gap squared \(g\) without selecting root square roots.

At the template, \(D_0=(e^{L\zeta}-1)^2\) and \(D_1=2(e^{L\zeta}-1)(Q_{11}-Q_{22})\). The quotient has at most a simple pole, so the linear part of the gap-square moment vanishes. Uniform Taylor estimates give \(|c_n|\le C\|Q_n\|\), \(|g_n|\le C\|Q_n\|^2\). Two-factor Cauchy–Schwarz plus bounded higher factors prove strong Banach analyticity into \(\ell^2\times\ell^1\), not merely coordinatewise analyticity.

The physical uniform background has \(Q(0)\ne0\) in general. The main now correctly proves its derivative cancellation separately: in the exact uniform eigenframe the multiplier difference \(F_n\) has a simple zero, \(D_0=F_n^2\), and \(D_1/F_n^2\) again has at most a simple pole. Shifting moments to the exact collision gives \(D_zg(0)=0\). Hence the physical \(\ell^1\) gap map has a quadratic leading term and a genuine \(\ell^1\) cubic remainder.

## 4. Independent Born Hessian and normalization check

On the fixed free-component mean leaf, \(\langle\dot A\rangle=0\), \(\dot H=0\), and \(\dot A=DA(0)f\) is independent of \(\lambda\). Actual Duhamel at the exact fast/slow collision gives offdiagonal entries \(\rho L\Gamma_n^+\), \(\rho L\Gamma_n^-\), with zero diagonal first variations. In the actual background eigenbasis the leading discriminant is
\[
\rho^2L^2\{\gamma_n^2(\lambda-\lambda_n)^2
4\epsilon^2\Gamma_n^+\Gamma_n^-\}.
\]
The actual half-root-difference square is therefore
\[
g_n(\epsilon f)=-4\epsilon^2\Gamma_n^+\Gamma_n^-/\gamma_n^2+O_{\ell^1}(\epsilon^3).
\]
Both the sign and the factor four pass. The moving-frame commutator vanishes inside the scalar collision block, and second-order off-cluster corrections do not alter this degree-two constant term. There is no diagonal first-order root shift to add on this fixed source mean leaf.

The \(\Gamma\) sequences also admit a direct budget: uniformly bounded actual eigenvectors and dual rows give \(|\Gamma_{\ell n}^\pm|\le C\|\widehat{\dot A}_{\pm n}\|\). Parseval proves \(X_0\to\ell^2\); the slope \(\gamma_n\) is uniformly separated from zero. Negative real-field indices correspond to channel \((M-\ell,-n)\), not a separate assertion that every positive-index gap is real.

For the framed offdiagonal candidates, template normalization divides by \(\rho_\ell(H_0)\), whereas actual Duhamel uses \(\rho_{\ell n}\). The main now retains \(\chi_{\ell n}=\rho_{\ell n}/\rho_\ell(H_0)=1+O(1/n)\). Their first variation is \(\chi_{\ell n}L\Gamma^\pm\); only after an explicitly stated extra division is it \(L\Gamma^\pm\). All these finite scalar changes preserve \(\ell^2\) analyticity.

## 5. Verdict and precise limitation

**PASS:** for every fixed finite \(M\) and the stated nonzero uniform background satisfying no-adjoint-alias, one balanced physical source ball supplies all sufficiently high actual rank-two Floquet blocks, center corrections in \(\ell^2\), invariant half-gap squares in \(\ell^1\), and the exact physical Born Hessian. The assumptions and high-index threshold depend on the background; no uniform-in-\(M\) assertion is made. Original \(B,\Gamma,c\) and the trace normalization remain in their established roles.

The candidates are not yet invariant action/divisor coordinates, a source inverse, canonical norming data, or a nonlinear Hamilton completeness theorem. This audit does not infer independence of infinite gap blocks, an ordinary common fiber, or all-M Liouville integrability from these sequence estimates alone.

## 6. Added main §8: finite high-gap independence — PASS

The newly added §8 was read in full. It supplies the required argument beyond the sequence estimate. At the constant physical background, the actual projected coefficient derivative is a real, translation-equivariant isomorphism \(D\Pi(0):X_0\to(L^2_0)^{2m}\), with zero derivatives of coefficient means and complete \(H\). Hence every finite real coefficient Fourier tangent has a finite real physical source preimage.

For positive \(n\), combine the exact Born outputs into \(\alpha_{\ell n}=\Gamma^+_{\ell n}\), \(\beta_{\ell n}=\overline{\Gamma^-_{\ell n}}\). Negative Fourier conjugation makes \((A_n,B_n)\mapsto(\alpha,\beta)\) complex linear. Its high-index limit is the slow eigenbasis map \((A_ns_\ell,t_{M-\ell}B_n)_\ell\), an invertible square matrix with a fixed channel permutation. Exact generator eigenvectors give an \(O(1/n)\) error. Therefore the exact maps and inverses are uniformly bounded for all sufficiently high \(n\).

For any finite set of positive indices, choose an actual finite real source direction with every selected \(\alpha=\beta=1\), and test directions with \(\delta\alpha=0\), \(\delta\beta=1,i\) coordinatewise. The gap Hessian is \(-4\alpha\overline\beta/\gamma^2\), so each complex gap contributes an invertible two-real-coordinate block. Distinct Fourier indices have no mixed second-order Born terms. At \(\epsilon f\), the corresponding nonlinear real Jacobian minor is \(\epsilon^d\) times a nonzero constant plus \(O(\epsilon^{d+1})\), \(d=2m\,\#F\). This proves actual finite-block independence arbitrarily near the background.

Real analytic nonzero minors have open dense nonzero loci on the connected physical source ball. Taking countably many finite positive-index sets gives a residual set where every finite high-gap block is independent. Each positive index supplies \(2m\) real functions; its negative reflected channels are not counted again.

Transfer to a thinner common strong parameter domain remains explicitly conditional on an actual analytic parameter map whose derivative range contains all the used real finite physical Fourier directions. Ambient residuality or dense source inclusion alone does not prove that transfer. The independence lemma supplies neither canonical norming data nor the common-fiber Hamilton maximality missing in general \(M\).
