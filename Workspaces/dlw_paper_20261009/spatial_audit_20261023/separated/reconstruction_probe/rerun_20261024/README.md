# Full-potential Centered-SD rerun, 2026-10-24

Current paper: `C:/Users/msz/aca/dlw-paper.html`.
Reading view: `C:/Users/msz/aca/report/dlw_full_potential_experiments_20261024.html`.

## Scope and measurements

Four continuous soliton references, unchanged parameters and regions. The h scan uses .1/.05/.025 with dx=.1; the dx scan uses .1/.05/.025 with h=.1. There are 20 new Centered records and 40 rerun Endpoint/FD records. All are t=0 physical time-derivative defects. Baselines reproduce the prior total defects.

Tables 2 and 3 now BOTH report complete initial defects, not isolated analytic-x Y and Fourier X contributions. The old decomposition is retained in `../../spatial.json`; it has not been silently copied into the new Centered data. The nonlinear inverse and Fourier primitive make that old analytic-x evaluator inapplicable without further development.

The zero-mean Fourier primitive is fixed for every case; zero/Nyquist multipliers vanish and Dxx J=Dx. U is nodal, V is on internal edges. Initial U,V are common continuous samples, and w is solved from the nonlinear constraint with lower w=v-u_y. All later w nodes, including the lower trace, evolve by their equation. Exact continuous lower U_t supplies the lattice integration constant. Time methods act on U,w, not on U,V directly, and V is recovered by the nonlinear map. This distinction is explicit in the paper.

Twelve time runs use h=dx=.1, dt=1e-4, T=.01, Euler/RK4/CN. All completed. The initial U-defect advantage does not remove the large B final error. No temporal convergence-order claim is made.

## Reproduction

From the parent `reconstruction_probe` directory, run `rerun_20261024.py CASE` for each A–D spatial scan, `rerun_20261024.py CASE time` for time runs, and `rerun_baselines_20261024.py` for Endpoint/FD. `rerun_20261024/update_paper.py` validates results, writes CSVs, updates theory source sections 3.2–3.4, and renders the current paper. It backs up the paper and theory source before writes.

Current numerical manuscript sources are `methods.md` and `experiments.md` in this directory. Do not run the older `separated/build_paper.py` to publish the current paper: it renders the former local Centered representation and old tables. The old source and outputs are retained as historical material.

## Verification

`validation.json` records 60 spatial and 12 time results; maximum Endpoint/new U-defect difference 9.73e-12, reconstruction residual 1.00e-12, first-equation identity difference 8.93e-12, centered chain-rule check difference 9.00e-9, and CN residual below 1e-12. Static KaTeX rendered 333 formulas; numbered equations 1–53, unique HTML IDs and internal links checked. Visual browser inspection was not performed in this run.

The paper's consistency statement is conditional on a smooth inverse branch. Lax coefficients are expressed in U,w; they are not advertised as an explicit local U,V pair. The matched Gram second-order argument is distinct from the common-continuous-initial-data experiments.
