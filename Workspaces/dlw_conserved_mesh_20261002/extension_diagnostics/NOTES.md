# T=0.01 independent audit of the frozen solver

The old source was imported without edits. Only `TIMES`, `OUT` and probe specs
were redirected. The probes use case A, the original physical parameters
`a=2,p=1,q=2`, x,y in [-1,1], h_y=1/8, fixed uniform x grids, and the original
boundary reconstruction, SD/FD equations, and RK4. No filtering, interior exact
forcing, or density modification was used.

## Findings

At nx=33 the solver reaches T=.01. At nx=65 it becomes grossly inaccurate before
T=.01. Halving dt from 5e-6 to 2.5e-6 leaves these trajectories unchanged to high
accuracy until nonlinear blow-up; this is not an RK4 timestep stability issue.

| Method,nx | T=.002 u/v max errors | T=.005 u/v max errors | T=.01 |
|---|---:|---:|---|
| SD,33 | 8.84025e-5 / 5.08754e-5 | 2.58891e-4 / 1.61440e-4 | 1.78600e-3 / 1.29242e-3 |
| FD,33 | 3.08552e-5 / 6.87005e-5 | 9.02890e-5 / 2.46952e-4 | 1.89840e-3 / 3.23240e-3 |
| SD,65 | 1.85432e-4 / 1.28779e-4 | 9.75365e-2 / 8.41302e-2 | stopped at .00903; u/v errors 167.75 / 214.99 |
| FD,65 | 1.19591e-4 / 1.65829e-4 | 7.49231e-2 / 1.00749e-1 | stopped at .00870; u/v errors 234.18 / 1314.70 |

At nx=33, final u/v errors change by <1.2e-13 under timestep halving. At nx=65,
T=.005 field errors change by ~1e-10. The FD stopping time differs by one old
5e-6 step because the magnitude guard is crossed between steps; comparing the
last unequal times would be misleading. SD stops at the same time in both runs.

The dense physical error includes cubic reconstruction. Its nonzero t=0 value
is interpolation error; nodal initialization remains exact. Both measures are
saved in every run, and the large late-time errors are not explained by initial
interpolation.

## Growing mode evidence

For the actual uniform derivative matrix, D1^2 restricted to interior Dirichlet
variables has most negative real eigenvalues -498.454 (nx=33) and -1993.544
(nx=65). The frozen initial physical-field Jacobian has positive rates about
593.64/585.00 (SD/FD,nx=33) and 2268.45/2232.70 (SD/FD,nx=65). Central directional
differences and sparse eigenvalue residuals are saved in `growth.json`.

This Jacobian probe diagnoses a mechanism; it is not a nonlinear error bound.
The underlying PDE linearization already admits a growing high-x-frequency
branch. Around u=v=0, with w=u_y and y frequency eta !=0,

lambda = -2 a i kappa +/- sqrt(kappa^2 (kappa^2+4 kappa/eta)).

For large |kappa|, the positive real rate is ~kappa^2. Thus smaller physical cells
can greatly increase the range of admitted growing modes. The present boundary
closures also seed and amplify those modes: at T=.005,nx=65 the largest errors
are at x~.935, close to the right boundary, but interior |x|<=.75 errors are
already ~.0042-.0052. Restricting the error norm to omit boundaries would not
repair the comparison.

At dt=2.5e-5,nx=33 the largest diagnosed positive rate has lambda*dt=.01484.
The scalar RK4 exponential accumulation defect through T=.01 is ~2.4e-9 relative.
At nx=65,dt=1.25e-5 it is ~1.2e-7. Both are small. These scalar estimates are
diagnostics only; the actual paired timestep checks remain the authority for
moving nonlinear grids.

## Interpretation for the density extension

Retain checkpoints .001,.002,.005,.01. Report actual final fields when a run
reaches .01, and separately label guard stops and density/Jacobian failures.
Keep same time in comparisons. For a late-time density improvement, require
that it survive x refinement, y refinement and timestep halving. If x refinement
amplifies errors rather than reducing them, do not call the coarse-grid ranking
a converged physical-field accuracy improvement. Positive mesh density alone
does not control the growing DLW branch. A larger error on the fine grid is an
observed failure of the current discretization and boundary experiment at that
time, not a theorem that every adaptive mesh or every DLW computation must fail.

The parent extension may use dt=2.5e-5 on nx=33 and dt=1.25e-5 on nx=65; these
are plausibly sufficient time resolutions here. Larger-time credibility is
limited primarily by spatial growth, not by those timesteps. No stabilizing
change is applied in these probes, so density and time comparisons remain clear.

## Files

- `probe_original.py`: reproducible eight runs, dt=5e-6/2.5e-6, nx=33/65, SD/FD.
- `out/*.json`, `out/*.npz`: full errors and numerical/exact/error fields.
- `frozen_growth.py`, `growth.json`: frozen spectrum diagnostics.
