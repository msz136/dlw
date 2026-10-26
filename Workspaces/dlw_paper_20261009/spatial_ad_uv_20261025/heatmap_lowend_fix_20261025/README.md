# Main-paper heatmap low-end repair

2026-10-25. Requested scope: repair the white-hole appearance of error heatmaps directly in `dlw-paper.html`.

Figures 9/13/17/21 and the corresponding current `../section-5.2.html` now link to the four terminal PNG/PDF groups in this directory's `figures/`. The previous images and manuscript snapshot are preserved. The main-paper captions explain that all values at or below the shared lower threshold, including zero, share the darkest color.

`plot_figures.py` is derived from the preceding source and reads only the same saved NPZ fields and CSV maxima. LogNorm now clips the display range; its unchanged vmin/vmax are shared by all three methods in each field row. Every colorbar includes an explicit `≤` label with its numerical lower limit. Zero errors no longer become masked white pixels. No source field, section curve, coordinate, crop, maximum or table entry was changed; no numerical evolution or reference evaluation was run.

The script renders terminal comparisons only. Per-figure PNG/PDF/reproduction scripts and source/color metadata are saved in `figures/manifest.json`. `before.json` records protected source hashes; `before_dlw-paper.html` and `before_section-5.2.html` preserve the immediate previous text. `validate_fix.py`/`validation.json`, `visual_check.md`, and `browser_check.json` record independent data/scope, image and actual-main-paper checks.

This repair updates the main paper and its current Section 5.2 source. Previous audit evidence and other presentation mirrors retain their original image paths. The unrelated 3D sampling and section-selection findings from the preceding audit remain outstanding.
