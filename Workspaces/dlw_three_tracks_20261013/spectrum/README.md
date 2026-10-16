# 1B — DLW error-field Fourier / wavelet diagnostics

This directory analyzes genuine snapshots of the existing DLW paper's Case A
and Case C solvers. It does not generate substitute test data. The shared
generator and its source notebook are recorded in `../shared/`; the analysis
manifest records every input file's SHA-256 checksum.

## Reproduce

From `C:\Users\msz\aca`:

```powershell
python Workspaces/dlw_three_tracks_20261013/spectrum/analyze_error_fields.py
python Workspaces/dlw_three_tracks_20261013/spectrum/build_findings.py
```

Optional arguments: `--skip-animation`, `--input-dir PATH`, `--output-dir PATH`.
Existing outputs are regenerated; no input or solver file is modified or deleted.

NumPy, SciPy, Matplotlib and Pillow use the existing Python 3.13 environment.
The user explicitly authorized an isolated PyWavelets installation:

```powershell
python -m pip install --target Workspaces/dlw_three_tracks_20261013/spectrum/vendor --no-deps PyWavelets
```

The installed wheel's distribution metadata reports **PyWavelets 1.10.0**.
Its own generated `pywt/version.py` reports **1.8.0**. Both values and the import
path are preserved in `out/manifest.json`; this is an upstream wheel metadata
inconsistency, not a second global installation. The local module successfully
computes Morlet transforms. No other package was installed or upgraded.

## Data and scope

- Six data sets: A/C × SD RK4, FD RK4, SD RK4 with half the time step.
- 21 snapshots over `0 <= t <= 0.01`; native spacing `dx = dy = 0.1`.
- A uses 101 x-nodes × 100 staggered y-nodes, C 601 × 600. Actual coordinates
  and spacing are read from the archives and recorded in the manifest.
- The fields are native physical `u,v`. Error is numerical minus the continuous
  exact reference on exactly those nodes, not an interpolated plotting grid.
- These are open-boundary line-soliton experiments, not a periodic Hamiltonian
  phase space. The finite-window Fourier transform is a diagnostic transform.
- `t = 0` is retained. Frequencies and peaks are undefined when the entire
  error is below `100 eps_machine max(1, max|reference|)`.
- The time-step comparison checks temporal contamination at this grid and this
  short time. It establishes neither spatial convergence nor long-time stability.

## Fourier definition

For a frame `e[j,i]`, let `w = hann(ny) outer hann(nx)`, `N = nx ny`,
`mu = sum(w e)/sum(w)`, and `Uw = mean(w^2)`. We calculate

```
G = fft2(w * (e - mu)) / N
P = abs(G)^2 / Uw
kx = 2 pi fftfreq(nx, dx)
ky = 2 pi fftfreq(ny, dy)
```

The displayed spectrum is two-sided power **per DFT bin**. It is neither a
radially averaged density nor an inverse-scattering spectrum. The exact discrete
identity is

```
sum(P) = mean((w * (e-mu))^2) / Uw .
```

The correction removes the mean-square attenuation of the window in a standard
way; it does not make windowed power identical to unwindowed physical error
energy for a localized deterministic field. Both raw RMS error and corrected
window power are saved separately. Parseval is asserted to relative tolerance
`1e-12` for every frame, both with Hann and with a rectangular window.

The dominant bin is selected in the half-plane `ky > 0` or `ky = 0, kx > 0`
to avoid reporting an arbitrary member of the real-field conjugate pair.
The self-conjugate Nyquist row/points of even grids are explicitly included.
The high-frequency band is `|kx| >= pi/(2 dx)` **or** `|ky| >= pi/(2 dy)`.
The rectangular-window diagnostics are retained under `raw_*` columns so
finite-window leakage can be assessed rather than misidentified as radiation.
Zero-padding is not used: bin spacing is exactly `2 pi/(nx dx)` and
`2 pi/(ny dy)`; spectral resolution differs between Cases A and C.

## Wavelets

The 2D Fourier transform is complemented by a 1D continuous wavelet transform
of the **common native row closest to y = 0**, for both physical fields. This
fixed policy avoids choosing a different most favorable section for each method.

- PyWavelets complex Morlet `cmor1.5-1.0`, FFT convolution method.
- 64 geometric scales from 4 cells to `min(nx/3,128)` cells.
- The section is demeaned; it is not multiplied by Hann.
- The vertical coordinate is the physical wavelength returned by
  `1 / scale2frequency(wavelet, scale) * dx`.
- The plotted scalogram is `|CWT|^2 / scale`; it has no claimed Parseval
  normalization and is not directly comparable to a Fourier bin value.
- At each scale, points closer than `sqrt(2*1.5) * scale * dx` to the x-window
  ends are shaded. This is an e^-2 Gaussian amplitude influence margin, not an
  exact compact support. Peak summaries exclude those shaded points.
- The shortest displayed wavelength is four cells. Features at that lower
  cutoff deserve caution; no subgrid feature is resolved by this analysis.

This is a section-wise wavelet diagnosis, not a full 2D wavelet decomposition
or a scattering calculation.

## Local extrema and extended structures

The peak table contains signed **grid extrema**, not counts of distinct solitons:

1. Apply a `5 x 5` maximum filter separately to `e` and `-e`.
2. Retain values at least `0.25 max|e|` and above the roundoff floor.
3. Exclude two grid cells at each boundary. Collapse an exactly flat connected
   plateau to one representative; save up to 64 strongest extrema of each sign.
4. Independently label 8-connected components of `|e| >= 0.5 max|e|`, requiring
   at least four cells. Save their physical centroid, covariance axes,
   aspect ratio, orientation, and boundary contact.

Aspect ratio >= 3 is labeled an elongated excursion. These thresholded
components are also not soliton counts. A single coherent line ridge can
produce many grid extrema; sign changes and threshold gaps can split one
underlying deformation into several components. The tables deliberately call
these `extrema` and `excursion_components`. No identities are assigned across
time, so persistence of a colored peak is not asserted as a tracked object.

`threshold_sensitivity.csv` repeats the component diagnosis at 0.35, 0.50,
0.65 of frame maximum. Changing component count with threshold is expected.
`dt_refinement.csv` compares the complete error field, dominant Fourier bin,
normalized power distribution, global absolute-peak coordinate and central
section wavelet maximum after halving `dt`.

## Outputs

| File | Meaning |
|---|---|
| `out/*_fourier.png/.pdf` | Final exact u,v; signed error; 2D Hann power |
| `out/*_wavelet.png/.pdf` | Final reference/numerical central sections, signed error, Morlet scalogram |
| `out/*_error_evolution.gif` | 21 frames; exact field, error, spectrum; fixed color scales; physical time label |
| `out/error_diagnostics_summary.png/.pdf` | Error RMS, high-frequency fraction, spectral width versus time |
| `out/spectral_metrics.csv` | Both fields, every frame, all six solver archives |
| `out/local_extrema.csv` | Signed grid-local extrema samples with coordinates |
| `out/excursion_components.csv` | Spatially connected high-error structures and aspect ratios |
| `out/threshold_sensitivity.csv` | Final component sensitivity to three thresholds |
| `out/dt_refinement.csv` | SD baseline versus half-dt checks |
| `out/*_spectral_data.npz` | Full final error, physical k coordinates, rectangular/Hann power, CWT data |
| `out/manifest.json` | Input hashes, package/runtime versions, numerical checks and endpoint metrics |
| `out/endpoint_summary.csv`, `FINDINGS.md` | Compact endpoint table and interpretation, generated by `build_findings.py` |

The animation uses separate scales for the distinct physical quantities, each
held fixed across **all times of the same animation**. A/C and SD/FD animation
color levels are not shared: compare numeric color bars or the summary table,
not apparent color saturation between different GIFs.

Independent review checked the final spectra against the input fields. The
largest Hann Parseval relative residual over all 252 field-frames is
`1.390e-15`. A separate synthetic calibration, excluded from all experiment
figures and tables, checks a known 2D Fourier mode, a self-conjugate Nyquist
mode, and a Morlet signal of wavelength 2 (recovered 1.972 on the discrete
scale grid). The main script's own SHA-256 and all six input hashes are checked.
Manifest JSON is strict: undefined zero-error diagnostics are `null`.

## Interpretation boundaries

A local Fourier or wavelet peak establishes spatial frequency localization.
It does not establish an additional discrete eigenvalue of a Lax operator.
The error can include phase displacement, profile deformation, boundary
effects and spatial/time discretization error. It is not legitimate to call
these features "ghost solitons" without a compatible scattering problem,
new discrete eigenvalues and their persistence under domain/grid refinement.

## Visual design / inspection

The plot-is-all-you-need skill was used. Its references
`oa-geo-bg-21-811-2024-f02` and `oa-geo-tc-20-5365-2026-f06` were inspected:
we borrow aligned scalar-field panels, individual physically labeled color
bars, a zero-centered diverging error map, and consistent coordinates.
The actual field/Fourier/wavelet combination is a task-specific scientific
layout, not a copied application figure. Figures are PNG 300 dpi plus PDF.
No research data or generated image was added to the skill's public gallery.
