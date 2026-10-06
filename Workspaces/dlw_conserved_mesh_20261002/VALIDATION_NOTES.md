# Independent validation of conserved-density DLW meshes

The experiment reference and initial state match the paper's continuous fields.
The ALE transport, fixed endpoints, nonperiodic x stencils, and matched density
fluxes pass independent checks. A first implementation exposed an upper-y ghost
artifact; the shared perturbation extrapolation removes it before the final runs.

## Reference and physical coordinates

The independent checker constructs the positive N=1/N=2 Gram tau directly from
Physica D equations (13), (29)--(31). It uses 60-digit joint cumulants obtained
from the set-partition formula for log-tau derivatives, not the implementation's
mean/covariance code. The physical fields are

\[
u=2(\log(f/g))_x,\qquad v=2(\log(fg))_{xy}.
\]

All cases have a=2, c_i=1, zero initial phases, and lambda=-2. A/B are Fig.1(a)/(b),
C/D/E are Fig.3/4/5. Coordinates are physical x,y; the older j+1/2 indexing
convention is not used as an additional offset. The source parameters are
(p,q)=(1,2), (4,-3), ((6,4),(-5,-3)), ((1,4),(2,-3)), and
((7/4,1),(-5/3,-4/5)).

Across 15 points in five cases, the two continuous PDE residuals are below
6.48e-59. The three continuous local density balances also vanish to high
precision. The original GSG source uses r=sqrt(1+u_x^2),
r_t+(r cos u)_x=0 and dy=r dx-r cos u dt (2.1)--(2.3).

## Numerical implementation checks

The independent comparison covers 160 initializations: five cases, SD/FD,
uniform/three density grids, nx=33/65, h=1/8 or 1/16. It performs no evolution run.

| Check | Maximum discrepancy or minimum value |
|---|---:|
| Native initial u/v versus independent taus | 6.22e-15 |
| Implementation exact u_t/v_t versus independent derivatives | 4.27e-14 |
| Initial mesh density | minimum 1.0097 |
| Initial mapped Jacobian | minimum 0.7958 |
| Analytic normalized-mass mesh velocity | 1.12e-16 |
| Implemented ALE directional derivative, u | 4.99e-9 |
| Implemented ALE directional derivative, v | 4.11e-8 |
| 30 local density/flux balances of spatial RHS | 1.69e-13 |

The first and second x derivative stencils have no coupling between opposite
endpoints. Constants and physical x have their expected first derivatives on
a nonuniform mapped grid. The mesh endpoint velocities are zero even when the
two endpoint fluxes differ. ALE checks include the derivative of the moving
analytic lower-y base and the derivative of the upper-y perturbation extrapolation.

The source hash, detailed point checks, initial RHS defects and decompositions
are in `independent_validation.json`. `verify.py` regenerates these results.

## Boundary artifact found and corrected

With an analytic upper-y ghost fixed to zero perturbation, reconstructed u_t
has an O(h^2) interior error next to a zero ghost error. The centered y derivative
divides this jump by 2h, giving an artificial O(h) contribution to v_t. All five
cases initially placed their largest v source at the upper-y row. For case B,
nx=65,h=1/8, the v source was 0.00280339: 0.00255700 came from this jump.

The final shared closure extrapolates the numerical physical-u perturbation
quadratically around the analytic exterior background. SD and FD use the same
closure. Its time derivative and ALE derivative use the same extrapolation.
The full initial v source now falls by about four when h is halved:

| Case, uniform SD, nx=65 | h=1/8 | h=1/16 |
|---|---:|---:|
| A | 1.83456e-2 | 4.59087e-3 |
| B | 3.28893e-4 | 8.22946e-5 |
| C | 4.22687e-4 | 1.05593e-4 |
| D | 2.03574e-2 | 5.09327e-3 |
| E | 4.82609e-6 | 1.20995e-6 |

These are initial physical RHS defects, not the final u/v errors. The first
implementation and its completed runs are preserved in `before_y_boundary_review`.

## Limits relevant to the comparison

The original exact solutions are substantially nonperiodic on x in [-1,1].
For A at y=t=0, the right-minus-left endpoint differences are -1.3911 for u and
-1.4716 for v. Nonperiodic analytic x boundary data are therefore necessary.

All methods evolve the interior from the same continuous physical initial fields.
The finite-domain boundary background is supplied analytically; the upper-y
numerical perturbation is extrapolated. This is a bounded reference-driven
boundary experiment, and its boundary choice remains part of the stated problem.

The local density check concerns the strong-form spatial RHS before prescribed
x endpoint overwrites. RK4 plus mapped finite differences and trapezoidal mass
does not automatically preserve an exact discrete total invariant or prove
integrability. Initial RHS defects identify sources and sensitivities; they do
not establish a rigorous finite-time nonlinear error bound. Final field errors
must come from the actual runs, with time, x, y and reconstruction controls.
