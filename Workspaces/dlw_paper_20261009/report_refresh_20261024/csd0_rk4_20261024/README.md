# CSD0: former Centered-SD formulation

Date: 2026-10-24. This directory contains new initial-rate and RK4 computations for the four soliton cases A-D.

## Definition and shared parameters

CSD0 is the original `Centered-SD` branch of `../../spatial_audit_20261023/run.py::Model`. Its state contains the physical fields `(u,v)` at the same y sites. It forms `w = v - delta_0 u` and uses the original flux

`H = u^2/2 + 2*a*u + h^2*(w^2/32 - w/4)`.

The first equation is integrated from the prescribed lower `u_t`. The second computes `v_t = -D_x((u+2*a)*w-4*u) + D_xx(w) + delta_0(u_t)`. The original exact-background plus quadratic-perturbation upper ghost closure is retained. No changes are made to the current full-potential Centered-SD implementation.

All runs use h=dx=0.1, a=2, lambda=-2, classical RK4, dt=1e-4 and T=0.01. The x derivatives use the same Fourier operators, zero first-derivative Nyquist multiplier and no filtering. Computational half-widths are 10,20,40,40; measurement half-widths R are 5,10,30,30. The error is the maximum absolute error on native physical-field samples with |x|<=R and |y|<R.

## References and outputs

Initial fields are the continuous exact soliton values returned by `Model.initial()`. Initial-rate references are analytic tau-function derivatives from `separated/run_separated.py::fields`. At final time, the reference is the continuous exact profile at the same native sites. There is no spatial interpolation in either error measurement.

- `initial_results.json` contains the four initial `(u_t,v_t)` maximum-error pairs in `total`.
- `results.json` contains the four final `(u,v)` maximum-error pairs in `error`.
- Per-case NPZ files retain coordinates, initial and final states, initial rates and their reference values, and final reference fields.
- `validation.json` reloads the saved fields and recomputes both errors. It also records comparisons against the previously saved initial defects and legacy RK4 trajectories.
- Per-case JSON files contain source hashes, artifact hashes, parameters, numerical settings and status.

All four RK4 trajectories are computed afresh. Legacy `separated/time_*_RK4_0.0001.npz` files are used only for an independent regression of the newly computed states.

## Reproduction

From the workspace root:

```powershell
python Workspaces/dlw_paper_20261009/report_refresh_20261024/csd0_rk4_20261024/run.py all
```

Existing result records are retained. Use `collect` to recompute the stored-table audit without evolving the fields again. The runner writes only to this directory.
