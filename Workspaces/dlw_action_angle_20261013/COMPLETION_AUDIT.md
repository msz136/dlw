# Completion audit of the general-field action–angle chain

2026-10-13. This is a branch-internal audit, not an independent reviewer report. The internal pass is complete for the explicitly restricted local proof draft; see §15 and LOCAL_ACTION_ANGLE_THEOREM.md for the current disposition. Earlier prospective paragraphs record the audit chronology. Numerical checks calibrate specific algebra only.

## 1. Requirements fixed before deciding completion

The user requests a general-field, general-fixed-M construction with the original physical Poisson/symplectic structure, actual reconstruction and original time, on an explicitly stated domain. The current candidate theorem uses small NONZERO uniform backgrounds and an open balanced field neighborhood for Cartesian coordinates; its logarithmic chart uses a declared relative topology, and actual original-time solutions use an infinite-dimensional Gaussian spectral domain. None of those domains is a finite soliton or Fourier truncation. The candidate does not cover arbitrary larger nonalias backgrounds or rough-E Cauchy well-posedness.

Completion requires more than the existence of the latest theorem files:

| Requirement | Authoritative dependency | Audit state |
| --- | --- | --- |
| Correct original fixed-mean source and physical inverse | Original free-field Poisson map; physical holonomy/state inverse | Original affine bracket and polynomial reconstruction rechecked in §§2,12 |
| Actual commuting spectral Hamiltonians and exact reciprocal weight | Rational gauge/trace bridge; RECIPROCAL_PERIODS | General matrix-unit identity, contraction sign and finite correction rechecked in §6 |
| Exact nonlinear single-label periods | PERIODIC_SPECTRAL_FLOWS | Transport, sign, gluing and physical uniqueness argument rechecked below |
| All-mode separation and true state inverse on a nonempty fixed-M domain | ALL_MODE_SMALL_BACKGROUND; actual Riesz and augmented-state lemmas | Analytic scaling and common source budget rechecked in §7; no explicit final numeric εM asserted |
| Bounded-profile original physical flows | BOUNDED_PROFILE_PHYSICAL_FLOWS | Full sequence derivative, compact-set tails and original Hamilton limit rechecked in §8 |
| Common infinite group and analytic inverse | INFINITE_TORUS_STATE_CHART | Uniform domains, germ extension, strong continuity and invariant saturation rechecked in §9 |
| Original weak canonical normalization and exact actions | SYMPLECTIC_LIOUVILLE_AVERAGING | Averaged actual vectors and norm-convergent analytic derivative limit rechecked in §10 |
| Complete invariant action dependence | INVARIANT_BASE_ACTION_INVERSE; no low block at N=1 | Banach-target invariant descent and topology rechecked in §11 |
| Original Hamilton normalization and external B(t) | ORIGINAL_TIME_ACTION_FLOW; original physical Hamiltonian | Source normalization, continuous polynomial extension and exact B split checked in §12 |
| Actual general-field reconstruction and original-time solution domain | ORIGINAL_TIME_ACTION_FLOW | Gaussian bound, smoothness and original weak identity checked in §13 |
| Genuine angle variables with an honest topology | SYMPLECTIC_LIOUVILLE_AVERAGING §6; ORIGINAL_TIME_ACTION_FLOW §6 | Relative inverse in §11; coordinatewise time lift and full labels clarified in §14 |
| Reviewable final theorem, report, limitations and reproducibility | LOCAL_ACTION_ANGLE_THEOREM; HTML report; proof sources and validation artifacts | Consolidated branch-internal proof draft supplied; evidence limits in §15 |

The status “to review” is not a finding that the assertion is false, but it is not completion evidence either. No full success claim is made at this stage.

## 2. Physical coordinates and the finite-frame uniqueness used by periodicity

Re-read the original free-field inverse and the physical holonomy/state inverse, §§1, 5, 6, 8. In the formula Δ_first=q+S+Ad_first, A is the m×m skew sign matrix on the INDEPENDENT components. It is not the full M×M sign matrix applied to all d. This convention makes Δ=0 on the stated uniform background and agrees with the original inverse b_j−b_m. The affine skew shift preserves the original derivative bracket; it is not a change to an auxiliary Poisson tensor.

At the background the constant GL_m orbit tangent is (q₀X,−Xr₀,[H₀,X]). All of its components are spatial constants. The physical graph tangent has zero variations in the finite mean/H components. Simple H₀ and q₀Pℓr₀≠0 force this orbit tangent to vanish only for X=0. Select an m²-output minor of the finite graph constraints with an invertible derivative in X. The parameter inverse-function theorem for C(zQ)=0 then gives a UNIQUE nearby Q for each physical z; Q=Id is already a solution. Therefore a nearby constant frame transform of physical data lying again in the same graph must be trivial. This is stronger than merely counting transverse tangent dimensions, and is precisely what the periodicity proof needs.

The period proof also bounds the final frame transform near Id via its K equation. Alternatively the actual observability matrix recovers Q from the two endpoints and forces it near Id when both endpoints are near the same background. The finite gauge argument does not classify arbitrary λ-dependent gauges; that stronger statement is neither used nor implied here.

## 3. Recheck of the exact single-index return argument

The sign convention δA=G_s−[A,G] gives the actual time/spatial intertwining equation T_s=A(t)T−TA(0) for T_t=G(t)T, T(0)=Id. The spectral-projector adjoint transports as W(t)=T_out W(0)T_out⁻¹. Since G_in−G_out=W(t), differentiating T_out⁻¹T_in gives the constant coefficient W(0), hence T_in=T_out exp(tW(0)). No time-dependent projector was mistakenly exponentiated as a constant.

At 2πi, exp(2πiW)=Id−2Π because the two selected eigenvalues of W are ±1/2. The total rank-two projector Π extends THROUGH the branch disk, even though the individual eigenlines need not. Multiplying the interior factor by (Id−2Π)⁻¹ produces an entire matrix matching the exterior factor. Its finite-contour exterior Cauchy generator has K+O(1/λ), so its limit at infinity is the spatially constant block frame solving Udot=KU. Finite-contour Liouville is legitimate here; the later infinite-contour counterexample is not used to infer any asymptotic expansion.

The common single-index analytic field bounds and vanishing at the background give existence along the full imaginary-time loop after a uniform radius reduction. The K bound simultaneously makes the endpoint frame small enough for §2. Thus the last step from frame conjugacy to actual physical return is supported by the stated source theorem, not an assumed inverse from spectral classes.

This recheck does not independently rederive the full rational R-tensor bridge; that remains a declared input needing its own audit closure.

## 4. A distinct direct computation of the original background pairs

New script [audit_physical_born.py](audit_physical_born.py) starts from the raw constant χ generator Aχ=i t P+δ sign and the original q,d coefficient derivatives. It solves actual signed generator collisions numerically and contracts the resulting rank-one Born covectors directly with J=−offdiag(D)/16. The left-hand computation does not call or implement the reciprocal-field or previously asserted norming-bracket formula.

The expected comparison is {Γα+,Γβ−}=δαβωαγα/L, with all cross-label and matching-phase possibilities checked when their spatial Fourier phases can pair. Independent q,d gradients include the m×m Δ shift from §2; this tests a convention that a vector-frame-only calculation could overlook.

For M=2,3,4,5, δ=1/(512M³), L=2π, and signed n=±1,±2,±5, the [saved output](physical_born_audit.json) contains 60 collision labels and 720 nontrivial bracket comparisons. Maximum scaled bracket error is 5.81×10⁻¹¹; maximum collision residual is 1.78×10⁻¹⁵. Positive-mode balanced Born matrix condition numbers range from about 4.27 to 25.05 in these samples.

These values support the factor L, sign, original pole weight and reflected-channel cancellation, including n=1. They do NOT prove an all-M/all-mode bound, a source radius, the nonlinear period theorem, or the small-background εM budget. The chosen test δ is not advertised as a numerically certified value of the final theorem's εM. The existing 37 exact algebra checks and these floating-point comparisons must be reported separately.

## 5. Next audit pass

The next pass must examine the analytic all-mode estimates, bounded-profile synthesis and common infinite group, then the original symplectic limit and original-time reconstruction. If any dependency fails, affected downstream conclusions must be marked conditional or repaired before a final completion claim. The current evidence is substantive progress but is not yet a passed full completion audit.

## 6. Actual all-M trace bridge: inspected source identity

Re-read spectral_independent_review_20261011.md §§16.3–16.5 and the rational physical bridge, together with the vector-frame correction proof §§3–5. The general identity pairs C+=R+B/2 with the FIRST connection and C−=R−B/2 with the second. Its matrix-unit reduction is dimension-free: the remaining row terms contain Θ(i,j,k)=1−sij sik−sik sjk+sjk sij, which vanishes for distinct indices and for exactly two equal indices, and equals one only when all three coincide. The two resulting Kronecker terms cancel. Thus the stated all-M identity has analytic algebra behind it; it is not inferred from the M=3..5 samples.

The original bracket contraction followed by periodic integration by parts makes the trace bracket an integral of an exact spatial derivative. The gauge residue is −ω(μ)W⁰, with ω=(S²−μ²)/(16S); this is the sign used by the reciprocal-period Cauchy generator. In the vector frame the principal λ coefficient is fixed. The λ-independent correction must commute with J*, then its diagonal equations and the nonalias condition make it spatially constant. The full H variation is a commutator, not an artificially frozen holonomy. The selected finite constraint minor determines the correction, while density of smooth physical states passes the unused constraints to the whole low chart. These are precisely the conditions used by ℬ; an arbitrary auxiliary tangent is not presumed physical.

## 7. All-mode small-background estimates

Rechecked the scale hierarchy in ALL_MODE_SMALL_BACKGROUND. For fixed M, the slow generator gap is |δ| times a fixed positive gap; the fast/slow generator separation is at least a fixed fraction of |kn|. The Schur-complement correction is O(δ²/|kn|), so slow eigenvector corrections are O(|δ|/|kn|). Near λ=ikn+pℓ+O(δ), ALL exponentiated generator eigenvalues are within O(L|δ|) of the identity multiplier. Consequently the eigenbasis conjugation error has the additional factor L|δ|, giving O(Lδ²/|kn|), not merely O(|δ|/|kn|).

This improvement is needed: its ratio to multiplier separation O(L|δ|) is O(|δ|/|kn|), uniformly small from n=1 when |δ|/k₁ is small enough. The same estimates keep the exact collision shifts inside the δ-sized windows, the roots away from ±S, and the slopes nonzero. The all-frequency Born derivative is then a uniform perturbation of the fixed invertible slow-basis map. The original coefficient derivative's explicit small-δ bound may be imposed simultaneously.

All constants are allowed to depend on fixed M and on the chosen nonzero δ. The source ball is subsequently chosen by continuity of the full ℓ² ambient monodromy map, with a δ-dependent common budget. This order avoids an unjustified uniform limit at δ=0 and avoids a countable intersection of source balls. The theorem has an existential positive εM; neither the coefficient-chart bound alone nor the floating-point test δ is a certified numerical replacement for all spectral budgets.

## 8. Bounded-profile synthesis and the physical limit

The needed hypothesis is the ambient holomorphic Q map into ℓ² of analytic matrix functions, proved by the full duration-kernel/Riesz construction. Its derivative is an operator into the FULL sequence space. Quadratic vanishing of the unweighted period functional gives

||D_ab ΣcαKα||≤C||c||∞||Q||ℓ²,

and restricting the sum to a tail replaces Q by that tail. This provides the strong auxiliary L² gradient and an unconditional field sum for every bounded profile. Individual field-norm bounds alone would not suffice.

The tail estimate is uniform on compact source sets, not arbitrary source balls. The ODE convergence proof compares against the compact image of a fixed limiting orbit, with a profile-uniform Lipschitz bound; this is sufficient and correctly avoids assuming derivative-tail operator convergence. Joint analyticity of the complete gradient map independently gives uniform field derivatives. The original Ω identity passes from finite physical sums, so the resulting field is in the original source chart with every physical graph constraint retained. No weak inverse of arbitrary covectors is used.

## 9. Common group, continuity and the state average

For each bounded angle cube, Gronwall gives one source radius for simultaneous flows and their two-step compositions. The finite composition/period identities hold initially as germs; both sides extend holomorphically to that common connected ball, so identity continuation extends the equality without multiplying the available radius by the number of labels. Bounded coordinatewise profile convergence then proves the infinite identities. The compact cube quotient produces product-torus continuity on individual states; uniform Lipschitz bounds give joint source continuity.

Saturating a sufficiently small open ball by these uniformly controlled local biholomorphisms produces an OPEN invariant neighborhood, rather than an unproved open countable intersection. The linear representation is strongly continuous on ℓ² with uniform norm bounds; no operator-norm continuity is claimed. Haar integration of the uniformly bounded holomorphic state maps has derivative Id by its uniform quadratic remainder, so its ordinary analytic inverse is legitimate. That average alone is not claimed symplectic.

## 10. The actual symplectic limit

The Liouville construction averages DΦg(x)⁻¹Φg(x) as vectors already in E. Fixed-vector derivative continuity follows from directional Cauchy integrals; uniform analytic bounds also control inverse derivatives on a smaller ball. Thus the vector-valued average is holomorphic even though the group representation need not be continuous in the operator norm. Its derivative is Id, and its Lie derivative of the ORIGINAL CONSTANT Ω is exactly 2Ω.

The negative flow estimate gives ||ψt(x)||≤2e⁻ᵗ||x||. Hence the limit eᵗψt has a uniform exponentially small tail on a complex ball. Cauchy estimates give operator-norm convergence of its derivative on smaller balls. This is the derivative convergence needed to pass the EXACT finite-time identity (eᵗψt)*Ω=Ω to the limit. The nonlinear group-equivariance remainder also decays like e⁻ᵗ, yielding conjugacy to the linear representation. The limit has derivative Id and an actual local inverse. This proof does not infer Moser range solvability from weak nondegeneracy; the earlier range failure example remains consistent with it.

## 11. Invariant descent and a concrete relative angle norm

For invariant Banach-valued holomorphic functions, restrict each homogeneous Taylor term to finite coordinate subspaces. Independent torus characters force balanced powers, hence a polynomial in Iα=vα+vα−. Square-root lifts bound its norm by C^k||I||₁^k. Polarization extends each polynomial from finite sequences to ℓ¹, with the same diagonal bound; the normally convergent sum gives a holomorphic invariant-base function. This is a Banach-target argument, not separate scalar analyticity. With N=1 there is no residual finite parameter. It can therefore be applied to the original scalar Hamiltonian once that functional's E analyticity is checked.

The relative angle topology is now stated without relying solely on the phrase “transported topology”: write aα=vα+/vα*,+−1, bα=vα−/vα*,−−1 with norm ||a||∞+||b||∞. On a small ball the exact inverse variables are ρα=(1+aα)(1+bα)−1 and ϑα=½log[(1+aα)/(1+bα)]. Banach-algebra logarithm/square-root series give mutually inverse analytic maps on smaller balls. The source subset is not E-open, and no bounded E inverse to division by a vanishing reference sequence is asserted. The canonical Cartesian chart itself IS E-open and still provides the physical state inverse.

The original Hamiltonian/time-domain audit and final theorem synthesis remain to be completed. No independent review is claimed for this second internal pass.

## 12. Original Hamiltonian and normalization: final internal pass

Re-read GENERAL_PERIOD_FREE_FIELD_POISSON §§1–2: the source-to-(q,d) map is affine because the common U component cancels; the unweighted bracket is exactly −offdiag(D)/16. Its inverse divides only by fixed S, and gives U∈L², w∈H¹. Periodic integration by parts changes ∫wUₓ to −∫wₓU. Each original K term is therefore a continuous polynomial on E. The constant Ω above has i_XΩ=dK with this bracket and no time rescaling.

The original CONSERVATION_FAMILY_VERDICT records K=−8G C₁+(γ/c)P+constant, G=hMc/4. The actual trace/action bridge includes commutation with defined local Cⱼ on smooth fields, not just formal pairwise commutation of Cⱼ. Smooth persistence under the bounded spectral flows and continuity of K then extend its invariance to E. With all modes present, invariant descent applies to K itself.

Directly substitute U=U⁰+2B, γ=2Bc into K. The change in its nondifferentiated integrand is 2BU⁰w+2B²w−2BcU⁰−4B²c. Summing uses ΣU⁰w=0, Σw=Mc and ΣU⁰=−Σps/c. This gives 2BP−2B²cMhL. Derivative terms are unchanged. Thus the B-dependent vector field is exactly 2B times negative translation; differentiating the reconstruction retains 2B_t in U. The five saved algebra checks calibrate this calculation but are not the proof of analytic invariance.

## 13. Time, spatial regularity and physical identification

On a smaller ℓ¹ ball, Dk₀ is bounded in ℓ∞. Multiplication by dα gives at most quadratic frequency growth. For real B, its translation factor has modulus one, so the Gaussian estimate follows componentwise and then by summing nonnegative terms. A strict margin σ−CT>0 bounds every polynomial frequency weight and the time derivative in ℓ². For analytic dependence into a fixed weaker Gaussian space choose a STRICTLY positive additional margin and a slightly smaller initial ball; no endpoint-radius analyticity is inferred merely from a pointwise bound.

The canonical inverse is spatially equivariant. Composition with the infinitely differentiable translation orbit of v(t) proves that its physical image has every spatial derivative in E. This yields classical smooth fields uniformly on smaller closed time intervals. Since vdot lies in ℓ², contracting the actual canonical form gives dK against every ℓ² test vector; Cauchy–Schwarz and Dk∈ℓ∞ justify the sum. The original smooth derivative-Poisson vector has the same contraction. Injectivity of the original form on the fixed-mean leaf identifies the two vectors. This checks the original PDE, not only spectral conservation.

No rough-E existence or continuous-dependence theorem follows. The original time domain is the preimage of the stated Gaussian spectral ball and is not E-open.

## 14. Full labels, reality and angles

The final theorem explicitly retains the full signed collision-label convention and its conjugation pairing. A real positive Fourier mode of 2m physical fields has 4m real degrees of freedom. Negative labels may be reconstructed by reality on the real slice, but they must not be discarded as independent coordinates on complexification. The phrase “positive modes and reflected partners” in earlier notes is read with this convention.

The canonical inverse commutes with physical conjugation; the original real Hamiltonian therefore preserves its fixed locus by the uniquely specified coordinatewise flow. This does not imply that each complex action or angle is individually real, or that all real directions are circular. Continued coordinatewise logarithms give the exact angle evolution. A family of local relative charts describes points along the Cartesian orbit, but does not imply that the orbit is continuous in one bounded-relative-angle norm. The period lattice obstructs the suggested n⁻² weighted injective logarithm chart.

## 15. Internal audit outcome

[LOCAL_ACTION_ANGLE_THEOREM.md](LOCAL_ACTION_ANGLE_THEOREM.md) consolidates the precise local result and proof dependencies. All twelve requirements have a branch-internal argument on the additional small nonzero background domain. The original research objective is met at the level of a constructive local proof draft, with an actual state inverse and a specified infinite-dimensional original-time domain. It is not a claim of an independently validated published theorem.

Unfinished extensions are stated separately: larger backgrounds and their low modes, singular zero background, global tori, rough-E Cauchy theory, certified numerical radii, priority research, and numerical computation of the nonlinear canonical inverse. None is silently included in the local theorem. The saved 37 algebra checks and separate 720 floating-point pairings remain calibration evidence only. Earlier “next pass” paragraphs above are the audit chronology; this section is its current disposition.
