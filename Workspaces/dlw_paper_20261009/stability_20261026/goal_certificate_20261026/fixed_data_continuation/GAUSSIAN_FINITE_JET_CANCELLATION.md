# Fixed-data Gaussian route: an exact low-jet cancellation that must be retained

2026-10-26. Independently reasoned check of a possible upgrade from the
actual-sine all-order jet obstruction to finite-order nonexistence for the
current nondegenerate Gaussian datum. This note proves a cancellation, not
existence of the full IVP or a reference error estimate.

## 1. Why the old 900th-order Gaussian proof cannot be transferred

The old `GAUSSIAN_EXPLICIT_OBSTRUCTION.md` used physical initial values
`u0=.05 sin(alpha z)G`, `v0=.03 sin(alpha z)G`. Its maximal-leaf trees have
one sign after a common phase is removed. The current reference instead has

    u0=lambda sin(alpha z)F0(X), v0=4-3u0_z,

plus an independent single-carrier change. In shifted variables
`A=u_z+v-4`, `B=v-u_z-4`, the boundary coefficients of the unperturbed
Gaussian are proportional to `(-2,-4)F0`, and the primitive is `(A-B)/2`.
The maximum-Gaussian-leaf tree contributions now have competing signs.
The known unperturbed exact solution supplies a direct check that merely
counting Gaussian factors cannot produce the old nonexistence conclusion.

Below is a stronger concrete check: a reciprocal-Gaussian term that first
looks fatal to backward heat is cancelled exactly by nonlinear forcing.

## 2. One inverse Laplace transformation at the lower boundary

For the BLP variables put

    Q0=-u/2, P0=(v-4-u_z)/4,
    P1=P0-Q0_z=(v-4+u_z)/4,
    Q1=Q0-(log P1)_X,
    P2=P1-Q1_z=2P1-P0+(log P1)_Xz.

Where P1 is nonzero, the inverse transformed pair satisfies

    P1_t=P1_XX+2(Q1 P1)_X,
    P2_t=-P2_XX+2(Q1 P2)_X.

At the lower boundary `u(X,0,t)=0`, hence `Q0=0` and

    g=P1|z=0,  Q1|z=0=-(log g)_X,  g_t=-g_XX.

For the periodic Gaussian, the known boundary g remains nonzero for the
current interval `T=.01<9`; its backward heat factor changes the initial
Gaussian exponent from9 to9-t. Thus the local transformation and all its
displayed real-periodic boundary ratios are legitimate.

For an independent u-only initialization with envelope `sin²(alpha z)`
and carrier `C=cos(kappa X)`, write

    h0=epsilon alpha² C/2.

The initial boundary derivatives are exactly

    P1_z=h0, P0_z=-h0, P1_zz=-alpha² g0,

and the initial first transformed invariant is

    q0=P2|z=0 = partial_X(h0/g0).

Let h solve `h_t=-h_XX`, `h(0)=h0`. It is a finite-carrier function, so it
is defined for every finite time. Direct differentiation verifies that

    q=partial_X(h/g)

solves exactly the boundary equation

    q_t=-q_XX-2 partial_X[(g_X/g)q].

The initial reciprocal Gaussian ratio therefore does not itself create a
boundary nonexistence theorem: the actual drift is essential.

## 3. The next transverse derivative and the quadratic cancellation

Set `q1=P2_z|z=0`. Differentiating the exact P2 equation gives

    q1_t=-q1_XX-2 partial_X[(g_X/g)q1]
          +2 partial_X[(g-q)q],

because `Q1_z=P1-P2=g-q` at the boundary. All these are equations from the
full nonlinear problem.

Choose a periodic potential W1 with `q1=partial_X W1`, and choose its
time-dependent additive constant so that

    W1_t=-W1_XX-2(g_X/g)W1_X+2(g-q)q.

Writing H1=g W1 eliminates the boundary drift:

    (partial_t+partial_XX)H1=2g²q-2gq².

The initial potential is, up to an irrelevant spatial constant,

    W1(0)=3 partial_X^{-1}h0-alpha²-(h0/g0)²,

so H1(0) contains the apparently problematic term `-h0²/g0`.
However, for any two nonvanishing-denominator backward heat solutions
g,h one has the exact identity

    (partial_t+partial_XX)(h²/g)
          =2g [partial_X(h/g)]²=2gq².

Consequently the renormalized quantity

    K=H1+h²/g

satisfies

    (partial_t+partial_XX)K=2g²q=2(g h_X-h g_X),
    K(0)=3g0 partial_X^{-1}h0-alpha²g0.

The reciprocal-Gaussian term and its nonlinear forcing cancel exactly.
Both the remaining initial data and the remaining forcing contain one
Gaussian factor and a finite carrier, rather than an uncancelled inverse
Gaussian. Their finite-carrier sidebands remain Gaussian-decaying on the
current short interval. This is a checked fact at these first two levels,
not an induction to all transverse orders.

## 4. Consequence for the fixed-data goal

One must not infer finite-order nonexistence from the initial transformed
ratio `cos(kappa X)/F0(X)`, or from the term `cos²/F0` in the next initial
jet. Their full variable-coefficient/nonlinear evolutions contain the
displayed cancellations.

This does not provide a full matching inverse, control all later jets,
or bound the actual physical fields. It eliminates a concrete tempting
but invalid proof route. The exact single-carrier perturbed Gaussian and
sine IVPs remain open in the lower transverse classes under consideration.

`gaussian_finite_jet_cancellation_check.py/json` verifies the transformed
invariant equation and the two quotient/heat identities algebraically.
No numerical fit or amplitude-series convergence is used.
