# Analytic invariant descent and a weighted high-action inverse

2026-10-13. This continues the [common infinite torus state chart](INFINITE_TORUS_STATE_CHART.md). It proves an analytic inverse on the high invariant base, with the finite low residual variables retained, and a Cartesian normalization of the exact high actions. It does not prove a canonical weak symplectic chart or a full original-time action–angle theorem. The proofs and their earlier dependencies remain subject to independent full review.

## 1. An invariant analytic-function theorem with a Banach target

Let Z=(Z+,Z−) belong to ℓ²(I)⊕ℓ²(I), let η belong to a finite-dimensional complex space, and let the product torus act by

\[
(Z_\alpha^+,Z_\alpha^-,\eta)
\mapsto(e^{i\theta_\alpha}Z_\alpha^+,e^{-i\theta_\alpha}Z_\alpha^-,\eta).
\tag{1}
\]

For any complex Banach space B, every B-valued holomorphic invariant f near (0,0) factors uniquely, on smaller neighborhoods, as

\[
f(Z,\eta)=\widehat f(I,\eta),\qquad
I_\alpha=Z_\alpha^+Z_\alpha^-,\qquad I\in\ell^1.
\tag{2}
\]

Here fhat is holomorphic on an OPEN neighborhood in ℓ¹×Cᵈ, not merely a coordinatewise function on the image of a particular source. The product map ℓ²⊕ℓ²→ℓ¹ is continuous quadratic.

Proof. Choose a product neighborhood ||Z||₂<R, ||η||<r on which ||f||B≤M; shrink from the original domain if needed. Expand in Z, with η as a parameter. On any finite coordinate subspace, invariance under each independent circle forces a Taylor monomial to contain equal powers of Zα+ and Zα−. Thus all odd homogeneous terms vanish, and the degree-2k term P2k(Z,η) is a degree-k polynomial pk(I,η) on finitely supported I. These polynomials agree as finite coordinate sets increase.

For such I choose any complex square roots and set Zα+=Zα−=sqrt(Iα). Then ||Z||₂²=2||I||₁ and

\[
\|p_k(I,\eta)\|_B
\le M R_1^{-2k}(2\|I\|_1)^k
\quad (R_1<R),
\tag{3}
\]

by the Cauchy bound for the homogeneous Taylor polynomial on the Z ball of radius R1. The square-root choice is only a device to bound a polynomial; no analytic square-root section is assumed. The polarization formula bounds the associated k-linear map on the dense space of finite sequences, so it extends continuously to ℓ¹. The diagonal estimate (3) passes to the extension. Hence Σpk(I,η) converges normally for 2||I||₁<R1² and defines a B-valued holomorphic map. Joint holomorphy in η follows by the same uniform bounds and its ordinary parameter Cauchy estimates. Finite truncation and continuity give (2) for all Z in a smaller ball.

Every sufficiently small I has a square-root lift in that ball, proving uniqueness. The claim concerns invariant analytic FUNCTIONS. Products do not distinguish every torus orbit: in particular they identify different zero-product configurations, and compact torus orbits need not contain the square-root lift.

## 2. Apply the theorem to the actual weighted periods

In the actual infinite state chart write the original reciprocal actions as Aα(Z,η). They are invariant under (1), because they commute with all high generators. The established map A has values in ℓ¹₂. Define fixed nonzero constants and normalized actions

\[
d_\alpha=L\omega_\alpha\gamma_\alpha,\qquad
J_\alpha=d_\alpha\mathcal A_\alpha,
\quad |d_\alpha|\asymp\langle n\rangle^2.
\tag{4}
\]

This is a bounded isomorphism between the weighted action sequence space and ℓ¹. It changes the coordinate used for the invariant base, not the original Poisson tensor or time. The Hamiltonian generating unit high flow remains Aα=Jα/dα.

Apply §1 with B=ℓ¹. There is a genuine holomorphic map

\[
J=F(I,\eta):\ell^1\times\mathbb C^d\longrightarrow\ell^1.
\tag{5}
\]

The exact quadratic normalization Aα^[2]=να+να−/dα and the identity derivative of the averaging chart imply

\[
F(0,0)=0,\qquad D_I F(0,0)=\operatorname{Id}_{\ell^1}.
\tag{6}
\]

This is an operator identity, not only equality on coordinates: the descended map is already holomorphic into ℓ¹ and finite sequences are dense. It follows that (I,η)↦(F(I,η),η) is locally biholomorphic once the remaining derivative assertions below are included. The statement is about invariant-base variables; the physical source-to-action derivative is still not an ordinary unweighted Hilbert submersion.

## 3. Fixed loci force coordinatewise divisibility

The high generator in state coordinates is

\[
X_{\mathcal A_\alpha}
=Z_\alpha^+\partial_{Z_\alpha^+}
-Z_\alpha^-\partial_{Z_\alpha^-}.
\tag{7}
\]

On the linear locus Zα+=Zα−=0 this vector field vanishes. The ORIGINAL Hamilton identity therefore gives dAα=0 there. Restrict to the connected intersection with a small coordinate ball: Aα is constant on that locus and its value is zero at the origin. No inversion of Ω is used in this argument.

For every sufficiently small (I,η) with Iα=0, take the square-root lift from §1, with both α coordinates zero. This shows

\[
F_\alpha(I,\eta)=0\quad\text{whenever }I_\alpha=0.
\tag{8}
\]

In particular F(0,η)=0 and DηF(0,0)=0, completing the triangular derivative needed for the parameter inverse-function theorem. There are open neighborhoods on which

\[
\boxed{\quad I=G(J,\eta)\quad}
\tag{9}
\]

is an actual holomorphic inverse in ℓ¹, with η retained. This is the weighted HIGH-action inverse on the invariant base, not a full action-only inverse or a state reconstruction from actions alone.

Moreover (8) gives

\[
F_\alpha(I,\eta)=I_\alpha f_\alpha(I,\eta),\qquad
f_\alpha=\int_0^1\partial_{I_\alpha}F_\alpha
(I+(t-1)I_\alpha e_\alpha,\eta)\,dt.
\tag{10}
\]

On a smaller ℓ¹ ball, all modified arguments in (10) stay in the original ball. The derivative bound for F gives a uniform bound for fα; uniform Cauchy estimates for further derivatives give a norm-convergent holomorphic Taylor series into ℓ∞. Thus f:ℓ¹×Cᵈ→ℓ∞ is holomorphic. Equations (6) and (10) imply f(0,0)=1 as an ℓ∞ identity. Shrink the domain so

\[
\|f(I,\eta)-1\|_\infty<\tfrac12.
\tag{11}
\]

This is a UNIFORM divisor normalization over all high indices. It does not follow from separate scalar inverse theorems.

## 4. Exact Cartesian products for the original actions

In the actual state coordinates make the analytic change

\[
U_\alpha^+=f_\alpha(I,\eta)Z_\alpha^+,
\qquad U_\alpha^-=Z_\alpha^-,\qquad \eta'=\eta.
\tag{12}
\]

The ℓ∞ multiplier bound makes this an analytic map on the ℓ² state space; its derivative at 0 is the identity. The analytic inverse function theorem supplies a true state inverse. More explicitly, from U take Jα=Uα+Uα−, recover I=G(J,η), then Z−=U− and Z+=U+/f(I,η); (11) controls that division. Therefore no summability or reconstruction condition has been hidden in the coordinate change.

All fα are invariant under the high torus, so (12) preserves its diagonal action. The ORIGINAL physical actions now have exact product form

\[
\boxed{\quad
\mathcal A_\alpha=\frac{U_\alpha^+U_\alpha^-}{d_\alpha},
\qquad
\{U_\beta^\pm,\mathcal A_\alpha\}
=\pm\delta_{\alpha\beta}U_\beta^\pm,
\qquad\{\eta_j,\mathcal A_\alpha\}=0.
\quad}\tag{13}

Reality is inherited: reflected actions, dα and coordinate products obey the original conjugation identities. Uniqueness in the invariant descent and (10) make f obey the same identities. The asymmetric choice in (12) is thus compatible with the physical real subspace; it is not asserted to be canonical.

The vanishing Aα=0 is equivalent to Uα+Uα−=0 on this neighborhood. It does NOT imply that both factors vanish or that the corresponding generator is zero. This distinction matters at singular action levels.

## 5. What the normalization says about the weak symplectic form

Let ΩU be the actual pushed-forward original form, and let Ωlin=ΩU(0) be its constant extension. The background pairings and the identity derivative of (12) give its high part

\[
\Omega_{\rm lin,high}
=\sum_\alpha d_\alpha^{-1}dU_\alpha^+\wedge dU_\alpha^-.
\tag{14}
\]

The finite low part is the original background restriction in η. There are no high/low cross terms at the background: torus invariance forces a bilinear pairing between nontrivial and trivial characters to vanish. The exact background high pairing fixes the coefficients in (14). The series defines the original weak weighted form, not a strong unweighted replacement.

Set Δ=ΩU−Ωlin. Both forms are closed and invariant under the high torus. By (13), for every α,

\[
\boxed{\quad\iota_{X_{\mathcal A_\alpha}}\Delta=0.\quad}
\tag{15}
\]

Indeed contracting either form gives d(Uα+Uα−/dα). Thus the remaining nonlinear correction is horizontal to ALL high period generators, vanishes at the background, and is invariant. This is a constraint on the actual remaining symplectic problem, not a proof that Δ=0. Nor does it by itself imply a bounded Moser field: solving against (14) can introduce the unbounded factors dα≈n².

For example Ωlin+b dI₁∧dI₂, with any fixed scalar b and two high labels, has the same high moment maps and invariance, but its correction is nonzero. It is still weakly nondegenerate: if its contraction with v is zero, evaluation on each high generator gives dIα(v)=0; the extra term then has zero contraction, leaving Ωlin(v,·)=0 and hence v=0. This explicit family shows why the product identities alone cannot identify the whole symplectic form.

## 6. Spectral completeness within the high invariant algebra

Every actual trace F_r(λ), at each fixed admissible λ, is analytic on the source ball and commutes with the high action flows. By §1 and (9) it has a local representation

\[
F_r(\lambda)=\mathcal F_{r,\lambda}(J,\eta).
\tag{16}
\]

The same applies to any other analytic invariant on this low source domain. This local representation is unique on the invariant-base neighborhood. Consequently the remaining analytic invariant information beyond the normalized high actions is carried by the finite residual η, although (16) does not prove which functions of η are spectral invariants or whether the spectral classes separate η.

The original DLW Hamiltonian and original time have their own regularity/domain requirements. If a Hamiltonian extends holomorphically to this source neighborhood and commutes with all high actions, this theorem gives H=h(J,η); it does not give h(J) alone. No such low-domain extension for the actual original H is added as an assumption-free conclusion here.

The remaining full task is now more precise: normalize the horizontal weak-form correction with valid range estimates, complete the finite low spectral invariants, establish a full action–angle domain including the appropriate relative topology at nonzero profiles, and recover the original-time evolution there. The full objective remains ACTIVE.

## 7. The intrinsic finite low fixed manifold

The common fixed set of the high torus is, in the genuine state chart,

\[
\mathcal C=\{U^+=U^-=0\}.
\tag{17}
\]

It is a finite-dimensional analytic embedded submanifold parametrized by η. It is much smaller than the level set of zero high actions, which also includes one-sided nonzero coordinate configurations. At a point of C, the differential torus representation splits the tangent space into its finite trivial η component and the high nontrivial character components. Invariance of ΩU forces their cross pairing to vanish: average any high tangent vector over the product torus, obtaining zero, while the low vector stays fixed.

If a low tangent v annihilates every low tangent under ΩU, it therefore annihilates every high tangent as well. Original weak nondegeneracy implies v=0. Since the low space is finite-dimensional,

\[
\boxed{\quad\Omega|_{\mathcal C}\text{ is an ordinary nondegenerate finite-dimensional symplectic form}.\quad}
\tag{18}
\]

It is the restriction of the original form, with no invented bracket. This identifies the remaining low sector geometrically but does not establish enough commuting spectral functions on it.

The points of C are spatially analytic, after shrinking its neighborhood. Here is a direct justification using the actual physical Fourier coordinates. The high action flows commute with spatial translation, so their fixed set C is translation-invariant wherever these local charts are defined. The exact high Born inverse shows that T₀C consists precisely of the physical nonzero Fourier modes with |n|<N. Let Plo be the bounded physical Fourier projection onto these modes. Its restriction to C has invertible derivative at 0. Thus C has an analytic finite-dimensional parametrization R(ξ), uniquely characterized by PloR(ξ)=ξ, on a small low-mode ball.

Real spatial translation T_s is isometric on E, preserves C, and obeys PloT_s=D_sPlo, where D_s is the finite Fourier phase matrix. Shrinking once so the relevant orbit remains in the parametrization domain, uniqueness yields

\[
T_sR(\xi)=R(D_s\xi),\qquad s\in\mathbb R/L\mathbb Z.
\tag{19}
\]

For ξ in a smaller ball, D_sξ stays in the complex parametrization domain for a uniform strip |Im s|<σ, since only finitely many Fourier frequencies occur in D_s. The right side of (19) is holomorphic and bounded there. Taking Fourier coefficients of this E-valued translation orbit gives exponentially decaying physical spatial Fourier modes. Consequently R maps a smaller finite-dimensional ball analytically into every fixed spatial Sobolev space, with uniform bounds from any smaller strip.

This regularity allows finite-jet physical Hamiltonians and spectral quantities to be restricted to C without imposing extra rough-field definitions. It still does not prove their Hamiltonian evolution is complete, that the restricted spectral functions are independent, or that this finite core supplies all missing actions. The target remains the full general-field neighborhood with its infinitely many high degrees of freedom; C isolates only the residual task.
