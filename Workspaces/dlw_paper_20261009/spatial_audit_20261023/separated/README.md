# Four-soliton spatial/time separation — 2026-10-23

User-approved scope: A–D only; Gaussian and sinusoidal cases deferred. Spatial tests at t=0 vary h=.1,.05,.025 with dx=.1, then dx=.1,.05,.025 with h=.1. Endpoint-SD, Centered-SD and FD are all evaluated. The shared base grid is reused, giving 60 distinct spatial records. Time tests use Centered-SD only, h=dx=.1, dt=1e-4, T=.01, a=2: Euler, RK4, Crank–Nicolson (12 completed runs).

## Definitions and evidence

- `spatial.json` / `spatial.csv`: Y = analytic-x spatial RHS minus exact continuous time derivative; X = Fourier RHS minus analytic-x RHS; total = Fourier RHS minus exact derivative. These are instantaneous derivative defects under the numerical boundary closure, not initial field errors or exact-lattice/continuous field differences. Pointwise signed components sum before taking maxima.
- Analytic derivatives use exponential-sum moments and Taylor coefficient division. `validation.json` checks time derivatives and first/second x derivatives against independent nearby evaluations. `observed_orders.json` records measured h orders.
- `time_*.json/.npz`: final states and metadata. All CN steps have maximum implicit equation residual <1e-12 (fixed-point solves, no failed steps). `temporal.csv` records final continuous-reference field errors; these are not isolated time-discretization errors or a time-order study.
- `time_method_differences.json`: differences from RK4 on the same grid. No separate numerical reference is introduced.
- All maxima use native nodes in |x|<=R, |y|<R; Endpoint v is sampled at its actual edge location. Unlike the older six-case report, no spline interpolation is used. Thus some displayed maxima differ from that report even at identical grid/time parameters.
- Periodic Fourier x representation and previous boundary closure are retained. B has a persistent initial x contribution; no cause has been proved by this scan. Final B errors are large and time-method-sensitive, not evidence of reliable continuum accuracy.

## Results and manuscript

Centered-SD and FD Y defects show orders ~2 in both components; Endpoint-SD u ~2 and v ~1. These are observations of derivative defects, not new exact-field convergence theorems. At dx=.1, X is small in A/C/D; B retains X_u about1.6e-5. Final B u errors: Euler .07496, RK4 .16340, CN .16686. Lower Euler errors at one dt do not establish higher temporal order.

`methods.md` and generated `experiments.md` supply sections4.1–4.2 and5.1–5.3. `build_paper.py` renders local static KaTeX, backs up and patches `C:/Users/msz/aca/dlw-paper.html`, and produces `report/dlw_separated_experiments_20261023.html`. Data tables follow a three-rule style, bold minima per component except X (tiny differences not ranked). Build validation checks formulas, duplicate IDs, internal links and record counts. Browser file-protocol preview was blocked; visual layout not verified this turn. No PDF regenerated.

Reproduce spatial scan: `python run_separated.py spatial`. Time run: `python run_separated.py A CN` (case A/B/C/D; Euler/RK4/CN). Existing time records are preserved and reused. Build: `python build_paper.py`. All old files and pre-edit backups retained.

Revision: both scans now use .1/.05/.025. Section5.2 contains only the Y-versus-h and X-versus-dx tables, grouped with merged case labels and spectral parameters. Total defects remain in JSON/CSV. Time data unchanged; time table renumbered4. Prior spatial sets retained in backups.
