# Four-case spatial figures and manuscript presentation

**Superseded presentation:** The current A/D edition emphasizes terminal physical fields and adds two 3D alternatives. See `../spatial_ad_uv_20261025/README.md`; do not run this publisher over the current paper.

2026-10-25. Readers: `../../../dlw-paper.html` and `../../../Report.html`.

The user selected A and C from the four soliton cases. The active case names are One-soliton, Two-soliton, Gaussian and Sinusoidal. A/C remain source keys. B/D source data and previous figures are retained.

## Figure design

The user specified markers only for numerical/reference profile comparisons and continuous colored lines for the errors. They subsequently requested that all three methods' two-dimensional heatmaps remain visible in the body. Each comparison is therefore one ten-panel group: two y=0 profile panels, two y=0 absolute-error curves and six native error maps. Exact references are black lines; numerical profiles use blue circles, orange squares and green triangles. Error curves connect every stored x sample without fitting or smoothing.

Four exact initial-field figures, four initial time-derivative comparisons and four terminal-field comparisons are in the body. There are no collapsed heatmap blocks. The two-soliton sections focus on [-8,8], with maps retaining [-30,30]. Gaussian plots show [-18,18]; sinusoidal plots show one period [-12,12]. Table regions remain unchanged. Each component's three error maps share a logarithmic color range; sub-range values are light gray. The y=0 section is marked in white on maps.

Gaussian/sinusoidal reference v equals four on y=0, and its initial time derivative is zero there. Those panels explicitly identify the symmetry and the observed section-error scale. Full native errors appear in the lower maps. The existing 12-point section reconstruction and its earlier independent controls are reused; the native reference certificate is not reassigned to interpolated plot values.

## Data and publication

No evolution runs or source-array edits occurred. Sources remain in `../report_refresh_20261024/natural_selection_20261025/figures/data/`. `four_case_quantitative_review.json` independently checks all cited comparisons. The report's current two CSVs each contain 12 records, retaining A/C provenance; originals and former report scripts are in `before_report/`.

`plot_figures.py` creates 300 dpi PNGs, PDFs and individual reproduction scripts under `figures/`. `publish.py` replaces only the Section 5 introduction, Sections 5.1–5.2 and the editorial guide in the main paper, and synchronizes the standalone English draft. It reads immutable pre-edit snapshots and guards against concurrent manuscript changes. `validate.py` checks 48 table values, 16 bold minima, all formulas/links, 12 figures/PDFs and unchanged theory, time-integration and moving-mesh sections.

Archived source entry: this directory. Current source: `../spatial_ad_uv_20261025/`. The previous `natural_selection_20261025/build_text_draft.py` and `manuscript_integration_20261025/integrate.py` reproduce earlier six-case editions and must not replace the current manuscript. The report-only builder has been updated to the selected four cases.

`validation.json`, `publication.json`, `report_update.json` and `INDEPENDENT_REVIEW.md` record the checks. The review's two editorial corrections (initial time-derivative heading and section interpolation explanation) have been applied. `figures/contact_sheet.png` covers all 12 groups; `figures/before_after_C.png` compares the old and new two-soliton sections.
