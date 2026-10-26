# Uniform-RK4 spatial-method comparison: independent audit

Date: 2026-10-24. Read-only review of the soliton solver and current full-potential Centered-SD implementation; no manuscript changes.

## Verdict

The four-soliton comparison is meaningful as **final physical-field error of three spatial formulations under common RK4 settings**: h=dx=0.1, dt=1e-4, T=0.01, a=2. It is not an isolated spatial truncation-error measurement. The existing t=0 table remains the direct spatial-defect comparison.

Use the current full-potential Centered-SD solver in `spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024.py`. The Centered-SD branch in the older `spatial_audit_20261023/run.py` is a different historical physical-field representation and must not be used for these new Centered results.

## What is aligned

- All cases use the same continuous tau-function references from `paper_comparison_20261022/solver_snapshot.py`, common continuous initial physical fields, and the same spectral parameters. A/B are one-soliton cases; C/D are two-soliton cases.
- Computational half-widths are 10,20,40,40 for A-D; measurement half-widths R are 5,10,30,30. The common sampled norm uses |x|<=R and |y|<R at each field's native positions.
- All x derivatives use the same unfiltered Fourier differentiation, including zero first-derivative Nyquist multiplier. FD denotes the continuous-system y finite-difference baseline within this shared x discretization.
- All methods prescribe the exact continuous lower U_t at every RK4 stage as the integration constant for the first equation.
- Initial u is sampled at the same nodal positions for all methods. Endpoint-SD and current Centered-SD v positions coincide on the internal edges. FD v is nodal. The extra lower Endpoint edge lies outside the reported region.
- Current Centered-SD initializes its auxiliary w by inversion of its physical-field map, so initial physical v matches the same continuous profile at the edge positions, up to the documented inverse tolerance.

## Differences that belong to the compared implementations

1. Endpoint-SD and FD advance (U,V), whereas current Centered-SD advances (U,w), then obtains V by the nonlinear full-potential map. Applying RK4 before and after a nonlinear coordinate transformation does not give exactly the same fully discrete scheme. A common dt and RK4 control the time-algorithm choice but do not eliminate its interaction with the variables. Label the result total physical-field error, without claiming the entire difference is spatial.
2. Boundary closures have the same exact-wave source but are not identical. Endpoint-SD uses the exact lower U ghost and an open backward chain. Current Centered-SD needs no upper U ghost; its lower w is initialized from continuous v-u_y and then evolves by its own equation. FD uses an exact lower U ghost and, at the upper side, the analytical background plus quadratic extrapolation of the numerical perturbation. These are the existing implementations used for the t=0 comparison, not an equal-closure controlled experiment.
3. Native v grids differ between SD and FD by half a y step. The reported norm is a sampled maximum at the respective physical locations, not a proved full-domain supremum norm. This is consistent with the current t=0 table.
4. Legacy `run.py` final errors interpolate onto a denser x grid using CubicSpline. Do not reuse those numbers alongside current Centered errors. Recompute all final errors directly from saved native-grid physical fields against analytic references with the same masks.

No new boundary intervention, filter, altered initial data, or alternative field reconstruction is required for the user's requested existing-method comparison. Such changes would redefine the methods and break continuity with the t=0 table. The new runner has been notified of the measurement and representation requirements.

## Reviewed sources

- `../README.md`
- `../../spatial_audit_20261023/run.py`: Model initialization, native grids, boundary data, spatial RHS, RK4.
- `../../spatial_audit_20261023/separated/run_separated.py`: analytic field derivatives and native sampled norms.
- `../../spatial_audit_20261023/separated/reconstruction_probe/probe.py`: Fourier primitive, physical map and nonlinear inverse.
- `../../spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024.py`: current Centered initialization, evolution, physical derivative and error norms.
- `../../paper_comparison_20261022/solver_snapshot.py`: continuous tau references and case parameters.

This review does not certify accumulated floating-point error or continuous PDE existence for arbitrary initial data; the final-time table here uses the available explicit continuous soliton solutions.
