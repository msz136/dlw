# Transparent-surface final review

Date: 2026-10-25

Result: **PASS**. No required correction.

## Data and scale checks

All eight outputs in `manifest.json` were checked against their source NPZ files. Source SHA-256 values and generated PNG SHA-256 values match. All six method/component records per image have the correct source maxima, source shapes, display shapes, and ordered native y indices. The display retains every native x sample inside the stated plot window and up to 242 native y rows, including the peak row. The maximum absolute error is preserved for each method and component.

Each component uses a common linear height scale and z range across Endpoint-SD, Centered-SD, and FD. Heights are the absolute stored errors at T = 0.01; no method-specific normalization or vertical offset is used. Plot windows are A [-5, 5], D [-30, 30], Gaussian [-18, 18], and Sinusoidal [-12, 12]. Reported maxima refer to those windows.

## Rendering checks

`pixel_surfaces.py` constructs piecewise-linear triangles from the selected native coordinates. Smooth vertex normals affect lighting only. All three methods use opacity 0.34 and the same continuous opacity fade below 1e-4 times the component-wide maximum. Rendering at 3960 × 1926 followed by downsampling to 1980 × 963 improves edge quality without changing the error geometry.

`render_surface_pixels.cjs` retains the visible surface sheet of each method at each pixel, sorts the three sheets by their pixel depth, and composites them back-to-front. Shared triangle edges do not acquire duplicate opacity. The optional 8 × 6 mesh is a faint surface texture, without sectional line artists or point markers.

## Visual checks

Reviewed plain D and Gaussian plus mesh D and Gaussian at output size. The surface-only treatment is clear, with distinguishable overlapping layers and a faint mesh where requested. Axis labels, scientific scale factors, and legends are readable and uncropped. No material triangle seams or surface/axis misalignment were found. D retains its narrow error ridges; Gaussian shows smooth overlapping error surfaces. Pale bands near zero follow the documented opacity fade. The low heights of the smaller v errors follow the common linear scale and the source values.

The new previews satisfy the requested overlapping transparent surfaces, with plain and sparse-mesh alternatives. Existing manuscript and source data were not changed during this review.
