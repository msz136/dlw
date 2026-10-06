# Open-chain logarithmic generator and exact benchmark spectral moments

This note complements the periodic monodromy theorem. It deliberately distinguishes a formal generating identity from a theorem about finite physical total charges.

## 1. Exact logarithmic identities

Let D=∂x, Δ=E−1, g=hw/4, A=(U+g)/2 and B=(U−g)/2. The verified full Darboux structure implies

\[
(D-B_j)\psi_{j+1}=(D-A_j)\psi_j,
\qquad \psi_{j,t}=-(D^2+V_j)\psi_j,
\qquad \Delta V=2Dg.
\]

For a nonzero formal wave define p_j=D log ψ_j and s_j=log(ψ_{j+1}/ψ_j). Then

\[
\Delta p=Ds,
\qquad s=\log(p-A)-\log(Ep-B),
\]

\[
p_t+D(p_x+p^2+V)=0,
\qquad s_t+\Delta(p_x+p^2+V)=0.
\]

These identities follow by differentiation and the full heat equation; they do not assert equivalence of the naked transfer equation on the degenerate w=0 branch.

Write p=z+Σ_{n≥1}p_nz^{-n} and s=Σ_{n≥1}s_nz^{-n}. If C_n(a;p) denotes the z^{-n} coefficient of log(1−a/z+Σp_kz^{-k−1}), the spatial triangular recursion is

\[
s_n=C_n(A;p)-C_n(B;Ep),\qquad \Delta p_n=Ds_n.
\]

The right side of the first formula only uses p₁,…,p_{n−1}. The conservation flux for s_n is

\[
(s_n)_t+\Delta F_n=0,\qquad
F_n=Dp_n+2p_{n+1}+\sum_{k=1}^{n-1}p_kp_{n-k}.
\]

Separately, (p_n)_t+DF_n=0. The field V appears at order z⁰ and requires 2p₁+V to be x independent. One can absorb the compatible scalar gauge.

The first coefficients are

\[
s_1=-g,\quad s_2=Dg-Ug/2,
\]

\[
s_3=-Ds_2+gp_1-BDs_1-g(U^2/4+g^2/12),
\]

\[
s_4=-Ds_3+gp_2-BDs_2+p_1Ds_1+(Ds_1)^2/2
       +Ugp_1-B^2Ds_1-g(U^3+Ug^2)/8.
\]

## 2. Open-chain primitive and low-order identification

In a compatible open-chain normalization choose the integration constants so that

\[
R=\frac h2+h\Delta^{-1},\qquad
p_n=D\Delta^{-1}s_n,
\]

\[
p_1=-RDw/4+hDw/8,
\quad p_2=(R/4-h/8)D^2w-(R/8-h/16)D(Uw).
\]

Modulo x divergences, assuming the trace and skewness manipulations are valid,

\[
\sum_js_1=-\frac h4\sum_jw,
\quad \sum_js_2\equiv-\frac h8\sum_jUw,
\]

\[
\sum_js_3\equiv-\mathcal H_0(x)/8,
\quad \sum_js_4\equiv-3\mathcal Q_4(x)/32.
\]

Here the two densities include the h factor:

\[
\mathcal H_0(x)=h\sum_j[U^2w/2+\beta w^3/3+wDU+wRDw/2],
\]

\[
\mathcal Q_4(x)=h\sum_j[U^3w/3+2\beta Uw^3/3+2UwDU
               -4(DU)(Dw)/3+UwRDw].
\]

For the last identity put S=R/h−1/2, so S*=−S−1 and p₁=−SDg. Integrating s₄ by parts first gives

\[
\sum_js_4\equiv\sum_j[-gU^3/8-Ug^3/8-3UgDU/4
                 +(DU)(Dg)/2-3UgR(Dg)/(2h)],
\]

which is precisely −3Q₄(x)/32. This identification explains the finite-h cubic-w correction without taking a one-dimensional reduction.

On a periodic chain, however, Δp_n=Ds_n implies DΣs_n=0. Blindly setting every lattice integration constant to zero fails already at n=3 for a general field: it would force the Hamilton density to be x independent. The periodic monodromy construction fixes these common modes consistently. The open-chain formula is a useful generating relation, but it does not by itself define a canonical periodic physical hierarchy.

## 3. Requested Gram benchmarks

For positive regular Gram waves, the normalized transmission is

\[
\mathcal T(z)=\prod_i\frac{z-p_i}{z+q_i},\qquad
\log\mathcal T(z)=\sum_{n\ge1}C_nz^{-n},
\quad C_n=-\frac1n\sum_i[p_i^n-(-q_i)^n].
\]

These moments equal the single-site integral of the x-logarithmic density p_n, with the prescribed spectral boundary normalization. They are independent of j,t,h on the exact solution family. They are not automatically hΣ_j∫p_n, which diverges when the same nonzero C_n repeats at every site.

For one soliton put k=p+q, r=e^θ/(p+q+e^θ). The wave ratio is 1−kr/(z+q). Its coefficients satisfy

\[
p_n=-k^2r(1-r)(kr-q)^{n-1},\qquad
Dr=kr(1-r),\quad r_t=-(p-q)Dr.
\]

Consequently ∫p_n dx=[(-q)^n−p^n]/n. The complete rational heat identity, not just sampled values, is checked for 1a, 1b and the two-soliton wave in check_benchmarks.py. Its finite checks also verify n=1,…,7 flux identities and n=1,…,8 endpoint moments for the two one-soliton cases.

The first four moment values are

| Benchmark | C₁ | C₂ | C₃ | C₄ |
|---|---:|---:|---:|---:|
| 1a, (p,q)=(1,2) | −3 | 3/2 | −3 | 15/4 |
| 1b, (4,−3) | −1 | −7/2 | −37/3 | −175/4 |
| Two solitons, (6,−5),(4,−3) | −2 | −9 | −128/3 | −423/2 |

The Jacobian of C₁,…,C_{2m} with respect to the 2m spectral endpoints has entries −r_i^{n−1}, r_i∈{p_i,−q_i}. It is a Vandermonde and has full rank for distinct endpoints. This is independence on the spectral-parameter family only; it says neither that all infinitely many C_n are independent on a fixed m-soliton manifold nor that their physical Poisson brackets vanish.

## 4. Scope to settle after the formal calculation

All Laurent inverses above are formal; no analytic inverse of D−B is required. Actual waves need a compatible normalization and ψ≠0 locally. Inverse Δ or R needs a domain and a choice of common mode. Passing from generating identities to total conserved integrals needs summability and matching endpoint fluxes. These issues do not invalidate the formal recursion, but they decide which of its coefficients becomes a finite charge on a chosen physical phase space.

The requested three line-wave backgrounds are nonperiodic. The periodic theorem is not automatically a theorem on their relative Hilbert phase spaces. Their spectral moments are exact benchmarks; an extension of the new charges to a common relative perturbation space and proof of its involutive hierarchy remain separate tasks.

There is a concrete domain obstruction, beyond just the lack of a finite monodromy. The old graph space Y requires p∈H¹ and r∈Dom(RD), but does not require p∈Dom(RD). The new gradients include RD(Uw). At an actual line-wave background choose r=0 and p_j=δ_{j,j₀}f(x), with smooth compact f supported where w_{*,j₀}≠0. This is in old Y. The perturbation of Uw is δ_{j,j₀}w_{*,j₀}f, a nonzero compact function of x. Its joint Fourier transform has a nonzero lattice zero-frequency value for a set of ξ≠0. Since RD has multiplier hξ cot(θ/2)/2 ∼hξ/θ, its squared norm diverges in θ. Thus the straightforward new gradient is not defined in old X for all old Y perturbations. This does not rule out a different relative functional, weaker bracket, or a strengthened invariant domain.
