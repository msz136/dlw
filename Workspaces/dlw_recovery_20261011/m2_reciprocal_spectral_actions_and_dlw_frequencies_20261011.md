# M=2: reciprocal spectral actions, exact physical angle flows, and original DLW frequencies

2026-10-11. This is a new exact bridge after [the physical cross-operator estimate](m2_action_angle_cross_operator_and_profile_obstructions_20261011.md). No certificate was rerun. All earlier low state-chart, small nonzero background, and central-section hypotheses remain in force. The physical tensor is still \(J_{uv}=-\operatorname{offdiag}(D)/16\).

## 1. New spectral Hamiltonians whose actual fields are individual angle rotations

Use the same full unit-period discriminant and actions:
\[
\Delta(z,J)=d(z,\rho(J),J),\quad
R^2=\Delta^2-4,\quad
\lambda(z,J)=\eta(J)-2iz/L,\quad
\omega_\lambda={S^2-\lambda^2\over16S}.
\]
The exact source variation at a moving center is
\[
d\Delta(z)=dF_\lambda+F'_\lambda\,d\eta,\qquad
F'_\lambda={iL\over2}\Delta_z.
\tag{1}
\]
Here \(dF_\lambda\) holds the original centered \(\lambda\) fixed. The physical trace field satisfies
\[
D\mathcal R X_{F_\lambda}=\omega_\lambda\Pi Y_{\lambda-\eta}.
\tag{2}
\]

For every noncentral contour choose a logarithm branch in its isolated spectral disk:
\[
P_n(z,\eta)=4iL\log_n{S+\lambda(z,\eta)\over S-\lambda(z,\eta)}.
\tag{3}
\]
The disks can be chosen to avoid \(\lambda=\pm S\), the two central branch points. This is a common small-domain choice: the fixed noncentral disks have positive separation from the central disk, while all sufficiently high disks go to infinity. Shrink the existing low domain once if necessary. Each logarithm is holomorphic on a slightly larger disk containing its contour. Branches for different \(n\) need not be continuations of one global logarithm.

For an explicit simultaneous choice, use the usual fixed KLTZ circles centered at \(n\pi\) of radius \(\pi/4\), and disks of radius \(\pi/3\) for their logarithms. Impose the additional harmless small-background bound \(L|S|<\pi/4\) and shrink the common low ball so that \(L|\eta|<\pi/4\). On every noncentral disk,
\[
|\lambda|\ge {2\over L}(\pi|n|-\pi/3)-|\eta|
>{13\pi\over12L}>|S|.
\tag{3a}
\]
Thus the ratio in (3) is holomorphic and nowhere zero on the product of each disk with the \(\eta\) disk. That product is simply connected, so it has a jointly holomorphic logarithm. The KLTZ common low neighborhood already supplies the simultaneous fixed contours, their spectral isolation, and the canonical square-root branches \(R\) along them; intersect it once with this holonomy bound. No \(n\)-dependent source radius is being intersected here. In a version using different fixed spectral disks, their positive common noncentral distance gives the identical argument.

The two identities that matter are
\[
\partial_zP_n={1\over\omega_\lambda},\qquad
\partial_\eta P_n={iL\over2\omega_\lambda}.
\tag{4}
\]
Define the reciprocal spectral actions
\[
\boxed{\mathcal A_n(J)={1\over\pi}\oint_{\Gamma_n}
P_n(z,\eta(J)){\Delta_z(z,J)\over R(z,J)}\,dz,\quad n\ne0.}
\tag{5}
\]
Adding a constant to the logarithm changes (5) by a constant times
\(\oint\Delta_z/R=0\); the same zero-winding proof as the ordinary action bridge applies. Thus the local branch choice does not affect this Hamiltonian.

The usual variation identity and closed-contour integration by parts give
\[
d\mathcal A_n=
-{1\over\pi}\oint_{\Gamma_n}{d\Delta\over\omega_\lambda R}\,dz
+{1\over\pi}\oint_{\Gamma_n}{iL\Delta_z\over2\omega_\lambda R}\,dz\,d\eta.
\]
Substituting (1) cancels the two \(d\eta\) terms **exactly**, and proves
\[
\boxed{d\mathcal A_n=
-{1\over\pi}\oint_{\Gamma_n}{dF_\lambda\over\omega_\lambda R}\,dz.}
\tag{6}
\]
In particular source dependence of the spectral center is fully included. This cancellation is stronger than assuming its coefficient has zero winding.

Use (2) inside (6), then the full standard action contour identity, before applying the central projection:
\[
\boxed{D\mathcal R X_{\mathcal A_n}
=-{1\over\pi}\oint_{\Gamma_n}{\Pi Y_{\lambda-\eta}\over R}\,dz
=\Pi Y_{I_n}=L G_n,}
\quad G_n=(-w_n,z_n)\text{ on pair }n.
\tag{7}
\]
This is an exact actual physical Hamiltonian field, throughout the neighborhood. In the angle convention
\(\alpha_m=(2i)^{-1}\log(w_m/z_m)-\vartheta_0\), it says
\[
\{\alpha_m,\mathcal A_n\}_{\rm phys}=iL\delta_{mn}.
\tag{8}
\]
All the \(\mathcal A_n\) commute under the original physical bracket, and commute with all \(F_\lambda,\eta,C_j\). This follows either from (6) and the established physical spectral involution, or from their action-only dependence together with their exact fields (7). No NLS bracket is being imported.

At the background, the same collapsed-gap residue calculation as in the cross-operator note gives
\[
\mathcal A_n(0)=0,\qquad
d\mathcal A_n(0)={16S\over k_n^2}\,dI_n,\qquad k_n=2\pi n/L.
\tag{9}
\]
The background value is zero because \(\Delta_z/R\) is holomorphic in the collapsed noncentral disk. Equation (9) retains the sign of \(S\).

## 2. Bounded infinite Hamiltonians on the common low mixed state chart

There is a stronger low-domain argument, independently proposed by the spectral-completeness reviewer, which avoids a high weighted action condition for these Hamiltonians. The original form
\[
\Omega(V,W)=-16\int[(K V_u)W_v+(K V_v)W_u]\,dx
\]
is a continuous weak symplectic form on \(E_0=L^2_0\times H^1_0\). The common analytic inverse \(\mathcal R^{-1}:(h^0)^2\to E_0\) transports it to an analytic locally bounded bilinear form \(\widetilde\Omega_W\). On a sufficiently small \(h^0\) ball,
\[
|\widetilde\Omega_W(U,V)|\le C\|U\|_{h^0}\|V\|_{h^0}.
\tag{10a}
\]
The individual contour Hamiltonians (5) are holomorphic on this same ball. Equation (7), first established on its dense higher intersections, extends by holomorphy and the continuous weak-form identity to the low ball. This also avoids assigning a classical differential bracket to rough fields without a budget.

For finite \(d\), put \(H_d=\sum d_n\mathcal A_n\) and
\(X_d(W)=L(-d_nw_n,d_nz_n)_n\). The radial Hamiltonian identity gives
\[
H_d(W)-H_d(0)=\int_0^1
\widetilde\Omega_{tW}(X_d(tW),W)\,dt,
\quad |H_d(W)|\le C\|d\|_\infty\|W\|_{h^0}^2.
\tag{10b}
\]
The central pair at \(tW\) is always filled by the same state section; thus this is a radial path in the reduced chart, not a path that freezes \(I_0\). Each \(\mathcal A_n(0)=0\) by (9). Choosing finite coefficients of modulus one to align the phases of their values proves
\[
\boxed{\mathcal A(W)=(\mathcal A_n(W))_{n\ne0}\in\ell^1,\quad
\|\mathcal A(W)\|_{\ell^1}\le C\|W\|_{h^0}^2.}
\tag{10c}
\]
This \(\ell^1\)-valued map is holomorphic, as a finite-block Cauchy argument proves without first assuming continuity of the infinite sum. On a ball \(B_r(W_0)\) with bound \(M\) in (10c), every finite coordinate projection is holomorphic with \(\ell^1\) norm at most \(M\). Its degree-\(m\) homogeneous Taylor polynomial \(P_m^F(h)\) satisfies the uniform diagonal estimate
\[
\|P_m^F(h)\|_{\ell^1}\le M r^{-m}\|h\|^m .
\tag{10c'}
\]
The finite projections are compatible. Taking the supremum over finite sets defines an \(\ell^1\)-valued diagonal polynomial \(P_m(h)\) with the same bound; complex polarization gives its continuous symmetric \(m\)-linear extension, with a constant depending only on \(m\). For \(\|h\|<r\), the series \(\sum_{m\ge0}P_m(h)\) converges in \(\ell^1\) by (10c'). Every coordinate is the Taylor series of the corresponding \(\mathcal A_n(W_0+h)\), so this sum equals \(\mathcal A(W_0+h)\). This proves Banach holomorphy and its Cauchy norm estimates.

Consequently every bounded \(d\) defines a genuine low-chart holomorphic Hamiltonian \(H_d=\langle d,\mathcal A\rangle\). Finite coefficient truncations of \(X_d(W)\) converge in \(h^0\) at each fixed \(W\); derivatives of \(\mathcal A\) take values in \(\ell^1\). Passing to the limit in the finite Hamiltonian identities proves
\[
\boxed{dH_d(W)V=\widetilde\Omega_W(X_d(W),V)}
\tag{10d}
\]
for every low tangent \(V\). At higher states the same truncations converge in every \(h^N\), and (10d) is exactly the original smooth physical identity. Its flow is the explicit order-zero low analytic flow (16). Thus no extension from only \(\ell^1_4\) is needed.

### 2.1 Cross-operator gradient bounds, as an additional high estimate

The previous note proved
\[
B(J):\ell^\infty\longrightarrow\mathcal V_2
\text{ boundedly invertible},\quad
\mathcal V_2=\{v:\sup |v_n|/\langle n\rangle^2<\infty\},
\tag{10}
\]
on a sufficiently small \(\ell^1_4\) action neighborhood, where
\(\langle n\rangle=1+|n|\). Equations (7)–(8) now prove the exact gradient identity
\[
B(J)\nabla_J\mathcal A_n=iL e_n,\qquad
\nabla_J\mathcal A_n=iL B(J)^{-1}e_n.
\tag{11}
\]
Thus the needed rows of the inverse operator really are closed action covectors: they come from the explicit functions (5). They were not merely selected pointwise coefficients.

Since \(\|e_n\|_{\mathcal V_2}=\langle n\rangle^{-2}\), (10) yields, uniformly on that action neighborhood,
\[
\|\nabla_J\mathcal A_n\|_{\ell^\infty}
\le C\langle n\rangle^{-2}.
\tag{12}
\]
Integrate along the segment from \(0\) to \(J\), which stays in the small \(\ell^1_4\) ball. Together with (9), this proves
\[
|\mathcal A_n(J)|\le C\langle n\rangle^{-2}\|J\|_{\ell^1}.
\tag{13}
\]
This bound suffices for all the following sums; no unproved identity \(\mathcal A_n=I_n f_n\) is needed.

For every \(d\in\ell^\infty\),
\[
H_d=\sum_{n\ne0}d_n\mathcal A_n,\qquad
\nabla_JH_d=\sum d_n\nabla_J\mathcal A_n\in\ell^\infty
\tag{14}
\]
converge absolutely and locally uniformly, as do the action gradients by (12). The scalar Hamiltonian is holomorphic on the stated weighted action neighborhood. The sums pull back to the actual physical higher state chart. At smooth states, the actual tensor and the analytic transpose budget justify passage to the sum in the Hamiltonian field. Equation (7) gives the exact field
\[
\boxed{D\mathcal R X_{H_d}
=L(-d_nw_n,d_nz_n)_n.}
\tag{15}
\]
The finite truncations converge in every \(h^N\), since \(W\) is rapid and \(d\) is bounded. This is a genuine infinite spectral Hamiltonian with a bounded angle field on a whole neighborhood, rather than a Hamiltonian chosen only at one action value.

Its explicit complex local flow is
\[
w_n(t)=e^{-Ld_nt}w_n(0),\qquad
z_n(t)=e^{Ld_nt}z_n(0).
\tag{16}
\]
For \(|t|\|d\|_\infty\) small this is an analytic local group in every \(h^N\), with one low \(h^0\) time window and all higher persistence. Composition with the common state inverse is therefore an actual flow on the mixed physical spaces \(E_N=H^N_0\times H^{N+1}_0\). Equation (10d) supplies its actual original Hamiltonian identity on the whole common low chart; on smooth states it preserves every \(C_j\) and action. The high gradient estimate (14) is an additional estimate rather than a condition for the existence of this low scalar Hamiltonian.

Identification of this entire infinite-flow family with the old strong presentation requires the same mixed-uniqueness transport argument used for finite auxiliary fields, now with the mixed low space \(E_0\). Equations (10c)–(10d) and (15)–(16) supply the low Hamiltonian, uniform Banach flow, and high persistence; commutation supplies the actual hierarchy transport. This note does not silently equate low mixed flow membership with old strong membership.

## 3. Original DLW frequency: exact constants and a primary complex-frequency theorem

The gauged AKNS fast logarithm at fixed \(\zeta=\lambda-\eta\) has
\[
\ell_\zeta={L\zeta\over2}+{c_1\over\zeta}
+{c_2\over\zeta^2}+{c_3\over\zeta^3}+O_{C^1}(\zeta^{-4}),
\]
\[
c_1=\int ab\,dx,\quad c_2=-\int ab_x\,dx,\quad
c_3=\int(ab_{xx}-a^2b^2)\,dx.
\tag{17}
\]
The actual periodic Riccati equation \(\beta_x=b-\zeta\beta-a\beta^2\) gives coefficients \(b,-b_x,b_{xx}-ab^2\). The contraction and differentiated-remainder proof is the same finite-order proof as the already established actual quasimomentum expansion; it requires a sufficiently regular bounded source ball, not convergence of its infinite formal series.

For \(\varphi_1(t)=-iLa(Lt)/2,\ \varphi_2(t)=2iLb(Lt)\), the unit NLS energy is
\[
\mathcal E=\int_0^1(\varphi_{1,t}\varphi_{2,t}
+\varphi_1^2\varphi_2^2)\,dt
=L^3\int(a_xb_x+a^2b^2)\,dx=-L^3c_3.
\tag{18}
\]
The auxiliary fields satisfy
\[
\Pi Y_{c_1}=0,\quad Y_{c_2}=(a_x,b_x),\quad
\Pi Y_{c_2}=8SL\,D\mathcal R X_\eta.
\tag{19}
\]
Here \(c_1=\mathcal M/L\) and the standard mass \(\mathcal M=\sum I_n\) generates the constant diagonal gauge removed by \(\Pi\).

The original actual fast logarithm is
\(\ell_{\lambda-\eta}=L(\lambda-\eta)/2+\mathcal K_\lambda\),
\(\mathcal K_\lambda=-\sum C_j\lambda^{-j}\) with the established finite \(C^1\) remainder. Therefore
\[
D\mathcal R X_{\mathcal K_\lambda}
=\omega_\lambda\Pi Y_{\ell_{\lambda-\eta}}
+{L\over2}D\mathcal R X_\eta.
\]
Expand its right side using (17). The order-\(\lambda^1\) term is gauge, the constant term cancels by (19), and its order-\(\lambda^{-1}\) coefficient is
\(-\Pi(Y_{c_3}+2\eta Y_{c_2})/(16S)\).
Comparing with the actual left side proves
\[
D\mathcal R X_{C_1}={1\over16S}\Pi(Y_{c_3}+2\eta Y_{c_2}).
\tag{20}
\]
One rigorous coefficient comparison is to pair the actual \(C^1(H^{N+2})\) remainder with a fixed finite angular Hamiltonian field at a source in mixed \(E_{N+4}\); that field lies in \(E_{N+2}\subset(H^{N+2})^2\). This is the fixed-coordinate argument in the cross-operator note §6.1, without an all-frequency remainder claim.

The original DLW Hamiltonian is \(H_{\rm DLW}=-16SC_1+4LS^3\). Since \(Y=(L/i)X^{\rm std}\), (18) gives \(Y_{c_3}=iX^{\rm std}_{\mathcal E}/L^2\). Consequently
\[
\boxed{D\mathcal R X_{H_{\rm DLW}}
=-{i\over L^2}\Pi X^{\rm std}_{\mathcal E}
-2\eta\Pi Y_{c_2}.}
\tag{21}
\]
Every sign and scale here is determined by (17)–(20), rather than by an NLS real-type analogy.

For the required spectral estimate use [Berti–Kappeler–Montalto, *Large KAM tori for perturbations of the dNLS equation*, Theorem 3.2(i), PDF p.22](https://arxiv.org/pdf/1603.09252). The theorem supplies an open complex neighborhood \(V\subset\ell^{1,2}\) of the nonnegative action cone, including \(0\), on which
\[
I\longmapsto(\omega_n^{\rm NLS}(I)-4\pi^2n^2)_n\in\ell^\infty
\tag{22}
\]
is analytic and locally bounded. The action normalization is the same contour normalization used here. Only this complex action statement is used.

Choose a zero-centered \(\ell^{1,2}\) ball of radius \(r_{\rm BKM}>0\) in \(V\). An additional explicit domain requirement is
\[
L^2S^2/4<r_{\rm BKM}/2,\qquad
|\rho(J)-I_0^*|+\sum_{n\ne0}\langle n\rangle^2|J_n|
<r_{\rm BKM}/2,\quad I_0^*=-L^2S^2/4.
\tag{23}
\]
Thus the negative central background is allowed by the actual complex extension. No numerical radius is provided by the external theorem, and the older KLTZ domain assumption does not alone imply (23).

The standard energy field has projected angle velocity
\(-(\omega_n^{\rm NLS}-\omega_0^{\rm NLS})\). Translation acts exactly as
\(w_n\mapsto e^{ik_ns}w_n,\ z_n\mapsto e^{-ik_ns}z_n\), with central angle unchanged. This identity follows from [Grébert–Kappeler, *Symmetries of the nonlinear Schrödinger equation*, Proposition 3.4, PDF p.10](https://www.numdam.org/item/BSMF_2002__130_4_603_0.pdf), and extends to the common complex neighborhood; the KLTZ Fourier derivative \(w_n=-\widehat{\varphi_2}(n)\) fixes its sign. Therefore (21) gives the original Cartesian torque
\[
\boxed{\Omega_{{\rm DLW},n}(J)
=-{\omega_n^{\rm NLS}(I)-\omega_0^{\rm NLS}(I)\over L^2}
-2i\eta(J)k_n
=-k_n^2-2i\eta(J)k_n+\mathfrak r_n(J),}
\tag{24}
\]
where \(\mathfrak r(J)\in\ell^\infty\) is analytic and locally bounded on (23). This is a precise polynomial-plus-bounded decomposition for original DLW time. Higher local times have the pure-action polynomial-growth statement from the preceding note; no polynomial-plus-bounded expansion for every higher time is asserted here.

For real original fields \(\eta\) is real. Externally prescribed \(\Gamma(t)\) adds the already proved physical spatial translation. This calculation preserves the unfrozen \(c_\Gamma,\Gamma\) scope of the original reduction.

## 4. The original physical real involution in Cartesian coordinates

Real physical \(a,b\) correspond to \(\varphi_1,\varphi_2\) that are individually purely imaginary. Thus their potential involution is
\[
\sigma_{\rm pot}(\varphi_1,\varphi_2)
=(-\overline{\varphi_1},-\overline{\varphi_2}).
\tag{25}
\]
The needed norming symmetry is provided by [Grébert–Kappeler 2002, Theorem 1.2 and Propositions 3.2–3.3, PDF pp.2,8–10](https://www.numdam.org/item/BSMF_2002__130_4_603_0.pdf): on the defocusing real plane, complex conjugation of its single potential reverses the action index and negates its angle; multiplication by \(-1\) adds \(\pi\) to all angles. The precise match to the KLTZ spectral normalization is checked in [the independent real-involution audit §1](m2_kltz_physical_real_involution_independent_audit_20261011.md), using the actual constant matrix
\[
C=2^{-1/2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}.
\]
It identifies the two sources' operators and Dirichlet roots. Their divisor sheets differ by the sheet involution, while the canonical sheet and \(2\pi\delta_{jn}\) period normalization identify the normalized Abel differentials uniquely. Thus the angles differ by a sign and at most a uniform \(\pi\) shift, both preserving the reflection-conjugation identity. This rules out an unverified action-dependent rephasing. The Fourier derivative is only a sign check; it would not establish the exact norming symmetry by itself.

On the defocusing totally real plane \((\varphi_1,\varphi_2)=(\overline u,u)\), (25) is the single-potential operation \(u\mapsto-\overline u\). In \(w=(x+iy)/\sqrt2,z=(x-iy)/\sqrt2\) the symmetry therefore gives
\[
\sigma_{\rm cart}(w,z)_n
=(-\overline{w_{-n}},-\overline{z_{-n}}).
\tag{26}
\]
The two sides of the claimed equivariance are antiholomorphic maps. Their difference, composed with \(\sigma_{\rm pot}\), is holomorphic and zero on an open piece of this totally real plane. The Banach-space identity theorem extends it to the connected common complex neighborhood of zero. Equality across Cartesian zero pairs follows by holomorphy, not by selecting a square root of a vanishing action. Directly, KLTZ (2.21) yields \(w_n=-\widehat{\varphi_2}(n)\), which confirms the sign in (26).

For the central angle choose the background-zero branch
\(\vartheta_0=(2i)^{-1}\log(w_0/z_0)\), \(\log1=0\). The even focusing constant background has \(y_0^*=0\), hence \(w_0^*=z_0^*\ne0\). Equation (26) gives
\(\vartheta_0(\sigma W)=-\overline{\vartheta_0(W)}\),
so its zero central-angle section is invariant. The central action fill \(\rho(\mathfrak c J)=\overline{\rho(J)}\) and square-root branch \(s(\overline I_0)=-\overline{s(I_0)}\) preserve this section. The constant gauge transforms by \(\tau\mapsto\overline\tau\), and uniqueness of the real-coefficient physical state inverse recovers real \(u,v,\tau\). These branch and gauge assertions are independently checked in the linked audit §§3–4. Consequently the reduced physical reality is precisely
\[
\boxed{w_n=-\overline{w_{-n}},\qquad
z_n=-\overline{z_{-n}},\quad n\ne0.}
\tag{27}
\]
This is not either standard NLS real slice. It is obtained from the original potential reality and the norming symmetry.

For a real base satisfying (27), relative coordinates
\(w_n=w_n^*e^{(a_n+\theta_n)/2}\),
\(z_n=z_n^*e^{(a_n-\theta_n)/2}\)
have real form \(a_{-n}=\overline a_n,\theta_{-n}=\overline\theta_n\), on any locally injective branch. A bounded-angle component has this same reversal-conjugation reality; the polynomial directions compatible with it are real multiples of \(n^2\) and purely imaginary multiples of \(n\).

The reciprocal actions obey
\(\mathcal A_{-n}=\overline{\mathcal A_n}\)
on this original real form. This follows from the antipodal conjugation of the contours and \(P_{-n}(-\overline z,\eta)=-\overline{P_n(z,\eta)}\), up to the harmless branch constant. Hence \(H_d\) in (14) is real for \(d_{-n}=\overline d_n\), and its flow (16) preserves (27).

## 5. The regular phase theorem supplied by these bridges

Equations (7), (15), and (16) supply actual bounded-angle Hamiltonians and their exact local flows. Equation (24) places original DLW time in bounded angles plus the finite quadratic/linear polynomial directions. Equation (27) provides the original real form for that proposed Banach model.

These inputs are now used in [the full real variable-action phase proof](m2_regular_variable_action_original_symplectic_phase_20261011.md), §§2–5,8–9. It gives two freely variable bounded complex-sequence coordinates with the original reflection-conjugation reality, and two independent real heat/translation coordinates. Its precise real polynomial model has a locally discrete period lattice; the state map and its differential are injective. A two-sided actual DLW orbit supplies the Gaussian margin of its nonzero-action base.

The linked construction proves the common-level split submersion and ordinary tangent equality, continuity and weak nondegeneracy of the **original** form, exact level Lagrangian maximality, and actual orbit transitivity by a finite composition of original DLW, translation, and the bounded infinite Hamiltonian (14). The whole core is a genuine original-flow Banach phase with a declared topology stronger than smooth-field topology. Its proof does not rely on assigning a manifold structure to every ambient rapid kernel. In particular it is a variable-action phase, rather than an isotropic fixed-action family.

The fixed-action component through the chosen old strong base retains the old strong membership by the mixed uniqueness transport. The entire variable-action core's all-hierarchy membership in the old strong presentation, regularity of its larger inherited fiber, natural openness in the full smooth-field space, and an all-\(M\) action inverse remain unproved. The resulting local weak Liouville theorem has exactly the small-background, common-chart, primary-frequency, original-reality, and nonzero-base conditions recorded in that linked proof.
