# Why the positive all-mode certificate cannot close

Date: 2026-10-24. This is a new exact obstruction to the particular sufficient certificate (R2) in `CERTIFICATE_ROUTE_REVIEW.md`. It is **not** a nonexistence theorem for either requested DLW solution.

## Result

The nonnegative convolution majorant (R2) cannot have a summable supersolution on any positive time interval if it contains a nonzero error or forcing at any nonzero x Fourier frequency. Arbitrarily small forcing has the same obstruction. Thus further optimization of Gaussian weights or smaller residual constants cannot complete that certificate.

The issue is stronger than failure of a chosen Banach-algebra estimate: the individual mode envelopes forced by (R2) grow without bound along a harmonic sequence.

## Proof

Write `xi_n=2*pi*n/192` and let `J>0` be the norm bound for the y primitive. The quadratic term already present in (R2) gives

\[
 \alpha_n(t)\ge \frac{J|\xi_n|}{2}
 \int_0^t e^{\xi_n^2(t-s)}(\alpha*\alpha)_n(s)\,ds.
 \tag{1}
\]

Every other contribution in that test is nonnegative and can be discarded in a lower bound. Suppose that, for one integer `m!=0`,

\[
 \alpha_m(s)\ge\delta>0,
 \qquad s_0\le s\le t_0<T.
 \tag{2}
\]

Set `kappa=|xi_m|`, `c=J*kappa/2`, and `tau=t0-s0>0`. Restricting the convolution in (1) to the single ordered pair `(m,(j-1)m)`, and using `exp(x)>=1`, proves inductively that

\[
 \alpha_{jm}(t)\ge
 j\delta[c\delta(t-s_0)]^{j-1},
 \qquad s_0\le t\le t_0,\quad j\ge1.
 \tag{3}
\]

For the induction step, integrate

\[
 cj\delta\,(j-1)\delta
 [c\delta(s-s_0)]^{j-2}
\]

from `s0` to `t`. For `j=2` the chosen convolution pair occurs once; the bound uses it only once and is unchanged. For larger `j` any additional ordered pairs only increase the right side.

Now evaluate (1) at `T`, restrict its time integral to `[s0,t0]`, and keep the antiheat factor. For every `j>=2`,

\[
 \boxed{
 \alpha_{jm}(T)\ge
 j\delta(c\delta\tau)^{j-1}
 \exp\!\left(j^2\kappa^2(T-t_0)\right).
 }
 \tag{4}
\]

No semigroup property of the envelope itself has been assumed here. Inequality (4) follows from its original Duhamel inequality, which is important because a supersolution of (R2) need not separately satisfy a two-time evolution inequality.

The logarithm of the right side of (4) equals

\[
 j^2\kappa^2(T-t_0)+(j-1)\log(c\delta\tau)
 +\log(j\delta).
\]

Its quadratic term is strictly positive, so this lower bound tends to infinity. In particular, the mode sequence cannot tend to zero and cannot be summable in any norm dominating the physical Fourier coefficients. This proves the assertion.

## Why any nonzero certificate uncertainty supplies the seed

The required envelopes are continuous. Therefore any positive `alpha_m` at a time strictly before `T` supplies an interval of the form (2). A positive initial bound `e_a,m` or a nonzero continuous residual bound `rho_a,m` forces such a seed directly.

The `beta` channel does not avoid this obstruction. The linear coupling in (R2) contains

\[
 \alpha_m(t)\ge
 2J|\xi_m|\int_0^t
 e^{\xi_m^2(t-s)}\beta_m(s)\,ds.
\]

Thus positive nonzero-frequency beta uncertainty also generates an alpha seed. Positive `e_b,m` or `rho_b,m` therefore has the same consequence.

This theorem does not exclude the identically zero certificate around an already exact solution: all initial errors and residuals zero allow `alpha=beta=0`. Nor does the quadratic argument alone treat an uncertainty restricted to the zero x mode. These exceptions do not provide a certificate for the current computed nonlinear reference trajectories.

For the periodic Gaussian, any finitely supported reference initial Fourier series has explicit nonzero high-mode initial errors. For the sinusoidal reference, finite initial support alone is no obstruction, but any positive nonzero-frequency residual or arithmetic enclosure in the reference trajectory triggers the theorem. Finite polynomial trajectory reconstructions with the recorded nonzero residual bounds are therefore not certifiable through (R2).

## Meaning for the requested error guarantee

This result closes off one proposed proof route. It does not prove that the physical solution has the positive cascade in (4): the actual Fourier coefficients are signed/complex, the two physical components interact, and (R2) deliberately discards cancellations. One must not transfer a lower bound for an absolute majorant to a lower bound for the true solution.

Consequently no numerical `eta_u` or `eta_v` follows from this review. A successful theorem must exploit additional DLW structure or a specifically characterized admissible solution class in a way that avoids the positive antiheat/quadratic cascade. Repeated finite-mode refinements, reducing residual size, and substituting another positive Fourier weight cannot repair (R2).

This is an exact algebraic/analytic proof about the proposed verification inequality. It requires no new numerical experiment and makes no claim that the given Gaussian or sinusoidal nonlinear initial-value problem has been proved unsolvable.
