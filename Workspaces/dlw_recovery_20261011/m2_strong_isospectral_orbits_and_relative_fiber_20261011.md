# M=2: actual strong isospectral orbits, a bounded relative fiber, and the growing-angle obstruction

2026-10-11. Independent continuation of the regular-fiber problem. No previous checks were executed. This note proves an infinite-function orbit statement and a ghost-free **bounded relative component** with a declared topology. It does not identify that component with the full inherited common level, and does not assert a regular full weak-symplectic phase.

Dependencies are the actual [reduced state chart](akns_physical_state_inverse_bridge_20261011.md), [physical trace push-forward](m2_physical_trace_poisson_closure_proof_20261011.md), [actual strong-flow bridge](spectral_m2_strong_domain_flow_bridge.md), the strong construction in [mixed §16](../../刘维尔可积性/research/mixed_independent_review_20261011.md), and the new [physical cross-operator proof](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md), §§1–6. The latter's uniform order-two budget and same-action tests were independently read: the gradient budget is \(H^2\times H^1\), the original tensor returns \(L^2_0\times H^1_0\), and the deliberately prescribed test coordinate, rather than an actual tiny gap, is divided out.

Throughout, all existing small-background/low-chart, central-root and central-angle hypotheses remain in force. Centered spectral parameters do not set the physical \(\Gamma(t)\) to a constant. Write the complexified reduced state coordinates as
\[
W=(w_k,z_k)_{k\ne0}\in s^2,\qquad
s=\bigcap_{r\ge0}h^r,\qquad J_k=w_kz_k.
\]
Let \(x_*\) be an actual strong state in this chart with every \(J_k^*\ne0\), as supplied by the already established same-parameter Baire construction. Fixed-action formulas below are complexified statements. Actual real states are obtained only on the fixed set of the transported physical anti-involution; no standard NLS reality is presumed.

## 1. Constant-on-fiber velocities for the actual hierarchy

The exact fixed-original-parameter trace identity gives, in the logarithmic convention
\[
\dot w_k=v_k(J,\lambda)w_k,\qquad
\dot z_k=-v_k(J,\lambda)z_k ,
\tag{1}
\]
where \(v_k\) is a pure-action function. Indeed the full standard angular coefficient is the difference
\(\partial_{I_k}d-\partial_{I_0}d\), multiplied by the physical scalar
\((S^2-\lambda^2)/(16S)\) and the specified \(L,i\) factors. The central constraint \(I_0=\rho(J)\), holonomy \(\eta=\widetilde\eta(J)\), and original fixed-\(\lambda\) shift are retained. This is not the derivative of the reduced functional with respect to \(J_k\).

This property passes to the actual \(C_j\), rather than only to a formal Laurent series. At sufficiently large positive real \(\lambda\), the actual quasimomentum is
\[
\mathcal K_\lambda
=\operatorname{arcosh}(F_\lambda/2)+\frac L2\eta-\frac L2\lambda ,
\qquad
X_{\mathcal K_\lambda}
=\frac{X_{F_\lambda}}{2\sinh\ell_\lambda}
 +\frac L2X_\eta .
\tag{2}
\]
Here the branch is the isolated actual fast multiplier and \(\ell_\lambda=\operatorname{arcosh}(F_\lambda/2)\). All scalar coefficients, and the translation angular coefficients of \(X_\eta\), are pure-action functions.

For every fixed \(N\), the actual Riccati construction provides
\[
\mathcal K_\lambda=-\sum_{j=1}^{N}C_j\lambda^{-j}
 +O_{C^1}(\lambda^{-N-1})
\tag{3}
\]
on a sufficiently high but finite Sobolev source ball. To extract one fixed angular component, apply the actual \(C^1\) remainder to the actual finite-coordinate angular covector followed by the original physical tensor. The common-domain state-chart transpose has a fixed finite loss; increasing the source Sobolev index by that loss makes this a legitimate source tangent. Equivalently, apply (3) along that fixed finite-coordinate Hamilton direction. The remainder is then still \(O(\lambda^{-N-1})\).

Compare two smooth points of the same action fiber. The entire expression (2) has the same angular component at both points. Successive multiplication by powers of \(\lambda\) and taking \(\lambda\to+\infty\) in (3) shows that every coefficient has the same angular component. Actual commutation with all \(I_k\) supplies the opposite \(w,z\) torques. Thus for each actual \(C_j\) there is a sequence \(c_{j,k}(J)\) such that
\[
\boxed{\quad
D\mathcal R X_{C_j}
=(c_{j,k}(J)w_k,-c_{j,k}(J)z_k)_{k\ne0}.
\quad}
\tag{4}
\]
This proves pure-action dependence componentwise with finite regularity and an actual remainder. It asserts no uniform-in-\(j\) polynomial asymptotic. The same conclusion for fixed traces and fixed contour actions follows directly from their exact formulas. The translation field can be added to this countable list.

In particular, on a true finite joint \(C_j\) orbit of \(x_*\), its reduced coordinates are exactly
\[
w_k(t)=w_k^*\exp\!\left(\sum_{j=1}^{N}t_jc_{j,k}(J^*)\right),
\qquad
z_k(t)=z_k^*\exp\!\left(-\sum_{j=1}^{N}t_jc_{j,k}(J^*)\right).
\tag{5}
\]
Equation (5) is deduced from existing actual solutions by the coordinate ODE. It is not a substitution of a formal hierarchy for actual solutions.

## 2. The exponential margin follows from existing complex joint germs

Choose positive complex-axis radii \(\rho_j\) of the strong presentation, shrinking successively if necessary so that all its finite-prefix images stay in one reduced low chart. For each finite \(N\), the closed smaller polydisc \(|t_j|\le\rho_j/2\) is compact and its actual image is bounded in every \(h^r\).

Put \(d_k=|w_k^*|+|z_k^*|\) and
\[
a_j=\frac{\rho_j}{8\sqrt2},\qquad
p_N(k)=\sum_{j=1}^{N}a_j|c_{j,k}(J^*)|.
\]
For each complex number \(c\), one of \(t=\pm\rho_j/2,\ \pm i\rho_j/2\) satisfies
\(\operatorname{Re}(tc)\ge\rho_j|c|/(2\sqrt2)\). Select such a corner separately for the \(w\) and \(z\) estimates. There are only \(4^N\) corners, all of which are actual solution points in that closed polydisc. From (5),
\[
\boxed{\quad d_k e^{4p_N(k)}\in s
\quad\text{for every finite }N.\quad}
\tag{6}
\]
The corner may depend on \(k\); taking the maximum of finitely many rapidly decreasing sequences preserves rapid decrease. This proves the needed exponential margin without a leading-symbol asymptotic, without an infinite simultaneous-time vector, and without claiming endpoint smoothness implies analyticity.

For completeness a single admissible growing weight can be chosen. Select increasing integers \(K_N\ge N\) so that, for \(|k|\ge K_N\),
\[
\langle k\rangle^N d_ke^{4p_N(k)}\le2^{-N}.
\]
Let \(N(k)=\max\{N:K_N\le|k|\}\), taking \(N(k)=0\) before the first threshold, and set
\[
g_k=\max\{1,p_{N(k)}(k)\}.
\tag{7}
\]
Then
\[
d e^{4g}\in s,\qquad
L_j:=\sup_k\frac{|c_{j,k}(J^*)|}{g_k}<\infty
\quad\text{for every fixed }j.
\tag{8}
\]
To verify the first statement, fix \(r\); in the tail where \(N(k)>r+2\), the displayed threshold estimate controls the \(h^r\) summand by a summable polynomial. The finite head is harmless. To verify the second, for \(|k|\ge K_j\), \(g_k\ge a_j|c_{j,k}|\); the remaining finite head is bounded and \(g_k\ge1\).

One may include any countable list of previously actual complex joint-germ axes in the same diagonal construction. No common radius or estimate over the entire hierarchy is required.

## 3. A genuine infinite-function bounded relative fiber inside the strong domain

Consider
\[
\mathscr P(q)_k=(w_k^*e^{q_k},z_k^*e^{-q_k}),
\qquad q\in\ell^\infty,\quad \|q\|_\infty<\varepsilon .
\tag{9}
\]
For \(\varepsilon<\pi/2\), this is locally injective: equality forces every \(q_k-\widetilde q_k\in2\pi i\mathbb Z\), whereas its absolute value is less than \(\pi\). It is analytic into every \(h^r\), since multiplication by the fixed rapid base controls all derivatives. Shrink \(\varepsilon\) once so that the image stays in the reduced low state chart.

This family has actual joint hierarchy germs. With \(q\) fixed, replace \(w_k^*,z_k^*\) in (5) by (9); the same pure-action coefficients \(c_{j,k}(J^*)\) apply. Multiplication by \(e^{\pm q}\) preserves every \(h^r\) bound of each known finite joint polydisc. The low chart can be retained for all finite prefixes by shrinking the old axes successively, with a summable low-norm variation budget. On each finite rectangle this formula differentiates in every \(h^r\) and satisfies exactly the actual physical \(C_j\) equations by (4). It also satisfies the centered original DLW equation, whose Hamiltonian is the already audited linear combination of \(C_1\) and a constant, with translation restoring arbitrary \(\Gamma(t)\).

Here is the strong-membership step, which is separate from formal agreement of vector fields. An actual finite joint complex rectangle gives the mixed source corners by the prescribed endpoint evaluations for its old axes. Evaluation and the previous lift operations are smooth maps of the joint solution; differentiating the rectangle shows that these corners solve the corresponding lifted auxiliary equation. Mixed uniqueness therefore identifies the corner-center map with the constructed \(E_j\), exactly. Recursing gives coherent source arrays.

For a whole bounded \(q\) ball, the source data needed at each finite stage have uniform bounds in its required, finite Sobolev norm. In fact its image in every smooth-field norm is relatively compact: the finitely many head coordinates are bounded, and the rapid tails are uniform; multiplication by bounded \(e^{\pm q}\) preserves this property. The same is true jointly with a fixed finite closed time rectangle. Consequently each next mixed contraction and source-chart domain can be chosen uniformly on this compact source family by taking that axis short enough. The old axes remain positive and fixed after each such choice. This supplies one strong presentation locally for every finite-dimensional smooth \(q\)-family. It proves that \(\mathcal R^{-1}\mathscr P(q)\) lies in the complexified \(\mathcal S_\infty\), and that these finite-dimensional families are legitimate strong plots.

This argument uses the actual finite rectangles to provide exact corners. It does not claim that a smoothing center map is onto arbitrary nearby physical data.

Give the image of (9) its **bounded-relative Banach topology and smooth plots**, transported from the small \(\ell^\infty\) ball. This is an infinite-function integral manifold. Its tangent is
\[
T_q\mathscr P=\{(v_kw_k,-v_kz_k):v\in\ell^\infty\}.
\tag{10}
\]
The state derivative is injective because every \(w_k,z_k\ne0\). Its internal tangent has no ghost: the ordinary Banach tangent is obtained from lines; addition combines a finite sum of plot directions; a zero-first-derivative curve has a Banach-valued Hadamard factorization and hence gives zero internal direction. The physical evaluation differential remains injective by the state-chart derivative.

All actions are constant on (9), so the original physical form restricts to zero, by the already proved common-kernel isotropy. Thus (9) is a ghost-free immersed isotropic integral manifold in the same strong physical domain with the stated admitted plots.

Its topology is deliberately specified. For a fixed small \(r>0\), \(q^{(n)}=r e_n\) has \(\ell^\infty\) norm \(r\), while its Cartesian and physical images converge to the base in every ambient smooth seminorm. The inverse chart is therefore not continuous for the inherited ambient topology. No regularity of the full subset-diffeological common level follows from this construction.

## 4. Exact actual Hamilton orbits of this bounded component

Assume in addition that \(J^*\) lies in the small \(\ell^1_4\) ball of the independently read cross-operator theorem. In its convention
\[
B(J^*):\ell^\infty\longrightarrow\mathcal V_2
\quad\text{is an isomorphism},\qquad
\mathcal V_2=\{a:\sup|a_k|/\langle k\rangle^2<\infty\}.
\]
For any bounded relative velocity \(v\), set
\[
c=B(J^*)^{-1}(-iv)\in\ell^\infty,\qquad
H_c=\sum_{k\ne0}c_kI_k.
\tag{11}
\]
This is a genuinely defined analytic Hamiltonian on the low Cartesian state chart; its physical smooth differential and field are obtained with the original tensor. Its actual torque is \(iB(J^*)c=v\). At every point of the fixed-action component the same identity holds, because \(B\) depends only on \(J\).

Therefore
\[
q(t)=q(0)+tv
\tag{12}
\]
is an actual local \(H_c\) flow, in the physical state chart and in the strong bounded component. This is an explicit solution of the true vector field, even though that field loses two derivatives on an unrestricted Sobolev Cauchy problem. For a finite list of bounded \(v\)'s the flows commute and have a common actual time box inside the bounded chart.

Every sufficiently close point of (9) is reached from every other by (12), choosing \(v=q_1-q_0\), time one, and the corresponding (11). Hence the bounded component is an actual Hamilton orbit for a stated family of genuinely defined spectral Hamiltonians, with full infinite \(\ell^\infty\) function freedom. This is stronger than only a closure of finite action velocities.

It does not assert that each \(H_c\) has an ordinary low-Sobolev Cauchy flow on an open physical neighborhood. Nor does it assert that its coefficients define an already proved real Hamiltonian: that requires taking the transported physical real structure into account.

## 5. The larger hierarchy orbit is real, but its weighted parameter space is a cover

Let \(E_g=\{q:\sup|q_k|/g_k<\infty\}\), with \(g\) from (7). The exponential map (9) is analytic \(B_{E_g}(0,R)\to s^2\) for any fixed \(R<4\). For its \(m\)-th derivative use
\[
g_k^m\le m!\sigma^{-m}e^{\sigma g_k},\qquad R+\sigma<4,
\]
and (8). This gives uniform convergence of the Banach power series into each \(h^r\). The low chart is retained by taking one smaller radius.

Every \(c_j(J^*)\) belongs to \(E_g\) by (8). Thus
\[
q\longmapsto q+t_jc_j(J^*)
\tag{13}
\]
gives actual local \(C_j\) solution formulas. For any finite list choose its time radii so that the sum of \(|t_j|L_j\) remains below the available radius. Positive fixed radii for all finite prefixes can be chosen, for example from a summable \(2^{-j}\) budget. The same mixed-corner reconstruction as in §3 applies, with uniform rapid bounds supplied by \(d e^{4g}\); finite-dimensional parameter families are strong plots.

This gives an actual infinite-function joint-hierarchy orbit presentation. It uses only finite time lists and makes no claim about a countably infinite simultaneous-time vector.

But if \(g_k\to\infty\) along a subsequence, its period vectors satisfy
\[
2\pi i e_k\ne0,\qquad
\|2\pi i e_k\|_{E_g}\to0,\qquad
\mathscr P(2\pi i e_k)=\mathscr P(0).
\tag{14}
\]
Therefore (9) is not locally a state inverse on this weighted parameter space. Imaginary branch strips have empty interior. The additive kernel is closed but nondiscrete, so the quotient is not supplied with Banach local charts by the exponential projection. The growing-angle construction proves true physical solutions and a group-orbit presentation; it does not prove a regular fiber or a ghost-free internal tangent for the quotient.

If this weight happens to remain bounded, §3 already applies and the period issue does not arise. The obstruction is precisely the use of an unbounded allowed coordinate amplitude.

## 6. What was settled, and what still prevents a full regular-level theorem

The established additions are (i) actual pure-action hierarchy torques, extracted using the actual \(C^1\) expansion; (ii) exponential margins directly from the known complex germs; (iii) a ghost-free bounded relative integral manifold with actual Hamilton transitivity; and (iv) an actual larger hierarchy-orbit cover, with its exact period obstruction.

The bounded relative component removes velocities whose ratios \(\delta w_k/w_k=-\delta z_k/z_k\) are unbounded. For example the caution's \(w_k=z_k=e^{-k^2}\), velocity \((e^{-k},-e^{-k})\), has ratio \(e^{k^2-k}\) and is excluded. The removed velocities are exactly why its tangent can be genuinely integrated without the caution's second-derivative contradiction.

The original DLW and translation angular profiles can grow in \(k\); they are represented by §5 and by the already verified actual germs, but need not be tangent to §3's bounded Banach component. A full phase with variable actions, a locally injective topology containing those velocities, the transported original real slice, nondegeneracy of the original form on that phase, and an ordinary regular common-level submersion remain to be proved. In particular this note does not turn the full inherited \(\mathcal S_\infty\) fiber into a regular leaf.

A precise next candidate is to separate bounded compact angles from the real hyperbolic original-DLW direction and the translation direction. If the real DLW profile has an unbounded real part comparable to \(k^2\), a period equality forces its real-time coefficient to vanish; translation periods can then be controlled by first finite differences. This avoids putting an entire unbounded **complex** angle ball into the model. Its reality, variable-action continuation and weak-symplectic pairing must still be checked. A countable LF extension using finite hierarchy-time coefficients is another candidate only after its lattice and model-space conditions are proved; it is not asserted here.
