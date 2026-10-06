# A finite-h fourth-weight charge and its periodic reduction

2026-10-04. Independent direct Hamilton calculation. Set D=∂x,
β=h²/32, R=d⁻¹M and A=RDw. Write ⟨f⟩=hΣ_j∫f_j dx. The full formal closure is

\[
U_t=-D B,\qquad w_t=-D C,
\quad B=U^2/2+\beta w^2+U_x+A,\quad C=Uw-w_x.
\]

The Hamilton density and the new density are

\[
e=\tfrac12U^2w+\tfrac\beta3w^3+wU_x+\tfrac12wA,
\]
\[
\boxed{q_4=\tfrac13U^3w+\tfrac{2\beta}{3}Uw^3
+2UwU_x-\tfrac43U_xw_x+UwA,\qquad Q_4=\langle q_4\rangle.}
\]

This is a density of weight four when wt(U)=wt(w)=wt(D)=1 and wt(R)=0.
Its integral representative has x-derivative order one. R is a specified
nonlocal lattice operator; the formula is not a finite-radius lattice density.

## Exact full-flow proof

Assume R*=-R, [R,D]=0, vanishing integrated Dx terms, and the cubic trace identity

\[
\sum_j f_j(Rf)_j^2=-\frac{h^2}{12}\sum_j f_j^3,\qquad f=Dw.
\tag{1}
\]

The variational derivatives, using (RD)*=RD, are

\[
(Q_4)_U=U^2w+\tfrac{2\beta}{3}w^3-2Uw_x
+\tfrac43w_{xx}+wA,
\]
\[
(Q_4)_w=U^3/3+2\beta Uw^2+2UU_x
+\tfrac43U_{xx}+UA+RD(Uw).
\tag{2}
\]

Denote the local parts of (2) by L_U,L_w and B_0=B−A.
After transferring every R through the summed pairing, the negative of the
Hamilton bracket is equivalent modulo Dx to

\[
L_U DB_0+L_w DC-\tfrac43Aw_{xxx}-\tfrac12w_xA^2.
\tag{3}
\]

The coefficient of A before the last integration by parts is exactly

\[
wDB_0+UDC-DL_U-D^2(Uw)=-\tfrac43w_{xxx}.
\]

The local part obeys the exact polynomial identity

\[
L_U DB_0+L_w DC=-\tfrac{4\beta}{3}w_x^3+DG,
\tag{4}
\]

where

\[
\begin{aligned}
G={}&\tfrac{4\beta^2}{15}w^5+\tfrac{4\beta}{3}U^2w^3
-2\beta Uw^2w_x+\tfrac{2\beta}{3}U_xw^3
+\tfrac{4\beta}{3}ww_x^2\\
&+\tfrac13U^4w-\tfrac13U^3w_x+U^2U_xw
-\tfrac23UU_xw_x+\tfrac23U_x^2w.
\end{aligned}
\]

The Awxxx integral vanishes because R is skew and commutes with D².
Consequently

\[
\{Q_4,H\}=\left\langle\tfrac{4\beta}{3}w_x^3
+\tfrac12w_x(Rw_x)^2\right\rangle=0
\]

by (1) and h²=32β. This proof does not infer conservation from a Lax pair.

For the cyclic N-lattice, R is the zero-mean inverse of d followed by M,
extended by RΠ=0. Identity (1) holds whenever Πf=0. Indeed its Fourier
symbol is r(θ)=−ih cot(θ/2)/2. On any nonzero-mode triad
θ₁+θ₂+θ₃=0 mod 2π,

\[
r(\theta_1)r(\theta_2)+r(\theta_2)r(\theta_3)
+r(\theta_3)r(\theta_1)=-h^2/4.
\]

Symmetrizing the trilinear trace proves (1), including the Nyquist mode.
The unrestricted pointwise modified Rota–Baxter identity needs a mean
correction; it was not used here. For infinite/open lattices (1) must be
justified for the chosen trace and inverse. Formal Fourier coefficients
whose proper frequency subsets avoid zero satisfy the same identity.

## The original periodic mean reduction

Let x be periodic and impose the already-established autonomous closure

\[
\Pi w=c\ne0,\qquad\Pi(Uw)=\gamma,
\quad U=B_m+p,\quad w=c+r,
\quad B_m=(\gamma-\Pi(pr))/c,
\quad\Pi p=\Pi r=0.
\]

Use the reduced bracket J_red=−[[0,PD],[PD,0]], P=I−Π, and
K=H−γ⟨U⟩ after substitution. The actual reconstructed full-field flow is

\[
U_t=-DB+\lambda,\qquad w_t=-DC,
\quad\lambda=\frac{2}{c}D\Pi e.
\tag{5}
\]

To obtain (5), the full-flow identity is

\[
\Pi(Uw)_t=-D\Pi[2e-D(Uw)].
\]

The mean constraints then determine cλ. Moreover,

\[
\Pi(Q_4)_U=2\Pi e
\]

since (Q₄)_U−2e=−2D(Uw)+(4/3)D²w.
Thus the extra drift contribution to dQ₄/dt is

\[
hN\int\lambda\Pi(Q_4)_U dx
=\frac{2hN}{c}\int D(\Pi e)^2dx=0.
\]

Therefore Q₄ restricted to this same periodic reduced phase space is a
conserved Hamilton functional and {Q₄,K}_red=0. The mean drift was not
discarded. The x-translation momentum is

\[
P_{red}=\langle pr\rangle,\qquad
J_{red}\nabla P_{red}=(-Dp,-Dr).
\]

Both K and Q₄ have no explicit x dependence, so
{P_red,K}_red={P_red,Q₄}_red=0. These are three mutually commuting charges.
Full-field ⟨Uw⟩ is fixed on this leaf. The full-field U mass is
⟨U⟩=(hNγL−P_red)/c and supplies no fourth independent charge.

## Nontriviality and independence

Fix all sitewise x-average Casimirs of p,r. For N≥3 choose r=0,
p_j=α_j cos x with Σα=0 and α_j² not all equal; for example on N=3 use
α=(1,2,−3). At this state, writing b=γ/c,

\[
(Q_4)_p=cP(p^2)+2\gamma p,\qquad K_p=cp,
\qquad (P_{red})_p=0.
\]

The first gradient contains a nonzero cos(2x) component, while K_p contains
only cos x. Sitewise Casimir gradients are x-independent. Hence dQ₄ cannot
lie in the span of dK,dP_red and these Casimir gradients. Since K_p≠0 and
(P_red)_r=p≠0, all three differentials are independent there. Continuity
gives independence on a neighborhood in a suitable smooth function space.
This also excludes q₄ being only a total derivative, lattice difference,
or a constant-coefficient repetition of the earlier charges. It is not a
completeness theorem or a Liouville-integrability proof.

## Search scope and certificates

`search_weight4.py` tested a fixed 20-dimensional basis: homogeneous weight
four, representative x-order ≤1, with R only acting on first derivatives
of U,w and no more than two R factors. Seventy-two exact polarized Fourier
conditions gave rank 19 and the one-dimensional nullspace spanned by q₄
at h=1. This is evidence only within that bounded basis, followed by the
exact proof above. `check_weight4_structure.py` verifies (3)–(4) symbolically.
`check_reduced_q4.py` evaluates the genuinely nonzero periodic mean drift
at an exact N=3 Laurent-polynomial state, and verifies both the full and
reduced integrated time derivatives vanish. The proof, rather than this
one sample, establishes the general reduced identity.
