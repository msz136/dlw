# Independent review: report wording and A time evolution

Read-only review of `report.source.html`, `transport/common.py`,
`run_transport.py`, the derivative validation, original-time-step and half-
time-step A .04 outputs. No reviewed scripts or template were changed.

## Verified evidence

1. The common-coordinate update includes the time-dependent physical output
   conversion. Its analytic tangent differentiates all four RK4 stages, not
   merely the RHS at the start. The recorded complex-step checks give
   relative L-infinity differences of 1.46e-15 (PE) and 8.96e-17 (FD).
2. The one-step defect is evaluated on the independently known reference,
   and the tangent predictor uses this defect and reference-stage derivatives.
   Actual terminal errors are used only for evaluation. The primary closure
   is therefore a predictive field comparison rather than an endpoint fit.
3. At t=.04, joint relative field residuals are PE .00258388 and FD .00217351;
   field cosines exceed .999997. This supports the stated accuracy of the
   linear attribution in the observed window.
4. Transported/unpropagated source-sum norm ratios grow from 1.03447/1.01624
   at .01 to 3.81876/3.89483 at .04. Their late cosines are only .27696/.24715,
   so the change includes a substantial spatial-direction change. A norm
   ratio alone would miss that second effect.
5. Actual joint RMS grows from 3.53511e-4 to 5.21657e-3 for PE, and from
   3.02598e-4 to 4.63369e-3 for FD. The unpropagated sums grow about fourfold,
   from 3.41731e-4 to 1.36471e-3 and 2.97762e-4 to 1.18913e-3 respectively.
   Increased source accumulation and increased propagation gain both matter.
6. Halving dt changes the actual terminal field by only 1.26e-7/1.60e-7
   relatively. Predictor changes are 4.61e-6/3.89e-6. Thus the observed large
   late amplification is not caused by the particular chosen time step
   within this refinement test.

## Wording recommendations

- The report appropriately limits its mechanism to the actual PE/FD routes,
  specified cases, closures and windows. It does not infer an integrability
  theorem from the advantage of one endpoint. Preserve this distinction.
- Replace the section 8 heading "传播开始主导增长" with "传播放大变得显著".
  The data directly establish increasing propagation gain; "主导" would
  introduce an additional attribution convention because source accumulation
  also grows and the factors combine multiplicatively.
- In the statement of about 17% field difference at .01, specify that the
  denominator is the unpropagated source-sum norm. This is how `C.compare`
  computes that particular comparison.
- This is evolution over the extended tested interval .01 to .04, not a
  general long-time stability result. Keep .04 and the fixed grid explicit.
- A ridge in the new field figure is not spectral evidence of a soliton.
  The current template correctly avoids making that identification.
- The y-domain experiment expands both endpoints. The report correctly
  distinguishes this full evolution intervention from the initial-source
  identity locating the lower-trace cumulative reconstruction contribution.

No blocking mathematical inconsistency was found in these reviewed parts.
The figure independently recomputes single-field v metrics and verifies the
stored CSV values; it supplies a direct spatial check accompanying the scalar
time-evolution curves.
