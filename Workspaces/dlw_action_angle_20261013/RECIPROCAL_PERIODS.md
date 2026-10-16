# General M: reciprocal-weighted actual Floquet periods

2026-10-13. A new construction of actual commuting spectral Hamiltonians on the original balanced field chart. These are candidate nonlinear ACTIONS, not an established complete action–angle chart. Their actual Hamilton identities, common-domain sequence estimates and exact quadratic normalization are derived below from the declared existing general-M inputs. No external reviewer or full source re-audit has been performed in this branch.

## 1. Data, annuli and branches

Use the common complex source ball U⊂E, original trace functions F_r(λ), pole weight ω(λ)=(S²−λ²)/(16S), exact background high collisions λα and original finite-graph reconstruction operator B_x from [the weighted field sequence proof](../dlw_recovery_20261011/general_m_gap_frequency_weighted_hamilton_sequence_20261011.md). In particular,

\[
 X_{F_r(\lambda)}=\mathscr B_x[\omega(\lambda)Y_{F_r(\lambda)}],
 \tag{1}
\]

where Y is the auxiliary offdiagonal coefficient Hamilton field with the entire slow matrix H held fixed ONLY for this auxiliary derivative. The physical field retains its full frame correction and H variation. B_x is bounded, analytic and independent of λ.

Increase the common high cutoff N once. The fixed, uniformly isolated λ circles Γα may be surrounded by annuli on which the two eigenvalues μ_+,μ_- of the actual rank-two multiplier cluster are simple. On each annulus choose the discriminant square root by continuation from the background fast/slow generator labels. This simultaneous choice is possible by uniform perturbation of the nonzero background discriminant on slightly thicker annuli. Its winding is even (two enclosed branch roots), so the background square root is single-valued on the annulus. A relative square root of D/D_bg then extends it to all x in the small source ball.

Choose the local logarithm

\[
 \kappa_\alpha(\lambda,x)=\tfrac12\log(\mu_+/\mu_-),
 \tag{2}
\]

with background value κ=L(y_f−y_ℓ−ik_n)/2 near λα. Taking small fixed radii makes the eigenvalue ratio uniformly close to 1 on the annuli, so the log is jointly holomorphic in λ and the source. The ratio removes any scalar monodromy normalization. It uses the actual rank-two characteristic cluster, not the trace of the entire M×M matrix alone.

All disks avoid ±S for high enough N, and |ω(λ)|≈n² on them. A constant change of log branch contributes zero to the following integral because 1/ω is holomorphic on the disk. Exchanging the sheet reverses the sign; the background fast/slow label fixes this sign.

## 2. Actual reciprocal periods and their exact fields

Define

\[
 \boxed{\mathcal A_\alpha(x)=\frac1{2\pi i}
 \oint_{\Gamma_\alpha}\frac{\kappa_\alpha(\lambda,x)}{\omega(\lambda)}\,d\lambda.}
 \tag{3}
\]

The contour is fixed in the original CENTERED λ-plane; S and the prescribed mean-leaf labels are fixed. If the external B(t) changes, the existing centering/translation bridge is used, rather than treating B as an extra frozen physical constraint. No source-dependent shift is omitted in (3).

For each fixed λ on Γα, κ is a holomorphic function of the actual characteristic classes. With determinant normalization det N=1, these can be expressed through F_1,…,F_{M−1} by the finite Newton identities. Thus, for jointly analytic scalar coefficients bαr,

\[
 d_x\kappa_\alpha=\sum_{r=1}^{M-1}b_{\alpha r}(\lambda,x)dF_r(\lambda).
 \tag{4}
\]

The cluster isolation and annular eigenvalue separation make these coefficients uniformly bounded for all high labels on a smaller common source ball.

Differentiating (3) at fixed λ and applying the ORIGINAL Hamilton identity gives

\[
 X_{\mathcal A_\alpha}=\frac1{2\pi i}\oint_{\Gamma_\alpha}
 \sum_r\frac{b_{\alpha r}}{\omega(\lambda)}X_{F_r(\lambda)}d\lambda
 =\mathscr B_x\left[\frac1{2\pi i}\oint_{\Gamma_\alpha}
 \sum_r b_{\alpha r}Y_{F_r(\lambda)}d\lambda\right].
 \tag{5}
\]

This is exact pole-weight cancellation for arbitrary fixed M. The second integral is the auxiliary coefficient Hamilton field of the UNWEIGHTED local period

\[
 \mathcal K_\alpha=\frac1{2\pi i}\oint\kappa_\alpha d\lambda
 \tag{6}
\]

with H held fixed in its auxiliary derivative. We do not assert the full physical tensor equals the auxiliary tensor on arbitrary functions.

Since all actual trace classes are in involution, the differentials (4) and Bochner contour identities show that all Aα mutually commute and commute with every fixed trace and each defined C_j. Derivatives of b do not enter this bracket calculation: it is the bilinear pairing of the already computed exact differentials. For real fields, choose the reflected sheet and log so Aα*=overline(Aα); independent Re/Im parts are real original Hamiltonians.

## 3. Common-domain summability without a residual 1/n estimate

In the moving slow-holonomy grid λ=K_n+h_ℓ(H)+ζ, the existing Riesz lemma gives

\[
 B_\alpha(\zeta,x)=\operatorname{diag}(e^{L\zeta},1)+Q_\alpha(\zeta,x),
 \qquad Q:U\to\ell^2(\mathcal A_r)\text{ strongly analytic}.
 \tag{7}
\]

Take a fixed contour in a smaller annulus. Deforming Γα to this contour crosses no branch roots or poles. The unweighted local period K is the same holomorphic matrix functional for all α and is independent of the translating grid center. The ratio also removes the normalizing scalar e^{Lhℓ}. At the uncoupled template,

\[
 \kappa_0=L\zeta/2,
 \quad D\kappa_0[Q]=\tfrac12(e^{-L\zeta}Q_{11}-Q_{22}).
 \tag{8}
\]

Both are holomorphic throughout the disk. Their contour integrals vanish. Thus K(0)=DK(0)=0 and uniform holomorphic Taylor estimates give

\[
 \|DK(Q)\|\le C\|Q\|_{\mathcal A_r}.
 \tag{9}
\]

For the weighted functional in (3), multiplication by 1/ω(K_n+hℓ+ζ) is holomorphic in the disk with norm ≤C/n². Its zeroth and first matrix variations also integrate to zero, uniformly in H. Consequently

\[
 |\mathcal A_\alpha(x)|\le C\langle n\rangle^{-2}\|Q_\alpha(x)\|_{\mathcal A_r}^2.
 \tag{10}
\]

When varying auxiliary a,b at fixed H, the old uniform ODE/Riesz estimate gives ||D_ab Qα||≤C as a map L²-pairs→A_r. Equations (5),(9) therefore imply

\[
 \|X_{\mathcal A_\alpha}(x)\|_E\le C\|Q_\alpha(x)\|_{\mathcal A_r}.
 \tag{11}
\]

In contrast to constant background division gα/ωα, no replacement of ω(λ) by ωα was made, and hence no separate O(1/n) remainder is needed in this bound. This is a structural estimate, not a proof that the actual tail has a strictly better decay rate: Q itself can have 1/n tails.

The same multilinear ℓ² ideal estimates as in the Riesz lemma, uniform contour Cauchy estimates, and holomorphic dependence on the finite H parameters give

\[
 \boxed{\mathcal A:U\to\ell^1_2\text{ analytic},\qquad
 (X_{\mathcal A_\alpha}):U\to\ell^2(E)\text{ analytic}.}
 \tag{12}
\]

Here ||A||ℓ¹₂=Σ⟨n⟩²|Aα|. For the field sequence one may also use local ℓ² boundedness and coordinate holomorphy in the Hilbert target. This argument works on one common source ball and cutoff; it is not a countable intersection of index-dependent neighborhoods.

Every c∈ℓ² now defines a genuine scalar Hamiltonian H_c=ΣcαAα and an absolutely E-convergent field Σcα X_Aα. Passing from finite sums in the continuous Ω identity proves i_XHc Ω=dH_c. Analytic Banach ODE gives actual local flows, with a common time for bounded coefficient balls. Spatial translation equivariance gives smooth persistence in the same low time window. Finite-profile approximation preserves the actual trace classes; smooth convergence gives every defined local C_j. Different profiles commute. No arbitrary bounded profile or old-strong-domain membership is inferred solely from (12).

## 4. Exact quadratic normalization at the ACTUAL background

Let ξ=λ−λα. At the uniform source,

\[
 \kappa_\alpha(\lambda,0)=\tfrac L2(y_f(\lambda)-y_\ell(\lambda)-ik_n),
 \quad \partial_\lambda\kappa_\alpha(\lambda^\alpha,0)=L\gamma_\alpha/2.
 \tag{13}
\]

In a sufficiently small disk the analytic function κ² has exactly the same two simple-or-double zeros as the characteristic discriminant. Its quotient by the Weierstrass polynomial is analytic and nonzero. Choosing its square root b gives on the annulus

\[
 \kappa_\alpha=b_\alpha(\lambda,x)
 \sqrt{(\lambda-a_\alpha(x))^2-g_\alpha(x)},
 \quad b_\alpha(\lambda^\alpha,0)=L\gamma_\alpha/2.
 \tag{14}
\]

Here κ² is single-valued in the disk: it is the analytic small-argument square of half-log of the local eigenvalue ratio (equivalently the local square of arccosh(tr B/(2√det B))). Individual κ branches are needed only on the annulus. The nonzero determinant and local logarithm/square-root branches are fixed once by the cluster near its nonzero common multiplier.

Expanding √(w²−g)=w−g/(2w)−g²/(8w³)−… on the contour gives the exact convergent local residue expansion

\[
 \mathcal A_\alpha=-\frac{g_\alpha}{2}
 \frac{b_\alpha(a_\alpha,x)}{\omega(a_\alpha)}+O(g_\alpha^2).
 \tag{15}
\]

The coefficients in O(g²) are analytic functions of the source on the fixed disk. In particular Aα(0)=dAα(0)=0. The old actual Born identity gα^[2]=−4Γα+Γα−/γα² and Dνα±(0)=LΓα± yield

\[
 \boxed{\mathcal A_\alpha^{[2]}
 =-\frac{L\gamma_\alpha}{4\omega_\alpha}g_\alpha^{[2]}
 =\frac{L\Gamma_\alpha^+\Gamma_\alpha^-}{\omega_\alpha\gamma_\alpha}
 =\frac{\nu_\alpha^{+,[1]}\nu_\alpha^{-,[1]}}
 {L\omega_\alpha\gamma_\alpha}.}
 \tag{16}
\]

The notation [2] means the quadratic Taylor polynomial, not the second differential without its 1/2 factor. All coefficients use the exact background collision and γ, not their high-frequency approximations.

By the independently established ORIGINAL bracket {να+,νβ−}_0=δαβ Lωαγα, the linearization of X_Aα in the actual calibrated norming chart is exactly

\[
 \boxed{\dot\nu_\alpha^+=\nu_\alpha^+,\quad
 \dot\nu_\alpha^-=-\nu_\alpha^-,}
 \tag{17}
\]

with zero linear components in other high labels and low Fourier supplements. These are complexified Hamiltonian identities; the real and imaginary Hamiltonians have the corresponding realification factors. We do not assert unit speed for Re A without that conversion.

Each finite real block of A has a nonzero quadratic independence minor by (16) and the old exact finite-Fourier Born preimages. The same analyticity/Baire argument as for gaps gives generic finite-block independence on the declared old source parameter ball, after intersecting the common domains once. This is not an infinite submersion or independence on every source.

## 6. What this construction does and does not accomplish

It produces actual, frame-invariant commuting spectral integrals for all fixed M, on general fields, with the original pole factor canceled in their actual fields and the correct unit quadratic normalization. It upgrades the purely background instruction “divide the gap by its frequency” to a nonlinear contour Hamiltonian.

It does NOT prove X_Aα να±=±δαβ νβ± away from the background, nor that the current ν are nonlinear canonical norming coordinates. The functions να still depend on the chosen full frame, and their nonlinear brackets are unknown. Low coefficient supplements remain nonspectral. The field sequence in (12) is still compact as a synthesis map, so the obstruction in RESEARCH.md applies to the unweighted infinite submersion route for these A as well.

The immediate next problem is to compute the nonlinear period-flow action on the framed norming data, including the moving two-plane and its center, and decide whether an analytic renormalization supplies conjugate variables with a controlled weighted inverse. Only then can these candidate actions become a complete action–angle system.

### Continuation

[PERIODIC_SPECTRAL_FLOWS.md](PERIODIC_SPECTRAL_FLOWS.md) subsequently proves the exact single-index 2πi return and finite-family nonlinear eigen-coordinates. [NONLINEAR_NORMING.md](NONLINEAR_NORMING.md) supplies the full moving-frame norming derivative. These replace the unfinished finite-family part of the preceding research task; they do not yet provide an infinite simultaneously controlled action–angle inverse. The next analytic input and its still-missing physical reconstruction are recorded in [UNIFORM_CAUCHY_ESTIMATE.md](UNIFORM_CAUCHY_ESTIMATE.md).

Latest continuation: [BOUNDED_PROFILE_PHYSICAL_FLOWS.md](BOUNDED_PROFILE_PHYSICAL_FLOWS.md) uses the AMBIENT full sequence derivative of the unweighted ℓ¹ period map, rather than the separate field norm estimate (11), to obtain actual ℓ∞-profile physical flows. [INFINITE_TORUS_STATE_CHART.md](INFINITE_TORUS_STATE_CHART.md) then gives a common infinite state chart diagonalizing all high generators. This supersedes the earlier profile/state-chart limitations, while full weak canonical/action inverse and original-time completeness remain unproved.
