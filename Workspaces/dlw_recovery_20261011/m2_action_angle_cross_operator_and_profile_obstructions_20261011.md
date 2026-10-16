# M=2: the physical action–angle cross operator and relative-profile obstructions

2026-10-11. New analytic argument; no old symbolic certificate was rerun. This note uses the exact physical trace push-forward and the common-domain reduced Cartesian state chart already proved in [the trace bridge](m2_physical_trace_poisson_closure_proof_20261011.md) and [the state inverse](akns_physical_state_inverse_bridge_20261011.md). It does not identify the physical tensor with the NLS tensor.

The new conclusion below is an invertible physical cross operator on a specified sequence scale. It strengthens closed-span generation to exact generation of every angular velocity of at most quadratic growth by a genuine bounded-coefficient spectral Hamiltonian. It does not by itself produce a regular infinite common-level manifold or a flow of that Hamiltonian in the old strong domain.

## 1. Conventions and exact pure-action angular velocities

Use all the small-background, central-section, and common low-chart hypotheses of the state inverse. Noncentral reduced coordinates are
\[
W=(w_n,z_n)_{n\ne0},\qquad J_n=w_nz_n,\qquad
I_0=\rho(J),\qquad \eta=\widetilde\eta(J).
\]
The noncentral background is \(W=0\), whereas \(I_0^*=-L^2S^2/4\ne0\). The fact that the noncentral Cartesian pairs vanish at this complex constant background has already been justified by the holomorphic continuation argument in the state inverse, §4.4–4.5.

For a nonzero pair set
\[
\vartheta_n={1\over2i}\log(w_n/z_n),\qquad
\alpha_n=\vartheta_n-\vartheta_0.
\]
Thus the full standard action field satisfies
\[
X^{\rm std}_{I_m}\vartheta_n=-\delta_{nm}.
\]
This sign follows from \(X^{\rm std}_{I_m}w_m=-iw_m\), \(X^{\rm std}_{I_m}z_m=iz_m\). In particular it must be retained when comparing an angle convention with another paper.

Write the full discriminant factorization as
\[
\Delta(\zeta_{\rm unit},I)=d(\zeta_{\rm unit},I),\qquad
\lambda(J,\zeta_{\rm unit})=\widetilde\eta(J)-{2i\zeta_{\rm unit}\over L},
\quad \omega_\lambda={S^2-\lambda^2\over16S}.
\]
Here the unit spectral variable is denoted \(z\) below to avoid long subscripts. The exact trace identity is
\[
D\mathcal R\,X_{F_\lambda}=\omega_\lambda\Pi Y_{\lambda-\eta},
\qquad Y={L\over i}X^{\rm std}.
\tag{1}
\]
For fixed original \(\lambda\), its reduced angular velocity is therefore
\[
\dot\alpha_n=iL\omega_\lambda
 \left(\partial_{I_n}d-\partial_{I_0}d\right)
 \left({iL(\lambda-\widetilde\eta(J))\over2},\,\rho(J),J\right).
\tag{2}
\]
All entries in (2) depend only on \(J\). This is the projected **full** standard derivative; it is not the reduced derivative
\(\partial_{J_n}(d(\rho(J),J))\).

The previously proved physical contour formula gives
\[
B_{nm}(J):=d\alpha_n(X_{I_m}^{\rm phys})
=-{iL\over\pi}\oint_{\Gamma_m}
 {\omega_{\lambda(J,z)}\left(\partial_{I_n}d(z,I)-\partial_{I_0}d(z,I)\right)
  \over R(z,I)}\,dz,\quad I=(\rho(J),J).
\tag{3}
\]
The source-dependent holonomy term in \(dI_m\) has zero contour integral; this is the actual winding cancellation proved in the action bridge. Thus (3) includes the complete physical field.

Equation (3) is holomorphic in \(J\) for each fixed pair \(n,m\) on the existing common action domain. Every finite linear combination of physical action fields has pure-action angular velocity. The corresponding Cartesian torque is
\[
(X_{H_c}^{\rm phys})_{w_n}=iw_n(B(J)c)_n,\qquad
(X_{H_c}^{\rm phys})_{z_n}=-iz_n(B(J)c)_n,
\quad H_c=\sum_{m\ne0}c_mI_m.
\tag{4}
\]
For initially finite \(c\), (4) follows directly from (3). It extends across zeros of any pair: action commutation forces the \(w_n\) component to vanish whenever \(w_n=0,z_n\ne0\), and holomorphic continuity covers \(w_n=z_n=0\). Holomorphic division by \(w_n\), and similarly by \(z_n\), then extends the torque coefficient. The coefficient depends only on \(J\), by (3) and the identity theorem. This extension permits the same-action tests in §4; they do not require all tested pairs to be nonzero.

## 2. Exact background diagonal

At the constant background,
\[
d_*(z)=2\cos\sqrt{z^2+L^2\delta^2},\qquad
z_n^*=\operatorname{sgn}(n)\sqrt{\pi^2n^2-L^2\delta^2}\quad(n\ne0),
\]
with the fixed contour labels of the state inverse. Since
\(\lambda_n^*=-2iz_n^*/L\), one has
\[
\omega_{\lambda_n^*}
={S^2+4(z_n^*)^2/L^2\over16S}
={k_n^2\over16S},\qquad k_n={2\pi n\over L}.
\tag{5}
\]

Here is a contour calculation of the derivative, without guessing from an open gap. Put
\[
P_\eta(z)={S^2-\eta^2\over16S}z
          +{i\eta\over8SL}z^2+{1\over12SL^2}z^3,
\quad P_\eta'(z)=\omega_{\eta-2iz/L},
\]
and define, with \(\eta\) held fixed while differentiating the full actions,
\[
K_m^\eta(I)={1\over\pi}\oint_{\Gamma_m}
P_\eta(z){\partial_zd(z,I)\over R(z,I)}\,dz.
\]
Contour integration by parts gives
\[
d_IK_m^\eta=-{1\over\pi}\oint_{\Gamma_m}
{\omega_{\eta-2iz/L}\,d_Id(z,I)\over R(z,I)}\,dz.
\tag{6}
\]
At the background \(R_*(z)\) has a simple zero at the collapsed noncentral gap \(z_m^*\). Therefore, for every full action variation, the residue in (6) equals
\(\omega_{\lambda_m^*}\,dI_m\); the unweighted residue is precisely the defining action variation. Consequently
\[
\partial_{I_n}K_m^0(I^*)=\omega_{\lambda_m^*}\delta_{nm},
\quad\partial_{I_0}K_m^0(I^*)=0\quad(m\ne0).
\]
Equations (3) and (6) prove
\[
\boxed{B_{nm}(0)=D_n\delta_{nm},\qquad
D_n={iLk_n^2\over16S}.}
\tag{7}
\]
In the stated angle convention this is \(iL\), not \(L/i\), times the real weight. The latter appears in the trace **field** before taking its negative canonical angular derivative.

## 3. The analytic order-two field bound that is available

Let \(h^N\) denote the usual two-sided noncentral weighted \(\ell^2\) space. On a sufficiently small \(h^2\) ball about \(W=0\), the physically pushed tensor is an analytic bounded-operator map
\[
\mathbb J(W):h^2\times h^2\longrightarrow h^0\times h^0.
\tag{8}
\]
This is a stronger, locally uniform version of the fixed-smooth-state transpose estimate in the trace bridge §4.4. The budget can be checked directly:

* The inverse state chart sends \(h^2\times h^2\) analytically to \(u\in H^2_0,\ v\in H^3_0\).
* The KLTZ transpose, obtained from its auxiliary canonical identity and the analytic inverse derivative, preserves \(H^2\). Balancing, rescaling, and the central-angle normalization contribute constant operators or finite-rank terms.
* The physical potential transpose sends an \(H^2\) potential covector to physical gradients in \(H^2\times H^1\). Its sole differential entry is \(D/S\); the remaining coefficients depend analytically on \(u\in H^2,v\in H^3\), and its primitive terms gain a derivative.
* The actual \(J_{uv}=-\operatorname{offdiag}(D)/16\) sends those gradients to \(L^2_0\times H^1_0\). The low derivative of the forward state chart then maps this mixed space to \(h^0\times h^0\).

The bounded operators in each step depend analytically on \(W\) in the \(h^2\) ball. Hence, after shrinking that ball once, there is \(C\) such that
\[
\|\mathbb J(W)-\mathbb J(0)\|_{\mathcal L((h^2)^2,(h^0)^2)}
\le C\|W\|_{(h^2)^2}.
\tag{9}
\]
This argument uses the actual physical tensor in the final steps. It does not borrow auxiliary NLS canonicity as a physical bracket.

For any \(c\in\ell^\infty\), \(H_c(W)=\sum c_mw_mz_m\) is a genuinely defined holomorphic Hamiltonian on the low \(h^0\) chart. Its Cartesian differential is
\[
d_WH_c=(c_mz_m,c_mw_m)_m,
\qquad \|d_WH_c\|_{(h^2)^2}\le\|c\|_\infty\|W\|_{(h^2)^2}.
\]
Thus its actual physical field, transported to reduced coordinates, exists on the \(h^2\) chart and satisfies
\[
\left\|X_{H_c}(W)-\mathbb J(0)d_WH_c\right\|_{(h^0)^2}
\le C\|c\|_\infty\|W\|_{(h^2)^2}^2.
\tag{10}
\]
For finite \(c\), the linear term is exactly the torque with diagonal (7). For bounded \(c\), finite truncations converge after multiplication by \(W\) in \(h^2\); application of (8) extends both this identification and (4). More explicitly, define \((B(J)c)_n\) as the coordinatewise limit of the finite-coefficient torques at a same-action test with its prescribed \(w_n\ne0\). This definition does not presuppose absolute summability of a matrix row. Pure-action dependence and the convergent physical fields identify the same coefficient at every other representative with that \(J\). No norm convergence of the bare truncations in \(\ell^\infty\) is asserted.

## 4. No division by a tiny actual gap: uniform same-action tests

Set \(\langle n\rangle=1+|n|\), and introduce the action norm
\[
\|J\|_{\ell^1_4}=\sum_{n\ne0}\langle n\rangle^4|J_n|.
\]
Fix a small \(r>0\), and assume \(\|J\|_{\ell^1_4}\le r^2\). For each index \(n\), choose a same-action test state as follows:
\[
w_n^{(n)}=r\langle n\rangle^{-2},\quad
z_n^{(n)}=J_n\langle n\rangle^2/r,
\]
while for \(m\ne n\) choose either complex square root and set
\[
w_m^{(n)}=z_m^{(n)}=\sqrt{J_m}.
\]
Only existence and the norm of this test are used; this is not a holomorphic choice of square roots. Its reduced \(h^2\) norm is bounded by a fixed multiple of \(r\), uniformly in \(n\). Indeed the two special weighted coordinates have absolute values at most \(r\), and the other weighted squared norms sum to at most \(2r^2\).

Fill the central pair by \(I_0=\rho(J)\) and the same fixed central-angle section. For all sufficiently small \(r\), every test lies in the same reduced low state chart and the \(h^2\) ball used in (8)–(10). The full tensor estimate and all domain radii are uniform in the tested index.

Pure-action dependence makes the torque coefficient at the test equal to its coefficient at the original state, even if the latter has an arbitrarily small \(w_n\). Apply (10) to the \(w_n\) component of the test and divide by the deliberately prescribed non-tiny coordinate. This proves
\[
\boxed{\sup_{n\ne0}{|(B(J)c)_n-D_nc_n|\over\langle n\rangle^2}
\le C_1r\|c\|_\infty.}
\tag{11}
\]
This is a uniform operator estimate, rather than a separate bound for each fixed action. It follows entirely from the analytic physical order-two tensor and pure-action torque.

## 5. Exact cross-operator inverse and the scope of exact generation

Let
\[
\mathcal V_2=\{v:\ \sup_{n\ne0}|v_n|/\langle n\rangle^2<\infty\}.
\]
The diagonal \(D:\ell^\infty\to\mathcal V_2\) in (7) is a bounded isomorphism because \(S\ne0\) and \(n\ne0\). From (11),
\[
\|D^{-1}B(J)-1\|_{\mathcal L(\ell^\infty)}
\le C_2r.
\]
Choose the single \(r\) so that \(C_2r<1\). Then
\[
\boxed{B(J):\ell^\infty\longrightarrow\mathcal V_2
\text{ is a bounded isomorphism},\qquad
B(J)^{-1}=(1+D^{-1}(B-D))^{-1}D^{-1}.}
\tag{12}
\]
In particular every prescribed \(v\in\mathcal V_2\) is the exact angular velocity of the genuine Hamiltonian \(H_c\) at that state, with \(c=B(J)^{-1}v\in\ell^\infty\). This removes a closure from **this specified angular sequence scale**. It says neither that every ambient rapid Cartesian kernel velocity has such a coefficient nor that \(X_{H_c}\) has a local Banach Cauchy flow in the old strong domain. The field (8) has loss two, while the previously proved individual compact-contour action fields have order zero.

The statement just made is on the complexified smooth physical leaf. There is also an intrinsic real restriction, without assigning the Cartesian chart a standard NLS real type. At a real physical state with every \(J_n\ne0\), set \(c^\#_n=\overline{c_{-n}}\). The proved relation \(I_{-n}=\overline{I_n}\), the reality of the original tensor, and the convergent finite truncations imply
\(\overline{X_{H_c}}=X_{H_{c^\#}}\).
Let \(\mathcal V_2^{\rm phys}(x)\) consist of those \(v\in\mathcal V_2\) for which the Cartesian torque \((iw_nv_n,-iz_nv_n)_n\), pulled back by \(D\mathcal R_x^{-1}\), is an ordinary real physical vector. By (12), write \(v=B(J)c\). It is real if and only if
\[
X_{H_c}=X_{H_{c^\#}}
\ \Longleftrightarrow\ B(J)(c-c^\#)=0
\ \Longleftrightarrow\ c=c^\#.
\]
The middle implication uses \(w_n,z_n\ne0\) and the last uses (12). Thus \(B(J)\) maps the closed real coefficient form \(\{c=c^\#\}\) isomorphically onto the intrinsically defined closed real angular form \(\mathcal V_2^{\rm phys}(x)\). Every member of this real form is generated by the real Hamiltonian \(H_c\). This is a tangent-space statement; it does not prove a real-invariant global profile chart or a flow domain.

At smooth states \(dH_c\) is rapid, so the original weak symplectic identity holds as an actual identity of physical smooth tangent vectors:
\[
\Omega(X_{H_c},V)=dH_c(V).
\]
Finite truncations of \(H_c\) and their fields converge at a fixed smooth state as in the trace-transpose argument. The coefficient sequence in (12) need not be a finite spectral combination.

## 6. A separate polynomial-frequency lemma

Suppose a particular actual Hamiltonian field \(X_H\), in the reduced state chart, is holomorphic \( (h^K)^2\to(h^0)^2\), has pure-action torque
\[
\dot w_n=w_n\Omega_n(J),\qquad
\dot z_n=-z_n\Omega_n(J),
\]
and is uniformly bounded on one sufficiently small \(h^K\) ball. Then on a sufficiently small \(\ell^1_{2K}\) action ball,
\[
|\Omega_n(J)|\le C_K\langle n\rangle^K.
\tag{13}
\]
Proof: repeat §4 with \(w_n=\varepsilon\langle n\rangle^{-K}\), \(z_n=J_n/w_n\), and balanced other pairs. The uniform field bound controls its \(n\)-th component; division by the prescribed test coordinate proves (13). This is an unconditional elementary implication of the stated field hypotheses. It avoids division by the actual small pair.

For a finite-order DLW local Hamiltonian field, the analytic \(h^K\to h^0\) budget follows once \(K\) exceeds its differential order and the state-chart losses. No uniform-in-\(j\) radius or common polynomial degree follows from this lemma.

### 6.1 The actual \(C_j\) expansion supplies pure-action torque

This additional step can use the already proved **actual \(C^1\)** quasimomentum expansion, rather than merely its formal Laurent series. See [spectral independent review, §14.1–14.3 and §17.1–17.3](../../刘维尔可积性/research/spectral_independent_review_20261011.md), especially (86), (92), (119), and (126).

For large positive original centered \(\lambda\), the actual simple fast multiplier of the split system gives
\[
F_\lambda=2\cosh\ell_\lambda,\quad
\ell_\lambda={L(\lambda-\eta)\over2}+\mathcal K_\lambda,\quad
\mathcal K_\lambda=-\sum_{j=1}^{N}C_j\lambda^{-j}
 +O_{C^1(H^{N+2})}(\lambda^{-N-1}).
\tag{16}
\]
The branch is fixed by the actual fast multiplier, and \(2\sinh\ell_\lambda\ne0\) for these positive parameters on the prescribed bounded source ball. Consequently
\[
X_{\mathcal K_\lambda}
={X_{F_\lambda}\over2\sinh\ell_\lambda}+{L\over2}X_\eta.
\tag{17}
\]
The first term has the pure-action torque (2). The second does also: \(\eta=\widetilde\eta(J)\) is analytic on the existing \(\ell^1\) action neighborhood, so \(d\eta=\sum\beta_ndI_n\), \(\beta\in\ell^\infty\). The bounded-coefficient field argument in §3 identifies its actual field and gives pure-action torque \(B(J)\beta\). This is consistent with the directly known translation field \(X_\eta=(u_x,v_x)/(8SL)\).

To extract a particular angular coefficient from the \(C^1\) remainder, first fix its index \(n\) at a point \(w_nz_n\ne0\). Its angular differential has a finite Cartesian covector with entries proportional to \(1/w_n,1/z_n\), together with the finite central-section correction. At a source in the mixed space \(E_{N+4}=H^{N+4}_0\times H^{N+5}_0\), the actual Hamiltonian field of this finite angular functional belongs to \(E_{N+2}\), hence to the balanced \(H^{N+2}\) space: the potential transpose loses one spatial derivative and the actual \(J\) loses one more. Apply the \(C^1(H^{N+2})\) remainder in (16) to that fixed direction. Antisymmetry of the actual bracket gives
\[
d\alpha_n(X_{\mathcal K_\lambda})
=-\sum_{j=1}^N\lambda^{-j}d\alpha_n(X_{C_j})
 +O(\lambda^{-N-1}).
\tag{18}
\]
The constant may depend on this fixed nonzero pair. No all-frequency estimate is obtained by this extraction alone.

Now compare two sufficiently regular states in the same chart with the same \(J\). Equations (16)–(17) make the left side of (18) equal at those states; the same sufficiently large positive parameters work after bounding both source norms. Successive coefficient comparison proves equality of every \(d\alpha_n(X_{C_j})\). Thus each actual local \(C_j\) has pure-action angular velocity. Holomorphic torque divisibility as in §1 extends it across zeros of individual pairs. The square-root same-action tests require no real-slice hypothesis, because this comparison is made in the original complexified physical chart.

Finally each fixed \(X_{C_j}\) is a finite differential-polynomial physical field, and the common higher state charts give an analytic map \((h^{K_j})^2\to(h^0)^2\) for some finite \(K_j\). Equations (13) and (18) therefore yield
\[
\boxed{\dot w_n=w_n\Omega_{j,n}(J),\quad
\dot z_n=-z_n\Omega_{j,n}(J),\quad
|\Omega_{j,n}(J)|\le A_j\langle n\rangle^{K_j}}
\tag{19}
\]
on a sufficiently small weighted action neighborhood for that fixed \(j\). This proves polynomial growth, not a polynomial-plus-bounded asymptotic expansion, and not a common action radius for the entire hierarchy. It also does not yet assert that exponentiating (19) gives a curve in the same old strong phase domain; that is a separate genuine-flow argument.

## 7. Why the proposed weighted complex logarithm is not a regular phase chart

Let \(g_n\to\infty\), and put
\[
E_g=\{\theta:\ \|\theta\|_g=\sup|\theta_n|/g_n<\infty\}.
\]
Even if a base \(w_n^*,z_n^*\ne0\) has enough decay that all profiles below lie in \(s^2\), the proposed map
\[
w_n=w_n^*e^{(a_n+\theta_n)/2},\qquad
z_n=z_n^*e^{(a_n-\theta_n)/2}
\tag{14}
\]
is not locally injective on any complex \(E_g\times E_g\) neighborhood. The vectors \(4\pi i e_n\) have norm \(4\pi/g_n\to0\) and give exactly the same Cartesian point. The independent action logarithm also has \(2\pi i e_n\to0\), so its common product level contains accumulating lattice points. The actual local level is not simply \(a=0\), although the differential kernel has \(da=0\).

Restricting every coordinate to an imaginary branch strip does not repair a Banach chart: this strip has empty interior in \(E_g\) once \(g_n\to\infty\). A quotient by the exponential lattice has a nondiscrete kernel and the projection is not a local diffeomorphism. Treating the parameter space as a covering phase with multiplicities must be stated explicitly; it does not yield a local state inverse.

There is a second issue even on a purely real hyperbolic logarithm. If
\[
(|w_n^*|+|z_n^*|)e^{\epsilon g_n}\in s,
\tag{15}
\]
then for \(0<r<\epsilon\), the profiles \(\theta^{(n)}=rg_ne_n\) have fixed \(E_g\) norm \(r\), while their Cartesian images converge to the base in every \(h^N\). Hence the inverse is not continuous for the ambient \(s^2\) subspace topology. An injective real version can be assigned its own stronger topology, but its image is then an immersed phase domain, not a regular submanifold for the inherited smooth-field topology.

Finally ordinary rapid decay of the base does not imply (15). For example \(w_n^*=z_n^*=e^{-n^2}\), \(g_n=e^n\) fails it. A base and an admissible weight must be constructed jointly.

These objections concern the proposed full phase, not just a fixed-action isotropic family. Keeping \(a\) variable does not remove them.

## 8. What a genuine manifold proof still needs

The new inverse (12) is a physical analytic bridge and not a proof of the full requested regularity. A complete positive route now has four explicit tasks:

1. Choose an angular model space containing the actual DLW and desired hierarchy frequency sequences **whose exponential period lattice is discrete**. A space containing an open weighted \(\ell^\infty\) ball with unbounded allowed coordinate amplitudes fails this requirement. Separating bounded compact angles from a controlled noncompact part is a possible route, but the transported original real involution and translation frequency must be checked.
2. Prove bounded invertibility of the physical \(B(J)\) on that angular/coefficient model. Equation (12) handles \(\mathcal V_2\) and bounded Hamiltonian coefficients; it does not give an inverse on a superpolynomial \(g\)-weighted space. Ordinary Cartesian loss-two estimates do not supply that extension.
3. Construct a **full phase with variable actions**, prove that its inclusion in physical states is locally one-to-one with the declared topology, prove induced reality, and identify its continuous weak symplectic form. The original physical common-kernel maximality is available, but the restriction can acquire degeneracy if its action directions are too small to pair with all its angular directions.
4. Prove actual local flows on that phase and either membership in the same strong \(\mathcal S_\infty\), or declare and prove a different genuine common DLW flow domain. The existing finite strong-flow theorem does not automatically cover \(H_c\) for arbitrary \(c\in\ell^\infty\), nor all relative-profile perturbations of one strong state.

A regular full-phase model, once these tasks are met, would make the common-level tangent equal its differential kernel by an ordinary submersion argument; (12) would then give actual angular Hamiltonian generation on its specified scale. Until then the regular common-level manifold and full Liouville conclusion remain unproved. The profile lattice obstruction prevents obtaining them by simply replacing closure with an unqualified exponential-profile Banach chart.
