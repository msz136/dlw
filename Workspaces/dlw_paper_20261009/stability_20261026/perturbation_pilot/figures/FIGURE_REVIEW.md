# Physical perturbation response figure

2026-10-26. Prepared for the current natural Centered-SD stability study.

## Design and inspection

- Four rows (one-soliton A, two-soliton D, Gaussian, Sinusoidal), paired output columns (physical delta u, delta v).
- Blue solid lines identify u-only initial input; orange dashed lines identify v-only initial input. This identification is unchanged across every panel.
- Paired axes, thin continuous lines, aligned ranges, and an unframed legend follow `oa-tech-pone-0116670-f16`; STIX serif typography follows the paper.
- All native times are plotted without smoothing. All panels share the same linear ordinate range. Curves are divided by epsilon = 1e-6, not by their sampled initial maximum.
- PNG and rasterized vector PDF were visually inspected. The final right margin was enlarged to retain the terminal time label. No clipped labels, overlaps, or missing symbols were observed.

## Data checks

The script checks each NPZ against its recorded SHA-256 hash, verifies all four runs reached T = 0.01, checks all 16 curves have 101 finite nonnegative values, and compares every endpoint with the stored JSON. The endpoint-table diagnostics also match the same source hashes. `figure_manifest.json` records these checks.

The HTML/JSON table reports native maximum-norm responses divided by epsilon and a separately defined pair L2 gain. The latter uses all periodic x nodes and the native interior y evaluation rows, with weight h*dx. The dense Fourier-interpolant diagnostics remain in JSON only.

## Interpretation

These are finite-grid nonlinear response curves. Their near-unit native maxima can change under translation of a wave relative to the sampling grid; a value slightly below one is not a damping measurement. The different y interval lengths also change the primitive entering v-only to u coupling. Comparisons with a constant-background response should use the actual interval and the same evaluation nodes. No perturbed continuous-solution error certificate is assigned to these artifacts.

## Files

- `physical_perturbation_responses.png`: 300 dpi figure.
- `physical_perturbation_responses.pdf`: vector figure.
- `physical_perturbation_responses.py`: reproducible authoring script.
- `physical_perturbation_responses_pdf_check.png`: rendered PDF used for visual review.
- `perturbation_endpoint_table.html`: paper-ready table fragment.
- `perturbation_endpoint_table.json`: endpoint values and explicit normalizations.
