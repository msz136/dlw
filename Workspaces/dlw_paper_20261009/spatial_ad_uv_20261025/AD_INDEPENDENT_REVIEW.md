# Independent review of the A/D terminal-field publication

2026-10-25. First pass reviews `publish.py`, the selected CSV records and representative D figures before publication. No main manuscript or plotting source was edited by the reviewer.

## Scope, parameters and numerical statements

The publisher selects A, D, Gaussian and Sinusoidal, displayed as One-soliton, Two-soliton, Gaussian and Sinusoidal. The two-soliton parameter row is correctly changed to (1,2),(4,-3); its R=30 and periodic x interval [-40,40) remain appropriate. Its description of a stronger negative u trough, smaller positive ridge and two negative v bands agrees with `exact_D.png`.

The initial u_t/v_t comparison is retained only as Table 2 and short diagnostic text. Section 5.2 centers its discussion and every comparison figure on the physical fields at T=0.01 with RK4, h=dx=0.1 and dt=1e-4. Its figure loop includes only terminal section/heatmap composites and two added 3D views. The four exact initial physical-field figures remain in Section 5.1; these are distinct from the removed derivative figures.

All stated method rankings agree with the selected CSVs. Endpoint-SD has the smallest initial u_t defect in all four cases; Centered-SD has the smallest initial v_t and terminal v errors in all four. FD has the smallest final u error for A/D, whereas Endpoint-SD has the smallest final u error for Gaussian/Sinusoidal.

The exact Endpoint/Centered terminal reduction factors are:

| Case | u | v |
|---|---:|---:|
| A | 2.8034775 | 71.7192264 |
| D | 2.7583340 | 70.1198895 |
| Gaussian | 0.7402547 | 86.6407595 |
| Sinusoidal | 0.7926580 | 60.1999860 |

The D paragraph correctly quotes u changing from 4.942e-4 to 1.792e-4 and v from 7.076e-3 to 1.009e-4. The narrative confines its comparisons to these tests and includes no unsupported stability mechanism or defensive disclaimer.

## Figures inspected

`exact_D.png`, `spatial_D.png`, `errors_3d_separate_D.png` and `errors_3d_overlay_D.png` were visually reviewed. The D central profiles show the expected mixed-polarity first field and negative second field. The 2D comparison uses markers for numerical profiles, continuous lines for section errors and native-coordinate heatmaps. The 3D figures identify their quantity as absolute physical-field error at T=0.01, with |u_h-u*| and |v_h-v*| labels. Separate panels share a linear height and color scale within each field; the overlay uses method colors and common axes. Labels and the repositioned overlay legend are readable without observed clipping or overlap.

Inspection of `plot_3d.py` confirms that the error mode loads the stored final error arrays and takes their absolute values. The surface meshes are thinned for display while retaining their displayed maxima. No method-dependent normalization or vertical displacement is introduced. The much smaller Centered/FD v heights in D are expected from the common linear scale and agree with the data.

## Minor prose suggestion sent to parent

The current Table 3 overview announces the 2.8/70 improvement factors, the A/D paragraphs repeat them, and the closing paragraph repeats the same ranking. To reduce repetition, shorten the overview to:

> The terminal errors distinguish the two physical components. Centered-SD gives the smallest v error in all four tests, while the smallest u error depends on the initial wave.

Keep the concrete numbers in the individual case paragraphs. The final repeated ranking paragraph can be shortened or omitted. Where used, “by a factor of approximately 2.8” is clearer than “by approximately 2.8 times.”

## Publication check

The rendered HTML and all active figure references remain to be checked after the publisher is run. This first pass verifies the intended replacements and representative plotted evidence, not a completed HTML publication.


## Post-publication check

The rendered-source structure of root `dlw-paper.html` and `report/dlw_uv_figure_choices_20261025.html` has now been inspected. The manuscript contains 16 figure groups: four exact initial physical-field profiles and, for each of the four retained cases, the terminal section/heatmap composite, separate 3D errors and overlaid 3D errors. The candidate page contains the 12 terminal comparison groups. All inspected image/PDF references resolve, IDs are unique, and no initial-derivative figure is linked in either active presentation. The D spectral pairs are (1,2),(4,-3); the old C pair is absent from the active numerical text.

The Table 3 overview has been shortened as suggested. Its conclusions and the case paragraphs agree with the current A/D CSV values. The original Section 4 and Sections 5.3–5.5 match the pre-publication snapshot exactly, so the time-algorithm and moving-mesh material is unchanged.

The 16-group contact sheet and the revised `errors_3d_overlay_D.png` were visually inspected after publication. The overlay shows the error magnitude in each panel title; the removed duplicate z label no longer risks right-edge clipping. The legend, axis labels and both magnitude annotations are legible. No remaining presentation defect requiring a correction was found in this review.

Reviewed manuscript SHA256: `dea40ee6a07ca5329a3646298f49238c7ab1b793aa74c9363568cef893b733b8`.
