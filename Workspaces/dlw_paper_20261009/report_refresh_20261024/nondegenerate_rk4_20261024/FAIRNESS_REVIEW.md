# Nondegenerate Gaussian/sinusoidal benchmark: independent review

Date: 2026-10-24. Independent review of the analytic construction, initial data, four spatial right-hand sides and comparison settings. All eight saved terminal arrays pass the independent checks below; terminal reference certification is maintained separately.

## Continuous solution and initial derivatives

Both cases use a=2 and the full continuous DLW equations

    u_yt = -v_xx - [(u+4)u_y]_x,
    v_t  = -u_xxy - [(u+4)v-4u]_x.

With z=y+2, kappa=pi/4, the common initial definition is

    u0 = A sin(kappa z) F(x),  v0 = 4-3u0_y.

The Gaussian has A=.05 and F=sum_j exp(-((x+192j)/6)^2); the sinusoid has A=.03 and F=cos(pi x/12). Direct integration of the first equation from the lower boundary and substitution into the second give

    ut(0) = 3uxx-(u+4)ux,
    vt(0) = -uxxy+3[ux uy+(u+4)uxy].

The lower boundary u=ut=0 holds at y=-2. The coefficient 3 is not a permanent relation: (v-4+3uy)_t=8uxxy at t=0. The previous compatible Cole-Hopf solution with v=4-uy does not solve this new initial-value problem.

The new reference in `../../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md` uses F_t=-F_XX, H_t=H_XX, psi_X=FH, psi_t=FH_X-F_XH and X=x-4t. The Laplace transformation supplies the physical fields in (N4). Substitution of u=-2U* and v=4+4P*-2U*_z into the BLP equations gives both full DLW equations with the displayed signs and translation. The reference formulas do not divide by F or s_z, so the auxiliary zero sets cause no physical singularity.

The analytic review finds the denominator estimates and Fourier/Taylor tail argument consistent with their stated domain. In particular Re[(i xi-sC)^2] is at most |s|^2 C^2, which justifies the complex-parameter heat bound. The Gaussian quasi-periodic zero mode psi_0=(FQ)_0/C, and the separately evolved sinusoidal zero mode, are essential parts of the full solution. At t=0 these formulas give D=-psi^2 and exactly recover the prescribed fields. The closed formulas are smooth, and satisfy the strong-solution conditions of the cited uniqueness proof.

An independent execution of the supplied symbolic Laplace identities and Arb constant calculation passed. The lower bounds are psi>0.66061799 and |D|>0.41996381; the propagated physical truncation bounds of the original M=48,K=128 evaluator are below 2.565e-51 for u and 2.598e-48 for v. Source hashes and complete interval results are recorded in `analytic_source_audit.json`. The faster sampled evaluator uses its own truncation settings and requires its separate certificate.

The analytic formulas also supply the necessary ghost values at y=-2.1 and 2.1 and Endpoint edge values at y=-2.05. The bounds only use |s|<=.025 and |s_y|<=.02, which hold for every real y. Consequently the same denominator and truncation estimates extend to these positions without changing their constants.

This is an independent analytic review and executable checking of a proof draft, rather than formal verification. A numerical comparison against binary64 reference arrays additionally needs a bound on those arrays' evaluation and conversion errors; the analytic truncation bound alone is not that bound.

## Alignment of the four numerical methods

All eight runs use h=dx=.1, dt=1e-4, classical RK4 and T=.01. The x interval is periodic [-96,96), with 1920 nodes. The nodal y interval is [-2,2], with 41 nodes. The same Fourier x operators are retained, including a zero first-derivative Nyquist multiplier and no filtering or dealiasing. Errors use every x node and each field's native sites with |y|<=1.8.

- Endpoint-SD evolves u,v directly; v is on the lower half-shifted edge grid. Its lower ghost and lower u_t come from the same continuous solution.
- CSD0 evolves nodal u,v and reconstructs w=v-delta_0u internally. It retains the previous centered physical-field definition.
- Current Centered-SD evolves u,w and reconstructs v at interior edges through the full-potential map. Its initial lower trace is w0=v0-u0_y=4-4u0_y; the other initial w values solve the map against the same prescribed physical v0. All w nodes subsequently evolve by their equation.
- FD evolves nodal u,v directly. CSD0 and FD retain the shared upper ghost rule: continuous background plus quadratic extrapolation of the numerical departure. CSD0 applies its differentiated closure consistently when reconstructing v_t.

The current Centered-SD state and the CSD0 state are intentionally distinct, and the runner's displayed method labels select their respective implementations. Final-time results are total physical-field errors under the stated common time integrator, not pure spatial truncation errors.

## Independent initial checks

`audit_saved.py --initial` reads the eight saved initial states without importing the runner. It independently implements the exact initial derivatives and all four spatial RHS formulas, including the full-potential pushforward and the CSD0 ghost derivative. The largest RHS difference is 4.303e-15 and the largest reference-derivative difference is 5.552e-17. See `independent_initial_audit.json`.

For Endpoint-SD the initial v_t errors reproduce the new benchmark's independent first-order-defect experiment: 6.0376806e-5 for Gaussian and 2.8333562e-5 for sinusoidal at h=.1. The new data therefore do not have the identically vanishing leading Endpoint v coefficient of the previous compatible family.

`certify_initial.py` separately encloses every stored initial u,v,u_t,v_t reference value using 80-digit Arb arithmetic at the exact binary64 sample coordinates. All 2,511,360 stored values have absolute error below 1e-13, including evaluation and conversion errors. The largest outward enclosure is below 7.258e-16. The infinite tails of the periodic Gaussian and its first two x derivatives are explicitly included and bounded by 1e-990. See `initial_reference_certificate.json`.

## Independent terminal-state checks

`audit_saved.py` checks the eight saved terminal states without importing the runner. Every run reaches T=.01 with the stated common parameters. The state and recorded source hashes match. Recomputing the two table maxima on the stated native field grids gives exactly the saved results; independent reconstruction of the current Centered-SD physical v also agrees exactly. Initial lower w traces differ from 4-4u0_y by at most 8.882e-16. The checks are stored in `independent_saved_audit.json`.

This saved-array audit does not independently rerun the complete trajectories. It verifies the stored data, initial RHS implementation, physical reconstruction, comparison grids and error extraction. The absolute reliability of the terminal comparison depends additionally on the all-grid continuum-reference certificate.
