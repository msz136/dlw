# Centered-SD selected from manuscript Section 3.2

**Current edition (2026-10-25):** Current active presentation selects A/D/Gaussian/Sinusoidal and emphasizes terminal physical fields. The publisher and 2D/3D figure source are in ../../spatial_ad_uv_20261025/. The older builder here reproduces the preceding six-case draft.

2026-10-25. The selected formulation is the natural physical-field system in
`../../natural_centered_section_20261025/section_3_2.md`. The display name is
`Centered-SD` throughout these selected records.

## Algebraic identification

The existing natural-edge implementation uses the auxiliary variable w. The
manuscript uses omega, with

    omega = h*w/4,
    v = Delta_h u + (w_k+w_(k-1))/2
      = Delta_h u + 2*(omega_k+omega_(k-1))/h.

The initial reconstruction therefore satisfies manuscript equation (34).
The numerical flux h²(w²/32-w/4) is exactly omega²/2-h*omega, and the w
evolution becomes omega_t=omega_xx-[(u+2a)omega-hu]_x. The lower auxiliary
trace evolves through this same equation. These substitutions identify both
physical-field equations in Proposition 3.2 with the saved natural-edge
trajectories.

`prepare.py` independently assembles both equations of Proposition 3.2 in
omega variables and compares them with the implementation's physical rates.
The largest discrepancy is 1.497e-12. The reconstruction recurrence differs by
at most 2.776e-17. The initial physical fields agree with the prescribed
continuous initial data to 8.882e-16.

## Selected data

`initial_results.json` contains six t=0 ut/vt errors freshly evaluated from the
saved initial states. `results.json` selects and relabels the six previously
computed natural-edge terminal trajectories; no time evolution was repeated.
Each terminal record retains its source record, source artifact, and hashes.
Initial rate arrays are stored in `initial_CASE.npz`.

All six cases use h=dx=.1, RK4, dt=1e-4, T=.01, a=2, and Fourier x
differentiation. The physical v field is sampled at interior edge midpoints.
The maximum-error regions match the existing comparison: soliton |x|<=R,
|y|<R with R=5,10,30,30; Gaussian/sinusoidal all periodic x nodes and native
field sites |y|<=1.8. The latter use u0=A sin(pi(y+2)/4)F(x), v0=4-3u0_y.

The six initial error pairs (ut,vt) are:

| Case | ut | vt |
|---|---:|---:|
| A | 1.6556974267e-2 | 8.4434350402e-3 |
| B | 6.8581916616e-4 | 3.4529558665e-4 |
| C | 8.3192550786e-4 | 4.3684413430e-4 |
| D | 1.2946318518e-2 | 1.0885587414e-2 |
| Gaussian | 2.9004733384e-6 | 6.9965522170e-7 |
| Sinusoidal | 2.0030274383e-6 | 4.7154707459e-7 |

## Reference and checks

Saved final fields are reconstructed again from u,w, and their errors are
recomputed from the original reference data. Both discrepancies are zero.
The non-soliton initial ut/vt reference arrays, final u/v reference arrays,
and all native coordinates are bitwise identical to arrays enclosed by the
existing nondegenerate benchmark certificate. The 1e-13 reference-value error
bound therefore also applies to these selected records.

`validation.json` records the numerical checks, source-script hash, and the
selected manuscript-source hash. Reproduce with:

    python Workspaces/dlw_paper_20261009/report_refresh_20261024/natural_selection_20261025/prepare.py

Older centered formulations and all earlier records remain in their original
project directories.

## Illustrated English numerical draft

Reader: `../../../../report/dlw_numerical_text_20261025.html`. `build_text_draft.py` and `illustrate_text.py` assemble revised numerical-formulation paragraphs and Sections5.1–5.2 with the two selected error tables. The draft uses the current natural physical fields and the three methods throughout. The user subsequently authorized main-manuscript integration. `../../manuscript_integration_20261025/` records the published Sections 3.3–3.4, 4.1–4.2 and 5.1–5.2, with all figures. The old full-potential time-comparison table is archived; current natural-form Euler/CN comparisons remain to be computed.

The illustrated draft contains30 figure groups:6 exact initial profiles,12 initial-derivative comparisons and12 final-field comparisons. Each has a300dpi PNG, vector PDF with rasterized heatmaps, and a reproduction script. Physical fields use continuous references; method error maps retain native sites. y=0 sections use native values when available, otherwise local12-point barycentric interpolation, checked against16points and exact sampled profiles. Reference bounds for the stored native arrays remain1e-13 for the two non-soliton cases; those bounds are not reassigned to interpolated plot lines.

`figures/data/validation.json` checks the native maxima against both tables; `text_draft_validation.json` verifies72 table numbers,30 figures,102 formulas, linked assets, single-pagePDFs and text placement. `figures/all_figures_contact.png` is the overview. Exact profiles follow the user's ESD slice/heatmap arrangement; their descriptions follow the existingDLW draft.

Rebuild: run `build_text_draft.py`, then `validate_text_draft.py`. Figure regeneration uses `figures/plot_initial_profiles.py` and `figures/plot_comparisons.py`.
