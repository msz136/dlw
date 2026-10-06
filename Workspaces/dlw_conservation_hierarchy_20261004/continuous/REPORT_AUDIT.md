# Independent mathematical audit of report.src.html

Audited file: `../report.src.html`, read 2026-10-04. The source was not edited in this audit.

## Verdict

The mathematical conclusions are supported by the current derivations, with the small scope/rendering clarifications listed below. The report correctly distinguishes the formal periodic theorem from the original nonperiodic line-wave baselines, and it does not claim Liouville completeness from the Lax structure.

## Specific corrections recommended

1. Equations (7) and (20) contain literal `qquad` instead of `\qquad`. This is a rendering/source correction.
2. The first independence example p=(1,2,−3)cos x in §4 is specifically N=3. Add this explicitly. The subsequent four-parameter witness is N=3,h=4,G=6,T=12, with fixed sitewise x averages. State the concluding four-functional independence on **that fixed Casimir leaf's open neighborhood**, rather than leaving room for an arbitrary-N reading. The family is pairwise commuting for general N, but the present rank certificate is N=3.
3. In §6, R→∂y⁻¹ means the inverse on zero-mean periodic transverse functions. The inverse-monodromy normalization has a finite nondegenerate formal limit **when the limiting G remains nonzero**; G_h≠0 for each h alone does not prevent a singular limit G_h→0.
4. The continuous Riccati q₄,q₅ identifications are after normalization and removal of full divergences: −32∫q₄=3Q₄|β=0 and −64∫q₅=Q₅|β=0. Add “经归一化并去除全散度后” to avoid reading them as literal same-coefficient density equalities.

## Checks that pass

### Original periodic phase and explicit heat potential

Equations (1)–(3) are consistent with the earlier Hamilton theorem. In particular the mean drift is λ=2D\bar e/c, and V=RDw/2−hDw/4−\bar e/c+v₀ gives ΔV=hDw/2. Substitution makes the sum of the two full intertwining residuals zero; the difference is the w equation. Consequently the periodic monodromy construction applies to the reconstructed original SD flow. It does not require an unrelated global tau assumption.

### Q₄ and Q₅

Equations (4)–(7) pass the variational and skew/mRB checks. The exact identity Π(Q₄)_U=2\bar e uses both DΠ(Uw)=0 and D²Πw=0, which are present on the stated leaf. Its extra drift is an x derivative. Translation invariance gives the claimed commutation with P_mom.

The q₅ formula agrees with the direct certificate. The full canonical bracket vanishes only instantaneously on the derivative mean-constraint manifold, as the report explicitly states. The full canonical closure generally leaves that manifold. The correction −8hN∫\bar e²/c is therefore essential for the original reduced flow; the report does not promote the bare-Q₅ calculation to a false trajectory theorem. The Q₅/Q₄ general pairwise bracket and their general monodromy deduplication are not claimed.

Independently reran `direct/check_q5_structure.py`: the linear-A polynomial is exactly zero, the local residual's two Euler derivatives vanish, and differentiation of its explicit primitive agrees exactly.

### Infinite generator and involution

The Laurent inverses require G≠0 for P−1, whereas each D−b_j inverse merely requires its already monic leading symbol. No sitewise w_j≠0 assumption is needed. The factor recursion (12), normalization recursion (13), residue flux (14), and densities (15)–(17) are correct.

The raw-field derivative convention in §5 gives factor kernels −D/8 and D/8, hence raw trace Adler scale 1/8. The product and inverse signs are correct. X_n commutes with P, so the trace bracket vanishes by an actual cyclic calculation. Its Hamiltonian vectors preserve p₁,p₂ because [Q_-,P−1] has order at most −3.

The common-U scalar gauge leaves residues pointwise invariant. Thus ΣδI_n/δU_j=0, and the restricted-gradient shear vanishes for these trace functionals. This transfers their involution to the existing J_red without attempting to invert the constant mode of periodic D. It is not a claim that a general full Dirac reduction equals J_red.

### General-N low-order deduplication

The BCH order argument is correct: C_j=log S_j has order −1, first commutators have order at most −3, and nested commutators at most −5. Through order −4, only single-site and pair terms occur. The pair coefficients and the triangular R primitive give the stated general-N p₃,p₄ relations, hence equation (18).

Independently reran `lax/verify_monodromy_hierarchy.py`: 25 exact checks pass, including single-site logarithms, pair-commutator primitives, low residues, normalization coefficients, residue fluxes and Q₄ comparison. Therefore the general-N statement in equation (18) is supported; it is no longer merely an N=3 inference.

### Independence

Independently reran `lax/verify_fixed_leaf_independence.py`: the four variations change only cosine amplitudes and preserve every reduced field's x average. Its exact Jacobian determinant is

411796986221479423/4426355198361600000≠0.

The tested [Σ∫U,H₀,I₂,I₃] span is equivalent to [P_mom,K,Q₄,I₃] on that leaf: Σ∫U is affine in P_mom, H₀=K+γhΣ∫U, and equation (18) gives a nonzero triangular Q₄ coefficient. Thus the four-functional conclusion is justified at N=3. No infinite-family independence is inferred.

### Continuous limit and original baselines

The limit h→0,Nh→Y>0 and the first-order expansion (22) are correct. The correct continuous spatial sign is (D−U/2)ψ_y=−wψ/4. The Riccati recursion (23) follows from both logarithmic spatial equations and the heat equation. Open-chain primitives require compatible common modes; periodic y cannot arbitrarily zero them. The report states that distinction.

The transmission moments (24) and one-soliton coefficients (25) are correct. Their signs agree with the four numerical entries for all three benchmark rows. Vandermonde independence applies to the finite spectral-parameter family with distinct endpoints, not to an infinite physical Poisson hierarchy.

The nonzero single-site C_n repeat at all lattice sites for the selected exact backgrounds. Consequently their proposed full hΣ∫ total diverges. The report correctly refrains from assigning periodic traces to the nonperiodic relative Hamilton space, or claiming finiteness in perturbation neighborhoods from exact-soliton checks alone.

## Overall scope

With the four clarifications above, the report gives a coherent formal periodic conservation/involution theorem, explicit fourth and corrected fifth charges, a four-charge independence witness at N=3, and exact nonperiodic spectral benchmarks. It leaves global Liouville completeness, infinitely many independent traces, and the common nonperiodic relative hierarchy explicitly open.
