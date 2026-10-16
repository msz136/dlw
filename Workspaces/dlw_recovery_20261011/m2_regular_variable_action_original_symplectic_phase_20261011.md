# M=2: a regular variable-action phase for the original form and the original DLW flow

2026-10-11. Independent construction, with a declared Banach topology. No old checks were run. This is a phase of actual physical fields with both infinite action and infinite phase freedom. Its topology is stronger than the ambient smooth-field topology. It does not give an ordinary \(C^\infty\)-open Cauchy domain or assert that its whole variable-action ball belongs to the previously constructed \(\mathcal S_\infty\).

This proof uses the established [reduced state chart](akns_physical_state_inverse_bridge_20261011.md), [actual Poisson/closure theorem](m2_physical_trace_poisson_closure_proof_20261011.md), and the [cross-operator estimate](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md). Two additional precise inputs are identified in §1, so their normalizations can be audited independently. These inputs concern the particular KLTZ-normalized chart; an abstract canonical chart is not enough.

Current navigation: §§2–5 establish the regular variable-action core and the original weak form. The earlier point-level limitation in §6 is **resolved for the bounded component by the new reciprocal-action construction in §8**. Section 9 states the resulting local weak Liouville theorem, while retaining the precise whole-\(\mathcal S_\infty\) and higher-hierarchy limitations of §7. Section 10 verifies the reconstruction into both original lattice fields, their intrinsic coupling and an open subbox excluding frozen or rigid-translation solutions.

## 1. Analytic inputs and a nonzero real base

Write \(k_n=2\pi n/L\), \(n\ne0\), and \(s=\bigcap_{r\ge0}h^r\). The common reduced state chart is
\[
\mathcal R:\mathcal O_{\rm red}\cap(H^r_0\times H^{r+1}_0)
\longleftrightarrow
\mathcal U_{\rm red}\cap(h^r\times h^r),
\qquad W=(w,z),\quad J_n=w_nz_n.
\tag{1}
\]
All scalar central constraints and branches are those of the existing low chart: \(I_0=\rho(J)\), \(\eta=\widetilde\eta(J)\). The source physical tensor is exactly
\[
J_{\rm phys}=-\frac1{16}
\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\tag{2}
\]

The following are the additional inputs.

**(R)** In this normalized reduced chart, transported physical conjugation is
\[
\sigma(w,z)_n=(-\overline{w_{-n}},-\overline{z_{-n}}).
\tag{3}
\]
Consequently \(J_{-n}=\overline{J_n}\) on the real physical slice. This is the exact chart-equivariance theorem established in [the independent KLTZ real-involution audit](m2_kltz_physical_real_involution_independent_audit_20261011.md), §§1–4. Its proof matches the two primary sources' normalized Abel–Dirichlet angles, extends the symmetry by the analytic identity theorem, and checks the central root and actual physical gauge. It applies to the specified common small domain and standard spectral normalization; no standard NLS real form is substituted.

**(K)** The actual centered original DLW Hamiltonian has pure-action torque
\[
\dot w_n=\Omega_{H,n}(J)w_n,\qquad
\dot z_n=-\Omega_{H,n}(J)z_n,
\]
\[
\boxed{\quad
\Omega_{H,n}(J)=-k_n^2-2i\widetilde\eta(J)k_n+r_n(J),
\qquad r:J\longmapsto\ell^\infty\ \text{analytic}.
\quad}
\tag{4}
\]
The original time normalization is proved in [the reciprocal-action/frequency bridge](m2_reciprocal_spectral_actions_and_dlw_frequencies_20261011.md), §3, and independently checked in [the root original-frequency audit](root_m2_original_frequency_normalization_audit_20261011.md), §§1–3. The actual \(C^1\) quasimomentum coefficient comparison gives the original factor \(H=-16SC_1+\mathrm{constant}\), the central-frequency subtraction and the translation term in (4). The external analytic input is [Berti–Kappeler–Montalto, arXiv:1603.09252](https://arxiv.org/abs/1603.09252), Theorem 3.2, for complex action frequencies with a bounded analytic remainder. Its additional domain condition remains essential: for a zero-centered \(\ell^{1,2}\) ball of radius \(r_{\rm BKM}>0\) in the theorem's complex neighborhood, require
\[
L^2S^2/4<r_{\rm BKM}/2,\qquad
|\rho(J)-I_0^*|+\sum_{n\ne0}\langle n\rangle^2|J_n|
<r_{\rm BKM}/2,\qquad I_0^*=-L^2S^2/4.
\]
The published theorem supplies no explicit numerical \(r_{\rm BKM}\), and an older mixed-flow or KLTZ radius does not automatically imply these inequalities.

At a real action sequence the functions in (4) obey
\[
\widetilde\eta\in\mathbb R,\qquad
r_{-n}=\overline{r_n},\qquad
\Omega_{H,-n}=\overline{\Omega_{H,n}},
\tag{5}
\]
because \(H\) and its physical field are real and (3) is the actual real structure. Spatial translation has the exact torque \(ik_n\).

Choose an actual real strong state \(x_*\) in this chart with every \(J_n^*\ne0\), satisfying the small \(\ell^1_4\) hypothesis of the physical cross-operator theorem and the action neighborhood of (4). Such a choice is possible after shrinking the common Hilbert parameter ball in the existing all-finite-block Baire construction in the finite \(h^2\) norm. This is a residual parameter assertion, not natural openness of all smooth physical states.

Let \(W_*=(w^*,z^*)=\mathcal R(x_*)\). Its existing complex \(H\) germ and (4) imply a Gaussian exponential margin
\[
\boxed{\quad
(|w_n^*|+|z_n^*|)e^{\gamma k_n^2}\in s
\quad\text{for some }\gamma>0.
\quad}
\tag{6}
\]
To see this, use the actual orbit \(w_n(t)=w_n^*e^{t\Omega_{H,n}(J^*)}\), \(z_n(t)=z_n^*e^{-t\Omega_{H,n}(J^*)}\) at four sufficiently small complex times \(\pm T,\pm iT\). One corner gives growth at least \(T|\Omega_{H,n}|/\sqrt2\) for each component. These corners have rapid coordinates. Since \(|\Omega_{H,n}|\ge k_n^2/2\) in the tail by (4), they imply (6). The finitely many other indices are harmless. Even real \(\pm T\) suffice here by the real quadratic leading term.

## 2. Full real Banach phase with both action and phase freedom

Define the real Banach space
\[
\mathcal B=\{a\in\ell^\infty(\mathbb Z\setminus\{0\},\mathbb C):
a_{-n}=\overline{a_n}\}.
\]
Its positive-index coordinates are arbitrary bounded complex sequences. Use variables
\[
(a,q,t,s)\in\mathcal B\times\mathcal B\times\mathbb R\times\mathbb R,
\]
and define
\[
\begin{split}
w_n&=w_n^*\exp\{a_n/2+q_n-tk_n^2+isk_n\},\\
z_n&=z_n^*\exp\{a_n/2-q_n+tk_n^2-isk_n\}.
\end{split}
\tag{7}
\]
Take an open product box with \(\|a\|_\infty<\delta\), \(\|q\|_\infty<\epsilon\), \(|t|<T_0\), \(|s|<S_0\), where
\[
\delta<\pi/4,\quad \epsilon<\pi/16,\quad
T_0<\gamma/4,\quad S_0<L/8.
\tag{8}
\]
Shrink these radii once more so that (7) remains in the state inverse low chart, the cross-operator action ball, and the domain of (4).

The map (7) is real analytic into every \(h^r\times h^r\). The only unbounded multipliers in its derivatives are powers of \(k_n\) and \(k_n^2\); (6) controls all of them with a strict exponential margin. The \(a,q\) derivatives are bounded coordinate multipliers. Composition with (1) gives actual real smooth physical fields by (3). Both freely chosen sequences remain present; no physical field is frozen.

Declare the image \(\mathcal P_{\rm core}\) to have the topology and ordinary Banach smooth structure transported from this box. This declared topology is part of the theorem. It is not the subspace topology of \(s^2\) or of physical \(C^\infty\).

## 3. State injectivity, derivative injectivity, and ordinary common levels

The exact products in (7) are
\[
J_n=J_n^*e^{a_n}.
\tag{9}
\]
All \(J_n^*\) are nonzero. Equality of two states therefore gives \(a=\widetilde a\), since \(|a_n-\widetilde a_n|<\pi\) excludes a nonzero \(2\pi i\) period.

For the remaining variables put
\[
b_n=q_n-\widetilde q_n-(t-\widetilde t)k_n^2
 +i(s-\widetilde s)k_n=2\pi i\ell_n,\qquad \ell_n\in\mathbb Z.
\tag{10}
\]
Taking real parts and using bounded \(q-\widetilde q\) forces \(t=\widetilde t\). On positive indices, second finite differences of (10) give
\[
2\pi\Delta^2\ell_n=\operatorname{Im}\Delta^2(q-\widetilde q)_n .
\]
The right side has magnitude at most \(8\epsilon<2\pi\); hence the integer \(\Delta^2\ell_n\) is zero. Thus \(\ell_n=An+B\) with integers \(A,B\). Boundedness of \(q-\widetilde q\) gives
\((s-\widetilde s)2\pi/L=2\pi A\). But \(|s-\widetilde s|<L/4\), so \(A=0\) and \(s=\widetilde s\). Finally \(\|q-\widetilde q\|_\infty<\pi\) gives \(B=0\). Negative indices give the same conclusion. The state map is injective.

Its differential is injective as well. A zero Cartesian derivative first gives \(\delta a=0\) by differentiating products. It then gives
\[
\delta q_n-\delta t\,k_n^2+i\delta s\,k_n=0 .
\]
The unbounded real quadratic part forces \(\delta t=0\), and the unbounded linear imaginary part forces \(\delta s=0\); hence \(\delta q=0\).

The relative action target is the Banach coordinate
\[
\mathscr A(x)_n=\log\bigl(J_n(x)/J_n^*\bigr)\in\mathcal B .
\tag{11}
\]
On \(\mathcal P_{\rm core}\) it is exactly \(a\). It is therefore a real-analytic split submersion. Its levels are the ordinary Banach submanifolds \(a=a_0\), with
\[
T_xY=\{\delta a=0\}
=\bigcap_{n\ne0}\ker d(\operatorname{Re}I_n,\operatorname{Im}I_n)
\quad\text{inside }T_x\mathcal P_{\rm core}.
\tag{12}
\]
This is an unclosed actual tangent equality on this declared phase. The usual Banach internal tangent agrees with its ordinary tangent, so both phase and level evaluation maps have zero ghost kernel by the injective state derivative. This does not settle the inherited fiber tangent of the larger \(\mathcal S_\infty\).

## 4. Original DLW, translation, and individual spectral Hamilton flows

At fixed \(a\), write \(J=J^*e^a\). Equation (4) gives the original centered field as the following genuinely analytic vector field on the entire core box:
\[
\boxed{\quad
\dot a=0,\quad \dot t=1,\quad
\dot s=-2\widetilde\eta(J),\quad \dot q=r(J).
\quad}
\tag{13}
\]
Its actual local flow is obtained by integrating these constant-on-level coefficients. The result differentiated through (7) is exactly the original physical field. Translation is \(\dot s=1\), all other coordinates fixed. The exact reconstruction with arbitrary prescribed smooth \(\Gamma(t)\) adds the corresponding spatial translation; it imposes no \(\Gamma_t=0\).

For each fixed actual normalized trace or contour action, its physical field is an analytic order-zero field on the low mixed state chart, and its Cartesian torque is pure-action. This gives a bounded \(\ell^\infty\) torque uniformly on a smaller relative action box. Here is a precise uniform test, avoiding tiny actual gaps.

The balanced representative \(w_n=z_n=\sqrt{J_n^*}e^{a_n/2}\) of that action family has relatively compact image in \(h^0\times h^0\): its tail is uniformly bounded by a fixed summable sequence, and every finite-coordinate image is bounded. Choose the slightly larger complex \(a\) box so that the compact closure of this image lies strictly inside the common low domain. This is possible by the initial small action ball and its strict margin. Around that compact closure an analytic order-zero field has a uniformly bounded holomorphic neighborhood. For a tail index \(n\), replace the \(n\)-th pair by \(w_n=r_0,\ z_n=J_n/r_0\), with a single small \(r_0>0\). All these test states remain in that neighborhood: the first component changes by at most \(r_0+o(1)\), and the second by \(o(1)\), uniformly in \(a\). The field's \(n\)-th component divided by the prescribed \(r_0\) bounds its pure-action torque uniformly in \(n\). The finite head is bounded by compactness and nonzero fixed pairs. The larger complex \(a\) box permits Cauchy estimates, hence holomorphic dependence into \(\ell^\infty\).

Thus every fixed realified trace/action field has
\[
\dot a=\dot t=\dot s=0,\qquad \dot q=v_F(J)\in\mathcal B
\tag{14}
\]
and an actual analytic flow on the whole core phase. The real condition follows from (3) and realification of the original Hamiltonian. Every fixed finite list has a common short time box, and the fields commute by the actual physical Poisson theorem. The constants may depend on the selected finite list.

No such bounded-torque assertion is made for all higher \(C_j\) on this core phase: their growing imaginary or higher polynomial parts need not belong to its tangent model.

## 5. The original form is weakly symplectic, and the actual levels are Lagrangian

Use the original continuous form on the smooth mean-zero physical leaf:
\[
\Omega(V,W)=-16\int_0^L
\bigl[(D_0^{-1}V_u)W_v+(D_0^{-1}V_v)W_u\bigr]\,dx.
\tag{15}
\]
It is antisymmetric because \(D_0^{-1}\) is skew-adjoint; it is the inverse of (2), with \(\Omega(X_F,V)=dF(V)\). Pull (15) back through the analytic state map (7). The resulting form is a smooth closed real two-form on the Banach core, since the state map is smooth into every physical seminorm.

Let \(V\) annihilate the entire core tangent under this form. The individual realified action fields (14) are core tangents. Pairing with them gives all \(dI_n(V)=0\), so (9) forces \(\delta a=0\). Its remaining Cartesian velocity is
\[
(\theta_nw_n,-\theta_nz_n),\qquad
\theta_n=\delta q_n-\delta t\,k_n^2+i\delta s\,k_n\in\mathcal V_2 .
\tag{16}
\]
The physical cross-operator isomorphism supplies \(c=B(J)^{-1}(-i\theta)\in\ell^\infty\). The genuinely defined ambient Hamiltonian \(H_c=\sum c_nI_n\) has exactly this physical velocity at this point. By uniqueness of the cross inverse and physical conjugation, \(c_{-n}=\overline{c_n}\) when \(V\) is real, so this is a real Hamiltonian. For each finite-support relative action variation \(b\in\mathcal B\),
\[
\Omega(V,V_b)=dH_c(V_b)=\sum_{n\ne0}c_nJ_nb_n .
\tag{17}
\]
The sum is finite for this test. Nonzero \(J_n\) and arbitrary real/imaginary values of \(b_n\) force every \(c_n=0\); hence \(\theta=0\), and derivative injectivity gives \(V=0\). The pulled-back original form is weakly nondegenerate.

Every vector in (12) belongs to the already proved closed ambient common kernel \(K\), which is isotropic for the original physical form. Thus each level is isotropic. Conversely a core tangent orthogonal to the level pairs to zero with all individual action fields in that level, so its \(a\) component vanishes. Therefore
\[
\boxed{\quad (T_xY)^{\perp_\Omega}=T_xY
\quad\text{inside }T_x\mathcal P_{\rm core}.\quad}
\tag{18}
\]
This is actual level-tangent maximality on the new phase, not merely a closure of level velocities.

The use of \(H_c\) in (17) is pointwise pairing. It does not assert that \(X_{H_c}\) remains tangent to the entire core neighborhood as \(J\) changes.

### 5.1 Independent density proof and direct level isotropy after §8

There is a simpler proof of weak nondegeneracy that does not use \(B^{-1}\). At any core point all \(w_n,z_n\) are nonzero. For an arbitrary finite-support Cartesian real tangent \((\dot w,\dot z)\), set
\[
\dot a_n=\dot w_n/w_n+\dot z_n/z_n,\qquad
\dot q_n=\tfrac12(\dot w_n/w_n-\dot z_n/z_n),\qquad
\dot t=\dot s=0.
\]
The two ratios have the same reflection-conjugation reality as \(\mathcal B\), so these are legitimate finite-support core tangents. Conversely their derivative in (7) is exactly the prescribed Cartesian tangent. Such finite-support tangents are dense in the real low space \(E_{\mathbb R}=\operatorname{Fix}\Sigma\subset(h^0)^2\).

The low form is continuous and weakly nondegenerate. Indeed on \(L^2_0\times H^1_0\), vanishing of (15) against all \(W_u\in L^2_0\) forces \(D_0^{-1}V_v=0\), hence \(V_v=0\); vanishing against all \(W_v\in H^1_0\), which is dense in \(L^2_0\), then forces \(D_0^{-1}V_u=0\), hence \(V_u=0\). The low state inverse is a Banach isomorphism on derivatives and preserves reality, so the same statement holds for \(\widetilde\Omega\) on \(E_{\mathbb R}\). If a core tangent annihilates every core tangent, it annihilates the dense finite-support test family, hence every low test by continuity. Its actual state velocity is zero; §3's derivative injectivity gives the zero core tangent.

The new family in §8 also proves level isotropy directly. At a fixed point, every level tangent \(V=(0,\dot q,\dot t,\dot s)\) is exactly
\[
V=\dot t\,X_H+(\dot s+2\eta\dot t)\,X_P+X_{H_d},
\qquad d=-\frac{\dot q-r(J)\dot t}{L}\in\mathcal B.
\]
All three fields are genuine fields on the whole core neighborhood, and all their Hamiltonians commute. Thus every two level tangents pair to zero under the original form. A core vector orthogonal to the level pairs to zero with each individual realified \(I_n\) field, which is a level tangent by §4. This forces its \(\dot a\) component to vanish by (9), proving (18).

This second proof requires neither the cross-operator isomorphism nor the ambient closed-kernel maximality theorem. The original small cross-operator domain remains a sufficient domain for the first proof and for the previously selected base; it is not needed as a new independent geometric assumption once the common low state chart, exact reciprocal fields, and original-frequency domain are supplied. It does not remove any of those state-chart or frequency hypotheses.

## 6. Actual ambient Hamilton trajectories on a fixed level, and their exact scope

Two nearby points on the same level differ by a relative logarithmic phase
\[
\theta=\Delta q-\Delta t\,k^2+i\Delta s\,k\in\mathcal V_2.
\]
At that fixed action \(J\), choose \(c=B(J)^{-1}(-i\theta)\). Along the level, \(B(J)c\) is constant. The actual ambient field \(X_{H_c}\) therefore has the exact physical trajectory obtained by linearly interpolating \((q,t,s)\); this stays in the core box for nearby endpoints.

Consequently each sufficiently small level piece is reached by genuine ambient spectral Hamiltonian trajectories, including an infinite bounded-coefficient Hamiltonian when necessary. This is an actual fixed-level trajectory theorem. It is not a claim that the same \(H_c\) has a vector field on a full core neighborhood. Indeed for neighboring \(J'\), \(B(J')c\) may be a general quadratic-growth sequence outside
\(\ell^\infty+\mathbb R k^2+i\mathbb R k\). Without a new global reciprocal-action or smoothing theorem, these trajectories must not be advertised as a group of core-phase Hamiltonian automorphisms.

## 7. Relation to the old strong domain and remaining completeness tasks

The fixed \(a=0\) component, including bounded \(q\) and sufficiently small real heat/translation times, lies in the same \(\mathcal S_\infty\): the actual joint-germ/endpoint reconstruction in [the relative-fiber note](m2_strong_isospectral_orbits_and_relative_fiber_20261011.md), §3, applies. Here is also the explicit infinite-profile version needed for §8. Start with the existing compatible actual \(C_j\) joint germs at \(x_*\). Their actions are constant, and their Cartesian components are their base components multiplied by the pure-action exponentials for each finite time prefix. A fixed bounded \(q\), or a reciprocal flow parameter \(d\in\mathcal B\), multiplies those same joint coordinates by \(e^{q_n}\) and \(e^{-q_n}\), or by \(e^{-Ld_n\tau}\) and \(e^{Ld_n\tau}\). These are bounded multipliers on every \(h^r\), uniformly for bounded parameter balls and short \(\tau\), and commute with every finite-prefix exponential. Compose with the actual common-domain inverse and reconstruct the mixed source corners. The inverse and finite-prefix center uniqueness give compatible actual germs through the new center.

The common low-domain margin can be retained by shrinking the existing auxiliary windows one coordinate at a time. At the \(j\)-th step continuity on the already compact finite time box allows a positive new width for that coordinate, with extra low displacement at most \(2^{-j}\varepsilon_0\). The summable budget keeps every finite joint box inside the fixed low-domain margin; no positive uniform lower bound for all widths is asserted or needed. On compact parameter families the same choices are uniform, so the reconstructed parameter maps are legitimate strong plots. Adding the already actual original \(H\) and translation axes uses the same argument. This proves fixed-action strong membership for the bounded infinite Hamilton profiles; it does not change the unproved variable-action assertion below.

For a **variable** \(a\) ball, this note proves actual original DLW, translation and every fixed finite trace/action flow directly, and proves all the ordinary geometry in §§2–5. It does not prove that all these points admit positive-window actual germs for every higher \(C_j\), or that the whole phase is contained in the old \(\mathcal S_\infty\). A Gaussian exponential margin is enough for the order-two original flow, but not automatically for every higher hierarchy axis. That all-hierarchy membership is a separate task.

The topology excludes the bad rapid-kernel example: its allowed angular ratios are bounded plus only the displayed heat and translation profiles. Arbitrary rapidly decreasing Cartesian velocities with exponentially enormous ratios are absent. Neither their omission nor the Gaussian margin is an artificial fixed physical-field ansatz: \(a\) and \(q\) range over two full infinite bounded-sequence spaces. Nevertheless this is a thin specified function phase, not a naturally open general smooth-field neighborhood.

The reality and original-time normalization inputs are now supplied by the independent proofs linked in §1. Section 8 supplies the full-neighborhood Hamilton orbit statement using a new family, resolving §6's earlier limitation for bounded profiles. The remaining distinctions are the whole variable-action core's all-hierarchy membership and the full inherited strong fiber. No all-M invariant-action inverse or all-M regular fiber is asserted.

## 8. Reciprocal spectral actions: full-neighborhood bounded Hamilton flows

### 8.1 Exact physical chain rule and the single-coordinate field

For each noncentral spectral contour choose a local logarithm and put
\[
\lambda=\eta-\frac{2iz}{L},\quad
\omega_\lambda=\frac{S^2-\lambda^2}{16S},\quad
P_n(z,\eta)=4iL\log_n\frac{S+\lambda}{S-\lambda},
\]
\[
\mathcal A_n=\frac1\pi\oint_{\Gamma_n}
P_n(z,\eta)\frac{\Delta_z(z)}{R(z)}\,dz,\qquad
R^2=\Delta^2-4.
\tag{19}
\]
These are the actual normalized discriminant and fixed KLTZ contours. The noncentral discs avoid \(\lambda=\pm S\) throughout a sufficiently small common low domain: those two spectral points remain in the separate central disc. Therefore the logarithm exists on a neighborhood of every noncentral closed contour, uniformly as a domain choice. Changing its branch adds a constant times \(\oint\Delta_z/R\), which vanishes by the already proved zero-winding identity. There is no unrecorded branch-dependent Hamiltonian.

The exact derivatives are
\[
P_z=\omega_\lambda^{-1},\qquad
P_\eta=\frac{iL}{2\omega_\lambda}.
\]
Variation and contour integration by parts give
\[
d\mathcal A_n
=-\frac1\pi\oint_{\Gamma_n}\frac{d\Delta}{\omega_\lambda R}\,dz
 +\frac1\pi\oint_{\Gamma_n}
\frac{iL\Delta_z}{2\omega_\lambda R}\,dz\,d\eta .
\]
At fixed \(z\), the actual state-dependent spectral shift gives
\[
d\Delta=dF_\lambda+\frac{iL}{2}\Delta_z\,d\eta .
\]
The two \(d\eta\) terms cancel exactly. Hence
\[
\boxed{\quad
d\mathcal A_n=-\frac1\pi\oint_{\Gamma_n}
\frac{dF_\lambda}{\omega_\lambda R}\,dz,\qquad
D\mathcal R X_{\mathcal A_n}=L(-w_n,z_n)
\text{ on pair }n,\ 0\text{ otherwise}.
\quad}
\tag{20}
\]
The field identity uses the exact physical trace push-forward
\(D\mathcal R X_{F_\lambda}=\omega_\lambda\Pi Y_\Delta\), followed by the full action contour identity. Projection preserves the individual noncentral action field. This proves (20) at every nearby action sequence, not just at one fixed level.

At the uniform background every noncentral gap is closed and the integrand in (19) extends holomorphically through its disc, so \(\mathcal A_n(0)=0\). Its background differential is
\[
d\mathcal A_n(0)=\frac{16S}{k_n^2}\,dI_n(0)
\tag{21}
\]
as an action differential, or equivalently as the coefficient of its Cartesian quadratic term. The numerical factor follows equally from (20) and the already checked background \(B_{nn}=iLk_n^2/(16S)\). All brackets of these actions with the actual traces, \(I_m\), original \(H\), translation, and \(C_j\) vanish: (20) pairs only the corresponding actual trace brackets. This claim concerns actual source regularity for each fixed \(C_j\), not an unrestricted formal gradient.

### 8.2 Uniform summability follows from the original low mixed form

Let \(E=(h^0)^2\), and transport the original form through the low state inverse:
\[
\widetilde\Omega_W(V_1,V_2)
=\Omega_{\mathcal R^{-1}(W)}
\bigl(D\mathcal R^{-1}_W V_1,D\mathcal R^{-1}_W V_2\bigr).
\]
It is an analytic bounded bilinear form on one small \(E\) ball. Indeed
\(\mathcal R^{-1}:E\to L^2_0\times H^1_0\) is analytic, and (15) is continuous on that mixed low space. Its bound needs no high Sobolev norm or transpose estimate.

For finite-support \(d\) set \(H_d^{\rm fin}=\sum d_n\mathcal A_n\). Formula (20) gives
\[
X_d(W)=(-Ld_nw_n,Ld_nz_n)_n,\qquad
\|X_d(W)\|_E\le L\|d\|_\infty\|W\|_E .
\]
On the radial path \(uW\), \(0\le u\le1\), all \(\mathcal A_n(0)=0\), so
\[
H_d^{\rm fin}(W)
=\int_0^1\widetilde\Omega_{uW}(X_d(uW),W)\,du .
\]
If \(\|\widetilde\Omega\|\le M\) on the ball, then
\[
|H_d^{\rm fin}(W)|
\le\frac{ML}{2}\|d\|_\infty\|W\|_E^2.
\]
Choose the phases of the finitely many \(d_n\)'s to align their \(\mathcal A_n(W)\)'s. It follows that
\[
\boxed{\quad
\sum_{n\ne0}|\mathcal A_n(W)|
\le\frac{ML}{2}\|W\|_E^2.
\quad}
\tag{22}
\]
This is a common-domain bound for the entire action family. No norm convergence of finite support sequences in \(\ell^\infty\) is used.

For clarity, coordinate holomorphy plus (22) gives \(\mathcal A:E\to\ell^1\) holomorphic. On each smaller complex disc in a source direction, Cauchy estimates can be summed over any finite set of output coordinates and then the finite set can increase; the uniform \(\ell^1\) bound supplies convergent \(\ell^1\)-valued Taylor coefficients and their normally convergent series. Polarization gives their continuous multilinear versions. Thus this is Banach holomorphy, not just pointwise coordinate analyticity.

Consequently for every \(d\in\ell^\infty\),
\[
\boxed{\quad H_d=\langle d,\mathcal A\rangle
\text{ is an actual holomorphic low-state Hamiltonian},\qquad
X_{H_d}(W)=(-Ld_nw_n,Ld_nz_n)_n.\quad}
\tag{23}
\]
To verify the Hamilton identity, finite truncations of (23) converge at fixed \(W\) in \(E\), because \(W\in\ell^2\); the differential sums converge in \(\ell^1\), since \(D\mathcal A:E\to\ell^1\). The bounded form therefore passes the finite identity to the limit. Higher restrictions use the same bounded coordinate multiplier and the common-domain higher state inverse.

Physical conjugation gives \(\mathcal A_{-n}=\overline{\mathcal A_n}\) on real states. An independent way to fix any branch constant is to conjugate (20): the two fields agree, the original low form has zero kernel, and both functions vanish at the background. Therefore \(H_d\) is real when \(d_{-n}=\overline{d_n}\).

### 8.3 Whole-core Hamilton flows and actual orbit transitivity

On the full core phase, (23) is exactly
\[
\dot a=\dot t=\dot s=0,\qquad \dot q=-Ld .
\tag{24}
\]
It is a fixed, globally defined Hamiltonian family for all neighboring actions, unlike §6's pointwise \(B(J)^{-1}\) choice. Its low-state actual flow is
\((w,z)\mapsto(w e^{-Ld\tau},z e^{Ld\tau})\), and its core flow is bounded translation of \(q\). Both are ordinary Banach analytic local flows. They preserve every physical integral in the above commuting list.

Fix two sufficiently close core points with the same \(a\). Put \(J=J^*e^a\) and
\[
\tau=t_1-t_0,\qquad
\sigma=s_1-s_0+2\eta(J)\tau,\qquad
d=-\frac{q_1-q_0-r(J)\tau}{L}.
\tag{25}
\]
First apply the original \(H\) flow for time \(\tau\), then translation for time \(\sigma\), then the \(H_d\) flow for time one. Formulas (13), (24) show that the result is exactly the second point. For a sufficiently small local level piece all paths stay in the core box. The flows commute, so their ordering is immaterial.

Thus each local regular common level is an actual orbit of the **whole-core Hamiltonian family**
\[
\{H,\ P,\ H_d:d\in\mathcal B\}.
\tag{26}
\]
It is not merely the closure of finitely many velocities. The infinite bounded profile \(d\) is a genuinely defined Hamiltonian and an actual flow parameter.

The low order-zero fields (23) commute with every fixed \(C_j\). The already proved strong transport lemma therefore also keeps their flows in the same old \(\mathcal S_\infty\) whenever the starting state belongs to it. This resolves the bounded-component orbit issue there. It still does not put the whole variable-action core ball into \(\mathcal S_\infty\).

## 9. Resulting local weak Liouville theorem and its domain

Assume the reduced common-domain state inverse and actual Poisson theorem, the additional small-background frequency domain and exact normalization (4), the chart reality (3), and a real nonzero-action strong base as in §1. Then the explicitly defined \(\mathcal P_{\rm core}\), with its declared real Banach topology, has all of the following properties:

1. It consists of actual original physical smooth fields, with two unrestricted infinite bounded-sequence coordinates and two independent real heat/translation coordinates.
2. The pullback of the **original** physical form (15) is smooth, closed and weakly nondegenerate. Phase and ordinary common-level tangent evaluations are injective.
3. The actual noncentral spectral actions define the split submersion (11). Each local common level is an ordinary regular Banach submanifold, its actual tangent is the common differential kernel, and that tangent equals its original-form orthogonal inside the phase.
4. The original DLW field, arbitrary-\(\Gamma(t)\) reconstruction by translation, each fixed realified trace/action field, and the whole family (23) have genuine local flows on this phase. Each fixed finite list has a common time box.
5. Each sufficiently small common level is an actual Hamilton orbit of (26), as shown by the exact finite composition (25). All these Hamiltonians commute with the spectral actions. The bounded-coordinate flows are solved by quadrature; no infinitely supported formal time vector is substituted for an actual flow.

This is a local weak Liouville theorem for the original \(M=2\) flow **on this specified phase**. It is conditional exactly on the analytic chart, reality and original-time frequency inputs stated above. It is not a theorem on every smooth physical Cauchy datum, not a finite-mode family, and not an all-\(M\) action inverse.

The fixed-action component through \(x_*\) and its bounded Hamilton orbits are legitimate parts of the old strong domain. Whether the whole variable-action core admits all higher auxiliary \(C_j\) as positive-window actual flows on one strong presentation remains open; the present original-flow phase makes no such claim. Likewise this theorem does not identify the larger inherited \(\mathcal S_\infty\) common level with this regular level.

## 10. Both original physical lattice fields remain free and intrinsically coupled

This section fixes the lattice reconstruction explicitly; the two fields are not recovered by imposing a frozen-field relation. For \(M=2\), let
\[
\delta=hc/8,\qquad S=2\delta,\qquad c=4S/h,\qquad
2B(t)=\Gamma(t)/c.
\]
The actual closure in the free source coordinates is
\[
d_0=\delta+v,\quad d_1=\delta-v,\quad
b_1=B-(\delta+v)u/S,\quad b_0=b_1+u.
\]
Since \(U_j=2b_j\) and \(w_j=8d_j/h\), the original physical fields are
\[
\boxed{\begin{aligned}
U_0&=2B+(1-2v/S)u,&
U_1&=2B-(1+2v/S)u,\\
w_0&=8(\delta+v)/h,&
w_1&=8(\delta-v)/h.
\end{aligned}}
\tag{27}
\]
In particular \(U_0-U_1=2u\), \((w_0+w_1)/2=c\), and direct multiplication gives
\[
\frac{U_0w_0+U_1w_1}{2}=2Bc=\Gamma(t).
\]
Thus (27) satisfies the original prescribed average flux exactly. The free variables still obey their fixed source means \(\langle u\rangle=\langle v\rangle=0\); no additional condition \(U_0\equiv0\) or \(U_1\equiv0\) was imposed.

Substitution in the original second equation gives the \(v\) equation below. For the first equation at \(j=0\), use
\[
\delta_-U=2u/h,\quad M_-w=c,\quad
U_0^2-U_1^2=8Bu-8u^2v/S,\quad
w_0^2-w_1^2=256\delta v/h^2.
\]
Multiplication by \(h/2\) yields the other equation:
\[
\boxed{\begin{aligned}
u_t&=-u_{xx}-2S v_x+\frac2S D(u^2v)-2B(t)u_x,\\
v_t&=v_{xx}-\frac S2 u_x+\frac2S D(uv^2)-2B(t)v_x.
\end{aligned}}
\tag{28}
\]
The linear cross derivatives and the two nonlinear products give intrinsic coupling even in the centered case \(B=0\). Arbitrary \(B(t)\) only adds the common translation velocity \(-2B(t)=-\Gamma(t)/c\). It is not the source of the two independent field freedoms.

On the centered chart shrink the low neighborhood so that \(\|v\|_\infty<|S|/4\). Then \(U_0\equiv0\), or \(U_1\equiv0\), would force \(u\equiv0\), because the two factors multiplying \(u\) in (27) are nowhere zero. The core has ordinary open subboxes excluding this possibility. To prove this without a finite-mode ansatz, repeat §5.1 in any high \(h^r\) norm: finite-support Cartesian tangents are dense in \((h^r)^2\), and the derivative of the higher state inverse is an isomorphism onto \(H^r_0\times H^{r+1}_0\). Therefore physical core tangent images are dense in that mixed space. For sufficiently large \(r\), evaluation of \(u(x_0)\) and \(v_x(x_1)\) is continuous. A smooth mean-zero test pair can assign both evaluations nonzero values; a finite-support core tangent approximates it and preserves both nonzero tests.

If either evaluation initially vanishes, a sufficiently small displacement along such a legitimate core parameter direction makes both nonzero; the finitely many possible zero parameters can be avoided. Around the resulting core point one can take an ordinary open parameter subbox on which
\[
|u(x_0)|>\varepsilon_1,\qquad |v_x(x_1)|>\varepsilon_2
\]
for positive \(\varepsilon_1,\varepsilon_2\). All the regular geometry and local Hamilton flows proved above restrict to this subbox. Both \(U_0,U_1\) are nonzero functions and \(v\) is nonconstant there. This restriction uses no varying external flux and retains both infinite sequence coordinates.

At a point with \(u(x_0)\ne0\), the local field reconstruction even has
\[
\det\frac{\partial(U_0,U_1)}{\partial(u,v)}
=-\frac{4u(x_0)}S\ne0.
\tag{29}
\]
Accordingly the physical changes of the two \(U\) components arise from independent changes of \(u,v\), rather than from a constant gauge unlock. The bounded \(a/q\) coordinates vary the actual action and phase data of the fields.

Finally the original flow on this phase is neither static nor a rigid spatial translation. Every \(J_n\ne0\) implies both \(w_n,z_n\ne0\). Static motion would require \(\Omega_{H,n}=0\) for all \(n\), whereas (4) has quadratic leading term \(-k_n^2\). Rigid translation would require \(\Omega_{H,n}=i\kappa k_n\) for one constant \(\kappa\), again incompatible with (4) on the infinite set of active indices. This is a genuinely infinite-field, coupled original DLW phase with the specified stronger topology; it remains subject to the small-background and analytic source-domain conditions of §1.
