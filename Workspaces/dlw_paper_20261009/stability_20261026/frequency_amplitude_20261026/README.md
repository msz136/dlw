# Frequency and amplitude dependence of independent perturbations

2026-10-26. This experiment measures the response of the current natural Centered-SD equations to independent changes in either physical field. The four backgrounds are A (one soliton), D (two solitons), Gaussian, and sinusoidal. The selected parameters are kappa = pi/2, pi, 2pi; epsilon = 1e-7, 1e-6, 1e-5; h = dx = .1; RK4 dt = 1e-4; T = .01. This gives 72 nonlinear perturbation trajectories. Each background also has two dt = 5e-5 controls at the largest kappa and epsilon.

The perturbation is epsilon sin²(pi(y-yL)/(yR-yL)) cos(kappa x), sampled at the native sites of the perturbed physical field. The other physical field is unchanged initially. The lower u trace is identical to the background; the auxiliary perturbation starts with zero lower value and then evolves by its equation. The transverse intervals and observation regions are inherited unchanged from the published four-case experiment. No filtering, dealiasing, or viscosity is added.

## Nonlinear evolution and normalization

Write the differences as delta u = epsilon r and delta w = epsilon s, with q = Delta_h r + M_h s giving delta v/epsilon. The code evolves (r,s) using the exact algebraically subtracted nonlinear equations. In particular, every quadratic difference term retains a factor epsilon:

    delta H/epsilon = (u+4)r + epsilon r²/2
                   + h²[(w/16-1/4)s + epsilon s²/32],
    s_t = D_xx s - D_x[(u+4)s + (w-4)r + epsilon r s].

The original production RHS advances one shared background through the same RK4 stages as all 18 perturbations. Normalizing before evolution avoids subtracting nearby physical fields while preserving the full nonlinear epsilon dependence. Initial normalized RHS values are checked against the previous algebraic-difference implementation.

All tabulated maxima divide the physical perturbation by the prescribed epsilon. For A/D they use the paper's interior x/y windows; for Gaussian/sinusoidal they use the full periodic x interval and interior y sites. The L2 pair gain uses the measured initial pair norm and all periodic x nodes with the same interior y sites. These two normalizations must not be interchanged.

The full-field amplitude discrepancy compares (r,q) at each epsilon against epsilon = 1e-6, at every stored time, in the paper's observation windows. Its relative denominator is the maximum of the reference pair's two native maxima over the corresponding time interval. A terminal-only version is also retained. This comparison uses the fields themselves, rather than only differences between their norms.

The optional `fourier8` endpoint diagnostic evaluates the saved trigonometric interpolant on eight times as many x samples, retaining the original y rows. Its x domain is the **full periodic interval**, including for A/D. It is distinct from the native-window maxima and is not a continuum error bound.

## Files and evidence

- `run_sweep.py`: all main and time-step control trajectories.
- `{case}.json`: 18 endpoint records, initialization checks, baseline/legacy comparisons, source and data hashes, completion status.
- `{case}.npz`: normalized initial/final auxiliary states, background initial/final states, native coordinates, 101 time levels of maxima and L2 norms, full-field amplitude discrepancies over time.
- `{case}_history.csv`: readable time histories of normalized maxima and pair gains.
- `{case}_half_step.*`: two largest-frequency/largest-amplitude controls at dt/2.
- `collect_sweep.py`: saved-array/hash validation, endpoint rows, and time-step differences.
- `terminal_rows.csv`, `summary.json`: collected data; consult `completed_cases` and `completed_trajectories` while computation is in progress.
- `audit/`: independently constructed constant-background predictions and validation of the saved arrays.

Main-grid background endpoints are checked against the previously published RK4 fields. The kappa = pi/2, epsilon = 1e-6 trajectories are compared with the earlier independent-perturbation suite. The time-step controls compare full terminal physical fields and are empirical temporal checks of the fixed spatial system.

These records describe finite-grid nonlinear perturbation responses. No continuous independently perturbed reference or physical-field error certificate is assigned: `continuous_certificate=false`, `eta_u=null`, `eta_v=null`.

## Completed computation

All 72 main trajectories and all eight half-time-step controls reached T = .01. The four main-grid background endpoints reproduce the prior published RK4 arrays exactly. At the legacy parameter pair (kappa = pi/2, epsilon = 1e-6), the largest physical-field difference from the previous perturbation runs is 4.613e-17. Initial physical-map residuals are at most 1.111e-16 in normalized fields; the normalized RHS comparison differs by at most 5.457e-12 from the previous implementation, consistent with rearranged floating-point operations.

The largest relative difference from the epsilon = 1e-6 normalized fields, taking all input types, wave numbers, other amplitudes, physical fields and recorded times, is:

| Background | Maximum relative amplitude discrepancy |
|---|---:|
| A, one soliton | 1.178293e-6 |
| D, two solitons | 7.805670e-6 |
| Gaussian | 4.391302e-7 |
| Sinusoidal | 4.391791e-7 |

At kappa = 2pi and epsilon = 1e-5, halving the time step changes the terminal physical fields by at most 1.005e-13 across all four cases. The largest relative paired-max difference is 5.985e-10. These are observed time-step differences for the fixed spatial system. Every completed result and the precise comparison normalization are recorded in `summary.json`; the independently reviewed saved-array checks are in `audit/`.


## Published results

All 72 main trajectories reached T=.01; all eight strongest-input time-step controls completed. The four case tables and their analysis are in `../../../../report/dlw_perturbation_sweep_20261026.html` and main manuscript Section 6.2 (`../../../../dlw-paper.html`). Each table has nine (kappa, epsilon) rows and both independent input fields. The existing Figure 29 is retained for kappa=pi/2 and epsilon=1e-6. The manuscript has 29 figures and 10 tables; the control table is renumbered 10. Only Section 6.2 and that caption number changed; abstract, introduction, conclusion and all figure bytes are preserved. See `publication_validation.json`, `audit/output_validation.json`, `summary.json`, and `terminal_rows.csv`. Continuous-reference certification is a separate research branch; these are nonlinear discrete trajectory responses.
