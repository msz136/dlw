# M=2 reciprocal actions: independent audit of the actual low Hamiltonian construction

2026-10-11. This audit reads [the root reciprocal-action proof, §§1–3](root_m2_reciprocal_actions_and_bounded_hamiltonians_audit_20261011.md), against the already audited [actual trace push](m2_physical_trace_poisson_closure_proof_20261011.md) and [mixed-low fields and real form](m2_actual_mixed_low_fields_bounded_torques_real_form_20261011.md). The variable-action core in [the regular phase note](m2_regular_variable_action_original_symplectic_phase_20261011.md) is used only to identify the precise new flow consequence. No checks were run and no shared record or other author's proof was edited.

**Verdict: PASS for the reciprocal contour, arbitrary bounded-coefficient Hamiltonian, actual whole-neighborhood low flow, and its bounded-profile core restriction.** The construction provides genuine Hamiltonian functions on a neighborhood, not only angular vectors at one state. The explicit local windows and the distinction from global time or all-hierarchy membership are recorded below.

## 1. Source-center cancellation and the exact normalization

Fix real \(L>0\) and \(S\ne0\), with the existing small-background/common-chart assumptions. Write

\[
\lambda(z;x)=\eta(x)-2iz/L,\qquad
\omega_\lambda=(S^2-\lambda^2)/(16S),\qquad
\Delta(z;x)=F_{\lambda(z;x)}(x).
\]

For each noncentral contour, a neighborhood of its closed disc avoids both \(\lambda=\pm S\) after shrinking the same low chart. The fixed noncentral disc separation from the calibrated central discs is essential. On such a simply connected neighborhood choose

\[
P_n(z,\eta)=4iL\log_n\frac{S+\lambda(z)}{S-\lambda(z)}.
\]

An additive source-dependent constant is immaterial: its contour contribution is zero by the established zero winding \(\oint\Delta_z/R\,dz=0\). Direct differentiation gives

\[
P_z=\frac{16S}{S^2-\lambda^2}=\omega_\lambda^{-1},\qquad
P_\eta=\frac{iL}{2}\omega_\lambda^{-1},\qquad
\partial_\lambda F_\lambda=\frac{iL}{2}\Delta_z.
\tag{1}
\]

Let

\[
A_n(x)=\frac1\pi\oint_{\Gamma_n}P_n(z,\eta(x))\frac{\Delta_z(z;x)}{R(z;x)}\,dz,
\qquad R^2=\Delta^2-4.
\tag{2}
\]

The variation identity

\[
\delta(\Delta_z/R)=\partial_z(\delta\Delta/R)
\]

is exact. Integration by parts, including the source dependence of \(P_n\), yields

\[
\delta A_n=-\frac1\pi\oint\frac{\delta\Delta}{\omega_\lambda R}\,dz
+\frac1\pi\oint\frac{iL\Delta_z}{2\omega_\lambda R}\,dz\,\delta\eta.
\]

At fixed \(z\), the correct chain rule is

\[
\delta\Delta=(d_xF_\lambda)_{\lambda\ \mathrm{fixed}}+\partial_\lambda F_\lambda\,\delta\eta.
\]

Equation (1) cancels the two center terms pointwise under the integral. Thus

\[
\boxed{dA_n=-\frac1\pi\oint_{\Gamma_n}\frac{dF_\lambda}{\omega_\lambda R}\,dz.}
\tag{3}
\]

This retains the actual fixed-original-centered-\(\lambda\) differential. It does not replace it by a fixed-\(\zeta\) trace differential or hold \(\eta\) constant. Because the compact-contour trace fields and their ordinary gradient representatives have the already proved mixed-low regularity, the contour can be passed through the actual linear differential tensor \(J_{uv}\). There is no additional derivative of the scalar coefficient at this step: (3) is already the full differential.

The audited exact field bridge is

\[
D\mathcal R X_{F_\lambda}=\omega_\lambda\Pi Y_{\lambda-\eta},\qquad
Y=(L/i)X_{\rm std}.
\]

Combining it with (3) and the actual full standard action contour identity gives

\[
D\mathcal R X_{A_n}
=\Pi Y_{I_n}=L G_n,
\qquad G_n=(-w_ne_n,z_ne_n),\qquad n\ne0.
\tag{4}
\]

The central-angle projection is retained. For the full noncentral \(I_n\), its central pair is zero, so \(d\vartheta_0(Y_{I_n})=0\), and the projection introduces no residual torque. With \(X_{I_n}^{\rm std}=iG_n\), the coefficient is precisely \((L/i)i=L\). This proves an equality of actual original physical Hamiltonian fields in a common neighborhood.

Each \(A_n\) is an analytic pure-action function, by the actual spectral factorization of \(\Delta\) and \(\eta\). At the background all its noncentral gaps collapse; \(\Delta_z/R\) extends through that collapsed zero and (2) integrates an analytic function. Therefore \(A_n(0)=0\). Formula (4) also shows directly that \(X_{A_n}J_m=0\) for every \(m\), including closed-gap pairs.

## 2. The continuous original low form

The physical low space is

\[
X_0=L^2_0(0,L)\times H^1_0(0,L),
\]

and the reduced low space is \(E_0=(\ell^2(\mathbb Z\setminus\{0\}))^2\). The original form

\[
\Omega(V,U)=-16\int_0^L\big[(D_0^{-1}V_u)U_v+(D_0^{-1}V_v)U_u\big]dx
\tag{5}
\]

is a continuous complex bilinear alternating form on \(X_0\). Indeed \(D_0^{-1}:L^2_0\to H^1_0\) and \(D_0^{-1}:H^1_0\to H^2_0\) are continuous; the displayed integral pairings are bounded. Skew-adjointness of \(D_0^{-1}\) gives antisymmetry. It is constant and hence closed. Testing independently against dense mean-zero \(H^1\) vectors and all mean-zero \(L^2\) vectors proves its weak nondegeneracy.

The common low inverse \(\mathcal R^{-1}\) is analytic. Consequently

\[
\widetilde\Omega_W(U,V)=
\Omega\big(D\mathcal R^{-1}_W U,D\mathcal R^{-1}_W V\big)
\tag{6}
\]

is analytic as a map into the Banach space of continuous alternating bilinear forms on \(E_0\), and is closed and weakly nondegenerate. Choose a star-shaped ball \(B_r\) centered at \(W=0\) inside this chart, small enough that \(\|\widetilde\Omega_W\|\le C_0\) there. Smooth-density extension, or directly the ordinary gradient identity, gives

\[
dA_n(W)[V]=\widetilde\Omega_W(LG_n(W),V)
\tag{7}
\]

also on this low ball.

## 3. Absolute action summability from radial integration

For finite-support \(d\), set

\[
M_dW=L(-d_nw_n,d_nz_n)_n,
\qquad H_d=\sum_{n\ne0}d_nA_n.
\]

Equation (7), \(H_d(0)=0\), and the fundamental theorem of calculus along the radial segment yield

\[
H_d(W)=\int_0^1\widetilde\Omega_{tW}(M_dtW,W)\,dt,
\qquad
|H_d(W)|\le\frac{LC_0}{2}\|d\|_\infty\|W\|_{E_0}^2.
\tag{8}
\]

For each finite set of indices, take \(d_n=\overline{A_n(W)}/|A_n(W)|\) where the denominator is nonzero and zero otherwise. Taking larger finite sets in (8) proves

\[
\boxed{\sum_{n\ne0}|A_n(W)|\le\frac{LC_0}{2}\|W\|_{E_0}^2.}
\tag{9}
\]

The coefficients are only test coefficients at this point; no analyticity of their phase selection is needed.

## 4. Arbitrary bounded coefficients: the required strong derivative limit

Fix any \(d\in\ell^\infty\). Define the actual analytic one-form

\[
\alpha_d(W)[V]=\widetilde\Omega_W(M_dW,V).
\]

Here \(M_d\) is one fixed bounded linear operator, with norm at most \(L\|d\|_\infty\). In particular \(\alpha_d:E_0\to E_0^*\) is genuinely Banach analytic. Its exact derivative is

\[
D\alpha_d(W)[U][V]=
D\widetilde\Omega_W[U](M_dW,V)
+\widetilde\Omega_W(M_dU,V).
\tag{10}
\]

For symmetric finite truncations \(d^{(N)}\), one has \(M_{d^{(N)}}W\to M_dW\) and \(M_{d^{(N)}}U\to M_dU\) in \(E_0\) for every fixed \(W,U\). The fixed forms \(D\widetilde\Omega_W[U]\) and \(\widetilde\Omega_W\) are continuous. Both terms in (10) therefore converge for each fixed \(W,U,V\). Exchanging \(U,V\) and using \(d\alpha_{d^{(N)}}=d^2H_{d^{(N)}}=0\) proves

\[
d\alpha_d=0.
\tag{11}
\]

No convergence of \(M_{d^{(N)}}\) in operator norm is asserted or needed. In particular, one must use the explicit derivative (10), rather than infer derivative convergence from pointwise convergence of functions alone.

Define \(H_d\) for arbitrary bounded \(d\) by the radial integral (8). It is analytic on \(B_r\), with the same bound. Its derivative is \(\alpha_d\): closedness gives

\[
DH_d(W)[U]
=\int_0^1\{tD\alpha_d(tW)[U][W]+\alpha_d(tW)[U]\}\,dt
=\int_0^1\partial_t\{t\alpha_d(tW)[U]\}\,dt
=\alpha_d(W)[U].
\tag{12}
\]

The segment is compact, all derivatives are locally uniformly bounded, and ordinary Banach differentiation under this finite integral is justified. Dominated convergence in (8), with \(\|M_{d^{(N)}}tW\|\le Lt\|d\|_\infty\|W\|\), identifies it as the absolutely convergent series

\[
H_d(W)=\sum_{n\ne0}d_nA_n(W).
\tag{13}
\]

The vector-valued map \(A:E_0\to\ell^1\) is analytic. One elementary justification avoids any reflexivity assumption: each component is analytic, (9) is locally bounded, and the Cauchy coefficients along each complex affine line have \(\ell^1\) norm bounded by the same circle bound times the inverse radius to the coefficient order. Tonelli applied to the componentwise Cauchy integrals gives this estimate. The resulting Taylor series converges in \(\ell^1\), proving line analyticity; local boundedness upgrades it to Banach analyticity. Equivalently, every \(\ell^\infty=(\ell^1)^*\) pairing is the analytic radial primitive (13). Formula (12) also gives

\[
\|DA(W)[U]\|_{\ell^1}\le LC_0\|W\|\|U\|.
\tag{14}
\]

## 5. These are actual original low Hamiltonians and flows

Pull \(H_d\) back to physical space and let

\[
X_d(x)=D\mathcal R^{-1}_{\mathcal R(x)}M_d\mathcal R(x)\in X_0.
\]

Equations (6), (12) give the genuine original identity

\[
\Omega(X_d,V)=d(H_d\circ\mathcal R)[V].
\tag{15}
\]

This can also be stated directly for the original differential Poisson tensor. The ordinary spatial gradient representative of the right side is

\[
g_u=-16D_0^{-1}(X_d)_v\in H^2_0,\qquad
g_v=-16D_0^{-1}(X_d)_u\in H^1_0.
\]

Pairing these gradients with \((V_u,V_v)\) reproduces (15), and

\[
-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}
\binom{g_u}{g_v}=X_d.
\tag{16}
\]

Thus the construction has not replaced the original tensor by an auxiliary canonical tensor. It also has not passed an infinite series through an unbounded differential operator without control. Weak nondegeneracy of (5) gives uniqueness of this actual field.

Its exact reduced flow is

\[
\Gamma_t(W)_n=(e^{-Ld_nt}w_n,e^{Ld_nt}z_n).
\tag{17}
\]

This is Banach analytic and solves the actual low field by the common inverse chart. It preserves all \(J_n\), so also the central fill and \(\eta\). If \(0<\delta<r\), then

\[
\|\Gamma_t(W)\|\le e^{L\|d\|_\infty|t|}\|W\|.
\]

Every \(W\in B_\delta\) has a common window \(|t|<T\) with any

\[
T<\frac{\log(r/\delta)}{L\|d\|_\infty}
\tag{18}
\]

when \(d\ne0\); \(d=0\) is the identity. This is a whole-neighborhood actual local flow, not merely a pointwise curve. For smooth inputs the same multipliers are bounded on every \(h^N\). The common higher inverse restrictions show that the same low time window preserves actual smooth physical fields. Global existence for all time inside the chart is not implied by (18).

## 6. Exact physical reality and the core consequence

The already independently proved normalized chart obeys

\[
\kappa(w,z)_n=(-\bar w_{-n},-\bar z_{-n}).
\]

The coefficients \(S,L\) and original form are real. From (4), \(\kappa_*LG_n=LG_{-n}\); therefore the reflected-conjugated Hamiltonian has the same differential as \(A_{-n}\). Both vanish at the background. Connectedness gives

\[
A_{-n}(\bar x)=\overline{A_n(x)}.
\tag{19}
\]

This supplies a sign check independent of guessing the reflection sign of the square-root or logarithm branch. For \(d_{-n}=\bar d_n\), (13) is real on the actual real physical slice and (17) preserves that slice.

On the variable-action core's coordinates

\[
w_n=w_n^*e^{a_n/2+q_n-tk_n^2+isk_n},\qquad
z_n=z_n^*e^{a_n/2-q_n+tk_n^2-isk_n},
\]

the same fixed \(H_d\), now defined on the whole common low ball, has

\[
\dot a=\dot t=\dot s=0,\qquad\dot q=-Ld.
\tag{20}
\]

Thus every bounded logarithmic phase direction is generated by an actual Hamiltonian whose field is tangent to the entire core neighborhood. Its flow is translation of \(q\) and remains in the chosen box for the corresponding ordinary local window. This fills the former neighborhood gap of using only \(B(J_0)^{-1}\) at one action value.

If the separate original-flow normalization has been proved, so that the original Hamiltonian has \((\dot t,\dot s,\dot q)=(1,-2\widetilde\eta(J),r(J))\), and the translation Hamiltonian has \(\dot s=1\), then a prescribed fixed-level displacement \((\delta q,\delta t,\delta s)\) at \(J_0\) is generated by the single actual charge

\[
\delta t\,H+
\bigl(\delta s+2\widetilde\eta(J_0)\delta t\bigr)P+H_d,
\qquad
d=\frac{\delta t\,r(J_0)-\delta q}{L}.
\tag{21}
\]

These coefficients are fixed constants for this charge. At nearby actions the same field still has analytic bounded \(q\) velocity and the displayed finite \(t,s\) velocities. Hence it is a genuine whole-core local Hamiltonian field; on the chosen level its time-one trajectory realizes the displacement whenever the intervening segment stays in the box. This consequence requires the original \(H,P\) normalization inputs, but no new pointwise cross-operator inverse.

## 7. Scope of this PASS

The reciprocal proof and its low Banach derivatives need no correction. The explicit formulas (10), (12), (16), and (18) make all limiting and actual-flow claims verifiable. A [separate independent bounded-sum audit](m2_reciprocal_bounded_sum_derivative_independent_audit_20261011.md) also checks these Banach steps.

This audit does not by itself certify the whole variable-action core's injectivity, Lagrangian fibers, or original quadratic-frequency normalization; those have their own phase and spectral audits. Arbitrary reciprocal bounded-charge curves have actual low and smooth flows, but membership of every point in the older all-hierarchy strong domain is a separate issue. The full ordinary general-field, all-M Liouville theorem is not obtained here.
