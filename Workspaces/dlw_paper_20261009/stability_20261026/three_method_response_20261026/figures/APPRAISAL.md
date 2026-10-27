# Final figure appraisal

2026-10-26. Final assets use the clean `native/{case}.npz` exports exclusively.

Reviewed `response_u_input.png`, `response_v_input.png`, and `response_overview.png` at rendered image size. All method legends, panel labels, axis labels and tick labels are legible and uncropped. The two four-row, two-column figures are preferred for manuscript reading. The sixteen-panel overview is a compact alternative for the reader report.

The requested components are present: three fixed colors and three line styles in every panel; u-only and v-only inputs separated; identical time interval; four backgrounds; both physical-field responses. Curves that coincide remain coincident, with dashed and dash-dot gaps revealing the other traces. No vertical offsets, point clouds, smoothing, or interpolation have been introduced.

All plotted time/value arrays are copied from the native response histories, and plotting checks the line data against those arrays. The data export verifies each source artifact hash. The normalization is the prescribed epsilon, not the sampled initial maximum. The Gaussian/sinusoidal v-only native maxima begin at different sampled values because their field locations differ; this initial sampling feature remains visible.

The old common-grid A preview is archived in `common_grid_preview_superseded/` and is excluded from final plots. There are no intermethod difference curves, alignment diagnostics or agreement thresholds in the final figures.
