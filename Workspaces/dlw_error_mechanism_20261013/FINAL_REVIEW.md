# Final review — 2026-10-13

The requested experimental explanation is complete for the paper's actual PE/FD A/C implementations and stated windows. It is not a theorem asserting a universal accuracy benefit of integrability.

## Established evidence

- Independently evaluated exact-reference sources split into y model/closure, x stencil and x wrap. Source arithmetic, physical/native conversion, analytic derivatives and independent h/dx refinements are verified (`sources/validation.json`, 32 checks).
- Actual common-coordinate one-step defects plus tangent propagation reconstruct both full physical error fields. Thirteen completed field, three-source and between-method-gap closure checks pass; sixteen targeted time-step controls pass (`transport/analysis_validation.json`).
- At T=.01, exchanging source changes joint RMS by about16.84% in A and8.16% in C. Holding source fixed and exchanging propagator changes it by at most .0166% in A and .000250% in C. These are conditional linear counterfactual comparisons, justified by field closure.
- Transported sources confirm FD cancellation in A and PE cancellation in C. C u has PE y contribution1.633045e−6 versus FD .246362e−6, but opposite x-source alignment yields the smaller PE total4.351495e−6 versus FD5.298434e−6.
- A reference-defect half-amplitude intervention produces the predicted near-half nonlinear error. Full defect subtraction is explicitly only algebraic calibration, and this exact-reference diagnostic is not presented as a new practical solver.
- The adaptive prediction of C ranking reversal was fixed before the fine-grid evolution. At the same T=.001, fixed h=.1, dx=.1→.025, u PE/FD=.8212106→2.6955529; both absolute errors decrease. dt was tightened, not held fixed, and PE was checked again at half dt. Fine-grid subsampling to identical coarse coordinates preserves the ratio2.6955533.
- Shared two-field phase fits do not meet the prespecified80% squared-error criterion. A explains1.20%/3.18%, C32.67%/39.55%; phase dominance is rejected in these experiments. Residual structures are not identified as new solitons.
- Expanding A's y buffer changes the u error field by about99% of its original norm, almost entirely in the y-constant direction, while changing total RMS by less than1%. Both y boundaries move; only the instantaneous source identity isolates the lower reconstruction mechanism.
- A at T=.04 has propagation gains3.82/3.89 relative to the accumulated unpropagated source. Full-field predictor residuals remain below.26%; half dt changes actual error by less than1.61e−7. The wording is amplification becoming significant, not a proved global stability or dominant-share theorem.

## C protocol amendment

The completed C attribution uses dt=.0005, compared with the original dt=.0001 actual endpoint (relative error-field changes below2.94e−8). Earlier full four-way and source-part outputs at t=.002 are also compared against the retained fine-step checkpoint. The incomplete fine-step run is preserved and is never treated as a completed T=.01 run.

Only auxiliary three-source forcing uses five time samples with fourth-degree interpolation. The main one-step defects and tangent maps remain directly evaluated at every step. Four held-out midpoint checks give y/x source error below7.72e−8. The tiny wrap component did not pass the initial uniform1e−5 relative threshold; this failure and the revised component-specific threshold are documented in `transport/CACHE_PROTOCOL.md`. Final independent source-sum closure is below1.75e−7. Coarse-step inner wrap is exactly zero because of the finite stencil propagation distance; this is not extrapolated to the fine-step or continuous-time model.

## Independent review and corrections

- `sources/REPORT_REVIEW.md`: source algebra, ranking intervention, matching-node control and final numerical tables.
- `transport/CACHE_REVIEW.md`: physical/native forcing conversion and cache consistency.
- `boundary/CROSS_REVIEW.md`: source and update-mixture implementation.
- `boundary/REPORT_AND_TIME_REVIEW.md`: extended-time interpretation and relative-error denominators.
- Root adopted the requested wording corrections: x-only *spatial* refinement with dt control; amplification wording; explicit denominator for17%; C time-step and interpolation declarations.

## Deliverables

`report/dlw_error_mechanism_20261013.html` contains7 generated tables,6 scientific figures,44 strictly rendered offline KaTeX fragments and14 checked local references. Figures are saved as300dpi PNG and PDF, and all six PNGs were visually inspected. Refinement labels were separated and explicitly colored by method. `delivery_validation.json` records23 aggregate checks; all passed. Frozen solver SHA256 remains `4323fa90ef051a88de371c4da1f642711e5ccb128fa4e1d79be5fd6e80c30db0`.

Browser screenshot preview was not performed: the app browser rejected the local file URL under its protocol policy. No alternate browser or local-server workaround was attempted. Verification consists of the source/HTML parser, strict formula compilation, local-reference checks, quantitative figure data checks and direct PNG visual inspection. Responsive browser layout is not claimed to have been tested.

No original solver or paper edits, no new dependencies, and no file deletion. Workspace project index has one mechanism-project entry; the existing DLW research progress entry is updated rather than duplicated.
