# Full nondegenerate continuum reference

The benchmark uses the continuous DLW system with `a=2`, x-period 192,
`y in [-2,2]`, and prescribed lower boundary `u(x,-2,t)=0`.
At t=0 the two fields are

    u0=A sin(pi(y+2)/4) F0(x),
    v0=4-3 u0_y,

with `(A,F0)=(.03,cos(pi*x/12))` or
`(.05,sum_j exp(-((x+192j)/6)^2))`.
The affine relation is imposed only at the initial time.

## Continuum solution and implementation

The underlying formula and its denominator bounds are proved in
`../../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md`.
The construction evolves two independent heat equations and applies a Laplace
transformation. It gives the full continuous DLW solution, without evolving a
spatially discretized reference system.

`reference_grid.py` evaluates that formula by finite Fourier series. It uses
an exponential Taylor polynomial of degree 32 and 96 positive Gaussian modes (one sine
mode). Fourier sums are folded onto the requested uniform x grid and evaluated
by an inverse FFT. This folding evaluates the finite series at the grid nodes;
it is not a differential spatial approximation or an evolution scheme.

The API `exact(case,x,y,t)` returns u,v; `rates(case,x,y,t)` returns u_t,v_t.
Time derivatives differentiate the formula analytically, including the shift
`X=x-4t`. No finite time differences are used for the reference. Values for
exterior ghosts use the same analytic extension. The construction depends on
`s=A sin(pi(y+2)/4)/2`, so `|s|<=.025` holds for all real y, including ghosts.

## Stored-sample enclosure

`certify_initial.py` independently encloses every stored initial physical field
and initial time derivative using Arb. The infinite Gaussian image tail is
included in the enclosure.

`certify_reference_grid.py` independently evaluates the terminal reference in
160-bit Arb/Acb arithmetic, at the exact nominal time `T=1/100`. Its analytic
truncation bounds use the same complex-parameter disk and Fourier norm estimates
as the continuum proof, recomputed for the smaller finite expansion. The largest
primitive bound is below `3.212e-34`; a common `1e-33` interval is added to each
primitive entering the physical fields. The physical quotients are then computed
with interval arithmetic, and their nonzero denominators are checked.

The interval DFT evaluates an exact rational x lattice. Each resulting primitive
is shifted to the actual stored binary64 x coordinate with a first-order Taylor
formula and a rigorous second-order remainder. Finite Fourier coefficient norms
provide the needed uniform derivatives. The binary64 y coordinates are passed
directly to Arb. Comparing the saved binary64 output to the final intervals also
accounts for conversion and evaluator roundoff. Because the intervals are
evaluated at exact `1/100`, the comparison includes the difference between the
floating-point final time and nominal T.

Only a successful certificate is authoritative. The combined
`reference_certificate.json` records the all-sample bound, counts, source hashes,
and subordinate certificates. It certifies the stored continuum references;
it is not a convergence theorem for any of the four numerical schemes.

The continuum argument is an analytic proof draft with symbolic and independent
review checks and Arb enclosures, rather than a proof-assistant formalization.

## Reproduction

    python certify_initial.py
    python certify_reference_grid.py Sinusoidal
    python certify_reference_grid.py Gaussian
    python certify_reference_grid.py

The solver outputs and this evaluator are kept separate. The numerical methods
are compared against the same continuous solution at their native field sites.
