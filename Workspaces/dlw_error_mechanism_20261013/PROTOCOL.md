# DLW error mechanism: prespecified experimental questions

Frozen before reading new experimental results, 2026-10-13.

The target is the paper's actual PE (code name SD) and FD fixed-grid soliton
computations, not a replacement periodic Hamilton experiment. Use the frozen
notebook cells from `../dlw_three_tracks_20261013/shared/solver_cells.json`.
The actual frozen x derivative and Laplacian are SECOND ORDER. Earlier reports
using a fourth-order x stencil are not the discretization analyzed here.

## Main questions and rejection criteria

1. Is error principally a phase displacement? Fit one shared phase to both
   physical fields in A, and the two Gram phases in C, using equal nondimensional
   field weights. Report squared-error fraction explained, linear orthogonal
   decomposition and nonlinear fit, at all 21 stored times. Call phase dominant
   only if at least 80% of joint squared error is explained at the terminal time;
   otherwise reject that explanation for the selected case/method. A fixed
   smaller window is a sensitivity check, never a replacement primary outcome.
2. Can an independently computed local defect and tangent propagation predict
   the actual physical error? Compute the actual RK4 map in common physical
   coordinates (p=delta_y u, v), local one-step defects on the exact reference,
   and its tangent map. Require relative terminal vector discrepancy <5% and
   field correlation >.99 for quantitative linear attribution. Report failures
   and nonlinear remainder, rather than choosing another favorable case.
3. Is the PE/FD difference mainly source injection or propagation? Cross both
   local defects with both tangent propagators (four predictions). Compare per
   physical field and joint RMS. Also propagate zero-order accumulated sources
   without tangent maps to quantify transport/amplification and directional
   changes. Do not infer terminal ranking from local residual norms alone.
4. Where do the sources originate? Split exact-reference physical RHS residuals
   into y-model residual using analytic x derivatives, interior x-stencil error,
   and x-boundary wrapping error, retaining the y reconstruction/closure.
   Test h and dx separately and preserve signed vector cancellation. The agent's
   sources/PROTOCOL.md specifies fixed snapshots and refinement levels.
5. Does manipulating the identified source have the predicted effect? On A,
   cancel fractions lambda=0,.5,1 of the independently computed reference local
   defect. Lambda=1 is only an algebraic calibration. The lambda=.5 response
   tests the linear error model; no claim of a usable exact-solution-free method.
6. Does the specific PE update correction produce a privileged accuracy optimum?
   Define the common-coordinate map
   Psi_lambda=(1-lambda)Psi_FD+lambda Psi_PE, lambda=0,.25,.5,.75,1.
   Starting from the identical physical initial state, compare A/C at T=.01,
   dt=.0001, the original computational domains and observation windows.
   Endpoints must reproduce the original methods. Intermediate maps are a
   numerical intervention, not proven nonintegrable systems. No best lambda
   is to be presented as universal or tuned for an unseen case.

## Causal interpretation

The interventions isolate identifiable differences between these two actual
updates, and distinguish source from propagation. They cannot by themselves
identify an abstract treatment called integrability: the finite-x, finite-time,
open-boundary solver has not been proved to retain the complete Lax hierarchy.
The report must state a concrete mechanism with measured support and refrain
from attributing any remaining difference to integrability merely by label.

## Shared checks and deliverables

- Original soliton reference, initial data, domains, time, and observation norms
  retained; no fitted terminal data enter the error predictor.
- Original solver/notebook files are read only. No files deleted.
- Endpoint regression, tangent derivative verification, time-refinement and
  source/parameter controls targeted to the experiments actually performed.
- Save protocols, scripts, CSV, exact field arrays needed for review and a
  compact validation record. Scientific figures use existing plotting packages,
  300 dpi PNG and PDF, and the established quiet panel style.
- Final user report is `report/dlw_error_mechanism_20261013.html`.
- Update existing DLW research progress entry; register this independent error
  mechanism project once, not every product in the workspace index.
