# DLW three parallel tracks — 2026-10-13

User-facing report: [1A–1C integrated report](../../report/dlw_three_tracks_20261013.html).

## Scope

- **1A conservation/**: new periodic reduced-Hamiltonian experiment; genuine first three inverse-monodromy trace integrals, their discrete diagnostic versions, space/time separation, numerical tables and figures.
- **1B spectrum/**: actual one- and two-soliton errors from the paper's fixed-grid PE and FD methods, Fourier/CWT analysis, local-extrema and ridge diagnostics, animations.
- **1C poisson/**: original physical-coordinate bracket on the periodic mean-constrained manifold, an all-grid Jacobi proof and exact symbolic checks, and an energy-preserving but momentum-breaking counterexample.

The periodic experiments in 1A/1C and the buffered line-soliton computations in 1B have different boundary conditions. No periodic trace invariant is assigned to a divergent whole-plane line-soliton integral.

## Reproduce

From `C:/Users/msz/aca`, using the existing Python 3.13 environment:

```powershell
python Workspaces/dlw_three_tracks_20261013/generate_shared.py
python Workspaces/dlw_three_tracks_20261013/conservation/conservation_experiment.py
python Workspaces/dlw_three_tracks_20261013/poisson/verify_poisson.py
python Workspaces/dlw_three_tracks_20261013/spectrum/analyze_error_fields.py
python Workspaces/dlw_three_tracks_20261013/spectrum/build_findings.py
python Workspaces/dlw_three_tracks_20261013/build_report.py
python Workspaces/dlw_three_tracks_20261013/verify_delivery.py
```

The spectrum script uses the user-approved isolated PyWavelets installation in `spectrum/vendor`; system packages were not upgraded. Its own report records package versions and the installation command.

`generate_shared.py` executes a frozen copy of the required notebook code cells, replacing only the optional IPython display import with a no-op. It does not execute plotting/export cells or write to the original notebook. Baseline endpoints are checked against the previously archived paper states. Existing complete trajectory files are reused.

## Shared trajectory layout

`shared/{A,C}_{SD,FD}_RK4.npz` and `shared/{A,C}_SD_RK4_halfdt.npz` contain:

- `x`, `y`, `t`: physical coordinates and 21 actual output times.
- `u`, `v`, `exact_u`, `exact_v`: arrays ordered `(time, y, x)`.
- `metadata_json`: parameters, source hashes, boundary conventions and sampling details.

These are unfiltered native-grid samples with `dx=h=0.1`, `T=0.01`. Paper tables use a finer interpolated evaluation grid, so sampled maxima need not equal the table maxima. Initial and final full computational states are saved separately as `*_endpoints.npz`.

## Interpretation

Jacobi is proved by a constant bracket and a finite-dimensional coordinate pushforward. Symbolic tests check the implementation; they do not replace the proof. Hamiltonian conservation belongs to the continuous-time spatial system; RK4 introduces a separate time error. Fourier/wavelet peaks characterize the error field and do not establish new soliton eigenvalues.
