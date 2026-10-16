# M=2 physical trace fields: exact Poisson bridge and ambient closure

2026-10-11. This note concerns the actual mean-zero physical leaf for M=2, S=2δ≠0. Its closure theorem is conditional on the common low-domain reduced Cartesian state inverse already established in [the AKNS bridge, §4.4–4.5](akns_physical_state_inverse_bridge_20261011.md), including the small-background and action-factorization-ball hypotheses. It is not an all-M theorem.

## 1. Actual trace and conventions

Let D=∂x, ⟨f⟩=L⁻¹∫₀ᴸf dx, P₀f=f−⟨f⟩, and K=D₀⁻¹P₀. The physical variables u,v have zero mean. Write

\[
q=u-S,\quad V=-2uv/S,\quad
A=(S^2/4-v^2)/S^2,\quad
r=A(S+u)-v_x/S,
\]
\[
\eta=\langle V\rangle,\quad\theta=KV,
\quad a=e^\theta q,\quad b=e^{-\theta}r.
\tag{1}
\]

The physical tensor for ordinary ∫dx variational gradients is

\[
J_{uv}=-\frac1{16}\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\tag{2}
\]

The trace-free split connection and its periodic diagonal gauge are

\[
\mathcal A_\lambda=\frac{\lambda-V}{2}H+qE_{12}+rE_{21},
\quad G=\operatorname{diag}(e^{-\theta/2},e^{\theta/2}),
\]
\[
G^{-1}\mathcal A_\lambda G-G^{-1}G_x
=\frac{\zeta}{2}H+aE_{12}+bE_{21},
\qquad\zeta=\lambda-\eta.
\tag{3}
\]

Here λ is the centered original spectral parameter, held fixed in the physical Hamiltonian Fλ. The AKNS trace at fixed ζ is denoted Tζ(a,b), so Fλ=Tλ−η(a,b). If the uncentered original parameter is used, λ=λorig−B, with B fixed as the external leaf parameter at the present state.

Let W be the periodic adjoint monodromy matrix for Fλ, with its scalar part omitted:

\[
W=\begin{pmatrix}h&E\\F&-h\end{pmatrix},\qquad
W_x=[\mathcal A_\lambda,W].
\]
\[
E_x=(\lambda-V)E-2qh,\quad
F_x=(V-\lambda)F+2rh,\quad
h_x=qF-rE.
\tag{4}
\]

The gauged adjoint has upper and lower entries e=eθE and f=e−θF. Thus δTζ=∫(f δa+e δb)dx and ∂ζTζ=∫h dx=L⟨h⟩. Define the x-normalized auxiliary canonical tensor J₀=[[0,1],[−1,0]] on (a,b); its trace field is

\[
Y_\zeta=J_0dT_\zeta=(e,-f).
\tag{5}
\]

This is an auxiliary standard tensor, not the physical pushed tensor. In the exact KLTZ normalization φ₁(t)=−iLa(Lt)/2, φ₂(t)=2iLb(Lt), t=x/L, the KLTZ NLS field, expressed in (a,b), is (i/L)Yζ. Therefore Yζ=(L/i)XstdTζ. This nonzero constant matters for exact formulas but not closed spans.

## 2. Fixed-λ physical gradients and the exact push-forward

Duhamel variation at fixed λ gives δFλ=∫tr(W δAλ)dx. Since

\[
\delta q=\delta u,\quad
\delta r=A\delta u-2v(1+u/S)\delta v/S-\delta v_x/S,
\quad\delta V=-2(v\delta u+u\delta v)/S,
\]

integration by parts and (4) yield the actual gradients

\[
g_u=F+AE+2vh/S,\qquad
g_v=(\lambda-2v)E/S+2h.
\tag{6}
\]

Equivalently, differentiating Tζ∘(a,b) with ζ held fixed gives

\[
g_u^{\mathrm{fixed}\,\zeta}=F+AE+2v(h-\langle h\rangle)/S,
\]
\[
g_v^{\mathrm{fixed}\,\zeta}
=-2v(1+u/S)E/S+E_x/S+2u(h-\langle h\rangle)/S.
\]

The extra term in dFλ is −(∂ζTζ)dη=−L⟨h⟩dη. Because dη has gradients (−2v/(SL),−2u/(SL)), this term adds (2v⟨h⟩/S,2u⟨h⟩/S) and gives (6). Omitting this shift would change the physical field.

From (2), uₜ=−Dgᵥ/16 and vₜ=−Dgᵤ/16. Eliminating adjoint derivatives with (4) gives derivative-free expressions

\[
u_t=-qF/8+A(S+u)E/8+(\lambda-2v)qh/(8S)
-(\lambda-2v)(\lambda-V)E/(16S),
\]
\[
v_t=(\lambda+2v)F/16-A(\lambda-2v)E/16-SA h/4.
\tag{7}
\]

For clarity the intermediate differentiated gradients are

\[
Dg_v=2qF+
\bigl[(\lambda-2v)(\lambda-V)/S-2A(S+u)\bigr]E
-2(\lambda-2v)qh/S,
\]
\[
Dg_u=-(\lambda+2v)F+A(\lambda-2v)E+4SAh.
\]

All vx terms cancel through r=A(S+u)−vx/S and Ax=−2v vx/S². Thus (7) includes the full E coefficient of uₜ and introduces no hidden spatial derivatives.

Define

\[
R_0=SF+(\lambda v/S-v^2/S-S/4)E+(2v-\lambda)h,
\qquad \omega_\lambda=\frac{S^2-\lambda^2}{16S}.
\tag{8}
\]

Substitution of (4) and (7), collecting F,E,h coefficients, gives

\[
V_t=-2(vu_t+uv_t)/S=D R_0/(8S),\quad
\eta_t=0,\quad
\theta_t=(R_0-\langle R_0\rangle)/(8S).
\tag{9}
\]

Indeed, if C=λv/S−v²/S−S/4, differentiation of R₀ has the coefficient form

\[
DR_0=-(\lambda u+2Sv)F
+[C(\lambda-V)+(\lambda-2v)A(S+u)]E
+[2SA(S+u)-2Cq]h.
\]

Using C=v(λ−2v)/S−SA and V=−2uv/S, these are precisely the coefficients of −16(vuₜ+uvₜ)=8SVₜ. Averaging and applying K prove the other two identities in (9).

The derivative identity here is for Vₜ, not vₜ. For the actual potentials,

\[
e^{-\theta}a_t=u_t+q\theta_t,
\quad e^\theta b_t=A u_t-2v(1+u/S)v_t/S-Dv_t/S-r\theta_t.
\]

Using the same three adjoint identities proves

\[
\boxed{
a_t=\omega_\lambda e-\frac{\langle R_0\rangle}{8S}a,\qquad
b_t=-\omega_\lambda f+\frac{\langle R_0\rangle}{8S}b.
}
\tag{10}
\]

If Q(a,b)=(a,−b) is the constant-diagonal gauge generator, the precise identity is

\[
D(a,b)\,X_{F_\lambda}
=\omega_\lambda Y_{\lambda-\eta}
-\frac{\langle R_0\rangle}{8S}Q.
\tag{11}
\]

In KLTZ standard-field notation the first coefficient is (L/i)ωλ. Thus the physical trace field agrees with a weighted standard trace field only after the gauge component is removed. No equality of the full physical and standard Poisson tensors is asserted.

The identities (6)–(10) were already checked in the saved [15-check certificate](m2_physical_trace_poisson_checks_20261011.json), script SHA256 `02a1391284e7fc6d8b0b8b34f34a82ab0f060c807e527c4dae6bc05be871aebf`, and in the independently structured [16-check certificate](m2_physical_trace_poisson_independent_checks.json), script SHA256 `1e808d56cfa35646200ce2f971854b258f6219a1b1c5ae1857d284f2bf19cdeb`. Neither script was rerun for this note. These certificates check finite identities, not the closure theorem below.

## 3. Central points and the reduced section

The original trace-free rank-one connection is upper triangular at λ=S and lower triangular at λ=−S. Its diagonal multipliers are 1 because u,v have zero mean. Consequently F±S=2 identically on the leaf and X_F±S=0. The two isolated zeros of ωλ do not remove a vector from a closed spectral span: ζ↦Yζ is continuous in every smooth seminorm, and each missing value is a limit of neighboring noncentral values.

The state inverse supplies full Cartesian coordinates (wₙ,zₙ), n∈Z, with Iₙ=wₙzₙ, χ=χ̂(I), and η=η̂(I) on the physical image. Locally χ=0 is I₀=ρ((Iₙ)ₙ≠₀), while I₀≠0 permits a fixed branch of ϑ₀=(2i)⁻¹log(w₀/z₀). The constant gauge acts as

\[
(w_n,z_n)\mapsto(e^{-\tau}w_n,e^\tau z_n),
\quad G=(-w_n,z_n)_n,
\quad d\vartheta_0(G)=i.
\tag{12}
\]

On χ=0 define the tangent projection to the fixed central-angle section by

\[
\Pi V=V-\frac{d\vartheta_0(V)}i\,G.
\tag{13}
\]

This is a continuous linear projection at the fixed state in every hᴺ topology; its kernel is the one-dimensional gauge direction. Composing the physical potential map with this unique gauge section and the KLTZ chart yields the exact reduced state inverse R:

\[
R:\mathcal O_{\rm red}\cap(H^N_0\times H^{N+1}_0)
\longleftrightarrow
\mathcal U_{\rm red}\cap(h^N_{n\ne0}\times h^N_{n\ne0}),
\qquad N\ge0.
\tag{14}
\]

These are restrictions of one low-domain analytic chart. At smooth states DR is a continuous linear isomorphism for the Fréchet topology of all Sobolev/sequence seminorms. It is a state chart, not a claim that these reduced coordinates are physically canonical. Since the standard trace depends only on actions, its field is tangent to χ=0 and commutes with constant gauge. Applying (13) to (11) gives

\[
\boxed{DR\,X_{F_\lambda}=\omega_\lambda\,\Pi Y_{\lambda-\eta},}
\tag{15}
\]

where the right side denotes the noncentral components after projection. The projection is evaluated at the chosen representative of the same gauge orbit, so gauge equivariance identifies both sides without an additional state-dependent gauge derivative.

## 4. Conditional ambient closed-span theorem

Let E∞=C∞₀×C∞₀ with its usual Fréchet topology. Equivalently use the mixed Sobolev seminorms Hᴺ₀×Hᴺ⁺¹₀ for every N; this gives the same smooth topology. Let s=⋂ᴺhᴺ(Z∖{0}). Fix a smooth physical state x in the chart (14) and assume

\[
I_n(x)\ne0\quad\text{for every }n\ne0.
\tag{16}
\]

The domain conditions in §1 remain part of this theorem. Define

\[
K_x^{\mathbb C}=\bigcap_{n\ne0}\ker dI_n(x)\subset E_\infty^{\mathbb C},
\quad
\mathcal H_x^{\mathbb C}
=\operatorname{span}_{\mathbb C}\{X_{F_\lambda}(x):\lambda\in\mathbb C\}.
\]

Then

\[
\boxed{\overline{\mathcal H_x^{\mathbb C}}^{\,E_\infty}=K_x^{\mathbb C}.}
\tag{17}
\]

No all-frequency inverse bound for an angular coefficient is needed to prove this equality. Every approximation is by finitely many coordinate directions or by one fixed compact spectral contour.

### 4.1 The common differential kernel in Cartesian coordinates

Put J=(Iₙ)ₙ≠₀. The reduced coordinate action map J:s²→ℓ¹ is the quadratic map Jₙ=wₙzₙ. Its differential is

\[
dJ_n(\dot w,\dot z)=z_n\dot w_n+w_n\dot z_n.
\tag{18}
\]

Because (16) gives wₙ,zₙ≠0, a vector in the common kernel has each pair of the form cₙ(−wₙ,zₙ). Let Pₖ retain the finitely many indices 0<|n|≤k. For every N,

\[
\|P_k(\dot w,\dot z)-(\dot w,\dot z)\|_{h^N\times h^N}\to0.
\tag{19}
\]

Each Pₖ kernel vector is a finite linear combination of the single-pair angular fields Gₙ=(−wₙ,zₙ) on pair n, zero elsewhere. Coefficients cₙ may grow arbitrarily; (19) uses the already rapid decay of the velocity, not a bound on cₙ.

Full KLTZ canonical action fields are XstdIₙ=−i wₙ∂wₙ+i zₙ∂zₙ. For n≠0 their central components vanish, so dϑ₀(XstdIₙ)=0 and ΠXstdIₙ=XstdIₙ. Their noncentral components are iGₙ. In the x-normalized tensor J₀ this is YIₙ=LGₙ. Hence the finite angular directions in (19) are exactly the restrictions of full standard noncentral action fields, up to a fixed nonzero constant.

### 4.2 Full contour fields supply the angular generators

At the chosen potential, KLTZ contour variation gives the full standard identity

\[
Y_{I_n}=-\frac1\pi\oint_{\Gamma_n}
\frac{Y_{T_{\zeta(z)}}}{R(z)}\,dz,
\qquad \zeta(z)=-2iz/L,
\quad R(z)^2=\Delta(z)^2-4.
\tag{20}
\]

The contour lies in its fixed annulus, R is single-valued and nonzero there, and Γₙ can be chosen to avoid the two points λ(z)=η(x)−2iz/L=±S. This is a choice for each fixed contour at the chosen state; it does not require a common lower bound over all n. A small contour deformation avoiding finitely many regular points leaves (20) unchanged.

Projection Π is a continuous linear map at x, so it commutes with this vector-valued contour integral. From (15), for every n≠0,

\[
LG_n
=-\frac1\pi\oint_{\Gamma_n}
\frac{DR_xX_{F_{\eta(x)-2iz/L}}(x)}
{R(z)\,\omega_{\eta(x)-2iz/L}}\,dz.
\tag{21}
\]

This expression is an equality of tangent vectors at x. The spectral parameter and scalar coefficients in the integrand are evaluated at x; it does not assert that state-dependent division by ω gives a Hamiltonian vector field in a neighborhood.

For a fixed contour, the actual fundamental matrix and its adjoint depend continuously on z in every spatial smooth seminorm, by the linear ODE and its differentiated equations. The gauge, KLTZ derivative, DRₓ and Π preserve this continuity. Since Rω is bounded away from zero on that compact contour, ordinary finite Riemann sums converge in every hᴺ seminorm to (21). Thus each Gₙ belongs to the closure of DRₓHₓ. Equation (19) and the Fréchet homeomorphism DRₓ show Kₓ⊂cl Hₓ.

Conversely every physical Fλ commutes with every Iₙ under the actual tensor (2), as established by the original actual spectral bracket and the physical contour action formula. Thus X_Fλ∈Kₓ. Each dIₙ is continuous on E∞, so Kₓ is closed and cl Hₓ⊂Kₓ. This proves (17).

### 4.3 Why the central constraint is not a canonical shortcut

For a full action-dependent standard functional d(I), projection of its full standard field to ϑ₀=constant has noncentral angular coefficients ∂Iₙd−∂I₀d. The actual differential of the reduced restriction d(ρ(J),J) instead has coefficients ∂Iₙd+(∂Jₙρ)∂I₀d. These expressions need not coincide. In particular χ=0 with the mass-gauge section is not being declared a standard symplectic reduction.

The proof deliberately applies (20) to full standard Iₙ, n≠0, before projecting. For those functionals ∂I₀Iₙ=0; ΠYIₙ=YIₙ supplies the individual noncentral direction. The physical tensor enters only through the exact field identity (15). Thus the change of derivative caused by I₀=ρ(J) is fully retained without contaminating the angular-generation argument.

Condition (16) is sufficient, and can be weakened to (wₙ,zₙ)≠(0,0) for every noncentral n. If a noncentral pair is (0,0), (18) has an entire two-dimensional kernel at that pair while all action-dependent standard trace fields vanish there. Therefore (17) is not asserted on the whole Cartesian chart, which also includes simultaneous closed-gap zeros.

### 4.4 The physical action fields have the same closed span

The preceding proof used full standard action fields to generate single-coordinate angular directions. To identify the closed span of the actual physical action fields as well, a continuous-transpose argument is needed. This is a consequence of the same smooth state chart; it does not identify the physical tensor with the standard one.

At a fixed smooth state, write R as the composition of the physical potential map Λ, fixed balancing/rescaling, the full KLTZ map B, central-angle gauge normalization Q, and the projection p onto noncentral pairs. For its derivative transpose use the ordinary complex bilinear ∫dx pairing in physical space and the coordinatewise bilinear sequence pairing.

The derivative of Q is a diagonal scaling plus the smooth gauge vector multiplied by a scalar covector supported on the central pair. Its transpose is therefore a diagonal scaling plus a finite-central-rank correction, continuous on every hᴺ at the fixed smooth state. The transpose p* inserts a zero central pair. For the full KLTZ chart, the known canonical identity gives

\[
DB\,J_{\rm pot}\,(DB)^*=J_{\rm seq},
\qquad (DB)^*=J_{\rm pot}^{-1}(DB)^{-1}J_{\rm seq}.
\tag{31}
\]

The two standard tensors in this formula are constant and invertible of order zero. The common-domain inverse differentiates to a bounded map hᴺ→Hᴺ for every N at smooth states. Thus (DB)* maps hᴺ continuously to Hᴺ. Fixed balancing, the change x↔t and the linear (xₙ,yₙ)↔(wₙ,zₙ) conversion only introduce constant invertible maps and the already specified factors of L and i.

The physical potential transpose follows directly from §3 of the state bridge:

\[
\Lambda=E_\theta(M+jKc),\quad
\Lambda^*=(M^*-c^{\mathsf T}Kj^{\mathsf T})E_\theta,
\]
\[
M=\begin{pmatrix}1&0\\A&B-D/S\end{pmatrix},
\quad M^*=\begin{pmatrix}1&A\\0&B+D/S\end{pmatrix},
\quad B=-2v(1+u/S)/S,
\]
\[
j=\binom q{-r},\qquad c=(-2v/S,-2u/S).
\tag{32}
\]

At a fixed smooth state every coefficient is smooth and K has order −1. Consequently Λ* maps (Hᴺ⁺¹)² continuously to (Hᴺ)². Combining these transposes, with the source mean-zero projection understood, proves

\[
DR_x^*:s^2\longrightarrow E_\infty^{\mathbb C}
\text{ is continuous},\qquad
J_{uv}DR_x^*:s^2\longrightarrow E_\infty^{\mathbb C}
\text{ is continuous}.
\tag{33}
\]

More precisely a seminorm of order N on the second map is controlled by a sequence seminorm of order N+2. A fixed finite derivative loss is continuous in this Fréchet topology. Formula (31) is used only to control the known chart transpose. Formula (32), and then the actual Juv, retain the original physical tensor.

Write the full trace action factorization in the x-normalized parameter as Tζ=t(ζ,I), and let η̃(J)=η̂(ρ(J),J). Then

\[
F_\lambda=t(\lambda-\widetilde\eta(J),\rho(J),J).
\]

At the chosen state the reduced action derivative has coefficients

\[
\beta_n=\partial_{I_n}t+(\partial_{J_n}\rho)\partial_{I_0}t
-\partial_\zeta t\,\partial_{J_n}\widetilde\eta,
\qquad n\ne0.
\tag{34}
\]

Every derivative here is a continuous functional on ℓ¹, so β∈ℓ∞. This is the functional chain rule, and correctly includes both the central constraint and the state-dependent spectral shift. It is not the projected standard angular coefficient discussed in §4.3.

The Cartesian sequence covector of Fλ is c=(βₙzₙ,βₙwₙ)ₙ≠₀. It belongs to s² because β is bounded and w,z are rapidly decreasing. Its finite truncations cᵏ converge in every hᴺ and equal ∑₀<|n|≤k βₙdCartesianIₙ. Applying (33) gives the actual physical equality

\[
\boxed{
X_{F_\lambda}(x)
=\lim_{k\to\infty}\sum_{0<|n|\le k}
\beta_n(x,\lambda)X_{I_n}^{\rm physical}(x)
\quad\text{in }E_\infty^{\mathbb C}.
}
\tag{35}
\]

The reverse closed-span inclusion follows from the already audited physical action field formula

\[
X_{I_n}^{\rm physical}(x)
=-\frac1\pi\oint_{\Gamma_n}
R(z)^{-1}X_{F_{\eta(x)-2iz/L}}(x)\,dz,
\tag{36}
\]

whose fixed-ζ dη coefficient vanishes by the zero-winding argument. Riemann sums converge in E∞ for each fixed contour as in §4.2. Thus

\[
\boxed{
\overline{\operatorname{span}_{\mathbb C}
\{X_{I_n}^{\rm physical}(x):n\ne0\}}
=\overline{\mathcal H_x^{\mathbb C}}=K_x^{\mathbb C}.
}
\tag{37}
\]

This argument also makes explicit why merely proving the trace-span theorem would not by itself identify the physical action-span theorem: the continuity of the chart transpose and of the actual order-two pushed tensor is the necessary additional step.

## 5. Fixed ζ, holonomy and the real physical leaf

The theorem uses the original fixed-λ family. At a fixed state its λ values range over all of C, so ζ=λ−η(x) ranges over all of C too. This relabeling of vectors at one state is valid; identifying the Hamiltonians in a neighborhood would require the chain rule.

For the fixed-ζ pulled-back AKNS trace Tζ∘(a,b), the exact physical Hamiltonian identity is

\[
X_{T_\zeta\circ(a,b)}
=X_{F_\lambda}+\partial_\lambda F_\lambda\,X_\eta,
\qquad\lambda=\eta+\zeta.
\tag{22}
\]

The real holonomy field is Xη=(uₓ,vₓ)/(8SL), and all actions are translation invariant. Hence Xη(x)∈Kₓ and, by (17), Xη(x) already lies in the closed span of fixed-λ physical trace fields. Consequently including η, or the corresponding nonzero scalar multiple of the momentum P, does not enlarge that closed span. The family consisting of fixed-ζ physical traces together with η has the same closed span, by (22) in both directions. No omission of the η term is permitted in an exact field formula.

On a real physical state x, the original connection has real coefficients when λ is real and respects complex conjugation for all λ. Therefore

\[
\overline{F_\lambda(x)}=F_{\bar\lambda}(x),\quad
\overline{X_{F_\lambda}(x)}=X_{F_{\bar\lambda}}(x).
\tag{23}
\]

The complex closed span in (17) is invariant under ordinary physical conjugation. Let Kₓᴿ=Kₓᶜ∩E∞ᴿ, equivalently the common kernel of real and imaginary parts of all noncentral actions on the real leaf. Taking real parts of a convergent finite complex linear combination gives a finite real linear combination of Re X_Fλ and Im X_Fλ. Conversely these realified trace fields lie in Kₓᴿ. Thus

\[
\boxed{
\overline{\operatorname{span}_{\mathbb R}
\{X_{\operatorname{Re}F_\lambda}(x),
X_{\operatorname{Im}F_\lambda}(x):\lambda\in\mathbb C\}}
^{\,E_\infty^{\mathbb R}}=K_x^{\mathbb R}.
}
\tag{24}
\]

Here Re X_Fλ=X_ReFλ and Im X_Fλ=X_ImFλ because the actual physical tensor is real. The reality of reduced Cartesian coordinates can be complicated; (23)–(24) transport the physical real structure without identifying it with a standard focusing or defocusing sequence slice.

Applying the same realification argument to (35)–(37) gives

\[
\overline{\operatorname{span}_{\mathbb R}
\{X_{\operatorname{Re}I_n}^{\rm physical},
X_{\operatorname{Im}I_n}^{\rm physical}:n\ne0\}}
=K_x^{\mathbb R}.
\tag{38}
\]

The complex action family need not obey the standard NLS reality relations; all its real and imaginary physical Hamiltonians are used in (38).

## 6. Maximal isotropy under the original form

Let Ω be the continuous weak symplectic form on the smooth mean-zero physical leaf obtained from the inverse of (2), so Ω(X_F,v)=dF(v). The continuity follows from K=D₀⁻¹P₀ being continuous on smooth mean-zero functions. All statements in this section use Ω, not the auxiliary standard AKNS form.

First, the actual trace fields pair to zero by their actual Poisson commutativity. Their closed real span is Kₓᴿ by (24), and continuity of Ω therefore gives Ω(Kₓᴿ,Kₓᴿ)=0.

The common trace differential kernel equals the common noncentral action differential kernel. One implication follows from the exact action variation

\[
dI_n=-\frac1\pi\oint_{\Gamma_n}
R(z)^{-1}dF_{\eta-2iz/L}\,dz.
\tag{25}
\]

Its omitted dη coefficient is zero by the already audited zero-winding calculation ∮Δz/R dz=0. The other implication follows by composing the action-only full discriminant d(z,I), the central constraint I₀=ρ(J), and η=η̂(ρ(J),J). If all dJₙ(v) vanish, then dJ(v)=0 in ℓ¹, hence dI₀(v)=dη(v)=0 and every dFλ(v)=0. Thus

\[
\bigcap_\lambda\ker dF_\lambda
=\bigcap_{n\ne0}\ker dI_n=K_x^{\mathbb C}.
\tag{26}
\]

If a real smooth v is Ω-orthogonal to Kₓᴿ, it pairs to zero with every realified trace field. Consequently all complex dFλ(v)=0, and (25) gives all dIₙ(v)=0. Therefore

\[
\boxed{(K_x^{\mathbb R})^{\perp_\Omega}=K_x^{\mathbb R}.}
\tag{27}
\]

This is closed ambient maximal isotropy. It is not a proof that an infinite common action level is a regular Fréchet submanifold.

## 7. What follows inside the fixed strong domain

Suppose x also belongs to the same strong coherent domain S∞ used in the actual-flow audits. The existing [all-M flow audit, §7](all_m_actual_spectral_independent_audit.md) and [action flow audit, §4](akns_actions_strong_domain_independent_audit.md) establish actual finite realified trace and action flows there, preserving the same strong diffeology and all the actions. Their common-time assertion concerns each fixed finite list of flows; no countably infinite simultaneous flow is used here.

Let Yₓ be the actual local common level of all the noncentral actions, equipped with the subset diffeology from S∞. Let Vₓ⊂E∞ᴿ be the image of its internal tangent space under the ambient evaluation differential. Every plot in Yₓ has zero action derivatives, so Vₓ⊂Kₓᴿ. Conversely, finite compositions of the verified realified trace flows give curves in Yₓ, with velocities equal to arbitrary finite real linear combinations of the trace fields. Equation (24) therefore yields

\[
\boxed{\overline{V_x}^{\,E_\infty^{\mathbb R}}=K_x^{\mathbb R},
\qquad V_x^{\perp_\Omega}=K_x^{\mathbb R}.}
\tag{28}
\]

This uses the ambient image of internal velocities. It proves neither injectivity of that map nor the unclosed equality Vₓ=Kₓᴿ. The small-gap counterexample in [the product-level caution](infinite_product_level_tangent_caution_20261011.md) excludes treating coordinatewise differential kernels as automatically integrable ambient smooth fiber velocities.

There is a separate precise internal-kernel statement, which must not be confused with TinternalYₓ. Write j:TinternalₓS∞→E∞ᴿ for the ambient evaluation map, and let the strong form be ω=j*Ω, as in the original-form construction. Define

\[
\mathcal A_x=\bigcap_{n\ne0}\ker d(\operatorname{Re}I_n,\operatorname{Im}I_n)
\subset T^{\mathrm{internal}}_xS_\infty.
\tag{29}
\]

Then j(Aₓ)⊂Kₓᴿ, so Aₓ is ω-isotropic. If ξ is ω-orthogonal to Aₓ, every verified internal realified trace direction belongs to Aₓ; therefore all dFλ(jξ)=0 and (25) implies all dIₙ(ξ)=0. Hence

\[
\boxed{\mathcal A_x^{\perp_\omega}=\mathcal A_x.}
\tag{30}
\]

The naturality identity used here is dIₙ(ξ)=dIₙᵃᵐᵇⁱᵉⁿᵗ(jξ), since each physical action restricts from a smooth ambient functional. This maximality lemma does not require injectivity of j. For the actual phase domain, injectivity has already been proved by the relative-extension and zero-velocity argument in the mixed strong construction, §16.4 (16.9); its phase evaluation kernel is therefore zero. That result does not by itself prove injectivity of TinternalYₓ→TinternalS∞, which is a different map. Equation (30) asserts maximal isotropy of the internal common differential kernel under the original pulled-back form, not an identification with the actual fiber tangent.

## 8. Dependencies and unresolved scope

The new conclusions are (17), (24), (27), (28), the carefully defined (30), and the physical action-span statements (37)–(38). Their prerequisites are the D7 common-domain state inverse, the action-only factorization of Δ, χ and η with I₀=ρ(J), the exact gauge action (12), the physical trace identity (11), actual spectral commutativity, and the already audited finite strong trace/action flows. The full KLTZ canonical identity is used only for the transpose regularity estimate (31), followed by the actual physical operators (32)–(33). Sections 1–7 supply the new closure argument; the finite certificates in §2 verify only its finite algebraic bridge.

The theorem applies pointwise under (16) and all stated low-chart/background conditions. The separate [same-strong-chart action genericity proof](akns_actions_same_strong_chart_genericity_20261011.md), §§3–5, supplies actual action Hessians I₋ₙ^[2]=κₙQₙPₙ with κₙ=Lkₙ²/(16S)≠0, and analytic finite minors on one real Hilbert parameter ball of a single strong presentation. Since that parameter map sends 0 to the physical constant background and is continuous into L²₀×H¹₀, shrink its Hilbert ball once so its entire image lies in the D7 low chart Ored; the arbitrarily small ε witnesses for every fixed action/minor remain available. Its Baire argument then gives a residual, dense, nonempty parameter subset whose physical states satisfy (16) and have every finite real noncentral action block independent on actual internal strong plot directions. Thus the action-regular strong states needed here are nonempty in that stated chart. The residual assertion is about that Hilbert parameter ball; it is not a global D-topological genericity claim for S∞.

The internal tangent evaluation of the phase S∞ is already injective by the mixed §16 construction. Still unresolved are injectivity/ghosts for the actual common fiber map TinternalYₓ→TinternalS∞, unclosed actual fiber-tangent equality, a regular common-level manifold, global action-angle coordinates, and a corresponding state inverse and closure theorem for M>2. The user's general-field all-M DLW Liouville objective therefore remains open beyond this conditional M=2 result.

The independent [closure-chain review](m2_physical_trace_closure_chain_independent_review_20261011.md) validates the exact projection, full-action contour generation, the smooth-transpose convergence step, physical realification, and the distinction between the internal common differential kernel and the actual fiber tangent. This note used saved certificates only; it executed none of the previous or current symbolic checks.
