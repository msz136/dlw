# General M: exact original Poisson pairs of actual high norming coordinates at the background

2026-10-11. This note computes the first actual Poisson brackets of the calibrated norming coordinates in [the augmented real state inverse](general_m_augmented_actual_high_norming_state_inverse_recovery_20261011.md), at its uniform nonalias physical background. The computation uses the original physical tensor and the exact all-M rational gauge identity. It is a background identity, not a nonlinear canonical-coordinate theorem. No checks were run and no shared records were edited.

Dependencies: [actual rational physical gauge bridge, §§1–4](all_m_rational_physical_gauge_hamilton_bridge_20261011.md), [actual vector-AKNS field bridge modulo constant frame](all_m_actual_trace_vector_akns_mod_frame_recovery_proof_20261011.md), and the actual high-frequency collision/basis normalization in [the Riesz lemma, §§6–8](general_m_actual_high_frequency_riesz_gap_lemma_20261011.md).

## 1. Original conventions and the background linear functionals

Use the original fixed-component-mean physical tensor, ordinary integral gradients and the convention

\[
\{F,G\}=dF(J_{\rm phys}dG)=dF(X_G),\qquad X_HF=\{F,H\}.
\tag{1}
\]

Keep the original current centered parameter \(\mu=\mu_{\rm original}-B\), \(B=\Gamma/(2c)\), nonzero \(S=M\delta\), \(L>0\), and uniform nonalias background. Let

\[
A_0(\mu)=\begin{pmatrix}\mu&q_0\\r_0&H_0\end{pmatrix}
\]

be its untraced vector connection. For each high label \(i=(\ell,n)\), \(|n|\ge N\), let \(\mu_i=\lambda_{\ell n}\) be the exact collision, with spatial eigenvalues

\[
y_{fi}-y_{\ell i}=i\kappa_n,\qquad \kappa_n=2\pi n/L,
\quad \gamma_i=\partial_\mu(y_f-y_\ell)(\mu_i).
\]

Choose the actual dual generator eigenvectors \(e_{fi},e_{\ell i}\), \(\ell_{fi},\ell_{\ell i}\), with dual pairings equal to one and crossed pairings zero. Define the trace-free matrices

\[
C_i^+=e_{\ell i}\ell_{fi},\qquad C_i^-=e_{fi}\ell_{\ell i},
\]

and the actual periodic adjoints

\[
W_i^+(x)=e^{-i\kappa_nx}C_i^+,\qquad
W_i^-(x)=e^{i\kappa_nx}C_i^-.
\tag{2}
\]

They satisfy \((W_i^\pm)'=[A_0(\mu_i),W_i^\pm]\), including for the trace-normalized connection, since scalar matrices do not change this commutator. The actual Born covectors are

\[
\Gamma_i^\pm(f)=\frac1L\int_0^L
\operatorname{tr}(W_i^\pm\,\delta A(f))dx.
\tag{3}
\]

Although (3) is stated in the vector frame, it is also an actual original physical covector. If \(U=\bar E^{-1}\delta\bar E\), the original connection variation in that frame is \(\delta A+U'-[A,U]\). The last term integrates to zero against the periodic adjoint, by its adjoint equation and periodic integration by parts. A scalar trace-normalization variation also pairs to zero because \(\operatorname{tr}W_i^\pm=0\). Thus (3) agrees with the original affine-connection linear functional with the conjugated fixed background adjoint. It has an ordinary original gradient and actual original Hamiltonian vector at this point.

## 2. The exact physical Hamiltonian vector of each Born covector

The R-tensor derivation in the rational gauge bridge contracts its algebraic identity with a periodic solution of \(W'=[L_\mu,W]\). It does not require that this solution be a trace-power adjoint. Consequently, at the background it applies to each \(W_i^\pm\) of (2). The original field of the normalized covector (3) has generator with residue

\[
-\frac{\omega_i}{L}W_i^\pm,
\qquad \omega_i=\frac{S^2-\mu_i^2}{16S}.
\]

Repeating the already proved moving-frame calculation gives, at this background,

\[
\delta A_{X_{\Gamma_i^\pm}}
=\frac{\omega_i}{L}[E_{00},W_i^\pm]
+\text{a constant-frame correction}.
\tag{4}
\]

Here this correction vanishes exactly. The original covector gradient and its original \(J\)-field have one nonzero Fourier mode, because the original background connection is affine with constant coefficient matrices. The actual background coefficient derivative \(D\Pi_0\) is a Fourier multiplier. Thus its \(\delta a,\delta b\) have zero means and \(\delta H=0\). The first term of (4) has the same nonzero frequency and the same zero means. The constant correction \((a_0X,-Xb_0,[H_0,X])\) must therefore satisfy

\[
a_0X=0,\qquad Xb_0=0,\qquad[H_0,X]=0.
\]

The actual uniform observability/controllability and simple slow spectrum force \(X=0\). It follows that

\[
\boxed{\delta A_{X_{\Gamma_i^\pm}}
=\frac{\omega_i}{L}[E_{00},W_i^\pm].}
\tag{5}
\]

This uses the original physical tensor. The auxiliary canonical expression on the right is justified only by the actual gauge computation and the physical finite graph at the background. A trace-normalized \(J_*=E_{00}-I/M\) gives the same commutator.

## 3. Different channels: exact pencil orthogonality

By (1), (3), (5), any two of these covectors have bracket

\[
\{\Gamma_i^\sigma,\Gamma_j^\tau\}
=\frac{\omega_j}{L^2}\int_0^L
\operatorname{tr}\big(W_i^\sigma[E_{00},W_j^\tau]\big)dx.
\tag{6}
\]

Write each constant rank-one adjoint as \(C_i=e_{pi}\ell_{qi}\), with phase \(e^{d_ix}\), where \(d_i=y_{pi}-y_{qi}\). For \(+\), \(d_i=-i\kappa_n\); for \(-\), \(d_i=i\kappa_n\). Fourier integration kills (6) unless \(d_i+d_j=0\).

For \(\mu_i\ne\mu_j\), the exact rank-one spectral pencil gives

\[
(y_{qi}-y_{pj})\ell_{qi}e_{pj}
=(\mu_i-\mu_j)\ell_{qi}E_{00}e_{pj}.
\tag{7}
\]

Using it twice yields

\[
\operatorname{tr}(C_i[E_{00},C_j])
=-\frac{d_i+d_j}{\mu_i-\mu_j}
(\ell_{qi}e_{pj})(\ell_{qj}e_{pi}).
\tag{8}
\]

Thus it is zero whenever the Fourier phases could pair. This cancels different slow channels at the same spatial frequency, and also cancels the reflected opposite-frequency same-sign adjoints. The already separated high label windows make distinct collision labels have distinct \(\mu_i\). No approximate leading-frequency eigenvectors are used in (7)–(8).

The remaining case is the same collision with opposite signs. Actual dual normalization and the finite-dimensional eigenvalue derivative give

\[
\operatorname{tr}(C_i^+[E_{00},C_i^-])
=\ell_{fi}E_{00}e_{fi}-\ell_{\ell i}E_{00}e_{\ell i}
=\gamma_i.
\tag{9}
\]

Combining (6)–(9), for all high collision labels,

\[
\boxed{
\{\Gamma_i^+,\Gamma_j^-\}_0
=\delta_{ij}\frac{\omega_i\gamma_i}{L},\qquad
\{\Gamma_i^+,\Gamma_j^+\}_0
=\{\Gamma_i^-,\Gamma_j^-\}_0=0.
}
\tag{10}
\]

The minus-plus bracket is the negative transpose, as required by the original convention. The subscript 0 emphasizes evaluation at the uniform state.

## 4. Actual norming coordinates and the real positive-mode form

The exact calibrated functions satisfy \(D\nu_i^\pm(0)=L\Gamma_i^\pm\). A Poisson bracket at one point depends only on these actual first differentials. Hence

\[
\boxed{
\{\nu_i^+,\nu_j^-\}_0
=\delta_{ij}\,L\omega_i\gamma_i,\qquad
\{\nu_i^+,\nu_j^+\}_0
=\{\nu_i^-,\nu_j^-\}_0=0.
}
\tag{11}
\]

For real physical fields the negative reflected label is \((M-\ell,-n)\). Put positive-mode real-chart coordinates \(\alpha_i=\nu_i^+\), \(\beta_i=\bar\nu_i^-\), \(n>0\). The complexified original brackets of these real-analytic functions are

\[
\{\alpha_i,\bar\beta_j\}_0=\delta_{ij}C_i,
\qquad C_i=L\omega_i\gamma_i,
\]

\[
\{\alpha_i,\beta_j\}_0=
\{\alpha_i,\bar\alpha_j\}_0=
\{\beta_i,\bar\beta_j\}_0=0.
\tag{12}
\]

At the pure-imaginary background collisions \(\omega_i\) is real. Moreover the original uniform generator is anti-Hermitian there and has parameter derivative the Hermitian projector \(P\). Thus each spatial eigenvalue derivative is its unit-vector expectation of \(P\), a real number; \(\gamma_i\) is real and \(\gamma_i=1+O(n^{-2})>0\) after increasing \(N\). Consequently \(C_i\) is real and nonzero. In \(\alpha=x+iy\), \(\beta=u+iv\), formula (12) gives

\[
\{x_i,u_j\}_0=\{y_i,v_j\}_0=\tfrac12\delta_{ij}C_i,
\qquad \{x_i,v_j\}_0=\{y_i,u_j\}_0=0.
\tag{13}
\]

Thus the real positive channels form actual nondegenerate background Poisson pairs. Their coefficients satisfy \(|C_i|\asymp n^2\), uniformly in the finitely many slow channels. This is an order-two inverse of a weak form on the low Hilbert chart, not a bounded canonical tensor on all \(\ell^2\) cotangent vectors.

## 5. Actual squared-gap linearization and the uniform-bound obstruction

The actual gap Hessian is

\[
g_i^{[2]}=-4\Gamma_i^+\Gamma_i^-/\gamma_i^2
=-\frac{4}{L^2\gamma_i^2}\nu_i^+\nu_i^-.
\tag{14}
\]

Since \(dg_i(0)=0\), variations of the nonlinear Poisson tensor do not contribute to the first derivative of its Hamiltonian field at the background. Equations (1), (11), (14) therefore force

\[
\boxed{
\frac{d}{dt}\nu_i^+=-\frac{4\omega_i}{L\gamma_i}\nu_i^+,
\qquad
\frac{d}{dt}\nu_i^-=\frac{4\omega_i}{L\gamma_i}\nu_i^-
}
\tag{15}
\]

for the linearization of the original complex gap Hamiltonian field. The other high-coordinate linear components vanish. Finite low Fourier-coordinate components vanish as well by Fourier-mode separation. The signs in (15) use \(X_HF=\{F,H\}\); changing this convention would reverse them.

The obstruction also applies to genuine real Hamiltonians. On the positive-mode real chart, \(g_i^{[2]}=-4\alpha_i\bar\beta_i/(L^2\gamma_i^2)\). Since the background coefficients are real, (12) gives

\[
DX_{\operatorname{Re}g_i}(0):\quad
\dot\alpha_i=-\frac{2\omega_i}{L\gamma_i}\alpha_i,
\qquad
\dot\beta_i=\frac{2\omega_i}{L\gamma_i}\beta_i,
\tag{16}
\]

\[
DX_{\operatorname{Im}g_i}(0):\quad
\dot\alpha_i=\frac{2i\omega_i}{L\gamma_i}\alpha_i,
\qquad
\dot\beta_i=\frac{2i\omega_i}{L\gamma_i}\beta_i.
\tag{17}
\]

The conjugate coordinates evolve by the conjugate equations. Thus (16) consists of real dilation blocks and (17) of real rotation blocks; both have operator norm proportional to \(n^2\). These are the first derivatives of the actual real original fields, because both real charges have zero differential at the background.

These are genuine finite Fourier physical linearized directions. The separately proved [fixed-gap balanced-low field theorem](general_m_fixed_gap_balanced_hamilton_flow_20261011.md) supplies each individual actual field analytically into \(X_0\). Via the bounded derivative and inverse of the augmented state chart, (15)–(17) imply that the operator norms of \(DX_{g_i}(0)\), \(DX_{\operatorname{Re}g_i}(0)\) and \(DX_{\operatorname{Im}g_i}(0)\) there are at least a constant times \(n^2\). Thus uniform-in-\(i\) original complex or real gap-field \(C^1\)/local Lipschitz bounds on one low neighborhood are impossible. A uniformly bounded family of holomorphic fields on one common complex low ball is also impossible, since the Banach Cauchy estimate would bound all derivatives at zero uniformly.

This last \(C^0\) obstruction is stated for a common complex holomorphic bound. A bare uniform real-domain \(C^0\) bound on real-analytic functions alone does not control derivatives, so this argument does not assert that broader implication.

Dividing each charge by its fixed nonzero background \(\omega_i\) removes the quadratic growth in this linearization: its eigenvalues become \(\mp4/(L\gamma_i)\). This is a useful candidate normalization for a later uniform nonlinear-field theorem. It does not prove that theorem or a common nonlinear flow window by itself.

## 6. Precise scope

The first brackets (10)–(13), channel orthogonality and original complex/real gap linearizations (15)–(17) are exact actual-background identities. They do not require a hyperelliptic curve, cyclic collision monodromy or a scalar-M=2 extension. The rational-gauge contraction is used with each actual periodic offdiagonal adjoint, which is available precisely because the collision has a geometrically double multiplier.

Away from the background, these norming functions have nonlinear differentials, moving centers and frame/holonomy dependence. No assertion that their brackets remain diagonal or that they provide a nonlinear Darboux chart has been proved here. Consequently this computation alone gives neither invariant actions, squared-eigenfunction completeness nor a general-M Liouville theorem. It supplies a concrete actual Poisson starting point and an exact frequency normalization that any such nonlinear construction must respect.
