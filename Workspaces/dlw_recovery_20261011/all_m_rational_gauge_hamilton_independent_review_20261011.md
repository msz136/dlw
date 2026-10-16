# All M: independent review of the rational physical gauge–Hamilton bridge

2026-10-11. Actual full reading and algebraic review of [the main rational-gauge proof](all_m_rational_physical_gauge_hamilton_bridge_20261011.md), §§1–9. No old or new machine checks were run. This note verifies the bridge and its limits; it does not turn a framed state inverse into an action inverse.

**Result.** The bounded-at-infinity finite-rational theorem, including arbitrary finite orders at cyclic poles and the exceptional points \(\mu=\pm S\), passes the checks below. The moving-frame sign and scalar normalization are essential. The new global meromorphic gauge exists, but its growth bound does not provide the required infinite-pole or entire-tail Hamilton approximation.

## 1. Exact source tensor contraction and the gauge sign

Use the main proof's \(H_i=E_{ii}-I/M\), \(K_i(a)\), \(a=\lambda/S\), \(b=\mu/S\), \(W'= [L_\mu,W]\), and \(C^\pm=R\pm B/2\). Let
\[
G=\operatorname{tr}_2(C^+(I\otimes W)).
\]
Contracting
\([C^+,L_\lambda\otimes I]+[C^-,I\otimes L_\mu]=0\)
against \(I\otimes W\) gives
\[
[L_\lambda,G]=\operatorname{tr}_2(C^-(I\otimes W')).
\]
Here the second partial trace is computed by cyclicity in its second matrix factor; the sign is positive because the commutator in the original tensor identity is \([C^-,I\otimes L_\mu]\). Since both \(C^\pm\) are independent of \(x\),
\[
G'-[L_\lambda,G]
=\operatorname{tr}_2(B(I\otimes W')).
\]
The physical Hamilton generator is therefore \(g=-G/16\), with
\[
\delta L_\lambda=g'-[L_\lambda,g].
\]
There is no sign flip to \(+G/16\).

This agrees with the constrained free-coordinate source bracket. Because \(\Delta_m=0\), \(d_m=S-\sum_{i<m}d_i\), and \(\sum_iH_i=0\), the actual gradients are
\[
\partial_{\Delta_i}F=\operatorname{tr}(H_iW),\qquad
\partial_{d_i}F=\operatorname{tr}((K_i(b)-K_m(b))W).
\]
Apply \(J_{\rm phys}=-\operatorname{offdiag}(D)/16\). In the connection variation the \(\Delta\) terms recombine as
\(\sum_iH_iD\operatorname{tr}(K_i(b)W)\), and the \(d\) terms as
\(\sum_iK_i(a)D\operatorname{tr}(H_iW)\). Their sum is exactly the stated partial trace with \(B\). Thus the use of all \(M\) indices in that tensor contraction introduces no fictitious independent last component.

## 2. Residues, special triangular points, and higher derivatives

For \(\rho=(1-ab)/(a-b)\), contraction of the flip gives \(W^0\), and contraction of the signed flip gives
\[
T_s(W)=\sum_{i\ne j}s_{ij}W_{ij}E_{ij}.
\]
Consequently the main proof's explicit formula is
\[
g=-\frac1{16}\left[
\rho W^0+T_s(W)+\sum_iH_i\operatorname{tr}(K_i(b)W)\right].
\]
Its residue at \(\lambda=\mu\) is
\[
\alpha(\mu)W^0,\qquad
\alpha(\mu)=\frac{\mu^2-S^2}{16S}.
\]
This retains the sign of \(S\).

At \(\mu=S\), \(W\) is upper triangular, \(\rho=-1\), the signed flip is its strict upper part and the Cartan contraction is its traceless diagonal part. These cancel \(-W^0\) exactly. At \(\mu=-S\), the lower-triangular calculation has \(\rho=1\), signed flip equal to the negative strict lower part, and Cartan contraction equal to the negative traceless diagonal part. Thus \(g=0\) in both cases. A triangular normalized monodromy need not equal \(I\); only its diagonal class data are fixed by the means.

Since \(\alpha'(\varepsilon S)=\varepsilon/8\), the first \(\mu\) derivative has a simple pole with residue \(\varepsilon W^0/8\). For a pole of order \(k\), the relevant highest coefficients are
\[
\partial_\mu^{k-1}g:
\quad\frac{(k-1)!\alpha(\mu)W^0}{(\lambda-\mu)^k}
\quad(\mu\ne\pm S),
\]
\[
\left.\partial_\mu^kg\right|_{\mu=\varepsilon S}:
\quad\frac{k!\varepsilon W^0/8}{(\lambda-\varepsilon S)^k}.
\]
The apparent order \(k+1\) term at the exceptional point is zero. These factors follow by differentiating the rational kernel; they do not require a new spectral asymptotic assumption.

The highest coefficient of any finite pole in a physical gauge solves
\(R_k'=[L_\mu,R_k]\). Cyclicity supplies the whole traceless periodic-adjoint space from the \(M-1\) trace powers, including a cyclic Jordan matrix. Subtracting the displayed actual parameter-derivative Hamilton generators lowers the pole order and preserves the physical tangent condition. Finite recursion is therefore legitimate. All the needed fixed-order parameter derivatives belong to the actual trace-field \(C^\infty\) closure by ordinary finite difference quotients.

## 3. Normalized moving frame and the constant-gauge obstruction

Let \(E=T_z\operatorname{diag}(1,G)\) be the actual state-dependent periodic frame. The normalization
\[
\bar E=(\det G)^{-1/M}E
\]
has constant determinant because \(\det T_z\) is state independent. Its transformed traceless connection is
\[
\bar A_\lambda=
\begin{pmatrix}\lambda&a\\b&H\end{pmatrix}
-\frac{\lambda+\operatorname{tr}H}{M}I .
\]
Indeed the identity \((\log\det G)'=\operatorname{tr}V-\operatorname{tr}H\) supplies exactly the scalar correction needed to replace the original pointwise trace by this constant block trace.

For a state variation, the transformed generator is
\[
\bar g=\bar E^{-1}g\bar E-\bar E^{-1}\delta\bar E.
\]
The frame-variation term has the **minus** sign. It follows by differentiating
\(\bar A=\bar E^{-1}L\bar E-\bar E^{-1}\bar E'\).
Its trace is zero because \(\det\bar E\) is state independent.

If \(g\) is independent of \(\lambda\), so is \(\bar g\). The \(\lambda\) coefficient forces \(\bar g=\operatorname{diag}(t,K)\). The top diagonal equation is
\[
t'=-\delta\operatorname{tr}H/M .
\]
Periodicity gives \(\delta\operatorname{tr}H=0\), \(t\) constant. The bottom equation is
\(\delta H=K'-[H,K]\).
Because \(\delta H\) is spatially constant, every nonzero Fourier mode satisfies
\((ik-\operatorname{ad}H)K_k=0\). The declared internal nonalias condition eliminates these modes. Hence \(K\) is constant and
\[
\delta a=ta-aK,\qquad
\delta b=Kb-bt,\qquad
\delta H=-[H,K].
\]
With \(X=tI-K\) this is the constant \(GL_m\) orbit tangent
\((aX,-Xb,[H,X])\).

The last elimination uses the proved transversality of the actual finite physical graph to this orbit, not just freeness of the \(GL_m\) action. Freeness alone would be insufficient. The finite-graph transversality is established at the uniform state by the endpoint-constraint derivative/minor in [the independent physical-constraint proof](general_m_physical_gauge_fredholm_and_spectral_constraints_20261011.md), §§4–6, and persists on the specified small physical neighborhood. Therefore the remaining physical variation is zero. Trace freeness then also gives \(t=K=0\).

This verifies the precise final step of the finite-rational theorem; it does not assume a Hamilton density theorem.

## 4. Global Krylov gauge: existence and remaining approximation problem

For a fixed cyclic starting point choose one fixed cyclic vector \(v\), and form
\[
P(\lambda)=[v,N_\lambda v,\ldots,N_\lambda^{M-1}v],\qquad
D(\lambda)=\det P(\lambda).
\]
Both are entire, with \(D\not\equiv0\). On \(D\ne0\), characteristic-coefficient variations zero imply that the companion matrix has zero variation. Differentiating \(NP=PC\) gives
\(\delta N=[\delta P\,P^{-1},N]\); subtract its scalar trace without changing the commutator. The main proof's
\[
g=\delta Y\,Y^{-1}+YG_0Y^{-1}
\]
has the correct periodic sign. At \(x=L\),
\[
g(L)=\delta NN^{-1}+NG_0N^{-1}=G_0=g(0)
\]
using \(\delta N=[G_0,N]\).
Thus one global meromorphic periodic gauge exists, with finite-order poles at the discrete zeros of \(D\).

The stated exponential-type numerator estimate follows from Gronwall and the finite polynomial formulas for \(P,\operatorname{adj}P,\delta P\). It supplies no lower bound for \(D\), no uniform residue control, and no convergence of physical tangent truncations. Frame poles can occur even at cyclic monodromy; noncyclic points require additional adjoint channels. Neither compact-\(\lambda\) rational approximation nor the full framed \(L^2\) state inverse resolves this.

Finally, the polynomial highest-channel calculation is correct: in the normalized frame a highest coefficient is \(\operatorname{diag}(t_N,K_N)\), with \(t_N\) constant and \(K_N\) constant in the centralizer of \(H\). For simple \(H\) that channel has dimension \(m\), not one. It remains necessary to match the slow channels and control the infinite meromorphic/entire remainder on the physical finite graph.

## 5. Exact conclusion

The bounded finite-rational cyclic-pole physical kernel has no missing directions beyond the actual trace Hamilton closure. General-\(M\) invariant-kernel maximality remains open at the infinite spectral-tail step. In particular the uniform closed-gap state has zero actual trace Hamilton fields and a large mean-zero common differential kernel; it is excluded from any inference that all kernel directions automatically possess the finite-rational representation. This audit does not make that inference.
