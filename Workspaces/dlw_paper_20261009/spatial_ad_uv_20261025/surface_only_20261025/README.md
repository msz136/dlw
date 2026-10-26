# Transparent surface-only previews

2026-10-25. User-directed revision of the three-method overlays. Reader: [surface preview](../../../../report/dlw_overlay_design_choices_20261025.html). The four plain surfaces are now added to the main manuscript, its numerical mirror and the figure gallery, adjacent to the existing wireframe overlays. The previous paper and mirrors are saved in `before_paper_insertion/`.

## Visual specification

- Layout: two shared 3D axes per case, one for each physical component.
- Geometry: overlapping translucent surfaces, without sectional curves or raw-point markers.
- Color: Endpoint-SD blue, Centered-SD orange, FD green, inherited from the existing overlays.
- Two variants: plain surface (preferred preview) and faint sparse surface grid.
- Orthographic camera, common linear height scale within each component, restrained axes and lighting.

All four cases A/D/Gaussian/Sinusoidal use existing RK4 results at T=.01, h=dx=.1, dt=1e-4. The plotted quantities are absolute terminal physical-field errors. No new numerical simulations were performed.

## Data and rendering

Data are the NPZ files under `../../report_refresh_20261024/natural_selection_20261025/figures/data/`. `pixel_surfaces.py` retains all native x samples inside the existing plotting windows and up to 241 native y rows plus the native peak row. Heights are the original sampled absolute errors; triangles interpolate them linearly. There is no field smoothing, per-method normalization, or vertical offset. Smooth lighting changes color only. Opacity is .34, fading linearly to zero below 1e-4 of the component's common maximum to avoid three overlapping colored zero planes.

`render_surface_pixels.cjs` rasterizes the nearest visible surface sheet of each method, then composites the three method sheets per pixel in depth order. This removes the translucent shared-edge seams of the earlier Matplotlib attempt. It represents one visible sheet per method, rather than all intersections of a folded surface. The mesh variant adds an 8-by-6 faint surface texture. The stored projected vertices and rasterizer metadata are in `render_data/`.

The previews are 180 dpi PNG drafts. `manifest.json` records source and image hashes, native selected indices, maxima, scales and renderer settings. `preview_validation.json` records file/hash checks, JavaScript syntax and unchanged manuscript hash. `FINAL_REVIEW.md` provides an independent data/rendering review. The selected native maxima are preserved; these preview plots do not add a new error certificate.

`insert_into_paper.py` added the plain surfaces as Figures 12, 16, 20 and 24. Only Section 5.2 changed in the main manuscript; all 20 previous figures and the numerical tables were retained. The text presents the numerical comparison as a finished paper, without design-choice commentary. `publication.json` records the addition; the parent `publication_validation.json` checks the 24/24/20 paper/mirror/gallery figures, continuity, adjacency, equations, links and unchanged protected sections. `PAPER_INSERT_REVIEW.md` records independent publication review. `publish.py` in the parent directory is guarded against reverting to the former 20-figure version.

## Reproduction

From the workspace root, run `python Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/surface_only_20261025/pixel_surfaces.py`, then `python Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/surface_only_20261025/publish_preview.py`.

`plot_surfaces.py` is the retained earlier Matplotlib attempt and supplies plotting constants. Its main routine must not be used to republish the current previews. `before_overlay_preview.html` preserves the previous line-based design page. `figures/contact_sheet.png` compares the eight new previews.
