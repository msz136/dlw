# Bounded spectral profiles give actual original-field flows

2026-10-13. This closes the bounded-profile field-synthesis gap by using the entire auxiliary period map before taking its gradient. It does not use an unproved inverse of the original weak symplectic operator, or a spectral factor's expansion at infinity. This is a branch-internal analytic proof, subject to independent full review.

## 1. Inputs and ambient extension

Use the original physical chart E, analytic coefficient map x↦z=(a,b,H), and the bounded analytic operator ℬx from [the established field bridge](../dlw_recovery_20261011/general_m_gap_frequency_weighted_hamilton_sequence_20261011.md), §3. In particular, for every individual reciprocal period,

\[
X_{\mathcal A_\alpha}(x)=\mathscr B_xY_{\mathcal K_\alpha}(z),
\quad
\mathcal K_\alpha(z)=\frac1{2\pi i}\oint_{\Gamma_\alpha}\kappa_\alpha(\lambda,z)d\lambda.
\tag{1}
\]

Y is the auxiliary canonical L² pair field with the complete H held fixed only when differentiating K. The physical field includes the actual H and frame changes through ℬ. Formula (1) is the exact reciprocal-weight cancellation proved in [RECIPROCAL_PERIODS.md](RECIPROCAL_PERIODS.md).

The full Riesz construction extends to an open AMBIENT neighborhood of (a₀,b₀,H₀) in

\[
\mathcal X=L^2(\mathbb C^{1\times m})\oplus L^2(\mathbb C^{m\times1})\oplus\operatorname{Mat}_m(\mathbb C).
\]

This is an available input, not an extension inferred from a function on the physical submanifold: the duration-kernel and Riesz estimates were first proved on that ambient space in the [high-frequency lemma, §§3–4](../dlw_recovery_20261011/general_m_actual_high_frequency_riesz_gap_lemma_20261011.md). On a smaller ambient ball the moving-grid compressed corrections satisfy

\[
Q:\mathcal X\supset V\longrightarrow\ell^2(\mathcal A_r),
\quad Q\text{ holomorphic},\qquad
\|D_{a,b}Q(z)\|_{\mathcal L(L^2\oplus L^2,\ell^2(\mathcal A_r))}\le C.
\tag{2}
\]

This operator bound into the WHOLE sequence space is essential. Bounding each coordinate derivative separately would lose the result below.

The unweighted contour period is invariant under translating the spectral grid. Dividing both multipliers by the moving scalar does not change their ratio. Consequently

\[
\mathcal K_\alpha(z)=k(Q_\alpha(z)),\qquad
k(0)=Dk(0)=0,
\quad |k(q)|\le C\|q\|^2,\quad\|Dk(q)\|\le C\|q\|.
\tag{3}
\]

Here k is a uniformly bounded holomorphic functional on the same small analytic-matrix ball. Its quadratic vanishing follows by integrating the template variation ½(e^{−Lζ}q₁₁−q₂₂), holomorphic throughout the disk. Fixed and moving contours define the same unweighted period by deformation inside the common branch-free annulus. Thus K:V→ℓ¹ is genuinely holomorphic.

## 2. Sum first, then take the L² gradient

For c∈ℓ∞ define Kc(z)=ΣcαKα(z). This is jointly holomorphic in z and c. With H fixed in the auxiliary derivative, for any L² pair h,

\[
|D_{a,b}K_c(z)h|
\le C\|c\|_\infty
\sum_\alpha\|Q_\alpha(z)\|\|(D_{a,b}Q(z)h)_\alpha\|
\le C\|c\|_\infty\|Q(z)\|_{\ell^2}\|h\|_2.
\tag{4}
\]

In the complex L² pair space, the bilinear integral pairing identifies its continuous complex dual with an L² pair by a bounded COMPLEX-LINEAR isomorphism. This is not the antilinear Hilbert-gradient convention. Write the differential as ∫(g_a h_a+g_b h_b), with row/column contractions understood. The auxiliary canonical field is Yc=(g_b,−g_a). It is an actual analytic L² pair, not a distributional or formal sum.

For every set S of labels, (4) gives the stronger tail estimate

\[
\boxed{\quad
\|Y_{c1_S}(z)\|_2
\le C\|c\|_\infty\|1_SQ(z)\|_{\ell^2}.
\quad}
\tag{5}
\]

Therefore finite sums ΣcαY_Kα converge unconditionally in L² to Yc for every fixed z. Convergence is uniform for z in compact subsets of V and c in bounded ℓ∞ sets, since continuous images of compact sets in ℓ² have uniformly small tails. It is NOT asserted uniform on an arbitrary ambient ball. Nor do the derivative tails generally converge in operator norm.

This last distinction is necessary: already a diagonal model Yα(z)=zαeα has vanishing vector tails for each z∈ℓ² but tail derivative norm one. The previous ℓ²(L²) estimate for the family of fields could not by itself prove (5); the joint sequence derivative in (2) supplies the missing cancellation.

## 3. Original physical synthesis and Hamilton identity

Define

\[
X_c(x)=\mathscr B_xY_c(z(x)),\qquad
\mathcal H_c(x)=\sum_\alpha c_\alpha\mathcal A_\alpha(x).
\tag{6}
\]

Both are jointly analytic in x and c; A∈ℓ¹₂ in particular makes Hc a scalar analytic functional for every bounded c. Finite sums in (6) are EXACTLY the original Hamilton fields by (1). Formula (5) and bounded ℬ give unconditional E convergence, locally uniformly on compact source sets. For each fixed x and test v∈E, scalar derivative convergence follows either from the analogous weighted version of (4), or from the absolute ℓ¹ pairing with DA(x)v. Passing to the limit in the finite original identity yields

\[
\boxed{\quad d\mathcal H_c(x)v=\Omega(X_c(x),v).\quad}
\tag{7}
\]

Thus the limit is an ORIGINAL physical Hamilton field. Although ℬ applied to an arbitrary auxiliary tangent need not satisfy every physical constraint, this particular limit is the limit of genuine physical fields. In addition x is the physical source coordinate itself; the ODE below stays in its original chart. No missing graph constraint is imposed by assertion.

At the uniform source, Y_Kα=0 for every α. One way to verify this is to diagonalize the constant background generator on each disk: first variations of the log multipliers are the diagonal averages of the coefficient variation in that analytic eigenbasis, hence holomorphic through the collision, and their unweighted contour integrals vanish. The same statement was used in the individual-period proof. Equation (5) then gives Yc(z₀)=0 and Xc(0)=0. Joint analytic bounds on a smaller source ball imply

\[
\|X_c(x)\|_E\le C\|c\|_\infty\|x\|_E,
\qquad
\|D_xX_c(x)\|\le C\|c\|_\infty.
\tag{8}
\]

These constants do not depend on the number of active labels. This does not contradict weak symplectic compactness: c↦Xc(x) has small tails for fixed x, while the differentiated family at x=0 contains all mode projections. No unweighted action submersion follows.

## 4. Genuine flows, limits and preservation

For every finite T, choose rT>0 so that e^{CT}rT remains inside the preceding source ball. Analytic Banach ODE and (8) give the real-parameter path

\[
\frac{dx}{du}=X_c(x),\quad0\le u\le1,
\quad\|c\|_\infty\le T,\quad\|x(0)\|_E<r_T,
\tag{9}
\]

with a uniform source radius and ||x(u)||≤e^{CTu}||x(0)||. Complex coefficients encode complex Hamiltonian times; the evolution parameter u in this argument is real.

If c_j are uniformly bounded and converge coordinatewise to c, then X_cj→X_c uniformly on every compact source subset: split finitely many coordinates from the remainder and use (5). Compare the c_j orbit with the fixed c orbit, whose image is compact, and use the common Lipschitz bound (8) in Gronwall. This proves convergence of the actual flows, uniformly in u for each initial source. No operator-norm convergence of derivative tails is required. The same argument is uniform over compact sets of initial sources.

Finite truncations preserve all actual trace classes; their E continuity passes this to (9). Reality follows for conjugation-compatible profiles. Spatial translation equivariance is inherited from the individual physical Hamiltonians and the convergent field sum. For a smooth initial source, differentiate its translation orbit through the analytic flow: all derivatives exist in E in the same low-norm time window, proving smooth persistence. Consequently all defined local spectral densities are preserved as well, using smooth approximation or their original differential identities on these smooth paths.

For bounded c,d, finite sums and (7) show Ω(Xc,Xd)=0. Closedness of Ω and the Hamilton identities imply that [Xc,Xd] has zero contraction with Ω; its injectivity forces [Xc,Xd]=0. Hence the actual local bounded-profile flows commute wherever their compositions are defined.

## 5. Consequence and scope

For imaginary profiles c=iθ with ||θ||∞≤2π, (9) gives precisely the previously missing common source radius for all finite simultaneous phase flows and their countable limits. It accomplishes physical reconstruction directly by an original-field ODE; an independent RH reconstruction theorem is unnecessary for this step. Existing single-index 2πi periods can now be combined with these bounds to study a common infinite torus action and averaging chart.

Still outstanding are a full action/invariant inverse, elimination or spectral completion of the finite low residual data, weak symplectic normalization of the nonlinear coordinates, and the original Hamiltonian's action-only expression on its actual time domain. The full goal remains ACTIVE.
