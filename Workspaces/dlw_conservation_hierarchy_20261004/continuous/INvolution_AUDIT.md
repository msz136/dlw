# Independent audit: monodromy trace involution and mean reduction

Audited source: `../lax/MONODROMY_POISSON_PROOF.md`, especially §§3–5. This audit derives the identities directly. It does not use a named factorization theorem as a substitute for calculation.

## Verdict

The updated direct chain-rule proof establishes pairwise involution of the restricted trace functionals under the existing J_red on the specified formal periodic leaf. The Adler scale is **1/8 for raw residue traces**. The earlier proposed unrestricted Dirac argument has a genuine periodic-D zero-mode defect; the updated proof avoids it. A general identity between the full Dirac reduction and J_red is neither needed nor established.

## 1. Scale and factor pushforward

Use the original pairing hΣ∫ and J₀=−offdiag D in U,w. For raw unweighted functional derivatives the field kernel is −(1/h)offdiag D. Let g=hw/4, A=(U+g)/2, B=(U−g)/2. Their raw kernels are

\[
J_{AA}=-D/8,\qquad J_{BB}=D/8,\qquad J_{AB}=0.
\]

For K=D+q and X=D⁻¹φ, the Adler expression

\[
\mathcal A_K(X)=(KX)_+K-K(XK)_+
\]

is −φ_x. Its q-coefficient Poisson kernel is −D. Consequently M=D−A has +(1/8)Adler kernel, whereas N=D−B has −(1/8)Adler kernel. The sign change q=−A does not change the scalar kernel: it is applied twice.

For a product KH, differentiating a trace functional gives gradients HX and XK. Expanding yields

\[
\mathcal A_K(HX)H+K\mathcal A_H(XK)=\mathcal A_{KH}(X).
\]

For K⁻¹, its gradient at K is −K⁻¹XK⁻¹ and its variation is −K⁻¹δK K⁻¹. Substitution gives the **negative** Adler kernel at K⁻¹. Thus N⁻¹ has positive scale 1/8, as does M. Independence of the A_j,B_j factors and repeated product differentiation therefore give

\[
J_P(X)=\tfrac18\mathcal A_P(X),\qquad
P=\prod_j(D-B_j)^{-1}(D-A_j).
\]

No field denominators g_j or w_j occur. Inverses D−B_j exist formally by their monic leading coefficient. The pushed bracket satisfies Jacobi on this image because the starting field bracket is constant; an independent universal Adler Jacobi theorem is unnecessary here.

## 2. Trace gradients, commuting brackets and tangency

Extend F_n=Tr Lⁿ off the constraint leaf by holding the numerical a,b fixed, where

\[
L=a(P-1)^{-1}+b/a.
\]

One needs the leading coefficient of P−1 nonzero in this neighborhood. Cyclic differentiation gives

\[
X_n=\frac{\delta F_n}{\delta P}
=-na(P-1)^{-2}L^{n-1}.
\]

This commutes with P. Thus J_P(X_n)=(1/8)[(PX_n)_+,P], and

\[
\{F_m,F_n\}_0=\tfrac18\operatorname{Tr}X_m[(PX_n)_+,P]=0
\]

because [P,X_m]=0 and the trace is cyclic modulo total D derivatives.

There is a particularly short tangency proof. Put Q=PX_n, so [Q,P]=0. Then

\[
P_{t_n}=-\tfrac18[Q_-,P-1].
\]

Both Q_- and P−1 have order at most −1. Their scalar leading symbols commute, so this commutator has order at most −3. Therefore p₁ and p₂ are preserved pointwise. Before imposing constant G,

\[
p_1=-G,\qquad p_2=G_x+(G^2-T)/2,
\quad G=\sum g_j,\quad T=\sum U_jg_j.
\]

Hence G,T are preserved. On G,T constant this is the desired fixed mean leaf, with a=−G≠0, b=(G²−T)/2.

## 3. What the naive Dirac argument misses

For clarity take an arbitrary raw canonical scale κ in U,g:

\[
J=-\kappa\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\]

Let χ₁=Σg−G and χ₂=ΣUg−T. On the leaf their constraint matrix is

\[
C=-\kappa D\begin{pmatrix}0&G\\G&2T\end{pmatrix}.
\]

The finite matrix is invertible when G≠0; D is not invertible on an x circle. On nonzero Fourier modes the inverse's (2,2) entry is zero, and the projected coordinates p=PU,r=Pg commute with χ₁. Consequently the nonzero-mode Dirac correction in these coordinates vanishes.

However, the constant x mode of χ₂ is ∫ΣUg, the ambient translation momentum. It is not an ambient Casimir: its Hamiltonian vector is −κ(U_x,g_x), usually nonzero and tangent to the leaf. Therefore one cannot use an everywhere-defined D⁻¹ or claim that all pointwise constraints are second class. Quotienting that first-class mode would introduce a translation quotient; the previously constructed J_red retains translation as a nontrivial Hamiltonian symmetry. These are different general constructions.

## 4. Direct restriction identity that proves the needed theorem

Write lattice averages with a bar. Let c_g=G/N, t_g=T/N and set

\[
g=c_g+r,\quad U=p+m,\quad
m=(t_g-\overline{pr})/c_g,\quad \bar p=\bar r=0.
\]

For a full functional F with raw gradients f_U,f_g, chain differentiation on this graph gives

\[
f_p=P f_U-\alpha_F r,\quad
f_r=P f_g-\alpha_F p,\qquad
\alpha_F=\bar f_U/c_g.
\]

If F's ambient Hamiltonian vector preserves G pointwise, then D\bar f_U=0, so α_F is independent of x. Apply the same to another F=F_n,G=F_m. Mean contributions to their full canonical bracket integrate to zero. Expanding the reduced bracket produces

\[
\{F|_S,G|_S\}_{\rm red}-\{F,G\}_0|_S
=\kappa\alpha_G\,\delta F[U_x,g_x]
-\kappa\alpha_F\,\delta G[U_x,g_x].
\]

The remaining term proportional to α_Fα_G is ∫D(Σpr)=0. Every raw residue trace is invariant under common x translation: infinitesimally δP=[D,P], and Tr X[D,P]=Tr[P,X]D=0. Therefore the two terms displayed also vanish. Together with §2 this proves

\[
\{F_m|_S,F_n|_S\}_{\rm red}=0
\]

for every pair of the formal trace functionals. In original U,w normalization this is exactly the previously defined J_red and its original hΣ∫ pairing. The arbitrary κ cancels from the comparison; the actual raw U,g scale is κ=1/4.

This argument requires no inverse of D, including on its constant mode. It establishes bracket equality **on the translation-invariant tangent functional algebra used here**, not on every functional on the constrained graph.

The restricted Hamiltonian vector may differ from the ambient tangent vector by κ α_F times common x translation. Thus the bracket comparison should not be stated as unconditional equality of every reduced and unreduced Hamiltonian vector field.

### Stronger property specific to these traces

There is a direct common-shift gauge identity. Replace every U_j by U_j+2k(x), leaving g_j fixed. Both A_j and B_j increase by k. The formal scalar conjugation with f_x/f=k therefore sends every factor D−A_j,D−B_j to its shifted factor, and sends P,L to fPf⁻¹,fLf⁻¹. For any scalar PDO K,

\[
\operatorname{res}(fKf^{-1})=\operatorname{res}K
\]

pointwise: a differential operator remains differential, the order −1 term retains its leading coefficient, and lower-order terms cannot contribute to order −1. This argument can equivalently use the formal gauge automorphism D↦D−k and requires no actual periodic f.

It follows that each F_n is invariant under an arbitrary common U variation, including its constant mode. Thus ΣδF_n/δU_j=0, not merely an x constant. For this particular fixed-a,b trace extension α_Fn=0. The general chain-rule comparison above remains valid and avoids relying on this stronger observation; when the gauge identity is used, the trace vector fields themselves have no residual translation shear on the graph.

## 5. Scope

The proof is formal periodic-x pseudodifferential algebra with cyclic trace, finite periodic lattice, fixed constant G,T and G≠0. It proves Jacobi via the canonical field bracket and pairwise trace involution via explicit calculation. It does not prove independence of infinitely many traces, a global flow, Liouville completeness, or applicability to the nonperiodic 1(a),1(b),two-soliton relative phase spaces. Those claims need separate arguments.

## 6. Explicit periodic heat potential from the reduced SD flow

This confirms that periodic heat potentials need not be imported from a global tau representation. Let c=mean w≠0, gamma=mean Uw be fixed constants. Denote the Hamilton density by

\[
e=U^2w/2+\beta w^3/3+wU_x+wRDw/2,
\qquad \bar e=\operatorname{mean}e.
\]

The reconstructed reduced SD flow is

\[
U_t=-D(U^2/2+\beta w^2+U_x+RDw)+\lambda,
\quad w_t=-(Uw)_x+w_{xx},\quad
\lambda=2D\bar e/c.
\]

The last formula follows from 0=(mean Uw)_t: the full canonical part gives −2D\bar e+D²mean(Uw), and the common drift contributes cλ.

Choose the periodic potential

\[
V=RDw/2-hDw/4-\bar e/c+v_0(t).
\]

Since (E−1)R=(h/2)(E+1)P and mean Dw=0,

\[
(E-1)V=hDw/2=2Dg.
\]

The sum of the two Darboux Riccati residuals is

\[
U_t+D(U^2/2+\beta w^2)+U_{xx}+(h/2)w_{xx}+2V_x=0
\]

by direct substitution. Their difference is the prescribed w equation. Thus both full intertwining identities hold with this explicit periodic V, and the periodic monodromy evolution follows for the reduced SD flow itself. No individual g_j nonzero condition or periodic global tau reconstruction is used.
