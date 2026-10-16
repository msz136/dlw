# Root audit: actual uniform all-M resonances and rank-two blocks

The complete `general_m_uniform_resonance_independent_audit_20261011.md` was read and its dispersion, labels, asymptotics and uniform resolvent argument independently checked. This audit covers the uniform background, not the separate source-dependent gap theorem. No checks were run.

## Actual dispersion and corrected grid

For \(A_\chi(\lambda)=\lambda\mathbf1\mathbf1^T/M+C_0\), \((C_0)_{ij}=\delta\operatorname{sign}(j-i)\), subtracting consecutive eigenvector equations gives \((y+\delta)v_{i+1}=(y-\delta)v_i\). The first equation then gives the actual rational dispersion
\[
\lambda=\mathcal R(y)=S\frac{(y+\delta)^M+(y-\delta)^M}{(y+\delta)^M-(y-\delta)^M},\qquad S=M\delta.
\]
Its slow poles are \(p_\ell=-i\delta\cot(\pi\ell/M)\), with positive residues \(r_\ell=\delta^2-p_\ell^2\), and exact regular part \(-p_\ell\). Polynomial division gives
\[
\mathcal R(y)=y+\sum_\ell\frac{r_\ell}{y-p_\ell},\quad
A=\sum r_\ell=\delta^2(M^2-1)/3.
\]
The actual exponent branches satisfy \(y_f=\lambda-A/\lambda+O(\lambda^{-3})\), \(y_\ell=p_\ell+r_\ell/\lambda-r_\ell p_\ell/\lambda^2+O(\lambda^{-3})\). Their Floquet collision is \(y_f-y_\ell=K_n\), \(K_n=2\pi in/L\). Inverting this difference gives
\[
\lambda_{\ell n}=K_n+p_\ell+(A+r_\ell)/K_n
-p_\ell(A+2r_\ell)/K_n^2+O(|n|^{-3}).
\]
Thus \(K_n+p_\ell\) is only a leading grid; it cannot be used as the exact collision. The coefficient follows directly: write \(\lambda=K+p+b/K+c/K^2\), expand \(1/\lambda=K^{-1}-pK^{-2}+\cdots\), and match \(b=A+r\), \(c=-p(A+2r)\).

## Actual high collisions are semisimple and isolated

The exact quadratic yields \(y_s=-K/2+\sqrt{K^2/4+Kp_\ell+\delta^2}\), with the analytic-at-infinity square-root branch \(K(1+4p_\ell/K+4\delta^2/K^2)^{1/2}/2\), not an unspecified principal branch. For real \(\delta\), the high solutions and \(\lambda_{\ell n}\) are imaginary. Hence \(A_\chi\) and its traceless normalization are anti-Hermitian there; actual monodromy is unitary.

Under the audited no-adjoint-alias condition, \(\rho_\ell=e^{Lp_\ell}\) are distinct. The slow multipliers approach these distinct numbers; exactly one collides with the fast multiplier at the labeled point. The repeated multiplier has multiplicity two and a uniform separation from the others. The slope of the exponent difference is \(1+O(n^{-2})\), so the multiplier difference has a nonzero uniformly bounded-below derivative.

Trace normalization multiplies every multiplier by \(e^{-L\lambda/M}\); at imaginary centers its modulus is one. Distances and collision slopes are preserved, but normalized slow multipliers have a common rotating phase and are not asserted to converge to \(\rho_\ell\).

## Uniform Riesz statement and scope

At each background collision take a circle of radius one quarter of a fixed lower separation. Unitarity supplies a uniform resolvent bound. Duhamel, applied to the fixed principal coefficient \(P\) or \(P-I/M\), gives
\[
\|T(\lambda)-T(\lambda_*)\|\le L|\lambda-\lambda_*|e^{L|\lambda-\lambda_*|}.
\]
A single positive spectral radius therefore keeps the contour spectrum-free and its projection analytic of rank two for every sufficiently high index and every channel. The actual collision grids themselves are uniformly separated by the finite nonalias distances modulo \(2\pi i/L\).

**PASS:** exact uniform-background collision labeling and uniformly isolated rank-two actual monodromy blocks. This is not a uniform source perturbation bound for the raw variable-principal physical connection. Such a bound must retain the state-adapted fixed-principal frame and is audited separately. No action/norming inverse or Hamilton completeness follows solely from these blocks.
