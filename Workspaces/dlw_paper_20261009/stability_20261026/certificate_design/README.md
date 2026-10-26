# Continuous-reference certification design

2026-10-26. Active scope: **independent perturbations of the two physical fields**, as selected by the user.

Current result: `INDEPENDENT_PERTURBATIONS.md` derives a mixed-time existence theorem specialized to the current v=4 Gaussian/sinusoidal background. `independent_constants.py/json` checks its explicit contraction and initial-data constants using 256-bit Arb. Exact initial matching and the infinite-dimensional tail estimate remain open; the requested independent-perturbation continuous reference is not certified (`eta_u=eta_v=null`). This mixed-time theorem must not be presented as an initial-value theorem.

Further advance: `NONZERO_MATCHING_DERIVATIVE.md` derives the full nonzero matching derivative and a conditional analytic x-smoothing theorem, computes a genuine sideband of the current benchmark's amplitude expansion, and identifies the infinite-tail Newton estimates still required. `matching_conditioning.py/json` records the theorem constants, sideband values, and constant-background continuum/finite-difference inverse precision scales. The active perturbation carrier is pi/2. The stronger analytic ball required for the quantitative smoothing bound has not yet been certified for the actual benchmark.

`structured_reference.py`, `certify_bounds.py` and `bounds.json` preserve an earlier exploratory route for the restricted heat/Laplace family. That route changes u and v compatibly and does not meet the user's subsequent selection of independent physical-field perturbations. The bound calculation ran, but the modified point evaluator has not undergone a complete end-to-end or independent review. Do not use this branch as an independent-perturbation certificate or as a replacement for the original initialization.

No main-paper, progress-log or earlier source files were modified by this subtask.
