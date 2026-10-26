# DLW revision, 2026-10-18

Checkout: C:/Users/msz/aca; origin ssh://git@github.com/msz136/dlw.git; branch main; HEAD 0a9a21a7c87cdc2b58db554833c1de5427c232ba. Target HTML and manuscript were clean before revision. Existing index/progress changes and archive deletions were retained. No commit, push, OPD action, or numerical simulation.

## Changed files
- report/dlw_paper_draft.html: revised English and Chinese paper.
- Workspaces/dlw_paper_20261009/manuscript.md: synchronized editable source.
- PROGRESS_LOG.md: merged update into existing DLW paper entry, preserving previous entries.
- This directory: before copies, formula-number mapping, revision scripts, checks and screenshots.

## Paper changes
- Section 2.5: same-spectral-parameter exact-family leading difference (Proposition 2.9); midpoint y=(j+1/2)h; Appendix A derives general-N tau coefficients by principal minors. Darboux theorem is now 2.10. Fixed N, regular spectra, compact region, nonvanishing tau and required derivative bounds are stated.
- Section 3.1: independent three-point D1/D2 expansions; cumulative PE/FD u rates; method-specific B_h at fixed h and common B in the joint limit. These are interior rate defects, with lower-boundary reconstruction and a separate wrap mismatch.
- Section 3.4: numerical deviation from the semi-discrete exact solution, initial/boundary mismatch, uncentered direction cosine and L2/RMS squared-norm identity; max errors remain total max errors.
- Appendices B/C retain full Gram auxiliary and Darboux calculations; D retains cumulative reconstruction/PF initialization; E retains mapping derivatives; F retains C–N and the complete time comparison. The elementary Euler update is replaced by method name and reference [10]. Main spatial/mesh comparison tables remain. Previous Table 2/Figure 5 are Table F1/Figure F1; previous Table 3/Figure 6 are Table 2/Figure 5.
- Explicit computation/evaluation domain distinction and actual continuation rules are retained in the main text. No images or numerical values changed.

## Formula evidence
- Existing Gram formula (11), centered extension (60) and amplitude identity (64) in the before source are the primary definitions. Symmetric Taylor reconstruction gives -beta_xyy/4 and u_yyy/6-beta_xyyy/12; substitution 4 beta_xy=v-u_y gives the stated C_U and C_V.
- The principal-minor row/column factors pair on the same index set. rho_i d/drho_i is its indicator, giving alpha2=sum_i (y c_i+d_i)rho_i d_i(alpha) and beta2=y sum_i c_i rho_i d_i(beta), where d_i(alpha) here means partial derivative with respect to rho_i. The unambiguous displayed formulas are in Appendix A.
- Workspaces/dlw_modified_equation_20260926/REPORT.md, section 4: earlier exact-family calculation; rechecked against current definitions.
- Workspaces/dlw_error_mechanism_20261013/sources/LEADING_U_FORMULAS.md, sections 1 and 4: actual cumulative PE/FD rates and x stencils. Current draft equations (89),(90),(95) before renumbering independently reproduce these rates.
- boundary_sampling.py and rerun_buffered.py provide continuation rules and computational domains; neither was executed.
- Reference [10] bibliographic data checked against the authors' page https://www.unige.ch/~wanner/ode_I.html and publisher https://link.springer.com/book/10.1007/978-3-540-78862-1.

## Validation and limits
- verification.json: symbolic phase/amplitude/stencil checks, N=3 independent-minor polynomial check supporting the general subset proof, physical coefficient identities, 776 strict KaTeX math items, 118 numbered displays per language, 290 unique IDs, all internal links and displayed linked equation numbers valid.
- layout.json is the final check on the installed actual HTML: 1440/390px, no document overflow, no KaTeX errors, all 20 bilingual image elements loaded. Equation containers retain existing horizontal scrolling at narrow widths. Screenshots include new Chinese/English formulas and appendices.
- All six existing bilingual tables are DOM-equivalent to the before version; all 20 image elements unchanged. All previous displayed formulas except the elementary Euler update are preserved apart from numbering.
- Printed HTML/PDF editions were not updated.

## Data support
The active buffered_run and comparison_fields directories contain manifest.json, with no saved fields. In particular comparison_fields/manifest.json uses h=0.125, nx=512, dt=0.000125 and therefore is not the current h=dx=0.1, dt=0.0001 four-case comparison. The relevant error-mechanism directories retain analysis sources and scripts but no NPZ/NPY fields; the accessible local Trash contains no archived data. No experiment or data restoration was attempted. Existing maximum-error tables remain supported by their unchanged published values, not a newly rerun reproduction.

A new exact-family decomposition table requires the matching numerical u/v snapshots, x/y evaluation coordinates, time, spectral parameters, per-method mesh/initial/boundary metadata, and consistent interpolation/quadrature weights. Current old RMS/direction tables concern instantaneous rate sources and their propagated responses, and were not repurposed as e_model/e_num field tables. The exact Gram model component could be evaluated independently, but without matching numerical fields the complete table cannot be supplied; no partial or invented table was inserted.
