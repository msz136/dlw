# Fixed-RK4 comparison of current spatial formulations

Date: 2026-10-24. This directory supplies the replacement final-time table in the root `Report.html`; it does not edit the manuscript.

All 12 runs use h=dx=0.1, dt=1e-4, T=0.01, a=2 and classical RK4. Four cases A–D use the same continuous soliton parameters, computational domains, and measurement regions as the existing initial-rate table. Errors are absolute sampled maxima at each method's native field locations, against the continuous exact soliton physical fields. There is no interpolation to a denser plotting grid.

## Implementations

- Endpoint-SD and FD are evolved freshly with `spatial_audit_20261023/run.py::Model.rhs`. Their stored state is the physical pair (u,v).
- Centered-SD uses the current full-potential reconstruction in `separated/reconstruction_probe/rerun_20261024.py`, with state (u,w) and physical v reconstructed on internal edges. The four unchanged RK4 outputs are reused only after checking configuration, reconstruction, initial data and final errors. The obsolete Centered-SD branch in `Model.rhs` is not used.
- All x differentiation is Fourier differentiation, with the first derivative Nyquist multiplier zero, the second derivative multiplier retained, and no filtering or dealiasing.
- All methods use the exact continuous lower u time derivative. Endpoint-SD uses the exact lower u ghost and an open backward chain. FD uses the same lower ghost and an upper ghost consisting of the exact continuous background plus quadratic extrapolation of the perturbation. Current Centered-SD evolves every w row, including its lower trace, and needs no upper y ghost.
- SD v fields are at edge midpoints; FD v is nodal. The Centered internal edge sites agree with the corresponding Endpoint edge sites. Common physical initial data are sampled at these locations; Centered-SD determines auxiliary w by its nonlinear inverse map.

These are total final physical-field errors for the current implementations under the same RK4 algorithm and time step. They are not isolated spatial truncation errors. RK4 does not commute exactly with the nonlinear transformation from auxiliary w to physical v.

## Outputs and reproduction

Run each case independently, then collect:

```powershell
python Workspaces/dlw_paper_20261009/report_refresh_20261024/rk4_spatial/run.py A
python Workspaces/dlw_paper_20261009/report_refresh_20261024/rk4_spatial/run.py B
python Workspaces/dlw_paper_20261009/report_refresh_20261024/rk4_spatial/run.py C
python Workspaces/dlw_paper_20261009/report_refresh_20261024/rk4_spatial/run.py D
python Workspaces/dlw_paper_20261009/report_refresh_20261024/rk4_spatial/run.py collect
```

The run script preserves existing records when rerun. Per-case/method JSON files contain provenance SHA256 values, settings, closure, initial-map residuals, status and final errors. NPZ files contain final and initial physical fields, evolved state, native coordinates and attained time. `results.json` contains all 12 records. `validation.json` recomputes every error from stored physical fields and verifies reconstruction and artifact hashes. Failed runs are retained at their last completed time and labelled explicitly.

Continuous soliton formula evaluation uses binary64 analytic exponential-sum moments. This numerical audit is not an interval-arithmetic certificate of those evaluations.
