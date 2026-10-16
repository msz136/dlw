# A uniform spectral-circle estimate for the infinite simultaneous-flow problem

2026-10-13. This is an analytic input for the next step after [exact individual periods](PERIODIC_SPECTRAL_FLOWS.md), not a claim that an infinite DLW dressing/state inverse has been constructed.

## 1. Geometry and the operator

Use the fixed high background circles Γℓn with centers

\[
 c_{\ell n}=2\pi in/L+p_\ell+e_{\ell n},\quad
 e_{\ell n}=O(1/|n|),\quad 1\le\ell\le m.
\]

The existing nonalias condition and the exact high-frequency separation allow a fixed sufficiently small common radius r and positive mutual separation after increasing N. Choose all circles counterclockwise. Let

\[
 \mathcal H=\ell^2_{\ell,|n|\ge N}(L^2(\Gamma_{\ell n};\operatorname{Mat}_M)),
\]

using normalized arclength, equivalent to the usual arclength because r is fixed. Define the Cauchy transform initially for finitely supported smooth boundary data by

\[
 Cf(\lambda)=\frac1{2\pi i}\sum_\alpha\oint_{\Gamma_\alpha}
 \frac{f_\alpha(\mu)}{\mu-\lambda}d\mu.
 \tag{1}
\]

**Lemma 1.** Its two boundary operators C± extend boundedly to H, with constants independent of the number of active circles. C+−C−=Id. The same constants work after a uniformly small bounded perturbation of the center corrections that preserves the common separation.

**Proof.** On the same circle, C± are the ordinary Fourier/Hardy projections, bounded on L². Between different circles whose Fourier labels differ by a large k=n−j, expand the kernel as

\[
 \frac1{\mu-\lambda}=\frac1{(2\pi i/L)(n-j)}+R_{\alpha\beta}(\mu,\lambda),
 \qquad |R_{\alpha\beta}|\le C|n-j|^{-2}.
 \tag{2}
\]

The bounded channel shifts, center corrections and contour radii give this estimate uniformly. The leading term applies the discrete Hilbert transform to the contour moments mα=(2πi)⁻¹∮fαdμ, then inserts the output as a constant on the target circle. The moment map and constant insertion are bounded between H and the sequence ℓ² spaces. The convolution kernel 1/k, k≠0, has bounded Fourier multiplier: its sine Fourier series is the bounded sawtooth function. Thus this term is bounded on ℓ²; deleting the finitely many central labels is a bounded projection and does not alter the conclusion.

The error kernel in (2) has summable row and column bounds because Σk≠0 k⁻²<∞. The finitely many slow channels contribute only finite multiplicities. Schur's estimate gives a bounded error operator. The remaining bounded differences |n−j| are controlled by uniform contour separation and have a uniformly finite number of neighbors per row. This proves the claimed bound. The jump formula follows first for smooth finite data and then by density. ∎

For f∈H, (1) converges normally on compact sets away from all circles: for distant n, the absolute contour contribution is ≤C||fℓn||L²/|n|, which is summable by Cauchy–Schwarz. This also justifies passage from finite supported data to the analytic transform and its derivatives on these compact sets.

## 2. Small matrix jumps: uniform finite and countable factorization

Suppose the jump is Vα=I+wα with

\[
 w\in\mathcal H\cap\ell^\infty(L^\infty),\qquad
 C_0\|w\|_\infty<1,
\]

where C0 bounds C−. Seek μ=I+η with η∈H. Although the constant sequence I is not in H, the unknown η and the products below are. The singular integral equation is

\[
 \eta=C_-w+C_-(\eta w).
 \tag{3}
\]

Right multiplication by w has H-operator norm ≤||w||∞. The Neumann series therefore gives a unique η∈H and

\[
 \|\eta\|_H\le\frac{C_0\|w\|_H}{1-C_0\|w\|_\infty}.
 \tag{4}
\]

Put F=I+C(w+ηw). Its boundary values satisfy F+=F−(I+w), with F−=I+η. The solution depends analytically on w in the intersection Banach space with norm ||w||H+||w||∞, and the constants do not depend on the number of nonzero jumps.

For invertibility take ||w||∞ smaller once so the corresponding inverse-jump equation also contracts; w_inv=(I+w)⁻¹−I has sup norm ≤||w||∞/(1−||w||∞) and H norm bounded by the same factor times ||w||H. Solve the left-multiplication version for G. For finite active circle sets, FG has no jumps, is entire, and tends to I at ordinary complex infinity; hence FG=I by Liouville. This establishes invertibility of the finite factors.

For countably many circles, truncate w on finite exhaustive sets. Equation (3), uniform resolvent bounds and the identity

\[
 \eta_F-\eta=(I-C_-M_{w_F})^{-1}
 C_-[(w_F-w)+\eta(w_F-w)]
\]

show ηF→η in H: the second term tends to zero by the H tail of η and the bounded sup norm of w. The inverse factors converge in the same manner. Normal compact convergence of their Cauchy transforms then gives FG=I off the contours and their analytic continuations. This establishes invertibility in the constructed Cauchy class, not a uniqueness theorem among all possible entire growth classes with an arbitrarily weak asymptotic normalization.

## 3. What must still be proved for DLW

The actual individual-period cocycle is exp(tαWα). Its diagonal reference exp(tαJα), where Jα is the constant fast/slow half-projector, can be absorbed into each interior factor. The remaining jump is a natural candidate for (3). Uniform bounds on bounded profiles would require proving, on the actual source domain, the appropriate small H and sup bounds for these remainder jumps, including their spatial regularity and the full frame dependence.

Even after obtaining those jump bounds, a factorization alone is NOT yet a physical DLW flow. The main remaining step is to reconstruct a connection of the exact affine spectral form in the correct mixed function space, satisfy every finite physical graph constraint, and control the original state inverse uniformly in the active label set. Infinite contours extend to spectral infinity, so the finite-contour Liouville argument must not be reused without growth and reconstruction estimates.

Lemma 1 and (3)–(4) remove the elementary Cauchy-operator dependence on the number of circles. They do not remove the missing source reconstruction theorem or prove an infinite Bochner chart.
