# A/D terminal physical-field comparison

The selected soliton records are A (spectral pair (1,2)) and D (pairs (1,2),(4,-3)), now displayed as One-soliton and Two-soliton. Gaussian and Sinusoidal remain unchanged. No trajectories or reference arrays were recomputed.

The active report retains the initial derivative table as a short diagnostic and focuses its interpretation on the physical fields at T=0.01. Endpoint-SD has the smallest initial u_t defect in all four cases. Centered-SD has the smallest initial v_t defect in all four. The terminal u winners are FD for A/D and Endpoint-SD for Gaussian/Sinusoidal; Centered-SD has the smallest terminal v error in all four cases.

For A, Endpoint-SD/Centered-SD error ratios are 2.8034775 in u and 71.7192264 in v. For D they are 2.7583340 and 70.1198895. Thus both soliton tests have the same componentwise terminal ranking, and the centered reconstruction improves both fields relative to Endpoint-SD. FD/Centered-SD v ratios are 1.8463041 in A and 1.6791440 in D.

D's terminal (u,v) errors are Endpoint-SD (4.9419240699e-4, 7.0755251857e-3), Centered-SD (1.7916337010e-4, 1.0090610865e-4), and FD (1.1493316110e-4, 1.6943588760e-4).

Gaussian/Sinusoidal retain centered v errors 6.9669638947e-9 and 4.7059751651e-9. The FD/Centered-SD v ratios are 3.1665220 and 3.4780613. Endpoint-SD gives the smallest u errors in these two smooth profiles.

All table entries and source identities are recorded in ad_quantitative_review.json. Report validation passed for 48 error entries, 16 minima, 24 CSV rows, local links, 62 formulas and preserved source hashes. Root manuscript and its preservation baseline were not edited by this subtask. Root should advance the preservation baseline only after its authorized main-manuscript edits, then rerun validate_report.py.
