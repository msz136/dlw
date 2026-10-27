# Continuous-reference goal: positive bound or high-frequency obstruction

2026-10-26. The user explicitly paused the persistent goal after the latest continuation. No token budget was specified. Main paper remains unchanged in this certification research round.

## Accepted target

Current A/D, Gaussian and sinusoidal backgrounds; independent u-only/v-only initial perturbations; actual continuous nonlinear solution on 0<=t<=.01. A useful finite error bound with all parameters is sufficient; it need not be tiny. Finite-grid, linearized or structured-family references do not replace this target.

## Attained results

- `INDEPENDENT_NO_GO_AUDIT.md`: independent proof audit and strengthened quantifiers. With no extra amplitude/derivative/tail cap, for every residual budget r>0 and every terminal v error M>0, compatible approximate fields preserve exact initial/boundary data and finite samples while full nonlinear residual<r. General-target result assumes a suitably regular exact target exists.
- `QUANTITATIVE_CONSTANT_BACKGROUND.md` and `quantitative_constant_background.py/json`: explicit exact-target (0,4) examples, exact nonlinear identities and 256-bit outward bounds. Includes terminal error1 with residual<1e-30 at T=.01.
- `ANALYTIC_CANDIDATE_EXTENSION.md` and `analytic_extension_checks.py/json`: entire candidate functions can preserve every specified finite value/derivative observation and have the same residual obstruction. Their analytic norms have no uniform quantitative cap.
- `ROBUST_SAME_ENVELOPE.md` and `robust_same_envelope_check.py/json`: same sin² envelope, independent physical-field direction, arbitrarily small analytic input tails, even exact finite initial sample equality. First changed boundary jet evolves exactly by backward heat and ceases to be a distribution. No solution/certificate uniform over a positive-radius ordinary C^r or analytic-strip uncertainty ball in the stated finite-jet class.
- `ACTUAL_IVP_CLASS_BOUNDARY.md`: optimized actual-sine derivative lower limit and explicit logical check that this alone cannot exclude unrestricted smooth transverse solutions.
- `fixed_data_continuation/GAUSSIAN_LINF_HOLDER_OBSTRUCTION.md`: actual Gaussian background, actual independent single-carrier directions, undifferentiated physical maximum norm. No uniform Lipschitz response along any nonzero amplitude sequence tending to zero; no all-small-amplitude Holder response with exponent above 1/2. Independent audit and symbolic/interval checks passed. This does not exclude one isolated amplitude or certify its reference.
- `fixed_data_continuation/FINITE_DARBOUX_TERMINATION.md`: all four actual perturbed data are outside finite regular standard Darboux constructions from the specified heat seeds. This is a construction-class obstruction.
- `fixed_data_continuation/TIME_PADDING_MATCHING_REDUCTION.md`: positive conditional reduction using a uniformly bounded sequence of exact mixed solutions with vanishing initial mismatch. No actual matching sequence has been verified.
- `fixed_data_continuation/rerun_base_bounds.json`: independently rerun global baseline denominator/truncation bounds and exact Laplace identities. Original pointwise evaluator samples were not rerun.

All identities rerun by root; analytic proofs independently reasoned/reviewed, not formal proof-assistant verification.

## Remaining gap and goal status

The exact prescribed single-carrier perturbed IVP still has no full existence/matching proof or physical-field error eta. No theorem excludes every conceivable structure/tail-aware method for that exact datum. The user has paused the broad goal; it has not been completed. The new theorems close specific, practically important certification information models; do not label them absolute noncomputability.

The next substantive mathematical question is fixed-data matching in a weaker transverse class, or a direct actual-data obstruction in that class. Repeating residual/refinement/precision calculations cannot answer it without a proven tail condition.

Reader entry: `../../../../report/dlw_reference_goal_20261026.html`. `STATUS.json` records manuscript hash and report validation. `publish_goal_results.py` only writes this reader report and status, preserving all manuscript bytes.
