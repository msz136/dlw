# Transverse jet obstruction for the actual independently perturbed sine data

2026-10-26. New necessary-condition theorem for the current sinusoidal benchmark. This is stronger than a constant-background perturbation calculation: the nonzero benchmark is included exactly. The conclusion excludes finite-order transverse Gevrey regularity at positive times. It does not assert nonexistence of a merely smooth solution or provide a numerical reference error bound.

## Problem and precise conclusion

Use the moving coordinate `X=x-4t`, `z=y+2 in [0,4]`, and the periodic x interval of length 192. Let

\[
 \alpha=\pi/4,\quad q=\pi/12,\quad \kappa=\pi/2=6q,
 \quad f(z)=\sin(\alpha z),\quad\phi(z)=\sin^2(\alpha z).
\]

The actual sine benchmark with amplitude `lambda=.03` is

\[
 u_0=\lambda f(z)\cos(qX),\qquad
 v_0=4-3\lambda f'(z)\cos(qX).
\]

Add `epsilon phi(z)cos(kappa X)` to exactly one of `u_0,v_0`, with the other unchanged and `epsilon=1e-6`. Keep the lower boundary `u(X,0,t)=0`. Put

\[
 A=u_z+v-4,\qquad B=v-u_z-4,\qquad
 u=\frac12\int_0^z(A-B)\,ds.
\]

Then the full nonlinear PDE is

\[
 A_t=-A_{XX}-(uA)_X,\qquad B_t=B_{XX}-(uB)_X. \tag{1}
\]

**Theorem.** Suppose a solution of (1) with the specified initial and lower-boundary data exists on `0<=t<=T` and is periodic in X. Assume that for every j its transverse boundary jets belong to `C^1([0,T];C^0_per(X))` and `C^0([0,T];C^2_per(X))`, with the mixed derivatives commuting so that (1) can be differentiated j times in z and evaluated at z=0. For either independent perturbation, at every `t in (0,T]` the pair `(A,B)` fails every finite-order Gevrey estimate in z at the lower boundary, uniformly in X. In particular, the physical pair `(u,v)` cannot be analytic in z there, or belong to any finite-order transverse Gevrey class.

Here a finite-order Gevrey estimate means constants `C,R<infinity`, finite `s>=1`, such that for every j,

\[
 \sup_X |\partial_z^j A(X,0,t)|
 +\sup_X |\partial_z^j B(X,0,t)|
 \le C R^j(j!)^s. \tag{2}
\]

If a sufficiently smooth solution exists, its boundary jets instead have a subsequence whose normalized coefficients grow at least like `exp(c j^2)` times an exponential in j. Smooth functions can have such jets, so this argument does not exclude the C-infinity class.

## Exact triangular jet equations

Write normalized boundary Taylor coefficients

\[
 a_j(X,t)=\frac{\partial_z^j A(X,0,t)}{j!},\qquad
 b_j(X,t)=\frac{\partial_z^j B(X,0,t)}{j!}.
\]

This notation requires only the derivatives, not convergence of their Taylor series. The coefficient of z^l in u is

\[
 u_l=\frac{a_{l-1}-b_{l-1}}{2l},\qquad l\ge1,
 \quad u_0=0.
\]

Differentiating (1) yields the exact finite triangular hierarchy

\[
 \dot a_j=-a_{j,XX}
       -\partial_X\sum_{l=1}^j
          \frac{a_{l-1}-b_{l-1}}{2l}a_{j-l},
\]
\[
 \dot b_j=b_{j,XX}
       -\partial_X\sum_{l=1}^j
          \frac{a_{l-1}-b_{l-1}}{2l}b_{j-l}. \tag{3}
\]

The initial base coefficients contain only the frequencies `+/-q`. A u-only perturbation first enters `(a_1,b_1)` with positive-frequency coefficients `(epsilon alpha^2,-epsilon alpha^2)` at `kappa`. A v-only perturbation first enters `(a_2,b_2)` with coefficients `(epsilon alpha^2/2,epsilon alpha^2/2)`. The later initial transverse coefficients have the same respective x frequencies and larger transverse degree.

## Why the nonzero baseline cannot cancel the selected coefficients

Assign coefficient `a_j` or `b_j` the weight `j+1`. Each product on the right of (3) preserves the sum of weights. The minimum initial weights and maximum absolute frequencies are:

| Initial contribution | Minimum weight | Absolute x frequency |
|---|---:|---:|
| Nonzero sine baseline | 1 | q |
| Independent u perturbation | 2 | 6q |
| Independent v perturbation | 3 | 6q |

For u input, at total weight `2n` the largest possible frequency is `6nq`; it requires exactly n perturbation factors, all at their minimum weight and positive frequency. Including any baseline factor or a higher-order initial jet lowers this maximum. For v input, the corresponding statement holds at total weight `3n` and the same frequency `6nq`.

This follows inductively in the finite hierarchy (3). For example, if m perturbation leaves occur at total weight `rn`, their frequency is at most `6m q + (rn-rm)q`; when `m<n`, this is strictly below `6nq` for r=2 or3. The maximum case uses no baseline factors. Initial higher-weight perturbation leaves also leave a strict deficit.

Thus the selected Fourier coefficients at `(j,frequency)=(2n-1,n kappa)` or `(3n-1,n kappa)` are exactly independent of the baseline amplitude lambda. They are not merely leading terms in a lambda expansion. Their positive recurrences below determine an actual boundary jet of every sufficiently differentiable solution.

The period 192 causes no extra modes: the initial data contain only multiples of q, and (3) preserves this frequency subgroup. For each fixed j the forcing has finitely many modes. The scalar Fourier equations with zero initial value outside those modes have identically zero solutions.

## Independent u input

Remove the phase and amplitude by defining the selected coefficients

\[
 [a_{2n-1}]_{n\kappa}=(-i\kappa)^{n-1}\epsilon^n C_n(t),
 \qquad
 [b_{2n-1}]_{n\kappa}=(-i\kappa)^{n-1}\epsilon^n D_n(t).
\]

The exact recurrence is

\[
 C_n'=n^2\kappa^2C_n+
 n\sum_{p=1}^{n-1}\frac{C_p-D_p}{4p}C_{n-p},
\]
\[
 D_n'=-n^2\kappa^2D_n+
 n\sum_{p=1}^{n-1}\frac{C_p-D_p}{4p}D_{n-p}. \tag{4}
\]

The initial values are `C_1(0)=alpha^2`, `D_1(0)=-alpha^2`, and `C_n(0)=D_n(0)=0` for `n>=2`. Consequently `C_n>=0`, `D_n<=0` by induction and variation of constants. Since

\[
 C_1-D_1=2\alpha^2\cosh(\kappa^2t)\ge2\alpha^2,
\]

the p=1 term alone gives `C_n'>=n^2 kappa^2 C_n+(n alpha^2/2)C_(n-1)`. On an interval `[0,s]` first drop the growth term and iterate integration; then retain only growth on `[s,t]`. This gives

\[
 C_n(t)\ge\alpha^2 n
       \left(\frac{\alpha^2s}{2}\right)^{n-1}
       e^{n^2\kappa^2(t-s)}.
\]

In particular,

\[
 |[a_{2n-1}]_{n\kappa}|
 \ge |\epsilon|^n\kappa^{n-1}\alpha^2 n
       \left(\frac{\alpha^2t}{4}\right)^{n-1}
       e^{n^2\kappa^2t/2}. \tag{5}
\]

The same modulus conclusion holds for negative nonzero epsilon by extracting its power.

## Independent v input

Now select index `j=3n-1` and remove the same phase and epsilon power. The recurrence has denominator `6p` in place of `4p`, and

\[
 C_1(0)=D_1(0)=\alpha^2/2.
\]

Variation of constants and the difference equation show `C_n>=D_n>=0`. Here

\[
 C_1-D_1=\alpha^2\sinh(\kappa^2t)
 \ge\alpha^2\kappa^2t.
\]

The p=1 term gives `C_n'>=n^2 kappa^2 C_n+(n alpha^2 kappa^2 t/6)C_(n-1)`. Integrating first on `[0,s]` yields

\[
 C_n(s)\ge\frac{\alpha^2}{2}n
   \left(\frac{\alpha^2\kappa^2s^2}{12}\right)^{n-1}.
\]

The second interval gives

\[
 |[a_{3n-1}]_{n\kappa}|
 \ge |\epsilon|^n\kappa^{n-1}\frac{\alpha^2}{2}n
   \left(\frac{\alpha^2\kappa^2t^2}{48}\right)^{n-1}
   e^{n^2\kappa^2t/2}. \tag{6}
\]

Both (5) and (6) are inequalities for actual jets, without assuming an amplitude-series solution.

## Contradiction with every finite Gevrey order

A normalized Fourier coefficient is bounded in magnitude by the supremum over one x period. Under (2), the selected normalized Taylor coefficient would satisfy

\[
 |[a_j]_{n\kappa}|\le C R^j(j!)^{s-1}.
\]

Its logarithm is `O(j log j)=O(n log n)` for every fixed finite s. In contrast, (5) and (6) have logarithm at least `n^2 kappa^2 t/2 + O(n)` at every fixed positive t. This is a contradiction. If the physical pair `(u,v)` satisfied finite-order Gevrey bounds, so would `A=u_z+v-4` after enlarging its constants; thus the physical-pair conclusion follows.

## Meaning for continuum certification

The sinusoidal initial functions are analytic in both variables, yet any sufficiently smooth solution of this lower-boundary IVP would immediately leave every finite transverse Gevrey class. A certificate based on analytic/Gevrey transverse Taylor tails therefore cannot be completed for these independently perturbed sine data by merely increasing resolution or arithmetic precision.

This theorem does not exclude a solution with unrestricted C-infinity transverse jets, does not establish ill-posedness in every weaker class, and does not assign a small approximation error. The Gaussian background has infinitely many x modes, so the unique-maximum-frequency argument used here does not apply to it. The soliton backgrounds require separate boundary analysis.

## Independent checks

The numerical-design agent independently reviewed the complete proof on 2026-10-26: weight isolation, cosine Fourier factors, recurrence denominators, two-interval lower bounds, and the Gevrey contradiction passed. At n=2, with `ell=kappa^2`, the recurrences give

\[
 C_2^{(u)}=\frac{\alpha^4}{8\ell}
 (3e^{4\ell t}-2e^{2\ell t}-1),\quad
 D_2^{(u)}=\frac{\alpha^4}{8\ell}
 (3e^{-4\ell t}-2e^{-2\ell t}-1),
\]

\[
 C_2^{(v)}=\frac{\alpha^4}{48\ell}(e^{2\ell t}-1)^2,
 \quad D_2^{(v)}=\frac{\alpha^4}{48\ell}(1-e^{-2\ell t})^2.
\]

All four symbolic recurrence residuals were checked to vanish. The theoretical growth occurs in increasingly high transverse jets; this theorem does not predict a large physical-field response on the current finite grid at T=.01.
