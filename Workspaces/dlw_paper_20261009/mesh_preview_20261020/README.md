# Case C SAMM figure proposals

Actual coupled PE/RK4/SAMM calculation, using the existing notebook definitions. No changes to the notebook or manuscript. Reproduce with compute_mesh.py then plot_options.py. Configuration and diagnostics are in metrics.json; snapshots and exact-field backdrop are in case_C_mesh.npz.

Four options in mesh_options.png: A matched exact-u background with uniform/SAMM mesh overlays; B averaged density and sampled node strips; C all local spacings normalized by the uniform spacing; D actual node displacement since adaptive initialization. Mesh overlays and strips use identical index subsampling, explicitly labelled. Both A backgrounds show the same exact field at T, isolating the node distribution. C includes the adaptive initial grid separately from final grid.

Visual reference inspected: plot-is-all-you-need/gallery/oa-geo-esd-15-527-2024-f12.png, borrowing aligned spatial panels and field overlays only. B–D are original layout proposals outside the gallery. Preview inspected: labels and axes visible; no overlap; numerical spacing extrema match metrics.json. The redistribution is mild (minimum spacing 0.098344 versus 0.1); recommend A+C or B+C rather than mesh overlay alone. No artwork added to the skill gallery.

Pending: user chooses layout, then produce publication PNG/PDF with caption and optional paper insertion. Section 3/3.1 and opening 3.2 conversational edits still await manuscript synchronization.
