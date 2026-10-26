# Figure data

`prepare_data.py` builds `{case}.npz` and `{case}.json` for A, B, C, D,
Gaussian and Sinusoidal. The shared API is `../figure_data.py`.

The selected methods have prefixes `endpoint`, `centered`, `fd`.
All two-dimensional arrays have shape `(ny,nx)` and use the displayed x
coordinates in `x`. Each physical field retains its native y coordinates in
`{prefix}_y_u` and `{prefix}_y_v`. The y region matches the error tables;
Gaussian/sinusoidal x displays are cropped to [-24,24].

For stage `initial`, `rate`, or `final` and field `u` or `v`:

- `{prefix}_{stage}_{field}` is the numerical physical value.
- `{prefix}_ref_{stage}_{field}` is its continuous reference at that native site.
- `{prefix}_error_{stage}_{field}` is their signed difference.
- `{prefix}_line_{stage}_{field}` is the physical numerical section at y=0 on x.
- `{prefix}_line_error_{stage}_{field}` subtracts the continuous y=0 reference.
- `exact_native_{stage}_{field}` is the continuous y=0 reference on x.
- `exact_line_{stage}_{field}` is the continuous y=0 curve on dense `line_x`.

At stage `rate`, the u and v keys hold u_t and v_t. The final time is .01.
Initial exact profile surfaces use `exact_initial_y`, `exact_initial_u`,
`exact_initial_v` and the same x array.

## Sections

A native node within 1e-12 of y=0 is used directly. Otherwise a degree-11
barycentric polynomial uses the twelve nearest native y nodes. The numerical
physical values themselves are interpolated. A separate degree-15 polynomial
and the interpolation of exact sampled values are checked against the analytic
y=0 section. Each case JSON records these controls for every stage and field.

The largest degree-11/15 difference is 4.961e-10 (case A, centered initial u_t).
It is 5.315e-12 for the same final u section. All initial and final maximum
errors recomputed on the full native measurement regions reproduce the tables
exactly. Gaussian/sinusoidal native reference arrays inherit the existing
1e-13 certificate. Interpolated sections and newly evaluated dense curves are
covered by the recorded evaluation and interpolation checks.

For the Gaussian and sinusoidal profiles, y=0 is a symmetry line on which
v=4 for all t and v_t=0. Their v-section values therefore display this constant
background; the two-dimensional errors show the off-axis behavior.

## Exact-value API

`exact_fields(case,x,y,t)` and `exact_rates(case,x,y,t)` accept arbitrary x,y
arrays and return two y-by-x arrays. Solitons use analytic exponential-sum
moments. The non-solitons use explicit initial formulas and, for positive time,
the finite Fourier/Laplace formula evaluated as Laurent polynomials at the
requested coordinates. `load_case(case)` returns the prepared NPZ arrays.

Sources, artifact hashes, table maxima and interpolation diagnostics are in
the case JSON files. `validation.json` supplies the aggregate checks.
