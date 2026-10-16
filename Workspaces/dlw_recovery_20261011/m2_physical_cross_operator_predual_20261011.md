# M=2 physical cross operator: predual and nondegeneracy lemma

2026-10-11. New analytic supplement, without rerunning any certificate. The small nonzero background, common reduced state chart, and original physical tensor remain those of [the cross-operator proof](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md). The reciprocal spectral Hamiltonians are [the exact physical actions](m2_reciprocal_spectral_actions_and_dlw_frequencies_20261011.md). This supplement proves a pairing property of the actual physical operator, not a transfer of the auxiliary NLS symplectic form.

## 1. Precise sequence spaces and established input

Let \(k_n=2\pi n/L\), \(n\ne0\), and \(\langle n\rangle=1+|n|\). Put
\[
\mathcal V_2=\{v:\sup_n |v_n|/\langle n\rangle^2<\infty\},
\qquad
\ell^1_2=\{p:\sum_n\langle n\rangle^2|p_n|<\infty\}.
\]
Use bilinear complex sequence pairings. Thus \(\mathcal V_2=(\ell^1_2)^*\) and \(\ell^\infty=(\ell^1)^*\). On the already established small \(\ell^1_4\) action neighborhood,
\[
B(J):\ell^\infty\longrightarrow\mathcal V_2,\qquad
D_n={iL k_n^2\over16S},\qquad
\|D^{-1}(B-D)\|_{\ell^\infty\to\ell^\infty}<1.
\tag{1}
\]
For \(H_c=\sum c_nJ_n\), the actual field in the reduced Cartesian chart has
\[
\dot w_n=iw_n(Bc)_n,\qquad
\dot z_n=-iz_n(Bc)_n.
\tag{2}
\]
For bounded \(c\) it is obtained from the actual pushed tensor
\(\mathbb J(W):(h^2)^2\to(h^0)^2\) and the action covector
\((c_nz_n,c_nw_n)\in(h^2)^2\). This tensor is continuous at the fixed state. Pure-action torque permits testing (2) at any higher state with the same \(J\).

## 2. The actual operator has a predual

Fix \(J\) in this neighborhood and a noncentral \(n\). Use the same-action test state from the cross-operator proof:
\[
w_n=r\langle n\rangle^{-2}\ne0,\qquad
z_n=J_n\langle n\rangle^2/r,
\]
with the other pairs balanced, and fill the central pair by the fixed section. This is one fixed \(h^2\) state for the present \(J,n\).

Suppose \(c^\alpha\to c\) weak star in \(\ell^\infty\), with a uniformly bounded net. For every index its coordinates converge. A finite-tail estimate gives
\[
(c^\alpha z,c^\alpha w)\longrightarrow(cz,cw)
\quad\hbox{strongly in }(h^2)^2.
\tag{3}
\]
For nets first choose a finite tail of the fixed weighted \(\ell^2\) sequences uniformly small, then use coordinate convergence on the finite head. Applying \(\mathbb J(W)\) and dividing the tested \(w_n\ne0\) proves
\[
(B c^\alpha)_n\longrightarrow(Bc)_n.
\tag{4}
\]
The uniform bound (1) extends this convergence from coordinates to every pairing with \(p\in\ell^1_2\), again by a finite-tail estimate.

More explicitly, each row functional \(c\mapsto(Bc)_n\), being weak-star continuous on bounded sets, is an \(\ell^1\) row. The estimate (1) bounds its \(\ell^1\) norm by \(C\langle n\rangle^2\). For every \(p\in\ell^1_2\), the sum of the row functionals weighted by \(p_n\) converges in \(\ell^1\). It defines a bounded predual
\[
B_*:\ell^1_2\longrightarrow\ell^1,\qquad B=B_*^*.
\tag{5}
\]
This follows from the actual physical tensor and same-action test. An arbitrary bounded operator on \(\ell^\infty\) need not have this property.

The diagonal \(D\) has a boundedly invertible predual
\(D_*:\ell^1_2\to\ell^1\), \((D_*p)_n=D_np_n\).
Thus \(T=D^{-1}(B-D)\) has a bounded predual \(T_*\) on \(\ell^1\), with norm less than one. Its Neumann series converges in predual operator norm and proves
\[
\boxed{B^{-1}:\mathcal V_2\longrightarrow\ell^\infty
\text{ is weak-star continuous},\qquad
(B^{-1})_*:\ell^1\longrightarrow\ell^1_2
\text{ is a bounded isomorphism}.}
\tag{6}
\]
The inverse bounds are uniform on the small action neighborhood in (1).

## 3. Reciprocal-action derivatives identify this exact predual

The exact reciprocal-action identity is
\[
B(J)\nabla_J\mathcal A_n=iL e_n.
\tag{7}
\]
Set
\[
M(J)=iL(B(J)^{-1})_*:\ell^1\longrightarrow\ell^1_2.
\tag{8}
\]
For a finite action variation \(p\), (7) gives
\[
(D_J\mathcal A\cdot p)_n
=\langle p,iL B^{-1}e_n\rangle=(Mp)_n.
\tag{9}
\]
The identity holds for \(\ell^1_4\) variations by finite-coordinate density and the established analytic action dependence. These are the variations needed for rapid relative-profile states. Since \(M\) is a bounded isomorphism,
\[
\boxed{D_J\mathcal A\cdot p=0\quad\Longrightarrow\quad p=0.}
\tag{10}
\]
Equation (8) additionally extends the derivative to all \(\ell^1\) directions at these higher action points. This is a derivative statement; it does not turn the old \(\ell^1_4\) neighborhood into an open \(\ell^1\) action chart.

The high-path integral from \(0\) to \(J\) and (8) give
\(\|\mathcal A(J)\|_{\ell^1_2}\le C\|J\|_{\ell^1}\)
on this higher action domain. Common low \(h^0\)-chart \(\ell^1\) holomorphy was proved separately by the original weak-form radial argument.

## 4. Nondegeneracy on any valid full relative-profile phase

This is a lemma for a phase chart, not a construction of that chart. Suppose a locally injective full phase chart has variable relative actions \(a\in\ell^\infty\), an angular model
\[
E=\ell^\infty\oplus\mathbb C n\oplus\mathbb C n^2,
\]
and rapid nonzero reference pairs. Write
\[
w_n=w_n^*e^{(a_n+\theta_n)/2},\qquad
z_n=z_n^*e^{(a_n-\theta_n)/2}.
\tag{11}
\]
Assume the actions remain in the small \(\ell^1_4\) neighborhood and the exponential map is analytic into every \(h^N\). Tangent action variation is \(p_n=J_n\dot a_n\in\ell^1_4\).

Pull back the actual continuous physical form. If a tangent \(V\) annihilates it against every phase tangent, test against the exact bounded-angle fields \(X_{\mathcal A_n}\). Equations (9)–(10) give \(p=0\), hence \(\dot a=0\) since \(J_n\ne0\).

The remaining \(V\) is purely angular. For
\(\alpha_n=(2i)^{-1}\log(w_n/z_n)-\vartheta_0\), its angular velocity is \(\dot\theta_n/(2i)\). Because \(E\subset\mathcal V_2\), select
\[
c=B^{-1}\bigl(\dot\theta/(2i)\bigr)\in\ell^\infty.
\tag{12}
\]
At this fixed state \(V=X_{H_c}\), by (2). Against finite-coordinate radial variations, the null condition gives
\[
0=dH_c(V_{\rm radial})=\sum_n c_nJ_n\dot a_n.
\tag{13}
\]
Thus \(c_n=0\) for every \(n\), so \(V=0\). The pulled-back physical form is weakly nondegenerate; continuity follows from the chart derivative into \(h^0\) and continuity of the original mixed low form.

Coefficients in (12) are frozen only for this tangent argument. A pointwise inverse is not automatically a neighborhood Hamiltonian. Actual neighborhood bounded-angle fields come from the reciprocal Hamiltonians; original DLW and translation supply the polynomial directions, and their transitivity requires the separate phase-domain argument.

On the exact original real form \(J_{-n}=\overline{J_n}\), \(\dot a_{-n}=\overline{\dot a_n}\), \(\dot\theta_{-n}=\overline{\dot\theta_n}\), test finite \(n,-n\) radial variations to obtain all real and imaginary tests. The actual real weak form is nondegenerate as well.

Regular common levels, a locally injective full phase model, and old strong-domain membership are separate chart hypotheses here. A simpler dense finite-Cartesian proof of restricted weak nondegeneracy is now available in [the full variable-action phase proof §5.1](m2_regular_variable_action_original_symplectic_phase_20261011.md); that construction does not require this cross-operator inverse. This supplement provides an additional pairing input and does not expand the established domain.

