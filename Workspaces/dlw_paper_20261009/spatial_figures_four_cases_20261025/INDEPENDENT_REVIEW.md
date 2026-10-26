# Independent review of the four-case manuscript and figures

2026-10-25. Read-only review of the active numerical text and plotted results. No main-text, numerical-data or plotting-source edits were made by this reviewer.

## Scope and observations

The main manuscript now presents One-soliton (source A), Two-soliton (source C), Gaussian and Sinusoidal. The two error tables contain four rows each and preserve the selected three-method values. The parameter table contains the two retained soliton problems. Searches of the active numerical section found no remaining Case B/D, six-case claim, or four-soliton introduction. Section 5 contains 12 figure groups and no collapsed details block: four exact initial profiles, four initial derivative comparisons and four terminal field comparisons. Heatmaps remain in the body.

The four terminal composites `spatial_A`, `spatial_C`, `spatial_Gaussian` and `spatial_Sinusoidal` were visually inspected. Representative initial/exact plots `initial_C`, `initial_Gaussian`, `exact_C` and `exact_Gaussian` were also inspected. Text, labels, legends and color bars are readable; no clipping or overlapping labels were observed. The enlarged two-soliton sections and narrower Gaussian/sinusoidal windows expose the profile shape while retaining the broader soliton heatmap window. The captions state the different display windows and full-region maxima.

Exact profiles use black lines and numerical profiles use method-specific open symbols. Error panels contain three continuous colored curves without markers. Inspection of `plot_figures.py` confirms that these curves connect the stored section-error samples at all x nodes; no smoothing or fitted data replaces the error. Error heatmaps use the same logarithmic scale for each component across the methods. Light-gray under-range regions are described in the captions.

The Gaussian and sinusoidal central second fields are explicitly labeled as v=4, with near-zero section-error maxima printed in the panels. The corresponding heatmaps show the errors away from the symmetry line. This keeps the exact flat central section legible while providing useful two-dimensional error information.

The numerical narrative agrees with `four_case_quantitative_review.json`: Endpoint-SD has the smallest initial u_t defect in all four cases; Centered-SD has the smallest v_t and terminal v errors in the one-soliton/Gaussian/sinusoidal cases, while FD has the smallest corresponding errors in the two-soliton case. The quoted terminal reductions, the two-soliton error magnitudes and the 0.43% short-time observation agree with the selected source records.

## Small corrections reported to the parent

1. The initial comparison figures were titled “Initial spatial derivatives” at review time. Their displayed fields are u_t and v_t, so the title should read “Initial time derivatives” or “Initial derivative comparison.” Axis labels already identify u_t and v_t correctly.
2. Add one sentence to the general figure description explaining that numerical sections use native y=0 values when available and the verified local polynomial reconstruction otherwise. This restores useful context for the staggered second field without repeating implementation details in every caption.

The review concerns the stated four-case data and the examined image files; it adds no new convergence or stability claim. The two small presentation corrections can be resolved without recomputing numerical trajectories.
