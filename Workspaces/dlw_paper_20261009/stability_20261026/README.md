# Independent physical-field perturbations and continuous certification

2026-10-26. The user has paused continuous-reference certification for independent u/v perturbations of A, D, Gaussian and sinusoidal initial data. The unresolved target is a quantitative continuous error bound (precision may be relaxed), or a rigorously scoped high-frequency impossibility theorem. The manuscript now includes native within-method response histories in Section 5.5 (Numerical Experiments); certification research is reported separately.

## Current reader entries

- Main manuscript: `../../../dlw-paper.html`, Section 5.5, “Evolution of independent physical-field perturbations”.
- Current reader report: `../../../report/dlw_native_perturbation_responses_20261026.html`; data and plots: `three_method_response_20261026/README.md`.
- Chinese research report: `../../../report/dlw_independent_stability_20261026.html`.
- Latest goal report: `../../../report/dlw_reference_goal_20261026.html`; full residual/finite-information and initial-neighborhood impossibility results, with fixed pure-carrier reference still open.
- Previous certification report: `../../../report/dlw_reference_certification_20261026.html`.
- Retained frequency/amplitude sweep: `frequency_amplitude_20261026/README.md`; reader report: `../../../report/dlw_perturbation_sweep_20261026.html`.
- Original single-carrier protocol/data: `perturbation_pilot/README.md`.
- Proof development: `certificate_design/INDEPENDENT_PERTURBATIONS.md` and `certificate_design/NONZERO_MATCHING_DERIVATIVE.md`.
- Independent checks: `AUDIT_DESIGN.md`, `AUDIT_FOLLOWUP.md`, `audit_four_case.json`, `audit_matching_correction.json`.

## Completed results

The current publication follows24 native-site trajectories (four backgrounds, three spatial methods, independentu/v inputs), all reachingT=.01 with epsilon=1e-6,kappa=pi/2,h=dx=.1 and RK4dt=1e-4. Each curve subtracts its own method's unperturbed trajectory. The user explicitly declined alignment and intermethod comparisons; common-grid diagnostics are superseded. All12 background arrays reproduce production RK4 results exactly. Independent native-data and figure audits passed.

The retained single-method sweep covers kappa=pi/2, pi, 2pi and epsilon=1e-7, 1e-6, 1e-5 for both independent inputs on all four backgrounds. All 72 trajectories reached T=.01. Each background has a nine-row table and a fieldwise amplitude-scaling analysis. Eight strongest-input time-step-halving controls and independent array audits passed. The normalizations remain max/epsilon and measured-initial-pair L2 gain.

Eight finite-grid nonlinear perturbation trajectories reached T=.01 using the current natural Centered-SD, h=dx=.1, RK4 dt=1e-4. Each background is perturbed in u and v separately with epsilon=1e-6 and carrier pi/2, multiplied by the transverse sin² envelope. Baseline reproduction is exact at the stored-array level; the physical initialization discrepancy is at most 1.06e-22. The paired response figure and terminal table use maxima divided by epsilon; do not mix these with the separately recorded gains relative to the sampled initial maximum.

The constant-state spectrum and the exact finite-h cosh/sinh physical-field response have been independently checked against the current production closure. Most of the D/A difference in v-to-u response is explained by the transverse primitive and observation domain: observed/control ratios are 1.002309 and 1.009236. Native peak decreases in the Gaussian/sinusoidal cases are substantially sampling-phase effects; the L2 and Fourier-interpolant diagnostics are retained.

The improved shifted mixed-time theorem is proved with explicit contraction constants. Nonzero matching derivatives, conditional analytic smoothing, first sideband/initial-matching corrections and the first Gaussian-correction tail have been independently reviewed. The latter tail bounds cover only the first formal correction, not the continuous physical-field error.

## Paused continuous-reference goal

`certified=false`, `eta_u=null`, `eta_v=null` for all eight independent nonlinear perturbation trajectories. The open part is exact initial matching, including the inverse on the infinite tail and all higher corrections. The A/D whole-line initial data additionally require domain-truncation control. Ordinary refinement and the constant-state linear examples do not supply this certificate. No general smooth-solution nonexistence theorem for these specific perturbed data has been established.

The continuation in `certificate_continuation/` contains independently reviewed proof drafts: actual sine data violate every finite-order transverse Gevrey boundary estimate under explicit smooth-solution hypotheses; the constant-background formal amplitude expansion has zero radius at positive time; the particular finite heat/Laplace chain cannot terminate for any of the four independently perturbed data. These results constrain specific certification routes. They do not establish nonexistence of a general smooth solution or provide physical-field error bounds. Full matching in an admissible weaker transverse class remains open.

New material in `goal_certificate_20261026/` proves an arbitrary-small-residual/arbitrary-large-terminal-error theorem for the full nonlinear PDE, including analytic candidates with finite-grid equality; the general-target version has explicit regularity/existence assumptions. A same-envelope theorem excludes robust initial-neighborhood certificates using only finite classical boundary jets. The latest actual-Gaussian theorem excludes uniform physical-maximum-norm Lipschitz response and all-small-amplitude Holder response above exponent 1/2, with independently audited analytic proof and symbolic/interval checks. Finite regular standard Darboux constructions are also excluded for all four actual perturbed data. A time-padding argument gives a conditional constructive reduction, but no actual uniformly bounded matching sequence. None proves that every specialized certificate for the exact prescribed fixed-amplitude data is impossible. The goal is paused at the user's request. `goal_certificate_20261026/STATUS.json` records the scope and checks.

## Manuscript state and preservation

The user moved the response study into Numerical Experiments as Section5.5. The main text describes each method's own response and coupling on native physical-field sites; it uses no intermethod error or agreement-time metric. The standalone Section6, its linear derivation and the four frequency/amplitude tables have been retained in reports/snapshots. Two new eight-panel figures showu-only andv-only inputs. Original figures1–28 and Sections1–4 are unchanged. Section5 gains a roadmap sentence and5.5; the conclusion is renumbered6 without changing its body. Current total:30figures,6tables. Current checks: `three_method_response_20261026/publication_validation.json`.

Old publishers, `section6.html`, and earlier validation files document historical states. Do not rerun them to overwrite current scope. Current subsection source is `three_method_response_20261026/section55.html`; edit the main paper locally while preserving newer user edits. Earlier proofs, datasets and snapshots are retained.

The older `linear_spectrum.py/json` in this directory predate this run and use a superseded node-field formulation. They cannot be cited as the current natural Centered-SD spectrum. The exploratory structured-reference files under `certificate_design/` are also outside the accepted independent-perturbation target.
