# Three-method perturbation-response figures

The user specifies time curves for three spatial discretizations on identical backgrounds, with u-only and v-only physical inputs shown separately. The plotted quantity is the computed perturbed trajectory minus its own unperturbed trajectory, normalized by the prescribed epsilon, measured at that method's own native physical-field sites. The user's correction explicitly excludes intermethod alignment, interpolation, difference norms and agreement thresholds. These are measured numerical responses, not certified continuous errors.

## Selected components

- Layout: repeated equal-size axes with common method encoding, informed by gallery `oa-bio-plos-pcbi-1007396-f04`; separate panels make background and response components legible.
- Lines: continuous traces differentiated by both color and dash pattern, informed by `oa-tech-pone-0116670-f16`; no sample-point clouds, filled areas, decorative icons or dual axes.
- Colors: existing DLW manuscript convention, Endpoint-SD blue `#2878B5`, Centered-SD orange `#E07A23`, FD green `#299568`.
- Primary layout: two four-row, two-column figures. Rows are one-soliton, two-soliton, Gaussian, sinusoidal. Columns are u and v responses. One figure uses u-only input, the other v-only input.
- Alternative: one four-row, four-column overview. Columns are u→u, u→v, v→u, v→v. This is a compact overview for screen inspection; the two-figure layout retains larger type for the manuscript.
- Axes: common time interval [0, .01], with ticks at 0, .0025, .005, .0075, .01. Panel-specific vertical ranges show the actual response magnitude; axis labels explicitly indicate normalization by epsilon.
- Legend: one shared legend above each figure. Same colors/styles are used in every panel.
- Rendering: 300 dpi PNG for display, vector PDF for publication, and standalone Python entry points. Only completed, recorded trajectory values are plotted.

The earlier common-grid A preview has been preserved in `common_grid_preview_superseded/` and is not a final figure. Final assets use native-node histories only.

Gallery images have been inspected; their subject data and annotations are not reproduced. The figures are not added to the skill gallery.
