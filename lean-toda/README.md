# Toda formalization

This is the first Lean checkpoint for the bilinear-to-semidiscrete Toda
calculation.

Build and verify it with:

```text
lake build TodaFormalization
```

`Main.lean` proves the algebraic conversion over `Rat` using only the Lean
toolchain. `todaGap` is the quotient that becomes an exponential of logarithmic
tau variables once positivity and the analytic `log`/`exp` layer are added.

## DLW semidiscrete candidate

`TodaFormalization/DLWSemidiscrete.lean` checks the rational algebra behind a centered,
nearest-neighbour bilinear discretization in y:

```text
B = Dx^2 + Dt + 2*a*Dx
B f[j].g[j] = 0
(B f[j+1].g[j] - B f[j].g[j+1])/h
  + lambda*Dx(f[j+1].g[j] + f[j].g[j+1]) = 0
```

The file proves the formal midpoint Taylor coefficients, the Cayley
one-exponential dispersion relation, the one-exponential edge cancellation,
and an exact counterexample to retaining the continuous two-soliton
interaction coefficient. All proofs are over `Rat`; smoothness, remainder
estimates, real/complex analytic statements, solvability, stability, and
integrability are NOT formalized or established by these checks.

The candidate is formally second-order consistent at edge midpoints. It is
not a claimed integrable discretization. The counterexample rules out the
tested unchanged two-soliton ansatz, not all possible integrable structures.

`check_dlw_candidate.py` reproduces the soliton coefficient checks using
Python's exact rational arithmetic (standard library only). Run it with
`python check_dlw_candidate.py`. The refinement output measures an ansatz
residual, not the error of an initial-value numerical solver.

## Complete one-exponential residual check

`TodaFormalization/DLWOneSoliton.lean` defines the full bilinear operators
on pointwise derivative data (value, x derivative, xx derivative, t
derivative). It proves the complete residual expansions for
`f=1+A*E`, `g=1+C*E`, `E_next=R*E`, with derivative data
`E_x=k*E`, `E_xx=k^2*E`, `E_t=w*E`.

The concrete theorems verify both equations for
`a=2, lambda=-2, k=w=3, A=1/12, C=1/3`, for every step
`h != 0`, `8+3*h != 0`, with `R=(8-3*h)/(8+3*h)`.
The special case `h=1/10`, `R=77/83` is also checked independently.
These theorems are polymorphic over characteristic-zero fields, and the
amplitude E is arbitrary, so this is not a numerical sample test.

This is a full ALGEBRAIC substitution proof. It does not formalize real
exponentials or analytic differentiation. The ordinary calculus bridge
from `E_j=R^j exp(3*x+3*t+theta)` to the specified derivative/shift data
is explicit but outside the Lean proof. No new axioms or sorry are used.

## Staggered system retaining the N-soliton determinant

The revised construction and its all-N reduction to the paper's determinant
identity are documented in `dlw_staggered_construction.md`. The new pair is
`(B-h*Dx) F_j.G_j=0`, `(B+h*Dx) F_j.G_(j+1)=0`, with F on half-grid
sites and G on integer-grid sites. This replaces, rather than supplements,
the earlier centered candidate.

`check_dlw_staggered.py` performs exact rational coefficient checks for
N=1 through 5. With `--symbolic` it verifies the general two-soliton
coefficients using SymPy. The JSON files store those results.

`TodaFormalization/DLWStaggered.lean` proves the parameter-shift identity
for individual determinant entries and the centered normalization/Taylor
coefficient algebra. The complete determinant identity and analytic Taylor
remainders are not formalized in Lean. Existence of this tau family does
not establish general initial-value stability, nonsingularity, or novelty.
