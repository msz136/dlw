# DLW initial-rate and final-field comparison

**Current edition (2026-10-25):** Current selection: A/D/Gaussian/Sinusoidal, displayed as One-soliton/Two-soliton/Gaussian/Sinusoidal. Current two CSVs each have 12 records; the report checks 48 error values and 16 minima. The preceding six-case artifacts are preserved under ../spatial_figures_four_cases_20261025/before_report/.

Updated 2026-10-25. Reader: `../../../Report.html`.

## Selected comparison

The active report compares Endpoint-SD, Centered-SD and FD on soliton cases A and D, periodic Gaussian initial data and sinusoidal initial data. Centered-SD is the natural physical-field representation now defined in manuscript Section 3.2:

    v_k = Delta_h Z_k = Delta_h u_k + 2(omega_k+omega_(k-1))/h.

The numerical implementation evolves u and w=4omega/h. Its equivalent edge map is v=Delta_h u+M_-w, and its first equation retains h^2 A(w), A(w)=w^2/32-w/4. The lower auxiliary trace is initialized from the continuous v-u_y and then evolves by its equation. The normalized code variable and manuscript omega describe the same system.

Table 1 gives the initial u_t,v_t defects. Table 2 gives the final u,v errors under common RK4, h=dx=.1, dt=1e-4, T=.01, a=2 and lambda=-2. All methods use unfiltered Fourier differentiation in x and the same continuous initial and boundary reference data. Errors are sampled maximum absolute values at each field's native positions. Endpoint-SD and Centered-SD use edge v; FD uses nodal v.

The soliton regions are |x|<=R, |y|<R, with R=5,30 for A,D. Gaussian and sinusoidal cases use periodic x in [-96,96), y in [-2,2], and measure all x nodes and native field sites |y|<=1.8. Their initial fields are u0=A sin(pi(y+2)/4)F(x), v0=4-3u0_y, where Gaussian A=.05 and F=sum_j exp(-((x+192j)/6)^2); sinusoidal A=.03 and F=cos(pi*x/12).

## Data and verification

- `natural_selection_20261025/initial_results.json`: six natural Centered-SD initial-rate records, with an independent verification of the physical-rate formula.
- `natural_selection_20261025/results.json`: the six existing natural-field terminal records, renamed Centered-SD for the selected comparison. Their original state files and provenance remain in `natural_edge_rk4_20261024/`.
- Endpoint-SD and FD initial soliton records remain in `../spatial_audit_20261023/separated/reconstruction_probe/rerun_20261024/baselines.json`. Their terminal soliton records remain in `rk4_spatial/results.json`. Non-soliton records remain in `nondegenerate_rk4_20261024/`.
- The continuous Gaussian/sinusoidal reference is the full two-heat/Laplace construction in `../reference_certificate_20261024/nondegenerate_benchmarks/PROOF.md`. The stored reference values have absolute error below1e-13, including analytic truncation and arithmetic effects. The natural-field reference arrays are compared with the certified arrays at identical native coordinates.
- `build_report.py` creates two 12-record CSVs and root Report.html. `validate_report.py` verifies 48 displayed values, bold minima, CSV ordering, links, retained baseline and natural terminal values, source/artifact hashes and the unchanged manuscript during this task.

```powershell
python Workspaces/dlw_paper_20261009/report_refresh_20261024/build_report.py
python Workspaces/dlw_paper_20261009/report_refresh_20261024/validate_report.py
```

Report-only runs preserve the currently authorized manuscript hash recorded in `natural_selection_20261025/report_preservation.json`; the 2026-10-25 integration advanced that hash and preserved the prior manifest. It leaves the earlier `preservation.json` intact. The report uses local static KaTeX; layout validation is structural rather than browser-based.

## Preserved earlier comparisons

`natural_selection_20261025/before_update/` preserves the previous report, builder, validator, CSVs and README. CSD0 and the previous full-potential Centered-SD data remain in their original directories. All earlier six-case, four-case and compatible-reference archives remain available. The active tables use only the selected Section3.2 Centered-SD definition.

## Illustrated prose and figures

The English draft is `../../../report/dlw_numerical_text_20261025.html`, with 16 figure groups for A/D/Gaussian/Sinusoidal. Initial derivatives have only a diagnostic table. Terminal physical-field plots retain the 2D heatmaps and add separate and overlaid 3D errors. Current publication sources and checks are in `../spatial_ad_uv_20261025/`; stored numerical arrays remain in `natural_selection_20261025/`. The archived old time-comparison table remains in `../manuscript_integration_20261025/`.
