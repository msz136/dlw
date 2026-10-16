# All nonzero modes on a sufficiently small nonzero uniform background

2026-10-13. This gives a concrete general-M domain where the finite low supplements can be removed: every nonzero Fourier mode satisfies the actual spectral separation and Born inverse estimates. It does not claim this for every nonalias background. The result uses the original physical state/Poisson bridges and the preceding actual-period and symplectic-linearization constructions. Proofs remain branch-internal and await independent full review.

## 1. Statement and scope

Fix finite M≥2 and L>0, and write k₁=2π/L, m=M−1. There is εM>0 such that, for

\[
0<|\delta|/k_1<\varepsilon_M,\qquad S=M\delta,
\tag{1}
\]

the prior construction can be made with cutoff N=1. All positive Fourier frequencies n≥1 and all m slow channels are included; negative labels are their reflected partners. On a sufficiently small original fixed-mean general-field neighborhood, depending on the chosen NONZERO δ, the actual norming map needs no finite Fourier supplements. Consequently the established original symplectic torus linearization gives a full Cartesian weak-canonical state chart with no low residual block:

\[
\Omega=\sum_{\alpha}w_\alpha\,dv_\alpha^+\wedge dv_\alpha^-,
\qquad A_\alpha=w_\alpha v_\alpha^+v_\alpha^-,
\quad w_\alpha=(L\omega_\alpha\gamma_\alpha)^{-1}.
\tag{2}
\]

The source remains E=(L²₀)^m×(H¹₀)^m and retains all infinite spatial degrees of freedom. Constants and neighborhood radii may deteriorate as δ→0; the singular background δ=0 is excluded. This is an additional explicit domain for the full fixed-M goal, not a replacement of the earlier arbitrary-nonalias-background statement, which still retains a finite low block.

## 2. Uniform scaled background geometry

In the calibrated vector frame, the actual constant background generator is

\[
A^0_\lambda=\begin{pmatrix}\lambda&q_0\\r_0&H_0\end{pmatrix},
\quad q_0=\delta\widetilde q,\quad r_0=\delta\widetilde r,
\quad H_0=\delta\widetilde H,
\]

where all tilded matrices depend only on M. The slow eigenvalues are pℓ=δ ptildeℓ, with ptildeℓ=−i cot(πℓ/M), simple for 1≤ℓ≤m. The slow eigenbasis and its condition number can be chosen independently of δ. For m=1 no inter-slow separation is required.

Choose a fixed small cM>0 less than a fixed fraction of all nonzero differences |ptildeℓ−ptildej|, when present. For |δ|/k₁ sufficiently small, the neighborhoods

\[
\lambda=ik_n+p_\ell+\zeta,\qquad |\zeta|\le C_M'|\delta|,
\quad k_n=n k_1,\quad n\ne0,
\tag{3}
\]

have |λ|≥|k_n|/2, with a fixed disk-radius constant C'M large enough for the annuli used below. Slow multiplier differences satisfy

\[
|e^{Lp_j}-e^{Lp_\ell}|\ge c_M L|\delta|\quad(j\ne\ell),
\tag{4}
\]

because L|δ| is small and the tilded differences are fixed nonzero numbers. Thus the nonalias assumption holds automatically on this range. Neighboring n windows remain separated by a fixed fraction of k₁.

Finite matrix perturbation can be made uniform in n using |δ/λ| as the small parameter. Eliminating the fast component gives the slow effective matrix

\[
H_0+\frac{r_0q_0}{y-\lambda};
\]

its correction is O_M(δ²/|k_n|), compared with slow eigenvalue separation of order |δ|. Resolvent Neumann series on circles of radius cM|δ| around the pℓ, and the separated fast root, yield

\[
y_f=\lambda+O_M(\delta^2/|k_n|),\quad
y_\ell=p_\ell+O_M(\delta^2/|k_n|),
\tag{5}
\]

and a generator eigenbasis relative to diag(1,S(H₀)) of the form Id+O_M(|δ|/|k_n|), with uniformly bounded inverse. These estimates hold on the slightly larger λ neighborhoods in (3). Derivative estimates give

\[
\partial_\lambda(y_f-y_\ell)=1+O_M(\delta^2/k_n^2).
\tag{6}
\]

The exact background dispersion relation from the existing Riesz lemma is also a direct way to obtain (5)–(6); here its expansion parameter is uniformly small even at |n|=1.

The implicit equation yf−yℓ=ikn therefore has exactly one solution in the appropriate small disk,

\[
\lambda_{\ell n}=ik_n+p_\ell+O_M(\delta^2/|k_n|),\qquad
\gamma_{\ell n}=1+O_M(\delta^2/k_n^2)\ne0.
\tag{7}
\]

The solution is purely imaginary for real δ: the original constant χ generator on the imaginary λ axis is anti-Hermitian, and the same real-axis implicit equation for its imaginary eigenvalues gives the unique local solution. This is an actual multiplier collision, not the leading grid point.

## 3. Actual multiplier estimates on every nonzero window

Choose λ circles of radius rM|δ| around the exact centers (7), with rM a sufficiently small fixed constant, and slightly thicker annuli. On these annuli, the fast and selected slow multipliers, and all other slow multipliers, have separation bounded below by a constant times L|δ|. Inside the disk the selected pair stays separated from the other slow multipliers.

Here it is important not to estimate the background monodromy by an arbitrary O(δ) perturbation. Diagonalize the ACTUAL constant generator using (5). Near (3), all its exponentiated diagonal entries are within O_M(L|δ|) of 1, since e^{ik_nL}=1. Conjugating this diagonal matrix by Id+O_M(|δ|/|k_n|) therefore changes it by O_M(Lδ²/|k_n|), not O_M(|δ|/|k_n|). Eigenvalue corrections in (5) change their exponentials by the same order. Consequently, in the fixed slow eigenbasis,

\[
\left\|e^{LA^0_\lambda}
-\operatorname{diag}(e^{L\lambda},e^{LH_0})\right\|
\le C_M\frac{L\delta^2}{|k_n|}.
\tag{8}
\]

Relative to the multiplier separation L|δ|, the perturbation is O_M(|δ|/|k_n|), uniformly small already for n=1 under (1). Uniform resolvent integration thus provides all required rank-two Riesz blocks, their annular individual projectors, the two-root discriminants and the uniformly controlled reductions. Disk and multiplier contours may depend on the fixed δ but not on n.

For each chosen δ, the background sequence in (8) is square summable over all n≠0. The actual ambient duration-kernel theorem gives a strong analytic ℓ² correction on a source neighborhood. Shrink that ONE neighborhood until its sequence-norm change is smaller than the common δ-dependent spectral budget. Since ℓ² embeds in ℓ∞, all the windows simultaneously retain separation and the Riesz estimates. This is not an intersection of n-dependent source neighborhoods.

Every circle avoids the poles ±S because its imaginary center has modulus at least a fixed fraction of k₁ while S=O_M(δ). The original reciprocal weights are nonzero and satisfy the same two-sided n² growth for the fixed δ. All contour and sequence arguments for periods and their original fields therefore remain valid with N=1.

## 4. The entire Born coordinate derivative is invertible

The [physical coefficient chart, §5](../dlw_recovery_20261011/all_m_physical_holonomy_state_inverse_20261011.md) supplies DΠ₀:E→(L²₀)^{2m} as a bounded isomorphism. Its direct Neumann budget is 0<|δ|≤k₁/(128M³), so choose εM≤1/(128M³), in addition to the spectral budgets above. This coefficient bound alone is not claimed to be the final sufficient constant for every spectral inequality. DΠ₀ is a translation-equivariant Fourier multiplier, and D⟨a⟩₀=D⟨b⟩₀=DH₀=0.

The exact collision basis from (5) has fast/slow vectors and duals within O_M(|δ|/|k_n|) of the uncoupled basis. Thus the full real high-channel Born map on each positive Fourier frequency satisfies

\[
T_n=T_\infty+O_M(|\delta|/|k_n|),
\tag{9}
\]

where T∞ is the invertible slow-eigenbasis map, including the reflected-channel permutation for the lower coupling. T∞ and its inverse are fixed finite matrices independent of n and δ. Choose εM so that ||T∞⁻¹(Tn−T∞)||<1/2 for EVERY n≥1. Then Tn and Tn⁻¹ are uniformly bounded for the entire sequence, not just for a tail.

The actual calibrated norming derivative is L times this Born map composed with DΠ₀. The n≥1 Parseval identification therefore makes it a bounded real Hilbert isomorphism onto the entire pair-sequence data space, with NO finite supplements. Its complexification is the corresponding complex isomorphism. The actual nonlinear norming sequence is strongly analytic by the preceding all-window estimates; the Banach inverse function theorem gives the true original physical state inverse on an open neighborhood.

No low coordinate has been thrown away: the complete derivative is invertible because all nonzero modes now appear among the actual labeled spectral pairs. Fixed component means already removed the zero modes from the source.

## 5. Consequences for complete spectral coordinates on this domain

The earlier actual reciprocal-period proof, bounded-profile field synthesis and common product-torus construction only required the uniform windows, strong sequence bounds, exact Born derivative and original physical graph identities now verified for n≥1. They therefore apply with all labels and no finite residual space. The [original Liouville-field averaging](SYMPLECTIC_LIOUVILLE_AVERAGING.md) produces (2) with an actual analytic state inverse and the original weak weights.

The [analytic invariant-descent theorem](INVARIANT_BASE_ACTION_INVERSE.md) then has no η variable: every source-analytic invariant commuting with all these actions has the form

\[
f=\widehat f(J),\qquad J_\alpha=v_\alpha^+v_\alpha^-
=d_\alpha A_\alpha\in\ell^1.
\tag{10}
\]

In particular the actual spectral traces have this complete action-only representation on the stated small-background domain. It is an invariant representation, not an assertion that actions alone reconstruct a state without its angles.

For an all-nonzero reference profile, the relative action–angle parametrization already proved now has no low block. Its topology and the weak weights remain exactly as stated there. The original physical Hamiltonian still must be checked against its actual low/smooth definition, and its frequency growth and real-time trajectory domain must be established. Scalar analytic action dependence alone does not imply a well-posed flow in the rough E topology.

## 6. Domain audit

The new conclusion is for every fixed finite M on the additional nonempty range (1), with a sufficiently small general-field perturbation at each chosen δ. It neither covers δ=0 nor resolves possible exceptional low collisions at larger nonalias backgrounds. It is compatible with the full requested general-field objective because no spatial truncation, soliton restriction, replacement Poisson bracket or artificial time change occurs. The remaining original-time proof is still essential, and the complete goal remains ACTIVE.

Subsequent progress: [ORIGINAL_TIME_ACTION_FLOW.md](ORIGINAL_TIME_ACTION_FLOW.md) supplies the original scalar Hamiltonian's low-domain analyticity and action representation, the exact external B translation split, and actual original-time trajectories with smooth physical reconstruction on a Gaussian spectral decay domain. The dependency chain remains subject to a completion audit and independent review; the rough-E Cauchy claim is deliberately not made.
