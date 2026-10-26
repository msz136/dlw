# Section 5.1 onward: independent figure/table audit

2026-10-25. Reader report: `../../../report/dlw_figtable_audit_20261025.html`.

This round reads the current 24 manuscript images, 3 tables, source CSV/JSON/NPZ records and plotting code. No solver, time evolution, continuous-reference evaluator or old publisher was run. The manuscript and existing plots/data were not changed.

- `table_audit.md`, `table_checks.json`, `audit_tables.py`: independent HTML/CSV/original-record/native-array checks.
- `plot_provenance.md`, `plot_data_checks.json`, `audit_plot_data.py`: native data identity, section reconstruction, scale, cropping, mesh-thinning and file identity checks.
- `visual_audit.md`, `visual_sheet_1.jpg`–`visual_sheet_4.jpg`: visual review covering all 24 figures.
- `layout_audit.cjs`, `layout_checks.json`, named PNG screenshots: current main-paper desktop and narrow-window layout inspection.

All numerical operations in these audit scripts are saved-array comparisons, extrema/statistics or diagnostics of the plotting interpolation; they do not recompute the original experiment. Surface sampling residuals diagnose the geometry representation between retained samples, not a change in the numerical solution or its reported maximum error.
