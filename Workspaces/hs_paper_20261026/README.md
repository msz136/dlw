# 2HS numerical manuscript — 2026-10-26

Reader entry: `../../2HS paper.html`. English manuscript, numerical study of the existing Hori–Tanaka–Maruno–Ohta integrable semi-discretization. No new integrability or continuous stability theorem is claimed.

## Reproduce

From the workspace root, run:

1. `python Workspaces/hs_paper_20261026/run_paper.py`
2. `python Workspaces/hs_paper_20261026/mesh_evolution.py`
3. `python Workspaces/hs_paper_20261026/error_maps.py`
4. `python Workspaces/hs_paper_20261026/figures/redraw.py`
5. `python Workspaces/hs_paper_20261026/verify_formulas.py`
6. `python Workspaces/hs_paper_20261026/case_figures.py`, then `python Workspaces/hs_paper_20261026/build.py`
7. `node Workspaces/hs_paper_20261026/render.cjs`
8. `python Workspaces/hs_paper_20261026/validate.py`

Requires the existing NumPy/SciPy/Matplotlib/SymPy/BeautifulSoup environment, Node and the local KaTeX package. Numerical source modules are `../hs_numerics_plan/hs_exact.py`, `hs_solver.py`, and `hs_fixed.py`; their SHA256 hashes are stored in `data/results.json`. `verify_formulas.py` is a preserved copy of the existing exact rational and symbolic validation, rerun here. All new output is kept in this project and the requested root HTML. Existing DLW manuscript is unchanged.

## Protocol and evidence

- Continuous normalization, tau formulas and the two moving vector fields are stated explicitly in the manuscript. Soliton parameters: c=1, p=(5) and (1.1,1.25), zero phase/shift. T=0.25. Reciprocal labels [-4,4]; fixed physical domain [-4,4].
- Spatial runs: a or dx=0.04,0.02,0.01, RK4 dt=0.0005, continuous initial fields. Finite-lattice exact model comparisons are separate, without numerical evolution.
- Temporal runs: exact lattice initial/boundary data, a=0.02, Euler/RK4/trapezoid dt=0.025,0.0125,0.00625. History figures use dt=0.0025. No rejected steps in main runs.
- Density is a cell mean on moving meshes and a point field on fixed meshes. The manuscript discloses this and the one-sided vs two-sided boundary closure. No universal ranking is inferred from the distinct settings.
- Mesh snapshot: 401 points; monitor is evaluated at T=0.25; measures representation only. Mesh evolution: 201 nodes, gamma=0 or 2, initial monitor on 8001 labels, cell mass fixed, ordinary moving equations actually integrated. Common-point metrics include interpolation and are separate from native metrics.
- Perturbations: velocity-only, epsilon=1e-6, identical initial positions and density, each method vs its own baseline. Matching labels on moving meshes and matching positions on fixed meshes. Two backgrounds × three methods, with amplitude/time-step-halving checks. These are numerical finite-time responses, not a continuum stability certificate.
- Heatmaps interpolate native absolute error magnitudes for display; maxima in tables are measured at native nodes/cells. Independent color scales are declared in captions. Raw maps are saved as NPZ.
- Numerical observations: first-order SD continuum approximation; second-order direct FD refinements; two-field improvement under curvature-adapted initial labels in both selected cases. Exact algebra checks support the RHS identity; empirical refinement rates are not presented as general convergence proofs.

## Figure design

Reference: user-approved DLW time-error plots, `../dlw_paper_20261009/time_samm_20261025/figures/time_error_u.png`. Same restrained blue/orange/green palette and compact multi-panel layout. Numerical field samples use symbols against black exact curves; error and response plots use lines only. Since 2HS has one physical spatial coordinate, heatmaps show x–t evolution rather than an artificial x–y slice. Each figure has PNG and vector PDF. No gallery ingestion.

Current main paper: 10 numbered main figures without heatmaps or expandable supplements, 9 case-separated tables numbered consecutively 1–9. Exact profiles and spatial comparison curves use T=0.125; terminal tables remain at T=0.25. New midpoint runs and temporal maps are saved in `data/case_figures.npz`. Spatial heatmaps and the standalone mesh interpolation experiment are retained on disk but omitted from the main paper. Mesh discussion fixes the moving FD formulation and compares uniform versus curvature-adapted initial labels; it does not mix SD changes into the adaptation comparison. Table grouping uses merged case/method cells. `case_layout.py` builds case-specific explanations and blocks. The conserved-cell-mass derivation and the curvature monitor's purpose are developed separately in Section 3.4.

Table cleanup: spatial spacing cells explicitly name a or Δx; adaptive-mesh tables 6/7 bold the minimum of each of the four error columns within each case. Removed temporal maps remain on disk.

2026-10-27 scope revision supersedes earlier layout counts: Section 4.2 displays integrable SD versus FD only; exact-lattice table removed. Section 4.4 compares fixed, natural moving and adaptive moving FD at 201 nodes with RK4. Run `fd_mesh_comparison.py` before `build.py` to generate these assets/data. Current counts: 10 figures, 8 tables; spatial minima and common-point mesh minima bold. Source datasets for removed comparisons remain available.


## Current conserved-density mesh revision (2026-10-27)
Supersedes all previous mesh protocols above. Sections 3.4/4.4 now use only fixed uniform FD and Rm=(u_xx+2)/(2 rho) moving FD. Both use the same three-point ALE field stencils, nodal rho, Poisson recovery and exact two-sided boundary values on fixed physical endpoints [-4,4]. Interior moving nodes follow Qm/Rm. Parameters: 201 nodes, RK4 dt=.0005, T=.25; common 2001 evaluation points in [-2.5,2.5], linear reconstruction. Initial m is D2(u_exact)+2; exact analytic tau derivatives provide boundary m and initial equidistribution density. Equal-mass continuum motion applies to interior material cells; fixed endpoint closure is stated explicitly.
Run `python conserved_mesh.py`, then `python build.py`, `node render.cjs`, `python validate.py`. This imports the established ALE primitives from ../hs_conserved_mesh_20260925/run_mesh_comparison.py and replaces its one-soliton reference with analytic tau derivatives supporting both current cases. Data: data/conserved_mesh.json and .npz; figures/conserved_mesh_0 and _1 PNG/PDF. Errors decrease by 34.0%/29.0% for one soliton and 42.0%/42.9% for two solitons (u/rho). All sampled grid widths, rho and Rm positive; dt-halving terminal differences below 1.6e-14. Analytic u_xx independently checked against centered differences (max 1.8e-8). These are measured errors for the stated cases. Current manuscript: 10 figures, 8 tables, 127 rendered formulas. Old data and manuscript sources remain archived. Plot layout: approved three-panel widths/u-error/rho-error; blue solid fixed vs orange dashed moving, no smoothing.


2026-10-27 nodal-error revision supersedes the reconstruction metric above: retain 201 actual nodes, evaluate exact fields at each final node, plot connected raw nodal errors and tabulate their maxima within [-2.5,2.5]. No field interpolation or smoothing. One-soliton fixed/moving u=3.050536e-6/4.485635e-6, rho=2.604896e-5/1.530503e-5; two-soliton u=1.318234e-5/9.815137e-6, rho=6.181527e-5/3.216622e-5. Thus density improves in both cases; velocity improves only in the two-soliton case. Previous 201-node reconstruction and exploratory 2001-node runs are archived in archive_mesh_201_reconstruction and archive_mesh_2001_nodes. Initial equidistribution still uses inversion of accumulated monitor mass; this does not interpolate evolved field values.

2026-10-27 refinement update: user selected 2,000 intervals/2,001 actual nodes for the mesh experiment. Reused completed archived 2001-node runs and verified NPZ maxima against JSON, preserving 201-node nodal results in archive_mesh_201_nodal. Figure/table protocol remains direct nodal errors at T=.25, dt=.0005. data/mesh_refinement.json compares all eight errors: factors 99.316–101.078 for tenfold interval refinement, observed orders 1.997–2.005; rankings unchanged. Main table/figure assets now use 2001 nodes.

1000-node check: check_1000_nodes.py uses exactly 999 intervals, same T=.25 and RK4 dt=.0005 with halving check. data/mesh_1000_nodes.json/.npz retain actual-node errors. Rankings unchanged from 201/2001 nodes; errors approximately four times the 2001-node values; terminal halving differences below 1.3e-13. Main paper remains at 2001 nodes.

Density exploration 2026-10-27: report/hs_density_search_20261027.html (workspace report directory), density_search.py/report.py, data/density_search/. Scanned diluted Rm at exactly 200/1000/2000 nodes, energy monitor and mixtures. Candidate R=1+.1(Rm-1)-.07E, E=u_x^2-c^2(rho^2-1), Q=.1Qm-.07QE, QE=-uE-4u^2+2c^2u. Same coefficients improve all four target metrics at each resolution; one-soliton gains only .2-.4%, two-soliton about7-18%. Time halving and doubled initial mass quadrature checks preserve gains. Frozen-parameter holdouts p4 fail both, p6 fails u, (1.12,1.28) improves both. Exploratory selected parameter, not universal superiority; main manuscript unchanged. All trial JSON retained.

Natural-density follow-up: user rejects fitted .1/-.07 monitor. natural_density_search.py tests nine untuned candidates plus fixed baseline at 200/1000/2000 nodes, 60 runs; none improves all four metrics. Includes rho, deficit, normalized momentum and its deficit, energy, Rm, R2=(m²-c²rho_x²)/(4rho³), and two Riccati branch representatives (m±c rho_x)/(2rho). R2 flux -uR2+c²(1/rho-1) symbolically verified. Report: ../../report/hs_natural_density_20261027.html; data/natural_density_search/*.json. Fitted monitor remains exploratory archive, not endorsed manuscript replacement.

## Three-density SAMM section (2026-10-27)
Current LaTeX Section 5 introduces rho, Rm and R2, derives their local fluxes and compares all three with fixed FD. N=2000 actual nodes; 16 runs including time-step-halving checks. Updated PDF 18 pages, 10 figures, 8 tables. See `samm_three_20261027/README.md` and validation.json. This supersedes the two-method mesh protocol for the LaTeX paper; source HTML is unchanged.
