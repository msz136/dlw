# Compatible continuum reference on the experiment grids

The reference uses the Cole--Hopf solution in
`../../reference_certificate_20261024/compatible_benchmarks/PROOF.md`.
The physical coordinate is `y=z-2`.  Initial data are

    u0=A sin(pi(y+2)/4) F(x),
    v0=4-A(pi/4)cos(pi(y+2)/4) F(x).

Gaussian: A=.05, F=sum_j exp(-((x+192j)/6)^2).
Sinusoidal: A=.03, F=cos(pi x/12).
The equations reduce on this invariant family to
`u_t=u_xx-(u+4)u_x`, `v=4-u_y`.

## Evaluation

`reference_grid.py` provides:

- `evaluate_grid(case,x,y,t) -> (u,v)`;
- `evaluate_ut(case,x,y,t) -> u_t`;
- `initial_data(case,x,y) -> dict(u,v,uy,ut,vt)`.

Each output has shape `(len(y),len(x))`.  All real y are accepted.  Both the
Cole--Hopf positivity argument and the analytic truncation estimates depend on
the uniform bounds |sin|,|cos|<=1, so the same solution extends to the exterior
ghost rows y=-2.1,2.1 and to the Endpoint-SD half sites.  This is an analytic
extension of the chosen solution.

The evaluator constructs the degree-32 Taylor polynomial of exp(s J_K), with
K=96 for Gaussian and K=1 for sinusoidal data.  Coefficients and their y
derivatives are cached.  A DFT evaluates the finite heat formula.  Modes above
the DFT dimension are folded modulo N; this evaluates the finite series at
the requested uniform sample positions without truncating those modes.
Nonuniform x requests use direct series evaluation.

Gaussian coefficient preparation for 41 rows takes about 1.1 seconds; cached
evaluation of five boundary rows takes about 4 milliseconds.  The
`reference_grid.py` SHA-256 recorded by all runs is
`be45705309b812da307c4ad0b289dd02fe692dda372d2f3051f44bd3f1817471`.

## All-node reference certificate

`certify_reference_grid.py` rebuilds the coefficients and DFT in 160-bit Arb
ball arithmetic and checks every stored reference value for all six runs.
The certificate covers the full saved grids, including points outside the
reported |y|<=1.8 measurement region.  Each case has 1,920 x nodes and 99
distinct binary64 y positions across the three layouts.  Stored repeated
values are checked separately.

At t=0 the analytic initial fields and rates are evaluated directly in Arb
at the exact binary64 sample coordinates.  Gaussian sums use five images;
the nearest omitted image has distance at least 480 and exponential factor
at most exp(-6400).  The field and derivative tails are below 1e-100, which
is added explicitly.  This includes the initial u,v arrays obtained from
the Fourier evaluator, not just the separate analytic rate arrays.

At the final time, the Arb DFT evaluates the finite series at the ideal
uniform grid x0+192i/N.  The difference between this grid and each actual
stored binary64 x is included using rigorous spatial derivative bounds.
Writing B_j=sum |omega n|^j |Q_n| exp(-(omega n)^2 t), and similarly Z_j for
Q_y, bounds for the exact H derivatives follow after adding the analytic
tail.  The tail is estimated in the weight-three Banach norm

    sum_n (1+|omega n|)^3 (sup_y |f_n| + sup_y |partial_y f_n|).

For the Gaussian tail, its successive positive summand ratio is bounded by
`((K+2)/(K+1))^3 exp(-9 omega^2(2K+3))<1`.  The resulting derivative tails
are below 9.60e-41 (Gaussian) and 2.98e-60 (sinusoidal).  The quotient rule,
H>.6, and the chain rule Y_y=-mu_y t give uniform bounds for |u_x| and
|v_x|.  Multiplying by the exact sample displacement bounds the coordinate
contribution by 4.31e-16.  The 1e-32 analytic physical-field truncation
envelope from the original proof is added separately.  The largest final
reference error enclosure at the actual binary64 time is 8.31e-16.

The nominal final time in the report is exactly 1/100.  Binary64 `.01`
differs from it by 2.081668171...e-19.  We also include this displacement.
The same norm with weight four gives exponent bounds R4<.625 (Gaussian)
and R4<.260 (sinusoidal), so all H derivatives through four x derivatives
and one y derivative have magnitude below 3.  Together with H>.6,
|mu|,|mu_y|<1 and t<.011, the quotient rule gives the conservative bounds

    |u|<11, |u_x|<60, |u_xx|<660,
    |u_y|<62, |u_xy|<668, |u_xxy|<11000.

For example, differentiating
`u_xx=-2(H_xxx/H-3H_x H_xx/H^2+2H_x^3/H^3)` in physical y uses total
H derivatives bounded by 3+.011*3=3.033.  The six product/quotient terms
then give |u_xxy|<11000.  Hence

    |u_t| <= |u_xx|+(|u|+4)|u_x| < 1560,
    |v_t| <= |u_xxy|+|u_y u_x|+(|u|+4)|u_xy| < 24740.

Using the common relaxed bound 1e5 adds at most 2.082e-14.  The largest
combined final enclosure is below 2.165e-14.  Thus **1e-13 is a valid
uniform bound for every stored initial u,v,u_t,v_t reference value and
every final u,v reference value at nominal T=1/100**, for both cases.
The certificate concerns the reference values used to measure the methods'
errors.  Its basis is an analytic proof and verified Arb computations.

`reference_certificate.json` contains per-field bounds, counts, time and
coordinate corrections, and source/data hashes.  Reproduction:

    python certify_reference_grid.py Gaussian
    python certify_reference_grid.py Sinusoidal
    python certify_reference_grid.py

The Gaussian full-grid verification takes about 94 seconds; sinusoidal
verification about 9 seconds.
