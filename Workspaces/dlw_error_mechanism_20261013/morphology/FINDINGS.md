# Actual DLW error is not predominantly a common phase displacement

2026-10-13. Computation complete; archived PDE trajectories are unchanged. This
note reports the prespecified phase-only test, not a new PDE experiment.

## Primary conclusion

The hypothesis that a common phase displacement explains at least 80% of the
joint physical squared error is rejected for **both methods in both A and C**.
This remains true in the prespecified central window and at every saved nonzero
time. A has only 1.20%–3.18% explained error at the terminal time in the full
window; C has 32.67%–39.55%. Therefore the previous suggestion that the observed
error is mainly a displacement, hiding substantially better PE waveform
preservation, is unsupported by these actual short-time trajectories.

Here PE is the paper's integrable semidiscrete route, named `SD` in the frozen
code and CSV files. These computations do not assert that the completed
finite-x, finite-time and open-boundary update retains a Lax hierarchy.

## Experimental definition

At each of the 21 original times, use the native nodes and the continuous Gram
reference at the same physical time. Change only additive subset phases in
both tau functions: one phase for A and two for C. All spectral parameters,
coefficients, rates and gamma values stay fixed. In C the two independent
phases are exactly equivalent to a common x/y translation of the two-wave
pattern. Fit the same phase to **both physical fields jointly** by minimizing

\[
J(\theta)=\operatorname{mean}(u_{\rm num}-u_{\rm exact}(\theta))^2
          +\operatorname{mean}(v_{\rm num}-v_{\rm exact}(\theta))^2.
\]

Thus the norm uses equal nondimensional u/v weights; it does not separately
align each field, normalize by field variance, filter, interpolate or crop
after seeing the results. The main windows are A: |x|≤5, |y|<5 and C: |x|≤30,
|y|<30. The independently specified sensitivity windows halve these extents.
The fit is a nearby phase fit in [-0.25,0.25] per phase; all solutions are far
from the bounds. The claim is not a global theorem about arbitrary translations.

For an exact additive error budget, also project the joint physical error
orthogonally onto the phase tangent space at zero phase. Its squared norm
satisfies E_total = E_phase + E_nonphase. Independently fit the nonlinear
reference to check that linearization does not materially change the result.

## Terminal results at t=0.01

| Case/window | PE phase-explained squared error | FD phase-explained squared error | PE/FD raw joint RMS | PE/FD aligned joint RMS |
|---|---:|---:|---:|---:|
| A/full | 1.19734% | 3.18186% | 1.168253 | 1.180165 |
| A/central | 1.54198% | 3.63930% | 1.167599 | 1.180237 |
| C/full | 32.66791% | 39.55176% | 0.918356 | 0.969238 |
| C/central | 36.70501% | 46.65459% | 0.943860 | 1.028119 |

Joint RMS is sqrt(RMS_u² + RMS_v²). Fractions above use squared error, not
RMS reduction. Full-window RMS reductions after fitting are respectively
A/PE 0.6005%, A/FD 1.6038%, C/PE 17.9439% and C/FD 22.2515%.

Interpretation:

- A: aligning the waves does not remove PE's disadvantage. PE has 16.83% larger
  raw joint RMS and 18.02% larger aligned RMS. Its phase component is smaller
  than FD's, but the increase in its non-phase component is substantially larger.
- C/full: PE has 8.16% lower raw joint RMS but only 3.08% lower aligned RMS.
  The **orthogonal linear budget** attributes 76.62% of the FD-minus-PE total
  squared-error difference to the smaller phase component and 23.38% to the
  smaller non-phase component. These percentages describe the difference
  between methods, not the composition of either method's total error.
- C/central: PE's 5.61% raw RMS advantage becomes a 2.81% aligned RMS
  disadvantage. Its phase-component advantage is 127.88% of its raw squared
  error advantage, with the non-phase component offsetting part of that gain.
  Thus a claim of uniformly better shape preservation would fail the declared
  window sensitivity check.
- The non-phase residual is what a common translation cannot explain. It is
  not by itself a proven radiation field, amplitude change, ghost soliton,
  solitary deformation mode or deviation normal to the full soliton manifold.

One physical field can worsen after a joint fit. For example A/PE u RMS grows
from 1.45980e-4 to 1.61602e-4 while v RMS decreases from 3.21963e-4 to
3.12024e-4. This is an expected consequence of the declared shared-phase
objective and must not be described as independent u/v best alignment.

## Time dependence and robustness

Over all 20 nonzero times (0.0005 through 0.01), nonlinear phase-explained
fractions remain in these ranges:

| Case/method | Full window | Central window |
|---|---:|---:|
| A/PE | 1.1973%–1.2286% | 1.5420%–1.5711% |
| A/FD | 3.1819%–3.2530% | 3.6393%–3.6942% |
| C/PE | 32.6679%–32.6801% | 36.6754%–36.7050% |
| C/FD | 39.5518%–39.5785% | 46.6472%–46.6546% |

The decomposition changes little through this short interval. At the terminal
time the PE half-dt archives change the explained fractions by at most
2.05e-12 (absolute fraction) and aligned RMS by at most 8.21e-12 relatively.
Time-step contamination cannot account for the observed conclusion at the
tested step sizes. This is not a spatial-convergence or long-time claim.

## Fit and data audit

`validation.json` contains 1054 passed checks and 172 result rows. Eight
initial frames at roundoff are excluded from fraction interpretation; the
remaining 164 nearby fits all converge, with no bound contact. The largest
fitted phase magnitude is 1.576e-4 against the bound 0.25. Tangent condition
numbers are 1 for A and at most 3.40845 for C. The maximum relative Pythagoras
residual is 1.48e-15. Analytic phase derivatives are checked against independent
centered differences, zero-phase fields against archived references at all
times, and final objectives against inherited Exact.uv evaluations.

Two starts give objectives agreeing to 2.92e-11 of the raw squared error. The
largest normalized final gradient is 3.18e-7, while the maximum difference
between nonlinear and linear explained fractions is 6.80e-7. Thus neither
phase ill-conditioning nor the optimizer's finite tolerances can explain the
large gap to the prespecified 80% threshold. Linear projection also supplies
an optimizer-independent check.

The protocol, script and six input archive SHA-256 hashes have been rechecked
against the completed validation record. `phase_only_budget.png` was viewed:
labels, full/central distinctions and the near-constant fractions match the
CSV values. Initial undefined fractions are omitted.

## Implication for the combined error mechanism study

Phase fitting rejects one proposed dominant explanation; it does not identify
the physical origin of the remaining error. The independent source and tangent
transport experiments should explain that non-phase majority and test whether
PE/FD differences are produced by their defect injection, propagation or both.
Do not use this result to relabel all residual as shape distortion or to infer
that abstract integrability itself causes either advantage or disadvantage.

## Outputs

- `PROTOCOL.md`: frozen local protocol; project parent protocol fixes 80% criterion.
- `phase_decomposition.py`: reproduction of phase diagnostics from saved fields.
- `fit_timeseries.csv`, `endpoint_summary.csv`, `method_comparison.csv`:
  full trajectories, terminal budgets and paired method comparisons.
- `fit_start_diagnostics.csv`, `validation.json`: optimization and numerical checks.
- `*_final_decomposition.npz`: signed field errors, phase tangents and components.
- `phase_only_budget.png` / `.pdf`: six-panel comparison.
