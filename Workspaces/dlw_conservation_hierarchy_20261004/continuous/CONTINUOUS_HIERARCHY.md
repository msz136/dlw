# Continuous DLW: Riccati generator and low coefficients

This note concerns the **formal continuous full flow**, not the finite-h reduced periodic flow. Its value is an independently checked continuous benchmark for the latter.

## 1. Equations and the correct continuous spatial operator

Write D=∂x, Y=∂y, R=Y^{-1}, K=RD. Put b=U/2 and c=−w/4. The potential is V=Kw/2, up to a y-independent term fixed by the full-flow gauge. Then

\[
U_t=-UU_x-U_{xx}-2V_x,\qquad w_t=-(Uw)_x+w_{xx},\qquad V_y=w_x/2.
\]

The continuous limit of the verified two Darboux intertwiners is

\[
P\psi=0,\quad P=(D-b)Y-c,
\qquad H\psi=0,\quad H=\partial_t+D^2+V.
\]

The sign of c is important: T⁺=D−U/2+hw/8, T⁻=D−U/2−hw/8, so (D−U/2)ψ_y=−wψ/4. Direct operator expansion gives

\[
P_t+[D^2+V,P]=-2b_xP
\]

when b_t=−b_xx−2bb_x−V_x, c_t=c_xx−2(bc)_x and V_y=−2c_x. The multiplier of P is harmless on its solution space, but should not be omitted from an operator statement.

## 2. Riccati recursion

Set

\[
p=\psi_x/\psi=z+\sum_{n\ge1}p_nz^{-n},\qquad
q=\psi_y/\psi=\sum_{n\ge1}q_nz^{-n}.
\]

The two spatial logarithmic identities are

\[
q_x+(p-b)q=c,\qquad p_y=q_x.
\]

Hence

\[
q_1=c,\qquad q_{n+1}=(b-D)q_n-\sum_{k=1}^{n-1}p_kq_{n-k},\qquad (p_n)_y=Dq_n.
\]

The heat identity is p_t+D(p_x+p²+V)=0. Its y compatibility gives the generating conservation law

\[
(q_n)_t+Y\left[D p_n+2p_{n+1}+\sum_{k=1}^{n-1}p_kp_{n-k}\right]=0.
\]

The relation p_n=DRq_n is a possible **open-chain normalization** after fixing y integration constants compatibly with the heat equation. It is not an unconditional prescription on periodic y. There the constants must match monodromy; setting every zero mode to zero can destroy the heat equation at subsequent orders.

No inverse of w or c is used. The only formal inverse in the Riccati equation is D+p−b, invertible as a Laurent series because its leading coefficient is z. For actual wave functions one also needs ψ≠0 locally. R must commute with D and t in the chosen gauge.

## 3. First coefficients

\[
q_1=-w/4,\qquad q_2=-Uw/8+w_x/4,
\]

\[
q_3=-U^2w/16+Uw_x/4+U_xw/8-w_{xx}/4-Vw/8.
\]

Thus, modulo x derivatives,

\[
-8q_3\equiv h_0=U^2w/2+wU_x+Vw.
\]

The corresponding open-chain p coefficients are

\[
p_1=-V/2,\quad p_2=-DR(Uw)/8+V_x/2,
\]

\[
p_3=-DR(h_0)/8+D^2R(Uw-w_x)/4.
\]

For compact formulas modulo x derivatives, let r_0=1 and

\[
r_{n+1}=(b+D)r_n-\sum_{k=1}^{n}p_kr_{n-k}.
\]

Then q_n≡c r_{n−1}. In particular

\[
r_3=b^3+3bb_x+b_{xx}-2bp_1-(p_1)_x-p_2,
\]

\[
\begin{aligned}
r_4={}&b^4+6b^2b_x+3b_x^2+4bb_{xx}+b_{xxx}\
&-(3b^2+3b_x)p_1-3b(p_1)_x-(p_1)_{xx}+p_1^2\
&-2bp_2-(p_2)_x-p_3.
\end{aligned}
\]

## 4. Two higher formal functionals

Removing x and y divergences with the prescribed potentials gives

\[
\mathcal C_4=-32\int q_4\,dxdy
=\int w[U^3+6UU_x+4U_{xx}+6UV],dxdy.
\]

Equivalently its density divided by 3 is

\[
U^3w/3+2UwU_x-4U_xw_x/3+UwKw.
\]

This is exactly the β→0 limit of the independently obtained finite-h fourth functional.

The next coefficient gives

\[
\begin{aligned}
\mathcal C_5=-64\int q_5\,dxdy
=\int\big\{&w[U^4+12U^2U_x+12U_x^2+16UU_{xx}+8U_{xxx}\
&+8U^2V+16U_xV+8UV_x+8V^2+8V_{xx}]\
&+2UwK(Uw)\big\}\,dxdy.
\end{aligned}
\]

The equality signs here are formal functional identities with vanishing/matching divergence fluxes. Arbitrary one-sided primitives can carry nonzero endpoint terms.

## 5. Independent exact verification

The script `check_continuous.py` checks full two-variable differential identities, not a y=x reduction. Set s_y=w, A_y=Uw, so V=s_x/2 and

\[
U_t=-UU_x-U_{xx}-s_{xx},\qquad s_t=-A_x+s_{xx}.
\]

For w, Uw, h₀, C₄ density and C₅ density, compute the complete t derivative, perform the indicated nonlocal-potential integrations by parts, and compute the Euler derivatives in U and s. All ten Euler derivatives vanish exactly.

For h₀, the A term −wA_xx/2 is equivalent to Uw s_xx/2. For C₄, −3UwA_xx=−3A_yA_xx is a full divergence.

For C₅, differentiating the term 2UwA_x in the integral gives 4A_x(Uw)_t after integration by parts. Collecting all derivatives of A into a single A_x term yields exactly

\[
4A_x(s_xw_x+w_{xxx})=A_xY(2s_x^2+4s_{xxx}).
\]

Use A_xy=(Uw)_x to replace it by −(Uw)_x(2s_x²+4s_xxx). The remaining local expression has both Euler derivatives identically zero. This certificate is recorded in `continuous_checks.json`.

These checks prove formal conservation laws. To obtain conserved total integrals, all surviving x/y fluxes must match or vanish. For example the C₄ step contains (3/2)Y(A_x²): merely taking U,s compactly supported does not force A_x(+∞)=0. This is an actual endpoint condition, not an inference from testing isolated solitons.

## 6. Limits of the conclusion

Mass w and momentum Uw are the first two coefficients. h₀ is the existing Hamiltonian. C₄ and C₅ supply higher polynomial orders; their principal terms U³w and U⁴w distinguish them from constant linear combinations of the earlier polynomial densities. Functional independence and global finite values still require a specified common admissible space.

Under a valid skew K and boundary conditions, the direct t-divergence identities give {C₄,H₀}=0 and {C₅,H₀}=0 in J₀=−[[0,D],[D,0]]. Translation invariance also gives commutation with P=∫Uw. The bracket {C₄,C₅} has **not** been verified in this note. Therefore this note does not establish a complete involutive hierarchy or Liouville integrability.

An additional common U drift in a periodic reduction contributes λ∫(δCₙ/δU)dy. It cannot be dropped: the leading term of δC₅/δU is 4U³w, whose y average is not a total x derivative by the basic constraints alone. C₅ is consequently a continuous full-flow benchmark, not yet a finite-h or periodically reduced theorem.

## 7. A simple continuous second bracket fails Jacobi

The direct 2+1 replacement of the one-dimensional two-boson bracket is

\[
J_2=-\tfrac12\begin{pmatrix}2RD^2&DU+2D^2\\UD-2D^2&wD+Dw\end{pmatrix}.
\]

It is skew and J₂δ∫Uw reproduces the full flow. However, for F=∫fU, G=∫gU, H=∫hw, its Jacobiator is

\[
\tfrac12\int h[f_x RD^2g-g_x RD^2f],dxdy.
\]

On a 2π torus take complex Fourier modes f=e^{i(x+y)}, g=e^{i(x+2y)}, h=e^{−i(2x+3y)}. The bracketed integrand equals 1/2, so the normalized Jacobiator is 1/4≠0. Complexification suffices to exclude a real Poisson operator. Thus the naive replacement of D by RD² in the (1,1) entry fails; it does not exclude other second brackets or a nonlocal recursion.

## 8. KP interpretation via y monodromy

Write ψ_y=Aψ with A=(D−b)^{-1}c of formal order −1, and B=−D²−V. Compatibility gives A_t=B_y+[B,A]. For a periodic y cycle its ordered monodromy P therefore satisfies P_t=[B,P]. This is the continuous counterpart of the finite-h monodromy construction, not a one-dimensional y=x restriction.

If F=P−1 has leading coefficient gD^{-1}, g≠0, and the first two monodromy coefficients g,p₂ are x,t independent in the chosen periodic gauge, then

\[
L=gF^{-1}+p_2/g=D+\ell_1D^{-1}+\ell_2D^{-2}+\cdots
\]

obeys L_t=[B,L]. The order-zero coefficient yields V_x=2(ℓ₁)_x. Hence, modulo an x-independent scalar gauge, B=−(L²)₊: this is the second KP flow. Formal residue traces ∫res Lⁿdx are conserved because the residue of a pseudodifferential commutator is an x derivative.

This supplies a structural explanation for a trace hierarchy, while leaving two distinct tasks: translating these traces back into the physical DLW variables with their mean constraints, and proving that their physical Poisson brackets commute. Conservation under one KP flow alone does not prove their involution in the previously constructed DLW bracket.
