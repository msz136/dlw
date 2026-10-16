# Frozen protocol: phase-only decomposition of actual DLW error

2026-10-13. This protocol is fixed before computing any fitted error fractions.
Its SHA-256 is recorded in validation.json. The existing PDE trajectories are
read only; no new PDE solve, filtering, interpolation, or boundary adjustment
is performed.

## Inputs and exact family

Use all 21 native snapshots of A_SD_RK4, A_FD_RK4, C_SD_RK4, C_FD_RK4 from
Workspaces/dlw_three_tracks_20261013/shared. The continuous Gram reference is
the frozen notebook Exact class obtained through generate_shared.load_solver.
Verify its zero-phase fields against both archived exact fields.

For Case A there is one phase theta; for Case C there are two. If S_alpha is
the 0/1 membership vector of a tau subset, add S_alpha dot theta to that
subset's exponent in BOTH tau functions. Preserve every coefficient, p, q,
rate, gamma, h and a. Do not fit by changing Exact.gamma.

Current rates are s_i=p_i+q_i and ell_i=1/(p_i-a)+1/(q_i+a). For Case A,
theta is a single line-wave phase. For Case C, the 2x2 matrix with rows
(s_i,ell_i) is nonsingular; hence its two phase changes are exactly equivalent
to a common x/y translation of the exact two-wave pattern. The reference is
evaluated at the same physical time as the numerical field.

## Fixed windows and objective

Run each fit separately on:

1. Full archived native observation window: A |x|<=5, |y|<5; C |x|<=30, |y|<30.
2. Central window: A |x|<=2.5, |y|<2.5; C |x|<=15, |y|<15.

Use existing nodes only, with constant rectangular-grid weights. No
window/taper function is applied. For a window with N nodes minimize

  J(theta) = mean[(u_num-u_exact(theta))^2]
           + mean[(v_num-v_exact(theta))^2].

The same theta fits both physical fields jointly. There is no per-field
independent alignment, amplitude rescaling, field-standard-deviation
normalization, or later window selection.

## Linear projection and nonlinear fit

Let e=(e_u,e_v)/sqrt(N), and let columns of T be the correspondingly weighted
joint physical field derivatives with respect to phase at theta=0. Use an
unregularized least-squares orthogonal projection:

  theta_linear = (T^T T)^(-1) T^T e,
  e_phase = T theta_linear, e_perp = e-e_phase.

Record the singular values and condition number of T, tangent rank,
orthogonality residual, and the relative Pythagoras residual in
||e||^2 = ||e_phase||^2 + ||e_perp||^2. If numerical rank is lost, report the
failure rather than silently add regularization or change the parameter set.

For nonlinear minimization use analytic phase derivatives and scipy
least_squares, theta_i in [-0.25,0.25], with two starts: zero and the clipped
linear estimate. Select the lower objective; record both outcomes, convergence
flags, normalized gradient and any active bound. Use ftol=xtol=1e-12,
gtol=1e-14, max_nfev=40. Report bound contact or unsuccessful convergence.

Report both:
- explained squared-error fraction = 1 - J_fit/J_zero;
- relative joint-RMS reduction = 1 - sqrt(J_fit/J_zero).

Do not conflate these percentages. Compare nonlinear explained fraction to
the linear projected fraction ||e_phase||^2/||e||^2. Report per-field RMS before
and after the COMMON fit; a field's error is allowed to increase.

At t=0, or any frame whose joint RMS is below
100*machine_epsilon*max(1,max|exact_u|,max|exact_v|), do not fit roundoff:
set theta=0, retain raw errors, and mark fraction metrics undefined.

## Validation and comparisons

- Verify analytic phase tangents against independent centered differences
  with phase step 1e-5 at t=0.01 on each declared window.
- Verify zero-phase agreement with archived references at every frame.
- Recompute final fit objectives directly from inherited Exact.uv, separately
  from the fitting function and its analytic Jacobian.
- Check the fixed central-window and full-window conclusions separately.
- At the final time, repeat SD fits for the saved half-dt archives as a
  temporal-contamination check; do not call this spatial convergence.
- Compare SD and FD raw AND phase-aligned joint RMS using the same window.
- Save CSV, validation JSON, fitted-parameter arrays and final field
  decompositions, with all input and code hashes.

No p,q shape-parameter fit is included in this phase-only test. The residual
orthogonal to the phase tangents is called "non-phase residual", not proven
radiation, solitons, ghost solitons, or a unique shape mode. The findings are
restricted to the stored short time interval 0<=t<=0.01 and these cases.

## Figures

If generated, use the previously selected scientific panel style: shared
physical time axes, explicit SD/FD labels, equal field weighting stated in
the caption, and separate full/central-window curves. Report full-error,
linear phase part and non-phase budget without plotting undefined initial
fractions as zero.
