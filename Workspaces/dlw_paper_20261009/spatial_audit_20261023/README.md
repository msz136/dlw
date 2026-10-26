# DLW six-case spatial audit, 2026-10-23

## Latest alignment: a=2 in all six cases

The user reverted the main grid to dx=h=.1 and requested alignment with the soliton settings: RK4, dt=1e-4, T=.01. Gaussian and sinusoidal runs now also use a=2, replacing the earlier a=1/3 for the primary table. Files have `short_a2_` in their names; run `paper_table.py --a2` to generate `paper_table_a2_results.json`, CSV and `../../../report/dlw_spatial_table_T001_a2_20261023.html`. Earlier tables remain archived comparisons.

The dx=h=.01 exploration was stopped at the user's request. Fourteen completed full-grid failure records remain in `fine_dx001`; C-FD and the three D runs were not completed. The proposed prefix-domain shortcut was never implemented or run. Four large disk-backed scratch arrays are retained there, not active calculations. A smaller-time-step Endpoint-SD control is in `fine_dx001/control`.

## Current primary table: all six cases at T=.01

Latest user instruction supersedes the mixed final times below. Entry: `../../../report/dlw_spatial_table_T001_20261023.html`; data: `paper_table_results.json`, `paper_table.csv`. Main settings are RK4, dx=h=.1, dt=1e-4, T=.01 for all six cases. Four exact-wave rows reuse corresponding main results. `short_time.py` computes nonexact rows and controls; `paper_table.py` creates the three-rule table with separate minima for u and v.

Nonexact reference: common FD solution with dx=.1, h=.0125, dt=.00005, T=.01. Reference refinement from h=.025 changes fields by about 1e-9 and leaves the winning methods unchanged; this is a fixed-x numerical reference, not a continuum exact solution. All nonexact short-time main runs completed, with half-step differences below 5e-13. Earlier T=.1 failure observations remain separate diagnostics.

Entry: `../../../report/dlw_spatial_audit_20261023.html`.
The user requires **dx=h=.1** for the primary comparison, including nonexact data.
`main_results.json` and `*_main*.json` implement that requirement.

## Provenance and scope

- Previous comparison: `../paper_comparison_20261022/`; frozen reference formulas are imported from its solver snapshot.
- Existing Endpoint-SD PDF: `Paper/sources/dlw_y_lattice_20261018/DLW_y_lattice_and_2HS.pdf`, pp12–13. Its reported nonexact runs use dx=.5, not .1.
- All three new solvers evolve physical u,v and use independent Fourier first/second derivatives; first Nyquist zero, second retained. No filtering/dealiasing/viscosity.
- Exact initial and boundary data for A–D are the common continuous fields. These runs measure continuous-reference errors, not exact-lattice solver errors.
- Endpoint-SD v is sampled at y_k−h/2; the other formulations are colocated. Error evaluation respects physical locations; y sampling sets differ.
- Centered-SD/FD upper ghost = analytical (or frozen initial) background plus quadratic extrapolation of the interior perturbation. The same rule is differentiated in time in the Centered-SD v_t equation. Endpoint-SD needs no right ghost.
- Nonexact common physical envelope e(y)=sin(pi*(y+2)/4); Endpoint-SD v uses shifted sampling. This differs from the PDF's index-wise prescription and is not an exact replication.
- Failure threshold: nonfinite field or max absolute field >1e6. Reported detection times are discrete numerical stops, not analytical blow-up times.

## Files and reproduction

`run.py`: experiments, caching by case/method/variant; `main` dx=.1, `main_halfdt` same grid and half time step. Existing exact-case `x_refined` runs use identical settings and are copied with provenance rather than recomputed. `base` is the original coarse diagnostic (.2 for solitons, .5 for nonexact); it is NOT the primary comparison.

Run a primary case with `python -c "from run import run; [run('A',m,v) for v in ('main','main_halfdt') for m in ('Endpoint-SD','Centered-SD','FD')]"` from this directory. Run `main_report.py` afterward. `summarize.py` writes the separate coarse/refinement diagnostic report. Do not mix the two tables.

`validation.json`: Fourier and ghost derivative checks. `variable_validation.json`: compare physical-field and frozen auxiliary-variable implementations under identical Fourier and ghost settings (case A). Their final field discrepancy is below 5.5e-13; this validates the variable rewrite, not general convergence/stability.

NPZ files retain successful final fields and initial states; JSON files retain parameters and failed-run stop times. Original sources, reports and manuscript are unchanged.

## Interpretation

At dx=h=.1, A/D show a field-dependent FD/Centered-SD tradeoff; Endpoint-SD v errors are larger. B errors grow dramatically on refining x from .2 to .1, across all methods. A smaller time step does not remove this issue. Nonexact runs at .1 stop before T=.1, unlike the coarse .5 controls. These observations must remain visible, not be screened out to select favorable rankings. Further work should isolate periodic-tail/closure/high-frequency effects before promoting the B row to a precision comparison.
