# Compatible Gaussian/sinusoidal RK4 comparison: independent review

Date: 2026-10-24. Status: parameter, model, initial-reference and saved-array checks passed. Final-time reference certification is recorded separately by the reference-grid implementation.

## Continuous problem and reference

Both new cases use a=2 and the same full DLW equations as the soliton comparisons,

    u_yt = -v_xx - [(u+4)u_y]_x,
    v_t  = -u_xxy - [(u+4)v-4u]_x.

The initial fields are u0=A sin(pi(y+2)/4)F(x), v0=4-u0_y. Gaussian uses A=.05 and the period-192 Gaussian of width 6; sinusoidal uses A=.03 and F=cos(pi x/12). The constant v background is therefore 4. The runner explicitly overrides the historical non-soliton Model value a=1/3 with a=2.

Substitution of v=4-u_y into both full equations gives the reduced equation u_t=u_xx-(u+4)u_x. Thus the positive heat-semigroup Cole-Hopf reference in `../../reference_certificate_20261024/compatible_benchmarks/PROOF.md` is a solution of the full nonlinear equations for these data. The mean-dependent translation Y=x-4t-mu(y)t and its y derivative are included in `reference_grid.py`. The polynomial recurrence, Gaussian Fourier coefficients, and field reconstruction agree with the proof formulas.

The formulas extend smoothly to all real y. The original uniform estimates use |sin|,|cos|<=1 and remain valid outside [-2,2], so the same analytic extension provides ghost values. The experimental computational interval is [-2,2]; reported errors use native field sites |y|<=1.8 and all periodic x nodes in [-96,96).

## Discrete-method alignment

All six evolutions use h=dx=.1, dt=1e-4, classical RK4 and T=.01, with the existing Fourier x differentiation, zero first-derivative Nyquist mode, and no filtering or dealiasing. The three current spatial methods are retained:

- Endpoint-SD advances physical u,v, with backward/open-chain relations and exact continuous lower u data.
- Centered-SD uses the current full-potential formulation with state (u,w). Its lower inverse trace is w0=v0-u0_y=4-2u0_y; the remaining w values are solved from the same physical v0 sampled on its edges. The initialization residual is below 2e-12, with physical reconstruction mismatch below 1e-12. Every w node then evolves by its equation. The first physical equation agrees with the Endpoint midpoint equation to roundoff.
- FD advances physical u,v, with exact lower data and the retained upper ghost rule: analytic background plus quadratic extrapolation of the numerical departure.

Thus RK4, resolution and physical initial fields agree across methods. The actual state variables and boundary formulas remain part of each implementation. The final table measures total physical-field error at T=.01.

## Independent checks

`certify_initial.py` encloses all 940,800 stored initial ut/vt reference values using 80-digit Arb arithmetic at the exact binary64 sample coordinates. The comparison includes floating-point reference evaluation and conversion, and an explicit bound for the periodic Gaussian infinite tail. Both components have uniform sample error below 1e-13. The largest computed outward bound is below 1.55e-17 for Gaussian and 1.37e-16 for sinusoidal. The formulas were implemented independently as

    ut = uxx-(u+4)ux,
    vt = -uxxy+uy*ux+(u+4)uxy.

`audit_saved.py` reloads all six final and initial NPZ files without importing the experiment runner. It recomputes the table maxima on the stated native grids, checks complete evolution to .01 and parameters, verifies artifact hashes, and independently reconstructs Centered physical v from u,w with the spectral primitive. All table differences and reconstructed-v differences are zero. See `independent_saved_audit.json` and `initial_reference_certificate.json`.

The completed all-node reference certificate covers binary64 output conversion, ideal-DFT versus stored-coordinate displacement, analytic truncation, and actual versus nominal final time T=1/100. Every stored initial u,v,ut,vt reference value and final u,v reference value has error below 1e-13; the largest final combined enclosure is below 2.165e-14. See reference_certificate.json and REFERENCE_GRID.md.

## Structural interpretation of this choice of data

The compatibility v=4-u_y also removes the formal first-order h contribution in the Endpoint v flux. At the v edge, the adjacent u average and difference are second-order approximations to u and u_y. The coefficient of h in the flux is

    v^2/4 - 2v - u_y^2/4 = ((v-4)^2-u_y^2)/4 - 4.

On the compatible family it equals the constant -4, whose x derivative vanishes. Therefore the small Endpoint v errors in these two cases are consistent with its general first-order expansion: this particular solution family has a vanishing first-order coefficient. No h-refinement study was performed in this run, so a measured convergence rate is not claimed.
