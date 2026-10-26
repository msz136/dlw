# Natural-edge Centered-SD final-field comparison

2026-10-24. Reader: `report/dlw_natural_edge_comparison_20261024.html` at workspace root.

Four new natural-edge trajectories use v = backward-difference(u) + adjacent-average(w), with no x primitive. The original h²A(w) flux remains in the u equation. Evolve (u,w), including the lower w trace; initialize that trace from continuous v-u_y and supply continuous lower u_t at each RK4 stage. Initial physical fields sample the same continuous solitons as the existing comparisons.

All runs use h=dx=.1, dt=1e-4, T=.01, RK4 and unfiltered Fourier x differentiation. Native-position maximum errors use |x|<=R, |y|<R with R=5,10,30,30. This is a final total-field comparison with the existing method-specific closures, not a proof about leading spatial coefficients.

`run.py A` (and B/C/D) preserves existing results. `run.py collect` combines these four runs with verified Endpoint-SD/full-potential Centered-SD/FD results in `../rk4_spatial/` and CSD0 results in `../csd0_rk4_20261024/`. It creates the separate reader report, comparison CSV, results JSON and markdown table. The user subsequently requested insertion only into root Report.html Table 2: the natural-edge column is now included there; Gaussian/sinusoidal natural-edge entries are marked unavailable. Table 1 is byte-identical at the DOM level. Main dlw-paper.html remains unchanged. The main report builder and validator include this column.

Checks: original natural-edge initial u defects reproduced exactly; initial physical-field mismatch <=2.23e-16; saved v independently reconstructed from saved u,w with zero difference; final physical-field errors recomputed from stored arrays with zero difference. All 40 displayed values and per-component bold minima checked. Source and NPZ hashes retained in per-case records.

Natural-edge final (u,v) errors: A (1.67723338e-4,7.73375836e-5), B (.163389702,.0340873453), C (1.16831154e-4,1.04938964e-5), D (1.79163370e-4,1.00906109e-4). It does not give a uniform improvement over the other methods. No claim about temporal convergence or continuous-supremum certification is made.

## Nondegenerate Gaussian and sinusoidal extension

`non_soliton.py Gaussian` / `Sinusoidal` completed the two natural-edge runs under the existing parameters and initial family v0=4-3u0_y. Root Report.html Table 2 now contains all six cases and five methods, with no missing entries. Table 1 and all prior numerical values remain unchanged. `non_soliton_validation.json` confirms saved-field error reproduction and bitwise equality of reference arrays and coordinates to the previously certified full-potential artifacts; the same reference bound 1e-13 applies. Gaussian errors: (2.8999367109e-8,6.9669638947e-9); sinusoidal: (2.0029342969e-8,4.7059751651e-9). This supersedes the earlier missing-entry statement above. The separate four-soliton HTML retains its four-case scope.
