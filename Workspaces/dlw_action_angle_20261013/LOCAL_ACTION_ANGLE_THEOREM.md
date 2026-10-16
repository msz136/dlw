# Local general-field action–angle theorem for semi-discrete DLW

2026-10-13. Consolidated branch-internal proof draft. The dependency audit is recorded in [COMPLETION_AUDIT.md](COMPLETION_AUDIT.md). This is not an independent review or a claim of established novelty. Earlier research notes record intermediate, superseded open questions; the scope below is the current synthesis.

## 1. Hypotheses and physical phase space

Fix any finite lattice period M≥2, spatial period L>0 and h>0. Put m=M−1, kₙ=2πn/L, δ=hc/8 and S=Mδ. There exists εM>0 such that the construction below applies when

    0 < |δ|/k₁ < εM.

The source radius depends on the chosen nonzero δ. The coefficient bound εM≤1/(128M³) is only one of the required budgets; no numerical value certifying all spectral budgets is asserted.

Use the original mean closure Σwⱼ=Mc, ΣUⱼwⱼ=2McB, and fix the component spatial means at their uniform-background values. With q,d the original independent free fields, the centered, complexified source is

    E=(L²₀)^m × (H¹₀)^m,
    Jphys=−offdiag(∂ₓ Iₘ)/16,
    Ω(ξ,η)=−16∫[(∂ₓ⁻¹ξq)·ηd+(∂ₓ⁻¹ξd)·ηq]dx.

The real source is the fixed locus of physical conjugation. The finite lattice period does not truncate the infinitely many x modes. B may be a prescribed real C¹ function of original time.

The index α runs over the complete signed collision labels (ℓ,n), 1≤ℓ≤m, n≠0, with the reflected-label reality identifications of the physical Born chart. One must retain that full label convention on complexification: a real positive Fourier mode of the 2m physical fields has 4m real degrees of freedom. Reflection is a reality relation, not permission to discard half the independent complexified data.

## 2. Canonical Cartesian coordinates and exact actions

There is an analytic local state isomorphism x↦v=(v⁺,v⁻) between E-open neighborhoods of the background and zero in the corresponding full ℓ² pair space. It has an analytic inverse, respects physical conjugation and spatial translation, and satisfies

    Ω=Σα dα⁻¹ dvα⁺∧dvα⁻,
    Aα=dα⁻¹vα⁺vα⁻,
    dα=L ω(λα) γα,       |dα|≍〈n〉²,
    ω(λ)=(S²−λ²)/(16S).

Here λα is the exact background fast/slow multiplier collision, γα=∂λ(yfast−yslow)(λα), and the action is the actual original spectral functional

    Aα=(2πi)⁻¹∮Γα [½log(μα,+/μα,−)]/ω(λ) dλ.

The sheets and logarithm continue the background labels on the isolated annulus; the contour encloses the selected pair of branch points and avoids ±S. The form series converges on ℓ² tangent pairs. Its weights tend to zero; it is the original weak form, not a strong Hilbert symplectic form. There is no finite residual coordinate on this small-background domain.

With i_XH Ω=dH, the exact identities are

    {vα⁺,vβ⁻}=δαβdα,
    X_Aα=vα⁺∂vα⁺−vα⁻∂vα⁻,
    {Aα,Aβ}=0.

At every state where all pairs are nonzero, each finite action block is independent. This does not assert that the full action derivative is a surjection in the E topology. Real dynamics can contain dilation directions; this is not a theorem that all real invariant leaves are compact tori.

## 3. Simultaneous local logarithms

Fix v* with every factor nonzero. In small relative variables (ρ,ϑ)∈ℓ∞⊕ℓ∞,

    vα±=vα*,±√(1+ρα) exp(±ϑα),
    Aα=Aα*(1+ρα),
    Ω=Σα Aα* dϑα∧dρα.

The relative source norm is ||v⁺/v*,⁺−1||∞+||v⁻/v*,⁻−1||∞. Writing these two ratios minus one as a,b, the inverse is ρ=(1+a)(1+b)−1 and ϑ=½log((1+a)/(1+b)). Banach-algebra series give an analytic inverse. Thus {ϑα,Aβ}=δαβ and the angles mutually commute.

This relative neighborhood is not E-open. The Cartesian chart is E-open and remains regular when individual pairs vanish. Logarithmic action–angle coordinates are singular there. The displayed complex coordinates restrict through the inherited real structure; they are not assumed to be real circular angles individually.

## 4. Original Hamiltonian and original time

Set Jα=vα⁺vα⁻=dαAα∈ℓ¹. The original Hamiltonian, with its unscaled normalization, has an analytic representation K_B=k_B(J). If P is the original negative-translation momentum, then

    P=P(0)+Σα(−ikₙ/dα)Jα,
    K_B=K₀+2BP+scalar(B),
    να(J)=dα∂Jα k₀(J),       |να(J)|≤C〈n〉²

on a smaller action ball. The exact original-time formula is

    τα(t)=tνα(J)−2ikₙ∫₀ᵗB(s)ds,
    vα±(t)=exp(±τα(t))vα±(0),       J(t)=J(0).

For σ>0 use ||v||σ²=Σα exp(2σ〈n〉²)(|vα⁺|²+|vα⁻|²). On any fixed interval |t|≤T with CT<σ, sufficiently small initial data in this Gaussian Hilbert space obey

    ||v(t)||σ−C|t| ≤ ||v(0)||σ.

They stay in the canonical neighborhood and reconstruct smooth solutions of the original physical equations, including the explicit 2B(t) contribution to U. Reality-compatible initial data reconstruct real fields. This is an infinite-dimensional class permitting every spectral channel to be nonzero.

Coordinatewise continued logarithms satisfy θα(t)=θα(0)+τα(t). For constant B these are affine functions of original time. The entire curve need not lie in one ℓ∞ relative-angle chart. The single-valued Cartesian formula supplies the trajectory; no injective logarithm chart in the norm sup|θα|/n² is claimed.

## 5. Proof chain

1. The exact free-field inverse preserves the original derivative Poisson tensor. The actual full-monodromy Riesz construction and physical finite-frame inverse give analytic state data, not only spectral classes.
2. [ALL_MODE_SMALL_BACKGROUND.md](ALL_MODE_SMALL_BACKGROUND.md) proves uniform separation and invertibility from n=1: multiplier errors O(Lδ²/|kₙ|) are small relative to gaps O(L|δ|). All nonzero modes are covered by one source ball.
3. [RECIPROCAL_PERIODS.md](RECIPROCAL_PERIODS.md) cancels the exact physical pole weight. [PERIODIC_SPECTRAL_FLOWS.md](PERIODIC_SPECTRAL_FLOWS.md) proves the nonlinear period 2πi using rank-two projector gluing and local uniqueness of the physical frame.
4. [BOUNDED_PROFILE_PHYSICAL_FLOWS.md](BOUNDED_PROFILE_PHYSICAL_FLOWS.md) controls the whole sequence derivative of the actual monodromy blocks. [INFINITE_TORUS_STATE_CHART.md](INFINITE_TORUS_STATE_CHART.md) constructs the common compact spectral action. Tail convergence on compact source sets suffices; uniform operator-norm tail convergence is not presumed.
5. [SYMPLECTIC_LIOUVILLE_AVERAGING.md](SYMPLECTIC_LIOUVILLE_AVERAGING.md) averages actual pullbacks of the Euler field. Its contracting flow gives a limit of exactly symplectic maps, with derivative convergence and an analytic inverse. Moment-map uniqueness gives the exact action products. This step never inverts the weak form on arbitrary covectors.
6. [INVARIANT_BASE_ACTION_INVERSE.md](INVARIANT_BASE_ACTION_INVERSE.md) descends analytic invariants to ℓ¹ products. [ORIGINAL_TIME_ACTION_FLOW.md](ORIGINAL_TIME_ACTION_FLOW.md) checks continuity of the original Hamiltonian, its normalization and momentum split, and the Gaussian time estimate. Translation equivariance gives smooth physical reconstruction. Pulling back i_vdotΩ=dK and using weak injectivity identifies the original PDE.

## 6. Evidence and remaining research

The branch-internal audit covers the above dependency chain and records its analytic arguments. Thirty-seven exact finite algebra checks and a separate direct physical Born audit (60 collisions, 720 floating-point pairings) support specified normalizations only. They do not certify the analytic theorem. No independent full review, literature priority determination, quantitative final εM, or numerical implementation of the nonlinear canonical inverse has been completed.

The local theorem does not cover δ=0, all larger nonalias backgrounds, arbitrary component-mean leaves, rough-E Cauchy well-posedness, global real invariant tori or global-in-time physical trajectories. These are further problems, not consequences of the local construction. The delivered result is a reviewable constructive proof draft with explicit state, angle and time domains.
