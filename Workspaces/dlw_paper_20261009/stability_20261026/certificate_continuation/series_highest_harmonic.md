# Highest-harmonic obstruction to a convergent amplitude expansion

2026-10-26. This note derives a positive, all-order recurrence before evaluating any high-order coefficients. It treats the continuous DLW equation around the constant background. Its leading-transverse-coefficient version also supplies the scalar recurrence independently used in `audit_sine_jet_obstruction.md` for the actual sine benchmark.

The result is an obstruction, not a continuous reference solution. A divergent amplitude expansion does not by itself imply nonexistence for a fixed nonzero datum.

## Continuous equation and initial data

In the moving coordinate `X=x-4t`, set

\[
 A=u_z+v-4,\quad B=v-u_z-4,\quad
 u=\frac12J(A-B),\qquad Jf(z)=\int_0^zf(s)\,ds.
\]

The prescribed lower value is `u(X,0,t)=0`. The equation becomes

\[
 A_t=-A_{XX}-(uA)_X,\qquad
 B_t=B_{XX}-(uB)_X. \tag{1}
\]

Take `phi(z)=sin²(pi*z/L)`, `kappa>0`. The two independent initial perturbations of `(u,v)=(0,4)` are

\[
 (u_0,v_0-4)=(\epsilon\phi\cos\kappa X,0)
 \quad\hbox{or}\quad
 (0,\epsilon\phi\cos\kappa X).
\]

Thus the positive-frequency initial coefficients of `(A,B)` are respectively `(epsilon phi'/2,-epsilon phi'/2)` and `(epsilon phi/2,epsilon phi/2)`.

## Exact triangular highest-harmonic recurrence

Consider the formal amplitude expansion `A=sum epsilon^n A^[n]`, and similarly for B and u. At amplitude order n, no frequency larger than `n*kappa` can occur. A quadratic contribution to frequency `+n*kappa` must pair the positive highest frequencies at its two constituent orders; lower or negative modes cannot enter this recurrence.

Write these highest-frequency coefficients as

\[
 [A^{[n]}]_{n\kappa}=(-i\kappa)^{n-1}\alpha_n,
 \quad [B^{[n]}]_{n\kappa}=(-i\kappa)^{n-1}\beta_n,
 \quad U_n=\frac12J(\alpha_n-\beta_n).
\]

Putting `ell=kappa²`, equation (1) gives exactly

\[
 \partial_t\alpha_n=n^2\ell\alpha_n
      +n\sum_{p=1}^{n-1}U_p\alpha_{n-p},\qquad
 \partial_t\beta_n=-n^2\ell\beta_n
      +n\sum_{p=1}^{n-1}U_p\beta_{n-p}. \tag{2}
\]

The factors `(-i*kappa)^(n-1)` remove the derivative phases from every product. Initial coefficients vanish for `n>=2`.

### Independent u input

On `0<=z<=L/2`, phi and phi' are nonnegative. At first order,

\[
 \alpha_1=\frac{\phi'}2e^{\ell t},\quad
 \beta_1=-\frac{\phi'}2e^{-\ell t},\quad
 U_1=\frac\phi2\cosh(\ell t)\ge\frac\phi2.
\]

Induction and variation of constants in (2) give `alpha_n>=0`, `beta_n<=0`, `U_n>=0` at every order. In particular,

\[
 \partial_t\alpha_n\ge n^2\ell\alpha_n
                         +n\frac\phi2\alpha_{n-1}.
\]

For any `0<s<=t`, ignore growth on `[0,s]` and then keep only growth on `[s,t]`. Repeated integration yields

\[
 \alpha_n(z,t)\ge \frac{\phi'(z)}2\,n
       \left(\frac{\phi(z)s}{2}\right)^{n-1}
       e^{n^2\ell(t-s)}. \tag{3}
\]

At `s=t/2`, this grows like `exp(n² ell t/2+O(n))`. At any fixed interior point where both phi and phi' are positive, the factor `epsilon^n*kappa^(n-1)` cannot offset this growth. The formal amplitude terms do not tend to zero in any norm controlling that Fourier coefficient.

This is also an obstruction for the physical u series, not only for a transverse derivative. Since `U_n>=J(alpha_n)/2`, integrating (3) gives

\[
 U_n(z,t)\ge
 \frac{\phi(z)^n s^{n-1}}{2^{n+1}}
 e^{n^2\ell(t-s)}. \tag{4}
\]

Hence its physical highest-harmonic terms likewise fail to tend to zero.

### Independent v input

Here phi is nonnegative on the whole interval. First order is

\[
 \alpha_1=\frac\phi2e^{\ell t},\quad
 \beta_1=\frac\phi2e^{-\ell t},\quad
 U_1=\frac{J\phi}{2}\sinh(\ell t)
       \ge\frac{\ell J\phi}{2}t.
\]

Inductively, `alpha_n>=beta_n>=0`, and `U_n>=0`: the difference of the two variation-of-constants formulas is nonnegative, since both the growth kernel and the source for alpha dominate those for beta. Therefore

\[
 \partial_t\alpha_n\ge n^2\ell\alpha_n
               +n\frac{\ell J\phi}{2}t\alpha_{n-1}.
\]

The same two-interval argument gives

\[
 \alpha_n(z,t)\ge\frac{\phi(z)}2\,n
     \left(\frac{\ell J\phi(z)s^2}{4}\right)^{n-1}
     e^{n^2\ell(t-s)}. \tag{5}
\]

For `s=t/2` this again has a positive quadratic exponent in n. The physical v coefficient is `(alpha_n+beta_n)/2>=alpha_n/2`, so the physical v amplitude expansion also has zero radius at every positive time.

## Optimized bound and arbitrary-precision evaluation

In a bound of the form `a0*n*(c*s^p)^(n-1)*exp(n² ell (t-s))`, the optimal admissible split is

\[
 s=\min\left(t,\frac{p(n-1)}{n^2\ell}\right),\qquad
 p=1\ (u\hbox{ input}),\quad p=2\ (v\hbox{ input}).
\]

Its logarithm is `n² ell t - O(n log n)`. This gives the all-order conclusion directly; it is not inferred from a fitted sequence of low orders.

`series_highest_harmonic.py` evaluates logarithms of these analytic bounds with 600-bit Arb arithmetic. It also evaluates an exact scalar comparison chain with 180 decimal digits. For the u chain `r_n'=n² ell r_n+n c r_(n-1)`, `r_1(0)=a0`, the exact expression is

\[
 r_n(t)=a_0n!\left(\frac c\ell\right)^{n-1}
 \sum_{j=1}^n
 \frac{2(-1)^{n-j}j^2e^{j^2\ell t}}{(n-j)!(n+j)!}. \tag{6}
\]

The signed sum evaluates the positive convolution chain. It is used as an independent numerical check, not as the proof of the lower bound.

At `L=4`, `z=L/4`, `kappa=pi/2`, `epsilon=1e-6`, `t=.01`, the logarithms below include the full factor `epsilon^n*kappa^(n-1)` and refer to the selected A coefficient:

| n | u-input lower bound, log10 | v-input lower bound, log10 |
|---:|---:|---:|
| 64 | -530.5740 | -682.3211 |
| 256 | -1760.5435 | -2521.3646 |
| 512 | -2275.2827 | -3953.1031 |
| 1024 | 754.1290 | -2912.1180 |
| 2048 | 23358.5713 | 15406.9158 |
| 4096 | 135368.2459 | 118228.9630 |

The optimized lower bound first exceeds one at tested orders n=953 and n=1310, respectively. These numbers describe formal coefficients, not physical field amplitudes of an actual fixed-epsilon solution. They show why a few extremely small, accurate low-order terms cannot certify the tail.

## Leading transverse coefficients

Let `alpha=pi/L`, so `phi=alpha²z²+O(z⁴)`. In (2), the highest harmonic at the lowest transverse degree has

\[
 \alpha_n=C_n z^{rn-1}+\cdots,\qquad
 \beta_n=D_n z^{rn-1}+\cdots,
\]

where r=2 for u input and r=3 for v input. The corresponding u coefficient is `(C_n-D_n)z^(rn)/(2rn)`. Thus

\[
 C_n'=n^2\ell C_n+
 n\sum_{p=1}^{n-1}\frac{C_p-D_p}{2rp}C_{n-p},
 \quad
 D_n'=-n^2\ell D_n+
 n\sum_{p=1}^{n-1}\frac{C_p-D_p}{2rp}D_{n-p}. \tag{7}
\]

For u input, `(C_1(0),D_1(0))=(alpha²,-alpha²)`. For v input they are `(alpha²/2,alpha²/2)`. The sign arguments above apply, and

\[
 C_n(t)\ge\alpha^2n(\alpha^2s/2)^{n-1}e^{n^2\ell(t-s)}
 \quad (u\hbox{ input}),
\]

\[
 C_n(t)\ge\frac{\alpha^2}{2}n
 (\alpha^2\ell s^2/12)^{n-1}e^{n^2\ell(t-s)}
 \quad (v\hbox{ input}). \tag{8}
\]

These are normalized Taylor coefficients. To recover a derivative jet, multiply by `(rn-1)!` as well as `epsilon^n*(-i*kappa)^(n-1)`. SymPy verifies the four exact second-order recurrence residuals are zero; the script records the check.

For the actual sinusoidal background, `audit_sine_jet_obstruction.md` proves that a weight/frequency constraint isolates exactly (7) in actual boundary jets: the background cannot contribute to, or cancel, the selected highest modes. That separate argument converts the coefficient growth into an obstruction to every finite transverse Gevrey class for the actual perturbed sine datum. The amplitude-series result alone would not justify that stronger conclusion.

## What is established

1. The constant-background independent u and v amplitude expansions have zero radius at every positive time, including in the corresponding physical-field norms controlling Fourier coefficients.
2. The high-order lower bounds follow from positive recurrences and hold for all n. Interval arithmetic evaluates their numerical size; no spatial mesh or floating-point instability enters the argument.
3. The leading-transverse recurrence is exact and independently checked. Its application to the actual sine background needs—and has—the separate highest-frequency isolation argument in the audit note.
4. No conclusion here supplies a continuous reference error enclosure or rules out every possible C-infinity solution for a fixed epsilon.
