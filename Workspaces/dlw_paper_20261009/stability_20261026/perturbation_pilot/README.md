# Independent physical-field perturbations: numerical implementation

2026-10-26. This directory implements nonlinear perturbations of the current natural Centered-SD equations. These runs measure separation of two solutions of the same finite-dimensional spatial system. They do not provide a continuous perturbed-reference solution or a PDE error certificate. `certificate=false` and both reference bounds remain null in the result records.

## Common-wave-number four-case exploration

`run_suite.py` uses the existing `time_samm_20261025/time/run_time.py` setup. The unperturbed RK4 state is checked against each previously published natural-edge trajectory. Both physical fields keep their native locations. For each background, two separate runs prescribe

    u-only: (delta u, delta v) = (epsilon phi(x,y), 0),
    v-only: (delta u, delta v) = (0, epsilon phi(x,y)),
    phi = sin^2(pi (y-yL)/(yR-yL)) cos(pi x/2), epsilon = 1e-6.

The two fields are perturbed independently; this does not impose the heat/Laplace compatibility relation. The common x wave number is pi/2 (period 4). The y envelope and its first derivative vanish at both transverse endpoints. The lower u trace remains the same prescribed analytic trace. The initial lower w perturbation is zero and evolves through the same w equation. The physical v perturbation is imposed before reconstruction of w, with its roundoff-level map residual recorded.

| Case | x interval | y node interval | x Fourier index |
|---|---|---|---:|
| A | [-10,10) | [-9.95,9.95] | 5 |
| D | [-40,40) | [-39.95,39.95] | 20 |
| Gaussian | [-96,96) | [-2,2] | 48 |
| Sinusoidal | [-96,96) | [-2,2] | 48 |

The grid is h=dx=.1, the integrator is RK4, dt=1e-4, T=.01. There is no filtering, dealiasing, or artificial viscosity. At all 101 time levels the code records max|delta u| and max|delta v| in the same native regions as the paper: |x|<=R, |y|<R (R=5,30) for A,D, and all periodic x nodes with |y|<=1.8 for the other cases. Every tenth step also records the unperturbed baseline's error against its known continuous reference.

The output directory is `four_case_kappa_pi_over_2/`. Each NPZ contains the initial and final baseline/difference states, native x/y coordinates, time histories, and baseline-reference errors. Each JSON records actual completion, initialization, maxima, checkerboard projection, source and artifact hashes. The CSV records are directly usable for plots. `analyze.py` validates hashes and generates `summary.csv` and `validation.json`.

All four cases and both independent perturbations reached T=.01. Each unperturbed baseline reproduces its published RK4 state with zero array difference. The largest initial physical-field reconstruction residual is 1.06e-22. Native terminal differences, divided by the initial perturbation maximum, are:

| Case | u-only: delta u | u-only: delta v | v-only: delta u | v-only: delta v |
|---|---:|---:|---:|---:|
| A | 1.02076 | 0.09186 | 0.22453 | 1.02174 |
| D | 1.02086 | 0.10278 | 0.97382 | 1.02864 |
| Gaussian | 0.99837 | 0.01935 | 0.04930 | 0.99837 |
| Sinusoidal | 0.99841 | 0.01933 | 0.04930 | 0.99841 |

## Algebraically subtracted nonlinear evolution

Writing w=4 omega/h, the state is (u,w), and v=Delta_h u+M_-w. If (d,e) is the difference in (u,w), the nonlinear flux difference is

    delta H = (u+2a)d + d^2/2 + h^2[(w/16-1/4)e + e^2/32].

The difference equations are

    Delta_h d_t = -D_x Delta_h(delta H) - D_xx(Delta_h d+M_-e),
    e_t = D_xx e - D_x[(u+2a)e + w d + d e - 4d],
    d_t at lower y = 0.

This is an exact algebraic subtraction of the same discrete nonlinear equations, not a linearization. It avoids catastrophic cancellation from subtracting two nearby numerical fields. The baseline and both differences are advanced together through all RK4 stages. The physical difference is reconstructed linearly as delta v=Delta_h d+M_-e. The code checks the expanded vector field against direct RHS subtraction; the latter difference is about 3e-13 at the A initialization, where subtractive floating-point cancellation dominates that check.

## Earlier A pilot and refinement diagnostic

`run_pilot.py` uses x Fourier index 4 on A, so kappa=2pi/5 rather than pi/2. These preliminary runs are preserved separately and must not be mixed with the four-case table. It uses fixed y endpoints [-9.95,9.95] across h refinements. Main-grid u-only and v-only perturbations reach T=.01. Time-step halving changes terminal perturbation fields by at most 1.81e-17 in the comparison region. Halving h changes the fields by at most 3.54e-11; the v comparison interpolates the refined edge field to the original edge sites. These are empirical finite-grid controls, not error bounds.

The dx=.05, dt=2.5e-5 u-only pilot stops after t=.007525 when the next step would exceed the fixed state threshold 1e6. At the last accepted step the unperturbed baseline already differs from its known exact soliton by (20.15,5.11) in the paper's comparison region. Global baseline maxima are approximately (4.01e4,3.23e5). The perturbation difference is small only in the interior comparison region; globally it has grown to (.148,1.37). The stopped trajectory is retained with its actual time. This is a numerical failure under the existing periodic-x closure, not a physical blow-up time or proof of PDE nonexistence. It rules out treating this particular float64 refinement as an accurate reference.

`pilot_analysis.json` records all controls and the stopped-run diagnostics. The first single-u script is retained as `run_pilot_u_snapshot.py`, matching its recorded source hash.

## Interpretation of native maximum curves

An advecting cosine can have a slightly decreasing maximum on fixed sampled x nodes even when its continuous amplitude is unchanged. For speed 4, kappa=pi/2, t=.01, the shift .04 produces the factor cos(pi*.04/2)=.99803 at the original peak node. Therefore gains near .998 in the Gaussian/sinusoidal native maxima do not, by themselves, establish physical damping. The measured quantity and its sampling are kept explicit.

`endpoint_metrics.py` reads the stored initial and terminal states and writes `endpoint_norms.json/csv`. It computes weighted discrete L2 norms over the full periodic x interval and the same native y evaluation region, together with 4x/8x evaluations of each finite-grid Fourier interpolant. The source NPZ files remain unchanged. The Gaussian/sinusoidal own-field peak gains become approximately 1.00036–1.00038 on the 8x x samples; the L2 pair gains are approximately 1.000553 (u-only) and 1.001470 (v-only). This confirms that the slightly subunit native maxima are a sampling effect in these saved fields. The Fourier interpolation diagnostics remain finite-grid quantities and are not bounds for the continuous perturbed PDE.

No manuscript, project progress, index, or existing scientific result was modified by these runs.
