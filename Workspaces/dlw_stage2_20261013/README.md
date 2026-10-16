# DLW stage 2: reduction, symplecticity, and error Lax defects

This directory continues the verified stage-1 work in
`../dlw_three_tracks_20261013/`. Source notebooks and the paper draft are read-only
inputs for this exploration.

## Tracks

- `reduction/`: whether evaluation at one transverse coordinate closes; an
  actual invariant family of the original periodic DLW flow and its inherited
  symplectic structure.
- `symplectic/`: variational-map measurements of numerical symplecticity on a
  fixed Casimir leaf of the stage-1 Hamiltonian spatial discretization.
- `error_lax/`: exact off-shell Darboux/Lax residual identities, error equations,
  and the distinction between forced error transport and autonomous
  isospectral evolution.

The physical spatial coordinate is not automatically a canonical momentum or
position of the field phase space. A fixed transverse slice is not automatically
an invariant reduction. The report gives the conditions under which a genuine
finite-dimensional result follows.

Plotting continues the stage-1 scientific figure style through the
`plot-is-all-you-need` workflow. No new package is needed or installed in stage 2.

## Reading

User-facing mathematical report: [integrated HTML](../../report/dlw_stage2_20261013.html).

Six track abstracts, one synthesis abstract, and an accessible account of the
error mechanism: [research abstracts](../../report/dlw_research_abstracts_20261013.html).
The source and offline renderer are in `abstracts/`; this synthesis reuses the
completed experiments and distinguishes same-model phase shear from conditional
continuous-to-semidiscrete comparisons. It adds no new numerical experiment.

- [2A theorem and proof](reduction/report.md): genuine M=2 inherited symplectic
  annulus, fixed-slice obstruction, and explicit elliptic waves.
- [2B experiment and derivation](symplectic/report.md): actual tangent maps,
  midpoint stopping branches, physical-field time errors, and plots.
- [2C forced Lax identities](error_lax/REPORT.md): exact error equations,
  residual-to-spectral-drift formulas, and discrete Leibniz defects.
- [Error mechanism](synthesis.md): phase-aligned orbital bounds and exact
  symplectic shear within the invariant family.
- [Review record](REVIEW.md) and [delivery checks](delivery_validation.json).

## Reproduce

From `C:/Users/msz/aca`, using the existing Python 3.13 environment:

```powershell
python Workspaces/dlw_stage2_20261013/reduction/verify_reduction.py
python Workspaces/dlw_stage2_20261013/symplectic/symplectic_experiment.py
python Workspaces/dlw_stage2_20261013/error_lax/verify_error_lax.py
python Workspaces/dlw_stage2_20261013/verify_synthesis.py
python Workspaces/dlw_stage2_20261013/build_report.py
python Workspaces/dlw_stage2_20261013/verify_delivery.py
```

The mathematical scripts use existing NumPy, SciPy, SymPy and Matplotlib.
The report builder uses existing Python Markdown and local KaTeX through Node.
Validation uses existing BeautifulSoup and Pillow. No installation is performed.

The first track has symbolic and explicit elliptic-profile checks; the second
has actual nonlinear time integration and tangent-map measurements; the third
has exact symbolic identities and rational matrix witnesses. Their results
must not be interchanged with the paper's open-boundary PE/PF experiments.

`baseline.json` records the original notebook, paper and stage-1 file hashes.
`update_records.py` merges this topic into the workspace progress and index.
