# Audit of the proposed physical maximum-norm extension

Completion update, 2026-10-26: the separate
`GAUSSIAN_COMPLEX_GROWTH_LEMMA.md` has now been independently audited.
Its shifted-lattice estimates, constants 648 and 162pi, tail exponent
Y²/288, and phase-test lower bound are valid. The completed combined
proof is `GAUSSIAN_LINF_HOLDER_OBSTRUCTION.md`, with passing exact
checks in `gaussian_linf_holder_check.py/json`. The earlier conditional
wording below records the reduction before that lemma was supplied;
the complex-growth step is no longer an outstanding gap.

2026-10-26. This note checks the weak-limit, distributional-transform,
and Fourier steps of a proposed extension of the Gaussian obstruction.
It deliberately leaves the final complex-Gaussian growth lemma to the
separate proof being developed by the parent task. The conclusion below
is conditional on that lemma; this note alone is not a completed
physical maximum-norm impossibility theorem.

## Hypothetical maximum-norm response

Let the real classical exact solutions have the specified independent
initial perturbations, period 192, fixed lower trace u(X,0,t)=0, and
exist on one common interval [0,T], T>0. Suppose epsilon_n ->0 and

    ||u^n-u^b||_infinity+||v^n-v^b||_infinity <= C |epsilon_n|

on the whole physical cylinder. Write w_n=(u^n-u^b)/epsilon_n and
q_n=(v^n-v^b)/epsilon_n. These functions are uniformly bounded, so a
subsequence converges weak-star in spacetime L-infinity to w,q.

In the moving coordinate X=x-4t, integration of the exact first equation
using the lower trace gives the conservative equations

    u_t=-partial_XX integral_0^z v(X,r,t)dr-partial_X(u²/2),
    v_t=-u_XXz-partial_X(uv-4u).

After subtraction and normalization their nonlinear remainders are
epsilon_n w_n²/2 and epsilon_n w_n q_n. Both tend uniformly to zero.
The weak limits therefore satisfy

    w_t=-partial_XX integral_0^z q(X,r,t)dr-partial_X(u^b w),
    q_t=-w_XXz-partial_X(u^b q+(v^b-4)w)

as distributions. The initial boundary terms in these weak formulations
are the exact prescribed initial variations, so they survive passage to
the limit. In particular w,q have the required initial traces in the
distributional sense. Taking a z derivative of the first equation yields
the complete linearized physical PDE. No spatial derivatives of w_n or
q_n have been assumed bounded.

## An exact residual identity makes the transform legitimate

For arbitrary smooth u,v set

    E_u=u_zt+v_XX+(u²/2)_Xz,
    E_v=v_t+u_XXz+(uv-4u)_X,
    P1=(v-4+u_z)/4,
    Q1=-u/2-(log|P1|)_X,
    R=(v-4+3u_z)/4+(log|P1|)_Xz.

Where P1 is nonzero, the following identity holds:

    R_t+R_XX-2(Q1 R)_X
      =(E_v+3E_u)/4+partial_Xz[(E_v+E_u)/(4P1)].       (D1)

I checked (D1) independently by exact SymPy expansion and cancellation.
It also follows from the two Laplace residual identities in
`GAUSSIAN_LINEARIZED_AUDIT.md`.

On a compact z patch inside (0,2) surrounding z=1, the certified base has
P1^b=s_z F D/psi² nonzero. Linearizing (D1) at this base, where R=E_u=E_v=0,
is an identity between linear differential operators with smooth
coefficients. Such an identity applies to distributional w,q. Hence

    rho=(q+3w_z)/4+partial_Xz[(q+w_z)/(4P1^b)]

obeys rho_t=-rho_XX+2(Q1^b rho)_X and has the computed initial trace.
This construction never divides by the perturbed P1^n. Possible zeros
of those perturbed invariants do not invalidate this linearized step.

## Gauge and lifting with distributional z dependence

Use the fixed base gauge Phi=psi/F and mu(z)=s(z)C. Multiplication by
the smooth nonzero Phi is legitimate on distributions, and r=rho/Phi
satisfies r_t=-r_XX-2W_X r, W=F_X/F. It has Bloch multiplier
exp(mu(z)L), with mu bounded away from zero on the compact z patch.

The inverse of T=partial_X-W in this Bloch sector can be written by
integrating (h/F)_X=r/F over one period and determining the integration
constant with the denominator exp(mu(z)L)-1. All its z coefficients
are smooth, and this denominator is bounded away from zero. Thus this
inverse is a continuous parameter-dependent operator on distributions
in X,z,t. Its use does not require pointwise values in z.

The intertwining identity gives T(h_t+h_XX)=0. Its kernel consists of
F(X,t)c(z,t). The Bloch condition then requires
(exp(mu(z)L)-1)c=0, so c=0 as a distribution. Therefore h_t=-h_XX.
The initial h0 is the unique Bloch lift of the already determined
initial defect.

## Gaussian initial Fourier tails without a time-slice assumption

Put h=exp(mu(z)X)p so p is periodic. Its Fourier coefficients are
distributions in z,t satisfying

    partial_t p_n=lambda_n(z)p_n,
    lambda_n=(nd)²-2i mu(z)nd-mu(z)².

Multiplication by exp(-lambda_n t) shows that
exp(-lambda_n t)p_n is constant in t, equal to p_n(0). Choose a smooth
chi(t) of integral one supported in [tau1,tau2] inside (0,T), tau1>0.
For a z test function g,

    <p_n(0),g>=<p_n(z,t),chi(t) exp(-lambda_n(z)t)g(z)>.

The spacetime distribution p has finite order on every fixed compact
patch. Its Fourier coefficients therefore have polynomial growth in n
in one fixed distribution norm. Derivatives of exp(-lambda_n t)
cost only polynomial factors in n: t derivatives contribute O(n²),
z derivatives O(n), while its modulus is bounded by a constant times
exp(-tau1(nd)²). Consequently, for some fixed m,N,C,

    |<p_n(0),g>| <= C(1+|n|)^N exp(-tau1(nd)²)||g||_(C^m).

The initial Fourier series thus defines an entire function of complex
X valued in distributions in z, with a finite-order bound

    |<h0(X),g>|+|<partial_X h0(X),g>|
         <= C exp(C(1+|X|²)) ||g||_(C^M)

on a fixed compact z patch. A larger finite M can absorb the smooth
Bloch multiplication and its z derivatives. This argument avoids any
unproved existence of positive-time distributional slices.

## What the remaining complex lemma must prove

The explicit initial relation is still

    F0 h0'-F0' h0=exp(s(z)J0(X)) E(z,X),
    E=a(z)F0² Ck-b(z)(F0 Ck'-Ck F0').

On a sufficiently small compact z patch about 1, s and a are strictly
positive in both directions, and b/a is bounded. It suffices to prove,
along some complex sequence X_Y with |X_Y|=O(Y),

    Re J0(X_Y) >= c exp(Y²/36)/Y,
    |J0(X_Y)| <= C exp(Y²/36)/Y,
    |F0(X_Y)| >= c exp(Y²/36),
    |F0'(X_Y)/F0(X_Y)| <= CY,
    |Ck'(X_Y)/Ck(X_Y)| <= C,

with ordinary finite-order upper and lower bounds on
A_Y=F0(X_Y)² Ck(X_Y). The proposed X_Y=9pi/Y+iY has the appropriate
phase, but these estimates are not certified in this note.

If those estimates hold, B_Y/A_Y=O(Y exp(-Y²/36)), where
B_Y=F0 Ck'-Ck F0'. Choose a nonnegative smooth cutoff theta in the patch
and the Y-dependent test function

    g_Y(z)=theta(z) exp(-i s(z) Im J0(X_Y)).

After removing the constant phase of A_Y, the real part of the paired
right side is at least
c |A_Y| exp(s_min Re J0(X_Y)) for large Y. Its test-function norm costs
only ||g_Y||_(C^M) <= C(1+|J0(X_Y)|)^M, whose logarithm is O(Y²).
This contradicts the distribution-valued order-two bound on the left
side. Variable-z phase cancellation therefore does not create an
obstruction once the stated complex estimates are proved.

The weak-limit and distributional steps above are verified reductions.
A completed theorem excluding the physical maximum-norm O(epsilon)
response requires the remaining complex-Gaussian estimates and their
incorporation into one proof. Even that theorem would concern uniform
arbitrarily small amplitudes, and would not rule out a solution or
assign a reference error at the isolated amplitude epsilon=1e-6.

## Further conditional extension: Holder exponents above one half

The same reduction supports a stronger conditional statement if exact
solutions exist for every sufficiently small positive epsilon on one
common interval, with

    ||u^epsilon-u^b||_infinity+||v^epsilon-v^b||_infinity
        <= C epsilon^alpha,    1/2<alpha<=1.

Normalize by epsilon, not by epsilon^alpha. The normalized fields then
have size O(epsilon^(alpha-1)), and their linearized physical residuals
are exactly

    E_u^lin=-epsilon partial_Xz(w_epsilon²/2),
    E_v^lin=-epsilon partial_X(w_epsilon q_epsilon).

Thus their size in one fixed spatial-distribution norm, uniformly in
time, is O(epsilon^(2alpha-1)). Applying the fixed linear defect operator,
the gauge, and the Bloch Darboux inverse gives

    h_epsilon,t+h_epsilon,XX=S_epsilon,

where h_epsilon has size O(epsilon^(alpha-1)) and S_epsilon has size
O(epsilon^(2alpha-1)) in fixed spatial-distribution norms. All these
operators use only spatial derivatives and smooth base coefficients;
no unbounded time derivatives are hidden in the source. Each h_epsilon
has exactly the same prescribed initial value h0.

After removing the Bloch factor, backward Duhamel for the n-th Fourier
coefficient at any fixed positive tau<T gives, when paired with a z
test function,

    |<p_n(0),g>| <= C(1+|n|)^N ||g||_(C^M)
      [epsilon^(alpha-1) exp(-tau(nd)²)
        +epsilon^(2alpha-1)].

Here derivatives in z of exp(-lambda_n(z)s) cost only polynomial powers
of n, and its modulus is at most C exp(-s(nd)²). The time integral of
the forcing is therefore bounded by a polynomial times its stated
epsilon size. The positive-time term is bounded in the same way.

For each sufficiently large |n| choose

    epsilon_n=exp(-(tau/alpha)(nd)²).

Both terms then decay as

    exp(-[tau(2alpha-1)/alpha](nd)²).

The fixed h0 again has Gaussian Fourier tails in a distribution norm,
and the remaining complex-growth lemma would give the same
contradiction. Exponents alpha>1 imply the alpha=1 hypothesis on
epsilon<1. Nothing in this argument rules out alpha<=1/2.

The quantifier over amplitudes matters. This Holder argument requires
solutions and the uniform bound at the mode-dependent amplitudes
epsilon_n; it has not shown the same conclusion for an arbitrary sparse
sequence of amplitudes. The Lipschitz weak-limit argument earlier in
this note does apply to any sequence tending to zero. This section is
still conditional on the separate complex-Gaussian growth lemma.
