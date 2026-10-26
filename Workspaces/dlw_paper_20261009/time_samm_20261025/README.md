# Time integration and moving mesh for the current Centered-SD formulation

> **Status 2026-10-25 (later):** Sections 5.1–5.4 have since been rewritten from a supplied narrative; see
> `../section5_rewrite_20261025/`. `publish.py` here must **not** be re-run: it would restore the earlier
> 5.3/5.4 wording. The data, figures and 4.3/4.2 text it produced remain in the manuscript.

2026-10-25. Data, figures, prose and publication for manuscript Sections 4.2–4.3 and 5.3–5.4.
Stability Sections 4.4 and 5.5 remain placeholders by agreement with the user.

## What was decided

* The time-integrator comparison keeps the published Centered-SD scheme unchanged: Fourier `x` operators,
  natural-edge state `(u, w)` with `omega = h w / 4`, RK4 baseline that must reproduce Section 5.2.
* The mesh comparison uses **mapped centred differences** in the computational coordinate for *both* the
  uniform and the adaptive member, so the only difference is the node distribution. These operators differ
  from the Fourier operators of Sections 5.2–5.3, and the fixed-mesh errors are correspondingly larger.
  The reason is recorded in `_scratch/check_error_sources.py`: with Fourier `x` differentiation, refining
  `h` from 0.1 to 0.05 already reduces the fixed-grid error by a factor of four, so the `x` resolution is
  not the limiting factor there and a redistribution of `x` nodes cannot show an effect. The mapped
  centred operator is also the standard SAMM setting, and it is the only one in which the comparison is
  meaningful.
* The mesh velocity uses the periodic form `V_i = (qbar_i - <qbar>) / rhobar_i`, i.e. the constant in
  `rho V - q = const` is the **node mean of the flux**. This conserves every cell mass, leaves the mean
  displacement zero and keeps the mapping periodic (`periodicity_defect = 0` in every run).

## Directory

| Path | Content |
| --- | --- |
| `time/` | Euler, RK4 and Crank–Nicolson histories for A, D, Gaussian and Sinusoidal; `*_controls.json` for half-step Euler/RK4 and a tighter C–N solve |
| `samm_periodic/` | Current fixed/adaptive comparison: `A`, `D` with uniform, frozen and moving meshes, mapped centred differences, periodic velocity |
| `samm_spectral/` | Control: the same comparison with mapped Fourier differences. The uniform member reproduces the published RK4 state to machine precision; the moving mesh then changes the error by less than 0.1 %, as expected from the `h`-refinement result |
| `samm/` | Earlier runs with the pinned-node velocity and with a lower-row transport error. **Superseded**, kept as a diagnostic record |
| `figures/` | `time_error_u`, `time_error_v`, `mesh_spacing`, `mesh_profile_A` (PNG + PDF), plotting scripts, `time_summary.json` |
| `publish.py` | Bounded replacement of Sections 4.2–4.3, 5.3–5.4, Appendix G and the navigation, with a concurrent-change hash guard |
| `validate_publication.py` | Independent check: changed-section set, figure/table counts and numbering, all 36 table entries against the recorded runs, the RK4/Table 3 identity, and the percentages quoted in the text |
| `prose_notes.md` | Earlier writing aid (kept) |
| `_scratch/` | Render helpers, section dumps and the `h`-refinement diagnostic |

## Verification performed

* `samm_spectral/A_uniform` reproduces the published natural-edge RK4 state from `time/A_time.npz`
  exactly; terminal errors agree to the last recorded digit.
* Crank–Nicolson: maximum trapezoidal residual `2.0e-14`; a `2e-15` control changes the terminal errors by
  at most `4e-13`. Halving the step moves the Euler errors towards RK4 in all four tests, which confirms
  that the Euler differences are first-order temporal effects and not improved resolution.
* Mesh runs: `J > 0`, ordered nodes, periodic mapping, relative mass drift `4.1e-8` (A) and `7.2e-10` (D),
  native reconstruction error below `1e-12`, terminal lower-row error at machine precision.
* Reductions: A `11.7 %` (u) and `17.4 %` (v); D `6.0 %` and `5.6 %`. Holding the equidistributed initial
  nodes fixed gives A `12.8 %`/`16.3 %` and D `5.3 %`/`5.8 %`, so most of the gain comes from the initial
  redistribution, with the node motion (`9.5e-4` for A, `5.2e-4` for D) changing the reductions by at most
  1.1 percentage points.

## Two defects found and corrected

1. The velocity `(qbar_i - qbar_0)/rhobar_i` used in `samm/` pins node 0 and therefore drifts: under the
   mapped Fourier operators the resulting non-periodic displacement contaminates the Jacobian. Replaced by
   the mean-flux form. Archived in `samm_spectral/diagnostic_pinned_velocity_20261025/`.
2. The lower-row transport used the scalar `vel[0]` instead of the nodal array, so the prescribed lower
   `u` trace did not follow its own node motion (error of order `|u_x|` times the displacement). Corrected
   in both scripts; the faulty runs are archived in `*/diagnostic_lower_row_bug_20261025/`.

Section 5.4 was then expanded on the user's request and trimmed again on the user's second request. Its
final discussion uses only the recorded quantities: the uniform and adaptive errors of Table 5, the frozen
control, the spacing of Figure 27, the profiles of Figure 28, and the node displacement and mass drift
already reported. A trial version that added independent diagnostics (root-mean-square reductions, node
counts and band error shares, a `(dx)^2` truncation estimate, the displacement of the exact equidistributed
mesh and the wave translation) was withdrawn; its script and numbers are kept in
`samm_periodic/not_used_in_paper_20261025/` and are not cited in the manuscript.

## Publication
`publish.py` produced the current `dlw-paper.html`: Sections 4.2 (C–N tolerance), 4.3 (moving mesh),
5.3 (three time integrators), 5.4 (fixed and adaptive meshes), Figures 25–28, Tables 4–5, the two section
introductions, the navigation entries and Appendix G. `validate_publication.py` records the result in
`validation.json`; `publication_manifest.json` records the before/after hashes.

Section 5.3 was then rewritten on the user's request so that Table 4, Figures 25–26 and their reading
alternate instead of forming separate blocks, and so that the subsection closes with what the comparison
establishes: the growth rate is set by the spatial discretization, the integrator sets the level, the level
is not a monotone accuracy order, and the growth rate changes where the interaction forms. The two error
figures were restyled (Euler orange with triangles, RK4 a thicker blue line, Crank–Nicolson a green long-dash
line on top, so the two coincident schemes remain separable) and are now separated by the paragraph that
carries the measurement over to the second field. The validator was extended to the rewritten claims.
