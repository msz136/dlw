# A quadratic smoothing map with a continuous bounded real lift beyond every finite Gevrey class

2026-10-26. Exact abstract counterexample. It strengthens the earlier cubic example by using a quadratic analytic map, a globally injective derivative, and a terminal lift continuous in the Banach norm. It blocks the proposed generic parameter-regularity inference; it does not establish a DLW nonexistence theorem.

## 1. Map, data and exact bounded lift

Let E=ell-infinity(N_0). Fix S>T>0 and beta>0. Define

    F_0(x)=x_0,
    F_n(x)=exp(-S n²)[exp(-beta n)x_n
                 -2 exp(-2beta)x_(n-1)²+exp(-2beta n)], n>=1.

This is an entire quadratic Banach-space map. It is entire into the Gaussian-output space Y_S, with norm sup_n exp(Sn²)|y_n|, because the bracket's coefficients are uniformly bounded. All derivatives have this Gaussian output smoothing; derivatives above order two vanish. On bounded E sets, F has uniformly vanishing tails and therefore relatively compact image in E.

The derivative is triangular:

    [DF(x)h]_0=h_0,
    [DF(x)h]_n=exp(-Sn²)[exp(-beta n)h_n
                         -4exp(-2beta)x_(n-1)h_(n-1)].

Its kernel is zero at every real or complex x: first h_0=0, then h_n=0 recursively. The same recursion shows that F itself is globally injective on E.

Take the entire input curve y(mu)=(mu,0,0,...). Its unique coordinatewise matching solution is

    x_n(mu)=exp(-beta n) T_(2^n)(mu),

where T_N is the Chebyshev polynomial. The doubling identity T_(2N)=2T_N²-1 verifies F(x(mu))=y(mu) exactly.

For real |mu|<=1, |x_n(mu)|<=exp(-beta n), so the lift is uniformly bounded by one. It is continuous in E on [-1,1]: the coordinate polynomials are continuous, and the tails are uniformly bounded by exp(-beta n). Thus the usual objection that a bounded but discontinuous terminal family was used does not apply.

## 2. Explicit conditional Hölder estimate after interior heat smoothing

Let c=S-T and define [K_T x]_n=exp(-c n²)x_n. For x,z in the E ball of radius R>0, put r=||F(x)-F(z)||, d_n=x_n-z_n and C=max(1,4R). Then

    |d_0|<=r,
    |d_n|<=r exp(Sn²+beta n)+C exp(beta n)|d_(n-1)|.

Iteration gives the valid elementary bound

    |d_n|<=r(n+1) C^n exp[(S+beta/2)n²+(3beta/2)n].

Also |d_n|<=2R. Interpolating these two bounds, for any

    0<theta<(S-T)/(S+beta/2),

set a=c-theta(S+beta/2)>0 and b=theta[1+log C+3beta/2]. Using n+1<=exp(n), one obtains

    ||K_T(x-z)||
      <= (2R)^(1-theta) exp[b²/(4a)] r^theta.             (QH)

This is a uniform conditional Hölder estimate on the entire radius-R ball, not merely along the matching curve. The concrete values S=.02, T=.01, beta=.001, R=1, theta=1/4 satisfy its strict inequality.

## 3. The interior parameter curve is smooth but not finite-order Gevrey

Let q(mu)=K_T x(mu). Each coordinate is

    q_n(mu)=exp(-c n²-beta n) T_(2^n)(mu).

Markov's polynomial derivative bound ||T_N^(m)||_[-1,1]<=N^(2m) shows that, for every fixed m, all derivative tails vanish uniformly:

    exp(-c n²-beta n) 2^(2mn) ->0 as n->infinity.

Thus q is an E-valued C-infinity function on [-1,1], obtained as the C^m-uniform limit of its finite coordinate truncations.

For even m=2r, N=2^n>=2m and n>=2, the Chebyshev equation gives exactly

    |T_N^(m)(0)|= product_(j=0)^(r-1)[N²-(2j)²]
                 >=(sqrt(3)/2)^m N^m.

Therefore

    log ||q^(m)(0)||
      >= -c n²+(m log2-beta)n+m log(sqrt(3)/2).

Choose n to be an integer nearest (m log2-beta)/(2c). For all sufficiently large even m it meets the preceding N condition, and

    log ||q^(m)(0)||
      >= (log2)² m²/(4c)-O(m).

The logarithm of a finite-order Gevrey bound C A^m(m!)^s is only O(m log m). Consequently q belongs to no finite-order Gevrey class near mu=0, despite all the properties in Sections 1–2.

This is compatible with QH. A conditional Hölder estimate on finite differences does not control arbitrarily high parameter derivatives.

## 4. Why real bounded lifts cannot be complexified without proof

For any complex mu outside [-1,1], one branch of w=mu+sqrt(mu²-1) has |w|>1 and

    T_(2^n)(mu)=(w^(2^n)+w^(-2^n))/2.

The exponential-in-n prefactor exp(-beta n) cannot suppress this double-exponential growth. Hence the unique coordinatewise lift does not belong to E there. In particular, the bounded real matching curve has no common complex parameter neighborhood containing zero.

The complex forward map is entire and its derivative is injective everywhere, but that supplies neither a locally bounded inverse nor a complex lift on the required range.

## 5. Meaning for the DLW dilation proposal

The proposed abstract bridge remains false even if the matching map is quadratic, compact, Gaussian-output smoothing, and globally derivative-injective, the real parameter lift is continuous and uniformly bounded, and an interior conditional Hölder estimate holds.

A DLW-specific argument must use additional properties, such as exact Fourier-convolution structure, a separately established complex lift, or a quantitative range theorem. This example's quadratic recurrence couples adjacent coordinate labels while doubling the parameter degree; it is not claimed to obey the DLW Fourier convolution law or its time-semigroup structure.

`quadratic_parameter_bridge_check.py/json` checks the exact matching recurrence, derivative injectivity's diagonal, conditional-estimate exponent, Chebyshev derivative product at finite orders and the concrete padded-time parameters. The infinite-dimensional proof is given above.
