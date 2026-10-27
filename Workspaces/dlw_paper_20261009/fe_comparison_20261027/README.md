# DLW FE spatial comparison and TeX-to-HTML synchronization

2026-10-27. **Current status: FE withdrawn from the main manuscript at the user's request.** The full four-method paper is preserved at `../../../report/dlw-paper-add-fem.html`. Main `../../../dlw-paper.html` again contains the three original methods, with the TeX synchronization retained. Focused FE reading copy: `../../../report/dlw_fe_comparison_20261027.html`. All results below remain valid records of the archived comparison. `withdrawal_validation.json` verifies the separation; print rows are independent. Do not automatically republish FE into the main manuscript.

## Formulation

FE is a transverse, continuous P1 approximation with cellwise constant tests for the first equation and continuous hat tests for the second. Fourier differentiation in x is unchanged. Integrating the first equation gives exactly the FD trapezoidal relation. For the second equation, M v_t = -D_x B(u,v) - D_xx C u, with M_ij = integral phi_i phi_j, C_ij = integral phi_i phi_j', and B_i = integral phi_i ((u_h+2a)v_h-4u_h). All element integrals are exact; the consistent mass matrix is solved without lumping. Endpoint hats have half support. No y ghost is introduced for FE. Only the lower u_t is prescribed, from the same continuous reference as FD. FD retains its existing upper ghost closure; identical parameters do not imply identical boundary operators.

Initial fields, native nodes, domains, a=2, h=dx=.1, RK4 dt=1e-4, T=.01 and evaluation masks match FD exactly (checked against saved FD states). Cases A/D/Gaussian/Sinusoidal are unchanged. These are computed errors against existing continuous references, not a new FE convergence theorem.

## Results and validation

- `run_fe.py`: main four FE runs, raw full-domain states and initial rates in case `.npz`; summaries in case `.json`.
- `check_fe.py`: independent Gauss quadrature of mass/derivative/product loads, constant/linear reproduction, initial first-equation equality with FD, four half-time-step runs.
- `validation.json`: same FD nodes/initial states; recomputed native maximum errors; half-step trajectory discrepancies. Largest relative discrepancy is 0.001055 (0.106%) of the corresponding measured main-run error.
- FE final v errors are 1.81058e-5, 2.58430e-5, 6.11963e-9, 2.85596e-9, smallest among these four methods on these four tests. Final u minima: FE/A, FD/D, Endpoint-SD/Gaussian and Sinusoidal.
- `plot_fe.py`: derives four-method section/heatmap figures from existing saved three-method arrays plus FE. Purple dashed FE errors preserve visibility of overlapping FD curves. No prior method values are changed. Source/reference arrays and exact-section evaluation follow the existing plot pipeline.
- `layout_validation.json`, `algorithm.png`, `table.png`, `figure_review.png`: HTML assets, rendered mathematics, table fit and visual checks. Fourteen figures/eight tables retained; Tables 2/3 each now have four method groups with unrounded minima determining bold.

## TeX synchronization and publication

`before.html` is the pre-task manuscript backup. `tex_sync_source.tex` captures the source TeX at synchronization. `sync_tex.py` brought back revised Figure 9/10 prose, before-figure narratives, Figure 13/14 captions and all 14 updated figures. `tex_sync.json` records the changes. `publish.py` adds FE only to the numerical formulation and spatial comparison; `finalize.py` applies final corrections, refreshes split print panels and creates the focused reading copy. The TeX and existing PDFs were not regenerated or edited. HTML is the active manuscript for this round.

The initial synchronization and publication scripts intentionally reject a second application. Do not rerun historical conversion/publication scripts over the active manuscript. Old numerical data and the independent time/mesh/perturbation experiments remain intact.
