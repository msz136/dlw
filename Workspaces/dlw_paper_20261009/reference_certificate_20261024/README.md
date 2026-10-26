# Nonexact-data reference certification

Date: 2026-10-24. **New nondegenerate pure sine/Gaussian benchmarks are available; original zero-background data remain unresolved.** This branch answers the request to build a computable reference error bound below 1% of the measured numerical discrepancy. It is separate from the finished four-soliton rerun and does not replace manuscript tables.

## Latest: pure profiles with a nonzero Endpoint v leading defect

[nondegenerate_benchmarks/PROOF.md](nondegenerate_benchmarks/PROOF.md) constructs u0=A sin(pi*z/4)F and **v0=4-3u0_z**, A=.03 sine / .05 Gaussian width6, period192 and T=.01. The factor -3 relation holds only initially. A Laplace-transformed heat construction yields the full DLW solution, with globally nonzero denominators, applicability of the existing strong-class uniqueness proof, uniform physical truncation bound <1e-40, and 320-bit Arb point enclosures (successful returns have radius <1e-50). This is a self-reviewed proof with symbolic/interval checks, not formal or external verification.

The Endpoint initial v coefficient is -4u0_z*u0_xz, nonzero. Calling the existing stencil on four h levels gives final observed orders .999957 (sine) and .998754 (Gaussian); remainder after subtracting hC is second order. This is an initial-rate test, not evolved error. [Readable report](../../../report/dlw_nondegenerate_reference_20261024.html), evaluator/certificate and stencil records reside in the new branch directory. Earlier statements that no suitable new parameter set was available are superseded by this construction. The original zero-background IVP goal is not completed by changing data.

## New user-approved preliminary branch: compatible sine/Gaussian data

**Error-analysis restriction (2026-10-24):** the user requires pure Gaussian/sine data with a nonvanishing target leading defect. Both v=4±u_y branches identically cancel the Endpoint v O(h) coefficient. These are therefore special degeneracy benchmarks, not suitable main examples for that coefficient. [Suitability audit](compatible_benchmarks/ERROR_BENCHMARK_SUITABILITY.md) verifies this and nonzero coefficients for the original independent-field data, whose positive-time reference remains unresolved. Rational trigonometric profiles do not meet the user's pure-shape requirement.

The user permits choosing the second field compatibly. [compatible_benchmarks/PROOF.md](compatible_benchmarks/PROOF.md) gives concrete sine/Gaussian u0 with v0=4-u0_z, an exact forward Burgers/heat construction, strong-class uniqueness through the existing theorem, and full-domain truncation bounds (each field <1.327e-60 sine, <4.680e-38 Gaussian). `compatible_benchmarks/reference.py` provides 256-bit Arb point evaluation including rounding, with returned ball radius <1.01e-32; `certificate.json` and `check.json` record bounds and checks. Self-reviewed proof, not formal/independent verification. [Readable report](../../../report/dlw_compatible_reference_20261024.html). Original initialization is different and its goal is still active.

The preceding spectral investigation is recorded in [BLP_STRIP_COMPATIBILITY.md](BLP_STRIP_COMPATIBILITY.md): the free top boundary balances transverse moments; whole-plane spectral conditions cannot simply be transferred to the strip. No original-data existence conclusion follows from that investigation.

## Current goal progress: original-IVP uniqueness and injective matching map

[INITIAL_VALUE_UNIQUENESS.md](INITIAL_VALUE_UNIQUENESS.md) supplies a self-contained weighted-energy proof of initial-value uniqueness for the explicitly stated strong-solution class, without high-order transverse regularity. The full difference has an indefinite selfadjoint second-order principal part plus bounded first-order coefficients; a decreasing convex time weight absorbs those coefficients. The proof covers the analytic-x mixed solutions from the previous round. Thus F is injective: the exact initial matching value, if it exists, is unique. Existence/range and physical error bounds remain unresolved.

`uniqueness_energy_check.py/json` checks the energy identity, absorption squares and uniform constants; `mixed_bvp_check.py/json` additionally verifies mean-compatible terminal data by replacing only the candidate zero mode with the exact conserved original mean. Sinusoidal period-24 invariance now follows conditionally from original-IVP uniqueness. These do not establish existence or stability. The goal remains active; all new proofs remain self-reviewed rather than independently/formally verified.

## Previous goal progress: mixed-time existence and exact initial matching

[MIXED_BVP_EXISTENCE.md](MIXED_BVP_EXISTENCE.md) proves a constructive auxiliary result for the FULL nonlinear equations with prescribed a(T)=g and the exact b(0)=b0. In the analytic-x Wiener trajectory norm with rho=.1, datum norm <=.15 gives a unique solution in radius .7. The transverse Volterra inverse is bounded by exp(16 sqrt(T/2)); the fixed-point image is <.680 and the contraction factor <.614. Both existing candidates provide terminal data satisfying the theorem; 256-bit bounds are in `mixed_bvp_check.py/json`.

This is not a replacement initialization. The original problem still requires solving F(g)=a0, where F maps the terminal datum to the initial a of the uniquely defined mixed solution. Smooth terminal candidates produce analytic-y mixed solutions and cannot exactly match the prescribed original data, conditional on the prior regularity obstruction proofs. General continuous-y terminal data are not excluded. Original-IVP uniqueness is now supplied by the continuation above; existence and a physical reference error bound remain unestablished. The active goal remains incomplete.

[Latest reading report](../../../report/dlw_reference_matching_20261024.html). Next work is the range of the now-injective F in a lower-y-regularity class, not more finite refinement. New proofs are self-reviewed, not independently or formally verified.

## Previous conclusion: no residual-only precision guarantee with exact initialization

[RESIDUAL_NO_GO_CLOSURE.md](RESIDUAL_NO_GO_CLOSURE.md) proves a new full-nonlinear obstruction: around any sufficiently regular exact target, approximate fields can preserve its entire initial data and lower boundary, have uniform physical PDE residual tending to zero, and retain a fixed terminal maximum error in v. The perturbation can lie in any open interior y interval and avoid any finite set of grid points. Thus no residual-to-error modulus tending to zero exists without additional quantitative regularity or tail constraints. This is not a construction of two exact solutions and does not prove that every future structural certificate is impossible.

The algebra and explicit numerical bounds pass `residual_no_go_check.py/json`. In addition, `no_go_candidate_bounds.py/json` proves six required background bounds below 1 for explicit, exact-initial baselines constructed from BOTH existing candidates. Around them, terminal v differences of 1e-3 coexist with full residual differences below 1.77e-77. These are residual differences, not certified errors or residual bounds of the baseline itself.

[Reading report: the closed negative result](../../../report/dlw_reference_no_go_20261024.html). The proof is self-reviewed with symbolic/Arb checks, not newly independently reviewed or formalized. Same-method finite refinement and smaller ordinary residuals cannot complete certification. The exact low-transverse-regularity existence/uniqueness problem remains open; eta_u/v remain null. Reopening requires genuinely additional proven structure or quantitative regularity/tail information.

## Previous continuation: explicit Gaussian obstruction constants

[GAUSSIAN_EXPLICIT_OBSTRUCTION.md](GAUSSIAN_EXPLICIT_OBSTRUCTION.md) rechecks the Gaussian boundary-jet argument and supplies an explicit uniform bound for all potentially cancelling tree terms. At m=900 and t=1801/180200, its positive lower bound has C>exp(-12265), while the subtraction has D<exp(26000). At original-period Fourier index 4,505,000 the conditional normalized jet coefficient exceeds exp(97000). This is a high-derivative obstruction, not a physical-field error lower bound. The derivation has been reviewed in this session, not independently or formally verified. `explicit_obstruction_check.py/json` validates the constants with 256-bit Arb.

Reading report: [reference candidates and theoretical obstruction](../../../report/dlw_reference_theory_20261024.html). The original initial data remain unchanged. Candidate evaluation was rerun successfully; eta_u/v remain null. Existence, uniqueness and tail control in a lower transverse regularity class remain unresolved, so the requested certified full-field reference has not been obtained.

## Previous continuation: true tails and Gaussian transverse regularity

[TAIL_ESTIMATE_CONTINUATION.md](TAIL_ESTIMATE_CONTINUATION.md) records the new derivations. The initial combined tail is zero for the sinusoid and below 2.63e-72 for the approved periodic Gaussian at the selected cutoffs. A conditional estimate closes the forward-diffusive b=u_y-v tail in terms of the unresolved backward-diffusive a=u_y+v tail and the retained-mode error. It does not establish a small total tail or a continuum certificate.

Section 5 gives a **new, not independently reviewed proof draft for the actual periodic-Gaussian data**. The exact lower-boundary transverse-derivative hierarchy has a finite Duhamel expansion at each derivative order. At order 900, a positive 901-Gaussian-factor contribution forces super-polynomial Fourier growth at t=1801/180200<.01; possible negative contributions and lower-factor terms are bounded separately. If the proof is confirmed, it excludes solutions retaining all transverse derivatives on any positive closed time interval. It does **not** exclude lower-transverse-regularity classical or weak solutions and does not give a physical-field error lower bound.

The next step is independent mathematical review of that draft, followed by a clearly specified weaker solution class if the original initial data are retained. Only the earlier sinusoidal result has the independent review cited below. Candidate data, manuscript tables and HTML reports have not been relabeled as certified.

## Latest proof audit: two routes excluded

`TAIL_MAJORANT_REVIEW.md` proves that the proposed positive Fourier envelope (R2) cannot be summable when any nonzero-frequency error or residual seed is present, however small. The nonlinear harmonic cascade followed by backward diffusion forces an unbounded sequence of envelope coefficients. The R2 search is therefore retired; it is not merely awaiting better constants.

`ACTUAL_DATA_REVIEW.md` proves, for the actual sinusoidal data, a quantitative lower bound on all lower-boundary y derivatives at positive time, conditional on sufficient smoothness. It excludes uniform finite-order Gevrey-y regularity, including an analytic-y solution class. `ACTUAL_DATA_INDEPENDENT_REVIEW.md` independently checks the argument and its scope. This prevents assuming geometric/stretched-exponential Chebyshev tails for the true sinusoidal solution. It does not prove classical nonexistence or a lower bound on the candidate's physical error. That earlier review did not establish a Gaussian counterpart; the separate new Gaussian draft and its unreviewed status are described above.

The requested numeric eta_u, eta_v remain unknown. The finite candidates and their observed agreement are unchanged. A cancellation- or structure-based existence and error theorem for these specific data has not been obtained; neither a generic residual bound nor more finite refinements closes the gap.

`COLE_HOPF_BVP_REVIEW.md` checks the structural alternative. The transformed system admits a stable two-time integral formulation with terminal q and initial r, but recovering these prescribed initial fields requires an exact infinite-dimensional compatibility equation for the terminal q. It is not solved or enclosed here. Factorial tails in initial q alone are not a nonexistence proof, since the coupled potential can alter their evolution. This review also supplies no eta.

## Latest continuation: exact boundary certificates and approved Gaussian change

The user explicitly selected the smooth periodic Gaussian sum G_per=sum_m exp(-((x+192m)/6)^2). This supersedes the literal truncated-periodic Gaussian as the intended future Gaussian target. Old runs retain their original meaning and are not relabeled as new-data runs.

`BOUNDARY_THEOREM.md` derives exact nonlinear boundary traces. For p=u_y and b=v at the zero-u lower boundary, p+b satisfies backward heat/advection and p-b forward heat/advection. This proves a trace-class obstruction for the OLD Gaussian (Fourier n^-2 tail); it does not establish the new nonlinear interior solution. For sinusoidal data the boundary trace is explicit. Arb verifies the old finest FD reference's boundary error lies in (4.2267e-8,4.2269e-8). This refutes a full-domain 1e-10 upper bound for THAT candidate; the historical interior-only evaluation domain is not covered by this lower-bound argument.

`boundary_certificate.py/json`: exact sinusoidal boundary sample representation error <1e-72. `periodic_gaussian.py` and `periodic_gaussian_certificate.json`: new Gaussian definition and exact boundary formula, omitted Gaussian sum error <1e-998, sample representation error <1e-80. These are rigorous BOUNDARY evaluation bounds only. Neither is eta for an interior reference. Full nonlinear existence/tails remain unresolved.

Reading report: `../../../report/dlw_reference_certificate_20261024.html`.

## Latest full-field attempt

User explicitly requested the second task: continuous full fields at T=.01 with a provably small reference error. `canonical_reference/` now contains 11 independent Fourier-Galerkin/Chebyshev runs, full trajectory coefficients, evaluation code, and refinement/independent DOP853 checks. It uses the exact nonlinear integral formulation, without the old FD ghost closure. The Gaussian initial coefficients represent the approved periodic sum. Latest reading report: `../../../report/dlw_continuum_reference_20261024.html`; rebuild with `build_full_report.py`.

The selected candidates have eta_u=null, eta_v=null, certificate=false. Refinement differences at about 1e-15 and sampled PDE residuals about 1e-12 are observations, not continuum bounds. Independent reviews in `INTERIOR_EXISTENCE_REVIEW.md` and `CERTIFICATE_ROUTE_REVIEW.md` give exact nonlinear forward/backward decomposition, an interior (not boundary-only) high-frequency obstruction, and the now-retired envelope conditions R2 with conditional physical bounds R3. The generic analytic-data nonlinear counterexample uses different v initial data; it must not be described as nonexistence for the requested cases. The user's certified-reference objective remains incomplete; the main paper is unchanged.

## Results and scope

- `THEORY.md`: exact nonlinear integral reformulation using w=v-u_y (no upper-y ghost); conditional scalar residual theorem and field-norm reconstruction requirements; exact Endpoint linear stability obstruction; literal periodic Gaussian derivative jump.
- `certificate.py`: outward Decimal arithmetic for the conditional tube bound. Analytic hypotheses/residual enclosure are not validated by this calculator. `continuum_certified` remains false.
- `audit.py`: eight nonlinear FD float64 runs at h=.1, T=.01, a=2. dx=.1/.05/.025; at dx=.05 also halve dt=1e-4. Original full period-192 interval, unchanged old closure. Hermite midpoint residuals are sampled ODE diagnostics, not rigorous enclosures or full PDE residuals. Threshold stops are not physical blowup times.
- `precision_probe.py`: sinusoidal nonlinear FD at 50 and 80 decimal digits, dx=.05, dt=1e-4, on the exact period-24 invariant subspace. No filter or altered differential equation. Acb/arb radii are deliberately discarded; these are arbitrary-precision point trajectories, not interval certificates. Coarse dx=.5, dps=30 agrees with the independent full-domain float64 solver to 9.72e-17. High-precision decimal final fields are saved as txt, float64 plotting/comparison copies as npz.
- `summarize.py`: symbolic eigenpair checks, numerical comparisons, precision comparison from decimal strings, validation.json and HTML. All assertions and observation labels distinguish certification from agreement.

Windows numpy.longdouble is float64 here. The optional `audit.py CASE extended` branch detects this and refuses to pretend it is higher precision. python-flint was installed for real arbitrary-precision arithmetic.

## Reproduce

From workspace root:

```
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/audit.py Gaussian
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/audit.py Sinusoidal
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/precision_probe.py 50
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/precision_probe.py 80
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/precision_probe.py 30 0.0001 0.5
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/precision_control.py
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/certificate.py
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/boundary_certificate.py
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/periodic_gaussian.py
python Workspaces/dlw_paper_20261009/reference_certificate_20261024/summarize.py
```

Existing individual run results are reused, not overwritten. Source: the frozen `../spatial_audit_20261023/run.py` nonlinear FD solver. The main manuscript is unchanged in this branch.

Actual result: 50/80 digit trajectories differ by 1.09189e-35 at the final time; maximum u remains about .03. On the same period-24 domain float64 reaches max u=.28422, while the original full-domain float64 reaches 2.76785. Thus changing the domain symmetry alone does not eliminate the observed precision sensitivity. These agreements/differences are NOT error bounds to the continuum solution.

## Remaining proof obligations

1. Establish the nonlinear initial-boundary problem's existence and stability in a specified function space for the actual periodic initial data.
2. Bound unresolved x modes (and y approximation) over the full interval. The fixed-cutoff ordinary norm bound is not uniform in x resolution. The Endpoint linear result does not prove nonlinear nonexistence for the two chosen data.
3. Enclose full space-time residuals, initial representation and boundary errors, including physical v reconstruction, using validated arithmetic/estimates.
4. Only then compute eta and test eta<=.01 D for EACH field and method; no current data record passes a continuum certification gate.

Next useful work is a tailored high-frequency tail/stability proof for the exact integral formulation with the NOW APPROVED periodic Gaussian and the original sinusoid. More finite-dimensional runs alone cannot discharge that condition. The periodic-Gaussian change is authorized; no regularization, filtering, or other boundary change is authorized or silently introduced.

## Compact matching criterion (2026-10-24)

`COMPACT_MATCHING_CRITERION.md` connects mixed existence and IVP uniqueness: a uniformly bounded analytic-x, Lipschitz-z terminal sequence with certified initial mismatch tending to zero converges to the unique original solution. A positive mismatch gap excludes only the specified compact class. Neither the required uniform bounds nor an actual mismatch sequence/gap is established. Physical transfer constants are <16.051258 for u and <4.012815 for v per unit terminal error; terminal error remains unknown, eta remains null.

## Quantitative conditional error modulus (2026-10-24)

`CONDITIONAL_ERROR_MODULUS.md` extends the weighted uniqueness argument to nonzero residual, with explicit spacetime-L2 and full physical sup-norm bounds under stated solution-size and Lipschitz hypotheses. `conditional_error_check.py/json` verifies the algebraic absorption and 256-bit constants. With c1=20,c0=13 the resulting residual threshold is below 10^(-6.2 billion) even for a unit bound on one term: this particular coarse estimate is not a practical validator. No actual-error lower bound or original-IVP nonexistence follows. Existence and a priori bounds remain unproved; eta remains null.

## Transverse analyticity bridge audit (2026-10-24)

`TRANSVERSE_ANALYTICITY_BRIDGE.md` proves intermediate-time transverse analyticity for bounded homogeneous backward-heat solutions with analytic transverse initial data, using Fourier–Chebyshev coefficient interpolation. It cannot yet be transferred to the nonlinear DLW system. An explicit positive-q example satisfies the backward q equation, the primitive constraint, zero-mean potential and analytic initial q,r, but loses transverse C2 regularity; its forward-r equation has a verified nonzero defect. Thus the full r evolution is essential to any such transfer. `transverse_bridge_check.py/json` checks these identities. Original-IVP existence/nonexistence and eta remain unresolved.

## Exact BLP mapping and spectral literature lead (2026-10-24)

`BLP_SPECTRAL_ROUTE.md` gives the exact moving-frame map U=-u/2, P=(v-u_z-4)/4 to BLP and transforms both original initializations without changing the domain or boundary. A maximum-principle argument keeps P strictly negative for any existing bounded classical solution. `blp_route_check.py/json` verifies the residual equivalence and 256-bit bounds. The directly relevant Garagash–Pogrebkov 1996 Cauchy/IST paper was identified (DOI 10.1007/BF02072003; Russian DOI 10.4213/tmf1219), but only its abstract was read: public full-text retrieval failed. Its scattering conditions and applicability to the periodic strip remain unverified. Neither final goal branch is achieved.
