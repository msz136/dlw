# Relative logarithmic profiles: a full-phase geometry audit

2026-10-11. This note audits a proposed replacement for the common-level tangent problem in the M=2 physical Cartesian chart. It uses the actual physical form transported by the state inverse. No symbolic checks were run, and no progress files were edited.

## 1. The proposed profile ball

Let the noncentral Cartesian base satisfy \(w_n^*z_n^*\ne0\), with \(w^*,z^*\in s\), where \(s=\bigcap_Nh^N\). For a positive weight \(g_n\ge1\), put
\[
E_g=\{q:\|q\|_g=\sup_n|q_n|/g_n<\infty\},
\qquad
\mathcal P(a,\vartheta)_n=
\left(w_n^*e^{(a_n+\vartheta_n)/2},
z_n^*e^{(a_n-\vartheta_n)/2}\right).
\tag{1}
\]
Its formal action formula is \(I_n=I_n^*e^{a_n}\). Both \(a\) and \(\vartheta\) vary: this is a proposed full phase, not a fixed-action isotropic family.

The following three issues are different.

1. Does a whole open ball in \(E_g^2\) map smoothly to \(s^2\)?
2. Is it a locally one-to-one physical state chart?
3. Is the actual common action level a regular submanifold of this phase?

For unbounded \(g\), the second and third issues have exact elementary obstructions, even if the first is supplied by a much stronger base decay.

## 2. A rapid base is insufficient

A necessary condition for the ball \(\max(\|a\|_g,\|\vartheta\|_g)<\varepsilon\) to map into \(s^2\) is
\[
w^*e^{r g}\in s,\qquad z^*e^{r g}\in s
\quad\text{for every }0<r<\varepsilon.
\tag{2}
\]
Indeed choose \(a=\vartheta=rg\), or \(a=-\vartheta=rg\), respectively. Ordinary rapid decay gives no such condition. In particular, if \(w_n^*=z_n^*=e^{-n^2}\) and \(g_n\) grows faster than every polynomial, then \(g_n/n^2\to\infty\), so (2) fails for every positive \(r\). The same example lies in every Sobolev sequence space and has every action nonzero.

Conversely (2), with a positive radius and a margin, gives an analytic map into every \(h^N\). On a smaller radius \(r<\rho<\varepsilon\), the \(k\)-th derivative is controlled by
\[
|w_n^*|e^{r g_n}g_n^k,\quad |z_n^*|e^{r g_n}g_n^k,
\qquad
g^ke^{-(\rho-r)g}\le k!(\rho-r)^{-k}.
\tag{3}
\]
Thus the extra exponential margin controls all derivatives. This is a genuine sufficient estimate; it is not a consequence of being a smooth state in the old strong domain.

## 3. Unbounded weights collapse the logarithmic branch

Suppose \(g_n\to\infty\) along a subsequence. The parameters
\[
a=0,\qquad \vartheta=4\pi i\,e_n
\tag{4}
\]
have norm \(4\pi/g_n\to0\), but (1) sends each of them to the base point. Hence \(\mathcal P\) is not locally one-to-one on any complex \(E_g^2\)-open neighborhood. Its derivative remains injective; an injective derivative here does not give an inverse-function theorem because the inverse derivative is not bounded into the profile norm.

The action map has a second version of the same defect:
\[
a=2\pi i\,e_n,\qquad \vartheta=0
\tag{5}
\]
has norm tending to zero and satisfies \(I=I^*\). Therefore the actual common level is not locally just \(a=0\). In particular it cannot be a split submanifold with tangent \(\{da=0\}\): projection onto the \(\vartheta\) coordinate would be locally one-to-one on that submanifold, whereas (5) gives distinct level points with the same \(\vartheta=0\) arbitrarily close to the base.

Restricting \(|\operatorname{Im}a_n|<\pi\) and \(|\operatorname{Im}\vartheta_n|<2\pi\) coordinatewise does not repair this as an \(E_g\)-open chart. These strips have no interior when \(g\) is unbounded.

The complex obstruction cannot simply be removed by asserting original reality. One must prove the lifted physical anti-involution preserves the chosen parameter domain and specify its fixed tangent space. Whenever that real tangent contains the periodic angular lattice directions in (4), the same obstruction applies to the real phase. A real hyperbolic logarithmic axis, considered alone, avoids periodicity, but its compatibility with the original real form cannot be assumed.

## 4. Even the real injective version is not an ambient embedding

Assume (2), and suppress the complex-period obstruction by taking real parameters only. Fix \(0<r<\varepsilon\) and use
\[
a^{(n)}=0,\qquad \vartheta^{(n)}=r g_n e_n.
\tag{6}
\]
Their profile norm is the fixed number \(r\). Their Cartesian differences from the base, however, converge to zero in every \(h^N\), by (2) with a margin greater than \(r/2\). Thus the inverse from the image with its ambient \(s^2\) subspace topology is not continuous.

The same issue already occurs for bounded \(g\) and relative \(\ell^\infty\) coordinates: a fixed-size logarithmic perturbation placed at a distant index is invisible in every ambient rapid-sequence seminorm. A profile phase can be assigned its own stronger topology and immersed into the physical smooth space. It must not be called an embedded ambient Fréchet submanifold.

## 5. The actual weak form survives an admissible full profile phase

There is a positive conclusion independent of the desired operator bound. Suppose a full profile map is defined on an open parameter domain, is injective there, and is smooth into the low physical state chart. Give its image the profile topology. Let \(\Omega_{\rm phys}\) be the original physical form, transported to the reduced Cartesian chart; define \(\omega=\mathcal P^*\Omega_{\rm phys}\).

At a point where all \(w_n,z_n\ne0\),
\[
D\mathcal P(\dot a,\dot\vartheta)_n
=\left(\tfrac12w_n(\dot a_n+\dot\vartheta_n),
\tfrac12z_n(\dot a_n-\dot\vartheta_n)\right).
\tag{7}
\]
This differential is injective and its range contains every finite-support Cartesian vector. Such vectors are dense in \(s^2\). Since the original form is continuous and weakly nondegenerate on the physical smooth space, \(\omega\) is continuous and weakly nondegenerate on the full profile tangent: a vector annihilating that tangent annihilates all finite-support physical directions and hence all physical directions.

This argument does not replace the physical form by the NLS canonical form. It also does not apply to the fixed-action family alone, whose pullback form vanishes.

For a physical real phase, the same conclusion follows if the lifted anti-involution is a smooth bounded involution of the profile phase, its fixed tangent complexifies to the complex profile tangent, and the transported physical form has its usual real compatibility. These are conditions to verify, not consequences of a real base point.

## 6. What a physical action cross-operator would actually supply

Suppose a repaired profile phase has a regular action coordinate \(a\), an angular model space \(E_\vartheta\), and a real coefficient space \(C\). Suppose the exact physical action fields have the form
\[
\dot a=0,\qquad \dot\vartheta=B(I)c,
\tag{8}
\]
where \(B(I):C\to E_\vartheta\) is a bounded isomorphism, depends only on actions, and respects the physical real structures. The phrase “elliptic of order two” is insufficient: the spaces and the bounded inverse are needed.

For every angle velocity \(v\in E_\vartheta\), choose \(c=B(I)^{-1}v\). If the Hamiltonian
\[
H_c=\sum_n c_n I_n
\tag{9}
\]
and its physical Hamiltonian field exist on this phase, then its flow on the fixed-action level is exactly
\[
\vartheta(t)=\vartheta(0)+t\,v.
\tag{10}
\]
All angle tangent vectors are therefore actual level velocities, and the level is an actual local Hamiltonian orbit. The proof requires convergence of (9), its differentiated series, the physical transpose formula, and preservation of the chosen phase under (10). A formal inverse of \(B\) does not verify those points.

If the space is \(E_g\) with \(g\) faster than every polynomial, then the expected coefficient \(c_n\sim v_n/n^2\) may grow faster than every polynomial. Such an \(H_c\) need not define a smooth functional on any ambient \(s^2\)-open set, even if it converges on an exceptionally small profile domain. It can be a valid Hamiltonian of a separately defined stronger phase after its derivative identity is proved. That claim must be distinguished from an already established ambient or old-strong-domain Hamiltonian.

The common action kernel is Lagrangian under the pulled-back original form whenever the regular profile level exists. Isotropy follows from the ambient kernel theorem. For maximality it is enough to test against finite actual action fields: orthogonality forces every \(dI_n\) to vanish, hence \(da=0\). This part does not by itself prove (8), the operator inverse, or an actual infinite orbit.

## 7. A possible repair with a different angular topology

A bounded logarithmic action variable \(a\in\ell^\infty\), with a uniform branch radius, avoids (5). To include a physical frequency growing like \(n^2\), one could investigate
\[
\vartheta_n=t\,p_n+\beta_n,\qquad
p_n\sim n^2,\quad t\in\mathbb C,\quad \beta\in\ell^\infty,
\tag{11}
\]
with \(t\) given its own finite-dimensional norm and \(\|\beta\|_\infty\) controlling the branch. This does not make a period at one high index arbitrarily small in the model-space topology. For the exact \(p_n=n^2\), local injectivity follows for sufficiently small \(t\) and bounded correction: a small nonzero imaginary \(t=i\tau\) has an index \(n\) near \(\sqrt{2\pi/|\tau|}\) where \(\tau n^2\) lies near \(2\pi\), so it cannot be canceled to a \(4\pi\) multiple by a uniformly small correction.

This is only a geometric direction. To make it an actual original-DLW phase one still needs:

- a physical real structure preserving (11);
- a base whose exponential decay survives all allowed \(t\,p\);
- exact physical frequencies contained in (11), and a continuous cross-operator inverse on the corresponding coefficient spaces;
- an action-varying phase for which all these conditions hold on an open set;
- either membership in the old strong domain, or a complete direct proof of the original flow on this newly defined phase.

No such conditions have been established by this audit. In particular the proposed superpolynomial weighted logarithmic ball cannot serve as the missing regular Liouville phase: it fails local single-valued state inversion and local common-level regularity before the physical cross-operator estimate is considered.

## 8. Finite polynomial growth plus a bounded branch

The finite-dimensional repair can be made geometrically precise without assuming a physical real slice. Let
\[
P_t(n)=\sum_{j=1}^d t_j\binom nj,\qquad
E^{(d)}=\mathbb C^d\oplus\ell^\infty,\qquad
\vartheta=P_t+\beta.
\tag{12}
\]
The nonconstant Newton basis is used so that a constant polynomial is not duplicated by the bounded term. Use uniformly bounded action logs \(a\in\ell^\infty\). Consider sufficiently small balls in \(a,t,\beta\).

The exponential state map is locally one-to-one. To prove this, suppose two points give the same Cartesian state. Since the action-log difference has sup norm less than \(2\pi\), their equal products imply \(\Delta a=0\). Their angular difference therefore obeys
\[
P_{\Delta t}(n)+\Delta\beta_n=4\pi i\,k_n,
\qquad k_n\in\mathbb Z.
\tag{13}
\]
Applying the \((d+1)\)-st forward difference gives
\[
4\pi|\Delta^{d+1}k_n|
\le 2^{d+1}\|\Delta\beta\|_\infty.
\tag{14}
\]
Choose the bounded-branch ball so that the right side is strictly less than \(4\pi\). Then the integer on the left is zero. Consequently \(k_n\) is an integer-valued polynomial of degree at most \(d\), and its Newton coefficients are integers. The polynomial \(P_{\Delta t}-4\pi i k\) is bounded on all indices by (13), so all its nonconstant coefficients vanish. Choosing \(|\Delta t_j|<4\pi\) forces these integer coefficients to be zero. Equation (13) is now a constant period; the uniformly small \(\Delta\beta\) forces it to be zero too. Thus \(\Delta t=\Delta\beta=0\).

The proof applies on positive indices; equality there is enough to determine \(t\). Bounded profiles on both positive and negative indices can then be included. For example, taking the \(\beta\) ball radius below \(2\pi/2^{d+1}\) makes the difference bound (14) sufficient. The action-log ball radius below \(\pi\) gives the product branch used above.

Thus adding independent \(n\) and \(n^2\) polynomial parameters is geometrically possible. It can contain a compact translation velocity proportional to \(i n\), a hyperbolic velocity proportional to \(n^2\), and bounded angular corrections. Smallness of the polynomial coefficient is controlled by its own finite-dimensional norm, even though the resulting pointwise angles are unbounded.

If the base satisfies
\[
(|w_n^*|+|z_n^*|)e^{r|n|^d}\in s
\quad\text{for some }r>0,
\tag{15}
\]
then the full map from this repaired local phase is analytic into every \(h^N\). Its image still carries a stronger topology than the ambient \(s^2\) topology, as in Section 4. Within that topology the actual level is exactly \(a=\text{constant}\), a split regular submanifold, and its tangent is exactly the common differential kernel. This is a full action-varying geometrical phase.

Equation (15), physical reality, and the membership of the actual physical frequency in \(E^{(d)}\) remain additional analytic conditions. In particular a bound \(\Omega_n=O(n^2)\) is insufficient to conclude \(\Omega\in E^{(2)}\): \(n^2\) times an arbitrary bounded sequence does not equal a quadratic polynomial plus a bounded remainder. The physical frequency must have the corresponding asymptotic expansion with bounded remainder.

If a proved physical \(B:\ell^\infty\to n^2\ell^\infty\) is an isomorphism, one may restrict its coefficient domain to \(B^{-1}(E^{(2)})\). This supplies all repaired angle velocities with bounded Hamiltonian coefficients, but it does not prove the original DLW frequency has the required polynomial-plus-bounded shape or prove its real-flow invariance.

## 9. The countable hierarchy requires a uniform lattice condition

For a sequence model space \(E\), the necessary local single-valuedness condition is that the exponential kernel be locally discrete:
\[
\Lambda_E=E\cap(4\pi i\mathbb Z)^{\mathbb Z\setminus\{0\}},
\qquad
U\cap\Lambda_E=\{0\}
\text{ for some zero-neighborhood }U\subset E.
\tag{16}
\]
The action-log model needs the analogous \(2\pi i\) condition. This is stronger than checking one fixed polynomial degree. A countable coefficient space cannot be declared safe merely because every finite-degree restriction is safe.

For example, if its topology permits the integer-valued polynomial profiles \(4\pi i\binom nj\) to tend to zero as \(j\to\infty\), (16) fails immediately. In a Banach coefficient norm \(\sum_j\alpha_j|t_j|\) in the Newton basis, this gives the necessary condition \(\inf_j\alpha_j>0\). It is only necessary: bounded corrections and completed infinite polynomial series also have to be controlled, and must not create additional small period sequences.

The finite-degree branch estimate in (14) worsens with degree. A countable completion therefore needs a separate uniform proof of (16), not a fixed branch radius copied from the finite-degree proof. Its evaluation map into a sufficiently rapidly weighted sequence space must also be continuous, so that the exponential state map and all actual hierarchy frequencies are well-defined on one open phase. These lattice, growth, real-structure, and frequency-preservation conditions are the outstanding requirements for a countable full-hierarchy profile phase.

## 10. Independent check of the new physical cross-operator estimate

The estimate in [the physical cross-operator note, Sections 3–5](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md) passes this independent operator-budget and same-action-test audit, subject to the already stated common analytic state-chart hypotheses.

The tensor budget is genuinely uniform on a small \(h^2\) ball. The inverse state map is analytic into \(u\in H^2,v\in H^3\). The full KLTZ derivative transpose preserves \(H^2\), using its auxiliary canonical identity to express that transpose through the bounded derivative of the analytic inverse. The central normalization adds analytic finite-rank terms; its central pair stays nonzero on the fixed chart. The exact physical potential transpose then maps potential \(H^2\) covectors into physical gradients in \(H^2\times H^1\), its only derivative entry being \(D/S\). Applying the original tensor gives velocities in \(L^2\times H^1\). The low forward state derivative maps this last mixed space to \(h^0\). Every operator factor depends analytically on the \(h^2\) state, so their product is analytic in the operator norm \(\mathcal L((h^2)^2,(h^0)^2)\).

For \(\sum\langle m\rangle^4|J_m|\le r^2\), prescribe the tested component \(w_n=r\langle n\rangle^{-2}\), \(z_n=J_n/w_n\), and choose balanced square roots at every other index. The two special weighted coordinates are each at most \(r\); the remaining squared weighted norm is at most \(2r^2\). Thus all tests lie in one fixed \(h^2\) ball, independently of \(n\), and carry the same action vector \(J\). Pure-action dependence is essential here. Dividing the uniform order-two field remainder \(O(r^2\|c\|_\infty)\) by the prescribed \(w_n\) gives
\[
\sup_n\frac{|(B(J)c)_n-D_nc_n|}{\langle n\rangle^2}
\le C r\|c\|_\infty.
\tag{17}
\]
This is a bound on the whole operator; it is not an estimate for one fixed action field.

For bounded \(c\), the safest definition of \(B(J)c\) is the coordinatewise limit of the finite-coefficient fields at these same-action tests. Their Cartesian covectors \((c_mz_m,c_mw_m)\) converge after finite truncation in \(h^2\), although the bare coefficients do not converge in \(\ell^\infty\). The analytic physical tensor therefore makes their fields converge in \(h^0\). Estimate (17) proves that this definition is a bounded linear map \(\ell^\infty\to\mathcal V_2\). No unproved absolute convergence of a displayed infinite matrix row is needed. The diagonal background coefficient is nonzero for every noncentral index, so the stated small perturbation estimate gives the Neumann inverse.

The resulting exact generation is an assertion about complex physical smooth tangent vectors at a state and genuine bounded-coefficient Hamiltonians. It supplies neither a profile manifold nor a flow in the old strong domain. For exact real generation on a newly chosen angular topology, one additionally needs the induced physical real angular tangent space to be preserved by that topology and the operator to identify it with the real coefficient space. Ordinary physical Poisson reality does not, by itself, prove boundedness of the lifted real involution on a relative-profile model.
