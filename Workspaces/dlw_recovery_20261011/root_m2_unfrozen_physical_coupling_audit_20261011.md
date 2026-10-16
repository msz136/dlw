# Root audit: the regular M=2 phase is physically unfrozen

This audit reads §10 of `m2_regular_variable_action_original_symplectic_phase_20261011.md` against its established actual reduced state inverse and original physical equations. It adds no frozen-field ansatz and does not replace the original bracket.

## Reconstruction and prescribed flux

Put \(S=hc/4\ne0\), \(\delta=S/2\), \(2B(t)=\Gamma(t)/c\). The free source has \(\langle u\rangle=\langle v\rangle=0\), and the exact original fields are
\[
U_0=2B+(1-2v/S)u,\quad U_1=2B-(1+2v/S)u,
\qquad w_0=8(\delta+v)/h,\quad w_1=8(\delta-v)/h.
\]
Direct multiplication gives \((w_0+w_1)/2=c\) and \((U_0w_0+U_1w_1)/2=2Bc=\Gamma(t)\). No choice of \(\Gamma\) was substituted for compatibility. The centered autonomous phase has \(B=0\); arbitrary \(B(t)\) is recovered by the already proved common translation and common field addition.

## Original dynamics

For the original first equation at lattice index zero,
\[
\delta_-U=2u/h,\quad M_-w=c,\quad
U_0^2-U_1^2=8Bu-8u^2v/S,\quad
w_0^2-w_1^2=256\delta v/h^2.
\]
Multiplying that equation by \(h/2\), and using the original second equation for \(w_0\), yields
\[
u_t=-u_{xx}-2Sv_x+(2/S)D(u^2v)-2B(t)u_x,
\qquad
v_t=v_{xx}-(S/2)u_x+(2/S)D(uv^2)-2B(t)v_x.
\]
The cross derivatives and nonlinear products remain at \(B=0\). Thus removing external flux does not remove intrinsic coupling.

There is also a direct original-equation check of the order-two time normalization. At \(u=v=0\), the Fourier generator is
\[
\begin{pmatrix}k_n^2&-2Sik_n\\-(S/2)ik_n&-k_n^2\end{pmatrix},
\quad \sigma_n^\pm=\pm\sqrt{k_n^4-S^2k_n^2}.
\]
Its high-frequency eigenvalues are \(\pm(k_n^2-S^2/2+O(k_n^{-2}))\). The required heat directions therefore have the original unit coefficient, consistently with the exact spectral torque's negative quadratic leading term. This is an analytic linearization check, not a nonlinear spectral inverse or a replacement for the normalized frequency proof.

## An ordinary open unfrozen subphase exists

Shrink the actual source neighborhood to \(\|v\|_\infty<|S|/4\). In the centered phase the factors \(1\pm2v/S\) never vanish. Hence either \(U_0\equiv0\) or \(U_1\equiv0\) would imply \(u\equiv0\).

At the nonzero-action base, each finite-support real Cartesian tangent is an actual finite-support \(a,q\) tangent: the two by two derivative at index \(n\) is invertible since \(w_nz_n\ne0\). These finite-support tangents are dense in every \((h^r)^2\). The actual higher state inverse has an isomorphic derivative onto \(H^r_0\times H^{r+1}_0\) on the same low domain. Consequently physical core tangent images are dense in every such mixed space, though the core topology itself is stronger than the ambient topology.

Choose \(r\) high enough for evaluation of \(u(x_0)\) and \(v_x(x_1)\) to be continuous. A mean-zero test pair has both evaluations nonzero, so a finite-support core tangent also has both nonzero. A sufficiently small parameter displacement avoids the isolated zeros of both analytic evaluations. Around its endpoint an ordinary core-open box has \(|u(x_0)|>\epsilon_1\), \(|v_x(x_1)|>\epsilon_2\). Both original \(U\) components are nonzero functions there, and \(v\) is nonconstant. Two unrestricted bounded-sequence parameter groups remain.

At \(u(x_0)\ne0\),
\[
\det\frac{\partial(U_0,U_1)}{\partial(u,v)}=-4u(x_0)/S\ne0.
\]
Independent local physical variation therefore occurs at fixed external flux, rather than by a gauge change of a frozen branch.

The open box actually excludes either identically zero component for every real external \(B\), not only \(B=0\). The factors \(g_\pm=1\pm2v/S>1/2\). If \(U_0\equiv0\), then \(u=-2B/g_-\); its zero mean gives \(B\langle g_-^{-1}\rangle=0\), hence \(B=0\) and \(u=0\). The same calculation for \(U_1\) uses \(g_+\). This contradicts \(u(x_0)\ne0\) on the chosen subbox.

## Genuine original motion and scope

All \(J_n=w_nz_n\ne0\). The proved actual original-time torque is \(\Omega_{H,n}=-k_n^2-2i\eta k_n+r_n(J)\), with bounded \(r\). Static motion would require every torque to vanish; rigid translation would require \(\Omega_{H,n}=i\alpha k_n\) for one real constant \(\alpha\). The quadratic real part contradicts both requirements on the infinitely many active indices.

**PASS:** this regular phase and its open unfrozen restriction preserve genuinely coupled infinite field freedoms, actual original dynamics and original weak symplectic structure. The result is local on a declared stronger Banach function topology near a sufficiently small nonzero background. It does not cover every smooth Cauchy datum, all \(M\), or a whole-variable-action common domain for all higher auxiliary hierarchy times. The real-line \(U_0=0\), \(s=Ax\) construction with a new symplectic form remains a separate audit baseline.
