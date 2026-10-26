# Overlay 3D audit — D and Gaussian

2026-10-25. Read-only inspection of the current error arrays and `plot_3d.py`; no manuscript, source array or existing figure was changed. Numerical details are in `audit_numbers.json`.

## What prevents comparison

1. **The linear vertical range compresses the two small v surfaces.** For D, Endpoint/Centered is 70.1199; for Gaussian it is 86.6408. The Centered peak occupies only 1.426% and 1.154% of the common height. This is a real error-magnitude contrast. Increasing saturation alone cannot make the small surfaces legible.
2. **Three intersecting grids compete with the surfaces.** The old overlay adds about 15 rows and 21 columns of wireframe per method. Every wireframe has a higher manual z-order than every surface. The resulting three-colored lattice stays visible through the surfaces, including remote lines, and the transparent fills mix colors. Reducing opacity alone exposes still more crossed lines.
3. **Thinning contributes to D's tooth-like ridges.** The native steps are 0.1. The surface is reduced to roughly 121×181 vertices, with x intervals 0.3–0.4 and y intervals near 0.5; the visible grid-line spacing is about x=3 and y=4.5. Narrow oblique bands cross those grids at different phases. The global maximum is deliberately retained, but the minimum retained row-peak ratio ranges from 0.615 to 0.883 across D's methods/components. In contrast, Gaussian row peaks are retained to at least 0.9988. Thus the D plot has a demonstrable sampling contribution to the serrated appearance; these ridges should not simply be described as numerical noise. Taking absolute values also introduces cusps at signed-error zeros.

## Native maxima on the displayed regions

| Case | Field | Endpoint-SD | Centered-SD | FD |
|---|---|---:|---:|---:|
| D | u | 4.9419241e-4 | 1.7916337e-4 | 1.1493316e-4 |
| D | v | 7.0755252e-3 | 1.0090611e-4 | 1.6943589e-4 |
| Gaussian | u | 2.1466919e-8 | 2.8999367e-8 | 4.2799509e-8 |
| Gaussian | v | 6.0362304e-7 | 6.9669639e-9 | 2.2061045e-8 |

D contains 600×601 native u points for all methods. Endpoint/Centered v have 599×601, FD v has 600×601. Gaussian contains 37×361 u points on the displayed x range; v has 36×361 for SD and 37×361 for FD. Native positions should be retained when drawing each method. A shared slice target that is not native to every method requires either a disclosed reconstruction or clearly identified nearest native slices.

## Recommended candidates

**1. Sparse one-direction sections with a very light surface.** Keep full native x sampling along 7–9 selected native y rows. Remove the crossing x-constant wireframe. Use three method colors, with line style as a second identifier; an orthographic camera around elevation 30–40° helps depth interpretation. A faint surface can retain the full-field context. This is the closest refinement of the existing common-axes plot. Its caption should say that the visible curves are selected cross-sections, not all grid rows.

**2. The same common linear view plus a lower-height inset.** Keep the full comparison at its physical height, and add a clearly labelled enlarged vertical range for the two smaller v errors. Prefer a compact 2D section inset or a secondary clipped-height 3D view if a spatial comparison is required. The inset should give its actual limits; an arrow from the low-height part of the main graph makes the relation clear. This addresses the factor-70/87 range directly while preserving absolute-magnitude comparisons in the main plot. No vertical offsets or methodwise normalization are needed.

**3. A common logarithmic-height candidate for scale comparison.** Plot log10 absolute error with common decade ticks, explicit lower cutoff and a clear legend/caption. This separates small components and answers relative-magnitude questions, but suppresses the linear visual ratio and changes the meaning of surface height. Zeros/below-cutoff values must be treated and stated consistently. It is a genuine alternative scale, not merely styling. An arbitrary added epsilon should not silently redefine the data.

Avoid unlabelled height offsets, separate normalization of the three methods, or smoothing the stored errors to remove inconvenient small structures. A light mesh is a rendering choice; modifying the error field is a different operation.
