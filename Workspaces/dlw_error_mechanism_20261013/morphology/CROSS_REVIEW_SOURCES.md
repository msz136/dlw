# Independent read-only review of source attribution

2026-10-13. Reviewed `sources/PROTOCOL.md`, `common_sources.py`, baseline
metrics/correlations, algebra/identity tables, jet validation and A/C validation
records. No source experiment was rerun or modified.

## Assessment

The decomposition is consistent with the actual common physical coordinates:
the SD conversion includes v_t=w_t+delta0(u_t), the prescribed lower trace and
the derivative of upper error extrapolation. The three vectors are formed by
telescoping differences at the same reference state, so their signed sum
equals the actual RHS defect. Recorded discrepancies in this sum are below
9e-19; reconstructed native RHS discrepancies are at most 2.67e-11 across the
refinement/buffer matrix. The explicit SD−FD identities also close to numerical
precision. Exact tau derivative formulas have the correct cumulant orders:
u_xx uses a third cumulant, v_xx uses kappa(x,x,x,y), and v_t uses
kappa(x,y,t). Direct u/v reference differences are at most 2.91e-14.

The source direction findings are substantive. At t=0 in the original
observation window, y-model and x-stencil cosines are:

| Case | Field | SD/PE | FD |
|---|---|---:|---:|
| A | u | +0.327887 | -0.853772 |
| A | v | +0.058404 | -0.978294 |
| C | u | -0.578355 | +0.865963 |
| C | v | -0.427137 | -0.775766 |

Thus the sign and effectiveness of source cancellation differ across A/C;
their norms alone cannot determine the combined source. This is a specific,
testable explanation for why the PE/FD accuracy ranking changes across cases.
The source-to-terminal link still requires the separately computed transport
closure and source interventions.

## Interpretation requirements for synthesis

1. Keep the name **y-model with prescribed closure**. It is not the local
   truncation defect of a boundary-free y PDE and is not an isolated causal
   treatment called integrability.
2. Do not treat component RMS values as additive percentages. Add signed
   vectors or include cross terms and their cosines.
3. An instantaneous x-wrap vector equal to zero in the interior does not
   prove zero boundary influence after propagation. Use propagated components
   and buffer controls for that conclusion.
4. These are RHS defects (error rates). The transport primary sources are
   actual one-step map defects. Passing between them requires the stated time
   quadrature/closure check.
5. Tangent prediction requires verification against the actual numerical error
   before counterfactual source/propagator swaps receive quantitative causal
   interpretation.

No blocking mathematical inconsistency was found in the reviewed source code
and recorded checks. Transport production outputs were not yet complete at
the time of this review, so no claim about their terminal closure is made here.
