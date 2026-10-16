# Stage-2 scientific review

2026-10-13. Three independent track authors plus root integration review.

## 2A

Root rederived the reduced M=2 physical Hamiltonian and traveling-profile ODE.
An independent SymPy script (`verify_synthesis.py`) checked the elliptic profile
against both first-order ODEs using the quartic curve and the velocity relation.
The full proof was read: periodicity, zero means, injective amplitude/phase
parameterization, inherited original symplectic form, nonzero momentum
derivative, explicit small interval, and one-degree-of-freedom integral count.
The Euler–Lagrange meaning of density derivatives was clarified during review.
The contour elliptic curve is not identified with the original Lax spectral
curve. The transverse alternating mode has a restricted continuous-limit
regime, explicitly recorded in the proof.

## 2B

Root manually differentiated one actual Newton correction, including the
Jacobian derivative and the Hessian symmetry that yields the h/4 term.
The analytic vector-field derivatives, fixed-leaf embedding, Poisson weights,
physical inverse differential and pulled-back symplectic-defect identity were
checked against the implementation. Track 2C independently repeated this
scientific review; see `error_lax/cross_review_symplectic.md`.

The report distinguishes the exact midpoint map from a finite stopping branch,
and distinguishes short-time physical accuracy from symplecticity. The two
plots were visually inspected by their author and root. A source-escaping issue
in the Markdown was corrected; strict KaTeX rendering subsequently passed.

## 2C

Root verified the Darboux defect sign, the intermediate-potential mismatch,
the matrix commutator defects, and the inverse-monodromy normalization. The
coefficient-level product defects are retained in addition to operator-level
commutator anomalies. Track 2A independently reviewed the h² sampling terms,
spectral trace prefactor and conditional bounds; see
`reduction/cross_review_error_lax.md`.

A missing plus sign in the first displayed residual definition was corrected.
The nonlinear error system is exact, but the error variable alone is not
declared autonomous or isospectral. Formal PDO traces, finite matrix traces,
and analytic trace-class estimates retain their distinct assumptions.

## Synthesis

Track 2A reviewed `synthesis.md`. Its orbital bounds apply only to two trajectories
inside a compact regular portion of the proven invariant annulus. The forced
coordinate bounds explicitly require a valid reduced model; they are not
applied to unrestricted numerical trajectories. An independent exact check
verified that phase shear can preserve the two-form while increasing distance.

The delivery validator checks saved certificates, source hashes, document
links, math rendering, tables and image integrity. It does not claim browser
layout testing, general-field stability, or a multi-degree-of-freedom Liouville
theorem.
