# Independent perturbation response of each spatial formulation

2026-10-26. The accepted publication scope follows each method's own perturbed-minus-unperturbed physical-field trajectory. Endpoint-SD, natural Centered-SD and FD curves are overlaid for display. There is no interpolated common-grid comparison or agreement threshold in the published dataset.

## Protocol

The four backgrounds are one-soliton A, two-soliton D, the current nondegenerate Gaussian and sinusoidal benchmarks. Each method starts from the same analytic physical background sampled at its native field locations. In separate runs, add `epsilon*sin(pi*(y-yL)/(yR-yL))^2*cos(kappa*x)` to u or v, with epsilon=1e-6, kappa=pi/2, h=dx=.1. All trajectories use RK4 dt=1e-4 to T=.01. The initial perturbation is sampled at each field's own locations: u shares y nodes; Endpoint-SD v lies at y-h/2, Centered-SD v at interior midpoint edges, FD v at nodes. Native peak values can differ slightly at t=0 because of these placements.

Each perturbed-minus-background difference is evolved by exact algebraic subtraction, divided by epsilon. Quadratic terms retain their epsilon factors. This avoids subtracting nearly equal floating-point trajectories without replacing nonlinear evolution by a linearization. All methods retain their existing production boundary rules and exact prescribed lower u trace. Endpoint-SD retains its lower ghost; FD retains the exact-background plus quadratic perturbation upper ghost; Centered-SD evolves the lower auxiliary value from its physically matched initial state.

Response maxima use each method's own native field sites in the original observation region: |x|<=5,|y|<5 for A; |x|<=30,|y|<30 for D; all periodic x and |y|<=1.8 for Gaussian/sinusoidal. No interpolation enters published curves or tables.

## Data

- `native/{case}.npz`: `t` and `response_normalized` with axes `(time,method,input,output)`, ordered methods Endpoint-SD/Centered-SD/FD, inputs u/v, outputs u/v. Native initial/final normalized difference fields and coordinates are also retained for audit.
- `native/{case}.json`: parameters, trajectory status, terminal response rows and within-method baseline reproduction checks.
- `native/terminal_rows.csv` and `native/summary.json`: report-ready final values, with one row per method and independently perturbed field.
- `audit/`: exact nonlinear flux identity and native-array recomputation checks.

The recorded baseline values at T=.01 are checked against the prior production RK4 solutions. The independently perturbed continuous PDE solution is not certified by these numerical response curves.

## Provenance and superseded intermediate work

`run_comparison.py` produced both native histories and preliminary common-grid metrics before the user clarified the desired presentation. `export_native.py` extracts only native histories and physical endpoints, and `collect_native.py` assembles the accepted dataset. The common-grid interpolation and agreement-window outputs are superseded; they are retained in `superseded_common_grid/` once all trajectories finish. They are not used in the paper or the native response figures. No numerical evolution is repeated merely to remove those unused diagnostic quantities.


## Manuscript and reader report

Current main text is Section 5.5, "Evolution of independent physical-field perturbations", in `../../../../dlw-paper.html`. The standalone reader report is `../../../../report/dlw_native_perturbation_responses_20261026.html`. Figures29/30 present u-only/v-only native-site histories, each with four cases and three method styles. The report contains three separate methodwise endpoint tables and an optional overview layout. No common-grid interpolation, intermethod field difference, or agreement threshold enters the published material. Previous Section6 and the72-trajectory frequency sweep remain in snapshots and separate reports. Main totals:30figures,6tables; conclusion renumbered6 with body preserved. Checks: `publication_validation.json`, `audit/native_output_validation.json`, `figures/figure_validation.json`.
