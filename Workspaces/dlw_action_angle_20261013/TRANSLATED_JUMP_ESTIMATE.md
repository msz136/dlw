# Actual bounded-profile jumps on one general-field neighborhood

2026-10-13. This supplies the missing actual-jump input to [UNIFORM_CAUCHY_ESTIMATE.md](UNIFORM_CAUCHY_ESTIMATE.md). It does not supply the physical reconstruction theorem. Proofs are internal to this branch and have not received independent full review.

## 1. Statement

Fix finite M, the original nonalias background, and the common physical source space E. Use the fixed disjoint circles Γα around the exact high background collisions, with a slightly wider collision-free annulus around each circle. Let s denote the spatial base point. In the full calibrated vector frame put

\[
J_\ell(H)=\tfrac12\{E_{ff}-\operatorname{diag}(0,P_\ell(H))\},
\qquad R_\alpha(s,\lambda;x)=W_\alpha(s,\lambda;x)-J_\ell(H(x)),
\]

where Pℓ(H) is the simple slow spectral projector and W is the actual half-difference of the two based monodromy projectors. No rank-two compression or frame derivative is omitted here. Define

\[
\mathcal Z_N=C(S^1_L;\ell^2_{\ell,|n|\ge N}(\mathcal A_{\rm ann})),
\]

where the annulus algebra uses the uniform matrix norm on its closure. Then, for N sufficiently large and a sufficiently small common physical ball,

\[
R:E\supset B_\varepsilon\longrightarrow\mathcal Z_N
\quad\text{is holomorphic},\qquad
\|R(x)\|_{\mathcal Z_N}\le b_N+C\|x\|_E,\quad b_N\to0.
\tag{1}
\]

The constant C can be chosen independently of N beyond a fixed cutoff. The statement on real fields is the restriction of this complexified statement. Importantly, the norm is sup_s of the ℓ² norm, not ℓ² of the spatial supremum.

For every fixed T<∞, every profile t∈ℓ∞ with ||t||∞≤T, define

\[
V_\alpha=e^{t_\alpha W_\alpha}e^{-t_\alpha J_\ell},\qquad
w_\alpha=V_\alpha-I.
\tag{2}
\]

Uniformly in the active label set, including countably many labels,

\[
\|w\|_{\mathcal Z_N}\le C_T(b_N+C\|x\|_E).
\tag{3}
\]

After choosing N and ε depending on T, the small-jump factorization exists at every s with uniform bounds in C(S¹;𝓗). It is holomorphic in x and t on the corresponding open domains. This conclusion concerns matrices over the spectral plane; it does not assert that all-label Hamiltonian flows exist in E.

## 2. Spatial translation gives the full based estimate

For any periodic L² potential z=(a,b,H), write τ_s z=(a(s+·),b(s+·),H). Translation is a bounded linear map

\[
z\longmapsto(s\longmapsto\tau_s z):
L^2\times L^2\times\operatorname{Mat}_m
\longrightarrow C(S^1;L^2\times L^2\times\operatorname{Mat}_m).
\tag{4}
\]

Strong continuity follows by density of smooth periodic functions; the norm bound follows from translation invariance of L². No differentiation of a rough potential is involved.

The full-monodromy duration-kernel theorem in [the high Riesz lemma, §§3–4](../dlw_recovery_20261011/general_m_actual_high_frequency_riesz_gap_lemma_20261011.md) gives a holomorphic ℓ²(𝒜)-valued remainder relative to diag(e^{Lλ},e^{LH}), locally uniformly Lipschitz on ambient coefficient balls. Its estimates hold on a slightly larger spectral disk before restriction to the annulus. Fixed circle centers cause no difficulty: λ=K_n+pℓ+eℓn+ζ with bounded eℓn, so evaluating the larger-disk analytic data at eℓn+ζ is a uniformly bounded map. Finite channels only alter constants.

The background (a₀,b₀,H₀) is spatially constant. Thus every τ_s z stays in the same ambient ball about that background. Applying the duration-kernel map pointwise in s, using its uniform holomorphic Taylor bounds, gives a holomorphic map into C_sℓ²(𝒜). This is stronger than separate coordinate analyticity and requires no uniform continuity on an infinite-dimensional bounded ball: local derivative bounds and the continuous translation path suffice.

For the actual fundamental solution, periodicity gives

\[
M_{\tau_s z}(\lambda)=Y_z(s,\lambda)M_z(\lambda)Y_z(s,\lambda)^{-1}.
\tag{5}
\]

Scalar trace normalization does not change projectors. Therefore the based projector obtained from translated potentials is exactly the W(s) used in the Hamiltonian gauge identity.

On the fixed annuli the uncoupled fast multiplier and the selected slow multiplier are uniformly separated from each other and from all other slow multipliers. Indeed the annuli stay away from the moving uncoupled collision after shrinking ||H−H₀||. The exponential has no other zero within the chosen spectral window. High tail smallness and the common perturbation budget preserve these separations for the full monodromy. Resolvent integration then gives the individual fast and slow eigenprojectors by uniformly bounded holomorphic matrix operations. At zero monodromy remainder these are Eff and diag(0,Pℓ(H)).

Consequently the half-projector difference minus Jℓ is holomorphic into ℓ²(𝒜ann), with a uniform Lipschitz bound. To see the sequence bound directly, the resolvent identity makes each correction bounded by its corresponding monodromy remainder; uniform Taylor bounds and the ℓ² multiplier-ideal inequality give strong analyticity. Compose with (4), then with the original analytic physical coefficient map. The background R is independent of s and belongs to ℓ²(𝒜ann), so its high tail bN tends to zero. The uniform Lipschitz bound gives (1). This also shows why a spatial maximal-Fourier estimate is unnecessary for this particular claim.

## 3. Exponentials and uniform small-jump factorization

The exact noncommutative difference formula is

\[
e^{tW}-e^{tJ}
=t\int_0^1 e^{(1-u)tW}(W-J)e^{utJ}\,du.
\tag{6}
\]

The uniformly bounded W and J give ||e^{tW}e^{-tJ}−I||≤C_T||W−J||. Apply this to each label before summing squares and taking sup_s. This proves (3) and, since ℓ² embeds in ℓ∞, the uniform boundary sup bound needed by the singular integral equation. Uniform exponential series also prove joint holomorphy in the ℓ∞ profile and x; every nonconstant difference contains one R factor.

Choose N,ε so that C₀C_T(b_N+Cε) is below the contraction and inverse-jump thresholds in the preceding Cauchy lemma. That lemma applies pointwise in s. Its Neumann solution is continuous in s and holomorphic in its Banach-space jump argument, hence yields

\[
\eta\in C(S^1;\mathcal H),\quad
\|\eta\|_{C_s\mathcal H}
\le\frac{C_0\|w\|_{C_s\mathcal H}}{1-C_0\|w\|_{C_s\ell^\infty L^\infty}},
\qquad F=I+C(w+\eta w).
\tag{7}
\]

The factors and inverse factors converge locally normally off the contours along finite exhaustive sets, uniformly in s. For the uniform-in-s assertion, the image of the continuous s-map in ℓ² is compact, so its sequence tails are uniformly small; the same applies to η(s). Thus the finite-exhaustion estimate from the Cauchy lemma holds in C_s𝓗. This is convergence for each fixed source and profile, not uniform convergence over an entire infinite-dimensional source ball.

## 4. The spatial equation after reference removal

The normalized jump in (2) is not an adjoint homogeneous solution for the same connection on both sides. With Cα=e^{−tαJℓ}, independent of s and λ within that patch, the exact identity is

\[
(V_\alpha)_s=\bar A_\lambda V_\alpha
-V_\alpha\bar A_\lambda^{C_\alpha},\qquad
\bar A_\lambda^{C_\alpha}=C_\alpha^{-1}\bar A_\lambda C_\alpha.
\tag{8}
\]

It holds in the spatial distribution sense for rough coefficients. It follows from W_s=[A,W], the exponential identity, and multiplication by Cα. Cα commutes with J* and the constant slow H, but generally not with a and b. Dropping this distinction would manufacture an incorrect connection reconstruction.

If F+=F−e^{tW}C, the original interior transport would be T_in=F+ C⁻¹, with exterior transport F−. Recovering the physical connection from these factors still requires spatial regularity and spectral growth estimates. Equation (7) alone gives neither an L² spatial derivative of the factors nor their required coefficient at λ=∞.

## 5. A precise obstruction to an unweighted reconstruction argument

There are arbitrarily small jumps in the established factorization class whose factors have no O(1/λ) expansion at spectral infinity. This is an insufficiency of the estimates, not a counterexample to DLW reconstruction.

Take circles centered at c_n=iκn, n≥N, of radius r<κ/3; set all other jumps to zero. Choose 1/2<p<1, a_n=εn^{−p}, and on the nth circle put

\[
f_n(\mu)=\frac{r a_n}{\mu-c_n},\qquad
w_n=f_n E_{12},\qquad E_{12}^2=0.
\tag{9}
\]

These jumps are smooth on every circle, have arbitrarily small ℓ²L² and ℓ∞L∞ norms, and determinant one. They may be taken independent of s, hence have arbitrarily strong spatial regularity. The exact factor and its inverse are

\[
F=I+C(f)E_{12},\qquad F^{-1}=I-C(f)E_{12}.
\tag{10}
\]

The jump identity follows from C+−C−=Id and E12²=0. For real R>0 outside all circles, residues give

\[
C(f)(R)=\sum_{n\ge N}\frac{ra_n}{i\kappa n-R},\qquad
-\operatorname{Re}C(f)(R)
=r\varepsilon\sum_{n\ge N}\frac{n^{-p}R}{R^2+\kappa^2n^2}.
\tag{11}
\]

The series is absolutely convergent. Restricting to R/κ≤n≤2R/κ proves −Re C(f)(R)≥cεR^{−p} for large R. Splitting the full sum at n≈R/κ bounds its modulus above by CεR^{−p}; hence F(R)→I but R||F(R)−I|| is unbounded. The first Cauchy moment Σra_n diverges. No F=I+F₁/R+o(R⁻¹) can hold.

Thus even determinant-one, spatially smooth small jumps and a genuine invertible Cauchy factor do not justify extracting the affine connection coefficient by the ordinary finite-contour expansion at infinity. Actual DLW jumps have the additional adjoint compatibility (8); the next proof must exploit that identity and the actual source structure to obtain a renormalized coefficient or an equivalent physical reconstruction estimate. This example does not show that (8) is insufficient, or that another reconstruction method cannot work.

## 6. Updated remaining target

The actual bounded-profile jump estimate and uniform countable matrix factorization now hold on a common general-field source ball. The remaining step is to show that those factors reconstruct the original affine connection in L², satisfy the finite physical graph constraints, and lift through the original state inverse to E with bounds independent of the active label set. Then one must still complete low spectral data, weak symplectic normalization, and original-time action-only evolution. The full research goal remains ACTIVE.

Subsequent update: [BOUNDED_PROFILE_PHYSICAL_FLOWS.md](BOUNDED_PROFILE_PHYSICAL_FLOWS.md) constructs the common physical bounded-profile flows directly from the full auxiliary period-map derivative and the exact original ℬ bridge. Thus RH reconstruction is no longer a prerequisite for the infinite flow/state-chart route. The specific RH affine-connection reconstruction discussed here is still not proved; its failure to follow from unweighted factorization remains relevant.
