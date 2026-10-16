# Original weak symplectic normalization: a range criterion and a radial failure example

2026-10-13. Continue from [exact high action products](INVARIANT_BASE_ACTION_INVERSE.md). This note proves a sufficient analytic normalization theorem, identifies the precise derivative estimate needed to apply it to the actual state inverse, and shows why the ordinary radial construction cannot be inferred from the geometric identities alone. The sufficient estimate is NOT yet proved for the DLW inverse. This is internal research, not an independent review.

## 1. The actual remaining problem

In the established Cartesian state chart u=(U+,U−,η), the original high actions and their vector fields are

\[
A_\alpha=w_\alpha U_\alpha^+U_\alpha^-,\quad
w_\alpha=(L\omega_\alpha\gamma_\alpha)^{-1},\quad
X_\alpha=U_\alpha^+\partial_{U_\alpha^+}-U_\alpha^-\partial_{U_\alpha^-}.
\]

The actual pulled-back physical form is Ω=Ω₀+Δ, where Ω₀ is its constant background value, with high block Σwα dUα+∧dUα− and the finite nondegenerate low block. We know

\[
d\Delta=0,\quad\Delta(0)=0,\quad
\Delta\text{ is torus invariant},\quad\iota_{X_\alpha}\Delta=0.
\tag{1}
\]

Let A₀:E→E* be A₀v=Ω₀(v,·). It is bounded and injective, but its inverse on its range is unbounded in the ordinary dual norm. Analyticity of Δ as a bounded two-form therefore does not imply that A₀⁻¹Δflat exists on all E, or is bounded.

Expressions df(XA) used for the new coordinate functions are legitimate even before df has its own Hamilton field. They must not be used to assert that every coordinate differential lies in the weak Hamiltonian range.

## 2. A sufficient analytic theorem preserving the actual actions

Suppose, in addition to (1), that on an open E ball there is an analytic operator map K(u)∈L(E) such that

\[
\Delta_u(v,z)=\Omega_0(K(u)v,z),\qquad K(0)=0.
\tag{2}
\]

This is a factorization through the ORIGINAL weak form, not merely a bound in L(E,E*). Shrink the ball so sup||K||<k<1. Then there exists a local analytic diffeomorphism φ tangent to the identity, commuting with the high torus and preserving EVERY Aα, such that

\[
\boxed{\quad\varphi^*\Omega=\Omega_0,\qquad A_\alpha\circ\varphi=A_\alpha.\quad}
\tag{3}
\]

Proof. On a star-shaped ball the radial homotopy gives the analytic one-form

\[
\beta_u(z)=\int_0^1 t\Delta_{tu}(u,z)\,dt,\qquad d\beta=\Delta.
\tag{4}
\]

By (2), β=A₀B with B(u)=∫₀¹tK(tu)u dt. In particular B=O(||u||²) is an E-valued analytic vector field. Put Ωs=Ω₀+sΔ. Then Ωsflat=A₀(Id+sK), and

\[
V_s(u)=-(\operatorname{Id}+sK(u))^{-1}B(u),\quad0\le s\le1,
\qquad\iota_{V_s}\Omega_s=-\beta.
\tag{5}
\]

Uniform Neumann bounds and V_s=O(||u||²) give an actual analytic nonautonomous Banach ODE flow on a sufficiently small ball for the entire s interval. Cartan's formula yields

\[
\frac d{ds}\varphi_s^*\Omega_s
=\varphi_s^*(\Delta+d\iota_{V_s}\Omega_s)=0.
\]

The radial primitive is invariant, because the torus acts linearly and preserves Δ. It is horizontal: for t>0, Xα(tu)=tXα(u), so (1) makes the integrand βu(Xα(u)) zero; the endpoint follows by continuity. Since i_XαΩs=dAα for every s, evaluating (5) on Xα shows dAα(V_s)=0. Thus the flow preserves all Aα. Uniqueness of (5), using injectivity of Ωsflat, also makes V_s and its flow torus equivariant. At s=1 this gives (3). Compatible real structures are preserved throughout if the input forms have them. No strong-symplectic theorem has been invoked. ∎

This theorem addresses the full weak-form normalization, including the finite low block; low spectral completeness and the original-time Hamiltonian would still require separate proofs even if (2) were verified.

## 3. A concrete test on the actual inverse derivative

Identify the original physical coordinates linearly with the new background coordinates, so the original constant physical form is Ω₀. Let R be the actual analytic state reconstruction from the current u coordinates to those linear physical coordinates, with R(0)=0 and DR(0)=Id. It already exists from the preceding state inverses. Then

\[
\Omega_u(v,z)=\Omega_0(DR(u)v,DR(u)z).
\tag{6}
\]

Write DR=Id+B. Define the symplectic adjoint Bsharp, if it exists as a bounded operator, by

\[
\Omega_0(B^\sharp v,z)=\Omega_0(v,Bz),
\qquad B^\sharp=A_0^{-1}B^*A_0.
\tag{7}
\]

Here B* is the Banach transpose, not a replacement inner-product pairing. If Bsharp is an analytic L(E)-valued map with Bsharp(0)=0, then (6) gives the exact sufficient factorization

\[
\boxed{\quad K=B+B^\sharp+B^\sharp B.\quad}
\tag{8}
\]

Thus the missing estimate can be posed concretely for the ESTABLISHED physical inverse: prove that B* maps Ran A₀ into Ran A₀ and that ||A₀⁻¹B*A₀|| is locally bounded, analytic, and tends to zero at the background. Ordinary boundedness of DR and DR⁻¹ in E does not imply this. Existing higher-regularity state reconstruction cannot be cited as a substitute unless it proves this specific dual-range property in the declared topology.

Formula (8) follows by expanding Ω₀((Id+B)v,(Id+B)z) and moving the second B using (7). It fixes the order of the two operator factors; the quadratic term is Bsharp B. This criterion is sufficient, not necessary: a different range-compatible primitive can work even when (2) fails.

## 4. An arbitrarily small analytic example where radial Moser fails

On ℓ²⊕ℓ² take w_n=n⁻², I_n=q_np_n, Ω₀=Σw_n dq_n∧dp_n, and

\[
F=\sum_{n\ge2}I_n,\qquad
\Delta=dI_1\wedge dF,\qquad\Omega_s=\Omega_0+s\Delta.
\tag{9}
\]

F is a continuous quadratic polynomial. Δ is analytic, closed, torus invariant, vanishes at 0, and is horizontal to all X_n=q_n∂q_n−p_n∂p_n. Its bounded two-form norm is O(||(q,p)||²), so it is arbitrarily small on small balls. Every Ωs is weakly nondegenerate: if Ωs(v,·)=0, testing against Xn gives dI_n(v)=0 for every n. Consequently dF(v)=0 by convergence of the differential series and i_vΔ=0; injectivity of Ω₀ then gives v=0. All moment maps w_nI_n are unchanged.

The radial primitive (4) is exactly

\[
\beta=\tfrac12(I_1dF-FdI_1).
\tag{10}
\]

If an E-valued Vs solved i_VsΩs=−β, evaluation on all Xn would force dI_n(Vs)=0, hence i_VsΔ=0. Therefore i_VsΩ₀=−β, and for n≥2 its components would necessarily be

\[
(V_s)_{q_n}=-\frac{I_1q_n}{2w_n},\qquad
(V_s)_{p_n}=\frac{I_1p_n}{2w_n}.
\tag{11}
\]

At q₁=p₁=ε and q_n=p_n=ε/n for n≥2, this is proportional to ε³n, so it is not in ℓ². Such states occur in every neighborhood of 0. Hence the radial Moser equation has NO E-valued solution at these states, although all the geometric identities (1), exact high moments, and even weak nondegeneracy of the entire interpolation hold.

Crucially, this is not a counterexample to symplectic normalization. Another primitive is βtilde=−F dI₁, with dβtilde=Δ. It has an admissible field supported in the first pair. In fact the explicit analytic map

\[
q'_1=e^{-F/w_1}q_1,\qquad p'_1=e^{F/w_1}p_1,
\qquad(q'_n,p'_n)=(q_n,p_n)\ (n\ge2)
\tag{12}
\]

preserves every I_n and satisfies (map (12))*Ω₀=Ω₀+Δ. Its inverse is equally analytic. Expanding dq'₁∧dp'₁ gives Ω₀−dI₁∧d(−F)=Ω₀+Δ. Thus a choice of primitive can remove the apparent range obstruction by putting the correction into a finite mode.

This example is also analytically congruent to the constant weak form. It shows that even knowing an analytic reconstruction R exists, together with (1), does not justify the radial construction or the particular sufficient estimate (2). It does not show any failure of actual DLW canonical coordinates.

## 5. Consequence for the current project

The original action products and invariant state inverse remain established at their stated level. To finish the canonical part there are now two precise routes: verify (7) for the actual reconstruction, obtaining (3) by the proved criterion; or construct a different invariant horizontal primitive whose range equation has a uniformly controlled E-valued solution. A proof must supply one of these actual estimates, rather than infer it from ordinary analyticity, form smallness, or moment-map identities. Low invariant completion and original-time evolution remain additional parts of the active goal.

Subsequent progress: [SYMPLECTIC_LIOUVILLE_AVERAGING.md](SYMPLECTIC_LIOUVILLE_AVERAGING.md) supplies a third route exploiting the original constant physical form and actual compact group action: average the original Euler vector field, contract, and take a limit of exact symplectic maps. This closes the high canonical step without asserting the sufficient weighted-adjoint condition above. The counterexample and the criterion remain valid; neither is needed as an unproved input to that new construction.
