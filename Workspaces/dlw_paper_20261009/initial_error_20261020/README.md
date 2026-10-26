# Initial PE/FD spatial error budget (2026-10-20)

Purpose: quantitative explanation after Section 3.5.1 figures; manuscript/HTML not yet synchronized.
Current notebook cells and parameters are recorded by hash/config in verification.json.
Run `python analyze.py` in this directory or from the workspace root with its full relative path.

## Definitions

Evaluate all signed fields at t=0 on the continuous exact solution, using the actual lower y boundary b and the paper's native fixed-grid nodes within its four stated regions. RMS is the unweighted root mean square on these nodes. Correlation is the normalized uncentered inner product (direction cosine).

The quantities are instantaneous spatial RHS residuals (field/time), not nonzero initial physical-field errors. With continuous physical initialization, the latter is zero up to field recovery error.

For smooth fields, r_m^u = X+Y_m+O(dx^4+dx²h²+h^4), X=dx²B, Y_m=h²A_m.
The common B is the coefficient already discussed in Section 3.1.
With Δ_b denoting upper minus lower endpoint:

- A_FD = -(1/12) ∂xx Δ_b v_y.
- A_PE = A_FD - ∂x Δ_b[(v-u_y)²/32-(v-u_y)/4] + (1/4)∂xx Δ_b u_yy.

Full derivation and analytic log-tau derivative evaluation:
`../../dlw_error_mechanism_20261013/sources/LEADING_U_FORMULAS.md`.

## Results

leading_u.csv contains RMS X, RMS Y, direction cosine, RMS/max sum, full residual and relative field difference.
A/D: FD negative correlation, PE positive; B/C: PE negative, FD positive.
Leading RMS and maximum residual rankings match the reported terminal u maximum-error rankings in all four cases.
Leading/full residual relative RMS differences: 0.118%–2.118%.
Native solver RHS versus independent operator decomposition: max absolute difference below 1.33e-12.
This is a quantitative initial forcing explanation, not an identification of RMS forcing with terminal maximum solution error.

exact_uv.csv additionally gives full finite-spacing x/y decomposition for both u and v (no common-B claim for v).
For v, initial maximum residual is lower for FD in all four cases, matching final v maximum-error ordering. B/C RMS residuals are slightly lower for PE; RMS and maximum comparisons must be distinguished.

## Files

- analyze.py: reads current notebook, imports established analytic coefficient routines, runs four cases; no PDE evolution or manuscript mutation.
- leading_u.csv, exact_uv.csv: numeric budgets.
- A/B/C/D_leading.npz: signed leading spatial arrays.
- verification.json: source hash, all case settings and algebra/RHS checks.

An initial validation caught an incorrect diagnostic class selection (SDModel used for FD); corrected to FDModel. Final outputs and verification are regenerated with the correct native class and assert all checks below 1e-8.
