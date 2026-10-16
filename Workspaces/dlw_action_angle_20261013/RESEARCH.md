# DLW general-field action–angle: independent continuation

2026-10-13. Branch objective: construct actual action–angle coordinates for general physical fields, preserving the original weak symplectic form and original time. General fixed M is the target. Finite-dimensional soliton manifolds and replacement Poisson brackets are not substitutes. The goal is ACTIVE, not achieved by the results below.

## 1. Declared input and scope

Take m=M−1, S≠0 and a fixed nonalias uniform background as in the existing general-M papers. Work on one fixed-component-mean real leaf

\[
 E=(L^2_0(S^1_L;\mathbb R))^m_q\times(H^1_0(S^1_L;\mathbb R))^m_d,
 \qquad J=-\tfrac1{16}\operatorname{offdiag}(D I_m).
\]

The original constant form, with K=D_0^{-1}, is

\[
 \Omega(v,w)=-16\int_0^L[(Kv_q)\cdot w_d+(Kv_d)\cdot w_q]dx.
 \tag{1}
\]

Use the convention i_XH Ω=dH and {f,g}=df(X_g). Hence the finite canonical form is Σ dQ_j∧dP_j and {Q_i,P_j}=δij.

Inputs not reproved in this continuation:

* [fixed-gap balanced Hamilton flows](../dlw_recovery_20261011/general_m_fixed_gap_balanced_hamilton_flow_20261011.md): actual gap functions, their original analytic E-valued Hamilton fields, involution and same-window smooth persistence;
* [frequency-weighted infinite flows](../dlw_recovery_20261011/general_m_gap_frequency_weighted_hamilton_sequence_20261011.md): on one source ball, Z_α=X_gα/ωα is strongly analytic into ℓ²(E), where ωα=(S²−λα²)/(16S), λα is the FIXED exact background collision, and |ωα|≈n²;
* [same-state finite-block independence](../dlw_recovery_20261011/general_m_high_gap_same_strong_hilbert_transfer_20261011.md): states with all finite real high-gap blocks independent exist on its declared parameter domain;
* [augmented state inverse](../dlw_recovery_20261011/general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md): an actual framed high-norming plus finite nonspectral low-data inverse. This is NOT an invariant action–angle inverse.

All conclusions using these inputs are conditional on their stated domains and proofs. No new claim is made about arbitrary smooth Cauchy data, unbounded M, the whole old strong domain, zero-mean singular branches, or compact invariant tori.

## 2. A topology obstruction already present in the ORIGINAL form

Equip E with its standard Hilbert inner product, H¹ using Fourier weight 1+k_n², k_n=2πn/L. Identify E* with E by the Riesz map and write Ω(v,w)=⟨Av,w⟩. At each nonzero Fourier frequency, the isometry to unweighted coordinates is

\[
 (q_n,d_n)\mapsto(q_n,\sqrt{1+k_n^2}\,d_n).
\]

The original D⁻¹ contributes 1/(ik_n), and the mixed H¹ coordinate contributes 1/√(1+k_n²). Thus the singular values of A at each positive frequency are

\[
 a_n=\frac{16}{|k_n|\sqrt{1+k_n^2}},
 \qquad\text{real multiplicity }4m.
 \tag{2}
\]

For clarity, D⁻¹ on the real orthonormal (cos,sin) basis is R_n=[[0,−1/k_n],[1/k_n,0]]. The real block of A has offdiagonal blocks −16 R_n/√(1+k_n²). It is skew, invertible for each finite n, and its transpose times itself is a_n² I_4.

Since Σ a_n<∞, A is trace class, in particular compact. It is injective because every Fourier block is invertible, but it cannot have a bounded inverse on the infinite-dimensional E. This explicitly identifies the weakness of Ω.

**Theorem 1 (no strong canonical chart in the same topology).** No local C¹ diffeomorphism between open subsets of E and an infinite-dimensional Hilbert phase with a boundedly invertible canonical symplectic operator can pull that strong form back to (1).

**Proof.** At any point, the coordinate derivative T is a bounded isomorphism. Pullback of a strong form is T* A_can T, a boundedly invertible operator E→E*. But Ω♭ is compact. A compact invertible operator on an infinite-dimensional Banach space would make the identity compact, a contradiction. Equivalently, the transformed form remains compact by the operator-ideal property. ∎

This rules out an unweighted strong ℓ² canonical form, not action–angle theory. A legitimate target may carry a weak weighted form, or a demonstrably stronger relative-action topology. Rescaling coordinates by the inverse weights in (2) is unbounded in E and therefore changes the topology. A statement using such a rescaling must prove its new state inverse and flow domain.

## 3. The normalized infinite gap map cannot be an ℓ² submersion

Use independent real components of the conjugate spectral labels; multiplication by fixed nonzero complex ω is represented by a bounded real 2×2 block. Define

\[
 \mathcal I(x)=(g_\alpha(x)/\omega_\alpha)_\alpha\in\ell^2,
 \qquad\mathcal T_x c=\sum_\alpha c_\alpha Z_\alpha(x).
 \tag{3}
\]

The ℓ²(E) input implies that T_x:ℓ²→E is Hilbert–Schmidt. All statements below have the same meaning in independent Re/Im coordinates; harmless fixed factors only change constants.

For v∈E, the actual original Hamilton identity gives

\[
 (D\mathcal I_x v)_\alpha=\Omega(Z_\alpha(x),v).
 \tag{4}
\]

Therefore D I_x is Hilbert–Schmidt and

\[
 \|D\mathcal I_x\|_{HS}\le\|\Omega\|\Big(\sum_\alpha\|Z_\alpha(x)\|_E^2\Big)^{1/2}.
 \tag{5}
\]

It is in fact trace class in the Hilbert identifications, since it factors through the trace-class Ω♭ and a bounded synthesis adjoint. Compactness is the only property required below.

**Theorem 2.** On this E domain the normalized action candidate I is not a submersion onto unweighted ℓ² at any state. In particular no bounded right inverse of its derivative exists.

**Proof.** A compact operator cannot surject onto infinite-dimensional ℓ²: surjectivity and the open mapping theorem would place a target ball inside the closure of the image of a bounded ball, hence make that ball relatively compact. For a claimed right inverse R, compactness of DI·R=Id gives the same contradiction. ∎

**Quantitative finite-section consequence.** Let P_F project onto a finite label set, and let R_F be any right inverse of P_F DI. For α∈F,

\[
 1=|(D I_\alpha)R_F e_\alpha|
 \le \|\Omega\|\|Z_\alpha(x)\|_E\|R_F\|.
 \tag{6}
\]

Because ||Zα(x)||→0, a sequence of finite sections covering all labels cannot have uniformly bounded right inverses. This does not contradict every finite block being independent. It shows precisely why finite-dimensional inverse function arguments alone do not pass to an infinite ordinary chart.

Neither theorem says that normalized actions are the right final action variables. Source-dependent or unbounded renormalization may avoid (5), but demands new estimates; scalar division by a very small actual gap cannot be assumed bounded on a neighborhood.

## 4. Positive result: exact finite canonical blocks on GENERAL fields

The following construction uses arbitrary general fields in E; it does not truncate their Fourier expansion or restrict them to a soliton manifold.

**Theorem 3 (finite spectral Darboux–Carathéodory block).** Let p=(p₁,…,p_r) be any finite real block of the actual spectral integrals on the common source domain, pairwise in involution, with independent differentials at x*. Suppose their original Hamilton fields are analytic E-valued fields, as supplied by the fixed-gap theorem. There is a local analytic chart

\[
 x\longleftrightarrow(P_1,…,P_r,Q_1,…,Q_r,\zeta),
 \quad P_j=p_j(x)-p_j(x_*),
\]

with ζ in an infinite-dimensional analytic transversal N such that

\[
 \Omega=\sum_{j=1}^r dQ_j\wedge dP_j+\Omega_N,
 \quad \{P_i,P_j\}=\{Q_i,Q_j\}=0,
 \quad \{Q_i,P_j\}=\delta_{ij}.
 \tag{7}
\]

Ω_N is the inherited closed weakly nondegenerate form. The actual spectral flows satisfy Q̇_j=δij, Ṗ=0, ζ̇=0 for Hamiltonian p_i. These are local conjugate coordinates, not a claim of periodic real angles or full infinite spectral completeness.

### 4.1 Admissible probes, not arbitrary weak-symplectic covectors

Independence of dp_i and weak nondegeneracy imply independence of X_pi. Smooth finite Fourier linear observables separate E and their original Hamilton fields are smooth constant E vectors. We can therefore choose r such probes ℓ_a for which

\[
 C_{ai}(x_*)=d\ell_a(X_{p_i}(x_*))
\]

is invertible. Existence follows by density of finite Fourier coordinate functionals in E* and openness of the nonzero finite determinant. This step avoids incorrectly assuming every E* covector has a Hamilton field for a weak form.

### 4.2 Simultaneous hitting times are genuine Hamilton functions

Let Φ_t be the local joint flow of the commuting X_pi. The analytic implicit function theorem gives a unique vector τ(x) near zero satisfying

\[
 \ell(\Phi_{-\tau(x)}x)=\ell(x_*).
 \tag{8}
\]

The derivative with respect to τ is −C at y=Φ_−τ x. The group law and uniqueness give τ(Φ_s x)=τ(x)+s, hence {τ_i,p_j}=δij.

Hamilton flows preserve the original Ω by Cartan's identity. If f_a(x)=ℓ_a(Φ_−τ x), with τ held fixed when differentiating in x, then

\[
 d\tau_i=\sum_a(C(y)^{-1})_{ia}\,d f_a,
\]

and their genuine Hamilton fields are

\[
 X_{\tau_i}(x)=\sum_a(C(y)^{-1})_{ia}
 D\Phi_{\tau(x)}(y)X_{\ell_a}(y).
 \tag{9}
\]

The finite sum and analytic low flows make (9) an analytic E-valued field. Its Hamilton identity follows term by term; differentiating the coefficients is not part of the pointwise contraction identity. The preliminary τ_i need not commute with one another.

### 4.3 Split one pair, then induct

Set Q₁=τ₁ and P₁=p₁−p₁(x*). Since {Q₁,p_j}=δ1j, the field X_Q₁ preserves every p_j for j>1. The constant bracket implies that X_P₁ and X_Q₁ commute. The codimension-two submanifold N₁={P₁=0,Q₁=0} is split, and

\[
 \Psi(s,t,z)=\phi_{P_1}^{t}\phi_{Q_1}^{-s}z
 \quad(z\in N_1)
 \tag{10}
\]

satisfies P₁=s,Q₁=t. Its derivative has a bounded direct-sum inverse locally. The two flows preserve Ω, so Ω on the transversal is independent of s,t; mixed terms vanish since dP₁,dQ₁ vanish on transversal tangents. Directly,

\[
 \Omega(\partial_t\Psi,\partial_s\Psi)
 =\Omega(X_{P_1},-X_{Q_1})=1.
\]

Thus Ψ*Ω=dt∧ds+Ω_N₁. If v∈TN₁ annihilates TN₁ under Ω, it also annihilates X_P₁ and X_Q₁; hence it annihilates E and v=0. So Ω_N₁ is weakly nondegenerate.

The remaining p_j are unchanged by both flows in (10), descend to N₁, and retain independent differentials and involution. Their Hamilton fields are tangent to N₁. Restricted admissible probes still separate its finite Hamilton directions: project an ambient probe field by subtracting its components along X_P₁,X_Q₁. This is a finite analytic Hamilton/Dirac correction and gives the Hamilton field of the restricted probe. Repeat (8)–(10) on N₁. Extend its new coordinates constantly along the first pair's flows. Induction gives (7) while preserving ALL originally prescribed p_j as P_j. ∎

### 4.4 What happens to the original DLW Hamiltonian

Whenever the original H is defined differentiably on the smooth part of this chart, its commutation with all p_j implies ∂H/∂Q_j=0. Thus

\[
 H=H(P,\zeta),\quad \dot P=0,\quad
 \dot Q_j=\partial_{P_j}H(P,\zeta),
 \quad\dot\zeta=X_{H(P,\cdot)}^{N}.
 \tag{11}
\]

This does NOT prove original-time linearization: ζ generally evolves, so Q frequencies need not be constant. Nor does it assert a rough E Cauchy flow for H. The original mixed/smooth flow hypotheses remain necessary. Equation (11) isolates the remaining completeness problem exactly: eliminate independent residual dynamics by a full invariant spectral chart and prove H is a function of those actions alone.

## 5. Consequences for the next construction

1. Do not seek unweighted strong Hilbert action–angle coordinates on E. The original Ω forbids them, independently of spectral technology.
2. Finite canonical charts exist on genuine general fields, but their constants must deteriorate along an exhaustion for the current normalized actions. A merely finite-block argument cannot complete the goal.
3. Investigate a weak weighted Cartesian spectral chart first. The state inverse already gives high full-frame norming plus finite coefficients; remaining work includes nonlinear original norming brackets, invariant completion of low data, and removal of frame dependence in the correct sense.
4. For logarithmic coordinates, jointly choose a nonzero base, relative-action norm and bounded angular norm. Prove the relative invariant map is a submersion IN THAT DECLARED TOPOLOGY. Nonzero gaps by themselves do not supply this property.
5. The M=2 reciprocal contour identity is a benchmark. Its exact cancellation of the moving central parameter must be reproduced, not guessed, for the vector spectral curve and full matrix holonomy. Dividing a spectral differential by ω(λ) is a candidate for an action differential, but exactness and normalized angular periods still require proof.

## 6. Verification and current status

`verify_blocks.py` checks the real Fourier block in (2), the weak-form canonical sign convention, a two-action nonlinear finite canonical change, and a quantitative compact-action example by exact symbolic calculations. These checks support algebra only; the functional-analytic arguments and the DLW inputs above carry the theorems. They do not certify a general-M infinite action inverse.

Established in this continuation: explicit original-form compactness; failure of the current unweighted infinite submersion route; finite exact canonical spectral blocks without truncating general fields. A further construction is given in [RECIPROCAL_PERIODS.md](RECIPROCAL_PERIODS.md): actual all-M reciprocal Floquet periods, exact pole cancellation, common-domain weighted summability and unit background norming torque. These are nonlinear commuting spectral Hamiltonians, still only candidate complete actions. Outstanding: nonlinear invariant action/norming inverse, all-angle Poisson normalization, common domain of original time, and full action-only Hamiltonian. Overall goal remains ACTIVE.

## 7. Continuation: exact periods, nonlinear eigen-coordinates, and the infinite bottleneck

[PERIODIC_SPECTRAL_FLOWS.md](PERIODIC_SPECTRAL_FLOWS.md) now gives the full projector-adjoint Cauchy generator, spectral jump exp(tW), and an exact original physical return map at complex time 2πi. The sign on the rank-two cluster is removed by its holomorphic total projector; the entire matrix gluing argument leaves only the finite constant frame, eliminated by the established original physical slice. One common radius handles every SINGLE high index. A finite joint torus then gives a Bochner state chart with exact {Zβ±,Aα}=±δαβZβ± and local logarithmic cross-conjugacy. The joint radius is not yet uniform in the number of selected labels, and the averaged chart is not automatically symplectic.

[NONLINEAR_NORMING.md](NONLINEAR_NORMING.md) derives the exact existing norming equations, including the moving-frame derivative. Absolute and moving-grid centers are constant under these flows. The raw pair product has the precise correction δ²/4; the scalar-free center discriminant is an actual commuting characteristic invariant. Fixed-index raw product drift begins at order four, without claiming its coefficient is nonzero for actual DLW sources.

[UNIFORM_CAUCHY_ESTIMATE.md](UNIFORM_CAUCHY_ESTIMATE.md) proves L² Cauchy bounds independent of the number of separated spectral circles and the corresponding small-jump factorization in the Cauchy class. The outstanding application is a uniform mixed-space source reconstruction and all physical constraints for infinite jumps. Without it there is no full infinite torus action, infinite Bochner average, action inverse or original-time linearization. The original objective remains ACTIVE.

`verify_periods.py` adds twelve exact checks for the generator sign, half-projector exponential and period jump, norming commutator, corrected product, and finite frame action. These are algebraic checks, not a computational validation of the analytic period or reconstruction theorems. New proofs remain branch-internal, not independently peer-reviewed.

## 8. Actual jumps for bounded profiles

[TRANSLATED_JUMP_ESTIMATE.md](TRANSLATED_JUMP_ESTIMATE.md) uses the full monodromy duration kernels and spatial translation to prove W−J(H)∈C_sℓ²(annulus algebra), with a small common high tail. Consequently every bounded phase profile has a small normalized jump on one common source ball, and the countable Cauchy factorization applies uniformly in s. The estimate uses sup_s||·||ℓ², not the stronger unproved ||sup_s|·|||ℓ². Reference removal changes the interior spatial connection by a constant conjugation; the exact patch equation is retained. An explicit nilpotent small-jump example shows that this unweighted factorization class alone does not yield a 1/λ coefficient at infinity, even with spatial smoothness. Physical reconstruction using the additional actual adjoint compatibility, and all subsequent full action–angle steps, remain open. No new algebra checks or PDE runs were needed for these analytic arguments.

## 9. Bounded-profile physical synthesis and the infinite state chart

[BOUNDED_PROFILE_PHYSICAL_FLOWS.md](BOUNDED_PROFILE_PHYSICAL_FLOWS.md) resolves the actual bounded-profile flow gap without using RH reconstruction. The ambient unweighted period map K belongs analytically to ℓ¹ and factors quadratically through the full ℓ² Riesz correction Q. Its entire sequence derivative DQ:L²-pairs→ℓ²(𝒜) gives ||D_ab ΣcαKα||≤C||c||∞||Q||ℓ² and the corresponding compact-set tail estimate. The strong auxiliary L² pairing then gives a true gradient; the exact original ℬ bridge yields an unconditional E limit of the original physical fields. Their original Ω identities pass to the limit. Joint analyticity and vanishing at the background give ||Xc(x)||≤C||c||∞||x||, so bounded profiles have one common source radius, commute, and preserve actual spectral data. No inverse of the original weak form is used.

[INFINITE_TORUS_STATE_CHART.md](INFINITE_TORUS_STATE_CHART.md) combines those actual flows with the individual exact periods to construct a common continuous product-torus action. Infinite Haar averaging in the genuine state chart gives an analytic local state inverse with exact {Zβ±,Aα}=±δαβZβ± for ALL high indices simultaneously; finite residual data η are invariant under these high flows. Product-topology continuity is strong on individual states, not operator-norm continuity on derivatives. A full logarithmic chart, original weak symplectic normalization, invariant low completion, complete action inverse, and original-time action-only H still need proofs. These newest arguments are branch-internal analytic proofs; the full objective remains ACTIVE.

## 10. Invariant-base inverse and exact high action products

[INVARIANT_BASE_ACTION_INVERSE.md](INVARIANT_BASE_ACTION_INVERSE.md) proves that every Banach-valued analytic high-torus invariant descends to a holomorphic function of Iα=Zα+Zα− in an open ℓ¹ neighborhood and finite η. Applied to Jα=(Lωαγα)Aα, this gives J=F(I,η), D_IF(0)=Id and the actual parameter inverse I=G(J,η). The original Hamilton identity on each fixed locus forces Fα=Iαfα with a uniformly invertible ℓ∞ analytic multiplier. Thus U+=fZ+, U−=Z− is a genuine analytic state change with EXACT original Aα=Uα+Uα−/(Lωαγα), retaining the diagonal high flows. This is a high invariant-base inverse with η retained, not full action-only reconstruction or ordinary source submersion.

The remaining actual weak-form correction is closed, invariant, and annihilates every high generator upon contraction. Its removal still needs a valid weak range estimate. The common high fixed set is a finite analytic manifold with the restricted ORIGINAL symplectic form nondegenerate; its physical Fourier parametrization and translation equivariance imply spatial analyticity. It isolates the low sector but does not prove low spectral independence. Original-time H and full action–angle remain open; new proofs have not been independently reviewed.

## 11. Weak range criterion, without an unjustified Moser step

[WEAK_SYMPLECTIC_RANGE_CRITERION.md](WEAK_SYMPLECTIC_RANGE_CRITERION.md) proves a sufficient action-preserving analytic normalization theorem under the explicit factorization Δflat=A₀K with K analytic bounded and K(0)=0. For the actual reconstruction DR=Id+B, the precise sufficient derivative condition is the bounded analytic weighted adjoint Bsharp=A₀⁻¹B*A₀; then K=B+Bsharp+Bsharp B. This condition has NOT been verified for the actual DLW reconstruction, so the canonical gap remains open.

An explicit analytic horizontal perturbation dI₁∧dΣn≥2Iₙ with weights n⁻² has unchanged moments and a weakly nondegenerate interpolation, but its radial Moser equation fails in ℓ² at arbitrarily small states. A different primitive gives an explicit analytic action-preserving symplectic change, so the example is not a nonexistence theorem. It prevents the incorrect inference from geometric identities or an ordinary state diffeomorphism to radial range solvability. Five exact finite algebra checks passed in verify_weak_range.py / weak_range_validation.json; they do not verify the infinite analytic criterion for DLW. Full goal remains ACTIVE.

## 12. Original Liouville averaging closes the high canonical step

[SYMPLECTIC_LIOUVILLE_AVERAGING.md](SYMPLECTIC_LIOUVILLE_AVERAGING.md) uses the original CONSTANT physical Ω and the established actual compact spectral action. Average the pulled-back Euler fields W=∫DΦg⁻¹Φg dg, obtaining an analytic actual vector field W=x+O(x²), invariant under the group and satisfying L_WΩ=2Ω. Its negative flow contracts like e⁻ᵗ. The maps eᵗψt are exactly symplectic at every finite t and converge uniformly analytically, with derivative convergence, to a local invertible symplectic group-linearizing map. This avoids weak inversion entirely and does not require the preceding sufficient weighted-adjoint condition.

The resulting full general-field STATE chart has exact original weighted canonical high pairs, Aα=vα+vα−/(Lωαγα), and a finite constant symplectic low block. A simultaneous high logarithmic chart is supplied on an explicitly declared ℓ∞ relative domain about a nonzero profile, not falsely on an ℓ²-open logarithmic neighborhood. Five exact polynomial model checks pass (cumulative algebra count 32). Independent review remains outstanding. Low spectral completion at arbitrary high parameters, complete action-only original H, and its genuine time/frequency domain remain open, so the full objective stays ACTIVE.

## 13. Full nonzero-mode coverage on small nonzero backgrounds

[ALL_MODE_SMALL_BACKGROUND.md](ALL_MODE_SMALL_BACKGROUND.md) adds a nonempty fixed-M domain 0<|δ|/k₁<εM on which the common spectral construction works from n=1. Generator perturbation gives actual multiplier-template error O_M(Lδ²/|kn|), compared with separation O_M(L|δ|), and the full Born matrices satisfy Tn=T∞+O_M(|δ|/|kn|). Thus every nonzero mode has a uniformly invertible Born block and a common actual Riesz window after shrinking the source ball. The coefficient chart's explicit |δ|≤k₁/(128M³) budget is included; additional spectral budgets are retained in εM rather than guessed numerically.

Taking N=1 in the actual state inverse removes all low Fourier supplements; the original symplectic averaging then yields a full all-mode canonical state chart and action-only representation of source-analytic spectral invariants. This remains general infinite-dimensional field data, with a stronger background hypothesis. Arbitrary larger nonalias backgrounds still have the previous finite low gap. Original H's low-domain analyticity, original-time frequencies and trajectory domain require verification; full goal remains ACTIVE. No new computation is presented as a proof of these analytic estimates.

## 14. Original Hamiltonian and actual time on a spectral decay domain

[ORIGINAL_TIME_ACTION_FLOW.md](ORIGINAL_TIME_ACTION_FLOW.md) checks the original physical K on E: after periodic integration by parts, U∈L², w∈H¹ and wx∈L² make every term a continuous polynomial, with the original normalization retained. Smooth spectral commutation extends through actual action-flow continuity to E, so all-mode invariant descent gives K_B=k_B(J) without residual variables. Frequencies are Ωα=dα∂Jαk_B=O(n²). Spatial equivariance of the Liouville chart gives exact P(J)=Σ(−ikn/dα)Jα plus its background constant, and the physical formula K_B=K₀+2BP−2B²cMhL gives the original external translation term −2iknB(t).

The actual spectral trajectories vα±(t)=exp(±[tΩα⁰(J)−2ikn∫B])vα±(0) reconstruct the original Hamilton field on a small infinite-dimensional Gaussian spectral ball, with radius estimate ||v(t)||σ−C|t|≤||v(0)||σ for C|t|<σ. Smooth physical reconstruction follows from spatial equivariance; weak Hamilton uniqueness identifies the original PDE time. This is not rough-E Cauchy stability or an invariant bounded-angle chart. Coordinatewise continued angles are exactly linear for constant B, with the correct translation correction otherwise. Five new exact normalization checks passed (cumulative 37); they do not prove the analytic chain. The objective remains ACTIVE pending a full dependency/completion audit and repairs if needed.

## 15. Completion audit, first pass

[COMPLETION_AUDIT.md](COMPLETION_AUDIT.md) fixes twelve requirements before deciding completion and records their current evidence status. Re-read the actual finite graph minor and observability argument: it provides the LOCAL UNIQUENESS of physical constant-frame intersections required by the periodic return, not merely tangent transversality. Rechecked the time/spatial transport sign, the initial-projector exponential, rank-two sign gluing and finite-contour infinity limit. The full rational bridge and remaining infinite analytic/time chain still require audit closure.

New [audit_physical_born.py](audit_physical_born.py) computes directly with the original raw χ connection and original q,d Poisson tensor, using the independent-component m×m skew Δ shift. Its [floating-point results](physical_born_audit.json) cover M=2..5, signed n=±1,±2,±5, 60 actual collision labels and 720 phase-compatible brackets; maximum scaled discrepancy 5.81e−11. This is a separate computation path, not an independent reviewer or an analytic all-mode certificate. Keep its numerical evidence separate from the 37 exact algebra checks. Goal remains ACTIVE until the full audit and any needed repairs are finished.

## 16. Consolidated local theorem and completed internal dependency audit

[LOCAL_ACTION_ANGLE_THEOREM.md](LOCAL_ACTION_ANGLE_THEOREM.md) is now the current entry point. It states the full fixed-M small-nonzero-background result: an E-open original weak-canonical Cartesian state chart, actual reciprocal spectral actions, an explicit relative logarithmic chart, action-only original Hamiltonian and genuine original-time reconstruction on a small infinite-dimensional Gaussian spectral domain. The signed collision-label convention and physical conjugation are explicit; real leaves are not asserted to be compact tori.

The audit §§6–15 rechecks the dimension-free tensor identity, all-mode perturbation scale, full sequence derivative, compact-source tail convergence, common group domain, symplectic Liouville limit and Banach invariant descent. The final time pass verifies the original unweighted −1/16 bracket, polynomial continuity of K, smooth spectral commutation, exact external B momentum split, Gaussian-radius loss, spatial smoothness by translation equivariance, and PDE identification by original weak injectivity. The relative angle inverse is now written in an explicit ℓ∞ ratio norm. Analytic dependence in a fixed weaker Gaussian space requires a strict extra margin.

All twelve internal audit requirements have supporting arguments within the stated local domain. The delivered achievement is a constructive proof draft, not an independently reviewed theorem or a novelty claim. Larger backgrounds, zero background, rough-E Cauchy theory, global real tori, numerical evaluation of the nonlinear inverse and a certified numerical εM remain separate extensions. Existing 37 exact algebra checks and the separate 720 floating-point comparisons have not been relabeled as analytic proof. The HTML report and project-level index now point to the consolidated result; the main manuscript is unchanged.
