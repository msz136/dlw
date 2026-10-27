# Conditional Hölder control does not imply analytic parameter regularity

2026-10-26. Exact counterexample to a proposed general bridge. This does not prove nonexistence for the DLW initial-value problem. It shows that analytic initial-parameter dependence, a smoothing analytic matching map, injectivity of its derivative, and time-padding-type conditional Hölder stability are insufficient by themselves to deduce analytic or Gevrey dependence of the observed interior solution on that parameter.

## 1. Analytic matching map with Gaussian output smoothing

Use the real Banach space E=ell-infinity(N), with its usual supremum norm, and let S>0. Put

    lambda_n=exp(-S n²),
    F_n(x)=lambda_n[lambda_n x_n+x_n³].

The map F:E->E is an entire polynomial Banach-space map. In the stronger Gaussian-output space

    Y_S={y: ||y||_(Y_S)=sup_n exp(S n²)|y_n|<infinity},

it is still an entire map E->Y_S: multiplication of F_n by exp(Sn²) leaves lambda_n x_n+x_n³. All derivatives of F therefore have this Gaussian output smoothing on every bounded E ball. Derivatives above order three are zero.

Its derivative at every real x is

    [DF(x)h]_n=lambda_n[lambda_n+3x_n²]h_n.

Every diagonal multiplier is strictly positive, hence DF(x) is injective. As an operator E->E it is compact, since its diagonal coefficients tend to zero for each bounded x. The map F itself maps bounded sets into relatively compact sets of E for the same uniform-tail reason.

F is injective on real E: each scalar map lambda_n x+x³ is strictly increasing.

## 2. An interior observation with a conditional Hölder estimate

For any 0<T<S define the heat-smoothed observation

    [K_T x]_n=exp[-(S-T)n²]x_n.

For real p,q,

    p²+pq+q² >= (p-q)²/4,

so monotonicity gives

    |F_n(p)-F_n(q)| >= lambda_n |p-q|³/4.

Consequently

    |[K_T(x-z)]_n|
      <= 4^(1/3) exp[(T-2S/3)n²] ||F(x)-F(z)||_E^(1/3).

If 0<T<=2S/3, this proves the global conditional stability estimate

    ||K_T(x-z)||_E <= 4^(1/3)||F(x)-F(z)||_E^(1/3).       (H)

In particular S=.02 and T=.01 satisfy the condition. The observation is strictly inside a padded interval in exactly the simple heat-smoothing sense represented by K_T.

## 3. Entire input data and a uniformly bounded real solution family

Fix alpha>0 and prescribe the parameter-dependent matching data

    y_n(mu)=exp(-S n²-alpha n)mu, mu real.

This curve is entire even as a Y_S-valued function. For each real mu, solve the scalar equations

    lambda_n x_n(mu)+x_n(mu)³=exp(-alpha n)mu.             (C)

Each equation has a unique real root, and

    |x_n(mu)|³ <= exp(-alpha n)|mu|,

so x(mu) belongs to E and is uniformly bounded for mu in any fixed bounded real interval. The family is Hölder continuous in E by the unsmoothed cubic monotonicity estimate. It satisfies F(x(mu))=y(mu) exactly.

Thus the example has exact matching, analytic data, a uniformly bounded real lift, an analytic smoothing forward map, an injective derivative, and the conditional interior estimate H.

## 4. The observed parameter curve is not differentiable

At mu=0, x_n(0)=0. Ordinary scalar implicit differentiation of C gives

    x_n'(0)=exp(S n²-alpha n).

If the E-valued observed curve mu -> K_T x(mu) had a derivative at zero, each continuous coordinate functional would recover the corresponding scalar derivative. Its derivative coordinates would therefore be

    [d_mu K_T x(mu)|_(mu=0)]_n=exp(T n²-alpha n).

For every T>0 this sequence is unbounded. It cannot belong to E, a contradiction. Hence the interior observed curve is not even once differentiable, and in particular is not analytic or finite-order Gevrey in mu.

There is no conflict with H: Hölder control does not give a bounded derivative. Injectivity of DF does not provide a bounded inverse; all its singular scales can still tend to zero.

## 5. Consequence for the proposed transverse-dilation argument

The generic inference

    analytic initial data in a real parameter
    + uniformly bounded exact real solutions on a longer interval
    + analytic/smoothing matching map with injective derivative
    + conditional Hölder stability on a shorter interval
    => analytic or Gevrey parameter regularity on that shorter interval

is false. The example satisfies all displayed abstract properties at S=.02,T=.01 and violates the conclusion.

A dilation trick specific to DLW could still work if additional structure excludes this example, for instance a complex-parameter bounded lift, a quantitative holomorphic inverse on the actual range, or more precise estimates connecting the linearized matching scales to the interior observation. None of those follows solely from the real conditional estimate.

This counterexample is cubic, whereas DLW is quadratic. It therefore refutes the proposed abstract bridge, not every possible DLW-specific quadratic argument. A real bounded parameter family cannot be replaced by a complex bounded family without proof: in this example the scalar cubic inverse has complex branch points approaching mu=0 as n grows, so no common holomorphic parameter disk exists.

`analytic_parameter_holder_check.py/json` verifies the scalar identities, derivatives and S=.02,T=.01 exponent inequality. The infinite-dimensional non-differentiability proof is the coordinate-functional argument above.
