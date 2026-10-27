# Three-density SAMM section — 2026-10-27

Current manuscript: `../../../pdf/2hs/main.tex`; PDF 18 pages, 10 figures, 8 tables. Direct LaTeX editing is authoritative for this revision; HTML remains unchanged.

Section 5 replaces former Sections 3.4 and 4.4. Section 4.4 now contains perturbations; Section 6 contains conclusions. Equations 18–25 derive and implement rho, Rm and R2 coordinates. Figures 9–10 and Tables 7–8 compare uniform fixed FD and the three SAMM choices; earlier perturbation figures/tables are renumbered.

Run `python Workspaces/hs_paper_20261026/samm_three.py` for eight baseline runs and eight dt-halving runs. Actual nodes N=2000, domain [-4,4], RK4 dt=.0005, T=.25, nodal maximum error in [-2.5,2.5]. Raw final samples: trajectories.npz; errors and sampled positive minima: results.json. Same ALE stencils, initial m=D2u+2, exact two-sided boundaries, fixed physical endpoints. Conservation-coordinate speed is imposed on interior nodes, not the endpoint cells. Plots connect raw samples and do not interpolate fields.

General-c conservation identities verified symbolically. Error maxima rechecked against NPZ. Maximum halving change 1.133e-12. Refinement uses existing 1000/2000-node natural-density runs; initial Poisson diagnostic uses exact sampled curvature (different diagnostic from the evolution initialization). Reproduce diagnostic with ../density_insights.py; its output is ../data/density_insights/analysis.json. This diagnostic corrects the earlier tentative explanation that poorer final u accuracy follows simply from poorer initial Poisson recovery: Rm and R2 improve that isolated single-wave recovery while worsening terminal u.

Observed conclusions: rho expands cells near the waves and increases both field errors; Rm improves rho in both cases and u in the two-wave case; R2 slightly improves single-wave rho relative to Rm while raising u errors. All four choices retain observed second-order refinement. These are numerical observations for the stated cases, not a universal convergence theorem.

`before_main.tex`, `before_main.pdf`, `before_desktop.pdf` preserve the prior manuscript. `validation.json` records checks. The source assembly program ../update_samm_tex.py reads this backup; do not rerun after subsequent manual edits without merging them.

## Narrative revision
User requested removal of standalone 5.4. Initial-grid diagnostic now follows the one-wave results; refinement and cross-case interpretation conclude 5.3. Abstract, introduction and conclusion incorporate the fieldwise error-coefficient insight. Sections 3–4 expand variable choice, reference selection and perturbation motivation. Formula/figure/table blocks are unchanged. Current PDF 20 pages, 10 figures, 8 tables; desktop synchronized. Backups and layout checks: narrative_revision/. Do not rerun older manuscript assembly scripts over this version.

## Appendices A–C
Current PDF 24 pages. Added correction derivation, nonuniform stencil/recovery details and three supplementary numerical tables, with five targeted body hyperlinks. See `appendices/README.md` and `appendices/validation.json`. Main figures, tables and equations unchanged.

Page 16 layout fix: Figure 9 split at an empty panel gap (PDF y=328), preserving vector content and .88 text-width scale. First two panels follow Table 7 on page 16; lower panel and original caption continue on page 17. PDF remains 24 pages; equations/tables unchanged. Evidence and backups: page16_layout/.
