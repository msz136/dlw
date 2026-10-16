# Independent audit: vector AKNS matched H¹ state inverse

2026-10-11. Reviewed the full final text of [the matched-kernel proof](vector_akns_twisted_h1_state_inverse_recovery_proof_20261011.md), including its added sample convolution (4a)–(4b), and the full [underlying framed L² proof](vector_akns_framed_l2_state_inverse_recovery_proof_20261011.md). No numerical or symbolic checks were run. No main proof, shared log, or shared index was edited.

**Verdict: PASS for the stated local framed H¹/h¹ state inverse for each fixed finite m, with general complex matrix H.** The first jet subtraction is also correct as a forward C²-input statement. The document does not establish an H² inverse, an all-order smooth chart, an inverse from conjugacy classes/actions, or original DLW Hamilton completeness.

## 1. Actual kernels, calibration, and sample coordinates

The preceding L² proof identifies its duration kernels with the absolutely convergent actual Volterra/Dyson series. Its fiber measure includes the coarea factor, and the bound uses the exact mass τʳ(L−τ)ʳ/(r!)². The new proof works with those kernels, so its correction is an operation on actual framed data rather than a formal asymptotic definition.

The right multiplication for U and left multiplication for V in (2) remove the zeroth-path twists exactly. The two matrix orders are necessary and correct. H is recovered from the complete raw low-data inverse; the proof correctly does not extract H from C alone.

With positive-exponential samples yₖ, the inverse Fourier representation is K(τ)=L⁻¹∑ₖyₖe⁻λₖτ. Multiplication by e⁻ᴴ⁽ᴸ⁻τ⁾ therefore gives exactly (4b), including its n−k index and its left/right order. Formula (4a) gives the claimed resolvent expression when invertible and the entire continuation when singular. Fourier truncation followed by bounded L² multiplication proves ℓ² convergence without an ℓ¹ coefficient assertion.

The higher-path endpoint values vanish because their exact fiber masses vanish and their continuous input products are uniformly bounded. The factorial majorant permits summation at the endpoints. Thus (5) and the matched periodic values follow. For H¹ kernels, integration by parts gives (5a); the derivative Fourier coefficient tends to zero, so the leading raw 1/n tails and the failure of raw h¹ when the endpoint numerator is nonzero are valid.

## 2. H¹ tame estimate

The affine duration coordinates give every transition-time derivative in [−1,1]. The slow-fraction derivatives have total absolute value 1. Differentiating the ordered H exponentials and the final correction therefore costs at most 2‖H‖e²ᴸ‖ᴴ‖; this uses submultiplicativity and does not commute H through the row/column products.

For differentiated inputs, the coarea/Cauchy bound remains applicable with the bounded affine coefficient. It produces (8). For r≥2, the squared extra factor for division by τ is controlled by sup τʳ⁻²(L−τ)ʳ/(r!)²≤L²ʳ⁻²/(r!)², and the reflected argument handles L−τ. Hence (9) and its r-weighted Jacobian estimate hold.

I independently checked the two r=1 path orders and changes of variables. For the upper path, t₁=t, t₂=t+s, t₃=σ+s with σ=L−τ. For the lower path, t₁=t, t₂=t+s, t₃=τ+s. These give the displayed integrals exactly. In the upper /τ estimate, the first a is bounded in L∞ and the t-integral uses L²×L² Cauchy–Schwarz; for /σ, the last a is bounded in L∞ and the s-integral uses Cauchy–Schwarz. In the lower estimates, use b(t) in L∞ for /τ and b(τ+s) in L∞ for /σ. This verifies (11) and handles the r=1 singular Jacobian terms omitted by the r≥2 argument.

After summation, every differentiated-input term has one H¹ factor and 2r low L² factors. The r=1 Jacobian term has coefficient O(R²), and the remaining factorial series is bounded by CR²eᶜᴿ². This proves (6), including the essential allowance of a large H¹ norm inside a small L² ball. Multilinear difference bounds and smooth approximation identify the obtained H¹ derivative with the weak derivative of the actual L² kernel. Normal convergence supplies the asserted H¹ holomorphy.

## 3. The common low domain and high inverse

The vacuum derivative (12) is a bounded isomorphism on both the L² and H¹ levels. The finite matrix remainder C−LH has no constant or linear term, including when a,b are present. Its quadratic low bound gives the finite-factor part of (13), while (6) gives an O(ε²) coefficient for the pair. One source radius ε can therefore ensure both low contraction and q₁<1/2.

For a sufficiently small low target ball, iteration (14) stays in that source ball and converges in X₀. A target in Y₁ makes each iterate periodic H¹. The one-sided estimate (13), without an H¹ contraction assertion, suffices for the uniform bound (15). Since X₁ is Hilbert (with a finite matrix factor), weak subsequential compactness and the already known strong X₀ limit identify the inverse as an X₁ element. Periodicity is preserved by weak closedness of the trace-matching subspace. This proves inverse regularity throughout V₀∩Y₁.

The holomorphic upgrade is also valid. Here the restrictions of L² test functionals are norm-dense in the H¹ dual: in Fourier coordinates this is the density of finite sequences in H⁻¹. Uniform local H¹ bounds make the corresponding scalar holomorphic approximations converge uniformly on compact complex-line discs. Weak line holomorphy plus local boundedness gives H¹-valued holomorphy. The inverse branch κ(V₀), explicitly confined to the chosen low ball, avoids any global-preimage assertion.

Consequently (16) and its Fourier form (17) are genuine restrictions of one low chart, with no high-norm-dependent source radius. The proof keeps m fixed, retains H as a finite complex variable, and imposes no normality or eigenvalue-gap hypothesis.

## 4. General matrix endpoint jets and the next-order limit

The scalar constant-potential series (18) follows directly from the same exact fiber mass. Only r=1 contributes to its endpoint first derivatives, giving (19). Its nonzero derivative jump yields a 1/n² tail, so this example lies in h¹ and fails h² even though its source is smooth.

The general matrix formulas (21)–(22) have the correct order. Dividing the upper r=1 kernel by τ at τ↓0 gives a₀eᴴᴸQᴴe⁻ᴴᴸ after the right twist; dividing by σ at σ↓0 gives ca₀. The analogous lower limits after the left twist give Qᴴb₀ and cb₀. The derivatives at L acquire a minus sign because σ=L−τ. Higher r paths have zero first endpoint derivatives, and the r=0 derivative jumps vanish for C² periodic sources. These facts verify (22), including its noncommuting conjugation term.

Since B₂(0)=B₂(1) and the derivative difference of B₂(τ/L) is 2/L, (23) removes precisely those first derivative jumps while preserving equal values. C² inputs therefore yield periodic H² corrected kernels and h² samples. The proof correctly limits this to a forward statement: a₀,b₀ are not continuous low-L² functionals, so these jet coefficients do not yet define a low-L² analytic coordinate change or a same-domain H² inverse.

No mathematical defect was found in the stated result. The remaining dependencies are the all-order inverse/compatibility argument, original physical-image transfer, and the class/action Hamilton completeness problem; none is supplied by the framed H¹ theorem.
