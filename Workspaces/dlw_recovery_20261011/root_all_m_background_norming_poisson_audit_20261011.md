# Root audit: actual high norming Poisson pairs and necessary frequency normalization

2026-10-11. Read `general_m_background_norming_original_poisson_pairing_recovery_proof_20261011.md` §§1–6 in full. Independently checked its gauge contraction, cross-channel pencil calculation, actual calibration and real-coordinate signs. No machine checks were rerun.

At an exact uniform collision \(\mu_i\), the actual dual generator vectors give periodic rank-one adjoints \(W_i^+=e^{-ik_nx}e_\ell\ell_f\), \(W_i^-=e^{ik_nx}e_f\ell_\ell\). Periodic integration by parts removes the moving-frame derivative from the Born covectors \(\Gamma_i^\pm=L^{-1}\int\operatorname{tr}(W_i^\pm\delta A)\). Scalar normalization also drops out because these adjoints are traceless. Their covectors are therefore covectors of the original physical state, rather than of an independently chosen vector model.

The original rational tensor identity contracts any periodic adjoint satisfying its actual ODE; it does not require a trace-power adjoint. Applying it gives the vector field contribution \((\omega_i/L)[E_{00},W_i^\pm]\). At the uniform state the original gradient has a single nonzero Fourier mode. The physical coefficient chart is then a Fourier multiplier, and its full holonomy and coefficient-mean derivatives vanish. The residual constant frame must satisfy \(a_0X=Xb_0=[H_0,X]=0\). Background observability and the simple slow spectrum force \(X=0\). This step is why the auxiliary canonical expression is justified here.

For distinct exact collisions, the pencil identity gives

\[
\operatorname{tr}(C_i[E_{00},C_j])
=-\frac{d_i+d_j}{\mu_i-\mu_j}
(\ell_{qi}e_{pj})(\ell_{qj}e_{pi}).
\]

The Fourier integral vanishes unless \(d_i+d_j=0\); in that remaining case this expression vanishes. Thus all different labels pair to zero, including the reflected negative labels. At one collision, the opposite-sign adjoints instead give \(\operatorname{tr}(C_i^+[E_{00},C_i^-])=\gamma_i\), by the exact eigenvalue derivative. With \(D\nu_i^\pm=L\Gamma_i^\pm\), the actual background brackets are

\[
\{\nu_i^+,\nu_j^-\}_0=\delta_{ij}L\omega_i\gamma_i,
\qquad \{\nu_i^+,\nu_j^+\}_0=\{\nu_i^-,\nu_j^-\}_0=0.
\]

At the purely imaginary collisions, anti-Hermitian normality of the original generator makes \(\gamma_i\) real, and \(\gamma_i=1+O(n^{-2})\). The positive real-chart variables \(\alpha_i=\nu_i^+\), \(\beta_i=\overline{\nu_i^-}\) obey \(\{\alpha_i,\overline\beta_j\}=\delta_{ij}C_i\), \(C_i=L\omega_i\gamma_i\), and the other displayed pairings vanish. Consequently \(\{\operatorname{Re}\alpha_i,\operatorname{Re}\beta_j\}=\{\operatorname{Im}\alpha_i,\operatorname{Im}\beta_j\}=\delta_{ij}C_i/2\). These are nondegenerate real pairs with coefficients of order \(n^2\), not bounded canonical \(\ell^2\) cotangent pairs.

The actual gap Hessian \(g_i^{[2]}=-4\nu_i^+\nu_i^-/(L^2\gamma_i^2)\), together with the convention \(X_HF=\{F,H\}\), gives linearized rates \(\mp4\omega_i/(L\gamma_i)\). Since \(dg_i(0)=0\), differentiating the nonlinear Poisson tensor contributes no extra term. Thus the original unweighted gap fields cannot have uniform high-frequency \(C^1\) or common-complex-ball holomorphic bounds. The same obstruction holds for real and imaginary components, with the corresponding factor of two. The argument does not infer derivative bounds merely from a real-domain \(C^0\) bound.

**PASS:** exact actual-background Poisson pairs, cross-channel orthogonality and the quadratic-growth obstruction are proved. The fixed-background normalization \(g_i/\omega_i\) removes that growth at the linearized level and supplies a concrete next route. Its nonlinear uniform-field estimate must be proved separately. No nonlinear diagonal norming bracket, invariant action chart or general-M completeness is asserted.
