# DLW bounded conserved-density mesh implementation review

## Reuse decision

The earlier single-soliton completion in `dlw_single_aligned_20260929/experiment.py` has a trustworthy common physical u/v initialization and snapshot protocol. Its underlying SD/FD equations are in `dlw_semidiscrete/numerics/lib/parametric.py`, `parametric_open.py`, `solver.py`, and `dynamics.py`. The existing moving-mesh code uses `Dx=J^-1 Dxi` and `Dx²=Dx(Dx)` with a common x mesh across y, which remains the right minimal architecture here.

The old x operator is periodic and the old lower-end mesh pinning uses only `(Q-Qleft)/R`. These cannot be reused on physical x∈[-1,1] without changing the boundary problem: the original solitary fields are not close to their far fields at those endpoints, and Qright generally differs from Qleft. The new experiment therefore reuses the mathematical equations and exact tau expressions, but implements nonperiodic x boundaries and normalized finite-interval mass coordinates in a new file.

## New numerical problem

- Original five cases A–E; a=2, ci=1, zero phases, no parameter scan.
- Physical x,y∈[-1,1]. Common x grid, inclusive fixed endpoints; y remains a fixed midpoint lattice.
- SD advances P=δ−u and W=v−δ0u. FD advances the same P and v.
- Analytic data are supplied at x endpoints and the lowest y layer of u. The lower-y ghost is analytic; the upper-y ghost is the analytic boundary background plus a quadratic extension of the numerical u perturbation from the last three layers. The same closure is used for SD and FD. Interior u/v are never reset or forced toward the exact solution.
- Initial u/v at native nodes are the same continuous physical data across SD/FD. SD's W is obtained from the actual discrete δ0 reconstruction.
- Five-point fourth-order first derivative in computational ξ; centered rows where possible, one-sided rows near either endpoint, no wrapped indices. Physical second derivative is the composed first derivative for both schemes. Composing the one-sided first-derivative rows gives a third-order second-derivative closure near x boundaries; a global fourth-order x claim is therefore not made.
- RK4 evolves fields and mesh positions at every intermediate stage. Moving fields receive the corresponding ALE transport.
- Mesh density is computed from the current numerical u/v. The initial mesh is an equal-density-mass inversion on a dense analytic initial profile, shared by each SD/FD pair.
- Density is averaged using fixed nonnegative weights in the physical y band [-.75,.75]. This band has the same definition after y refinement and avoids imposed ghost-layer terms in the finite-h conservation identities.
- Moving and frozen-density controls have identical initial nodes. The finite-domain velocity subtracts both the left flux and the normalized total-mass correction, fixing both endpoints.

## Matched fluxes

The finite-h SD density fluxes include δ0(H) and Δh(W), rather than inserting the continuous flux formulas unchanged. FD uses its own finite-h flux with δ0(A) and Δh(v). The conservative identities only require the x derivative's linearity, its commutation with the common-y differences, and D2=D1(D1). They consequently remain algebraic identities at interior x nodes for the actual spatial implementation. They do not assert exact conservation of the RK4 trajectory or exact equidistribution under the trapezoidal primitive used by the mesh algorithm.

## Upper-y closure correction

The first 230-run batch used exact u ghosts on both y sides. Independent differentiation of the physical reconstruction showed that an O(h²) accumulated interior u error jumped to a zero ghost error across the top cell; its centered y difference introduced an O(h) term in the top-layer v source. That batch, source, and protocol are preserved in `before_y_boundary_review/`.

The current batch extends the numerical perturbation rather than setting its upper ghost to zero. Its ghost is `u_exact_ghost + 3e_top − 3e_next + e_third`, with e computed from the numerical field and analytic boundary background. This is a shared boundary closure change, not density tuning. The 230 comparisons are regenerated with one frozen source; previous numbers are not mixed into the current results. Independent time differentiation and source-decomposition checks are owned by the separate exact-solution audit.

## Interpretation constraints

1. Dense physical-grid total error includes the initial spline representation error. Native nodal error is reported separately; do not remove the initial dense error from the headline result.
2. A small T does not establish a long-time error bound. Short T is deliberate because the DLW linearization includes high-frequency growth.
3. Refining x or concentrating its nodes may amplify unstable modes. Successful completion alone does not imply controlled field accuracy; inspect time, x, y, and combined controls.
4. Frozen versus moving isolates the added effect of motion. Uniform versus moving includes both initial concentration and motion.
5. The results are actual u/v field errors for these five original examples and this boundary problem. They do not compare arbitrary parameter boxes or claim a globally optimal density.
6. The monitor band is narrower than the evaluation rectangle. Error is still evaluated over all y layers in [-1,1]; the band simply defines one shared x mesh.

## Sources checked

- GSG original `Paper/sources/gsg.txt`, §2 (2.1)–(2.6): positive r=√(1+ux²), rt+(r cos u)x=0 and reciprocal coordinate.
- GSG §4 (4.1)–(4.14): four moving formats and a fixed Crank–Nicolson format. This supplies the comparison logic, not a DLW-specific density or a general convergence theorem.
- `Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md`: local continuous DLW density derivations, finite-h minus density, finite-domain endpoint warning, and common-x mesh restriction.
- `Workspaces/dlw_two_soliton_20260929/reference.py`: positive N=2 four-term tau for original figures 3–5.
- `Workspaces/dlw_paper_cases_20260927/run.py`: the two regular N=1 branches, original a/p/q, zero phases, and independent exact solution formula checks.

The standalone `experiment.py` is the frozen experiment source. Independent verification is performed by a separate agent; this note does not replace that verification.
