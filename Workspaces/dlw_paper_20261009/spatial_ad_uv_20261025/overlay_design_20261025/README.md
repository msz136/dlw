# Overlay design alternatives, 2026-10-25

Reader: `../../../../report/dlw_overlay_design_choices_20261025.html` (workspace-root report directory; resolve from ROOT when opening).

The user likes the common-axes three-method 3D idea but wants clearer error comparisons. This preview uses D and Gaussian stored T=.01 errors, comparing the existing figure (A) with light surfaces (B), sparse profiles (C), logarithmic profiles (D), linear profiles plus full-y maximum curves (E), and a second low-height 3D view (F). E is the recommended publication design; F retains an all-3D alternative.

No paper, source-array, table or published figure has been changed. `plot_candidates.py` produces ten draft PNGs (no new PDFs); `build_preview.py` creates the selector page and contact sheets. `manifest.json`, `validation.json`, `audit.md`, `audit_numbers.json` and `REVIEW.md` preserve evidence.

Lines retain every native x sample on seven selected native y rows. D uses a common log floor equal to component max * 1e-4, omitting lower values. B uses that floor for faint surface patches. E's lower curves use every native y row at each x; they are not maxima of the seven displayed profiles. F's lower panels omit line segments above the displayed upper height. No offsets, methodwise normalization or smoothing were used.

The base figure's shared linear v range compresses Centered to about 1–1.4% of full height. Its dense intersecting meshes and thinning add clutter. The current preview tests visual presentation, not a new numerical result.

Design components: current DLW paired-u/v layout and three method colors; gallery oa-geo-tc-20-5365-2026-f10 distinct profiles/line styles; oa-geo-tc-20-5365-2026-f02 large view with smaller quantitative companion. The gallery contains no direct three-surface overlay template. No figures were added to the skill gallery.
