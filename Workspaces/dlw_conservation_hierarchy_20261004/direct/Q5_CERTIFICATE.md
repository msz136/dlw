# Finite-h weight-five charge: exact conservation and mean correction

2026-10-04. Use the notation and hypotheses of `Q4_CERTIFICATE.md`. In
particular A=RDw, K=RD, β=h²/32, Πw=c≠0 and Π(Uw)=γ on the cyclic original
DLW reduction. Set C₀=Uw−w_x and B₀=U²/2+βw²+U_x. The new density is

\[
\begin{aligned}
q_5={}&U^4w+12U^2wU_x-4wU_x^2-16UU_xw_x+8U_xw_{xx}\\
&+4U^2wA+4wU_xA-4Uw_xA+2wA^2-4w_xA_x
+2UwK(Uw)\\
&+4\beta U^2w^3+\tfrac{4\beta^2}{5}w^5
+\tfrac{8\beta}{3}w^3U_x-8\beta ww_x^2
+\tfrac{8\beta}{3}w^3A.
\end{aligned}
\tag{1}
\]

The uncorrected formal full-flow charge is Q₅=⟨q₅⟩. Its density is weight
five and has representative x-order two. Its nonlocal terms use K on
linear or quadratic fields and at most two R factors. For h→0, β→0 and
R→∂y⁻¹; (1) reduces modulo Dx to the independently derived continuous DLW
weight-five density. The five terms on the last line and its continuation
are explicit finite-h corrections. R has unbounded lattice range.

## Exact full-flow conservation certificate

Put f=w_x, g=D(Uw), A=Rf and C=Rg. Polarizing the cubic trace identity gives

\[
\sum_j[g(Rf)^2+2f(Rf)(Rg)]_j
=-\frac{h^2}{4}\sum_j f_j^2g_j.
\tag{2}
\]

On the cyclic lattice (2) holds for Πf=Πg=0, precisely the derivative mean
conditions supplied by Πw=c and Π(Uw)=γ. On any other trace/inverse
realization it is an explicit additional algebraic hypothesis.

Let q_loc be (1) without A,C terms, and L_U,L_w its Euler derivatives:

\[
\begin{aligned}
L_U={}&4U^3w-12U^2w_x+16Uw_{xx}+8U_xw_x
+8U_{xx}w-8w_{xxx}\\
&+8\beta Uw^3-8\beta w^2w_x,
\end{aligned}
\]
\[
\begin{aligned}
L_w={}&U^4+12U^2U_x+16UU_{xx}+12U_x^2+8U_{xxx}\\
&+12\beta U^2w^2+8\beta U_xw^2
+16\beta ww_{xx}+8\beta w_x^2+4\beta^2w^4.
\end{aligned}
\]

Write F₀=U²w+wU_x−Uw_x+(2β/3)w³ and F=F₀+wA=2e−D(Uw). Then

\[
(Q_5)_U=L_U+8C_0A-4wA_x+4wC,
\]
\[
\begin{aligned}
(Q_5)_w={}&L_w+(4U^2+8U_x+8\beta w^2)A
+4UA_x+2A^2+8A_{xx}+4UC+4KF.
\end{aligned}
\tag{3}
\]

Using skewness of R, self-adjointness of K and integration by parts, the
negative Hamilton bracket is equivalent to

\[
L_U DB_0+L_w DC_0-2gA^2-4fAC.
\tag{4}
\]

In this reduction, the coefficient of every linear-A term is the exact
zero polynomial

\[
\begin{aligned}
&-DL_U+8C_0DB_0+(4U^2+8U_x+8\beta w^2)DC_0\\
&\quad+4D(wDB_0)-4D(UDC_0)
+D^2(8DC_0-4F_0)=0.
\end{aligned}
\]

Equation (2) converts the summed last terms of (4) into
+16βf²g. The remaining local polynomial satisfies

\[
L_U DB_0+L_w DC_0+16\beta w_x^2D(Uw)=DG_5.
\tag{5}
\]

An exact explicit primitive G₅ is stored in `q5_structure.json`; the script
`check_q5_structure.py` independently differentiates it and returns zero
for the difference in (5). Thus {Q₅,H}_full=0 on the stated mean-constraint
manifold, under the trace identities, without inferring this from a Lax
representation. This is an instantaneous full-bracket identity. The
uncorrected cyclic full closure need not keep Π(Uw) spatially constant, so
this statement alone does not assert its invariance for arbitrary
full-closure initial states.

## Necessary correction on the original periodic Hamilton leaf

The full formal closure is not the reconstructed original cyclic flow:
U_t=−DB+λ with λ=(2/c)D ē, B=B₀+A and ē=Πe. Uncorrected Q₅ generally
fails under this drift. For the exact N=3,h=1,c=−4,γ=0 Laurent state in
`reduced_q4_counterexample.json`,

\[
\operatorname{Tr}_x(dQ_5/dt)_{red}=-473181/256,
\qquad\operatorname{Tr}_x(dQ_5/dt)_{full}=0.
\]

The required corrected charge is

\[
\boxed{\widehat Q_5=Q_5-\frac{8hN}{c}\int(\Pi e)^2dx.}
\tag{6}
\]

For a general field define

\[
F_e=-BC_0-wDB-\tfrac12wK C_0.
\]

Local differentiation and R skewness give

\[
\bar e_t=D\left[\Pi F_e+\frac{2\gamma}{c}\bar e
+2D\bar e\right]
\tag{7}
\]

on the reconstructed reduced flow. The gradient in (3) obeys

\[
\Pi(Q_5)_U+8\Pi F_e+16D\bar e
=16D^2\Pi(Uw)-8D^3\Pi w+8\Pi[w_xRw_x]=0.
\tag{8}
\]

Combining (7)–(8) with λ=(2/c)D ē proves the drift contribution to Q₅ is
exactly the time derivative of the subtraction in (6). The full-flow
bracket vanishes by (2)–(5), so dQ̂₅/dt=0 and {Q̂₅,K}_red=0. Translation
invariance gives {Q̂₅,P_red}_red=0 as well. This is an exact mean-mode
correction, not a change of the original equation.

## Independence and remaining involution issue

On the fixed sitewise x-average Casimir leaf at N=3, r=0,
p=α cos x, α=(1,2,−3), let m₂=Π α²=14/3. The p-component of dQ̂₅ has cubic
cosine coefficient

\[
4c[P\alpha^3-2m_2\alpha]=-(28c/3)\alpha\ne0.
\]

It therefore contains cos(3x); Q₄ has highest cosine cos(2x), K has only
cos x, and (P_red)_p=0 while (P_red)_r=p≠0. Hence
K,Q₄,Q̂₅,P_red are four differentially independent functionals at that
state, and in a nearby smooth neighborhood. This rules out total
derivatives, lattice differences and repetition of previous charges.

The general pairwise bracket {Q̂₅,Q₄}_red is not proved in this direct
certificate. `check_q4_q5_involution.py` gives exact zero at a nontrivial
N=3 Laurent state with nonzero mean drift, which is supporting evidence
only. A monodromy/Adler proof may establish the general bracket separately.
These finite initial charges and a formal infinite commuting hierarchy do
not by themselves supply a Liouville-integrability theorem.

## Bounded search evidence

The 47-dimensional weight-five basis in `search_weight5.py` imposes
representative x-order ≤2, R only on D(linear or quadratic fields), and at
most two R factors. 240 exact polarized Fourier conditions gave rank 46.
A separate 256-row trace test had rank 47, so the density basis has no
sampled null-density combinations. The unique candidate was reconstructed
from a finite-field elimination and then verified against every original
rational row exactly. The general conservation proof (2)–(8) supersedes
these samples. The search excludes no candidates outside this bounded
basis, and does not constitute a general classification theorem.
